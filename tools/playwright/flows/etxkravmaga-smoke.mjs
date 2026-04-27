#!/usr/bin/env node
// ETKM site smoke test — runs against https://etxkravmaga.com
// Bulletproofing:
//   - 3 internal retries with exponential backoff (5s/15s/45s) before failing
//   - Records a Playwright trace + console + network log on each attempt
//   - Hard timeouts at every step
//   - Captures desktop + mobile screenshots on every outcome (PASS or FAIL)
//   - Emits a machine-readable summary to artifacts/smoke-summary.json so the
//     GitHub Actions workflow can build a clean issue body
//
// Exit codes: 0 = PASS, 1 = FAIL after retries, 2 = config / runner error.

import { existsSync } from 'node:fs';
import { mkdir, writeFile, rm } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

// ─── Resolve playwright (local tools dir → cwd → globals) ────────────────────
const here = dirname(fileURLToPath(import.meta.url));
function loadPlaywright() {
  const candidates = [
    join(here, '..'),
    process.cwd(),
    '/opt/node22/lib/node_modules',
    '/usr/lib/node_modules',
    '/usr/local/lib/node_modules',
  ];
  for (const root of candidates) {
    try {
      const req = createRequire(join(root, 'noop.js'));
      return req('playwright');
    } catch { /* try next */ }
  }
  throw new Error('playwright not found. Run `npm ci` in tools/playwright.');
}
if (!process.env.PLAYWRIGHT_BROWSERS_PATH && existsSync('/opt/pw-browsers')) {
  process.env.PLAYWRIGHT_BROWSERS_PATH = '/opt/pw-browsers';
}
const { chromium } = loadPlaywright();

// ─── Config ──────────────────────────────────────────────────────────────────
const URL = process.env.SMOKE_URL || 'https://etxkravmaga.com';
const ARTIFACTS = process.env.SMOKE_ARTIFACTS_DIR
  || join(process.cwd(), 'artifacts');
const RETRIES = 3;
const BACKOFF_MS = [5_000, 15_000, 45_000];
const NAV_TIMEOUT_MS = 30_000;
const PAGE_TIMEOUT_MS = 45_000;
// Title must contain at least one of these (case-insensitive). Tweak as the
// site evolves — keep it tight enough to catch a hijack, loose enough to
// survive a copy edit.
const TITLE_KEYWORDS = ['krav', 'east texas'];
// A primary CTA must exist somewhere on the page with text matching this regex.
const CTA_REGEX = /trial|book|schedule|sign[\s-]?up|contact|class|membership|join|get started/i;
// Body bg must be reasonably dark. RGB sum < 200 = very dark.
const MAX_BODY_RGB_SUM = 200;
const VIEWPORTS = {
  desktop: { width: 1280, height: 900 },
  mobile:  { width: 390,  height: 844 },
};

// ─── Helpers ─────────────────────────────────────────────────────────────────
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function ensureCleanArtifacts() {
  await rm(ARTIFACTS, { recursive: true, force: true });
  await mkdir(ARTIFACTS, { recursive: true });
}

