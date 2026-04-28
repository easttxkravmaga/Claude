---
name: etkm-carousel-system
version: 2.2
updated: 2026-04-27
description: >
  Production ruleset for building ETKM Instagram carousels. V2.2: Section 8
  (Arc Construction Protocol) rewritten with StoryBrand-first build sequence.
  Beat map is the governing spine — slide type is the last decision, not the
  first. Full source routing table lives in Carousel Source Protocol page
  (350924c8-1673-81b1-983c-e0ab7a0a34e6). All 20 books from Book Intelligence
  Library mapped to beats. etkm-cta-architecture Derivation Engine closes every
  carousel at Beat 11. No arc map approved without all 11 beats sourced.
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

**Version:** 2.2
**Last Updated:** 2026-04-27
**Changes from V2.1:** Section 8 (Arc Construction Protocol) completely rewritten. StoryBrand beats now govern the build sequence. Slide type is the last decision. Full source routing table in Carousel Source Protocol (350924c8-1673-81b1-983c-e0ab7a0a34e6). 20 books from Book Intelligence Library mapped to beats. Beat map is the permanent 11-position spine of every carousel.
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

## Section 4 — Typography Hierarchy

| Role | Font | Canvas size | Color |
|---|---|---|---|
| H1 Cover | Montserrat 900 | 108px | #FFFFFF |
| H1 Body responsive | Montserrat 900 | 52/46/36px by line length | #FFFFFF |
| H2 Sub-headline | Inter 600 | 36px | rgba(255,255,255,0.60) |
| Body copy | Inter 400 | 30px | rgba(255,255,255,0.75) |
| Eyebrow / label | Montserrat 900 | 22px | #BBBBBB |
| CTA setup line (Z) | Inter 700 | 20px display | #575757 |
| CTA headline (Z) | Montserrat 900 | 64px display | #FFF / #CC0000 |

Responsive headline sizing: 1-2 words/line = 52px. 3-4 = 46px. 5+ = 36px. max-width: 340px hard limit.

---

## Section 5 — Slide Type Library

Full specs in Notion Slide Type Library (350924c8-1673-815d-a299-d8f50b8c14ee).
Operational summary in this skill Section 5 (unchanged from v2.1 — see prior version for full type tables).

---

## Section 6 — The 11-Position StoryBrand Beat Map

This is the permanent spine of every ETKM carousel. The beat column is the narrative architecture. The type column serves the beat — never the other way around.

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

This is the complete 9-stage build sequence. Every carousel follows every stage in order.
No HTML is written until Stage 8 is complete and Nathan has approved the arc map.

### Stage 1 — Identify Segment and Pull StoryBrand Arc

Identify the target segment. Pull from the Story Arcs Master File (335924c8-1673-814c-ae2e-e0ff833c8760) for the segment's hero's journey arc. This arc is the governing narrative — every subsequent stage must serve it.

Use the Quick Reference Index (335924c8-1673-8144-a201-d7c0e4b35aee) to locate the segment's arc number and cross-reference it to the Problem-Solution Map section and Fear-Based Messaging section.

### Stage 2 — Pull Problem-Solution Map for the Segment

Query Problem & Solution Maps (335924c8-1673-815c-87f4-dd02d0c8d0eb) for the segment's entry. Extract all four components:
- External Problem → Beat 01, 02
- Internal Problem → Beat 02, 03
- Philosophical Problem → Beat 03
- ETKM Solution → Beat 08

This is the raw material for the narrative spine. Not to be improvised.

### Stage 3 — Pull Fear-Based Messaging Entry for the Segment

Query Fear-Based Messaging Framework (335924c8-1673-8113-9d86-de99b1cf1f07) for the segment's entry. Extract:
- Fear statement → Beat 02, 06
- Mindset component → Beat 08
- Skill component → Beat 08, 10
- Drill component → Beat 10

### Stage 4 — Query Book Intelligence for Beat-Relevant Entries

Query Content Bank database (30aa3a08-c412-4eed-874a-537a8221ea1b) for books relevant to the carousel topic. Use the Carousel Source Protocol beat-to-source table (350924c8-1673-81b1-983c-e0ab7a0a34e6) to identify which books serve which beats.

Priority lookup by beat:
- Beats 01, 02, 04-05: Awareness & Threat Recognition category (Left of Bang, Situational Awareness, Gift of Fear, Six Minute X-Ray, Protecting the Gift)
- Beat 07 (guide signal): Pull one extended quote from the most relevant book. Mark as verbatim or paraphrase before the arc map is written. Verbatim = Type M. Paraphrase = Type U.
- Beat 08 (plan): Communication & Influence category first (Verbal Judo — de-escalation as the first tool). Then Krav Maga & Combat category. Then Tactics & Survival.
- Beats 06, 09: Mindset & Psychology category (On Combat, Unthinkable, Deep Survival, Meditations on Violence)

### Stage 5 — Pull Messaging Themes and Principles

Query Messaging Themes, Principles & Taglines (335924c8-1673-8184-9412-d2cc89e3ba43). Identify:
- The ETKM principle(s) most relevant to the carousel topic
- The philosophical statement that serves Beat 03
- The tagline(s) that fit the segment and arc

### Stage 6 — Map Content to the 11 Beat Positions

With all source material pulled, map extracted content to the 11-position beat table. Every beat must be filled before the arc map is written. If any beat cannot be filled from the available sources — stop. Either the segment is wrong, the topic needs adjustment, or a source is missing. Do not improvise content to fill a gap.

### Stage 7 — Assign Slide Types

With beats mapped and content sourced, assign the slide type that best presents each beat's content. Type is the last decision. The content determines the type.

