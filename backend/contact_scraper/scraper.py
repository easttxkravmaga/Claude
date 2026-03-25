"""
scraper.py — Async scraper engine
Handles static pages (httpx), JS-rendered pages (Playwright),
crawling, rate limiting, retries, and deduplication.
"""

import asyncio
import random
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from extractor import ContactRecord, extract_contacts


# ── Config ────────────────────────────────────────────────────────────────────

@dataclass
class ScraperConfig:
    # Concurrency
    max_concurrent: int = 10          # parallel requests
    max_per_domain: int = 3           # max simultaneous requests per domain

    # Delays (seconds)
    min_delay: float = 0.5
    max_delay: float = 2.0

    # Retries
    max_retries: int = 3
    retry_backoff: float = 2.0        # exponential backoff multiplier

    # Timeouts
    connect_timeout: float = 10.0
    read_timeout: float = 20.0

    # Crawling
    follow_links: bool = False        # crawl internal links found on pages
    max_depth: int = 2                # crawler depth limit
    max_pages_per_domain: int = 50    # safety cap

    # Rendering
    use_playwright: bool = False      # use headless browser for JS pages
    playwright_timeout: float = 15.0  # page load timeout

    # Filtering
    contact_pages_only: bool = True   # prioritize /contact, /about, etc.
    user_agent: str = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )


CONTACT_PAGE_HINTS = [
    "/contact", "/about", "/team", "/staff", "/people",
    "/reach", "/connect", "/get-in-touch", "/support",
    "/company", "/leadership", "/directory",
]


# ── Domain rate limiting ──────────────────────────────────────────────────────

class DomainLimiter:
    """Semaphore pool — one semaphore per domain."""

    def __init__(self, max_per_domain: int):
        self._max = max_per_domain
        self._locks: dict[str, asyncio.Semaphore] = defaultdict(
            lambda: asyncio.Semaphore(self._max)
        )

    def get(self, url: str) -> asyncio.Semaphore:
        domain = urlparse(url).netloc
        return self._locks[domain]


# ── Result container ──────────────────────────────────────────────────────────

@dataclass
class ScrapeResult:
    url: str
    success: bool
    record: Optional[ContactRecord] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    elapsed_ms: Optional[float] = None
    js_rendered: bool = False


@dataclass
class ScrapeSession:
    results: list[ScrapeResult] = field(default_factory=list)
    failed_urls: list[str] = field(default_factory=list)
    total_emails: int = 0
    total_phones: int = 0
    duration_seconds: float = 0.0

    def summary(self) -> dict:
        successful = [r for r in self.results if r.success and r.record and not r.record.is_empty()]
        return {
            "total_urls": len(self.results) + len(self.failed_urls),
            "successful": len(successful),
            "failed": len(self.failed_urls),
            "total_emails": self.total_emails,
            "total_phones": self.total_phones,
            "duration_seconds": round(self.duration_seconds, 2),
        }


# ── Static page fetcher ───────────────────────────────────────────────────────

async def fetch_static(
    client: httpx.AsyncClient,
    url: str,
    config: ScraperConfig,
    domain_limiter: DomainLimiter,
    retries: int = 0,
) -> tuple[Optional[str], int]:
    """Fetch page HTML with retry + domain rate limiting."""

    async with domain_limiter.get(url):
        # Random delay to be polite
        await asyncio.sleep(random.uniform(config.min_delay, config.max_delay))

        try:
            resp = await client.get(url)
            if resp.status_code == 200:
                return resp.text, resp.status_code
            elif resp.status_code in (429, 503) and retries < config.max_retries:
                wait = config.retry_backoff ** (retries + 1)
                await asyncio.sleep(wait)
                return await fetch_static(client, url, config, domain_limiter, retries + 1)
            else:
                return None, resp.status_code
        except (httpx.TimeoutException, httpx.ConnectError) as e:
            if retries < config.max_retries:
                wait = config.retry_backoff ** (retries + 1)
                await asyncio.sleep(wait)
                return await fetch_static(client, url, config, domain_limiter, retries + 1)
            raise e


# ── JS-rendered fetcher ───────────────────────────────────────────────────────

async def fetch_playwright(url: str, config: ScraperConfig) -> Optional[str]:
    """Use headless Chromium for JS-heavy pages."""
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                user_agent=config.user_agent,
                extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
            )
            await page.goto(url, timeout=int(config.playwright_timeout * 1000))
            # Wait for network to settle
            await page.wait_for_load_state("networkidle", timeout=int(config.playwright_timeout * 1000))
            html = await page.content()
            await browser.close()
            return html
    except Exception as e:
        return None


# ── Link discovery ────────────────────────────────────────────────────────────

