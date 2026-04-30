---
name: zapier
version: 1.0
date: 2026-04-29
description: Operational skill for all Zapier work in the ETKM stack. Pure Zapier — no routing references to other automation platforms. Covers platform architecture, task economics, ETKM-specific integrations, build protocol, problem-solving, constraints, and collaboration standard.
triggers:
  - "build a Zap"
  - "Zapier workflow"
  - "Zapier MCP"
  - "Zap trigger"
  - "connect apps in Zapier"
  - "Zapier action"
  - "task count"
  - "Zapier error"
  - "polling trigger"
  - "Zapier agent"
  - "automation in Zapier"
  - "Zapier integration"
---

# Zapier Operational Skill — ETKM
**Version:** 1.0 | **Date:** April 29, 2026
**Reference Doc:** Google Drive → AI Resources → Zapier Platform Intelligence — ETKM Reference
**Notion Record:** Platform Intelligence Hub → Zapier

---

## 1. Platform Identity

Zapier is ETKM's active AI orchestration and workflow automation platform. It connects 9,000+ applications through 40,000+ triggers and actions. It is connected to ETKM's Claude account as a live MCP server at mcp.zapier.com.

Zapier serves two distinct roles in the ETKM stack:
- **Automation layer** — trigger-based workflows that run automatically when events occur in connected apps
- **MCP server** — gives Claude and other AI clients the ability to call actions across ETKM's tech stack on demand

Both roles draw from the same billing pool under Zapier's task-based pricing model.

---

## 2. Core Architecture

### Fundamental Primitives

| Primitive | Definition |
|-----------|------------|
| **Trigger** | Event in an app that starts a Zap. Either polling (Zapier asks the API on a schedule) or instant (app pushes a webhook). Type is fixed by the app's API — cannot be changed by the user. |
| **Action** | Step Zapier performs in another app. Each successful action = 1 billable task. |
| **Search** | Read-only lookup step. Returns data without creating or updating records. |
| **Zap** | One trigger + one or more steps. The core workflow unit. |
| **Filter** | Halts Zap if conditions not met. FREE — does not consume tasks. |
| **Paths** | Conditional if/then branching. FREE — does not consume tasks. |
| **Formatter** | Built-in data transformation (text, numbers, dates, utilities). FREE — does not consume tasks. |
| **Delay** | Pause workflow for time or until a datetime. FREE — does not consume tasks. |
| **Webhooks** | HTTP listener and request tool — Catch Hook, GET, POST, Custom Request. |
| **Code** | Sandboxed JavaScript or Python execution. 1 task per run. |
| **Looping** | Repeat actions for each item in a list. Each iteration's actions count as tasks. |
| **Sub-Zap** | Reusable Zap components invoked from a parent Zap. |
| **Storage** | Key-value store persisting data between Zap runs. |
| **Digest** | Batch events across runs into a single summary output. |
| **Tables** | Native no-code database. Included on all plans. |
| **Interfaces** | Form and lightweight app builder. Included on all plans. |
| **Agents** | Autonomous AI teammates that call Zapier app tools. |
| **Copilot** | AI assistant that builds Zaps and systems from natural language. |
| **MCP Server** | Exposes Zapier's 40,000+ actions as tools to any compliant AI client. |

### Polling Intervals by Plan

| Plan | Interval |
|------|----------|
| Free | 15 minutes |
| Professional | 2 minutes |
| Team | 1 minute |
| Enterprise | 1 minute (custom configurable) |

---

## 3. Task Economics

**A task = any successful action Zapier completes on your behalf.**

### What Counts as a Task
- Each successful action step (create record, send message, update field, call webhook, generate AI response)
- Each MCP tool call = **2 tasks** (the only step type with a multiplier)
- Each record sent via Transfer = 1 task
- Each loop iteration's actions each count individually

### What Does NOT Count as a Task
- Triggers
- Filter steps
- Formatter steps
- Paths steps
- Delay steps
- Failed actions
- Sub-Zap call overhead

### Task Cost Estimation Formula
```
(expected daily runs) × (billable steps per run) × 30 = monthly task estimate
```
Always run this before building. Never start a Zap design without a task estimate.

### Overage Model
- Tasks beyond the monthly cap run at **1.25× the per-task rate**
- Hard ceiling: **3× the plan's task limit** before Zaps pause
- 80% usage warning emails fire before the limit is hit

### Cost-Aware Design Rules
- Use Filter, Formatter, and Paths aggressively — they are free
- MCP tool calls cost 2 tasks — batch operations wherever possible
- Prefer Digest over one-action-per-event patterns for notifications
- Use Formatter's lookup table or Sub-Zaps to consolidate repeated logic

---

## 4. ETKM Stack Integration

### Active Connected Apps (as of April 2026)

| App | Key Triggers / Actions | Notes |
|-----|------------------------|-------|
| Gmail | New Email, Send Email, Create Draft | Instant triggers available |
| Google Calendar | New Event, Create/Update Event | Polling |
| Google Drive | New File in Folder, Create/Upload File | Polling |
| Notion | New Database Item, Create/Update Page | Deep integration |
| Calendly | Invitee Created, Invitee Canceled | Instant webhook — key for trial booking |
| Anthropic Claude | Send Message, Send Message with Image | AI steps inside Zaps |
| OpenAI / ChatGPT | Conversation, image gen, transcription, embeddings | Full action suite |
| WordPress | New Post, Create/Update Post | Polling — blog/content workflows |
| Slack | Send Channel/DM Message | Instant triggers for mentions |

