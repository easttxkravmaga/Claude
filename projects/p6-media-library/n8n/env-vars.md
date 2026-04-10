# P6 Pipeline — n8n Environment Variables

Set these in n8n Settings → Variables before activating the workflow.

| Variable | Value | Where to Get It |
|---|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key | console.anthropic.com |

## Notion Database — Already Built

The ETKM Media Library database is live in Notion:

- **ID:** `9d79095f-e24a-4490-8fd5-42922196c58f`
- **Location:** Ai Resources → ETKM Operational Dashboards

No manual database setup required.

## n8n Credentials Required

1. **Google Drive OAuth2** — used by Drive trigger and download nodes
2. **Notion (Internal Integration)** — used by Notion create node
   - Create at: notion.so/my-integrations
   - Name it: `ETKM n8n Pipeline`
   - Grant the integration access to the `ETKM Media Library` database:
     open the database → `···` → Connections → Add connections → select your integration
