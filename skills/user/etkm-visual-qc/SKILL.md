---
name: etkm-visual-qc
version: 1.0
updated: 2026-05-04
description: >
  Visual layout and brand compliance self-audit protocol for ALL ETKM visual
  outputs. Claude runs this skill internally before delivering any visual
  deliverable — HTML pages, carousels, PDFs, email templates, SVGs, and web
  components. This skill does not wait for Nathan to ask. It runs automatically
  on every visual output as the final step before present_files or any delivery
  action. One failure = rebuild before delivery. No exceptions.
triggers:
  - "visual QC"
  - "check the layout"
  - "does this look right"
  - "review the design"
  - "QC the carousel"
  - "QC the HTML"
  - "QC the email"
  - "QC the PDF layout"
  - "before you deliver"
  - "visual audit"
  - "brand check"
  - "layout check"
  - "inspect the output"
  - "does this match the brand"
  - "carousel QC"
  - "HTML QC"
  - "email QC"
  - "PDF QC"
  - "SVG QC"
  - "visual standards check"
  - any visual deliverable about to be handed off
dependencies:
  - etkm-brand-kit v3.2 (all token values — authoritative source)
  - etkm-carousel-system v2.3 (carousel-specific Gate 1 + typography calibration)
  - etkm-web-production v1.0 (HTML/email/PDF build standard)
  - etkm-deliverable-qc v2.1 (overall QC gate — this skill plugs into Gate 1.6)
---

# ETKM Visual QC
## The visual inspection protocol Claude runs on every deliverable before it ships.

---

## Why This Skill Exists

Every ETKM visual output has locked design tokens, locked layout rules, and locked
brand standards. The failure mode is not ignorance of the rules — the rules are
documented in four places. The failure mode is that Claude builds something, it
looks roughly correct, and it gets delivered without a systematic inspection.

"Roughly correct" is not ETKM standard. ETKM standard is exact.

This skill exists to eliminate the gap between "I built it" and "it passes."
It forces Claude to inspect the output against the actual token values, not against
a memory of what it thinks the token values are, before any file is presented
to Nathan.

---

## Protocol Law — Applies Before Every Visual Delivery

**Rule 1:** This skill runs before every `present_files` call on any visual output.
If Claude is about to say "here is the file" or "here is the design" — stop. Run this
skill first. No exceptions.

**Rule 2:** Every check is binary. PASS or FAIL. No partial credit. No "mostly correct."
A FAIL on any item means rebuild that item before delivering.

**Rule 3:** Claude does not deliver a visual output with a known failure. If a failure
is found and cannot be immediately fixed, Claude reports the failure and the specific
fix required. Claude does not present the file and mention the issue after the fact.

**Rule 4:** Claude reports the QC result. Format:
```
Visual QC — [Output Type]: [X]/[total] pass. STATUS: PASS / FAIL
[If FAIL]: Gate [N] item [specific item]: [what is wrong] → [what fix is required]
```

**Rule 5:** When a failure is found in one element of a series or batch, assume the
same failure exists in all other elements. Audit the full batch before reporting back.

---

## Output Type Routing

Identify the output type first. Route to the correct section.

| Output Type | Route To |
|---|---|
| Instagram carousel (HTML slides) | Section A + Section E |
| HTML web page / landing page / component | Section B + Section E |
| Email template (HTML) | Section C + Section E |
| PDF (branded document, lead magnet) | Section D + Section E |
| SVG diagram or illustration | Section B (layout) + Section E (brand) |
| React/JSX artifact | Section B (layout) + Section E (brand) |

All output types run Section E (Universal Brand Standards) in addition to their
format-specific section. Section E is never skipped.

---

## Section A — Carousel Visual QC

*Covers: Instagram carousel slides built in HTML (400x500 display) for Playwright export to 1080x1350.*

Source authority: etkm-carousel-system v2.3 Section 9, etkm-brand-kit v3.2.

### A1 — Structural Fixed Layer (Every Slide)

Run on every slide in the carousel, including Type Z.

