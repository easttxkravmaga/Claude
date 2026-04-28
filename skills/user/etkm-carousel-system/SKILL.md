---
name: etkm-carousel-system
version: 2.3
updated: 2026-04-27
description: >
  Production ruleset for building ETKM Instagram carousels. V2.3: Section 4
  (Typography Hierarchy) updated with production canvas calibration standard.
  All type sizing is calibrated to the 1080x1350 production canvas — not the
  400x500 HTML preview. Display sizes are multiplied by 2.7 at export. Minimum
  headline dominance rule added: largest headline must fill at least 40% of
  slide width at production scale. This corrects the systematic undersizing
  error identified in the Street Reality college carousel v1-v2 builds.
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
  - "final slide"
  - "CTA slide"
  - "storybrand carousel"
  - "book intelligence carousel"
depends_on:
  - etkm-brand-foundation
  - etkm-cta-architecture
loads_on_demand:
  - etkm-audience-intelligence
  - etkm-behavior-intelligence
---

# ETKM Carousel System

**Version:** 2.3
**Last Updated:** 2026-04-27
**Changes from V2.2:** Section 4 (Typography Hierarchy) updated with production canvas calibration standard. All sizing is calibrated to the 1080×1350 production canvas. The HTML preview (400×500) scales at 2.7× on export — type that looks correct in preview is systematically undersized at production scale. Section 4 now carries both display sizes and production canvas equivalents, plus the minimum headline dominance rule.
**Carousel Source Protocol (Notion):** 350924c8-1673-81b1-983c-e0ab7a0a34e6
**Library (Notion):** ETKM Carousel Slide Type Library — 350924c8-1673-815d-a299-d8f50b8c14ee
**Template:** etkm_final_slide_TYPE_Z_TEMPLATE.html

---

## Section 1 — Design Token System (Locked)

| Token | Value | Role |
|---|---|---|
| Structural black | #000000 | All backgrounds |
| Primary white | #FFFFFF | Headlines, body copy |
| Signal red | #CC0000 | Accent, badge, CTA, red bar |
| Mid gray | #575757 | Eyebrows, swipe cue, setup line |
| Light gray | #BBBBBB | Counters, attribution |
| Headline font | Montserrat 900 | ALL CAPS, all headlines |
| Body font | Inter 400/600/700 | Sub-lines, body, setup line |
| Canvas | 1080x1350px | 4:5 portrait, sRGB, JPG 90% |

Hard rules: #CC0000 max three places per slide. #FF0000 permanently retired. Gradients prohibited.

---

## Section 2 — Structural Elements (Fixed Layer — Every Slide)

| Element | Position | Color | Override |
|---|---|---|---|
| Red bar | Left edge, full height | #CC0000 | Never removed |
| Series badge | Top-left | #FFF on #CC0000 | Text changes per series only |
| Slide counter | Top-right | #BBBBBB | Numbers change only |
| ETKM logo/handle | Footer bottom-left | #CC0000 | Type Z: @etxkravmaga in #333 |
| Swipe cue / location | Footer bottom-right | #575757 | Type Z: Tyler, TX in #333 |
| Bottom rule | Footer top | rgba(255,255,255,0.10) | Type Z: 0.06 opacity |

---

## Section 3 — Photo & Background Treatment (Locked)

Every slide A through Y: grayscale 100%, brightness 40%, contrast +20%, 4:5 portrait crop, 45% black overlay.
Type Z ONLY: #000000 solid. No photo. No overlay. The single exception in the system.
One photo per carousel. Same photo, same treatment, all body slides.

---

## Section 4 — Typography Hierarchy (Production Canvas Standard)

### The Calibration Rule

All type is sized for the 1080×1350 production canvas. The HTML build environment renders slides at 400×500 (display). Playwright exports at 2.7× scale to produce 1080×1350. Type that looks correct in the 400px preview is systematically 35-50% undersized at the production scale the audience actually sees.

**The operating rule:** Build in HTML at 400px display. Before exporting, verify every headline against the production canvas standard below — not the preview render.

