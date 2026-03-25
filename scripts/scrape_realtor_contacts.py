"""
Scrape realtor contacts for Smith County, TX.

Sources:
1. HAR.com agent search (Tyler/Smith County)
2. Realtor.com agent search (Tyler TX)

Outputs: output/smith_county_realtors.csv
"""

import csv
import json
import time
import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

OUTPUT_FILE = "output/smith_county_realtors.csv"
FIELDNAMES = ["name", "phone", "email", "office", "city", "state", "zip", "source", "profile_url"]


def clean(val):
    if not val:
        return ""
    return " ".join(str(val).split())


# ── Source 1: HAR.com ──────────────────────────────────────────────────────────

def scrape_har(session):
    """Scrape HAR.com agent listings for Tyler, TX (Smith County)."""
    results = []
    base_url = "https://www.har.com/real-estate-agents/tyler-tx"
    page = 1

    print("[HAR] Starting scrape...")

    while page <= 20:  # cap at 20 pages (~400 agents)
        url = f"{base_url}?page={page}" if page > 1 else base_url
        try:
            resp = session.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                print(f"[HAR] Page {page} returned {resp.status_code} — stopping")
                break
        except Exception as e:
            print(f"[HAR] Request error page {page}: {e}")
            break

        soup = BeautifulSoup(resp.text, "lxml")
        cards = soup.select(".agent-card, .agentcard, [class*='agent-info'], [data-testid='agent-card']")

        # Fallback: look for agent list items
        if not cards:
            cards = soup.select("li.agent-listing, div.agent-listing, article.agent")

        # Broader fallback: find by structure
        if not cards:
            cards = soup.find_all("div", class_=re.compile(r"agent", re.I))

        if not cards:
            print(f"[HAR] No cards found on page {page} — stopping")
            break

        found_new = False
        for card in cards:
            name_el = card.select_one("a.agent-name, .agent-name, h3, h4, [class*='name']")
            name = clean(name_el.get_text()) if name_el else ""
            if not name:
                continue

            profile_url = ""
            link = card.select_one("a[href*='/realtor/']") or (name_el if name_el and name_el.name == "a" else None)
            if link and link.get("href"):
                href = link["href"]
                profile_url = href if href.startswith("http") else f"https://www.har.com{href}"

            phone_el = card.select_one("[class*='phone'], [href^='tel:']")
            phone = ""
            if phone_el:
                phone = clean(phone_el.get("href", "").replace("tel:", "") or phone_el.get_text())

            email_el = card.select_one("[href^='mailto:']")
            email = clean(email_el.get("href", "").replace("mailto:", "")) if email_el else ""

            office_el = card.select_one("[class*='office'], [class*='company'], [class*='brokerage']")
            office = clean(office_el.get_text()) if office_el else ""

            results.append({
                "name": name,
                "phone": phone,
                "email": email,
                "office": office,
                "city": "Tyler",
                "state": "TX",
                "zip": "",
                "source": "HAR.com",
                "profile_url": profile_url,
            })
            found_new = True

        print(f"[HAR] Page {page}: {len(cards)} cards found, total so far: {len(results)}")

        # Check for next page
        next_link = soup.select_one("a[rel='next'], a.next, .pagination a[aria-label='Next']")
        if not next_link or not found_new:
            break

        page += 1
        time.sleep(1.5)

    print(f"[HAR] Done — {len(results)} contacts collected")
    return results


# ── Source 2: Realtor.com ──────────────────────────────────────────────────────

