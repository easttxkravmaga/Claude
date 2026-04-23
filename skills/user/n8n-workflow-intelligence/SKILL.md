---
name: n8n-workflow-intelligence
version: 1.0
updated: 2026-04-23
description: >
  Bulletproof n8n intelligence layer for all three Claude surfaces — Chat,
  Cowork, and Code. Governs pre-build protocol, surface-specific execution
  playbooks, diagnostic and recovery procedures, and the Notion audit loop.
  Covers universal n8n principles, all ETKM-stack integrations (Notion, Google
  Suite, Pipedrive, Anthropic, Telegram, Calendly, Superhuman, WordPress),
  advanced AI agent architecture, and every known production gotcha. This skill
  is the execution layer. The intelligence layer lives in Notion.
trigger: >
  Load whenever any n8n task is in scope — building, debugging, modifying, or
  auditing any workflow. Trigger phrases: "n8n", "workflow", "automation",
  "trigger", "Sheriff Agent", "WF-001", "WF-002", "WF-003", "Pipedrive
  automation", "Calendly trigger", "Telegram bot", "HTTP Request", "webhook",
  "loop", "Code node", "AI Agent node", "sub-workflow", "MCP server".
  Also load for any task where an n8n workflow is a dependency, even if n8n
  is not the primary subject.
notion_reference:
  registry_db: https://www.notion.so/b72c1b3cee304ae9b31635ef4150100a
  registry_db_id: 03a4fe80-8d9a-4b53-bda4-4128207b79ce
  n8n_deep_page: https://www.notion.so/34b924c81673818484e6d1ce956f4b42
  n8n_deep_page_id: 34b924c8-1673-8184-84e6-d1ce956f4b42
dependencies:
  - nate-collaboration-workflow (always loaded in ETKM sessions)
surfaces:
  - Chat (MCP execution, architecture, coordination)
  - Cowork (primary builder — UI canvas execution)
  - Code (Code node JS/Python, workflow JSON, n8n API scripting)
---

# n8n Workflow Intelligence
## The execution layer for zero-mistake n8n operations across Chat, Cowork, and Code.

---

## NOTION AUDIT — MANDATORY FIRST STEP

Before any n8n task begins — on every surface, every session — run this sequence:

1. Open the n8n Deep Reference Page:
   `https://www.notion.so/34b924c81673818484e6d1ce956f4b42`
2. Check **Last Verified** date in Section 1. If >30 days old → flag to Nathan
   before proceeding.
3. Read **Open Issues** (Section 7). If any open issue is relevant to the
   current task → surface it to Nathan before starting.
4. Check **Version & Change Log** (Section 6). Note any entries since last
   session.
5. Confirm the target workflow exists in the **Active Workflow Registry**
   (Section 3).
6. Confirm required credentials are listed as **Active** in Section 1.

Only after this sequence completes does any build, modification, or debug work
begin. This is the audit loop that prevents drift. It runs on use, not on a
schedule.

---

## SURFACE ROUTING — WHICH CLAUDE DOES WHAT

This skill serves three surfaces. Each has a distinct role and execution model.
Know which surface is active and operate within its constraints.

### Chat — Strategic Commander
**Capabilities**: Reason, architect, plan, write workflow JSON, call n8n MCP
tools directly, fetch/push workflow state, interpret execution results, manage
the build queue, coordinate Cowork and Code.

**Primary role**: Architect workflows, design system integrations, manage build
sequencing, interpret failures at a strategic level. Operates via MCP tools or
n8n REST API when MCP is insufficient.

**Execution path**:
1. MCP tools (primary) — `create_workflow`, `update_workflow`, `execute_workflow`,
   `get_workflow_details`, `search_workflows`
2. n8n REST API via HTTP Request (fallback) — `GET/POST /api/v1/workflows`,
   `/api/v1/executions`, `/api/v1/credentials`
3. Produce workflow JSON for Cowork to deploy when UI build is needed

**When to hand off**:
- Hand to **Cowork** when: UI canvas interaction needed, credential configuration
  required, visual node debugging needed, complex multi-branch build
- Hand to **Code** when: Code node JS/Python logic >15 lines, workflow JSON
  construction, n8n API scripting, complex data transformation

### Cowork — Primary Builder
**Capabilities**: Operate the n8n Cloud UI directly at
`https://etxkravmaga.app.n8n.cloud`. Navigate the canvas, drag/connect nodes,
configure parameters, manage credentials, test workflows, read visual error
states, iterate live workflows, deploy to production via Publish.

