"""
ETKM Backend — Flask App + MCP Server
Deployed on Render. Serves as middleware between Pipedrive, Claude API,
and any AI agent via MCP protocol.
v1.3.0 — Dropbox integration for P6 Media Library intake
"""

import os
import json
import base64
import asyncio
import requests
from flask import Flask, request, jsonify, Response, redirect
from datetime import datetime

app = Flask(__name__)

# ─────────────────────────────────────────────
# Environment
# ─────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
PIPEDRIVE_API_KEY = os.environ.get("PIPEDRIVE_API_KEY", "")
GITHUB_TOKEN      = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO       = "easttxkravmaga/Claude"
GITHUB_BRANCH     = "main"
GITHUB_API_BASE   = f"https://api.github.com/repos/{GITHUB_REPO}/contents"
RENDER_API_KEY    = os.environ.get("RENDER_API_KEY", "")
RENDER_SERVICE_ID = os.environ.get("RENDER_SERVICE_ID", "")

# Dropbox OAuth
DROPBOX_APP_KEY      = os.environ.get("DROPBOX_APP_KEY", "")
DROPBOX_APP_SECRET   = os.environ.get("DROPBOX_APP_SECRET", "")
DROPBOX_REDIRECT_URI = "https://claude-r82h.onrender.com/oauth/callback"

# Dropbox tokens — loaded from env on startup, refreshed in memory
_dropbox_tokens = {
    "access_token":  os.environ.get("DROPBOX_ACCESS_TOKEN", ""),
    "refresh_token": os.environ.get("DROPBOX_REFRESH_TOKEN", ""),
    "expires_at":    0
}

# Notion Media Library
NOTION_MEDIA_DB_ID = "9d79095fe24a44908fd542922196c58f"
NOTION_TOKEN       = os.environ.get("NOTION_TOKEN", "")

# P6 Dropbox folder paths — Nathan creates these in Dropbox
P6_FOLDERS = {
    "Class Pics":           "/P6 Media Library/Class Pics",
    "Scenario Pics":        "/P6 Media Library/Scenario Pics",
    "Email Pics":           "/P6 Media Library/Email Pics",
    "Videos":               "/P6 Media Library/Videos",
    "Ready for Production": "/P6 Media Library/Ready for Production",
}


# ─────────────────────────────────────────────
# Health
# ─────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "etkm-backend",
        "version": "1.3.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "dropbox_auth": "configured" if _dropbox_tokens.get("refresh_token") else "not_configured"
    })


# ─────────────────────────────────────────────
# Dropbox OAuth Flow
# ─────────────────────────────────────────────
@app.route("/authorize", methods=["GET"])
def authorize():
    """Redirect to Dropbox consent screen."""
    if not DROPBOX_APP_KEY:
        return jsonify({"error": "DROPBOX_APP_KEY not set in environment"}), 500

    url = (
        f"https://www.dropbox.com/oauth2/authorize"
        f"?client_id={DROPBOX_APP_KEY}"
        f"&response_type=code"
        f"&token_access_type=offline"
        f"&redirect_uri={DROPBOX_REDIRECT_URI}"
    )
    return redirect(url)


@app.route("/oauth/callback", methods=["GET"])
def oauth_callback():
    """Exchange Dropbox code for refresh token and persist."""
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "No code in callback"}), 400

    resp = requests.post(
        "https://api.dropboxapi.com/oauth2/token",
        data={
            "code":          code,
            "grant_type":    "authorization_code",
            "client_id":     DROPBOX_APP_KEY,
            "client_secret": DROPBOX_APP_SECRET,
            "redirect_uri":  DROPBOX_REDIRECT_URI,
        },
        timeout=15
    )

    if resp.status_code != 200:
        return jsonify({"error": "Token exchange failed", "detail": resp.text}), 500

    tokens = resp.json()
    _dropbox_tokens["access_token"]  = tokens.get("access_token", "")
    _dropbox_tokens["refresh_token"] = tokens.get("refresh_token", "")
    _dropbox_tokens["expires_at"]    = datetime.utcnow().timestamp() + tokens.get("expires_in", 14400)

    # Persist to Render so tokens survive redeploys
    _persist_to_render("DROPBOX_ACCESS_TOKEN",  _dropbox_tokens["access_token"])
    _persist_to_render("DROPBOX_REFRESH_TOKEN", _dropbox_tokens["refresh_token"])

    # Create P6 folder structure in Dropbox
    _ensure_p6_folders()

    return jsonify({
        "status": "authorized",
        "message": "Dropbox access granted. P6 folders created. Pipeline is ready.",
        "folders_created": list(P6_FOLDERS.keys())
    })


