---
name: etkm-carousel-system
version: 1.0
updated: 2026-04-27
description: >
  Production ruleset for building ETKM Instagram carousels. Carries slide type
  selection logic, key rules per type A-Y, design tokens, responsive headline
  sizing, StoryBrand compliance, and dual-mode QC gates (Gate 1: design
  compliance, Gate 2: messaging compliance). Load this skill at the start of
  every carousel build session. References ETKM Carousel System Notion page
  (34e924c8) for full visual specs — this skill carries execution rules only.
  Depends on etkm-brand-foundation and etkm-cta-architecture. Load
  etkm-audience-intelligence on-demand when building segment-specific carousels.
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
depends_on:
  - etkm-brand-foundation
  - etkm-cta-architecture
loads_on_demand:
  - etkm-audience-intelligence
---

# ETKM Carousel System

**Version:** 1.0
**Last Updated:** 2026-04-27
**Notion Reference:** ETKM Carousel System — Design & Messaging Standards (page 34e924c8)
**Library Reference:** ETKM Carousel Slide Type Library v3 (25 types A–Y)

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

**Hard rules:**
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
| ETKM logo | Bottom-left X:100px Y:1255px | Montserrat 900 28px | #CC0000 | CTA slide: 48px centered |
| Swipe cue | Bottom-right X:1020px Y:1258px | Inter 400 18px | #575757 | CTA slide: replaced with ETXKRAVMAGA.COM |
| Bottom rule | Y:1230px X:100px-980px | 1px | rgba(255,255,255,0.10) | CTA slide: 0.20 opacity |

---

## Section 3 — Photo & Background Treatment (Locked)

Every slide (01-08): Two-layer system applied identically.

Layer A — Image processing:
- Color mode: grayscale 100%
- Brightness: 40%
- Contrast: +20%
- Crop: 4:5 portrait, action zone centered

Layer B — Normalization overlay:
- Type: solid black rectangle, full bleed
- Opacity: 45%
- CTA slide override: 60% opacity only

Series photo rule: One photo per carousel. Same photo, identical treatment, slides 01-08.
Slide 09/10 (CTA): no photo — #000 solid field.

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

### The 9-Position Sequence (Standard Carousel)

| Position | Type | Job | Non-negotiable rule |
|---|---|---|---|
| Slide 01 | A Cover Hook | Stop the scroll | External problem only, no solutions, sub-line max 12 words |
| Slide 02 | B Re-Hook | Second-chance hook | Inverts cover register, works cold, internal problem |
| Slide 03 | C Stakes Bridge | Authority establishment | Philosophical claim, bridge line required, never bashes alternatives |
| Slides 04-N | D Principle Body | Value delivery | One idea per slide, max 40 words, bridge line on all but final |
| Midpoint slide 5-7 | E H I or O (choose one) | Pattern interrupt | Maximum ONE per carousel, breaks visual rhythm |
| Slide N-1 | F Save Magnet | Algorithm play | Reference card format, Screenshot this, standalone test required |
| Slide N | G CTA Close | Conversion | Four StoryBrand elements, #CC0000 button, prohibited language check |

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

---

## Section 6 — StoryBrand Compliance Rules

These rules govern every slide in every carousel. They are non-negotiable.

The hero rule: The student is always the hero. ETKM is always the guide.
- Every headline must be about the student's reality — not ETKM's credentials
- ETKM is never the subject of a body slide sentence
- Authority is established by depth of knowledge, not by self-promotion

The villain rule: The threat, the false belief, or the missed skill is the villain.
- Never make another school, approach, or instructor the villain
- Never shame the audience for not knowing something
- Most people believe X — the belief is the villain, not the person

The guide formula: Empathy first, authority second.
- Empathy = naming what the hero already feels
- Authority = delivering the plan with confidence, not credentials
- Never lead with ETKM's history or certifications

Bridge line rule: Every body slide (D-S) except the final principle slide ends with a bridge line.
- Bridge lines open a loop — they do not reveal the answer
- Format: italic, Inter 400, 10px, #575757
- Never say "In the next slide we'll cover..." — imply, do not announce

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

Step 2 — Principle sequence: Order principles by how they activate in a real encounter — not alphabetically or arbitrarily.
Physical logic: Awareness to Distance to Mobility to Angle to Improvise (Krav)
De-escalation logic: Awareness to Verbal to Distance to Positioning to Physical

Step 3 — Pattern interrupt placement: Identify the midpoint slide (position 5-7 depending on carousel length). Select pattern interrupt type from the matrix. Mark it in the arc before building.

Step 4 — Save magnet content: Draft the save magnet before building body slides. It must summarize the full arc in reference card format. If it cannot be drafted, the arc is incomplete.

