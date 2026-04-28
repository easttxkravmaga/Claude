---
name: etkm-carousel-system
version: 1.1
updated: 2026-04-27
description: >
  Production ruleset for building ETKM Instagram carousels. Carries slide type
  selection logic, key rules per type A-Z, design tokens, responsive headline
  sizing, StoryBrand compliance, and dual-mode QC gates (Gate 1: design
  compliance, Gate 2: messaging compliance). Load this skill at the start of
  every carousel build session. References ETKM Carousel System Notion page
  (34e924c8) for full visual specs — this skill carries execution rules only.
  Depends on etkm-brand-foundation and etkm-cta-architecture. Load
  etkm-audience-intelligence on-demand when building segment-specific carousels.
  V1.1: Added Type Z Brand Close back cover spec and static/dynamic layer rule.
triggers:
  - "build a carousel"
  - "carousel slide"
  - "carousel system"
  - "krav breakdown"
  - "slide type"
  - "instagram carousel"
  - "carousel for ETKM"
  - "build slides"
  - "carousel arc"
  - "save magnet"
  - "carousel QC"
  - "back cover"
  - "brand close"
depends_on:
  - etkm-brand-foundation
  - etkm-cta-architecture
loads_on_demand:
  - etkm-audience-intelligence
---

# ETKM Carousel System

**Version:** 1.1
**Last Updated:** 2026-04-27
**Changes from V1.0:** Added Type Z Brand Close spec (Section 5 and Section 13). Updated standard carousel sequence to 11 positions. Added static/dynamic layer rule for back cover production.
**Notion Reference:** ETKM Carousel System — Design & Messaging Standards (page 34e924c8)
**Library Reference:** ETKM Carousel Slide Type Library v3 (25 types A-Y) + Type Z Brand Close

This skill governs execution. Full visual specs, pixel values, and layout documentation
live in the Notion page and HTML library. This skill answers three operational questions:
Which type do I select? What are the non-negotiable rules? Did the output pass the gate?

---

## Section 1 — Design Token System (Locked)

Five tokens. Two fonts. One canvas. No exceptions.

| Token | Value | Role |
|---|---|---|
| Structural black | #000000 | All backgrounds |
| Primary white | #FFFFFF | Headlines, body copy |
| Signal red | #CC0000 | Accent, badge, CTA button, red bar |
| Mid gray | #575757 | Eyebrows, swipe cue, dividers |
| Light gray | #BBBBBB | Counters, attribution, ghost numerals |
| Headline font | Montserrat 900 | ALL CAPS, all headlines |
| Body font | Inter 400/600 | Sub-lines, body, spec text |
| Canvas | 1080x1350px | 4:5 portrait, sRGB, JPG 90% |

Hard rules:
- #CC0000 appears maximum three places per slide: red bar (always), series badge bg (always), one optional H1 accent line
- #BBBBBB and #575757 never appear on the same text element at the same weight
- #FF0000 is permanently retired — never use
- Gradients, pastels, and trend palettes are prohibited

---

## Section 2 — Structural Elements (Fixed Layer)

These six elements appear on every slide at fixed positions. They never move, scale, or change color.

| Element | Position | Size | Color | Override |
|---|---|---|---|---|
| Red bar | Left edge, full height | 25px wide | #CC0000 | None — never removed |
| Series badge | Top-left X:100px Y:60px | Montserrat 900 22px | #FFF on #CC0000 bg | Content changes per series only |
| Slide counter | Top-right X:1020px Y:68px | Inter 400 22px | #BBBBBB | Numbers change only |
| ETKM logo | Bottom-left X:100px Y:1255px | Montserrat 900 28px | #CC0000 | CTA slide: 48px centered. Back cover: omitted (logo image used instead) |
| Swipe cue | Bottom-right X:1020px Y:1258px | Inter 400 18px | #575757 | CTA slide: ETXKRAVMAGA.COM. Back cover: omitted |
| Bottom rule | Y:1230px X:100px-980px | 1px | rgba(255,255,255,0.10) | CTA slide: 0.20 opacity. Back cover: present in static layer |

---

## Section 3 — Photo & Background Treatment (Locked)

Every slide (01 through N-2): Two-layer system applied identically.

Layer A — Image processing:
- Color mode: grayscale 100%
- Brightness: 40%
- Contrast: +20%
- Crop: 4:5 portrait, action zone centered

Layer B — Normalization overlay:
- Type: solid black rectangle, full bleed
- Opacity: 45%
- CTA slide override: 60% opacity only

Series photo rule: One photo per carousel. Same photo, identical treatment, all body slides.
CTA close (Type G): no photo — #000 solid field.
Back cover (Type Z): no photo — #000 solid field. Static core PNG handles the full layout.

