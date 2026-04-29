---
name: make-mcp-intelligence
version: 2.0
updated: 2026-04-29
description: >
  Platform intelligence for Make.com — how Make works, how its MCP server
  operates, connection methods across all Claude surfaces, tool surface
  architecture, authentication models, and operational constraints. Load this
  skill whenever working with Make.com on any Claude surface. The living
  intelligence for your specific Make account and scenarios lives in the Make
  Deep Reference Page in Notion.
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
  - "Make is not working"
  - "Make MCP not connecting"
  - "make.com"
  - "Make credentials"
  - "Make connection"
  - "Make execution"
  - "Make blueprint"
  - "Make platform"
  - "how does Make work"
  - "Make MCP server"
  - "Make OAuth"
  - "Make token"
---

# Make MCP Intelligence

## Purpose

This skill documents how Make.com works as a platform — its MCP server
architecture, authentication model, connection methods across every Claude
surface, tool surface capabilities, and operational constraints. It is platform
knowledge, not a runbook. Use it to understand what Make can and cannot do,
how to connect to it, and how its MCP protocol behaves.

---

## Platform Architecture

Make exposes three distinct MCP surfaces. Understanding which one applies to
a given use case is the foundational decision.

### 1. Make MCP Server (full account-scoped)
A cloud-hosted MCP server that exposes all active, on-demand scenarios in a
user's account as callable tools — plus optional management tools for
scenarios, connections, webhooks, data stores, teams, and organizations.
Available on paid plans.

### 2. MCP Toolboxes (curated server)
A second server type for sharing a controlled subset of scenarios. Each
toolbox has a unique URL and one or more keys. Supports per-tool custom names,
descriptions, and read-only vs. read-and-write annotations. Best when
exposing AI tools without granting full account access.

### 3. MCP Client (inside Make scenarios)
Make scenarios can themselves call external MCP servers via an MCP Client
module. This is Make acting as a consumer of MCP, not a provider — scenarios
can reach into GitHub, Webflow, or other MCP-compatible services and
re-expose them through Make's own MCP server.

---

## Authentication

Two authentication mechanisms. Pick based on context.

### OAuth 2.1
Interactive flow. Used by `mcp.make.com` and the built-in Claude connector.
The user selects an organization and grants scopes on a consent screen:
- **Run your scenarios** — minimum required scope
- **View and modify scenarios** — needed for scenario management operations
- **View and modify connections, webhooks, data stores** — needed for
  infrastructure management

OAuth is the recommended path for interactive Claude chat sessions.

### MCP Token
Static bearer token generated under Make Profile → API / MCP Access → Add
Token → Type: MCP Token. Default scope is `mcp:use` (run-only). Additional
management scopes available on paid plans. Can be scoped to a specific
organization, team, or individual scenario via URL query parameters:
- `?organizationId=<id>`
- `?teamId=<id>`
- `?scenarioId=<id>`

Treat MCP tokens as API keys — rotate regularly, never commit to code.

---

## Connection Endpoints

### OAuth endpoints
- Primary (Streamable HTTP): `https://mcp.make.com`
- Stream variant: `https://mcp.make.com/stream`
- SSE variant: `https://mcp.make.com/sse`

### MCP Token endpoints (zone-specific)
- URL-embedded token: `https://<ZONE>/mcp/u/<TOKEN>/stateless`
- Header auth: `https://<ZONE>/mcp/stateless` + `Authorization: Bearer <TOKEN>`

### MCP Toolbox endpoint
`https://<ZONE>/mcp/server/<TOOLBOX_ID>/t/<KEY>/stateless`

### Transport priority
Always prefer `/stateless` (Streamable HTTP). Fall back to `/stream` then
`/sse` only if the client does not support Streamable HTTP. SSE is being
deprecated industry-wide.

### Zone
Make accounts are assigned to a zone (e.g., `us1`, `us2`, `eu1`, `eu2`).
The zone appears in the Make UI URL and in the API response under
`organization.zone`. Always use the account's actual zone — never guess.

---

## Connecting Make MCP Across Claude Surfaces

### claude.ai (web) — Built-in Connector
The recommended path for chat sessions. Make is a first-party connector
in claude.ai as of March 2026.
1. Settings → Connectors → Browse Connectors → search "Make" → click +
2. Complete Make's OAuth consent screen — select organization and scopes
3. Claude now has access to Make's MCP tools in the chat session

### Claude Desktop — Custom Connector
Settings → Connectors → Add custom connector → paste the MCP server or
toolbox URL. Use `/stateless` transport. For toolboxes, paste the full
`…/t/<KEY>/stateless` URL.

### Claude Code (CLI)
```bash
# OAuth
claude mcp add --transport http make https://mcp.make.com

# MCP Token via URL
claude mcp add --transport http make https://<ZONE>.make.com/mcp/u/<TOKEN>/stateless

# MCP Token via header
claude mcp add --transport http make https://<ZONE>.make.com/mcp/stateless \
  --header "Authorization: Bearer <TOKEN>"
```
Run `/mcp` inside Claude Code to verify the connection after adding.

