---
name: etkm-workflow-registry
description: >
  Use this skill at the start of ANY session involving building, modifying,
  reviewing, or deploying any part of the ETKM system. Prevents duplicate
  work, enforces role boundaries between Claude and Manus, and governs all
  handoffs. Trigger whenever the user is working on any ETKM workflow,
  automation, email sequence, Pipedrive setup, content system, or platform.
  Also trigger when asking what has already been built, or for any
  coordination question between Claude, Manus, Cowork, or Claude Code.
  Trigger phrases include "what's been built", "don't want to duplicate",
  "what's the status of", "is this already done", "before we start building",
  "check the registry", "workflow status", "what does Manus have", "handoff
  to Manus", "ready to deploy", "where did we leave off", "what's next".
---

# ETKM Workflow Registry

**Version:** 3.0
**Last Updated:** 2026-03-11

---

## ID FORMAT

Every workflow uses the permanent PROJECT-WF-### format.

```
[PROJECT CODE]-WF-[###]
```

| Code | Project | Scope |
|------|---------|-------|
| ACQ | Student Acquisition | Stranger → signed student |
| RET | Retention & Advancement | Keep and advance current students |
| EVT | Events | All event campaigns |
| CNT | Content | Blog, social, email content systems |
| OPS | Operations | Internal tools, skills, infrastructure |
| TRN | Training Program | Curriculum, checklists, definitions |

Next available numbers: ACQ-019 | RET-020 | EVT-021 | CNT-022 | OPS-023 | TRN-024

---

## ROLE DIVISION — NON-NEGOTIABLE

| Role | Owner | Rule |
|------|-------|------|
| All copy | Claude | Write it, own it, lock it |
| All automation | Manus | Build it, run it, never rewrite copy |
| Scripts + APIs | Claude Code | Build it, test it, document it |
| Background monitoring | Cowork | Watch folders, detect receipts, alert Nathan |
| Status updates | Nathan | Nathan moves status; systems only read it |

If copy needs to change → goes back to Claude.
If automation logic needs to change → Manus handles it.
If a script or API build is needed → Claude Code handles it.
These lanes do not cross.

---

## STATUS LEGEND

| Status | Meaning | Action |
|--------|---------|--------|
| ✅ LIVE | Deployed and running | Read only — flag changes to Nathan |
| ✅ APPROVED | Written and approved, not yet deployed | Deliver to executing AI |
| ⏳ PENDING | Ready for executing AI to load/deploy | Deliver brief, await receipt |
| 🔵 DRAFT | In progress | Continue from where it stopped |
| 🔴 BLOCKED | Waiting on dependency | Identify blocker, report to Nathan |
| ❌ RETIRED | Deprecated | Do not use or reference |

---

## WORKFLOW REGISTRY

### ACQ — STUDENT ACQUISITION

| ID | Workflow | Status | Notes |
|----|---------|--------|-------|
| ACQ-WF-001 | Pre-Trial Email Funnel (6 arcs × 8 emails) | ✅ LIVE | Arc classified by Claude API via Railway endpoint |
| ACQ-WF-002 | 90-Day Onboarding Sequence (28 emails) | ⏳ PENDING MANUS | Brief at docs/WF-002-Manus-Deploy-Brief.md |
| ACQ-WF-007 | Sales Communication System | ✅ LIVE | Advisor-model guides, objection responses |
| ACQ-WF-011 | First-Touch Landing Page + PDF Lead Magnet | ✅ APPROVED | "Protect What Matters" — Drive hosted |
| ACQ-WF-016 | Student Intake Form + CRM Backend | ⏳ BUILT | Multi-step HTML form + Pipedrive backend |
| ACQ-WF-018 | Free Trial Landing Page Rewrite | ✅ APPROVED | StoryBrand copy — WordPress implementation pending |

### RET — RETENTION & ADVANCEMENT

| ID | Workflow | Status | Notes |
|----|---------|--------|-------|
| RET-WF-004 | 52-Week PEACE Social Calendar | ✅ LIVE | Nathan posts manually |
| RET-WF-005 | March Monthly/Weekly Themes | ✅ LIVE | Distance Management focus |

### EVT — EVENTS

| ID | Workflow | Status | Notes |
|----|---------|--------|-------|
| EVT-WF-003 | CBLTAC Event Campaign (10 emails) | ✅ LIVE | April 24-25 2026. John Wilson. |

### CNT — CONTENT