- [ ] Red bar present — left edge, full height, #CC0000, 25px wide, never removed
- [ ] Series badge present — top-left, #CC0000 background, #FFFFFF text, Montserrat 900, ALL CAPS
- [ ] Slide counter present — top-right, #BBBBBB, "01 / 09" format (zero-padded, spaces around slash)
- [ ] ETKM handle/logo present — bottom-left, #CC0000 (Type A-Y) or #333 (Type Z only)
- [ ] Swipe cue present on all slides except Type Z — bottom-right, #575757, ALL CAPS
- [ ] Bottom rule present — horizontal line at footer top, rgba(255,255,255,0.10) (0.06 on Type Z)
- [ ] No Tier 1 element has been moved, resized, or recolored

KNOWN FAILURE: Swipe cue carried onto Type Z. Fixed: "SWIPE" replaced with "ETKM.COM" on Type Z only.
KNOWN FAILURE: Red bar removed on Type Z. Fixed: Red bar is present on all slides including Type Z.

### A2 — Photo and Background Treatment (Slides A-Y)

- [ ] Same photo used across all body slides (Slides 01-08 or equivalent) — never per-slide variation
- [ ] Grayscale applied: 100%
- [ ] Brightness: 40%
- [ ] Contrast: +20%
- [ ] 4:5 portrait crop with action zone centered
- [ ] Black overlay present: 45% opacity (60% on Type Z)
- [ ] Type Z only: solid #CC0000 background, no photo, no overlay — this is the only permitted exception

KNOWN FAILURE: Type Z carrying a photo background. Fixed: Type Z is pure solid #CC0000, no photo layer.

### A3 — Typography Production Standard

Critical: HTML renders at 400px display. Export is 2.7x to produce 1080px production canvas.
Type that looks correct in preview is systematically undersized at production scale.

Verify every body headline against production canvas standard before passing:

| Role | Display Size (400px) | Production Equivalent (1080px) |
|---|---|---|
| H1 Cover | 46px | 124px |
| H1 Body 1-2 words/line | 60-72px | 162-194px |
| H1 Body 3-4 words/line | 46-54px | 124-146px |
| H1 Body 5+ words/line | 34-40px | 92-108px |
| Stat number | 90-100px | 243-270px |
| Quote text | 13-16px | 35-43px |
| CTA headline (Type Z) | 64-72px | 173-194px |

Minimum headline dominance rule: The largest headline on any slide must fill at
least 40% of slide width at production scale (432px of 1080px). If it does not — the
type is undersized. This is a Gate 1 failure. Increase until the dominance rule passes.

The 50% growth rule: When headlines feel undersized, the correction is approximately
+50% on affected body headlines. Timid type does not stop a scroll.

- [ ] Cover headline at 46px display minimum (124px production)
- [ ] All body headlines verified against word count per line sizing table
- [ ] Largest headline on each body slide fills at least 40% of slide width at production scale
- [ ] H2 sub-headline never #FFFFFF — must be rgba(255,255,255,0.60) to maintain hierarchy
- [ ] Body copy never used on Type A (cover) or Type Z (CTA)

KNOWN FAILURE: Headlines sized for the 400px preview, not the 1080px canvas — systematic undersizing.
Fixed: Apply 2.7x calibration check. Correct with +50% growth rule.

### A4 — Color Compliance

- [ ] #CC0000 appears in max three places per slide: red bar (always) + series badge background (always) + one optional H1 accent line
- [ ] #CC0000 never on body copy
- [ ] #CC0000 never on sub-headlines
- [ ] #FF0000 — confirm zero instances (permanently retired)
- [ ] No gradients anywhere
- [ ] Colors used: #000000, #FFFFFF, #CC0000, #575757, #BBBBBB, rgba opacity variants only

### A5 — Content Compliance

- [ ] All text within safe zone: horizontal 100-980px, vertical 80-1230px (display scale equivalent)
- [ ] Headline max-width: 320px display (864px production) — hard limit
- [ ] Body copy word count within type limits (max 40 words per body slide)
- [ ] Type Z: all 8 dynamic elements present (setup line, headline, accent line, command, separator, CTA button, transitional CTA, stakes line — omit stakes for Survivor arc)
- [ ] Type Z: .cta-command sits on one line — if it wraps, shorten the copy

### A6 — Series Integrity

- [ ] Series badge text consistent across all slides — content changes, never position/size/color
- [ ] Slide counter numbers sequential and correct throughout
- [ ] One photo per carousel — same photo on all body slides (A-Y)
- [ ] Slide type assignments match the approved arc map (never assign type before arc is locked)

