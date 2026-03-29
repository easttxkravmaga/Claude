---
name: etkm-event-page
description: >
  Use this skill to build any ETKM event landing page as a production-ready,
  self-contained HTML file that deploys directly into WordPress via Raw HTML block.
  Trigger whenever Nathan asks to build, update, or clone an event page — including
  seminars, workshops, specialty training events, CBLTAC-style courses, or any
  multi-session training event. Also trigger for: "build an event page", "make a
  landing page for [event]", "same layout as the WSD page", "same layout as the
  CBLTAC page", "use the event page format", "clone this page for [audience]", or
  any request involving an event registration page. This skill encodes two complete
  production page systems: TYPE 1 (Seminars/Workshops — WSD as locked reference)
  and TYPE 3 (Specialty/Guest Instructor — CBLTAC series as locked reference).
  Always load etkm-brand-kit alongside this skill. Load etkm-event-planning for
  event structure and curriculum details.
---

# ETKM Event Page Build System

**Version:** 2.1
**Updated:** March 2026
**Templates:** TYPE 1 (Seminar/Workshop) + TYPE 3 (Specialty/Guest Instructor)
**Deployment target:** WordPress via Raw HTML block (Visual Composer)

---

## Determine Template Type First

| Event Type | Template | Reference Page |
|-----------|----------|----------------|
| Women's Self Defense, Youth SD, College Ready, Intro to Krav, any public seminar | **TYPE 1** | etxkravmaga.com/fight-back-etx/womens-self-defense-seminar-in-tyler-tx/ |
| CBLTAC, guest instructor, multi-session specialty training | **TYPE 3** | etxkravmaga.com/cbltac-courses/ |

---

## Load Order for Event Page Sessions

1. `etkm-event-page` — HTML system (primary, this file)
2. `etkm-brand-kit` — colors, type, visual rules
3. `etkm-event-planning` — curriculum structure, email/social package
4. `etkm-deliverable-qc` — before anything ships

---

## Dependencies

| Skill | Why |
|-------|-----|
| `etkm-brand-kit` | Visual standard (already referenced) |
| `etkm-webpage-build` | Parent page standard — event pages inherit all hero spec, section patterns, font loading, and WordPress deployment rules |
| `etkm-webform-build` | Any registration form on the event page must follow webform build standard — field whitelist, Web3Forms config, arc dropdown |

---

## TYPE 1 — Seminar / Workshop Template

