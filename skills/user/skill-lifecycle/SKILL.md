---
name: skill-lifecycle
version: 1.0
updated: 2026-04-26
description: >
  Governs the full lifecycle of ETKM skill creation and updates — naming
  conventions, authoring standards, validation, push process, and recovery.
  Load this skill any time a new skill is being built or an existing skill
  is being modified. Ensures skills never corrupt the ecosystem.
triggers:
  - "build a skill"
  - "create a skill"
  - "write a skill"
  - "update a skill"
  - "new skill"
  - "write a SKILL.md"
  - "skill authoring"
  - "push a skill"
  - any task where push_skill will be called
---

# Skill Lifecycle — ETKM Skill Authoring & Deployment Protocol

## Purpose

Skills are the intelligence layer of the ETKM AI stack. A corrupt or malformed
skill silently breaks Claude's behavior across every surface — Chat, Cowork, and
Code. This skill enforces a five-step lifecycle so every skill that enters the
repo is structurally sound, properly validated, and verified before it can cause
damage. Never author or push a skill without following this protocol.

## When to Load

Load this skill at the start of any session where:
- A new skill is being created from scratch
- An existing skill is being updated, renamed, or extended
- The user asks about skill structure, format, naming, or process
- You are about to call push_skill, scaffold_skill, or validate_skill
- A skill push failed and you are diagnosing why

## Canonical SKILL.md Template

Every skill starts from this template via scaffold_skill. Never start from a blank
file — the frontmatter must be correct from line one.

```
---
name: <skill-name-in-kebab-case>
version: 1.0
description: >
  One to three sentences. What this skill does and exactly when to load it.
  Be specific about trigger conditions — vague descriptions cause missed loads.
triggers:
  - "phrase that triggers this skill"
  - "another trigger phrase"
  - specific task or context that requires this skill
---

# Skill Title

## Purpose
One paragraph. What this skill enables Claude to do that it could not do
reliably otherwise.

## When to Load
Exhaustive trigger list. If Claude misses the trigger, the skill does not load.

## Core Instructions
Main content — process, rules, templates, constraints. Be concrete, not
aspirational. "Use 4-space indentation" not "use good formatting."

## Step-by-Step Process
1. Step one
2. Step two
3. Step three

## What Not to Do
- Never do X
- Avoid Y under all circumstances

## Recovery
What to do when things go wrong at each step.
```

## Naming Conventions

- Skill names are kebab-case, lowercase, no spaces, no special characters
- User skills live at skills/user/<skill-name>/SKILL.md in the repo
- When calling get_skill, push_skill, scaffold_skill, or validate_skill,
  pass only the base name: etkm-brand-foundation — never user/etkm-brand-foundation
- The path sanitizer strips user/ prefixes, but avoid passing them at all
- Names must be descriptive and specific: etkm-brand-foundation, not brand

## The Five-Step Lifecycle

Every skill creation or update follows this exact sequence. Do not skip steps.

### Step 1 — Scaffold
Call scaffold_skill(skill_name, description, triggers) to generate a pre-built
template with correct frontmatter. Fill in the returned template — never start
from a blank file or from memory.

### Step 2 — Author
Complete the template content. Before moving to Step 3, verify all of these:
- Minimum 100 characters of content after stripping whitespace
- YAML frontmatter block present (--- at top and closing --- after metadata)
- name and description fields populated with real content
- At least one meaningful section beyond frontmatter
- No placeholder text remaining in the template
- triggers list is exhaustive

### Step 3 — Validate (Pre-Push)
Call validate_skill(skill_name, content) before pushing. It runs the same guards
as push_skill but is non-destructive. Fix every reported error before proceeding.
Do not skip this step even if you are confident the content is correct.

A passing validation confirms:
- Content length >= 100 chars
- YAML frontmatter present and well-formed
- No double-nested path issues (user/user/ prefix)
- Required fields name and description present

### Step 4 — Push
Call push_skill(skill_name, content, commit_message).
- skill_name: base name only, no user/ prefix
- commit_message: use format feat: add <skill-name> skill or fix: update <skill-name> skill
- If push returns an error, read the error message carefully and fix at Step 2

### Step 5 — Verify
Immediately after a successful push, call get_skill(skill_name) and confirm:
- Response length is within a few characters of what was pushed
- Frontmatter is intact at the top of the response
- No truncation, garbling, or corruption is present

If verification fails, the push succeeded but the file is corrupt. Report the
discrepancy to the user before taking any further action.

## Content Quality Standards

Beyond the minimum validation guards, every shipped skill must meet these:

- Trigger coverage: Every realistic way a user could ask for this skill is listed
- Specificity: Instructions are concrete steps, not general guidance
- Anti-patterns: Every skill has a What Not to Do section
- Recovery: Every skill documents recovery steps for common failures
- Version: Increment version on every update — 1.0 to 1.1 for minor changes,
  1.x to 2.0 for rewrites

## Common Failures and Recovery

push_skill returns too short: Content was trimmed or lost during authoring.
Return to Step 2 and ensure the full content is present before retrying.

push_skill returns missing frontmatter: The --- block is missing or malformed.
Confirm the file starts with --- and has a closing --- after the metadata.

validate_skill reports warnings but no errors: Warnings are advisory. Fix them
if the skill will be a primary reference — skip them only for quick utility skills.

get_skill returns wrong content after push: The skill_name has a user/ prefix
somewhere in the call chain. Strip it and retry get_skill.

get_skill returns HTTP 404: Skill has not been pushed yet or the name is
misspelled. Call list_skills to confirm available skill names.

Render deploy fails after app.py change: Check the deploy log in Render
dashboard. If it is a Python syntax error, fix it in the GitHub editor and commit.

## What Not to Do

- Never call push_skill without first calling validate_skill
- Never author a skill starting from a blank file — always use scaffold_skill
- Never pass user/<skill-name> to push_skill or get_skill
- Never ship a skill with placeholder text still in the template
- Never skip the Step 5 verification read-back after push
- Never update a skill without incrementing its version number
- Never treat a warning from validate_skill as a pass if it blocks errors
