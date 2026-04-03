---
name: etkm-content-ecosystem
version: 1.0
updated: 2026-04-03
description: >
  The production engine for all ETKM content — from single social posts to full
  topic cluster packages. Load this skill whenever planning, building, or routing
  any content production run. Governs the Content Brief, scale dials, derivative
  templates, asset registry protocol, and cross-link rules. Works alongside
  etkm-marketing-engine (framework routing), etkm-brand-foundation (voice/messaging),
  and etkm-audience-intelligence (segment data). Trigger for: "write a blog",
  "content for X topic", "build a series", "what do we need for this subject",
  "produce content", "content brief", "social for this", "email series",
  "field manual", "action plan", "student resource", "checklist", "package",
  "topic cluster", "how deep do we go on this".
---

# ETKM Content Ecosystem

**Version:** 1.0
**Established:** 2026-04-03
**Works Alongside:** etkm-marketing-engine, etkm-brand-foundation, etkm-audience-intelligence
**Publishes To:** WordPress (primary), Notion Blog Database (mirror), CRM via etkm-crm-operations

---

## SECTION 1: WHAT THIS SKILL DOES

This skill governs the full content production lifecycle at ETKM — from the moment
a subject is identified to the moment assets are catalogued and cross-linked in the
vault. It does not contain framework templates (those live in etkm-marketing-engine)
or segment profiles (those live in etkm-audience-intelligence). This skill governs:

- How a content run starts (trigger types)
- How deep it goes (scale dials)
- What gets produced (derivative templates by dial setting)
- How assets are registered after production
- How existing assets get cross-linked into new content

Every content production run begins with a completed Content Brief. No exceptions.

---

## SECTION 2: THE TWO TRIGGER MODELS

Content production at ETKM is initiated one of two ways. Both use the same system.

### Model 1 — Doctrine-Led (Vault Trigger)
A vault entry, book extraction, training principle, or curriculum concept is ready
to be published. Content is rooted in existing ETKM doctrine.

**Signal:** "We have this concept in the vault and need to get it out." / "Book X
produced this insight — let's build content around it." / "This principle needs
a blog."

**Brief Entry Point:** Subject comes from vault. Existing vault entry is cited in
the brief under "Vault References."

### Model 2 — Calendar-Led (Schedule Trigger)
The 52-Week PEACE Calendar has a slot to fill. Content is scheduled first; vault
is referenced inside the brief to ground the content in doctrine.

**Signal:** "We need content for this week's slot." / "The calendar has [topic]
scheduled — let's build it." / "PEACE calendar says we're in [phase] — what
should we produce?"

**Brief Entry Point:** Calendar slot drives the subject. Vault is queried for
supporting material after subject is set.

---

## SECTION 3: THE CONTENT BRIEF

The Content Brief is the atom. Every piece of content — a single social post or
a 12-article package — starts here. Fill all six fields before production begins.

```
CONTENT BRIEF
─────────────────────────────────────────────────────────
SUBJECT:        [The topic, concept, or doctrine being addressed]

CONTEXT:        [Who this is for. What moment in their journey.
                 Which audience segment. What problem it solves.]

EXPECTED        [What you want at the end of this production run.
OUTPUT:          One article? A full series? An asset? A package?
                 State it plainly.]

SCALE:          [ ] Small   [ ] Medium   [ ] Large

SOCIAL:         [ ] Off     [ ] Light    [ ] Full

DELIVERY:       [ ] Blog Only
                [ ] Blog + Email
                [ ] Blog + Email + Assets
                [ ] Full Package

─────────────────────────────────────────────────────────
AUTO-CONFIGURED BY SYSTEM (Claude fills these from the dials above):

TRIGGER MODEL:  [ ] Doctrine-Led   [ ] Calendar-Led
VAULT REFS:     [Existing vault entries relevant to this subject]
ASSET TARGETS:  [Which assets will be produced — see Section 4]
CRM ARC:        [Which pipeline/arc this content feeds]
CROSS-LINK:     [Existing content to reference in this run]
PUBLISH TARGETS: WordPress + Notion Blog Database (always)
─────────────────────────────────────────────────────────
```

---

## SECTION 4: THE SCALE DIALS

### Dial 1 — Scale

Sets the depth and scope of the content run.

| | SMALL | MEDIUM | LARGE |
|---|---|---|---|
| **Concept** | Single, focused | Multi-angle | Full doctrine cluster |
| **Articles** | 1 | 3–5 | 8–12 |
| **Article length** | 600–900 words | 900–1,400 words | 1,200–2,000 words |
| **Vault impact** | 1 new entry | Multiple entries + cross-links | Sub-vault cluster built |
| **Sessions to produce** | 1 | 2–3 | Multi-week project |
| **Use when** | Timely topic, single concept, quick publish | Deep treatment of one subject, short series | Full topic cluster, package build, definitive ETKM resource |

### Dial 2 — Social

Controls social media production. Independent of Scale.

