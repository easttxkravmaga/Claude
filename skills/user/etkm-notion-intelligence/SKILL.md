---
name: etkm-notion-intelligence
version: 1.1
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

**Version:** 1.1
**Last Updated:** 2026-04-24
**Changes from 1.0:** All 12 database IDs verified via live workspace fetch. Stub IDs replaced with real IDs. Full schemas added for ETKM Media Library, Audience Segments, and Nurture Sequences. Corrected P6 Media Library → ETKM Media Library. Section 4 now covers all 12 databases.
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

### Live Database and Data Source IDs (All Verified 2026-04-24)

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
| Blog Article Database | `13455c39-b650-4076-ad65-a4c8701dd378` | `collection://0b46f054-5967-4d66-9090-35ef654e397f` | 📰 |
| ETKM Media Library | `9d79095f-e24a-4490-8fd5-42922196c58f` | `collection://711e3a52-1604-4182-ae94-9d23a2960963` | 🎬 |
| Audience Segments | `d43e07c2-22df-42f6-a2a4-907fb007acba` | `collection://843f9f21-aa1c-45b6-a593-600430156d18` | 🎯 |
| Nurture Sequences | `c699d080-0035-4d58-8ef7-a6a88ad18675` | `collection://5e53329e-01e0-470a-b759-9e5999718d9e` | 📧 |

> All 12 database and data source IDs verified via live MCP fetch on 2026-04-24. No stubs remain.

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
│   └── Blog Article Database [database]
├── ETKM Operational Dashboards (333924c8-1673-81b5-a00d-d037d3127366)
│   └── ETKM Media Library [database]
├── Skill Reference Data (332924c8-1673-813d-8886-fbf703a73168)
│   ├── Audience Segments [database]
│   └── Nurture Sequences [database]
└── ETKM Tasks [database] (standalone under AI Resources)
```

---

## SECTION 4 — DATABASE SCHEMAS (All Live, Verified 2026-04-24)

### 4.1 ETKM Tasks

**Database ID:** `a5ef89df-ba16-48a0-9762-1d1338992bc9`
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
- Owner = `Nathan` + Status = `To Do` for tasks assigned to Nathan
- Owner = `Claude` + Status = `In Progress` for tasks Claude owns now
- Always link Project when the task belongs to an active project
- Set Completed Date when marking Status = `Done` — never leave it empty
- Never write to Created or Last Edited

**Write example (MCP `notion-create-pages`):**
```json
{
  "parent": {"data_source_id": "cc91430b-f1b0-486b-afdf-fccd26dd7433"},
  "properties": {
    "Task": "Push pipedrive-intelligence SKILL.md to GitHub",
    "Status": "To Do",
    "Owner": "Nathan",
    "Phase": "Deploy",
    "date:Due Date:start": "2026-04-25",
    "date:Due Date:is_datetime": 0
  }
}
```

---

### 4.2 Projects

**Database ID:** `e1e5d9e9-6e15-4e7a-b5aa-fd8b92097da6`
**Data Source:** `collection://f290238d-1616-45f2-a694-f8710f036bc4`
**Purpose:** Every major ETKM initiative. Tasks relate to this via the `Project` relation.
**Schema status:** Data source ID confirmed via Tasks relation reference. Full schema not yet retrieved — run `notion-fetch` on the database ID before writing properties beyond title and status.

---

### 4.3 🛠️ ETKM Tools Registry

**Database ID:** `b72c1b3c-ee30-4ae9-b316-35ef4150100a`
**Data Source:** `collection://03a4fe80-8d9a-4b53-bda4-4128207b79ce`
**Purpose:** Authoritative registry of every tool in the ETKM stack. Claude checks this before building integrations.

