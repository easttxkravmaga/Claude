# Playwright CLI — ETKM Utilization Plan

**Branch:** `claude/playwright-cli-research-eQnf7`
**Date:** 2026-04-27
**Owner:** Main Agent / Nathan
**Filter:** More revenue. Less time wasted.

---

## 1. What Playwright CLI Actually Is

There are two related tools, and we need to be precise about which is which:

### A. Classic Playwright CLI — `playwright` (Microsoft, mature)
Bundled with the `playwright` npm package. Drives Chromium, Firefox, WebKit from the terminal. Stable, widely used, ships with its own test runner.

Top-level commands available right now on this system:
- `open`, `codegen` — launch a browser, record actions, generate replay code
- `screenshot <url> <file>` — capture a page (full page, viewport, or element)
- `pdf <url> <file>` — render a page to PDF (Chromium only, headless)
- `install` / `install-deps` — pull browser binaries and OS deps
- `test` — run Playwright Test specs
- `show-trace`, `show-report` — view traces and HTML reports
- `init-agents` — scaffold agent files into a repo

### B. Agent-Optimized CLI — `@playwright/cli` / `playwright-cli` (newer)
A re-thought CLI built for coding agents (Claude Code, Copilot). Token-efficient — does not stuff page HTML into the LLM. Returns a snapshot with element refs (e.g., `e15`) that the agent then targets, instead of CSS selectors. Adds named sessions, route mocking, video, tracing, and a `--skills` install that registers a Playwright skill into the agent.

Key extras over the classic CLI: `snapshot`, `eval`, `route`, `tracing-start/stop`, `video-start/stop`, `state-save/load`, `generate-locator`, `-s=name` named sessions, `show --annotate` for human-in-the-loop feedback.

---

## 2. Install Status and Commands

### Already installed on this environment
```
playwright            v1.56.1   (global, /opt/node22/bin/playwright)
node                  v22.22.2
npm                   v10.9.7
chromedriver          v147.0.0
```

The classic CLI is ready to use today. Verify with `playwright --help`.

### To add the agent-optimized CLI
```bash
# Global install
npm install -g @playwright/cli@latest

# One-time setup (downloads browsers and registers skill)
playwright-cli install
playwright-cli install --skills    # registers Claude Code skill

# Per-project alternative (no global install)
npx @playwright/cli@latest --help
```

### To make the classic CLI ready for headed/PDF work
Browser binaries may not be downloaded yet. Run once:
```bash
playwright install chromium          # smallest, covers PDF + most jobs
playwright install --with-deps       # full set + OS dependencies
```

### Recommendation
Install **both**. The classic CLI handles headless batch jobs (PDF, screenshot, scripted tests) cleanly. The agent-optimized CLI is what we want when Claude Code itself drives a browser during a session.

---

## 3. ETKM Use Cases — Ranked by Revenue / Time Impact

Each use case is scored against the doctrine: does it move ETKM toward more revenue or less time wasted? If neither, it does not ship.

### Tier 1 — Build immediately (high impact, low effort)

**1. Visual QC for HTML deliverables (Gate 4 automation)**
QA Agent currently eyeballs HTML deliverables for black background, white text, single red accent. Replace with a Playwright screenshot script that renders every HTML output in `output/` and saves a thumbnail. A second pass samples pixels in known regions to flag any light background or missing accent. Gate 4 becomes deterministic instead of vibes-based.
- *Time saved:* every HTML build, ~5 min of human review
- *Revenue tie-in:* faster turnaround on landing pages, lead magnets, campaign assets

**2. HTML → PDF rendering for one-pagers**
ReportLab is correct for complex PDFs (rosters, certificates, the Gate 4A audited stuff). For a one-page lead magnet or schedule flyer, `playwright pdf` against a styled HTML template is faster to author and easier to revise. ETKM brand HTML stays the source of truth; PDF falls out for free.
- *Time saved:* removes round-trips through ReportLab for simple layouts
- *Revenue tie-in:* lead magnet output cycle drops from hours to minutes

