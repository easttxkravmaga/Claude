#!/usr/bin/env python3
"""Validate every SKILL.md against the schema. Exit 1 on any issue.

Run locally:

    python3 scripts/validate_skills.py

CI invokes this on every push (`.github/workflows/validate-skills.yml`).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from skill_metadata import (
    DATE_RE,
    REPO_ROOT,
    REQUIRED_FIELDS,
    SKILLS_ROOT,
    USER_SKILLS_ROOT,
    VERSION_RE,
    Skill,
    collect_skills,
    load_registered,
)

MIN_BODY_CHARS = 100
MIN_DESCRIPTION_CHARS = 60


def check_corrupt_nesting() -> list[str]:
    """Catch the regression that motivated all this — skills/user/user/."""
    issues: list[str] = []
    bad_root = USER_SKILLS_ROOT / "user"
    if bad_root.exists():
        issues.append(
            f"CORRUPT path detected: {bad_root.relative_to(REPO_ROOT)} — "
            "skill_name was passed with a 'user/' prefix. Move contents to "
            "skills/user/<name>/ and delete the nested directory."
        )
    return issues


def validate_skill(s: Skill) -> list[str]:
    issues: list[str] = []
    fm = s.frontmatter

    for field_name in REQUIRED_FIELDS:
        value = str(fm.get(field_name, "")).strip()
        if not value:
            issues.append(f"missing required frontmatter field: {field_name}")

    name = str(fm.get("name", "")).strip()
    dir_name = s.path.parent.name
    if name and name != dir_name:
        issues.append(f"name '{name}' does not match directory '{dir_name}'")

    version = str(fm.get("version", "")).strip()
    if version and not VERSION_RE.match(version):
        issues.append(f"version '{version}' is not semver-style (expected '1.0' or '2.3.1')")

    updated = str(fm.get("updated", "")).strip()
    if updated and not DATE_RE.match(updated):
        issues.append(f"updated '{updated}' is not ISO format (expected YYYY-MM-DD)")

    description = str(fm.get("description", "")).strip()
    if description and len(description) < MIN_DESCRIPTION_CHARS:
        issues.append(
            f"description is too short ({len(description)} chars) — must explain "
            "when to load the skill, scope, and exclusions"
        )

    if s.body_chars < MIN_BODY_CHARS:
        issues.append(
            f"body is too short ({s.body_chars} chars) — likely empty or stub"
        )

    return issues


def validate_registered(skills: list[Skill]) -> list[str]:
    """REGISTERED.txt must be parseable; phantoms are surfaced but not fatal."""
    issues: list[str] = []
    try:
        registered = load_registered()
    except Exception as e:
        issues.append(f"REGISTERED.txt unreadable: {e}")
        return issues
    repo_user = {s.name for s in skills if s.location.startswith("skills/user/")}
    phantoms = [name for name in registered if name not in repo_user]
    if phantoms:
        # Warn (not fail) — phantoms are documented in SKILLS.md.
        for name in phantoms:
            print(
                f"WARN: '{name}' is in REGISTERED.txt but not in skills/user/. "
                "Either author it or de-register at Anthropic.",
                file=sys.stderr,
            )
    return issues


def main() -> int:
    all_issues: list[str] = []

    for issue in check_corrupt_nesting():
        all_issues.append(issue)

    skills = collect_skills()
    if not skills:
        all_issues.append("no SKILL.md files found under skills/ — repo state looks broken")

    for s in skills:
        for issue in validate_skill(s):
            all_issues.append(f"{s.location}: {issue}")

    all_issues.extend(validate_registered(skills))

    if all_issues:
        print("SKILL VALIDATION FAILED:", file=sys.stderr)
        for issue in all_issues:
            print(f"  FAIL  {issue}", file=sys.stderr)
        return 1

    print(f"All {len(skills)} skills passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
