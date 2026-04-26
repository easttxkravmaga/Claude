#!/usr/bin/env python3
"""Package skills into ZIP files ready for upload to Claude.ai → Customize → Skills.

Claude.ai expects each skill as a ZIP whose root is the skill folder itself
(SKILL.md must sit at the ZIP root, not inside a parent directory). This script
produces correctly-structured ZIPs in dist/ for any combination of skills.

Run from the repo root:

    # Package every skill in skills/user/
    python3 scripts/package_skills.py --all

    # Package only skills not yet on the disk mount (per REGISTERED.txt)
    python3 scripts/package_skills.py --pending

    # Package a specific skill or list of skills
    python3 scripts/package_skills.py etkm-audience-intelligence etkm-cta-architecture

After running, drag-and-drop each ZIP into Claude.ai → Customize → Skills.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path

from skill_metadata import (
    REPO_ROOT,
    USER_SKILLS_ROOT,
    collect_skills,
    load_registered,
)

DIST_DIR = REPO_ROOT / "dist" / "skills"


def package_skill(skill_dir: Path, dist: Path) -> Path:
    """Zip skill_dir so the skill folder name is the ZIP root.

    Resulting ZIP layout:
        <skill-name>/SKILL.md
        <skill-name>/references/...   (if present)
        <skill-name>/<other files>... (if present)
    """
    name = skill_dir.name
    out = dist / f"{name}.zip"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(skill_dir.rglob("*")):
            if path.is_dir():
                continue
            arcname = Path(name) / path.relative_to(skill_dir)
            zf.write(path, arcname.as_posix())
    return out


def resolve_targets(args: argparse.Namespace) -> list[Path]:
    if args.all:
        return sorted(p for p in USER_SKILLS_ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())

    if args.pending:
        registered = set(load_registered())
        repo = collect_skills()
        pending = [
            USER_SKILLS_ROOT / s.name
            for s in repo
            if s.location.startswith("skills/user/") and s.name not in registered
        ]
        return sorted(pending)

    if not args.names:
        print("error: pass --all, --pending, or one or more skill names.", file=sys.stderr)
        sys.exit(2)

    targets: list[Path] = []
    missing: list[str] = []
    for name in args.names:
        candidate = USER_SKILLS_ROOT / name
        if candidate.is_dir() and (candidate / "SKILL.md").is_file():
            targets.append(candidate)
        else:
            missing.append(name)
    if missing:
        print(f"error: not found in skills/user/: {', '.join(missing)}", file=sys.stderr)
        sys.exit(2)
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="package every skill in skills/user/")
    group.add_argument("--pending", action="store_true", help="package only skills missing from REGISTERED.txt")
    parser.add_argument("names", nargs="*", help="explicit skill names (relative to skills/user/)")
    parser.add_argument("--clean", action="store_true", help="delete dist/skills/ before packaging")
    args = parser.parse_args()

    if args.clean and DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)

    targets = resolve_targets(args)
    if not targets:
        print("nothing to package.")
        return 0

    print(f"Packaging {len(targets)} skill(s) into {DIST_DIR.relative_to(REPO_ROOT)}/")
    for skill_dir in targets:
        out = package_skill(skill_dir, DIST_DIR)
        size_kb = out.stat().st_size / 1024
        print(f"  {out.relative_to(REPO_ROOT)} ({size_kb:.1f} KB)")

    print()
    print("Next: open Claude.ai → Customize → Skills → '+' → '+ Create skill' and")
    print("upload each ZIP. Skills appear in your Skills list and can be toggled on/off.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