---

## Section B — HTML / Web Component / SVG Visual QC

*Covers: WordPress page sections, landing pages, lead magnets, React artifacts, SVG diagrams.*

Source authority: etkm-web-production v1.0, etkm-brand-kit v3.2.

### B1 — Color Token Compliance

- [ ] No raw hex values in CSS — every color references a CSS variable or confirmed token
- [ ] Zero instances of #FF0000 (grep confirms)
- [ ] Zero gradients (grep gradient returns zero)
- [ ] Colors used: #000000/#111111 (black), #FFFFFF (white), #CC0000 (red), #575757 (gray), #BBBBBB (light gray) only
- [ ] Red buttons and red backgrounds carry color: #fff !important
- [ ] No background color outside: solid black, solid white — no gray backgrounds

### B2 — Typography Compliance

- [ ] Headlines: Montserrat 900 (loaded via Google Fonts CDN)
- [ ] Body: Inter 400 (loaded via Google Fonts CDN)
- [ ] No serif fonts, no decorative fonts, no script fonts
- [ ] No font-stretching or distortion
- [ ] Typography hierarchy visible: clear H1 to H2 to body distinction

### B3 — Layout and Spacing

- [ ] Swiss layout doctrine: asymmetric, high contrast, left-aligned default
- [ ] No centered layout except hero headlines and step numbers
- [ ] Aggressive negative space — layout does not feel crowded
- [ ] Hard edges — no rounded corners except functional buttons
- [ ] No drop shadows unless subtle and functional in a layered UI
- [ ] No borders on all four sides — use one or two sides maximum
- [ ] WordPress: H1 is never injected — injected HTML starts at H2
- [ ] WordPress: No bare element selectors (h2 { } bleeds into theme — must scope to wrapper)

### B4 — Image Treatment

- [ ] All images: filter: grayscale(100%) applied
- [ ] Every img element has: width, height, alt attributes
- [ ] Above-fold / LCP image: fetchpriority="high" — never loading="lazy"
- [ ] Below-fold images: loading="lazy"
- [ ] No CSS background image for LCP element — must be HTML img

### B5 — Interactive Elements

