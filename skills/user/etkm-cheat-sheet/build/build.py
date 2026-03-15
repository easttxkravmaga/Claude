#!/usr/bin/env python3
"""
ETKM Cheat Sheet Builder
========================
Reads a book JSON data file and renders the canonical HTML template.

Usage:
  # Build one book
  python build.py gift_of_fear

  # Build one book with explicit paths
  python build.py gift_of_fear --data data/ --template template/ --output output/

  # Build ALL books in the data directory
  python build.py --all

  # Build all and report
  python build.py --all --verbose

Requirements:
  pip install jinja2
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
except ImportError:
    print("ERROR: Jinja2 not installed. Run: pip install jinja2")
    sys.exit(1)


# ─── Paths (relative to this script) ───────────────────────────────────
SCRIPT_DIR    = Path(__file__).parent
DATA_DIR      = SCRIPT_DIR.parent / "data"
TEMPLATE_DIR  = SCRIPT_DIR.parent / "template"
OUTPUT_DIR    = SCRIPT_DIR.parent / "output"
TEMPLATE_FILE = "cheat_sheet.html"


# ─── Validation ──────────────────────────────────────────────────────────────
VALID_BELT_LEVELS   = {"Yellow", "Orange", "Green", "Blue", "Brown", "Black", "All"}
VALID_PEACE_PILLARS = {"Prepared", "Empowered", "Aware", "Capable", "Engaged"}
VALID_ARC_POSITIONS = {"foundation", "intermediate", "advanced", "all-levels"}
VALID_ETKM_PILLARS  = {
    "Mindset", "Awareness", "Tactics", "Skills",
    "Physiology", "Identity", "Resilience", "Recovery", "Prepared"
}

def validate(data: dict, book_id: str) -> list:
    """Returns a list of validation errors. Empty list = valid."""
    errors = []
    meta = data.get("meta", {})
    journey = data.get("journey", {})
    pillars = data.get("pillars", [])
    principles = data.get("principles", [])
    action = data.get("action_plan", {})

    for field in ["book_id", "title", "title_line_1", "title_line_2", "author", "year"]:
        if not meta.get(field):
            errors.append(f"meta.{field} is missing or empty")
    if meta.get("book_id") != book_id:
        errors.append(f"meta.book_id '{meta.get('book_id')}' does not match filename '{book_id}'")

    if not journey.get("identity_shift"):
        errors.append("journey.identity_shift is missing")
    if not journey.get("unlocks"):
        errors.append("journey.unlocks is missing")

    if not (2 <= len(pillars) <= 4):
        errors.append(f"pillars: expected 2-4, got {len(pillars)}")
    for i, p in enumerate(pillars):
        if p.get("name") not in VALID_ETKM_PILLARS:
            errors.append(f"pillars[{i}].name '{p.get('name')}' is not a valid ETKM pillar")
        if not p.get("why"):
            errors.append(f"pillars[{i}].why is empty")

    if not (8 <= len(principles) <= 12):
        errors.append(f"principles: expected 8-12, got {len(principles)}")
    for i, p in enumerate(principles):
        if not p.get("text"):
            errors.append(f"principles[{i}].text is empty")

    week = action.get("this_week", [])
    month = action.get("this_month", [])
    perm = action.get("permanent", [])
    if not (2 <= len(week) <= 3):
        errors.append(f"action_plan.this_week: expected 2-3 items, got {len(week)}")
    if not (3 <= len(month) <= 4):
        errors.append(f"action_plan.this_month: expected 3-4 items, got {len(month)}")
    if not (3 <= len(perm) <= 4):
        errors.append(f"action_plan.permanent: expected 3-4 items, got {len(perm)}")

    return errors


def build(book_id: str, data_dir: Path, template_dir: Path, output_dir: Path, verbose: bool = False) -> bool:
    data_file = data_dir / f"{book_id}.json"

    if not data_file.exists():
        print(f"  \u2717 ERROR: {data_file} not found")
        return False

    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  \u2717 ERROR: {data_file} \u2014 invalid JSON: {e}")
        return False

    errors = validate(data, book_id)
    if errors:
        print(f"  \u2717 VALIDATION FAILED: {book_id}")
        for err in errors:
            print(f"      \u2022 {err}")
        return False

    if verbose:
        print(f"  \u2713 Valid: {data['meta']['title']} \u2014 {data['meta']['author']}")

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        undefined=StrictUndefined,
        autoescape=True
    )

    try:
        template = env.get_template(TEMPLATE_FILE)
    except Exception as e:
        print(f"  \u2717 ERROR: Could not load template: {e}")
        return False

    try:
        html = template.render(**data)
    except Exception as e:
        print(f"  \u2717 ERROR: Template render failed for {book_id}: {e}")
        return False

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"04_{book_id}_cheat_sheet.html"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = output_file.stat().st_size / 1024
    print(f"  \u2713 Built: {output_file.name}  ({size_kb:.1f} KB)")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="ETKM Cheat Sheet Builder \u2014 generates HTML from JSON data files"
    )
    parser.add_argument("book_id", nargs="?", help="Book ID to build (e.g. gift_of_fear)")
    parser.add_argument("--all", "-a", action="store_true", help="Build all JSON files in the data directory")
    parser.add_argument("--data", type=Path, default=DATA_DIR)
    parser.add_argument("--template", type=Path, default=TEMPLATE_DIR)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    print(f"\n{'\u2550' * 50}")
    print(f"  ETKM Cheat Sheet Builder")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'\u2550' * 50}\n")

    if args.all:
        json_files = sorted(args.data.glob("*.json"))
        if not json_files:
            print(f"  No JSON files found in {args.data}")
            sys.exit(1)
        print(f"  Building {len(json_files)} book(s) from {args.data}\n")
        results = []
        for f in json_files:
            book_id = f.stem
            print(f"  \u2192 {book_id}")
            success = build(book_id, args.data, args.template, args.output, args.verbose)
            results.append((book_id, success))
        print(f"\n{'\u2500' * 50}")
        passed = sum(1 for _, s in results if s)
        failed = len(results) - passed
        print(f"  Built: {passed}  Failed: {failed}")
        if failed:
            sys.exit(1)

    elif args.book_id:
        print(f"  Building: {args.book_id}\n")
        success = build(args.book_id, args.data, args.template, args.output, args.verbose)
        if not success:
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)

    print(f"\n  Output: {args.output.resolve()}")
    print(f"{'\u2550' * 50}\n")


if __name__ == "__main__":
    main()
