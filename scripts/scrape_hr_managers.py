"""
East Texas — Corporate HR Manager Contact Scraper
Coverage: Smith County (Tyler) + surrounding counties
  Cherokee (Jacksonville), Gregg (Longview), Henderson (Athens),
  Van Zandt (Canton), Upshur (Gilmer), Wood (Quitman), Rusk (Henderson)

Sources:
  1. Tyler Area Chamber of Commerce member directory
  2. Longview Chamber of Commerce member directory
  3. Jacksonville Chamber member directory
  4. Athens Chamber member directory
  5. Indeed — HR job postings in Tyler/Longview area (surfaces active companies)
  6. Seed list of major known East Texas employers
  7. Hunter.io API — domain search with department=hr filter
"""

import csv
import json
import re
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse, urljoin

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "smith_county_hr_managers.csv"

HUNTER_API_KEY = "c0a802ddeebc40350568e391654f7598de9aebb3"
HUNTER_DOMAIN_SEARCH = "https://api.hunter.io/v2/domain-search"
HUNTER_ACCOUNT = "https://api.hunter.io/v2/account"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

# HR-related title keywords for secondary filtering
HR_TITLE_KEYWORDS = [
    "human resources", "hr manager", "hr director", "hr coordinator",
    "hr generalist", "hr business partner", "hrbp", "people operations",
    "talent acquisition", "workforce", "chief people", "vp hr",
    "director of hr", "head of hr", "employee relations", "benefits manager",
    "recruiting manager", "recruiter", "staffing manager", "compensation",
    "hr specialist", "hr analyst", "training manager", "learning and development",
]

