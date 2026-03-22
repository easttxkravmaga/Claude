# Smith County Contact Scraper — Developer Spec
**Project:** ACQ — Student Acquisition | East Texas Krav Maga
**Branch:** `claude/smith-county-training-contacts-PVM4I`
**Last Updated:** 2026-03-22
**Purpose:** Generate a clean, deduplicated contact list from 10 high-yield Smith County organizations, mapped to ETKM audience segments and Pipedrive arc types for cold outreach sequencing.

---

## Output Schema

Every scraped record must conform to this schema before import into Pipedrive:

```json
{
  "first_name": "string",
  "last_name":  "string",
  "email":      "string | null",
  "phone":      "string | null",
  "org_name":   "string",
  "source":     "SOURCE_ID (see below)",
  "title":      "string | null",
  "arc_type":   "Safety | Parent | Fitness | LE/Mil | Former MA | Default",
  "segment":    "integer (1–14)",
  "notes":      "string | null"
}
```

**Arc type** determines which arm of `WF-001 Pre-Trial Email Funnel` the contact enters.
**Segment** maps to the ETKM Master Audience Map.
**Source** must be recorded — tracks which list each contact came from for outreach personalization.

---

## Deduplication Rules

Run dedup **before** Pipedrive import:
1. Primary key: `email` (exact match)
2. Fallback key: `first_name + last_name + org_name` (case-insensitive)
3. If duplicate found across sources → keep record with most data fields populated, log both `source` values comma-separated
4. Strip all whitespace, normalize phone to `(###) ###-####` format
5. Normalize email to lowercase

---

## Source Specifications

---

### SOURCE 1 — Tyler Area Chamber of Commerce
**Source ID:** `CHAMBER`
**URL:** `https://www.tylertexas.com/business-directory/`
**Alt URL (member search):** `https://www.tylertexas.com/list/`
**Audience Segments:** Seg. 3 (Men), Seg. 13 (Corporate), Seg. 2 (Women)
**Arc Type:** `Default` (mixed professional — refine post-outreach)
**WF-001 Arm:** Default arc
**Volume Est.:** 500–1,500 members

**Extraction Method:** Paginated HTML
- The directory uses server-rendered HTML with pagination or a JS-rendered grid. Check for `?page=` or `?offset=` params on pagination.
- If JS-rendered, use Playwright/Puppeteer with headless Chrome — not raw requests.
- Each member card typically contains: business name, contact name, phone, address, website, sometimes email.

**Target Selectors (verify on live page):**
```
.member-card        → container
.member-name        → contact name
.member-business    → org name
.member-phone       → phone
.member-email       → email (may be obfuscated — check for mailto: href)
```

**Email Obfuscation:** Many chamber sites encode email as `data-email` or use rot13 — parse the `mailto:` href or decode as needed.

**Auth Required:** Some Chamber directories are public; others require login. Test first. If login-walled, flag for manual CSV export request via Nathan (Chamber membership gives export access).

**Rate Limit:** 1 request/3s. Randomize delay 2–5s between pages. Send `User-Agent: Mozilla/5.0` header.

**Normalization Notes:**
- Many listings will be businesses, not individuals. Extract primary contact name if present; otherwise set `first_name = org_name`, `last_name = ""` and flag for manual review.
- Set `notes = "Chamber member — verify contact name"`

---

### SOURCE 2 — BNI Tyler Chapters
**Source ID:** `BNI`
**URL:** `https://www.bni.com/find-a-chapter` → filter by Tyler, TX
**Audience Segments:** Seg. 2 (Women), Seg. 3 (Men), Seg. 13 (Corporate)
**Arc Type:** `Default`
**WF-001 Arm:** Default arc
**Volume Est.:** 80–200 contacts across 3–5 local chapters

**Extraction Method:** Multi-step HTML
1. Hit the chapter finder, search for Tyler TX, collect chapter page URLs
2. For each chapter page, extract the member roster

**BNI Chapter Pages:**
BNI Tyler typically has 2–4 active chapters. Known chapters to try:
- BNI Tyler (core chapter)
- BNI Cornerstone Tyler
- Search: `https://www.bni.com/find-a-chapter?location=Tyler%2C+TX`

**Target Data per Member:**
- Member name
- Business name
- Business category/industry (use to refine arc type — see mapping below)
- Phone
- Website (email rarely exposed publicly)

**Industry → Arc Type Mapping:**
| BNI Category | Arc Type Override |
|---|---|
| Real Estate | Safety (alone in properties — Seg. 11) |
| Healthcare / Nurse / Medical | Safety (Seg. 11) |
| Law Enforcement / Security | LE/Mil (Seg. 8) |
| Fitness / Gym | Fitness (Seg. 6) |
| Education | Parent (Seg. 1) |
| All others | Default |