| | OFF | LIGHT | FULL |
|---|---|---|---|
| **Posts produced** | 0 | 1–2 | 3–5 |
| **Platforms** | — | Primary platform only | Multi-platform |
| **Format** | — | Single post, direct CTA | PEACE format, sequenced |
| **Scheduling** | — | Single publish | Spread over publish window |
| **Use when** | Internal resource, student-only content | Single announcement, awareness post | Campaign launch, series kickoff, package release |

### Dial 3 — Delivery

Controls which output types are produced beyond the blog.

| Setting | What Gets Built |
|---|---|
| **Blog Only** | Article(s) only. Published to WordPress + Notion. No derivatives. |
| **Blog + Email** | Article(s) + email series (see email specs below). Feeds CRM arc. |
| **Blog + Email + Assets** | Above + 1–2 supporting assets (checklist, PDF, resource card). |
| **Full Package** | All of the above + field manual + action plan(s) + full asset set. |

---

## SECTION 5: OUTPUT SPECS BY DIAL COMBINATION

Claude reads the three dial settings from the brief and configures the production
checklist below. Only the checked items are produced for that run.

### Blog Article (always produced)
- Follows ETKM voice rules (etkm-brand-foundation)
- Student is hero, ETKM is guide — no exceptions
- Opens with internal problem, not surface topic
- Minimum 2 cross-links to existing vault assets or past articles
- Closes with single CTA appropriate to funnel stage
- Published to WordPress AND mirrored to Notion Blog Database (see Section 7)
- Tagged on publish: topic tags, segment tag, funnel stage, date

### Email Series
| Scale | Emails Produced |
|---|---|
| Small | 1–2 emails |
| Medium | 4–8 emails |
| Large | 16–24 emails (2 per article) |

- Email 1: Article announcement + core insight
- Email 2: Application — what to do with the insight
- Additional emails: Deepen doctrine, handle objections, move toward CTA
- Ties to CRM arc specified in brief
- Follows etkm-marketing-engine nurture rules (one message, one job)

### Social Posts (Light)
- 1 post: Article announcement with hook and link
- 1 post: Pull a single insight from the article as standalone value
- Platform: Facebook primary unless brief specifies otherwise

### Social Posts (Full — PEACE Format)
- P: Principle post (doctrine, insight, or belief)
- E: Education post (how-to, what-to-know, breakdown)
- A: Authority post (proof, transformation, result)
- C: Connection post (story, behind-the-scenes, community)
- E: Engagement post (question, poll, challenge)
- Each mapped to a day in the publish window
- Multi-platform: Facebook + Instagram; LinkedIn if segment warrants

### Assets — Checklist
- 1 page, print-ready
- Built with etkm-pdf-pipeline
- Actionable items only — behavior-change focused
- CTA at bottom

### Assets — Student Resource Card
- Single concept, single page
- Student-facing (in-class or download)
- Visual layout, minimal copy
- No external CTA — internal use

### Assets — PDF Lead Magnet
- 5-page structure: Cover / Problem (×2) / Solution (×2) / 4-Step Plan / CTA
- Built for specific segment from brief
- Entry point to Nurture Sequence A
- Built with etkm-pdf-pipeline

### Full Package Assets
Produced only on Large + Full Package dial setting:

| Asset | Description |
|---|---|
| **Field Manual** | Full doctrine treatment. 8–15 pages. Complete reference on the subject. |
| **Action Plan** | Step-by-step protocol for applying the doctrine. Behavior-change focused. |
| **Checklist(s)** | 1 per major concept in the cluster |
| **Resource Cards** | 1 per article in the series |
| **PDF Lead Magnet** | Entry-point asset for the package |
| **Email Series** | Full 16–24 email sequence |
| **Social Campaign** | Full PEACE set for each article in the cluster |

---

## SECTION 6: THE PROTECTOR IDENTITY STANDARD

All content produced at any scale must move the reader toward a stronger protector
identity. This is not a marketing standard — it is an editorial standard.

**The test for every piece:**
- Does this change how the reader sees themselves?
- Does it move them from "I hope I could" to "I know I can"?
- Does the content build capability, not just awareness?
- Is the reader left more capable and confident than before they read it?

If the answer to any of these is no — rewrite before publishing.

This standard applies to social posts, emails, checklists, and field manuals equally.
Brevity is not an excuse for identity-neutral content.

---

## SECTION 7: NOTION BLOG DATABASE

Every blog article published to WordPress is also recorded in the Notion Blog Database.
This is non-negotiable. The Notion record is the permanent registry entry.

**Record fields (fill on every publish):**

| Field | What Goes Here |
|---|---|
| Title | Exact article title as published |
| Publish Date | Date published to WordPress |
| Topic Tags | Subject matter tags (2–5 per article) |
| Segment Tags | Audience segment(s) this targets |
| Funnel Stage | Awareness / Consideration / Student / Advanced |
| Content Cluster | Standalone or cluster name if part of a series |
| Linked Assets | Any PDFs, checklists, emails, or resources produced from this article |
| WordPress Status | Published / Draft / Scheduled |
| Vault Entry | Link to corresponding Master Vault entry if exists |
| Cross-Links | Articles or assets this piece references |

