# 07 — Assumptions

Every guess made during this spec, flagged so Nathan can confirm or correct
before code is written. Read first; resolve before build phase begins.

Each entry: what was assumed, why, what to do if wrong, urgency to resolve.

---

## RESOLVED — 2026-05-08

Nathan confirmed all 5 high-priority items plus 3 bonus improvements and 1 reduction. All resolutions below override the original assumption text. Spec docs (`01-architecture.md`, `02-ui-spec.md`, `05-ai-generator.md`) updated to match.

### Resolutions

| # | Item | Decision |
|---|---|---|
| **A1 / A16** | Single-platform per post / single-select Compose | **Multi-select platform with fan-out.** Compose form shows FB / IG / LI as checkboxes. One save creates N rows under a shared `post_group_id` (UUID), one row per ticked platform, all with the same scheduled time. Edit/delete actions operate on the group by default; per-platform overrides supported. |
| **A12** | Notion-mirrored 7-value Program tag dropdown | **Free-text Program / Topic field with 5 quick-fill buttons** (Adult Krav Maga, Women's Self-Defense, Youth Program, LE / Security, General). User can type anything else. No coupling to Notion's tag list. |
| **A14** | Re-authorization post-deploy | **Confirmed.** Documented in handoff; one-time ~5 minute task when the new Cloud Run hostname goes live. |
| **A20** | Subdirectory vs. separate repo | **Subdirectory `social-publishing/` in this repo.** Same gcloud commands, shared brand kit/skills, single source of truth for ETKM tooling. |

### Bonus improvements added (B1, B2, B3)

| # | Improvement | Spec'd in |
|---|---|---|
| **B1** | **Per-platform caption editing.** When 2+ platforms ticked, Compose shows a per-platform caption box for each. Master caption auto-fills all three; user can override per-platform. | `02-ui-spec.md` |
| **B2** | **AI "Tailor for X" buttons.** Click "Tailor for Instagram" → Claude rewrites the master caption with platform-appropriate length, hooks, and hashtag count. New endpoint `POST /api/ai/tailor-caption`. | `02-ui-spec.md`, `05-ai-generator.md` |
| **B3** | **Click empty calendar cell → Compose pre-filled with that date+time.** | `02-ui-spec.md` Calendar tab |

### Reduction

- **Batch Upload tab dropped from v1.** AI Generator + multi-select Compose cover the use cases. Underlying API endpoint (`POST /api/posts/batch`) kept for future automation but no UI tab. Saves ~half a day of build work. |

### Net build cost

| | Original spec | After resolution |
|---|---|---|
| Sessions to build | ~5 | ~7 |
| Pages in Scheduler | 5 tabs | 4 tabs (Calendar, All Posts, Compose, AI Generator) |
| Compose UX | Single-select platform | Multi-select with per-platform caption editing + AI Tailor |

---

The original assumption entries below are kept for audit. Items marked **RESOLVED** above override their original text.

---

## A1 — Single-platform per post (matches Manus)

**Assumed:** Each post row targets exactly one platform. Posts that should hit FB + IG + LI become three separate rows with the same caption.

**Why:** This matches the Manus All Posts screenshot — duplicate "Mental & Physical" entries for FB and IG with identical captions, slightly different timestamps. Suggests the Manus build fanned out at compose time.

**If wrong:** If you'd rather have one row that targets multiple platforms with one publish action, change `posts.platform` from a single ENUM to a JSON array of platforms, and update the publisher to fan out. ~1 day of additional work.

**Urgency:** **HIGH — answer before build.** The data model differs significantly between the two approaches.

---

## A2 — Multi-platform fan-out happens client-side, not server-side

**Assumed:** When Nathan ticks FB + IG in Compose (if multi-target is supported per A1 above), the App creates N rows, one per platform. The DB stores one row per row in the All Posts table — no joining or fan-out at publish time.

**Why:** Simpler data model. Each row has its own status, platform_post_id, error_message. Easy to retry one failed platform without affecting the others.

**If wrong:** Could move to one logical "post" with N platform-specific publish records. More normalized but more code.

**Urgency:** Medium. Depends on A1.

---

## A3 — SQLite on Cloud Storage FUSE mount is acceptable for v1

**Assumed:** Running SQLite on a `/data` mount backed by Cloud Storage FUSE gives us a single-file durable database with zero infra cost beyond Cloud Run.

**Why:** Single user, single writer, low write volume (16 posts/week). Postgres is overkill at this scale and adds $10+/month minimum.

**If wrong:** Postgres on Cloud SQL is the upgrade path. Existing models work as-is — change `DATABASE_URL` and run Alembic migrations.

**Risk:** Cloud Storage FUSE has higher latency than local disk. SQLite operations may be 10-50x slower than usual. For 16 writes/week this doesn't matter. If we ever batch-import 1000 rows it might.

**Urgency:** Low — easy migration if it bites.

---

## A4 — Cloud Run min-instances=1 keeps APScheduler warm

**Assumed:** Setting min-instances=1 on Cloud Run prevents the container from being torn down between requests, so the in-memory APScheduler thread keeps running and fires the publish job every 60 seconds.

**Why:** Cloud Run scales to zero by default. APScheduler is in-process. Without min=1, the scheduler thread dies during quiet periods and posts don't fire.

**If wrong:** If Cloud Run still recycles instances even with min=1 (rare but possible during deploys), we'd miss publish windows. Mitigation: add a Cloud Scheduler cron that pings `/health` every 60 seconds — that wakes the container and APScheduler picks up where it left off. Easy add.

**Urgency:** Medium. Verify in deploy. If problematic, add the Cloud Scheduler ping.

---

## A5 — Basic auth is enough for Nathan-only access

**Assumed:** A single `ADMIN_USER` / `ADMIN_PASS` env-var pair via HTTP Basic Auth gates every page. Nathan logs in once per browser session.

**Why:** Single user, internal tool, no multi-tenancy. CSRF, session management, OAuth-for-the-app-itself, etc. are all overkill.

**If wrong:** If we ever expose this externally or Nathan wants to give an assistant access, we add Flask-Login + a small users table. ~half a day.

**Urgency:** Low.

---

## A6 — Existing GCP project hosts the new Cloud Run service

**Assumed:** Deploy to `project-9c425f11-39e5-4743-b9d`, the same project that hosts `etkm-backend` per `SESSION_STATE.md`.

**Why:** Same billing account, same IAM, easy. Adds one Cloud Run service and one GCS bucket to the project.

**If wrong:** Spin up a new GCP project specifically for this app. Adds ~30 min of project creation + IAM setup. No technical reason to avoid it.

**Urgency:** Low.

---

## A7 — `etkm-social-media-assets` is the GCS bucket name

**Assumed:** Bucket name is descriptive, lowercase, hyphens. The name itself doesn't expose anything sensitive (bucket names are globally unique on GCS, but not publicly listed).

**Why:** Convention. Matches Cloud Storage naming rules.

**If wrong:** Pick a different name. Update `GCS_BUCKET` env var.

**Urgency:** Trivial.

---

## A8 — 200 MB video upload cap is sufficient

**Assumed:** No ETKM video will exceed 200 MB. A typical 90-second 1080p MP4 H.264 / AAC is 30-100 MB. Higher-quality 1440p Reels can hit 200 MB.

**Why:** This covers the IG Reels + FB Page Video use cases described in Notion's Content Type Master Reference.

**If wrong:** Cap can be raised to 1 GB easily — just increase the validation in `/api/media/sign-upload-url`. Above 1 GB requires resumable upload to GCS in chunks; not hard but adds a day of work.

**Urgency:** Low.

---

## A9 — `ffprobe` is available in the Cloud Run container

**Assumed:** The Dockerfile installs `ffmpeg` (which includes `ffprobe`) so the App can read video metadata (duration, dimensions, aspect ratio) at upload time without doing a full transcode.

**Why:** We need the metadata for the IG Reels aspect-ratio warning and to display in the Compose preview. `ffprobe` reads from a streaming HTTP source — we don't have to download the whole video first.

**If wrong:** Use Python-native `pymediainfo` instead. Less mature but no system dependency. Or skip server-side metadata extraction and trust client-side `<video>` element metadata events. Loses the upload-time validation.

**Urgency:** Low.

---

## A10 — Anthropic SDK uses `ANTHROPIC_API_KEY` from existing env

**Assumed:** Nathan already has an Anthropic API key configured in the ETKM environment (per `SESSION_STATE.md` and `backend/app.py`). The new Cloud Run service inherits or duplicates that env var.

**Why:** No new account creation needed; existing key works.

**If wrong:** Generate a separate API key scoped to this app and set `ANTHROPIC_API_KEY` on the new Cloud Run service. ~5 minutes.

**Urgency:** Trivial.

---

## A11 — Sonnet 4.6 is the right Claude model

**Assumed:** `claude-sonnet-4-6` is the right tier for AI campaign generation — fast, cheap, brand-voice-capable.

**Why:** Per CLAUDE.md model guidance ("default to the latest and most capable Claude models"), Sonnet 4.6 is the recommended general-purpose model. Opus 4.7 would be 5-10x the cost for marginal quality gain on short-form copy. Haiku would be cheaper but tighter on brand voice.

**If wrong:** Swap the model string in `ai_generator.py`. Trivial.

**Urgency:** Trivial.

---

## A12 — ETKM Program list is locked to the seven Notion options

**Assumed:** The Program / Topic dropdown in AI Generator and the Program Tag field share these seven values:
1. Adult Krav Maga
2. Women Self-Defense
3. Youth Program
4. LE / Security
5. Seminars
6. Fight Back ETX
7. General ETKM

**Why:** These come from the ETKM Social Calendar's `Program Tag` multi-select in Notion. Match to keep the App and Notion strategy doc consistent terminology.

**If wrong:** Edit the dropdown options in `02-ui-spec.md` and `05-ai-generator.md`. No code change.

**Urgency:** Trivial. Worth Nathan's quick confirmation.

---

## A13 — 16 posts/week cadence is the operational target

**Assumed:** The Publishing App is expected to handle ~16 posts/week (Phase 1: FB + IG only) growing to ~22/week in Phase 2 when LinkedIn enters. Per the Notion Weekly Post Template.

**Why:** Sets expectations on storage growth (~64 posts/month × ~50 KB media on avg = ~3 MB/month — trivial) and API rate limits (well below Meta + LinkedIn caps).

**If wrong:** Larger volume is fine — the architecture handles 100+/week without changes.

**Urgency:** Trivial.

---

## A14 — Nathan re-authorizes after deploy

**Assumed:** After the Publishing App goes live on Cloud Run, Nathan does a one-time re-authorize of LinkedIn and Meta against the new `LINKEDIN_REDIRECT_URI` (the new Cloud Run hostname). The existing Manus credentials don't carry over.

**Why:** OAuth redirect URIs are bound to specific hostnames. Manus's hostname is dead; new hostname needs new approval.

**If wrong:** N/A — there's no other path. Manus credentials cannot be transferred.

**Urgency:** Operational, post-deploy. Document in handoff notes.

---

## A15 — No video transcoding in v1

**Assumed:** The App accepts the MP4 H.264 / AAC that Nathan uploads and passes it to platforms as-is. If Nathan uploads a non-9:16 video to Instagram Reels, the App warns but doesn't auto-rotate or re-encode.

**Why:** Server-side video transcoding requires `ffmpeg` invocations on Cloud Run. Doable but slow and expensive. Adds 2-5 minutes per upload to CPU time and complicates the worker. Out of scope for v1.

**If wrong:** Add a transcode step at upload time (or as a background job after upload). ~3 days of work to do well.

**Urgency:** Low. The aspect-ratio warning + manual re-export by Nathan is sufficient.

---

## A16 — Compose form is single-platform; multi-platform happens via duplicate rows

**Assumed:** The Compose form's Platform dropdown is single-select. To post the same content to FB + IG + LI, Nathan saves three drafts. The All Posts table's "duplicate post" row action (added in v1) makes this a one-click operation per platform.

**Why:** Matches the Manus build (single-select platform per row). The duplicate action is a small ergonomic improvement.

**If wrong:** Change Platform to multi-select; on save, fan out to N rows per ticked platform. Adds ~half a day.

**Urgency:** Worth Nathan's call. Not urgent — can ship single-select v1, add multi-select v1.1.

---

## A17 — Calendar tab is the default landing on `/scheduler`

**Assumed:** Opening `/scheduler` lands on the Calendar tab because that's how the Manus build behaved.

**Why:** Visual overview is the most common reason to open the page.

**If wrong:** Change default to All Posts (more useful for triaging) or Compose (fastest path to creating a post). Trivial change.

**Urgency:** Trivial.

---

## A18 — All-or-nothing on Notion removal

**Assumed:** The Publishing App has zero Notion integration. No read, no write, no link, no display of Notion data.

**Why:** Per the architecture lock with Nathan. The Notion Social Calendar stays as a strategy reference document Nathan maintains by hand.

**If wrong:** If you'd like a small "reference card" on the Home page that links out to the Notion Social Calendar URL (no API integration, just a link), add it as a static HTML link. ~5 minutes.

**Urgency:** Trivial. Nathan to confirm — currently spec'd as zero Notion reference anywhere.

---

## A19 — Backend uses Flask, not FastAPI

**Assumed:** The new Publishing App is built on Flask 3.x to match the existing `etkm-backend` and the root `app.py` patterns in this repo.

**Why:** Consistency with existing infra. Both backends running Flask means shared conventions, no new framework to learn.

**If wrong:** FastAPI is the modern alternative — async-native, automatic OpenAPI docs, stricter typing. Switching to FastAPI is ~1-2 days of work but doesn't change the architecture.

**Urgency:** Low.

---

## A20 — Existing repo subdirectory `social-publishing/` is the build location

**Assumed:** The rebuilt app lives at `social-publishing/` in this repo, alongside `backend/`. Same monorepo, separate Cloud Run service.

**Why:** Keeps ETKM infrastructure in one place.

**If wrong:** Could split into a separate repo `easttxkravmaga/etkm-social-publishing`. Cleaner separation but two repos to maintain.

**Urgency:** Trivial. Nathan's call.

---

## Summary — gates before code starts

The five most important to resolve before build:

1. **A1** — single-platform per post (and therefore A2)
2. **A12** — confirm the 7 Program tag values
3. **A14** — confirm re-authorization is acceptable post-deploy
4. **A16** — single-select platform in Compose, or multi-select fan-out
5. **A20** — `social-publishing/` subdirectory or separate repo

Everything else can be defaulted to the assumption above and changed later without significant rework.

---

*End of spec — next is `output/handoff-notes.md` and `output/qa-report.md` per ETKM doctrine.*
