# SKILL: contact-scraper
Version: 1.0  
Location: `skills/contact-scraper/SKILL.md`

---

## PURPOSE

Run the ETKM contact scraper to extract emails, phones, and social links from any website. One command. Results delivered as `output/scrape_contacts.xlsx`.

---

## WHEN TO LOAD THIS SKILL

Load when Nate says any of:
- "scrape [any URL or list of URLs]"
- "/scrape [URL]"
- "scrape this site"
- "get contacts from"
- "find emails on"
- "pull contacts from these URLs"
- "who's the contact at [company/site]"

---

## SCRAPER LOCATION

```
skills/contact-scraper/scraper/
├── run.py          ← entry point
├── scraper.py      ← async fetch engine
├── extractor.py    ← email/phone/social parser
├── exporter.py     ← CSV + JSON export
└── __init__.py
```

All output goes to: `scraper_output/contacts_[TIMESTAMP].csv` and `.json`

---

## HOW TO RUN — CLAUDE CODE COMMANDS

### Single URL
```bash
cd skills/contact-scraper/scraper
python run.py --urls https://example.com
```

### Multiple URLs
```bash
python run.py --urls https://site1.com https://site2.com https://site3.com
```

### From a file (one URL per line)
```bash
python run.py --file urls.txt
```

### Crawl contact/about/team pages automatically
```bash
python run.py --urls https://example.com --crawl
```

### JS-heavy sites (React, Angular, etc.)
```bash
python run.py --urls https://example.com --playwright
```

### Full power — crawl + JS rendering
```bash
python run.py --file urls.txt --playwright --crawl --output results/batch
```

### Return JSON to this chat (no file saved)
```bash
python run.py --urls https://example.com --json-only
```

---

## INSTALL (first time only)

```bash
pip install httpx beautifulsoup4 lxml phonenumbers playwright --break-system-packages
playwright install chromium
```

---

## WHAT IT EXTRACTS

| Field | Source |
|---|---|
| Emails | Regex, mailto: links, data-email attrs, [at] obfuscation, schema.org |
| Phones | tel: links, regex, Google phonenumbers validation |
| Social links | LinkedIn, Twitter, Facebook, Instagram, YouTube, TikTok |
| Company name | og:site_name, schema.org Organization |
| Address | schema.org structured data |
| Page title | `<title>` tag |

---

## OUTPUT FORMAT

**CSV columns:**
`source_url | page_title | name | title | company | emails | phones | address | linkedin | twitter | facebook | instagram`

**JSON structure:**
```json
{
  "summary": {
    "total_urls": 5,
    "successful": 5,
    "total_emails": 12,
    "total_phones": 8,
    "duration_seconds": 4.2
  },
  "contacts": [
    {
      "source_url": "https://...",
      "emails": ["contact@company.com"],
      "phones": ["(555) 123-4567"],
      "company": "Company Name",
      "social_links": {"linkedin": "..."}
    }
  ]
}
```

---

## CLAUDE BEHAVIOR WHEN THIS SKILL IS LOADED

1. Take the URL(s) Nate provides
2. Run the appropriate command via Claude Code
3. Report back: how many contacts found, emails, phones — show a clean summary table
4. Offer to show the full CSV or open the output file
5. If zero results on a URL — try again with `--crawl` flag to hit the contact page
6. If site looks JS-rendered and returns empty — retry with `--playwright`

**Never ask Nate which flags to use. Pick the right ones based on the URL and results.**

---

## SPEED SETTINGS

| Scenario | Command |
|---|---|
| Fast single site | Default (no flags) |
| Directory / staff page | `--crawl` |
| Modern JS site | `--playwright` |
| Large batch (50+ URLs) | `--concurrent 20` |
| Be extra polite to site | `--concurrent 3` |
