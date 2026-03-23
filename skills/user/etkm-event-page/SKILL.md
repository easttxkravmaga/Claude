---
name: etkm-event-page
description: >
  Use this skill to build any ETKM event landing page as a production-ready,
  self-contained HTML file that deploys directly into WordPress via Raw HTML block.
  Trigger whenever Nathan asks to build, update, or clone an event page — including
  seminars, workshops, specialty training events, CBLTAC-style courses, or any
  multi-session training event. Also trigger for: "build an event page", "make a
  landing page for [event]", "same layout as the CBLTAC page", "use the event
  page format", "clone this page for [audience]", or any request involving an
  event registration page. This skill encodes the full CBLTAC page design system
  (three production pages built March 2026) including CSS architecture, all section
  components, copy doctrine, Stripe payment button patterns, WordPress deployment
  rules, and audience variant logic. Always load etkm-brand-kit alongside this
  skill. Load etkm-event-planning for event structure and curriculum details.
---

# ETKM Event Page Build System

**Version:** 1.0
**Built from:** CBLTAC General, Professionals, and First Responders pages (March 2026)
**Deployment target:** WordPress via Raw HTML block (Visual Composer)

---

## Quick Reference — What This System Produces

A single self-contained `.html` file that:
- Deploys into WordPress Raw HTML block with zero external dependencies
- All images embedded as base64 (no folder/CDN needed)
- Full ETKM brand compliance (black/white/red, Barlow Condensed + Inter)
- Scoped CSS — never bleeds into WP theme
- Stripe payment buttons wired directly
- Scroll-triggered fade animations
- Fully responsive (collapses gracefully at 860px)

---

## Critical WordPress Architecture Rules

**Problem:** WordPress Visual Composer wraps content in boxed containers that constrain width and conflict with CSS resets.

**Solution — always apply these three patterns:**

### 1. Wrapper ID Scoping
Every page uses a unique wrapper div ID. CSS is scoped to that ID only.
```html
<div id="cbltac-main">   <!-- general -->
<div id="cbltac-pro">    <!-- professionals -->
<div id="cbltac-fr">     <!-- first responders -->
<div id="etkm-event-X">  <!-- new events: use event slug -->
```

### 2. WP Container Override Block
Always include this at the top of the `<style>` block — it forces WP containers to full-width:
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
Never write bare `.container`, `.hero`, etc. — they will bleed into the WP theme.

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

**Font loading** (always include in `<head>` or via `<link>` inside the HTML block):
```html
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
```

---

## Section Component Library

Load `references/components.md` for full CSS + HTML for each section.

### Page Structure (Standard Order)
1. **Top Bar** — red announcement strip
2. **[Discount Banner]** — optional, first responder / special pricing
3. **Hero** — headline + subhead + CTAs + event bar
4. **Who This Is For** — audience grid (6–8 cards)
5. **[Classroom/Proof Photo]** — optional, full-width B&W cinematic
6. **Core Insight** — the "bad decisions" red-border quote block
7. **[How This Works]** — optional, interactive/hands-on format explainer
8. **Courses Section** — two-column course blocks
9. **Combined/Best Value** — red-border combo block with pricing
10. **Instructor** — photo card + bio
11. **Location** — two-column venue + presenter info
12. **Final CTA** — centered pricing options + main button
13. **Footer** — ETKM contact

---

## Audience Variant System

Three proven variants. See `references/variants.md` for full copy patterns.

| Variant | Hero Headline | Who Grid Focus | Key Differentiators |
|---------|--------------|----------------|---------------------|
| **General** | "Train to Think Clearly / When It Matters Most" | All segments: LE, healthcare, leaders, travelers, families | Broadest appeal, John's full origin story |
| **Professionals** | "Your Decisions / Under Pressure / Define Your Career" | C-Suite, Sales, RE, Managers, Insurance, Travelers, Owners, Healthcare | Career/reputation framing, no military heavy |
| **First Responders** | "You Handle Crises / For Everyone Else. / Who Handles It for You?" | LE, Fire, EMS, Dispatchers, ER, Security | 50% discount banner, John's CHP/Ranger credentials lead, cumulative stress language |

**Rule:** The audience variant changes the hero, who-grid, insight copy, application blocks, and instructor framing. The course content, pricing, and structure stay identical across variants.

---

## Stripe Payment Button Pattern

```html
<!-- Always target="_blank" on all payment links -->
<!-- Course 1 button -->
<a href="[STRIPE_URL_C1]" class="ccta" target="_blank">Register for Course 1</a>

<!-- Course 2 button -->
<a href="[STRIPE_URL_C2]" class="ccta" target="_blank">Register for Course 2</a>

<!-- Both Sessions button -->
<a href="[STRIPE_URL_BOTH]" class="combo-cta" target="_blank">Register for Both Sessions — $[PRICE]</a>

<!-- Final CTA pricing options -->
<a href="[STRIPE_URL_C1]" target="_blank" class="fopt">...</a>
<a href="[STRIPE_URL_C2]" target="_blank" class="fopt">...</a>
<a href="[STRIPE_URL_BOTH]" target="_blank" class="fopt" style="border-color:#CC0000;">...</a>

<!-- Main bottom CTA defaults to Both Sessions (best value) -->
<a href="[STRIPE_URL_BOTH]" class="fcta-main fd" target="_blank">Register Now</a>
```

