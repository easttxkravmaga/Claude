# ETKM Cheat Sheet — Design Decisions Record
**Why the canonical format is built the way it is**

---

## Why This Document Exists

Two cheat sheets were produced before this format was locked:
- `04_Gift_of_Fear_Cheat_Sheet.html` — desktop-first, 3-column pillars, 2-column principles, 3-column action tiers
- `04_OnCombat_Cheat_Sheet.html` — mobile-first, stacked pillars, stacked principles, stacked action tiers

Both were on-brand and functional. Neither was canonical. This document records every decision made in reconciling them into a single repeatable format.

---

## Decision Log

### 1. Mobile-first layout
**Decision:** Mobile-first base, with responsive grid enhancements at ≥ 640px.
**From:** On Combat (mobile-first) over Gift of Fear (desktop-first).
**Why:** Most students access etkmstudent.com on phones. Start with the smaller screen and add complexity — never start wide and try to shrink.

### 2. Header structure
**Decision:** Red top bar (series label only) + black main block with giant Barlow Condensed 900 title.
**From:** On Combat's red top bar. Gift of Fear's left-border accent was replaced.
**Why:** The red left border is harder to see on mobile. A full-width red top bar carries more visual authority and reads clearly at all sizes. The title goes oversized (3.8rem mobile, 5rem desktop) — Swiss International principle: type as visual mass.

### 3. Section architecture
**Decision:** Three sections only: Pillars → Principles → Action Plan. Each section gets a chip tag + counter.
**From:** Hybrid — Gift of Fear's section chips merged with On Combat's counter labels.
**Why:** The chip communicates content type. The counter communicates position. Never more than 3 sections — if content doesn't fit here, it belongs in Asset 01 not Asset 04.

### 4. Pillar cards
**Decision:** Black background tiles, pillar name in white uppercase Barlow 700, why-text in #BBBBBB Inter.
**From:** On Combat's black tile treatment over Gift of Fear's white cards with red pillar names.
**Why:** Black tiles on white background creates higher contrast. Red pillar names (Gift of Fear) violated the one-red-element-per-section rule — the numbers in Section 2 need to own the red.

### 5. Principle numbers
**Decision:** Red numbers, bold secondary-white principle text.
**From:** On Combat's red numbers over Gift of Fear's light gray numbers.
**Why:** Red numbers draw the eye to each rule and serve as the single red accent element for Section 2. Gray numbers disappeared on mobile screens.

### 6. Action plan tiers
**Decision:** Colored left bars (red/gray/black) + uppercase tier label. Stacked mobile, 3-col desktop.
**From:** On Combat's tier bar system over Gift of Fear's bordered tier cards.
**Why:** The bar-and-label treatment is cleaner at mobile sizes. The border card treatment compressed poorly on narrow screens.

### 7. Arrow prefix on action items
**Decision:** → arrow in gray (#575757), not the red ▶ used in Gift of Fear.
**From:** On Combat.
**Why:** Red bullets competed with red principle numbers. Gray arrows are directional without adding color weight. Enforces the one-red-per-section rule.

### 8. Footer
**Decision:** Single row: site name + URL, phone number, book title + author.
**From:** On Combat.
**Why:** The multi-span footer in Gift of Fear required more horizontal space. One row with flex-wrap handles narrow screens gracefully.

### 9. Max-width and centering
**Decision:** `max-width: 680px; margin: 0 auto`.
**From:** On Combat's 640px with slight expansion.
**Why:** 640px felt slightly tight for the 2-col desktop principle grid.

### 10. Background color
**Decision:** Black background (#000000) for all sections.
**Why:** Web-first assets use black backgrounds for authority and brand impact. Print stylesheet (@media print) automatically inverts to white background — one file serves both contexts.

---

## What Was Removed from Both Originals

| Element | Original Source | Removal Reason |
|---------|-----------------|----------------|
| Red left-border on header | Gift of Fear | Too narrow/subtle on mobile |
| Red pillar names | Gift of Fear | Violated one-red-per-section rule |
| Gray pillar number in principles | Gift of Fear | Too low contrast on mobile |
| Red bullet triangles in action items | Gift of Fear | Competed with Section 2 red numbers |
| Bordered action tier cards | Gift of Fear | Compressed poorly on mobile |
| book-meta italic line below title | Gift of Fear | Replaced by structured author/year line |
| "X of Y" book count in eyebrow | Both | Creates maintenance burden and false ceiling on library size |

---

## Invariants — Never Change These

1. **Three sections only.** No fourth section.
2. **Red appears in two places per document:** the top bar and the principle numbers.
3. **Font stack:** Barlow Condensed + Inter via Google Fonts.
4. **No gradients. No rounded corners on content blocks.**
5. **Max 4 pillars.** Pick the 4 a book serves most.
6. **Min 8, max 12 principles.**
7. **Action items are behaviors, not concepts.**
8. **Footer always includes:** ETKM name, website, phone number.
9. **Eyebrow is:** "ETKM Cheat Sheet / Asset 04" — no book count.
10. **Print stylesheet inverts** to white background automatically.
