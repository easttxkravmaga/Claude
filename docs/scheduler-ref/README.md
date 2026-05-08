# ETKM Social Media Publishing App — Rebuild Spec

Reverse-engineered specification for the **ETKM Social Media Publishing App** —
the Cloud Run replacement for the now-offline Manus deployment originally
hosted at `https://etkmoauth-bmydy76p.manus.space`.

This directory is the source of truth for the rebuild. Everything here is
text-complete: an implementation session can build the app from these docs
without re-asking Nathan for missing details. Where details are guesses, they
are flagged in `07-assumptions.md` and must be reviewed before code is written.

---

## What this app is

The **ETKM Social Media Publishing App** — internal tooling for Nathan that:

1. Stores OAuth credentials for LinkedIn and Meta (Facebook + Instagram) in an
   encrypted local database
2. Refreshes those tokens automatically on a 6-hour cycle
3. Lets Nathan compose, schedule, and approve posts (image OR video) inside the App
4. Stores media files (images and video) in Google Cloud Storage
5. Publishes posts to Facebook, Instagram, and LinkedIn at their scheduled time
6. Generates campaign post drafts via the Claude API on demand

It replaces manual posting across three platforms and gives ETKM a single
calendar view for the publishing schedule.

---

## Source of truth — locked

| Thing | Where it lives |
|---|---|
| **Posts** (caption, schedule, status, platform) | The App's own SQLite database on Cloud Run |
| **Media files** (images and video) | Google Cloud Storage, private bucket |
| **OAuth tokens** | Same database, Fernet-encrypted at rest |
| **Strategy / templates / pillar plans** | Existing Notion pages — untouched, never read or written by the App |

**The App does NOT integrate with Notion.** The Manus build's broken Notion
sync is removed entirely. Nathan's Notion Social Calendar stays as a strategy
reference document; the App ignores it. This is the single biggest
simplification over the Manus version.

---

## Source material

| Source | Status |
|---|---|
| Live deployment `etkmoauth-bmydy76p.manus.space/scheduler` | DEAD — returns `403 host_not_allowed` (Manus app expired or paused) |
| 9 screenshots — Home, Scheduler (5 sub-tabs), LinkedIn setup, Meta setup, Dashboard | Captured in conversation. Nathan can drop the originals in `docs/scheduler-ref/screenshots/` for durable visual reference; the spec does not require them to be implemented from. |
| Original Manus source code | Not available |
| Notion intelligence on Meta + LinkedIn + Social Calendar | Reviewed via Notion MCP. Confirms the Manus build ran identically — App was source of truth, Notion sync was a broken side-channel. |

---

## Decisions locked (this branch)

| # | Question | Decision |
|---|---|---|
| 1 | Sequencing | Spec doc first, then build |
| 2 | Deploy target | Google Cloud Run (matches existing `etkm-backend` infra in `us-central1`) |
| 3 | App name | **ETKM Social Media Publishing App** — locked. Internal short form: "Publishing App". The Manus-era "OAuth Manager" / "Social Agent" branding is retired. |
| 4 | Source of truth for posts | The App's own database. Not Notion. |
| 5 | Media file storage | Google Cloud Storage, private bucket, signed-URL access for platform fetches |
| 6 | Video upload | Supported. MP4 H.264 / AAC, up to ~200 MB per file. Browser uploads directly to GCS via signed PUT URL (bypasses Cloud Run request size limit). |
| 7 | AI Generator | Keep — wired to Claude Sonnet 4.6. Generated drafts written to the App's database (not Notion). |
| 8 | Notion integration | None. Removed entirely. |
| 9 | Brand kit | Full ETKM brand kit applies — black background (`#000`/`#111`), white text, single red accent (`#CC0000`), Swiss layout, no light surfaces, no prohibited words, strip all "Made with Manus" branding. |

---

## Document index

| File | Purpose | Read when |
|---|---|---|
| `01-architecture.md` | Stack, data model, background jobs, deploy target, video handling | Before any code. Foundation. |
| `02-ui-spec.md` | Page-by-page UI spec captured from each screenshot, retitled for the new app name | When scaffolding templates |
| `03-oauth.md` | LinkedIn + Meta OAuth flows step-by-step, with the LinkedIn `offline_access` fix called out | When wiring the auth routes |
| `04-storage-and-publishing.md` | GCS bucket setup, signed URL upload pattern, per-platform publish flows for image AND video (FB Graph, IG Reels multi-step, LinkedIn UGC asset upload) | When wiring the worker |
| `05-ai-generator.md` | AI Campaign Generator — Claude API call shape and ETKM brand-voice system prompt | When implementing the AI tab |
| `06-bugs-and-brand-fixes.md` | Three concrete bugs visible in the live build + brand-rule violations | Treat as pre-flight checklist for the rebuild — these must NOT recur. |
| `07-assumptions.md` | Every guess made during the spec, flagged so Nathan can correct before code is written | Read first. Resolve before build. |

---

## Build phases (when this spec is approved)

| Phase | Owner | Output |
|---|---|---|
| **A. Spec review** | Nathan | Sign-off on `07-assumptions.md` |
| **B. GCP infra prep** | Claude (with Nathan's approval at each step) | New Cloud Run service `etkm-social-publishing`, new GCS bucket `etkm-social-media-assets`, Cloud SQL skipped (SQLite v1) |
| **C. Backend scaffold** | Claude | Flask app, SQLAlchemy models, Dockerfile, Alembic migrations |
| **D. OAuth flows** | Claude | LinkedIn (with `offline_access` scope) + Meta (short→long token exchange) wired and tested |
| **E. UI templates** | Claude | Jinja templates for all 5 pages, ETKM-branded |
| **F. Media upload + publishers** | Claude | GCS signed-URL upload, FB/IG/LI publishers including video flows |
| **G. Background jobs** | Claude | Token refresh + post publisher (APScheduler) |
| **H. AI Generator** | Claude | Claude API integration with brand-voice system prompt |
| **I. Cloud Run deploy** | Claude → Nathan approves | Live URL |
| **J. Migration** | Nathan | Re-authorize LinkedIn (with `offline_access` scope this time) and Meta |

Each phase has its own QC pass against the 8 brand gates before it closes.

---

## What this spec deliberately does NOT include

- **No real credentials, tokens, or secrets** in any file. All examples are
  redacted or placeholder. The Manus screenshots showed some IDs; those values
  are referenced only where structurally necessary (e.g. the LinkedIn redirect
  URI shape) and are never used as defaults in code.
- **No pixel-perfect CSS port** of the Manus build. The rebuild applies ETKM's
  brand kit, which already conflicts with the live build (light hero card on
  Home, gray header bar). The UI spec describes layout and components, not
  exact CSS values from the broken original.
- **No dependency on Manus.** The rebuild stands alone on Cloud Run.
- **No Notion integration.** The Notion Social Calendar remains a separate
  strategy document Nathan maintains by hand. The App does not read or write
  to it.
- **No video transcoding.** If Nathan uploads a horizontal video to Instagram
  Reels, IG renders it with black bars. The Compose form will warn but won't
  re-encode. Server-side ffmpeg is out of scope for v1.

---

*Spec doc — version 1.1 — built 2026-05-08 — branch `claude/reverse-engineer-oauth-scheduler-VzuAb`*
*Supersedes v1.0; v1.0 was based on incorrect "Notion as source of truth" assumption.*