Step 5 — Nathan approval: Present the complete arc map (slide number, type, hook) before building. Do not build until arc is approved. This is non-negotiable per Rule 1 of nate-collaboration-workflow.

---

## Section 8 — QC Gate 1 (Design Compliance — Claude Runs)

Environment Claude Code (Playwright — authoritative): Claude renders every slide as PNG via Playwright. Visual inspection and overflow check. Brightness, overlay, and contrast values verified against rendered output, not source.

Environment Chat (Structured source audit): Claude reads HTML source for every slide. Checks each item against the code. Produces written QC report with explicit pass/fail on every item. Overflow check uses font metrics and max-width constraints to flag risk.

The hard stop rule: No slide is presented to Nathan with a known Gate 1 failure. If any item fails — rebuild the slide before presentation. No exceptions. No explanatory notes in lieu of fixing.

Gate 1 Checklist — Binary pass/fail on every item:
- Red bar present, left edge, 25px, #CC0000, full height, z-index 3
- Series badge present, top-left, correct series name, #CC0000 bg, #FFF text
- Slide counter present, top-right, 01 / 09 format, #BBBBBB, zero-padded
- All headline text within safe zone (100-980px horizontal, 80-1230px vertical)
- Photo treatment applied: grayscale, 40% brightness, +20% contrast, 45% overlay
- Headline does not overflow 340px max-width
- Maximum one #CC0000 line in the headline per slide
- Body copy absent from Type A (cover) and Type G (CTA) slides
- ETKM logo present, bottom-left, #CC0000, correct size for slide type
- Swipe cue present on all slides except CTA, bottom-right, #575757
- Bottom rule present, correct opacity per slide type
- No Tier 1 design token modified
- Word count within limit for slide type (A: 12 sub-line, D: 40 body, F: reference card)
- CTA slide (G): #CC0000 button present, #000 background, no photo layer

Gate 1 report format: "Gate 1 QC: [X]/14 items pass. [List any failures with slide number and item.]"

---

## Section 9 — QC Gate 2 (Messaging Compliance — Nathan Approves)

Claude prepares this report. Nathan reviews and approves before the carousel ships.
Gate 2 runs identically in both Claude Code and chat environments.

Gate 2 Checklist — Claude evaluates, Nathan approves:

Cover slide (Type A):
- Hook addresses the external problem — not a solution, not a list
- Format: question or declarative tension statement
- Student is the implied subject — no ETKM mention in the hook

Re-hook (Type B):
- Works as a standalone hook with no cover context
- Inverts the cover register (if cover = question then re-hook = declaration)
- Addresses the internal problem — the self-doubt beneath the external threat

Stakes slide (Type C):
- Establishes guide authority without referencing or implying other approaches are inferior
- Philosophical claim is specific, not generic
- Bridge line opens a loop without revealing what comes next

Body slides (D through S):
- Student is the hero on every slide — ETKM never the subject of a body sentence
- Each slide delivers exactly one idea — no slide contains two ideas
- Bridge lines on all but the final principle slide — and they open loops, not summaries
- Red accent line carries the most emotionally resonant phrase per slide
- Word count within limit per slide type

Save magnet (Type F):
- Reads as a reference tool, not a recap
- Would be useful to someone who saved it and reopened it 30 days later with no context
- Save cue headline: Screenshot this. or Pin this. You'll want it.

CTA slide (Type G):
- All four StoryBrand elements present: transformation, direct CTA, transitional CTA, stakes line
- Transformation statement uses identity language: Stop [X]. Start [Y].
- Direct CTA contains: action verb + specific action + Tyler, TX location qualifier
- Prohibited language absent: no Learn More / Get Started / Click Here
- DM keyword present in transitional CTA

Full arc:
- Arc completes the StoryBrand hero's journey: External problem (A) to Internal problem (B) to Philosophical problem (C) to Plan (D-N) to Success vision (F) to Call to action (G)
- Carousel can be entered at slide 2 cold — re-hook works independently
- No slide contradicts another slide's claim
- Consistent voice across all slides — no slide sounds like a different brand

Gate 2 report format: "Gate 2 QC prepared for Nathan review. [X]/[total] items pass. Items requiring Nathan judgment: [list any items that are edge cases]. Ready to ship pending Nathan approval."

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
| ETKM logo | Text box, Montserrat Bold 900, 28px, #CC0000 |
| Swipe cue | Text box, Inter Regular, 18px, #575757 |
| Bottom rule | Line, 1px, rgba(255,255,255,0.10) |
| Export | JPG, 90% quality, download all slides as ZIP |

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
5. Confirm the content arc with Nathan before building (Rule 1: content before code)
6. Pull the current production status from Notion (34e924c8 Section 12) to confirm where the session picks up
7. State: Ready to build. Arc is [confirmed / needs confirmation]. Last completed slide: [X].

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