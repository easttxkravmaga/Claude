#!/usr/bin/env bash
# setup_cron.sh — Schedule smith_county_scraper.py to run every Monday at 6 AM
# and email the results to easttxkravmaga@gmail.com.
#
# Run once:  bash scrapers/setup_cron.sh
# Remove:    crontab -e  → delete the added line

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$(which python3)"
SCRAPER="$SCRIPT_DIR/smith_county_scraper.py"
LOGFILE="$SCRIPT_DIR/scraper_cron.log"

if [ ! -f "$SCRAPER" ]; then
  echo "ERROR: scraper not found at $SCRAPER"
  exit 1
fi

if [ ! -f "$SCRIPT_DIR/.env" ]; then
  echo "WARNING: $SCRIPT_DIR/.env not found."
  echo "  Copy .env.example to .env and fill in your Gmail App Password"
  echo "  before the first scheduled run, or emailing will be skipped."
fi

# Cron line: every Monday at 6:00 AM
CRON_LINE="0 6 * * 1 cd \"$SCRIPT_DIR\" && $PYTHON \"$SCRAPER\" --email >> \"$LOGFILE\" 2>&1"

# Add only if not already present
( crontab -l 2>/dev/null | grep -qF "$SCRAPER" ) && {
  echo "Cron job already exists — no changes made."
  echo "Current crontab:"
  crontab -l | grep "$SCRAPER"
  exit 0
}

( crontab -l 2>/dev/null; echo "$CRON_LINE" ) | crontab -

echo ""
echo "✓ Cron job added. Scraper will run every Monday at 6:00 AM."
echo "  Log file: $LOGFILE"
echo "  CSV will be emailed to easttxkravmaga@gmail.com after each run."
echo ""
echo "To verify:   crontab -l"
echo "To remove:   crontab -e  →  delete the smith_county line"
