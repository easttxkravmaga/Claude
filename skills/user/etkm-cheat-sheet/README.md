# ETKM Cheat Sheet System
**Asset 04 — Book Intelligence Series | East Texas Krav Maga**
**v2.0 — Data-Driven Architecture**

---

## What This Is

A data-driven build system for the ETKM Asset 04 Cheat Sheet — the permanent
student-facing HTML reference page produced for every book in the ETKM
Book Intelligence Series.

Content and presentation are fully separated. Every book is a JSON data file.
One HTML template generates every cheat sheet. One build script runs the whole library.

---

## Quick Start

```bash
# Install dependency
pip install jinja2

# Build one book
python build/build.py gift_of_fear

# Build all books
python build/build.py --all --verbose
```

Output lands in `output/`.

---

## Adding a New Book

1. Complete the ETKM 7-layer book extraction
2. Create `data/[book_id].json` using the schema in `references/schema.md`
3. Run `python build/build.py [book_id] --verbose`
4. Review the output HTML
5. Upload to etkmstudent.com

That's it. The template never changes. Only data files change.

---

## Repository Structure

```
etkm-cheat-sheet/
├── SKILL.md                         ← Claude's operating instructions
├── README.md                        ← This file
├── data/
│   ├── gift_of_fear.json            ← Book data files (one per book)
│   ├── on_combat.json
│   └── [book_id].json               ← Add new books here
├── template/
│   └── cheat_sheet.html             ← Jinja2 template — one file, forever
├── build/
│   └── build.py                     ← Build script
├── output/
│   └── 04_[book_id]_cheat_sheet.html  ← Generated files (git-ignored)
└── references/
    ├── schema.md                    ← Full JSON schema with rules
    └── design-decisions.md          ← Why every design decision was made
```

---

## The Three-Section Format

Every cheat sheet has exactly three sections:

| # | Section | Content | Count |
|---|---|---|---|
| 1 | ETKM Pillars | Which pillars this book supports, and why | 2–4 |
| 2 | Principles | Numbered actionable rules from the book | 8–12 |
| 3 | Action Plan | This Week / This Month / Permanent | 3 tiers |

No 4th section. No exceptions.

---

## The Journey Block

Every JSON file includes a `journey` object that positions the book in the
student transformation arc:

```json
"journey": {
  "belt_level": ["Yellow", "Orange"],
  "peace_pillars": ["Aware", "Prepared"],
  "arc_position": "foundation",
  "unlocks": "The ability to name what you already felt but couldn't articulate.",
  "identity_shift": "From person who overrides gut signals — to person who treats fear as information."
}
```

This powers the library page, curriculum integration, and the AI layer as they come online.

---

## Media Slots

Four optional media slots are built into the template. They render when enabled.

| Slot | Position | Powers | Status |
|---|---|---|---|
| `header_image` | Below title | Cinematic image | Ready — awaiting assets |
| `video_intro` | Below header | HeyGen / YouTube | Ready — awaiting HeyGen integration |
| `diagram` | Between Section 2 & 3 | SVG / Canvas | Ready — awaiting diagrams |
| `audio_summary` | Above footer | ElevenLabs | Ready — awaiting ElevenLabs integration |

---

## Brand Standards

| Element | Value |
|---|---|
| Background | #000000 (all sections) |
| Text primary | #ffffff |
| Red accent | #ff0000 (series bar + principle numbers only) |
| Gray | #575757 |
| Light gray | #bbbbbb |
| Font: headers | Barlow Condensed 700/900 |
| Font: body | Inter 400/600 |
| Print | @media print — auto-inverts to white background |

---

## Current Library

| book_id | Title | Author | Built |
|---|---|---|---|
| `gift_of_fear` | The Gift of Fear | Gavin de Becker | ✅ |
| `on_combat` | On Combat | Lt. Col. Dave Grossman | ✅ |
| `left_of_bang` | Left of Bang | Van Horne & Riley | Queued |
| `survivors_club` | The Survivors Club | Ben Sherwood | Queued |
| `the_unthinkable` | The Unthinkable | Amanda Ripley | Queued |
| `deep_survival` | Deep Survival | Laurence Gonzales | Queued |
| `boyd` | Boyd | Robert Coram | Queued |

---

## Connected Skills

| Skill | Role |
|---|---|
| `etkm-book-intelligence` | Source data — provides extraction for the JSON |
| `etkm-brand-kit` | Visual standards — authoritative for all brand decisions |
| `etkm-deliverable-qc` | QC gate — every file passes before delivery |

---

## Version History

| Version | Date | Notes |
|---|---|---|
| 1.0 | 2026-03-14 | Initial canonical format |
| 2.0 | 2026-03-15 | Data-driven architecture. JSON + Jinja2. Media slots. Journey block. Print stylesheet. |

---

*East Texas Krav Maga · etxkravmaga.com · Nathan Lundstrom*