def _persist_to_render(key: str, value: str):
    """Write env var to Render so tokens survive redeploys."""
    if not RENDER_API_KEY or not RENDER_SERVICE_ID:
        return
    try:
        requests.put(
            f"https://api.render.com/v1/services/{RENDER_SERVICE_ID}/env-vars",
            headers={
                "Authorization": f"Bearer {RENDER_API_KEY}",
                "Content-Type": "application/json"
            },
            json=[{"key": key, "value": value}],
            timeout=10
        )
    except Exception:
        pass


def _get_dropbox_token() -> str:
    """Return a valid Dropbox access token, refreshing if needed."""
    now = datetime.utcnow().timestamp()

    if _dropbox_tokens["access_token"] and _dropbox_tokens["expires_at"] > now + 300:
        return _dropbox_tokens["access_token"]

    refresh_token = _dropbox_tokens.get("refresh_token") or os.environ.get("DROPBOX_REFRESH_TOKEN", "")
    if not refresh_token:
        raise Exception("Dropbox not authorized. Visit https://claude-r82h.onrender.com/authorize")

    resp = requests.post(
        "https://api.dropboxapi.com/oauth2/token",
        data={
            "grant_type":    "refresh_token",
            "refresh_token": refresh_token,
            "client_id":     DROPBOX_APP_KEY,
            "client_secret": DROPBOX_APP_SECRET,
        },
        timeout=15
    )

    if resp.status_code != 200:
        raise Exception(f"Token refresh failed: {resp.text}")

    tokens = resp.json()
    _dropbox_tokens["access_token"] = tokens["access_token"]
    _dropbox_tokens["expires_at"]   = now + tokens.get("expires_in", 14400)
    _persist_to_render("DROPBOX_ACCESS_TOKEN", _dropbox_tokens["access_token"])

    return _dropbox_tokens["access_token"]


# ─────────────────────────────────────────────
# Dropbox Helpers
# ─────────────────────────────────────────────
def _ensure_p6_folders():
    """Create P6 folder structure in Dropbox if it doesn't exist."""
    token = _get_dropbox_token()
    for folder_path in P6_FOLDERS.values():
        try:
            requests.post(
                "https://api.dropboxapi.com/2/files/create_folder_v2",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={"path": folder_path, "autorename": False},
                timeout=10
            )
        except Exception:
            pass  # Folder may already exist — not fatal


def dropbox_list_folder(folder_path: str, folder_name: str) -> list:
    """List all files in a Dropbox folder."""
    token = _get_dropbox_token()
    files = []

    resp = requests.post(
        "https://api.dropboxapi.com/2/files/list_folder",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={"path": folder_path, "recursive": False, "limit": 500},
        timeout=15
    )

    if resp.status_code == 409:
        # Folder doesn't exist yet — return empty
        return []

    resp.raise_for_status()
    data = resp.json()

    for entry in data.get("entries", []):
        if entry.get(".tag") == "file":
            file_id = entry.get("id", "")
            # Build a shareable link
            link_url = f"https://www.dropbox.com/home{entry.get('path_display', '')}"
            files.append({
                "file_id":     file_id,
                "file_name":   entry.get("name", ""),
                "mime_type":   _guess_mime(entry.get("name", "")),
                "drive_url":   link_url,
                "folder_name": folder_name,
                "created":     entry.get("client_modified", ""),
                "path":        entry.get("path_display", ""),
            })

    # Handle pagination
    cursor = data.get("cursor")
    has_more = data.get("has_more", False)

    while has_more and cursor:
        cont_resp = requests.post(
            "https://api.dropboxapi.com/2/files/list_folder/continue",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={"cursor": cursor},
            timeout=15
        )
        cont_resp.raise_for_status()
        cont_data = cont_resp.json()

        for entry in cont_data.get("entries", []):
            if entry.get(".tag") == "file":
                file_id = entry.get("id", "")
                link_url = f"https://www.dropbox.com/home{entry.get('path_display', '')}"
                files.append({
                    "file_id":     file_id,
                    "file_name":   entry.get("name", ""),
                    "mime_type":   _guess_mime(entry.get("name", "")),
                    "drive_url":   link_url,
                    "folder_name": folder_name,
                    "created":     entry.get("client_modified", ""),
                    "path":        entry.get("path_display", ""),
                })

        cursor   = cont_data.get("cursor")
        has_more = cont_data.get("has_more", False)

    return files


def _guess_mime(filename: str) -> str:
    """Guess MIME type from file extension."""
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    video_exts = {"mp4", "mov", "avi", "mkv", "wmv", "m4v", "webm"}
    image_exts = {"jpg", "jpeg", "png", "gif", "webp", "bmp", "tiff", "heic", "svg"}
    if ext in video_exts:
        return "video/mp4"
    if ext in image_exts:
        return "image/jpeg"
    return "application/octet-stream"