**Auth Required:** BNI member rosters are often public on chapter pages. Some chapters use password-protected PDFs — flag these for manual follow-up.

**Rate Limit:** 1 request/5s. BNI has Cloudflare on main site — use Playwright.

---

### SOURCE 3 — Greater Tyler Association of Realtors (GTAR)
**Source ID:** `GTAR`
**URL:** `https://www.gtar.net/find-a-realtor/` (verify exact path)
**Alt:** `https://www.gtar.net/members/`
**Audience Segments:** Seg. 2 (Women — primary), Seg. 3 (Men), Seg. 11 (High-Risk Occupational)
**Arc Type:** `Safety`
**WF-001 Arm:** Safety arc
**Volume Est.:** 300–700 licensed agents

**Extraction Method:** HTML or API
- GTAR often uses a realtor search widget backed by a JSON API. Open DevTools → Network tab → search for a name → capture the XHR/fetch request and replicate it directly.
- Target fields: first name, last name, email, phone, brokerage

**Why Safety Arc:**
Realtors routinely show properties alone to strangers. This is the highest single-issue safety concern that ETKM directly solves. The Safety arc messaging maps perfectly — personalize cold outreach with this hook.

**Hook for Outreach (include in `notes` field):**
`"Realtor — alone in properties — Safety arc — hook: showing safety"`

**Rate Limit:** 1 request/3s. If JSON API found, pull in one batch — do not hammer paginated HTML.

---

### SOURCE 4 — Junior League of Tyler
**Source ID:** `JL_TYLER`
**URL:** `https://www.jltyler.org/about/leadership/` (or `/members/`)
**Audience Segments:** Seg. 2 (Adult Women — primary), Seg. 1 (Parents)
**Arc Type:** `Safety`
**WF-001 Arm:** Safety arc
**Volume Est.:** 20–60 contacts (leadership and committee chairs — not full membership)

**Extraction Method:** Manual-assisted HTML
- Junior League sites typically expose leadership/board rosters as static HTML with no pagination.
- Full membership lists are private. Only scrape publicly visible leadership + committee rosters.
- Expected fields: name, title/role, sometimes email (often listed on leadership pages)

**Target Pages:**
- `/about/leadership/`
- `/about/board/`
- `/committees/`

**Notes:**
- This is a warm-adjacent audience — these are community leaders who respond well to mission-aligned outreach.
- Do not cold-email with a generic blast. These contacts warrant personalized, cause-first messaging.
- Set `notes = "JL Tyler — community leader — high-value warm outreach — personalize by role"`

**Rate Limit:** Static pages — single fetch, no rate limit needed. Under 10 pages total.

---

### SOURCE 5 — Tyler ISD School Directory
**Source ID:** `TYLER_ISD`
**URL:** `https://www.tylerisd.org/domain/12` (or staff directory path — verify)
**Per-campus:** `https://www.tylerisd.org/[campus-name]/staff`
**Audience Segments:** Seg. 1 (Parents & Families — staff who are also parents), Seg. 12 (Faith/Homeschool adjacent)
**Arc Type:** `Parent`
**WF-001 Arm:** Parent arc
**Volume Est.:** 200–500 staff across campuses (teachers, admin, counselors)

**Extraction Method:** Multi-page HTML
- Tyler ISD publishes per-campus staff directories. Crawl each campus page.
- Typically exposes: name, title/role, email (`@tylerisd.org` format), phone extension

**Campus List to Crawl:**
Pull the full campus list from `https://www.tylerisd.org/domain/12` first, then iterate each campus staff page.

**Field Mapping:**
```
name          → first_name + last_name
title         → notes (keep job title for context)
email         → email (district format)
arc_type      → Parent
notes         → "Tyler ISD staff — [campus name] — Parent arc"
```

**Important Guidance:**
- These are professional educators, not personal contacts. Outreach should reference youth programs, teen safety, or family training — not direct personal safety pitches.
- Do not use generic safety-in-parking-lot messaging. Use: "programs for your students and families."
- Verify Tyler ISD staff directory is publicly accessible without login — it typically is.

**Rate Limit:** 1 request/3s per campus page. There are ~15–20 campuses; do not blast all at once.

---

### SOURCE 6 — Rotary Club of Tyler
**Source ID:** `ROTARY`
**URL:** Primary chapter: search `rotary.org club locator` for Tyler TX clubs
**Alt:** `https://www.tylerrotary.org` or `https://tylerrotaryclub.com`
**Audience Segments:** Seg. 3 (Men — primary), Seg. 13 (Corporate)
**Arc Type:** `Default`
**WF-001 Arm:** Default arc
**Volume Est.:** 30–100 contacts per chapter; Tyler may have 2–3 active chapters

**Extraction Method:** Manual HTML
- Rotary chapter websites vary widely in tech quality. Some have member directories, others only list officers.
- Target: board/leadership pages first, member roster if public.
- `rotary.org` itself does not expose member rosters — go to local chapter sites directly.

