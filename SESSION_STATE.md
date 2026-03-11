# ETKM Session State
_Last updated: 2026-03-11_

## Current Repo: easttxkravmaga/Claude (private)
Branch: main | Auto-deploy: pending Railway connection

---

## Completed This Session

| # | What | Commit |
|---|---|---|
| 1 | Folder structure (7 dirs + README) | 13077a0 |
| 2 | All 21 skill files → /skills/ | 3da96bf |
| 3 | Arc classification system prompt → /prompts/ | 0be39d5 |
| 4 | Flask MCP server (app.py, 432 lines) | 0be39d5 |
| 5 | Railway config (Procfile, railway.toml) | 0be39d5 |

---

## Current Repo Structure

```
easttxkravmaga/Claude/
├── SESSION_STATE.md        ← this file
├── README.md               ← master map
├── Procfile                ← Railway: gunicorn backend.app:app
├── railway.toml            ← Railway: build + health check config
├── backend/
│   ├── app.py              ← Flask + MCP server (432 lines)
│   ├── requirements.txt    ← flask, requests, gunicorn
│   └── __init__.py
├── crm/                    ← Pipedrive architecture docs
├── docs/                   ← Brand/strategy reference
├── prompts/
│   └── arc-classification-system-prompt.md  ← DONE ✓
├── registry/
│   └── README.md           ← Workflow registry + session protocol
├── skills/
│   └── [21 skill folders]  ← DONE ✓ (all SKILL.md files)
└── workflows/              ← WF-001/002/003 (not yet populated)
```

---

## MCP Server — What's Built

**Endpoints:**
- `GET  /health` → Railway health check
- `POST /classify-arc` → arc classification + Claude API email generation
- `POST /webhook/square` → payment failure → Pipedrive P4
- `POST /mcp` → JSON-RPC 2.0 MCP server
- `GET  /mcp` → SSE transport

**MCP Tools exposed:**
- `get_skill` — fetch any SKILL.md by name from GitHub
- `list_skills` — list all 21 skills
- `get_prompt` — fetch any prompt file
- `get_workflow_status` — fetch registry/README.md
- `classify_arc` — keyword-based arc classification

---

## ✅ DEPLOYED — Railway

**Required env vars:**
- `ANTHROPIC_API_KEY` — from console.anthropic.com
- `GITHUB_TOKEN` — use PAT: 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 (expires Apr 10 2026)
- `PIPEDRIVE_API_KEY` — from Pipedrive settings

**Deploy method — Railway CLI (bash, no browser):**
```bash
npm install -g @railway/cli
railway login --token RAILWAY_TOKEN
railway link   # select easttxkravmaga/Claude
railway up
railway variables set ANTHROPIC_API_KEY=xxx GITHUB_TOKEN=xxx PIPEDRIVE_API_KEY=xxx
```

**Railway token location:** railway.app → Account Settings → Tokens

MCP URL (LIVE): `https://etkm-backend-production.up.railway.app/mcp`
Add that URL as a custom MCP connector in Claude.ai Settings → Connectors.

---

## Remaining Work

| Priority | Task | Owner |
|---|---|---|
| 🔴 NOW | Deploy Flask app to Railway | Nathan → Railway token → Claude bash |
| 🔴 NOW | Set 3 env vars on Railway | Claude bash |
| 🟡 NEXT | Add Railway URL as MCP connector in Claude.ai | Nathan (Settings → Connectors) |
| 🟡 NEXT | Populate /workflows/ with WF-001/002/003 email content | Claude |
| 🟢 LATER | Test /classify-arc with live Manus call | Manus |
| 🟢 LATER | WF-001 completion (D-01/D-02 dependencies) | Claude + Manus |

---

## Active PAT
Name: ETKM-Skills-Migration
Token: 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
Scope: repo (read/write) on easttxkravmaga/Claude
Expires: 2026-04-10

---

## Deployment — LIVE ✅
_Deployed: 2026-03-11_

**Railway Service:** etkm-backend  
**Project ID:** 207aec28-f967-427f-ae14-f26bd0676012  
**Service ID:** d75dba90-a0f7-41bc-9142-f6c1d316058c  
**Environment:** production (731ec61f-d24a-4599-8d1e-d7084cbb13b1)

**Live Endpoints:**
- Health: `GET  https://etkm-backend-production.up.railway.app/health`
- MCP:    `POST https://etkm-backend-production.up.railway.app/mcp`
- Arc:    `POST https://etkm-backend-production.up.railway.app/classify-arc`
- Square: `POST https://etkm-backend-production.up.railway.app/webhook/square`

**To add as MCP connector in Claude.ai:**
Settings → Connectors → Add MCP Server → URL: `https://etkm-backend-production.up.railway.app/mcp`

**Next:**
- [ ] Add MCP URL as connector in Claude.ai (Nathan does this in Settings)
- [ ] Populate /workflows/ with WF-001/002/003 email content
- [ ] Test /classify-arc with live Manus call