# ─────────────────────────────────────────────
# Notion Helpers
# ─────────────────────────────────────────────
def notion_get_existing_drive_urls() -> set:
    """Pull all Drive/Dropbox URLs already in the Notion Media Library."""
    existing = set()
    has_more = True
    cursor   = None

    while has_more:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor

        resp = requests.post(
            f"https://api.notion.com/v1/databases/{NOTION_MEDIA_DB_ID}/query",
            headers={
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            },
            json=body,
            timeout=15
        )
        resp.raise_for_status()
        data = resp.json()

        for page in data.get("results", []):
            prop = page.get("properties", {}).get("Drive URL", {})
            url = prop.get("url")
            if url:
                existing.add(url)

        has_more = data.get("has_more", False)
        cursor   = data.get("next_cursor")

    return existing


def infer_asset_type(file_name: str, mime_type: str) -> str:
    name = file_name.lower()
    if "video" in mime_type:
        return "Video"
    if any(k in name for k in ["graphic", "logo", "banner", "flyer"]):
        return "Graphic"
    if any(k in name for k in ["screenshot", "screen"]):
        return "Screenshot"
    return "Image"


def infer_tags(file_name: str, folder_name: str) -> list:
    name = file_name.lower()
    tags = []

    folder_tags = {
        "Class Pics":           ["class", "training"],
        "Scenario Pics":        ["training", "demonstration", "real-world"],
        "Email Pics":           ["training", "demonstration", "email-ready"],
        "Videos":               ["training"],
        "Ready for Production": [],
    }
    tags.extend(folder_tags.get(folder_name, []))

    rules = [
        (["women", "woman"],                         ["women"]),
        (["youth", "kid", "teen"],                   ["youth"]),
        (["efc", "armed", "firearm", "gun"],         ["efc", "armed-citizen"]),
        (["fight-back", "fightback", "ipv"],         ["fight-back-etx"]),
        (["headshot"],                               ["headshot", "portrait"]),
        (["group"],                                  ["group"]),
        (["facility", "gym", "mat"],                 ["facility", "environment"]),
        (["seminar", "event"],                       ["event", "seminar"]),
        (["kick", "strike", "choke", "grab",
          "defense", "escape"],                      ["action-shot"]),
        (["parking", "street", "outdoor",
          "scenario"],                               ["real-world"]),
        (["portrait", "pose"],                       ["portrait", "posed"]),
        (["candid"],                                 ["candid"]),
        (["college"],                                ["college-safety"]),
        (["private"],                                ["private-lessons"]),
        (["community"],                              ["community", "community-event"]),
        (["instructor", "teach"],                    ["instructional"]),
        (["high-energy"],                            ["high-energy"]),
        (["calm", "focus"],                          ["calm-focus"]),
    ]

    for keywords, assigned_tags in rules:
        if any(k in name for k in keywords):
            tags.extend(assigned_tags)

    return list(dict.fromkeys(tags))


def infer_content_uses(file_name: str, folder_name: str) -> list:
    name = file_name.lower()
    uses = []

    if folder_name == "Email Pics":
        uses.append("Email header")
    if "social" in name:
        uses.append("Social media post")
    if "hero" in name:
        uses.append("Landing page hero")
    if any(k in name for k in ["seminar", "event"]):
        uses.extend(["Seminar promotion", "Event promotion"])
    if any(k in name for k in ["curriculum", "class"]):
        uses.append("Curriculum visual aide")
    if "testimonial" in name:
        uses.append("Testimonial support")
    if "print" in name:
        uses.append("Print ad")

    if not uses:
        if any(k in name for k in ["kick", "strike", "choke", "grab", "defense", "escape"]):
            uses.append("Social media post")
        elif any(k in name for k in ["facility", "gym", "mat", "outdoor"]):
            uses.extend(["Website background", "Landing page hero"])
        else:
            uses.append("Social media post")

    return list(dict.fromkeys(uses))


def notion_create_record(file: dict) -> dict:
    """Create a Notion Media Library record for a file."""
    asset_type   = infer_asset_type(file["file_name"], file["mime_type"])
    tags         = infer_tags(file["file_name"], file["folder_name"])
    content_uses = infer_content_uses(file["file_name"], file["folder_name"])
    description  = f"ETKM {asset_type.lower()} — {file['file_name'].rsplit('.', 1)[0].replace('-', ' ').replace('_', ' ')} ({file['folder_name']})."

    body = {
        "parent": {"database_id": NOTION_MEDIA_DB_ID},
        "properties": {
            "Name":             {"title": [{"text": {"content": file["file_name"]}}]},
            "Asset Type":       {"select": {"name": asset_type}},
            "Source":           {"select": {"name": "Drive"}},
            "Status":           {"select": {"name": "Active"}},
            "Drive URL":        {"url": file["drive_url"]},
            "Description":      {"rich_text": [{"text": {"content": description}}]},
            "Tags":             {"multi_select": [{"name": t} for t in tags]},
            "Content Use Cases":{"multi_select": [{"name": u} for u in content_uses]},
        }
    }

    resp = requests.post(
        "https://api.notion.com/v1/pages",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        },
        json=body,
        timeout=15
    )
    resp.raise_for_status()

    return {
        "file_name":    file["file_name"],
        "folder":       file["folder_name"],
        "asset_type":   asset_type,
        "tags":         tags,
        "content_uses": content_uses,
        "notion_url":   resp.json().get("url", "")
    }


