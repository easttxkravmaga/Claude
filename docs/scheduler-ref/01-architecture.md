# 01 — Architecture

The stack, data model, background jobs, and deploy target for the rebuild.
Implementation-ready.

---

## Stack

| Layer | Choice | Why |
|---|---|---|
| **Language** | Python 3.12 | Matches existing ETKM backend (`backend/app.py`) |
| **Web framework** | Flask 3.x | Same as existing ETKM backend; minimal surface area; Jinja templating built in |
| **ORM** | SQLAlchemy 2.x | Standard with Flask; DB-portable so we can move SQLite → Postgres later without rewriting models |
| **Database (v1)** | SQLite via Cloud Run volume *or* Cloud SQL Postgres | See "Database choice" below |
| **Templates** | Jinja2 (server-rendered) | Matches Manus-built original; no SPA needed; fewer moving parts |
| **Frontend JS** | Vanilla JS + Alpine.js for tab state + FullCalendar.js v6 for the calendar grid | No bundler step; CDN imports allowed at the document level (we'll self-host the lib files in `static/vendor/` so the page itself follows ETKM "no external CDN" rule for self-contained outputs) |
| **CSS** | Hand-rolled CSS in `static/css/etkm.css` (one file). No Tailwind, no Bootstrap. | ETKM brand kit is small enough to express in ~200 lines of CSS; avoids framework bloat and class soup |
| **Background jobs** | APScheduler 3.x (BackgroundScheduler) | Single-process scheduler runs in the Flask app; survives Cloud Run cold starts via the `/health` keep-alive endpoint |
| **HTTP client** | `requests` for outbound API calls (LinkedIn, Meta, Notion, Anthropic) | Standard, already a dependency in `backend/app.py` |
| **AI** | Anthropic Python SDK (`anthropic`) calling Claude Sonnet 4.6 (`claude-sonnet-4-6`) by default | Per CLAUDE.md model guidance |
| **Auth on the admin pages** | HTTP Basic Auth gated by `ADMIN_USER` / `ADMIN_PASS` env vars | This is internal tooling for Nathan only. Don't over-engineer. Cloud Run + a single password header is fine for v1. |

### Database choice

Two options. Pick one before build:

**Option 1 — SQLite on a Cloud Run volume (recommended for v1)**
- Pro: zero infra, zero cost beyond Cloud Run, file-level backups trivial
- Con: single-instance only; no concurrent writers across replicas
- Con: Cloud Run filesystem is ephemeral by default — needs a Cloud Storage FUSE mount or a 2nd-gen volume
- Verdict: fine for v1. Nathan is the only user. Concurrency is one writer.

**Option 2 — Cloud SQL Postgres (recommended for v2)**
- Pro: durable, multi-instance, point-in-time recovery
- Con: ~$10/mo minimum even on db-f1-micro
- Verdict: defer to v2 unless v1 actually outgrows SQLite

Recommendation: ship v1 on SQLite with a Cloud Storage FUSE mount at
`/data/etkm-social.db`. Migrate to Postgres only if and when concurrency
or durability become real problems.

---

## Data model

Three tables. SQLAlchemy declarative.

### `oauth_credentials`

One row per connected social account.

| Column | Type | Notes |
|---|---|---|
| `id` | INT PK | |
| `provider` | ENUM(`linkedin`, `meta`) | |
| `label` | VARCHAR(120) | e.g. "ETKM LinkedIn", "ETKM Meta" — shown on Dashboard |
| `client_id` | VARCHAR(255) | App's developer Client ID / App ID |
| `client_secret_enc` | TEXT | Encrypted at rest with `Fernet(key=APP_SECRET_KEY)` |
| `access_token_enc` | TEXT | Encrypted |
| `refresh_token_enc` | TEXT NULL | Encrypted. Null if provider doesn't issue one (or for Meta long-lived Page tokens, which never expire and don't need a refresh token). |
| `expires_at` | TIMESTAMPTZ NULL | Null = "never expires" (Meta long-lived Page token case) |
| `person_urn` | VARCHAR(255) NULL | LinkedIn-only: e.g. `urn:li:person:XXX` — needed as the `author` field on UGC posts |
| `page_id` | VARCHAR(64) NULL | Meta-only: Facebook Page ID |
| `ig_account_id` | VARCHAR(64) NULL | Meta-only: Instagram Business Account ID |
| `last_refresh_at` | TIMESTAMPTZ NULL | |
| `last_refresh_status` | ENUM(`success`, `failed`, `pending`) NULL | |
| `last_refresh_error` | TEXT NULL | Stored only on failure |
| `created_at` | TIMESTAMPTZ DEFAULT now() | |
| `updated_at` | TIMESTAMPTZ DEFAULT now() | Auto-updated on save |

Indexes: `(provider, label)` unique.

### `posts`

One row per scheduled or published post. Three platform-specific posts (FB, IG, LI) for the same content = three rows. This matches the live build's All Posts view, which shows the same caption replicated per platform.