- [ ] All interactive elements are native HTML: button, a, input — never div onclick
- [ ] All clickable elements minimum 44x44px touch target
- [ ] Focus-visible outline: 2px outline, 3px offset — visible on every interactive element
- [ ] CTA buttons: red (#CC0000) background, white text with !important, action verb + specific destination

### B6 — Responsive Behavior

- [ ] Layout correct at 375px — no horizontal overflow, no broken columns
- [ ] Multi-column layouts collapse to single column below 768px
- [ ] Form inputs and body text: 16px minimum (prevents iOS zoom)
- [ ] Nothing clips or truncates on mobile

### B7 — Red Usage Compliance (Single Attention Element Rule)

- [ ] One red element per visual section — never two or more red elements in the same view
- [ ] Red is applied to: one word, one short phrase, one CTA button, one accent line — not paragraphs
- [ ] No decorative red bars on multiple sides, no red borders as decoration
- [ ] When red appears, all other elements are neutral (black, white, gray)

---

## Section C — Email Template Visual QC

*Covers: HTML event emails, Pipedrive campaign templates, nurture sequence HTML.*

Source authority: etkm-web-production v1.0 Output Standards (Email), etkm-brand-kit v3.2.

### C1 — Structure

- [ ] DOCTYPE is XHTML 1.0 Transitional
- [ ] Zero display: grid declarations
- [ ] Zero display: flex declarations
- [ ] Layout uses table elements throughout
- [ ] MSO conditional tables present for Outlook
- [ ] All layout, spacing, and typography is inlined (not in style block)
- [ ] Email container max-width: 600px

### C2 — Image Compliance

- [ ] All images use absolute https:// URLs (never relative paths)
- [ ] All img elements have display: block
- [ ] Image spec where applicable: 600x280px, PNG, under 200KB, B&W
- [ ] Images hosted at etxkravmaga.com/wp-content/uploads/etkm-email-headers/

### C3 — Client Compatibility

- [ ] Bulletproof VML button present for Outlook CTA
- [ ] Hidden preheader text present
- [ ] Dark mode @media (prefers-color-scheme: dark) present
- [ ] Web fonts have system font fallback stack (Arial, Helvetica, sans-serif)

### C4 — Brand Compliance

- [ ] Red top bar or red CTA button as primary red element
- [ ] Black footer
- [ ] Swiss grid structure — not centered with decorative elements
- [ ] No gradients
- [ ] No colors outside ETKM palette

### C5 — Token Verification

- [ ] All template tokens replaced before delivery: PREHEADER_TEXT, EVENT_TITLE, EVENT_DATE,
  EVENT_LOCATION, CTA_TEXT, CTA_URL, UNSUBSCRIBE_URL and all other merge tokens —
  zero unfilled tokens in the final output

---

## Section D — PDF Visual QC

*Covers: Branded PDFs, lead magnets, tier result PDFs, reading companions, handouts.*

Source authority: etkm-deliverable-qc v2.1 (Gates 1, 1.5, 4), etkm-brand-kit v3.2,
etkm-format-standards (Notion: 324924c8).

### D1 — Page Template Integrity

- [ ] Cover page uses cover template (black background, white type, red accent)
- [ ] Interior pages use interior template (white background, black type)
- [ ] Back page uses back template where applicable
- [ ] No cover content bleeding to interior pages
- [ ] NextPageTemplate('Normal') flowable inserted before first PageBreak() in story
- [ ] Cover placeholder is an empty Paragraph object — never actual content

KNOWN FAILURE: Cover content repeating on interior pages.
Fixed: NextPageTemplate('Normal') + PageBreak() transition after cover placeholder.

### D2 — Typography and Layout

- [ ] Cover title: Montserrat Black, 60pt, all caps (or Helvetica/Helvetica-Bold for ReportLab)
- [ ] Interior headers consistent on every interior page
- [ ] Header and footer absent on cover/back — present on all interior pages
- [ ] ETKM logo present on cover
- [ ] Nathan's title when present: "Self Protection Specialist - East Texas Krav Maga" — never "Founder"

### D3 — Table and Content Rendering

This check requires visual render inspection — automated text extraction will not catch these failures.

Run the visual render procedure when any table is present:
```python
from pdf2image import convert_from_path
pages = convert_from_path(path, dpi=150)
for i, page in enumerate(pages):
    page.save(f"qc_page_{i+1:02d}.jpg", "JPEG", quality=90)
```
Then visually inspect every page image:

- [ ] All text in every table cell fully visible — no clipping at cell boundary
- [ ] Text wraps correctly within columns — no single-line overflow
- [ ] All table rows fully rendered with complete content
- [ ] Right edge of every page free of mid-word cuts
- [ ] Column dividers clean — no text bleeding across boundaries

KNOWN FAILURE: Table cells built with raw Python strings clip text instead of wrapping.
Fixed: Every table cell with more than 8 words must use a Paragraph object with explicit style.

### D4 — Color and Brand

- [ ] Cover: Bold Black Foundation (black background, white type, red accent)
- [ ] Red stripe/accent: 5pt narrow column method — colWidths=[5, CONTENT_W-5], RED background
- [ ] No LINEBEFORE, LINEABOVE, LINEAFTER, LINEBELOW in RED except two approved QR exceptions
- [ ] Gate 4A grep audit: grep -n "LINEBEFORE|LINEABOVE|LINEAFTER|LINEBELOW" build_pdf.py | grep -i "red" — exactly 2 lines expected
- [ ] No gradients
- [ ] No colors outside ETKM palette
- [ ] #FF0000 absent (confirmed #CC0000 only)

### D5 — Structural Integrity

- [ ] No blank or near-blank pages
- [ ] Page count consistent with intended design
- [ ] No empty Paragraph or Spacer at end of story (triggers blank trailing page)
- [ ] Section/chapter sequence runs without gaps
- [ ] All cross-references point to content that exists in the document

---

## Section E — Universal Brand Standards

*Runs on ALL output types. Never skipped.*

Source authority: etkm-brand-kit v3.2.

### E1 — Color System

- [ ] All colors from ETKM 5-color palette only: #000000, #FFFFFF, #CC0000, #575757, #BBBBBB
- [ ] #FF0000 — zero instances (permanently retired sitewide)
- [ ] Zero gradients of any kind
- [ ] Solid black or solid white backgrounds only — no gray backgrounds
- [ ] White text on dark backgrounds; black text on light backgrounds — no contrast violations

### E2 — Typography

- [ ] Headlines: Montserrat 900
- [ ] Body: Inter 400
- [ ] No serif, decorative, or script fonts anywhere in the system
- [ ] No font stretching or distortion
- [ ] No accent lines under titles — hallmark of AI-generated content, never acceptable in ETKM output

### E3 — Layout Doctrine (Swiss International)

- [ ] Asymmetric grid — not centered, not symmetrical
- [ ] Aggressive use of negative space — layout does not feel dense or cluttered
- [ ] High contrast between elements
- [ ] Hard edges, sharp lines, defined boundaries
- [ ] Massive typography used as design element where appropriate
- [ ] No rounded corners except functional buttons
- [ ] No decorative elements, no ornaments, no illustration outside cinematic photography

### E4 — Red Usage (Single Attention Rule)

- [ ] One red element per view/section — maximum
- [ ] Red draws the eye to exactly one thing: one word, one phrase, one CTA, one command
- [ ] Red is never used for paragraphs, decorative bars on multiple sides, or multiple elements simultaneously
- [ ] When red appears, all surrounding elements are neutral (black, white, gray)

### E5 — Image Direction

- [ ] All photography: grayscale(100%) treatment
- [ ] Cinematic framing — not stock photo aesthetic
- [ ] Subject is the observer, not the observed (back-turned or profile preferred)
- [ ] No martial arts action shots unless specifically requested
- [ ] Tone: quiet confidence, not aggression

### E6 — Prohibited Elements (Hard Stop)

Any of these found = immediate rebuild before delivery:

- [ ] #FF0000 anywhere in the deliverable
- [ ] Any gradient
- [ ] Any color outside the 5-color palette
- [ ] More than one red element in a single view
- [ ] Centered, symmetrical layout (Swiss is asymmetric)
- [ ] Rounded, playful, or whimsical design elements
- [ ] Decorative fonts or script typography
- [ ] Multiple borders on all four sides of an element
- [ ] Serif fonts used as primary or headline type
- [ ] Accent lines under section titles (AI hallmark)
- [ ] Nathan's title as "Founder" — always "Self Protection Specialist - East Texas Krav Maga"

### E7 — Functional Element Verification

- [ ] Primary URL: etxkravmaga.com (NOT easttxkravmaga.com)
- [ ] Student portal: etkmstudent.com
- [ ] Fight Back site: fightbacketx.com
- [ ] Phone: 903-590-0085
- [ ] Location: Tyler, TX
- [ ] All URLs correct and properly formatted

---

## Section F — Messaging Compliance (Visual Copy)

*All visible copy in any visual output must pass these checks.*
*Source authority: etkm-brand-foundation v1.2.*

### F1 — StoryBrand Doctrine

- [ ] Student is hero — ETKM is guide — ETKM never positions itself as the hero
- [ ] Copy speaks to internal problem first (not just surface fear)
- [ ] ETKM introduced with empathy before authority
- [ ] CTA is bold and direct — action verb + specific destination
- [ ] CTA never uses: "Learn More", "Get Started", "Click Here", "Submit"
- [ ] Transformation is visible: copy shows who the student is becoming, not just what they're learning

### F2 — Voice

- [ ] Confident and direct — short sentences, active voice
- [ ] Warm and supportive — builds up, never shames
- [ ] Grounded — claims backed by specifics
- [ ] No aggressive, militaristic, or violent language
- [ ] No fear-heavy content without an immediate path to solution

### F3 — Prohibited Words

- [ ] Zero instances of: mastery, dominate, destroy, killer, beast, crush, elite, warrior
- [ ] No belt-based language — always skills/training-based
- [ ] No overpromises ("guaranteed outcomes", "win any fight")

---

## Section G — QC Report Format

After every visual QC run, Claude produces a report in this format:

VISUAL QC REPORT
Output type: [Carousel / HTML / Email / PDF / SVG]
Output name: [filename or description]
Date: [today's date]

SECTION A/B/C/D: [X]/[total] PASS
SECTION E (Universal Brand): [X]/7 categories PASS
SECTION F (Messaging): [X]/3 categories PASS

OVERALL STATUS: PASS / FAIL

If FAIL — list each failure:
FAILURE 1: [Section + item] — [exactly what is wrong] — [exactly what fix is required]
FAILURE 2: [Section + item] — [exactly what is wrong] — [exactly what fix is required]

If PASS: All checks passed. Delivering now.

Claude does not deliver the output until the report shows PASS on all sections.
If failures are found — rebuild, re-run QC, then deliver.

---

## Section H — Known Visual Failure Registry

Every confirmed visual failure is logged here permanently. These are checked first in every QC run.

| Date | Output Type | Failure | Section | Fix |
|---|---|---|---|---|
| 2026-04-xx | Carousel (Street Reality) | Headlines undersized — 400px preview used instead of 1080px production calibration | A3 | +50% growth rule applied; 2.7x calibration standard locked in carousel-system v2.3 |
| 2026-03-13 | PDF (Reading Companion) | Cover header block repeating on all interior pages | D1 | NextPageTemplate + PageBreak before first interior page |
| 2026-03-13 | PDF (Reading Companion) | Table cell text truncated — raw strings instead of Paragraph objects | D3 | All table cells >8 words rebuilt with Paragraph objects and explicit styles |
| 2026-03-14 | PDF (Validation Brief) | Validation table text clipped — visual QC false negative from text extraction | D3 | Visual render via pdf2image mandatory for all PDFs with tables |

When a new visual failure type is discovered, add it to this table immediately.
It becomes a permanent first-check item for all future runs.

---

## Section I — Integration with etkm-deliverable-qc

This skill integrates with etkm-deliverable-qc as Gate 1.6 — Visual Layout Self-Audit.
Gate 1.6 sits between Gate 1 (Structural Integrity) and Gate 2 (Text Completeness).

Gate 1.6 fires on:
- Any output with a visual layout component (HTML, carousel, email, PDF with layout, SVG)
- Any output where brand tokens could have been applied incorrectly
- Any output where typography sizing, color application, or layout structure could drift

Gate 1.6 does NOT fire on:
- Plain text outputs (emails written as plain text, markdown documents, pure copy)
- Code without visual output (Python scripts, JSON files, workflow configs)
- Internal planning documents not seen by students or prospects

Gate 1.6 output feeds directly into Gate 4 (Brand and Visual Standards) in etkm-deliverable-qc.
If Gate 1.6 fails, Gate 4 automatically fails. No deliverable proceeds past Gate 4 with an open Gate 1.6 failure.

Load sequence when visual output is being produced:
1. Build the output
2. Load etkm-visual-qc (this skill)
3. Route to correct section(s) based on output type
4. Run Section E (Universal) on everything
5. Run Section F (Messaging) on anything with visible copy
6. Produce Section G report
7. If PASS: proceed to remaining etkm-deliverable-qc gates
8. If FAIL: rebuild failing items, re-run etkm-visual-qc, do not advance until PASS

---

## Section J — Self-Audit Mental Model

When Claude inspects its own visual output, the inspection sequence is:

1. Token audit — Does every color, font, and size value match the locked token system?
   Start here. Wrong tokens produce wrong output at every scale.

2. Hierarchy audit — Is the visual hierarchy immediately clear?
   H1 dominant, H2 subordinate, body supporting. Anything competing with the headline must reduce.

3. Red audit — Where does red appear? Count the instances.
   One per view is the rule. More than one = failure.

4. Spacing audit — Does the layout breathe?
   Swiss doctrine demands aggressive negative space. Dense, crowded layouts violate the doctrine even if every element is technically correct.

5. Alignment audit — Is the grid logic consistent?
   Asymmetric does not mean random. The layout has a logic — is that logic consistent across the deliverable?

6. Copy audit — Is the student the hero?
   Final check on all visible copy. If ETKM is center stage and the student is secondary — the copy needs to flip.

7. Prohibition audit — Run E6.
   Hard stop on any prohibited element. No exceptions, no negotiation.

---

*Version 1.0 — Built 2026-05-04*
*Synthesized from: etkm-brand-kit v3.2, etkm-carousel-system v2.3, etkm-web-production v1.0,*
*etkm-deliverable-qc v2.1, ETKM Carousel System (Notion 34e924c8),*
*ETKM Format Standards (Notion 324924c8)*
*Maintained by: Nathan Lundstrom / East Texas Krav Maga*