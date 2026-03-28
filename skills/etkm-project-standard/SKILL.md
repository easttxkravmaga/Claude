---
name: etkm-project-standard
version: 1.0
updated: 2026-03-23
description: >
  The master production standard for every ETKM project — regardless of type,
  tool, or deliverable. Load this skill at the start of any new project build,
  before any asset is created, any code is written, or any brief is sent to another
  tool. This is the packaging layer. It does not replace etkm-brand-kit,
  etkm-deliverable-qc, or etkm-format-standards — it governs when and how those
  skills are applied. No project enters production without a completed Project Card.
  No deliverable leaves production without passing QC. No handoff happens without
  a completed Brief. These three rules are absolute.
trigger: >
  Load this skill whenever: a new project is being started, a project is being
  scoped or planned, a handoff to Manus or Claude Code is being prepared, a project
  is being audited for quality, or Nathan asks "what do we need before we build this?"
  Trigger phrases: "new project", "start building", "scope this", "what do we need",
  "before we build", "hand this off", "project card", "production standard",
  "what does this project need", "build the package first", "set the standard".
  Also load at the start of any session involving a project that does not yet have
  a completed Project Card.
dependencies:
  - etkm-brand-kit (visual standards — loads at Brand & Voice layer)
  - etkm-brand-foundation (voice standards — loads at Brand & Voice layer)
  - etkm-format-standards (output format rules — loads at Output Spec layer)
  - etkm-deliverable-qc (QC gates — loads at QC layer, mandatory before delivery)
  - etkm-ai-roles (tool routing — loads when preparing any handoff brief)
---

# ETKM Project Production Standard
## The container every project is built inside. One standard. No exceptions.

**Version:** 1.0
**Established:** 2026-03-23
**Authority:** Nathan Lundstrom / East Texas Krav Maga
**Benchmark:** P1 Book Intelligence System

---

## Why This Skill Exists

Every tool in the ETKM stack — Claude Chat, Claude Code, Manus, Cowork — produces
better output when it receives better input. The root cause of inconsistent quality
is not a capability problem. It is a packaging problem.

When a project enters production without a locked spec, tools improvise. When a
handoff brief is missing, the receiving tool fills the gaps with defaults. When QC
criteria are not written before the build, "done" becomes subjective.

This skill is the permanent fix.

It establishes one standard container that every project — regardless of type or
tool — gets built inside. The container defines what goes in, what comes out, who
does each job, and what "done" looks like before anyone starts building.

**The P1 Book Intelligence System is the benchmark.** It works at a consistently
high level because it has all six layers locked before any session runs. Every
project we build from this point forward gets the same treatment.

---

## The Non-Negotiable Rule Set

**Rule 1:** No project enters production without a completed Project Card.
**Rule 2:** No deliverable leaves production without passing all QC gates.
**Rule 3:** No handoff happens without a completed Handoff Brief.
**Rule 4:** No tool improvises brand, voice, or format decisions.
**Rule 5:** The benchmark for every project is the best version of that project type — not the average.

---

## The Six-Layer Framework

Every project is built by completing six layers in sequence.
Do not begin Layer 2 until Layer 1 is complete.
Do not begin production until all six layers are complete.

---

### LAYER 1 — PROJECT IDENTITY

Define the project completely before touching any tool.

**Six questions. Every question answered before moving to Layer 2.**

**Q1: What does this project receive?**
The exact format of the input. What comes in — document, data, brief, content draft?
What format? What minimum quality standard must the input meet before the project runs?
If the input is wrong, the output will be wrong. Define acceptable input here.

**Q2: What does this project produce?**
Every deliverable named. Not "a PDF" — which PDF, what length, what sections, what
format. Not "an email sequence" — how many emails, what arc, what platform, what format.
Be specific enough that the output could be QC'd against this description without
asking the builder any questions.

**Q3: What is this project looking for?**
The extraction or processing framework. What does the agent mine from the input to
produce the output? What are the key signals, structures, or data points that drive
the deliverables? This is the intelligence layer — what makes the output smart vs. generic.

**Q4: What brand and voice rules govern this project?**
Which skills load. What tone. What audience. What prohibited language. What required
phrasing. This layer locks before any copy is written so no tool makes brand decisions
independently.

**Q5: What are the rejection criteria?**
Write the failure conditions before the build starts. What does a failed deliverable
look like for this project specifically? Add project-specific QC items to the universal
gates in etkm-deliverable-qc. If you cannot describe failure, you cannot QC for it.

