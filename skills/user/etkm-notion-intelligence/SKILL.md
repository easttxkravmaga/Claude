---
name: etkm-notion-intelligence
version: 1.0
updated: 2026-04-24
description: >
  Load this skill for ANY task that reads, writes, queries, or builds on top of
  ETKM's Notion workspace. Triggers include: n8n workflows touching Notion,
  Sheriff Agent reads/writes, MCP operations in Claude sessions, dashboard builds,
  schema changes, automation architecture, and database queries. This is the
  authoritative reference for all Notion operations in the ETKM stack. Do NOT
  operate on Notion without this skill loaded.
---

# ETKM Notion Intelligence

**Version:** 1.0
**Last Updated:** 2026-04-24
**API Version in Use:** 2025-09-03 (mandatory on all calls)
**Next Quarterly Review:** 2026-07-24

---

## SECTION 1 — SYSTEM CONTEXT

### What Notion Is in the ETKM Stack

Notion is the **operations and knowledge brain**. It is NOT a transactional system.

| Layer | System | What It Owns |
|---|---|---|
| Sales pipeline + lead CRM | Pipedrive | Deals, contacts, pipeline stages, activity logs |
| Operations + knowledge | **Notion** | Projects, tasks, content, SOPs, curriculum, assets, tools registry, blog DB |
| Automation connective tissue | n8n | All bidirectional sync between systems |
| AI execution | Claude API + MCP | Reads/writes Notion for knowledge work and agent tasks |
| File storage | Google Drive | Video, large media, book reports, delivered assets |
| Website | WordPress + GeneratePress | Public-facing site; Notion feeds content pipeline |
| Messaging | Telegram | Sheriff Agent surfaces Notion data to Nathan |
| Email | Superhuman + Pipedrive | Outbound; Notion holds email system schemas |

**The division of truth is non-negotiable:**
- Pipedrive = source of truth for all sales and CRM data
- Notion = source of truth for all operational, project, content, and knowledge data
- Never try to run the CRM from Notion. Never try to run project ops from Pipedrive.

### Three Claude Surfaces and How They Hit Notion

| Surface | Auth Method | Use Case |
|---|---|---|
| Claude Chat / Code (interactive) | Hosted MCP — `mcp.notion.com` — OAuth | Knowledge queries, page creation, schema updates during live sessions |
| Sheriff Agent / headless automation | Direct REST API — bearer token `ntn_...` | Daily briefs, automated writes, cron-triggered operations |
| n8n workflows | n8n Notion node OR HTTP Request node | All sync operations between Notion and Pipedrive, WordPress, etc. |

**Critical rule:** The hosted MCP server does NOT support bearer token auth. Headless agents must use the direct API or local MCP server. Never attempt OAuth in an unattended workflow.

---

## SECTION 2 — THE MANDATORY FIRST STEP (2025-09-03 Migration)

### Why This Matters

In September 2025, Notion split the "database" into two layers:
- **Database** — the container (ID you see in the URL)
- **Data Source** — the actual table of records with its schema

**All API reads and writes must target the `data_source_id`, not the `database_id`.**

Old integrations using `/v1/databases/{id}/query` still work on single-source databases — but the moment a second data source is added, they break silently. Build everything on the new pattern.

### Mandatory First Step Pattern

```bash
# Step 1: Retrieve the database to get the data_source_id
GET /v1/databases/{DATABASE_ID}
Headers:
  Authorization: Bearer ntn_...
  Notion-Version: 2025-09-03

# Response contains:
# "data_sources": [{ "id": "collection://...", "name": "..." }]

# Step 2: Cache the data_source_id
# Step 3: All subsequent reads/writes use data_source_id, not database_id
POST /v1/data_sources/{DATA_SOURCE_ID}/query
```

**The IDs below are pre-retrieved and verified against the live workspace on 2026-04-24. Use them directly. Verify quarterly.**

---

## SECTION 3 — ETKM DATABASE REGISTRY

### Live Database and Data Source IDs (Verified 2026-04-24)

