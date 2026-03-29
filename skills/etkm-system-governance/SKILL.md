---
name: etkm-system-governance
version: 1.0
updated: 2026-03-29
description: >
  The constitution for the ETKM skill and database system. Load this skill whenever
  creating a new skill, modifying an existing skill, adding or editing Notion databases,
  preparing a Manus handoff, syncing laptops with GitHub, or running a quarterly review.
  This skill governs how every other skill gets created, edited, versioned, stored, and
  deployed. Trigger for: "create a skill", "new skill", "edit skill", "update database",
  "add a field", "Manus handoff", "push to GitHub", "sync skills", "quarterly review",
  "audit skills", "version check", "skill template", or any task that modifies the
  infrastructure of the ETKM system itself. Load this skill in the ETKM System
  Maintenance project. It does not need to be in every project.
---

# ETKM System Governance

**Version:** 1.0
**Established:** 2026-03-29
**Purpose:** Single source of rules for how skills, databases, and deployments work across the ETKM system.

---

## SECTION 1: SKILL CREATION RULES

### The 6-Section Template

Every ETKM skill follows this exact structure. No exceptions.

```
SECTION 1: HEADER
- Skill name, version (V1.0), date, one-line purpose
- What this skill does
- What databases it references (if any)

SECTION 2: WHEN TO LOAD
- Trigger phrases and session types
- What NOT to load this for

SECTION 3: DECISION LOGIC
- Rules, routing tables, decision trees
- "If X, query Y. If Z, do W."
- Non-negotiable rules that override everything

SECTION 4: NOTION REFERENCES
- Exact database names and what to query for each task type
- Field-level guidance: which fields matter for which job
- (Omit this section only if the skill genuinely does not reference any database)

SECTION 5: QUALITY GATES
- What to check before output ships
- Common failure modes specific to this skill's domain

SECTION 6: CHANGELOG
- V1.0 — date — initial build
- V1.1 — date — what changed
```

### Naming Convention

- All skills: `etkm-[domain]` — lowercase, hyphens, no spaces
- The only exception: `nate-collaboration-workflow` (historical, stays as-is)

### Version Numbering

| Change Type | Version Bump | Example |
|---|---|---|
| Typo fix, corrected data, added a field | V1.0 → V1.1 | Fixed #CC0000 color code |
| New section added, rule changed, database schema updated | V1.1 → V1.2 | Added error recovery protocol |
| Structural change, merge, scope change | V1.x → V2.0 | Merged 4 skills into one |

Every version change gets a one-line entry in the CHANGELOG section.

### Size Limits

- Target: 5-8K per skill
- Hard ceiling: 15K
- If a skill exceeds 10K, audit whether data belongs in a Notion database instead
- Skills carry logic. Databases carry data. Never duplicate data in a skill that exists in a database.

### New Skill Gate — Three Questions

Before creating any new skill, answer these three questions:

1. Does this belong inside an existing skill as a new section?
2. Does the data belong in an existing Notion database as new records?
3. Is this a genuinely new domain that doesn't fit anywhere?

Only if the answer to #3 is yes does a new skill get created. And it follows the 6-section template.

### Where Skills Live

| Location | Role |
|---|---|
| GitHub (`easttxkravmaga/Claude`) | Single source of truth. All skills stored here. |
| ETKM MCP server | Serves skills on demand via `get_skill`. Reads from GitHub. |
| Claude Project Knowledge | Always-on skills only (4 files). Lightweight copies. |
| Local laptop skill folders | Cloned from GitHub. Synced via `git pull`. |

---

## SECTION 2: NOTION DATABASE RULES

### Location

All reference databases live under: **AI Resources → Skill Reference Data**

No reference databases outside this location. Operational databases (Big Projects List, Asset Registry, etc.) are separate and not governed by this skill.

### Naming Convention

- Database title: "ETKM [Domain Name]"
- Must match the skill it backs (e.g., ETKM Audience Segments → `etkm-audience-intelligence`)

### Schema Standards

- Every field has a COMMENT description explaining what goes in it
- Every record is self-contained — Claude can pull one record and have everything it needs without a second query
- SELECT fields use consistent color coding across databases (green = active/positive, red = negative/retired, yellow = pending, blue = informational)

