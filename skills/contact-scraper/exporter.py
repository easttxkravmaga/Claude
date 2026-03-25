"""
exporter.py — Export and deduplication layer
Deduplicates across all results, exports to CSV and JSON.
"""

import csv
import json
import os
from datetime import datetime
from typing import Optional

from extractor import ContactRecord
from scraper import ScrapeSession


def deduplicate_records(session: ScrapeSession) -> list[ContactRecord]:
    """
    Merge records by email address. If two pages found the same email,
    combine their data into one enriched record.
    """
    email_index: dict[str, ContactRecord] = {}
    no_email_records: list[ContactRecord] = []

    for result in session.results:
        if not result.success or not result.record:
            continue
        record = result.record
        if record.is_empty():
            continue

        if record.emails:
            primary = record.emails[0].lower()
            if primary in email_index:
                email_index[primary].merge(record)
            else:
                email_index[primary] = record
        else:
            # Phone-only record
            no_email_records.append(record)

    return list(email_index.values()) + no_email_records


def _flatten_record(record: ContactRecord) -> dict:
    """Flatten nested fields to CSV-friendly format."""
    return {
        "source_url": record.source_url,
        "page_title": record.page_title or "",
        "name": record.name or "",
        "title": record.title or "",
        "company": record.company or "",
        "emails": "; ".join(record.emails),
        "phones": "; ".join(record.phones),
        "address": record.address or "",
        "linkedin": record.social_links.get("linkedin", ""),
        "twitter": record.social_links.get("twitter", ""),
        "facebook": record.social_links.get("facebook", ""),
        "instagram": record.social_links.get("instagram", ""),
    }


def export_csv(
    session: ScrapeSession,
    output_path: str,
    deduplicate: bool = True,
) -> int:
    """Export results to CSV. Returns number of rows written."""
    records = deduplicate_records(session) if deduplicate else [
        r.record for r in session.results
        if r.success and r.record and not r.record.is_empty()
    ]

    if not records:
        return 0

    fieldnames = [
        "source_url", "page_title", "name", "title", "company",
        "emails", "phones", "address",
        "linkedin", "twitter", "facebook", "instagram",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(_flatten_record(record))

    return len(records)


def export_json(
    session: ScrapeSession,
    output_path: str,
    deduplicate: bool = True,
    include_meta: bool = True,
) -> int:
    """Export results to JSON. Returns number of records written."""
    records = deduplicate_records(session) if deduplicate else [
        r.record for r in session.results
        if r.success and r.record and not r.record.is_empty()
    ]

    output = {
        "exported_at": datetime.utcnow().isoformat() + "Z",
        "summary": session.summary(),
        "contacts": [r.to_dict() for r in records],
    }

    if not include_meta:
        output = output["contacts"]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    return len(records)


def export_both(
    session: ScrapeSession,
    base_path: str,
    deduplicate: bool = True,
) -> dict:
    """Export to both CSV and JSON. Returns paths and counts."""
    os.makedirs(os.path.dirname(base_path) if os.path.dirname(base_path) else ".", exist_ok=True)

    csv_path = base_path + ".csv"
    json_path = base_path + ".json"

    csv_count = export_csv(session, csv_path, deduplicate)
    json_count = export_json(session, json_path, deduplicate)

    return {
        "csv": {"path": csv_path, "records": csv_count},
        "json": {"path": json_path, "records": json_count},
    }


def print_summary(session: ScrapeSession) -> None:
    """Print a clean summary to stdout."""
    s = session.summary()
    records = deduplicate_records(session)

    print("\n" + "═" * 50)
    print("  CONTACT SCRAPER — SESSION SUMMARY")
    print("═" * 50)
    print(f"  URLs processed : {s['total_urls']}")
    print(f"  Successful     : {s['successful']}")
    print(f"  Failed         : {s['failed']}")
    print(f"  Emails found   : {s['total_emails']}")
    print(f"  Phones found   : {s['total_phones']}")
    print(f"  Unique contacts: {len(records)}")
    print(f"  Duration       : {s['duration_seconds']}s")
    print("═" * 50)

    if records:
        print("\n  SAMPLE CONTACTS:")
        for r in records[:5]:
            print(f"  • {r.emails[0] if r.emails else r.phones[0] if r.phones else '?'}"
                  f"  |  {r.company or r.page_title or r.source_url[:40]}")
    print()
