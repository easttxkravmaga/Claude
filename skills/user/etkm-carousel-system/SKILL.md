---
name: etkm-carousel-system
version: 1.4
updated: 2026-04-27
description: >
  Production ruleset for building ETKM Instagram carousels. V1.4: Type Z
  architecture corrected — static core contains background, red bar, and footer
  only. ALL CTA copy is dynamic and arc-driven by etkm-cta-architecture skill.
  CTA language is never hardcoded — it is derived from the carousel arc using
  the Derivation Engine in etkm-cta-architecture Section 8.
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

**Version:** 1.4
**Last Updated:** 2026-04-27
**Changes from V1.3:** Type Z architecture corrected. Static core now contains ONLY background (#000), red bar, and footer (@etxkravmaga, Tyler TX). All CTA copy moved to dynamic layer. CTA language is always derived from etkm-cta-architecture — never hardcoded, never static. Template: etkm_final_slide_TYPE_Z_TEMPLATE.html.

---

## Section 1 — Design Token System (Locked)

| Token | Value | Role |
|---|---|---|
| Structural black | #000000 | All backgrounds |
| Primary white | #FFFFFF | Headlines, body copy |
| Signal red | #CC0000 | Accent, badge, CTA, red bar |
| Mid gray | #575757 | Eyebrows, setup line |
| Light gray | #BBBBBB | Counters, attribution |
| Headline font | Montserrat 900 | ALL CAPS, all headlines |
| Body font | Inter 400/600/700 | Sub-lines, body, setup line |
| Canvas | 1080x1350px | 4:5 portrait, sRGB, JPG 90% |

Hard rules: #CC0000 max three places per slide. #FF0000 permanently retired. Gradients and trend palettes prohibited.

---

## Section 2 — Structural Elements (Fixed Layer)

| Element | Position | Size | Color | Override |
|---|---|---|---|---|
| Red bar | Left edge, full height | 25px | #CC0000 | None — never removed |
| Series badge | Top-left | Montserrat 900 22px | #FFF on #CC0000 | Text changes per series |
| Slide counter | Top-right | Inter 400 22px | #BBBBBB | Numbers change only |
| ETKM handle | Footer bottom-left | Montserrat 900 8px | #333 | Type Z: @etxkravmaga |
| Location | Footer bottom-right | Inter 400 7.5px | #333 | Type Z: Tyler, TX |
| Bottom rule | Footer top | 0.5px | rgba(255,255,255,0.06) | Type Z value |

---

## Section 3 — Photo & Background Treatment (Locked)

Body slides: grayscale 100%, brightness 40%, contrast +20%, 45% black overlay. One photo per carousel, same treatment all body slides.
Type Z: #000000 solid — no photo, no overlay.

---

## Section 4 — Typography Hierarchy

| Role | Font | Size | Color |
|---|---|---|---|
| H1 Cover | Montserrat 900 | 108px canvas | #FFFFFF |
| H1 Body responsive | Montserrat 900 | 52/46/36px by line length | #FFFFFF |
| H2 Sub-headline | Inter 600 | 36px canvas | rgba(255,255,255,0.60) |
| Body copy | Inter 400 | 30px canvas | rgba(255,255,255,0.75) |
| Micro label | Montserrat 900 | 22px canvas | #BBBBBB |
| CTA setup line (Type Z) | Inter 700 | 20px display | #575757 |
| CTA headline (Type Z) | Montserrat 900 | 64px display | #FFF / #CC0000 |
| CTA command (Type Z) | Montserrat 900 | 12px display | #CC0000 |
| CTA sub-command (Type Z) | Inter 400 | 9.5px display | rgba(255,255,255,0.28) |
| CTA stakes (Type Z) | Inter 400 italic | 8.5px display | #383838 |

Responsive headline sizing (body slides): 1-2 words/line=52px, 3-4=46px, 5+=36px. max-width:340px.

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
| Slide N | Z Final Slide | Arc-derived CTA + brand close |

Content type matrix: Principles/C/D/E · List/C/K/O · Stats/C/H/V · Scenario/C/J/W · Protocol/C/M/I · Framework/C/Q/E · Deep/C/D+L+N/P
Additional types L-Y: see Notion library (34e924c8).

---

## Section 6 — StoryBrand Compliance Rules

Hero: Student always hero. ETKM always guide. ETKM never the subject of a body slide sentence.
Villain: The threat, false belief, or missed skill. Never another school. Never shame.
Guide formula: Empathy first, authority second. Never lead with credentials.
Bridge lines: Every body slide except the final principle slide. Opens a loop, never reveals answer.
CTA: Governed entirely by etkm-cta-architecture — see Section 13.

---

## Section 7 — Arc Construction Protocol

1. Content type identified from matrix
2. Principle sequence by physical activation order
3. Pattern interrupt marked at midpoint (5-7)
4. Save magnet drafted before body slides built
5. Nathan explicit approval before any HTML written

---

## Section 8 — QC Gate 1 (Design Compliance — Claude Runs)

Hard stop rule: No slide presented with a known Gate 1 failure. Rebuild before presenting. No exceptions.

15-item checklist:
1. Red bar: left edge, 25px, #CC0000, full height
2. Series badge: top-left, correct name, #CC0000 bg, #FFF text
3. Slide counter: top-right, "01 / 09" format, #BBBBBB
4. Safe zone: all text 100-980px H, 80-1230px V
5. Photo treatment (body): grayscale, 40% brightness, +20% contrast, 45% overlay
6. Headline: does not exceed 340px max-width
7. Red accent: maximum one #CC0000 line per body slide
8. Body copy: absent from Type A and Type Z
9. Handle/logo: present, correct position
10. Swipe cue: present on body slides, absent on Type Z
11. Bottom rule: present, correct opacity
12. Tier 1 tokens: not modified
13. Word count: within limit for slide type
14. Type Z: static layer rendering (background + bar + footer only)
15. Type Z: CTA copy present in all five dynamic elements, badge matches series name

Gate 1 report: "Gate 1 QC: [X]/15 items pass. [Failures by slide and item.]"

---

## Section 9 — QC Gate 2 (Messaging — Nathan Approves)

Type Z specific:
- CTA derived from etkm-cta-architecture for the correct arc (verify derivation against Section 8 of that skill)
- Setup line present and arc-appropriate
- Transformation headline uses identity language: Stop [X] / Start [Y]
- Direct CTA: action verb + specific action (no "Learn More" / "Get Started" / "Click Here")
- Transitional CTA: DM keyword matching the arc
- Stakes line: present unless Survivor arc (Survivor arc = stakes line omitted entirely)
- Badge matches series name throughout carousel

Full arc Gate 2: see Notion (34e924c8) Domain 6.
Gate 2 report: "Gate 2 QC prepared for Nathan review. [X]/[total] pass. Ready pending Nathan approval."

---

## Section 10 — Canva Production Spec

Body slides: Photo/grayscale/overlay/bar/badge/counter/logo/swipe/rule — standard system.
Final slide: Use etkm_final_slide_TYPE_Z_TEMPLATE.html — edit all 8 dynamic elements per arc.

---

## Section 11 — Notion Reference Map

| Need | Location |
|---|---|
| Full visual specs | ETKM Carousel System (34e924c8) |
| Content arc library | ETKM Carousel System Section 9 |
| Production status | ETKM Carousel System Section 12 |
| Slide type library | ETKM Carousel Slide Type Library v3 (HTML) |
| CTA language bank | etkm-cta-architecture skill Section 3 |
| CTA derivation engine | etkm-cta-architecture skill Section 8 |
| Audience segments | etkm-audience-intelligence skill |
| Brand voice | etkm-brand-foundation skill |

---

## Section 12 — Session Opening Protocol

1. Load etkm-carousel-system
2. Load etkm-brand-foundation
3. Load etkm-cta-architecture (required for every carousel — governs final slide)
4. If segment-specific: load etkm-audience-intelligence
5. Confirm arc with Nathan before building
6. Pull production status from Notion (34e924c8 Section 12)
7. State: "Ready to build. Arc is [confirmed]. Last completed slide: [X]."

---

## Section 13 — Type Z Final Slide Spec

### Design Register

Option 5 — GBRS Group / Jocko Willink aesthetic. Pure black. Pure command.
No logo. No photo. No decoration. The words do all the work.

### Architecture

Static core (never edit): Background (#000) + red left bar + @etxkravmaga footer + Tyler TX + bottom rule.
That is all. Four structural elements only.

Dynamic layer (edit per carousel): 8 elements, all CTA copy.

### The 8 Dynamic Elements

| # | Class | What it is | Source |
|---|---|---|---|
| 1 | .series-badge | Series name | Carousel series name |
| 2 | .slide-counter | "XX / XX" | Total slide count |
| 3 | .cta-setup | Setup line | Arc transformation — before state |
| 4+5 | .cta-headline / .red | Transformation headline | etkm-cta-architecture Element 1 |
| 6 | .cta-command | Direct CTA | etkm-cta-architecture Element 2 |
| 7 | .cta-sub | Transitional CTA + DM keyword | etkm-cta-architecture Element 3 |
| 8 | .cta-stakes | Stakes line | etkm-cta-architecture Element 4 |

### CTA Derivation Rule

Before writing any CTA copy on the final slide, run the Derivation Engine from etkm-cta-architecture Section 8:

Step 1: Extract four signals from the carousel content (problem layer, reader arc, funnel stage, implicit promise)
Step 2: Match signals to the Language Bank (Section 3 of that skill)
Step 3: If no exact match, build custom CTA from the content's own language
Step 4: Verify the arc is complete before placing the CTA

The arc of the carousel determines every word on the final slide.
Never default to the ETKM General set without checking the arc.
Survivor arc: omit .cta-stakes entirely.

### Arc Examples

ETKM General (default for general Krav Maga content):
  setup: "Stop Hoping." · headline: "START KNOWING." · command: "Attend a Free Trial Class" · sub: "DM CONFIDENT · etxkravmaga.com" · stakes: "Because waiting does not make the threat go away."

Fight Back ETX (Fight Back series):
  setup: "You Don't Have to Feel Powerless." · headline: "TAKE BACK CONTROL." · command: "Register for the Next Fight Back ETX Class" · sub: "DM SAFE · etxkravmaga.com" · stakes: omit (Survivor arc proximity)

Protector arc:
  setup: "You Already Decided They Matter." · headline: "NOW ACT ON IT." · command: "Attend a Free Trial Class" · sub: "DM FAMILY · etxkravmaga.com" · stakes: "Every week you wait is a week your family doesn't have this."

Awakened arc:
  setup: "That Feeling Is Telling You Something." · headline: "TRUST IT." · command: "Book Your Free Trial Class This Week" · sub: "DM READY · etxkravmaga.com" · stakes: "The moment of clarity doesn't last. Act while it's loud."

### Production Steps

1. Open etkm_final_slide_TYPE_Z_TEMPLATE.html
2. Run CTA Derivation Engine (etkm-cta-architecture Section 8) for this carousel's arc
3. Edit elements 1-8 in the dynamic layer
4. Export as JPG
5. Run Gate 1 items 14-15
6. Done

---

## Non-Negotiables

- Never build without a locked arc
- Never present a slide with a known Gate 1 failure
- Never use prohibited CTA language (Learn More / Get Started / Click Here / Sign Up)
- Never make ETKM the hero
- Never modify a Tier 1 design token
- Never use #FF0000
- Always load etkm-cta-architecture — it governs the final slide
- Always run Gate 1 before Gate 2
- Always run Gate 2 before handoff to Nathan
- Type Z is always the final slide — never omit
- Type G (separate CTA slide) is retired — never use
- CTA copy is never hardcoded — always derived from the arc via etkm-cta-architecture