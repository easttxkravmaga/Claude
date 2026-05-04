---
name: etkm-deliverable-qc
version: 2.2
updated: 2026-05-04
description: >
  Non-negotiable QC gate for ALL ETKM deliverables before they reach Nathan.
  Triggers any time a PDF, DOCX, HTML page, email sequence, slide deck, or printed
  asset is about to be handed off or marked complete. Also triggers for batch audits
  of multiple files. If you are about to call present_files or say "here is your
  [document]" — stop and run this checklist first. No deliverable ships without a
  passing QC run.
trigger: >
  Trigger phrases: "ready to deliver", "done", "here is the file", "finished",
  "ready for review", "QC this", "audit the deliverables", "check the files",
  "before we send", "final version". If you are about to present_files or deliver
  any document — stop and run this skill first.
dependencies:
  - etkm-brand-kit (visual standards reference for Gate 4)
  - etkm-brand-foundation (voice reference for Gate 5)
  - etkm-visual-qc (visual layout self-audit — runs as Gate 1.6 on all visual outputs)
  - pdf2image + pillow (required for Gate 1.5 visual render check on PDFs)
---

# ETKM Deliverable QC
## The gate between "built" and "delivered." Runs every time. No exceptions.

---

## Why This Skill Exists

Two incidents created this skill:

**Incident 1 — 2026-03-13:** A Reading Companion PDF was delivered with the intro/header
block repeating on every page, a chapter focus table with nearly every row truncated
mid-sentence, chapters 12-14 missing entirely, and a blank final page. None of these
were subtle. All were visible on first read. The file shipped anyway.
Root cause: content completion was treated as delivery readiness. They are not the same.

**Incident 2 — 2026-03-14:** A Curriculum Validation Brief was delivered with table cell
text overflowing and clipping — illegible content in the validation table. The automated
QC checker (pdfplumber text extraction) passed it because it reads characters, not visual
rendering. The problem was only caught when Nathan opened the file.
Root cause: automated text extraction cannot detect visual rendering failures. A visual
render check is mandatory for any PDF containing tables.

This skill is the permanent fix. It runs every time. Both incidents are now encoded as
mandatory check items that will never be skipped.

---

## The QC Gates — Run In Order

---

### GATE 1 — Structural Integrity
*Does the document exist and render as intended?*

- [ ] Does the document open and render without errors?
- [ ] Does any content that should appear once (title block, intro, header, cover text) repeat on multiple pages?
- [ ] Are there any blank or near-blank pages that should not exist?
- [ ] Is the page count consistent with the intended design?
- [ ] Do all page templates switch correctly — cover page uses cover template, interior pages use interior template, back page uses back template?
- [ ] Is the header/footer present on interior pages and absent on cover/back pages?

**KNOWN FAILURE — check first:**
Cover content bleeding to interior pages. Caused by page template not switching correctly.
Fix: ensure NextPageTemplate('Normal') flowable is inserted before the first PageBreak() in the story. Cover page placeholder must be an empty Paragraph object — never actual content.

**Failure here = do not proceed. Fix first.**

---

### GATE 1.6 — Visual Layout Self-Audit (ALL VISUAL OUTPUTS)
*Does this output pass ETKM visual brand standards?*

This gate runs on every output that has a visual layout: HTML pages, carousels, email templates,
PDFs, SVGs, React/JSX artifacts. It does NOT run on plain text, pure code, or internal planning docs.

**Load etkm-visual-qc and run the full protocol.**

Route by output type:
- Carousel: Section A + Section E
- HTML / web component / SVG / React: Section B + Section E
- Email template: Section C + Section E
- PDF: Section D + Section E

Section E (Universal Brand Standards) runs on all visual output types without exception.
Section F (Messaging Compliance) runs on any output with visible copy directed at students or prospects.

**Gate 1.6 report format (from etkm-visual-qc Section G):**
Visual QC — [Output Type]: [X]/[total] pass. STATUS: PASS / FAIL

**If Gate 1.6 FAILS:** Gate 4 (Brand and Visual Standards) automatically fails.
Rebuild the failing elements. Re-run Gate 1.6. Do not advance to Gate 2 until Gate 1.6 passes.

