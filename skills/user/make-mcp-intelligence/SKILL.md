---
name: make-mcp-intelligence
version: 1.0
updated: 2026-04-29
description: >
  Load this skill for any task involving Make.com via MCP — triggering scenarios
  from Claude chat, managing Make scenarios or webhooks, configuring the Make MCP
  connector, or deciding whether a task belongs in Make. This is a routing skill:
  the living intelligence lives in the Make Deep Reference Page in Notion. Always
  fetch that page at session start before taking any Make action.
triggers:
  - "Make MCP"
  - "Make scenario"
  - "trigger a Make scenario"
  - "Make connector"
  - "Make toolbox"
  - "Make webhook"
  - "Make data store"
  - "run a Make scenario"
  - "use Make from Claude"
  - "Make account"
  - "Make integration"
  - "Make automation"
  - "configure Make"
  - "Make tool"
  - "what scenarios are in Make"
  - "Make is not working"
  - "Make MCP not connecting"
  - "Make session"
  - "Make Deep Reference"
  - "make.com"
  - "Make scenario registry"
  - "Make credentials"
  - "Make connection"
  - "Make execution"
  - "Make blueprint"
---

# Make MCP Intelligence

## Purpose

Make.com is the ETKM on-demand tool layer. Its role is to expose pre-built
scenarios as MCP tools that Claude can trigger directly from chat, Claude Code,
or the Anthropic API. This skill tells Claude how to connect to Make, when to
use it, and how to operate it correctly. The authoritative living reference —
account config, scenario registry, known errors, open issues, and session
protocol — lives in the Make Deep Reference Page in Notion. This skill is the
entry point. Notion is the intelligence.

---

## When to Load

Load this skill whenever:
- A Make scenario is being triggered, reviewed, built, or retired
- The Make MCP connector is being configured or debugged on any Claude surface
- A task involves Make webhooks, data stores, connections, or scenario management
- A decision about whether a task belongs in Make needs to be made
- The Make Deep Reference Page needs to be fetched or updated
- Any phrase containing "Make", "make.com", "Make scenario", "Make MCP",
  "Make toolbox", "Make webhook", or "Make data store" appears in the task

---

## Core Instructions

### Step 1 — Fetch the Make Deep Reference Page First

Before taking any Make action, fetch the Notion intelligence page:

**Notion Page ID:** `351924c8-1673-81ae-aa6b-f6224cfccf76`

Fetch it via the Notion MCP tool. Read these sections before proceeding:
1. **Open Issues** — surface any blockers relevant to the current task
2. **Active Scenario Registry** — confirm the target scenario exists, is active,
   and is MCP-ready (all four requirements met)
3. **Last Verified date** — flag to Nate if >30 days old
4. **Known Error Log** — check before diagnosing any failure independently

Do not attempt to trigger, build, or modify any Make scenario without first
completing this fetch-and-read sequence.

### Step 2 — Confirm the Target Scenario is MCP-Ready

A scenario must meet all four requirements before Claude can invoke it as an
MCP tool:

1. **Scheduling = On Demand (immediately)** — scheduled scenarios are invisible
   to Make MCP
2. **isActive = true** — inactive scenarios cannot be called
3. **Description written** — Claude uses the description to select the right tool
4. **Inputs and Outputs defined** — without these, Claude cannot pass arguments
   or parse results

If any of the four requirements are unmet, stop and flag to Nate. Do not
attempt to invoke an unready scenario.

### Step 3 — Connect to Make MCP

Use the first applicable connection method for the current Claude surface:

| Surface | Method | Config |
|---|---|---|
| claude.ai chat | Built-in connector (OAuth) | Settings → Connectors → Make |
| Claude Desktop | Built-in connector or custom toolbox URL | Settings → Connectors → Make, or paste toolbox URL |
| Claude Code | MCP token via CLI | `claude mcp add --transport http make https://us2.make.com/mcp/u/<TOKEN>/stateless` |
| Anthropic API | `mcp_servers` parameter | See Pattern: API Integration below |

**Transport:** Always use `/stateless` (Streamable HTTP). Fall back to `/stream`
then `/sse` only if the client does not support Streamable HTTP.

**Account identifiers (do not guess — use these exact values):**
- Zone: `us2.make.com`
- Organization ID: `1945651`
- Team ID: `51888`
- Plan: Pro (management tools available)

### Step 4 — Execute the Task

With the intelligence page read and the scenario confirmed MCP-ready, proceed.

