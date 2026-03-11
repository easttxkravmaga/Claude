# ETKM Session State
_Last updated: 2026-03-11_

## Current Repo: easttxkravmaga/Claude (private)
Branch: main | Railway: LIVE at etkm-backend-production.up.railway.app

---

## Completed — Full Build History

| # | What | Commit |
|---|---|---|
| 1 | Folder structure + README | 13077a0 |
| 2 | All 21 skill files → /skills/ | 3da96bf |
| 3 | Arc classification system prompt + Flask MCP server | 0be39d5 |
| 4 | Railway config (Procfile, railway.toml, Dockerfile) | c265e55 |
| 5 | Deployed to Railway — LIVE | — |
| 6 | Claude.ai MCP connector active | — |

---

## Live Endpoints

| Endpoint | URL | Status |
|---|---|---|
| Health | https://etkm-backend-production.up.railway.app/health | ✅ LIVE |
| MCP Server | https://etkm-backend-production.up.railway.app/mcp | ✅ LIVE |
| Arc Classification | https://etkm-backend-production.up.railway.app/classify-arc | ✅ LIVE |
| Square Webhook | https://etkm-backend-production.up.railway.app/webhook/square | ✅ LIVE |

---

## Workflow Status (Verified 2026-03-11)

| ID | Workflow | Status | Notes |
|---|---|---|---|
| WF-001 | Pre-Trial Email Funnel (6 arcs, 8 emails each) | ✅ LIVE | Calendly URL + PDF link confirmed in place |
| WF-002 | 90-Day Onboarding Sequence (28 emails) | ⏳ APPROVED | Pending Manus load into Pipedrive |
| WF-003 | CBLTAC Event Campaign (10 emails) | ✅ LIVE | Nathan confirmed deployed |
| WF-004 | 52-Week PEACE Social Calendar | ✅ LIVE | Nathan posts manually |
| WF-005 | March Monthly/Weekly Themes | ✅ LIVE | — |

---

## Key URLs (Confirmed)

| Asset | URL |
|---|---|
| Free Trial Booking | https://calendly.com/easttxkravmaga-fud9/free-trial-lesson |
| Welcome PDF (Protect What Matters) | https://drive.google.com/file/d/1BI0ZLUe6qUTzK-JXRGpxveslVS8YAUtg/view?usp=drive_link |
| CBLTAC Registration | https://etxkravmaga.com/cbltac-courses/ |
| ETKM Student Journey Map | https://etxkravmaga.com/etkm-student/etkm-journey-map/ |

---

## Open Dependencies

| ID | Item | Needed By | Status |
|---|---|---|---|
| D-02 | PDF public share link confirmed | WF-001 | ✅ CLOSED |
| D-01 | Calendly URL confirmed | WF-001 | ✅ CLOSED |
| D-03 | Anthropic API key | Manus→Claude API | ✅ CLOSED |
| D-04 | CBLTAC registration URL | WF-003 | ✅ CLOSED |
| D-11 | WF-002 phase-transition emails (Days 30 + 60) | WF-002 | DRAFT — may need completion check |
| D-12 | Notion skill migration | Skills library | PLANNED |

---

## Next Priorities

| Priority | Task | Owner |
|---|---|---|
| 🔴 NOW | WF-002 Manus load into Pipedrive | Manus |
| 🟡 NEXT | Pipedrive MCP tools (5 endpoints in app.py) | Claude |
| 🟡 NEXT | Populate /workflows/ with email content | Claude |
| 🟢 LATER | Shopify store build | Nathan decision |

---

## Repo Structure

```
easttxkravmaga/Claude/
├── SESSION_STATE.md        ← this file
├── README.md
├── Dockerfile              ← Railway build
├── railway.toml
├── Procfile
├── backend/
│   ├── app.py              ← Flask + MCP server
│   └── requirements.txt
├── prompts/
│   └── arc-classification-system-prompt.md
├── registry/README.md
├── skills/[21 folders]
└── workflows/              ← WF email content (not yet populated)
```

---

## Active Credentials (stored in Railway env vars)

| Key | Notes |
|---|---|
| ANTHROPIC_API_KEY | Set in Railway ✅ |
| GITHUB_TOKEN | PAT ghp_hbJT4... expires 2026-04-10 |
| PIPEDRIVE_API_KEY | Set in Railway ✅ |

---

## Pipedrive Audit — 2026-03-11

### Completed via API
- Deal labels: reduced from 11 → 2 (Not Interested, Invalid)
- Person labels: reduced from 20 → 17 (removed Cold/Warm/Hot lead)

### Pending Manus
- Delete duplicate CBLTAC Enrolled Date field (see docs/Pipedrive-Cleanup-Brief.md)

### Clean Label Dictionary

**Deal Labels (2):**
- Not Interested
- Invalid

**Person Labels (17):**
- ETKM Student, Former Student, Fight Back
- Law Enforcement, Military, Private Security, Armed Citizen Tactics
- Youth, Seminar Attendee, Private Lesson
- Sponsor, Coach, Instructor, School Admin, Hosting Seminars, Paladin Security
- Invalid

**Custom Person Fields (kept):**
- ETKM Arc Type: Safety, Parent, Fitness, LE/Mil, Former MA, Default
- CBLTAC Enrolled Date (1 of 2 — Manus to delete duplicate)
- CBLTAC Status: active, complete, paused
- Sakari Opt In / Opt Out (SMS)

---

## Project-Workflow Labeling System — Adopted 2026-03-11

**New ID format:** `[PROJECT]-WF-[###]`

**Project codes:**
- ACQ — Student Acquisition
- RET — Retention & Advancement
- EVT — Events
- CNT — Content
- OPS — Operations
- TRN — Training Program

**Full registry:** registry/WORKFLOW-REGISTRY.md

**Commit format going forward:** `[ACQ-WF-001] ACTION — description`

**Next available numbers:** ACQ-WF-019 | RET-WF-020 | EVT-WF-021 | CNT-WF-022 | OPS-WF-023 | TRN-WF-024