# --------------------------------------------------------------------------
# SEED LIST — major East Texas employers (guaranteed company + domain pairs)
# --------------------------------------------------------------------------
SEED_COMPANIES = [
    # Tyler / Smith County
    {"company": "UT Health Tyler", "domain": "uthct.edu", "city": "Tyler", "county": "Smith"},
    {"company": "Christus Trinity Mother Frances", "domain": "christushealth.org", "city": "Tyler", "county": "Smith"},
    {"company": "Tyler Technologies", "domain": "tylertech.com", "city": "Tyler", "county": "Smith"},
    {"company": "ALDI Distribution Center Tyler", "domain": "aldi.us", "city": "Tyler", "county": "Smith"},
    {"company": "Brookshire Grocery Company", "domain": "brookshires.com", "city": "Tyler", "county": "Smith"},
    {"company": "Trane Technologies Tyler", "domain": "tranetechnologies.com", "city": "Tyler", "county": "Smith"},
    {"company": "CHRISTUS Mother Frances Hospital", "domain": "christushealth.org", "city": "Tyler", "county": "Smith"},
    {"company": "University of Texas at Tyler", "domain": "uttyler.edu", "city": "Tyler", "county": "Smith"},
    {"company": "Tyler ISD", "domain": "tylerisd.org", "city": "Tyler", "county": "Smith"},
    {"company": "Tyler Junior College", "domain": "tjc.edu", "city": "Tyler", "county": "Smith"},
    {"company": "East Texas Medical Center", "domain": "etmc.org", "city": "Tyler", "county": "Smith"},
    {"company": "Suddenlink Communications Tyler", "domain": "alticeusa.com", "city": "Tyler", "county": "Smith"},
    {"company": "Smith County", "domain": "smith-county.com", "city": "Tyler", "county": "Smith"},
    {"company": "City of Tyler", "domain": "cityoftyler.org", "city": "Tyler", "county": "Smith"},
    {"company": "Rusk State Hospital", "domain": "hhs.texas.gov", "city": "Rusk", "county": "Cherokee"},
    {"company": "Target Tyler Distribution", "domain": "target.com", "city": "Tyler", "county": "Smith"},
    {"company": "Amazon Tyler", "domain": "amazon.com", "city": "Tyler", "county": "Smith"},
    {"company": "KLTV / East Texas Media Group", "domain": "kltv.com", "city": "Tyler", "county": "Smith"},
    {"company": "Regions Bank Tyler", "domain": "regions.com", "city": "Tyler", "county": "Smith"},
    {"company": "JPMorgan Chase Tyler", "domain": "jpmorganchase.com", "city": "Tyler", "county": "Smith"},
    {"company": "Wells Fargo Tyler", "domain": "wellsfargo.com", "city": "Tyler", "county": "Smith"},
    {"company": "Southside Bank", "domain": "southsidebank.com", "city": "Tyler", "county": "Smith"},
    {"company": "Peoples Bank Tyler", "domain": "mypeoplesbank.com", "city": "Tyler", "county": "Smith"},
    {"company": "First Bank and Trust East Texas", "domain": "fbtet.com", "city": "Tyler", "county": "Smith"},
    {"company": "American National Insurance", "domain": "anico.com", "city": "Galveston", "county": "Smith"},
    {"company": "Bracewell LLP Tyler", "domain": "bracewell.com", "city": "Tyler", "county": "Smith"},
    {"company": "Rose Capital Hotels", "domain": "rosecapitalhotels.com", "city": "Tyler", "county": "Smith"},
    {"company": "Whitehouse ISD", "domain": "whitehouseisd.org", "city": "Whitehouse", "county": "Smith"},
    {"company": "Lindale ISD", "domain": "lindaleeagles.org", "city": "Lindale", "county": "Smith"},
    {"company": "Hallsville ISD", "domain": "hallsville.org", "city": "Hallsville", "county": "Harrison"},
    # Gregg County (Longview)
    {"company": "Longview Regional Medical Center", "domain": "longviewregional.com", "city": "Longview", "county": "Gregg"},
    {"company": "Good Shepherd Medical Center Longview", "domain": "gsmc.org", "city": "Longview", "county": "Gregg"},
    {"company": "Longview ISD", "domain": "lisd.org", "city": "Longview", "county": "Gregg"},
    {"company": "Gregg County", "domain": "co.gregg.tx.us", "city": "Longview", "county": "Gregg"},
    {"company": "City of Longview", "domain": "longviewtexas.gov", "city": "Longview", "county": "Gregg"},
    {"company": "Eastman Chemical Longview", "domain": "eastman.com", "city": "Longview", "county": "Gregg"},
    {"company": "Halliburton Longview", "domain": "halliburton.com", "city": "Longview", "county": "Gregg"},
    {"company": "LeTourneau University", "domain": "letu.edu", "city": "Longview", "county": "Gregg"},
    {"company": "Kilgore College", "domain": "kilgore.edu", "city": "Kilgore", "county": "Gregg"},
    {"company": "Longview News-Journal", "domain": "news-journal.com", "city": "Longview", "county": "Gregg"},
    # Henderson County (Athens)
    {"company": "Athens ISD", "domain": "athenstigers.net", "city": "Athens", "county": "Henderson"},
    {"company": "Henderson County", "domain": "hendersoncounty.net", "city": "Athens", "county": "Henderson"},
    {"company": "Trinity Mother Frances Hospital Athens", "domain": "christushealth.org", "city": "Athens", "county": "Henderson"},
    # Van Zandt County (Canton)
    {"company": "Canton ISD", "domain": "cantonisd.net", "city": "Canton", "county": "Van Zandt"},
    {"company": "Van Zandt County", "domain": "vanzandtcounty.org", "city": "Canton", "county": "Van Zandt"},
    # Cherokee County (Jacksonville)
    {"company": "Jacksonville ISD", "domain": "jacksonvilleisd.net", "city": "Jacksonville", "county": "Cherokee"},
    {"company": "Jacksonville Medical Center", "domain": "jacksonvillemc.com", "city": "Jacksonville", "county": "Cherokee"},
    {"company": "Lon Morris College", "domain": "lonmorris.edu", "city": "Jacksonville", "county": "Cherokee"},
    # Upshur County (Gilmer)
    {"company": "Gilmer ISD", "domain": "gilmerisd.org", "city": "Gilmer", "county": "Upshur"},
    {"company": "Upshur County", "domain": "upshurcounty.org", "city": "Gilmer", "county": "Upshur"},
    # Wood County (Quitman)
    {"company": "Quitman ISD", "domain": "quitmanisd.net", "city": "Quitman", "county": "Wood"},
    {"company": "Wood County", "domain": "mywoodcounty.com", "city": "Quitman", "county": "Wood"},
    # Misc large East Texas employers
    {"company": "Southern Tire Mart", "domain": "southerntiremart.com", "city": "Columbia", "county": "Smith"},
    {"company": "Harvey Industries", "domain": "harveyindustries.com", "city": "Tyler", "county": "Smith"},
    {"company": "East Texas Communities Foundation", "domain": "etcf.org", "city": "Tyler", "county": "Smith"},
    {"company": "HomeTeam Pest Defense", "domain": "hometeam.com", "city": "Tyler", "county": "Smith"},
    {"company": "McCann Industries", "domain": "mccannindustries.com", "city": "Tyler", "county": "Smith"},
    {"company": "BancorpSouth Tyler", "domain": "bancorpsouth.com", "city": "Tyler", "county": "Smith"},
    {"company": "Security Bank Tyler", "domain": "securitybank.com", "city": "Tyler", "county": "Smith"},
    {"company": "Broadway National Bank Tyler", "domain": "broadwaynational.com", "city": "Tyler", "county": "Smith"},
    {"company": "KTRE / ABC Tyler", "domain": "ktre.com", "city": "Lufkin", "county": "Angelina"},
    {"company": "Pilgrim's Pride", "domain": "pilgrims.com", "city": "Tyler", "county": "Smith"},
    {"company": "Genco Industries Tyler", "domain": "gencoindustries.com", "city": "Tyler", "county": "Smith"},
    {"company": "Holiday Inn Tyler", "domain": "ihg.com", "city": "Tyler", "county": "Smith"},
    {"company": "Whataburger Corporate", "domain": "whataburger.com", "city": "San Antonio", "county": "Smith"},
    {"company": "Buc-ee's", "domain": "buc-ees.com", "city": "Lake Jackson", "county": "Smith"},
    {"company": "Texas Health & Human Services Tyler", "domain": "hhs.texas.gov", "city": "Tyler", "county": "Smith"},
    {"company": "Texas Workforce Commission Tyler", "domain": "twc.texas.gov", "city": "Tyler", "county": "Smith"},
    {"company": "Caliber Collision Tyler", "domain": "calibercollision.com", "city": "Tyler", "county": "Smith"},
    {"company": "Fletcher's Tire & Auto", "domain": "fletcherstire.com", "city": "Tyler", "county": "Smith"},
    {"company": "East Texas Council of Governments", "domain": "etcog.org", "city": "Kilgore", "county": "Gregg"},
    {"company": "Walmart Distribution Center", "domain": "walmart.com", "city": "Tyler", "county": "Smith"},
    {"company": "Home Depot Tyler", "domain": "homedepot.com", "city": "Tyler", "county": "Smith"},
    {"company": "HEB Tyler", "domain": "heb.com", "city": "Tyler", "county": "Smith"},
]