| Database | Database ID | Data Source ID | Emoji |
|---|---|---|---|
| Tools Registry | `b72c1b3c-ee30-4ae9-b316-35ef4150100a` | `collection://03a4fe80-8d9a-4b53-bda4-4128207b79ce` | 🛠️ |
| ETKM Tasks | `a5ef89df-ba16-48a0-9762-1d1338992bc9` | `collection://cc91430b-f1b0-486b-afdf-fccd26dd7433` | ✅ |
| Projects | `e1e5d9e9-6e15-4e7a-b5aa-fd8b92097da6` | `collection://f290238d-1616-45f2-a694-f8710f036bc4` | 📋 |
| Assets | `72dfe39a-4d78-451d-b658-67e233cba8d8` | `collection://5381e8ec-1e5f-4588-b9cc-74107c176341` | 📁 |
| Social Media Calendar | `53e7a656-3fac-482b-9725-1a2c43a4c7f0` | `collection://589dcd23-97f2-4959-8574-f7ea9c742cf1` | 📅 |
| Content Hub | `69345a21-3d44-466f-8905-bfa99f97d3fb` | `collection://093b4700-f05f-4e5b-bfc6-a0605f499c1b` | 📝 |
| Categories & Tags | `98ffeef2-a44f-45d0-ab60-a3ae48d52ac0` | `collection://22366aac-1432-4971-8cd0-9f0f5247e76b` | 🏷️ |
| People & Organizations | `342d3e39-af77-405f-9709-5873e9008584` | `collection://ca593219-63c9-4f91-8ee8-727df8a5efc9` | 👥 |
| ETKM Blog Article Database | `13455c39-b650-4076-ad65-a4c8701dd378` | `collection://0b46f054-5967-4d66-9090-35ef654e397f` | 📰 |
| P6 Media Library | `9d79095f-0000-0000-0000-000000000000` | *(retrieve on first use)* | 🎬 |
| Audience Segments | `d43e07c2-0000-0000-0000-000000000000` | *(retrieve on first use)* | 🎯 |
| Nurture Sequences | `c699d080-0000-0000-0000-000000000000` | *(retrieve on first use)* | 📧 |

> **Note:** Rows marked `*(retrieve on first use)*` have database IDs from memory but data source IDs not yet confirmed via live call. Run the mandatory first step pattern before writing to those databases.

### Parent Page Structure

```
AI Resources (30f924c8-1673-80f0-95db-c64fa64f8f86)
├── ETKM Big Projects List (323924c8-1673-814d-a1b7-f0fcee8b9772)
│   ├── 🛠️ ETKM Tools Registry [database]
│   ├── n8n — Deep Reference Page
│   └── Pipedrive — Deep Reference Page
├── ETKM Content System (302924c8-1673-8123-8e3a-e9e406bfdbf6)
│   ├── Content Hub [database]
│   ├── Social Media Calendar [database]
│   ├── Assets [database]
│   ├── Projects [database]
│   ├── Categories & Tags [database]
│   ├── People & Organizations [database]
│   └── ETKM Blog Article Database [database]
└── ETKM Tasks [database] (standalone under AI Resources)
```

---

## SECTION 4 — DATABASE SCHEMAS (Live, Verified 2026-04-24)

### 4.1 ETKM Tasks

**Data Source:** `collection://cc91430b-f1b0-486b-afdf-fccd26dd7433`
**Purpose:** All active work items across Nathan + Claude + External. Single task database for the entire system.

| Property | Type | Values / Notes |
|---|---|---|
| Task | title | The task name — always populate |
| Status | select | `To Do` / `In Progress` / `Awaiting Nathan` / `Blocked` / `Done` |
| Owner | select | `Nathan` / `Claude` / `External` |
| Phase | select | `Strategy` / `Copy` / `Build` / `QC` / `Launch` / `Monitor` / `Planning` / `Logistics` / `Marketing` / `Execution` / `Post-Event` / `Arc Map` / `Draft` / `Review` / `Load` / `Activate` / `Scope` / `Extract` / `Deploy` / `Other` |
| Project | relation → Projects | Links to `collection://f290238d-1616-45f2-a694-f8710f036bc4` |
| Due Date | date | `date:Due Date:start` / `date:Due Date:end` / `date:Due Date:is_datetime` |
| Completed Date | date | `date:Completed Date:start` — set when Status → Done |
| Notes | rich_text | Supporting context, blockers, links |
| Created | created_time | Auto — read only |
| Last Edited | last_edited_time | Auto — read only |

