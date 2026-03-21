---
name: etkm-crm-doctrine
description: >
  The permanent operating doctrine for how ETKM manages every client relationship
  through Pipedrive. Load this skill any time a task involves pipeline structure,
  stage names, label behavior, client journey logic, or CRM decision-making for
  ETKM. This is the non-negotiable structural reference — Claude and Manus never
  deviate from this architecture without Nathan's explicit authorization. Trigger
  for any question about where a contact belongs, what pipeline or stage they
  should be in, what labels apply, how a student moves between pipelines, what
  fires at a promotion or re-engagement event, or anything touching the ETKM
  client lifecycle in Pipedrive. Always load alongside etkm-brand-foundation for
  any communication work and etkm-pipedrive-manus for automation mechanics.
---

# ETKM CRM Operating Doctrine

**Version:** 2.0
**Last Updated:** 2026-03-11
**Audit status:** Verified against live Pipedrive via API — all stages, labels,
and field names confirmed accurate as of this date.

---

## THE FIVE PIPELINES

| ID | Pipeline Name | Purpose |
|----|--------------|---------|
| P1 | Prospects | Convert trial interest to signed membership |
| P2 | Level 1 Students | Onboard, retain, build identity. Highest dropout risk. |
| P3 | Adv / Exp. Students | Long-term progression, retention, promotion tracking |
| P4 | At-Risk / Retention | Escalated retention + proactive financial triggers |
| P5 | Private Lessons | Personalized training consultation and delivery |

Events are NOT a pipeline. Make.com manages event sequences and deposits
warm contacts into P1 with labels applied.

---

## P1 — PROSPECTS (live stage IDs)

| Stage ID | Name | Order |
|----------|------|-------|
| 2 | Contact Made | 1 |
| 1 | Qualified | 2 |
| 3 | Free Trial Lesson | 3 — ACQ-WF-001 fires here |
| 8 | Trial Attended | 4 — Nate moves manually |
| 7 | No Show | 5 — Nate moves manually |
| 6 | Signed Up | 6 — Triggers P2 entry + ACQ-WF-002 |
| 4 | Discussed Membership Options | 7 |
| 9 | Decision Pending | 8 — Auto after 48hrs in Trial Attended |

---

## P2 — LEVEL 1 DEVELOPMENT (live stage IDs)

| Stage ID | Name | Order |
|----------|------|-------|
| 11 | Orientation | 1 |
| 12 | Foundations | 2 |
| 13 | Confidence | 3 |
| 14 | Applying Skills | 4 |
| 15 | Testing Prep | 5 |
| 16 | Earned Advancement | 6 — Yellow Belt. P2→P3 handoff. |

At-Risk trigger: 2 missed classes → create P4 deal at Stage 24 while P2 stays active.

---

## P3 — LEVELS 2-6 DEVELOPMENT (live stage IDs)

| Stage ID | Name | Order |
|----------|------|-------|
| 17 | Orientation | 1 |
| 18 | Foundation | 2 |
| 19 | Operational Capability | 3 |
| 20 | Proficiency Confirmed | 4 |
| 21 | Testing | 5 |
| 22 | Earned Advancement | 6 — Promotion loop back to Stage 17 |

At-Risk trigger: 2 weeks no attendance → create P4 deal at Stage 24 while P3 stays active.

---

## P4 — AT-RISK / RETENTION (live stage IDs)

| Stage ID | Name | Order | Notes |
|----------|------|-------|-------|
| 23 | Active Monitoring | 1 | Manual entry only. 7-day task created. No email. |
| 24 | At-Risk | 2 | Escalated from P2/P3. Email + SMS fires. |
| 25 | Intervention | 3 | Automated comms. Nate makes personal call if no response. |
| 26 | Re-Engaged | 4 | Student returned. 48hr hold → exits P4, returns to P2/P3. |
| 27 | Payment Due | 5 | Auto: Square failure → Make.com → creates deal here. |
| 29 | PIF Due | 6 | Proactive — fires BEFORE PIF period expires. |
| 28 | Alumni | 7 | Long-term nurture only. No active outreach. |

Retired: "Lapsed" does not exist. Never use this stage name or label.

---

## P5 — PRIVATE LESSONS (live stage IDs)

| Stage ID | Name | Order |
|----------|------|-------|
| 30 | Consultation | 1 |
| 31 | Orientation | 2 |
| 32 | Assessment | 3 |
| 33 | Building a Plan | 4 |
| 34 | Plan Execution | 5 |
| 35 | Advancement | 6 |