**3. Email template visual previews**
HTML campaign emails today are reviewed by opening files in a browser. Script: render template with sample data, screenshot at desktop + mobile widths, drop into `output/email-previews/`. Nathan reviews thumbnails, not files.
- *Time saved:* batch review of 5–10 templates in under a minute
- *Revenue tie-in:* faster campaign approval = more sends per month

### Tier 2 — Build when the need shows up

**4. Codegen for CRM / Pipedrive automation**
`playwright codegen https://app.pipedrive.com` records Nathan's repetitive workflow once, emits a script he runs nightly. Candidates: lead intake hygiene, pipeline cleanup, weekly export.
- *Time saved:* whatever Nathan currently does manually in Pipedrive
- *Revenue tie-in:* indirect — frees Nathan time, cleaner pipeline data

**5. Smoke tests for live ETKM web properties**
A `playwright test` suite hits the public booking page, the contact form, and the schedule, asserts they load and render the expected ETKM colors. Run on a cron in Railway. If a deploy breaks the booking funnel we hear about it immediately, not from a lost lead.
- *Time saved:* avoids silent revenue loss
- *Revenue tie-in:* every broken-funnel hour is lost trial bookings

**6. Competitor schools — visual snapshot archive**
Monthly screenshot of the front page of every other martial arts school in the East Texas market. Builds a reference archive for Nathan to scan for pricing changes, new programs, or weak positioning to exploit.
- *Time saved:* replaces ad-hoc browsing
- *Revenue tie-in:* market intelligence drives offer/positioning decisions

### Tier 3 — Capability we should know we have, but do not build now

- **Network mocking (`route`)** — only useful if we start doing front-end dev for ETKM web
- **Tracing / video** — only useful when we have to debug an automation that broke in production
- **Multi-session (`-s=name`)** — useful if we ever automate against multiple logged-in accounts in parallel

---

## 4. File Layout When We Build

Per CLAUDE.md ownership rules, when this work moves from plan to build:

```
tools/playwright/
  qc-html.mjs              # Tier 1.1 — Gate 4 visual QC
  html-to-pdf.mjs          # Tier 1.2 — HTML → PDF
  email-preview.mjs        # Tier 1.3 — email previews
  smoke-tests/
    booking.spec.mjs       # Tier 2.5 — public site smoke tests
  competitor-snapshot.mjs  # Tier 2.6 — competitor archive

output/
  qc-screenshots/          # produced by qc-html.mjs
  email-previews/          # produced by email-preview.mjs
  competitor-archive/YYYY-MM/   # produced by competitor-snapshot.mjs
```

Each tool is owned by one agent at build time. No two scripts share a write target.

---

## 5. Recommended Next Steps

1. **Decision needed from Nathan:** approve building Tier 1 items now, or pick one to pilot first.
2. If approved, spawn a single Builder agent (this is plumbing, not a brand deliverable — no team required) to:
   - Run `playwright install chromium` if not already done
   - Build `tools/playwright/qc-html.mjs` first (highest leverage, lowest risk)
   - Wire it into the QA Agent's Gate 4 checklist in `docs/agent-team-playbooks.md`
3. Add `@playwright/cli` install to the SessionStart hook so future Claude Code sessions can drive a browser without manual setup.
4. Re-evaluate Tier 2 after Tier 1 has run for two weeks.

---

## 6. What This Plan Is Not

- Not a recommendation to rebuild ReportLab PDFs — those stay where they are
- Not a vote for Playwright Test as our primary test framework — we have no test suite worth migrating
- Not a green light to scrape competitor sites at scale — the Tier 2 use case is monthly snapshots of public front pages, nothing more

---

## Sources

- [microsoft/playwright-cli on GitHub](https://github.com/microsoft/playwright-cli)
- [Playwright command-line docs](https://playwright.dev/docs/test-cli)
- [Playwright getting-started for coding agents](https://playwright.dev/docs/getting-started-cli)
- [@playwright/cli on npm](https://www.npmjs.com/package/@playwright/cli)
- [playwright-cli SKILL.md](https://github.com/microsoft/playwright-cli/blob/main/skills/playwright-cli/SKILL.md)
