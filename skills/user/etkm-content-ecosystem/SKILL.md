---
name: etkm-content-ecosystem
version: 1.0
updated: 2026-04-03
description: >
  The production routing skill for all ETKM content runs — from a single blog post
  to a full topic cluster package. Load this skill when a content production run is
  being planned or executed. Governs the Content Brief, three production dials
  (Scale / Social / Delivery), output configuration, asset registration, and
  cross-link protocol. Works alongside etkm-marketing-engine (funnel framework
  routing), etkm-brand-foundation (voice), and etkm-audience-intelligence (segment
  data). Trigger for: "write a blog", "content for X topic", "build a series",
  "content brief", "how much do we produce on this", "social for this",
  "email series for this topic", "field manual", "action plan", "checklist",
  "student resource", "topic cluster", "package", "how deep do we go".
---

# ETKM Content Ecosystem

**Version:** 1.0
**Established:** 2026-04-03
**Project Instructions:** ETKM-Content-Ecosystem-Instructions.md (Google Drive → AI Resources)
**Works Alongside:** etkm-marketing-engine, etkm-brand-foundation, etkm-audience-intelligence
**Publishes To:** WordPress (primary) + Notion Blog Database (mirror, always)

---

## SECTION 1: WHAT THIS SKILL DOES

Routes all ETKM content production runs. Every run — regardless of size — starts
with a Content Brief and three dial settings. This skill tells Claude how to read
the brief, configure the production checklist, and hand off to the right skills
for execution.

This skill does NOT contain funnel framework templates (etkm-marketing-engine),
segment profiles (etkm-audience-intelligence), or visual standards (etkm-brand-kit).
It governs production scope and routing only.

For full procedures — brief format, output specs, asset registry, cross-link
protocol, Notion Blog Database fields — load the project instructions document.

---

## SECTION 2: WHEN TO LOAD

**Load for:**
- Planning any content production run (single article or full package)
- Filling out a Content Brief
- Determining scale, social output, and delivery format
- Configuring the production checklist for a run
- Registering assets after a production run
- Running the cross-link pass on new content

**Load ALONGSIDE:**
- `etkm-marketing-engine` — always. Routes content to correct funnel framework.
- `etkm-audience-intelligence` — when segment-specific content is being produced.
- `etkm-brand-foundation` — always active for voice QC.
- `etkm-pdf-pipeline` — when any PDF asset is being built.

**Do NOT load for:**
- Pure funnel or campaign work with no blog/content component
- CRM or automation work
- Website page builds

---

## SECTION 3: THE TWO TRIGGER MODELS

Every production run is initiated one of two ways:

**Model 1 — Doctrine-Led**
A vault entry, book extraction, training principle, or curriculum concept drives
the content. Subject comes from existing ETKM doctrine.
Signal: "We have this in the vault and need to publish it." / "This principle
needs a blog."

**Model 2 — Calendar-Led**
The 52-Week PEACE Calendar has a slot to fill. Schedule drives the subject;
vault is referenced to ground the content in doctrine.
Signal: "The calendar has this topic scheduled." / "We're in this PEACE phase —
what do we produce?"

Both models use the same Content Brief. Only the entry point differs.

---

## SECTION 4: THE THREE DIALS

Every Content Brief carries three dial settings. Claude reads these and configures
the production checklist accordingly.

### Dial 1 — Scale
Sets content depth and scope.

| Setting | Articles | Use When |
|---|---|---|
| **Small** | 1 | Single concept, timely topic, quick publish |
| **Medium** | 3–5 | Deep treatment of one subject, short series |
| **Large** | 8–12 | Full topic cluster, package build, definitive resource |

### Dial 2 — Social
Controls social media output. Independent of Scale.

| Setting | Output |
|---|---|
| **Off** | No social content |
| **Light** | 1–2 posts, primary platform, direct CTA |
| **Full** | 3–5 posts, PEACE format, multi-platform, sequenced |

### Dial 3 — Delivery
Controls which output types are produced beyond the blog.

| Setting | What Gets Built |
|---|---|
| **Blog Only** | Article(s) only. WordPress + Notion. No derivatives. |
| **Blog + Email** | Article(s) + email series. Feeds CRM arc. |
| **Blog + Email + Assets** | Above + 1–2 supporting assets (checklist, PDF, resource card). |
| **Full Package** | All of the above + field manual + action plan(s) + full asset set. |

---

## SECTION 5: ROUTING TABLE

| Task | Route To |
|---|---|
| Fill Content Brief | Project instructions — Section 3 |
| Configure production checklist from dials | Project instructions — Sections 4–5 |
| Route article to funnel framework | etkm-marketing-engine |
| Segment-specific messaging | etkm-audience-intelligence |
| Apply brand voice | etkm-brand-foundation |
| Build any PDF asset | etkm-pdf-pipeline |
| Notion Blog Database record | Project instructions — Section 7 |
| Asset Registry entry | Project instructions — Section 8 |
| Cross-link pass | Project instructions — Section 9 |
| QC before any asset ships | etkm-deliverable-qc |

---

## SECTION 6: PRODUCTION QUALITY GATES

Before any content production run is marked complete:

- [ ] Content Brief fully filled — all six input fields set
- [ ] All three dials set explicitly before production begins
- [ ] All specified output types produced per dial settings
- [ ] Protector Identity Standard met on every piece — reader moves toward capability
- [ ] Minimum cross-links met (Small: 2 / Medium: 3 / Large: 4 per article)
- [ ] Blog published to WordPress
- [ ] Notion Blog Database record created and fully tagged
- [ ] Asset Registry entries created for all produced assets
- [ ] Back-link update list noted for existing content
- [ ] etkm-deliverable-qc run on all PDF and document assets

---

## SECTION 7: CHANGELOG

- V1.0 — 2026-04-03 — Initial build. Thin routing skill. Full procedures in
  ETKM-Content-Ecosystem-Instructions.md. Establishes two trigger models,
  three-dial system, routing table, and production quality gates.
