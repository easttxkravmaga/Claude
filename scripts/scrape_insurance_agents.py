"""
Smith County, TX — Insurance Agents & Adjusters Scraper
Coverage: Tyler, Lindale, Whitehouse, Bullard, Troup, Winona, Arp, Flint + surrounding
Sources:
  1. TDI Open Data Portal (Socrata API) — primary, authoritative
     Queries by every Smith County city name AND every Smith County ZIP code
  2. IIA of Tyler (iiatyler.org) — independent agents, has emails
  3. YellowPages — supplemental phone/address (all Smith County cities)
  4. Allstate, State Farm, Farmers, Progressive, Texas Farm Bureau — carrier finders
"""

import csv
import json
import re
import time
import random
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, quote

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "smith_county_insurance_agents.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

SMITH_COUNTY_ZIPS = {
    # Tyler
    "75701", "75702", "75703", "75704", "75705",
    "75708", "75709", "75711", "75712", "75713",
    # Lindale / Hideaway
    "75771",
    # Whitehouse
    "75791",
    # Bullard (partly Smith, partly Cherokee)
    "75757",
    # Troup (partly Smith, partly Cherokee)
    "75789",
    # Winona
    "75792",
    # Arp
    "75750",
    # Flint / Noonday / New Chapel Hill / Chapel Hill
    "75762",
}

SMITH_COUNTY_CITIES = {
    "TYLER", "LINDALE", "WHITEHOUSE", "BULLARD",
    "TROUP", "WINONA", "ARP", "FLINT", "NOONDAY",
    "NEW CHAPEL HILL", "CHAPEL HILL", "HIDEAWAY",
}

FIELDS = [
    "name", "phone", "email", "agency", "license_type",
    "license_number", "address", "city", "state", "zip",
    "carrier", "source", "notes"
]


def sleep(lo=1.0, hi=2.5):
    time.sleep(random.uniform(lo, hi))


