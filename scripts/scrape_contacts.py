#!/usr/bin/env python3
"""
ETKM Contact Scraper
Uses Playwright with a real Chromium browser to bypass 403 blocks.
Usage:
    python3 scripts/scrape_contacts.py <url> [url2] [url3] ...
    python3 scripts/scrape_contacts.py --file urls.txt
Output: output/contacts.csv (appends each run)
"""

import sys
import re
import csv
import json
import argparse
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

CHROMIUM_PATH = "/root/.cache/ms-playwright/chromium-1194/chrome-linux/chrome"
OUTPUT_DIR = Path("/home/user/Claude/output")
OUTPUT_CSV = OUTPUT_DIR / "contacts.csv"

# Patterns for extracting contact info from raw text
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4})")
CSV_FIELDS = ["source_url", "name", "title", "email", "phone", "address", "department", "scraped_at"]


def fetch_page_text(url: str, timeout: int = 20000) -> tuple[str, str]:
    """Returns (page_text, page_title) using headless Chromium."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROMIUM_PATH,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"],
            headless=True,
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()
        # Hide automation markers
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        try:
            page.goto(url, wait_until="networkidle", timeout=timeout)
        except Exception:
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        title = page.title()
        text = page.inner_text("body")
        browser.close()
        return text, title


def extract_contacts(text: str, url: str) -> list[dict]:
    """
    Heuristic extraction of contact blocks from raw page text.
    Returns a list of contact dicts.
    """
    emails = EMAIL_RE.findall(text)
    phones = PHONE_RE.findall(text)
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # Build a simple contact per unique email found
    contacts = []
    used_emails = set()

    for email in emails:
        if email in used_emails:
            continue
        used_emails.add(email)

        # Look for a name/title near the email in the line list
        name, title, address, department = "", "", "", ""
        for i, line in enumerate(lines):
            if email in line:
                # Scan surrounding lines for name/title clues
                window = lines[max(0, i - 5):i + 5]
                for wline in window:
                    if email in wline:
                        continue
                    # Skip lines that are just phone numbers or URLs
                    if PHONE_RE.fullmatch(wline.strip()):
                        continue
                    if wline.startswith("http") or wline.startswith("www"):
                        continue
                    # First non-email, non-phone line nearby → likely a name or title
                    if not name and len(wline) < 60 and not any(
                        w in wline.lower() for w in ["©", "privacy", "cookie", "menu", "navigation"]
                    ):
                        name = wline
                    elif not title and len(wline) < 80:
                        title = wline
                break

        # Match a phone to this contact if only one phone on page, or leave blank
        phone = phones[0] if len(phones) == 1 else ""

        contacts.append({
            "source_url": url,
            "name": name,
            "title": title,
            "email": email,
            "phone": phone,
            "address": address,
            "department": department,
            "scraped_at": datetime.now().isoformat(timespec="seconds"),
        })

    # If no emails found, still record phones/address as a general org contact
    if not contacts and phones:
        contacts.append({
            "source_url": url,
            "name": "",
            "title": "",
            "email": "",
            "phone": phones[0],
            "address": "",
            "department": "",
            "scraped_at": datetime.now().isoformat(timespec="seconds"),
        })

    return contacts


def save_contacts(contacts: list[dict]):
    OUTPUT_DIR.mkdir(exist_ok=True)
    write_header = not OUTPUT_CSV.exists()
    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerows(contacts)


def scrape(url: str):
    print(f"\n→ Scraping: {url}")
    try:
        text, title = fetch_page_text(url)
        print(f"  Page: {title}")
        contacts = extract_contacts(text, url)
        if contacts:
            save_contacts(contacts)
            print(f"  Found {len(contacts)} contact(s):")
            for c in contacts:
                print(f"    {c['name'] or '(unnamed)':30s}  {c['title'] or '':35s}  {c['email']}  {c['phone']}")
        else:
            print("  No structured contacts found. Raw text sample:")
            print("  " + text[:500].replace("\n", " "))
    except Exception as e:
        print(f"  ERROR: {e}")


def main():
    parser = argparse.ArgumentParser(description="ETKM Contact Scraper")
    parser.add_argument("urls", nargs="*", help="One or more URLs to scrape")
    parser.add_argument("--file", help="Text file with one URL per line")
    args = parser.parse_args()

    urls = list(args.urls)
    if args.file:
        urls += [l.strip() for l in Path(args.file).read_text().splitlines() if l.strip()]

    if not urls:
        parser.print_help()
        sys.exit(1)

    for url in urls:
        scrape(url)

    print(f"\n✓ Contacts saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