**Minimum headline dominance rule:** The largest headline on any slide must fill at least 40% of the slide width at production scale (432px of 1080px). If it doesn't — it's undersized. Increase until it does.

### Production Canvas Type Standards

| Role | Display size (400px HTML) | Production equivalent (1080px) | Color |
|---|---|---|---|
| H1 Cover | 46px | 124px | #FFFFFF |
| H1 Body — 1-2 words/line | 60-72px | 162-194px | #FFFFFF |
| H1 Body — 3-4 words/line | 46-54px | 124-146px | #FFFFFF |
| H1 Body — 5+ words/line | 34-40px | 92-108px | #FFFFFF |
| Stat number | 90-100px | 243-270px | #CC0000 |
| Quote text | 13-16px | 35-43px | #FFFFFF italic |
| H2 Sub-headline | 12-14px | 32-38px | rgba(255,255,255,0.60) |
| Body copy | 11-13px | 30-35px | rgba(255,255,255,0.55) |
| Eyebrow / label | 7px | 19px | #575757 |
| Bridge line | 9-10px | 24-27px | #444 italic |
| Save magnet title | 12-13px | 32-35px | #FFFFFF |
| Save magnet item title | 11-12px | 30-32px | #FFFFFF |
| Save magnet item desc | 9-10px | 24-27px | rgba(255,255,255,0.50) |
| Save cue | 10px | 27px | #CC0000 |
| CTA setup line (Z) | 14px | 38px | #575757 |
| CTA headline (Z) | 64-72px | 173-194px | #FFF / #CC0000 |
| CTA command (Z) | 11px | 30px | #CC0000 |

### Responsive Headline Selection

Use word count per line to select the correct H1 Body size:
- 1-2 words/line: 60-72px display — these are the punchy one-word-per-line stacks (CALM. / AWARE. / READY.)
- 3-4 words/line: 46-54px display — standard principle headlines
- 5+ words/line: 34-40px display — longer philosophical statements

max-width: 320px display (864px production) — hard limit, no exceptions.

### The 50% Growth Rule (From Nathan, v2.3)

When a carousel build is reviewed and headlines feel undersized, the correction is approximately +50% on all affected body headlines. This reflects the systematic calibration gap between the 400px preview and the 1080px production canvas. If in doubt — go bigger. GBRS and Jocko run their headlines large enough to stop a scroll at full canvas scale. Timid type doesn't stop a scroll.

### What Does Not Change With Scale

Structural elements (badge, counter, footer, red bar, eyebrow) stay at their display sizes — these are deliberately small. The hierarchy depends on the contrast between dominant headlines and subordinate structural elements. The badge at 7px display is correct at both scales — it should feel small. The headline at 46px display is correct at production scale — it should feel dominant.

---

## Section 5 — Slide Type Library

Full specs in Notion Slide Type Library (350924c8-1673-815d-a299-d8f50b8c14ee).

---

## Section 6 — The 11-Position StoryBrand Beat Map

| Position | Type | StoryBrand Beat | Beat Job |
|---|---|---|---|
| 01 | A — Cover Hook | External problem | Name the villain. Stop the scroll. No solutions. |
| 02 | B — Re-Hook | External problem (cold entry) | Works with zero context. Inverts cover register. |
| 03 | C — Stakes Bridge | Internal + philosophical problem | The wound beneath the surface. The injustice behind it. |
| 04-05 | N, O — Data | Villain named with evidence | Proof the threat is real. Stats, behavioral patterns, citations. |
| 06 | F — Fears | Internal problem deepened | What freezing actually feels like. Cost of unpreparedness. |
| 07 | M — Quote | Guide introduced — empathy signal | External authority names the problem and points toward the path. |
| 08 | F — Solution | Guide introduces the plan | What training produces. The finish line — identity, not technique. |
| 09 | Y — Myth Buster | Stakes / failure without acting | The belief that puts people at risk. Named and corrected. |
| 10 | D — Save Magnet | Success visible / tools given | The hero equipped. Reference card. Screenshot-worthy. |
| 11 | Z — Final | CTA — hero asked to act | Arc complete. etkm-cta-architecture Derivation Engine closes it. |