**Primary role**: This is the primary execution environment for n8n builds.
Receives a precise spec from Chat or Nathan, executes it step-by-step in the
canvas, applies diagnostic protocol on failure, reports results back.

**Execution path**:
1. Navigate to n8n Cloud instance
2. Verify login and instance health
3. Execute the build spec node-by-node
4. Test with pinned data before production
5. Publish when test passes
6. Report result and update Notion Audit Trail (Section 8)

**When to hand off**:
- Hand to **Code** when: Code node logic is complex, workflow JSON needs
  programmatic construction, API scripting needed
- Hand to **Chat** when: architectural decision surfaces mid-build that has
  downstream implications Nathan should own
- Escalate to **Nathan** only when: credential creation needed, or a genuine
  external blocker (API outage, permission wall) is confirmed after diagnostic

### Code — Precision Engineer
**Capabilities**: Write and validate JavaScript/Python for Code nodes, construct
workflow JSON programmatically, build test scripts against the n8n REST API,
handle complex data transformations, manage the GitHub repo, build and validate
SKILL.md files.

**Primary role**: Any logic too complex for node-native operations. Outputs
validated code or JSON in the exact format Cowork or Chat needs to deploy.

**Execution path**:
1. Receive specific code/JSON build task with clear input/output spec
2. Map assumptions explicitly before writing a line
3. Write minimum code that solves exactly what was asked
4. Validate against known patterns in this skill
5. Output in deployment-ready format (Code node JS block or importable JSON)

**When to hand off**:
- Hand to **Cowork** when: code is written and ready to paste into canvas
- Hand to **Chat** when: strategic architecture decision surfaces

---

## PRE-BUILD PROTOCOL — ALL SURFACES

Mandatory before any build, modification, or debug session. Runs mentally on
Chat. Runs as a literal checklist on Cowork and Code.

### Step 1 — Map the full workflow before touching anything
- Name every node in sequence: Trigger → [Node 1] → [Node 2] → ... → Output
- Identify every branch (IF outputs, Switch outputs, error output)
- Name every external service the workflow touches
- Identify every dependency: credentials, workflow IDs, database IDs, API keys

### Step 2 — Confirm dependencies exist
- Every credential in play → confirmed Active in Notion Section 1
- Every Notion database ID → confirmed accessible
- Every Pipedrive pipeline/stage ID → confirmed in Notion Section 3
- Every sub-workflow → confirmed Published and accessible

### Step 3 — State the test plan
- What pinned data will be used for testing?
- What does a passing test look like? (specific output values, not just "no error")
- What edge cases need testing? (empty array, null field, auth failure)

### Step 4 — State the error handling plan
- What happens when the primary path fails?
- Which nodes need `onError = continueErrorOutput`?
- Is the global Error Workflow (Telegram alert) set for this workflow?

### Step 5 — State any assumptions explicitly
If anything in the spec is ambiguous, state the assumption before building.
Don't build on an unspoken assumption. If the assumption is wrong, rework is
expensive. Stating it costs nothing.

Only after Steps 1–5 are complete does any node get created.

---

## SECTION 1 — UNIVERSAL n8n PRINCIPLES

### Execution model
Every workflow is a directed graph starting from a trigger. No trigger = no
execution. Flow runs left-to-right. In v2.x, branches run sequentially to
completion before the next branch starts.

**Publish model (2.0+)**: Workflows are Saved (draft) or Published (live).
Only Published workflows respond to production webhooks and schedule triggers.
Save ≠ Publish. This is the #1 cause of "it worked in test, nothing in prod."

**Manual executions**: Do NOT persist static data. Do NOT trigger Error Workflow.
Only production (Published) executions do both.

### Data structure — items array
Every data packet is an array of item objects:
```json
[{
  "json": { "field": "value" },
  "binary": { "data": { "data": "<base64>", "mimeType": "...", "fileName": "..." } },
  "pairedItem": { "item": 0 }
}]
```
`json` is always required. `binary` is optional. `pairedItem` preserves lineage
for `$('Node').item` expression access. Binary data is dropped unless explicitly
carried through — in a Code node return `{ json: ..., binary: item.binary }`.