# ─────────────────────────────────────────────
# Arc Classification
# ─────────────────────────────────────────────
ARC_KEYWORDS = {
    "Arc: Safety":    ["fear", "safety", "nervous", "walking alone", "parking lot",
                       "attacked", "unsafe", "threatened"],
    "Arc: Parent":    ["kids", "children", "family", "protect", "parent", "son", "daughter"],
    "Arc: Fitness":   ["fitness", "workout", "shape", "condition", "cardio", "athletic", "weight"],
    "Arc: LE/Mil":    ["military", "police", "security", "officer", "law enforcement",
                       "guard", "veteran", "tactical"],
    "Arc: Former MA": ["krav", "bjj", "jiu-jitsu", "karate", "trained",
                       "used to train", "martial arts", "belt"],
}

def classify_arc(qa_text: str) -> str:
    if not qa_text or qa_text.strip() == "":
        return "Arc: Default"
    lower = qa_text.lower()
    for arc, keywords in ARC_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            return arc
    return "Arc: Default"

def load_system_prompt() -> str:
    if GITHUB_TOKEN:
        try:
            url = f"{GITHUB_API_BASE}/prompts/arc-classification-system-prompt.md"
            resp = requests.get(url, headers={
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3.raw"
            }, timeout=5)
            if resp.status_code == 200:
                content = resp.text
                start = content.find("```\n") + 4
                end = content.find("\n```", start)
                if start > 4 and end > start:
                    return content[start:end]
        except Exception:
            pass
    return EMBEDDED_SYSTEM_PROMPT

EMBEDDED_SYSTEM_PROMPT = """You are the email copywriter for East Texas Krav Maga (ETKM), a reality-based self-defense training facility in Tyler, TX. Your job is to write personalized, conversion-focused email copy for prospects who have booked a free trial lesson.

Brand voice: Direct, warm, confident. Never aggressive. Short paragraphs. Plain language.
Prohibited words: mastery, dominate, destroy, killer, beast, crush, elite, warrior.
Format: Open with [person_first_name], — no "Dear" or "Hello". One CTA per email. No markdown.
Sign off: Nate Lundstrom / East Texas Krav Maga / (903) 590-0085 / etxkravmaga.com"""

@app.route("/classify-arc", methods=["POST"])
def classify_arc_endpoint():
    data = request.get_json(silent=True) or {}
    first_name   = data.get("first_name", "")
    email_number = data.get("email_number", 1)
    email_name   = data.get("email_name", "Booking Confirmation")
    qa_response  = data.get("qa_response", "")
    trial_date   = data.get("trial_date", "")
    trial_time   = data.get("trial_time", "")
    word_limit   = data.get("word_limit", 200)
    arc_type     = data.get("arc_type") or classify_arc(qa_response)

    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY not configured"}), 500

    user_message = f"""You are writing Email {email_number} — {email_name} — for East Texas Krav Maga.

PROSPECT CONTEXT:
- First name: {first_name}
- Arc type: {arc_type}
- Q&A response: {qa_response or "none"}
- Trial date: {trial_date or "not provided"}
- Trial time: {trial_time or "not provided"}

TASK:
Write Email {email_number} — {email_name} — exactly as specified in the ETKM email sequence.
Apply arc-type personalization if arc is not Arc: Default.
Follow all brand voice rules. Stay under {word_limit} words.
Sign off as Nate Lundstrom, East Texas Krav Maga, (903) 590-0085.

Return only the email — subject line first, blank line, then body. No preamble, no markdown."""

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 1024,
                "system": load_system_prompt(),
                "messages": [{"role": "user", "content": user_message}]
            },
            timeout=30
        )
        resp.raise_for_status()
        result = resp.json()
        return jsonify({
            "arc_type":     arc_type,
            "email_number": email_number,
            "email_name":   email_name,
            "email_copy":   result["content"][0]["text"],
            "model":        result.get("model"),
            "usage":        result.get("usage")
        })
    except requests.RequestException as e:
        return jsonify({"error": str(e), "arc_type": arc_type}), 502