### No Orphan Records

- Every database record maps to something in the CRM, the funnel, or the curriculum
- If a record doesn't map to an active system component, it gets a "Retired" status, not deleted
- New records require all required fields populated. No partial records.

### Sync Rule

- New Pipedrive label → update Arc/CRM Crosswalk in Notion AND update the corresponding Audience Segment record
- New audience segment in Notion → map arc labels before it is used in any campaign
- No orphaned arcs. No unmapped segments.

---

## SECTION 3: SKILL-TO-DATABASE RELATIONSHIP

### The Core Rule

Skills carry logic. Databases carry data. Never duplicate.

| Lives in the Skill | Lives in the Database |
|---|---|
| Decision rules and routing logic | Segment profiles, hooks, headlines, objections |
| "When to load" triggers | Pipeline stages, label IDs, automation specs |
| Quality gates and checklists | Email sequence specs, timing patterns |
| Non-negotiable rules | Offer details, pricing, value equations |
| Changelog and version history | Framework templates and structures |

### How Skills Reference Databases

Every slim skill's Section 4 (Notion References) must include:

1. The exact database name
2. What to query for each task type (e.g., "When writing copy for a specific audience, query ETKM Audience Segments for the matching segment code")
3. Which fields are critical for which job (e.g., "For ad copy: use Hooks, Headlines, and CTAs fields. For email: use Email Subjects and Objections fields.")

### When Data Doesn't Exist Yet

If a skill needs data that doesn't exist in a database:

1. Add the data to the appropriate database first
2. Then reference it from the skill
3. Never put raw data in the skill as a "temporary" measure — it becomes permanent

---

## SECTION 4: MANUS HANDOFF DOCTRINE

### When a Handoff is Needed

- Any new or updated skill file needs to be pushed to GitHub
- Any Pipedrive configuration change (labels, fields, stages)
- Any deployment to Cloud Run or other infrastructure
- Any browser automation task (WordPress, Make.com)

### What Claude Produces for Every Handoff

Two deliverables, always:

**1. The .zip file** — contains the actual files to be pushed or deployed

**2. The Handoff Brief** — plain text, follows this exact format:

```
ETKM HANDOFF BRIEF
Date: [date]
From: Claude
To: Manus
Type: [GitHub Push / Pipedrive Update / Deployment / Browser Automation]

ACTION REQUIRED:
1. [First specific action]
2. [Second specific action]
3. [Continue as needed]

FILES:
[file name] → [exact destination path]
[file name] → [exact destination path]

COMMIT MESSAGE (if GitHub):
"[Single clear commit message]"

VERIFICATION:
- [ ] [What Manus checks after step 1]
- [ ] [What Manus checks after step 2]

DO NOT:
- [Anything Manus should NOT touch or modify]
```

### Handoff Rules

- One commit per handoff. No multi-commit instructions.
- File-level specificity — never "push the whole folder." Name every file and its destination.
- Verification checks are mandatory. No handoff ships without at least one.
- "DO NOT" section is mandatory. Always specify what Manus should leave alone.

### When No Handoff is Needed

- Notion database edits — Nathan edits directly, Claude reads live. No push required.
- Notion schema changes — only need a handoff if a skill file must be updated to reference new fields.

---

## SECTION 5: LAPTOP SYNC PROTOCOL

### Architecture

GitHub (`easttxkravmaga/Claude`) is the single source of truth. Both laptops pull from it.

```
GitHub Repo (source of truth)
    ↓ Manus pushes
    ↓
    ├── Laptop 1: git pull → local skills folder → Claude Desktop reads
    └── Laptop 2: git pull → local skills folder → Claude Desktop reads
    ↓
    ETKM MCP Server: reads from GitHub → serves via get_skill
```

### Initial Setup (one time per laptop)

1. Open terminal
2. Navigate to desired location: `cd ~/Documents` (or wherever skills should live)
3. Clone the repo: `git clone https://github.com/easttxkravmaga/Claude.git`
4. Point Claude Desktop's skill folder to: `[clone location]/Claude/skills/`
5. Verify: open Claude Desktop, check that skills load correctly