---

## Section 7 — StoryBrand Compliance Rules

Hero: Student always hero. ETKM always guide. ETKM never the subject of a body slide sentence.
Villain: The threat, false belief, or missed skill. Never another school. Never shame.
Guide formula: Empathy first. Authority second. Never lead with credentials.
Bridge lines: Every body slide (F-Y) except the final principle slide ends with a bridge line.
CTA: Governed entirely by etkm-cta-architecture. See Section 13.

---

## Section 8 — Arc Construction Protocol (StoryBrand-First Build Sequence)

Nine stages. Every carousel. No exceptions. No HTML before Stage 8 approval.

Stage 1: Pull segment StoryBrand arc from Story Arcs Master File (335924c8-1673-814c-ae2e-e0ff833c8760)
Stage 2: Pull Problem-Solution Map (335924c8-1673-815c-87f4-dd02d0c8d0eb) — External / Internal / Philosophical / Solution
Stage 3: Pull Fear-Based Messaging entry (335924c8-1673-8113-9d86-de99b1cf1f07) — Fear / Mindset / Skill / Drill
Stage 4: Query Book Intelligence (30aa3a08-c412-4eed-874a-537a8221ea1b) using Carousel Source Protocol beat-to-source table (350924c8-1673-81b1-983c-e0ab7a0a34e6)
Stage 5: Pull Messaging Themes and Principles (335924c8-1673-8184-9412-d2cc89e3ba43)
Stage 6: Map all sourced content to 11 beat positions — every beat filled before arc map is written
Stage 7: Assign slide types — type is the LAST decision, beat and source determine it
Stage 8: Present three-column arc map (Slide | Type + Beat | Source + draft) — Nathan approves before HTML is written
Stage 9: Run CTA Derivation Engine (etkm-cta-architecture Section 8) — four signals → Language Bank → final slide copy

---

## Section 9 — QC Gate 1 (Design Compliance — Claude Runs)

Hard stop rule: Rebuild any failing slide before presenting. No exceptions.

15-item checklist:
1. Red bar — 25px, #CC0000, full height
2. Series badge — correct name, #CC0000 bg
3. Slide counter — zero-padded, "01 / 11" format
4. Safe zone — all text within bounds
5. Photo treatment (A-Y) — grayscale 40% brightness +20% contrast 45% overlay
6. Headline overflow — max-width 320px display
7. Red accent — one #CC0000 line maximum per slide
8. Body copy — absent from Type A and Type Z
9. Handle/logo — present, correct position
10. Swipe cue — present A-Y, absent Z
11. Bottom rule — present, correct opacity
12. Tier 1 tokens — not modified
13. Word count — within type limits
14. Type Z static layer — bg + bar + footer only
15. Type Z dynamic layer — all 8 elements present, badge matches throughout

**Typography production check (new in v2.3):** Before Gate 1 passes on any carousel, verify the largest headline on each body slide against Section 4 production canvas standards. If the headline fails the 40% dominance rule — flag as a Gate 1 failure and rebuild at correct size.

Gate 1 report: "Gate 1 QC: [X]/15 items pass. Typography production check: [pass/flag]."

---

## Section 10 — QC Gate 2 (Messaging — Nathan Approves)

Claude prepares, Nathan approves. Nothing ships without sign-off. Source verification: every body slide traceable to a named source.

Gate 2 report: "Gate 2 QC — [Name]. PASS: [X]/[total]. Source verification: [pass/flag]. Ready pending Nathan approval."

---

## Section 11 — Canva Production Spec

Canvas 1080x1350px. Photo layer grayscale/brightness/contrast. Overlay 45% black. Export JPG 90%.
Final slide: Use etkm_final_slide_TYPE_Z_TEMPLATE.html — edit all 8 dynamic elements per arc derivation.