| Property | Type | Values / Notes |
|---|---|---|
| Tool Name | title | The tool name |
| Status | select | `active` / `evaluating` / `deprecated` / `retired` |
| Category | select | `automation` / `AI` / `CRM` / `communication` / `design` / `storage` / `analytics` / `email` |
| Primary Surface | multi_select | `Chat` / `Cowork` / `Code` / `Agent` / `All` |
| Version in Use | text | Current version string |
| Deep Reference Page | url | URL to the tool's Deep Reference Page in Notion |
| Skill File | url | URL to the skill file in GitHub |
| Last Verified | date | When this entry was last confirmed accurate |
| Open Issues | number | Count of unresolved issues |
| Stack Notes | rich_text | Operational notes, known gotchas |
| Last Edited | last_edited_time | Auto — read only |

**AI Usage Rules:**
- Check this registry before building any new integration
- When a skill file is deployed, update the `Skill File` URL property on that tool's record
- Flag any record where `Last Verified` is > 30 days old — surface in Sheriff Agent brief

---

### 4.4 Content Hub

**Database ID:** `69345a21-3d44-466f-8905-bfa99f97d3fb`
**Data Source:** `collection://093b4700-f05f-4e5b-bfc6-a0605f499c1b`
**Purpose:** Central database for all content pieces across blog, social, email, and video.
**Schema status:** Data source ID confirmed. Full schema not yet retrieved — run `notion-fetch` on the data source ID before writing.

---

### 4.5 Social Media Calendar

**Database ID:** `53e7a656-3fac-482b-9725-1a2c43a4c7f0`
**Data Source:** `collection://589dcd23-97f2-4959-8574-f7ea9c742cf1`
**Purpose:** 52-week PEACE content calendar. All social posts scheduled here.

**Critical:** Two Social Media Calendar databases exist in the Content System. Always use the primary:
- **Primary (use this):** `collection://589dcd23-97f2-4959-8574-f7ea9c742cf1`
- **Legacy (do not write to):** `collection://42eb3bbc-99ae-4a2c-bb92-039a03165435`

**Schema status:** Data source ID confirmed. Run `notion-fetch` on the data source ID before writing.

---

### 4.6 Assets

**Database ID:** `72dfe39a-4d78-451d-b658-67e233cba8d8`
**Data Source:** `collection://5381e8ec-1e5f-4588-b9cc-74107c176341`
**Purpose:** Catalog of all media files. Links to Google Drive folders — not file hosting.
**Schema status:** Run `notion-fetch` on the data source ID before writing.

---

### 4.7 Categories & Tags

**Database ID:** `98ffeef2-a44f-45d0-ab60-a3ae48d52ac0`
**Data Source:** `collection://22366aac-1432-4971-8cd0-9f0f5247e76b`
**Purpose:** Central taxonomy. All content, assets, and campaigns relate to this.
**Rule:** Never create new tags via free-text on content records. Always relate to this database or explicitly add to the multi_select options list first.

---

### 4.8 Blog Article Database

**Database ID:** `13455c39-b650-4076-ad65-a4c8701dd378`
**Data Source:** `collection://0b46f054-5967-4d66-9090-35ef654e397f`
**Purpose:** 114-article WordPress database. Three-stage plan: audit → cleanup → gap map. WordPress ID property links back to WP REST API for sync.
**Schema status:** Run `notion-fetch` on the data source ID before writing.

---

### 4.9 People & Organizations

**Database ID:** `342d3e39-af77-405f-9709-5873e9008584`
**Data Source:** `collection://ca593219-63c9-4f91-8ee8-727df8a5efc9`
**Purpose:** Contacts, collaborators, vendors, partners. Operational contacts layer — NOT a CRM. Pipedrive owns CRM.
**Schema status:** Run `notion-fetch` on the data source ID before writing.

---

### 4.10 ETKM Media Library (formerly P6)

**Database ID:** `9d79095f-e24a-4490-8fd5-42922196c58f`
**Data Source:** `collection://711e3a52-1604-4182-ae94-9d23a2960963`
**Purpose:** All ETKM visual assets — images, videos, graphics, screenshots. Links to Google Drive. 36-tag taxonomy. Used by the P6 intake pipeline.

