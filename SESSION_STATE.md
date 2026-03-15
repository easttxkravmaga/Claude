# ETKM Session State
_Last updated: 2026-03-15_

## Current Repo: easttxkravmaga/Claude (private)
Branch: main | Cloud Run: LIVE

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

## SMS / Twilio Integration — Added 2026-03-15

| Component | Status | Notes |
|---|---|---|
| Twilio SMS module (`twilio_sms.py`) | ✅ BUILT | Webhooks, send, opt-out, signature verification |
| Message templates (`message_templates.py`) | ✅ BUILT | 9 pre-approved templates, compliance copy |
| Pipedrive SMS integration (`pipedrive_sms.py`) | ✅ BUILT | Contact lookup, note logging, send-by-person |
| Flask routes registered in `app.py` | ✅ BUILT | Blueprints registered |
| Sole Proprietor Setup Guide | ✅ WRITTEN | `docs/TWILIO-SOLE-PROPRIETOR-SETUP.md` |
| Technical Implementation Docs | ✅ WRITTEN | `docs/TWILIO-SMS-IMPLEMENTATION.md` |
| Twilio Console Registration | ⏳ PENDING | Nathan to complete in Twilio Console |
| Twilio Env Vars on Cloud Run | ⏳ PENDING | TWILIO_ACCOUNT_SID, AUTH_TOKEN, etc. |
| Webhook URL configuration | ⏳ PENDING | Set after Cloud Run deploy |

### SMS Endpoints (ready for deploy)

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/twilio/inbound-sms` | POST | Inbound SMS webhook (Twilio calls this) |
| `/api/twilio/status-callback` | POST | Delivery status callback (Twilio calls this) |
| `/api/twilio/send` | POST | Send SMS (internal API) |
| `/api/twilio/opt-in` | POST | Register opt-in |
| `/api/twilio/opt-status/<phone>` | GET | Check opt status |
| `/api/twilio/messages` | GET | Message log |
| `/api/twilio/templates` | GET | List templates |
| `/api/pipedrive/send-sms` | POST | Send to Pipedrive contact |
| `/api/pipedrive/log-inbound` | POST | Log inbound to Pipedrive |

---

## Next Priorities

| Priority | Task | Owner |
|---|---|---|
| 🔴 NOW | Twilio Console sole proprietor registration | Nathan |
| 🔴 NOW | Set Twilio env vars on Cloud Run | Claude Code |
| 🔴 NOW | WF-002 Manus load into Pipedrive | Manus |
| 🟡 NEXT | Deploy SMS endpoints to Cloud Run | Claude Code |
| 🟡 NEXT | Pipedrive MCP tools (5 endpoints in app.py) | Claude |
| 🟡 NEXT | Populate /workflows/ with email content | Claude |
| 🟢 LATER | Shopify store build | Nathan decision |

---

## Repo Structure

```
easttxkravmaga/Claude/
├── SESSION_STATE.md        ← this file
├── README.md
├── Dockerfile              ← Cloud Run build
├── railway.toml
├── Procfile
├── backend/
│   ├── app.py              ← Flask + MCP server + Twilio routes
│   ├── twilio_sms.py       ← Twilio SMS webhooks, send, opt-out
│   ├── message_templates.py ← Pre-approved SMS templates
│   ├── pipedrive_sms.py    ← Pipedrive ↔ Twilio integration
│   └── requirements.txt
├── docs/
│   ├── TWILIO-SOLE-PROPRIETOR-SETUP.md  ← Console registration guide
│   └── TWILIO-SMS-IMPLEMENTATION.md     ← Technical API reference
├── prompts/
│   └── arc-classification-system-prompt.md
├── registry/README.md
├── skills/[27 folders]
└── workflows/              ← WF email content (not yet populated)
```

---

## Active Credentials (stored in Cloud Run env vars)

| Key | Notes |
|---|---|
| ANTHROPIC_API_KEY | Set in Cloud Run ✅ |
| GITHUB_TOKEN | PAT ghp_hbJT4... expires 2026-04-10 |
| PIPEDRIVE_API_KEY | Set in Cloud Run ✅ |
| TWILIO_ACCOUNT_SID | ⏳ PENDING — set after Twilio registration |
| TWILIO_AUTH_TOKEN | ⏳ PENDING — set after Twilio registration |
| TWILIO_MESSAGING_SERVICE_SID | ⏳ PENDING — set after Messaging Service creation |
| TWILIO_PHONE_NUMBER | ⏳ PENDING — set after number purchase |
| APP_BASE_URL | ⏳ PENDING — Cloud Run service URL |

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
