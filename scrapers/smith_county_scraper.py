"""
Smith County Contact Scraper
Project: ACQ — Student Acquisition | East Texas Krav Maga
Branch: claude/smith-county-training-contacts-PVM4I

Builds a deduplicated contact list from 10 Smith County organizations,
maps each contact to ETKM audience segments and arc types for WF-001.

Usage:
    python smith_county_scraper.py [--sources SOURCE1 SOURCE2 ...] [--output FILE]

    --sources   One or more source IDs to run (default: all, in priority order)
                CHAMBER GTAR SCSO BNI TYLER_ISD TYP JL_TYLER ROTARY VET_ORGS HOMESCHOOL
    --output    Output CSV filename (default: smith_county_contacts_YYYY-MM-DD.csv)

Requirements:
    pip install -r requirements_scraper.txt
    playwright install chromium
"""

import argparse
import csv
import logging
import random
import re
import time
from abc import ABC, abstractmethod
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
log = logging.getLogger("smith_county_scraper")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

OUTPUT_COLUMNS = [
    "source", "first_name", "last_name", "email",
    "phone", "org_name", "title", "arc_type", "segment", "notes",
]

PRIORITY_ORDER = [
    "CHAMBER", "GTAR", "SCSO", "BNI",
    "TYLER_ISD", "TYP", "JL_TYLER", "ROTARY",
    "VET_ORGS", "HOMESCHOOL",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_phone_re = re.compile(r"[\D]")
_email_re = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")


def normalize_phone(raw: str) -> str:
    """Normalize to (###) ###-#### or return empty string."""
    if not raw:
        return ""
    digits = _phone_re.sub("", raw)
    if len(digits) == 10:
        return f"({digits[0:3]}) {digits[3:6]}-{digits[6:10]}"
    if len(digits) == 11 and digits[0] == "1":
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:11]}"
    return raw.strip()


def normalize_email(raw: str) -> str:
    return (raw or "").strip().lower()


def split_name(full: str):
    """Split 'First Last' → (first, last). Handles middle names by collapsing."""
    parts = full.strip().split()
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


def random_delay(lo=2.0, hi=4.0):
    time.sleep(random.uniform(lo, hi))


def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def soup_get(session: requests.Session, url: str, delay=True) -> BeautifulSoup:
    if delay:
        random_delay()
    resp = session.get(url, timeout=20)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def deduplicate(contacts: list[dict]) -> list[dict]:
    """
    1. Primary key: email (exact, lowercased)
    2. Fallback key: first_name + last_name + org_name (case-insensitive)
    Keeps record with most populated fields; merges source values.
    """
    by_email: dict[str, dict] = {}
    by_name: dict[str, dict] = {}

    def field_count(r):
        return sum(1 for v in r.values() if v)

    def merge_into(existing, new):
        # Merge source tags
        existing_sources = set(existing["source"].split(","))
        existing_sources.add(new["source"])
        existing["source"] = ",".join(sorted(existing_sources))
        # Keep whichever record has more data (overwrite field-by-field from richer)
        if field_count(new) > field_count(existing):
            src = existing["source"]
            existing.update(new)
            existing["source"] = src

    deduped = []

    for rec in contacts:
        email_key = normalize_email(rec.get("email", ""))
        name_key = (
            f"{rec.get('first_name','').strip().lower()}|"
            f"{rec.get('last_name','').strip().lower()}|"
            f"{rec.get('org_name','').strip().lower()}"
        )

        if email_key and email_key in by_email:
            merge_into(by_email[email_key], rec)
            continue

        if name_key != "||" and name_key in by_name:
            merge_into(by_name[name_key], rec)
            continue

        # New record
        rec["email"] = email_key or rec.get("email", "")
        rec["phone"] = normalize_phone(rec.get("phone", ""))
        deduped.append(rec)

        if email_key:
            by_email[email_key] = rec
        if name_key != "||":
            by_name[name_key] = rec

    return deduped