| Property | Type | Values / Notes |
|---|---|---|
| Name | title | Asset name |
| Status | select | `Active` / `Archived` |
| Asset Type | select | `Image` / `Video` / `Graphic` / `Screenshot` |
| Source | select | `Drive` / `Canva` / `Event` / `Other` |
| Drive URL | url | Direct link to the file in Google Drive |
| Description | rich_text | What the asset shows |
| Notes | rich_text | Usage notes, restrictions |
| Date Added | created_time | Auto — read only |
| Content Use Cases | multi_select | `Social media post` / `Email header` / `Landing page hero` / `Print ad` / `PDF/lead magnet` / `Seminar promotion` / `Curriculum visual aide` / `Testimonial support` / `Event promotion` / `Website background` / `Ad creative` / `Course thumbnail` |
| Tags | multi_select | 36 options — see full list below |

**Full Tags taxonomy (36 tags):**
`training` / `demonstration` / `class` / `seminar` / `event` / `headshot` / `facility` / `equipment` / `group` / `individual` / `youth` / `adult` / `women` / `efc` / `social-ready` / `print-ready` / `web-ready` / `email-ready` / `testimonial-context` / `action-shot` / `portrait` / `environment` / `candid` / `posed` / `fight-back-etx` / `armed-citizen` / `youth-program` / `college-safety` / `private-lessons` / `open-enrollment` / `community-event` / `high-energy` / `calm-focus` / `community` / `instructional` / `real-world` / `confidence`

**AI Usage Rules:**
- Always set Drive URL when creating a new asset record
- Tags drive filtering for content production — apply all relevant tags at creation
- Never use tags outside the 36-tag taxonomy — this pollutes filtering
- `efc` tag = LE/military content. `armed-citizen` tag = civilian firearms content. Apply correctly.

---

### 4.11 Audience Segments

**Database ID:** `d43e07c2-22df-42f6-a2a4-907fb007acba`
**Data Source:** `collection://843f9f21-aa1c-45b6-a593-600430156d18`
**Purpose:** Intelligence database for all 14 ETKM audience segments. Feeds the StoryBrand Intelligence Engine and all segmented email, social, and ad copy work. One record per segment.

| Property | Type | Purpose |
|---|---|---|
| Segment Name | title | Segment display name (e.g., "Adult Women", "LE/Military/First Responders") |
| Segment Code | text | Short slug: `parents`, `leo`, `college-female`, etc. |
| Demographics | text | Who they are — age, role, situation |
| External Problem | text | What they face in the world |
| Internal Problem | text | How it makes them feel |
| Philosophical Problem | text | Why it is wrong — the deeper injustice |
| Pain Points | text | Specific fears and frustrations |
| Desired Transformation | text | What they want to become |
| Fear-Mindset-Skill-Drill | text | The four-part training frame for this segment |
| Story Arc Template | text | Before/after narrative structure |
| Hooks | text | Top 5 ready-to-use hooks |
| Headlines | text | Top 5 ready-to-use headlines |
| Email Subjects | text | Top 5 ready-to-use email subject lines |
| CTAs | text | Segment-specific calls to action |
| Objections and Responses | text | Common objections with responses |
| Sub-Persona Variants | text | Variations within this segment |
| Platform Notes | text | Facebook/Instagram/LinkedIn nuances |
| Person Arc Label | text | Matching Pipedrive person-level arc label name + ID |
| Deal Arc Label | text | Matching Pipedrive deal-level arc label name + ID |
| Person Type Labels | text | Pipedrive person-type labels for this segment |
| Related Behavioral Labels | text | Pipedrive behavioral/classification labels for this segment |

**AI Usage Rules:**
- This database is read-heavy — Claude queries it when generating segment-specific copy
- Never create duplicate segment records — 14 segments exist, one record each
- When generating copy, always fetch the target segment record first and use its fields directly
- The Pipedrive label fields (`Person Arc Label`, `Deal Arc Label`) are the cross-system link — use them when syncing segment intelligence back to CRM