# ─────────────────────────────────────────────
# Square Webhook → Pipedrive P4
# ─────────────────────────────────────────────
@app.route("/webhook/square", methods=["POST"])
def square_webhook():
    payload    = request.get_json(silent=True) or {}
    event_type = payload.get("type", "")
    if "payment.failed" not in event_type and "subscription" not in event_type.lower():
        return jsonify({"status": "ignored", "event_type": event_type}), 200
    data        = payload.get("data", {}).get("object", {})
    customer_id = (
        data.get("payment", {}).get("customer_id") or
        data.get("subscription", {}).get("customer_id") or
        "unknown"
    )
    return jsonify({
        "status":      "processed",
        "event_type":  event_type,
        "customer_id": customer_id,
        "action":      "move_to_p4_payment_due",
        "timestamp":   datetime.utcnow().isoformat() + "Z"
    })


# ─────────────────────────────────────────────
# Quiz Webhook → Pipedrive Person + Deal
# ─────────────────────────────────────────────
PIPEDRIVE_DOMAIN = "easttexaskravmaga.pipedrive.com"
PIPEDRIVE_BASE   = f"https://{PIPEDRIVE_DOMAIN}/api/v1"
OWNER_ID         = 21519696
PIPELINE_ID      = 1
STAGE_ID         = 1

QUIZ_FIELD_MAP = {
    "entry_reason":       "fd235088591c58d957cffaa27e7e85a804f73cea",
    "score":              "39051ebf8f2001d53d23c38ef85cb0552aa61180",
    "tier_name":          "0ce15f1cb1943e4017a9c98649fc377dcb2a9359",
    "identity_statement": "6aec18882b061254c804fb4f290344e2e0eb13a3",
    "vision_statement":   "d90d46159cb1a1487f112293424b35508149c9b8",
    "confidence_type":    "22f5e8d233b391e515df63c0dcbb0213f8d28c47",
    "primary_objection":  "9a28210fc9693618507d6a8c8020abd46e975fb0",
    "firearm_status":     "2d3de05af26cc6f8ee839d211d59ece76c51592f",
    "family_motivation":  "7abb9b8107081b6809141de27ae3b652db83582b",
    "must_protect":       "ec69ea4a4ffebd979e57d7a5de9880c4302333e7",
    "prior_incident":     "ce3267994db16a8e860eb75c578b5dba5dddea4e",
    "returning_pract":    "49bd6796dd47f83dae488a9d4d7d9e50c1e501f4",
    "auto_pdf":           "998e468cd3a69d1a7d0aed8e481384d1ef42e728",
    "bonus_pdf":          "6bf2526c2ff7fbfc6e4566f021aeff5ce31f8635",
    "urgency_flag":       "c6c7c5392f0eb4e5aa9dc9ea32fd42192fe2c3f7",
    "completed_date":     "db849879591eca16552aad77711175973f431a06",
}

FLAG_LABEL_MAP = {
    "HIGH_URGENCY": 99, "AWARENESS_GAP": 100, "AWARENESS_SUPPRESSED": 101,
    "NO_BASELINE_SKILLS_GAP": 102, "FALSE_CONFIDENCE_URGENT": 103,
    "HIGH_COACHABILITY": 104, "NO_ONSET_PLAN": 105, "NO_ACTION_PLAN": 106,
    "PRIOR_INCIDENT_CONSULT_CARE": 107, "REALITY_EXPOSURE_GAP": 108,
    "PARENT_FAMILY_ARC": 109, "MUST_PROTECT_CONSULT_FIRST": 110,
    "NO_FIREARM_ACT_AWARENESS": 111, "ACT_CONSULT_PRIORITY": 112,
    "ACT_CANDIDATE_ADVANCED": 113, "RETURNING_PRACTITIONER_PRIORITY": 114,
    "IDENTITY_BARRIER_OPEN_WITH_INCLUSION": 115, "PHYSICAL_FLAG_Q12_ACTIVE": 116,
    "COACHABILITY_NEEDS_WARMUP": 117, "ENCOURAGEMENT_PATH": 118,
    "ACT_CONFIRMED": 119, "FAMILY_ARC_CONFIRMED": 120, "FEAR_BARRIER_CONFIRMED": 121,
}

TIER_PDF_MAP = {
    "Unaware": "The Wake-Up Call Guide",
    "Aware of the Gap": "The Gap Assessment Guide",
    "Ready to Act": "The Action Readiness Guide",
    "Already Acting": "The Practitioner's Edge Guide",
}

def pipedrive_request(method, path, **kwargs):
    url    = f"{PIPEDRIVE_BASE}/{path}"
    params = kwargs.pop("params", {})
    params["api_token"] = PIPEDRIVE_API_KEY
    return requests.request(method, url, params=params, timeout=15, **kwargs)

