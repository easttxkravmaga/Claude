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

**Version:** 1.4
**Last Updated:** 2026-03-27

This is the permanent structural reference for how ETKM manages client
relationships in Pipedrive. It governs every pipeline, stage, label, and
transition in the system. Claude and Manus treat this as fixed architecture.
Nothing changes without Nathan's explicit authorization.

---

## WHY THIS STRUCTURE EXISTS

ETKM manages people at fundamentally different stages of their journey —
a first-time prospect, a brand-new Yellow Belt student, a 3-year Blue Belt,
and a lapsed member all need different communication, different tracking, and
different responses from the system. A single pipeline cannot do this well.

The multi-pipeline architecture gives every person a home that reflects where
they actually are. It prevents people from falling through the cracks, ensures
the right communication fires at the right moment, and gives the CRM the same
intentionality as the training program itself.

**The complete client lifecycle in five words:**
Prospect → Develop → Progress → Retain → Specialize

---

## THE FIVE PIPELINES

| ID | Pipeline Name | Who Lives Here | Purpose |
|----|--------------|----------------|---------|
| P1 | Prospects | Pre-enrollment contacts | Convert trial interest to signed membership |
| P2 | Level 1 Students | Yellow Belt students, first 90 days | Onboard, retain, build identity. Highest dropout risk. |
| P3 | Adv / Exp. Students | Orange through Black Belt Prep | Long-term progression, retention, promotion tracking |
| P4 | At Risk / Retention | Escalated retention cases from P2 or P3 | Deeper intervention when P2/P3 at-risk response fails |
| P5 | Private Lesson | Private lesson clients | Personalized training consultation and delivery |

**Note on Events:** Events are NOT a Pipedrive pipeline. Events are managed
entirely by Make.com. Make runs the email sequence and deposits warm contacts
into P1 with labels already applied when ready to pursue.

**Note on Intake Form:** The Calendly intake flow landing point will be updated
to align with P1 — Prospects after the current build is complete. This is a
separate task. Do not modify the intake flow during the pipeline build.

---

## PIPELINE 1 — PROSPECTS

| Stage | Name | Notes |
|-------|------|-------|
| 1 | Contact Made | First contact established. |
| 2 | Qualified | Prospect vetted and confirmed as viable. |
| 3 | Free Trial Lesson | Calendly confirmed. WF-001 fires. |
| 4 | Trial Attended | Nate manually moves after attendance confirmed. |
| 5 | No Show | Prospect did not attend scheduled trial. |
| 6 | Signed Up | Conversion confirmed. Triggers P2 entry. |
| 7 | Discussed Membership Options | Post-trial membership conversation happened. |
| 8 | Decision Pending | Prospect is considering — awaiting decision. |

**Handoff:** Stage 6 → auto-creates P2 deal. Applies ETKM Student + Level 1.
Drops all temperature labels.

---

## PIPELINE 2 — LEVEL 1 DEVELOPMENT

| Stage | Name | Meaning |
|-------|------|---------|
| 1 | Orientation | Enter the ETKM community |
| 2 | Foundations | Build core skills |
| 3 | Confidence | Develop comfort and coordination |
| 4 | Applying Skills | Use techniques in realistic drills |
| 5 | Testing Prep | Refine and review the material |
| 6 | At-Risk | Attendance dropped — first internal flag. NOT escalation to P4 yet. |
| 7 | Earned Advancement | Yellow Belt passed. P2→P3 handoff stage. |

**At-Risk in P2:** Triggers when student misses 2 consecutive classes.
Check-in email fires. If no re-engagement in 14 days → escalate to P4.
Student can be active in P2 and P4 simultaneously.

**Handoff:** Stage 7 → 48-hour celebration hold → auto-creates P3 deal.
Atomic label swap: DROP Level 1, ADD Level 2. Same step, no gap.

---

## PIPELINE 3 — LEVELS 2-6 DEVELOPMENT

Belt level is tracked via labels (Level 2–6), not via separate stages or pipelines.
One stage set serves all belt levels. The promotion loop (Stage 7 → Stage 1)
repeats at every level.

| Stage | Name | Meaning |
|-------|------|---------|
| 1 | Orientation | Understand the mission of the level |
| 2 | Foundation | Build the mechanics and structure |
| 3 | Operational Capability | Apply techniques in realistic situations |
| 4 | Proficiency Confirmed | Demonstrate consistent performance |
| 5 | Testing | Perform under evaluation and pressure |
| 6 | At-Risk | Attendance dropped — first internal flag within P3. |
| 7 | Earned Advancement | Test passed. Label swap. 48hr hold, return to Stage 1. |

