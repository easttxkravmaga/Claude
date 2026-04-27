# Handoff — Playwright HTML Visual QC Tool

**Branch:** `claude/playwright-cli-research-eQnf7`
**Date:** 2026-04-27
**Built:** Tier 1.1 from `docs/playwright-cli-plan.md`

## What was built

- `tools/playwright/qc-html.mjs` — automated Gate 4 visual check for HTML deliverables
- `tools/playwright/fixtures/` — 1 PASS fixture, 2 FAIL fixtures used to verify the tool
- Generated artifacts (gitignored intent — these will be re-created on every run):
  - `output/qa-report-visual.md` — pass/fail summary
  - `output/qc-screenshots/<slug>-desktop.png` and `<slug>-mobile.png`

## What it checks (Gate 4 automation)

1. Body background is `#000000` or `#111111` (rejects any other rendered bg)
2. No element covering >25% of the viewport has a light background (RGB sum > 500)
3. At least one use of the brand red `#CC0000` is present
4. Brand red is not overused (threshold: 12 distinct usages — flag for human review)
5. Renders desktop (1280×800) + mobile (390×844) screenshots for human spot-check

## How to run

```bash
node tools/playwright/qc-html.mjs                  # scans output/
node tools/playwright/qc-html.mjs path/to/dir      # scans custom dir
```

Exit code: `0` all PASS, `1` any FAIL, `2` config/render error.

## Environment notes (this sandbox)

- Playwright resolves from the global install at `/opt/node22/lib/node_modules`
- Chromium binary is at `/opt/pw-browsers/` — script auto-sets `PLAYWRIGHT_BROWSERS_PATH`
- Sandbox blocks the Playwright CDN, so `playwright install` fails. Pre-installed browsers are required. On a fresh dev box, run `playwright install chromium` once.

## Verification log

Tested 2026-04-27 against fixtures:
- `pass-sample.html` → PASS (accent ×2)
- `fail-light-bg.html` → FAIL ×3 (white body bg, large light surface, no accent)
- `fail-no-accent.html` → FAIL ×1 (no accent)

Exit code 1 (correct — failures present).

## Where it plugs in

`docs/agent-team-playbooks.md` Playbook 01 (Event Landing Page) — QA Agent's Gate 4 line now references this tool. Use the same pattern in any future playbook that produces HTML.

## Open items

- Gitignore rule for `output/qc-screenshots/` and `output/qa-report-visual.md` not added — call when ready, or leave as run-time artifacts the team regenerates.
- Tier 1.2 (HTML → PDF) and Tier 1.3 (email previews) from the plan are still pending Nathan's approval.
