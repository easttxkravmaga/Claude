# OPS-WF-009 — Cowork Watcher Deploy Notes

## What this is
A Railway worker script that replaces Make.com for the Notion → Google Drive
Cowork briefing automation. Polls Notion every 15 minutes. No browser needed.

## Railway setup
1. In Railway dashboard → ETKM project → add New Service → GitHub Repo
2. Point to `easttxkravmaga/Claude`, root dir `scripts/`
3. Start command: `pip install -r requirements-cowork.txt && python notion-cowork-watcher.py`
4. Add these env vars in Railway:

| Variable | Value |
|----------|-------|
| NOTION_TOKEN | (Notion internal integration token — see below) |
| GOOGLE_SA_CREDS | (base64-encoded service account JSON — see below) |
| GOOGLE_DRIVE_FOLDER | (Google Drive folder ID for /ETKM-AI/Briefings/) |
| POLL_INTERVAL_SEC | 900 (15 min — optional, this is default) |

## Getting NOTION_TOKEN
1. Go to https://www.notion.so/my-integrations
2. Click "New integration" → name it "ETKM Cowork Watcher"
3. Give it Read content permission on the workspace
4. Copy the Internal Integration Token
5. **Important:** Share the Todo List database with the integration in Notion

## Getting GOOGLE_SA_CREDS
1. Google Cloud Console → Create service account → "ETKM Cowork Watcher"
2. Give it "Google Drive API" access
3. Download JSON key
4. Base64 encode it: `base64 -w 0 service-account.json`
5. Paste that string as the env var value

## Getting GOOGLE_DRIVE_FOLDER
The folder ID is the last part of the /ETKM-AI/Briefings/ Google Drive URL.
Share that folder with the service account email.

## How it works
1. Every 15 min: queries Notion for tasks where Cowork=checked AND Status≠Done
2. For each new task: creates a .md briefing file in /ETKM-AI/Briefings/
3. Auto-routes to Claude Chat / Manus / Claude Code / ChatGPT based on task name keywords
4. Tracks already-briefed IDs in memory (resets on redeploy — safe, just re-briefs)

## Notion step
Add a Checkbox property named "Cowork" to the Todo List database.
Nathan checks it → watcher picks it up within 15 min → briefing lands in Drive.
