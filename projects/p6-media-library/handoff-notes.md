# Handoff Notes — P6 Media Intelligence Library

**Built:** 2026-04-09
**Updated:** 2026-04-09 — Taxonomy finalized, Notion database created
**Status:** All deliverables complete. Ready for Nathan to deploy.

---

## What Was Built

| File | Purpose |
|---|---|
| `cloud-run/app.py` | Flask microservice — accepts image, returns grayscale JPEG |
| `cloud-run/requirements.txt` | Flask, Pillow, gunicorn |
| `cloud-run/Dockerfile` | Cloud Run container, correct `sh -c` CMD form |
| `n8n/workflow.json` | Complete n8n pipeline — import and activate |
| `n8n/env-vars.md` | All environment variables needed (Notion DB ID pre-filled) |
| `notion/database-setup.md` | Reference schema documentation |
| `claude-prompt/prompt.md` | Finalized Claude API prompt with taxonomy reference |
| `deployment-guide.md` | Full deployment sequence |
| `handoff-notes.md` | This file |
| `qa-report.md` | QA gate results |

---

## Key Decisions Made

**1. Haiku 4.5 for tagging**
`claude-haiku-4-5-20251001` — classification task, not reasoning. Correct model for structured JSON extraction from image at cost.

**2. Taxonomy: 14 audience arcs + 6 scene intents (20 tags total)**
Original generic taxonomy replaced with ETKM-native system:
- 14 audience arc tags (blue in Notion) — from `etkm-audience-intelligence` skill
- 6 scene intent tags (red in Notion) — from `etkm-cinematic-doctrine` skill
Every image gets 1-2 arc tags + 1-2 scene intent tags.

**3. Notion database already created**
Database is live: `ETKM Media Library` under Ai Resources → ETKM Operational Dashboards
URL: https://www.notion.so/6d54ec60e8334edc86ca2d8b18e3aeb2
ID: `6d54ec60-e833-4edc-86ca-2d8b18e3aeb2`
Nathan only needs to connect the n8n integration credential to it.

**4. Error Logger node removed**
No webhook destination exists. Removed cleanly — no open references in workflow.

**5. "Move" = Upload B&W + Delete original**
n8n has no native move. Upload to library → delete from ingest. Identical net result.

**6. B&W filename prefixed with `bw_`**
Uploaded file to library is named `bw_[original_filename].jpg`. Distinguishable in Drive, original filename preserved.

**7. 1Gi Cloud Run memory**
Pillow processing spikes higher than the existing `etkm-backend` (512Mi). Prevents OOM during bulk backlog runs.

**8. `tone` field removed**
The original spec had a `tone` field in the JSON response. Dropped — scene intent tags carry that signal more precisely and connect directly to the cinematic doctrine.

---

## Deviations from Spec

| Item | Spec | Actual | Reason |
|---|---|---|---|
| Taxonomy | Original 4-category tag system | 14 arcs + 6 scene intents | Nathan directed — connects media library directly to audience system |
| Error Logger | Present | Removed | Nathan directed — no webhook destination |
| Notion parent | "Under Notion Infrastructure" | Ai Resources → ETKM Operational Dashboards | Most logical location found in workspace |
| `tone` field | JSON field in Claude response | Removed | Scene intent tags make it redundant |

---

## How to Deploy (Exact Steps)

**Notion database** — already created. Skip to step 2.

1. **Create Google Drive folders** (5 min) — deployment-guide.md Phase 1
2. **Connect Notion integration** (5 min) — notion.so/my-integrations → new integration → grant it access to `ETKM Media Library`
3. **Deploy Cloud Run service** (10 min) — deployment-guide.md Phase 3
4. **Import and configure n8n workflow** (10 min) — deployment-guide.md Phase 4
   - Set 4 env vars (Drive folder IDs, Cloud Run URL, Anthropic key)
   - Notion DB ID is pre-filled in env-vars.md
5. **Smoke test** — 1 image through the pipeline
6. **Drop backlog** — 100 images, pipeline runs unattended

Total active setup time: ~30 minutes.

---

## Open Items

None. All decisions resolved.

---

## Feeds Into

- **P4 Marketing** — query by arc tag when building campaign assets
- **P5 Content Production** — query by content_use_cases field
- **Future Social Media Engine** — `Social media post` use case tag already in place; contrast/transparency rules go in the social engine, not here