**At-Risk in P3:** Triggers when student has no attendance for 2 weeks.
Check-in email fires. If no re-engagement in 30 days → escalate to P4.
Student can be active in P3 and P4 simultaneously.

**Promotion loop:** Stage 7 (Earned Advancement) → ATOMIC label swap
(DROP current level, ADD next level, same step) → 48-hour hold →
auto-move to Stage 1 (Orientation) at new level → "welcome to your new era"
email fires.

---

## PIPELINE 4 — AT RISK / RETENTION

Receives escalations from P2 and P3 when At-Risk response fails.
Student remains active in their development pipeline simultaneously.
Also handles proactive financial triggers (PIF and Payment Due).

| Stage | Name | What Happens |
|-------|------|--------------|
| 1 | Active Monitoring | Nate's gut feel — manual entry only. System creates 7-day follow-up task. No email fires. |
| 2 | At-Risk | Formal flag. Escalated from P2/P3. Email + SMS fires. Nate task created. |
| 3 | Intervention | Automated email/SMS delivered. Nate task: make personal call if no response within window. Human-action stage. |
| 4 | Re-Engaged | Student returned. 48-hour hold. After 48hrs, exits P4, returns to development pipeline at same stage they left. |
| 5 | PIF Due | Proactive trigger — fires BEFORE PIF period expires. Communication: appreciative, forward-looking tone. On renewal: drop PIF Due stage, student returns to P2/P3 uninterrupted. |
| 6 | Payment Due | Reactive trigger — Square payment failure fires Make scenario, creates P4 deal at this stage. Payment Due label applied. On resolution: drop label, close P4 deal, student returns to development pipeline. |
| 7 | Alumni | Re-engagement window closed. Long-term nurture only. No active outreach. |

**Retired stage:** "Lapsed" does not exist in the active system. Do not
use this label or stage name. It was retired in v1.2. Students who do
not respond to intervention move directly to Alumni.

**Critical rule:** At-Risk label persists after re-engagement. It is a
permanent history marker. A student who carries the At-Risk label and goes
quiet again is flagged faster — lower threshold, quicker escalation.

**PIF label:** Permanent Financial Status label. Visible across P2 and P3.
Stays as long as the PIF arrangement continues. PIF Due stage in P4 is
the proactive trigger — it fires before the period ends, not after.

**Payment Due label:** Transient Student Status label. Applied when Square
payment fails. Removed when payment is resolved. Student's training is
not interrupted during this process.

**Returning from P4:** Student exits at Stage 4 (Re-Engaged), returns to
P2 or P3 at the same stage they left. The At-Risk label stays.

---

## PIPELINE 5 — PRIVATE LESSON

| Stage | Name | Meaning |
|-------|------|---------|
| 1 | Consultation | Discuss goals and needs |
| 2 | Orientation | Explain training structure and expectations |
| 3 | Assessment | Evaluate skill level and specific needs |
| 4 | Building a Plan | Develop personalized training plan |
| 5 | Plan Execution | Conduct private training sessions |
| 6 | Advancement | Transition to group classes or build new plan |

---

## THE 33 LABELS

Full definitions in: ETKM_Pipedrive_Label_Reference_v1.1.docx

### Label Categories

**Temperature (Transient — mutually exclusive, one at a time)**
Cold Lead | Warm Lead | Hot Lead

**Student Status (Transient)**
ETKM Student | Former Student | At-Risk | Payment Due | Alumni

**Financial Status (Permanent while active)**
PIF

**Retired Labels — Do Not Use**
Lapsed (retired v1.2 — does not exist in the active system)

**Belt Level (Transient — mutually exclusive, one at a time)**
Level 1 | Level 2 | Level 3 | Level 4 | Level 5 | Level 6

**Arc Classification (Single-select within category — assigned at classification, persists through prospect phase)**
Arc: Default | Arc: Safety | Arc: Parent | Arc: Fitness | Arc: LE/Mil | Arc: Former MA

Arc labels are applied when a prospect enters the system. Web form leads
are classified by the interest dropdown value. Calendly leads are classified
by Manus reading the Q&A response and matching keyword signals. Arc labels
persist through the entire P1 prospect journey. They are not modified after
initial classification unless Nate explicitly reclassifies. Only one Arc
label active at a time — they are mutually exclusive within the Arc category.

**Role (Permanent)**
Instructor | Coach | School Admin | Sponsor

**Program Affiliation (Permanent except Private Lesson)**
Fight Back | Youth | Private Lesson (Transient) | Armed Citizen Tactics |
Law Enforcement | Private Security

**Partner & Event (Mixed)**
Seminar Attendee (Transient — applied by Make.com) |
Hosting Seminar (Transient) | Paladin Security (Permanent)