---

### 4.12 Nurture Sequences

**Database ID:** `c699d080-0035-4d58-8ef7-a6a88ad18675`
**Data Source:** `collection://5e53329e-01e0-470a-b759-9e5999718d9e`
**Purpose:** Registry of all ETKM email nurture sequences. Maps each sequence to its trigger, timing, pipeline stage, and arc/segment.

| Property | Type | Values / Notes |
|---|---|---|
| Sequence Name | title | Sequence display name (e.g., "WF-001 Pre-Trial", "WF-002 Onboarding") |
| Status | select | `Live` / `Built Not Deployed` / `Planned` / `Retired` |
| Type | select | `Post-Download` / `Pre-Visit` / `Post-Seminar` / `Re-engagement` / `Onboarding` / `Retention` |
| Trigger | text | What starts the sequence (download, booking, deal stage move, etc.) |
| Timing Pattern | text | Day 0, Day 1, Day 3, Day 7, etc. |
| Total Emails | number | Count of emails in the sequence |
| Pipeline Stage | text | Which Pipedrive pipeline and stage this maps to |
| Arc or Segment | text | Which arcs or audience segments this sequence serves |
| Exit Conditions | text | What stops or branches the sequence |
| Email Details | text | Subject, purpose, and CTA for each email in order |

**Active sequences as of 2026-04-24:**
- WF-001 Pre-Trial (Status: Built, pending credential assignment)
- WF-002 Onboarding — 28 emails / 90 days (Status: Live)
- WF-003 CBLTAC Events — 10 emails (Status: Live, frozen during CBLTAC event)
- Nurture A — PDF Download
- Nurture B — Post-Seminar
- Nurture C — Pre-Visit
- Nurture D — Re-engagement

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

Before any create or update in a Claude session:

1. Call `notion-fetch` on the target database to confirm current schema
2. Verify property names **exactly** — case sensitive, no trailing spaces
3. Confirm data_source_id from the `<data-source url="collection://...">` tag
4. Build the write payload from live schema — never from memory alone
5. Execute write
6. Call `notion-fetch` on the created/updated page to verify

---

## SECTION 7 — API EXECUTION PATTERNS

### 7.1 Standard Query Pattern

```javascript
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

Never create without checking for an existing record first.

```javascript
const existing = await queryDataSource(DATA_SOURCE_ID, {
  filter: { property: 'External Sync ID', rich_text: { equals: externalId } }
});

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
    chunks.push({ type: 'text', text: { content: text.slice(i, i + maxChunkSize) } });
  }
  return chunks;
}
// Max 2,000 chars per rich_text content object — hard limit.
```

### 7.5 Append Block Children (Long Page Bodies)

```javascript
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
    await new Promise(r => setTimeout(r, 350)); // 350ms between batches
  }
}
// Max 100 blocks per PATCH request — hard limit.
```

### 7.6 Relation Write Timing Rule

```javascript
const relatedPage = await createPage(...);
await new Promise(r => setTimeout(r, 1000)); // 1 second — relation index propagation
await updatePage(mainPageId, {
  'Related': { relation: [{ id: relatedPage.id }] }
});
```

Skipping this wait causes intermittent relation write failures with no useful error message.

---

## SECTION 8 — n8n INTEGRATION RULES

### 8.1 n8n Node vs. HTTP Request Node

| Use n8n Notion Node | Use HTTP Request Node |
|---|---|
| Standard CRUD: create page, get page, update simple text/number/select properties | Writing `relation` properties |
| Trigger: page added, page updated (polling) | Writing `status` type properties |
| Get database, search database | Any call requiring explicit `Notion-Version: 2025-09-03` header |
| Low-risk reads where schema is stable | Post-2025-09-03 data_source queries |
| | Bulk operations needing precise rate control |

### 8.2 HTTP Request Node Configuration

```
Method: POST (queries) / PATCH (updates) / GET (reads)
URL: https://api.notion.com/v1/data_sources/{{$env.NOTION_DATA_SOURCE_ID}}/query
Headers:
  Authorization: Bearer {{$credentials.notionApi.apiKey}}
  Notion-Version: 2025-09-03
  Content-Type: application/json