Graphic-only slides (no photo available): #000 solid background. All structural elements unchanged.

---

## Section 4 — Typography Hierarchy

| Role | Font | Size (canvas) | Case | Color | Usage |
|---|---|---|---|---|---|
| H1 Headline | Montserrat 900 | 108px | ALL CAPS | #FFFFFF | Cover headlines |
| H1 Responsive | Montserrat 900 | See below | ALL CAPS | #FFFFFF | Body slide headlines |
| H2 Sub-headline | Inter 600 | 36px | Sentence | rgba(255,255,255,0.60) | Supporting context |
| Body copy | Inter 400 | 30px | Sentence | rgba(255,255,255,0.75) | Content slides only |
| Micro label | Montserrat 900 | 22px | ALL CAPS | #BBBBBB | Eyebrows, counters, step labels |

Responsive headline sizing (body slides):
- 1-2 words per line: 52px tracking -1.5px
- 3-4 words per line: 46px tracking -1px
- 5+ words per line: 36px tracking -0.5px
- max-width: 340px on all body slide headlines — hard limit, no exceptions

H1 red accent rule: Maximum one line per slide rendered in #CC0000. One line only.

---

## Section 5 — Slide Type Selection Logic

### The 11-Position Standard Sequence (Full Carousel with Back Cover)

| Position | Type | Job | Non-negotiable rule |
|---|---|---|---|
| Slide 01 | A Cover Hook | Stop the scroll | External problem only, no solutions, sub-line max 12 words |
| Slide 02 | B Re-Hook | Second-chance hook | Inverts cover register, works cold, internal problem |
| Slide 03 | C Stakes Bridge | Authority establishment | Philosophical claim, bridge line required, never bashes alternatives |
| Slides 04-N | D Principle Body | Value delivery | One idea per slide, max 40 words, bridge line on all but final |
| Midpoint slide 5-7 | E H I or O (one only) | Pattern interrupt | Maximum ONE per carousel, breaks visual rhythm |
| Slide N-2 | F Save Magnet | Algorithm play | Reference card format, Screenshot this, standalone test required |
| Slide N-1 | G CTA Close | Conversion | Four StoryBrand elements, #CC0000 button, prohibited language check |
| Slide N | Z Brand Close | Brand impression | Static core PNG + dynamic badge and counter only |

### Content Type to Slide Type Matrix

| Carousel type | Slide 03 | Body slides | Pattern interrupt |
|---|---|---|---|
| Principles | C | D (one per principle) | E (quote card) |
| Top 5 / List | C | K (numbered list) | O (myth buster) |
| Statistics | C | H (stat card) + D | V (did you know) |
| Scenario | C | J (scenario frame) + D | W (decision tree) |
| How-to / Protocol | C | M (3-step process) + D | I (wrong/right) |
| Framework | C | Q (framework) + D | E or N (quote) |
| Education / Deep | C | D + L (book ref) + N (quote) | P (before/after) |

### Additional Type Insertion Rules

| Type | When to insert | Position |
|---|---|---|
| L Book Reference | When a principle can be sourced to a named book | Any body position |
| M Three-Step Process | What to do when X scenarios | Any body position |
| N Extended Quote | External authority reinforces the point | After Type D body slides |
| O Myth Buster | A held belief needs correcting | Pattern interrupt position |
| P Before/After | Transformation arc needs making visible | Before CTA slide |
| Q Framework | Teaching a named mental model | Body position after context |
| R Timeline | Curriculum or progression content | Body position |
| S Comparison Table | Two approaches across multiple dimensions | Body position |
| T Checklist | Actionable audit the viewer applies now | Body position |
| U Misconception Chain | Compounding false beliefs to bad outcome | Pattern interrupt |
| V Did You Know | Three rapid-fire surprising facts | Body or pattern interrupt |
| W Decision Tree | Conditional protocol: if X do Y | Body position |
| X Authority Credentials | Guide authority needed | Slide 5 or later — never 1-3 |
| Y Social Proof | Student proof before conversion | Before CTA slide |
| Z Brand Close | Every carousel — always last | Final slide N — always |

---

## Section 6 — StoryBrand Compliance Rules

The hero rule: The student is always the hero. ETKM is always the guide.
- Every headline must be about the student's reality — not ETKM's credentials
- ETKM is never the subject of a body slide sentence
- Authority is established by depth of knowledge, not by self-promotion

The villain rule: The threat, the false belief, or the missed skill is the villain.
- Never make another school, approach, or instructor the villain
- Never shame the audience for not knowing something

The guide formula: Empathy first, authority second.
- Empathy = naming what the hero already feels
- Authority = delivering the plan with confidence, not credentials
- Never lead with ETKM's history or certifications

