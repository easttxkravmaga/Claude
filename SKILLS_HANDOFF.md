# Skills Consolidation — Handoff Notes

**Date completed:** 2026-04-26
**Branch:** `claude/fix-skills-file-paths-BmQd5` → merged to `main`
**Authored by:** Claude Code session

---

## What Was Built

A bulletproof skill management system for the ETKM repo. The skills tree was
audited, consolidated, validated, and CI-enforced so that schema drift,
duplicate skills, and registry staleness are now impossible to merge.

## What Changed

### Repo layout
- **Removed:** 5 duplicate skills + corrupt `skills/README.md`
- **Moved to `skills/user/`:** 9 ETKM-specific skills (canonical home for all
  ETKM-specific intelligence)
- **Moved to `skills/`:** `karpathy-coding-guidelines` (general-purpose; not
  ETKM-specific)
- **Recovered into repo:** `etkm-leadgen-architecture` (was on Anthropic disk
  mount only; now also in repo)

### Frontmatter
- Lifted `version` and `updated` from body text into YAML frontmatter for 8
  skills that had them in the wrong place

### Tooling (`scripts/`)
- `skill_metadata.py` — shared stdlib YAML frontmatter parser. No PyYAML
  dependency; runs in any CI environment.
- `validate_skills.py` — schema enforcement. Required fields, semver versions,
  ISO dates, body length, name/directory match, corrupt-nesting detection.
- `generate_skills_registry.py` — auto-generates `SKILLS.md`. `--check` mode
  fails CI if the registry is stale instead of rewriting it.

### CI (`.github/workflows/validate-skills.yml`)
- Validates schema on every push to `skills/`, `scripts/`, or `SKILLS.md`
- Verifies `SKILLS.md` is current via `--check` mode
- Replaced a previously corrupted workflow with mangled Python heredoc
  indentation

### Registration manifest
- `skills/user/REGISTERED.txt` — human-editable mirror of what's mounted at
  `/mnt/skills/user/` on Claude.ai. CI warns on drift (skills registered but
  not in repo).

### Bug fixes
- `backend/app.py` `scaffold_skill` was generating SKILL.md templates without
  the required `updated:` field. Every scaffolded skill failed CI on push.
  Fixed: today's date now injected at scaffold time.
- `skill-lifecycle/SKILL.md` canonical template had the same gap. Fixed.
  Bumped to v1.1.

### Reference stubs
- `skills/user/etkm-brand-foundation/references/` — three "content needed"
  stubs created (`brand-identity.md`, `storybrand-framework.md`,
  `voice-and-themes.md`). The skill cross-references these but they did not
  exist. Stubs flag the gap; Nathan pastes real content from the Claude.ai
  skills UI when ready.

### Documentation
- `docs/anthropic-registration-request.md` — ready-to-send request listing the
  14 pending skills for Anthropic to register on the disk mount

---

## Final State

| Metric | Value |
|---|---|
| Total skills | 22 (1 general, 21 ETKM-specific) |
| Skills passing validation | 22/22 |
| Skills mounted on Claude.ai | 7 |
| Skills pending registration | 14 |
| `SKILLS.md` freshness | Current (CI-verified) |
| Working tree | Clean, on `main` |

---

## Open Items (Nathan)

1. **Send registration request.** Share `docs/anthropic-registration-request.md`
   with Anthropic to register the 14 pending skills on the disk mount. Update
   `skills/user/REGISTERED.txt` once they confirm and regenerate `SKILLS.md`.

2. **Replace the three reference stubs with real content.** Each stub is
   minimal and explicitly marked "Content needed." Open the Claude.ai skills
   UI for `etkm-brand-foundation`, copy the contents of each file from the
   `references/` folder there, and paste over the stub. Files:
   - `skills/user/etkm-brand-foundation/references/brand-identity.md`
   - `skills/user/etkm-brand-foundation/references/storybrand-framework.md`
   - `skills/user/etkm-brand-foundation/references/voice-and-themes.md`

3. **Verify Render deploy succeeded** for the `app.py` template fix. Live
   verification was not possible from this session (no Render API access).
   Confirm the deployed `scaffold_skill` now includes `updated:` in its output
   by calling it once and inspecting the template.

---

## How to Use the System Going Forward

### Adding or modifying a skill
1. Use `scaffold_skill` (the template now includes `updated:` automatically)
   — or follow the canonical template in `skill-lifecycle/SKILL.md`
2. Edit the SKILL.md content
3. Run `python3 scripts/validate_skills.py` — must pass
4. Run `python3 scripts/generate_skills_registry.py` — regenerates `SKILLS.md`
5. Commit both files together

### After Anthropic registers a skill
1. Add the skill name to `skills/user/REGISTERED.txt`
2. Run `python3 scripts/generate_skills_registry.py`
3. Commit

### When CI fails
- "missing required frontmatter field" → add the missing field to YAML
- "name does not match directory" → fix one or the other so they agree
- "version is not semver-style" → use `1.0` or `2.3.1`, not `v1.0` or `1`
- "SKILLS.md is stale" → run the generator and commit the result
- "CORRUPT path detected: skills/user/user/" → another path-prefix regression;
  inspect `app.py` `scaffold_skill`/`push_skill` for missing strip logic

---

## Commits in This Effort

```
a8c343c  docs: add voice-and-themes.md stub for etkm-brand-foundation references
cc60d25  docs: add storybrand-framework.md stub for etkm-brand-foundation references
c52459a  docs: add brand-identity.md stub for etkm-brand-foundation references
386578f  docs: add Anthropic skill registration request for 14 pending skills
dfd97e4  Merge claude/fix-skills-file-paths-BmQd5 into main
b07fe42  Fix scaffold_skill and skill-lifecycle template: add required updated field
ed71e1a  Add etkm-leadgen-architecture skill and update SKILLS.md registry
e6db30f  Enforce skill schema and SKILLS.md freshness in CI
e4d0084  Add SKILLS.md generator and disk-mount registration manifest
e088343  Lift version/updated metadata into YAML frontmatter
fc237dc  Consolidate skill locations: ETKM skills under skills/user/, general under skills/
303eaf6  Remove duplicate skills and corrupt skills/README.md
```
