---
name: etkm-carousel-system
version: 1.3
updated: 2026-04-27
description: >
  Production ruleset for building ETKM Instagram carousels. Carries slide type
  selection logic, key rules per type A-Z, design tokens, responsive headline
  sizing, StoryBrand compliance, and dual-mode QC gates. V1.3: Type Z final
  slide locked as Option 5 — pure black, "Stop Hoping. START KNOWING." Pure
  command register aligned with GBRS/Jocko. Template: etkm_final_slide_TYPE_Z_LOCKED.html.
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

**Version:** 1.3
**Last Updated:** 2026-04-27
**Changes from V1.2:** Type Z final slide locked as Option 5 — pure black, pure command register. "Stop Hoping. / START KNOWING." aligned with GBRS Group and Jocko aesthetic. Template file: etkm_final_slide_TYPE_Z_LOCKED.html. Static core PNG embedded. Only badge and counter change per carousel.
**Notion Reference:** ETKM Carousel System (page 34e924c8)
**Library Reference:** ETKM Carousel Slide Type Library v3 (25 types A-Y) + Type Z

---

## Section 1 — Design Token System (Locked)

| Token | Value | Role |
|---|---|---|
| Structural black | #000000 | All backgrounds |
| Primary white | #FFFFFF | Headlines, body copy |
| Signal red | #CC0000 | Accent, badge, CTA, red bar |
| Mid gray | #575757 | Eyebrows, swipe cue, "Stop Hoping." line |
| Light gray | #BBBBBB | Counters, attribution |
| Headline font | Montserrat 900 | ALL CAPS, all headlines |
| Body font | Inter 400/600/700 | Sub-lines, body, "Stop Hoping." line |
| Canvas | 1080x1350px | 4:5 portrait, sRGB, JPG 90% |

Hard rules: #CC0000 max three places per slide. #FF0000 permanently retired. Gradients and trend palettes prohibited.

---

## Section 2 — Structural Elements (Fixed Layer)

| Element | Position | Size | Color | Override |
|---|---|---|---|---|
| Red bar | Left edge, full height | 25px | #CC0000 | None — never removed |
| Series badge | Top-left X:100px Y:60px | Montserrat 900 22px | #FFF on #CC0000 | Content changes per series only |
| Slide counter | Top-right X:1020px Y:68px | Inter 400 22px | #BBBBBB | Numbers change only |
| ETKM logo text | Bottom-left X:100px Y:1255px | Montserrat 900 28px | #CC0000 | Type Z: @etxkravmaga handle in footer |
| Swipe cue | Bottom-right X:1020px Y:1258px | Inter 400 18px | #575757 | Type Z: "Tyler, TX" in footer |
| Bottom rule | Y:1230px X:100px-980px | 1px | rgba(255,255,255,0.10) | Type Z: rgba(255,255,255,0.06) |

---

## Section 3 — Photo & Background Treatment (Locked)

Body slides (01 through N-1): grayscale 100%, brightness 40%, contrast +20%, 45% black overlay. Same photo, all body slides.
Type Z (final slide): #000000 solid — no photo, no overlay. Static core PNG handles all layout.

---

## Section 4 — Typography Hierarchy

| Role | Font | Canvas size | Color |
|---|---|---|---|
| H1 Cover | Montserrat 900 | 108px | #FFFFFF |
| H1 Body responsive | Montserrat 900 | 52/46/36px by word count | #FFFFFF |
| H2 Sub-headline | Inter 600 | 36px | rgba(255,255,255,0.60) |
| Body copy | Inter 400 | 30px | rgba(255,255,255,0.75) |
| Micro label | Montserrat 900 | 22px | #BBBBBB |
| Setup line (Type Z) | Inter 700 | 20px display scale | #575757 |

Responsive headline sizing: 1-2 words/line=52px, 3-4=46px, 5+=36px. max-width:340px hard limit.

---

## Section 5 — Slide Type Selection Logic

### Standard 10-Position Sequence

| Position | Type | Job |
|---|---|---|
| Slide 01 | A Cover Hook | External problem, stop the scroll |
| Slide 02 | B Re-Hook | Internal problem, works cold |
| Slide 03 | C Stakes Bridge | Philosophical problem, guide authority |
| Slides 04-N | D-Y Body | Value delivery, one idea per slide |
| Midpoint 5-7 | Pattern interrupt (one only) | Engagement reset |
| Slide N-1 | F Save Magnet | Reference card, algorithm play |
| Slide N | Z Final Slide | CTA + brand close, pure command |

Content type matrix, additional type rules: see etkm-carousel-system skill v1.2 Section 5 (unchanged).

---

## Section 6 — StoryBrand Compliance Rules

Hero rule: Student is always hero. ETKM is always guide. Never make ETKM the subject of a body slide sentence.

