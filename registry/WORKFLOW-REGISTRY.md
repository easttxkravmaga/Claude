# ETKM WORKFLOW REGISTRY
**Version:** 2.0
**Updated:** 2026-03-11
**System:** Project → Workflow hierarchy. All IDs are permanent once assigned.

---

## ID FORMAT

```
[PROJECT CODE]-WF-[###]
```

Example: `ACQ-WF-001` = Acquisition project, workflow #001

---

## PROJECT CODES

| Code | Project Name | Scope |
|------|-------------|-------|
| **ACQ** | Student Acquisition | Everything that turns a stranger into a signed student |
| **RET** | Retention & Advancement | Everything that keeps and advances a current student |
| **EVT** | Events | All event campaigns — CBLTAC and future |
| **CNT** | Content | Blog, social, email content systems |
| **OPS** | Operations | Internal tools, skills library, forms, infrastructure |
| **TRN** | Training Program | Curriculum, checklist sheets, definitions |

---

## WORKFLOW REGISTRY — ALL WORKFLOWS

### ACQ — Student Acquisition

| ID | Workflow | Status | Notes |
|----|---------|--------|-------|
| ACQ-WF-001 | Pre-Trial Email Funnel (6 arcs, 8 emails each) | ✅ LIVE | WF-001 legacy |
| ACQ-WF-002 | 90-Day Onboarding Sequence (28 emails) | ⏳ PENDING MANUS | WF-002 legacy. Manus brief at docs/WF-002-Manus-Deploy-Brief.md |
| ACQ-WF-007 | Sales Communication System (advisor model) | ✅ LIVE | WF-007 legacy |
| ACQ-WF-011 | First-Touch Landing Page + PDF Lead Magnet | ✅ APPROVED | WF-011 legacy |
| ACQ-WF-016 | Student Intake Form + CRM Backend | ⏳ BUILT | WF-016 legacy |
| ACQ-WF-018 | Free Trial Landing Page Rewrite | ✅ APPROVED | WF-018 legacy |

### RET — Retention & Advancement

| ID | Workflow | Status | Notes |
|----|---------|--------|-------|
| RET-WF-004 | 52-Week PEACE Social Calendar | ✅ LIVE | WF-004 legacy |
| RET-WF-005 | March Monthly/Weekly Themes | ✅ LIVE | WF-005 legacy |

### EVT — Events

| ID | Workflow | Status | Notes |
|----|---------|--------|-------|
| EVT-WF-003 | CBLTAC Event Campaign (10 emails) | ✅ LIVE | WF-003 legacy. April 24-25 2026 |

### CNT — Content

| ID | Workflow | Status | Notes |
|----|---------|--------|-------|
| CNT-WF-006 | The Reclaim — Sarah's Story | ✅ APPROVED | WF-006 legacy |
| CNT-WF-012 | Aware & Able Blog Series | 🔵 DRAFT | WF-012 legacy |
| CNT-WF-013 | Cinematic Prompt Generator v4 | ✅ LIVE | WF-013 legacy |
| CNT-WF-017 | Awareness Advantage Ecosystem | ✅ APPROVED | WF-017 legacy |

### OPS — Operations

| ID | Workflow | Status | Notes |
|----|---------|--------|-------|
| OPS-WF-008 | Core Brand Skill System | ✅ LIVE | WF-008 legacy |
| OPS-WF-009 | Extended Skill Library (21 skills) | ✅ LIVE | WF-009 legacy |
| OPS-WF-010 | Visual Aide Builder | ✅ LIVE | WF-010 legacy |
| OPS-WF-015 | Student Etiquette Agreement PDF | ✅ APPROVED | WF-015 legacy |

### TRN — Training Program

| ID | Workflow | Status | Notes |
|----|---------|--------|-------|
| TRN-WF-014 | Curriculum Checklist Sheets | ✅ APPROVED | WF-014 legacy |

---

## NUMBERING RULES

- Numbers are assigned sequentially and never reused
- Next available: ACQ-WF-019, RET-WF-020, EVT-WF-021 (etc.)
- Legacy WF-### IDs are retired — use full PROJECT-WF-### going forward

---

## COMMIT FORMAT

```
[PROJECT-WF-###] ACTION — description
```

Examples:
- `[ACQ-WF-001] FIX — update arc 3 subject line`
- `[ACQ-WF-002] ADD — load complete to Pipedrive`
- `[OPS-WF-009] UPDATE — etkm-brand-kit to v3.1`

---

## STATUS LEGEND

| Status | Meaning |
|--------|---------|
| ✅ LIVE | Deployed and running |
| ✅ APPROVED | Written and approved, not yet deployed |
| ⏳ PENDING MANUS | Ready for Manus to load/deploy |
| ⏳ BUILT | Built but pending approval/deployment |
| 🔵 DRAFT | In progress |
| 🔴 BLOCKED | Waiting on dependency |
| ❌ RETIRED | Deprecated, do not use |
