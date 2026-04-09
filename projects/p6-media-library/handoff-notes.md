# Handoff Notes — P6 Media Intelligence Library

**Built:** 2026-04-09  
**Session:** Claude Code build session  
**Status:** All deliverables complete. Ready for Nathan to deploy.

---

## What Was Built

| File | Purpose |
|---|---|
| `output/p6-media-library/cloud-run/app.py` | Flask microservice — accepts image, returns grayscale JPEG |
| `output/p6-media-library/cloud-run/requirements.txt` | Flask, Pillow, gunicorn |
| `output/p6-media-library/cloud-run/Dockerfile` | Cloud Run container, correct `sh -c` CMD form |
| `output/p6-media-library/n8n/workflow.json` | Complete n8n pipeline — import and activate |
| `output/p6-media-library/n8n/env-vars.md` | All environment variables needed, with sourcing instructions |
| `output/p6-media-library/notion/database-setup.md` | Step-by-step Notion database build with full schema |
| `output/p6-media-library/claude-prompt/prompt.md` | Finalized Claude API prompt with design rationale |
| `output/p6-media-library/deployment-guide.md` | Full deployment sequence from Drive setup through backlog run |

---

## Key Decisions Made

**1. Haiku 4.5 for tagging (not Sonnet)**
Spec confirmed: `claude-haiku-4-5-20251001` is used for image tagging. This is a classification task (structured JSON from image), not complex reasoning. Haiku handles it reliably at lower cost. At 100+ images, savings are material.

**2. "Move" is implemented as Upload + Delete**
n8n's Google Drive node does not have a native "move file" operation. The workflow uploads the B&W image to `/ETKM Media Library/` then deletes the original from `/ETKM Media Ingest/`. Net effect is identical to a move.

**3. B&W filename prefixed with `bw_`**
Uploaded file to the library is named `bw_[original_filename].jpg`. This makes it visually distinct in Drive and preserves traceability to the original filename.

**4. 1Gi memory on Cloud Run (not 512Mi)**
The existing `etkm-backend` uses 512Mi. Pillow image processing (especially EXIF handling + JPEG encode) can spike memory with larger files. Set to 1Gi to avoid OOM kills during bulk backlog processing.

**5. Error Logger node is wired but optional**
The n8n workflow has an Error Logger HTTP node. If `N8N_ERROR_WEBHOOK_URL` is not set, remove that node before activating. It does not affect the happy path.

**6. Claude JSON parse is fault-tolerant**
The Code node strips markdown fences before parsing Claude's response. Claude occasionally wraps JSON in ```json blocks despite the prompt. The Code node handles this without failing the execution.

---

## Deviations from Spec

None. All pipeline steps, Notion fields, tags, and content use cases match the spec exactly.

---

## How to Deploy (Exact Steps)

1. **Nathan creates Drive folders** (5 min) — see `deployment-guide.md` Phase 1
2. **Nathan builds Notion database** (15 min) — see `notion/database-setup.md`
3. **Deploy Cloud Run service** (10 min) — see `deployment-guide.md` Phase 3
4. **Import and configure n8n workflow** (10 min) — see `deployment-guide.md` Phase 4
5. **Smoke test with 1 image** — verify full pipeline end-to-end
6. **Drop backlog** — 100 images into ingest folder, let pipeline run (~2 hours)

Total setup time: ~40 minutes of active work.

---

## Open Decisions (from spec — still pending Nathan)

- [ ] Confirm Notion parent page for Media Library database
- [ ] Approve tagging taxonomy as-is or adjust before running backlog
- [ ] Confirm Phase 1 approach: full pipeline (recommended) vs. manual session processing
- [ ] Decide if error webhook destination exists (Slack, email, or skip)

---

## Feeds Into

- **P4 Marketing** — n8n can query Notion library by tag when building campaign assets
- **P5 Content Production** — queryable by content_use_cases field
- **Future Social Media Engine** — tag `social-ready` is already in taxonomy; contrast/transparency rules go in the social engine, not here (per spec)
