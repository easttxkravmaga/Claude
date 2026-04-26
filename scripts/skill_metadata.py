"""Shared helpers for skill registry tooling.

Walks the repo's skills tree, parses YAML frontmatter from each SKILL.md,
and surfaces the disk-mount registration list. Stdlib only — no PyYAML
dependency so the scripts run in any CI environment.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"
USER_SKILLS_ROOT = SKILLS_ROOT / "user"
REGISTERED_FILE = USER_SKILLS_ROOT / "REGISTERED.txt"

REQUIRED_FIELDS = ("name", "version", "updated", "description")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VERSION_RE = re.compile(r"^\d+(\.\d+){1,2}$")


@dataclass
class Skill:
    name: str
    location: str
    path: Path
    frontmatter: dict
    body_chars: int = 0
    issues: list = field(default_factory=list)

    @property
    def version(self) -> str:
        return str(self.frontmatter.get("version", "")).strip() or "—"

    @property
    def updated(self) -> str:
        return str(self.frontmatter.get("updated", "")).strip() or "—"

    @property
    def description(self) -> str:
        return str(self.frontmatter.get("description", "")).strip()


def parse_frontmatter(text: str) -> tuple[dict, int]:
    """Return (fields, body_char_count). Handles flat scalars and `>`/`|`
    block scalars. Lists and nested mappings are captured as empty
    strings — adequate for our schema, which only requires flat fields."""
    if not text.startswith("---"):
        return {}, len(text)
    end = text.find("\n---", 4)
    if end < 0:
        return {}, len(text)
    head = text[4:end]
    body_chars = len(text) - (end + 4)

    out: dict = {}
    current_key: str | None = None
    current_block: list[str] = []
    for line in head.split("\n"):
        is_top_level = bool(line) and not line[0].isspace()
        m = re.match(r"^([a-zA-Z_][\w-]*):\s*(.*)$", line) if is_top_level else None
        if m:
            if current_key is not None:
                out[current_key] = " ".join(s.strip() for s in current_block if s.strip())
            current_key = m.group(1)
            value = m.group(2).strip()
            if value in (">", "|", ">-", "|-"):
                current_block = []
            else:
                out[current_key] = value
                current_key = None
                current_block = []
        elif current_key is not None:
            current_block.append(line)
    if current_key is not None:
        out[current_key] = " ".join(s.strip() for s in current_block if s.strip())
    return out, body_chars


def collect_skills() -> list[Skill]:
    """Every SKILL.md under skills/ and skills/user/, sorted by location."""
    skills: list[Skill] = []
    seen_dirs: set[Path] = set()
    for parent in (SKILLS_ROOT, USER_SKILLS_ROOT):
        if not parent.is_dir():
            continue
        for child in sorted(parent.iterdir()):
            if not child.is_dir():
                continue
            if child == USER_SKILLS_ROOT:
                continue
            if child in seen_dirs:
                continue
            seen_dirs.add(child)
            skill_md = child / "SKILL.md"
            if not skill_md.is_file():
                continue
            text = skill_md.read_text(encoding="utf-8")
            fm, body_chars = parse_frontmatter(text)
            skills.append(
                Skill(
                    name=str(fm.get("name", child.name)).strip(),
                    location=str(skill_md.relative_to(REPO_ROOT)),
                    path=skill_md,
                    frontmatter=fm,
                    body_chars=body_chars,
                )
            )
    skills.sort(key=lambda s: s.location)
    return skills


def load_registered() -> list[str]:
    if not REGISTERED_FILE.is_file():
        return []
    out = []
    for raw in REGISTERED_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out