def scrape_realtor_com(session):
    """Scrape Realtor.com agent search for Tyler TX."""
    results = []
    print("[Realtor.com] Starting scrape...")

    for page in range(1, 11):  # 10 pages
        url = f"https://www.realtor.com/realestateagents/tyler_tx/pg-{page}"
        try:
            resp = session.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                print(f"[Realtor.com] Page {page} status {resp.status_code} — stopping")
                break
        except Exception as e:
            print(f"[Realtor.com] Error page {page}: {e}")
            break

        soup = BeautifulSoup(resp.text, "lxml")

        # Try JSON-LD structured data first
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "")
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict):
                    items = data.get("@graph", [data])
                else:
                    continue
                for item in items:
                    if item.get("@type") in ("RealEstateAgent", "Person"):
                        name = clean(item.get("name", ""))
                        if not name:
                            continue
                        phone = clean(item.get("telephone", ""))
                        email = clean(item.get("email", ""))
                        org = item.get("worksFor", {})
                        office = clean(org.get("name", "") if isinstance(org, dict) else "")
                        addr = item.get("address", {})
                        city = clean(addr.get("addressLocality", "Tyler") if isinstance(addr, dict) else "Tyler")
                        state = clean(addr.get("addressRegion", "TX") if isinstance(addr, dict) else "TX")
                        zip_code = clean(addr.get("postalCode", "") if isinstance(addr, dict) else "")
                        url_val = clean(item.get("url", ""))
                        results.append({
                            "name": name,
                            "phone": phone,
                            "email": email,
                            "office": office,
                            "city": city,
                            "state": state,
                            "zip": zip_code,
                            "source": "Realtor.com",
                            "profile_url": url_val,
                        })
            except Exception:
                pass

        # HTML fallback
        cards = soup.select("[data-testid='agent-card'], .agent-card, li[class*='agent']")
        for card in cards:
            name_el = card.select_one("[data-testid='agent-name'], .agent-name, h3, h4")
            name = clean(name_el.get_text()) if name_el else ""
            if not name:
                continue

            phone_el = card.select_one("[data-testid='agent-phone'], [href^='tel:']")
            phone = ""
            if phone_el:
                phone = clean(phone_el.get("href", "").replace("tel:", "") or phone_el.get_text())

            office_el = card.select_one("[data-testid='agent-office'], [class*='office']")
            office = clean(office_el.get_text()) if office_el else ""

            link = card.select_one("a[href*='/realestateagents/']")
            profile_url = link["href"] if link else ""
            if profile_url and not profile_url.startswith("http"):
                profile_url = f"https://www.realtor.com{profile_url}"

            results.append({
                "name": name,
                "phone": phone,
                "email": "",
                "office": office,
                "city": "Tyler",
                "state": "TX",
                "zip": "",
                "source": "Realtor.com",
                "profile_url": profile_url,
            })

        print(f"[Realtor.com] Page {page}: total so far {len(results)}")
        time.sleep(1.5)

    print(f"[Realtor.com] Done — {len(results)} contacts collected")
    return results


# ── Source 3: Texas REALTORS public search ────────────────────────────────────

def scrape_txrealtors(session):
    """
    Texas REALTORS member search — Smith County filter.
    URL: https://www.texasrealtors.com/find-a-realtor/?county=Smith
    """
    results = []
    print("[TexasREALTORS] Starting scrape...")

    base = "https://www.texasrealtors.com/find-a-realtor/"
    params_base = {"county": "Smith", "state": "TX"}

    for page in range(1, 16):
        params = {**params_base, "pg": page}
        try:
            resp = session.get(base, params=params, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                print(f"[TexasREALTORS] Page {page} status {resp.status_code}")
                break
        except Exception as e:
            print(f"[TexasREALTORS] Error page {page}: {e}")
            break

        soup = BeautifulSoup(resp.text, "lxml")
        cards = soup.select(".member-card, .realtor-card, .agent-result, [class*='member']")

        if not cards:
            # Try table rows
            cards = soup.select("table tr[class*='member'], table tr[class*='agent']")

        if not cards:
            print(f"[TexasREALTORS] No cards on page {page} — stopping")
            break

        for card in cards:
            name_el = card.select_one(".member-name, .realtor-name, h3, h4, td.name")
            name = clean(name_el.get_text()) if name_el else ""
            if not name:
                continue

            phone_el = card.select_one("[href^='tel:'], .phone, td.phone")
            phone = ""
            if phone_el:
                phone = clean(phone_el.get("href", "").replace("tel:", "") or phone_el.get_text())

            email_el = card.select_one("[href^='mailto:'], .email")
            email = clean(email_el.get("href", "").replace("mailto:", "")) if email_el else ""

            office_el = card.select_one(".office, .brokerage, .company, td.office")
            office = clean(office_el.get_text()) if office_el else ""

            city_el = card.select_one(".city, td.city")
            city = clean(city_el.get_text()) if city_el else "Tyler"

            results.append({
                "name": name,
                "phone": phone,
                "email": email,
                "office": office,
                "city": city,
                "state": "TX",
                "zip": "",
                "source": "TexasREALTORS.com",
                "profile_url": "",
            })

        print(f"[TexasREALTORS] Page {page}: {len(cards)} found, total: {len(results)}")
        next_link = soup.select_one("a[rel='next'], a.next")
        if not next_link:
            break
        time.sleep(1.5)

    print(f"[TexasREALTORS] Done — {len(results)} contacts collected")
    return results


# ── Dedup & Save ──────────────────────────────────────────────────────────────

def dedup(records):
    seen = set()
    out = []
    for r in records:
        key = (r["name"].lower(), r["phone"])
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def save_csv(records, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)
    print(f"\nSaved {len(records)} records → {path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    session = requests.Session()
    session.headers.update(HEADERS)

    all_records = []

    all_records += scrape_har(session)
    all_records += scrape_realtor_com(session)
    all_records += scrape_txrealtors(session)

    unique = dedup(all_records)
    print(f"\nTotal before dedup: {len(all_records)} | After dedup: {len(unique)}")

    save_csv(unique, OUTPUT_FILE)


if __name__ == "__main__":
    main()