def get(url, session, params=None, json_mode=False, timeout=15):
    try:
        r = session.get(url, headers=HEADERS, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json() if json_mode else r
    except Exception as e:
        print(f"  [WARN] GET failed: {url} — {e}")
        return [] if json_mode else None


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 1: TDI Open Data Portal (Socrata API)
# ─────────────────────────────────────────────────────────────────────────────

def _tdi_row_to_record(row):
    first = row.get("first_name", "").strip().title()
    last  = row.get("last_name", "").strip().title()
    name  = f"{first} {last}".strip()
    if not name or name == " ":
        name = row.get("business_name", "").strip().title()
    agency = row.get("business_name", "").strip().title()
    return {
        "name":           name,
        "phone":          "",
        "email":          "",
        "agency":         agency if agency.lower() != name.lower() else "",
        "license_type":   row.get("license_type_description", "").strip(),
        "license_number": row.get("license_number", "").strip(),
        "address":        row.get("address_line_1", "").strip().title(),
        "city":           row.get("city", "").strip().title(),
        "state":          row.get("state_code", "TX"),
        "zip":            row.get("zip_code", "").strip()[:5],
        "carrier":        "",
        "source":         "TDI Open Data Portal",
        "notes":          "",
    }


def scrape_tdi(session):
    """Pull all insurance agents & adjusters licensed in Smith County, TX from TDI."""
    print("\n[1/5] TDI Open Data Portal...")
    records = []
    seen = set()
    base = "https://data.texas.gov/resource/kxv3-diwf.json"
    limit = 1000

    def _key(row):
        return (
            row.get("first_name", "") + row.get("last_name", "") +
            row.get("license_number", "")
        )

    def _add_batch(batch):
        for row in batch:
            k = _key(row)
            if k in seen:
                continue
            seen.add(k)
            records.append(_tdi_row_to_record(row))

    # --- Pass 1: query each Smith County city name ---
    for city_name in sorted(SMITH_COUNTY_CITIES):
        offset = 0
        while True:
            params = {
                "$where": f"upper(city) = '{city_name}' AND upper(state_code) = 'TX'",
                "$limit": limit,
                "$offset": offset,
                "$order": "last_name ASC",
            }
            batch = get(base, session, params=params, json_mode=True)
            if not batch:
                break
            _add_batch(batch)
            print(f"  {city_name}: {len(records)} total so far (offset {offset})...")
            if len(batch) < limit:
                break
            offset += limit
            sleep(0.5, 1.0)

    # --- Pass 2: query by every Smith County ZIP to catch records with non-standard city names ---
    for z in sorted(SMITH_COUNTY_ZIPS):
        params = {
            "$where": f"zip_code = '{z}' AND upper(state_code) = 'TX'",
            "$limit": limit,
            "$offset": 0,
        }
        batch = get(base, session, params=params, json_mode=True)
        if not batch:
            continue
        before = len(records)
        _add_batch(batch)
        added = len(records) - before
        if added:
            print(f"  ZIP {z}: +{added} new records")
        sleep(0.3, 0.8)

    print(f"  TDI total: {len(records)} unique records")
    return records


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 2: IIA of Tyler (independent agents with email)
# ─────────────────────────────────────────────────────────────────────────────

def scrape_iia_tyler(session):
    """Scrape member directory from iiatyler.org."""
    print("\n[2/5] IIA of Tyler...")
    records = []
    base = "https://iiatyler.org"

    for cat_slug in ("member", "associate-member"):
        url = f"{base}/member-categories/{cat_slug}/"
        resp = get(url, session)
        if not resp:
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        # Find member links
        member_links = []
        for a in soup.select("a[href*='/members/']"):
            href = a.get("href", "")
            if href and "/members/" in href:
                member_links.append(href)

        # Also check article/post links
        for a in soup.select(".entry-title a, h2 a, h3 a, .member-name a"):
            href = a.get("href", "")
            if href:
                member_links.append(href)

        member_links = list(set(member_links))
        print(f"  Found {len(member_links)} member links in /{cat_slug}/")

        for link in member_links:
            if not link.startswith("http"):
                link = urljoin(base, link)
            sleep(0.8, 1.5)
            resp2 = get(link, session)
            if not resp2:
                continue
            soup2 = BeautifulSoup(resp2.text, "html.parser")

            # Agency/company name from title or heading
            agency = ""
            title_el = soup2.select_one("h1.entry-title, h1.page-title, h1")
            if title_el:
                agency = title_el.get_text(strip=True)

            # Extract contact fields from page text
            text = soup2.get_text(separator=" ")

            phone = ""
            phone_m = re.search(r'(\(?\d{3}\)?[\s\-\.]\d{3}[\s\-\.]\d{4})', text)
            if phone_m:
                phone = phone_m.group(1)

            email = ""
            email_m = re.search(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', text)
            if email_m:
                email = email_m.group(0).lower()
            # Also check mailto links
            for a in soup2.select("a[href^='mailto:']"):
                email = a["href"].replace("mailto:", "").strip()
                break

            # Address
            address = ""
            for sel in [".address", ".location", "address", "[class*='addr']"]:
                el = soup2.select_one(sel)
                if el:
                    address = el.get_text(" ", strip=True)
                    break

            # Contact person name
            contact_name = ""
            for sel in [".contact-name", ".person-name", "[class*='contact']"]:
                el = soup2.select_one(sel)
                if el:
                    contact_name = el.get_text(strip=True)
                    break

            records.append({
                "name":         contact_name or agency,
                "phone":        phone,
                "email":        email,
                "agency":       agency,
                "license_type": "Independent Agent",
                "license_number": "",
                "address":      address,
                "city":         "Tyler",
                "state":        "TX",
                "zip":          "",
                "carrier":      "",
                "source":       "IIA of Tyler",
                "notes":        link,
            })
            print(f"    + {agency}")

    print(f"  IIA Tyler total: {len(records)}")
    return records


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 3: YellowPages
# ─────────────────────────────────────────────────────────────────────────────

def scrape_yellowpages(session):
    """Scrape YellowPages for insurance agents in Tyler, TX."""
    print("\n[3/5] YellowPages...")
    records = []
    seen = set()
    base = "https://www.yellowpages.com"

    yp_cities = [
        "tyler-tx", "lindale-tx", "whitehouse-tx", "bullard-tx",
        "troup-tx", "winona-tx", "arp-tx",
    ]

    for city_slug in yp_cities:
        for search_term in ["insurance-agents", "insurance-adjusters"]:
            page = 1
            while True:
                url = f"{base}/{city_slug}/{search_term}"
                params = {"page": page} if page > 1 else {}
                sleep(2.0, 4.0)
                resp = get(url, session, params=params)
                if not resp:
                    break

                soup = BeautifulSoup(resp.text, "html.parser")
                listings = soup.select(".result")
                if not listings:
                    listings = soup.select("[class*='srp-listing']")
                if not listings:
                    break

                new_count = 0
                for listing in listings:
                    name_el = listing.select_one(".business-name, .n, h2 a")
                    name = name_el.get_text(strip=True) if name_el else ""
                    if not name or name in seen:
                        continue
                    seen.add(name)
                    new_count += 1

                    phone_el = listing.select_one(".phone, .phones")
                    phone = phone_el.get_text(strip=True) if phone_el else ""

                    street_el = listing.select_one(".street-address, .adr .street-address")
                    city_el   = listing.select_one(".city, .locality")
                    street    = street_el.get_text(strip=True) if street_el else ""
                    city_text = city_el.get_text(strip=True) if city_el else city_slug.split("-")[0].title()

                    cats  = [c.get_text(strip=True) for c in listing.select(".categories a")]
                    notes = ", ".join(cats)

                    records.append({
                        "name":           name,
                        "phone":          phone,
                        "email":          "",
                        "agency":         name,
                        "license_type":   "Insurance Agent/Adjuster",
                        "license_number": "",
                        "address":        street,
                        "city":           city_text or city_slug.split("-")[0].title(),
                        "state":          "TX",
                        "zip":            "",
                        "carrier":        "",
                        "source":         "YellowPages",
                        "notes":          notes,
                    })

                print(f"  {city_slug} / page {page} ({search_term}): {new_count} new")
                if new_count == 0:
                    break
                next_el = soup.select_one("a.next")
                if not next_el:
                    break
                page += 1

    print(f"  YellowPages total: {len(records)}")
    return records


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 4: Allstate Agent Finder
# ─────────────────────────────────────────────────────────────────────────────

def scrape_allstate(session):
    """Scrape Allstate agent finder for Tyler, TX."""
    print("\n[4/5] Carrier finders...")
    records = []

    # Allstate
    url = "https://agents.allstate.com/usa/tx/tyler"
    sleep(1.5, 3.0)
    resp = get(url, session)
    if resp:
        soup = BeautifulSoup(resp.text, "html.parser")
        # Agent cards
        for card in soup.select(".agent-card, [class*='agent'], .result-card"):
            name_el = card.select_one("h2, h3, .agent-name, .name")
            name = name_el.get_text(strip=True) if name_el else ""
            if not name:
                continue
            phone_el = card.select_one(".phone, [class*='phone']")
            phone = phone_el.get_text(strip=True) if phone_el else ""
            addr_el = card.select_one(".address, [class*='addr']")
            addr = addr_el.get_text(" ", strip=True) if addr_el else ""

            records.append({
                "name": name, "phone": phone, "email": "",
                "agency": name, "license_type": "Insurance Agent",
                "license_number": "", "address": addr,
                "city": "Tyler", "state": "TX", "zip": "",
                "carrier": "Allstate", "source": "Allstate Agent Finder", "notes": "",
            })

    # Progressive
    sleep(1.5, 3.0)
    url2 = "https://www.progressiveagent.com/local-agent/texas/tyler/"
    resp2 = get(url2, session)
    if resp2:
        soup2 = BeautifulSoup(resp2.text, "html.parser")
        for card in soup2.select(".agent-card, .agency-card, [class*='agent'], li[class*='result']"):
            name_el = card.select_one("h2, h3, .name, a")
            name = name_el.get_text(strip=True) if name_el else ""
            if not name or len(name) < 3:
                continue
            phone_el = card.select_one(".phone, [class*='phone']")
            phone = phone_el.get_text(strip=True) if phone_el else ""
            records.append({
                "name": name, "phone": phone, "email": "",
                "agency": name, "license_type": "Insurance Agent",
                "license_number": "", "address": "",
                "city": "Tyler", "state": "TX", "zip": "",
                "carrier": "Progressive", "source": "Progressive Agent Finder", "notes": "",
            })

    # Texas Farm Bureau — Smith County
    sleep(1.5, 3.0)
    url3 = "https://www.txfb-ins.com/county/details/smith"
    resp3 = get(url3, session)
    if resp3:
        soup3 = BeautifulSoup(resp3.text, "html.parser")
        for card in soup3.select(".agent, .agent-card, [class*='agent'], .staff-member"):
            name_el = card.select_one("h2, h3, .name, strong")
            name = name_el.get_text(strip=True) if name_el else ""
            if not name:
                continue
            phone_el = card.select_one(".phone, [class*='phone']")
            phone = phone_el.get_text(strip=True) if phone_el else ""
            records.append({
                "name": name, "phone": phone, "email": "",
                "agency": "Texas Farm Bureau Insurance", "license_type": "Insurance Agent",
                "license_number": "", "address": "",
                "city": "Tyler", "state": "TX", "zip": "",
                "carrier": "Texas Farm Bureau", "source": "TX Farm Bureau Agent Finder", "notes": "",
            })

    print(f"  Carrier finders total: {len(records)}")
    return records


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 5: Known agents from research (seed data)
# ─────────────────────────────────────────────────────────────────────────────

SEED_AGENTS = [
    {"name": "Thomas Perry",    "phone": "903-592-1000", "agency": "Thomas Perry - State Farm", "carrier": "State Farm", "address": "", "zip": ""},
    {"name": "Taylor Berumen",  "phone": "903-939-3535", "agency": "Taylor Berumen - State Farm", "carrier": "State Farm", "address": "", "zip": ""},
    {"name": "Richard Davis",   "phone": "903-593-2503", "agency": "Richard Davis - State Farm", "carrier": "State Farm", "address": "723 S Broadway Ave", "zip": "75701"},
    {"name": "John Merrill",    "phone": "903-730-9139", "agency": "John Merrill - State Farm", "carrier": "State Farm", "address": "", "zip": ""},
    {"name": "Brice Borgeson",  "phone": "",             "agency": "Brice Borgeson - State Farm", "carrier": "State Farm", "address": "6004 S Broadway Ave Ste 300", "zip": ""},
    {"name": "Jimmie Bergman",  "phone": "",             "agency": "Jimmie Bergman - State Farm", "carrier": "State Farm", "address": "", "zip": ""},
    {"name": "Michael Lindner", "phone": "",             "agency": "Michael Lindner - Allstate", "carrier": "Allstate", "address": "", "zip": ""},
    {"name": "Jeff Callens",    "phone": "",             "agency": "Jeff Callens - Allstate", "carrier": "Allstate", "address": "", "zip": ""},
    {"name": "Neal Nevejans",   "phone": "",             "agency": "Neal J. Nevejans - Allstate", "carrier": "Allstate", "address": "", "zip": ""},
    {"name": "Jeremy Thomas",   "phone": "",             "agency": "Jeremy Thomas - Allstate", "carrier": "Allstate", "address": "", "zip": ""},
    {"name": "Tom Sorrels",     "phone": "903-526-2626", "agency": "Tom Sorrels Insurance Agency", "carrier": "Progressive", "address": "", "zip": ""},
    {"name": "Insurance One Agency", "phone": "903-526-0208", "agency": "Insurance One Agency LC", "carrier": "Progressive", "address": "", "zip": ""},
    # IIA Tyler members from research
    {"name": "Ark Assurance Group",        "phone": "", "agency": "Ark Assurance Group", "carrier": "Independent", "address": "", "zip": ""},
    {"name": "Bergfeld Insurance Agency",  "phone": "", "agency": "Bergfeld Insurance Agency", "carrier": "Independent", "address": "", "zip": ""},
    {"name": "Bosworth & Associates",      "phone": "", "agency": "Bosworth & Associates", "carrier": "Independent", "address": "", "zip": ""},
    {"name": "Cozad Insurance",            "phone": "", "agency": "Cozad Insurance", "carrier": "Independent", "address": "", "zip": ""},
    {"name": "Exploration Insurance Group","phone": "", "agency": "Exploration Insurance Group", "carrier": "Independent", "address": "", "zip": ""},
    {"name": "Gibb Agency",                "phone": "", "agency": "Gibb Agency", "carrier": "Independent", "address": "", "zip": ""},
    {"name": "Hibbs Hallmark & Company",   "phone": "", "agency": "Hibbs Hallmark & Company", "carrier": "Independent", "address": "", "zip": ""},
    {"name": "Higginbotham Insurance Agency","phone":"","agency": "Higginbotham Insurance Agency","carrier": "Independent", "address": "", "zip": ""},
    {"name": "Jim Toman Insurance",        "phone": "", "agency": "Jim Toman Insurance", "carrier": "Independent", "address": "", "zip": ""},
    {"name": "Legacy IG LLC",              "phone": "", "agency": "Legacy IG LLC", "carrier": "Independent", "address": "", "zip": ""},
    {"name": "Thompson-Hicks Agency",      "phone": "", "agency": "Thompson-Hicks Agency", "carrier": "Independent", "address": "", "zip": ""},
    {"name": "Threlkeld & Company Insurance","phone":"","agency": "Threlkeld & Company Insurance","carrier": "Independent", "address": "", "zip": ""},
    {"name": "Watkins Insurance Group",    "phone": "", "agency": "Watkins Insurance Group", "carrier": "Independent", "address": "", "zip": ""},
    # NYL
    {"name": "Rodger K. Johnson",  "phone": "", "agency": "New York Life", "carrier": "New York Life", "address": "", "zip": ""},
    {"name": "Tiffany H. Kirgan",  "phone": "", "agency": "New York Life", "carrier": "New York Life", "address": "", "zip": ""},
    {"name": "Amanda L. Monk",     "phone": "", "agency": "New York Life", "carrier": "New York Life", "address": "", "zip": ""},
]

def seed_records():
    out = []
    for s in SEED_AGENTS:
        out.append({
            "name":           s["name"],
            "phone":          s.get("phone", ""),
            "email":          "",
            "agency":         s.get("agency", ""),
            "license_type":   "Insurance Agent",
            "license_number": "",
            "address":        s.get("address", ""),
            "city":           "Tyler",
            "state":          "TX",
            "zip":            s.get("zip", ""),
            "carrier":        s.get("carrier", ""),
            "source":         "Research / Directory",
            "notes":          "",
        })
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Dedup & Save
# ─────────────────────────────────────────────────────────────────────────────

def normalize_name(s):
    return re.sub(r'\s+', ' ', s.strip().lower())

def dedup(records):
    seen = set()
    out = []
    for r in records:
        key = normalize_name(r.get("name", "") + r.get("license_number", "") + r.get("phone", ""))
        if key in seen or not key.strip():
            continue
        seen.add(key)
        out.append(r)
    return out

def save(records):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    print(f"\n  Saved {len(records)} records → {OUTPUT_FILE}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Smith County TX — Insurance Agents & Adjusters Scraper")
    print("=" * 60)

    session = requests.Session()
    session.headers.update(HEADERS)

    all_records = []

    # 1. TDI — primary authoritative source
    all_records += scrape_tdi(session)

    # 2. IIA of Tyler — independent agents with emails
    all_records += scrape_iia_tyler(session)

    # 3. YellowPages
    all_records += scrape_yellowpages(session)

    # 4. Carrier finders
    all_records += scrape_allstate(session)

    # 5. Seed data from research
    all_records += seed_records()

    # Dedup and save
    final = dedup(all_records)
    print(f"\nTotal before dedup: {len(all_records)}")
    print(f"Total after dedup:  {len(final)}")
    save(final)

    # Summary by source
    from collections import Counter
    by_source = Counter(r["source"] for r in final)
    print("\nBy source:")
    for src, cnt in sorted(by_source.items(), key=lambda x: -x[1]):
        print(f"  {cnt:4d}  {src}")

    # Summary by license type
    by_type = Counter(r["license_type"] for r in final if r["license_type"])
    print("\nBy license type:")
    for lt, cnt in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {cnt:4d}  {lt}")


if __name__ == "__main__":
    main()
