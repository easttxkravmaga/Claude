---
name: etkm-pdf-sop
version: 1.0
updated: 2026-03-21
description: >
  Non-negotiable format SOP for every PDF built in the ETKM system.
  Load this skill at the start of ANY PDF build session before writing
  a single line of code. Covers cover page layout, interior page standards,
  typography minimums, color palette, content block specs, flow rules,
  QC checklist, and known failure patterns. This is the single source of
  truth for ETKM PDF production. If etkm-deliverable-qc is the gate,
  this skill is the blueprint.
trigger: >
  Trigger whenever building, rebuilding, or auditing any ETKM PDF.
  Phrases: "build a pdf", "make a pdf", "pdf format", "cover page",
  "interior pages", "action box", "CTA box", "section header",
  "font size", "pdf layout", "pdf standards", "before we build".
  Load alongside etkm-brand-kit for color/visual confirmation and
  etkm-deliverable-qc for the full QC gate protocol.
dependencies:
  - etkm-brand-kit (color and visual standards)
  - etkm-deliverable-qc (QC gate protocol)
---

# ETKM PDF FORMAT SOP
**Version:** 1.0
**Locked:** 2026-03-21
**Applies to:** Every PDF built in the ETKM system. No exceptions.

---

## COVER PAGE

- Full bleed black background `#000000`
- Red bar top: full width, 0.15" tall, pinned at `H - 0.46"`
- Red bar bottom: full width, 3pt, pinned at `0.58"`
- Series label: centered between top bar and top of page, 7.5pt Helvetica-Bold, LTGRAY
- URL: centered between bottom bar and bottom of page, 8.5pt Helvetica, LTGRAY
- **Title block: entire block (title + byline) treated as one unit. Position as-is when it looks right — do not over-engineer the vertical math.**
- Title line 1: Helvetica-Bold 80pt, WHITE (single large word or number)
- Title line 2: Helvetica-Bold 58pt, WHITE (long word or phrase)
- Red rule below title: full text width, 6pt, `#CC0000`
- Subtitle bold: Helvetica-Bold 19pt, WHITE
- Subtitle descriptor: Helvetica 12pt, `#888888`
- Thin divider: 0.5pt, `#444444`
- FROM label: Helvetica 8pt, LTGRAY
- Name: Helvetica-Bold 16pt, WHITE — always "Nathan Lundstrom"
- Title line: Helvetica 10pt, LTGRAY — always "Self Protection Specialist  ·  East Texas Krav Maga"

---

## INTERIOR PAGES

- White background `#FFFFFF`
- Margins: Left 0.7" / Right 0.7" / Top 0.68" / Bottom 0.78"
- Footer on every interior page:
  - Left: "East Texas Krav Maga  ·  etxkravmaga.com" — 8pt Helvetica, GRAY
  - Right: "Page N" — 8pt Helvetica, GRAY
  - LTGRAY rule above footer at 0.57"
- No footer on cover page

---

## TYPOGRAPHY MINIMUMS (NON-NEGOTIABLE)

| Element | Minimum Size |
|---|---|
| Body text / paragraphs | 11pt |
| Section labels (WHAT IT IS, WHY IT MATTERS, etc.) | 8.5pt |
| Table cell body | 9.5pt |
| Section headers (H2) | 14pt |
| Cover subtitle bold | 19pt |
| Cover name | 16pt |
| Footer text | 8pt |
| Captions / labels | 8.5pt — never below this |

**If any text falls below these minimums — fix it before delivery.**

---

## COLOR PALETTE (NON-NEGOTIABLE)

| Color | Hex | Use |
|---|---|---|
| Black | `#000000` | Cover background, section header bars |
| White | `#FFFFFF` | Body text on dark, interior page background |
| Red | `#CC0000` | One accent element per section — never decorative |
| Dark Gray | `#222222` | Callout bar backgrounds |
| Gray | `#575757` | Footer text |
| Light Gray | `#BBBBBB` | Dividers, secondary text |
| Off-White | `#F2F2F2` | Action boxes only |

- No gradients. Ever.
- No colors outside this palette. Ever.
- Maximum one red element per visual section.

---

## CONTENT BLOCKS

### Section Header Bar (PrincipleHeader / HeaderBar)
- Black background `#000000`
- Red left stripe with number: 0.50" wide, `#CC0000`
- Label: 7.5–8pt Helvetica-Bold, LTGRAY, uppercase
- Headline: 14–16pt Helvetica-Bold, WHITE
- Height: 1.05"

### Action Box (ONE THING TO DO THIS WEEK)
- Background: `#F2F2F2`
- Border: 1pt `#DDDDDD`, rounded corners 3pt
- Red left accent bar: 3pt wide
- Body text: Helvetica 10.5pt, BLACK
- Used exclusively for action assignments

### Callout Bar
- Background: `#222222`
- Red left bar: 4pt wide
- Text: Helvetica-BoldOblique 10.5pt, WHITE
- Used for pull quotes and key statements

### CTA Box
- Background: `#000000`, rounded corners 6pt
- Red left bar: 5pt wide
- Headline: Helvetica-Bold 14pt, WHITE
- Sub: Helvetica 10pt, LTGRAY
- Label: Helvetica 9pt, LTGRAY uppercase
- URL: Helvetica-Bold 13pt, WHITE — always "etxkravmaga.com/free-trial"
- Always the final element on the last content page

### Section Labels (WHAT IT IS / WHY IT MATTERS / etc.)
- 8.5pt Helvetica-Bold, `#CC0000`
- Placed directly above the body paragraph they introduce
- No background, no box — label only

---

## CONTENT FLOW RULES

- **No forced PageBreaks between principles or sections** — let content flow naturally
- `KeepTogether` on every header + first paragraph — headers never orphan
- No blank trailing pages — remove any empty Paragraph or Spacer at end of story
- Half-empty pages are a layout failure — adjust spacing or content before delivery
- Sections flow 2-per-page naturally at standard body text length

---

## QC CHECKLIST — RUN BEFORE EVERY DELIVERY

Run `pdf2image` render at 120dpi. Visually inspect every page. No skipping.

- [ ] Cover: all elements present, no overlap, no text touching red bars
- [ ] Cover: "Self Protection Specialist · East Texas Krav Maga" present
- [ ] Cover: URL "etxkravmaga.com" in footer
- [ ] Interior: no half-empty pages
- [ ] Interior: no orphaned headers
- [ ] Interior: all action boxes rendering with gray background and red bar
- [ ] Interior: footer present on every page except cover
- [ ] Final page: CTA box present and fully rendered
- [ ] URL correct throughout: etxkravmaga.com (never easttxkravmaga.com)
- [ ] No prohibited words: mastery, dominate, destroy, killer, beast, crush, elite, warrior
- [ ] No specific year count — "a lifetime dedicated to self-protection" only
- [ ] All font sizes at or above minimums
- [ ] No gradients, no off-palette colors

---

## KNOWN FAILURE PATTERNS — CHECK FIRST

| Failure | Cause | Fix |
|---|---|---|
| Cover content bleeding to p2 | Missing `PageBreak()` after cover callback | Add `PageBreak()` as first story item |
| Half-empty pages | Forced `PageBreak()` between short sections | Remove — let content flow |
| Header orphaned at page bottom | Missing `KeepTogether` | Wrap header + first para in `KeepTogether` |
| Action box text clipped | Raw string instead of dynamic height | Use `wrap()` method to calculate height from text |
| Wrong URL | Typo | Always etxkravmaga.com — audit every build |
| Title too small on cover | Using wrong font size tier | 80pt for 1–2 char, 58pt for full word |