```

Always set `Notion-Version` header explicitly — the n8n Notion node uses an older default.

### 8.3 The Webhook Bridge Pattern (Preferred Over Polling)

Replace polling with Notion's native automation webhook action:

1. In Notion database: Settings → Automations → Add automation
2. Trigger: `Property edited → Status` (or specific property)
3. Action: `Send webhook` → paste n8n Webhook trigger URL
4. In n8n: Webhook trigger node receives the payload

Webhook payload is sparse (page metadata only). Follow with an HTTP GET to retrieve the full record when needed.

### 8.4 n8n Node Configuration Rules

- **Simplify toggle:** OFF on all Notion trigger nodes when downstream nodes need raw structure
- **Continue on Fail:** ON for every Notion node in production workflows
- **Error Workflow:** Every Notion workflow connects to an Error Workflow that creates a task in ETKM Tasks (Owner: Nathan, Status: Blocked, Phase: Other)
- **Credentials:** After deploying a migrated workflow, manually assign Notion API credential in n8n UI — does not carry over automatically
- **Test in staging:** Clone the workflow, point at a test database, validate before touching production

### 8.5 Two-Way Sync Guard

Every database involved in bidirectional sync requires a `Sync Source` property:

```
Property name: Sync Source
Type: select
Options: Notion / Pipedrive / WordPress / External

Rule: Only the owning system's webhook writes to the record.
      Mirror system reads only.
      On conflict: Sync Source = owner wins.
```

No exceptions. Bidirectional automation without this guard creates infinite loops.

### 8.6 Known n8n + Notion Gotchas

| Issue | Cause | Fix |
|---|---|---|
| Workflow breaks after adding a second data source | Old node uses database_id, not data_source_id | Switch to HTTP Request node with explicit data_source_id |
| Relation write fails intermittently | Index propagation lag | 1-second wait after creating related page |
| Status property not writable via n8n node | n8n node doesn't support `status` type cleanly | HTTP Request node with `"status": {"name": "value"}` |
| Trigger fires but downstream node returns empty | `Simplify` toggle is ON | Turn Simplify OFF |
| Workflow halts on one bad row | `Continue on Fail` is OFF | Turn it ON, connect error workflow |

---

## SECTION 9 — NATIVE NOTION AUTOMATION ARCHITECTURE

### 9.1 What Notion Automations Can Do

**Triggers:**
- Page added to database
- Property edited (any property, or specific property + specific value for select/multi_select/status)
- Compound AND/OR trigger logic supported

**Actions (multiple per automation supported):**
1. Edit property on the triggering page
2. Add a page to another database (with pre-filled properties)
3. Edit pages in another database (filtered)
4. Send notification to up to 20 Notion users
5. Send Gmail (subject to Gmail daily limits)
6. **Send webhook** → the n8n bridge
7. Send Slack notification
8. Define variables (reusable across actions in the same automation)

### 9.2 ETKM Automation Targets

| Trigger | Action | Purpose |
|---|---|---|
| Task Status → Done | Set Completed Date = today | Auto-timestamp completion |
| Blog Article Status → Ready | Send webhook → n8n → WordPress draft | Content pipeline |
| Blog Article Status → Published | Set Published Date = today, notify Nathan | Publication confirmation |
| Tools Registry Last Verified > 30 days | Notify Nathan | Maintenance trigger |
| Task Status → Blocked | Notify Nathan | Unblock signal |

### 9.3 Automation Hard Limits

- Do NOT fire on pages with restricted access — share the database with the integration first
- Text property changes cannot filter on specific values — only "any change." Use select/status for trigger-specific conditions
- Recurring template automations do NOT trigger database automations
- Button click automations DO trigger database automations — use buttons as manual triggers
- Free plan can use but cannot edit automations — Plus or higher required to modify

---

## SECTION 10 — DASHBOARD BUILD PATTERNS

### 10.1 Two Approaches

**Dashboard View (Notion 2.52+):**
- Pure data widgets, tabbed layout
- Cannot contain callouts, headings, or text blocks between widgets
- Best for: executive KPI view, dense multi-database data overview
- Build sequence: databases first → views per database → Dashboard assembles views

**Classic Linked-View Page:**
- Mix of callout zones, toggles, buttons, and linked database views
- Full layout control via columns
- Best for: operational dashboards where context and data appear together
- Performance rule: Load Limit = 50 on every linked view, hide unused properties

### 10.2 ETKM Dashboard Targets

**Operations Dashboard:**
- Enrollment chart (Chart view from Projects)
- Open leads list (Pipedrive sync, Status = Active)
- This week's sessions (Calendar view, current week filter)
- Nathan's open tasks (Board view of Tasks, Owner = Nathan, Status ≠ Done)

**Content Dashboard:**
- Content pipeline (Board view of Content Hub by Status)
- Publish calendar (Calendar view by Publish Date)
- Asset registry (Gallery view of ETKM Media Library)

**Project Dashboard:**
- Active projects (Board view of Projects by Status)
- Open tasks by phase (Board view of Tasks)
- Tools registry (Table view, Status = active)

### 10.3 Performance Rules

- Load Limit = 50 on every linked database view
- Hide all properties not essential to that specific view
- Max 6–8 linked views per dashboard page
- No circular rollup dependencies
- Segment databases by year at 5,000 rows (e.g., `Sessions 2025`, `Sessions 2026`)

---

## SECTION 11 — AI-SAFE SCHEMA STANDARDS

### 11.1 Property Naming Conventions

| Rule | Correct | Wrong |
|---|---|---|
| Title case | `Due Date` | `due_date` / `DUE DATE` |
| No punctuation | `Is Active` | `Is Active?` / `Active:` |
| No trailing spaces | `Status` | `Status ` |
| No apostrophes | `Owners Name` | `Owner's Name` |
| No slashes | `Start End` | `Start/End` |
| Consistent capitalization | `In Progress` | `in progress` / `IN PROGRESS` |

