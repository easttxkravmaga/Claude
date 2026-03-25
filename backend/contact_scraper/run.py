"""
run.py — CLI runner + MCP tool wrapper
Usage:
  python run.py --urls "https://example.com" "https://site2.com"
  python run.py --file urls.txt --output results/contacts --playwright
  python run.py --url "https://example.com" --crawl --depth 2

MCP tool function: scrape_contacts() — callable by Claude Code or ETKM MCP server.
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

from scraper import ScraperConfig, scrape_batch, ScrapeSession
from exporter import export_both, print_summary, deduplicate_records


# ── Progress printer ──────────────────────────────────────────────────────────

def make_progress_printer(quiet: bool = False):
    def callback(completed: int, total: int, result):
        if quiet:
            return
        status = "✓" if result.success else "✗"
        contacts = ""
        if result.record and not result.record.is_empty():
            e = len(result.record.emails)
            p = len(result.record.phones)
            contacts = f" [{e}e {p}p]"
        url_short = result.url[:60] + ("…" if len(result.url) > 60 else "")
        print(f"  [{completed}/{total}] {status} {url_short}{contacts}")
    return callback


# ── MCP-callable function ─────────────────────────────────────────────────────

async def scrape_contacts(
    urls: list[str],
    output_dir: str = "scraper_output",
    use_playwright: bool = False,
    follow_links: bool = False,
    max_concurrent: int = 10,
    contact_pages_only: bool = True,
) -> dict:
    """
    MCP Tool: scrape_contacts
    
    Parameters:
        urls             - List of URLs to scrape
        output_dir       - Directory to save CSV and JSON exports
        use_playwright   - Enable headless browser for JS-heavy sites
        follow_links     - Crawl internal links (contact/about pages)
        max_concurrent   - Max parallel requests (default: 10)
        contact_pages_only - Only follow links to contact/about/team pages

    Returns:
        {
            "summary": {...},
            "contacts": [...],
            "exports": {"csv": "path.csv", "json": "path.json"}
        }
    """
    config = ScraperConfig(
        use_playwright=use_playwright,
        follow_links=follow_links,
        max_concurrent=max_concurrent,
        contact_pages_only=contact_pages_only,
    )

    session = await scrape_batch(
        urls=urls,
        config=config,
        progress_callback=make_progress_printer(quiet=False),
    )

    # Export
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = str(Path(output_dir) / f"contacts_{timestamp}")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    exports = export_both(session, base_path)

    # Build return payload
    records = deduplicate_records(session)
    contacts_data = []
    for r in records:
        contacts_data.append({
            "source_url": r.source_url,
            "emails": r.emails,
            "phones": r.phones,
            "name": r.name,
            "company": r.company,
            "page_title": r.page_title,
            "social_links": r.social_links,
        })

    return {
        "summary": session.summary(),
        "contacts": contacts_data,
        "exports": {
            "csv": exports["csv"]["path"],
            "json": exports["json"]["path"],
            "record_count": exports["csv"]["records"],
        },
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Async contact scraper — emails, phones, social links",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape two URLs
  python run.py --urls https://example.com https://company.com

  # Scrape from a file of URLs
  python run.py --file urls.txt

  # Enable JS rendering + crawl internal links
  python run.py --urls https://example.com --playwright --crawl

  # Full power mode
  python run.py --file urls.txt --playwright --crawl --depth 3 --concurrent 15 --output my_results
        """
    )

    # Input
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--urls", nargs="+", help="One or more URLs to scrape")
    input_group.add_argument("--file", help="Path to a text file with one URL per line")

    # Output
    parser.add_argument(
        "--output", default="scraper_output/contacts",
        help="Base output path (no extension). Default: scraper_output/contacts"
    )

    # Behavior
    parser.add_argument("--playwright", action="store_true", help="Use headless browser for JS pages")
    parser.add_argument("--crawl", action="store_true", help="Follow internal links to contact/about pages")
    parser.add_argument("--all-links", action="store_true", help="Follow ALL internal links (not just contact pages)")
    parser.add_argument("--depth", type=int, default=2, help="Crawl depth (default: 2)")
    parser.add_argument("--concurrent", type=int, default=10, help="Max concurrent requests (default: 10)")
    parser.add_argument("--no-dedup", action="store_true", help="Skip deduplication")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")
    parser.add_argument("--json-only", action="store_true", help="Output results to stdout as JSON (no files)")

    return parser.parse_args()


async def main():
    args = parse_args()

    # Load URLs
    if args.urls:
        urls = args.urls
    else:
        with open(args.file) as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not urls:
        print("No URLs provided. Exiting.")
        sys.exit(1)

    print(f"\n  Starting scrape of {len(urls)} URL(s)...")
    if args.playwright:
        print("  Mode: JS-rendering ON (Playwright)")
    if args.crawl:
        depth = args.depth
        print(f"  Mode: Crawling ON (depth={depth}, {'all links' if args.all_links else 'contact pages only'})")
    print()

    config = ScraperConfig(
        use_playwright=args.playwright,
        follow_links=args.crawl,
        max_depth=args.depth,
        max_concurrent=args.concurrent,
        contact_pages_only=not args.all_links,
    )

    session = await scrape_batch(
        urls=urls,
        config=config,
        progress_callback=make_progress_printer(quiet=args.quiet),
    )

    if args.json_only:
        records = deduplicate_records(session)
        output = {
            "summary": session.summary(),
            "contacts": [
                {
                    "emails": r.emails,
                    "phones": r.phones,
                    "name": r.name,
                    "company": r.company,
                    "source_url": r.source_url,
                    "page_title": r.page_title,
                    "social_links": r.social_links,
                }
                for r in records
            ],
        }
        print(json.dumps(output, indent=2))
        return

    # Export files
    exports = export_both(session, args.output, deduplicate=not args.no_dedup)
    print_summary(session)
    print(f"  Exports saved:")
    print(f"    CSV  → {exports['csv']['path']}  ({exports['csv']['records']} records)")
    print(f"    JSON → {exports['json']['path']}  ({exports['json']['records']} records)")
    print()


if __name__ == "__main__":
    asyncio.run(main())
