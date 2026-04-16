---
name: etkm-crm-operations
version: 1.3
updated: 2026-04-15
description: >
  The routing brain for all ETKM CRM and automation work. Load this skill whenever
  building, troubleshooting, or planning any part of ETKM's Pipedrive CRM — including
  pipeline structure, stage logic, label management, deal transitions, automation
  triggers, Calendly integration, arc classification, or the Claude API connection.
  All pipeline, stage, and label data lives in the ETKM CRM Architecture database in
  Notion — this skill tells Claude how to use it. Trigger for: "Pipedrive", "pipeline",
  "deals", "stages", "labels", "automation", "n8n", "Calendly", "arc classification",
  "deal stage", "promotion", "at-risk", "re-engagement", "onboarding", "WF-001",
  "WF-002", "merge tags", "merge fields", "email triggers", "webhook", "payment due",
  "PIF", or any task touching the ETKM client lifecycle in Pipedrive. Replaces:
  etkm-crm-doctrine, etkm-pipedrive-manus, etkm-make-automation.
---

# ETKM CRM Operations

**Version:** 1.3
**Established:** 2026-03-29
**Updated:** 2026-04-15
**Replaces:** etkm-crm-doctrine, etkm-pipedrive-manus, etkm-make-automation
**Databases:** ETKM CRM Architecture, Arc/Segment/CRM Crosswalk (Notion → AI Resources → Skill Reference Data)

---

## SECTION 1: WHAT THIS SKILL DOES

This skill is the decision layer for all Pipedrive CRM and automation work. It does NOT
contain pipeline specs, stage lists, or label dictionaries. That data lives in the ETKM
CRM Architecture database in Notion (40 records: 5 pipelines + 35 stages) and the
Arc/Segment/CRM Crosswalk reference page.

This skill tells Claude:
- The rules that govern how contacts move through the ETKM lifecycle
- What triggers transitions between pipelines and stages
- What Claude is responsible for vs what automation handles
- How arc classification works
- What non-negotiable CRM rules must never be broken
- How Pipedrive merge fields work in automation emails

---

## SECTION 2: WHEN TO LOAD

**Load for:**
- Any task involving Pipedrive pipeline structure, stages, or labels
- Building or reviewing automation workflows (Pipedrive native or n8n)
- Writing email sequences that trigger from deal stage moves
- Arc classification logic or intake flow questions
- Deal transition planning (P1→P2, P2→P3, P3 promotion loop, P4 escalation)
- Label management or custom field questions
- Any question about merge fields or email personalization in Pipedrive

**Do NOT load for:**
- Writing marketing copy (load etkm-marketing-engine)
- Audience segment research (load etkm-audience-intelligence)
- Visual design (load etkm-brand-kit)
- General collaboration questions (nate-collaboration-workflow covers this)

---

## SECTION 3: PIPEDRIVE MERGE FIELDS — HOW THEY ACTUALLY WORK

**Critical — read before writing any automation email spec.**

Pipedrive automation emails do NOT use typed merge tag syntax. There is no `[field_name]`,
`{{field}}`, or `*|FIELD|*` that you type manually into the email body.

**The actual mechanism:**
When building an email inside a Pipedrive automation, there is a **"Merge fields" button**
in the email editor. You click it, select the field from a dropdown (e.g., Person First Name,
Activity Due Date, Deal Title), and Pipedrive inserts a **visual token/chip** into the email.
It displays as a styled placeholder in the editor but resolves to the actual field value
when the email sends.

**What this means for documentation:**
- Use `[person_first_name]`, `[activity_due_date]` etc. in specs and copy docs as
  **reference notation only** — so the builder knows which field to select in the UI.
- These are NOT literally typed into Pipedrive. They are UI field selections.
- When building, open the Merge fields picker and match the label to the reference notation.

**Fields available depend on the trigger type:**
- Deal trigger → gives access to Deal fields + linked Person fields
- Activity trigger → gives access to Activity fields (due date, due time, subject, type)
- Stage change trigger → gives access to Deal + Person + Activity fields

**Note on WF-001:** The transactional emails in WF-001 (booking confirmation, reminders,
reschedule, cancellation) are now owned by Calendly, which has direct access to booking
date/time data. Pipedrive merge fields are used only for the Pipedrive Sequence and
post-trial automations — which do not require date/time fields.

---

## SECTION 4: WF-001 AUTOMATION ARCHITECTURE

**Established:** 2026-04-15
**Architecture revision:** 2026-04-15 — Calendly/Pipedrive split locked