---

### GATE 1.5 — Visual Render Check (MANDATORY FOR ALL PDFs WITH TABLES)
*Can a human actually read everything on every page?*

This gate exists because pdfplumber text extraction cannot detect visual rendering failures.
A cell that clips its text passes automated text checks but fails visually.
This gate is non-negotiable for any PDF containing tables, multi-column layouts, or
dense content blocks.

**Run this procedure:**

```python
from pdf2image import convert_from_path
from PIL import Image

pages = convert_from_path(path, dpi=150)
for i, page in enumerate(pages):
    out = f"qc_page_{i+1:02d}.jpg"
    page.save(out, "JPEG", quality=90)
```

**Then visually inspect every page image:**

- [ ] Is all text in every table cell fully visible and not clipped?
- [ ] Does text wrap correctly within columns — no single-line overflow?
- [ ] Are all table rows fully rendered with complete content?
- [ ] Is the right edge of every page free of mid-word cuts?
- [ ] Are column dividers clean — no text bleeding across column boundaries?
- [ ] Is content in narrow columns (under 2 inches) still legible at normal reading size?

**How to distinguish header/footer dark pixels from overflow:**
Check where dark pixels appear in the right edge strip:
- Dark pixels concentrated at top and bottom only = header/footer bars = false positive
- Dark pixels in the middle section = potential text overflow = investigate

**KNOWN FAILURE — check first:**
Table cells built with raw Python strings instead of Paragraph objects. ReportLab
clips raw string content rather than wrapping it. Every table cell that contains more
than ~8 words must use a Paragraph object with an explicit style.

Fix pattern:
```python
# WRONG — clips text
rows = [['This is a long description that will be clipped', 'Another long value']]

# CORRECT — wraps text
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

cell_style = ParagraphStyle('cell', fontName='Helvetica', fontSize=9.5, leading=15)
rows = [[
    Paragraph('This is a long description that will wrap correctly', cell_style),
    Paragraph('Another long value that also wraps', cell_style)
]]
```

**Failure here = rebuild tables with Paragraph objects. Do not deliver.**

---

### GATE 2 — Text Completeness
*Is every sentence, cell, and list fully present?*

- [ ] Read every sentence. Does every sentence end completely?
- [ ] Read every table cell. Is any cell truncated, cut off, or missing its ending?
- [ ] Are there any mid-word cuts anywhere in the document?
- [ ] Does every list, numbered sequence, or outline run to its expected end?
- [ ] Are there any placeholder tokens, template variables, or unfilled fields visible (e.g., [INSERT], {{variable}}, TBD)?
- [ ] Does every section contain its full intended content — nothing was accidentally deleted or skipped during build?

**If any text is incomplete:** identify the source (column width too narrow, raw string
in table cell, overflow, missing content in data file) and fix before delivery.

---

### GATE 3 — Sequence and Completeness
*Does the document contain everything it is supposed to contain?*

- [ ] Does the section/chapter/module sequence run without gaps?
- [ ] If sections are numbered, do they count consecutively with no skips?
- [ ] If the document references a source outline or asset spec, does every item from that spec appear?
- [ ] Are all cross-references, links, and internal references pointing to real content that exists in the document?
- [ ] For the Field Manual specifically: are all 10 sections present including the Quick Reference Card back page?
- [ ] For the Validation Brief specifically: are all 7 sections present including the "Your Next Step" closing?
- [ ] For the Content Bank specifically: are all 6 banks (A-F) present with entries in each?

**KNOWN FAILURE — check first:**
Chapter sequence gaps. In the original Reading Companion, chapters 12-14 were missing
entirely from the chapter focus points table. Always count chapters against the book's
actual table of contents.

---

### GATE 4 — Brand and Visual Standards
*Does this look like an ETKM document?*

Gate 1.6 (etkm-visual-qc) is the full execution protocol for this gate.
If Gate 1.6 passed, Gate 4 passes for visual standard items.
Run the key checks below as a confirmation layer:

