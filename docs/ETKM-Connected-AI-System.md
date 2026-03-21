# EAST TEXAS KRAV MAGA — CONNECTED AI SYSTEM
**How Claude, Claude Code, Cowork, and Manus work together to finish a task**
March 2026 · Build Reference & Instruction Guide

---

## THE PROBLEM THIS DOCUMENT SOLVES
Claude, Claude Code, Cowork, and Manus don't talk to each other natively. Without a deliberate connection layer, every task requires Nathan to manually hand off between tools. This document builds that connection layer — a shared workspace, a code repository, and clear prompts so each tool knows exactly what to do and in what order.

---

## 01 THE CONNECTED SYSTEM — THREE LAYERS

### LAYER 1 — Google Drive (Shared Workspace)
Every tool can read from and write to Google Drive.
- `AI Resources/Queue/` — new tasks waiting to be executed
- `AI Resources/In-Progress/` — tasks currently being worked
- `AI Resources/Completed/` — finished and deployed
- `AI Resources/Registry/` — live workflow registry (source of truth)
- `AI Resources/Scripts/` — Claude Code scripts archived after each build

### LAYER 2 — GitHub (Code Repository)
All scripts Claude Code writes live in a GitHub repository.
- `etkm-automations/make-scenarios/` — Make.com build scripts
- `etkm-automations/pipedrive/` — Pipedrive config and setup scripts
- `etkm-automations/utils/` — shared helper functions
- `etkm-automations/docs/` — deployment docs as markdown

### LAYER 3 — Make.com (Execution Orchestrator)
- Receives webhooks when a new task is queued in Drive
- Calls Pipedrive API to pull filtered contact lists at send time
- Sends event promotion emails via Nathan's Gmail account
- Calls Claude API for personalized content when needed

---

## 02 TOOL ROLES

### Claude (claude.ai chat) — THE BRAIN
**DOES:** Writes all copy, designs all architecture, produces deployment docs, saves deliverables to Google Drive /Queue/
**NEVER DOES:** Execute automations, directly access Pipedrive/Make.com/any platform, rewrite approved copy without Nathan's instruction

### Claude Code (CLI) — THE ENGINEER
**DOES:** Reads deployment docs from Drive, scripts Make.com scenarios via API, calls Pipedrive API, commits to GitHub, runs tests
**NEVER DOES:** Write or modify email copy, make routing/strategy decisions, replace Manus for browser-only tasks

### Claude Cowork (desktop) — THE PROJECT MANAGER
**DOES:** Monitors /Queue/ for new deployment docs, moves files Queue→In-Progress→Completed, keeps registry updated, triggers Claude Code scripts
**NEVER DOES:** Write copy or strategy, build automations directly, replace Claude Code for API/scripting work

### Manus — THE BROWSER OPERATOR
**DOES:** Step-by-step Pipedrive canvas instructions, verifies completed automations, runs test sends, connects Make.com to Gmail/Pipedrive (OAuth)
**NEVER DOES:** Rewrite/shorten/modify any copy, attempt 30-step canvas builds solo under session timeout, make routing/architecture decisions

---

## 03 STANDARD TASK FLOW (WF-003 as example)

1. **Claude** writes deployment doc
2. **Nathan** saves doc to Google Drive /Queue/
3. **Cowork** detects new file → moves to /In-Progress/ → notifies Nathan
4. **Nathan** opens Claude Code with build prompt
5. **Claude Code** reads doc, writes Make.com scenario script, calls Make.com API, creates scenario
6. **Claude Code** commits script to GitHub: `etkm-automations/make-scenarios/wf003-cbltac.js`
7. **Cowork** moves doc to /Completed/ → updates registry: WF-003 status → LOADED
8. **Manus** verifies Make.com scenario matches deployment doc, runs test send
9. **Nathan** reviews test result, flips scenario to ON → LIVE

---

## 04 CLAUDE CODE PROMPTS

### PROMPT 1 — Build Make.com Event Promotion Scenario
```
You are building a Make.com scenario for an ETKM event promotion.
DEPLOYMENT DOC: [paste Google Drive link]
MAKE.COM API KEY: [key]
PIPEDRIVE API KEY: [key]
CONTACT FILTER: Pull all Pipedrive contacts where [tag = 'X' OR deal stage = 'Y']
SEND FROM: Nathan's Gmail account (already connected in Make.com)

TASK:
1. Read deployment doc, extract: email subjects, body copy, send day offsets, stop conditions
2. Write Node.js script that calls Make.com API to create a new scenario
3. Scenario structure: Schedule trigger (8AM Central daily) → Pipedrive contact pull → date offset calculation → Gmail send
4. Build one module branch per email
5. Add stop condition: skip contacts where status = 'complete' or 'unsubscribed'
6. Run script and confirm scenario appears in Make.com
7. Commit to GitHub: etkm-automations/make-scenarios/[workflow-name].js
8. Report back: scenario ID, modules created, any errors
```