**Q6: What is the north star?**
The single governing standard every deliverable is measured against. One sentence.
Not a goal — a standard. P1's north star: "Learning only happens if there is changed
behavior." Every asset in P1 is measured against that one sentence.
Every project needs its own.

---

### LAYER 2 — PROJECT CARD

The completed Project Card is the single-page identity document for the project.
It is written once, stored in the project skill, and loaded at the start of every
session that touches this project.

```
PROJECT CARD
─────────────────────────────────────────────────────────
Name:           [Project name]
Code:           [P# or WF-###]
Type:           [PDF / Email / HTML / App / Campaign / System]
Owner:          Nathan Lundstrom
Status:         [Scoping / In Production / Complete / Live]
North Star:     [One sentence — the governing standard]
Purpose:        [One sentence — what this project does]
─────────────────────────────────────────────────────────
INPUT
Format:         [Exact description of what comes in]
Minimum Std:    [What the input must contain to be acceptable]
Provided by:    [Nathan / Claude / Manus / External]
─────────────────────────────────────────────────────────
OUTPUT
Deliverables:   [Every asset named, one per line]
                [Asset 01: Name — format, approx length, destination]
                [Asset 02: Name — format, approx length, destination]
Format Rules:   [Load etkm-format-standards — specify which formats apply]
Destination:    [Where the output goes — Nathan / Pipedrive / WordPress / GitHub]
─────────────────────────────────────────────────────────
SKILLS LOADED
Strategy:       [etkm-brand-foundation, etkm-audience-map, etc.]
Voice:          [etkm-brand-kit, etkm-messaging-playbook, etc.]
Format:         [etkm-format-standards + specific format skill]
QC:             [etkm-deliverable-qc — always]
Domain:         [Project-specific skills: etkm-book-intelligence, etc.]
─────────────────────────────────────────────────────────
AGENT STACK
[See Layer 3 — Agent Stack]
─────────────────────────────────────────────────────────
QC GATES
Universal:      etkm-deliverable-qc — all 9 gates
Project-Spec:   [Additional rejection criteria specific to this project]
Benchmark:      [The best existing version of this deliverable type]
─────────────────────────────────────────────────────────
NORTH STAR
[The single governing standard. One sentence.]
─────────────────────────────────────────────────────────
```

---

### LAYER 3 — AGENT STACK

Define which agent handles which job and what they receive and return.

The agent stack is the internal team for this project. For Chat-only projects
it describes the roles Claude plays sequentially. For multi-tool projects it
defines which tool owns which phase and what travels between them.

Every project has at minimum four agents:

| Agent | Role | Receives | Returns |
|-------|------|----------|---------|
| **Strategist** | Defines structure, approach, audience alignment | Project Card | Outline + strategic direction |
| **Writer/Builder** | Produces the content or build | Outline + brand rules | Draft deliverables |
| **Brand Editor** | Applies voice, visual, format standards | Draft deliverables | Branded deliverables |
| **QC Agent** | Holds against all gates — rejects or passes | Branded deliverables | PASS or FAIL with findings |

Complex projects add specialized agents:

| Agent | Role | When to Add |
|-------|------|-------------|
| **Architect** | Structures multi-asset projects | 3+ deliverables |
| **Extractor** | Mines raw input for key data | Book, research, or document processing |
| **Code Agent** | Builds scripts, apps, APIs | Any Claude Code deliverable |
| **Deployment Agent** | Loads to Pipedrive, WordPress, GitHub | Any Manus deliverable |

**Agent Stack Rules:**
- Each agent has one job. It does not expand into another agent's territory.
- No agent improvises brand or format decisions. Those are locked in Layer 1.
- The QC Agent has authority to reject any deliverable and send it back.
  Rejection is not a failure — it is the system working correctly.
- Nothing moves to the next agent until the current agent's output is complete
  and meets the acceptance criteria defined in Layer 1.

---

### LAYER 4 — GATE SYSTEM

Gates are checkpoints between phases. Nothing moves through a gate without a pass.

**Universal Gate Structure:**