### Built-in variables — production reference
| Variable | Use |
|---|---|
| `$json` | Current item's JSON |
| `$binary` | Current item's binary |
| `$input.all()` | All input items as array |
| `$input.first()` / `.last()` | First or last input item |
| `$input.item` | Current item (per-item mode) |
| `$('NodeName').all()` | All items from named upstream node |
| `$('NodeName').first()` | First item from named upstream node |
| `$('NodeName').item` | Paired item from named upstream node |
| `$itemIndex` | Index of current item in run |
| `$runIndex` | Run count (increments in loops) |
| `$workflow.id` / `.name` / `.active` | Workflow metadata |
| `$execution.id` / `.mode` / `.resumeUrl` | Execution metadata |
| `$vars.varName` | Custom variables (use instead of `$env`) |
| `$now` | Luxon DateTime, current instant |
| `$today` | Luxon DateTime, today at 00:00 |
| `$getWorkflowStaticData('global'|'node')` | Persistent state (production only) |
| `$fromAI('key', 'desc', 'type')` | LLM-populated param (Tools Agent only) |

**`$env` is blocked by default on n8n Cloud.** Use `$vars` or Credentials.

### Expression syntax — when and how
Fields toggle between **Fixed** and **Expression** mode (purple).
In Fixed mode, `{{ $json.id }}` is sent as the literal string — most common
beginner mistake.

**Common patterns**:
```
{{ $json.email }}                           // current item field
{{ $json?.address?.city ?? 'Unknown' }}     // null-safe with fallback
{{ $('GetDeals').first().json.stage_id }}   // upstream node first item
{{ $('GetDeals').all().length }}            // count upstream items
{{ $now.toFormat('yyyy-MM-dd') }}           // Luxon date format
{{ $now.plus({ days: 7 }).toISO() }}        // date math
{{ $jmespath($json, 'items[].id') }}        // JMESPath query
{{ $vars.slackChannel }}                    // custom variable
```

**Use `??` not `||` for fallbacks.** `||` treats `""`, `0`, and `false` as
empty. `??` only treats `null` and `undefined` as empty.

**Use `?.` for nested access.** `$json.user?.address?.zip` returns undefined
instead of throwing when intermediate keys are missing.

### Code node — rules
**All Items mode** (default): receives full input array via `$input.all()`.
Must return `[{ json: {...} }]` array.

**Each Item mode**: runs N times. Current item via `$json`. Return a single
`{ json: {...} }` object (auto-wrapped since v0.166).

**On n8n Cloud**: no `require()` of external npm modules. Only built-in Node.js
modules available (`crypto`, `url`, etc.) when enabled by self-hosted config
— not available on Cloud. Use native JS only.

```javascript
// All Items — canonical pattern
return $input.all().map((item, i) => ({
  json: { ...item.json, enriched: true, index: i },
  pairedItem: { item: i }
}));

// Static data persistence (production runs only)
const store = $getWorkflowStaticData('global');
const lastId = store.lastSeenId ?? 0;
const fresh = $input.all().filter(i => i.json.id > lastId);
if (fresh.length) store.lastSeenId = Math.max(...fresh.map(i => i.json.id));
return fresh;

// HMAC signature verification
const crypto = require('crypto');
const sig = $json.headers['x-signature-256'];
const expected = 'sha256=' + crypto
  .createHmac('sha256', $vars.WEBHOOK_SECRET)
  .update($json.rawBody)
  .digest('hex');
if (!crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(sig))) {
  throw new Error('Invalid webhook signature');
}
return $input.all();
```

### Core nodes — critical behavior

**IF**: Routes each item to true (output 0) or false (output 1). AND/OR
combinators available but cannot be mixed in one node — nest IFs for AND+OR.

**Switch**: Rules mode or Expression mode. First match wins unless
"Send to all matching outputs" is enabled.

**Merge** — know the modes:
- `Append`: concatenates inputs sequentially
- `Combine > Matching Fields`: join by key — inner/left/right/outer
- `Combine > All Possible Combinations`: cartesian product — use with caution
- `Choose Branch`: synchronize without combining — use when one branch may be empty

**Merge hangs** when an input branch never fires. Fix: use Choose Branch or
restructure to avoid empty branches.

**Loop Over Items (Split In Batches)**: Two outputs — `loop` (current batch,
connect processing here AND back to Loop input) and `done` (fires once when
complete, connect aggregation/next step here). Connecting processing to `done`
is a common mistake — it runs once with all items, not per batch.

**Wait node**: Use for retry backoff: `{{ Math.pow(2, $runIndex) * 1000 }}` ms.
Intervals <65s are in-memory; ≥65s are offloaded to DB.

**Edit Fields (Set)**: Key toggles — `Keep Only Set` removes all other fields.
`Support Dot Notation` (default ON) means `a.b = 1` creates `{ a: { b: 1 } }`.