**Tag discipline:** Tags are the foundation of the gap-finding system. Every record
must be fully tagged before the production run is considered complete. Untagged
articles are invisible to the gap map.

---

## SECTION 8: ASSET REGISTRY PROTOCOL

When any asset is produced (article, PDF, email, checklist, field manual), it is
registered in the ETKM Asset Registry before the session closes.

**Minimum registry entry:**

```
Asset Name:
Asset Type:        [Blog / Email / PDF / Checklist / Field Manual / Action Plan /
                    Resource Card / Social Post Set]
Topic:
Segment:
Funnel Stage:
Date Produced:
File Location:     [Google Drive path or Notion page link]
Audience:          [Prospect-facing / Student-facing / Internal]
Linked To:         [Other assets in the same production run]
Content Cluster:   [Standalone or cluster name]
```

**Rule:** No production session ends without registry entries for every asset produced.
This is a QC gate — etkm-deliverable-qc checks for it.

---

## SECTION 9: CROSS-LINK PROTOCOL

Every content production run includes a cross-link pass. This is what turns a
collection of articles into a compounding ecosystem.

### Minimum Cross-Link Standard

| Scale | Minimum Cross-Links Per Article |
|---|---|
| Small | 2 |
| Medium | 3 |
| Large | 4 |

### Cross-Link Types

**Forward links** — New content links to existing assets:
- "For a deeper treatment of X, see our Field Manual on [topic]."
- "This principle is part of our [Series Name] — start here if you haven't."
- "Download the [Checklist Name] to apply this immediately."

**Back-links** — Existing content updated to reference new assets:
- When a new article is published that relates to an older article, the older
  article gets a "See Also" or "Related" update at the bottom.
- When a new field manual is published, all articles on that topic get a link added.

**Vault links** — Content that came from a vault entry links back to it.
- The Notion record carries the vault entry reference.
- Future content production on the same topic queries the vault first.

### Cross-Link Pass Procedure

At the end of every production run:
1. Query the Notion Blog Database for articles with matching topic/segment tags
2. Identify 2–4 existing articles or assets that directly relate to new content
3. Add cross-links to new content before publishing
4. Note which existing articles need back-link updates
5. Schedule back-link updates (complete within same session if Small/Medium;
   batch update is acceptable for Large cluster builds)

---

## SECTION 10: CONTENT GAP AWARENESS

The tag system in the Notion Blog Database is also the foundation of ETKM's
content gap map. As the database grows, patterns emerge:

- Topics covered thoroughly vs. topics barely touched
- Segments with rich content vs. segments with no content
- Funnel stages that are saturated vs. stages with gaps
- Curriculum arcs with blog support vs. arcs with none

**Gap map inputs (query the Notion Blog Database for):**
- All 14 audience segments — which have 3+ articles, which have 0–1
- All funnel stages — which are over-indexed, which are thin
- All content clusters — which are complete, which are started but incomplete
- ETKM curriculum principles — which have been addressed, which haven't

**Rule:** Gap analysis is a separate project (see new chat prompt in session notes).
This skill supports it by maintaining tag discipline on every publish.

---

## SECTION 11: TASK ROUTING

| Task | Load |
|---|---|
| Fill the Content Brief | This skill — Section 3 |
| Set dials and configure production checklist | This skill — Sections 4–5 |
| Apply brand voice to any output | etkm-brand-foundation |
| Route content to correct funnel framework | etkm-marketing-engine |
| Get segment-specific messaging data | etkm-audience-intelligence |
| Build any PDF asset | etkm-pdf-pipeline |
| Publish or configure WordPress | etkm-web-production (website build session) |
| Enter Notion Blog Database record | This skill — Section 7 |
| Register assets in Asset Registry | This skill — Section 8 |
| Run cross-link pass | This skill — Section 9 |
| QC before any asset ships | etkm-deliverable-qc |

---

## SECTION 12: QUALITY GATES

Before any content production run is considered complete:

- [ ] Content Brief fully filled — all six fields plus auto-configured fields
- [ ] Scale, Social, and Delivery dials set explicitly
- [ ] All specified output types produced per dial settings
- [ ] Protector Identity Standard met — every piece moves reader toward capability
- [ ] Minimum cross-links met per scale setting
- [ ] WordPress publish confirmed (blog articles)
- [ ] Notion Blog Database record created and fully tagged
- [ ] Asset Registry entries created for all produced assets
- [ ] Back-link update list noted (existing content to update)
- [ ] etkm-deliverable-qc run on all PDF and document assets before handoff
- [ ] CRM arc connection confirmed if Delivery includes email

---

## SECTION 13: CHANGELOG

- V1.0 — 2026-04-03 — Initial build. Establishes Content Brief format, three-dial
  system (Scale / Social / Delivery), two trigger models (Doctrine-Led / Calendar-Led),
  derivative output specs, Notion Blog Database protocol, Asset Registry protocol,
  Cross-Link Protocol, Protector Identity Standard, and gap awareness framework.
  Designed to work alongside etkm-marketing-engine, etkm-brand-foundation, and
  etkm-audience-intelligence without replacing them.