**Known Local Chapters:**
1. Tyler Rotary Club (the original) — check `https://www.tylerrotary.org`
2. Rotary Club of Tyler Midtown — search separately
3. Rotary E-Club possibilities — lower priority

**Rate Limit:** Static pages only — no rate limiting needed.

---

### SOURCE 7 — VFW Post 8904 / American Legion Tyler Posts
**Source ID:** `VET_ORGS`
**URLs:**
- VFW Post 8904: `https://vfw8904.org` or search vfw.org
- American Legion Tyler Post: `https://www.legion.org` → locate Tyler posts
- American Legion Post 28 (Tyler): verify current URL
**Audience Segments:** Seg. 8 (Military/LE/First Responders — primary), Seg. 3 (Men)
**Arc Type:** `LE/Mil`
**WF-001 Arm:** LE/Mil arc
**Volume Est.:** 20–80 contacts (officers/leadership — full rosters are private)

**Extraction Method:** Manual HTML
- Public pages typically list post commanders, officers, and event contacts.
- Full membership rosters are never public on VFW/Legion sites.
- Target: officers list, adjutant contact, event contact emails

**Outreach Note:**
Veterans respond to peer identity, mission framing, and respect — not marketing language. The LE/Mil arc must speak to capability maintenance, tactical edge, and protecting others. Never use consumer-facing fitness or "build confidence" language with this segment.

**Set `notes = "VFW/Legion — LE/Mil arc — use Seg. 8 tactical voice — no fitness framing"`**

---

### SOURCE 8 — Smith County Sheriff's Office
**Source ID:** `SCSO`
**URL:** `https://www.smithcountysheriff.com/staff-directory/` (verify path)
**Alt:** `https://www.smith-county.com` → departments → Sheriff
**Audience Segments:** Seg. 8 (Law Enforcement — primary)
**Arc Type:** `LE/Mil`
**WF-001 Arm:** LE/Mil arc
**Volume Est.:** 30–80 contacts (public-facing staff only)

**Extraction Method:** HTML or PDF
- Some sheriff offices publish a public staff directory as HTML, others as PDF.
- If PDF: use `pdfplumber` or `PyMuPDF` — see PDF extraction notes below.
- Typically exposes: name, title/rank, department, email (`.gov` format)

**PDF Extraction Setup (if applicable):**
```python
import pdfplumber

with pdfplumber.open("scso_directory.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        # Parse name + rank + email from text blocks
        # SCSO emails typically follow: firstname.lastname@smith-county.com
```

**Important Guidance:**
- Do not scrape personal cell numbers — only official listed contacts.
- This is an organizational outreach target, not individual cold email. Flag for Nathan to consider a direct partnership conversation with command staff before individual outreach.
- Set `notes = "SCSO — LE arc — consider command-level partnership conversation first"`

---

### SOURCE 9 — East Texas Homeschool Association / THSC Tyler
**Source ID:** `HOMESCHOOL`
**URLs:**
- Texas Home School Coalition (THSC): `https://thsc.org/find-a-group/` → filter Tyler TX area
- Local co-ops: search Facebook Groups + Google for "Tyler TX homeschool co-op"
- `https://www.setaonline.org` (Southeast Texas homeschool groups)
**Audience Segments:** Seg. 12 (Homeschool Families & Faith Communities), Seg. 1 (Parents)
**Arc Type:** `Parent`
**WF-001 Arm:** Parent arc
**Volume Est.:** 20–100 contacts (co-op leaders, THSC chapter reps)

**Extraction Method:** Manual research + HTML
- THSC's group finder is partially dynamic. Search by ZIP code (75701–75709 for Tyler area).
- Most homeschool groups do not publish member lists — extract group leaders/contacts only.
- Supplement with Facebook Group admins: search "Tyler Texas Homeschool" — admin names are public.

**Outreach Approach for Homeschool Segment:**
Lead with youth programs and character development. The values hook is stronger than the safety hook for faith-based homeschool families. Offer to present at a co-op day — peer-to-peer seminar format works best here.

**Set `notes = "Homeschool/THSC — Parent arc — youth + character framing — offer co-op presentation"`**

---

### SOURCE 10 — Tyler Young Professionals (TYP)
**Source ID:** `TYP`
**URL:** `https://www.tylertexas.com/typ/` or `https://typtyler.com`
**Audience Segments:** Seg. 14 (College/Young Adults), Seg. 3 (Men), Seg. 2 (Women)
**Arc Type:** `Default` (skews Safety for women, Default for men)
**WF-001 Arm:** Default arc (Safety arm for confirmed women contacts)
**Volume Est.:** 50–200 contacts

