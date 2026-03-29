# ETKM Skill Update Patches
**Version:** 1.0  
**Date:** 2026-03-28  
**Purpose:** Spec for updating 7 existing skills per the skill ecosystem plan

These are the exact additions required. Each patch shows what to add and where.
Do not rewrite the skill — append or insert only.

---

## PATCH 1 — etkm-brand-kit

**Type:** Color correction + outbound references
**Priority:** High — affects all downstream visual work

### Change 1: Fix Red Hex Value

Find in Section 1 Color Palette:
```
| Red | #CC0000 | Attention only — one element per view |
```

Replace with:
```
| Red | #CC0000 | Attention only — one element per view |
```

Also update any instance of `#CC0000` in Section 2 Proven Red Applications table.

**Reason:** All March 2026 production work uses `#CC0000`. The brand kit has `#CC0000` which is pure red — too bright, never what was used in production.

### Change 2: Add Outbound References section at the bottom

Append to end of SKILL.md:

```markdown
---

## 8. Outbound References

Skills that build outputs governed by this brand kit:

| Skill | What It Governs |
|-------|----------------|
| `etkm-webpage-build` | HTML page visual standard — hero spec, sections, fonts, breakpoints |
| `etkm-webform-build` | Form CSS standard — input styles, button colors, label typography |
| `etkm-pdf-pipeline` | PDF design system — same fonts and palette, HTML→Playwright pipeline |
| `etkm-event-page` | Event landing page patterns — inherits all page standards |
| `etkm-social-graphics` | Social canvas specs — brand palette applied to platform formats |

Any skill that produces a visual output for ETKM should reference this skill.
This brand kit IS the standard — it has no QC gates because all other skills
gate against it.
```

---

## PATCH 2 — etkm-crm-doctrine

**Type:** Outbound reference addition
**Priority:** Medium

Append to end of SKILL.md:

```markdown
---

## Outbound References

Skills that must validate against this doctrine:

| Skill | Why |
|-------|-----|
| `etkm-webform-build` | Web forms must map all fields to Pipedrive fields per this doctrine. No field ships without a CRM home. |
| `etkm-pipedrive-manus` | Make.com automation mechanics — implements this doctrine in Pipedrive |
| `etkm-nurture-sequence` | Arc labels used in email sequences must match label names in this doctrine exactly |

No pipeline structure, stage name, or arc label can be invented or modified
without Nathan's explicit authorization. These references enforce that rule.
```

---

## PATCH 3 — etkm-deliverable-qc

**Type:** Two new gate sections
**Priority:** High — blocks delivery of pages and forms without proper QC

Add two new sections after the existing gate sections (before any closing notes):

```markdown
---

## Gate: HTML Pages (etkm-webpage-build)

Run this gate before delivering any ETKM HTML page.

- [ ] Background is `#000` or `#111` — no other backgrounds
- [ ] Red is `#CC0000` — not `#CC0000` or any variant
- [ ] Fonts: Montserrat + Inter loaded from Google Fonts CDN
- [ ] Hero filter: `brightness(0.42) grayscale(100%)` — no deviations
- [ ] All images have `filter: grayscale(100%)`
- [ ] No emojis in the entire HTML file
- [ ] No prohibited words (mastery, dominate, destroy, killer, beast, crush, elite, warrior)
- [ ] No split-layout heroes
- [ ] `@media (max-width: 768px)` block present and covers all grid layouts
- [ ] All href values are real URLs — no placeholder `#` left in

Reference: `etkm-webpage-build` (full QC gate detail in Section 10)

---

## Gate: Web Forms (etkm-webform-build)

Run this gate before delivering any ETKM web form.

- [ ] `access_key` = `8365e17b-3dd5-481d-ba48-465042f70e3d`
- [ ] `subject` hidden field matches the page-specific string exactly
- [ ] `botcheck` hidden field present
- [ ] `reply_subject` and `reply_message` (Email 0) present
- [ ] `full_name` used — not `first_name` / `last_name`
- [ ] Arc dropdown option values are exact Pipedrive label strings (e.g., `Arc: Safety`)
- [ ] Every field passed the Three-Question Filter
- [ ] Every field maps to a named Pipedrive field, label, or note

Reference: `etkm-webform-build` (full QC gate detail in Section 11)
```

---

## PATCH 4 — etkm-pdf-pipeline

**Type:** Reference addition + 2 QC gates
**Priority:** Medium

### Add reference

At the top of the skill or in a dependencies section, add:

```markdown
## Dependencies

| Skill | Why |
|-------|-----|
| `etkm-brand-kit` | Visual standard — colors, fonts, palette (already referenced) |
| `etkm-webpage-build` | PDF design system uses the same HTML patterns as web pages — same fonts, same color rules, same section patterns adapted for fixed-page layout |
```

### Add QC Gates section (if not already present)

```markdown
---

## QC Gates

### Gate 1 — Font Rendering
- [ ] Montserrat is loading from base64 `@font-face` — not from Google CDN (CDN unreliable in Playwright)
- [ ] Inter is loading from base64 `@font-face`
- [ ] Headlines render in Montserrat 900 — not system fallback
- [ ] Body text renders in Inter — not system fallback
- [ ] Verify by screenshot: open the generated PDF and inspect font rendering