@app.route("/quiz-webhook", methods=["POST"])
def quiz_webhook():
    payload    = request.get_json(silent=True) or {}
    first_name = payload.get("firstName", "")
    email      = payload.get("email", "")
    score      = payload.get("score", 0)
    tier_name  = payload.get("tierName", "")
    answers    = payload.get("answers", {})
    flags      = payload.get("flags", [])
    timestamp  = payload.get("timestamp", datetime.utcnow().isoformat() + "Z")

    if not email:
        return jsonify({"error": "email is required"}), 400
    if not PIPEDRIVE_API_KEY:
        return jsonify({"error": "PIPEDRIVE_API_KEY not configured"}), 500

    person_fields = {
        QUIZ_FIELD_MAP["entry_reason"]:       answers.get("entryReason", ""),
        QUIZ_FIELD_MAP["score"]:              str(score),
        QUIZ_FIELD_MAP["tier_name"]:          tier_name,
        QUIZ_FIELD_MAP["identity_statement"]: answers.get("identityStatement", ""),
        QUIZ_FIELD_MAP["vision_statement"]:   answers.get("visionStatement", ""),
        QUIZ_FIELD_MAP["confidence_type"]:    f"{answers.get('confidence', '')} / {answers.get('confidenceValidated', '')}",
        QUIZ_FIELD_MAP["primary_objection"]:  answers.get("objection", ""),
        QUIZ_FIELD_MAP["firearm_status"]:     f"{answers.get('firearmOwnership', '')} / {answers.get('carryStatus', '')}",
        QUIZ_FIELD_MAP["family_motivation"]:  answers.get("motivation", ""),
        QUIZ_FIELD_MAP["must_protect"]:       "Yes" if answers.get("motivation") == "public" else "No",
        QUIZ_FIELD_MAP["prior_incident"]:     answers.get("experience", ""),
        QUIZ_FIELD_MAP["returning_pract"]:    "Yes" if answers.get("objection") == "trained" else "No",
        QUIZ_FIELD_MAP["auto_pdf"]:           TIER_PDF_MAP.get(tier_name, ""),
        QUIZ_FIELD_MAP["bonus_pdf"]:          payload.get("bonusPdfLabel", ""),
        QUIZ_FIELD_MAP["urgency_flag"]:       "Yes" if "HIGH_URGENCY" in flags else "No",
        QUIZ_FIELD_MAP["completed_date"]:     timestamp,
    }

    try:
        search_resp = pipedrive_request("GET", "persons/search", params={"term": email, "fields": "email"})
        search_resp.raise_for_status()
        items = search_resp.json().get("data", {}).get("items", [])
        if items:
            person_id = items[0]["item"]["id"]
            pipedrive_request("PUT", f"persons/{person_id}", json=person_fields).raise_for_status()
        else:
            create_resp = pipedrive_request("POST", "persons", json={
                "name": first_name or email.split("@")[0],
                "email": [{"value": email, "primary": True}],
                "owner_id": OWNER_ID,
                **person_fields,
            })
            create_resp.raise_for_status()
            person_id = create_resp.json()["data"]["id"]
    except requests.RequestException as e:
        return jsonify({"error": f"Pipedrive person error: {str(e)}"}), 502

    try:
        label_ids = [FLAG_LABEL_MAP[f] for f in flags if f in FLAG_LABEL_MAP]
        deal_body = {
            "title": f"Quiz Lead — {first_name or email}",
            "person_id": person_id,
            "pipeline_id": PIPELINE_ID,
            "stage_id": STAGE_ID,
            "user_id": OWNER_ID,
        }
        if label_ids:
            deal_body["label"] = label_ids
        deal_resp = pipedrive_request("POST", "deals", json=deal_body)
        deal_resp.raise_for_status()
        deal_id = deal_resp.json()["data"]["id"]
    except requests.RequestException as e:
        return jsonify({"error": f"Pipedrive deal error: {str(e)}", "person_id": person_id}), 502

    try:
        flags_str    = ", ".join(flags) if flags else "None"
        note_content = f"""QUIZ SUBMISSION — {timestamp[:10]}

SCORE: {score} / 100 — {tier_name}
FLAGS: {flags_str}

ENTRY REASON: {answers.get('entryReason', 'N/A')}
IDENTITY STATEMENT: {answers.get('identityStatement', 'N/A')}
CLOSING VISION: {answers.get('visionStatement', 'N/A')}
CONFIDENCE TYPE: {answers.get('confidence', '')} / {answers.get('confidenceValidated', '')}
FIREARM STATUS: {answers.get('firearmOwnership', '')} / {answers.get('carryStatus', '')}
PRIMARY OBJECTION: {answers.get('objection', '')}
FAMILY MOTIVATION: {answers.get('motivation', '')}
PRIOR INCIDENT: {answers.get('experience', '')}"""
        pipedrive_request("POST", "notes", json={
            "deal_id": deal_id, "content": note_content, "pinned_to_deal_flag": 1
        }).raise_for_status()
    except requests.RequestException:
        pass

    return jsonify({
        "status": "ok", "person_id": person_id, "deal_id": deal_id,
        "flags_applied": len(label_ids),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    })