**Aggregate**: Collapses N items into 1 item with an array. Required when a
downstream API needs `{ records: [...] }` format.

### Error handling

**Global Error Workflow**: Set in Workflow Settings → Error workflow. Points to
a dedicated workflow starting with Error Trigger. All production workflows must
use this. Fires only on production executions.

**Error Trigger payload** (key fields):
```
$json.execution.error.message     // error text
$json.execution.url               // link to the failed execution
$json.execution.lastNodeExecuted  // which node failed
$json.workflow.name               // which workflow
```

**Per-node settings** (Settings tab):
- `Retry On Fail` + Max Tries (max 5) + Wait Between Tries (max 5000ms)
- `On Error`: `stopWorkflow` (default), `continueRegularOutput`, `continueErrorOutput`

**Known bug**: When `onError ≠ stopWorkflow`, Retry On Fail is silently ignored.
Keep `stopWorkflow` and handle failures via Error Workflow for retries to work.

### Schedule Trigger — timezone rule
Default timezone is `America/New_York` on self-hosted n8n. ETKM instance uses
`America/Chicago` (Central). **Always set timezone explicitly in Workflow
Settings** — do not rely on instance default.

Common cron patterns:
```
0 9 * * *        // daily 9am
0 9 * * 1-5      // weekdays 9am
0 9 * * 0        // Sunday 9am
*/15 * * * *     // every 15 minutes
0 0 1 * *        // first of month midnight
```

### Webhook — test vs production
- Test URL: `/webhook-test/<path>` — active 120s after "Listen for test event"
- Production URL: `/webhook/<path>` — active only when workflow is Published
- One (method + path) combination per instance — no duplicates
- Max payload: 16MB
- Cloudflare on n8n Cloud enforces 100s timeout → use Respond Immediately for
  long-running workflows

---

## SECTION 2 — ETKM STACK INTEGRATIONS

### Notion
**Credential**: Notion API (token `ntn_...`). Every target page/database must
be shared with the integration via Notion Connections menu — `object_not_found`
error means it's not shared.

**Operations**: Block (Append After, Get Child), Database (Get, Search),
Database Page (Create, Get, Get Many, Update), Page (Archive, Create, Search).

**Property write formats** (most common):
```javascript
// rich_text
{ "field": { "rich_text": [{ "text": { "content": "value" } }] } }
// select
{ "Status": { "select": { "name": "Active" } } }
// multi_select
{ "Tags": { "multi_select": [{ "name": "tag1" }, { "name": "tag2" }] } }
// relation — MUST use dashed UUID
{ "Projects": { "relation": [{ "id": "6c42-40a9-..." }] } }
// date
{ "Due": { "date": { "start": "2026-04-23" } } }
// number, checkbox, url: raw value
```

**Property names are case-sensitive.** `"Status"` ≠ `"status"`. Copy exactly
from Notion UI.

**Pagination**: Enable `Return All` on Get Many — n8n handles cursor internally.
Rate limit: 3 req/sec. Throttle bulk operations with Loop Over Items (batch 3)
+ Wait (350ms).

**Relation field gotcha**: IDs must be dashed UUID format. Pre-process with:
`{{ $json.id.replace(/(.{8})(.{4})(.{4})(.{4})(.{12})/, '$1-$2-$3-$4-$5') }}`

**ETKM active database IDs** (from memory — verify in Notion Section 3):
- Assets: `72dfe39a`
- Social Calendar: `53e7a656`
- Content Hub: `69345a21`
- Projects: `e1e5d9e9`
- Audience Segments: `d43e07c2`
- Nurture Sequences: `c699d080`
- Categories/Tags: `98ffeef2`
- P6 Media Library: `9d79095f`
- Tools Registry: `03a4fe80-8d9a-4b53-bda4-4128207b79ce`

### Gmail
**Credential**: Gmail OAuth2. Requires re-auth if token expires.

**Send params**: `sendTo`, `subject`, `emailType` (text/html), `message`,
`options.attachmentsUi.attachmentsBinary[].property` (binary key names).

**Reply threading**: Use `messageId` parameter — node auto-sets `threadId` and
`In-Reply-To`. Add `Re:` prefix check in subject.

**Trigger**: Polling only (no push webhooks in n8n). Filters: `q` (Gmail search
operators), `labelIds`, `readStatus`.

**Useful Gmail search operators**:
```
from:alice@x.com  subject:"invoice"  has:attachment  is:unread  newer_than:7d
label:billing  -label:archived  after:2026/04/01
```