**AI Usage Rules:**
- When creating tasks for Nathan, set Owner = `Nathan`, Status = `To Do`
- When creating tasks for Claude to execute, set Owner = `Claude`, Status = `In Progress`
- Always link to Project when the task belongs to an active project
- Completed Date must be set when marking Status = `Done` — do not leave it empty
- Never write to Created or Last Edited — read only

**Write example:**
```json
{
  "parent": {"data_source_id": "cc91430b-f1b0-486b-afdf-fccd26dd7433"},
  "properties": {
    "Task": {"title": [{"text": {"content": "Push pipedrive-intelligence SKILL.md to GitHub"}}]},
    "Status": {"select": {"name": "To Do"}},
    "Owner": {"select": {"name": "Nathan"}},
    "Phase": {"select": {"name": "Deploy"}},
    "date:Due Date:start": "2026-04-25",
    "date:Due Date:is_datetime": 0
  }
}
```

---

### 4.2 Projects

**Data Source:** `collection://f290238d-1616-45f2-a694-f8710f036bc4`
**Purpose:** Every major ETKM initiative. The Tasks database relates back to this.
**Note:** Full schema not yet retrieved via live call — run `notion-fetch` on database ID `e1e5d9e9-6e15-4e7a-b5aa-fd8b92097da6` before writing to this database.

---

### 4.3 🛠️ ETKM Tools Registry

**Data Source:** `collection://03a4fe80-8d9a-4b53-bda4-4128207b79ce`
**Purpose:** Authoritative registry of every tool in the ETKM stack. 9 active tool entries. Claude checks this before building integrations.

| Property | Type | Values / Notes |
|---|---|---|
| Tool Name | title | The tool name |
| Status | select | `active` / `evaluating` / `deprecated` / `retired` |
| Category | select | `automation` / `AI` / `CRM` / `communication` / `design` / `storage` / `analytics` / `email` |
| Primary Surface | multi_select | `Chat` / `Cowork` / `Code` / `Agent` / `All` |
| Version in Use | text | Current version string |
| Deep Reference Page | url | URL to the tool's Deep Reference Page in Notion |
| Skill File | url | URL to the skill file in GitHub |
| Last Verified | date | When tool entry was last confirmed accurate |
| Open Issues | number | Count of unresolved issues |
| Stack Notes | rich_text | Operational notes, known gotchas |
| Last Edited | last_edited_time | Auto — read only |

**AI Usage Rules:**
- Always check this registry before building a new integration
- When a skill file is built and deployed, update the Skill File URL property
- When Last Verified is > 30 days old, flag in Sheriff Agent brief for review

---

### 4.4 Content Hub

**Data Source:** `collection://093b4700-f05f-4e5b-bfc6-a0605f499c1b`
**Purpose:** Central database for all content pieces across blog, social, email, video.
**Note:** Run `notion-fetch` on `collection://093b4700-f05f-4e5b-bfc6-a0605f499c1b` to retrieve full schema before writing.

---

### 4.5 Social Media Calendar

**Data Source:** `collection://589dcd23-97f2-4959-8574-f7ea9c742cf1`
**Purpose:** 52-week PEACE content calendar. All social posts scheduled here.
**Note:** Two Social Media Calendar databases exist in the Content System. The primary active one is `collection://589dcd23-97f2-4959-8574-f7ea9c742cf1`. The secondary (`collection://42eb3bbc-99ae-4a2c-bb92-039a03165435`) is the older version — do not write to it.

---

### 4.6 Assets

**Data Source:** `collection://5381e8ec-1e5f-4588-b9cc-74107c176341`
**Purpose:** Catalog of all media files. Links to Google Drive folders, not file hosting.

---

### 4.7 Categories & Tags

**Data Source:** `collection://22366aac-1432-4971-8cd0-9f0f5247e76b`
**Purpose:** Central taxonomy. All content, assets, and campaigns relate to this. 36-tag taxonomy for the P6 Media Library.
**Rule:** Never create new tags via free-text on content records. Always relate to this database or add to multi_select options here first.