Violations cause `validation_error` or silent `property not found` failures.

### 11.2 Required Properties on Every Syncable Database

| Property | Type | Purpose |
|---|---|---|
| External Sync ID | rich_text | Foreign system ID (Pipedrive deal ID, WP post ID, etc.) |
| Sync Source | select | Owning system: Notion / Pipedrive / WordPress / External |
| Last Synced | date | Timestamp of last successful sync — detects failures |

### 11.3 Required Views

Every database that the API or MCP targets must have an **`API - Primary` view:**
- Minimal stable filter (e.g., Status ≠ Archived)
- Shows only the properties integrations need
- n8n workflows reference this view's ID — insulates them from schema changes elsewhere

### 11.4 Property Descriptions

Populate the description field on every property Claude or n8n reads/writes. The MCP exposes descriptions as schema context. Examples:

- `Status`: "Workflow stage. Valid values: To Do, In Progress, Awaiting Nathan, Blocked, Done. Default: To Do."
- `External Sync ID`: "ID from the originating external system. Pipedrive deal IDs, WordPress post IDs. Used for upsert deduplication."
- `Sync Source`: "Which system owns this record. Only the owning system's webhook may write to it."

### 11.5 Status Option Standards

- Short, title-case, no special characters, no emoji in values
- Consistent across all databases: `In Progress` everywhere, never `in-progress` in one DB and `Active` in another for the same concept

---

## SECTION 12 — HARD LIMITS QUICK REFERENCE

