---
name: etkm-brand-kit
version: 4.0
updated: 2026-03-25
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

companion_skills:
  required_by_type:
    pdf:     [etkm-pdf-pipeline, etkm-deliverable-qc]
    html:    [etkm-deliverable-qc]
    docx:    [etkm-deliverable-qc]
    pptx:    [etkm-deliverable-qc]
    diagram: [etkm-deliverable-qc]
  always_load:
    - etkm-deliverable-qc  # Run before EVERY delivery — no exceptions

mandatory_workflow: >
  Loading this skill is Step 1 of production. Before writing a single line of code
  or content, identify the deliverable type and load the companion skill(s) listed
  above. QC runs last — before present_files, before handoff, before "done."
  The chain is always: Brand Kit → Type Skill → Build → QC → Deliver.
---

# ETKM Brand Kit
**Version:** 4.0
**Last Updated:** 2026-03-25

---

## ⚠️ MANDATORY COMPANION SKILLS — LOAD BEFORE BUILDING

This skill defines the visual identity. Companion skills define how each deliverable
type is built and validated. They are not optional add-ons — they are part of the
same production standard.

**Before building anything, load the companion skill for the deliverable type:**

| Deliverable Type | Load These Skills (in order) |
|-----------------|------------------------------|
| **PDF** | `etkm-brand-kit` → `etkm-pdf-pipeline` → build → `etkm-deliverable-qc` |
| **HTML** (any web page, block, landing page) | `etkm-brand-kit` → build → `etkm-deliverable-qc` |
| **DOCX** (Word document) | `etkm-brand-kit` → `docx` (public skill) → build → `etkm-deliverable-qc` |
| **PPTX** (Presentation) | `etkm-brand-kit` → `pptx` (public skill) → build → `etkm-deliverable-qc` |
| **Diagram / Visual Aid** | `etkm-brand-kit` → `etkm-diagram` (when built) → build → `etkm-deliverable-qc` |

**QC is the final gate before every delivery — no exceptions.**
If you are about to call `present_files` without having run `etkm-deliverable-qc` —
stop. Run QC first.

---

## Why This Matters

Every time a font is wrong, a background is white when it should be black, or a
heading uses the wrong typeface — it is because a companion skill was skipped.
These are not judgment calls. They are the standard. The companion skills encode
the standard so it doesn't have to be re-learned or re-corrected session after session.

---

## 1. Color Palette (Non-Negotiable)

| Color | Hex | Role |
|-------|-----|------|
| Black | #000000 | Primary background |
| Surface | #111111 | Card backgrounds, elevated surfaces |
| White | #FFFFFF | Primary text on dark backgrounds |
| Red | #CC0000 | Attention only — one element per section |
| Gray | #575757 | Supporting elements, secondary text |
| Lite Gray | #BBBBBB | Body text on dark backgrounds, dividers |

### Color Rules

- **HTML deliverables:** Body background is always `#000000`. Surfaces are `#111111`.
  Text is `#FFFFFF` (headlines) and `#BBBBBB` (body). This is non-negotiable and applies
  to every HTML file produced for ETKM — web pages, WordPress blocks, landing pages,
  email templates, and any other HTML deliverable.
- **PDF deliverables:** Cover page is black background. Interior pages are white
  background with black header bar and single red accent rule.
- **DOCX deliverables:** White background, black text, black header bar, red accent line.
- Backgrounds: Solid Black or Solid White only. Never gray backgrounds.
- Gradients: Prohibited. No exceptions.
- No other colors exist in the ETKM system.

---

## 2. Red Usage (Attention Only)

