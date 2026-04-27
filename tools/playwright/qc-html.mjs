#!/usr/bin/env node
// ETKM HTML Visual QC — Gate 4 automation
// Renders every .html in a target directory, screenshots it at desktop+mobile,
// and flags brand violations: light backgrounds, missing red accent, accent overuse.
//
// Usage:
//   node tools/playwright/qc-html.mjs [target-dir]   # default: output/
//
// Exit code 0 = all PASS, 1 = at least one FAIL.

import { readdir, stat, mkdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join, resolve, relative, basename, extname } from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

// Resolve playwright from globals if not in this project
function loadPlaywright() {
  const candidates = [
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
  throw new Error('playwright not found. Install with: npm install -g playwright');
}

if (!process.env.PLAYWRIGHT_BROWSERS_PATH && existsSync('/opt/pw-browsers')) {
  process.env.PLAYWRIGHT_BROWSERS_PATH = '/opt/pw-browsers';
}

const { chromium } = loadPlaywright();

const TARGET_DIR = resolve(process.argv[2] || 'output');
const SHOTS_DIR = resolve('output/qc-screenshots');
const REPORT_PATH = resolve('output/qa-report-visual.md');

const BRAND_BG = ['rgb(0, 0, 0)', 'rgb(17, 17, 17)'];
const BRAND_ACCENT = 'rgb(204, 0, 0)';
const ACCENT_OVERUSE_THRESHOLD = 12;

async function findHtml(dir) {
  const out = [];
  async function walk(d) {
    let entries;
    try { entries = await readdir(d, { withFileTypes: true }); }
    catch { return; }
    for (const e of entries) {
      const p = join(d, e.name);
      if (e.isDirectory()) {
        if (['node_modules', '.git', 'qc-screenshots'].includes(e.name)) continue;
        await walk(p);
      } else if (e.isFile() && extname(e.name).toLowerCase() === '.html') {
        out.push(p);
      }
    }
  }
  await walk(dir);
  return out;
}

// Reject light bg by sampling computed body background and counting accent uses.
// Done in-page so we get the rendered values, not the source CSS.
async function inspectPage(page) {
  return await page.evaluate(({ accent }) => {
    const body = document.body;
    const bodyBg = getComputedStyle(body).backgroundColor;

    let accentCount = 0;
    let lightSurface = null;
    const viewportArea = window.innerWidth * window.innerHeight;

    for (const el of document.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      const bg = cs.backgroundColor;
      const color = cs.color;
      const border = cs.borderColor;

      if ([bg, color, border].includes(accent)) accentCount++;

      // flag any element covering >25% of viewport that has a clearly light background
      const m = bg.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
      if (m) {
        const [r, g, b] = [+m[1], +m[2], +m[3]];
        const isLight = r + g + b > 500;
        const rect = el.getBoundingClientRect();
        const area = Math.max(0, rect.width) * Math.max(0, rect.height);
        if (isLight && area > viewportArea * 0.25 && !lightSurface) {
          lightSurface = { tag: el.tagName.toLowerCase(), bg, areaPct: Math.round(area / viewportArea * 100) };
        }
      }
    }

    return { bodyBg, accentCount, lightSurface };
  }, { accent: BRAND_ACCENT });
}

function evaluateGates({ bodyBg, accentCount, lightSurface }) {
  const failures = [];
  if (!BRAND_BG.includes(bodyBg)) {
    failures.push(`Gate 4 — body background is ${bodyBg}, expected #000000 or #111111`);
  }
  if (lightSurface) {
    failures.push(`Gate 4 — large light surface detected: <${lightSurface.tag}> bg=${lightSurface.bg} covers ~${lightSurface.areaPct}% of viewport`);
  }
  if (accentCount === 0) {
    failures.push('Gate 4 — no red accent (#CC0000) found anywhere');
  }
  if (accentCount > ACCENT_OVERUSE_THRESHOLD) {
    failures.push(`Gate 4 — red accent used ${accentCount} times (threshold ${ACCENT_OVERUSE_THRESHOLD}); flag for human review`);
  }
  return failures;
}

async function qcOne(browser, htmlPath) {
  const url = pathToFileURL(htmlPath).href;
  const slug = basename(htmlPath, '.html').replace(/[^a-z0-9._-]/gi, '_');

  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();

  await page.goto(url, { waitUntil: 'networkidle', timeout: 15000 });
  await page.screenshot({ path: join(SHOTS_DIR, `${slug}-desktop.png`), fullPage: true });
  const desktop = await inspectPage(page);

  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({ path: join(SHOTS_DIR, `${slug}-mobile.png`), fullPage: true });

  await ctx.close();

  return {
    file: relative(process.cwd(), htmlPath),
    slug,
    inspection: desktop,
    failures: evaluateGates(desktop),
  };
}

function renderReport(results) {
  const lines = [
    '# Visual QC Report',
    '',
    `Generated: ${new Date().toISOString()}`,
    `Target: \`${relative(process.cwd(), TARGET_DIR)}\``,
    `Files scanned: ${results.length}`,
    '',
  ];

  const passed = results.filter(r => r.failures.length === 0);
  const failed = results.filter(r => r.failures.length > 0);
  lines.push(`**PASS:** ${passed.length}  |  **FAIL:** ${failed.length}`, '');

  if (failed.length) {
    lines.push('## Failures', '');
    for (const r of failed) {
      lines.push(`### ${r.file}`, '');
      lines.push(`- Body bg: \`${r.inspection.bodyBg}\``);
      lines.push(`- Accent count: ${r.inspection.accentCount}`);
      lines.push('', '**Failures:**');
      for (const f of r.failures) lines.push(`- ${f}`);
      lines.push('', `Screenshots: \`output/qc-screenshots/${r.slug}-desktop.png\`, \`output/qc-screenshots/${r.slug}-mobile.png\``, '');
    }
  }

  if (passed.length) {
    lines.push('## Passed', '');
    for (const r of passed) {
      lines.push(`- ${r.file} (accent ×${r.inspection.accentCount})`);
    }
    lines.push('');
  }

  return lines.join('\n');
}

async function main() {
  if (!existsSync(TARGET_DIR)) {
    console.error(`Target directory does not exist: ${TARGET_DIR}`);
    process.exit(2);
  }

  await mkdir(SHOTS_DIR, { recursive: true });

  const files = await findHtml(TARGET_DIR);
  if (files.length === 0) {
    console.log(`No .html files found under ${TARGET_DIR}`);
    return;
  }

  console.log(`Scanning ${files.length} HTML file(s)…`);
  const browser = await chromium.launch({ headless: true });

  const results = [];
  for (const f of files) {
    process.stdout.write(`  ${relative(process.cwd(), f)} … `);
    try {
      const r = await qcOne(browser, f);
      results.push(r);
      console.log(r.failures.length === 0 ? 'PASS' : `FAIL (${r.failures.length})`);
    } catch (e) {
      results.push({ file: f, slug: basename(f, '.html'), inspection: { bodyBg: '?', accentCount: 0, lightSurface: null }, failures: [`Render error: ${e.message}`] });
      console.log(`ERROR: ${e.message}`);
    }
  }

  await browser.close();

  await writeFile(REPORT_PATH, renderReport(results));
  console.log(`\nReport: ${relative(process.cwd(), REPORT_PATH)}`);
  console.log(`Screenshots: ${relative(process.cwd(), SHOTS_DIR)}/`);

  const anyFail = results.some(r => r.failures.length > 0);
  process.exit(anyFail ? 1 : 0);
}

main().catch(e => { console.error(e); process.exit(2); });