# ─────────────────────────────────────────────
# GitHub Helpers
# ─────────────────────────────────────────────
def github_get_file(path: str) -> str:
    url     = f"{GITHUB_API_BASE}/{path}"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.text

def github_list_dir(path: str) -> list:
    url     = f"{GITHUB_API_BASE}/{path}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

def github_push_file(path: str, content: str, commit_message: str) -> dict:
    url     = f"{GITHUB_API_BASE}/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    sha = None
    try:
        check = requests.get(url, headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }, timeout=10)
        if check.status_code == 200:
            sha = check.json().get("sha")
    except Exception:
        pass
    payload = {"message": commit_message, "content": encoded, "branch": GITHUB_BRANCH}
    if sha:
        payload["sha"] = sha
    resp = requests.put(url, headers=headers, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


# ─────────────────────────────────────────────
# MCP Server
# ─────────────────────────────────────────────
MCP_TOOLS = [
    {
        "name": "get_skill",
        "description": "Retrieve the full content of an ETKM skill file by name.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_name": {"type": "string", "description": "e.g. 'etkm-brand-foundation'"}
            },
            "required": ["skill_name"]
        }
    },
    {
        "name": "list_skills",
        "description": "List all available ETKM skill names in the repository.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "get_prompt",
        "description": "Retrieve a prompt file from the /prompts directory by name.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt_name": {"type": "string", "description": "e.g. 'arc-classification-system-prompt'"}
            },
            "required": ["prompt_name"]
        }
    },
    {
        "name": "get_workflow_status",
        "description": "Get the current status of all ETKM workflows.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "classify_arc",
        "description": "Classify a prospect's story arc based on their Q&A intake response.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "qa_response": {"type": "string", "description": "The prospect's Q&A response"}
            },
            "required": ["qa_response"]
        }
    },
    {
        "name": "scrape_contacts",
        "description": "Scrape emails, phones, and social links from a list of URLs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "urls": {"type": "array", "items": {"type": "string"}},
                "follow_links": {"type": "boolean"},
                "max_concurrent": {"type": "integer"}
            },
            "required": ["urls"]
        }
    },
    {
        "name": "push_skill",
        "description": "Create or update a skill file in the ETKM GitHub repository.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_name":      {"type": "string"},
                "content":         {"type": "string"},
                "commit_message":  {"type": "string"}
            },
            "required": ["skill_name", "content"]
        }
    },
    {
        "name": "p6_run_intake",
        "description": "Run the P6 Media Library intake pipeline. Scans all 5 Dropbox intake folders, deduplicates against existing Notion records, creates Notion records for new files with full tagging. Returns a summary.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dry_run": {
                    "type": "boolean",
                    "description": "If true, report new files without creating Notion records. Default: false."
                }
            }
        }
    },
    {
        "name": "p6_check_auth",
        "description": "Check whether Dropbox OAuth is configured and working.",
        "inputSchema": {"type": "object", "properties": {}}
    }
]


