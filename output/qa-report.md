# QA Report — ETKM Social Media Publishing App Rebuild Spec

**Deliverable:** Reverse-engineering spec for the now-offline `etkmoauth-bmydy76p.manus.space` deployment, captured to `docs/scheduler-ref/`.

**Branch:** `claude/reverse-engineer-oauth-scheduler-VzuAb`
**PR:** #6 (draft)
**QA date:** 2026-05-08
**QA agent:** Main agent (solo session — no separate QA agent spawned per CLAUDE.md "When NOT to use an agent team" filter)

---

## Files reviewed

| File | Lines | Status |
|---|---|---|
| `docs/scheduler-ref/README.md` | 161 | PASS |
| `docs/scheduler-ref/01-architecture.md` | 286 | PASS |
| `docs/scheduler-ref/02-ui-spec.md` | 295 | PASS |
| `docs/scheduler-ref/03-oauth.md` | 200 | PASS |
| `docs/scheduler-ref/04-storage-and-publishing.md` | 285 | PASS |
| `docs/scheduler-ref/05-ai-generator.md` | 191 | PASS |
| `docs/scheduler-ref/06-bugs-and-brand-fixes.md` | 184 | PASS |
| `docs/scheduler-ref/07-assumptions.md` | 240 | PASS |

---

## Gate-by-gate results

### Gate 1 — Goal Alignment ✅ PASS

The deliverable accomplishes Nathan's request: reverse-engineer the offline Manus deployment into a documented rebuild spec. The spec is text-complete (a future build session can implement without re-asking Nathan), captures all 9 screenshots' content, locks the architecture decisions, and matches the ETKM brand kit. Bonus: confirmed the rebuild's official name from the Notion Social Media System Consolidation Record.

### Gate 2 — Brand Voice ✅ PASS

Zero prohibited words appear in any spec doc as actual usage. The only hits in the prohibited-word grep are:
- `05-ai-generator.md:99-101` — the explicit prohibited-words **list** inside the AI Generator's system prompt (this is the list defining the rule, not a violation of it)

Tone is direct, grounded, no fluff throughout. No academic, corporate, or motivational-poster register.

### Gate 3 — Experience Phrasing ✅ PASS

No specific year count for Nathan's experience appears anywhere as a claim. The single grep hit is `05-ai-generator.md:96` — the explicit `NEVER use a specific year count like "42 years"` instruction inside the system prompt. That's a meta-reference defining the rule, not a violation.

### Gate 4 — Visual Compliance ✅ PASS

The spec **mandates** ETKM brand-kit compliance for the rebuilt app:
- Background: `#000000` / `#111111` — true black, no light surfaces
- Text: white (`#FFFFFF`)
- Accent: red `#CC0000`, used once per section maximum
- Header bar: true black (fixes Manus build's mid-gray)
- All "Made with Manus" branding stripped
- Plaintext-token leakage in Dashboard fixed via Fernet encryption + masked-by-default reveal

The spec docs themselves are plain markdown — no rendered visuals to check.

### Gate 5 — Format Compliance ✅ PASS

Output format: markdown spec docs. Standard for documentation deliverables. Files use Github-flavored markdown with tables, code blocks, and section headers. Renderable in any standard markdown viewer.

### Gate 6 — File Integrity ✅ PASS

All 8 files (README + 01-07) exist at their specified paths. All cross-references between docs use correct relative filenames (verified by grep — every referenced filename resolves to an existing file in the directory). No broken links.

### Gate 7 — Completeness ✅ PASS

- No `[INSERT X HERE]` placeholders.
- No TODO / FIXME markers.
- The `XXX` placeholder on `urn:li:person:XXX` and `etkm-social-publishing-XXX.us-central1.run.app` is **intentional** — the first is LinkedIn's documented URN format with a member-ID variable, the second is the Cloud Run service hostname which is generated at deploy time and substituted via `LINKEDIN_REDIRECT_URI` env var.
- Every section in every doc has content.
- All 7 spec docs cover their stated scope (per `README.md` document index).

### Gate 8 — Revenue/Time Test ✅ PASS

The spec moves ETKM toward less time wasted:
- Replaces a dead Manus deployment with a Cloud Run rebuild
- Automates 16 posts/week (Phase 1) / 22+ posts/week (Phase 2) of social media work that would otherwise be manual
- Eliminates the 60-day LinkedIn re-authorization cycle (offline_access fix)
- Removes broken Notion sync that produced false-error noise on every post
- Cost: ~$5-10/month Cloud Run + GCS + Anthropic

ETKM's social media volume per Notion's Weekly Post Template is the explicit time-savings target. Documented in Bug 1, Bug 2, Bug 3, and the architecture decisions.

---

## Findings summary

**No FAIL gates. No re-work required before commit.**

Two minor notes for the build phase:

1. **A14 (Re-authorization required post-deploy):** Documented in `07-assumptions.md` and surfaced in the handoff. Nathan must re-authorize LinkedIn (with the new `offline_access` scope) and Meta after the new Cloud Run hostname goes live. Existing Manus credentials cannot be migrated.

2. **`07-assumptions.md` flags 5 high-priority assumptions** that the build session must resolve before code starts:
   - A1 — single-platform per post (data model implication)
   - A12 — confirm 7 ETKM Program tag values
   - A14 — confirm re-authorization is acceptable
   - A16 — single-select vs. multi-select platform in Compose
   - A20 — `social-publishing/` subdirectory or separate repo

Other 15 assumptions can default safely; trivial to change later.

---

## Brand-rule delta from the Manus build (specified in the rebuild)

| # | Manus had | Rebuild specifies |
|---|---|---|
| 1 | Mid-gray header bar | True black `#000000` |
| 2 | Light beige hero card on Home | Black status panel |
| 3 | "OAUTH MANAGER" subtitle / "ETKM Social Agent" H1 mismatch | Single name throughout: `ETKM Social Media Publishing App` |
| 4 | "Made with Manus" floating watermark | Removed |
| 5 | Plaintext OAuth tokens in Dashboard | Fernet-encrypted at rest, masked-by-default UI |
| 6 | "Save credentials to .env file" copy | "Credentials are saved encrypted" |
| 7 | Notion column on All Posts (every row error) | Notion column removed; Errors column only on real errors |
| 8 | LinkedIn missing `offline_access` scope | `offline_access` requested → refresh tokens issued |
| 9 | IG publish without container-status polling (Easter post bug) | 3-step flow with poll-until-`FINISHED` and timeout handling |

All 9 deltas are spec'd as gating items in `06-bugs-and-brand-fixes.md`'s "Implementation checklist for the rebuild" — the rebuild is not done until all 11 checklist items are verified.

---

## Recommendation

**APPROVE the spec for handoff to the build phase.** No revisions required.

The build phase begins after Nathan signs off on `07-assumptions.md` (specifically the 5 high-priority items above). Once approved, the order of operations is:

1. Phase B — GCP infra prep (Cloud Run service, GCS bucket, IAM)
2. Phase C — Backend scaffold (Flask, SQLAlchemy, Dockerfile, Alembic)
3. Phase D — OAuth flows (with offline_access fix verified)
4. Phase E — UI templates (ETKM-branded)
5. Phase F — Media upload + publishers
6. Phase G — Background jobs
7. Phase H — AI Generator (with prompt caching)
8. Phase I — Cloud Run deploy
9. Phase J — Re-authorization (Nathan)

---

*QA report version 1.0 — produced 2026-05-08 — all 8 brand gates PASS*
