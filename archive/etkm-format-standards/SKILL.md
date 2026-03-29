---
name: etkm-format-standards
version: 1.0
updated: 2026-03-15
description: >
  Use this skill whenever building, editing, or delivering any ETKM document,
  email, presentation, or PDF. Contains locked format standards for all 5 ETKM
  output formats: HTML, PDF, DOCX, Email, and PPTX. Load alongside etkm-brand-kit
  for any production deliverable. Trigger phrases: "build a PDF", "create a slide
  deck", "write an email template", "make a Word doc", "DOCX", "PPTX",
  "presentation", "email template", "HTML page", "format standard", "deliverable",
  "build script", "locked standards". If you are producing any file that will be
  delivered to Nathan, students, or prospects — load this skill first.
dependencies:
  - etkm-brand-kit (visual standards)
  - etkm-deliverable-qc (QC gates before delivery)
---

# ETKM Format Standards
## All 5 formats locked. Do not deviate without Nathan's explicit instruction.

**Notion reference:** https://www.notion.so/324924c816738198b3f9ea7cf7f3100e

---

## Brand Constants (Universal)

| Token | Hex | Usage |
|---|---|---|
| BLACK | #000000 / 000000 | Backgrounds, headlines |
| WHITE | #FFFFFF / FFFFFF | Content backgrounds, reversed text |
| RED | #CC0000 / FF0000 | One accent per section maximum |
| GRAY | #575757 / 575757 | Body text, captions |
| LT_GRAY | #F2F2F2 / F2F2F2 | Alternating rows, callout backgrounds |
| MID_GRAY | #BBBBBB / BBBBBB | Rules, dividers, secondary text |
| NEAR_BLK | #111111 / 111111 | Dark content backgrounds |

Note: PPTX requires hex WITHOUT # prefix (pptxgenjs corrupts on #CC0000 — use FF0000)

---

## HTML — LOCKED

- Fonts: Barlow Condensed Black (headlines) + Inter (body)
- Layout: 1200px max-width, full-bleed sections, Swiss International
- Nav: Black sticky, red 2px bottom border
- Hero: Black background, oversized condensed type
- Left anchor: Large number (80px) + red category tag
- Image Treatments (3 types — all locked):
  - A: Full-width, dimmed, text overlay with gradient
  - B: 50/50 two-column, image left, red left-border panel right
  - C: Contained max-width, image above white caption block
- Diagrams: Canva export PNG only — no inline SVG
- Scroll animations: Triggered on scroll

**HTML Color Rules (Non-Negotiable):**
- Background: #000000
- Surfaces/cards: #111111 or #1a1a1a
- Text: #FFFFFF primary, #BBBBBB secondary
- Accent: #CC0000 only (one element per view)
- Light backgrounds are a format violation — no white or light backgrounds on any HTML deliverable

---

## PDF — LOCKED

- Page: Letter 8.5×11, 0.75" margins
- Cover: Black background, red left stripe, white/red title, identity bar
- Header: Black bar, red 2pt rule, title left, ETKM right
- Footer: Light gray, contact left, page number right

**Gate 4A — Red Stripe Rule (NON-NEGOTIABLE):**
- Every red stripe = 5pt narrow column: `colWidths=[5, CONTENT_W-5]`, RED background
- Stripe column: TOPPADDING=0, BOTTOMPADDING=0 explicitly set — never inherit
- ZERO use of LINEBEFORE/LINEABOVE/LINEAFTER/LINEBELOW in RED except 2 approved exceptions:
  - Video QR block LINEABOVE
  - Audio QR block LINEABOVE
- Run before every PDF delivery:
  `grep -n "LINEBEFORE\|LINEABOVE\|LINEAFTER\|LINEBELOW" build_pdf.py | grep -i "red"`
  Expected: exactly 2 results. Any other result = hard failure, fix before delivery.

- Build tool: ReportLab (Python)
- Build script: build_pdf.py

---

## DOCX — LOCKED

- Page: Letter 8.5×11, 1" margins
- Background: WHITE throughout — no dark cover, no black sections
- Font: Arial throughout — no external dependencies
- Title block: Red bottom rule under title, italic subtitle, no cover page
- Headings: `keepWithNext: true` — labels and titles never orphan from body
- Red accent method: Paragraph-level left border (THICK, 24pt, RED, space: 12)
  - NOT table wrappers — paragraph borders only
- Checklist items: □ (Unicode square) in RED + Arial body
- Tables: Dual widths required — `width` on table AND `width` on each cell, both DXA
- Header/Footer: Tab stops — NOT tables
- Target density: ~3 pages for standard handout
- Build tool: docx-js (Node.js)
- Build script: build_docx.js

