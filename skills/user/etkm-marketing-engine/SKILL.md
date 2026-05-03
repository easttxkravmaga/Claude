---
name: etkm-marketing-engine
version: 1.4
updated: 2026-05-03
description: >
  The routing brain for all ETKM marketing, funnel, lead generation, content
  creation, offer positioning, and nurture sequence work. Load this skill whenever
  building, planning, reviewing, or troubleshooting any part of the ETKM marketing
  system — including lead magnets, email sequences, content strategy, funnel
  architecture, offer packaging, ad campaigns, or nurture flows. All frameworks,
  templates, offer data, and sequence specs live in Notion databases — this skill
  tells Claude how to use them. etkm-cta-architecture MUST be loaded any time this
  skill is loaded — no exceptions. Trigger for: "funnel", "TOFU", "MOFU", "BOFU",
  "lead gen", "lead magnet", "nurture sequence", "email sequence", "drip
  campaign", "offer stack", "content template", "what to post", "content
  calendar", "hook template", "ad framework", "conversion", "Grand Slam Offer",
  "value equation", "More/Better/New", "how do we get more leads", "pricing",
  "membership tiers", "follow-up emails", "after they download", "re-engagement".
  Replaces:
---

# ETKM Marketing Engine

**Version:** 1.4
**Established:** 2026-03-29
**Updated:** 2026-05-03
**Replaces:** etkm-funnel-master, etkm-leads-engine, etkm-lead-gen, etkm-content-templates, etkm-grand-slam-offer, etkm-nurture-sequence
**Databases:** ETKM Marketing Frameworks, ETKM Offer Stack, ETKM Nurture Sequences (Notion → AI Resources → Skill Reference Data)

---

## SECTION 1: WHAT THIS SKILL DOES

This skill is the decision layer for all ETKM marketing work. It does NOT contain
framework templates, offer specs, or sequence email details. That data lives in three
Notion databases.

This skill tells Claude:
- How the ETKM funnel is structured and what each stage's job is
- How to route a task to the right framework, offer, or sequence
- What rules govern lead generation, content creation, and nurture flows
- How to apply the Hormozi frameworks ($100M Offers, $100M Leads) to ETKM
- What quality gates apply before marketing content ships
- That `etkm-cta-architecture` MUST be loaded alongside this skill — always, no exceptions

---

## SECTION 2: WHEN TO LOAD

**Load for:**
- Building any marketing content (ads, emails, social posts, landing pages, blog posts, video scripts)
- Planning content calendars or campaign strategy
- Creating or auditing lead magnets and opt-in assets
- Building or reviewing email/text nurture sequences
- Packaging, pricing, or auditing any ETKM offer
- Diagnosing why a funnel stage is underperforming
- Applying Hormozi frameworks to any ETKM product or campaign

**Do NOT load for:**
- Audience-specific messaging (load etkm-audience-intelligence — it has the segment data)
- CRM pipeline or automation mechanics (load etkm-crm-operations)
- Visual design or brand standards (load etkm-brand-kit)
- Event-specific planning (check project instructions for etkm-event-planning)

**ALWAYS LOAD** `etkm-cta-architecture` whenever this skill is loaded. No exceptions.
Every marketing session involves CTA decisions — even planning and strategy sessions
shape downstream CTAs. CTA construction, language, structure, and quality gates are
governed entirely by etkm-cta-architecture. This skill determines which funnel stage
the content serves; etkm-cta-architecture determines how the ask is built. Claude does
not make a judgment call on whether to load it. If the marketing engine is on, the CTA
architecture is on.

**Load ALONGSIDE** `etkm-audience-intelligence` when producing any segment-specific
marketing content. This skill provides the framework; audience-intelligence provides
the segment data.

**Load ALONGSIDE** `etkm-content-ecosystem` for any multi-asset content production
run — blog series, email series, PDFs, topic clusters, or packages. Content ecosystem
governs production scope and depth; this skill routes the content to the correct
funnel framework.

**REFERENCE** the **Email Strategies, Principles & Tactical Playbook** (Notion → ETKM
Content System → Brand Intelligence Hub) when writing any email copy, structuring a
sequence, or making decisions about subject lines, preview text, body length, copy
formulas, CTA placement, P.S. usage, or open-loop sequencing. This skill routes to the
right sequence and funnel stage. The playbook governs the craft of writing and
structuring the emails themselves — including copywriting formulas (PAS, AIDA, BAB,
4Ps), the psychology behind subject lines and P.S. lines, open-loop technique for
sequence continuity, spacing and timing research, and current engagement benchmarks.
The playbook is brand-agnostic; apply etkm-brand-foundation and etkm-cta-architecture
on top of it for ETKM-specific voice and CTA construction.

---

## SECTION 3: DECISION LOGIC

### The ETKM Funnel — Three Stages

