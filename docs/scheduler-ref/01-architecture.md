# 01 — Architecture

The stack, data model, background jobs, media handling, and deploy target for
the **ETKM Social Media Publishing App**. Implementation-ready.

---

## Stack

| Layer | Choice | Why |
|---|---|---|
| **Language** | Python 3.12 | Matches existing ETKM backend (`backend/app.py`) |
| **Web framework** | Flask 3.x | Same as existing ETKM backend; minimal surface area; Jinja built in |
| **ORM** | SQLAlchemy 2.x | Standard with Flask; DB-portable so we can move SQLite → Postgres later without rewriting models |
| **Database (v1)** | SQLite via Cloud Storage FUSE mount at `/data/publishing.db` | Single user (Nathan), single writer, durable on restart, zero infra cost |
| **Templates** | Jinja2 (server-rendered) | Matches the Manus-built original; no SPA needed; fewer moving parts |
| **Frontend JS** | Vanilla JS + Alpine.js for tab state + FullCalendar.js v6 for the calendar grid | No bundler step; libraries self-hosted in `static/vendor/` per ETKM "no external CDN" rule |
| **CSS** | Hand-rolled in `static/css/etkm.css` (one file) | ETKM brand kit is small enough to express in ~200 lines; avoids framework bloat |
| **Background jobs** | APScheduler 3.x (BackgroundScheduler) | Single-process; survives Cloud Run cold starts via min-instances=1 |
| **HTTP client** | `requests` for outbound API calls (LinkedIn, Meta, Anthropic, GCS) | Standard, already in `backend/app.py` |
| **Object storage** | Google Cloud Storage (`google-cloud-storage` SDK) | Same project as Cloud Run; signed URLs let browser upload direct to bucket and let platforms download for publish |
| **AI** | Anthropic Python SDK (`anthropic`) calling Claude Sonnet 4.6 (`claude-sonnet-4-6`) | Per CLAUDE.md model guidance |
| **Encryption at rest** | `cryptography` Fernet, keyed by `APP_SECRET_KEY` | OAuth tokens stored encrypted (Manus stored them in plaintext) |
| **Auth on the admin pages** | HTTP Basic Auth gated by `ADMIN_USER` / `ADMIN_PASS` env vars | Internal tooling for Nathan only — single password header is fine for v1 |

---

## Data model — three tables

SQLAlchemy declarative.

### `oauth_credentials`

One row per connected social account.

| Column | Type | Notes |
|---|---|---|
| `id` | INT PK | |
| `provider` | ENUM(`linkedin`, `meta`) | |
| `label` | VARCHAR(120) | "ETKM LinkedIn", "ETKM Meta" — shown on Dashboard |
| `client_id` | VARCHAR(255) | Developer App's Client ID / App ID |
| `client_secret_enc` | TEXT | Fernet-encrypted |
| `access_token_enc` | TEXT | Fernet-encrypted |
| `refresh_token_enc` | TEXT NULL | Fernet-encrypted. Null when provider doesn't issue one (Meta long-lived Page tokens never expire). |
| `expires_at` | TIMESTAMPTZ NULL | Null = "never expires" |
| `person_urn` | VARCHAR(255) NULL | LinkedIn-only: `urn:li:person:XXX` — required as `author` on UGC posts |
| `page_id` | VARCHAR(64) NULL | Meta-only: Facebook Page ID |
| `ig_account_id` | VARCHAR(64) NULL | Meta-only: Instagram Business Account ID |
| `last_refresh_at` | TIMESTAMPTZ NULL | |
| `last_refresh_status` | ENUM(`success`, `failed`, `pending`) NULL | |
| `last_refresh_error` | TEXT NULL | Stored only on failure |
| `created_at` | TIMESTAMPTZ DEFAULT now() | |
| `updated_at` | TIMESTAMPTZ DEFAULT now() | |

Index: `(provider, label)` unique.

### `posts`

One row per scheduled or published post. A row that targets multiple platforms
(e.g. FB + IG) creates one row per platform on save, all sharing a common
`post_group_id`. Group-level edit/delete operations affect all rows in the
group; per-platform overrides are supported via the per-row `caption` field.