**Attachments incoming**: Enable `Download Attachments` → binary keys
`attachment_0`, `attachment_1`, etc.

### Google Drive
**Credential**: Google Drive OAuth2. **Expires every 7 days on unpublished
consent screens** — re-authenticate when Drive workflows fail on auth.

**Upload**: Set `inputDataFieldName` to match the binary property key name
(default `data`). Mismatch → silent failure.

**Download Google-native files** (Docs/Sheets/Slides): must specify export
format. Docs → `docx`/`pdf`, Sheets → `csv`/`xlsx`, Slides → `pptx`/`pdf`.

**Service accounts** (post April 15, 2025): cannot access My Drive without
domain-wide delegation. Use Shared Drives or OAuth2 for My Drive access.

### Google Calendar
**Event create**: `start`/`end` in ISO 8601. All-day events use `date` format
(`2026-06-01`), not `dateTime`. Timed events use full ISO with timezone.

**Timezone**: Always set explicitly — ETKM uses `America/Chicago`.

### Pipedrive
**Credential**: Pipedrive API Token (simplest, recommended for ETKM use).

**Custom fields gotcha**: API uses 40-char hash keys (`dcf558aac1ae...`), not
labels. Silently ignores unknown keys. Get hash from:
`GET https://api.pipedrive.com/api/v2/dealFields?api_token=X`
Then use `$json.key` field value.

**v2 node (April 2026)**: custom fields now nested under `custom_fields` in
response. Update field access to `$json.custom_fields.{hash}`.

**Stage-triggered workflows**: subscribe to `deal.updated` webhook event.
Compare `data.stage_id` vs `previous.stage_id` in IF node.

**ETKM pipeline IDs** (from memory — verify in Notion):
- P1 Prospects: 8 stages
- P2 Level 1: 7 stages
- P3 Advanced/Experienced: 5 stages
- P4 At-Risk: 2 stages
- P5 Private: standalone

**Rate limiting (active Dec 2025)**: Daily budget = `30000 × plan_mult × seats`.
Throttle bulk ops with Loop Over Items (batch 10) + Wait (200ms).

**Pipedrive Trigger max**: 40 webhooks per user. Audit and delete unused before
adding new ones.

### Anthropic Claude API
**Credential**: Anthropic API (Predefined Credential Type) — auto-injects
`x-api-key` header.

**HTTP Request pattern** (production-robust):
```
POST https://api.anthropic.com/v1/messages
Header: anthropic-version: 2023-06-01
Body (JSON):
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 4096,
  "system": "...",
  "messages": [{ "role": "user", "content": "{{ $json.prompt }}" }]
}
```

**Response extraction**:
```
{{ $json.content.find(b => b.type === 'text').text }}
```

**⚠️ MODEL DEPRECATION WARNING**: `claude-sonnet-4-20250514` retires
**June 15, 2026**. Any workflow using this model string will silently fail
after that date. Audit all workflows. Migrate to `claude-sonnet-4-5-20250929`.

**Current model defaults for ETKM**:
- Primary: `claude-sonnet-4-5-20250929` (stable, pinned)
- Light/fast tasks: `claude-haiku-4-5`
- High-complexity: `claude-sonnet-4-6`

**JSON extraction via tool_use** (most reliable for structured output):
```json
"tools": [{ "name": "emit", "input_schema": { ...schema... } }],
"tool_choice": { "type": "tool", "name": "emit" }
```
Then: `{{ $json.content.find(b => b.type === 'tool_use').input }}`

**Error codes**: 429 → honor `retry-after` header. 403 → check billing/limits.
529 → overloaded, not billed, retry with backoff.

### Telegram
**Credential**: Telegram Bot (BotFather token). ETKM bot: `@etkmSheriff_bot`.
Live on Render at `claude-r82h.onrender.com`.

**Parse modes**: Use `HTML` for ETKM messages — simpler escaping than
MarkdownV2. Tags: `<b>`, `<i>`, `<code>`, `<pre>`, `<a href="">`. Escape
`< > &` in content.

**Chat ID**: Nathan's personal chat ID stored in Telegram credentials. Get
from `{{ $json.message.chat.id }}` on first message.

**Trigger**: Webhook-only. Auto-registers on workflow activation. Only one
webhook per bot token — test and production workflows cannot share the same
bot credential. Use separate bots for test vs prod.

**Rate limits**: 1 msg/sec per chat, 20 msg/min per group.