### System Architecture — Division of Responsibility

**The rule:** If an email would be wrong or broken without a specific date or time in it,
Calendly sends it. If the email works regardless of the exact date, Pipedrive sends it.

| Owner | Handles | Why |
|---|---|---|
| Calendly | Transactional emails requiring live booking data | Has the date/time, confirmation #, and reschedule/cancel events |
| Pipedrive Sequence | Relationship emails — value-first, no dates needed | Stage-aware, voice-heavy, fires on deal creation |
| Pipedrive Automations | Post-trial follow-up — stage-triggered, no dates | Driven by what happened at the visit, not when it was |

---

### Calendly Owns — Transactional Emails (5)

These fire from Calendly's own workflow automation. They are on-brand voice but
fundamentally transactional. Calendly sends them because it holds the live booking data.

| Email | Trigger | Purpose |
|---|---|---|
| Booking Confirmation | Booking created | Logistics + date/time/location + what to expect |
| 24-Hour Reminder | 24 hours before event | Confirm attendance, logistics reinforcement |
| Morning-Of Reminder | Day of event (morning) | Final prep, confidence builder |
| Reschedule Confirmation | Booking rescheduled | Acknowledge new date/time, maintain relationship |
| Cancellation Acknowledgment | Booking cancelled | Acknowledge, soft recovery, leave door open |

**Build sequence:** Write copy → Nathan approves → load into Calendly workflow automation.
No Pipedrive involvement for these five emails.

---

### Pipedrive Sequence Owns — Relationship Emails (2)

These fire from the Pipedrive native Sequence feature, triggered on deal creation.
No specific date/time required — they work regardless of when the trial is scheduled.

| Email | Day | Trigger | Purpose |
|---|---|---|---|
| PDF + Welcome | Day 0 | Deal creation (P1-S3) | Deliver lead magnet, set expectations, build identity |
| Pre-Class Nurture | Day 1–2 | Sequence delay | Address objections ("What if I can't keep up?") |

**Arc classification applies here in Phase 2.** In Phase 1, all leads receive the same
sequence. Arc-specific variants are written and ready but inactive until Phase 2.

**Trigger source:** Calendly → Pipedrive native integration creates Deal + Person record.
Deal enters P1-S3 (Free Trial Booked). Sequence fires on deal creation.

---

### Pipedrive Automations Own — Post-Trial (3)

These are stage-triggered automations. No dates needed. They respond to what happened
at the trial visit, not when it was.

| Automation | Trigger | Purpose |
|---|---|---|
| Trial Attended Follow-Up | Deal moves to P1-S4 (Attended) | Strike while warm — next step, enrollment offer |
| No-Show Recovery | Deal moves to P1-S5 (No Show) | Re-engage, lower barrier, second chance |
| Needs More Time Nurture | Deal stage or label condition | Long-burn nurture for the undecided |

These automations run from Pipedrive native. Voice-driven. No merge field date/time
references required.

---

### Phase 2 — Arc Classification (Future)

When ready:
1. Build n8n workflow: reads Calendly Q&A note → calls Claude API → writes ETKM Arc
   Type field to Pipedrive Person record
2. Activate arc variant logic in Pipedrive Sequence for Day 0 and Day 1–2 emails
3. All arc variant copy already exists in WF-001 docs — no rewrite needed

**Arc signal map, variant copy, and classification prompt live in:**
WF-001 Implementation Guide (Google Drive / AI Resources)

---

### Open Items — WF-001

| ID | Item | Blocks |
|---|---|---|
| D-02 | Google Drive PDF link for "Before You Walk In" | Pipedrive Sequence Day 0 email — insert when Nathan provides |
| T-01 | Confirm Calendly→Pipedrive integration fires on booking | Deal creation trigger for Pipedrive Sequence |
| T-02 | Test Calendly reschedule/cancellation events | Confirm Calendly fires those workflow emails correctly |
| T-03 | Test post-trial automations fire on stage move | P1-S4 (Attended) and P1-S5 (No Show) triggers |

---

## SECTION 5: DECISION LOGIC

### The Client Lifecycle — Five Words

**Prospect → Develop → Progress → Retain → Specialize**

