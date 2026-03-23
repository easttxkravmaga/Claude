# CLAUDE.md — East Texas Krav Maga (ETKM)
## Claude Code Operating Instructions
**Authority:** Nathan Lundstrom | etxkravmaga.com
**Repo:** easttxkravmaga/Claude
**Last Updated:** 2026-03-23

---

## RULE ZERO

Before any code is written, any file is created, or any agent is spawned:
**Read the skills. Load the standard. Then build.**

This is not optional. Projects that skip this step produce inferior output.
The ETKM production standard exists because improvisation fails.

---

## PART 1 — SESSION OPENING PROTOCOL

Every Claude Code session opens with these four steps in order.
Do not skip any step. Do not begin building until all four are complete.

### STEP 1 — Locate the Skills Directory

```bash
ls skills/
```

The skills directory lives at `skills/` in the repo root.
It contains every production standard, brand rule, workflow, and agent spec for ETKM.

Subdirectory layout:
```
skills/
  user/          ← ETKM-specific skills (always load these)
  public/        ← Format and tool skills (load when relevant)
  examples/      ← Builder utilities (load when relevant)
```

### STEP 2 — Load the Project Standard First

**Always load this skill before anything else:**

```bash
cat skills/user/etkm-project-standard/SKILL.md
```

This is the master container for all ETKM production work. It tells you:
- What a Project Card is and why it must exist before building
- The six layers every project must complete before production starts
- The agent stack structure for this project type
- The QC gates nothing ships without passing
- The handoff brief format for Manus and other tools

**If no Project Card exists for the task Nathan has described — build it before writing one line of code.**

### STEP 3 — Identify and Load Relevant Domain Skills

Based on the task, load the appropriate skills. Common loads:

| Task Type | Skills to Load |
|-----------|---------------|
| Any ETKM build | `etkm-project-standard`, `etkm-brand-kit`, `etkm-deliverable-qc` |
| Email / copy | + `etkm-brand-foundation`, `etkm-messaging-playbook` |
| PDF | + `etkm-brand-kit` (pdf skill from public/) |
| HTML / web page | + `etkm-brand-kit` (HTML = black bg, white text, red accent) |
| Lead magnet | + `etkm-lead-gen`, `etkm-funnel-master` |
| Nurture sequence | + `etkm-nurture-sequence`, `etkm-crm-doctrine` |
| Event page | + `etkm-event-page`, `etkm-event-planning` |
| Book asset | + `etkm-book-intelligence` |
| Workflow / automation | + `etkm-workflow-registry`, `etkm-pipedrive-manus` |
| Visual / image prompt | + `etkm-cinematic-doctrine` |
| Any output format | + `public/pdf`, `public/docx`, `public/pptx`, or `public/xlsx` |

**Load command pattern:**
```bash
cat skills/user/[skill-name]/SKILL.md
```

### STEP 4 — Check the Workflow Registry

Before building anything, confirm it hasn't already been built:

```bash
cat skills/user/etkm-workflow-registry/SKILL.md
```

Then fetch the live registry from Google Drive (ETKM AI Resources folder).
Check workflow status. Do not rebuild anything with status APPROVED, LOADED, LIVE, or DEPRECATED.

---

## PART 2 — AUTOMATIC SKILL DISCOVERY

When Nathan describes a task and the right skills aren't obvious, run this discovery sequence:

```bash
# 1. List all available user skills
ls skills/user/

# 2. Read the description block of any candidate skill
head -30 skills/user/[candidate-skill]/SKILL.md

# 3. Check the trigger: field — does the task match any trigger phrase?
grep -A 10 "trigger:" skills/user/[candidate-skill]/SKILL.md
```

**Skill selection rule:** If the trigger field of a skill matches the task being described — load it.
When in doubt, load it. Skills are free to read. Improvised decisions are expensive to fix.

**Never do any of the following without loading the relevant skill first:**
- Write ETKM copy (load `etkm-brand-foundation`)
- Produce a visual or colored output (load `etkm-brand-kit`)
- Build a PDF (load `public/pdf/SKILL.md`)
- Build a DOCX (load `public/docx/SKILL.md`)
- Build a PPTX (load `public/pptx/SKILL.md`)
- Finalize any deliverable (load `etkm-deliverable-qc`)
- Hand off to Manus (load `etkm-workflow-registry`)