| Column | Type | Notes |
|---|---|---|
| `id` | INT PK | |
| `post_group_id` | UUID | Shared by all platform rows created from one Compose save. Generated server-side on insert. Indexed. Even single-platform posts get a group ID for future-proofing. |
| `title` | VARCHAR(200) | Internal title — never published |
| `caption` | TEXT | Post body. FB cap ~63,206 chars; IG cap 2,200; LI cap 3,000. Compose UI validates. Each row's caption may differ if user used per-platform override (B1). |
| `platform` | ENUM(`facebook`, `instagram`, `linkedin`) | |
| `media_type` | ENUM(`none`, `image`, `video`) DEFAULT `none` | |
| `media_gcs_path` | VARCHAR(2048) NULL | `gs://etkm-social-media-assets/<filename>` — internal reference |
| `media_mime` | VARCHAR(64) NULL | `image/png`, `image/jpeg`, `image/gif`, `image/webp`, `video/mp4` |
| `media_size_bytes` | BIGINT NULL | Stored at upload for Compose UI display |
| `media_duration_sec` | INT NULL | Video duration; populated client-side at upload |
| `media_aspect_ratio` | VARCHAR(8) NULL | e.g. `9:16`, `16:9`, `1:1` — used by IG Reels warning logic |
| `scheduled_at` | TIMESTAMPTZ NULL | Null = unscheduled draft |
| `campaign_tag` | VARCHAR(120) NULL | Free-text tag (e.g. `fight-back-march-2026`) — indexed |
| `status` | ENUM(`draft`, `scheduled`, `posting`, `processing`, `posted`, `failed`) | `processing` is the post-upload-pre-publish state for IG Reels (encoding wait) |
| `approved` | BOOLEAN DEFAULT false | Auto-publish requires `approved=true AND status='scheduled' AND scheduled_at <= now()` |
| `platform_post_id` | VARCHAR(255) NULL | Returned ID after successful publish; powers "View post" link |
| `error_message` | TEXT NULL | Last error from the platform API |
| `retry_count` | INT DEFAULT 0 | Incremented on failure; max 3 retries before manual intervention |
| `batch_id` | INT NULL FK → `batches.id` | Set only when imported via Batch Upload |
| `created_at` | TIMESTAMPTZ DEFAULT now() | |
| `updated_at` | TIMESTAMPTZ | |
| `posted_at` | TIMESTAMPTZ NULL | When publish actually succeeded |

Indexes: `(status, scheduled_at)`, `(campaign_tag)`, `(platform, posted_at)`, `(post_group_id)`.

### `batches`

One row per CSV/XLSX import or AI-generated batch.

| Column | Type | Notes |
|---|---|---|
| `id` | INT PK | |
| `name` | VARCHAR(200) | "March 2026 Campaign" |
| `source` | ENUM(`csv`, `xlsx`, `manual`, `ai`) | |
| `row_count` | INT | |
| `created_at` | TIMESTAMPTZ DEFAULT now() | |

---

## Media upload flow

**Why this matters:** Cloud Run has a 32 MB request size limit. Videos
routinely exceed that. The browser must upload directly to GCS, bypassing
Cloud Run.

### Image upload (≤ 20 MB) — direct to App

1. User drops image in Compose form
2. Browser POSTs `multipart/form-data` to `/api/media/upload-image`
3. Flask receives, validates MIME, writes to GCS via SDK, returns `{gcs_path, mime, size}`
4. Compose form stores the values in hidden inputs

### Video upload (≤ 200 MB) — signed URL, browser-direct-to-GCS

1. User drops video in Compose form
2. Browser POSTs `{filename, content_type, size}` to `/api/media/sign-upload-url`
3. Flask returns `{upload_url, gcs_path}` — a 15-minute signed PUT URL
4. Browser uploads the video file via PUT directly to that URL (multipart-resumable for files >50MB)
5. Browser POSTs `{gcs_path}` to `/api/media/finalize` to confirm
6. Flask reads the GCS object's metadata, returns `{gcs_path, mime, size, duration, aspect_ratio}`

GCS bucket configuration:
- Name: `etkm-social-media-assets`
- Location: `us-central1` (same region as Cloud Run)
- Uniform bucket-level access enabled
- Service account: Cloud Run service account has `roles/storage.objectAdmin` on this bucket only
- Lifecycle rule: delete objects after 365 days (cost control; posted media older than a year is rarely re-fetched)

---

## Routes — overview

Detailed UI behavior per page is in `02-ui-spec.md`. Detailed publish flows are in `04-storage-and-publishing.md`.

### Page routes (HTML, server-rendered, basic-auth gated)

| Method | Path | Renders |
|---|---|---|
| GET | `/` | Home / status |
| GET | `/scheduler` | Scheduler shell, Calendar tab default |
| GET | `/scheduler?tab=all` | All Posts tab |
| GET | `/scheduler?tab=compose` | Compose tab |
| GET | `/scheduler?tab=compose&date=YYYY-MM-DDTHH:MM` | Compose tab pre-filled with that scheduled time (B3 — clicking an empty calendar cell links here) |
| GET | `/scheduler?tab=ai` | AI Generator tab |
| GET | `/linkedin` | LinkedIn setup wizard |
| GET | `/meta` | Meta setup wizard |
| GET | `/dashboard` | Credential Dashboard |

