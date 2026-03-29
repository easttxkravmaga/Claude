---
name: etkm-ai-roles
description: >
  Use this skill whenever any question involves which AI handles a task, how AIs
  coordinate with each other, what the role boundaries are, or how to route a task
  to the correct tool. Trigger for: "who should do this", "is this Claude or Manus",
  "what does Cowork handle", "AI role division", "task routing", "which tool",
  "how do the AIs work together", "briefing another AI", "handoff", or any time
  there is ambiguity about which AI owns a piece of work. This is the master
  reference for the ETKM five-AI coordination stack. Load at the start of any
  session that involves multiple AI tools.
---

# ETKM AI Roles & Coordination System

**Version:** 1.0
**Last Updated:** 2026-03-11

The ETKM AI stack runs five tools in defined lanes. No tool self-assigns work
outside its role. Claude is the manager. All other AIs are execution layers.

---

## THE FIVE-AI STACK

| AI | Layer | Primary Function |
|----|-------|-----------------|
| Claude (Chat) | Management | Strategy, all copy, task routing, system management |
| Cowork | Monitoring | Background watch, receipt detection, file routing, Nathan alerts |
| Claude Code | Backend | Scripts, APIs, server builds, technical infrastructure |
| Manus | Automation | Browser tasks, Pipedrive builds, Make.com scenarios |
| ChatGPT / Gemini | Research | Deep research, supplemental generation, fact-checking |

---

## CLAUDE — SYSTEM MANAGER

**Owns:** All strategic decisions. All written copy. All handoff briefs.
All task routing. Registry and SESSION_STATE maintenance.

**What Claude produces for other AIs:**
- For Manus: complete deployment briefs with copy, delays, success criteria
- For Claude Code: technical specifications with exact endpoints and requirements
- For Cowork: monitoring rule specs (watch folder, receipt file, stall threshold)
- For ChatGPT/Gemini: research briefs when deep external research is needed

**What Claude never does:**
- Implements automation in Pipedrive or Make.com
- Executes browser workflows
- Writes to production systems directly (except Pipedrive API for admin tasks)

**Session opening:** Claude reads MCP server (skill library + workflow status +
SESSION_STATE) at the start of every session. No briefing from Nathan required.

---

## COWORK — BACKGROUND MONITOR

**Owns:** Google Drive /ETKM-AI/Status/ folder watching. Stall detection.
File routing to project folders. Nathan alert generation. Sequence continuation prep.

**What Cowork watches:**
- Completion receipts from Manus and Claude Code in /Status/ folder
- In-Progress files that stop updating (stall detection)
- Project output files that need routing to correct folders
- P4 Pipedrive alerts surfaced by Manus receipts

**What Cowork never does:**
- Makes copy or strategy decisions
- Writes to Pipedrive
- Executes next workflow step without Nathan approval
- Overrides any other AI