def handle_mcp_tool(tool_name: str, tool_input: dict) -> dict:
    try:
        if tool_name == "list_skills":
            items       = github_list_dir("skills")
            skill_names = [i["name"] for i in items if i["type"] == "dir"]
            try:
                user_items  = github_list_dir("skills/user")
                skill_names += [f"user/{i['name']}" for i in user_items if i["type"] == "dir"]
            except Exception:
                pass
            return {"type": "text", "text": json.dumps({"skills": skill_names, "count": len(skill_names)})}

        elif tool_name == "get_skill":
            skill_name = tool_input.get("skill_name", "")
            try:
                content = github_get_file(f"skills/user/{skill_name}/SKILL.md")
            except Exception:
                content = github_get_file(f"skills/{skill_name}/SKILL.md")
            return {"type": "text", "text": content}

        elif tool_name == "get_prompt":
            content = github_get_file(f"prompts/{tool_input.get('prompt_name', '')}.md")
            return {"type": "text", "text": content}

        elif tool_name == "get_workflow_status":
            content = github_get_file("registry/README.md")
            return {"type": "text", "text": content}

        elif tool_name == "classify_arc":
            qa  = tool_input.get("qa_response", "")
            arc = classify_arc(qa)
            return {"type": "text", "text": json.dumps({
                "arc_type": arc, "qa_response": qa, "classification_method": "keyword_match"
            })}

        elif tool_name == "scrape_contacts":
            from contact_scraper import scrape_contacts
            result = asyncio.run(scrape_contacts(
                urls=tool_input.get("urls", []),
                follow_links=tool_input.get("follow_links", False),
                max_concurrent=tool_input.get("max_concurrent", 10),
                output_dir="/tmp/scraper_output",
            ))
            return {"type": "text", "text": json.dumps(result)}

        elif tool_name == "push_skill":
            if not GITHUB_TOKEN:
                return {"type": "text", "text": "Error: GITHUB_TOKEN not configured"}
            skill_name     = tool_input.get("skill_name", "")
            content        = tool_input.get("content", "")
            commit_message = tool_input.get("commit_message", f"Update skill: {skill_name}")
            if not skill_name or not content:
                return {"type": "text", "text": "Error: skill_name and content are required"}
            path   = f"skills/user/{skill_name}/SKILL.md"
            result = github_push_file(path, content, commit_message)
            return {"type": "text", "text": json.dumps({
                "status":     "success",
                "skill_name": skill_name,
                "path":       path,
                "commit":     result.get("commit", {}).get("sha", "")[:7],
                "url":        result.get("content", {}).get("html_url", "")
            })}

        elif tool_name == "p6_check_auth":
            has_refresh = bool(_dropbox_tokens.get("refresh_token") or os.environ.get("DROPBOX_REFRESH_TOKEN"))
            has_client  = bool(DROPBOX_APP_KEY and DROPBOX_APP_SECRET)
            return {"type": "text", "text": json.dumps({
                "oauth_configured":       has_refresh,
                "client_credentials_set": has_client,
                "authorize_url":          "https://claude-r82h.onrender.com/authorize" if has_client else None,
                "status":                 "ready" if has_refresh else "needs_authorization"
            })}

        elif tool_name == "p6_run_intake":
            dry_run = tool_input.get("dry_run", False)

            # Verify auth
            try:
                _get_dropbox_token()
            except Exception as e:
                return {"type": "text", "text": json.dumps({
                    "status": "error",
                    "error":  "Dropbox not authorized",
                    "detail": str(e),
                    "action": "Visit https://claude-r82h.onrender.com/authorize"
                })}

            # Scan all folders
            all_files = []
            for folder_name, folder_path in P6_FOLDERS.items():
                try:
                    folder_files = dropbox_list_folder(folder_path, folder_name)
                    all_files.extend(folder_files)
                except Exception:
                    pass

            # Dedup against Notion
            existing_urls = notion_get_existing_drive_urls()
            new_files     = [f for f in all_files if f["drive_url"] not in existing_urls]

            if not new_files:
                return {"type": "text", "text": json.dumps({
                    "status":          "current",
                    "message":         "P6 pipeline complete — no new files.",
                    "total_scanned":   len(all_files),
                    "already_in_notion": len(existing_urls),
                    "new_files":       0,
                    "timestamp":       datetime.utcnow().isoformat() + "Z"
                })}

            if dry_run:
                return {"type": "text", "text": json.dumps({
                    "status":    "dry_run",
                    "new_files": len(new_files),
                    "files":     [{"name": f["file_name"], "folder": f["folder_name"]} for f in new_files],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })}

            # Create Notion records
            created = []
            errors  = []
            for f in new_files:
                try:
                    record = notion_create_record(f)
                    created.append(record)
                except Exception as e:
                    errors.append({"file": f["file_name"], "error": str(e)})

            return {"type": "text", "text": json.dumps({
                "status":           "complete",
                "total_scanned":    len(all_files),
                "new_files_found":  len(new_files),
                "records_created":  len(created),
                "errors":           len(errors),
                "created":          created,
                "error_details":    errors,
                "timestamp":        datetime.utcnow().isoformat() + "Z"
            })}

        else:
            return {"type": "text", "text": f"Unknown tool: {tool_name}"}

    except requests.HTTPError as e:
        return {"type": "text", "text": f"HTTP error: {e.response.status_code} — {str(e)}"}
    except Exception as e:
        return {"type": "text", "text": f"Tool error: {str(e)}"}


@app.route("/mcp", methods=["POST"])
def mcp_endpoint():
    body    = request.get_json(silent=True) or {}
    method  = body.get("method", "")
    params  = body.get("params", {})
    req_id  = body.get("id", 1)

    if method == "initialize":
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {
                "name": "etkm-mcp", "version": "1.3.0",
                "description": "ETKM AI Operations Hub — skills, prompts, arc classification, P6 Dropbox intake"
            }
        }})

    elif method == "tools/list":
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS}})

    elif method == "tools/call":
        tool_name  = params.get("name", "")
        tool_input = params.get("arguments", {})
        result     = handle_mcp_tool(tool_name, tool_input)
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": {"content": [result]}})

    elif method == "notifications/initialized":
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": {}})

    else:
        return jsonify({"jsonrpc": "2.0", "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"}}), 404


@app.route("/mcp", methods=["GET"])
def mcp_sse():
    def event_stream():
        data = json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized",
            "params": {"serverInfo": {"name": "etkm-mcp", "version": "1.3.0"}}})
        yield f"data: {data}\n\n"
    return Response(event_stream(), mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
