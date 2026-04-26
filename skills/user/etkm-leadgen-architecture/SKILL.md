---
name: etkm-leadgen-architecture
version: 0.1
updated: 2026-04-10
description: >
  Use this skill for ANY task involving ETKM lead generation content architecture —
  free reports, lead magnets, opt-in pages, drip sequences, blog posts, or any
  top-of-funnel content designed to attract and convert cold prospects. Trigger when
  building or reviewing content intended to generate leads for ETKM. Governs the
  seven-section content framework, format calibrations, and CTA integration for
  leadgen-specific deliverables. Companion to etkm-brand-foundation (always load)
  and etkm-brand-kit (for visual builds).
---

# ETKM Lead Generation Content Architecture

**Version:** 0.1
**Status:** Pre-test — first real content build is the test. Revise to v1.0 after.
**Last Updated:** 2026-04-10

This skill governs the structure, sequencing, and tone of all ETKM lead generation
content — free reports, lead magnets, opt-in pages, drip sequences, blog posts, and
any top-of-funnel content designed to attract and convert cold prospects.

Always load `etkm-brand-foundation` alongside this skill. The brand rules there
are non-negotiable and govern voice, prohibited words, and hero/guide framing.

---

## The Seven-Section Content Architecture

Every lead gen piece — regardless of format — maps to these seven sections in order.
Abbreviate or expand each section based on format length (see Format Calibrations below).

---

### Section 1 — The Hook

**Job:** Stop the scroll. Create immediate recognition.

- Open with the internal problem, not the external symptom
- Use a pattern-interrupt question, statement, or scenario
- The reader should think: "That's me."
- No setup. No throat-clearing. First line earns the second.

**Length:** 1–3 sentences in short formats. Up to one paragraph in longer formats.

---

### Section 2 — The Problem

**Job:** Name what they're already living with. Build empathy before offering anything.

Three layers to cover (not necessarily three paragraphs — weave them):

1. **External problem** — the visible, surface-level threat or gap
2. **Internal problem** — the doubt, fear, or identity wound underneath it
3. **Philosophical problem** — why this shouldn't have to be true for them

The reader should feel seen before they feel sold to.

**Length:** 1–3 paragraphs. Longer in drip email format, shorter in PDF section headers.

---

### Section 3 — The Content

**Job:** Deliver real, actionable value. This is the core of the lead magnet.

Structure the content using two nested frameworks:

#### The Mirror Principle
Each piece of content must reflect the reader back to themselves — not showcase ETKM.
Frame every insight as: "Here's what you already know but haven't been able to name."

#### Crawl → Walk → Run
Sequence the content from accessible to capable:
- **Crawl** — A concept or principle they can absorb immediately, no experience required
- **Walk** — A framework or mental model they can apply with minimal practice
- **Run** — A skill, drill, or decision process that produces real capability over time

**Length:** The majority of the piece. Scales to format (see Format Calibrations).

---

### Section 4 — The Happy Ending

**Job:** Show them who they become. Future-pace the transformation.

- Describe the after state using identity language, not outcome language
- "You become someone who..." not "You will be able to..."
- Tie the transformation back to the internal problem named in Section 2
- Keep it brief — one short paragraph. The content earned this; don't oversell it.

Reference the Identity Transformation table in `etkm-brand-foundation` for approved language.

---

### Section 5 — The Action Plan

**Job:** Introduce ETKM as the guide. Make the path feel simple.

Present the 3-Step Plan from `etkm-brand-foundation`:

1. Attend a Free Trial Lesson
2. Get Your Personalized Training Blueprint
3. Become a Confident, Capable Protector

Frame ETKM as the bridge between where they are now and who they become.
One sentence of authority signal is enough — never more than two.

**Length:** 3–5 sentences maximum.

---

### Section 6 — The Three-Step Arc Summary

**Job:** Compress the full narrative arc into one scannable block.

Format as three short statements:
- Before: [What they're living with now]
- Bridge: [What ETKM provides]
- After: [Who they become]

This functions as a visual anchor and is especially useful in PDF and opt-in page formats.
Skip in plain-text email formats.

---

### Section 7 — The Echo CTA

**Job:** Close with one bold, specific call to action.

All CTA construction is governed by `etkm-cta-architecture`. Load that skill for
exact language, structure, and quality gates. Do not improvise CTA language here.

The Echo CTA echoes the internal problem from Section 2 — it closes the loop.
Format: one line of empathy acknowledgment + the direct CTA.

---

## Format Calibrations

| Format | Hook | Problem | Content | Happy Ending | Action Plan | Arc | CTA |
|---|---|---|---|---|---|---|---|
| Short PDF (1–2 pages) | 1–2 sentences | 1 paragraph | 3–5 bullets per crawl/walk/run | 2–3 sentences | 3 sentences | Yes | 1 line |
| Medium PDF (4–8 pages) | 1 paragraph | 2–3 paragraphs | Full crawl/walk/run with subheads | 1 paragraph | 4–5 sentences | Yes | Full CTA block |
| Drip email (sequence) | 1 sentence | 1–2 paragraphs | One crawl/walk/run level per email | 1–2 sentences | 2–3 sentences | No | 1 line |
| Blog post | 1–2 paragraphs | 2 paragraphs | Full crawl/walk/run + examples | 1 paragraph | 3–4 sentences | Optional | Full CTA block |

---

## Companion Skills — Load When

| Skill | Load When |
|---|---|
| `etkm-brand-foundation` | Always — voice, prohibited words, hero/guide framing |
| `etkm-brand-kit` | Any visual deliverable — colors, fonts, layout |
| `etkm-deliverable-qc` | Before handoff — run QC gates on every deliverable |
| `etkm-cta-architecture` | Section 7 — every CTA in every leadgen piece |

---

## Quick-Check Before Handing Off

- Does Section 1 stop the scroll without setup?
- Does Section 2 name the internal problem — not just the external threat?
- Does Section 3 deliver real value using the crawl/walk/run sequence?
- Does Section 4 use identity language, not outcome language?
- Is ETKM positioned as guide, not hero, in Section 5?
- Is the CTA built per `etkm-cta-architecture`?
- Zero prohibited words from `etkm-brand-foundation`?
- Does the full piece leave the reader feeling capable — not scared, not sold to?

---

## Changelog

- V0.1 — 2026-04-10 — Initial draft. Pre-test status. First real content build will
  validate and trigger revision to v1.0.