**Receipt convention:** Every AI drops [PROJECT-WF-###]-COMPLETE.md to
/ETKM-AI/Status/ when done. Cowork reads it, confirms it, updates Nathan.

---

## CLAUDE CODE — BACKEND & SCRIPTS

**Owns:** Railway MCP server (app.py). All Python/JS scripts.
API integrations. Data processing. Testing and verification.

**Current infrastructure maintained:**
- Railway Flask server: classify_arc, get_skill, get_workflow_status endpoints
- Pipedrive API audit scripts
- GitHub file and registry management
- Future: Pipedrive MCP tools (move_to_stage, apply_arc_label, create_prospect)

**What Claude Code never does:**
- Makes copy or strategy decisions
- Self-assigns tasks — receives fully specified briefs from Claude
- Deploys to production without Nathan's confirmation

**Brief format from Claude to Claude Code:**
```
Task: [PROJECT-WF-###] [task name]
Endpoint/script: [what needs to be built or modified]
Inputs: [parameters and data types]
Outputs: [expected return format]
Test criteria: [how to confirm it works]
Location: [file path in repo]
Receipt: Write [ID]-COMPLETE.md to Google Drive /ETKM-AI/Status/
```

---

## MANUS — BROWSER AUTOMATION

**Owns:** All browser-based workflows. Pipedrive email sequence loads.
Make.com scenario builds. URL verification. Multi-step platform setup.

**What Manus never does:**
- Rewrites copy — copy is locked when it arrives from Claude
- Makes strategic decisions about what to build
- Marks a task LIVE without writing a completion receipt

**Brief format from Claude to Manus:**
```
Task: [PROJECT-WF-###] [task name]
Status: APPROVED — ready for load
Copy: [attached or linked — complete, do not modify]
Steps: [numbered, exact sequence]
Dependencies to verify: [list of URLs, fields, or conditions]
Success criteria: [what done looks like exactly]
Receipt: Write [ID]-COMPLETE.md to Google Drive /ETKM-AI/Status/
```

**Claude API calls from Manus:**
Manus calls the Railway /classify-arc endpoint for arc classification.
Manus calls the Anthropic API directly for personalized email copy generation.
See etkm-pipedrive-manus for full API specifications.

---

## CHATGPT / GEMINI — RESEARCH & SUPPLEMENTAL

**Owns:** Deep web research tasks. Supplemental content generation.
Cross-reference and fact-checking. NotebookLM document analysis.

**Receives from Claude:** Research briefs with specific questions, scope,
and output format needed.

**Returns to Claude:** Research findings in structured format for Claude to
synthesize into ETKM-branded content.

**What ChatGPT/Gemini never does:**
- Produces final ETKM copy — Claude rewrites everything in ETKM voice
- Accesses Pipedrive or Make.com
- Makes decisions about ETKM's system architecture

**Session context:** ChatGPT and Gemini have no persistent memory of ETKM.
Paste the ETKM Session Brief (docs/ETKM-Session-Brief.md in GitHub) at the
start of any research session to orient them correctly.

---

## TASK ROUTING DECISION TREE

When a task arrives, Claude routes it using this logic:

```
Is it written copy, strategy, or a brief for another AI?
  → Claude handles it.

Does it require a browser, UI clicks, or platform setup?
  → Manus handles it. Claude writes the brief first.

Does it require a script, API build, or server change?
  → Claude Code handles it. Claude writes the spec first.

Does it require monitoring, receipt detection, or file routing?
  → Cowork handles it. Claude writes the monitoring rule spec.

Does it require deep external research or fact-checking?
  → ChatGPT or Gemini handles it. Claude writes the research brief.
```

When a task crosses multiple lanes (example: new email sequence):
1. Claude writes all copy
2. Claude writes the Manus deployment brief
3. Manus loads the sequence into Pipedrive
4. Manus writes receipt to /Status/
5. Cowork confirms receipt and notifies Nathan
6. Claude updates registry to LIVE

---

## AI COORDINATION FLOW

```
Nathan → Claude (strategy + copy + routing)
              ↓
        Claude writes briefs
              ↓
    ┌─────────┬─────────┬──────────┐
    ↓         ↓         ↓          ↓
  Manus   Claude     ChatGPT    Cowork
  (build)  Code      /Gemini   (monitor)
           (build)   (research)
    ↓         ↓         ↓
 Receipt   Receipt   Returns
 → /Status/ → /Status/ → to Claude
              ↓
           Cowork detects receipts
              ↓
           Nathan notified
```

---

## SESSION OPENING FOR ANY AI

**Claude:** Reads MCP server automatically. No briefing needed.

**Manus:** Receives task brief from Claude. Reads GitHub for skill files if needed.

**Claude Code:** Receives specification from Claude. Reads repo for current state.

**Cowork:** Monitors continuously. No per-session setup needed once configured.

**ChatGPT/Gemini:** Paste docs/ETKM-Session-Brief.md at session start.
This gives them: ETKM context, project codes, role division, where things live.

---

## WHAT NO AI EVER DOES

- Rebuilds a workflow that already exists in APPROVED or LIVE status
- Changes copy without Claude's authorization
- Changes automation logic without Manus's build
- Moves a workflow to LIVE without a completion receipt
- Makes a structural change to Pipedrive without Nathan's explicit instruction