Bridge line rule: Every body slide (D-S) except the final principle slide ends with a bridge line.
- Bridge lines open a loop — they do not reveal the answer
- Format: italic, Inter 400, 10px, #575757

CTA four-element rule (Type G):
1. Transformation statement: Stop [X]. Start [Y]. — identity shift, not skill promise
2. Direct CTA: action verb + specific action + location (Attend a Free Trial Class — Tyler, TX)
3. Transitional CTA: DM keyword format (DM us PRINCIPLES for the free guide)
4. Stakes line (optional ~50%): acknowledgment that waiting has a cost

Prohibited CTA language: Learn More / Get Started / Click Here / Sign Up — never on any slide

---

## Section 7 — Arc Construction Protocol

Before building any carousel, the arc must be locked. Building before arc lock is prohibited.

Step 1 — Content type selection: Identify the carousel type from the matrix in Section 5. Name the content arc explicitly.

Step 2 — Principle sequence: Order principles by how they activate in a real encounter.
Physical logic: Awareness to Distance to Mobility to Angle to Improvise (Krav)
De-escalation logic: Awareness to Verbal to Distance to Positioning to Physical

Step 3 — Pattern interrupt placement: Identify the midpoint slide (position 5-7). Select pattern interrupt type. Mark it in the arc before building.

Step 4 — Save magnet content: Draft the save magnet before building body slides. If it cannot be drafted, the arc is incomplete.

Step 5 — Nathan approval: Present the complete arc map before building. Do not build until arc is approved. Non-negotiable per Rule 1 of nate-collaboration-workflow.

---

## Section 8 — QC Gate 1 (Design Compliance — Claude Runs)

Environment Claude Code (Playwright — authoritative): Claude renders every slide as PNG. Visual inspection and overflow check. Values verified against rendered output, not source.

Environment Chat (Structured source audit): Claude reads HTML source. Checks each item against the code. Produces written QC report with explicit pass/fail.

The hard stop rule: No slide is presented to Nathan with a known Gate 1 failure. Rebuild before presenting. No exceptions.

Gate 1 Checklist — Binary pass/fail:
- Red bar present, left edge, 25px, #CC0000, full height
- Series badge present, top-left, correct series name, #CC0000 bg, #FFF text
- Slide counter present, top-right, 01 / 09 format, #BBBBBB, zero-padded
- All headline text within safe zone (100-980px horizontal, 80-1230px vertical)
- Photo treatment applied on body slides: grayscale, 40% brightness, +20% contrast, 45% overlay
- Headline does not overflow 340px max-width
- Maximum one #CC0000 line in headline per slide
- Body copy absent from Type A and Type G slides
- ETKM logo present, bottom-left, #CC0000, correct size
- Swipe cue present on all slides except CTA and back cover, bottom-right, #575757
- Bottom rule present, correct opacity per slide type
- No Tier 1 design token modified
- Word count within limit for slide type
- Type G: #CC0000 button present, #000 background, no photo layer
- Type Z: static core PNG present, only badge and counter in dynamic layer

Gate 1 report format: "Gate 1 QC: [X]/15 items pass. [List any failures with slide number and item.]"

---

## Section 9 — QC Gate 2 (Messaging Compliance — Nathan Approves)

Claude prepares this report. Nathan reviews and approves before the carousel ships.

Gate 2 Checklist:

Cover (Type A): External problem addressed, question or declarative tension, student is implied subject.

Re-hook (Type B): Works standalone cold, inverts cover register, names internal problem.

Stakes (Type C): Guide authority without implying others are inferior, specific philosophical claim, bridge line opens loop.

Body slides (D-S): Student is hero, one idea per slide, bridge lines present and open loops, red accent on most resonant phrase, word count within limit.

Save magnet (Type F): Reference tool not recap, passes 30-day test, save cue explicit.

CTA (Type G): All four StoryBrand elements present, transformation uses identity language, direct CTA has verb plus action plus Tyler TX, prohibited language absent, DM keyword present.

Full arc: StoryBrand hero's journey complete, slide 2 works cold, no contradictions, consistent voice.

Back cover (Type Z): Static core present, only badge and counter changed from template, badge matches series name used throughout carousel.

Gate 2 report format: "Gate 2 QC prepared for Nathan review. [X]/[total] items pass. Items requiring Nathan judgment: [list]. Ready to ship pending Nathan approval."

---

## Section 10 — Canva Production Spec (Quick Reference)

