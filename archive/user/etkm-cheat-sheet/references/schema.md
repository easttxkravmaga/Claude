# ETKM Cheat Sheet — JSON Schema v1.0
## The data contract every book file must follow

Every book in the ETKM library is a JSON file in the `data/` directory.
The build script reads the JSON and generates the HTML. The template never
changes. Only data files change when adding books.

---

## Top-Level Structure

```json
{
  "meta": { ... },
  "journey": { ... },
  "pillars": [ ... ],
  "principles": [ ... ],
  "action_plan": { ... },
  "media": { ... },
  "connections": { ... }
}
```

---

## `meta` — Book identity

```json
"meta": {
  "asset_id": "04",
  "book_id": "gift_of_fear",
  "title": "The Gift of Fear",
  "title_line_1": "The Gift",
  "title_line_2": "of Fear",
  "subtitle": "",
  "author": "Gavin de Becker",
  "author_last": "de Becker",
  "year": 1997,
  "series_label": "ETKM Book Intelligence Series"
}
```

| Field | Required | Notes |
|---|---|---|
| `asset_id` | Yes | Always "04" for cheat sheets |
| `book_id` | Yes | Slug used for filenames and URLs. Lowercase, underscores. |
| `title` | Yes | Full title for `<title>` tag and footer |
| `title_line_1` | Yes | First line of giant display title |
| `title_line_2` | Yes | Second line — break for typographic impact |
| `subtitle` | No | Long book subtitle. Empty string if none. |
| `author` | Yes | Full author credit line (may include "with [co-author]") |
| `author_last` | Yes | Last name(s) only for compact footer display |
| `year` | Yes | Publication year (integer) |
| `series_label` | Yes | Always "ETKM Book Intelligence Series" |

---

## `journey` — Student arc positioning

This is the identity layer. It tells the system where this book lives in the
student transformation arc. Used now for metadata. Used later for library page,
curriculum integration, and AI layer context.

```json
"journey": {
  "belt_level": ["Yellow", "Orange"],
  "peace_pillars": ["Aware", "Prepared"],
  "arc_position": "foundation",
  "unlocks": "The ability to name what you already felt but couldn't articulate.",
  "pairs_with": ["left_of_bang", "on_combat"],
  "read_after": [],
  "identity_shift": "From person who ignores gut signals to person who treats fear as information."
}
```

| Field | Required | Notes |
|---|---|---|
| `belt_level` | Yes | Array. Options: Yellow / Orange / Green / Blue / Brown / Black / All |
| `peace_pillars` | Yes | Array. Options: Prepared / Empowered / Aware / Capable / Engaged |
| `arc_position` | Yes | Options: foundation / intermediate / advanced / all-levels |
| `unlocks` | Yes | One sentence. What becomes possible for a student after this book. |
| `pairs_with` | No | Array of book_id values. Books that complement this one. |
| `read_after` | No | Array of book_id values. Books that should come first. |
| `identity_shift` | Yes | One sentence. From → To. The identity transformation this book produces. |

---

## `pillars` — ETKM pillars this book supports

Array of 2–4 objects.

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | Must be from official ETKM pillar list |
| `why` | Yes | One sentence. Why does THIS book matter to this pillar? |

**Official ETKM pillar names:**
Mindset · Awareness · Tactics · Skills · Physiology · Identity · Resilience · Recovery · Prepared

**Rules:** Minimum 2, maximum 4.

---

## `principles` — Numbered rules from the book

Array of 8–12 objects.

| Field | Required | Notes |
|---|---|---|
| `number` | Yes | Zero-padded string: "01", "02"... "12" |
| `text` | Yes | The principle. Starts with verb or declarative. No hedging. |

**Rules:** Minimum 8, maximum 12. Every principle must be a rule, not a summary.

---

## `action_plan` — Tiered field assignments

Exactly 3 tiers. Fixed keys: `this_week`, `this_month`, `permanent`.

| Tier | Min items | Max items | Character |
|---|---|---|---|
| `this_week` | 2 | 3 | Immediate. Doable today. Specific. |
| `this_month` | 3 | 4 | Habit or system. Builds over 30 days. |
| `permanent` | 3 | 4 | Identity-level. Present tense. |

---

## `media` — Future media slots (build now, populate later)

All four slots are optional. Set `enabled: true` and add a URL to activate.

| Slot | Renders where | Powered by |
|---|---|---|
| `video_intro` | Below header, above Section 1 | HeyGen / YouTube / Vimeo |
| `audio_summary` | Above footer | ElevenLabs / any audio URL |
| `diagram` | Between Section 2 and Section 3 | SVG / Canvas / img |
| `header_image` | Below title block | Any image URL |

---

## `connections` — Cross-book relationships

| Field | Notes |
|---|---|
| `next_recommended` | book_id of the natural next read |
| `thematic_cluster` | Options: threat_recognition / stress_physiology / decision_making / survival_mindset / tactics / identity |
| `curriculum_sequence` | Integer. Suggested reading order within a cluster. |

---

## File naming

```
data/[book_id].json
```

The `book_id` in the JSON must exactly match the filename (without `.json`).
