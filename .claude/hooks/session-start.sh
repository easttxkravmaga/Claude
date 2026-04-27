#!/bin/bash
# SessionStart hook — ensure Playwright + Chromium are ready for tools/playwright/qc-html.mjs
# Sync mode. Exits 0 even on browser-install failure so the session still starts.

set -uo pipefail

# Only run in remote (Claude Code on the web) sessions
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

status() { echo "[playwright-hook] $*" >&2; }

PW_PATH="/opt/pw-browsers"

# 1. Persist PLAYWRIGHT_BROWSERS_PATH for the session if the cache dir exists
if [ -d "$PW_PATH" ]; then
  if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
    echo "export PLAYWRIGHT_BROWSERS_PATH=$PW_PATH" >> "$CLAUDE_ENV_FILE"
  fi
  export PLAYWRIGHT_BROWSERS_PATH="$PW_PATH"
fi

# 2. Confirm playwright CLI is available
if ! command -v playwright >/dev/null 2>&1; then
  status "FAIL — playwright CLI not on PATH; qc-html.mjs will not run"
  exit 0
fi

PW_VERSION="$(playwright --version 2>/dev/null | awk '{print $2}')"
status "playwright v${PW_VERSION:-unknown}"

# 3. Check whether chromium is already cached for this playwright version
DRY_OUT="$(playwright install --dry-run chromium 2>&1 || true)"
NEEDS_INSTALL=0
if echo "$DRY_OUT" | grep -q "Install location"; then
  # parse the install path and confirm the chrome binary exists
  CHROME_DIR="$(echo "$DRY_OUT" | awk '/^[[:space:]]*Install location:/ {print $3; exit}')"
  if [ -n "$CHROME_DIR" ] && [ -x "$CHROME_DIR/chrome-linux/chrome" ]; then
    status "chromium ready at $CHROME_DIR"
  else
    NEEDS_INSTALL=1
  fi
else
  NEEDS_INSTALL=1
fi

# 4. Attempt install if missing; fail loudly but do not break the session
if [ "$NEEDS_INSTALL" = "1" ]; then
  status "chromium missing — attempting playwright install chromium"
  if playwright install chromium >/tmp/pw-install.log 2>&1; then
    status "chromium install OK"
  else
    status "FAIL — chromium install failed (likely sandbox CDN block). See /tmp/pw-install.log"
    status "qc-html.mjs will not run until a chromium build matching playwright v${PW_VERSION} is available at $PW_PATH"
    exit 0
  fi
fi

# 5. Smoke test — launch + close the browser via the node API
SMOKE_OUT="$(node --input-type=module -e "
import { createRequire } from 'node:module';
const req = createRequire('/opt/node22/lib/node_modules/noop.js');
const { chromium } = req('playwright');
const b = await chromium.launch({ headless: true });
await b.close();
console.log('ok');
" 2>&1)"

if echo "$SMOKE_OUT" | grep -q "^ok$"; then
  status "READY — qc-html.mjs is runnable this session"
else
  status "FAIL — chromium present but failed to launch:"
  echo "$SMOKE_OUT" | sed 's/^/[playwright-hook]   /' >&2
fi

exit 0