### Anthropic API (`mcp_servers` parameter)
```python
import anthropic
client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    messages=[{"role": "user", "content": "YOUR PROMPT HERE"}],
    mcp_servers=[{
        "type": "url",
        "url": "https://<ZONE>.make.com/mcp/stateless",
        "name": "make",
        "authorization_token": "YOUR_MAKE_MCP_TOKEN",
    }],
    betas=["mcp-client-2025-11-20"],
)
```
The `mcp-client-2025-11-20` beta header is required. Anthropic calls Make
from its own cloud infrastructure — not the client machine. Not covered by
Zero Data Retention. Not supported on Amazon Bedrock or Google Vertex.

---

## Tool Surface

### Scenario tools
Make dynamically generates one MCP tool per active, on-demand scenario in
the connected account. Tool name, description, and input/output schema are
derived entirely from the scenario's own configuration:
- **Name** — from the scenario name (truncated to 56 chars by default;
  override with `?maxToolNameLength=<32–160>`)
- **Description** — from the scenario description field (Claude uses this
  to decide when to invoke — write it carefully)
- **Input schema** — from the scenario's defined Inputs panel
- **Output schema** — from the scenario's defined Outputs panel

A scenario without a description or defined inputs/outputs is still callable
but Claude cannot select it intelligently or parse its results reliably.

### Management tools (paid plans, management scopes required)
When the appropriate OAuth scopes or token scopes are granted, Make exposes
a suite of management tools covering:
- **Scenarios** — list, get, create, update, delete, activate, deactivate,
  clone, run, get execution logs, retrieve execution results by executionId
- **Connections** — list, view metadata
- **Webhooks** — list, create, get URL, modify, delete
- **Data stores** — list, view schema, read/write/delete records
- **Data structures** — list, view
- **Teams and Organizations** — list members, view roles
- **Keys** — list, view

---

## Scenario Visibility Rules

A scenario is only visible as an MCP tool when ALL of the following are true:

1. **Scheduling = On Demand (immediately)** — scheduled or manually-triggered
   scenarios do not appear as MCP tools
2. **isActive = true** — inactive scenarios are invisible
3. **Description present** — without it, Claude cannot reliably select the tool
4. **Inputs and Outputs defined** — without these, Claude cannot pass arguments
   or interpret results

These four requirements are non-negotiable. A scenario missing any one of them
will not function correctly as an MCP tool regardless of other configuration.

---

## Timeout Behavior

Scenario-run tool calls have hard timeout thresholds:
- **OAuth connection:** 25 seconds
- **MCP token connection:** 40 seconds
- **MCP toolbox scenarios:** 40 seconds
- **Management tools (OAuth):** 30 seconds
- **Management tools (stream/SSE):** up to 5 minutes 20 seconds

**Critical:** When a scenario-run call times out, Make returns:
```json
{ "instruction": "...", "executionId": "abc123", "scenarioId": 12345 }
```
The scenario continues running in Make for up to 40 minutes. Retrieve the
result by calling the execution-result tool with the `executionId`. Never
retry the trigger — the original execution is still in progress.

Design all MCP-callable scenarios to complete in under 25 seconds. For longer
work, use a kick-off + poll pattern: scenario 1 enqueues the job and returns
an ID immediately; scenario 2 accepts the ID and returns the result.

---

## What Make MCP Can and Cannot Do

### Can do
- Trigger any active, on-demand scenario as a structured tool call
- Pass typed inputs and receive structured outputs
- List, activate, deactivate, clone, and inspect scenarios (paid + scopes)
- Create and manage webhooks, returning callable URLs
- Read and write Make Data Store records as agent memory
- Retrieve execution logs and async results by executionId

### Cannot do
- Expose scheduled or inactive scenarios as tools
- Provide visual canvas inspection or bundle-by-bundle execution traces
- Function inside Claude artifacts (artifacts cannot call MCP — use Make
  webhooks directly from artifact code instead)
- Operate on Amazon Bedrock or Google Vertex deployments of Claude
- Be covered by Zero Data Retention when used via the Anthropic API

---

## What Not to Do

- Never assume a scenario is MCP-visible without verifying all four
  visibility requirements
- Never retry a timed-out scenario trigger — retrieve by executionId
- Never use SSE transport when stateless is available
- Never expose the full Make account when only specific scenarios are needed
  — use a toolbox
- Never build a single MCP-callable scenario with >25 second runtime
- Never treat scenario names as stable contracts — renaming breaks tool
  selection silently
- Never attempt complex scenario authoring via the management tool surface
  — use the Make UI or Make's Maia assistant for scenario construction

---

## Recovery

**Scenario not visible as MCP tool:**
Verify all four visibility requirements. Most common failure: scheduling not
set to On Demand, or scenario is inactive.

**Claude selects wrong scenario:**
Scenario descriptions are missing or ambiguous. Write descriptions as a
single action sentence — "Receives [inputs], does [action], returns [outputs]."

**Tool call returns executionId instead of result:**
Scenario exceeded timeout threshold. Retrieve result by executionId — do not
retry the trigger.

**Management tools not available:**
OAuth scope or token scope does not include management permissions.
Re-authenticate with the correct scopes selected.

**Make MCP not connecting:**
Verify the connector is active on the correct Claude surface. For built-in
connector: check claude.ai Settings → Connectors → Make toggle is ON. For
token-based: confirm the zone in the URL matches the account's actual zone.

**`isinvalid` scenario fails:**
The scenario's underlying connection credential has expired. Re-authenticate
the connection in Make UI → Connections before attempting to run.