Note: `/scheduler?tab=batch` was in the original spec but the Batch Upload tab is dropped from v1. The underlying batch import API (`POST /api/posts/batch`) is retained for future automation.

### API routes (JSON, basic-auth gated)

| Method | Path | Purpose |
|---|---|---|
| **Posts** | | |
| GET | `/api/posts` | List. Query: `?platform=&status=&campaign_tag=&group_id=&limit=&offset=` |
| POST | `/api/posts` | Create. Body: `{title, master_caption, platforms: ["facebook", "instagram"], per_platform_captions: {instagram: "..."}, ...}`. Server creates one row per platform with the master caption (or per-platform override if provided), all sharing a generated `post_group_id`. Returns the group ID and the array of created rows. |
| GET | `/api/posts/<id>` | Read one row |
| GET | `/api/posts/group/<group_id>` | Read all rows in a group |
| PATCH | `/api/posts/<id>` | Edit one row only |
| PATCH | `/api/posts/group/<group_id>` | Edit all rows in a group at once (e.g. reschedule the whole group) |
| DELETE | `/api/posts/<id>` | Delete one row only |
| DELETE | `/api/posts/group/<group_id>` | Delete all rows in a group |
| POST | `/api/posts/<id>/publish` | Publish immediately, regardless of `scheduled_at` |
| POST | `/api/posts/<id>/approve` | `approved=true` |
| POST | `/api/posts/<id>/retry` | Reset `status=scheduled` and clear `error_message` for retry |
| POST | `/api/posts/batch` | (Retained for future automation; no UI tab in v1.) Multi-row CSV/XLSX import. Body: `{name, rows:[...]}`. Media URLs must be public HTTPS URLs. |
| **Media** | | |
| POST | `/api/media/upload-image` | Direct image upload to GCS (≤ 20 MB) |
| POST | `/api/media/sign-upload-url` | Signed PUT URL for video upload |
| POST | `/api/media/finalize` | Post-upload metadata read |
| **AI Generator** | | |
| POST | `/api/ai/generate-campaign` | Body shape in `05-ai-generator.md`. Creates N draft posts per platform. |
| POST | `/api/ai/tailor-caption` | (B2) Body: `{master_caption, target_platform: "facebook"\|"instagram"\|"linkedin", program?, tone?}`. Returns a platform-tailored rewrite. Used by the "Tailor for X" buttons in Compose. Detail in `05-ai-generator.md`. |
| **OAuth — LinkedIn** | | |
| GET | `/api/oauth/linkedin/authorize` | 302 → LinkedIn consent screen with `offline_access` scope |
| GET | `/api/oauth/linkedin/callback` | Code exchange, store credentials |
| **OAuth — Meta** | | |
| POST | `/api/oauth/meta/exchange` | Body: `{app_id, app_secret, short_lived_token}`. Returns long-lived Page token, stores credentials. |
| **Credentials** | | |
| GET | `/api/credentials` | Dashboard list |
| POST | `/api/credentials/<id>/refresh` | Manual token refresh |
| DELETE | `/api/credentials/<id>` | Delete |
| **Background scheduler** | | |
| GET | `/api/scheduler/status` | `{busy: bool, next_token_refresh_at, next_publish_check_at}` — drives the orange "Scheduler busy" pill |
| **Health** | | |
| GET | `/health` | Cloud Run probe; unauthenticated; lightweight |

---

## Background jobs

Two APScheduler jobs.

### Job 1 — Token refresh sweep

- **Cadence:** every 6 hours
- **Action:**
  1. Find `oauth_credentials` where `expires_at IS NOT NULL AND expires_at < now() + interval '7 days'`
  2. For each:
     - **LinkedIn:** if `refresh_token_enc` exists, POST `https://www.linkedin.com/oauth/v2/accessToken` with `grant_type=refresh_token`. Update `access_token_enc`, `expires_at`, `last_refresh_*`.
     - **Meta long-lived Page tokens:** never expire. Skip.
  3. On missing refresh token: write `last_refresh_status='failed'` with error "No refresh token available — re-authorize required." Dashboard surfaces this loudly.

### Job 2 — Post publisher