**Extraction Method:** HTML
- TYP typically maintains a public leadership board page and sometimes a member showcase.
- Full member directory is usually member-login only.
- Scrape: leadership board (public), featured members (public), event speakers/panelists (public)

**Gender-Based Arc Routing:**
- If `gender` can be inferred from name: route women to Safety arc, men to Default
- If ambiguous: Default arc; update after first response
- Do not over-optimize — get contacts in the pipeline, adjust arc type after engagement

**Set `notes = "TYP — young professional — route women → Safety arc, men → Default"`**

---

## PDF Extraction — General Pattern

For any source that requires PDF parsing (SCSO, some BNI chapters, some government directories):

```python
# requirements: pdfplumber>=0.10.0
import pdfplumber, re, csv

def extract_contacts_from_pdf(pdf_path, source_id):
    contacts = []
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    phone_pattern = re.compile(r'\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}')

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            emails = email_pattern.findall(text)
            phones = phone_pattern.findall(text)
            # Further parse name/org from surrounding text blocks
            contacts.append({
                'source': source_id,
                'emails': emails,
                'phones': phones,
                'raw_text': text  # store raw for manual review pass
            })
    return contacts
```

---

## Pipedrive Import Schema

Once cleaned and deduplicated, import each record as a **Person** in Pipedrive with a linked **Deal** in the Cold Outreach stage.

**Required Pipedrive Fields:**
```
Person:
  - First Name
  - Last Name
  - Email
  - Phone
  - Organization
  - Label: (leave blank — Nathan assigns after first response)
  - Custom Field: ETKM Arc Type → [Safety / Parent / Fitness / LE/Mil / Former MA / Default]
  - Custom Field: Source → [SOURCE_ID from above]

Deal:
  - Title: "[First Name] [Last Name] — [SOURCE_ID] Cold Outreach"
  - Stage: Cold Outreach (or equivalent TOFU stage)
  - Pipeline: Student Acquisition
```

**WF-001 Trigger:**
WF-001 triggers from Pipedrive stage + arc type. Once the Person + Deal are created in the Cold Outreach stage, Manus's Make.com automation will route them to the correct arc arm. No manual email send needed.

---

## Rate Limiting — Universal Rules

| Rule | Value |
|---|---|
| Default delay between requests | 2–4s (randomized) |
| Max requests/min to any single domain | 15 |
| User-Agent header | `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36` |
| Respect `robots.txt` | Yes — check before scraping |
| JS-rendered pages | Use Playwright with stealth plugin |
| Login-walled pages | Do NOT attempt bypass — flag for Nathan |

---

## JS-Rendered Sites — Playwright Setup

```python
# requirements: playwright>=1.40.0
# Run: playwright install chromium

from playwright.sync_api import sync_playwright
import time, random

def fetch_js_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = context.new_page()
        page.goto(url, wait_until='networkidle')
        time.sleep(random.uniform(2, 4))
        content = page.content()
        browser.close()
        return content
```

---

## Output File Format

Final cleaned output: `smith_county_contacts_[YYYY-MM-DD].csv`

Columns:
```
source, first_name, last_name, email, phone, org_name, title, arc_type, segment, notes
```

Deliver as CSV to Nathan for review before Pipedrive import.

---

## Priority Build Order

Build scrapers in this sequence (highest ROI first, simplest extraction first):

| Priority | Source ID | Reason |
|---|---|---|
| 1 | `CHAMBER` | Highest volume, structured HTML, broadest segment coverage |
| 2 | `GTAR` | Likely JSON API — single clean pull, Safety arc, high-value segment |
| 3 | `SCSO` | Small volume but highest-intent segment (LE/Mil) — likely PDF |
| 4 | `BNI` | Medium complexity, warm networkers, high conversion potential |
| 5 | `TYLER_ISD` | Multi-page crawl, parent arc, high volume |
| 6 | `TYP` | Leadership-only, quick win |
| 7 | `JL_TYLER` | Leadership-only, quick win |
| 8 | `ROTARY` | Static pages, leadership only, fast |
| 9 | `VET_ORGS` | Low volume, leadership only, LE/Mil arc |
| 10 | `HOMESCHOOL` | Most manual work, lowest volume — do last |

---

## What to Flag to Nathan

Before running any scraper, flag these items:

- [ ] Chamber directory — is it login-walled? Nathan has member access.
- [ ] SCSO — command-level partnership conversation recommended before individual outreach.
- [ ] Tyler ISD — confirm district permits third-party contact of staff via listed directory emails.
- [ ] VFW/Legion — Nathan may have personal connections at these posts. Warm intro > cold email.
- [ ] BNI — Nathan may already be a BNI member or know chapter presidents. Warm intro > cold.

---

*Spec authored by Claude for ETKM dev handoff. All outreach must comply with CAN-SPAM — every email must include unsubscribe link and physical mailing address. WF-001 handles this automatically via Pipedrive/Make.com integration.*
