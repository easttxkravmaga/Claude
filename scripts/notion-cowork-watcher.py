"""
ETKM Notion Cowork Watcher
Polls the Notion Todo List every 15 minutes.
When a task has Cowork = checked AND Status != Done,
it creates a briefing .md file in Google Drive /ETKM-AI/Briefings/

Deploy on Railway as a cron job or always-on worker.
Required env vars:
  NOTION_TOKEN         — Notion Internal Integration Token
  GOOGLE_SA_CREDS      — Google Service Account JSON (base64 encoded)
  GOOGLE_DRIVE_FOLDER  — Google Drive folder ID for /ETKM-AI/Briefings/
"""

import os
import json
import base64
import time
import logging
from datetime import datetime, timezone

import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger("cowork-watcher")

# ── Config ────────────────────────────────────────────────────────────────────
NOTION_TOKEN        = os.environ["NOTION_TOKEN"]
NOTION_DB_ID        = "2fd924c8-1673-800b-83e0-000b19433106"   # Todo List data source
GOOGLE_SA_CREDS_B64 = os.environ["GOOGLE_SA_CREDS"]
BRIEFINGS_FOLDER_ID = os.environ["GOOGLE_DRIVE_FOLDER"]
POLL_INTERVAL_SEC   = int(os.getenv("POLL_INTERVAL_SEC", "900"))  # 15 min default

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# Track already-briefed task IDs so we don't re-fire
briefed_ids: set[str] = set()

# ── Routing logic ─────────────────────────────────────────────────────────────
def route_task(task_name: str) -> str:
    name = task_name.lower()
    if any(k in name for k in ["copy", "email", "blog", "social", "content", "write", "draft", "post"]):
        return "Claude Chat"
    if any(k in name for k in ["pipedrive", "make", "zapier", "browser", "automation", "form", "upload"]):
        return "Manus"
    if any(k in name for k in ["script", "api", "github", "code", "deploy", "railway", "webhook"]):
        return "Claude Code"
    if any(k in name for k in ["research", "find", "search", "look up", "investigate"]):
        return "ChatGPT / Gemini"
    return "Claude Chat"  # default

# ── Notion polling ────────────────────────────────────────────────────────────
def get_cowork_tasks() -> list[dict]:
    """Query Notion for tasks where Cowork = checked and Status != Done."""
    url = f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query"
    payload = {
        "filter": {
            "and": [
                {"property": "Cowork", "checkbox": {"equals": True}},
                {"property": "Status", "status": {"does_not_equal": "Done"}}
            ]
        }
    }
    r = requests.post(url, headers=NOTION_HEADERS, json=payload, timeout=15)
    r.raise_for_status()
    return r.json().get("results", [])

def extract_task(page: dict) -> dict:
    props = page.get("properties", {})
    def text(prop): 
        items = prop.get("title") or prop.get("rich_text") or []
        return "".join(t.get("plain_text", "") for t in items)
    def select(prop): 
        s = prop.get("select") or prop.get("status") or {}
        return s.get("name", "")
    def date(prop):
        d = prop.get("date") or {}
        return d.get("start", "")

    return {
        "id":         page["id"],
        "url":        page["url"],
        "task_name":  text(props.get("Task name", {})),
        "status":     select(props.get("Status", {})),
        "priority":   select(props.get("Priority", {})),
        "due_date":   date(props.get("Due date", {})),
    }

# ── Google Drive ──────────────────────────────────────────────────────────────
def get_drive_service():
    creds_json = base64.b64decode(GOOGLE_SA_CREDS_B64).decode()
    creds_dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds, cache_discovery=False)

def create_briefing_file(task: dict) -> str:
    drive = get_drive_service()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    safe_name = "".join(c if c.isalnum() or c in " -_" else "" for c in task["task_name"]).strip()
    date_str  = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filename  = f"{safe_name} — Cowork Brief — {date_str}.md"
    route     = route_task(task["task_name"])

    content = f"""# COWORK BRIEF — AUTO-GENERATED
**Generated:** {now}

---

## Task
**{task['task_name']}**

| Field | Value |
|-------|-------|
| Priority | {task['priority'] or '—'} |
| Due Date | {task['due_date'] or '—'} |
| Status | {task['status']} |
| Notion URL | {task['url']} |

---

## Routing
**→ Assigned to: {route}**

| Task Type | Route To |
|-----------|----------|
| Copy / content / emails | Claude Chat |
| Browser / Pipedrive / Make.com | Manus |
| Scripts / API / GitHub | Claude Code |
| Research | ChatGPT / Gemini |

---

## Instructions
1. Execute the task above
2. When complete, create a receipt file in `/ETKM-AI/Status/`:
   - Filename: `{safe_name}-COMPLETE.md`
   - Include: what was done, any decisions needed from Nathan, links to outputs

---
*ETKM Cowork Watcher v1.0 — No Make.com required*
"""

    media = MediaInMemoryUpload(content.encode("utf-8"), mimetype="text/markdown", resumable=False)
    file_meta = {"name": filename, "parents": [BRIEFINGS_FOLDER_ID]}
    created = drive.files().create(body=file_meta, media_body=media, fields="id,webViewLink").execute()
    log.info(f"Created briefing: {filename} → {created.get('webViewLink')}")
    return created.get("webViewLink", "")

# ── Main loop ─────────────────────────────────────────────────────────────────
def run():
    log.info(f"Cowork Watcher started. Polling every {POLL_INTERVAL_SEC}s.")
    while True:
        try:
            tasks = get_cowork_tasks()
            log.info(f"Found {len(tasks)} cowork task(s).")
            for page in tasks:
                task = extract_task(page)
                if not task["task_name"]:
                    continue
                if task["id"] in briefed_ids:
                    log.info(f"Already briefed: {task['task_name']}")
                    continue
                link = create_briefing_file(task)
                briefed_ids.add(task["id"])
                log.info(f"Briefed: {task['task_name']} → {link}")
        except Exception as e:
            log.error(f"Error in poll cycle: {e}")
        time.sleep(POLL_INTERVAL_SEC)

if __name__ == "__main__":
    run()
