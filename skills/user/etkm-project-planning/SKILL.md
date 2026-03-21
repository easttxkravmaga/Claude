---
name: etkm-project-planning
description: >
  Project planning protocol for East Texas Krav Maga. Load this skill before
  any new project, feature build, or multi-session initiative. Enforces the
  REBB protocol: start at the finish line, work backwards to today, map every
  dependency, identify every gap, verify every tool assignment, then write
  the build sequence. The governing principle: never ask "what should we
  build?" — ask "what does working look like, and what has to be true for
  that to exist?" Trigger before any planning session, any new project
  kickoff, or any time a build session is about to start without a plan.
---

# ETKM Project Planning Protocol

**Version:** 1.0
**Last Updated:** 2026-03-21

The most expensive problems are discovered after building starts.
This skill finds them before.

---

## THE GOVERNING PRINCIPLE

Start at the finish line. Work backwards to today.

Never ask "what should we build?" Ask "what does working look like —
and what has to be true for that to exist?"

---

## THE 5-STEP PROTOCOL

### Step 1 — Define the End State

Write what success looks like in precise, specific terms before
anything else. No building until this is written and confirmed.

### Step 2 — Map Every Dependency

Work backwards from the end state. For each dependency ask: what
has to be true for this to exist? Keep going until you hit ground
level.

### Step 3 — Identify All Gaps

List every gap with owner, path, and estimated time. If any gap
has no clear owner — stop and resolve before building.

### Step 4 — Verify Tool Assignments

For every task, verify the assigned tool can actually do the job.
Check etkm-deployment-doctrine capability matrix. Never assume.

### Step 5 — Write the Build Sequence

Phased, dependency-ordered, with Nathan's hands clean throughout.

---

## THE IRON RULE

If any phase requires Nathan to interact with infrastructure
(terminal, deployment commands, gcloud, Docker) — redesign the
phase. Nathan's hands stay clean. Always.

---

## SESSION SCOPE RULES

One session = one clear deliverable. When scope expands, open a
new session.

| Session Type | Contains | Does NOT contain |
|-------------|----------|-----------------|
| Planning | REBB protocol, dependency mapping | Any actual building |
| Content | Writing, copy, PDF drafts | Code, deployment |
| Build | Code writing, skill development | Deployment, content |
| Deployment | Production deployment only | New features, content |
| Review | QC, testing, validation | New building |

---

## THE PLANNING DOCUMENT

Every project gets a Notion planning document before building starts:

1. **End State** — precisely written
2. **Dependency Map** — full tree to ground level
3. **Gap List** — every gap with owner and path
4. **Tool Assignment Verification** — confirmed capability
5. **Build Sequence** — phased, dependency-ordered
6. **Deployment Plan** — specific path, proven tool, Nathan's hands clean
