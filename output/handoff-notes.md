# Handoff Notes — ETKM Social Media Publishing App Rebuild Spec

**Session date:** 2026-05-08
**Branch:** `claude/reverse-engineer-oauth-scheduler-VzuAb`
**PR:** [#6 (draft)](https://github.com/easttxkravmaga/Claude/pull/6)

---

## What Nathan asked for

> Reverse-engineer this. https://etkmoauth-bmydy76p.manus.space/scheduler

The deployment was offline (`403 host_not_allowed` — Manus expired the app). Nathan provided 9 screenshots of the live build instead.

---

## What was built

**A complete reverse-engineering specification** for the rebuilt app, captured to `docs/scheduler-ref/`. Eight markdown files totaling ~1,840 lines that fully describe the Manus build's behavior, the corrected ETKM-branded rebuild, and every assumption that was made in the absence of source code.

### Files produced (with locations)

| Path | Purpose |
|---|---|
| `docs/scheduler-ref/README.md` | Index + locked decisions + document map |
| `docs/scheduler-ref/01-architecture.md` | Stack, data model, jobs, deploy target, media upload flow |
| `docs/scheduler-ref/02-ui-spec.md` | Page-by-page UI for all 5 pages and 5 sub-tabs |
| `docs/scheduler-ref/03-oauth.md` | LinkedIn (with `offline_access` fix) + Meta short→long token flows |
| `docs/scheduler-ref/04-storage-and-publishing.md` | GCS bucket setup, signed-URL upload, per-platform publishers including IG Reels multi-step and LinkedIn UGC asset upload |
| `docs/scheduler-ref/05-ai-generator.md` | Claude Sonnet 4.6 integration with ETKM brand-voice system prompt |
| `docs/scheduler-ref/06-bugs-and-brand-fixes.md` | 3 live-build bugs + 7 brand violations to correct |
| `docs/scheduler-ref/07-assumptions.md` | 20 flagged assumptions for Nathan to confirm before build |
| `output/qa-report.md` | Self-QC against 8 ETKM brand gates — all PASS |
| `output/handoff-notes.md` | This file |

---

## Key decisions made (and why)

### Decision 1 — Sequencing: spec doc first, then build

Reasoning: a full Cloud Run + Flask + GCS rebuild is a multi-session effort. Writing the spec first means the build session can execute deterministically without re-asking questions. Lower risk, no wasted code if assumptions miss.

### Decision 2 — Deploy target: Google Cloud Run, `us-central1`

Reasoning: matches the existing `etkm-backend` infra (per `SESSION_STATE.md`). Same project (`project-9c425f11-39e5-4743-b9d`), same region, same deploy pattern.

### Decision 3 — App name: ETKM Social Media Publishing App

Reasoning: confirmed during the session by reading the **ETKM Social Media System Consolidation Record** in Notion (`358924c8-1673-81b7-a6d1-c944dc3a2f88`, dated May 6, 2026). That doc explicitly names the rebuild "**ETKM Publishing App**". Nathan confirmed the full name as "ETKM Social Media Publishing App". The Manus-era branding ("OAuth Manager", "Social Agent") is retired.

### Decision 4 — Source of truth for posts: the App's own database, NOT Notion

Reasoning: this was the biggest pivot in the session. Initially I recommended using Notion as the source of truth (since the ETKM Social Calendar database was already populated and consolidated). Nathan clarified that:
- He composed posts in the Manus app, not in Notion
- The Manus build's Notion sync errored on every row but posts still went out
- Notion was a broken side-channel, not the publish path

So the rebuild removes Notion entirely. The Notion Social Calendar stays as a strategy reference document; the App ignores it. This is a major simplification over both the Manus version (which tried to dual-write) and my initial recommendation.

### Decision 5 — Media files in Google Cloud Storage

Reasoning: Cloud Run's 32 MB request body limit can't accept video uploads directly. Browser-direct-to-GCS via signed PUT URL bypasses the limit. Also: GCS is cheap (~$0.02/GB/month) and same auth surface as Cloud Run.

### Decision 6 — Video upload supported

Reasoning: Nathan asked. Spec'd MP4 H.264 / AAC up to 200 MB (covers any ETKM Reel or Page Video format). Instagram Reels handled via the multi-step container/poll/publish flow with a `processing` status during the encoding wait.

### Decision 7 — AI Generator wired to Claude Sonnet 4.6

Reasoning: the Manus build had an AI Generator tab; Nathan wants to keep it. Sonnet 4.6 is the right tier per CLAUDE.md guidance (Opus too expensive for short-form copy, Haiku too constrained on brand voice). Prompt caching wired in to drop input cost ~95%.

### Decision 8 — No video transcoding in v1

Reasoning: server-side transcoding requires `ffmpeg` invocations and adds 2-5 min per upload. Out of scope for v1. Instead, the Compose form warns when uploading a non-9:16 video to Instagram (the gotcha). Nathan re-exports manually if needed.

---

## Deviations from the original Manus build

The rebuild is **not** a pixel-perfect port. Documented deviations:

| Manus had | Rebuild has |
|---|---|
| Light beige hero card on Home | Black status panel showing OAuth health, queue depth, last published |
| Mid-gray header bar | True black `#000000` |
| Plaintext OAuth tokens in Dashboard | Fernet-encrypted at rest, masked-by-default UI |
| LinkedIn token without `offline_access` (token died at 60 days) | `offline_access` scope requested; refresh tokens issued |
| Notion column on All Posts (every row error) | Removed entirely |
| IG publish without container-status polling (Easter post bug) | 3-step flow with poll-until-FINISHED and timeout handling |
| "Made with Manus" floating watermark | Removed |
| Inconsistent app name (header vs H1) | Single name: ETKM Social Media Publishing App |
| "Save credentials to .env file" copy | "Credentials are saved encrypted" |
| No video upload | MP4 H.264 / AAC up to 200 MB, browser-direct-to-GCS |
| Image upload only via direct POST | Image direct (≤ 20 MB) + Video signed-URL (≤ 200 MB) |

---

## What's pending — Nathan's gates before build

`07-assumptions.md` flags 20 items. Five are high-priority and need Nathan's confirmation before code starts:

1. **A1 — Single-platform per post.** The data model has `posts.platform` as a single ENUM (matches the Manus build). If Nathan wants one row to target multiple platforms with one publish action, change to a JSON array; ~1 day of additional work.
2. **A12 — The 7 ETKM Program tag values.** The AI Generator dropdown and Compose form use these. Pulled from Notion's `Program Tag` multi-select. Confirm or amend.
3. **A14 — Re-authorization post-deploy.** Existing Manus OAuth credentials cannot be migrated — they're bound to the dead Manus hostname. Nathan must re-authorize LinkedIn and Meta against the new Cloud Run hostname after deploy.
4. **A16 — Single-select vs. multi-select platform in Compose.** Currently spec'd as single-select with a "duplicate post" row action. Easy to change.
5. **A20 — `social-publishing/` subdirectory or separate repo?** Currently spec'd as a subdirectory in this monorepo, alongside `backend/`.

The other 15 assumptions can default to the spec'd value and be changed later without significant rework.

---

## How to use these docs (deploy steps)

When the spec is approved and the build phase begins:

### Phase B — GCP infra prep (~30 min)

```bash
# Set project
gcloud config set project project-9c425f11-39e5-4743-b9d

# Create GCS bucket
gcloud storage buckets create gs://etkm-social-media-assets \
  --location=us-central1 \
  --uniform-bucket-level-access

# Apply CORS policy (see 04-storage-and-publishing.md for exact JSON)
gcloud storage buckets update gs://etkm-social-media-assets \
  --cors-file=cors.json

# Set lifecycle (delete after 365 days)
gcloud storage buckets update gs://etkm-social-media-assets \
  --lifecycle-file=lifecycle.json

# Create service account
gcloud iam service-accounts create etkm-social-publishing \
  --display-name="ETKM Social Publishing App"

# Grant bucket access
gcloud storage buckets add-iam-policy-binding gs://etkm-social-media-assets \
  --member="serviceAccount:etkm-social-publishing@<project>.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

### Phase C-H — Build (multi-session)

Implementation follows `01-architecture.md` directory layout. Build in order:
1. Models + migrations (`models.py`, `migrations/`)
2. OAuth modules (`auth/linkedin.py`, `auth/meta.py`)
3. Templates + static (`templates/`, `static/css/etkm.css`)
4. Media upload + publishers (`media/`, `publishers/`)
5. AI generator (`ai_generator.py`)
6. APScheduler jobs (`jobs.py`)
7. Flask entry + routing (`app.py`)
8. Dockerfile + requirements

### Phase I — Cloud Run deploy

```bash
cd social-publishing/

gcloud run deploy etkm-social-publishing \
  --source . \
  --region us-central1 \
  --service-account etkm-social-publishing@<project>.iam.gserviceaccount.com \
  --min-instances 1 \
  --max-instances 1 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --set-env-vars="GCS_BUCKET=etkm-social-media-assets,GCS_PROJECT_ID=<project>" \
  --set-secrets="APP_SECRET_KEY=app-secret-key:latest,ADMIN_PASS=admin-pass:latest,ANTHROPIC_API_KEY=anthropic-api-key:latest"
```

### Phase J — Re-authorization (Nathan)

After deploy succeeds:
1. Visit `https://etkm-social-publishing-XXXXX.us-central1.run.app/linkedin`
2. Paste LinkedIn Client ID + Secret (regenerate from LinkedIn Developer Portal if old)
3. **CRITICAL:** Update redirect URI in LinkedIn Developer Portal to match the new Cloud Run hostname
4. **CRITICAL:** Confirm `offline_access` is selected in the LinkedIn app's OAuth 2.0 settings
5. Click Authorize → LinkedIn consent → returns to Dashboard with green "Active" status
6. Visit `/meta`, paste App ID + App Secret + new short-lived token from Graph API Explorer, click Exchange
7. Confirm Dashboard shows green "Active" / "Never expires" for both providers
8. Test with one scheduled post on each platform before going live with 16 posts/week

---

## Open items / future work

These are deliberately out of scope for v1 but worth noting:

- **Multi-image carousel posts** (Instagram up to 10) — defer to v1.1
- **Stories posting** (different API surface) — defer to v2
- **Video transcoding** (server-side ffmpeg) — defer to v2 if aspect-ratio warnings prove insufficient
- **Engagement analytics** (post likes/comments/shares) — defer to v2
- **Multi-user / role-based auth** — only if Nathan adds an assistant
- **Postgres migration** — only if SQLite latency on Cloud Storage FUSE becomes a problem
- **Webhook receivers for platform events** — only if real-time post-status updates become valuable

---

## How to run / verify the spec docs

Spec docs are markdown — open them directly:

```bash
cd docs/scheduler-ref/
ls
# README.md  01-architecture.md  02-ui-spec.md  03-oauth.md
# 04-storage-and-publishing.md  05-ai-generator.md
# 06-bugs-and-brand-fixes.md  07-assumptions.md
```

Or browse on GitHub:
- https://github.com/easttxkravmaga/Claude/tree/claude/reverse-engineer-oauth-scheduler-VzuAb/docs/scheduler-ref

QA report is at `output/qa-report.md`. All 8 ETKM brand gates passed.

---

## Reporting summary

| Metric | Value |
|---|---|
| Spec docs produced | 8 markdown files |
| Total spec content | ~1,840 lines |
| Bugs identified in live Manus build | 3 (LinkedIn refresh, Notion sync, Easter IG post) |
| Brand violations identified | 7 (mid-gray header, light hero card, Manus watermark, plaintext tokens, etc.) |
| Architectural decisions locked | 8 (with reasoning) |
| Assumptions flagged for Nathan's review | 20 (5 high-priority) |
| Brand gates passed | 8/8 |
| Build phases queued | 9 (B through J) |
| Estimated cost when live | ~$5-10/month (Cloud Run + GCS + Anthropic) |

---

*Handoff notes — version 1.0 — 2026-05-08*
*Next: Nathan reviews `07-assumptions.md`, signs off on the 5 high-priority items, and the build phase begins.*
