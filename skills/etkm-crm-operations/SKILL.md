---
name: etkm-crm-operations
version: 1.0
updated: 2026-03-29
description: >
  The routing brain for all ETKM CRM and automation work. Load this skill whenever
  building, troubleshooting, or planning any part of ETKM's Pipedrive CRM — including
  pipeline structure, stage logic, label management, deal transitions, automation
  triggers, Make.com scenarios, Calendly integration, arc classification, or the
  Claude-Manus API connection. All pipeline, stage, and label data lives in the ETKM
  CRM Architecture database in Notion — this skill tells Claude how to use it. Trigger
  for: "Pipedrive", "pipeline", "deals", "stages", "labels", "automation", "Make.com",
  "Calendly", "arc classification", "deal stage", "promotion", "at-risk", "re-engagement",
  "onboarding", "WF-001", "WF-002", "merge tags", "email triggers", "webhook", "payment
  due", "PIF", or any task touching the ETKM client lifecycle in Pipedrive. Replaces:
  etkm-crm-doctrine, etkm-pipedrive-manus, etkm-make-automation.
---

# ETKM CRM Operations

**Version:** 1.0
**Established:** 2026-03-29
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
- What Claude is responsible for vs what Manus handles
- How arc classification works
- What non-negotiable CRM rules must never be broken

---

## SECTION 2: WHEN TO LOAD

**Load for:**
- Any task involving Pipedrive pipeline structure, stages, or labels
- Building or reviewing automation workflows (Make.com scenarios)
- Writing email sequences that trigger from deal stage moves
- Arc classification logic or intake flow questions
- Deal transition planning (P1→P2, P2→P3, P3 promotion loop, P4 escalation)
- Label management or custom field questions
- Manus handoff briefs involving Pipedrive or Make.com

**Do NOT load for:**
- Writing marketing copy (load etkm-marketing-engine)
- Audience segment research (load etkm-audience-intelligence)
- Visual design (load etkm-brand-kit)
- General collaboration questions (nate-collaboration-workflow covers this)

---

## SECTION 3: DECISION LOGIC

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
2. Auto-create P2 deal at Stage 1 (Orientation)
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

These rules override everything. Claude and Manus never deviate without Nathan's explicit authorization.

**Labels:**
- Permanent labels (Fight Back, LE, ACT, Private Security, Instructor, Coach, Sponsor, School Admin, Paladin) travel through all pipelines. Never drop unless explicitly instructed.
- Transient labels reflect current status only. One Temperature label at a time. One Belt Level at a time.
- Belt level swap is ATOMIC. DROP old + ADD new in the same step. Never a gap where a student carries zero belt labels.
- At-Risk label persists after re-engagement. It is a permanent history marker.
- Fight Back applies to ALL female students at enrollment. No exceptions. Lifetime.
- Arc labels are mutually exclusive within their category. One arc at a time. Assigned at classification, persist through P1.
- Multiple Program Affiliation labels can coexist (Fight Back + LE + ACT simultaneously).

**Pipelines:**
- Events are NOT a pipeline. Events managed by Make.com. Warm contacts deposited into P1 with labels applied.
- Students can be in P2/P3 and P4 simultaneously (development pipeline + retention intervention).
- P5 can run alongside P2 or P3 (private lessons + group membership).
- "Lapsed" does not exist. Retired in v1.2. Students move to Alumni, not Lapsed.

**Automation:**
- Web form leads create a Person record only — no Deal until Calendly booking.
- Group Inquiry field (Yes/No, deal-level) must be checked by all automated email sequences. Exclude deals where Group Inquiry = Yes.
- Do not modify the Calendly intake flow during active build phases without Nathan's authorization.

### Arc Classification

Arc labels are applied at prospect entry based on the interest dropdown (web form) or
Calendly Q&A keyword match (Manus reads response, calls Claude API for classification).

For the full arc-to-segment-to-label mapping, reference the Arc/Segment/CRM Crosswalk
in Notion. Key facts:

- 6 deal-level arcs: Default, Parent, Safety, LE/Mil, Former MA, Fitness (+ 4 pending: Private Security, High School, Armed Citizen, College Student)
- 10 person-level arcs: All 6 above + Private Security, High School, Armed Citizen, College Student
- 22 behavioral/classification labels (IDs 100-121): These are NOT arcs. They are flags from intake classification.
- Person records carry more granular arc data than deals.

### Claude vs Manus — Division of CRM Work

| Claude | Manus |
|---|---|
| Write all email copy for sequences | Implement sequences in Pipedrive/Make.com |
| Design pipeline/stage/label architecture | Create pipelines/stages/labels in Pipedrive |
| Write arc classification prompts | Deploy classification via API/webhook |
| Produce handoff briefs for any CRM change | Execute handoff briefs exactly as written |
| Define automation logic and trigger rules | Build Make.com scenarios implementing the logic |
| All API prompt design | All browser automation and deployment |
| Never implements automation directly | Never rewrites Claude's copy or classification logic |

### Three-Question Filter for CRM Fields

Before adding any new field to Pipedrive:
1. How do we want to use this?
2. How is it best used in the CRM?
3. How can we import data that will be an asset, not a liability?

---

## SECTION 4: NOTION REFERENCES

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

## SECTION 5: QUALITY GATES

Before delivering any CRM-related work:

- [ ] Pipeline names, stage names, and label names match Notion exactly — no drift
- [ ] Transition logic matches documented rules — no improvised stage moves
- [ ] ATOMIC label swaps specified where required (belt promotions)
- [ ] At-Risk label persistence rule respected (never removed after re-engagement)
- [ ] "Lapsed" not used anywhere — Alumni only
- [ ] Fight Back applied to all female students at enrollment
- [ ] Arc labels are mutually exclusive — only one active
- [ ] Group Inquiry field check included in any automated sequence
- [ ] Manus handoff follows governance skill format (if applicable)
- [ ] No pipeline structure, stage name, or arc label invented without Nathan's authorization

---

## SECTION 6: CHANGELOG

- V1.0 — 2026-03-29 — Initial build. Replaces etkm-crm-doctrine (v1.4), etkm-pipedrive-manus, etkm-make-automation. Pipeline and stage data migrated to ETKM CRM Architecture database in Notion (40 records). Label mapping in Arc/Segment/CRM Crosswalk reference page. Skill contains lifecycle rules, transition logic, non-negotiable CRM rules, classification routing, and Claude/Manus division only.
