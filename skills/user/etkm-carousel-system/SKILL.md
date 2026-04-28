---
name: etkm-carousel-system
version: 1.2
updated: 2026-04-27
description: >
  Production ruleset for building ETKM Instagram carousels. Carries slide type
  selection logic, key rules per type A-Z, design tokens, responsive headline
  sizing, StoryBrand compliance, and dual-mode QC gates. V1.2: Type G (separate
  CTA slide) retired. Type Z now serves as the single final slide carrying both
  the StoryBrand four-element CTA and the brand close. Standard carousel is now
  10 positions. References ETKM Carousel System Notion page (34e924c8).
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
  - "final slide"
  - "CTA slide"
depends_on:
  - etkm-brand-foundation
  - etkm-cta-architecture
loads_on_demand:
  - etkm-audience-intelligence
---

# ETKM Carousel System

**Version:** 1.2
**Last Updated:** 2026-04-27
**Changes from V1.1:** Type G (separate CTA close) retired. Type Z now unified — carries StoryBrand four-element CTA + brand close on one black slide. Standard carousel sequence is 10 positions. Production template: etkm_final_slide_TEMPLATE.html. Only badge and counter change per carousel.
**Notion Reference:** ETKM Carousel System (page 34e924c8)
**Library Reference:** ETKM Carousel Slide Type Library v3 (25 types A-Y) + Type Z

---

## Section 1 — Design Token System (Locked)

| Token | Value | Role |
|---|---|---|
| Structural black | #000000 | All backgrounds |
| Primary white | #FFFFFF | Headlines, body copy |
| Signal red | #CC0000 | Accent, badge, CTA button, red bar |
| Mid gray | #575757 | Eyebrows, swipe cue, dividers |
| Light gray | #BBBBBB | Counters, attribution |
| Headline font | Montserrat 900 | ALL CAPS, all headlines |
| Body font | Inter 400/600 | Sub-lines, body, spec text |
| Canvas | 1080x1350px | 4:5 portrait, sRGB, JPG 90% |

Hard rules:
- #CC0000: red bar (always) + series badge bg (always) + one optional H1 accent line per body slide
- #FF0000 permanently retired
- Gradients, pastels, trend palettes prohibited

---

## Section 2 — Structural Elements (Fixed Layer)

Present on every slide at fixed positions. Never move, scale, or change color.

| Element | Position | Size | Color | Override |
|---|---|---|---|---|
| Red bar | Left edge, full height | 25px | #CC0000 | None — never removed |
| Series badge | Top-left X:100px Y:60px | Montserrat 900 22px | #FFF on #CC0000 | Content changes per series only |
| Slide counter | Top-right X:1020px Y:68px | Inter 400 22px | #BBBBBB | Numbers change only |
| ETKM logo text | Bottom-left X:100px Y:1255px | Montserrat 900 28px | #CC0000 | Type Z: in static core |
| Swipe cue | Bottom-right X:1020px Y:1258px | Inter 400 18px | #575757 | Type Z: omitted (no swipe on final slide) |
| Bottom rule | Y:1230px X:100px-980px | 1px | rgba(255,255,255,0.10) | Type Z: in static core |

---

## Section 3 — Photo & Background Treatment (Locked)

Body slides (01 through N-1): Two-layer system applied identically.
- Layer A: grayscale 100%, brightness 40%, contrast +20%, 4:5 portrait crop
- Layer B: solid black overlay, 45% opacity

Series photo rule: One photo per carousel. Same photo, same treatment, all body slides.
Type Z (final slide): #000000 solid — no photo, no overlay. Static core PNG handles all layout.

---

## Section 4 — Typography Hierarchy

| Role | Font | Canvas size | Color |
|---|---|---|---|
| H1 Cover | Montserrat 900 | 108px | #FFFFFF |
| H1 Body (responsive) | Montserrat 900 | See below | #FFFFFF |
| H2 Sub-headline | Inter 600 | 36px | rgba(255,255,255,0.60) |
| Body copy | Inter 400 | 30px | rgba(255,255,255,0.75) |
| Micro label | Montserrat 900 | 22px | #BBBBBB |

Responsive headline sizing (body slides):
- 1-2 words per line: 52px, -1.5px tracking
- 3-4 words per line: 46px, -1px tracking
- 5+ words per line: 36px, -0.5px tracking
- max-width: 340px — hard limit, no exceptions

Red accent rule: Maximum one line per slide in #CC0000.

---

## Section 5 — Slide Type Selection Logic

### Standard 10-Position Sequence

| Position | Type | Job | Key rule |
|---|---|---|---|
| Slide 01 | A Cover Hook | Stop the scroll | External problem, no solutions, sub-line max 12 words |
| Slide 02 | B Re-Hook | Second-chance hook | Inverts cover, works cold, internal problem |
| Slide 03 | C Stakes Bridge | Authority + philosophical problem | Bridge line required, never bashes alternatives |
| Slides 04-N | D Principle Body | Value delivery | One idea per slide, max 40 words, bridge line on all but final |
| Midpoint 5-7 | E/H/I/O/U/V (one only) | Pattern interrupt | Maximum ONE per carousel |
| Slide N-1 | F Save Magnet | Algorithm play | Reference card, "Screenshot this", standalone test required |
| Slide N | Z Final Slide | CTA + Brand close | Static core PNG — edit badge and counter only |