### Sync Process (after any skill update)

1. Claude produces updated skill files → packaged in .zip with Handoff Brief
2. Nathan gives Manus the brief → Manus pushes to GitHub
3. On each laptop, open terminal in the repo folder:
   ```
   cd ~/Documents/Claude
   git pull
   ```
4. Claude Desktop picks up the changes next session

### Drift Check (part of quarterly review)

1. Run `ETKM MCP:list_skills` to get GitHub/MCP skill list
2. Compare against local folder on each laptop: `ls skills/*/SKILL.md`
3. Flag any mismatches
4. Resolve with `git pull` — never manually copy files

### Rules

- Never manually copy skill files between laptops
- Never edit skill files directly on a laptop — edit in Claude session, output to file, push via Manus
- GitHub is the hub. Everything flows through it.
- If a laptop's local folder has files that GitHub doesn't, those files are orphans — investigate before deleting

---

## SECTION 6: QUALITY GATES

### New Skill — Before It Ships

- [ ] Follows 6-section template exactly
- [ ] Has V1.0 version stamp in header
- [ ] Has changelog entry
- [ ] Naming follows `etkm-[domain]` convention
- [ ] Under 15K (ideally under 8K)
- [ ] Passed the 3-question new-skill gate
- [ ] References at least one Notion database (or documents why it doesn't need one)
- [ ] Trigger phrases in description are specific and "pushy" enough to ensure loading when relevant
- [ ] No raw data that belongs in a Notion database

### New Database — Before It Ships

- [ ] Lives under AI Resources → Skill Reference Data
- [ ] Title follows "ETKM [Domain Name]" convention
- [ ] Every field has a COMMENT description
- [ ] Referenced by at least one skill
- [ ] At least one record populated to prove the schema works

### New Database Record — Before It Ships

- [ ] All required fields populated (no blanks on critical fields)
- [ ] Maps to an active system component (CRM label, funnel stage, audience segment, etc.)
- [ ] If it has CRM mapping fields, the Pipedrive IDs are current

### Schema Change — Before It Ships

- [ ] Version increment on the database (noted in the skill that references it)
- [ ] Version increment on the referencing skill
- [ ] Changelog entries on both
- [ ] No orphaned records from the change
- [ ] Manus handoff brief produced if the skill file needs to be pushed

### Manus Handoff — Before It Sends

- [ ] .zip file contains all and only the files listed in the brief
- [ ] Brief follows the standardized format exactly
- [ ] Every file has a named destination path
- [ ] Verification checks are specific and testable
- [ ] "DO NOT" section is present
- [ ] Single commit message is clear and descriptive

---

## SECTION 7: QUARTERLY REVIEW PROTOCOL

**Frequency:** Once every 3 months (first review: June 2026)
**Duration:** 30 minutes
**Owner:** Nathan + Claude

### The Checklist

1. **Skill Inventory**
   - Pull `ETKM MCP:list_skills` — compare to master list in punch list
   - Check for new skills that appeared without going through the gate
   - Check for skills that have grown beyond their scope (split needed?)
   - Check for skills that overlap (merge needed?)

2. **Version Audit**
   - Every skill should have a current version stamp
   - Any skill last updated more than 3 months ago — review for staleness
   - Check that GitHub versions match MCP-served versions

3. **Notion Database Health**
   - Check each database for stale or outdated records
   - Check for records that no longer map to anything active
   - Verify Pipedrive IDs are still current in CRM Architecture and Audience Segments

4. **Laptop Sync**
   - Verify both laptops are current with GitHub
   - `git pull` on both if needed
   - Check for orphan files

5. **System Metrics**
   - Note total skill count (target: stay under 15)
   - Note total database record count
   - Note any context window overflow incidents since last review
   - Note any drift incidents (wrong version loaded, stale data referenced)

6. **Action Items**
   - List any skills to update, merge, or retire
   - List any database records to add or archive
   - Schedule Manus handoff if changes are needed

---

## SECTION 8: CHANGELOG

- V1.0 — 2026-03-29 — Initial build. Covers skill creation, Notion database rules, skill-to-database relationships, Manus handoff doctrine, laptop sync protocol, quality gates, and quarterly review protocol.