| ID | Workflow | Status | Notes |
|----|---------|--------|-------|
| CNT-WF-006 | The Reclaim — Sarah's Story | ✅ APPROVED | Women's segment story |
| CNT-WF-012 | Aware & Able Blog Series | 🔵 DRAFT | Outlines stage in progress |
| CNT-WF-013 | Cinematic Prompt Generator v4 | ✅ LIVE | AI image prompts with ETKM visual doctrine |
| CNT-WF-017 | Awareness Advantage Ecosystem | ✅ APPROVED | 5 articles, 7 emails, 35 social posts |

### OPS — OPERATIONS

| ID | Workflow | Status | Notes |
|----|---------|--------|-------|
| OPS-WF-008 | Core Brand Skill System | ✅ LIVE | 5 brand skills active |
| OPS-WF-009 | Extended Skill Library | ✅ LIVE | 21 skills on MCP server |
| OPS-WF-010 | Visual Aide Builder | ✅ LIVE | 16 visual aide types |
| OPS-WF-015 | Student Etiquette Agreement PDF | ✅ APPROVED | Signed during onboarding |

### TRN — TRAINING PROGRAM

| ID | Workflow | Status | Notes |
|----|---------|--------|-------|
| TRN-WF-014 | Curriculum Checklist Sheets | ✅ APPROVED | Beginner/Intermediate/Advanced tracks |

---

## OPEN DEPENDENCIES

| ID | Item | Needed By | Status |
|----|------|-----------|--------|
| D-02 | Google Drive PDF hosting link | ACQ-WF-001 Email 1 | PENDING |
| D-05 | etkmstudent.com content rewrite | Platform | PLANNED |
| D-06 | 4 website page voice rewrites | ACQ-WF-002 competency emails | PENDING — pages live, voice updates remaining |
| D-08 | Real student testimonial | ACQ-WF-018 | PENDING |
| D-09 | Free trial form render verification | ACQ-WF-018 | PENDING |
| D-12 | CBLTAC duplicate field | etkm-crm-doctrine | PENDING MANUS |

---

## SESSION OPENING PROTOCOL

Three steps before any build session begins.

1. Load this skill — confirm active.
2. Declare intent: "I am about to build/modify: [ID and name]"
3. Confirm status in registry — do not rebuild anything that is not DRAFT or PLANNED.

If status is ambiguous or a dependency is missing — STOP and ask Nathan.

---

## COMMIT FORMAT

```
[PROJECT-WF-###] ACTION — description
```

Examples:
- [ACQ-WF-001] FIX — update arc 3 subject line day 7
- [ACQ-WF-002] ADD — load complete, all 28 emails active
- [OPS-WF-009] UPDATE — etkm-crm-doctrine to v2.0
- [EVT-WF-003] VERIFY — CBLTAC registration URL confirmed

---

## HANDOFF PROTOCOL: CLAUDE TO MANUS

When delivering approved copy or a build brief, Claude provides:
1. Workflow ID (PROJECT-WF-###) and name
2. Status: APPROVED or READY FOR LOAD
3. Complete copy with all merge tags
4. All dependencies and open items
5. Success criteria — what "done" looks like
6. Explicit note: Manus does not rewrite copy

When done: Manus writes completion receipt to Google Drive /Status/[ID]-COMPLETE.md.
Cowork detects receipt, updates Nathan.

---

## INFRASTRUCTURE REFERENCE

| Asset | Location |
|-------|---------|
| Workflow Registry | github.com/easttxkravmaga/Claude /registry/WORKFLOW-REGISTRY.md |
| SESSION_STATE | github.com/easttxkravmaga/Claude /SESSION_STATE.md |
| Skill Library | github.com/easttxkravmaga/Claude /skills/ |
| MCP Server | etkm-backend-production.up.railway.app |
| Arc Classifier | /classify-arc — POST {qa_response} |
| Free Trial Booking | calendly.com/easttxkravmaga-fud9/free-trial-lesson |
| Student Journey Map | etxkravmaga.com/etkm-student/etkm-journey-map/ |

---

## COPY RULES

Prohibited words: mastery, dominate, destroy, killer, beast, crush, elite, warrior
Voice: Advisor not salesperson. Student is the hero. ETKM is the guide.
Core mission: Go Home Safe.
PEACE Framework: Prepared, Empowered, Aware, Capable, Engaged.
Merge tag format: [square_bracket] — Pipedrive native only.