**Reference page:** [etxkravmaga.com/fight-back-etx/womens-self-defense-seminar-in-tyler-tx/](http://etxkravmaga.com/fight-back-etx/womens-self-defense-seminar-in-tyler-tx/)
**Checkout system:** Ecwid (NOT Stripe)

Load `references/type1-seminar.md` for full CSS + HTML for all 10 sections.

### Fixed 10-Section Order (Non-Negotiable)

| # | Section | Notes |
|---|---------|-------|
| 1 | Top Bar | Red background, event name + "Spots Are Limited" |
| 2 | Hero | Full-bleed B&W background image, headline, event bar |
| 3 | Registration | Ecwid buy now embed + price + 3-cell meta — JUST UNDER FOLD |
| 4 | Who This Is For | 6-card audience grid |
| 5 | Insight Block | Red left-border quote, core training truth |
| 6 | Seminar Content | 2×2 level/module cards with ghost numbers |
| 7 | Testimonial | Pull quote (omit section entirely if none available) |
| 8 | Location | Venue address + ETKM contact |
| 9 | Final CTA | Headline + button that scrolls to `#register` |
| 10 | Footer | ETKM address/phone/URL |

### What Changes vs. What Never Changes

**Only three things change per event:**
- **Wording** — headlines, copy, level descriptions, who-grid
- **Images** — hero background (always B&W embedded base64)
- **Checkout** — Ecwid embed code + price

**Nothing else changes.** CSS, structure, spacing, animation, WP deploy rules — all fixed.

### TYPE 1 Key Rules

- **Hero headline:** MUST span exactly two lines — use `<br>` to control the break. Never let it wrap naturally.
- **Registration block:** MUST have `id="register"`. Ecwid widget embeds here.
- **Final CTA button:** MUST use `href="#register"`. It NEVER re-embeds Ecwid. Non-negotiable.
- **Hero background:** Always B&W. Always embedded as base64. Gradient overlay: `linear-gradient(to right, rgba(0,0,0,0.82) 0%, rgba(0,0,0,0.55) 60%, rgba(0,0,0,0.30) 100%)`.
- **Seminar Content:** 2×2 grid with ghost numbers (large faded numerals behind each card).

---

## TYPE 3 — Specialty / Guest Instructor Template

**Reference pages:**
- [etxkravmaga.com/cbltac-courses/](http://etxkravmaga.com/cbltac-courses/) (general)
- [etxkravmaga.com/cbltac-professionals/](http://etxkravmaga.com/cbltac-professionals/) (professional)
- [etxkravmaga.com/events/cbltac-first-responders/](http://etxkravmaga.com/events/cbltac-first-responders/) (first responder)

**Checkout system:** Ecwid (Multiple Embeds)

Load `references/components.md` for full CSS + HTML for all sections.

### Fixed 13-Section Order

| # | Section | Notes |
|---|---------|-------|
| 1 | Top Bar | Red, event + dates |
| 2 | [Discount Banner] | Optional — first responder / special pricing |
| 3 | Hero | Headline, subhead, CTAs, event bar |
| 4 | Who This Is For | 6–8 audience cards |
| 5 | [Proof Photo] | Optional classroom/action photo |
| 6 | Insight Block | "Bad decisions...unmanaged stress" |
| 7 | [Format Block] | Optional interactive/hands-on explainer |
| 8 | Courses | Two-column course blocks |
| 9 | Combined/Best Value | Red-top combo block |
| 10 | Instructor | B&W photo card + bio |
| 11 | Location | Venue + ETKM info |
| 12 | Final CTA | Pricing options + main buy now button |
| 13 | Footer | ETKM address/phone/URL |

### TYPE 3 Key Rules

- **Audience variants:** Hero, who-grid, insight copy, and instructor framing change per variant. Course content, pricing, and structure stay identical. See `references/variants.md`.

---

## Wrapper ID Convention

All CSS MUST be scoped to a unique wrapper ID. Never reuse a wrapper ID from another page.

| Event | Wrapper ID |
|-------|-----------|
| Women's Self Defense | `etkm-wsd` |
| Youth Self Defense | `etkm-youth-sd` |
| College Ready | `etkm-college` |
| Intro to Krav | `etkm-intro-km` |
| CBLTAC General | `cbltac-main` |
| CBLTAC Professionals | `cbltac-pro` |
| CBLTAC First Responders | `cbltac-fr` |
| New events | `etkm-[event-slug]` |

---

## Checkout System — All Events Use Ecwid Embedded Buy Now

**All ETKM event pages use Ecwid embedded buy now code. No external payment links.**
Nathan provides the Ecwid embed code per product. Claude drops it in exactly as provided and never modifies it.

### TYPE 1 — Single Ecwid Embed
One Ecwid widget lives in the Registration block (section 3). The Final CTA button uses `href="#register"` to scroll up to the widget. Ecwid is **never embedded twice** on the same page.
- Registration block → Ecwid buy now widget (the widget)
- Final CTA button → `href="#register"` (scrolls to widget)

### TYPE 3 — Multiple Ecwid Embeds
Each course option gets its own Ecwid embed — one per product. The main bottom button uses the Both Sessions product embed.
- Course 1 card → Ecwid embed (Course 1 product)
- Course 2 card → Ecwid embed (Course 2 product)
- Combo block → Ecwid embed (Both Sessions product)
- Final CTA option 1 → Ecwid embed (Course 1 product)
- Final CTA option 2 → Ecwid embed (Course 2 product)
- Final CTA option 3 → Ecwid embed (Both Sessions product)
- Main bottom button → Ecwid embed (Both Sessions product)

### Ecwid Placement Rules
- Wrap each embed in a plain `<div>` with no extra styling
- Never modify the embed code
- Never add CSS to Ecwid elements — it breaks the widget
- Load the Ecwid `<script>` tag only once per page (the first embed carries it; subsequent product embeds call `xProduct()` only)

---

## Critical WordPress Architecture Rules

**Problem:** WordPress Visual Composer wraps content in boxed containers that constrain width and conflict with CSS resets.

**Solution — always apply these three patterns:**

### 1. Wrapper ID Scoping
Every page uses a unique wrapper div ID. CSS is scoped to that ID only.
```html
<div id="etkm-wsd">      <!-- Women's Self Defense -->
<div id="cbltac-main">   <!-- CBLTAC general -->
<div id="etkm-[slug]">   <!-- new events -->
```

### 2. WP Container Override Block
Always include this at the top of the `<style>` block:
```css
body, .vcv-content--blank, .entry-content, .vce-col-content,
.vce-col-inner, .vce-row-container {
  background: #000 !important; max-width: 100% !important; width: 100% !important;
  padding-left: 0 !important; padding-right: 0 !important;
}
.vce-row, .vce-row-content, .vce-col, .vce-col-inner {
  padding: 0 !important; margin: 0 !important;
  width: 100% !important; max-width: 100% !important;
}
```

### 3. All CSS Scoped to Wrapper
Every rule prefixed: `#wrapper-id .class-name { ... }`
Never write bare `.container`, `.hero`, etc.

---

## CSS Variable System

```css
#wrapper-id {
  --black:    #000000;
  --surface:  #111111;
  --surface2: #1A1A1A;
  --white:    #FFFFFF;
  --gray:     #575757;
  --lgray:    #BBBBBB;
  --red:      #CC0000;
  --font-hed: 'Barlow Condensed', sans-serif;
  --font-body:'Inter', sans-serif;
}
```

**Font loading:**
```html
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
```

---

## Image Handling

### Hero Background (TYPE 1)
- Convert to B&W: `img.convert('L')`
- Resize to 1400px wide
- Save JPEG quality 80
- Embed as base64
- Apply gradient overlay in CSS (not on the image itself)

### Profile Photos (TYPE 3)
- Convert to B&W: `img.convert('L')`
- Resize to 300px wide max
- Save JPEG quality 82
- Embed as base64
- CSS: `filter:grayscale(100%) contrast(1.05)`

### Classroom/Proof Photos (TYPE 3)
- Download, convert to B&W, resize to 900px wide
- Save JPEG quality 80
- Optional crop top third if too much dead space
- Embed as base64

### Python Pattern
```python
from PIL import Image
import base64, io

img = Image.open('source.jpg')
bw = img.convert('L').resize((900, int(img.height*900/img.width)), Image.LANCZOS)
buf = io.BytesIO()
bw.save(buf, 'JPEG', quality=80)
b64 = base64.b64encode(buf.getvalue()).decode()
```

---

## Fade Animation System

```css
#wrapper .fd { opacity:0; transform:translateY(22px); transition:opacity .6s ease,transform .6s ease; }
#wrapper .fd.vis { opacity:1; transform:none; }
```

```javascript
(function(){
  var els = document.querySelectorAll('#[WRAPPER-ID] .fd');
  var obs = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('vis'); obs.unobserve(e.target); } });
  },{threshold:0.08,rootMargin:'0px 0px -30px 0px'});
  els.forEach(function(el){ obs.observe(el); });
})();
```

---

## Build Workflow

### Step 1 — Gather Inputs
- Event name, type, audience
- Date(s), time(s), price(s)
- **Ecwid embed code(s)** — Nathan provides per product
- Venue name and address
- Hero background image (URL or upload)
- Instructor photo (URL or upload) — TYPE 3 only
- Any discount or special pricing
- Testimonial quote (if available)

### Step 2 — Fetch & Process Images
```bash
curl -s -L --insecure -A "Mozilla/5.0" "[IMAGE_URL]" -o image.jpg
```
Then run Python conversion (see Image Handling above).

### Step 3 — Build HTML
Use unique wrapper ID. Apply full CSS from the appropriate reference file.
Insert all sections in standard order. Embed all Ecwid codes exactly as provided. Embed all images as base64.

### Step 4 — Screenshot & QC
Use Playwright to screenshot hero, mid-page, and bottom sections.
Check against QC gates before delivering.

### Step 5 — Deliver
Copy to `/mnt/user-data/outputs/[event-slug].html`
Present file to Nathan via `present_files`.

---

## QC Gates (All Must Pass Before Delivery)

- [ ] No placeholder text or comments remaining in the HTML
- [ ] All Ecwid embed code present and unmodified
- [ ] No external image src — all images embedded as base64
- [ ] WP override block present in CSS
- [ ] All CSS scoped to unique wrapper ID
- [ ] TYPE 1: Final CTA button is `href="#register"`, not a second embed
- [ ] Red used max once per visible section
- [ ] Responsive breakpoint at 860px present
- [ ] `target="_blank"` on all external links
- [ ] Google Fonts link included

---

## QC Gate — Event Page Delivery

- [ ] Registration/booking link is present and correct (Ecwid, Stripe, or Calendly — confirmed live)
- [ ] CTA button text is white — not default browser style
- [ ] Event date, time, and location are accurate and not placeholder text
- [ ] Price displayed correctly (no rounding, no missing $ sign)
- [ ] All etkm-webpage-build Gate 1–4 checks pass
- [ ] If form is on page: all etkm-webform-build Gate 1–3 checks pass

---

## Reference Files

| File | Load When |
|------|-----------|
| `references/type1-seminar.md` | Building or auditing any TYPE 1 seminar/workshop page — full CSS + HTML for all 10 sections |
| `references/components.md` | Building or auditing any TYPE 3 specialty/guest instructor page — full CSS + HTML |
| `references/variants.md` | Writing copy for a specific TYPE 3 audience variant |
| `references/copy-doctrine.md` | Writing headlines, insight blocks, or CTAs |

---

## Production Pages (Live Reference)

| Page | Template | URL | Wrapper ID |
|------|---------|-----|-----------|
| Women's Self Defense | TYPE 1 | etxkravmaga.com/fight-back-etx/womens-self-defense-seminar-in-tyler-tx/ | etkm-wsd |
| CBLTAC General | TYPE 3 | etxkravmaga.com/cbltac-courses/ | cbltac-main |
| CBLTAC Professionals | TYPE 3 | etxkravmaga.com/cbltac-professionals/ | cbltac-pro |
| CBLTAC First Responders | TYPE 3 | etxkravmaga.com/events/cbltac-first-responders/ | cbltac-fr |

---

## Operational Rules (All Event Pages)

### Update vs. Rebuild
If only date, price, or Ecwid embed changes — update the existing file, do not rebuild. Pull the current HTML, swap those specific values, re-deliver. A full rebuild is only needed when wording or images change significantly. Treat the file as a living document, not a one-time build.

### Ecwid Not Yet Provided
If Nathan hasn't sent the embed code yet: insert a clearly marked comment block — `<!-- ECWID EMBED: [PRODUCT NAME] GOES HERE -->` — and deliver the page as complete except for that block. Never use a fake button or `href="#"` as a stand-in. Flag it explicitly in the delivery note.

### File Naming Convention
Always: `etkm-[event-slug].html` — lowercase, hyphenated, matches the WordPress page slug.
- Women's Self Defense → `etkm-wsd.html`
- Youth Self Defense → `etkm-youth-sd.html`
- Intro to Krav → `etkm-intro-km.html`
- College Ready → `etkm-college.html`

### Screenshot Before Rebuilding a Live Page
Before rebuilding or updating any page that is already deployed: fetch the live URL and screenshot it first. Confirm the current deployed state matches the last known local file before making changes. If they differ, surface the discrepancy to Nathan before proceeding.

---

## Nathan's Filter for This Project

Every deliverable must produce **more revenue** or **less time wasted**. Both if possible.
A technically impressive page that takes three sessions to build has failed. A clean, deployable page that gets registrations has succeeded.
