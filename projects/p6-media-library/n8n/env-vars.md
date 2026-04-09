# P6 Pipeline — n8n Environment Variables

Set these in n8n Settings → Variables before activating the workflow.

| Variable | Value | Where to Get It |
|---|---|---|
| `GOOGLE_DRIVE_INGEST_FOLDER_ID` | ID of `/ETKM Media Ingest/` folder | From Drive URL after `/folders/` |
| `GOOGLE_DRIVE_LIBRARY_FOLDER_ID` | ID of `/ETKM Media Library/` folder | From Drive URL after `/folders/` |
| `CLOUD_RUN_BW_SERVICE_URL` | Cloud Run service URL (no trailing slash) | After deploying the microservice |
| `ANTHROPIC_API_KEY` | Anthropic API key | console.anthropic.com |
| `NOTION_MEDIA_LIBRARY_DB_ID` | `6d54ec60-e833-4edc-86ca-2d8b18e3aeb2` | **Already created — use this ID** |

## Notion Database — Already Built

The ETKM Media Library database is live in Notion:

- **URL:** https://www.notion.so/6d54ec60e8334edc86ca2d8b18e3aeb2
- **ID:** `6d54ec60-e833-4edc-86ca-2d8b18e3aeb2`
- **Location:** Ai Resources → ETKM Operational Dashboards

Paste the ID above directly into n8n as `NOTION_MEDIA_LIBRARY_DB_ID`. No manual database setup required.

## n8n Credentials Required

1. **Google Drive OAuth2** — used by Drive trigger, download, upload, delete nodes
2. **Notion (Internal Integration)** — used by Notion create node
   - Create at: notion.so/my-integrations
   - Name it: `ETKM n8n Pipeline`
   - Grant the integration access to the `ETKM Media Library` database:
     open the database → `···` → Connections → Add connections → select your integration