function rgbSum(rgbStr) {
  const m = rgbStr?.match(/(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/);
  if (!m) return null;
  return +m[1] + +m[2] + +m[3];
}

// Run the actual checks against an open page. Returns { failures, info }.
async function runChecks(page) {
  const failures = [];
  const info = {};

  info.title = await page.title();
  info.finalUrl = page.url();

  if (!info.title || info.title.length < 3) {
    failures.push(`Empty or missing <title> ("${info.title}")`);
  } else if (!TITLE_KEYWORDS.some(k => info.title.toLowerCase().includes(k))) {
    failures.push(`Title does not contain any of [${TITLE_KEYWORDS.join(', ')}]: "${info.title}"`);
  }

  const pageData = await page.evaluate(() => {
    const txt = el => (el?.innerText || el?.value || '').trim();
    const buttons = Array.from(document.querySelectorAll('a, button, input[type=submit]'))
      .map(el => txt(el)).filter(Boolean);
    const headings = Array.from(document.querySelectorAll('h1, h2'))
      .map(el => txt(el)).filter(Boolean);
    return {
      bodyText: document.body?.innerText?.slice(0, 5000) || '',
      bodyBg: getComputedStyle(document.body).backgroundColor,
      headingCount: headings.length,
      buttons,
      hasH1: !!document.querySelector('h1'),
      docHeight: document.documentElement.scrollHeight,
      viewportWidth: window.innerWidth,
    };
  });

  info.bodyTextLength = pageData.bodyText.length;
  info.bodyBg = pageData.bodyBg;
  info.headingCount = pageData.headingCount;
  info.buttonCount = pageData.buttons.length;

  if (pageData.bodyText.length < 200) {
    failures.push(`Body text suspiciously short (${pageData.bodyText.length} chars) — page may not have rendered`);
  }
  if (!pageData.hasH1) {
    failures.push('No <h1> found on page');
  }
  const ctaMatch = pageData.buttons.find(t => CTA_REGEX.test(t));
  if (!ctaMatch) {
    failures.push(`No primary CTA found matching ${CTA_REGEX} (sampled ${pageData.buttons.length} buttons/links)`);
  } else {
    info.ctaSample = ctaMatch;
  }

  const sum = rgbSum(pageData.bodyBg);
  info.bodyRgbSum = sum;
  if (sum !== null && sum > MAX_BODY_RGB_SUM) {
    failures.push(`Body background looks too light (${pageData.bodyBg}, RGB sum ${sum} > ${MAX_BODY_RGB_SUM})`);
  }

  return { failures, info };
}

// One full attempt: launch browser, navigate, take screenshots, run checks.
async function attempt(attemptNum) {
  const log = (msg) => console.log(`[attempt ${attemptNum}] ${msg}`);
  const consoleErrors = [];
  const failedRequests = [];

  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    viewport: VIEWPORTS.desktop,
    ignoreHTTPSErrors: true,
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 (ETKM-Smoke/1.0)',
  });
  await ctx.tracing.start({ screenshots: true, snapshots: true, sources: true });

  const page = await ctx.newPage();
  page.setDefaultTimeout(PAGE_TIMEOUT_MS);
  page.on('pageerror', e => consoleErrors.push(`pageerror: ${e.message}`));
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(`console.error: ${m.text()}`); });
  page.on('requestfailed', r => failedRequests.push({ url: r.url(), failure: r.failure()?.errorText }));

  const result = {
    attempt: attemptNum,
    ts: new Date().toISOString(),
    url: URL,
    failures: [],
    info: {},
    consoleErrors,
    failedRequests,
    httpStatus: null,
    timings: {},
  };

  const t0 = Date.now();
  try {
    log(`GET ${URL}`);
    const resp = await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: NAV_TIMEOUT_MS });
    result.httpStatus = resp?.status() ?? null;
    result.timings.domcontentloaded_ms = Date.now() - t0;

    if (!resp || !resp.ok()) {
      result.failures.push(`HTTP ${result.httpStatus} on initial navigation`);
    } else {
      // Wait for network idle but cap it — slow third-party scripts shouldn't fail us.
      await page.waitForLoadState('networkidle', { timeout: 15_000 }).catch(() => {});
      result.timings.networkidle_ms = Date.now() - t0;

      // Desktop screenshot + checks
      await page.screenshot({ path: join(ARTIFACTS, `attempt${attemptNum}-desktop.png`), fullPage: true });
      const { failures, info } = await runChecks(page);
      result.failures.push(...failures);
      result.info = info;

      // Mobile screenshot
      await page.setViewportSize(VIEWPORTS.mobile);
      await sleep(300);
      await page.screenshot({ path: join(ARTIFACTS, `attempt${attemptNum}-mobile.png`), fullPage: true });
    }

    // Console errors are info-level until they pile up. Two or more is suspicious.
    if (consoleErrors.length >= 2) {
      result.failures.push(`${consoleErrors.length} console/page error(s) on load`);
    }
  } catch (e) {
    result.failures.push(`Exception during attempt: ${e.message}`);
  } finally {
    try { await ctx.tracing.stop({ path: join(ARTIFACTS, `attempt${attemptNum}-trace.zip`) }); } catch {}
    await browser.close();
  }

  result.timings.total_ms = Date.now() - t0;
  log(result.failures.length === 0 ? `PASS in ${result.timings.total_ms}ms` : `FAIL: ${result.failures.length} issue(s)`);
  return result;
}

// ─── Main ────────────────────────────────────────────────────────────────────
async function main() {
  await ensureCleanArtifacts();

  const attempts = [];
  let pass = false;
  for (let i = 1; i <= RETRIES; i++) {
    const r = await attempt(i);
    attempts.push(r);
    if (r.failures.length === 0) { pass = true; break; }
    if (i < RETRIES) {
      const wait = BACKOFF_MS[i - 1] ?? 30_000;
      console.log(`  retrying in ${wait / 1000}s…`);
      await sleep(wait);
    }
  }

  const last = attempts.at(-1);
  const summary = {
    url: URL,
    pass,
    attemptsMade: attempts.length,
    finalAttempt: last,
    allAttempts: attempts.map(a => ({
      attempt: a.attempt,
      ts: a.ts,
      httpStatus: a.httpStatus,
      timings: a.timings,
      failureCount: a.failures.length,
      failures: a.failures,
    })),
  };
  await writeFile(join(ARTIFACTS, 'smoke-summary.json'), JSON.stringify(summary, null, 2));

  // Human-readable report
  const md = [
    `# Smoke test ${pass ? 'PASS ✅' : 'FAIL ❌'}`,
    '',
    `- URL: ${URL}`,
    `- Attempts: ${attempts.length}/${RETRIES}`,
    `- Final HTTP status: ${last.httpStatus ?? 'n/a'}`,
    `- Final load time: ${last.timings.total_ms}ms`,
    last.info.title ? `- Title: \`${last.info.title}\`` : '',
    last.info.ctaSample ? `- Sample CTA: \`${last.info.ctaSample}\`` : '',
    '',
    pass ? '' : '## Failures (final attempt)',
    pass ? '' : last.failures.map(f => `- ${f}`).join('\n'),
    '',
    last.consoleErrors?.length ? `## Console errors\n${last.consoleErrors.slice(0, 10).map(e => `- ${e}`).join('\n')}` : '',
    last.failedRequests?.length ? `## Failed network requests\n${last.failedRequests.slice(0, 10).map(r => `- ${r.url} → ${r.failure}`).join('\n')}` : '',
  ].filter(Boolean).join('\n');
  await writeFile(join(ARTIFACTS, 'smoke-report.md'), md + '\n');

  console.log(`\n${pass ? '✅ PASS' : '❌ FAIL'} after ${attempts.length} attempt(s)`);
  console.log(`Artifacts: ${ARTIFACTS}`);
  process.exit(pass ? 0 : 1);
}

main().catch(e => {
  console.error('Runner error:', e);
  process.exit(2);
});