| Stage | Job | Audience Mindset | Success Metric |
|---|---|---|---|
| **TOFU** (Awareness) | Stop the scroll. Deliver immediate value. Make them curious. | "I didn't know about this" | Views, shares, saves, profile visits |
| **MOFU** (Consideration) | Build trust. Dismantle false beliefs. Capture contact info. | "I'm interested but not sure" | Lead capture, email opens, engagement |
| **BOFU** (Decision) | Convert. Stack the value. Remove the last objection. | "I'm almost ready" | Trial bookings, membership signups, conversion rate |

**Rule:** Every piece of content belongs to one stage. If it tries to do two stages, it does neither well.

### Task Routing — What to Query

| Task | Database to Query | What to Look For |
|---|---|---|
| "Write a social post / ad / video script" | Marketing Frameworks | Match by Funnel Stage + Type (T1-T3 for TOFU, M1-M4 for MOFU, B1-B3 for BOFU) |
| "Build a content calendar" | Marketing Frameworks | Pull the Content Calendar Framework record |
| "What kind of content should this be?" | Marketing Frameworks | Pull the Content Type x Stage Matrix record |
| "Build an offer / audit our pricing" | Offer Stack | Pull matching offer record |
| "What's included in [tier]?" | Offer Stack | Pull matching offer record, use What Is Included and Value Equation fields |
| "Build an email sequence / nurture" | Nurture Sequences | Pull matching sequence by Type (Post-Download, Pre-Visit, etc.) |
| "They downloaded the PDF, what happens next?" | Nurture Sequences | Pull Sequence A (PDF Download) |
| "They booked but haven't shown up" | Nurture Sequences | Pull Sequence C (Pre-Visit) |
| "Lead went cold" | Nurture Sequences | Pull Sequence D (Re-Engagement) |
| "Build a lead magnet" | Marketing Frameworks | Pull relevant MOFU framework + query Offer Stack for positioning context |

### The Nurture Philosophy — Three Rules

Every nurture sequence follows these rules without exception:

1. **Every touch must earn the next one.** If a message doesn't deliver value, it burns trust.
2. **The ask always comes after the value — never before it.** CTA is last, not first.
3. **One message. One job.** Never two ideas in one email. Never two CTAs. Confusion kills action.

### Offer Architecture — Hormozi Value Equation

When building or auditing any ETKM offer, apply the Value Equation:

```
            Dream Outcome × Perceived Likelihood of Achievement
Value = ─────────────────────────────────────────────────────────
            Time Delay × Effort and Sacrifice
```

**To increase value:** Increase the top (bigger outcome, higher confidence) or decrease
the bottom (faster results, less effort). The Offer Stack database has this
pre-calculated for each tier.

### Lead Generation — Core Four Channels

From Hormozi's $100M Leads framework, adapted for ETKM:

| Channel | ETKM Application | Priority |
|---|---|---|
| Warm Outreach | Personal network, current student referrals, community connections | HIGH — lowest cost, highest trust |
| Content (Free) | Social media, blog, video, lead magnets | HIGH — builds authority over time |
| Cold Outreach | Email campaigns to LE, churches, schools, employers | MEDIUM — 292 contacts across 10 segments built |
| Paid Ads | Facebook/Instagram ads targeting local segments | LOW — activate after organic machine is running |

**Scaling framework:** More → Better → New
1. **More:** Do more of what's already working
2. **Better:** Improve conversion rates on existing channels
3. **New:** Only add new channels after More and Better are maxed

### Lead Magnet Rules

Every ETKM lead magnet follows this structure:
- 5 pages: cover, pain points (×2), solutions (×2), four-step onboarding, CTA
- Built for a specific segment (not generic)
- Entry point to Sequence A (PDF Download Nurture)
- Created using etkm-pdf-pipeline for production

### Content Rules — Non-Negotiable

- TOFU: Never mention pricing. Never push for sign-ups. Give value, build curiosity.
- MOFU: Never hard sell. Tell real stories. Prove they can do this. Low-risk next step.
- BOFU: One CTA only. Value before ask. Urgency only if authentic — never manufactured.
- All stages: Student is the hero. ETKM is the guide. Internal problem drives conversion.
- **All CTAs:** Governed by `etkm-cta-architecture` (loaded automatically with this skill).
  Do not construct CTA language, structure, or slides outside of that skill's standards.

### Sequence Performance Standards

**Note on open rates (2025–2026):** Apple Mail Privacy Protection (MPP) inflates
reported open rates by pre-fetching email content regardless of whether the recipient
opens it. Roughly 40–60% of reported opens may be machine-triggered. Open rate is now
a directional signal for deliverability health, not a primary engagement KPI. Prioritize
click-through rate, click-to-open rate, conversion rate, and revenue per recipient.
Current benchmarks are maintained in the Email Strategies, Principles & Tactical Playbook
(Notion → Brand Intelligence Hub).