- [ ] Color palette: black (#000000/#111111), white (#FFFFFF), red (#CC0000), gray (#575757), light gray (#BBBBBB) only — no other colors
- [ ] No gradients anywhere
- [ ] Typography: Montserrat 900 headlines, Inter body (HTML) — Helvetica/Helvetica-Bold (PDFs)
- [ ] One red accent element per section — not multiple
- [ ] Headers and footers consistent on every interior page
- [ ] Cover page uses Bold Black Foundation (black background, white type, red accent)
- [ ] Interior pages use Clean White Canvas (white background, black type)
- [ ] ETKM logo present on cover page
- [ ] Swiss International layout — asymmetric, high contrast, no decorative elements
- [ ] Visual hierarchy is clear — reader can navigate without confusion
- [ ] No style drift between sections — consistent throughout
- [ ] No accent lines under section titles (AI hallmark — never acceptable)

---

### GATE 5 — Voice and Copy Quality
*Does this sound like ETKM?*

Reference etkm-brand-foundation skill for full standards. Key checks:

- [ ] Plain-spoken. Never clinical or academic.
- [ ] Direct. No hedging language ("it could be argued that," "perhaps," "one might consider")
- [ ] Principle-focused. Ideas connect to action.
- [ ] No prohibited words: mastery, dominate, destroy, killer, beast, crush, elite, warrior
- [ ] Tone consistent throughout — no shifts between formal, casual, or clinical
- [ ] Nathan's voice sections (closing statements, recommendations) sound like Nathan — advisor, not salesperson
- [ ] Grammar and spelling correct throughout
- [ ] If audience-facing: voice appropriate for the intended reader

---

### GATE 6 — Functional Elements
*Do all the working parts work?*

- [ ] URLs correct and formatted properly:
  - Primary site: etxkravmaga.com (NOT easttxkravmaga.com)
  - Student resource: etkmstudent.com
  - Fight Back: fightbacketx.com
- [ ] Phone number correct where present: 903-590-0085
- [ ] Email addresses accurate where present
- [ ] If the document is part of a numbered asset series (Asset 01, 02, 03, 04), is the asset number correct and consistent throughout?
- [ ] If the document contains fillable areas or reflection prompts, do they render correctly with adequate space?
- [ ] For HTML deliverables: does the page render correctly in a browser? Is it mobile-responsive?
- [ ] For DOCX deliverables: does the file open without errors and display correctly in Word?

---

### GATE 7 — Behavior Change Standard
*Does this document do what it was designed to do?*

This gate is specific to ETKM deliverables. Every front-facing asset must pass
the Hormozi standard: learning only happens if there is changed behavior.

- [ ] Can you state in one sentence the specific changed behavior this document is designed to produce?
- [ ] Does every section earn its place by moving the reader toward that behavior change?
- [ ] Does Asset 01 (Field Manual) end with a concrete, tiered action plan — this week / this month / permanent?
- [ ] Does Asset 02 (Validation Brief) end with a clear, specific next step for the person holding it?
- [ ] Does Asset 04 (Cheat Sheet HTML) have an action plan section with specific, concrete assignments — not vague advice?
- [ ] Is there any section that is purely informational with no connection to action? If yes — does it earn its place anyway, or should it be cut?

---

### GATE 8 — Final Read
*Would Nathan hand this to a student or prospect today?*

Before marking complete, read the entire document as a first-time reader — not as the
builder. Ask:

- [ ] Does this make sense to someone picking it up for the first time?
- [ ] Does it flow logically from beginning to end?
- [ ] Is there anything that would make a student, prospect, or parent trust ETKM less after reading this?
- [ ] Is there anything missing that a reader would expect to find?
- [ ] Would Nathan be comfortable handing this to a student or prospect today?

**If the answer to any of those is no — identify exactly what is wrong and fix it.**

---

## Batch Audit Protocol

When auditing multiple deliverables at once (e.g., a full book package):

1. List every file in the batch
2. Run all gates against each file independently
3. For each file, produce a findings report:

FILE: [filename]
STATUS: FAIL

GATE 1.6 — Visual Layout Self-Audit
  - Section B3: Centered layout detected on interior section — Swiss doctrine requires asymmetric
  - Section E6: #FF0000 found in button element — permanently retired, replace with #CC0000

GATE 3 — Sequence and Completeness
  - Chapter focus points missing Ch. 12, 13, 14

ACTION REQUIRED: Fix layout and color violations. Add missing chapters. Re-run QC.

4. Do not present any file to Nathan as complete until it has a PASS status
5. Deliver a summary table showing all files and their status before any file links

Summary table format:

| File | Pages | G1 | G1.6 | G1.5 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01_Field_Manual.pdf | 11 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 02_Validation_Brief.pdf | 7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

---

## Escalation Rule

If a QC failure is found in one file in a series, assume the problem exists in all files
until proven otherwise. Run the full batch audit before reporting back. Do not report a
single failure and wait — audit everything and come back with the full picture.

---

## Known Failure Pattern Registry

Every confirmed failure is logged here permanently. These are checked first in every QC run.

| Date | File | Failure Type | Gate | Fix Applied |
|---|---|---|---|---|
| 2026-03-13 | Gift_of_Fear_Reading_Companion_v1.pdf | Cover header block repeating on all interior pages | Gate 1 | NextPageTemplate() flowable before PageBreak() on cover page |
| 2026-03-13 | Gift_of_Fear_Reading_Companion_v1.pdf | Chapter focus table — all rows truncated mid-sentence | Gate 1.5 / Gate 2 | Paragraph objects required in all table cells |
| 2026-03-13 | Gift_of_Fear_Reading_Companion_v1.pdf | Chapter sequence skipping Ch. 12, 13, 14 | Gate 3 | Count chapters against source book's table of contents |
| 2026-03-13 | Gift_of_Fear_Reading_Companion_v1.pdf | Blank final page | Gate 1 | Remove empty story entries at document end |
| 2026-03-14 | Gift_of_Fear_Validation_Brief_v1.pdf | Validation table and vocab table — text clipped, not wrapping | Gate 1.5 | All table cells rebuilt with Paragraph objects and explicit styles |

When a new failure type is discovered, add it to this table immediately. It becomes a
permanent check item for all future deliverables.

---

## Quick Reference — Most Common Failures

**Page template bleed** (cover content on interior pages)
→ Missing NextPageTemplate('Normal') + PageBreak() transition

**Table cell text clipping**
→ Raw strings in table cells instead of Paragraph objects

**Missing chapters or sections**
→ Source data file incomplete or section accidentally skipped in story builder

**Blank trailing page**
→ Empty Paragraph or Spacer at end of story triggering a new page

**Wrong URL** (easttxkravmaga.com instead of etxkravmaga.com)
→ Always verify URLs against Gate 6 checklist

**Visual QC false positives** (dark pixels flagged at page edges)
→ Check if dark pixels are concentrated at top/bottom only (header/footer bars)
   vs. spread through middle (actual overflow). Middle = real problem.

**#FF0000 in any visual output**
→ Gate 1.6 / Gate 4 hard failure. Replace with #CC0000 everywhere.

**Accent lines under section titles**
→ Gate 1.6 / Gate 4 hard failure. Remove. This is an AI hallmark — never in ETKM output.

---

## Integration With etkm-book-intelligence

When processing books through the Book Intelligence System, run this QC skill
after every build step:

After build_01.py: QC Asset 01
After build_02.py: QC Asset 02
After build_03.py: QC Asset 03 (PDF and DOCX)
After build_04.py: QC Asset 04 (HTML)
All pass: package zip, deliver
Any fail: fix, rebuild, re-run QC, do not skip re-check

Never batch-deliver without independent QC on each file.
A passing Asset 01 does not mean Asset 02 passes.

---
*Version 2.2 — Updated 2026-05-04*
*Changes from V2.1: Added Gate 1.6 (Visual Layout Self-Audit) — fires etkm-visual-qc on all visual outputs.*
*Added etkm-visual-qc to dependencies. Updated Gate 4 to reference Gate 1.6 as primary execution protocol.*
*Updated batch audit summary table to include Gate 1.6 column. Added two new quick-reference failure entries.*
*Version 2.1 — Updated 2026-03-14*
*Incorporates visual render check (Gate 1.5) added after table clipping failure*
*Maintained by: Nathan Lundstrom / East Texas Krav Maga*