---

## PART 3 — AGENT TEAMS

### When to Use Agent Teams

Use agent teams when the project has:
- Multiple distinct domains (frontend + backend, copy + code + QC)
- Parallel workstreams that don't have to wait on each other
- A need for agents to react to each other's output (QA loops, review cycles)
- 3 or more deliverables with separate ownership

Do NOT use agent teams for:
- Sequential tasks where step 2 always waits on step 1
- Simple single-file builds
- Anything that can be done in one focused pass

**Keep teams at 2–5 agents maximum.** More agents = more cost. Stay lean.

---

### Enabling Agent Teams

Agent teams are disabled by default. Enable at the project level:

```bash
# Claude Code will create this file automatically if you ask it to
.claude/settings.local.json
```

Content:
```json
{
  "experimental": {
    "agentTeams": true
  }
}
```

Or tell Claude Code: *"Enable agent teams by adding the required variable to our local project settings."*

---

### The ETKM Agent Stack

Every ETKM project has a defined agent stack in its Project Card (Layer 3 of the project standard).
The standard stack maps like this:

| Agent | Role | Receives | Returns |
|-------|------|----------|---------|
| **Strategist** | Defines structure, approach, audience alignment | Project Card + skills | Outline + strategic direction |
| **Writer/Builder** | Produces content or build | Outline + brand rules | Draft deliverables |
| **Brand Editor** | Applies voice, visual, format standards | Draft deliverables | Branded deliverables |
| **QC Agent** | Holds against all gates — rejects or passes | Branded deliverables | PASS or FAIL with findings |

Add specialized agents when the project calls for them:

| Agent | Add When |
|-------|----------|
| **Extractor** | Input is a book, document, or research report to mine |
| **Code Agent** | Project includes scripts, apps, or APIs |
| **Deployment Agent** | Output goes to Pipedrive, WordPress, or GitHub |
| **Architect** | Project has 3+ deliverables that need structure before writing |

---

### How to Prompt Agent Teams

**Pattern:**

```
Goal: [What the complete project produces and why]

Create a team of [N] agents using [model].

Agent 1 — [Role Name]
Job: [Exactly what this agent does]
Receives: [What it starts with]
Produces: [What it hands off]
Territory: [Its files — it does not touch other agents' files]
Skills to load: [List the skill files from skills/user/ this agent needs]

Agent 2 — [Role Name]
Job: [...]
Receives: [Agent 1's output]
Produces: [...]
Territory: [Its files]
Skills to load: [...]

QC Agent — Brand & Quality Gate
Job: Review every deliverable against etkm-deliverable-qc gates
Receives: All final deliverables from all agents
Produces: PASS or FAIL with specific findings per gate
Authority: Any FAIL sends the deliverable back to its owner agent for correction

Shared rules for all agents:
- Load skills from skills/user/ before doing any work
- No agent improvises brand, voice, color, or format decisions
- Each agent owns its territory — do not overwrite another agent's files
- Nothing moves to QC until the producing agent confirms it is complete
```

---

### Real ETKM Example — Lead Gen PDF Team