---

### 4.8 ETKM Blog Article Database

**Data Source:** `collection://0b46f054-5967-4d66-9090-35ef654e397f`
**Purpose:** 114-article WordPress database. Three-stage execution plan: audit → cleanup → gap map. WordPress ID property links back to WP REST API.

---

### 4.9 People & Organizations

**Data Source:** `collection://ca593219-63c9-4f91-8ee8-727df8a5efc9`
**Purpose:** Contacts, collaborators, vendors, partners. Not a CRM — that's Pipedrive. This is the operational contacts layer.

---

## SECTION 5 — MCP SURFACE DECISION TREE

Run this logic at the start of every Notion operation.

```
┌─ Is this an interactive Claude session (human present)?
│
├── YES → Use hosted MCP (mcp.notion.com)
│         Auth: OAuth (already connected in Claude.ai)
│         Tools available: see Section 6
│         Rate limit: 180 req/min general, 30 req/min search
│
└── NO  → Is this a headless/automated operation?
          (Sheriff Agent, n8n AI node, cron job)
          │
          └── YES → Use direct REST API
                    Auth: Bearer ntn_... (stored in n8n credentials)
                    Base: https://api.notion.com
                    Header: Notion-Version: 2025-09-03
                    Rate limit: 3 req/sec avg, ~10 burst

─────────────────────────────────────────────────────
BEFORE ANY WRITE — verify these two things:

1. Is the integration shared with this database?
   NO → Share it first. Otherwise: 404 object_not_found.

2. Is this the SOURCE database (not a linked view)?
   LINKED VIEW → API cannot query it. Find the source DB.
   SOURCE → Proceed.
─────────────────────────────────────────────────────
```

---

## SECTION 6 — MCP TOOL ROUTING

### When to Use Each Tool

| Tool | Use It For | Don't Use It For |
|---|---|---|
| `notion-fetch` | Reading page content, retrieving DB schema, getting data_source_id | Querying multiple rows |
| `notion-search` | Semantic search across workspace (requires Notion AI plan) | Structured filtered queries |
| `notion-query-database-view` | Querying pre-built views by URL (Business+ with AI) | Schema retrieval |
| `notion-create-pages` | Creating new records in any database, new pages anywhere | Updating existing records |
| `notion-update-page` | Updating properties or content on existing pages | Creating new records |
| `notion-move-pages` | Reorganizing pages in the hierarchy | Changing property values |
| `notion-duplicate-page` | Copying a page with its content | Template application (use template_id instead) |
| `notion-create-database` | Standing up a new database | Adding properties to existing DB |
| `notion-update-data-source` | Modifying schema — add/rename/delete properties | Updating individual page values |
| `notion-create-view` | Adding a new view to a database | Changing view settings |
| `notion-update-view` | Changing filters, sorts, grouping on a view | Creating new views |
| `notion-create-comment` | Adding comments to pages or blocks | Page content edits |
| `notion-get-comments` | Reading discussion threads | Property value reads |
| `notion-get-teams` | Listing teamspaces | |
| `notion-get-users` | Listing workspace members | |

### Pre-Write Protocol (Interactive Sessions)

Before any create or update operation in a Claude session:

1. Call `notion-fetch` on the target database to get current schema
2. Verify property names **exactly** — case sensitive, no trailing spaces
3. Confirm data_source_id from the `<data-source url="collection://...">` tag
4. Build the write payload from the live schema — never from memory
5. Execute write
6. Call `notion-fetch` on the created/updated page to verify

---

## SECTION 7 — API EXECUTION PATTERNS

### 7.1 Standard Query Pattern

```javascript
// Query with filter, sort, pagination
const response = await fetch(
  `https://api.notion.com/v1/data_sources/${DATA_SOURCE_ID}/query`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.NOTION_TOKEN}`,
      'Notion-Version': '2025-09-03',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      filter: {
        and: [
          { property: 'Status', select: { equals: 'In Progress' } },
          { property: 'Owner', select: { equals: 'Nathan' } }
        ]
      },
      sorts: [{ property: 'Due Date', direction: 'ascending' }],
      page_size: 100
    })
  }
);