---

## DEAL LABELS — 2 Active (audited 2026-03-11)

| Label | ID | Purpose |
|-------|-----|---------|
| Not Interested | 39 | Prospect closed — not converting |
| Invalid | 44 | Bad data, spam, or duplicate |

ALL other deal labels retired. Pipeline stages handle status tracking.
Retired: Webform Leads, Lead Contacted, Engaged Lead, Meeting Scheduled,
Qualified Prospect, Qualified Lead, Free Trial Scheduled, Call Back, Lead Nurturing.

---

## PERSON LABELS — 17 Active (audited 2026-03-11)

**Student Status**
- ETKM Student (id: 30) — applied at signup, drops on departure
- Former Student (id: 34) — applied when ETKM Student drops

**Program Affiliation**
- Fight Back (id: 29) — ALL female students at enrollment, no exceptions, permanent
- Youth (id: 32)
- Armed Citizen Tactics (id: 47)
- Private Lesson (id: 31) — transient, P5 only
- Seminar Attendee (id: 33) — transient, applied by Make.com

**Audience / Segment**
- Law Enforcement (id: 28) — aligns with LE/Mil arc
- Military (id: 54) — aligns with LE/Mil arc
- Private Security (id: 51)

**Operational (Permanent)**
- Sponsor (id: 49)
- Instructor (id: 50)
- Coach (id: 56)
- School Admin (id: 57)
- Hosting Seminars (id: 55)
- Paladin Security (id: 48)

**System**
- Invalid (id: 46)

RETIRED person labels: Cold lead, Hot lead, Warm lead — replaced by ETKM Arc Type field.

---

## CUSTOM PERSON FIELDS

| Field | Key (first 20 chars) | Values |
|-------|---------------------|--------|
| ETKM Arc Type | eed887654d2c1f82908c | Safety, Parent, Fitness, LE/Mil, Former MA, Default |
| CBLTAC Enrolled Date | (duplicate — Manus resolving) | Date |
| CBLTAC Status | 95f1cd40004d4277a98d | active, complete, paused |
| Sakari Opt In | 8cae8f528afa52fd268f | Date |
| Sakari Opt Out | 624eeb304949f6989717 | Date |

Do NOT write to CBLTAC Enrolled Date until Manus confirms duplicate resolved.

---

## LABEL RULES

- Permanent labels travel through all pipelines — never drop without explicit instruction
- Multiple program affiliation labels can coexist (Fight Back + LE + ACT is valid)
- At-Risk label persists after re-engagement — intentional history marker
- Fight Back on ALL female students — no exceptions
- Cold/Warm/Hot lead labels are RETIRED — use ETKM Arc Type instead

---

## KEY TRANSITIONS

**P1 Stage 6 (Signed Up) → P2:**
Auto-create P2 deal at Stage 11. Apply: ETKM Student. Fire: ACQ-WF-002.

**P2 Stage 16 → P3 (Yellow Belt):**
Fire congratulations. ATOMIC: DROP Level 1, ADD Level 2.
Create P3 deal at Stage 17. 48hr hold. Fire "welcome to your new era."

**P3 Stage 22 → Promotion Loop:**
Fire congratulations. ATOMIC: DROP current level, ADD next level.
48hr hold. Auto-move to Stage 17. Fire "welcome to your new era."

**At-Risk P2/P3 → P4:**
Create P4 deal at Stage 24. P2/P3 deal stays active. Dual pipeline.

**Re-Engaged P4 Stage 26:**
48hr hold. Close P4 deal. Student stays in P2/P3 at same stage. At-Risk label stays.

**Payment Failure → P4:**
Square → Make.com → P4 deal at Stage 27. Payment Due label on person.
On resolution: drop label, close P4 deal.

---

## HARD RULES — NEVER VIOLATE

1. Never use "Lapsed" — retired, does not exist
2. Never use Cold/Warm/Hot lead labels — retired
3. Never change pipeline or stage names without Nathan's authorization
4. Never move a student between pipelines without a defined trigger
5. Never stack two belt level labels simultaneously
6. Never let a student carry zero belt level labels during a promotion swap
7. Never write to CBLTAC Enrolled Date until duplicate field resolved

Load etkm-pipedrive-manus for automation mechanics.
Load etkm-cowork-protocol for Cowork monitoring integration.
