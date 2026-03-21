---
name: etkm-cowork-protocol
description: >
  Use this skill for ANY task involving Cowork's role in the ETKM AI operations
  system — including folder monitoring setup, AI completion receipt conventions,
  stall detection, file routing, and cross-AI coordination. Trigger whenever
  discussing Cowork's responsibilities, setting up background monitoring, defining
  what Cowork watches for, or planning how Cowork connects Claude, Manus, and
  Claude Code. Trigger phrases: "Cowork", "background monitoring", "completion
  receipt", "status folder", "stall detection", "file routing", "AI check-in",
  "automated alert", "Cowork setup", "monitor Drive", "notify Nathan".
---

# ETKM Cowork Protocol

**Version:** 1.0
**Last Updated:** 2026-03-11

Cowork is the always-on layer of the ETKM AI operations system. It runs without
Nathan present, monitors all AI output, and closes the gap that chat conversations
cannot close. It does not make strategic decisions — it watches, detects, routes,
and alerts.

---

## COWORK'S ROLE

Cowork handles four things:

1. **Receipt detection** — when an AI finishes a task, it verifies the work is done
2. **Stall detection** — when an AI task stops moving, it alerts Nathan
3. **File routing** — output files get moved to the correct project folder automatically
4. **Sequence triggering** — when Step N is complete, it prepares the brief for Step N+1

Cowork never writes copy. Never makes automation decisions. Never modifies Pipedrive.
Those lanes belong to Claude, Manus, and Claude Code respectively.

---

## GOOGLE DRIVE FOLDER STRUCTURE

All AI coordination runs through a defined folder structure in Google Drive.
Every AI reads and writes to these folders using the same conventions.

```
/ETKM-AI/
  ├── Status/         ← Completion receipts. Every AI drops .md file here when done.
  ├── In-Progress/    ← Active task files. Cowork watches for updates.
  ├── Needs-Review/   ← Work requiring Nathan's approval before next step.
  └── Briefings/      ← Briefs written by Claude for Manus or Claude Code.

/ACQ/                 ← Student Acquisition project outputs
/RET/                 ← Retention & Advancement project outputs
/EVT/                 ← Events project outputs
/CNT/                 ← Content project outputs
/OPS/                 ← Operations project outputs
/TRN/                 ← Training Program project outputs
```

Cowork auto-routes files tagged with a PROJECT-WF-### ID to the matching
project folder when they land in the output area.

---

## COMPLETION RECEIPT FORMAT

Every AI writes a receipt file to /ETKM-AI/Status/ when a task is complete.
File name format: [PROJECT-WF-###]-COMPLETE.md

```markdown
# [PROJECT-WF-###] — [Workflow Name]
**Completed by:** [Manus / Claude Code]
**Date:** [YYYY-MM-DD]
**Task:** [Brief description of what was built/loaded]
**Verified:**
  - [What was confirmed working]
  - [URLs or endpoints checked]
**Issues / Open Items:**
  - [Any flags for Nathan or Claude]
**Registry status:** Ready to move to LIVE
```

Cowork reads this file, updates the registry status, and notifies Nathan.
No receipt = no LIVE status. Nathan does not manually close tasks.

---

## STALL DETECTION RULES

Cowork monitors /ETKM-AI/In-Progress/ for files that stop updating.

| Task type | Stall threshold | Action |
|-----------|-----------------|--------|
| Manus CRM load | 4 hours with no update | Alert Nathan |
| Claude Code build | 2 hours with no update | Alert Nathan |
| Manus browser task | 2 hours with no update | Alert Nathan |
| Any task past deadline | Immediately | Alert Nathan + flag for review |

When a stall is detected, Cowork:
1. Moves the task file from /In-Progress/ to /Needs-Review/
2. Adds a stall notice to the top of the file with timestamp
3. Sends Nathan an alert with the task ID and last known state

---

## AI CHECK-IN CONVENTION

Cowork verifies AI task completion by checking for receipts — not by asking AIs directly.

| What Cowork checks | How |
|-------------------|-----|
| Manus completed CRM load | Receipt exists in /Status/ |
| Claude Code build deployed | Receipt + endpoint health check |
| Sequence is LIVE | Receipt confirmed + Pipedrive stage verified |
| File routed to correct folder | PROJECT-WF-### prefix on file → matched to project folder |

If receipt is missing after the expected completion window:
→ Cowork flags as stalled → moves to /Needs-Review/ → alerts Nathan.

---

## SEQUENCE CONTINUATION

When Cowork detects a receipt for Step N of a multi-step workflow, it:
1. Reads the receipt to confirm success
2. Places the Step N+1 brief (already written by Claude) in /Needs-Review/
3. Notifies Nathan: "ACQ-WF-002 load complete. Next step ready for review."
4. Nathan reviews and approves before Step N+1 executes

Cowork never auto-executes the next step without Nathan's approval.
It only prepares and surfaces it.

---

## FILE ROUTING RULES

Cowork routes output files based on PROJECT-WF-### prefix:

| File prefix | Destination folder |
|-------------|-------------------|
| ACQ-WF-### | /ACQ/ |
| RET-WF-### | /RET/ |
| EVT-WF-### | /EVT/ |
| CNT-WF-### | /CNT/ |
| OPS-WF-### | /OPS/ |
| TRN-WF-### | /TRN/ |
| No prefix | /Needs-Review/ — Nathan categorizes |

---

## COWORK + PIPEDRIVE INTEGRATION

Cowork does NOT write to Pipedrive directly. Manus owns all Pipedrive writes.

Cowork CAN surface alerts related to Pipedrive events:
- Payment Due stage entry → alert Nathan within 1 hour
- At-Risk escalation with no Manus receipt → flag as possibly incomplete
- PIF Due stage approaching → prepare Nathan notification

These alerts come from Cowork monitoring completion receipts from Manus,
not from Cowork having direct Pipedrive access.

---

## SETTING UP COWORK MONITORING

To set up a new monitoring rule for a workflow, Claude specifies:

```
Workflow: [PROJECT-WF-###]
Watch folder: /ETKM-AI/In-Progress/[ID]-[name]/
Receipt expected: [file name in /Status/]
Deadline: [expected completion date/time]
On receipt: [next action — route file, notify Nathan, prepare next brief]
On stall: [alert Nathan with context]
```

Claude writes this spec. Cowork executes it. Nathan approves the monitoring rule
before it activates.

---

## WHAT COWORK NEVER DOES

- Makes copy or strategy decisions
- Modifies Pipedrive records
- Executes the next workflow step without Nathan approval
- Moves a workflow status to LIVE without a confirmed receipt
- Overrides Claude, Manus, or Claude Code decisions

Cowork's job is visibility and coordination — not execution.

Load etkm-ai-roles for the full AI stack role reference.
Load etkm-workflow-registry for the full workflow inventory.