```
GATE A — Input Validation
  Before any work begins.
  Confirm input meets the minimum standard defined in the Project Card.
  If input is insufficient → return to Nathan with specific list of what's missing.
  Pass criteria: Input matches the format and minimum standard defined in Layer 1 Q1.

GATE B — Structure Review
  After Architect/Strategist completes outline.
  Confirm structure matches output spec and north star.
  Before Writer/Builder begins.
  Pass criteria: Every deliverable in the output spec is accounted for in the structure.

GATE C — Draft Review
  After Writer/Builder completes draft deliverables.
  Confirm content is complete, on-voice, and on-spec.
  Before Brand Editor begins.
  Pass criteria: All content present, no placeholder tokens, voice review passes.

GATE D — Brand Review
  After Brand Editor completes branded deliverables.
  Confirm visual standards, format standards, typography, color.
  Before QC Agent runs full gate check.
  Pass criteria: Matches etkm-format-standards for the deliverable type.

GATE E — QC Full Run
  After Brand Editor — mandatory before any delivery.
  Run all 9 gates from etkm-deliverable-qc plus project-specific gates.
  Any failure = return to the responsible agent, fix, re-run QC.
  Pass criteria: All gates PASS with no exceptions.

GATE F — Delivery
  After QC full run passes.
  Confirm destination, format, file naming.
  Present to Nathan or trigger handoff brief.
  Pass criteria: Files named correctly, delivered to correct destination, receipt logged.
```

**Gate Failure Protocol:**
- Log the failure: which gate, which deliverable, what specifically failed.
- Return to the correct agent — not the beginning.
- Fix only what failed — do not rebuild what passed.
- Re-run only the gates affected by the fix.
- Do not skip re-check after a fix. The fix must pass before moving forward.

---

### LAYER 5 — HANDOFF BRIEFS

Any project that crosses a tool boundary requires a Handoff Brief before the
receiving tool begins work. No tool starts blind.

Load `etkm-ai-roles` before writing any Handoff Brief.

---

#### HANDOFF BRIEF — CLAUDE CODE

Use when: the project requires a script, API, app, or server-side build.

```
CLAUDE CODE BRIEF
─────────────────────────────────────────────────────────
Task:           [PROJECT-WF-###] [task name]
Status:         APPROVED — ready to build

WHAT TO BUILD
[Plain-language description of what the script/app/API does]

INPUT
Format:         [Exact data format coming in]
Source:         [Where it comes from]
Sample:         [Attach sample or describe precisely]

OUTPUT
Deliverable:    [Exact file, endpoint, or return value]
Format:         [File type, data structure, naming convention]
Destination:    [Where it goes when done]

TECHNICAL SPEC
Language:       [Python / Node.js / other]
Libraries:      [Specific libraries required]
Endpoints:      [If API — exact endpoint names and parameters]
File path:      [Where in the repo]

ACCEPTANCE CRITERIA
[Numbered list — specific, testable conditions that confirm it works]
1.
2.
3.

QC REQUIREMENT
Run etkm-deliverable-qc on any document output.
For apps: run against acceptance criteria list above.

RECEIPT
Write [PROJECT-WF-###]-COMPLETE.md to Google Drive /ETKM-AI/Status/
Include: what was built, file location, any deviations from spec.
─────────────────────────────────────────────────────────
```

---

#### HANDOFF BRIEF — MANUS

Use when: the project requires browser automation, Pipedrive setup, WordPress
deployment, Make.com build, or any platform-level action.

```
MANUS BRIEF
─────────────────────────────────────────────────────────
Task:           [PROJECT-WF-###] [task name]
Status:         APPROVED — ready to deploy
Copy locked:    YES — do not modify any copy

ASSETS ATTACHED
[List every file being handed to Manus with its name and location]
- [filename] → [Google Drive path or GitHub path]

STEPS
[Numbered, exact sequence. No ambiguity. One action per step.]
1.
2.
3.

DEPENDENCIES TO VERIFY BEFORE STARTING
[List every URL, field, credential, or condition that must exist first]
-
-

SUCCESS CRITERIA
[What done looks like — exactly. Manus confirms each item.]
-
-

IF SOMETHING DOES NOT MATCH THE SPEC
Stop. Do not improvise. Return to Claude with specific question.

RECEIPT
Write [PROJECT-WF-###]-COMPLETE.md to Google Drive /ETKM-AI/Status/
Include: what was deployed, live URL if applicable, any issues encountered.
─────────────────────────────────────────────────────────
```

---

#### HANDOFF BRIEF — COWORK

Use when: the project requires background monitoring, file routing, or
ongoing watch tasks.

```
COWORK BRIEF
─────────────────────────────────────────────────────────
Task:           [PROJECT-WF-###] [monitoring task]

WATCH
Folder/file:    [Exact Google Drive path]
Watch for:      [What Cowork is looking for — receipt file, update, stall]
Interval:       [How often to check]

TRIGGER CONDITION
[Exactly what Cowork sees that triggers an action]

ACTION ON TRIGGER
[Exactly what Cowork does — alert Nathan, route file, update status]

ALERT FORMAT
Notify Nathan: [What the alert says]

RECEIPT
Update [PROJECT-WF-###] status in registry when trigger fires.
─────────────────────────────────────────────────────────
```