**Error alert template** (use in Error Workflow):
```
<b>🚨 Workflow Failed</b>
<b>Workflow:</b> {{ $json.workflow.name }}
<b>Node:</b> {{ $json.execution.lastNodeExecuted }}
<b>Error:</b> {{ $json.execution.error.message }}
<b>Execution:</b> <a href="{{ $json.execution.url }}">View in n8n</a>
```

### Calendly
**Trigger only** in n8n — no action node. All Calendly operations via HTTP
Request with Predefined Credential Type = Calendly API.

**v2 API only** (v1 retired May 2025). Personal Access Token required.
Standard+ plan needed.

**Trigger events**: `invitee.created`, `invitee.canceled`,
`routing_form_submission.created`.

**Reschedule fires both events** — `invitee.canceled` (with `rescheduled: true`)
AND `invitee.created`. Add IF check on `{{ $json.payload.rescheduled }}` to
deduplicate.

**Key payload paths**:
```
$json.payload.email
$json.payload.scheduled_event.start_time
$json.payload.scheduled_event.location.join_url
$json.payload.questions_and_answers
$json.payload.cancellation.reason
```

**WF-001 integration**: Calendly `invitee.created` fires → Pipedrive person
create/find → move to P1-S3 → trigger WF-001 email sequence.

### Superhuman
**No native n8n node.** Two paths:

**Path 1 (recommended)**: Drive the Gmail mailbox directly via Gmail node.
Superhuman is a Gmail client — all actions reflect in Gmail in real-time.
"Done" in Superhuman = archive (remove `INBOX` label).

**Path 2 (MCP)**: Superhuman MCP server at `https://mcp.mail.superhuman.com/mcp`.
Available tools: `list_threads`, `query_email_and_calendar`, `send_draft`,
`send_email`. Requires Business plan + "Ask AI" enabled. Only usable inside
AI Agent node via MCP Client Tool — not as a deterministic action node.

### HTTP Request — universal patterns

**Auth options**: Predefined Credential Type (best — use existing app
credentials), Generic Credential (manual header/bearer/OAuth2), None.

**Body types**:
- `JSON` → set content-type `application/json` automatically
- `Form-Data Multipart` → for file uploads (set Name + Input Data Field Name)
- `Binary` → stream single binary file as body
- `Raw` → supply Content-Type + raw string

**Pagination modes**:
1. Update Parameter Each Request — use `$pageCount`, `$response.body` variables
2. Response Contains Next URL — expression returning next page URL
3. Manual with Loop Over Items + IF (stop when empty/no next cursor)

**File download**: `Options → Response Format: File` + set `Put Output in Field`.

**Resilient pattern** (all external API calls):
```
Options → Enable: Never Error + Include Response Headers and Status
→ IF: {{ $json.statusCode < 300 }} → success path
                                   → error path (retry or alert)
```

**Rate limit handling**:
```javascript
// In Code node after 429
const retryAfter = parseInt($json.headers['retry-after'] ?? '2', 10);
// Then Wait node with: {{ retryAfter * 1000 }}
```

### WordPress REST API
**No native node** — use HTTP Request with Basic Auth.
Username: WordPress username. Password: Application Password (not account
password) — generate at `Users → Profile → Application Passwords`.

```
GET https://your-site.com/wp-json/wp/v2/posts?per_page=100&page={{ $runIndex + 1 }}
GET https://your-site.com/wp-json/wp/v2/posts/{{ $json.id }}
POST https://your-site.com/wp-json/wp/v2/posts
```

**Pagination pattern**: Loop Over Items → HTTP (fetch page N) → IF (array
length > 0) → loop back; else → done.

---

## SECTION 3 — ADVANCED PATTERNS

### AI Agent (Tools Agent)
As of n8n v1.82, the AI Agent operates only as Tools Agent (native tool-calling).
Previous modes (ReAct, Conversational, etc.) are removed.

**Cluster node slots**:
- `ai_languageModel` → connect Chat Model sub-node
- `ai_memory` → connect Memory sub-node (Postgres Chat Memory for production)
- `ai_tool` → connect Tool nodes (one or more)

**`$fromAI()` for tool parameters**:
```
{{ $fromAI('recipient_email', 'The email address to send to', 'string') }}
{{ $fromAI('subject', 'Email subject line', 'string') }}
```
Descriptions become the tool schema — write them as instruction text for the LLM.

**Production memory**: Use Postgres Chat Memory or Redis Chat Memory. Simple
Memory is in-memory only — lost on restart, dev/test only.