### MCP Server Status
- Active at mcp.zapier.com
- Connected to ETKM's Claude account
- All OAuth connections from ETKM's Zapier account are available as MCP tools
- When a connection expires: alert icon appears next to the tool → click "Update authentication" → re-run OAuth flow

---

## 5. Build Protocol

### Pre-Build: Required Before Any Zap Work

1. **State the full plan** — trigger, all steps in order, estimated task cost, estimated monthly volume
2. **Get explicit confirmation from Nathan** before building anything
3. **Never turn on a Zap** without explicit confirmation
4. **Estimate task cost** using the formula above
5. **Confirm all required app connections** are live and authenticated before starting

### During Build

- Surgical changes only — modify only what was specified, touch nothing adjacent
- Use Filter and Formatter before reaching for Code — free steps are always preferred
- Name Zaps descriptively: `[trigger app] → [action app] — [purpose]` (e.g., `Calendly → Notion — Trial Booking`)
- Test with sample data, not production records

### QC Before Handoff

- Verify step count matches the plan
- Confirm all field mappings are correct
- Run a test with known inputs and verify outputs
- Confirm no unintended side effects on connected apps
- Document final task-per-run count

---

## 6. Problem-Solving

### Common Failure Modes & Recovery

| Failure | Diagnosis & Fix |
|---------|-----------------|
| Zap stops triggering — no errors in history | Polling trigger state reset. Fix: **off → wait 60 seconds → on**. This resets the trigger connection. |
| Authentication failure on a step | OAuth token expired. Go to Zapier → Connected Accounts → find app → Reconnect. All Zaps using that connection resume automatically. |
| MCP tool connection alert icon | App connection expired. Go to mcp.zapier.com → find affected tool → "Update authentication" → re-run OAuth flow. |
| Unexpected task overages | Audit Zap history for unexpected loop iterations, runaway retry loops, or high-frequency triggers. Add Zapier Manager alert at 80% task threshold. |
| Action fails intermittently | Usually downstream API rate limit or temporary outage. Enable Autoreplay (Pro+) for automatic retry. Add Zapier Manager error-alert Zap for monitoring. |
| ChatGPT MCP tools not updating | ChatGPT does not auto-refresh tools. Must manually click Refresh in ChatGPT Connector Settings after any Zapier-side tool change. |
| Data not mapping correctly | Re-select the correct output field using the field picker. Use Formatter → Utilities → Default Value to handle null/empty fields. |
| Duplicate records being created | Trigger firing multiple times for the same event. Add a Filter step checking a unique field (ID, email) before the action step. |

### Diagnostic Order — Work This Sequence Before Escalating
1. Check Zap History for the specific run — what step failed and what was the error message?
2. Check the app connection is still authenticated
3. Check if the downstream app has rate limits or outages
4. If polling trigger: off → 60 seconds → on
5. Test the failing step in isolation with manual trigger
6. Only after exhausting the above: rebuild the step from scratch

---

## 7. Constraints & Guardrails

### Hard Limits — Non-Negotiable

- **No HIPAA** — zero Protected Health Information in any Zapier workflow, ever, without exception
- **No sandbox** — all testing uses the live Zapier account; always use test/dummy data, never production records, when testing
- **ChatGPT MCP is not automatic** — never assume ChatGPT has updated tools after a Zapier-side change; manual refresh is always required
- **Transfer scheduling is deprecated** — do not design workflows that depend on scheduled Transfers; use triggered Zaps instead
- **Polling triggers are not real-time** — never build time-critical workflows on polling triggers without explicitly accounting for the interval

### Design Guardrails

- Always estimate task cost before building
- Always use Filter/Formatter/Paths over Code when they can do the job
- Always state the full Zap plan before executing — no hands on keyboard until confirmed
- Never turn on a Zap without Nathan's explicit confirmation
- Never modify anything outside the specified scope
- Never build speculative features or unrequested steps

---

## 8. Collaboration Standard

This skill operates under the `nate-collaboration-workflow` standard. Zapier-specific additions:

### Communication Protocol
- **Describe plan first** — trigger, steps, task cost estimate, before any building
- **Wait for go** — do not start building until Nathan confirms
- **One task per session** — complete one Zap or workflow fully before starting another
- **Surface blockers immediately** — if a connection is missing, an app doesn't support the required action, or cost estimate is unexpectedly high, stop and surface it before proceeding

### Execution Standards
- State assumptions before coding or configuring
- Write minimum configuration that solves what was asked — no speculative additions
- Surgical changes only — touch nothing outside the request
- Multi-step builds: state plan with verify steps before executing

### What a Complete Zapier Deliverable Looks Like
- Zap is built, tested with sample data, and confirmed working
- Step count and task-per-run count documented
- All field mappings verified
- Zap is **OFF** until Nathan confirms it should be turned on
- Any new app connections or OAuth flows flagged for Nathan's awareness

---

## Reference

- **Full Research Brief:** Google Drive → AI Resources → Zapier Platform Intelligence — ETKM Reference
- **Notion Record:** Platform Intelligence Hub → Zapier (ID: 352924c8-1673-81be-8366-ef35d3f4dc77)
- **Zapier Docs:** https://docs.zapier.com
- **MCP Config:** https://mcp.zapier.com
- **Zapier Plans & Pricing:** https://zapier.com/pricing