| Column | Type | Notes |
|---|---|---|
| `id` | INT PK | |
| `title` | VARCHAR(200) | Internal title — never published. e.g. "FB — Women's Program Launch" |
| `caption` | TEXT | The actual post body. FB cap ~63,206 chars; IG cap 2,200; LI cap 3,000. Validated in Compose UI. |
| `platform` | ENUM(`facebook`, `instagram`, `linkedin`) | |
| `media_url` | VARCHAR(2048) NULL | Cloud Storage public URL for the image. Required for IG. Optional for FB and LI. |
| `media_mime` | VARCHAR(64) NULL | `image/png`, `image/jpeg`, `image/gif`, `image/webp` |
| `scheduled_at` | TIMESTAMPTZ NULL | Null = unscheduled draft |
| `campaign_tag` | VARCHAR(120) NULL | Free-text tag used to group posts (e.g. `fight-back-march-2026`). Indexed. |
| `status` | ENUM(`draft`, `scheduled`, `posting`, `posted`, `failed`) | |
| `approved` | BOOLEAN DEFAULT false | Posts only auto-publish when `approved=true AND status='scheduled' AND scheduled_at <= now()` |
| `platform_post_id` | VARCHAR(255) NULL | Returned ID after successful publish. Used to build `View post` link. |
| `error_message` | TEXT NULL | Last error from the Graph API / LinkedIn API |
| `notion_page_id` | VARCHAR(64) NULL | Set after Notion sync succeeds |
| `notion_sync_status` | ENUM(`pending`, `synced`, `error`, `disabled`) DEFAULT `pending` | |
| `notion_sync_error` | TEXT NULL | |
| `sync_to_notion` | BOOLEAN DEFAULT true | Per-post override; defaults to true for v1 |
| `batch_id` | INT NULL FK → `batches.id` | Set only when imported via Batch Upload |
| `created_at` | TIMESTAMPTZ DEFAULT now() | |
| `updated_at` | TIMESTAMPTZ | |
| `posted_at` | TIMESTAMPTZ NULL | When publish actually succeeded |

Indexes: `(status, scheduled_at)`, `(campaign_tag)`, `(platform, posted_at)`.

### `batches`

One row per CSV/XLSX import.

| Column | Type | Notes |
|---|---|---|
| `id` | INT PK | |
| `name` | VARCHAR(200) | "March 2026 Campaign" |
| `source` | ENUM(`csv`, `xlsx`, `manual`, `ai`) | |
| `row_count` | INT | |
| `created_at` | TIMESTAMPTZ DEFAULT now() | |

---

## Routes — overview

Full request/response shapes are in `03-oauth.md` for auth routes and
inline below for the rest. Detailed UI behavior per page is in `02-ui-spec.md`.

### Page routes (HTML, server-rendered)

| Method | Path | Renders | Auth |
|---|---|---|---|
| GET | `/` | Home | Basic auth |
| GET | `/scheduler` | Scheduler shell with calendar tab default | Basic auth |
| GET | `/scheduler?tab=all` | Scheduler with All Posts tab active | Basic auth |
| GET | `/scheduler?tab=compose` | Compose tab | Basic auth |
| GET | `/scheduler?tab=batch` | Batch Upload tab | Basic auth |
| GET | `/scheduler?tab=ai` | AI Generator tab | Basic auth |
| GET | `/linkedin` | LinkedIn setup wizard | Basic auth |
| GET | `/meta` | Meta setup wizard | Basic auth |
| GET | `/dashboard` | Credential Dashboard | Basic auth |

### API routes (JSON)

| Method | Path | Purpose |
|---|---|---|
| **Posts** | | |
| GET | `/api/posts` | List posts. Query: `?platform=&status=&campaign_tag=&limit=&offset=` |
| POST | `/api/posts` | Create one post (Compose form) |
| GET | `/api/posts/<id>` | Read one |
| PATCH | `/api/posts/<id>` | Edit fields |
| DELETE | `/api/posts/<id>` | Delete |
| POST | `/api/posts/<id>/publish` | Publish immediately, regardless of `scheduled_at` |
| POST | `/api/posts/<id>/approve` | Set `approved=true` |
| POST | `/api/posts/<id>/sync-notion` | Manual Notion sync trigger |
| POST | `/api/posts/batch` | Multi-row CSV/XLSX import. Body: `{name, rows:[...]}` |
| **AI Generator** | | |
| POST | `/api/ai/generate-campaign` | Body: see `05-ai-generator.md`. Creates N draft posts per platform. |
| **OAuth — LinkedIn** | | |
| GET | `/api/oauth/linkedin/authorize` | 302 → LinkedIn consent screen |
| GET | `/api/oauth/linkedin/callback` | Exchange code for token, store in DB |
| **OAuth — Meta** | | |
| POST | `/api/oauth/meta/exchange` | Body: `{app_id, app_secret, short_lived_token}`. Returns long-lived Page token, stores in DB. |
| **Credentials** | | |
| GET | `/api/credentials` | Dashboard list |
| POST | `/api/credentials/<id>/refresh` | Manual token refresh |
| DELETE | `/api/credentials/<id>` | Delete a credential |
| **Background scheduler control** | | |
| GET | `/api/scheduler/status` | `{busy: bool, next_token_refresh_at, next_publish_check_at}` — drives the orange "Scheduler busy" pill on Dashboard |
| **Health** | | |
| GET | `/health` | Cloud Run health probe; also keeps APScheduler thread warm |