| Element | Canva setting |
|---|---|
| Canvas size | 1080x1350px custom |
| Photo layer | Grayscale filter: 100%, Brightness: -60%, Contrast: +20% |
| Black overlay | Rectangle, full bleed, black fill, 45% transparency |
| Red bar | Rectangle, 25px wide, full height, locked layer |
| Series badge | Text box, Montserrat Bold 900, 22px, #FFF, #CC0000 bg rectangle |
| Slide counter | Text box, Inter Regular, 22px, #BBBBBB |
| ETKM logo text | Text box, Montserrat Bold 900, 28px, #CC0000 |
| Swipe cue | Text box, Inter Regular, 18px, #575757 |
| Bottom rule | Line, 1px, rgba(255,255,255,0.10) |
| Export | JPG, 90% quality, download all slides as ZIP |
| Back cover | Use etkm_back_cover_TEMPLATE.html — change badge and counter only |

Layer order (bottom to top): Photo, Overlay, Red bar, Content elements

---

## Section 11 — Notion Reference Map

| Need | Notion page / database |
|---|---|
| Full visual specs + pixel values | ETKM Carousel System (34e924c8) |
| Content arc library | ETKM Carousel System Section 9 |
| Production status tracker | ETKM Carousel System Section 12 |
| Slide type library (visual) | ETKM Carousel Slide Type Library v3 (HTML file) |
| CTA language bank | etkm-cta-architecture skill |
| Audience segment data | etkm-audience-intelligence skill |
| Brand voice rules | etkm-brand-foundation skill |

---

## Section 12 — Session Opening Protocol

At the start of every carousel session:
1. Load this skill (etkm-carousel-system)
2. Load etkm-brand-foundation
3. Load etkm-cta-architecture
4. If segment-specific carousel: load etkm-audience-intelligence
5. Confirm the content arc with Nathan before building
6. Pull the current production status from Notion (34e924c8 Section 12)
7. State: Ready to build. Arc is [confirmed / needs confirmation]. Last completed slide: [X].

---

## Section 13 — Type Z Brand Close (Back Cover) Spec

Type Z is the final slide of every carousel. Always. No exceptions.

### Architecture: Static Core + Dynamic Layer

Static core (never edit):
- Rendered PNG: etkm_back_cover_TEMPLATE.html static layer
- Contains: black background (#000000), red left bar, ETKM circle logo (148px), etxkravmaga.com website, Tyler Texas Est. 2006 tagline, red rule, FB/IG/LI/YT social icons in #CC0000, bottom rule, ETKM wordmark bottom-left, Tyler TX bottom-right
- This PNG is pre-rendered and embedded. It never changes.

Dynamic layer (edit per carousel — two elements only):
1. Series badge (top-left): Change text to match the series name used throughout the carousel
2. Slide counter (top-right): Change to "XX / XX" matching the carousel total

Production rule: Open etkm_back_cover_TEMPLATE.html. Change the text inside .series-badge and .slide-counter. Export. Done. Nothing else is touched.

### Design spec

| Element | Value |
|---|---|
| Background | #000000 solid — no photo, no overlay |
| Red bar | Present — left edge, 5px, #CC0000, full height |
| Logo | ETKM circle logo, 148x148px, centered |
| Website | ETX in #CC0000, KRAVMAGA.COM in #FFFFFF, Montserrat 900, 15px |
| Tagline | Tyler, Texas · Est. 2006, #575757, Inter 400, 9px |
| Red rule | 48px wide, 2px tall, #CC0000, centered |
| Social icons | FB, IG, LI, YT — #CC0000 fill SVG, 24px, 18px gap |
| Bottom rule | rgba(255,255,255,0.08) |
| Logo wordmark | ETKM, bottom-left, #CC0000, Montserrat 900, 10px |
| Location | Tyler, TX, bottom-right, #575757, Inter 400, 8px |

### Logo rendering note

The ETKM circle logo PNG has a black (#000000) background. On the pure black slide field, the logo background is invisible — white ring, red text, and white symbol render cleanly with no transparency processing required. Do not convert the logo to RGBA. Do not add mix-blend-mode. Place it as-is. The black-on-black merge is the intended behavior.

### QC Gate 1 addition for Type Z

- Static core PNG present and rendering correctly
- Only .series-badge and .slide-counter changed from template
- Badge text matches series name used on all other slides in the carousel
- Counter format correct: "XX / XX" zero-padded, spaces around slash
- No other element in the static layer has been modified

---

## Non-Negotiables

- Never build a carousel without a locked arc
- Never present a slide with a known Gate 1 failure
- Never use prohibited CTA language
- Never make ETKM the hero
- Never modify a Tier 1 design token
- Never use #FF0000 — ever
- Never present options when direction has already been given
- Always run Gate 1 before Gate 2
- Always run Gate 2 before handoff to Nathan
- Type Z is always the final slide — never omit the back cover