// Paginate: check has_more, pass next_cursor as start_cursor
```

### 7.2 Upsert Pattern (Required for All Sync Operations)

Never create without checking for duplicates first.

```javascript
// Step 1: Query for existing record by stable external ID
const existing = await queryDataSource(DATA_SOURCE_ID, {
  filter: {
    property: 'External Sync ID',
    rich_text: { equals: externalId }
  }
});

// Step 2: Create or update
if (existing.results.length === 0) {
  await createPage(DATA_SOURCE_ID, properties);
} else {
  await updatePage(existing.results[0].id, properties);
}
```

### 7.3 Rate Limit Handler (Mandatory on All Integrations)

```javascript
async function notionCall(fn, attempt = 0) {
  try {
    return await fn();
  } catch (e) {
    if (e.status === 429 && attempt < 5) {
      const retryAfter = parseInt(e.headers?.get?.('retry-after') || '2');
      const wait = (retryAfter * 1000) + (Math.random() * 500); // jitter
      await new Promise(r => setTimeout(r, wait));
      return notionCall(fn, attempt + 1);
    }
    throw e;
  }
}

// NEVER use Promise.all() for Notion API calls.
// Always sequential or p-limit(1) concurrency.
```

### 7.4 Rich Text Chunker (Required for Long Text)

```javascript
function toRichTextBlocks(text, maxChunkSize = 2000) {
  const chunks = [];
  for (let i = 0; i < text.length; i += maxChunkSize) {
    chunks.push({
      type: 'text',
      text: { content: text.slice(i, i + maxChunkSize) }
    });
  }
  return chunks;
}
// Max 2,000 chars per rich_text content object — enforced, not optional.
```

### 7.5 Append Block Children (Long Page Bodies)

```javascript
// Max 100 blocks per PATCH request
async function appendBlocksInBatches(pageId, blocks) {
  const BATCH_SIZE = 100;
  for (let i = 0; i < blocks.length; i += BATCH_SIZE) {
    const batch = blocks.slice(i, i + BATCH_SIZE);
    await notionCall(() => fetch(
      `https://api.notion.com/v1/blocks/${pageId}/children`,
      {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${process.env.NOTION_TOKEN}`,
          'Notion-Version': '2025-09-03',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ children: batch })
      }
    ));
    // Wait 350ms between batches to stay under rate limit
    await new Promise(r => setTimeout(r, 350));
  }
}
```

### 7.6 Relation Write Timing Rule

When creating a related page and immediately writing a relation property pointing to it:

```javascript
// Step 1: Create the related page
const relatedPage = await createPage(...);

// Step 2: WAIT — Notion's relation index needs to propagate
await new Promise(r => setTimeout(r, 1000)); // 1 second minimum

// Step 3: Now write the relation
await updatePage(mainPageId, {
  'Related': { relation: [{ id: relatedPage.id }] }
});
```

Skipping this wait causes intermittent relation write failures that don't surface a useful error.

---

## SECTION 8 — n8n INTEGRATION RULES

### 8.1 n8n Node vs. HTTP Request — When to Use Each

| Use n8n Notion Node | Use HTTP Request Node |
|---|---|
| Standard CRUD: create page, get page, update simple properties | Writing `relation` properties |
| Trigger: page added, page updated (polling) | Writing `status` type properties |
| Get database, search database | Any call requiring `Notion-Version: 2025-09-03` header |
| Low-risk reads | Post-2025-09-03 data_source queries |
| | Bulk operations needing precise rate control |

### 8.2 HTTP Request Node Configuration (Mandatory)

```
Method: POST (for queries) / PATCH (for updates) / GET (for reads)
URL: https://api.notion.com/v1/data_sources/{{$env.NOTION_DATA_SOURCE_ID}}/query
Headers:
  Authorization: Bearer {{$credentials.notionApi.apiKey}}
  Notion-Version: 2025-09-03
  Content-Type: application/json
```

**Always store the `Notion-Version` header explicitly.** The n8n Notion node uses an older default version — HTTP Request node gives you control.

### 8.3 The Webhook Bridge Pattern (Preferred Over Polling)

**Old pattern (polling):** n8n cron trigger → query Notion for recent changes.
**New pattern (webhook bridge):** Notion native automation → Send webhook → n8n Webhook trigger node.

Benefits: real-time, no polling overhead, no duplicate processing.

**Setup:**
1. In Notion database: Settings → Automations → Add automation
2. Trigger: `Property edited → Status` (or whichever property)
3. Action: `Send webhook` → URL = n8n webhook URL
4. In n8n: Webhook trigger node → processes the Notion payload

**Webhook payload** contains basic page metadata — not full page content. Follow with a `notion-fetch` or HTTP GET to retrieve full record if needed.

### 8.4 n8n Node Configuration Rules

- **Simplify toggle:** Always OFF on Notion trigger nodes when downstream nodes need raw data structure
- **Continue on Fail:** Always ON for every Notion node in production workflows
- **Error Workflow:** Connect every Notion workflow to an Error Workflow that logs to the ETKM Tasks database (Owner: Nathan, Status: Blocked, Phase: Other)
- **Credential assignment:** After deploying migrated workflows, manually assign Notion API credential in n8n UI — it does not carry over automatically
- **Test in staging first:** Clone the workflow, point it at a test database, validate behavior before touching production

### 8.5 Two-Way Sync Guard

Never build two-way automations between Notion and any other system without a sync-source guard. Circular automations cause infinite loops.

```
Required: Add a hidden property "Sync Source" (select) to every synced database.
Options: Notion / Pipedrive / WordPress / External

Rule: Only the owning system's webhook is allowed to write to the record.
      The mirror system reads only.
      On conflict: Sync Source = owning system wins.
```

### 8.6 Known n8n + Notion Gotchas

| Issue | Cause | Fix |
|---|---|---|
| Workflow breaks after someone adds a second data source | Old n8n node uses database_id, not data_source_id | Switch to HTTP Request node with explicit data_source_id |
| Relation write fails intermittently | Index propagation lag | Add 1-second wait after creating related page |
| Status property not writable via n8n node | n8n node doesn't support `status` type cleanly | Use HTTP Request node with `"status": {"name": "value"}` |
| Trigger fires but downstream node returns empty | `Simplify` toggle is ON | Turn Simplify OFF |
| Workflow halts on one bad row | `Continue on Fail` is OFF | Turn it ON, connect to error workflow |

---

## SECTION 9 — NATIVE NOTION AUTOMATION ARCHITECTURE

### 9.1 What Notion Automations Can Do

**Triggers available:**
- Page added to database
- Property edited (any, or specific property + specific value for select/multi_select/status)

**Actions available:**
1. Edit property on the triggering page
2. Add a page to another database (with pre-filled properties)
3. Edit pages in another database (filtered)
4. Send notification to Notion users (up to 20)
5. Send Gmail (subject to Gmail daily limits)
6. **Send webhook** → this is the n8n bridge (see Section 8.3)
7. Send Slack notification
8. Define variables (reusable in subsequent actions in the same automation)

**Compound triggers:** AND/OR combinations supported.
**Multiple actions per automation:** Supported.

### 9.2 ETKM Automation Targets

| Trigger | Action | Purpose |
|---|---|---|
| Task Status → Done | Set Completed Date = today | Auto-timestamp task completion |
| Blog Article Status → Ready | Send webhook → n8n → WordPress draft | Content pipeline trigger |
| Blog Article Status → Published | Set Published Date = today, notify Nathan | Publication confirmation |
| Tools Registry Last Verified > 30 days | Send notification to Nathan | Maintenance reminder |
| Task Status → Blocked | Send notification to Nathan | Unblock signal |

### 9.3 Automation Limitations (Hard Rules)

- Automations do NOT fire on pages with restricted access — share the database with the integration first
- Text property changes cannot filter on specific values — only "any change." Use select/status for trigger-specific logic
- Recurring template automations do NOT trigger database automations
- Button click automations DO trigger database automations — use buttons as manual triggers
- Free plan can use automations but cannot edit them — must be on Plus or higher to modify

---

## SECTION 10 — DASHBOARD BUILD PATTERNS

### 10.1 Two Dashboard Approaches

**Dashboard View (Notion 2.52+):**
- Pure data, multi-widget, tabs
- Cannot contain content blocks (callouts, headings) between widgets
- Best for: executive KPI view, data-dense operations overview
- Build sequence: databases → views per database → dashboard assembles views

**Classic Linked-View Page:**
- Mix of narrative blocks + linked database views
- Full layout control (columns, callouts, toggles, buttons, embedded views)
- Best for: operational dashboards where context sits alongside data
- Performance rule: `Load Limit = 50` on every linked view, hide unused properties

### 10.2 ETKM Dashboard Targets

**Operations Dashboard (build next):**
- Enrollment numbers: Chart view from Projects/Enrollments
- Open leads: List view from Pipedrive sync table, Status = Active
- This week's sessions: Calendar view filtered to current week
- Nathan's open tasks: Board view of Tasks, Owner = Nathan, Status ≠ Done

**Content Dashboard:**
- Content pipeline: Board view of Content Hub by Status
- Publish calendar: Calendar view by Publish Date
- Asset registry: Gallery view of Assets

**Project Dashboard:**
- Active projects: Board view of Projects by Status
- Open tasks: Board view of Tasks by Phase, filtered to active projects
- Tools registry: Table view of Tools Registry, Status = active

### 10.3 Dashboard Performance Rules

- Every linked view: set Load Limit = 50
- Hide all properties not essential to the view
- Maximum 6–8 linked views per dashboard page before performance degrades
- No circular rollup dependencies — kills performance, hard to debug
- Segment databases by year when they exceed 5,000 rows (`Sessions 2025`, `Sessions 2026`)

---

## SECTION 11 — AI-SAFE SCHEMA STANDARDS

### 11.1 Property Naming Conventions

These rules make Claude's reads and writes reliable. Violating them causes `validation_error` or `property not found`.

| Rule | Correct | Wrong |
|---|---|---|
| Title case | `Due Date` | `due_date` / `DUE DATE` |
| No punctuation in names | `Is Active` | `Is Active?` / `Active:` |
| No trailing spaces | `Status` | `Status ` |
| No apostrophes | `Owners Name` | `Owner's Name` |
| No slashes | `Start End` | `Start/End` |
| Consistent capitalization | `In Progress` | `in progress` / `IN PROGRESS` |

### 11.2 Required Properties on Every Syncable Database

Add these to any database that n8n or the Claude API reads/writes:

| Property | Type | Purpose |
|---|---|---|
| External Sync ID | rich_text | Foreign system ID (Pipedrive deal ID, WP post ID, etc.) |
| Sync Source | select | Which system owns this record (Notion/Pipedrive/WordPress/External) |
| Last Synced | date | Timestamp of last successful sync — flags failures |

### 11.3 Required Views

Every database the API or MCP targets must have:
- **`API - Primary` view:** Minimal filter (e.g., Status ≠ Archived), shows only properties needed by integrations. n8n workflows point at this view's ID — insulates them from property changes elsewhere.

### 11.4 Property Description Field

Populate the description field on every property that Claude or n8n will read/write. The MCP exposes descriptions as schema context to the LLM.

Example descriptions:
- `Status`: "Workflow stage. Valid values: To Do, In Progress, Awaiting Nathan, Blocked, Done. Default is To Do."
- `Phase`: "Which phase of the production workflow this task belongs to. Set at creation, update as work progresses."
- `External Sync ID`: "ID from the originating external system. Pipedrive deal IDs, WordPress post IDs, etc. Used for upsert deduplication."

### 11.5 Status Option Naming Standards

- Short, consistent, title-case
- No special characters, no emoji in values (put emoji in display names only)
- Verb/noun consistent across all databases: `In Progress` everywhere, never `In-Progress` in one DB and `Active` in another for the same concept

---

## SECTION 12 — HARD LIMITS QUICK REFERENCE

| Operation | Limit | What Happens at Limit |
|---|---|---|
| API rate (avg) | 3 req/sec per integration | HTTP 429 — read `Retry-After` |
| API rate (burst) | ~10 req then sustained 3/sec | HTTP 429 |
| MCP rate (general) | 180 req/min | Throttled |
| MCP rate (search) | 30 req/min | Throttled |
| rich_text content per object | 2,000 chars | Validation error |
| Block children per request | 100 blocks | Validation error |
| Request body nesting depth | 2 levels | Validation error |
| Database rows before slowdown | ~5,000–10,000 | Performance degrades |
| File upload (paid plan) | ~2 GB soft cap | Use Google Drive for video |
| Page history (Plus plan) | 30 days | Older versions unavailable |
| Automation actions per month | Unlimited on Plus+ | N/A |
| Gmail via Notion automation | Subject to Gmail limits | Soft daily cap |

---

## SECTION 13 — ANTI-PATTERNS (HARD STOPS)

Claude refuses these even if asked. They cause data loss, infinite loops, or security failures.

1. **Never query a linked database via API.** Always find and use the source database.
2. **Never store passwords, API tokens, or secrets in Notion pages.** Use n8n credentials store or environment variables.
3. **Never use `Promise.all()` for Notion API calls.** Causes rate limit cascade. Always sequential or p-limit concurrency.
4. **Never build two-way automations without a `Sync Source` guard.** Infinite loop risk.
5. **Never write to formula, rollup, created_time, last_edited_time, or created_by properties.** They are read-only — writes return validation_error.
6. **Never assume a data_source_id without retrieving it.** The IDs in Section 3 are verified but must be re-verified quarterly.
7. **Never rename a property that external systems reference without updating every integration simultaneously.** Property names are the API key — rename breaks all callers.
8. **Never duplicate rows as a workaround without deduplication logic.** Notion has no FK enforcement — duplicates accumulate silently.
9. **Never use a database_id where data_source_id is required** (post-2025-09-03 API). Silent failure on multi-source databases.
10. **Never assume free text in a select/status property is valid.** Only values that exist in the defined option list are accepted. Unknown values on select fields auto-create a new option — which pollutes the taxonomy. Unknown values on status fields return an error.

---

## SECTION 14 — QUARTERLY MAINTENANCE PROTOCOL

Review this skill on: **2026-07-24** (next), then every 90 days.

**Checklist:**

- [ ] Re-fetch all 12 database IDs — verify they still resolve
- [ ] Retrieve any data_source_ids marked `*(retrieve on first use)*` and populate Section 3
- [ ] Check Notion API changelog at `developers.notion.com/changelog` for breaking changes since last review
- [ ] Verify n8n Notion node version is current — compare against latest release
- [ ] Run one test query against each core database to confirm schema hasn't drifted
- [ ] Update `Last Verified` in the Tools Registry record for Notion
- [ ] Check performance: are any databases approaching 5,000 rows? Plan segmentation if so
- [ ] Review automation inventory: any automations firing unexpectedly or not at all?
- [ ] Confirm `API - Primary` views exist and have correct filters on all 8+ active databases
- [ ] Update this skill's `updated` date and increment version

**Version increment rules:**
- Minor fix (typo, URL update): increment patch (1.0 → 1.1)
- Schema change (new property, new database): increment minor (1.0 → 1.1)
- Breaking change (API version change, major restructure): increment major (1.0 → 2.0)

---

## SECTION 15 — KEY PAGE URLS (QUICK REFERENCE)

| Page | URL |
|---|---|
| ETKM Big Projects List | https://www.notion.so/323924c81673814da1b7f0fcee8b9772 |
| ETKM Content System | https://www.notion.so/302924c8167381238e3ae9e406bfdbf6 |
| n8n Deep Reference Page | https://www.notion.so/34b924c81673818484e6d1ce956f4b42 |
| Pipedrive Deep Reference Page | https://www.notion.so/34b924c8167381019e8ec47b0d89abfa |
| 🛠️ ETKM Tools Registry | https://www.notion.so/b72c1b3cee304ae9b31635ef4150100a |
| ETKM Tasks | https://www.notion.so/a5ef89dfba1648a097621d1338992bc9 |
| ETKM Operational Dashboards | https://www.notion.so/333924c8167381b5a00dd037d3127366 |
| Brand Intelligence Hub | https://www.notion.so/335924c8167381d39133e68b41e26c36 |
| AI Resources (root) | https://www.notion.so/30f924c8167380f095dbc64fa64f8f86 |
