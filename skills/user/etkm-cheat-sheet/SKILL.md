---
name: etkm-cheat-sheet
version: 2.1
created: 2026-03-14
updated: 2026-03-15
description: >
  Canonical format and build system for the ETKM Asset 04 Cheat Sheet. Load this skill
  whenever building, repairing, auditing, or adding a new book to the cheat sheet system.
  Trigger phrases: "build the cheat sheet", "Asset 04", "book cheat sheet", "ETKM cheat
  sheet", "cheat sheet for [book title]", "add a new book", "make the HTML for the book",
  "update the book data", or any session where a cheat sheet HTML file is being produced
  or revised. CRITICAL: This skill runs the FULL automated pipeline end-to-end without
  asking Nathan for extra steps. Nathan never runs commands manually. Claude does it all.
dependencies:
  - etkm-brand-kit (visual standards)
  - etkm-book-intelligence (source data — extraction must be complete before building)
  - etkm-deliverable-qc (QC protocol — runs automatically as part of the pipeline)
---

# ETKM Cheat Sheet System — v2.1
## Asset 04 | Book Intelligence Series | Fully Automated Pipeline

---

## THE PRIME DIRECTIVE

**Nathan never runs commands. Nathan never remembers extra steps. Claude handles the
complete pipeline automatically, every time, without being asked.**

When Nathan says "build the cheat sheet for [book]" — Claude:
1. Creates the JSON data file
2. Runs the build script
3. Runs QC
4. Pushes to GitHub
5. Reports back with a clean one-line summary

No "here's the command to run." No "now push to GitHub." No extra steps.
The pipeline is invisible to Nathan. The output appears.

---

## Automated Pipeline — Run Every Time

```
Trigger: "build the cheat sheet for [book]"

Step 1  CREATE — Build data/[book_id].json from the book extraction
Step 2  BUILD  — Run: python build/build.py [book_id] --verbose
Step 3  QC     — Run etkm-deliverable-qc on output/04_[book_id]_cheat_sheet.html
Step 4  PUSH   — Commit and push to GitHub (easttxkravmaga/Claude repo)
Step 5  REPORT — One clean summary: what was built, QC status, GitHub link
```

Claude runs all 5 steps in sequence without pausing for input between them.
If a step fails, Claude fixes it and continues — never stops to ask Nathan to do it.
The only time Claude pauses is if it genuinely needs content from Nathan that
cannot be derived from the book extraction (extremely rare).

---

## What "Automatic" Means For Each Step

### Step 1 — CREATE the JSON
Claude builds the complete JSON file from the Layer 1–3 extraction data.
No template to fill in manually. Claude fills every field. Claude validates it.
Output: `data/[book_id].json`

### Step 2 — BUILD the HTML
Claude runs `python build/build.py [book_id] --verbose` using the bash tool.
If Jinja2 is not installed: Claude runs `pip install jinja2 --break-system-packages` first.
Output: `output/04_[book_id]_cheat_sheet.html`

### Step 3 — QC
Claude runs the etkm-deliverable-qc checklist against the output file automatically.
If QC fails: Claude fixes the JSON, rebuilds, and re-runs QC. Nathan never sees failures.
Output: PASS confirmation (or fixed file)

### Step 4 — PUSH to GitHub
Claude uses Claude in Chrome to push both the JSON and HTML to the repo.
Repo: easttxkravmaga/Claude
Paths:
  - skills/user/etkm-cheat-sheet/data/[book_id].json
  - skills/user/etkm-cheat-sheet/output/04_[book_id]_cheat_sheet.html (optional — generated)
Commit message: "Add [Book Title] cheat sheet — Asset 04"
If Chrome is not connected: Claude notes it and gives Nathan the two files to push manually.
Never blocks the rest of the pipeline on this step.

### Step 5 — REPORT
One clean summary. Example:
  "Done. Gift of Fear cheat sheet built, QC passed, pushed to GitHub.
   etkmstudent.com upload: output/04_gift_of_fear_cheat_sheet.html"

That's it. No step-by-step recap. No "here's what I did." Just the result.

---

## System Overview

The cheat sheet system is data-driven. Content and presentation are separated.

```
data/[book_id].json          ← All content lives here. One file per book.
template/cheat_sheet.html    ← One template. Never edit per-book.
build/build.py               ← Reads JSON, renders template, outputs HTML.
output/04_[book_id]_cheat_sheet.html  ← Final deliverable.
```

---

## JSON Data Structure — Quick Reference

Full schema with all rules in `references/schema.md`. Summary:

```json
{
  "meta":        { book identity — title, author, year, IDs },
  "journey":     { arc positioning — belt level, PEACE pillars, identity shift },
  "pillars":     [ 2–4 ETKM pillars this book supports ],
  "principles":  [ 8–12 numbered rules from the book ],
  "action_plan": { this_week, this_month, permanent },
  "media":       { video_intro, audio_summary, diagram, header_image — all optional },
  "connections": { next_recommended, thematic_cluster, curriculum_sequence }
}
```

---

## Media Slots

All four slots built in. Set `"enabled": true` and add URL. No other changes needed.

| Slot | Position | Powers |
|---|---|---|
| `media.header_image` | Below title, above Section 1 | Any image URL |
| `media.video_intro` | Below header, above Section 1 | HeyGen / YouTube |
| `media.diagram` | Between Section 2 and Section 3 | SVG / Canvas |
| `media.audio_summary` | Above footer | ElevenLabs |

---

## Design Invariants — Non-Negotiable

| Element | Rule |
|---|---|
| Background | Black (#000000) — all sections |
| Colors | Black / White / Red / Gray / LGray only |
| Red usage | Series top bar + principle numbers only |
| Sections | Exactly 3. No 4th section. |
| Pillar count | 2–4 |
| Principle count | 8–12 |
| Action tiers | This Week / This Month / Permanent |
| Eyebrow | "ETKM Cheat Sheet / Asset 04" — no book count |
| Print | @media print auto-inverts to white |

---

## Content Rules — Quick Reference

**Pillars:** One sentence. Why does THIS book matter to this pillar?
**Principles:** Rules not summaries. Verb-first or declarative. No hedging.
**Action items:** Specific behaviors. Passes test: "Can a person DO this today?"
**Identity shift:** From → To. One sentence. The transformation this book produces.

---

## Current Library

| book_id | Title | Author | Status |
|---|---|---|---|
| gift_of_fear | The Gift of Fear | Gavin de Becker | ✅ v2.1 |
| on_combat | On Combat | Lt. Col. Dave Grossman | ✅ v2.1 |
| left_of_bang | Left of Bang | Van Horne & Riley | Queued |
| survivors_club | The Survivors Club | Ben Sherwood | Queued |
| the_unthinkable | The Unthinkable | Amanda Ripley | Queued |
| deep_survival | Deep Survival | Laurence Gonzales | Queued |
| boyd | Boyd | Robert Coram | Queued |

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-03-14 | Initial canonical format |
| 2.0 | 2026-03-15 | Data-driven architecture. JSON + Jinja2. Media slots. Journey block. |
| 2.1 | 2026-03-15 | Full pipeline automation. Claude runs all steps. No manual commands. |

---
*Maintained by: Nathan Lundstrom / East Texas Krav Maga*