Content type to slide type selection guide:
- External problem with a scenario: Type A (cover) or Type G (scenario frame)
- Internal problem as a statement: Type B (re-hook) or Type F (body)
- Philosophical claim: Type C (stakes bridge)
- Single stat with reframe: Type N (stat card)
- Three rapid facts: Type O (did you know)
- Book-sourced verbatim quote: Type M (extended quote)
- Book-sourced paraphrased principle: Type U (book reference)
- Named framework or model: Type S (framework)
- Protocol or steps: Type Q (three-step process)
- Before/after transformation: Type H (before/after)
- Myth correction: Type Y (myth buster)
- Reference card: Type D (save magnet)
- Final: Type Z — always

### Stage 8 — Draft Three-Column Arc Map for Nathan's Approval

Draft the complete arc map with three columns:

| Slide | Type + StoryBrand Beat | Content source + draft |
|---|---|---|

The source column must name the specific source document for every slide — not general knowledge. If a slide's content came from the Problem-Solution Map, name it. If it came from Left of Bang, name it. If it came from the Fear-Based Messaging Framework, name it.

Gate: Nathan approves the arc map explicitly before Stage 9 begins. No HTML is written without Nathan's approval. No exceptions.

### Stage 9 — CTA Derivation Engine

Before writing a single word of copy for Type Z, run the Derivation Engine from etkm-cta-architecture Section 8. Extract four signals from the completed arc:
- Signal A: Problem layer dominant (external / internal / philosophical)
- Signal B: Reader arc (Protector / Awakened / Regainer / Quiet Builder / Survivor / Professional)
- Signal C: Funnel stage (TOFU / MOFU / BOFU)
- Signal D: Implicit promise (from [current state] → to [desired state])

Match signals to Language Bank (etkm-cta-architecture Section 3). The arc determines every word on the final slide. Never default to ETKM General without checking the arc first.

---

## Section 9 — QC Gate 1 (Design Compliance — Claude Runs)

Hard stop rule: No slide presented with a known Gate 1 failure. Rebuild before presenting. No exceptions.

15-item checklist (full detail in prior skill versions):
1. Red bar — left edge, 25px, #CC0000, full height
2. Series badge — correct name, #CC0000 bg
3. Slide counter — zero-padded, "01 / 11" format
4. Safe zone — all text within bounds
5. Photo treatment (A-Y) — grayscale, 40% brightness, +20% contrast, 45% overlay
6. Headline overflow — max-width 340px
7. Red accent — one #CC0000 line per slide maximum
8. Body copy absent — Type A cover and Type Z final
9. Handle/logo present — correct position
10. Swipe cue — present A-Y, absent Z
11. Bottom rule — present, correct opacity
12. Tier 1 tokens — not modified
13. Word count — within type limits
14. Type Z static layer — bg + bar + footer only, no photo, no baked-in CTA
15. Type Z dynamic layer — all 8 elements present, badge matches series name throughout

Gate 1 report: "Gate 1 QC: [X]/15 items pass."

---

## Section 10 — QC Gate 2 (Messaging — Nathan Approves)

Three-column arc map verified before Gate 2 runs. Gate 2 checks messaging compliance per position. Nothing ships without Nathan's sign-off.

Additional Gate 2 check (new in v2.2): Source verification. Every body slide's content is traceable to a named source in the arc map. No slide should contain improvised content without a source citation. If a slide's content cannot be traced to a source — flag it.

Gate 2 report: "Gate 2 QC — [Name]. PASS: [X]/[total]. Source verification: [pass/flag]. Ready pending Nathan approval."

---

## Section 11 — Canva Production Spec

Unchanged from v2.1. Canvas 1080x1350px. Photo layer grayscale/brightness/contrast. Overlay 45% black. Export JPG 90%.
Final slide: Use etkm_final_slide_TYPE_Z_TEMPLATE.html — edit all 8 dynamic elements per arc derivation.

---

## Section 12 — Session Opening Protocol

1. Load etkm-carousel-system (this skill) — confirm v2.2
2. Load etkm-brand-foundation
3. Load etkm-cta-architecture (required — governs Beat 11)
4. Load etkm-audience-intelligence if segment-specific
5. Pull Carousel Source Protocol from Notion (350924c8-1673-81b1-983c-e0ab7a0a34e6)
6. Pull production status from Notion (34e924c8 Section 12)
7. Confirm segment and arc with Nathan
8. State: "Skills loaded. Source Protocol pulled. Segment confirmed: [X]. Arc: [confirmed / needs confirmation]."

---

## Section 13 — Type Z Final Slide Spec

Unchanged from v2.1. GBRS/Jocko register. Pure black. Pure command. No photo.
Static core: bg + red bar + @etxkravmaga + Tyler TX + bottom rule.
Dynamic: 8 elements, all from etkm-cta-architecture Derivation Engine.
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
| **Carousel Source Protocol (routing table)** | **Carousel Source Protocol** | **350924c8-1673-81b1-983c-e0ab7a0a34e6** |
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
- Never write a single word of copy before Stages 1-7 are complete
- Never present a slide with a known Gate 1 failure
- Never use prohibited CTA language
- Never make ETKM the hero
- Never modify a Tier 1 design token
- Never use #FF0000
- Every slide A-Y carries the photo background — no exceptions
- Type Z is the ONLY slide without a photo
- Type Z is always the final slide — never omitted
- CTA copy always derived from etkm-cta-architecture — never improvised
- Every body slide's content is traceable to a named source
- Slide type is always the last decision — the beat and source determine type
- Beat map is the spine — 11 positions, all beats present before arc map is approved
- Survivor arc never carries a stakes line