"""
extractor.py — Contact extraction engine
Pulls emails, phones, names, URLs, and social links from raw HTML.
"""

import re
from dataclasses import dataclass, field, asdict
from typing import Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

try:
    import phonenumbers
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False


# ── Patterns ──────────────────────────────────────────────────────────────────

EMAIL_RE = re.compile(
    r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
    re.IGNORECASE
)

# Obfuscated email patterns: "user [at] domain [dot] com"
OBFUSCATED_RE = re.compile(
    r'([a-zA-Z0-9._%+\-]+)\s*[\[\(]?\s*at\s*[\]\)]?\s*([a-zA-Z0-9.\-]+)\s*[\[\(]?\s*dot\s*[\]\)]?\s*([a-zA-Z]{2,})',
    re.IGNORECASE
)

PHONE_RE = re.compile(
    r'(?:(?:\+?1[\s.\-]?)?(?:\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4})|'
    r'(?:\+\d{1,3}[\s.\-]?\d{1,4}[\s.\-]?\d{1,4}[\s.\-]?\d{1,9}))',
)

SOCIAL_DOMAINS = {
    "linkedin": "linkedin.com",
    "twitter": "twitter.com",
    "facebook": "facebook.com",
    "instagram": "instagram.com",
    "youtube": "youtube.com",
    "tiktok": "tiktok.com",
}


@dataclass
class ContactRecord:
    source_url: str
    emails: list[str] = field(default_factory=list)
    phones: list[str] = field(default_factory=list)
    name: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    social_links: dict[str, str] = field(default_factory=dict)
    page_title: Optional[str] = None

    def is_empty(self) -> bool:
        return not self.emails and not self.phones

    def to_dict(self) -> dict:
        return asdict(self)

    def merge(self, other: "ContactRecord") -> "ContactRecord":
        """Merge another record's data into this one (dedup)."""
        self.emails = list(set(self.emails + other.emails))
        self.phones = list(set(self.phones + other.phones))
        self.social_links.update(other.social_links)
        if not self.name and other.name:
            self.name = other.name
        if not self.company and other.company:
            self.company = other.company
        return self


def extract_contacts(html: str, source_url: str = "") -> ContactRecord:
    """
    Master extraction function. Pass raw HTML, get back a ContactRecord.
    """
    record = ContactRecord(source_url=source_url)
    soup = BeautifulSoup(html, "lxml")

    # Page title
    if soup.title:
        record.page_title = soup.title.get_text(strip=True)

    # Remove script/style noise before text extraction
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    full_text = soup.get_text(separator=" ")

    # ── Emails ───────────────────────────────────────────────────────────────
    # 1. Standard regex on full text
    found_emails = set(EMAIL_RE.findall(full_text))

    # 2. mailto: href attributes
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("mailto:"):
            email = href[7:].split("?")[0].strip()
            if email:
                found_emails.add(email)

    # 3. data-email / data-cfemail attributes (Cloudflare obfuscation)
    for el in soup.find_all(attrs={"data-email": True}):
        found_emails.add(el["data-email"])

    # 4. Obfuscated "user [at] domain [dot] com"
    for match in OBFUSCATED_RE.finditer(full_text):
        reconstructed = f"{match.group(1)}@{match.group(2)}.{match.group(3)}"
        found_emails.add(reconstructed)

    # Filter junk / image file emails
    record.emails = [
        e.lower() for e in found_emails
        if not any(e.lower().endswith(ext) for ext in [".png", ".jpg", ".gif", ".svg", ".webp"])
        and "example" not in e.lower()
        and "noreply" not in e.lower()
        and len(e) < 100
    ]

    # ── Phones ───────────────────────────────────────────────────────────────
    found_phones = set()

    # tel: href
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("tel:"):
            phone = href[4:].strip()
            if phone:
                found_phones.add(phone)

    # Regex on text
    raw_phones = PHONE_RE.findall(full_text)
    for ph in raw_phones:
        cleaned = re.sub(r"[^\d+\-\s\(\)\.x]", "", ph).strip()
        if len(re.sub(r"\D", "", cleaned)) >= 10:
            found_phones.add(cleaned)

    # Validate with phonenumbers if available
    if PHONENUMBERS_AVAILABLE:
        validated = set()
        for ph in found_phones:
            try:
                parsed = phonenumbers.parse(ph, "US")
                if phonenumbers.is_valid_number(parsed):
                    formatted = phonenumbers.format_number(
                        parsed, phonenumbers.PhoneNumberFormat.NATIONAL
                    )
                    validated.add(formatted)
            except Exception:
                # Keep raw if parse fails but looks like a real number
                if len(re.sub(r"\D", "", ph)) == 10:
                    validated.add(ph)
        record.phones = list(validated)
    else:
        record.phones = list(found_phones)

    # ── Social links ─────────────────────────────────────────────────────────
    for a in soup.find_all("a", href=True):
        href = a["href"]
        for platform, domain in SOCIAL_DOMAINS.items():
            if domain in href and platform not in record.social_links:
                record.social_links[platform] = href

    # ── Name / Title / Company heuristics ────────────────────────────────────
    # Check common meta tags
    for meta in soup.find_all("meta"):
        name_attr = meta.get("name", "").lower()
        prop_attr = meta.get("property", "").lower()
        content = meta.get("content", "")
        if name_attr == "author" or prop_attr == "og:site_name":
            if not record.company:
                record.company = content
        if prop_attr == "og:title" and not record.name:
            record.page_title = content

    # Schema.org structured data
    for script in soup.find_all("script", {"type": "application/ld+json"}):
        try:
            import json
            data = json.loads(script.string or "{}")
            types = data.get("@type", "")
            if isinstance(types, str):
                types = [types]
            if any(t in ["Person", "Organization", "LocalBusiness"] for t in types):
                if not record.name:
                    record.name = data.get("name")
                if not record.company:
                    record.company = data.get("name") or data.get("legalName")
                if not record.address:
                    addr = data.get("address", {})
                    if isinstance(addr, dict):
                        record.address = ", ".join(filter(None, [
                            addr.get("streetAddress"),
                            addr.get("addressLocality"),
                            addr.get("addressRegion"),
                            addr.get("postalCode"),
                        ]))
                # Grab email/phone from schema too
                if schema_email := data.get("email"):
                    record.emails = list(set(record.emails + [schema_email]))
                if schema_phone := data.get("telephone"):
                    record.phones = list(set(record.phones + [schema_phone]))
        except Exception:
            pass

    return record