def is_hr_title(title: str) -> bool:
    """Return True if the title string indicates an HR role."""
    if not title:
        return False
    title_lower = title.lower()
    return any(kw in title_lower for kw in HR_TITLE_KEYWORDS)


def check_hunter_credits() -> int:
    """Return remaining Hunter.io searches."""
    try:
        resp = requests.get(HUNTER_ACCOUNT, params={"api_key": HUNTER_API_KEY}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            remaining = data.get("data", {}).get("requests", {}).get("searches", {}).get("available", 0)
            print(f"[Hunter.io] Remaining searches: {remaining}")
            return remaining
    except Exception as e:
        print(f"[Hunter.io] Could not check credits: {e}")
    return 0


def hunter_domain_search(domain: str, company: str) -> list[dict]:
    """
    Query Hunter.io domain search with department=hr filter.
    Returns list of contact dicts.
    Falls back to unfiltered search if hr filter returns nothing.
    """
    contacts = []

    def _search(department=None):
        params = {
            "domain": domain,
            "api_key": HUNTER_API_KEY,
            "limit": 100,
        }
        if department:
            params["department"] = department

        try:
            resp = requests.get(HUNTER_DOMAIN_SEARCH, params=params, timeout=15)
            if resp.status_code == 200:
                return resp.json().get("data", {}).get("emails", [])
            elif resp.status_code == 429:
                print(f"  [Hunter] Rate limited — waiting 60s")
                time.sleep(60)
            else:
                print(f"  [Hunter] {domain} → HTTP {resp.status_code}")
        except Exception as e:
            print(f"  [Hunter] {domain} error: {e}")
        return []

    # First pass: filter by HR department
    emails = _search(department="hr")
    time.sleep(1.5)

    # If nothing, fallback to full domain scan and filter by title
    if not emails:
        emails = _search()
        emails = [e for e in emails if is_hr_title(e.get("position", ""))]
        time.sleep(1.5)

    for e in emails:
        first = e.get("first_name", "")
        last = e.get("last_name", "")
        full_name = f"{first} {last}".strip()
        title = e.get("position", "")
        email_addr = e.get("value", "")
        confidence = e.get("confidence", 0)
        linkedin = e.get("linkedin", "")

        if email_addr and (is_hr_title(title) or not title):
            contacts.append({
                "company": company,
                "domain": domain,
                "name": full_name,
                "title": title,
                "email": email_addr,
                "confidence": confidence,
                "linkedin": linkedin,
            })

    return contacts


def scrape_tyler_chamber() -> list[dict]:
    """
    Tyler Area Chamber of Commerce member directory.
    URL: https://members.tylertexas.com/list/
    Returns list of {company, website} dicts.
    """
    companies = []
    base_url = "https://members.tylertexas.com/list/"
    page = 1

    print("[Tyler Chamber] Scraping member directory...")
    while True:
        url = f"{base_url}?pg={page}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                break
            soup = BeautifulSoup(resp.text, "html.parser")

            # Member cards typically have .card or .member-listing structure
            entries = soup.select(".card-body, .member-name, .list-item, .member-listing")
            if not entries:
                # Try alternate selectors
                entries = soup.select("h3 a, h2 a, .business-name a")

            found_this_page = 0
            for entry in entries:
                name_tag = entry if entry.name == "a" else entry.find("a")
                if not name_tag:
                    continue
                name = name_tag.get_text(strip=True)
                href = name_tag.get("href", "")
                if name and len(name) > 2:
                    companies.append({"company": name, "source_url": href, "city": "Tyler", "county": "Smith"})
                    found_this_page += 1

            if found_this_page == 0:
                break

            print(f"  Page {page}: {found_this_page} entries")
            page += 1
            time.sleep(1.5)

            # Safety cap
            if page > 50:
                break

        except Exception as e:
            print(f"  [Tyler Chamber] Error page {page}: {e}")
            break

    print(f"[Tyler Chamber] Total: {len(companies)} companies")
    return companies


def scrape_chamber_directory(name: str, list_url: str, city: str, county: str) -> list[dict]:
    """Generic chamber directory scraper."""
    companies = []
    print(f"[{name}] Scraping...")
    try:
        resp = requests.get(list_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"  [{name}] HTTP {resp.status_code}")
            return companies
        soup = BeautifulSoup(resp.text, "html.parser")

        for a_tag in soup.select("h3 a, h2 a, .member-name a, .card-title a, .business-name a, .gz-member-name a"):
            name_text = a_tag.get_text(strip=True)
            if name_text and len(name_text) > 2:
                companies.append({
                    "company": name_text,
                    "source_url": a_tag.get("href", ""),
                    "city": city,
                    "county": county,
                })

        print(f"  [{name}] Found {len(companies)} companies")
    except Exception as e:
        print(f"  [{name}] Error: {e}")

    return companies


def scrape_indeed_hr_postings() -> list[dict]:
    """
    Scrape Indeed for HR Manager job postings in Tyler / Longview TX area.
    Surfaces companies actively seeking HR staff.
    """
    companies = []
    search_queries = [
        ("HR Manager Tyler TX", "Tyler", "Smith"),
        ("Human Resources Director Tyler TX", "Tyler", "Smith"),
        ("HR Coordinator Longview TX", "Longview", "Gregg"),
        ("Human Resources Manager East Texas", "Tyler", "Smith"),
    ]

    print("[Indeed] Scraping HR job postings...")
    for query, city, county in search_queries:
        url = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}&l=Tyler%2C+TX&radius=50"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                print(f"  [Indeed] HTTP {resp.status_code} for: {query}")
                time.sleep(3)
                continue

            soup = BeautifulSoup(resp.text, "html.parser")

            # Indeed job cards have company name in data-company-name or .companyName
            for card in soup.select("[data-company-name], .companyName, span[class*='company']"):
                company_name = card.get("data-company-name") or card.get_text(strip=True)
                if company_name and len(company_name) > 2:
                    companies.append({
                        "company": company_name,
                        "city": city,
                        "county": county,
                        "source_url": url,
                    })

            time.sleep(2)
        except Exception as e:
            print(f"  [Indeed] Error: {e}")

    # Deduplicate
    seen = set()
    unique = []
    for c in companies:
        key = c["company"].lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(c)

    print(f"[Indeed] Found {len(unique)} unique companies with HR postings")
    return unique


