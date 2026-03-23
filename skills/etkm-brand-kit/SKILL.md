---
name: etkm-brand-kit
description: >
  Use this skill whenever producing any visual output for ETKM — HTML pages, PDFs,
  presentations, forms, social media image briefs, React artifacts, SVGs, flyers,
  email templates, landing pages, or any design deliverable. Also trigger for Canva
  image briefs, branded documents, app UIs, visual aide tools, or any file where
  colors, typography, layout, or visual styling decisions are being made for ETKM.
  Trigger phrases: "make it on-brand", "ETKM brand", "brand colors", "brand kit",
  "visual style", "design for ETKM", "branded", "Swiss layout", "red accent",
  "black and white design". If the output will be seen by students, prospects, or
  the public and carries the ETKM name, use this skill. Non-negotiable for all
  final-revision and production-ready visual work.
---

# ETKM Brand Kit

**Version:** 4.0
**Last Updated:** 2026-03-23
**Change:** Typography system locked — Montserrat Black 900 is the permanent
            ETKM headline font across all deliverables. No exceptions.

---

## 1. Color Palette (Non-Negotiable)

| Color | Hex | Role |
|-------|-----|------|
| Black | #000000 | Primary background, primary text |
| White | #FFFFFF | Primary background, primary text |
| Red | #CC0000 | Attention only — one element per view |
| Gray | #575757 | Supporting elements, secondary text |
| Lite Gray | #BBBBBB | Dividers, borders, subtle structure |

### Color Rules

- Backgrounds: Solid Black or Solid White only. Never gray backgrounds.
- Gradients: Prohibited. No exceptions.
- Contrast: White text on dark backgrounds. Black text on light backgrounds.
- No other colors exist in the ETKM system. If a design needs color
  beyond this palette, the design is wrong.

---

## 2. Red Usage (Attention Only)

Red is a weapon, not decoration. It draws the eye to exactly one thing.

- Use for: One word, one short phrase, one command, one warning, one decision point.
- Do NOT use for: Paragraphs, backgrounds, multiple elements, decorative bars on multiple sides.
- Principle: When red appears, all other elements must be neutral (black, white, gray).
- Maximum: One red element per visual section. If tempted to add a second — remove the first.

### Proven Red Applications

| Context | Red Usage |
|---------|-----------|
| Social graphics | Category label OR supporting line — never both |
| PDFs and documents | Single attention phrase (e.g., "Train Hard.") |
| HTML pages and forms | CTA button background, single accent line |
| Email templates | Red top bar, red CTA button |
| Curriculum sheets | Single red accent line below header |

---

## 3. Typography System (LOCKED 2026-03-23)

### THE LOCKED FONT STACK

| Role | Font | Weight | Source |
|------|------|--------|--------|
| **Display Headlines** | **Montserrat Black** | **900** | **Google Fonts / CDN — FREE** |
| Body / UI Text | Inter | 400 Regular, 600 SemiBold | Google Fonts / CDN — FREE |
| Category Labels | Inter | 600 SemiBold, uppercase + letter-spacing | Google Fonts / CDN — FREE |
| Data / Captions | Inter | 400 Regular, uppercase + letter-spacing | Google Fonts / CDN — FREE |

### Why Montserrat Black 900

Montserrat Black 900 is the confirmed ETKM display font as of 2026-03-23.
Selected from a live comparison of Manrope 800, Montserrat 900, Oswald 700,
and Barlow Condensed 900. Nathan selected Montserrat Black immediately.
This is not a fallback — it is the standard.

- Free font — no licensing issues, available in all environments
- Available via CDN: `https://cdn.jsdelivr.net/fontsource/fonts/montserrat@latest/latin-900-normal.ttf`
- Available via Google Fonts: `https://fonts.googleapis.com/css2?family=Montserrat:wght@900`
- Embed as base64 in HTML files for offline/rendering environments

### Implementation — HTML / Social Graphics

```css
@font-face {
  font-family: 'Montserrat';
  font-weight: 900;
  src: url('data:font/ttf;base64,[BASE64]') format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-weight: 400;
  src: url('data:font/ttf;base64,[BASE64]') format('truetype');
}
@font-face {
  font-family: 'Inter';
  font-weight: 600;
  src: url('data:font/ttf;base64,[BASE64]') format('truetype');
}

/* Headline usage */
.headline {
  font-family: 'Montserrat', 'Arial Black', sans-serif;
  font-weight: 900;
  text-transform: uppercase;
}

/* Body / UI usage */
.body, .label, .url {
  font-family: 'Inter', Arial, sans-serif;
}
```