- **Cadence:** every 60 seconds
- **Action:**
  1. Find posts where `status='scheduled' AND approved=true AND scheduled_at <= now()`
  2. For each, set `status='posting'` and dispatch to the platform-specific publisher (see `04-storage-and-publishing.md`)
  3. Image posts complete in one round-trip — set `status='posted'` and `platform_post_id`
  4. Instagram Reels need a multi-step flow: after upload, set `status='processing'` and re-check status every 30 seconds. When IG returns `FINISHED`, call `media_publish` and set `status='posted'`.
  5. On failure: increment `retry_count`. If `< 3`, leave `status='scheduled'` for next cycle. If `>= 3`, set `status='failed'` and write `error_message`. No further auto-retry — Nathan retries from UI.

### Scheduler-busy indicator

In-memory flag set during Job 1 or Job 2 execution. Dashboard polls
`/api/scheduler/status` every 30 seconds.

---

## Deploy target — Cloud Run

| Setting | Value |
|---|---|
| Project | `project-9c425f11-39e5-4743-b9d` |
| Region | `us-central1` |
| Service name | `etkm-social-publishing` |
| Memory | 512 MiB |
| CPU | 1 |
| Min instances | 1 (keeps APScheduler warm) |
| Max instances | 1 (single SQLite writer) |
| Port | 8080 |
| Timeout | 300s |
| Concurrency | 80 |
| Service account | `etkm-social-publishing@<project>.iam.gserviceaccount.com` with `roles/storage.objectAdmin` on the GCS bucket only |

### Repo subdirectory layout

```
social-publishing/
├── Dockerfile
├── requirements.txt
├── app.py                  # Flask entry
├── models.py               # SQLAlchemy
├── jobs.py                 # APScheduler tasks
├── auth/
│   ├── linkedin.py
│   └── meta.py
├── publishers/
│   ├── facebook.py
│   ├── instagram.py
│   └── linkedin.py
├── media/
│   ├── upload.py           # GCS direct + signed URL
│   └── inspect.py          # MIME, size, duration, aspect ratio
├── ai_generator.py
├── templates/              # Jinja
├── static/
│   ├── css/etkm.css
│   ├── js/
│   └── vendor/             # FullCalendar, Alpine self-hosted
└── migrations/             # Alembic
```

### Required env vars

| Var | Purpose |
|---|---|
| `APP_SECRET_KEY` | Flask session key + Fernet key for encrypted credentials |
| `ADMIN_USER` | Basic auth username |
| `ADMIN_PASS` | Basic auth password |
| `DATABASE_URL` | `sqlite:////data/publishing.db` (v1) |
| `LINKEDIN_REDIRECT_URI` | `https://etkm-social-publishing-XXX.us-central1.run.app/api/oauth/linkedin/callback` |
| `ANTHROPIC_API_KEY` | Already exists in ETKM env |
| `GCS_BUCKET` | `etkm-social-media-assets` |
| `GCS_PROJECT_ID` | `project-9c425f11-39e5-4743-b9d` |

### Outbound APIs

- LinkedIn: `api.linkedin.com`, `www.linkedin.com/oauth/v2/*`
- Meta: `graph.facebook.com/v19.0`
- Anthropic: `api.anthropic.com/v1/messages`
- GCS: `storage.googleapis.com`

All reachable from default Cloud Run egress. No VPC connector needed.

---

## Security notes

- OAuth tokens encrypted at rest with Fernet (Manus stored them plaintext, visible in Dashboard screenshots).
- Basic auth gates every page except `/health`.
- No CSRF in v1 — Nathan is the only user, single tenant. If externalized, add Flask-WTF.
- GCS bucket private with uniform access; public reads only via short-lived signed URLs (10-minute TTL) handed to platforms at publish time.
- Signed upload URLs scoped to a single GCS object path with a 15-minute TTL.
- LinkedIn redirect URI bound to the exact Cloud Run hostname — rotate on hostname change.

---

## What changed from v1.0 of this doc

- Renamed throughout: ETKM Social Agent → ETKM Social Media Publishing App
- Removed all Notion fields from `posts` (the broken Manus sync is gone, not rebuilt)
- Removed `notion_sync` route and `NOTION_*` env vars
- Added `media_type`, `media_gcs_path`, `media_mime`, `media_size_bytes`, `media_duration_sec`, `media_aspect_ratio` to `posts`
- Added `processing` status for IG Reels encoding wait
- Added media upload flow (direct image, signed-URL video)
- Added GCS bucket config + service account binding
- Added retry counter on `posts`

---

*Next: `02-ui-spec.md` — page-by-page UI captured from screenshots, retitled for the new app name.*