### PROMPT 2 — Pull and Filter Pipedrive Contacts
```
PIPEDRIVE API KEY: [key]
FILTER CRITERIA: [tag, deal stage, custom field, etc.]
OUTPUT FORMAT: CSV — first_name | email | phone | deal_stage | tags

TASK:
1. Call Pipedrive Persons API with defined filter
2. Handle pagination — pull all matching contacts
3. Write results to CSV
4. Save to Google Drive: AI Resources/Exports/[filename]-[date].csv
5. Report: total contacts pulled, any missing email addresses
```

### PROMPT 3 — Update Workflow Registry
```
REGISTRY DOC: AI Resources/Registry/ETKM_Workflow_Registry.docx
WORKFLOW ID: [WF-001 / WF-002 / WF-003]
NEW STATUS: [PLANNED / DRAFT / APPROVED / LOADED / LIVE / PAUSED]
NOTES: [dependencies resolved, dates, etc.]

TASK:
1. Read current registry doc from Drive
2. Find row for specified workflow ID
3. Update Status and Notes columns
4. Save back to Drive (overwrite existing)
5. Confirm update with current registry state
```

### PROMPT 4 — Pipedrive Organizational Setup
```
PIPEDRIVE API KEY: [key]
TASK: [describe exactly what needs to be set up]

TASK:
1. Call appropriate Pipedrive API endpoint
2. Confirm change with API read-back
3. Report: what was created/changed, IDs of new objects
4. Commit reusable scripts to GitHub: etkm-automations/pipedrive/
```

### PROMPT 5 — Test a Make.com Scenario
```
MAKE.COM API KEY: [key]
SCENARIO ID: [from Make.com URL]
TEST EMAIL: [Nathan's email]

TASK:
1. Call Make.com API to trigger manual run
2. Override recipient with test email for all send modules
3. Confirm each module executes without errors
4. Report: which modules ran, which emails sent, any errors
5. If errors: identify module, describe error, suggest fix
```

---

## 05 COWORK AUTOMATION RULES

| Trigger | Action | Why |
|---|---|---|
| New file in /Queue/ | Move to /In-Progress/. Desktop notification: 'New task ready: [filename]. Open Claude Code to build.' | Tells Nathan a doc is staged without manual checking |
| Claude Code writes `build-complete-[wf-id].txt` to /In-Progress/ | Move deployment doc + status file to /Completed/. Update registry: status → LOADED | Closes loop after build |
| New file in /Completed/ | Gmail to Nathan: 'WF-[id] build complete. Ready for Manus verification.' | Prompts Manus handoff |
| Weekly Monday 8AM | Read registry, email Nathan: all LIVE workflows, PENDING dependencies, next priority | Weekly system status |

---

## 06 ENVIRONMENT VARIABLES

| Variable | Source | Used By | Purpose |
|---|---|---|---|
| MAKE_API_KEY | Make.com → Account → API | Claude Code | Creates/manages Make.com scenarios |
| PIPEDRIVE_API_KEY | Pipedrive → Settings → Personal Preferences → API | Claude Code + Make.com | Contact pulls, pipeline setup |
| GOOGLE_DRIVE_CREDENTIALS | Google Cloud Console → Service Account → JSON | Claude Code + Cowork | Drive read/write |
| GITHUB_TOKEN | GitHub → Developer Settings → Personal Access Tokens | Claude Code | Commits to etkm-automations/ |
| ANTHROPIC_API_KEY | Anthropic Console → API Keys | Make.com | Personalize event emails via Claude API |
| GMAIL_OAUTH | Make.com → Connections → Gmail → Connect | Make.com | Send from Nathan's Gmail |

---

## 07 GITHUB REPOSITORY STRUCTURE

```
etkm-automations/
├── make-scenarios/
│   ├── wf003-cbltac-event.js
│   └── template-event-promotion.js
├── pipedrive/
│   ├── setup-pipeline-stages.js
│   ├── setup-custom-fields.js
│   ├── bulk-tag-contacts.js
│   └── pull-filtered-contacts.js
├── utils/
│   ├── make-api-helpers.js
│   ├── pipedrive-api-helpers.js
│   └── google-drive-helpers.js
├── docs/
└── README.md
```

**Commit format:**
```
[WF-003] ADD — CBLTAC event promotion Make.com scenario
[WF-003] FIX — corrected Pipedrive contact filter
[UTIL] ADD — shared Pipedrive API helper functions
```

---

## 08 ONE-TIME SETUP CHECKLIST

| # | Task | Who | Tool |
|---|---|---|---|
| 1 | Create GitHub repo: etkm-automations | Nathan | GitHub |
| 2 | Create Drive folder structure: /Queue/, /In-Progress/, /Completed/, /Registry/, /Scripts/, /Exports/ | Nathan | Google Drive |
| 3 | Create Google Cloud service account + JSON credentials | Nathan | Google Cloud Console |
| 4 | Set all env vars in Claude Code terminal | Nathan | Claude Code |
| 5 | Connect Gmail to Make.com (OAuth) | Manus | Make.com |
| 6 | Connect Pipedrive to Make.com | Manus | Make.com + Pipedrive |
| 7 | Configure Cowork folder monitoring rules | Nathan | Cowork |
| 8 | Save WF-003 deployment doc to /Queue/ and run first full build | Nathan | All |

---
*ETKM Connected AI System · East Texas Krav Maga · March 2026 · Update when architecture changes*
