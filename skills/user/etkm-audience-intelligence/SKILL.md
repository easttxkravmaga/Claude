---
name: etkm-audience-intelligence
version: 1.1
updated: 2026-04-26
description: >
  The routing brain for all ETKM audience-specific work. Load this skill whenever
  writing, planning, or reviewing content for a specific ETKM audience segment.
  Covers segment identification, messaging, problem-solution framing, story arcs,
  objection handling, and CRM arc mapping. All audience data lives in the ETKM
  Audience Segments database in Notion — this skill tells Claude how to use it.
  Trigger for: "who is this for", "write for [segment]", "what are their pain points",
  "hooks for parents", "headlines for women", "objection handling", "which segment",
  "target audience", "persona", "story arc", "transformation story", "what problem
  do we solve for [group]", "StoryBrand layers", "arc classification", or any task
  requiring audience-specific content, messaging, or positioning. Replaces:
  etkm-audience-map, etkm-messaging-playbook, etkm-problem-solution, etkm-story-arcs.
---

# ETKM Audience Intelligence

**Version:** 1.1
**Established:** 2026-03-29
**Updated:** 2026-04-26
**Replaces:** etkm-audience-map, etkm-messaging-playbook, etkm-problem-solution, etkm-story-arcs
**Database:** ETKM Audience Segments (Notion → AI Resources → Skill Reference Data)

---

## SECTION 1: WHAT THIS SKILL DOES

This skill is the decision layer between a task and the audience data. It does NOT
contain segment profiles, hooks, headlines, or copy. That data lives in the ETKM
Audience Segments database in Notion.

This skill tells Claude:
- How to identify which segment a task is for
- What to query from Notion for each type of task
- How to apply the data once retrieved
- What rules govern audience-specific content
- How segments map to the CRM

---

## SECTION 2: WHEN TO LOAD

**Load for:**
- Writing any content targeting a specific audience (ads, emails, social posts, landing pages, video scripts)
- Planning campaigns or content calendars for specific segments
- Handling objections in sales copy or email sequences
- Writing transformation stories or testimonials
- Mapping audience segments to CRM arcs and labels
- Answering "who is this for" or "what problem do we solve for [group]"

**Do NOT load for:**
- General brand voice questions (load etkm-brand-foundation)
- Visual design decisions (load etkm-brand-kit)
- CRM pipeline/stage questions with no audience component (load etkm-crm-operations)
- Training curriculum questions (load etkm-training-program)

**Load ALONGSIDE** `etkm-cta-architecture` when writing any segment-specific content
that includes a call to action. This skill provides the audience context; etkm-cta-architecture
provides the arc-matched and program-matched CTA language and structure.

---

## SECTION 3: DECISION LOGIC

### Step 1 — Identify the Segment

Before producing any audience-specific content, identify which segment the task targets.

**The 14 Segments:**

| Code | Segment |
|---|---|
| `parents` | Parents & Families |
| `women` | Adult Women |
| `men` | Adult Men |
| `teens` | Teenagers (13-17) |
| `older-adults` | Older Adults (55+) |
| `fitness` | Fitness-Motivated Adults |
| `former-ma` | Former Martial Artists & BJJ |
| `leo-mil` | Law Enforcement / Military / First Responders |
| `private-security` | Private Security & Executive Protection |
| `ipv-survivors` | IPV Survivors |
| `occupational` | High-Risk Occupational Workers |
| `homeschool-faith` | Homeschool Families & Faith Communities |
| `corporate` | Corporate & Organizational Groups |
| `college` | College Students & Young Adults (18-26) |

**How to identify:**
1. If Nathan names the segment → use it
2. If the task implies a segment (e.g., "write a Facebook ad about family training") → infer it
3. If ambiguous → ask one question: "Which audience is this for?"
4. If it is for multiple segments → query each separately and customize per segment

### Step 2 — Query Notion

Once the segment is identified, query the **ETKM Audience Segments** database in Notion
for the matching Segment Name or Segment Code. Use the fields relevant to the task type.

### Step 3 — Apply the Data

Use the retrieved fields to produce the content. Never improvise hooks, headlines,
objections, or pain points when the database has them. The database is the source of truth.

### Content-Type Routing

| Task Type | Fields to Use from Notion |
|---|---|
| Ad copy / social post | Hooks, Headlines, Platform Notes, CTAs |
| Email campaign | Email Subjects, Hooks, Objections and Responses, CTAs |
| Landing page copy | Headlines, Pain Points, Desired Transformation, CTAs |
| Objection handling | Objections and Responses |
| StoryBrand messaging | External Problem, Internal Problem, Philosophical Problem, Desired Transformation |
| Transformation story / testimonial | Story Arc Template, Desired Transformation, Pain Points |
| Video script | Hooks, Story Arc Template, Pain Points, CTAs |
| Campaign planning | Demographics, Platform Notes, Related Behavioral Labels |
| CRM / automation | Deal Arc Label, Person Arc Label, Related Behavioral Labels, Person Type Labels |

**Note on CTAs:** The CTAs field in the Notion database provides segment-level CTA
context. For CTA construction, structure, transformation language, and arc-matched
language, load `etkm-cta-architecture`. The two sources work together — Notion provides
the segment signal; etkm-cta-architecture builds the CTA from it.

### The Three-Layer Rule (StoryBrand)

When writing any problem-solution content, always address all three layers:

1. **External Problem** — The visible, surface-level problem they would say out loud
2. **Internal Problem** — The emotional, identity-level fear (THIS drives conversion)
3. **Philosophical Problem** — The moral reason this problem should not exist

**Rule:** Internal problem drives conversion. External gets them in the door.
Philosophical makes them loyal. Always include internal. Never lead with only external.

### The Universal Solution Structure

For every segment, ETKM's solution answers all three layers:
- **External Solution:** Real-world self-defense skills that hold up under stress
- **Internal Solution:** Confidence, capability, and readiness — earned through training
- **Philosophical Solution:** Everyone deserves the right to protect themselves and the people they love

### The "I WILL GO HOME" Principle

The ultimate problem ETKM solves across every segment:
**Every person has someone they want to go home to. Every person has someone who wants them to come home.**

Training is not about fighting. It is about making it home. Use this principle to anchor
any message that needs a deeper "why."

### Multi-Segment Content

When content must speak to multiple segments (e.g., a general awareness post):
- Lead with the universal solution structure
- Use the shared motivations (capability, responsibility, frustration with performative training, confidence)
- Do NOT try to address segment-specific pain points — they conflict across segments
- Keep the CTA general: see etkm-cta-architecture ETKM General entries

### Tone Matching

Each segment record includes tone guidance in the Demographics and Platform Notes fields.
Key tone rules by segment:

| Segment | Tone |
|---|---|
| IPV Survivors | Trauma-informed, gentle, zero pressure, never center victimhood |
| LE/Military | Peer-level, operational, no fluff, credibility through specificity |
| Teens | Direct, respect-giving, NOT condescending. Parents: warm, trust-building |
| Corporate | Professional, ROI-aware, outcome-focused |
| College | Authentic, peer-level, no corporate speak |
| Former MA | Peer-to-peer, intellectually honest, never dismiss their system |

When in doubt, check the segment's Demographics field for explicit tone guidance.

---

## SECTION 4: NOTION REFERENCES

**Primary Database:** ETKM Audience Segments
**Location:** Notion → AI Resources → Skill Reference Data
**Records:** 14 (one per segment)

**How to query:** Search Notion for the segment name (e.g., "Parents & Families") or use
the segment code (e.g., "parents") to locate the matching record.

**Field Inventory (19 fields per record):**

| Field | What It Contains | When You Need It |
|---|---|---|
| Segment Name | Full segment name | Always — identification |
| Segment Code | Short code (parents, leo-mil, etc.) | Routing and lookup |
| Demographics | Who they are — age, role, situation, tone guidance | Campaign planning, tone matching |
| External Problem | Surface-level problem statement | StoryBrand content, landing pages |
| Internal Problem | Emotional/identity fear | Core messaging, email sequences |
| Philosophical Problem | Moral injustice statement | Brand-level content, loyalty messaging |
| Pain Points | Specific fears and frustrations | Ad copy, email hooks, objection context |
| Desired Transformation | Before/after identity shift | Testimonials, landing pages, video scripts |
| Hooks | Top 4 ready-to-use hooks | Social posts, ads, video openers |
| Headlines | Top 5 ready-to-use headlines | Landing pages, ads, email headers |
| Email Subjects | Top 5 ready-to-use subject lines | Email campaigns |
| Objections and Responses | Common objections with responses | Sales copy, FAQ pages, email sequences |
| Story Arc Template | Before/after narrative structure | Testimonials, case studies, video scripts |
| CTAs | Segment-level CTA context — load etkm-cta-architecture for structure and language | Every conversion-oriented piece |
| Platform Notes | Facebook/Instagram/LinkedIn nuances | Platform-specific content planning |
| Deal Arc Label | Matching Pipedrive deal-level arc label + ID | CRM mapping, automation design |
| Person Arc Label | Matching Pipedrive person-level arc label + ID | CRM mapping, automation design |
| Related Behavioral Labels | Behavioral/classification labels commonly paired | Intake classification, nurture routing |
| Person Type Labels | Person-type labels that commonly apply | CRM record management |

**Supporting Reference:** Arc / Segment / CRM Label Crosswalk V1.0 (same Notion location)
— Use when mapping between marketing segments and Pipedrive labels.

---

## SECTION 5: QUALITY GATES

Before delivering any audience-specific content:

- [ ] Segment correctly identified — not assumed from vague context
- [ ] Notion data queried — not improvised from memory or training data
- [ ] All three StoryBrand layers addressed (for problem-solution content)
- [ ] Internal problem given prominence — not buried behind external
- [ ] Tone matches segment guidance — especially for sensitive segments (IPV, teens, LE)
- [ ] CTA matches segment — built per etkm-cta-architecture using arc and program entries
- [ ] Platform matches segment — content fits where it will be published
- [ ] No prohibited vocabulary used (reference etkm-brand-foundation)
- [ ] No hooks, headlines, or objection responses improvised when database has them
- [ ] CRM arc labels referenced correctly if content connects to pipeline/automation

---

## SECTION 6: CHANGELOG

- V1.1 — 2026-04-26 — Added load-alongside reference to etkm-cta-architecture in
  Section 2. Updated CTAs field note in Section 4 to defer to etkm-cta-architecture
  for structure and language. Updated quality gate CTA line to reference
  etkm-cta-architecture. Updated multi-segment CTA note to reference etkm-cta-architecture.
- V1.0 — 2026-03-29 — Initial build.