---

### LAYER 6 — BENCHMARK STANDARD

Before the first asset is built, name the benchmark.

The benchmark is the best existing version of this deliverable type in the ETKM
system. If no existing benchmark exists, the benchmark is the P1 Book Intelligence
output standard applied to this project type.

**Benchmark Questions:**
- What is the best example of this deliverable type we have produced?
- What makes it work at the level it works?
- What would we change if we were refining it to an even higher standard?
- Is there an external benchmark (outside ETKM) that represents the ultimate
  version of this deliverable type?

The benchmark is named in the Project Card and referenced by the QC Agent
during Gate E. "Does this match or exceed the benchmark?" is the final
standard before delivery.

---

## Project Type Library

As projects are completed through this framework, their Project Cards become
reusable templates for the next project of the same type. This section grows
over time.

### Currently Established Project Types

**P1 — Book Intelligence (BENCHMARK)**
- Input: Book report from NotebookLM/Claude
- Output: 5 assets (Field Manual PDF, Validation Brief PDF, Reading Companion PDF,
  Cheat Sheet HTML, Instructor DOCX)
- North Star: Learning only happens if there is changed behavior
- Agent Stack: Extractor → Architect → Writer → Brand Editor → QC Agent
- Skill: etkm-book-intelligence

**PDF Production (IN DEVELOPMENT)**
- Input: Content brief + audience + purpose
- Output: Polished brand-compliant PDF
- North Star: TBD — pending benchmark review with Nathan
- Agent Stack: TBD — pending Project Card completion
- Skill: etkm-pdf-sop (format standard exists, production skill TBD)

*Additional project types are added here as their Project Cards are completed.*

---

## Required Pre-Build Checks by Deliverable Type

| Deliverable | Required Skills to Load Before Starting |
|-------------|----------------------------------------|
| HTML page | `etkm-brand-kit` + `etkm-webpage-build` |
| Web form | `etkm-brand-kit` + `etkm-webpage-build` + `etkm-webform-build` |
| PDF | `etkm-brand-kit` + `etkm-pdf-pipeline` |
| Event page | `etkm-brand-kit` + `etkm-webpage-build` + `etkm-event-page` |
| Email | `etkm-brand-foundation` |
| Social graphic | `etkm-brand-kit` + `etkm-social-graphics` + `etkm-cinematic-doctrine` |
| CRM / automation | `etkm-crm-doctrine` + `etkm-pipedrive-manus` |

No deliverable leaves production without passing the relevant QC gates in
`etkm-deliverable-qc`.

---

## Session Opening Protocol for All Tools

**Claude Chat:**
Load this skill at the start of any session involving a new or in-progress project.
Confirm Project Card exists. If it doesn't — build it before doing anything else.

**Claude Code:**
Receive Handoff Brief. Confirm all acceptance criteria are understood before writing
a single line. If anything in the brief is ambiguous — ask before building.

**Manus:**
Receive Handoff Brief. Confirm all steps are clear and all assets are present
before executing. Never modify copy. Never improvise steps not in the brief.

**Cowork:**
Receive Monitoring Brief. Watch for triggers. Alert Nathan. Log receipts.

---

## What No Tool Ever Does

- Begins a project without a completed Project Card
- Improvises brand, voice, color, or format decisions
- Delivers a file without passing QC Gates
- Modifies copy after it has been locked by Claude
- Rebuilds a project that already has COMPLETE or LIVE status
- Skips a gate because the project "feels done"
- Proceeds through a handoff without a completed Handoff Brief

---

## Integration Map

This skill governs when and how all other production skills are loaded.

| Layer | Skills That Load |
|-------|-----------------|
| Project Identity | etkm-audience-map, etkm-brand-foundation, etkm-problem-solution |
| Brand & Voice | etkm-brand-kit, etkm-brand-foundation, etkm-messaging-playbook |
| Output Format | etkm-format-standards + format-specific skill (pdf, docx, html, email, pptx) |
| Agent Stack | etkm-ai-roles (for multi-tool projects) |
| QC | etkm-deliverable-qc (always — no exceptions) |
| Handoff | etkm-ai-roles, etkm-pipedrive-manus (for Manus handoffs) |
| Domain | Project-specific skill (etkm-book-intelligence, etkm-lead-gen, etc.) |

---

*Version 1.0 — Established 2026-03-23*
*Built from: P1 Book Intelligence System (benchmark)*
*Authority: Nathan Lundstrom / East Texas Krav Maga*
*Maintained in: easttxkravmaga/Claude → skills/etkm-project-standard/SKILL.md*