| Operation | Limit | Behavior at Limit |
|---|---|---|
| API rate (avg) | 3 req/sec per integration | HTTP 429 — read `Retry-After` |
| API rate (burst) | ~10 req, then sustained 3/sec | HTTP 429 |
| MCP rate (general) | 180 req/min | Throttled |
| MCP rate (search) | 30 req/min | Throttled |
| rich_text content per object | 2,000 chars | Validation error |
| Block children per request | 100 blocks | Validation error |
| Request body nesting depth | 2 levels | Validation error |
| Database rows before slowdown | ~5,000–10,000 | Performance degrades |
| File upload (paid plan) | ~2 GB soft cap | Use Google Drive for video |
| Page history (Plus plan) | 30 days | Older versions unavailable |
| Gmail via Notion automation | Subject to Gmail daily limits | Soft cap |

---

## SECTION 13 — ANTI-PATTERNS (HARD STOPS)

Claude refuses these regardless of what is asked. Each one causes data loss, infinite loops, or security failure.

1. **Never query a linked database via API.** Always find and use the source database.
2. **Never store passwords, API tokens, or secrets in Notion pages.** Use n8n credentials store or environment variables.
3. **Never use `Promise.all()` for Notion API calls.** Rate limit cascade. Use sequential or p-limit(1).
4. **Never build two-way automations without a `Sync Source` guard.** Infinite loop risk.
5. **Never write to formula, rollup, created_time, last_edited_time, or created_by properties.** Read-only — writes return validation_error.
6. **Never use a database_id where data_source_id is required.** Silent failure on multi-source databases.
7. **Never rename a property that external systems reference without updating every integration simultaneously.** Property names are the API key.
8. **Never duplicate rows as a workaround without deduplication logic.** No FK enforcement — duplicates accumulate silently.
9. **Never create tags via free-text on content records.** Always relate to Categories & Tags DB or explicitly add to the option list first.
10. **Never assume free text in a select/status property is a valid value.** Unknown select values auto-create a new option — polluting the taxonomy. Unknown status values return an error.

---

## SECTION 14 — QUARTERLY MAINTENANCE PROTOCOL

**Next review:** 2026-07-24. Then every 90 days.

- [ ] Re-fetch all 12 database IDs — verify they still resolve
- [ ] Check Notion API changelog at `developers.notion.com/changelog` for breaking changes
- [ ] Verify n8n Notion node version is current
- [ ] Run one test query against each core database to confirm schema hasn't drifted
- [ ] Update `Last Verified` in the Tools Registry entry for Notion
- [ ] Check performance: any database approaching 5,000 rows? Plan segmentation
- [ ] Review automation inventory — any firing unexpectedly or silently failing?
- [ ] Confirm `API - Primary` views exist on all 12 databases
- [ ] Update this skill's `updated` date and increment version

**Version rules:**
- Typo or URL fix: patch (1.1 → 1.2)
- New/changed property or database: minor (1.1 → 1.2)
- Breaking API change or major restructure: major (1.x → 2.0)

---

## SECTION 15 — KEY PAGE URLS (QUICK REFERENCE)

| Page | URL |
|---|---|
| AI Resources (root) | https://www.notion.so/30f924c8167380f095dbc64fa64f8f86 |
| ETKM Big Projects List | https://www.notion.so/323924c81673814da1b7f0fcee8b9772 |
| ETKM Content System | https://www.notion.so/302924c8167381238e3ae9e406bfdbf6 |
| ETKM Operational Dashboards | https://www.notion.so/333924c8167381b5a00dd037d3127366 |
| Skill Reference Data | https://www.notion.so/332924c81673813d8886fbf703a73168 |
| 🛠️ ETKM Tools Registry | https://www.notion.so/b72c1b3cee304ae9b31635ef4150100a |
| ETKM Tasks | https://www.notion.so/a5ef89dfba1648a097621d1338992bc9 |
| n8n Deep Reference Page | https://www.notion.so/34b924c81673818484e6d1ce956f4b42 |
| Pipedrive Deep Reference Page | https://www.notion.so/34b924c8167381019e8ec47b0d89abfa |
| Brand Intelligence Hub | https://www.notion.so/335924c8167381d39133e68b41e26c36 |