# ---------------------------------------------------------------------------
# Base scraper
# ---------------------------------------------------------------------------

class BaseScraper(ABC):
    SOURCE_ID: str = ""

    def __init__(self):
        self.session = make_session()
        self.log = logging.getLogger(f"scraper.{self.SOURCE_ID}")

    @abstractmethod
    def scrape(self) -> list[dict]:
        """Return list of contact dicts matching OUTPUT_COLUMNS schema."""

    def _record(self, **kwargs) -> dict:
        rec = {col: "" for col in OUTPUT_COLUMNS}
        rec["source"] = self.SOURCE_ID
        rec.update(kwargs)
        rec["email"] = normalize_email(rec["email"])
        rec["phone"] = normalize_phone(rec["phone"])
        return rec

    def _fetch_js(self, url: str, wait="networkidle") -> str:
        """Fetch a JS-rendered page via Playwright."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            ctx = browser.new_context(user_agent=USER_AGENT)
            page = ctx.new_page()
            page.goto(url, wait_until=wait, timeout=30000)
            random_delay(2, 4)
            html = page.content()
            browser.close()
        return html


# ---------------------------------------------------------------------------
# SOURCE 1 — Tyler Area Chamber of Commerce
# ---------------------------------------------------------------------------

class ChamberScraper(BaseScraper):
    SOURCE_ID = "CHAMBER"
    BASE_URL = "https://www.tylertexas.com/list/"

    def scrape(self) -> list[dict]:
        contacts = []
        self.log.info("Fetching Chamber directory…")
        page_num = 1

        while True:
            url = f"{self.BASE_URL}?page={page_num}"
            try:
                html = self._fetch_js(url)
            except Exception as e:
                self.log.warning(f"Page {page_num} failed: {e}")
                break

            soup = BeautifulSoup(html, "html.parser")
            cards = soup.select(".list-item, .member-card, .card, [class*='member']")

            if not cards:
                self.log.info(f"No cards found on page {page_num} — stopping.")
                break

            for card in cards:
                name_el = card.select_one(".member-name, .contact-name, [class*='name']")
                biz_el  = card.select_one(".member-business, .org-name, [class*='business'], [class*='company']")
                phone_el = card.select_one(".member-phone, [class*='phone']")
                email_el = card.select_one("a[href^='mailto:'], .member-email, [class*='email']")

                full_name = (name_el.get_text(strip=True) if name_el else "")
                org       = (biz_el.get_text(strip=True) if biz_el else "")
                phone     = (phone_el.get_text(strip=True) if phone_el else "")

                email = ""
                if email_el:
                    href = email_el.get("href", "")
                    if href.startswith("mailto:"):
                        email = href[7:].split("?")[0]
                    else:
                        email = email_el.get_text(strip=True)
                    found = _email_re.search(email)
                    email = found.group() if found else email

                if not full_name and not org:
                    continue

                first, last = split_name(full_name) if full_name else (org, "")

                contacts.append(self._record(
                    first_name=first,
                    last_name=last,
                    email=email,
                    phone=phone,
                    org_name=org or first,
                    arc_type="Default",
                    segment=3,
                    notes="Chamber member — verify contact name",
                ))

            self.log.info(f"Page {page_num}: {len(cards)} cards collected.")
            page_num += 1
            random_delay(3, 5)

        self.log.info(f"CHAMBER total: {len(contacts)}")
        return contacts


# ---------------------------------------------------------------------------
# SOURCE 2 — BNI Tyler Chapters
# ---------------------------------------------------------------------------

class BNIScraper(BaseScraper):
    SOURCE_ID = "BNI"
    SEARCH_URL = "https://www.bni.com/find-a-chapter?location=Tyler%2C+TX"

    INDUSTRY_ARC = {
        "real estate": ("Safety", 11),
        "healthcare":  ("Safety", 11),
        "nurse":       ("Safety", 11),
        "medical":     ("Safety", 11),
        "law enforcement": ("LE/Mil", 8),
        "security":    ("LE/Mil", 8),
        "fitness":     ("Fitness", 6),
        "gym":         ("Fitness", 6),
        "education":   ("Parent", 1),
        "school":      ("Parent", 1),
    }

    def _arc_for_industry(self, industry: str):
        lower = industry.lower()
        for kw, (arc, seg) in self.INDUSTRY_ARC.items():
            if kw in lower:
                return arc, seg
        return "Default", 3

    def scrape(self) -> list[dict]:
        contacts = []
        self.log.info("Fetching BNI chapter list…")

        try:
            html = self._fetch_js(self.SEARCH_URL)
        except Exception as e:
            self.log.error(f"BNI search page failed: {e}")
            return contacts

        soup = BeautifulSoup(html, "html.parser")
        chapter_links = []

        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/chapters/" in href or "/chapter/" in href:
                full = href if href.startswith("http") else f"https://www.bni.com{href}"
                if full not in chapter_links:
                    chapter_links.append(full)

        self.log.info(f"Found {len(chapter_links)} BNI chapter links.")

        for ch_url in chapter_links:
            try:
                ch_html = self._fetch_js(ch_url)
            except Exception as e:
                self.log.warning(f"Chapter {ch_url} failed: {e}")
                continue

            ch_soup = BeautifulSoup(ch_html, "html.parser")
            members = ch_soup.select(".member, .member-card, [class*='member-item']")

            for m in members:
                name_el     = m.select_one("[class*='name']")
                biz_el      = m.select_one("[class*='business'], [class*='company']")
                industry_el = m.select_one("[class*='category'], [class*='industry'], [class*='profession']")
                phone_el    = m.select_one("[class*='phone']")

                full_name = name_el.get_text(strip=True) if name_el else ""
                org       = biz_el.get_text(strip=True) if biz_el else ""
                industry  = industry_el.get_text(strip=True) if industry_el else ""
                phone     = phone_el.get_text(strip=True) if phone_el else ""

                if not full_name:
                    continue

                first, last = split_name(full_name)
                arc, seg = self._arc_for_industry(industry)

                contacts.append(self._record(
                    first_name=first,
                    last_name=last,
                    phone=phone,
                    org_name=org,
                    title=industry,
                    arc_type=arc,
                    segment=seg,
                    notes=f"BNI member — {industry}" if industry else "BNI member",
                ))

            random_delay(5, 8)

        self.log.info(f"BNI total: {len(contacts)}")
        return contacts


# ---------------------------------------------------------------------------
# SOURCE 3 — Greater Tyler Association of Realtors (GTAR)
# ---------------------------------------------------------------------------

class GTARScraper(BaseScraper):
    SOURCE_ID = "GTAR"
    SEARCH_URL = "https://www.gtar.net/find-a-realtor/"
    ALT_URL    = "https://www.gtar.net/members/"

    def scrape(self) -> list[dict]:
        contacts = []
        self.log.info("Fetching GTAR realtor directory…")

        # Try to find a JSON API endpoint via the search page first
        contacts = self._try_api() or self._try_html()
        self.log.info(f"GTAR total: {len(contacts)}")
        return contacts

    def _try_api(self) -> list[dict]:
        """Attempt to discover and use the underlying JSON search API."""
        contacts = []
        try:
            resp = self.session.get(self.SEARCH_URL, timeout=20)
            soup = BeautifulSoup(resp.text, "html.parser")

            # Look for inline JS that reveals an API endpoint
            for script in soup.find_all("script"):
                text = script.string or ""
                api_match = re.search(r'(https?://[^\s"\']+/api/[^\s"\']+)', text)
                if api_match:
                    api_url = api_match.group(1)
                    self.log.info(f"Found possible API: {api_url}")
                    data = self.session.get(api_url, timeout=20).json()
                    contacts = self._parse_api_response(data)
                    if contacts:
                        return contacts
        except Exception as e:
            self.log.warning(f"GTAR API probe failed: {e}")
        return []

    def _parse_api_response(self, data) -> list[dict]:
        contacts = []
        items = data if isinstance(data, list) else data.get("results", data.get("members", []))
        for item in items:
            if not isinstance(item, dict):
                continue
            first = item.get("first_name") or item.get("firstName", "")
            last  = item.get("last_name")  or item.get("lastName", "")
            email = item.get("email", "")
            phone = item.get("phone", "") or item.get("phoneNumber", "")
            org   = item.get("brokerage") or item.get("company", "")
            if not (first or last):
                continue
            contacts.append(self._record(
                first_name=first, last_name=last,
                email=email, phone=phone, org_name=org,
                arc_type="Safety", segment=11,
                notes="Realtor — alone in properties — Safety arc — hook: showing safety",
            ))
        return contacts

    def _try_html(self) -> list[dict]:
        contacts = []
        for url in [self.SEARCH_URL, self.ALT_URL]:
            try:
                soup = soup_get(self.session, url)
                cards = soup.select(".realtor, .agent, .member-card, [class*='agent'], [class*='realtor']")
                for card in cards:
                    name_el  = card.select_one("[class*='name']")
                    email_el = card.select_one("a[href^='mailto:']")
                    phone_el = card.select_one("[class*='phone']")
                    biz_el   = card.select_one("[class*='broker'], [class*='company']")

                    full = name_el.get_text(strip=True) if name_el else ""
                    if not full:
                        continue
                    first, last = split_name(full)
                    email = ""
                    if email_el:
                        href = email_el.get("href", "")
                        email = href[7:].split("?")[0] if href.startswith("mailto:") else ""
                    phone = phone_el.get_text(strip=True) if phone_el else ""
                    org   = biz_el.get_text(strip=True) if biz_el else ""

                    contacts.append(self._record(
                        first_name=first, last_name=last,
                        email=email, phone=phone, org_name=org,
                        arc_type="Safety", segment=11,
                        notes="Realtor — alone in properties — Safety arc — hook: showing safety",
                    ))
                if contacts:
                    break
                random_delay()
            except Exception as e:
                self.log.warning(f"GTAR HTML {url} failed: {e}")
        return contacts


# ---------------------------------------------------------------------------
# SOURCE 4 — Smith County Sheriff's Office
# ---------------------------------------------------------------------------

class SCSoScraper(BaseScraper):
    SOURCE_ID = "SCSO"
    URLS = [
        "https://www.smithcountysheriff.com/staff-directory/",
        "https://www.smith-county.com/departments/sheriff/",
    ]

    def scrape(self) -> list[dict]:
        contacts = []
        self.log.info("Fetching SCSO staff directory…")
        for url in self.URLS:
            try:
                soup = soup_get(self.session, url)
                contacts = self._parse_html(soup)
                if contacts:
                    break
                random_delay()
            except Exception as e:
                self.log.warning(f"SCSO URL {url} failed: {e}")

        if not contacts:
            self.log.warning("SCSO HTML failed — check for PDF at source URLs manually.")

        self.log.info(f"SCSO total: {len(contacts)}")
        return contacts

    def _parse_html(self, soup: BeautifulSoup) -> list[dict]:
        contacts = []
        rows = soup.select("tr, .staff-item, .employee, [class*='staff'], [class*='directory']")
        for row in rows:
            cells = row.find_all(["td", "th", "span", "div"])
            text  = " | ".join(c.get_text(strip=True) for c in cells if c.get_text(strip=True))
            if not text:
                continue

            emails = _email_re.findall(text)
            email  = emails[0] if emails else ""
            name_match = re.match(r"^([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-zA-Z'\-]+)", text)
            full_name  = name_match.group(1) if name_match else ""
            if not full_name:
                continue

            first, last = split_name(full_name)
            phone_match = re.search(r"\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}", text)
            phone = phone_match.group() if phone_match else ""
            title_match = re.search(r"\|\s*([A-Za-z\s/]+?)\s*\|", text)
            title = title_match.group(1).strip() if title_match else ""

            contacts.append(self._record(
                first_name=first, last_name=last,
                email=email, phone=phone,
                org_name="Smith County Sheriff's Office",
                title=title,
                arc_type="LE/Mil", segment=8,
                notes="SCSO — LE arc — consider command-level partnership conversation first",
            ))
        return contacts


# ---------------------------------------------------------------------------
# SOURCE 5 — Tyler ISD School Directory
# ---------------------------------------------------------------------------

class TylerISDScraper(BaseScraper):
    SOURCE_ID = "TYLER_ISD"
    CAMPUS_LIST_URL = "https://www.tylerisd.org/domain/12"

    def scrape(self) -> list[dict]:
        contacts = []
        self.log.info("Fetching Tyler ISD campus list…")

        try:
            soup = soup_get(self.session, self.CAMPUS_LIST_URL)
        except Exception as e:
            self.log.error(f"Tyler ISD campus list failed: {e}")
            return contacts

        campus_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/staff" in href or "/directory" in href:
                full = href if href.startswith("http") else f"https://www.tylerisd.org{href}"
                if full not in campus_links:
                    campus_links.append(full)

        # Also try standard per-campus staff patterns
        for link in soup.select("a[href]"):
            href = link["href"]
            if "tylerisd.org" in href and href not in campus_links:
                campus_links.append(href)

        self.log.info(f"Found {len(campus_links)} campus pages to check.")

        for campus_url in campus_links:
            try:
                campus_soup = soup_get(self.session, campus_url)
                campus_name = campus_soup.find("h1") or campus_soup.find("title")
                campus_label = campus_name.get_text(strip=True) if campus_name else campus_url

                staff_rows = campus_soup.select(
                    ".staff, .employee, tr, [class*='staff'], [class*='teacher']"
                )
                for row in staff_rows:
                    name_el  = row.select_one("[class*='name'], td:first-child")
                    email_el = row.select_one("a[href^='mailto:']")
                    title_el = row.select_one("[class*='title'], [class*='position'], td:nth-child(2)")

                    full  = name_el.get_text(strip=True) if name_el else ""
                    title = title_el.get_text(strip=True) if title_el else ""
                    email = ""
                    if email_el:
                        href = email_el.get("href", "")
                        email = href[7:].split("?")[0] if href.startswith("mailto:") else ""
                    else:
                        found = _email_re.search(row.get_text())
                        email = found.group() if found else ""

                    if not full or full.lower() in ("name", "staff", "employee"):
                        continue

                    first, last = split_name(full)
                    contacts.append(self._record(
                        first_name=first, last_name=last,
                        email=email,
                        org_name="Tyler ISD",
                        title=title,
                        arc_type="Parent", segment=1,
                        notes=f"Tyler ISD staff — {campus_label} — Parent arc",
                    ))

                random_delay(3, 5)
            except Exception as e:
                self.log.warning(f"Campus {campus_url} failed: {e}")

        self.log.info(f"TYLER_ISD total: {len(contacts)}")
        return contacts


# ---------------------------------------------------------------------------
# SOURCE 6 — Tyler Young Professionals
# ---------------------------------------------------------------------------

class TYPScraper(BaseScraper):
    SOURCE_ID = "TYP"
    URLS = [
        "https://typtyler.com/leadership/",
        "https://typtyler.com/board/",
        "https://www.tylertexas.com/typ/",
    ]

    # Simple heuristic first-name gender inference
    FEMALE_NAMES = {
        "ashley", "amanda", "jessica", "sarah", "emily", "brittany", "stephanie",
        "jennifer", "nicole", "melissa", "elizabeth", "rachel", "lauren", "megan",
        "taylor", "madison", "kayla", "alexis", "hannah", "samantha", "anna",
        "victoria", "morgan", "destiny", "chelsea", "andrea", "kaitlyn", "allison",
        "brianna", "danielle", "natalie", "mary", "patricia", "linda", "barbara",
        "margaret", "lisa", "betty", "dorothy", "sandra", "donna", "carol", "ruth",
        "sharon", "michelle", "laura", "sara", "diana", "heather", "amber", "courtney",
        "kelsey", "katelyn", "paige", "holly", "erica", "abigail", "sophia", "olivia",
        "ava", "isabella", "mia", "charlotte", "amelia", "harper", "evelyn", "ella",
        "chloe", "penelope", "lily", "grace", "zoey", "nora", "riley", "leah",
        "claire", "ellie", "sofia", "scarlett", "victoria", "brooklyn",
    }

    def _infer_arc(self, first_name: str) -> tuple[str, int]:
        if first_name.lower() in self.FEMALE_NAMES:
            return "Safety", 2
        return "Default", 3

    def scrape(self) -> list[dict]:
        contacts = []
        self.log.info("Fetching TYP leadership…")

        for url in self.URLS:
            try:
                soup = soup_get(self.session, url)
                members = soup.select(
                    ".board-member, .leader, .person, [class*='member'], [class*='leader'], [class*='officer']"
                )
                for m in members:
                    name_el  = m.select_one("[class*='name'], h3, h4, strong")
                    title_el = m.select_one("[class*='title'], [class*='role'], [class*='position'], p")
                    email_el = m.select_one("a[href^='mailto:']")

                    full  = name_el.get_text(strip=True) if name_el else ""
                    title = title_el.get_text(strip=True) if title_el else ""
                    email = ""
                    if email_el:
                        href = email_el.get("href", "")
                        email = href[7:].split("?")[0] if href.startswith("mailto:") else ""

                    if not full:
                        continue

                    first, last = split_name(full)
                    arc, seg = self._infer_arc(first)

                    contacts.append(self._record(
                        first_name=first, last_name=last,
                        email=email,
                        org_name="Tyler Young Professionals",
                        title=title,
                        arc_type=arc, segment=seg,
                        notes="TYP — young professional — route women → Safety arc, men → Default",
                    ))

                if contacts:
                    break
                random_delay()
            except Exception as e:
                self.log.warning(f"TYP {url} failed: {e}")

        self.log.info(f"TYP total: {len(contacts)}")
        return contacts


# ---------------------------------------------------------------------------
# SOURCE 7 — Junior League of Tyler
# ---------------------------------------------------------------------------

class JLTylerScraper(BaseScraper):
    SOURCE_ID = "JL_TYLER"
    URLS = [
        "https://www.jltyler.org/about/leadership/",
        "https://www.jltyler.org/about/board/",
        "https://www.jltyler.org/committees/",
    ]

    def scrape(self) -> list[dict]:
        contacts = []
        self.log.info("Fetching JL Tyler leadership…")

        for url in self.URLS:
            try:
                soup = soup_get(self.session, url)
                members = soup.select(
                    ".board-member, .leader, .officer, [class*='member'], [class*='leader'], [class*='chair']"
                )

                for m in members:
                    name_el  = m.select_one("[class*='name'], h3, h4, strong, b")
                    title_el = m.select_one("[class*='title'], [class*='role'], p, em, i")
                    email_el = m.select_one("a[href^='mailto:']")

                    full  = name_el.get_text(strip=True) if name_el else ""
                    title = title_el.get_text(strip=True) if title_el else ""
                    email = ""
                    if email_el:
                        href = email_el.get("href", "")
                        email = href[7:].split("?")[0] if href.startswith("mailto:") else ""

                    if not full:
                        continue

                    first, last = split_name(full)
                    contacts.append(self._record(
                        first_name=first, last_name=last,
                        email=email,
                        org_name="Junior League of Tyler",
                        title=title,
                        arc_type="Safety", segment=2,
                        notes="JL Tyler — community leader — high-value warm outreach — personalize by role",
                    ))

                random_delay()
            except Exception as e:
                self.log.warning(f"JL Tyler {url} failed: {e}")

        self.log.info(f"JL_TYLER total: {len(contacts)}")
        return contacts


# ---------------------------------------------------------------------------
# SOURCE 8 — Rotary Club of Tyler
# ---------------------------------------------------------------------------

class RotaryScraper(BaseScraper):
    SOURCE_ID = "ROTARY"
    URLS = [
        "https://www.tylerrotary.org/board/",
        "https://www.tylerrotary.org/members/",
        "https://www.tylerrotary.org/about/",
        "https://tylerrotaryclub.com/members/",
        "https://tylerrotaryclub.com/board/",
    ]

    def scrape(self) -> list[dict]:
        contacts = []
        self.log.info("Fetching Rotary Tyler leadership…")

        for url in self.URLS:
            try:
                soup = soup_get(self.session, url)
                members = soup.select(
                    ".member, .officer, .board-member, [class*='member'], tr, li"
                )
                for m in members:
                    name_el  = m.select_one("[class*='name'], td:first-child, h3, h4, strong")
                    title_el = m.select_one("[class*='title'], [class*='role'], td:nth-child(2), p")
                    email_el = m.select_one("a[href^='mailto:']")

                    full  = name_el.get_text(strip=True) if name_el else ""
                    title = title_el.get_text(strip=True) if title_el else ""
                    email = ""
                    if email_el:
                        href = email_el.get("href", "")
                        email = href[7:].split("?")[0] if href.startswith("mailto:") else ""

                    if not full or len(full) < 4:
                        continue

                    first, last = split_name(full)
                    contacts.append(self._record(
                        first_name=first, last_name=last,
                        email=email,
                        org_name="Rotary Club of Tyler",
                        title=title,
                        arc_type="Default", segment=3,
                        notes="Rotary Tyler — Default arc — civic/professional",
                    ))

                random_delay()
            except Exception as e:
                self.log.warning(f"Rotary {url} failed: {e}")

        self.log.info(f"ROTARY total: {len(contacts)}")
        return contacts


# ---------------------------------------------------------------------------
# SOURCE 9 — VFW / American Legion Tyler
# ---------------------------------------------------------------------------

class VetOrgsScraper(BaseScraper):
    SOURCE_ID = "VET_ORGS"
    URLS = [
        "https://vfw8904.org",
        "https://vfw8904.org/officers/",
        "https://vfw8904.org/leadership/",
    ]

    def scrape(self) -> list[dict]:
        contacts = []
        self.log.info("Fetching VFW/Legion officer contacts…")

        for url in self.URLS:
            try:
                soup = soup_get(self.session, url)
                officers = soup.select(
                    ".officer, .board, [class*='officer'], [class*='commander'], tr, li"
                )
                for o in officers:
                    name_el  = o.select_one("[class*='name'], td:first-child, h3, h4, strong, b")
                    title_el = o.select_one("[class*='title'], [class*='rank'], [class*='role'], td:nth-child(2), p")
                    email_el = o.select_one("a[href^='mailto:']")
                    phone_el = o.select_one("[class*='phone'], td:nth-child(3)")

                    full  = name_el.get_text(strip=True) if name_el else ""
                    title = title_el.get_text(strip=True) if title_el else ""
                    email = ""
                    if email_el:
                        href = email_el.get("href", "")
                        email = href[7:].split("?")[0] if href.startswith("mailto:") else ""
                    phone = phone_el.get_text(strip=True) if phone_el else ""

                    if not full or len(full) < 4:
                        continue

                    first, last = split_name(full)
                    contacts.append(self._record(
                        first_name=first, last_name=last,
                        email=email, phone=phone,
                        org_name="VFW Post 8904 / American Legion Tyler",
                        title=title,
                        arc_type="LE/Mil", segment=8,
                        notes="VFW/Legion — LE/Mil arc — use Seg. 8 tactical voice — no fitness framing",
                    ))

                random_delay()
            except Exception as e:
                self.log.warning(f"VetOrgs {url} failed: {e}")

        self.log.info(f"VET_ORGS total: {len(contacts)}")
        return contacts


# ---------------------------------------------------------------------------
# SOURCE 10 — East Texas Homeschool / THSC Tyler
# ---------------------------------------------------------------------------

class HomeschoolScraper(BaseScraper):
    SOURCE_ID = "HOMESCHOOL"
    URLS = [
        "https://thsc.org/find-a-group/?location=Tyler%2C+TX",
        "https://www.setaonline.org/groups/",
    ]

    def scrape(self) -> list[dict]:
        contacts = []
        self.log.info("Fetching THSC/homeschool group contacts…")

        for url in self.URLS:
            try:
                html = self._fetch_js(url)
                soup = BeautifulSoup(html, "html.parser")
                groups = soup.select(
                    ".group, .co-op, [class*='group'], [class*='chapter'], [class*='coop'], li, tr"
                )
                for g in groups:
                    name_el    = g.select_one("[class*='name'], h3, h4, strong")
                    contact_el = g.select_one("[class*='contact'], [class*='leader'], [class*='director']")
                    email_el   = g.select_one("a[href^='mailto:']")
                    phone_el   = g.select_one("[class*='phone']")

                    org  = name_el.get_text(strip=True) if name_el else ""
                    full = contact_el.get_text(strip=True) if contact_el else ""
                    email = ""
                    if email_el:
                        href = email_el.get("href", "")
                        email = href[7:].split("?")[0] if href.startswith("mailto:") else ""
                    phone = phone_el.get_text(strip=True) if phone_el else ""

                    if not org and not full:
                        continue

                    first, last = split_name(full) if full else (org, "")
                    contacts.append(self._record(
                        first_name=first, last_name=last,
                        email=email, phone=phone,
                        org_name=org or "Tyler Homeschool Co-op",
                        arc_type="Parent", segment=12,
                        notes="Homeschool/THSC — Parent arc — youth + character framing — offer co-op presentation",
                    ))

                random_delay(3, 5)
            except Exception as e:
                self.log.warning(f"Homeschool {url} failed: {e}")

        self.log.info(f"HOMESCHOOL total: {len(contacts)}")
        return contacts


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

SCRAPERS: dict[str, type[BaseScraper]] = {
    "CHAMBER":    ChamberScraper,
    "GTAR":       GTARScraper,
    "SCSO":       SCSoScraper,
    "BNI":        BNIScraper,
    "TYLER_ISD":  TylerISDScraper,
    "TYP":        TYPScraper,
    "JL_TYLER":   JLTylerScraper,
    "ROTARY":     RotaryScraper,
    "VET_ORGS":   VetOrgsScraper,
    "HOMESCHOOL": HomeschoolScraper,
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(sources: list[str], output_path: Path):
    all_contacts = []

    for source_id in sources:
        cls = SCRAPERS.get(source_id)
        if not cls:
            log.warning(f"Unknown source ID: {source_id} — skipping.")
            continue
        log.info(f"=== Running scraper: {source_id} ===")
        try:
            contacts = cls().scrape()
            all_contacts.extend(contacts)
            log.info(f"{source_id} done — {len(contacts)} contacts collected.")
        except Exception as e:
            log.error(f"{source_id} scraper raised an unhandled error: {e}", exc_info=True)

    log.info(f"Total before dedup: {len(all_contacts)}")
    deduped = deduplicate(all_contacts)
    log.info(f"Total after dedup:  {len(deduped)}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(deduped)

    log.info(f"Output written to: {output_path}")
    print(f"\n✓ {len(deduped)} contacts → {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Smith County Contact Scraper — ETKM ACQ")
    parser.add_argument(
        "--sources", nargs="*", default=PRIORITY_ORDER,
        metavar="SOURCE_ID",
        help=f"Source IDs to run (default: all in priority order). Choices: {', '.join(PRIORITY_ORDER)}",
    )
    parser.add_argument(
        "--output", default=f"smith_county_contacts_{date.today().isoformat()}.csv",
        help="Output CSV file path",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    log.info(f"Sources: {args.sources}")
    log.info(f"Output:  {output_path}")

    run(args.sources, output_path)


if __name__ == "__main__":
    main()