---

## Email — LOCKED (Two-Track System)

### Track 1: Plain Text (Communication Emails)
- Use for: WF-001/002 sequences, 1:1 follow-ups, private lessons, re-engagement
- Platform: Pipedrive 1:1 email templates
- Voice: Nathan writing to one person. Short sentences. One ask per email.
- Max length: 150 words for follow-ups
- 5 templates: Trial follow-up, Re-engagement, Private lesson follow-up,
  Cold/referral outreach, Event save-the-date
- File: email-plain-text-templates.txt

### Track 2: HTML Event Template
- Use for: Seminars, events, CBLTAC-style campaigns
- Platform: Pipedrive Campaigns → Upload HTML
- Container: 600px, single-column, mobile-responsive
- Structure: Header bar → Image header → Hero (black) → Body + detail block
  → CTA → Signature → Footer
- Image swap: Change `src` in `<!-- IMAGE SWAP -->` comment block
- Image host: etxkravmaga.com/wp-content/uploads/etkm-email-headers/
  - Arc images: .../arc/ (audience-based, 6 images)
  - Subject images: .../  (topic-based, 10 images + CBLTAC.png)
- Image spec: 600×280px, PNG, under 200KB, B&W
- File: email-html-event-template.html
- Tokens: {{PREHEADER_TEXT}} {{EVENT_TYPE_LABEL}} {{EVENT_TITLE}}
  {{EVENT_DATE}} {{EVENT_LOCATION}} {{OPENING_PARAGRAPH}} {{BODY_PARAGRAPH}}
  {{DETAIL_WHAT}} {{DETAIL_WHEN}} {{DETAIL_WHERE}} {{DETAIL_WHO}}
  {{CLOSING_PARAGRAPH}} {{CTA_TEXT}} {{CTA_URL}} {{UNSUBSCRIBE_URL}}

---

## PPTX — LOCKED

- Layout: LAYOUT_16x9 (10" × 5.625")
- Fonts: Arial Black (headlines) + Arial (body)
- CRITICAL: No # prefix on hex colors in pptxgenjs — use FF0000 not #CC0000
- Never reuse option objects across shape calls (pptxgenjs mutates in-place)
- Never use accent lines under titles
- All diagrams: Canva export PNG → insert as image. Never build diagrams in PPTX.
- Build tools: pptxgenjs (Node.js)
- Build scripts: build_pptx.js (7 slides) / build_pptx_options.js (20 slides)

**Consistent elements on every slide:**
- Black header bar: label left (RED, charSpacing 3), ETKM right (MID_GRAY)
- Section title with black bottom rule
- Red left stripe (0.08") as primary accent
- Footer bar (LT_GRAY): etxkravmaga.com · 903-590-0085 · Tyler, TX

**20 locked slide types:**
01 Title (black)          08 Full-bleed image        15 Problem/Solution
02 Section divider        09 Image left/text right   16 Numbered sequence
03 Content single col     10 Big stat callout         17 Step-by-step 4-col
04 Two column table       11 Before/After             18 Spectrum/scale
05 Quote/principle        12 Video+audio QR           19 Pyramid hierarchy
06 Checklist              13 Diagram slot (Canva)     20 PEACE cycle
07 Closing/CTA            14 Scenario narrative

---

## Canva Diagram Library

Design ID: DAHBWJFkfVA

| Page | Diagram |
|---|---|
| 16–17 | OODA loop (4-node circular) |
| 22–26 | Decision tree variants |
| 42 | MINDSET/TACTICS/SKILLS/KIT pyramid |
| 47 | Training evaluation cycle (6-node) |
| 13–15 | Circle infographics |

Workflow: Build in Canva → export PNG → embed in PDF/DOCX/PPTX as image

---

## QC Skill

Load `etkm-deliverable-qc` (v3.0) before any delivery.
8 gates: Structural integrity → Visual render → Text completeness →
Sequence → Brand/visual (includes Gate 4A red stripe) → Voice →
Functional elements → Behavior change → Final read

GitHub: easttxkravmaga/Claude → skills/etkm-deliverable-qc/SKILL.md
Commit: 08e688a

---

## Key URLs

- Primary: etxkravmaga.com
- Student: etkmstudent.com
- Fight Back: fightbacketx.com
- Email headers: etxkravmaga.com/wp-content/uploads/etkm-email-headers/
- Phone: 903-590-0085 · Tyler, TX

---

*Version 1.1 — 2026-03-17*
*Format audit complete. All 5 formats locked.*
*Maintained by: Nathan Lundstrom / East Texas Krav Maga*