### Gate 2 — Brand Compliance
- [ ] Background is white (`#fff`) or black (`#000`) — correct for document type
- [ ] Accent is `#CC0000` only
- [ ] No emojis in the document
- [ ] No prohibited words
- [ ] Layout matches the HTML source — no float or grid collapse artifacts
```

---

## PATCH 5 — etkm-event-page

**Type:** Reference additions + 1 QC gate
**Priority:** Medium

### Add references

Add or update the References/Dependencies section:

```markdown
## Dependencies

| Skill | Why |
|-------|-----|
| `etkm-brand-kit` | Visual standard (already referenced) |
| `etkm-webpage-build` | Parent page standard — event pages inherit all hero spec, section patterns, font loading, and WordPress deployment rules |
| `etkm-webform-build` | Any registration form on the event page must follow webform build standard — field whitelist, Web3Forms config, arc dropdown |
```

### Add QC Gate

```markdown
---

## QC Gate — Event Page Delivery

- [ ] Registration/booking link is present and correct (Ecwid, Stripe, or Calendly — confirmed live)
- [ ] CTA button text is white — not default browser style
- [ ] Event date, time, and location are accurate and not placeholder text
- [ ] Price displayed correctly (no rounding, no missing $ sign)
- [ ] All etkm-webpage-build Gate 1–4 checks pass
- [ ] If form is on page: all etkm-webform-build Gate 1–3 checks pass
```

---

## PATCH 6 — etkm-social-graphics

**Type:** Explicit brand-kit reference + 1 QC gate
**Priority:** Low

### Update Dependencies section

Ensure `etkm-brand-kit` is listed as an explicit dependency:

```markdown
## Dependencies

| Skill | Why |
|-------|-----|
| `etkm-brand-kit` | **Primary** — all canvas colors, font specs, and image treatment come from here |
| `etkm-cinematic-doctrine` | Image composition, subject positioning, sightline zones |
```

### Add QC Gate

```markdown
---

## QC Gate — Social Graphic Delivery

- [ ] Canvas size is correct for platform (Facebook: 1200×630 / Instagram: 1080×1080 / LinkedIn: 1200×627)
- [ ] Background is `#000` or `#fff` only — no gray, no gradient
- [ ] Red is `#CC0000` — one element maximum per graphic
- [ ] Image is grayscale — no color photography
- [ ] No emojis in the graphic or caption copy
- [ ] Font is Montserrat (headline) + Inter (body) — no substitutions
```

---

## PATCH 7 — etkm-project-standard

**Type:** Reference additions for new Tier 2 skills
**Priority:** High — governs project gates

### Add to required pre-build checklist (or create one if not present)

```markdown
## Required Pre-Build Checks by Deliverable Type

| Deliverable | Required Skills to Load Before Starting |
|-------------|----------------------------------------|
| HTML page | `etkm-brand-kit` + `etkm-webpage-build` |
| Web form | `etkm-brand-kit` + `etkm-webpage-build` + `etkm-webform-build` |
| PDF | `etkm-brand-kit` + `etkm-pdf-pipeline` |
| Event page | `etkm-brand-kit` + `etkm-webpage-build` + `etkm-event-page` |
| Email | `etkm-brand-foundation` |
| Social graphic | `etkm-brand-kit` + `etkm-social-graphics` + `etkm-cinematic-doctrine` |
| CRM / automation | `etkm-crm-doctrine` + `etkm-pipedrive-manus` |

No deliverable leaves production without passing the relevant QC gates in
`etkm-deliverable-qc`.
```

---

## PATCH 8 — nate-collaboration-workflow

**Type:** Skill ecosystem section addition
**Priority:** Low — convenience reference

Append to end of SKILL.md:

```markdown
---

## ETKM Skill Ecosystem — Quick Reference

The skill library is organized in four tiers. Load skills in order of dependency.

### Tier 1 — Foundation (load for any ETKM work)
- `etkm-brand-kit` — Visual standard (colors, fonts, image rules)
- `etkm-brand-foundation` — Voice, tone, prohibited words
- `etkm-crm-doctrine` — Pipedrive architecture

### Tier 2 — Build Skills (load when making things)
- `etkm-webpage-build` — HTML pages
- `etkm-webform-build` — Web forms (requires webpage-build)
- `etkm-pdf-pipeline` — PDFs
- `etkm-event-page` — Event landing pages

### Tier 3 — Strategy (load for planning and copy)
- `etkm-funnel-master` → `etkm-leads-engine`, `etkm-nurture-sequence`
- `etkm-messaging-playbook` → `etkm-audience-map`, `etkm-content-templates`
- `etkm-grand-slam-offer`

### Tier 4 — Orchestration (load for project governance)
- `etkm-project-standard` — Master production standard
- `nate-collaboration-workflow` — This document
- `etkm-workflow-registry` — Build status tracker

### Build order for new skills
When a new skill needs to be created:
1. Define the tier (Foundation / Build / Strategy / Orchestration)
2. Load all skills it will reference before writing it
3. Write the SKILL.md with QC gates matching its tier (Tier 2: 3-4 gates, Tier 3: 1 gate)
4. Add outbound references in any Tier 1 skills it belongs under
5. Update `etkm-project-standard` pre-build checklist if it's a Tier 2 skill
```