**Rule:** Main hero CTA + main bottom CTA always link to the Both Sessions / best value option.

---

## Image Handling

### Profile Photos
- Convert to B&W grayscale via PIL: `img.convert('L')`
- Resize to 300px wide max for headshots
- Save as JPEG quality 82
- Embed as `data:image/jpeg;base64,...`
- Apply CSS: `filter:grayscale(100%) contrast(1.05)`

### Classroom/Proof Photos
- Source: WordPress uploads URL
- Download via curl, convert to B&W
- Resize to 900px wide
- Save JPEG quality 80
- Crop top third if too much dead space: `img.crop((0, h//3, w, h))`
- Embed as base64
- Display: full-width cinematic with left gradient overlay, headline overlay, CBLTAC badge bottom-right

### Python Pattern
```python
from PIL import Image
import base64, io

img = Image.open('source.jpg')
# Optional crop: img = img.crop((0, img.height//3, img.width, img.height))
bw = img.convert('L').resize((900, int(img.height*900/img.width)), Image.LANCZOS)
buf = io.BytesIO()
bw.save(buf, 'JPEG', quality=80)
b64 = base64.b64encode(buf.getvalue()).decode()
```

---

## Fade Animation System

Apply `.fd` class to any element that should fade in on scroll.

```css
#wrapper .fd { opacity:0; transform:translateY(22px); transition:opacity .6s ease,transform .6s ease; }
#wrapper .fd.vis { opacity:1; transform:none; }
```

```javascript
(function(){
  var els = document.querySelectorAll('#wrapper-id .fd');
  var obs = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('vis'); obs.unobserve(e.target); } });
  },{threshold:0.08,rootMargin:'0px 0px -30px 0px'});
  els.forEach(function(el){ obs.observe(el); });
})();
```

---

## Build Workflow

### Step 1 — Gather Inputs
Collect before writing any code:
- Event name and type (seminar, workshop, specialty)
- Audience variant (general / professional / first responder / custom)
- Course 1: title, date, time, price, Stripe URL
- Course 2: title, date, time, price, Stripe URL
- Both Sessions: price, Stripe URL
- Venue name and address
- Instructor: name, credentials, photo URL (or upload)
- Classroom/proof photo URL (or upload) — optional
- Any audience-specific discount (amount, who qualifies)
- Any testimonial video (WordPress upload URL)

### Step 2 — Fetch & Process Images
```bash
# Download and convert instructor photo
curl -s -L --insecure -A "Mozilla/5.0" "[PHOTO_URL]" -o instructor.jpg

# Download and convert classroom photo
curl -s -L --insecure -A "Mozilla/5.0" "[CLASSROOM_URL]" -o classroom.jpg
```
Then run Python conversion (see Image Handling above).

### Step 3 — Build HTML
Use unique wrapper ID. Apply full CSS from `references/components.md`.
Insert all sections in standard order, skipping optional ones if not needed.
Wire all Stripe links. Embed all images as base64.

### Step 4 — Screenshot & QC
Use Playwright to screenshot hero, mid-page, and instructor sections.
Check against QC gates below before delivering.

### Step 5 — Deliver
Copy to `/mnt/user-data/outputs/[event-slug].html`
Present file to Nathan via `present_files`.

---

## QC Gates (All Must Pass Before Delivery)

- [ ] No `href="#"` placeholders — all buttons have real URLs
- [ ] No external image src — all images embedded as base64
- [ ] WP override block present in CSS
- [ ] All CSS scoped to wrapper ID
- [ ] Wrapper ID is unique (not reused from another page)
- [ ] Fade animation JS uses correct wrapper ID selector
- [ ] Hero CTA and main bottom CTA both link to best-value option
- [ ] Red only used once per visible section (brand rule)
- [ ] Responsive breakpoint at 860px present
- [ ] No `#000` shorthand — use `#000000` or CSS var
- [ ] `target="_blank"` on all external links
- [ ] Google Fonts link included

---

## Reference Files

| File | Load When |
|------|-----------|
| `references/components.md` | Building or auditing any section — full CSS + HTML |
| `references/variants.md` | Writing copy for a specific audience variant |
| `references/copy-doctrine.md` | Writing headlines, insight blocks, or CTAs |

---

## Production Pages (Live Reference)

| Page | URL | Wrapper ID | Variant |
|------|-----|------------|---------|
| CBLTAC General | etxkravmaga.com/cbltac-courses/ | cbltac-main | General |
| CBLTAC Professionals | etxkravmaga.com/cbltac-professionals/ | cbltac-pro | Professional |
| CBLTAC First Responders | etxkravmaga.com/events/cbltac-first-responders/ | cbltac-fr | First Responder |