| Metric | Below Average | Target | Strong |
|---|---|---|---|
| Email open rate (MPP-inflated) | < 25% | 35-43% | > 45% |
| Click-through rate | < 2% | 2.5-4% | > 5% |
| Lead to trial booking | < 5% | 8-15% | > 20% |
| Trial booking to show-up | < 50% | 65-75% | > 80% |
| Trial show-up to member | < 30% | 40-60% | > 65% |

**Troubleshooting by metric:**
- Low open rate → Fix subject lines
- Good opens, low clicks → Fix the CTA (etkm-cta-architecture is already loaded)
- Good clicks, no bookings → Fix the landing page (not a sequence problem)
- Good bookings, low show-up → Fix Sequence C (pre-visit)
- Good show-up, low conversion → Fix the offer or first class experience (not a sequence problem)

---

## SECTION 4: NOTION REFERENCES

### Database 1: ETKM Marketing Frameworks
**Location:** Notion → AI Resources → Skill Reference Data
**Records:** 12

| Record Pattern | When to Query |
|---|---|
| T1, T2, T3 | Building TOFU content (social posts, reels, carousels) |
| M1, M2, M3, M4 | Building MOFU content (emails, blog posts, videos, testimonials) |
| B1, B2, B3 | Building BOFU content (offer pages, testimonial capture, pre-visit nurture) |
| Content Calendar Framework | Planning monthly content rhythm |
| Content Type x Stage Matrix | Routing any content piece to the right stage and framework |

**Key fields:** Framework Name, Funnel Stage, Type, Template Structure, Metrics to Watch, When to Use

### Database 2: ETKM Offer Stack
**Location:** Notion → AI Resources → Skill Reference Data
**Records:** 5

| Record | Price |
|---|---|
| Standard Membership | $125/mo |
| Guided Membership | $175/mo |
| Fast Track Membership | $300/mo |
| All Access Membership | $500/mo |
| Private Lessons | Per session |

**Key fields:** Offer Name, Price, What Is Included, Value Equation, Bonuses, Guarantee, Best For

### Database 3: ETKM Nurture Sequences
**Location:** Notion → AI Resources → Skill Reference Data
**Records:** 4

| Sequence | Trigger | Emails |
|---|---|---|
| A — PDF Download | Lead magnet download | 7 over 14 days |
| B — Seminar Registration | Event registration | 5 over 7 days |
| C — Pre-Visit | Trial lesson booked | 3 over 24-48 hrs |
| D — Re-Engagement | No email open in 30+ days | 3 over 7 days |

**Key fields:** Sequence Name, Trigger, Timing Pattern, Email Details, Exit Conditions, Pipeline Stage, Status

---

## SECTION 5: QUALITY GATES

Before delivering any marketing content:

- [ ] Funnel stage identified — content serves one stage only
- [ ] Correct framework queried from Notion — not improvised
- [ ] etkm-cta-architecture confirmed loaded (mandatory with this skill)
- [ ] If segment-specific: etkm-audience-intelligence loaded and segment data queried
- [ ] Internal problem addressed (for any content with a problem-solution component)
- [ ] Student is the hero, ETKM is the guide — never reversed
- [ ] CTA is singular and clear — one ask per piece
- [ ] CTA built per etkm-cta-architecture standards — not improvised
- [ ] No manufactured urgency — only authentic scarcity
- [ ] Offer details match the Offer Stack database exactly — no improvised pricing or inclusions
- [ ] Sequence timing matches the Nurture Sequences database — no improvised schedules
- [ ] Brand voice checked against etkm-brand-foundation (no prohibited vocabulary)
- [ ] No contractions in formal copy

---

## SECTION 6: CHANGELOG

- V1.4 — 2026-05-03 — Changed etkm-cta-architecture from conditional load-alongside
  to ALWAYS LOAD — mandatory whenever this skill is loaded, no exceptions. Updated
  Section 1, Section 2, Section 3 Content Rules, Section 5 Quality Gates, and
  frontmatter description to reflect mandatory CTA architecture loading. Claude no
  longer makes a judgment call on whether to load CTA architecture.
- V1.3 — 2026-05-03 — Added Email Strategies, Principles & Tactical Playbook
  reference to Section 2 (load-alongside / reference guidance). Updated Sequence
  Performance Standards with Apple MPP open-rate caveat, adjusted benchmarks to
  reflect 2025-2026 MPP-inflated reality, added note to prioritize CTR/CTOR/conversion
  over opens. Pointed benchmark maintenance to the playbook in Brand Intelligence Hub.
- V1.2 — 2026-04-26 — Added etkm-cta-architecture to load-alongside guidance.
  Updated Content Rules CTA line to defer to etkm-cta-architecture. Updated
  quality gates to require CTA built per etkm-cta-architecture. Updated
  troubleshooting table to reference etkm-cta-architecture for low-click diagnosis.
- V1.1 — 2026-04-03 — Added etkm-content-ecosystem load-alongside instruction.
- V1.0 — 2026-03-29 — Initial build.