```
Goal: Produce a complete, brand-compliant lead gen PDF for the adult mother
persona, ready for WordPress upload, passing all QC gates.

Create a team of 4 agents using claude-sonnet-4-6.

Agent 1 — Content Strategist
Job: Define PDF structure, section order, and copy brief
Receives: Project Card, etkm-lead-gen skill, etkm-funnel-master skill,
          etkm-audience-map skill (adult mother persona)
Produces: Detailed content outline with section-by-section copy direction
Territory: /build/outline.md
Skills: skills/user/etkm-lead-gen, skills/user/etkm-funnel-master,
        skills/user/etkm-audience-map, skills/user/etkm-brand-foundation

Agent 2 — Copywriter
Job: Write all PDF copy from the approved outline
Receives: Agent 1's outline + etkm-brand-foundation + etkm-messaging-playbook
Produces: Complete copy draft for all PDF sections
Territory: /build/copy-draft.md
Skills: skills/user/etkm-brand-foundation, skills/user/etkm-messaging-playbook,
        skills/user/etkm-brand-kit (prohibited word list)

Agent 3 — PDF Builder
Job: Assemble final PDF using approved copy + brand kit
Receives: Agent 2's locked copy + etkm-brand-kit + public/pdf skill
Produces: Production-ready PDF file
Territory: /build/output.pdf, /build/pdf-build.py
Skills: skills/user/etkm-brand-kit, skills/public/pdf/SKILL.md

QC Agent — Brand & Quality Gate
Job: Run etkm-deliverable-qc against the PDF — all 9 gates
Receives: Agent 3's completed PDF
Produces: PASS with gate-by-gate confirmation, or FAIL with specific findings
Authority: FAIL on any gate sends PDF back to the responsible agent for correction
Skills: skills/user/etkm-deliverable-qc, skills/user/etkm-brand-kit
```

---

### Agent Team Key Rules

**Territory:** Each agent owns its files. No agent edits another agent's output directly — it sends findings or corrections back through the task list.

**Direct messaging:** Agents can communicate with each other without routing through the main session. Let them.

**Parallel work:** Agents that don't depend on each other run at the same time. Don't force sequential work when parallel is possible.

**Plan approval mode:** For complex builds, use plan approval — each agent submits its plan before executing. The main session (or a designated Plan Reviewer agent) approves before any agent proceeds.

**Clean shutdown:** When a session ends, each agent confirms its work is saved and handed off before the session closes. Never force-kill. Always confirm clean.

**Permissions:** Agents inherit permissions from the main session. Set permissions at the project level in `.claude/settings.local.json`.

---

## PART 4 — WHAT CLAUDE CODE NEVER DOES

These rules are absolute. No exception. No improvisation.

- **Never begins a build without a completed Project Card**
- **Never writes ETKM copy without loading etkm-brand-foundation**
- **Never produces a visual without loading etkm-brand-kit**
- **Never ships a deliverable without running etkm-deliverable-qc**
- **Never modifies copy that Claude Chat has locked**
- **Never rebuilds a workflow with LIVE or APPROVED status**
- **Never improvises brand colors, fonts, voice, or format decisions**
- **Never hands off to Manus without a completed Manus Handoff Brief**
- **Never uses light/white backgrounds on HTML deliverables** (black bg, white text, red accent only)
- **Never uses a specific year count for Nathan's experience** (use "over four decades" or "a lifetime of experience in self-protection")

---

## PART 5 — TOOL STACK ROLE DIVISION

| Tool | Job | What It Never Does |
|------|-----|--------------------|
| **Claude Chat** | Writes all copy, plans all structure, builds all briefs | Does not deploy, does not run automation |
| **Claude Code** | Builds scripts, apps, PDFs, HTML | Does not rewrite locked copy, does not deploy to live platforms |
| **Manus** | Deploys to WordPress, Pipedrive, GitHub, Make.com | Does not write copy, does not modify locked files |
| **Make.com** | Runs webhook workflows and automations | Does not make copy decisions |
| **Cowork** | Monitors, routes files, watches triggers | Does not write or build |

**The governing filter for every project:**
> Nathan builds for two reasons only: more revenue and less time wasted.
> Work that produces the opposite has failed — no matter how technically impressive it is.

---

## QUICK REFERENCE — Session Start Checklist

```
□ Run: ls skills/user/
□ Load: skills/user/etkm-project-standard/SKILL.md
□ Load: domain skills for this task (see table in Part 1, Step 3)
□ Load: skills/user/etkm-workflow-registry/SKILL.md
□ Confirm: Project Card exists — if not, build it
□ Confirm: This workflow is not already LIVE/APPROVED/DEPRECATED
□ Load: skills/user/etkm-deliverable-qc/SKILL.md (always, before any output)
□ If agent team: define agent stack from Project Card Layer 3
□ Build.
```

---

*Maintained in: easttxkravmaga/Claude → CLAUDE.md*
*Authority: Nathan Lundstrom / East Texas Krav Maga*