---

## Background jobs

Two APScheduler jobs.

### Job 1 — Token refresh sweep

- **Cadence:** every 6 hours
- **Action:**
  1. Find all `oauth_credentials` where `expires_at IS NOT NULL AND expires_at < now() + interval '7 days'`
  2. For each, call provider-specific refresh:
     - **LinkedIn:** if `refresh_token_enc` exists, POST to `https://www.linkedin.com/oauth/v2/accessToken` with `grant_type=refresh_token`. Update `access_token_enc`, `expires_at`, `last_refresh_at`, `last_refresh_status='success'`. If no refresh token, mark `last_refresh_status='failed'` with error "No refresh token available — re-authorize required."
     - **Meta long-lived Page tokens:** these never expire. Skip.
     - **Meta long-lived User tokens (if used):** POST `/oauth/access_token?grant_type=fb_exchange_token` to extend.
  3. Write status back to row.

### Job 2 — Post publisher

- **Cadence:** every 60 seconds
- **Action:**
  1. Find posts where `status='scheduled' AND approved=true AND scheduled_at <= now()`
  2. For each:
     - Set `status='posting'`
     - Call platform-specific publish (see `03-oauth.md` for shape)
     - On success: set `status='posted'`, `posted_at=now()`, `platform_post_id=<id>`. Trigger Notion sync.
     - On failure: set `status='failed'`, `error_message=<error>`. Do NOT retry automatically — Nathan retries from the UI.

### Scheduler-busy indicator

- The orange "Scheduler busy" pill on Dashboard reflects an in-memory flag set
  whenever Job 1 or Job 2 is mid-execution. Frontend polls `/api/scheduler/status`
  every 30s.

---

## Deploy target — Cloud Run

| Setting | Value |
|---|---|
| Project | `project-9c425f11-39e5-4743-b9d` (existing ETKM project) |
| Region | `us-central1` |
| Service name | `etkm-social-agent` |
| Memory | 512 MiB |
| CPU | 1 |
| Min instances | 1 (keeps APScheduler warm; without min=1 the scheduler stops on cold-start) |
| Max instances | 1 (single writer to SQLite) |
| Port | 8080 |
| Timeout | 300s |
| Concurrency | 80 |

### Files needed at the repo root for the build subdirectory

```
social-agent/
├── Dockerfile
├── requirements.txt
├── app.py                # Flask entry
├── models.py             # SQLAlchemy
├── jobs.py               # APScheduler tasks
├── auth/
│   ├── linkedin.py
│   └── meta.py
├── publishers/
│   ├── facebook.py
│   ├── instagram.py
│   └── linkedin.py
├── notion_sync.py
├── ai_generator.py
├── templates/            # Jinja
├── static/
│   ├── css/etkm.css
│   ├── js/
│   └── vendor/           # FullCalendar, Alpine self-hosted
└── migrations/           # Alembic
```

### Required env vars

| Var | Purpose |
|---|---|
| `APP_SECRET_KEY` | Flask session key + Fernet encryption key for stored tokens |
| `ADMIN_USER` | Basic auth username |
| `ADMIN_PASS` | Basic auth password |
| `DATABASE_URL` | `sqlite:////data/etkm-social.db` (v1) or Postgres URL (v2) |
| `LINKEDIN_REDIRECT_URI` | `https://etkm-social-agent-XXX.us-central1.run.app/api/oauth/linkedin/callback` |
| `NOTION_TOKEN` | Same Notion integration token Nathan already has — needs access to the new ETKM Social Posts DB |
| `NOTION_SOCIAL_POSTS_DB_ID` | Set after Phase B (Notion DB creation) |
| `ANTHROPIC_API_KEY` | Already exists in ETKM env |
| `GCS_BUCKET` | Cloud Storage bucket for uploaded post images. e.g. `etkm-social-media` |

### Outbound APIs

- LinkedIn: `api.linkedin.com`, `www.linkedin.com/oauth/v2/*`
- Meta: `graph.facebook.com/v19.0`
- Notion: `api.notion.com/v1`
- Anthropic: `api.anthropic.com/v1/messages`

All four must be reachable from Cloud Run egress (default open). No VPC connector needed.

---

## Security notes

- Tokens stored encrypted with Fernet using `APP_SECRET_KEY` as the key.
  The Manus build appears to have stored them in plaintext (visible as
  fully-formed strings in the redacted screenshots).
- Basic auth gates every page including `/health` for the auth-required
  variant; we expose `/health` unauthenticated for Cloud Run probes only.
- No CSRF protection in v1 — Nathan is the only user, single-tenant. If we
  ever expose this externally we add Flask-WTF CSRF tokens.
- Uploaded images go to a private GCS bucket. The Meta Graph API only
  needs the URL during the brief publish call, so we sign URLs with a
  10-minute expiry.

---

*Next: `02-ui-spec.md` — page-by-page UI captured from screenshots.*
