# ETKM Social Agent — Rebuild Spec

Reverse-engineered specification for the ETKM Social Agent web app, captured
from 9 screenshots of the now-offline Manus deployment originally hosted at
`https://etkmoauth-bmydy76p.manus.space`.

This directory is the source of truth for the rebuild. Everything here is
text-complete: an implementation session can build the app from these docs
without re-asking Nathan for missing details. Where details are guesses, they
are flagged in `07-assumptions.md` and must be reviewed before code is written.

---

## What this app is

ETKM Social Agent — a web app that:

1. Stores OAuth credentials for LinkedIn and Meta (Facebook + Instagram)
2. Refreshes those tokens automatically on a 6-hour cycle
3. Schedules and publishes posts to Facebook, Instagram, and LinkedIn
4. Mirrors every post to a dedicated Notion database
5. Generates campaign post drafts via the Claude API on demand

It replaces manual posting across three social platforms and gives ETKM a
single calendar view for the publishing schedule.

---

## Source material

| Source | Status |
|---|---|
| Live deployment `etkmoauth-bmydy76p.manus.space/scheduler` | DEAD — returns `403 host_not_allowed` (Manus app expired or paused) |
| 9 screenshots — Home, Scheduler (5 sub-tabs), LinkedIn setup, Meta setup, Dashboard | Captured in this conversation. Nathan can drop the originals in `docs/scheduler-ref/screenshots/` for durable visual reference; the spec does not require them to be implemented from. |
| Original source code | Not available |

---

## Decisions made (this branch)

| # | Question | Decision |
|---|---|---|
| 1 | Sequencing | Spec doc first, then build |
| 2 | Deploy target | Google Cloud Run (matches existing `etkm-backend` infra in `us-central1`) |
| 3 | AI Generator | Keep — wired to Claude API (Sonnet 4.6 by default) |
| 4 | Notion sync target | New dedicated **ETKM Social Posts** database. The existing P6 Media Library DB (`9d79095fe24a44908fd542922196c58f`) is for media files and stays untouched. |
| 5 | Brand kit | Full ETKM brand kit applies — black background (`#000`/`#111`), white text, single red accent (`#CC0000`), Swiss layout, no light surfaces, no prohibited words, strip all "Made with Manus" branding. |

---

## Document index

| File | Purpose | Read when |
|---|---|---|
| `01-architecture.md` | Stack, data model, background jobs, deploy target | Before any code. Foundation. |
| `02-ui-spec.md` | Page-by-page UI spec captured from each screenshot | When scaffolding templates |
| `03-oauth.md` | LinkedIn + Meta OAuth flows step-by-step | When wiring the auth routes |
| `04-notion.md` | New "ETKM Social Posts" Notion database schema and sync logic | When building Notion integration. The MCP-driven DB creation step is included. |
| `05-ai-generator.md` | AI Campaign Generator — Claude API call shape and ETKM brand-voice system prompt | When implementing the AI tab |
| `06-bugs-and-brand-fixes.md` | Three concrete bugs visible in the live build + brand-rule violations | Treat as a pre-flight checklist for the rebuild — these must NOT recur. |
| `07-assumptions.md` | Every guess made during the spec, flagged so Nathan can correct before code is written | Read first. Resolve before build. |

---

## Build phases (when this spec is approved)

| Phase | Owner | Output |
|---|---|---|
| **A. Spec review** | Nathan | Sign-off on `07-assumptions.md` |
| **B. Notion DB creation** | Claude (via Notion MCP) | Live `ETKM Social Posts` DB; ID written back into `04-notion.md` |
| **C. Backend scaffold** | Claude | Flask app, SQLAlchemy models, Cloud Run Dockerfile |
| **D. OAuth flows** | Claude | LinkedIn + Meta authorize/callback/exchange routes wired |
| **E. UI templates** | Claude | Jinja templates for all 5 pages, ETKM-branded |
| **F. Background jobs** | Claude | Token refresh + post publisher (APScheduler) |
| **G. AI Generator** | Claude | Claude API integration with brand-voice system prompt |
| **H. Cloud Run deploy** | Claude → Nathan approves | Live URL |
| **I. Migration** | Nathan | Re-authorize LinkedIn (with `offline_access` scope this time) and Meta |

Each phase has its own QC pass against the 8 brand gates before it closes.

---

## What this spec deliberately does NOT include

- **No real credentials, tokens, or secrets** in any file. All examples are
  redacted or placeholder. The Manus screenshots leaked some IDs publicly to
  Nathan's screen-buffer; those values are noted only where structurally
  necessary (e.g. confirming the LinkedIn redirect URI shape) and are never
  used as defaults in code.
- **No pixel-perfect CSS port** of the Manus build. The rebuild applies
  ETKM's brand kit, which already conflicts with the live build (light hero
  card, gray header). The UI spec describes layout and components, not
  exact CSS values from the broken original.
- **No dependency on Manus.** The rebuild stands alone on Cloud Run.

---

*Spec doc — version 1.0 — built 2026-05-08 — branch `claude/reverse-engineer-oauth-scheduler-VzuAb`*