**Canva type note:** When building in Canva rather than HTML, use the production canvas sizes from Section 4 directly. Canva renders at native 1080px so no scaling factor applies.

---

## Section 12 — Session Opening Protocol

1. Load etkm-carousel-system v2.3
2. Load etkm-brand-foundation
3. Load etkm-cta-architecture
4. Load etkm-audience-intelligence if segment-specific
5. Pull Carousel Source Protocol (350924c8-1673-81b1-983c-e0ab7a0a34e6)
6. Pull production status (34e924c8 Section 12)
7. Confirm segment and arc with Nathan
8. State: "Skills loaded. Source Protocol pulled. Segment: [X]. Arc: [confirmed / needs confirmation]."

---

## Section 13 — Type Z Final Slide Spec

GBRS/Jocko register. Pure black. Pure command. No photo.
Static core: bg + red bar + @etxkravmaga + Tyler TX + bottom rule.
Dynamic: 8 elements, all from etkm-cta-architecture Derivation Engine.
.cta-command must sit on one line — shorten if it wraps.
Survivor arc: omit .cta-stakes always.

Arc Quick Reference:
- ETKM General: "Stop Hoping." / "START KNOWING." / "Attend a Free Trial Class" / CONFIDENT / stakes
- Protector: "You Already Decided They Matter." / "NOW ACT ON IT." / FAMILY / stakes
- Awakened: "That Feeling Is Telling You Something." / "TRUST IT." / "Book Your Free Trial Class" / READY / stakes
- Fight Back ETX: "You Don't Have to Feel Powerless." / "TAKE BACK CONTROL." / SAFE / omit stakes
- Survivor: arc-appropriate / always omit stakes

---

## Section 14 — Notion Reference Map

| Need | Location | ID |
|---|---|---|
| **Carousel Source Protocol** | **Carousel Source Protocol** | **350924c8-1673-81b1-983c-e0ab7a0a34e6** |
| Slide type specs | ETKM Carousel Slide Type Library | 350924c8-1673-815d-a299-d8f50b8c14ee |
| Full visual specs | ETKM Carousel System | 34e924c8 |
| Production status | ETKM Carousel System Section 12 | 34e924c8 |
| StoryBrand 2.0 Framework | Brand Intelligence Hub | 335924c8-1673-8105-bd94-db7f68bffcd8 |
| Problem & Solution Maps | Brand Intelligence Hub | 335924c8-1673-815c-87f4-dd02d0c8d0eb |
| Fear-Based Messaging | Brand Intelligence Hub | 335924c8-1673-8113-9d86-de99b1cf1f07 |
| Story Arcs Master File | Brand Intelligence Hub | 335924c8-1673-814c-ae2e-e0ff833c8760 |
| Messaging Themes & Principles | Brand Intelligence Hub | 335924c8-1673-8184-9412-d2cc89e3ba43 |
| Quick Reference Index | Brand Intelligence Hub | 335924c8-1673-8144-a201-d7c0e4b35aee |
| Book Intelligence Library | Content Bank database | 30aa3a08-c412-4eed-874a-537a8221ea1b |
| CTA language bank | etkm-cta-architecture skill Section 3 | — |
| CTA derivation engine | etkm-cta-architecture skill Section 8 | — |

---

## Non-Negotiables

- Never build without a locked arc
- Never write copy before Stages 1-7 complete
- Never present a slide with a known Gate 1 failure
- Typography production check runs before Gate 1 passes — undersized headlines are Gate 1 failures
- Never use prohibited CTA language
- Never make ETKM the hero
- Never modify a Tier 1 design token
- Never use #FF0000
- Every slide A-Y carries photo background — Type Z is the ONLY exception
- Type Z is always the final slide — never omitted
- CTA copy always from etkm-cta-architecture — never improvised
- Every body slide traceable to a named source
- Slide type is always the last decision
- Survivor arc never carries a stakes line
- .cta-command on Type Z must sit on one line — shorten if it wraps