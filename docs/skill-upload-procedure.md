# Skill Upload Procedure — Claude.ai

**Purpose:** Get any skill from this repo onto the `/mnt/skills/user/` disk
mount in your Claude.ai chat sessions, where it auto-loads when triggered.

**Authority:** This is a self-service process. There is no Anthropic team to
email — you upload skills yourself through the Claude.ai UI.

---

## One-Time Setup

Confirm Skills are enabled on your account:

- Plan: Skills are available on Free, Pro, Max, and Team plans
- Team plan: an admin must enable it at the org level first
- Open `claude.ai`, go to **Customize → Skills**. If you see the page, you're set.

---

## Standard Process (Every Skill)

### Step 1 — Package the skill into a ZIP

Run from the repo root:

```bash
# Package one skill
python3 scripts/package_skills.py etkm-cta-architecture

# Package every pending skill at once (recommended for first-time bulk upload)
python3 scripts/package_skills.py --pending

# Package every skill in skills/user/ (use after a major refactor)
python3 scripts/package_skills.py --all
```

ZIPs land in `dist/skills/<skill-name>.zip`. The script structures each ZIP so
the skill folder is the ZIP root — this is what Claude.ai expects. Do not
re-zip manually; use the script.

### Step 2 — Upload to Claude.ai

1. Open `claude.ai` → **Customize → Skills**
2. Click **+** then **+ Create skill**
3. Drag-and-drop the ZIP from `dist/skills/`
4. Confirm the skill appears in your Skills list and the toggle is **on**

Repeat for each ZIP.

### Step 3 — Mirror the registration in the repo

Once Claude.ai confirms the upload:

1. Open `skills/user/REGISTERED.txt`
2. Add the skill name on its own line, alphabetical order
3. Run `python3 scripts/generate_skills_registry.py`
4. Commit both files together with message `docs: register <skill-name> on disk mount`

This keeps `SKILLS.md` showing the true mount state and lets CI catch drift.

### Step 4 — Verify in a chat session

1. Open a fresh Claude.ai chat
2. Use a phrase that should trigger the skill (the skill's `description` field
   tells you which phrases load it)
3. Confirm Claude loads the skill and behaves accordingly

---

## When You Update a Skill

Skills do not auto-sync from the repo to your Claude.ai account. Every edit
requires re-uploading.

1. Edit `skills/user/<skill-name>/SKILL.md` and bump the `version` field
2. Run validators: `python3 scripts/validate_skills.py`
3. Re-package: `python3 scripts/package_skills.py <skill-name>`
4. In Claude.ai → Customize → Skills, find the skill, click **Edit** (or
   delete and re-upload — UI may vary)
5. Upload the new ZIP

---

## Bulk Upload — Currently Pending Skills

14 skills are in this repo but not yet on the Claude.ai disk mount. To onboard
all of them:

```bash
python3 scripts/package_skills.py --pending
```

Then upload each ZIP from `dist/skills/` into Claude.ai → Customize → Skills.
After all 14 are uploaded, run:

```bash
# Add the 14 names to REGISTERED.txt manually, alphabetical order
# Then regenerate SKILLS.md:
python3 scripts/generate_skills_registry.py
git add skills/user/REGISTERED.txt SKILLS.md
git commit -m "docs: register 14 skills on Claude.ai disk mount"
git push origin main
```

---

## Constraints to Be Aware Of

- **`description` field** — Anthropic's docs recommend keeping it concise
  (their public guidance mentions a ~200-character target). Some ETKM skills
  exceed this; existing mounted skills like `etkm-brand-foundation` work fine
  despite long descriptions, but if an upload fails, shorten the description
  and try again.
- **`name` field** — 64 character maximum. All ETKM skills are well under this.
- **Skills are private** to your individual Claude.ai account. They do not
  sync to other surfaces (API, Claude Code, etc.) automatically.
- **No directory-name magic** — Anthropic's example layouts use `resources/`
  and `templates/` for supporting files, but the ETKM repo uses `references/`
  for `etkm-brand-foundation`. The runtime reads SKILL.md and follows
  references the SKILL.md text describes; directory naming is convention, not
  enforcement. If a sub-folder file fails to load after upload, rename it to
  `resources/` and re-upload as a fallback.

---

## What Not to Do

- Do not zip the folder's parent — the ZIP root must be the skill folder
  itself (the packaging script handles this; don't bypass it)
- Do not edit skills directly in the Claude.ai UI without mirroring back to
  the repo — the repo is the source of truth, and CI enforces schema
- Do not skip the version bump on edits — `etkm-deliverable-qc` and
  `skill-lifecycle` both treat the version field as authoritative
- Do not add a skill name to `REGISTERED.txt` before confirming the Claude.ai
  upload actually succeeded — `REGISTERED.txt` mirrors reality, not intent