Villain rule: The threat, false belief, or missed skill is the villain. Never make another school the villain.

Bridge line rule: Every body slide except the final principle slide ends with a bridge line. Opens a loop, never reveals the answer. Format: italic, Inter 400, 10px, #575757.

CTA rules: Four-element structure per etkm-cta-architecture skill. Prohibited: "Learn More" / "Get Started" / "Click Here" / "Sign Up".

---

## Section 7 — Arc Construction Protocol

Arc locked before building. Arc map approved by Nathan before any HTML written.
1. Content type from matrix
2. Principle sequence by physical activation order
3. Pattern interrupt at midpoint (5-7), marked in arc
4. Save magnet drafted before body slides
5. Nathan explicit approval required

---

## Section 8 — QC Gate 1 (Design Compliance — Claude Runs)

Hard stop rule: No slide presented with a known Gate 1 failure. Rebuild before presenting. No exceptions.

Gate 1 — 15-item checklist:
1. Red bar: left edge, 25px, #CC0000, full height
2. Series badge: top-left, correct name, #CC0000 bg, #FFF text
3. Slide counter: top-right, "01 / 09" format, #BBBBBB, zero-padded
4. Safe zone: all text 100-980px horizontal, 80-1230px vertical
5. Photo treatment (body slides): grayscale, 40% brightness, +20% contrast, 45% overlay
6. Headline overflow: no headline exceeds 340px max-width
7. Red accent: maximum one #CC0000 line per slide
8. Body copy absent from Type A (cover) and Type Z (final)
9. Logo/handle: present, correct position
10. Swipe cue: present on body slides, absent on Type Z
11. Bottom rule: present, correct opacity
12. Tier 1 tokens: no modification
13. Word count: within limit for slide type
14. Type Z: static core PNG rendering correctly, no photo layer
15. Type Z: only badge and counter changed, badge matches series name throughout

Gate 1 report: "Gate 1 QC: [X]/15 items pass."

---

## Section 9 — QC Gate 2 (Messaging — Nathan Approves)

Type Z specific checks:
- "Stop Hoping." setup line present
- "START KNOWING." headline present in white/red
- "ATTEND A FREE TRIAL CLASS" command present in #CC0000
- "DM CONFIDENT · etxkravmaga.com" sub-command present
- @etxkravmaga handle and Tyler TX in footer
- Badge matches series name used throughout the carousel

Full Gate 2 checklist: see v1.2 Section 9 (unchanged).
Gate 2 report: "Gate 2 QC prepared for Nathan review. [X]/[total] items pass. Ready to ship pending Nathan approval."

---

## Section 10 — Canva Production Spec

Body slides: see v1.2 Section 10 (unchanged).
Final slide: Use etkm_final_slide_TYPE_Z_LOCKED.html — change .series-badge and .slide-counter only.

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

## Section 13 — Type Z Final Slide Spec (Locked — Option 5)

### Design Register

GBRS Group / Jocko Willink aesthetic. Pure command. No logo. No photo. No decoration.
The restraint is the authority signal. The words do all the work.

### Static Core (never edit)

Pre-rendered PNG — etkm_final_slide_TYPE_Z_LOCKED.html static layer.

| Element | Value |
|---|---|
| Background | #000000 solid |
| Red bar | 5px, #CC0000, full height |
| Setup line | "Stop Hoping." — Inter 700, 20px, #575757 |
| Headline | "START KNOWING." — Montserrat 900, 64px, #FFF / #CC0000, -2.5px tracking |
| Command | "ATTEND A FREE TRIAL CLASS" — Montserrat 900, 12px, #CC0000, 4px tracking |
| Sub-command | "DM CONFIDENT · ETXKRAVMAGA.COM" — Inter, 9.5px, rgba(255,255,255,0.28) |
| Footer | @etxkravmaga (left, #333) · Tyler, TX (right, #333) |
| Bottom rule | rgba(255,255,255,0.06) |

### Dynamic Layer (edit per carousel — two elements only)

1. .series-badge (top-left): series name matching all other slides in the carousel
2. .slide-counter (top-right): "XX / XX" matching carousel total

### Production Steps

1. Open etkm_final_slide_TYPE_Z_LOCKED.html
2. Change .series-badge text to the series name
3. Change .slide-counter to match total
4. Export as JPG
5. Done

### Why This Register

This is the Jocko/GBRS close. No logo because the brand is built through the carousel — the final slide doesn't need to reintroduce it. No photo because the content is over and the ask stands alone. No decoration because restraint signals confidence. The viewer has been through 9 slides of value. The final slide simply tells them what to do next. That clarity converts.

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
- Type Z is always the final slide — never omit
- Type G (separate CTA slide) is retired — never use