| Pipeline | Who Lives Here | Purpose |
|---|---|---|
| P1 — Prospects | Pre-enrollment contacts | Convert trial interest to signed membership |
| P2 — Level 1 Students | Yellow Belt, first 90 days | Onboard, retain, build identity (highest dropout risk) |
| P3 — Adv / Exp. Students | Orange through Black Belt Prep | Long-term progression, retention, promotion tracking |
| P4 — At Risk / Retention | Escalated cases from P2/P3 | Deeper intervention when at-risk response fails |
| P5 — Private Lesson | Private lesson clients | Personalized consultation and delivery |

For full stage details, query the ETKM CRM Architecture database filtered by Type = "Stage" and the relevant Parent pipeline.

### Key Transition Events

**P1 → P2 (Signed Up):**
1. Deal moves to P1-S6 (Signed Up)
2. n8n webhook fires — auto-create P2 deal at Stage 1 (Orientation)
3. Apply: ETKM Student + Level 1
4. Drop: all temperature labels
5. Fire: WF-002 onboarding sequence

**P2 → P3 (Earned Advancement — Yellow Belt):**
1. Nathan moves to P2-S7 (Earned Advancement)
2. Congratulations email fires immediately
3. ATOMIC label swap: DROP Level 1, ADD Level 2
4. Create P3 deal at Stage 7 (Earned Advancement)
5. 48-hour celebration hold
6. Auto-move P3 deal to Stage 1 (Orientation)
7. "Welcome to your new era" email fires

**P3 Promotion Loop (every belt level):**
1. Nathan moves to P3-S7 (Earned Advancement)
2. Congratulations email fires immediately
3. ATOMIC: DROP current level, ADD next level
4. 48-hour hold
5. Auto-move to Stage 1 (Orientation) at new level

**At-Risk Escalation (P2/P3 → P4):**
1. At-Risk stage triggers in P2 or P3 with no re-engagement within window
2. Create P4 deal at Stage 2 (At-Risk)
3. Student remains active in P2/P3 — dual pipeline
4. P2 window: 14 days. P3 window: 30 days.

**Re-Engagement from P4:**
1. Student returns → P4 deal moves to Stage 4 (Re-Engaged)
2. 48-hour hold
3. P4 deal closes, student returns to P2/P3 at same stage they left
4. At-Risk label stays permanently

### Non-Negotiable CRM Rules

These rules override everything. Claude and automation never deviate without Nathan's explicit authorization.

**Labels:**
- Permanent labels (Fight Back, LE, ACT, Private Security, Instructor, Coach, Sponsor, School Admin, Paladin) travel through all pipelines. Never drop unless explicitly instructed.
- Transient labels reflect current status only. One Temperature label at a time. One Belt Level at a time.
- Belt level swap is ATOMIC. DROP old + ADD new in the same step. Never a gap where a student carries zero belt labels.
- At-Risk label persists after re-engagement. It is a permanent history marker.
- Fight Back applies to ALL female students at enrollment. No exceptions. Lifetime.
- Arc labels are mutually exclusive within their category. One arc at a time. Assigned at classification, persist through P1.
- Multiple Program Affiliation labels can coexist (Fight Back + LE + ACT simultaneously).

**Pipelines:**
- Events are NOT a pipeline. Events managed by n8n. Warm contacts deposited into P1 with labels applied.
- Students can be in P2/P3 and P4 simultaneously (development pipeline + retention intervention).
- P5 can run alongside P2 or P3 (private lessons + group membership).
- "Lapsed" does not exist. Retired in v1.2. Students move to Alumni, not Lapsed.

**Automation:**
- Web form leads create a Person record only — no Deal until Calendly booking.
- Group Inquiry field (Yes/No, deal-level) must be checked by all automated email sequences. Exclude deals where Group Inquiry = Yes.
- Do not modify the Calendly intake flow during active build phases without Nathan's authorization.
- All automation runs through Calendly (transactional), Pipedrive native (sequences + post-trial), or n8n (webhooks + arc classification). Make.com is fully deprecated.
- Manus is no longer involved in WF-001. Pipedrive native and Calendly handle WF-001 entirely.

### Arc Classification

Arc labels are applied at prospect entry based on the interest dropdown (web form) or
Calendly Q&A keyword match (n8n receives Calendly webhook, calls Claude API for classification).

For the full arc-to-segment-to-label mapping, reference the Arc/Segment/CRM Crosswalk
in Notion. Key facts:

- 6 deal-level arcs: Default, Parent, Safety, LE/Mil, Former MA, Fitness (+ 4 pending: Private Security, High School, Armed Citizen, College Student)
- 10 person-level arcs: All 6 above + Private Security, High School, Armed Citizen, College Student
- 22 behavioral/classification labels (IDs 100-121): These are NOT arcs. They are flags from intake classification.
- Person records carry more granular arc data than deals.
- Phase 1 of WF-001 does not use arc classification. All leads receive Default arc until Phase 2 is activated.