def extract_domain(website: str) -> str:
    """Extract clean domain from a URL string."""
    if not website:
        return ""
    if not website.startswith("http"):
        website = "https://" + website
    try:
        parsed = urlparse(website)
        domain = parsed.netloc.lower()
        # Strip www.
        domain = re.sub(r"^www\.", "", domain)
        return domain.strip()
    except Exception:
        return ""


def build_company_list() -> list[dict]:
    """Aggregate companies from all sources. Returns deduplicated list with domains."""
    all_companies = []

    # 1. Seed list (already has domains)
    all_companies.extend(SEED_COMPANIES)
    print(f"[Seed] {len(SEED_COMPANIES)} hardcoded companies loaded")

    # 2. Tyler Chamber
    tyler_members = scrape_tyler_chamber()
    all_companies.extend(tyler_members)

    # 3. Longview Chamber
    longview = scrape_chamber_directory(
        "Longview Chamber",
        "https://www.longviewtexas.com/list/",
        "Longview", "Gregg"
    )
    all_companies.extend(longview)

    # 4. Indeed HR postings
    indeed = scrape_indeed_hr_postings()
    all_companies.extend(indeed)

    # Deduplicate by company name (case-insensitive)
    seen_names = set()
    unique = []
    for c in all_companies:
        key = c.get("company", "").lower().strip()
        if key and key not in seen_names:
            seen_names.add(key)
            unique.append(c)

    print(f"\n[Company List] Total unique companies: {len(unique)}")
    return unique