Red (#CC0000) is a weapon, not decoration. It draws the eye to exactly one thing.

- Use for: One word, one short phrase, one CTA button, one warning, one decision point.
- Do NOT use for: Paragraphs, full backgrounds, multiple elements per section, decorative borders.
- Maximum: One red element per visual section.
- When red appears, all other elements must be neutral (black, white, gray).

### Proven Red Applications

| Context | Red Usage |
|---------|-----------|
| HTML pages | CTA button background, single accent rule, phase dot, kicker label |
| PDFs | 3px rule below header, cover accent, single attention phrase |
| DOCX | Single red accent line below header |
| Email templates | Red top bar, red CTA button |
| Social media | One accent element per image |

---

## 3. Typography System (Non-Negotiable)

### Primary Type Stack

| Role | Font | Weight |
|------|------|--------|
| Headlines (H1, H2, display) | Montserrat | 900 Black — default for maximum impact |
| Subheadings (H3, H4) | Montserrat | 700–800 Bold/ExtraBold |
| Labels, kickers, captions | Montserrat | 700 Bold, uppercase, letter-spacing |
| Body text, paragraphs | Inter | 400 Regular |
| Supporting body, strong | Inter | 500 Medium or 600 SemiBold |

### Typography Rules

- **HTML:** Load via Google Fonts CDN. Never fall back to system fonts.
  `@import` from `fonts.googleapis.com` — both Montserrat and Inter required.
- **PDF:** Fonts MUST be base64-encoded into `@font-face` declarations.
  No CDN imports in headless Playwright. See `etkm-pdf-pipeline` for embedding script.
- **DOCX:** Use Arial as the closest system-available substitute. Montserrat
  is not a system font — Arial Bold approximates the weight.
- Never stretch, distort, or substitute decorative fonts.
- Uppercase with wide letter-spacing for labels and category headers.

---

## 4. Visual Style and Geometry

### Layout Doctrine: Swiss International

- High contrast between elements
- Asymmetric grids — not centered, not symmetrical
- Aggressive use of negative space
- Massive typography as a design element, not just text
- Clean geometric shapes — no rounded corners unless functional (buttons only)
- Hard edges, sharp lines, defined boundaries
- One red element per section draws the eye — everything else is neutral

### Layout Standards by Type

| Type | Standard |
|------|----------|
| HTML | Black body (#000), surface cards (#111), white headlines, #BBBBBB body text, CC0000 red accent |
| PDF cover | Black background, white Montserrat 900 headline, 3px red rule, Inter body in #BBBBBB |
| PDF interior | White background, black header bar, 3px red rule, black body text |
| DOCX | White background, Arial Bold headings, black header bar, single red accent line |
| Email | Red top bar (#CC0000), black footer, Swiss grid, red CTA button |

---

## 5. Logo and Identity — APPROVED FILES ONLY

**RULE: Text logos are NEVER used. No "ETKM." No "ETKM" typed in any font. Always use approved PNG files.**

### Approved Logo Files

| File | Version | Use When |
|------|---------|----------|
| `ETKM_Circle_Logo__2_.png` | Circle — white outline | Default web use, nav, footer, email header — on black background |
| `ETKM_Circle_Logo__4_.png` | Circle — dark/blend | When circle should be subtle on black — red text and icon visible |
| `2.png` (wordmark white) | Wordmark — white | Footer alongside circle, email header, banner |
| `1.png` (wordmark dark) | Wordmark — embossed | Background texture, watermark only — not primary identification |

### Logo Placement Rules

- Circle logo: nav (44–56px height), footer (48–64px height), PDF cover only — never interior pages
- Wordmark: alongside circle in footer and email header, or alone in wide-format contexts
- Always on black (#000) or transparent background — never on white or light backgrounds
- Never stretch, distort, apply filters, drop shadows, or additional effects
- Never recreate the logo in CSS, SVG, or typed text

### Prohibited

- ❌ "ETKM." — not an approved logo
- ❌ "ETKM" typed in Montserrat or any font — not an approved logo  
- ❌ Logo on white or light backgrounds
- ❌ Any logo not in the approved file list above

---

## 6. Image and Photography Direction

- Cinematic, not stock photo
- Desaturated or monochromatic base with red as single color accent
- Subjects positioned with intentional sightlines
- Back-turned or profile subjects preferred over direct-to-camera
- Environmental storytelling — setting communicates the message
- No martial arts action shots unless specifically requested
- Mood: quiet confidence, not aggression

---

## 7. What This Kit Prohibits

- Gradients of any kind
- Colors outside the 5-color palette
- Multiple red elements in a single section
- Rounded, playful, or whimsical design elements
- White or light backgrounds on HTML deliverables
- Centered-and-symmetrical layouts (Swiss style is asymmetric)
- Decorative fonts or script typography
- Drop shadows unless subtle and functional
- Borders on all four sides of an element (one or two sides maximum)
- Any font other than Montserrat (headlines) and Inter (body) on HTML/PDF deliverables

---

## 8. QC Before Delivery — Always

**The production chain is:**
```
Load Brand Kit → Load Type Skill → Build → Run etkm-deliverable-qc → Deliver
```

No deliverable reaches Nathan without a passing QC run.
If you are about to call `present_files` — stop and run `etkm-deliverable-qc` first.

---

*Version 4.0 — Updated 2026-03-25*
*Added: companion skill references, mandatory workflow chain, HTML black background rule locked*
*Typography updated: Montserrat + Inter locked across all types. Arial for DOCX only.*
*Maintained by: Nathan Lundstrom / East Texas Krav Maga*

---

## 8. Outbound References

Skills that build outputs governed by this brand kit:

| Skill | What It Governs |
|-------|----------------|
| `etkm-webpage-build` | HTML page visual standard — hero spec, sections, fonts, breakpoints |
| `etkm-webform-build` | Form CSS standard — input styles, button colors, label typography |
| `etkm-pdf-pipeline` | PDF design system — same fonts and palette, HTML→Playwright pipeline |
| `etkm-event-page` | Event landing page patterns — inherits all page standards |
| `etkm-social-graphics` | Social canvas specs — brand palette applied to platform formats |

Any skill that produces a visual output for ETKM should reference this skill.
This brand kit IS the standard — it has no QC gates because all other skills
gate against it.
