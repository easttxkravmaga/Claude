---
name: etkm-cheat-sheet
version: 2.0
created: 2026-03-14
updated: 2026-03-15
description: >
  Canonical format and build system for the ETKM Asset 04 Cheat Sheet — the permanent
  student portal reference HTML page produced for every book in the ETKM Book Intelligence
  Series. Load this skill whenever building, repairing, auditing, or adding a new book to
  the cheat sheet system. Trigger phrases: "build the cheat sheet", "Asset 04", "book cheat
  sheet", "ETKM cheat sheet", "cheat sheet for [book title]", "add a new book", "make the
  HTML for the book", "update the book data", or any session where a cheat sheet HTML file
  is being produced or revised. Do not build cheat sheets from memory or prior examples —
  the system is now data-driven. Add a JSON file, run the build script, done.
dependencies:
  - etkm-brand-kit (visual standards — load for any color/type questions)
  - etkm-book-intelligence (source data — extraction must be complete before building)
  - etkm-deliverable-qc (QC protocol — run on every file before delivery)
---

# ETKM Cheat Sheet System — v2.0
## Asset 04 | Book Intelligence Series | Data-Driven Architecture

---

## System Overview

The cheat sheet system is now **data-driven**. Content and presentation are separated.

```
data/[book_id].json          ← All content lives here. One file per book.
template/cheat_sheet.html    ← One template. Never edit per-book.
build/build.py               ← Reads JSON, renders template, outputs HTML.
output/04_[book_id]_cheat_sheet.html  ← Final deliverable.
```

**To add a new book:** Create a JSON file. Run the build script. Done.
**To change the design:** Edit the template once. Rebuild all books. Every file updates.
**To fix a content error:** Edit the JSON. Rebuild that book. One file, clean.

---

## Adding a New Book — The Workflow

```
Step 1  Complete the 7-layer book extraction (etkm-book-intelligence skill)
Step 2  Create data/[book_id].json using the schema in references/schema.md
Step 3  Run: python build/build.py [book_id] --verbose
Step 4  Review output/04_[book_id]_cheat_sheet.html
Step 5  Run etkm-deliverable-qc on the output file
Step 6  Copy to Google Drive: Book Intelligence/[Book Title]/
Step 7  Upload to etkmstudent.com LearnWorlds module
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

**The `journey` block is required even if the media slots are empty.**
It carries the identity transformation framing that will power the library page,
AI layer, and curriculum integration as they come online.

---

## Build Script — Commands

```bash
# Build one book
python build/build.py gift_of_fear

# Build one book — show validation detail
python build/build.py gift_of_fear --verbose

# Build ALL books in data/
python build/build.py --all

# Build all — verbose output
python build/build.py --all --verbose

# Custom paths
python build/build.py gift_of_fear \
  --data data/ \
  --template template/ \
  --output output/
```

**Requirements:** `pip install jinja2`

The script validates every JSON file before rendering. Validation errors are
reported with specific field paths — the build fails on any error.

---

## Media Slots

All four media slots are built into the template. They render when `enabled: true`
in the JSON. They produce no HTML when `enabled: false`.

| Slot | JSON key | Renders where | Powered by |
|---|---|---|---|
| Header image | `media.header_image` | Below header title, above Section 1 | Any URL |
| Video intro | `media.video_intro` | Below header, above Section 1 | HeyGen / YouTube / Vimeo |
| Diagram | `media.diagram` | Between Section 2 and Section 3 | SVG / Canvas / img |
| Audio | `media.audio_summary` | Above footer | ElevenLabs / any audio URL |

**To enable a slot:** Set `"enabled": true` and populate `"url"` in the JSON.
No template changes required.

---

## Design Invariants — Non-Negotiable

| Element | Rule |
|---|---|
| Background | Black (#000000) — all sections |
| Colors | Black / White / Red (#FF0000) / Gray (#575757) / LGray (#BBBBBB) only |
| Red usage | Series top bar + principle numbers only |
| Fonts | Barlow Condensed + Inter via Google Fonts |
| Sections | Exactly 3. No 4th section under any circumstances. |
| Pillar count | 2–4 |
| Principle count | 8–12 |
| Action tiers | Exactly 3: This Week / This Month / Permanent |
| Eyebrow | "ETKM Cheat Sheet / Asset 04" — no book count, no "X of Y" |
| Print | @media print inverts to white background automatically |

---

## Content Rules — Quick Reference

**Pillars:** One sentence each. Answers "Why does THIS book matter to this pillar?"
Not a definition of the pillar itself. Verb-first or declarative.

**Principles:** Rules, not summaries. Start with verb or declarative.
No hedging. No "the book discusses..." — the principle IS the rule.

**Action items:** Specific behaviors, not concepts. Every item passes:
"Can a specific person DO this specific thing today?" If yes: include. If it's
an idea or concept: cut it.

**Identity shift (journey block):** From → To. One sentence. The transformation
this book produces in a committed student. This is the north star of the whole asset.

---

## Current Library

| book_id | Title | Author | Status |
|---|---|---|---|
| gift_of_fear | The Gift of Fear | Gavin de Becker | ✅ v2.0 |
| on_combat | On Combat | Lt. Col. Dave Grossman | ✅ v2.0 |
| left_of_bang | Left of Bang | Van Horne & Riley | Queued |
| survivors_club | The Survivors Club | Ben Sherwood | Queued |
| the_unthinkable | The Unthinkable | Amanda Ripley | Queued |
| deep_survival | Deep Survival | Laurence Gonzales | Queued |
| boyd | Boyd | Robert Coram | Queued |

---

## File Structure

```
etkm-cheat-sheet/
├── SKILL.md                         ← This file
├── README.md                        ← GitHub documentation
├── data/
│   ├── gift_of_fear.json            ← Book data files
│   ├── on_combat.json
│   └── [book_id].json               ← Add new books here
├── template/
│   └── cheat_sheet.html             ← Jinja2 template — one file, forever
├── build/
│   └── build.py                     ← Build script
├── output/
│   ├── 04_gift_of_fear_cheat_sheet.html
│   └── 04_on_combat_cheat_sheet.html
└── references/
    ├── schema.md                    ← Full JSON schema documentation
    └── design-decisions.md          ← Why every design decision was made
```

---

## Relationship to Other Skills

| Skill | When to load |
|---|---|
| `etkm-book-intelligence` | Always first — provides the extraction data for the JSON |
| `etkm-brand-kit` | When in doubt about color, font, or layout decisions |
| `etkm-deliverable-qc` | After build — run before any file ships |

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-03-14 | Initial canonical format |
| 2.0 | 2026-03-15 | Data-driven architecture. JSON + Jinja2 build system. Media slots. Journey block. Print stylesheet. Removed "X of Y" count from eyebrow. |

---
*Maintained by: Nathan Lundstrom / East Texas Krav Maga*