### Claude vs Automation — Division of CRM Work

| Claude | Calendly / Pipedrive / n8n |
|---|---|
| Write all email copy for sequences | Execute sends via Calendly workflow or Pipedrive native |
| Design pipeline/stage/label architecture | Create pipelines/stages/labels in Pipedrive |
| Write arc classification prompts | Deploy classification via n8n + Claude API |
| Produce automation specs and trigger logic | Build automations implementing the spec |
| All API prompt design | All webhook workflows (n8n) |
| Never implements automation directly | Never rewrites Claude's copy or classification logic |

### Three-Question Filter for CRM Fields

Before adding any new field to Pipedrive:
1. How do we want to use this?
2. How is it best used in the CRM?
3. How can we import data that will be an asset, not a liability?

---

## SECTION 6: NOTION REFERENCES

### Database: ETKM CRM Architecture
**Location:** Notion → AI Resources → Skill Reference Data
**Records:** 40 (5 pipelines + 35 stages)

**How to query:**
- For pipeline overview: filter by Type = "Pipeline"
- For stages in a specific pipeline: filter by Type = "Stage" AND Parent = "[pipeline name]"
- For labels: reference the Arc/Segment/CRM Crosswalk page (same Notion location)

**Key fields:** Item Name, Type (Pipeline/Stage/Deal Label/Person Label/Custom Field/Automation/Arc Label), Parent, Pipedrive ID, Purpose, Trigger, Exit Condition, Automation, Level (Deal/Person/System), Notes

### Reference Page: Arc / Segment / CRM Label Crosswalk V1.0
**Location:** Notion → AI Resources → Skill Reference Data

Contains:
- Deal-level arc labels with Pipedrive IDs
- Person-level arc labels with Pipedrive IDs
- Behavioral/classification labels (IDs 100-121) with action implications
- Person-type labels (IDs 28-57) with purposes
- Mapping between audience segments, arcs, and CRM labels
- Sync rule for keeping all three systems aligned

---

## SECTION 7: QUALITY GATES

Before delivering any CRM-related work:

- [ ] Pipeline names, stage names, and label names match Notion exactly — no drift
- [ ] Transition logic matches documented rules — no improvised stage moves
- [ ] ATOMIC label swaps specified where required (belt promotions)
- [ ] At-Risk label persistence rule respected (never removed after re-engagement)
- [ ] "Lapsed" not used anywhere — Alumni only
- [ ] Fight Back applied to all female students at enrollment
- [ ] Arc labels are mutually exclusive — only one active
- [ ] Group Inquiry field check included in any automated sequence
- [ ] No pipeline structure, stage name, or arc label invented without Nathan's authorization
- [ ] No Make.com references in any new automation spec — n8n only
- [ ] Pipedrive automation email specs use reference notation for merge fields (not typed syntax)
- [ ] WF-001 transactional emails (booking confirm, reminders, reschedule, cancellation) are specified for Calendly — not Pipedrive
- [ ] WF-001 Pipedrive Sequence scope is Day 0 (PDF+welcome) + Day 1-2 (pre-class nurture) only

---

## SECTION 8: CHANGELOG

- V1.3 — 2026-04-15 — WF-001 architecture updated to Calendly/Pipedrive split. Section 4 rewritten: Calendly owns 5 transactional emails (booking confirm, 24hr/morning reminders, reschedule, cancellation); Pipedrive Sequence owns Day 0 PDF+welcome + Day 1-2 pre-class nurture; Pipedrive Automations own post-trial (Attended, No-Show, Needs More Time). Section 3 WF-001 merge field note updated to reflect Calendly ownership of date/time emails. Automation non-negotiable rule updated (Calendly added). Claude vs Automation table updated. Two new quality gates added. Open items tracker updated.
- V1.2 — 2026-04-15 — Added Section 3: Pipedrive Merge Fields. Added Section 4: WF-001 Automation Architecture (Phase 1 skeleton — Pipedrive native). Manus deprecated from WF-001.
- V1.1 — 2026-04-01 — Make.com fully removed. All automation references updated to n8n.
- V1.0 — 2026-03-29 — Initial build. Replaces etkm-crm-doctrine, etkm-pipedrive-manus, etkm-make-automation.
