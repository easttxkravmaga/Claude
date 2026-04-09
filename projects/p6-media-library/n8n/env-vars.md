# P6 Pipeline — n8n Environment Variables

Set these in n8n Settings → Variables before activating the workflow.

| Variable | Value | Where to Get It |
|---|---|---|
| `GOOGLE_DRIVE_INGEST_FOLDER_ID` | ID of `/ETKM Media Ingest/` folder | From Drive URL after `/folders/` |
| `GOOGLE_DRIVE_LIBRARY_FOLDER_ID` | ID of `/ETKM Media Library/` folder | From Drive URL after `/folders/` |
| `CLOUD_RUN_BW_SERVICE_URL` | Cloud Run service URL (no trailing slash) | After deploying the microservice |
| `ANTHROPIC_API_KEY` | Anthropic API key | console.anthropic.com |
| `NOTION_MEDIA_LIBRARY_DB_ID` | Notion database ID | From database URL (32-char ID) |
| `N8N_ERROR_WEBHOOK_URL` | Optional: webhook for error alerts | Your Slack/email endpoint, or remove node |

## n8n Credentials Required

1. **Google Drive OAuth2** — used by Drive trigger, download, upload, delete nodes
2. **Notion (Internal Integration)** — used by Notion create node
   - Create at: notion.so/my-integrations
   - Grant integration access to the ETKM Media Library database

## Getting the Notion Database ID

From the database page URL:
```
https://www.notion.so/ETKM-Media-Library-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX?v=...
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                          This 32-character string is the DB ID
```

Format it with hyphens as: `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`