### Content Type Matrix

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

| Type | When | Position |
|---|---|---|
| L Book Reference | Principle sourced to a named book | Any body position |
| M Three-Step Process | What to do when X | Any body position |
| N Extended Quote | External authority reinforces point | After Type D |
| O Myth Buster | Held belief needs correcting | Pattern interrupt |
| P Before/After | Transformation arc needs visibility | Before final slide |
| Q Framework | Named mental model | Body after context |
| R Timeline | Curriculum or progression | Body position |
| S Comparison Table | Two approaches, multiple dimensions | Body position |
| T Checklist | Actionable audit | Body position |
| U Misconception Chain | Compounding false beliefs | Pattern interrupt |
| V Did You Know | Three rapid-fire facts | Body or pattern interrupt |
| W Decision Tree | If X do Y protocol | Body position |
| X Authority Credentials | Guide authority needed | Slide 5 or later |
| Y Social Proof | Student proof before conversion | Before final slide |

---

## Section 6 — StoryBrand Compliance Rules

Hero rule: Student is always hero. ETKM is always guide.
- Every headline is about the student's reality — not ETKM's credentials
- ETKM is never the subject of a body slide sentence

Villain rule: The threat, false belief, or missed skill is the villain.
- Never make another school or instructor the villain
- Never shame the audience

Guide formula: Empathy first, authority second.
- Never lead with ETKM's history or certifications

Bridge line rule: Every body slide (D-S) except the final principle slide ends with a bridge line.
- Opens a loop, never reveals the answer
- Format: italic, Inter 400, 10px, #575757

CTA rules (all governed by etkm-cta-architecture skill):
- Four-element structure: transformation → direct CTA → transitional CTA → stakes line
- Direct CTA: action verb + specific action + location (Tyler, TX)
- Prohibited: "Learn More" / "Get Started" / "Click Here" / "Sign Up"
- ETKM General primary set: "Stop hoping you could handle it. Start knowing." / "Attend a Free Trial Class" / "DM us CONFIDENT" / "Because waiting does not make the threat go away."

---

## Section 7 — Arc Construction Protocol

Arc must be locked before building. Building before arc lock is prohibited.

1. Content type: identify from matrix in Section 5
2. Principle sequence: order by physical activation in a real encounter
3. Pattern interrupt: identify midpoint position (5-7), select type, mark in arc
4. Save magnet: draft before building body slides — if it can't be drafted, arc is incomplete
5. Nathan approval: present complete arc map before building — explicit approval required

---

## Section 8 — QC Gate 1 (Design Compliance — Claude Runs)

Hard stop rule: No slide presented to Nathan with a known Gate 1 failure. Rebuild before presenting. No exceptions.

Claude Code environment: Playwright renders every slide as PNG. Pixel-level overflow check. Authoritative.
Chat environment: HTML source audit. Written QC report. Overflow estimated via font metrics.

Gate 1 Checklist — 15 items, binary pass/fail:
1. Red bar: left edge, 25px, #CC0000, full height
2. Series badge: top-left, correct name, #CC0000 bg, #FFF text
3. Slide counter: top-right, "01 / 09" format, #BBBBBB, zero-padded
4. Safe zone: all text 100-980px horizontal, 80-1230px vertical
5. Photo treatment (body slides): grayscale, 40% brightness, +20% contrast, 45% overlay
6. Headline overflow: no headline exceeds 340px max-width
7. Red accent limit: maximum one #CC0000 line per slide
8. Body copy restriction: no body copy on Type A (cover) or Type Z (final)
9. ETKM logo/wordmark: present, correct position, #CC0000
10. Swipe cue: present on all slides except final, bottom-right, #575757
11. Bottom rule: present, correct opacity
12. Tier 1 token integrity: no Tier 1 token modified
13. Word count: Type A sub-line max 12 words, Type D body max 40 words
14. Type Z: static core PNG rendering correctly, no photo layer
15. Type Z: only badge and counter changed from template, badge matches series name throughout

Gate 1 report: "Gate 1 QC: [X]/15 items pass. [Failures listed with slide number and item.]"

---

## Section 9 — QC Gate 2 (Messaging Compliance — Nathan Approves)

Claude prepares, Nathan approves. Nothing ships without Gate 2 sign-off.

Cover (A): External problem, question or declarative tension, student is implied subject.
Re-hook (B): Standalone cold, inverts cover register, names internal problem.
Stakes (C): Guide authority without implying others inferior, specific claim, bridge line opens loop.
Body (D-S): Student is hero, one idea per slide, bridge lines open loops, red accent on most resonant phrase.
Save magnet (F): Reference tool not recap, passes 30-day test, save cue explicit.
Final slide (Z): All four StoryBrand elements present, transformation uses identity language, direct CTA has verb + action + Tyler TX, prohibited language absent, DM keyword present, badge matches series name.
Full arc: StoryBrand hero's journey complete, slide 2 works cold, no contradictions, consistent voice.