**Sheriff Agent architecture** (live):
- Trigger: Schedule (9am CT daily, Sunday digest)
- Model: Anthropic Chat Model
- Memory: (check current config)
- Tools: Notion query tools, Telegram send
- Deployment: Render at `claude-r82h.onrender.com`

### Sub-workflow architecture
Use when: workflow >30 nodes, reusable logic module, memory isolation for large
datasets, failure domain isolation.

**Child workflow must start with Execute Sub-workflow Trigger** (not Manual
Trigger or Start node — Start node is removed in 2.0).

**Data flows**: Parent passes items → child trigger → child processing → child
returns items → parent continues. Parent waits for child completion including
through Wait states (2.0 behavior change).

**Error propagation**: Child errors bubble to parent unless parent node has
`onError = continueErrorOutput`.

### MCP Server (n8n as server for Claude)
n8n instance exposes an MCP server at:
`https://etxkravmaga.app.n8n.cloud/mcp-server/http`

Tool nodes wired to MCP Server Trigger become exposed tools callable by Claude
(Chat, Cowork, Code) via the MCP connection.

**Transport**: Streamable HTTP (no stdio). **Queue mode**: sticky-route `/mcp*`
to one replica if using workers.

### Polling with deduplication
```javascript
// Code node — All Items mode
const store = $getWorkflowStaticData('global');
const last = store.lastSeenId ?? 0;
const fresh = $input.all().filter(i => i.json.id > last);
if (fresh.length) {
  store.lastSeenId = Math.max(...fresh.map(i => i.json.id));
}
return fresh.length > 0 ? fresh : [{ json: { _empty: true } }];
// Follow with IF: {{ !$json._empty }} to stop on no new items
```

### Idempotency pattern
Every write operation should be safely re-runnable:
- Use deterministic external IDs: `md5(source + recordId)`
- Use upsert operations: Postgres `ON CONFLICT`, Notion Create or Update,
  Pipedrive Find or Create
- Propagate `Idempotency-Key` header on HTTP writes

### Rate limiting — universal throttle pattern
```
Loop Over Items (batchSize: 3-10)
  → [operation node]
  → Wait (350ms for Notion, 200ms for Pipedrive, 1000ms for Gmail)
  → back to Loop input
Loop done output → next step
```

---

## SECTION 4 — DIAGNOSTIC & RECOVERY PROTOCOL

### When a workflow fails — mandatory sequence

**Step 1**: Stop. Do not retry the same approach.

**Step 2**: Identify the failure type:
- **Auth failure** → check credential status in Notion Section 1 → re-authenticate
- **Data shape error** → inspect input/output panel → check expression syntax
- **Rate limit (429)** → add Loop + Wait throttling pattern
- **Notion error** → check property name case, relation UUID format, integration sharing
- **Pipedrive error** → check custom field hash vs label, stage ID vs name
- **Webhook not firing** → check Published status, test vs prod URL
- **Empty array stop** → add Always Output Data or length IF check

**Step 3**: Check the Known Error Log in Notion Section 5 before diagnosing
independently. Pattern may already be documented.

**Step 4**: Exhaust all alternative approaches within the skill before escalating.

**Step 5**: Escalate to Nathan only when:
1. New credential creation is required (only Nathan can create credentials)
2. A strategic architecture decision has downstream implications Nathan should own
3. A genuine external blocker is confirmed (API outage, permission wall) after
   all diagnostic paths are exhausted

**Never escalate** without stating: what was tried, what failed, and exactly
what the specific blocker is.

### Top 20 mistakes — active checklist

When a build produces unexpected results, run this list:

| # | Mistake | Check |
|---|---|---|
| 1 | Node in Fixed mode, not Expression mode | Field showing `{{ }}` as literal string? Toggle to Expression |
| 2 | Workflow Saved but not Published | Production webhook/schedule not firing? Click Publish |
| 3 | Test URL used in production | URL contains `/webhook-test/`? Switch to `/webhook/` |
| 4 | Empty branch causing Merge hang | Merge node waiting forever? Check for branch that never fires |
| 5 | Processing connected to Loop `done` output | Loop running once not per batch? Connect processing to `loop` output |
| 6 | Notion property name case mismatch | `object` error? Copy property name exactly — case sensitive |
| 7 | Pipedrive label used instead of hash key | Custom field silently ignored? Use 40-char hash from `/dealFields` |
| 8 | Binary property name mismatch | Binary lost between nodes? Check exact property key in output schema |
| 9 | Google Drive credential expired | Drive 401 after days? Re-authenticate OAuth2 credential |
| 10 | `$env` returns undefined | Using `$env` on Cloud? Switch to `$vars` |
| 11 | Code node returning wrong shape | All Items mode returning bare object? Return `[{ json: {...} }]` array |
| 12 | Sub-workflow missing Execute Trigger | Sub-workflow not receiving data? Add Execute Sub-workflow Trigger |
| 13 | Calendly reschedule double-firing | Getting duplicate events? Check `payload.rescheduled` flag |
| 14 | Telegram MarkdownV2 parse error | Message fails with entity error? Switch to HTML parse mode |
| 15 | Empty array stops workflow silently | Workflow just stops? Enable Always Output Data |
| 16 | Timezone mismatch on Schedule | Schedule fires at wrong time? Set timezone in Workflow Settings |
| 17 | Notion relation ID not dashed | Relation write fails? Pre-process to dashed UUID format |
| 18 | `||` treating `0` or `""` as empty | Wrong fallback value? Use `??` instead of `||` |
| 19 | Pipedrive webhook limit hit | New trigger not firing? Audit and delete unused webhooks (max 40) |
| 20 | Deprecated Claude model string | Claude node silently fails June 15 2026? Migrate from `claude-sonnet-4-20250514` |

---

## SECTION 5 — GOLDEN RULES

These are non-negotiable across all surfaces. Violating them is the primary
cause of rework.

1. **Notion audit first.** Every session. Every surface. No exceptions.

2. **Publish ≠ Save.** Never assume a workflow is live because it's saved.
   Always verify Published status before debugging production behavior.

3. **Expression mode must be on.** Whenever a field uses `{{ }}` syntax,
   it must be in Expression mode (purple field). Fixed mode sends `{{ }}` as
   literal text.

4. **`??` not `||` for defaults.** Protects against `0`, `""`, and `false`
   being treated as empty.

5. **Always Output Data on every conditional.** Prevents silent stops when
   an IF branch returns zero items.

6. **Loop connections are critical.** Processing connects to `loop` output.
   Aggregation connects to `done` output. Wrong connection = loop runs once or
   infinitely.

7. **Throttle every bulk operation.** Loop Over Items + Wait before any API
   that has rate limits (Notion, Pipedrive, Gmail, Telegram). Not optional.

8. **Binary property names must match exactly.** Check the output schema tab
   before referencing a binary key in the next node.

9. **Every production workflow has the Error Workflow set.** If it's not set,
   failures are silent. Set it in Workflow Settings before Publish.

10. **Never use `claude-sonnet-4-20250514` after June 15, 2026.** Audit all
    workflows now. Migrate to `claude-sonnet-4-5-20250929`.

11. **Credential issues are not code issues.** When auth fails, check the
    credential in n8n settings before touching the workflow.

12. **State the plan before building.** If the plan isn't clear enough to
    state, it's not clear enough to build. Run the Pre-Build Protocol.

---

## SECTION 6 — NOTION MAINTENANCE PROTOCOL

After every n8n session that surfaces a new error, pattern, or change:

**If a new error was encountered and resolved**:
→ Add entry to Known Error Log (Notion Section 5)
→ Increment `Open Issues` count if unresolved, or keep count if resolved
→ Update Audit Trail (Notion Section 8) with date, surface, what changed

**If a new pattern was proven in production**:
→ Add entry to Patterns & Recipes (Notion Section 4)
→ Update Audit Trail

**If a new workflow was created or modified**:
→ Update Active Workflow Registry (Notion Section 3) with workflow ID, trigger
  type, and dependencies

**If a version change is detected**:
→ Add entry to Version & Change Log (Notion Section 6)
→ Update `Last Verified` date in Notion Section 1
→ Update `Version in Use` field in Tools Registry row

**If Open Issues count changes**:
→ Update the `Open Issues` number field in the Tools Registry database row
  for n8n — this is visible from the index without opening the deep page

---

## SESSION CLOSING PROTOCOL

When an n8n session completes:

1. **State what was built** — workflow name(s), node count, trigger type
2. **State what was tested** — test method, result
3. **State what's live** — Published status confirmed
4. **Flag open items** — anything unresolved, with specific blocker
5. **Update Notion** — run Notion Maintenance Protocol above
6. **Next action and owner** — what happens next, who does it

---

## VERSION HISTORY

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-04-23 | Initial build. Full universal principles, all ETKM stack integrations, AI agent architecture, diagnostic protocol, Notion audit loop, surface routing playbooks. Notion deep reference page live at `34b924c8-1673-8184-84e6-d1ce956f4b42`. |