**To trigger a scenario from chat:**
Describe the intent naturally. Claude selects the correct MCP tool and invokes
it. If Claude selects the wrong tool, the scenario descriptions are insufficiently
distinct — update them before retrying.

**To manage scenarios, webhooks, or data stores:**
Management tools are available on the Pro plan. Scope selection during OAuth
must include "View and modify scenarios" and/or "View and modify connections,
webhooks, data stores" as needed.

**To handle a timeout (scenario runtime >25s OAuth / >40s token):**
Make returns `{ executionId, scenarioId }`. The scenario continues running in
Make for up to 40 minutes. Retrieve the result by calling the execution-result
tool with the returned `executionId`. Never retry the scenario trigger — the
original execution is still running.

---

## Patterns

### Pattern: Anthropic API Integration

```python
import anthropic
client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    messages=[{"role": "user", "content": "YOUR PROMPT HERE"}],
    mcp_servers=[{
        "type": "url",
        "url": "https://us2.make.com/mcp/stateless",
        "name": "make",
        "authorization_token": "YOUR_MAKE_MCP_TOKEN",
    }],
    betas=["mcp-client-2025-11-20"],
)
```

Note: Anthropic's MCP connector calls Make from Anthropic's cloud infrastructure.
Not covered by Zero Data Retention. Not supported on Bedrock or Vertex.

### Pattern: MCP Toolbox for Scoped Access

When Claude should only see a curated subset of scenarios:
1. Make UI → MCP Toolboxes → Create Toolbox
2. Add specific scenarios, set name and description per scenario
3. Copy toolbox URL: `https://us2.make.com/mcp/server/<TOOLBOX_ID>/t/<KEY>/stateless`
4. Add as custom connector in Claude Desktop or pass as `mcp_servers` URL in API

### Pattern: Async Long-Running Scenario

For scenarios that take >25 seconds:
1. Design the scenario to enqueue work and return a job ID immediately
2. Build a separate status-check scenario that accepts the job ID
3. Call kick-off → receive job ID → wait → call status-check → retrieve result
Never build a single blocking scenario >25 seconds if it will be MCP-callable.

### Pattern: Scenario Description Standard

Write every scenario description as a single action sentence:
"Receives [inputs], does [action], returns [outputs]."

Example: "Receives a student name, email, and phone number, creates a Person
and Deal in Pipedrive, and returns the new deal ID."

Claude uses this description verbatim to select the correct tool. Treat scenario
names and descriptions as an external API contract — renaming silently breaks
MCP tool selection.

---

## What Not to Do

- Never trigger a Make scenario without first fetching the Notion reference page
- Never invoke a scenario that does not meet all four MCP-Ready requirements
- Never use `/sse` transport when `/stateless` is available
- Never use `us1.make.com` — the account zone is `us2.make.com`
- Never retry a timed-out scenario trigger — retrieve by `executionId` instead
- Never build a single scenario >25 seconds runtime for MCP use
- Never expose the full Make account when only specific scenarios are needed —
  use a toolbox
- Never hardcode scenario names in prompts or instructions — they drift
- Never attempt to author a complex scenario through the MCP management tool
  surface — use the Make UI for visual scenario construction
- Never push a scenario into production without a description and defined
  inputs/outputs

---

## Recovery

**Scenario not visible as MCP tool:**
Check all four MCP-Ready requirements. The most common failure is scheduling
not set to On Demand (immediately) or scenario is inactive.

**Claude invokes wrong scenario:**
Scenario descriptions are ambiguous or missing. Update descriptions per the
Scenario Description Standard pattern above.

**Tool call returns executionId instead of result:**
Scenario runtime exceeded timeout threshold. Use the async pattern — retrieve
by executionId. Do not retry the trigger.

**`isinvalid: true` on a scenario:**
The scenario's connection credential has expired or been disconnected. Re-
authenticate the connection in Make UI → Connections before attempting to run.

**Management tools not available:**
Either the OAuth scope was not set to include management permissions, or the
MCP token was generated with run-only scope. Re-authenticate with the correct
scopes.

**Make MCP not connecting in Claude chat:**
Verify the built-in Make connector is toggled ON in claude.ai Settings →
Connectors. If it was connected but stopped working, disconnect and reconnect
via OAuth.

**Notion reference page not loading:**
Use page ID `351924c8-1673-81ae-aa6b-f6224cfccf76` directly in the Notion
fetch tool. If the page is inaccessible, work from the last known account
values in this skill and flag the issue to Nate.