Gate 2 report: "Gate 2 QC prepared for Nathan review. [X]/[total] items pass. Items requiring Nathan judgment: [list]. Ready to ship pending Nathan approval."

---

## Section 10 — Canva Production Spec

| Element | Canva setting |
|---|---|
| Canvas size | 1080x1350px custom |
| Photo layer | Grayscale 100%, Brightness -60%, Contrast +20% |
| Black overlay | Rectangle, full bleed, black, 45% transparency |
| Red bar | Rectangle, 25px, full height, locked layer |
| Series badge | Montserrat Bold 900, 22px, #FFF, #CC0000 bg |
| Slide counter | Inter Regular, 22px, #BBBBBB |
| ETKM logo text | Montserrat Bold 900, 28px, #CC0000 |
| Swipe cue | Inter Regular, 18px, #575757 |
| Bottom rule | Line, 1px, rgba(255,255,255,0.10) |
| Export | JPG, 90% quality, all slides as ZIP |
| Final slide | Use etkm_final_slide_TEMPLATE.html — change badge and counter only |

---

## Section 11 — Notion Reference Map

| Need | Location |
|---|---|
| Full visual specs | ETKM Carousel System (34e924c8) |
| Content arc library | ETKM Carousel System Section 9 |
| Production status | ETKM Carousel System Section 12 |
| Slide type library | ETKM Carousel Slide Type Library v3 (HTML) |
| CTA language bank | etkm-cta-architecture skill |
| Audience segments | etkm-audience-intelligence skill |
| Brand voice | etkm-brand-foundation skill |

---

## Section 12 — Session Opening Protocol

1. Load etkm-carousel-system
2. Load etkm-brand-foundation
3. Load etkm-cta-architecture
4. If segment-specific: load etkm-audience-intelligence
5. Confirm arc with Nathan before building
6. Pull production status from Notion (34e924c8 Section 12)
7. State: "Ready to build. Arc is [confirmed / needs confirmation]. Last completed slide: [X]."

---

## Section 13 — Type Z Final Slide Spec (Unified CTA + Brand Close)

Type Z is the final slide of every carousel. Always. One slide. Two jobs.

### Architecture

Static core (never edit): Pre-rendered PNG containing the complete layout.
- Black background (#000000), red left bar
- ETKM circle logo (110px centered)
- ETXkravmaga.com (ETX in #CC0000, KRAVMAGA.COM in #FFF)
- Tyler, Texas · Est. 2006 tagline (#575757)
- Red rule (40px)
- FB / IG / LI / YT social icons (#CC0000, 20px)
- Horizontal mid-rule separating brand from CTA
- CTA Element 1 — Transformation: "STOP HOPING YOU COULD HANDLE IT. START KNOWING." (#FFF / #CC0000)
- CTA Element 2 — Direct CTA button: "ATTEND A FREE TRIAL CLASS" (#CC0000 bg, #FFF text)
- CTA Element 3 — Transitional: "Not ready? DM us CONFIDENT for the free training checklist."
- CTA Element 4 — Stakes: "Because waiting does not make the threat go away."
- Bottom rule, ETKM wordmark, Tyler TX

Dynamic layer (edit per carousel — two elements only):
1. .series-badge (top-left): series name matching all other slides
2. .slide-counter (top-right): "XX / XX" matching carousel total

Production: Open etkm_final_slide_TEMPLATE.html. Change badge and counter. Export. Done.

### CTA Language Source

ETKM General primary set from etkm-cta-architecture skill Section 3A.
For segment-specific carousels: rebuild static core using the arc-appropriate language from Section 3B.
The static core is rebuilt once per segment, then reused for all carousels in that segment series.

### Logo Rendering Note

ETKM circle logo PNG has black (#000000) background. On the black slide field the logo background is invisible — white ring, red text, and white symbol render cleanly. No transparency processing required. Place as-is.

### Final Slide Background

#000000 solid. No photo. No overlay. Static core PNG handles all layout.
This is a system rule — not a slide-by-slide decision.

### Sequence Position

| Slide | Type | Background |
|---|---|---|
| 01 | A Cover | Photo + 45% overlay |
| 02 | B Re-Hook | Photo + 45% overlay |
| 03 | C Stakes | Photo + 45% overlay |
| 04-N | D-Y Body | Photo + 45% overlay |
| N-1 | F Save Magnet | Photo + 45% overlay |
| N | Z Final Slide | #000 solid — static core |

---

## Non-Negotiables

- Never build without a locked arc
- Never present a slide with a known Gate 1 failure
- Never use prohibited CTA language
- Never make ETKM the hero
- Never modify a Tier 1 design token
- Never use #FF0000
- Always run Gate 1 before Gate 2
- Always run Gate 2 before handoff to Nathan
- Type Z is always the final slide — one slide, two jobs — never omit
- Type G is retired — do not use a separate CTA-only slide