---

## CUSTOM FIELDS

**Group Inquiry** (Deal-level, Single option: Yes / No)
Applied when a web form submission has interest = group. Provides a durable
system marker for any automation to filter on. Any automated email sequence
must check this field and exclude deals where Group Inquiry = Yes. This field
is set by the Make.com web form scenario and is not manually managed.

---

## LABEL RULES — Non-Negotiable

**Permanent labels travel through all pipelines.**
Fight Back, Law Enforcement, Armed Citizen Tactics, Private Security, Instructor,
Coach, Sponsor, School Admin, Paladin Security — these never drop unless a
specific condition explicitly removes them. They apply in P1, P2, P3, P4, P5.

**Transient labels reflect current status only.**
Only one Temperature label active at a time. Only one Belt Level label active
at a time. Drop the old one when the new one is applied.

**Belt level swap is atomic.**
On promotion: DROP old level AND ADD new level in the same automation step.
There must never be a window where a student carries no level label.

**At-Risk label persists after re-engagement.**
This is intentional. It marks history, not just current status.

**Fight Back applies to ALL female students at enrollment.**
No exceptions. It stays for the life of membership.

**Multiple Program Affiliation labels can coexist.**
A student can carry Fight Back + Law Enforcement + Armed Citizen Tactics
simultaneously. These are not mutually exclusive.

**Arc labels are mutually exclusive within their category.**
Only one Arc label active at a time. Arc is assigned at classification
(web form interest field or Calendly Q&A keyword match) and persists
through the P1 prospect phase. Do not modify Arc classification after
initial assignment unless Nate explicitly reclassifies. Arc labels
coexist with all other label categories — a prospect can carry
Warm Lead + Arc: Parent + Fight Back simultaneously.

---

## KEY TRANSITION EVENTS

### P1 → P2 (Signed Up)
1. Nate moves deal to Stage 6 (Signed Up) in P1
2. Auto-create deal in P2 Stage 1 (Orientation)
3. Apply: ETKM Student, Level 1
4. Drop: all temperature labels
5. Fire: WF-002 onboarding sequence

### P2 → P3 (Earned Advancement — Yellow Belt)
1. Nate moves to Stage 7 (Earned Advancement) in P2
2. Fire: congratulations email immediately
3. ATOMIC: DROP Level 1, ADD Level 2
4. Create deal in P3 Stage 7 (Earned Advancement)
5. 48-hour hold
6. Auto-move P3 deal to Stage 1 (Orientation)
7. Fire: "welcome to your new era" email

### P3 Belt Promotion Loop
1. Nate moves to Stage 7 (Earned Advancement)
2. Fire: congratulations email immediately
3. ATOMIC: DROP current level, ADD next level
4. 48-hour hold
5. Auto-move to Stage 1 (Orientation) at new level
6. Fire: "welcome to your new era" email

### At-Risk Escalation (P2 or P3 → P4)
1. At-Risk stage in P2 or P3 produces no re-engagement within window
2. Create deal in P4 Stage 2 (At-Risk)
3. Student remains active in P2 or P3 at same stage — dual pipeline
4. At-Risk label already applied from P2/P3 trigger

### Re-Engagement from P4
1. Student returns — move P4 deal to Stage 4 (Re-Engaged)
2. 48-hour hold
3. P4 deal closes, student remains in P2 or P3 at same stage they left
4. At-Risk label stays permanently

---

## WHAT CLAUDE AND MANUS NEVER DO

- Change pipeline names, stage names, or label names without Nathan's authorization
- Apply the retired "Lapsed" label — it does not exist in the active system
- Move a student between pipelines without a defined trigger event
- Remove a permanent label without explicit instruction
- Stack two temperature labels simultaneously
- Stack two belt level labels simultaneously
- Stack two Arc labels simultaneously
- Let a student carry zero belt level labels at any point
- Modify Arc classification after initial assignment without Nate's explicit instruction
- Modify the Calendly intake flow during the current build phase
- Rebuild this structure from scratch — changes are amendments, not replacements

---

## REFERENCE DOCUMENTS

| Document | Purpose |
|----------|---------|
| ETKM_Pipedrive_Label_Reference_v1.2.docx | Full label dictionary — updated with PIF, Payment Due, retired Lapsed |
| ETKM_Manus_Pipedrive_Phase_Build_v1.2.docx | Updated phased build instructions including revised P4 |
| etkm-pipedrive-manus skill | Automation mechanics, merge tags, API call structure, email sequence map |
| etkm-workflow-registry skill | Active workflow status, open dependencies, build sequence |