### Implementation — PDF (ReportLab)

Download and register Montserrat Black TTF before any PDF build:
```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Montserrat-Black', 'Montserrat-Black.ttf'))
```

### Implementation — PPTX

Use Arial Black as the closest system fallback when Montserrat is
not embeddable. Note in the Manus brief to substitute Montserrat Black
if the target machine has it installed.

### Typography Rules

- Montserrat Black headlines are ALWAYS uppercase in ETKM graphics
- Letter-spacing on headlines: -2px to -4px (tight — the weight earns it)
- Line height on headlines: 0.85–0.92 (stacked tight, Swiss International)
- Category labels (Inter SemiBold): uppercase, letter-spacing 6–8px, small size
- Body copy (Inter Regular): sentence case, normal letter-spacing
- Never stretch, distort, or embellish typography
- No decorative fonts anywhere in the system

---

## 4. Social Graphics Typography Scale

For 1080×1080 social graphics specifically:

| Element | Font | Weight | Size | Case | Color |
|---------|------|--------|------|------|-------|
| Category label | Inter | 600 | 22–26px | UPPER | #CC0000 |
| Main headline | Montserrat | 900 | 130–170px | UPPER | #FFFFFF |
| Supporting line | Montserrat | 900 | 38–48px | UPPER | #CC0000 |
| URL footer | Inter | 400 | 20–24px | UPPER | #444444 |

---

## 5. Visual Style and Geometry

### Layout Doctrine: Swiss International

- High contrast between elements
- Asymmetric grids — not centered, not symmetrical
- Aggressive use of negative space
- Massive typography as a design element, not just text
- Clean geometric shapes — no rounded corners unless functional
- Hard edges, sharp lines, defined boundaries

### Layout Patterns

| Pattern | When to Use |
|---------|-------------|
| Bold Black Foundation | Default for high-impact pieces — black bg, white type, red accent |
| Clean White Canvas | Documents, forms, instructional content |
| Split Screen | Before/after, two-concept layouts, event announcements |
| Red Accent Block | Single red bar draws attention to one element |
| Minimalist Text-Only | Quotes, slogans, Type B social graphics |
| Structured Grid | Multi-section content, dashboards, tables |
| Asymmetric Bold | Hero sections, landing pages, cinematic images |

### HTML Output Standard (LOCKED)

All HTML deliverables follow this standard without exception:

- Body background: `#000000`
- Card / surface background: `#111111`
- Text: `#FFFFFF` on black always
- Accent: `#CC0000`
- No light or white backgrounds on any HTML deliverable

---

## 6. Logo Standards

Three logo variants — use the correct one per background:

| Variant | File | Use On |
|---------|------|--------|
| White/Red circle | ETKM_Circle_Logo_White_Red.png | Dark backgrounds (social graphics, HTML) |
| White circle | ETKM_Circle_Logo_White.png | Dark backgrounds where red conflicts |
| Black/Red circle | ETKM_Circle_Logo_Black_Red.png | Light backgrounds (PDFs, DOCX) |

- Placement on social graphics: bottom right, always
- Size on 1080×1080: 110–120px
- Never compete with headline copy
- Embed as base64 in self-contained HTML/PDF files

---

## 7. Image and Photography Direction

- Cinematic, not stock photo
- B&W only — no color photography in graphics
- Subjects positioned with intentional sightlines and spatial awareness
- Back-turned or profile subjects preferred over direct-to-camera
- Environmental storytelling — setting communicates the message
- No violence in progress — awareness moment only
- Mood: quiet confidence, not aggression

---

## 8. What This Kit Prohibits

- Gradients of any kind
- Colors outside the 5-color palette
- Multiple red elements in a single view
- Any headline font other than Montserrat Black 900
- Rounded, playful, or whimsical design elements
- Stock photo aesthetic or color photography
- Centered-and-symmetrical layouts
- Decorative or script typography
- Drop shadows (unless subtle and functional)
- Borders on all four sides of an element
- Specific year counts for Nathan's experience —
  evergreen phrasing only: "a lifetime dedicated to self-protection",
  "over four decades", or "decades of experience"

---

*Version 4.0 — 2026-03-23*
*Montserrat Black 900 locked as permanent ETKM display font*
*Selected by Nathan Lundstrom from live comparison 2026-03-23*
*Maintained in: easttxkravmaga/Claude → skills/etkm-brand-kit/SKILL.md*