def resolve_domain_for_company(company: dict) -> str:
    """Return domain string for a company dict, resolving from website if needed."""
    # Already has domain
    if company.get("domain"):
        return company["domain"]

    # Has a source URL that might be the company site
    source = company.get("source_url", "")
    if source and "tylertexas.com" not in source and "longviewtexas.com" not in source:
        return extract_domain(source)

    return ""


def main():
    print("=" * 60)
    print("ETKM — East Texas HR Manager Scraper")
    print("=" * 60)

    # Check Hunter credits upfront
    remaining_credits = check_hunter_credits()
    if remaining_credits == 0:
        print("[WARNING] Hunter.io credits may be exhausted — will attempt anyway")

    # Build company list
    companies = build_company_list()

    # Write output CSV
    fieldnames = ["company", "city", "county", "name", "title", "email", "confidence", "domain", "linkedin"]
    results = []
    domains_searched = set()
    no_domain_count = 0

    print(f"\n[Hunter.io] Searching {len(companies)} companies for HR contacts...")
    print("-" * 60)

    for i, company in enumerate(companies):
        domain = resolve_domain_for_company(company)

        if not domain:
            no_domain_count += 1
            continue

        if domain in domains_searched:
            continue

        domains_searched.add(domain)

        company_name = company.get("company", "")
        city = company.get("city", "")
        county = company.get("county", "")

        print(f"[{i+1}/{len(companies)}] {company_name} ({domain})")

        contacts = hunter_domain_search(domain, company_name)

        if contacts:
            print(f"  → {len(contacts)} HR contact(s) found")
            for c in contacts:
                results.append({
                    "company": company_name,
                    "city": city,
                    "county": county,
                    "name": c["name"],
                    "title": c["title"],
                    "email": c["email"],
                    "confidence": c["confidence"],
                    "domain": domain,
                    "linkedin": c["linkedin"],
                })
        else:
            print(f"  → No HR contacts found")

        # Write incrementally so partial results are saved if script is interrupted
        if (i + 1) % 10 == 0:
            _write_csv(results, fieldnames)
            print(f"  [Checkpoint] {len(results)} contacts saved so far")

        # Polite delay
        time.sleep(1)

    # Final write
    _write_csv(results, fieldnames)

    print("\n" + "=" * 60)
    print(f"DONE — {len(results)} HR contacts written to {OUTPUT_FILE}")
    print(f"Domains searched: {len(domains_searched)}")
    print(f"Companies skipped (no domain): {no_domain_count}")
    print("=" * 60)


def _write_csv(results: list[dict], fieldnames: list[str]):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