def discover_contact_links(html: str, base_url: str, config: ScraperConfig) -> list[str]:
    """Find internal links worth scraping (contact/about pages first)."""
    soup = BeautifulSoup(html, "lxml")
    base_domain = urlparse(base_url).netloc
    found = []

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        # Same domain only
        if parsed.netloc != base_domain:
            continue
        # No files
        if any(parsed.path.endswith(ext) for ext in [".pdf", ".jpg", ".png", ".zip", ".doc"]):
            continue

        url_lower = full_url.lower()
        is_contact_page = any(hint in url_lower for hint in CONTACT_PAGE_HINTS)

        if config.contact_pages_only and is_contact_page:
            found.insert(0, full_url)  # Prioritize
        elif not config.contact_pages_only:
            found.append(full_url)

    return list(dict.fromkeys(found))  # Dedup, preserve order


# ── Core scrape function ──────────────────────────────────────────────────────

async def scrape_url(
    client: httpx.AsyncClient,
    url: str,
    config: ScraperConfig,
    domain_limiter: DomainLimiter,
    semaphore: asyncio.Semaphore,
) -> ScrapeResult:
    """Scrape a single URL."""
    async with semaphore:
        t0 = time.monotonic()
        js_rendered = False

        try:
            html, status = await fetch_static(client, url, config, domain_limiter)

            # Fallback to Playwright if page looks JS-heavy or empty
            if (html is None or len(html) < 500) and config.use_playwright:
                html = await fetch_playwright(url, config)
                js_rendered = True
                status = 200 if html else status

            if not html:
                return ScrapeResult(
                    url=url, success=False,
                    error=f"HTTP {status}", status_code=status,
                    elapsed_ms=round((time.monotonic() - t0) * 1000, 1)
                )

            record = extract_contacts(html, source_url=url)
            return ScrapeResult(
                url=url, success=True,
                record=record, status_code=status,
                elapsed_ms=round((time.monotonic() - t0) * 1000, 1),
                js_rendered=js_rendered,
            )

        except Exception as e:
            return ScrapeResult(
                url=url, success=False,
                error=str(e),
                elapsed_ms=round((time.monotonic() - t0) * 1000, 1)
            )


# ── Crawler (optional follow-links mode) ─────────────────────────────────────

async def crawl_domain(
    client: httpx.AsyncClient,
    start_url: str,
    config: ScraperConfig,
    domain_limiter: DomainLimiter,
    semaphore: asyncio.Semaphore,
) -> list[ScrapeResult]:
    """Crawl a domain up to max_depth, collecting all contacts."""
    visited = set()
    queue = [(start_url, 0)]  # (url, depth)
    all_results = []

    while queue and len(visited) < config.max_pages_per_domain:
        batch = []
        while queue and len(batch) < config.max_concurrent:
            url, depth = queue.pop(0)
            if url not in visited:
                visited.add(url)
                batch.append((url, depth))

        if not batch:
            break

        tasks = [
            scrape_url(client, url, config, domain_limiter, semaphore)
            for url, _ in batch
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for (url, depth), result in zip(batch, results):
            if isinstance(result, ScrapeResult):
                all_results.append(result)
                # Discover more links if under depth limit
                if result.success and depth < config.max_depth and result.record:
                    # Re-fetch html for link discovery (stored in result ideally)
                    # For crawling, we also stored html — simplified here
                    pass

    return all_results


# ── Main batch scraper ────────────────────────────────────────────────────────

async def scrape_batch(
    urls: list[str],
    config: Optional[ScraperConfig] = None,
    progress_callback=None,
) -> ScrapeSession:
    """
    Main entry point. Scrape a list of URLs concurrently.
    Returns a ScrapeSession with all results.
    """
    if config is None:
        config = ScraperConfig()

    session = ScrapeSession()
    t0 = time.monotonic()

    semaphore = asyncio.Semaphore(config.max_concurrent)
    domain_limiter = DomainLimiter(config.max_per_domain)

    headers = {
        "User-Agent": config.user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    timeout = httpx.Timeout(
        connect=config.connect_timeout,
        read=config.read_timeout,
        write=10.0,
        pool=5.0,
    )

    async with httpx.AsyncClient(
        headers=headers,
        timeout=timeout,
        follow_redirects=True,
        verify=False,   # Skip SSL errors on corporate/old sites
    ) as client:

        tasks = [
            scrape_url(client, url, config, domain_limiter, semaphore)
            for url in urls
        ]

        completed = 0
        for coro in asyncio.as_completed(tasks):
            result = await coro
            session.results.append(result)
            completed += 1

            if not result.success:
                session.failed_urls.append(result.url)
            elif result.record:
                session.total_emails += len(result.record.emails)
                session.total_phones += len(result.record.phones)

            if progress_callback:
                progress_callback(completed, len(urls), result)

    session.duration_seconds = time.monotonic() - t0
    return session
