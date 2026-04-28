---
name: etkm-carousel-system
version: 2.1
updated: 2026-04-27
description: >
  Production ruleset for building ETKM Instagram carousels. V2.1: Added Notion
  Slide Type Library page (350924c8-1673-815d-a299-d8f50b8c14ee) to reference
  map — this is now the authoritative type reference for Claude during sessions.
  Slide types regrouped by format: Structural (A-D), Narrative (F-I), List
  Formats (J-K), Quote Formats (L-M), Data & Stats (N-P), Protocol & Decision
  (Q-R), Framework & Model (S-T), Authority & Proof (U-W), Pattern Interrupts
  (X-Y), Final Slide (Z). All slides A-Y carry photo background. Type Z is the
  single exception: pure black, always final, CTA copy from etkm-cta-architecture only.
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
depends_on:
  - etkm-brand-foundation
  - etkm-cta-architecture
loads_on_demand:
  - etkm-audience-intelligence
---

# ETKM Carousel System

**Version:** 2.1
**Last Updated:** 2026-04-27
**Changes from V2.0:** Added Notion Slide Type Library page to Section 14. This page (350924c8-1673-815d-a299-d8f50b8c14ee) is now the authoritative type reference Claude reads via Notion MCP during sessions. The HTML library (etkm_carousel_library_v4_FINAL.html) is Nathan's Canva visual companion — not for Claude's operational use.
**Library (Notion):** ETKM Carousel Slide Type Library — 350924c8-1673-815d-a299-d8f50b8c14ee
**Library (Visual):** etkm_carousel_library_v4_FINAL.html (Nathan's Canva reference only)
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

Hard rules: #CC0000 max three places per slide (bar + badge + one accent line). #FF0000 permanently retired. Gradients and trend palettes prohibited.

---

## Section 2 — Structural Elements (Fixed Layer — Every Slide)

| Element | Position | Size | Color | Override |
|---|---|---|---|---|
| Red bar | Left edge, full height | 25px | #CC0000 | None — never removed |
| Series badge | Top-left | Montserrat 900 22px | #FFF on #CC0000 | Text changes per series only |
| Slide counter | Top-right | Inter 400 22px | #BBBBBB | Numbers change only |
| ETKM logo/handle | Footer bottom-left | Montserrat 900 | #CC0000 | Type Z: @etxkravmaga in #333 |
| Swipe cue / location | Footer bottom-right | Inter 400 | #575757 | Type Z: Tyler, TX in #333 |
| Bottom rule | Footer top | 0.5px | rgba(255,255,255,0.10) | Type Z: 0.06 opacity |

---

## Section 3 — Photo & Background Treatment (Locked)

EVERY slide A through Y: Two-layer system applied identically.
- Layer A: grayscale 100%, brightness 40%, contrast +20%, 4:5 portrait crop centered on action zone
- Layer B: solid black overlay, 45% opacity

Type Z ONLY: #000000 solid — no photo, no overlay. This is the single exception in the entire system.

Series photo rule: One photo per carousel. Same photo, same treatment, all body slides.

---

## Section 4 — Typography Hierarchy

| Role | Font | Canvas size | Color |
|---|---|---|---|
| H1 Cover | Montserrat 900 | 108px | #FFFFFF |
| H1 Body responsive | Montserrat 900 | See below | #FFFFFF |
| H2 Sub-headline | Inter 600 | 36px | rgba(255,255,255,0.60) |
| Body copy | Inter 400 | 30px | rgba(255,255,255,0.75) |
| Eyebrow / label | Montserrat 900 | 22px | #BBBBBB |
| CTA setup line (Z) | Inter 700 | 20px display | #575757 |
| CTA headline (Z) | Montserrat 900 | 64px display | #FFF / #CC0000 |

Responsive headline sizing (body slides): 1-2 words/line = 52px (-1.5px tracking). 3-4 words = 46px (-1px). 5+ words = 36px (-0.5px). max-width: 340px hard limit.
Red accent rule: Maximum one line per slide in #CC0000.

---

## Section 5 — Slide Type Library

Reference the Notion Slide Type Library (350924c8-1673-815d-a299-d8f50b8c14ee) for full specs per type.
Below is the operational summary for session use.

### Complete Type Reference (A-Z)

**GROUP 1: STRUCTURAL** — Position-fixed. Never interchangeable.

| Type | Name | Position | Job |
|---|---|---|---|
| A | Cover Hook | Slide 01 — always | Stop the scroll · external problem · no solutions |
| B | Re-Hook | Slide 02 — always | Second-chance hook · internal problem · works cold · inverts cover |
| C | Stakes Bridge | Slide 03 — always | Philosophical problem · guide authority · bridge line required |
| D | Save Magnet | Slide N-1 — always | Reference card · "Screenshot this." · standalone test required |

**GROUP 2: NARRATIVE** — Content delivery. One idea per slide. Bridge lines required except final principle slide.

| Type | Name | Job |
|---|---|---|
| F | Principle / Body | The workhorse · responsive headline sizing · max 40 words |
| G | Scenario Frame | Places viewer in a real-world situation · present tense always |
| H | Before / After | Transformation arc in one slide · first-person identity language · student hero in both columns |
| I | Misconception Chain | 3 connected beliefs to 1 outcome · nodes escalate in color · beliefs are villain not person |

**GROUP 3: LIST FORMATS** — Scannable items. #1 save-rate format category.

| Type | Name | Job |
|---|---|---|
| J | Numbered List | Multiple items · max 6 · reference-worthy not narrative · #1 save-rate format |
| K | Checklist | Actionable audit · ~50% checked · max 6 items · highest repeat-save format |

**GROUP 4: QUOTE FORMATS** — Both carry photo background.

| Type | Name | Job |
|---|---|---|
| L | Quote Card | Short powerful statement · pattern interrupt at midpoint · max 8 words · max one per carousel |
| M | Extended Quote | Longer attributed quote · author name as authority · must be exact and verifiable |

**GROUP 5: DATA & STATS** — Number-forward. All stats must be citable before carousel ships.

| Type | Name | Job |
|---|---|---|
| N | Stat Card | Large number dominant · reframe delivers the meaning · not a restatement |
| O | Did You Know | Three rapid-fire facts · exactly 3 · highest send/forward rate · all verifiable |
| P | Comparison Table | Side-by-side multi-attribute · max 4 rows · 2 columns · never name a competitor |

**GROUP 6: PROTOCOL & DECISION** — Highest save rate: in-the-moment reference cards.

| Type | Name | Job |
|---|---|---|
| Q | Three-Step Process | Exactly 3 steps — non-negotiable · sequential protocol · action verb leads each step |
| R | Decision Tree | If X to Y / if not X to Z · root node #CC0000 · YES neutral · NO red · max 2 levels deep |

**GROUP 7: FRAMEWORK & MODEL** — Named mental models.

| Type | Name | Job |
|---|---|---|
| S | Framework Slide | Named model · framework name in #CC0000 · max 4 components · if no name exists, create one |
| T | Timeline / Progression | Sequential phases · active nodes #CC0000 · inactive at 45% opacity · max 4 phases |

**GROUP 8: AUTHORITY & PROOF** — Used after value delivery. V and W never on the same slide.

| Type | Name | Job |
|---|---|---|
| U | Book Reference | Attribute concept to named book · takeaway leads · book in source block always |
| V | Authority Credentials | Instructor proof · matter-of-fact · factual only · never slides 1-3 |
| W | Community / Social Proof | Student outcome numbers · 2x2 stat grid · outcome-based not vanity · primes conversion |

**GROUP 9: PATTERN INTERRUPTS** — Maximum ONE per carousel. Inserted at midpoint (slides 5-7).

| Type | Name | Job |
|---|---|---|
| X | Wrong / Right Split | What most people do vs Krav approach · wrong column never shames |
| Y | Myth Buster | Widely held belief corrected · highest share-rate format · myth is villain not person |

**TYPE Z: FINAL SLIDE — ALWAYS LAST**
The ONLY slide without a photo background. Pure black. GBRS/Jocko register. One CTA in the system.
See Section 13 for full spec.

---

## Section 6 — Standard 10-Position Sequence

| Position | Type | Job |
|---|---|---|
| Slide 01 | A — Cover Hook | External problem |
| Slide 02 | B — Re-Hook | Internal problem · works cold |
| Slide 03 | C — Stakes Bridge | Philosophical problem · guide authority |
| Slides 04-N | F-Y body slides | Value delivery · type selected by content |
| Midpoint 5-7 | Pattern interrupt (one only) | Engagement reset |
| Slide N-1 | D — Save Magnet | Reference card |
| Slide N | Z — Final Slide | Arc-derived CTA + brand close |

### Content Type to Slide Type Matrix

| Carousel type | Slide 03 | Body slides | Pattern interrupt |
|---|---|---|---|
| Principles | C | F (one per principle) | L (quote card) |
| Top 5 / List | C | J (numbered list) | Y (myth buster) |
| Statistics | C | N (stat card) + F | O (did you know) |
| Scenario | C | G (scenario frame) + F | R (decision tree) |
| How-to / Protocol | C | Q (3-step process) + F | X (wrong/right) |
| Framework | C | S (framework) + F | L or M (quote) |
| Education / Deep | C | F + U (book ref) + M (quote) | H (before/after) |

### Additional Type Insertion Rules

| Type | When | Position |
|---|---|---|
| G Scenario Frame | Scenario-based carousel | Body position |
| H Before/After | Transformation needs making visible | Before final slide |
| I Misconception Chain | Compounding false beliefs | Pattern interrupt |
| K Checklist | Actionable audit content | Body position |
| M Extended Quote | External authority reinforces point | After F body slides |
| O Did You Know | Three rapid-fire facts needed | Body or pattern interrupt |
| P Comparison Table | Two approaches across multiple dimensions | Body position |
| R Decision Tree | Conditional protocol content | Body position |
| T Timeline | Curriculum or progression content | Body position |
| U Book Reference | Principle can be sourced to a named book | Any body position |
| V Authority Credentials | Guide authority needed | Slide 5 or later — never 1-3 |
| W Social Proof | Student proof before conversion | Before final slide |

---

## Section 7 — StoryBrand Compliance Rules

Hero rule: Student is always hero. ETKM is always guide. ETKM never the subject of a body slide sentence.
Villain rule: The threat, false belief, or missed skill. Never another school. Never shame the audience.
Guide formula: Empathy first, authority second. Never lead with credentials.
Bridge line rule: Every body slide (F-Y) except the final principle slide ends with a bridge line. Opens a loop, never reveals the answer. Format: italic, Inter 400, 10px, #575757.
CTA: Governed entirely by etkm-cta-architecture skill. See Section 13.

---

## Section 8 — Arc Construction Protocol

Arc locked before building. Arc map approved by Nathan before any HTML written.
1. Content type: identify from matrix in Section 6
2. Principle sequence: order by physical activation order in a real encounter
3. Pattern interrupt: marked at midpoint position (5-7) in the arc map before building
4. Save magnet: drafted before body slides — if it cannot be drafted, the arc is incomplete
5. Final slide CTA signals: extracted at arc mapping stage (problem layer, reader arc, funnel stage, implicit promise)
6. Nathan explicit approval required before Stage 3 begins

---

## Section 9 — QC Gate 1 (Design Compliance — Claude Runs)

Hard stop rule: No slide presented to Nathan with a known Gate 1 failure. Rebuild before presenting. No exceptions.

Claude Code (authoritative): Playwright renders every slide as PNG. Pixel-level overflow check.
Chat: HTML source audit. Written QC report. Overflow estimated via font metrics — risks flagged explicitly.

15-item checklist:
1. Red bar: left edge, 25px, #CC0000, full height
2. Series badge: top-left, correct name, #CC0000 bg, #FFF text
3. Slide counter: top-right, "01 / 09" format, #BBBBBB, zero-padded
4. Safe zone: all text 100-980px H, 80-1230px V
5. Photo treatment (A-Y): grayscale 100%, brightness 40%, contrast +20%, overlay 45%
6. Headline overflow: no headline exceeds 340px max-width
7. Red accent: maximum one #CC0000 line per slide
8. Body copy: absent from Type A (cover) and Type Z (final)
9. Logo/handle: present, correct position
10. Swipe cue: present on A-Y, absent on Z
11. Bottom rule: present, correct opacity
12. Tier 1 tokens: not modified
13. Word count: within limit for slide type (A sub-line: max 12 words. F body: max 40 words.)
14. Type Z: static layer contains background + bar + footer only. No photo. No CTA baked in.
15. Type Z: all 8 dynamic elements present. Badge matches series name throughout.

Gate 1 report: "Gate 1 QC: [X]/15 items pass. [Failures by slide and item.]"

---

## Section 10 — QC Gate 2 (Messaging — Nathan Approves)

Claude prepares. Nathan approves. Nothing ships without Gate 2 sign-off.

Cover (A): External problem. Question or declarative tension. Student implied subject. No ETKM mention.
Re-hook (B): Standalone cold. Inverts cover register. Names internal problem.
Stakes (C): Guide authority without implying others inferior. Specific philosophical claim. Bridge line opens loop.
Body (F-Y): Student is hero. One idea per slide. Bridge lines open loops. Red accent on most resonant phrase.
Save magnet (D): Reference tool not recap. Passes 30-day test. Save cue explicit.
Final slide (Z): CTA derived from correct arc. All 8 dynamic elements present. Survivor arc stakes omitted. Badge matches series name.
Full arc: StoryBrand hero's journey complete. Slide 2 works cold. No contradictions. Consistent voice.

Judgment calls flagged explicitly with Claude's assessment. Nathan decides.
Revision protocol: revise flagged slides only, Gate 1 re-runs on revised slides, Gate 2 re-runs on full arc.

Gate 2 report: "Gate 2 QC — [Name]. PASS: [X]/[total]. [Judgment calls listed.] Ready pending Nathan approval."

---

## Section 11 — Canva Production Spec

| Element | Setting |
|---|---|
| Canvas size | 1080x1350px custom |
| Photo layer | Grayscale 100%, Brightness -60%, Contrast +20% |
| Black overlay | Rectangle, full bleed, black, 45% transparency |
| Red bar | Rectangle, 25px, full height, locked layer |
| Series badge | Montserrat Bold 900, 22px, #FFF, #CC0000 bg |
| Slide counter | Inter Regular, 22px, #BBBBBB |
| ETKM logo | Montserrat Bold 900, 28px, #CC0000 |
| Swipe cue | Inter Regular, 18px, #575757 |
| Bottom rule | Line, 1px, rgba(255,255,255,0.10) |
| Export | JPG, 90% quality, all slides as ZIP |
| Final slide | Use etkm_final_slide_TYPE_Z_TEMPLATE.html — edit all 8 dynamic elements per arc |

Layer order (bottom to top): Photo, Overlay, Red bar, Content elements

---

## Section 12 — Session Opening Protocol

1. Load etkm-carousel-system (this skill)
2. Load etkm-brand-foundation
3. Load etkm-cta-architecture (required — governs final slide)
4. If segment-specific: load etkm-audience-intelligence
5. Pull production status from Notion (34e924c8 Section 12)
6. Confirm arc with Nathan before building
7. State: "Ready to build. Arc is [confirmed / needs confirmation]. Last completed: [slide X or new carousel]."

---

## Section 13 — Type Z Final Slide Spec

### Design Register
GBRS Group / Jocko Willink aesthetic. Pure black. Pure command. No logo. No photo. No decoration. The words do all the work. The restraint is the authority signal.

### Architecture
Static core (never edit): background (#000) + red left bar + @etxkravmaga footer + Tyler TX + bottom rule. Four structural elements only.
Dynamic layer (edit per carousel): 8 elements, all HTML, all from etkm-cta-architecture.

### The 8 Dynamic Elements

| # | Class | What it is | Source |
|---|---|---|---|
| 1 | .series-badge | Series name | Carousel series name |
| 2 | .slide-counter | "XX / XX" | Total slide count |
| 3 | .cta-setup | Setup line — arc before-state | etkm-cta-architecture arc language |
| 4+5 | .cta-headline / .red | Transformation headline | etkm-cta-architecture Element 1 |
| 6 | .cta-command | Direct CTA | etkm-cta-architecture Element 2 |
| 7 | .cta-sub | Transitional CTA + DM keyword | etkm-cta-architecture Element 3 |
| 8 | .cta-stakes | Stakes line | etkm-cta-architecture Element 4 |

### CTA Derivation Rule
Run Derivation Engine (etkm-cta-architecture Section 8) before writing any copy on elements 3-8.
Extract four signals: problem layer, reader arc, funnel stage, implicit promise.
Match to Language Bank (etkm-cta-architecture Section 3).
The carousel arc determines every word. Never default to ETKM General without checking the arc.
Survivor arc: omit .cta-stakes entirely — never negotiable.

### Arc Quick Reference

| Arc | Setup | Headline | Command | DM Keyword | Stakes |
|---|---|---|---|---|---|
| ETKM General | Stop Hoping. | START KNOWING. | Attend a Free Trial Class | CONFIDENT | Because waiting does not make the threat go away. |
| Protector | You Already Decided They Matter. | NOW ACT ON IT. | Attend a Free Trial Class | FAMILY | Every week you wait is a week your family doesn't have this. |
| Awakened | That Feeling Is Telling You Something. | TRUST IT. | Book Your Free Trial Class This Week | READY | The moment of clarity doesn't last. Act while it's loud. |
| Fight Back ETX | You Don't Have to Feel Powerless. | TAKE BACK CONTROL. | Register for Fight Back ETX | SAFE | Omit |
| Survivor | Arc-appropriate | Arc-appropriate | Arc-appropriate | Arc-appropriate | Always omit |

### Production Steps
1. Open etkm_final_slide_TYPE_Z_TEMPLATE.html
2. Run CTA Derivation Engine (etkm-cta-architecture Section 8)
3. Edit all 8 dynamic elements
4. Run Gate 1 items 14-15
5. Export as JPG

---

## Section 14 — Notion Reference Map

| Need | Location | ID |
|---|---|---|
| Full visual specs + pixel values | ETKM Carousel System — Design & Messaging Standards | 34e924c8 |
| **Slide type specs (authoritative — Claude reads this)** | **ETKM Carousel Slide Type Library** | **350924c8-1673-815d-a299-d8f50b8c14ee** |
| Content arc library | ETKM Carousel System Section 9 | 34e924c8 |
| Production status tracker | ETKM Carousel System Section 12 | 34e924c8 |
| Operational hub | ETKM Carousel Project Hub | 350924c8 |
| CTA language bank | etkm-cta-architecture skill Section 3 | — |
| CTA derivation engine | etkm-cta-architecture skill Section 8 | — |
| Audience segments | etkm-audience-intelligence skill | — |
| Brand voice | etkm-brand-foundation skill | — |

**Note on the HTML library:** etkm_carousel_library_v4_FINAL.html is Nathan's visual Canva companion — all 26 types rendered with photo background. It is not for Claude Project Knowledge (too large). Open in browser when building in Canva.

---

## Non-Negotiables

- Never build without a locked arc
- Never present a slide with a known Gate 1 failure
- Never use prohibited CTA language (Learn More / Get Started / Click Here / Sign Up)
- Never make ETKM the hero
- Never modify a Tier 1 design token
- Never use #FF0000
- Every slide A-Y carries the photo background — no exceptions
- Type Z is the ONLY slide without a photo
- Type Z is always the final slide — never omitted
- Type E (old separate CTA) permanently retired — never use
- CTA copy is always derived from etkm-cta-architecture — never invented, never generic by default
- Always load etkm-cta-architecture — governs the final slide
- Always run Gate 1 before Gate 2
- Always run Gate 2 before handoff to Nathan
- Survivor arc never carries a stakes line
- When looking up slide type specs during a session: pull from Notion library page 350924c8-1673-815d-a299-d8f50b8c14ee via Notion MCP