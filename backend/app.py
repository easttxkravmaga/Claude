"""
ETKM Backend — Flask App + MCP Server
Deployed on Render. Serves as middleware between Pipedrive, Claude API,
and any AI agent (Claude, Gemini, Manus) via MCP protocol.
"""

import os
import json
import base64
import hashlib
import hmac
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

# Google OAuth
GOOGLE_CLIENT_ID     = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI  = os.environ.get("GOOGLE_REDIRECT_URI", "https://claude-r82h.onrender.com/oauth/callback")

# Google tokens — loaded from env on startup, refreshed in memory
_google_tokens = {
    "access_token":  os.environ.get("GOOGLE_ACCESS_TOKEN", ""),
    "refresh_token": os.environ.get("GOOGLE_REFRESH_TOKEN", ""),
    "expires_at":    0
}

# P6 Drive folder IDs
P6_FOLDERS = {
    "Class Pics":           "1ebfk6lp21V6mD3ryfW3JoKocoiKROokI",
    "Scenario Pics":        "1mY9dBj1DiGwPM6lvu6LGp4cEcFniH1ww",
    "Email Pics":           "1QO1rHOWYaNpvd8XriHTyM85xbE_CE3pd",
    "Videos":               "1SCSF9b5qSYo8zFaUo5yiSfF00Urwa5aD",
    "Ready for Production": "1muXfteK840-b7GASYS3iwBhEsqS9aZhS",
}

# Notion Media Library
NOTION_MEDIA_DB_ID   = "711e3a52-1604-4182-ae94-9d23a2960963"
NOTION_TOKEN         = os.environ.get("NOTION_TOKEN", "")


# ─────────────────────────────────────────────
# Health
# ─────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "etkm-backend",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "google_auth": "configured" if _google_tokens.get("refresh_token") else "not_configured"
    })


# ─────────────────────────────────────────────
# Google OAuth Flow
# ─────────────────────────────────────────────
@app.route("/authorize", methods=["GET"])
def authorize():
    """Step 1 — redirect Nathan to Google consent screen."""
    if not GOOGLE_CLIENT_ID:
        return jsonify({"error": "GOOGLE_CLIENT_ID not set in environment"}), 500

    scope = "https://www.googleapis.com/auth/drive.readonly"
    params = (
        f"client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={scope}"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?{params}")


@app.route("/oauth/callback", methods=["GET"])
def oauth_callback():
    """Step 2 — exchange code for tokens and persist to Render env."""
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "No code in callback"}), 400

    # Exchange code for tokens
    token_resp = requests.post("https://oauth2.googleapis.com/token", data={
        "code":          code,
        "client_id":     GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri":  GOOGLE_REDIRECT_URI,
        "grant_type":    "authorization_code",
    }, timeout=15)

    if token_resp.status_code != 200:
        return jsonify({"error": "Token exchange failed", "detail": token_resp.text}), 500

    tokens = token_resp.json()
    _google_tokens["access_token"]  = tokens.get("access_token", "")
    _google_tokens["refresh_token"] = tokens.get("refresh_token", "")
    _google_tokens["expires_at"]    = datetime.utcnow().timestamp() + tokens.get("expires_in", 3600)

    # Persist refresh token to Render environment variable so it survives redeploys
    _persist_to_render("GOOGLE_REFRESH_TOKEN", _google_tokens["refresh_token"])
    _persist_to_render("GOOGLE_ACCESS_TOKEN",  _google_tokens["access_token"])

    return jsonify({
        "status": "authorized",
        "message": "Google Drive access granted. P6 pipeline is ready.",
        "refresh_token_stored": bool(_google_tokens["refresh_token"])
    })


def _persist_to_render(key: str, value: str):
    """Write an env var to the Render service so tokens survive redeploys."""
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
        pass  # Non-fatal — token still works in memory for this process


def _get_valid_access_token() -> str:
    """Return a valid Google access token, refreshing if needed."""
    now = datetime.utcnow().timestamp()

    # If token is still valid (with 5-min buffer), return it
    if _google_tokens["access_token"] and _google_tokens["expires_at"] > now + 300:
        return _google_tokens["access_token"]

    # Refresh using refresh token
    refresh_token = _google_tokens.get("refresh_token") or os.environ.get("GOOGLE_REFRESH_TOKEN", "")
    if not refresh_token:
        raise Exception("No Google refresh token available. Visit /authorize to authenticate.")

    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "refresh_token": refresh_token,
        "client_id":     GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "grant_type":    "refresh_token",
    }, timeout=15)

    if resp.status_code != 200:
        raise Exception(f"Token refresh failed: {resp.text}")

    tokens = resp.json()
    _google_tokens["access_token"] = tokens["access_token"]
    _google_tokens["expires_at"]   = now + tokens.get("expires_in", 3600)
    _persist_to_render("GOOGLE_ACCESS_TOKEN", _google_tokens["access_token"])

    return _google_tokens["access_token"]


# ─────────────────────────────────────────────
# Google Drive Helpers
# ─────────────────────────────────────────────
def drive_list_folder(folder_id: str, folder_name: str) -> list:
    """List all files in a Drive folder. Returns list of file dicts."""
    token = _get_valid_access_token()
    files = []
    page_token = None

    while True:
        params = {
            "q":        f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed = false",
            "fields":   "nextPageToken, files(id, name, mimeType, webViewLink, createdTime)",
            "pageSize": 100,
        }
        if page_token:
            params["pageToken"] = page_token

        resp = requests.get(
            "https://www.googleapis.com/drive/v3/files",
            headers={"Authorization": f"Bearer {token}"},
            params=params,
            timeout=15
        )
        resp.raise_for_status()
        data = resp.json()

        for f in data.get("files", []):
            files.append({
                "file_id":     f["id"],
                "file_name":   f["name"],
                "mime_type":   f.get("mimeType", ""),
                "drive_url":   f.get("webViewLink", f"https://drive.google.com/file/d/{f['id']}/view"),
                "folder_name": folder_name,
                "created":     f.get("createdTime", ""),
            })

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return files


def notion_get_existing_drive_urls() -> set:
    """Pull all Drive URLs already in the Notion Media Library."""
    existing = set()
    has_more = True
    cursor = None

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
        cursor = data.get("next_cursor")

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
        (["headshot"],                                ["headshot", "portrait"]),
        (["group"],                                   ["group"]),
        (["facility", "gym", "mat"],                 ["facility", "environment"]),
        (["seminar", "event"],                       ["event", "seminar"]),
        (["kick", "strike", "choke", "grab",
          "defense", "escape"],                      ["action-shot"]),
        (["parking", "street", "outdoor",
          "scenario"],                               ["real-world"]),
        (["portrait", "pose"],                       ["portrait", "posed"]),
        (["candid"],                                  ["candid"]),
        (["college"],                                 ["college-safety"]),
        (["private"],                                 ["private-lessons"]),
        (["community"],                              ["community", "community-event"]),
        (["instructor", "teach"],                    ["instructional"]),
        (["high-energy"],                            ["high-energy"]),
        (["calm", "focus"],                          ["calm-focus"]),
    ]

    for keywords, assigned_tags in rules:
        if any(k in name for k in keywords):
            tags.extend(assigned_tags)

    return list(dict.fromkeys(tags))  # deduplicate, preserve order


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

    # Defaults
    if not uses:
        if any(k in name for k in ["kick", "strike", "choke", "grab", "defense", "escape"]):
            uses.append("Social media post")
        elif any(k in name for k in ["facility", "gym", "mat", "outdoor"]):
            uses.extend(["Website background", "Landing page hero"])
        else:
            uses.append("Social media post")

    return list(dict.fromkeys(uses))


def infer_description(file_name: str, folder_name: str, asset_type: str) -> str:
    name = file_name.lower().replace("-", " ").replace("_", " ")
    # Strip extension
    name = name.rsplit(".", 1)[0] if "." in name else name
    return f"ETKM {asset_type.lower()} — {name} ({folder_name})."


def notion_create_record(file: dict) -> dict:
    """Create a single Notion Media Library record."""
    asset_type   = infer_asset_type(file["file_name"], file["mime_type"])
    tags         = infer_tags(file["file_name"], file["folder_name"])
    content_uses = infer_content_uses(file["file_name"], file["folder_name"])
    description  = infer_description(file["file_name"], file["folder_name"], asset_type)

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

    arc_type = data.get("arc_type") or classify_arc(qa_response)

    if not ANTHROPIC_API_KEY:
        return jsonify({"error": "ANTHROPIC_API_KEY not configured"}), 500

    user_message = f"""You are writing Email {email_number} — {email_name} — for East Texas Krav Maga.

PROSPECT CONTEXT:
- First name: {first_name}
- Arc type: {arc_type}
- Q&A response: {qa_response or "none"}
- Trial date: {trial_date or "not provided"}
- Trial time: {trial_time or "not provided"}
- Email number: {email_number}
- Sequence position: {email_name}

TASK:
Write Email {email_number} — {email_name} — exactly as specified in the ETKM email sequence.
Apply arc-type personalization if arc is not Arc: Default.
Follow all brand voice rules. Stay under {word_limit} words.
Sign off as Nate Lundstrom, East Texas Krav Maga, (903) 590-0085.

Return only the email — subject line first, blank line, then body. No preamble, no explanation, no markdown."""

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
        email_copy = result["content"][0]["text"]

        return jsonify({
            "arc_type": arc_type,
            "email_number": email_number,
            "email_name": email_name,
            "email_copy": email_copy,
            "model": result.get("model"),
            "usage": result.get("usage")
        })

    except requests.RequestException as e:
        return jsonify({"error": str(e), "arc_type": arc_type}), 502


# ─────────────────────────────────────────────
# Square Webhook → Pipedrive P4
# ─────────────────────────────────────────────
@app.route("/webhook/square", methods=["POST"])
def square_webhook():
    payload = request.get_json(silent=True) or {}
    event_type = payload.get("type", "")

    if "payment.failed" not in event_type and "subscription" not in event_type.lower():
        return jsonify({"status": "ignored", "event_type": event_type}), 200

    data = payload.get("data", {}).get("object", {})
    customer_id = (
        data.get("payment", {}).get("customer_id") or
        data.get("subscription", {}).get("customer_id") or
        "unknown"
    )

    return jsonify({
        "status": "processed",
        "event_type": event_type,
        "customer_id": customer_id,
        "action": "move_to_p4_payment_due",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })


# ─────────────────────────────────────────────
# Quiz Webhook → Pipedrive Person + Deal
# ─────────────────────────────────────────────
PIPEDRIVE_DOMAIN = "easttexaskravmaga.pipedrive.com"
PIPEDRIVE_BASE   = f"https://{PIPEDRIVE_DOMAIN}/api/v1"

OWNER_ID    = 21519696
PIPELINE_ID = 1
STAGE_ID    = 1

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
    "HIGH_URGENCY":                        99,
    "AWARENESS_GAP":                       100,
    "AWARENESS_SUPPRESSED":                101,
    "NO_BASELINE_SKILLS_GAP":              102,
    "FALSE_CONFIDENCE_URGENT":             103,
    "HIGH_COACHABILITY":                   104,
    "NO_ONSET_PLAN":                       105,
    "NO_ACTION_PLAN":                      106,
    "PRIOR_INCIDENT_CONSULT_CARE":         107,
    "REALITY_EXPOSURE_GAP":                108,
    "PARENT_FAMILY_ARC":                   109,
    "MUST_PROTECT_CONSULT_FIRST":          110,
    "NO_FIREARM_ACT_AWARENESS":            111,
    "ACT_CONSULT_PRIORITY":                112,
    "ACT_CANDIDATE_ADVANCED":              113,
    "RETURNING_PRACTITIONER_PRIORITY":     114,
    "IDENTITY_BARRIER_OPEN_WITH_INCLUSION":115,
    "PHYSICAL_FLAG_Q12_ACTIVE":            116,
    "COACHABILITY_NEEDS_WARMUP":           117,
    "ENCOURAGEMENT_PATH":                  118,
    "ACT_CONFIRMED":                       119,
    "FAMILY_ARC_CONFIRMED":                120,
    "FEAR_BARRIER_CONFIRMED":              121,
}

TIER_PDF_MAP = {
    "Unaware":           "The Wake-Up Call Guide",
    "Aware of the Gap":  "The Gap Assessment Guide",
    "Ready to Act":      "The Action Readiness Guide",
    "Already Acting":    "The Practitioner's Edge Guide",
}

def pipedrive_request(method, path, **kwargs):
    url = f"{PIPEDRIVE_BASE}/{path}"
    params = kwargs.pop("params", {})
    params["api_token"] = PIPEDRIVE_API_KEY
    return requests.request(method, url, params=params, timeout=15, **kwargs)


@app.route("/quiz-webhook", methods=["POST"])
def quiz_webhook():
    payload = request.get_json(silent=True) or {}

    first_name = payload.get("firstName", "")
    email      = payload.get("email", "")
    score      = payload.get("score", 0)
    tier       = payload.get("tier", 0)
    tier_name  = payload.get("tierName", "")
    answers    = payload.get("answers", {})
    flags      = payload.get("flags", [])
    timestamp  = payload.get("timestamp", datetime.utcnow().isoformat() + "Z")

    if not email:
        return jsonify({"error": "email is required"}), 400

    if not PIPEDRIVE_API_KEY:
        return jsonify({"error": "PIPEDRIVE_API_KEY not configured"}), 500

    confidence_type = f"{answers.get('confidence', '')} / {answers.get('confidenceValidated', '')}"
    firearm_status  = f"{answers.get('firearmOwnership', '')} / {answers.get('carryStatus', '')}"
    must_protect    = "Yes" if answers.get("motivation") == "public" else "No"
    returning_pract = "Yes" if answers.get("objection") == "trained" else "No"
    urgency_flag    = "Yes" if "HIGH_URGENCY" in flags else "No"
    auto_pdf        = TIER_PDF_MAP.get(tier_name, "")
    bonus_pdf       = payload.get("bonusPdfLabel", "")

    person_fields = {
        QUIZ_FIELD_MAP["entry_reason"]:       answers.get("entryReason", ""),
        QUIZ_FIELD_MAP["score"]:              str(score),
        QUIZ_FIELD_MAP["tier_name"]:          tier_name,
        QUIZ_FIELD_MAP["identity_statement"]: answers.get("identityStatement", ""),
        QUIZ_FIELD_MAP["vision_statement"]:   answers.get("visionStatement", ""),
        QUIZ_FIELD_MAP["confidence_type"]:    confidence_type,
        QUIZ_FIELD_MAP["primary_objection"]:  answers.get("objection", ""),
        QUIZ_FIELD_MAP["firearm_status"]:     firearm_status,
        QUIZ_FIELD_MAP["family_motivation"]:  answers.get("motivation", ""),
        QUIZ_FIELD_MAP["must_protect"]:       must_protect,
        QUIZ_FIELD_MAP["prior_incident"]:     answers.get("experience", ""),
        QUIZ_FIELD_MAP["returning_pract"]:    returning_pract,
        QUIZ_FIELD_MAP["auto_pdf"]:           auto_pdf,
        QUIZ_FIELD_MAP["bonus_pdf"]:          bonus_pdf,
        QUIZ_FIELD_MAP["urgency_flag"]:       urgency_flag,
        QUIZ_FIELD_MAP["completed_date"]:     timestamp,
    }

    try:
        search_resp = pipedrive_request("GET", "persons/search", params={"term": email, "fields": "email"})
        search_resp.raise_for_status()
        search_data = search_resp.json()
        items = search_data.get("data", {}).get("items", [])

        if items:
            person_id = items[0]["item"]["id"]
            update_body = {**person_fields}
            pipedrive_request("PUT", f"persons/{person_id}", json=update_body).raise_for_status()
        else:
            create_body = {
                "name": first_name or email.split("@")[0],
                "email": [{"value": email, "primary": True}],
                "owner_id": OWNER_ID,
                **person_fields,
            }
            create_resp = pipedrive_request("POST", "persons", json=create_body)
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
        date_str = timestamp[:10] if len(timestamp) >= 10 else timestamp
        flags_str = ", ".join(flags) if flags else "None"

        note_content = f"""QUIZ SUBMISSION — {date_str}

SCORE: {score} / 100 — {tier_name}
FLAGS: {flags_str}

ENTRY REASON (Q0):
{answers.get('entryReason', 'N/A')}

IDENTITY STATEMENT (Q1):
{answers.get('identityStatement', 'N/A')}

CLOSING VISION (Q13):
{answers.get('visionStatement', 'N/A')}

CONFIDENCE TYPE: {answers.get('confidence', '')} / {answers.get('confidenceValidated', '')}
FIREARM STATUS: {answers.get('firearmOwnership', '')} / {answers.get('carryStatus', '')}
PRIMARY OBJECTION: {answers.get('objection', '')}
FAMILY MOTIVATION: {answers.get('motivation', '')}
PRIOR INCIDENT: {answers.get('experience', '')}"""

        note_body = {
            "deal_id": deal_id,
            "content": note_content,
            "pinned_to_deal_flag": 1,
        }
        pipedrive_request("POST", "notes", json=note_body).raise_for_status()
    except requests.RequestException:
        pass

    return jsonify({
        "status": "ok",
        "person_id": person_id,
        "deal_id": deal_id,
        "flags_applied": len(label_ids),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    })


# ─────────────────────────────────────────────
# MCP Server — Tools for AI Agents
# ─────────────────────────────────────────────
MCP_TOOLS = [
    {
        "name": "get_skill",
        "description": "Retrieve the full content of an ETKM skill file by name. Returns the raw SKILL.md content.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "Skill name, e.g. 'etkm-brand-foundation', 'etkm-crm-doctrine', 'nate-collaboration-workflow'"
                }
            },
            "required": ["skill_name"]
        }
    },
    {
        "name": "list_skills",
        "description": "List all available ETKM skill names in the repository.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_prompt",
        "description": "Retrieve a prompt file from the /prompts directory by name.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt_name": {
                    "type": "string",
                    "description": "Prompt filename without extension, e.g. 'arc-classification-system-prompt'"
                }
            },
            "required": ["prompt_name"]
        }
    },
    {
        "name": "get_workflow_status",
        "description": "Get the current status of all ETKM workflows (WF-001, WF-002, WF-003) and active dependencies.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "classify_arc",
        "description": "Classify a prospect's story arc based on their Q&A intake response.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "qa_response": {
                    "type": "string",
                    "description": "The prospect's free-text Q&A response from Calendly intake"
                }
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
                "urls": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of URLs to scrape."
                },
                "follow_links": {
                    "type": "boolean",
                    "description": "Crawl internal contact/about pages. Default: false."
                },
                "max_concurrent": {
                    "type": "integer",
                    "description": "Max parallel requests. Default: 10."
                }
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
                "skill_name": {
                    "type": "string",
                    "description": "The skill directory name, e.g. 'etkm-behavior-intelligence'"
                },
                "content": {
                    "type": "string",
                    "description": "The full SKILL.md content to write"
                },
                "commit_message": {
                    "type": "string",
                    "description": "Git commit message describing the change"
                }
            },
            "required": ["skill_name", "content"]
        }
    },
    {
        "name": "p6_run_intake",
        "description": "Run the P6 Media Library intake pipeline. Scans all 5 Drive intake folders, deduplicates against existing Notion records, creates Notion records for new files with full tagging. Returns a summary of what was processed.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dry_run": {
                    "type": "boolean",
                    "description": "If true, scan and report new files but do not create Notion records. Default: false."
                }
            }
        }
    },
    {
        "name": "p6_check_auth",
        "description": "Check whether Google Drive OAuth is configured and working. Returns auth status and authorize URL if not configured.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


def github_get_file(path: str) -> str:
    url = f"{GITHUB_API_BASE}/{path}"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.text

def github_list_dir(path: str) -> list:
    url = f"{GITHUB_API_BASE}/{path}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

def github_push_file(path: str, content: str, commit_message: str) -> dict:
    url = f"{GITHUB_API_BASE}/{path}"
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

    payload = {
        "message": commit_message,
        "content": encoded,
        "branch": GITHUB_BRANCH
    }
    if sha:
        payload["sha"] = sha

    resp = requests.put(url, headers=headers, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


def handle_mcp_tool(tool_name: str, tool_input: dict) -> dict:
    try:
        if tool_name == "list_skills":
            items = github_list_dir("skills")
            skill_names = [item["name"] for item in items if item["type"] == "dir"]
            try:
                user_items = github_list_dir("skills/user")
                user_skill_names = [f"user/{item['name']}" for item in user_items if item["type"] == "dir"]
                skill_names = skill_names + user_skill_names
            except Exception:
                pass
            return {
                "type": "text",
                "text": json.dumps({"skills": skill_names, "count": len(skill_names)})
            }

        elif tool_name == "get_skill":
            skill_name = tool_input.get("skill_name", "")
            try:
                content = github_get_file(f"skills/user/{skill_name}/SKILL.md")
            except Exception:
                content = github_get_file(f"skills/{skill_name}/SKILL.md")
            return {"type": "text", "text": content}

        elif tool_name == "get_prompt":
            prompt_name = tool_input.get("prompt_name", "")
            content = github_get_file(f"prompts/{prompt_name}.md")
            return {"type": "text", "text": content}

        elif tool_name == "get_workflow_status":
            content = github_get_file("registry/README.md")
            return {"type": "text", "text": content}

        elif tool_name == "classify_arc":
            qa = tool_input.get("qa_response", "")
            arc = classify_arc(qa)
            return {
                "type": "text",
                "text": json.dumps({
                    "arc_type": arc,
                    "qa_response": qa,
                    "classification_method": "keyword_match"
                })
            }

        elif tool_name == "scrape_contacts":
            from contact_scraper import scrape_contacts
            urls = tool_input.get("urls", [])
            follow = tool_input.get("follow_links", False)
            concurrent = tool_input.get("max_concurrent", 10)
            result = asyncio.run(scrape_contacts(
                urls=urls,
                follow_links=follow,
                max_concurrent=concurrent,
                output_dir="/tmp/scraper_output",
            ))
            return {"type": "text", "text": json.dumps(result)}

        elif tool_name == "push_skill":
            if not GITHUB_TOKEN:
                return {"type": "text", "text": "Error: GITHUB_TOKEN not configured in environment"}
            skill_name     = tool_input.get("skill_name", "")
            content        = tool_input.get("content", "")
            commit_message = tool_input.get("commit_message", f"Update skill: {skill_name}")
            if not skill_name or not content:
                return {"type": "text", "text": "Error: skill_name and content are required"}
            path = f"skills/user/{skill_name}/SKILL.md"
            result = github_push_file(path, content, commit_message)
            html_url   = result.get("content", {}).get("html_url", "")
            commit_sha = result.get("commit", {}).get("sha", "")[:7]
            return {
                "type": "text",
                "text": json.dumps({
                    "status": "success",
                    "skill_name": skill_name,
                    "path": path,
                    "commit": commit_sha,
                    "url": html_url
                })
            }

        elif tool_name == "p6_check_auth":
            has_refresh = bool(_google_tokens.get("refresh_token") or os.environ.get("GOOGLE_REFRESH_TOKEN"))
            has_client  = bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)
            return {
                "type": "text",
                "text": json.dumps({
                    "oauth_configured": has_refresh,
                    "client_credentials_set": has_client,
                    "authorize_url": "https://claude-r82h.onrender.com/authorize" if has_client else None,
                    "status": "ready" if has_refresh else "needs_authorization"
                })
            }

        elif tool_name == "p6_run_intake":
            dry_run = tool_input.get("dry_run", False)

            # Verify auth
            try:
                _get_valid_access_token()
            except Exception as e:
                return {
                    "type": "text",
                    "text": json.dumps({
                        "status": "error",
                        "error": "Google Drive not authorized",
                        "detail": str(e),
                        "action": "Visit https://claude-r82h.onrender.com/authorize to authorize"
                    })
                }

            # Scan all folders
            all_files = []
            for folder_name, folder_id in P6_FOLDERS.items():
                try:
                    folder_files = drive_list_folder(folder_id, folder_name)
                    all_files.extend(folder_files)
                except Exception as e:
                    pass  # Log but continue with other folders

            # Get existing Notion Drive URLs for deduplication
            existing_urls = notion_get_existing_drive_urls()

            # Filter to new files only
            new_files = [f for f in all_files if f["drive_url"] not in existing_urls]

            if not new_files:
                return {
                    "type": "text",
                    "text": json.dumps({
                        "status": "current",
                        "message": "P6 pipeline complete — no new files. Library is current.",
                        "total_scanned": len(all_files),
                        "already_catalogued": len(existing_urls),
                        "new_files": 0,
                        "timestamp": datetime.utcnow().isoformat() + "Z"
                    })
                }

            if dry_run:
                return {
                    "type": "text",
                    "text": json.dumps({
                        "status": "dry_run",
                        "total_scanned": len(all_files),
                        "new_files": len(new_files),
                        "files": [{"name": f["file_name"], "folder": f["folder_name"]} for f in new_files],
                        "timestamp": datetime.utcnow().isoformat() + "Z"
                    })
                }

            # Create Notion records
            created = []
            errors  = []
            for f in new_files:
                try:
                    record = notion_create_record(f)
                    created.append(record)
                except Exception as e:
                    errors.append({"file": f["file_name"], "error": str(e)})

            return {
                "type": "text",
                "text": json.dumps({
                    "status": "complete",
                    "total_scanned": len(all_files),
                    "new_files_found": len(new_files),
                    "records_created": len(created),
                    "errors": len(errors),
                    "created": created,
                    "error_details": errors,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
            }

        else:
            return {"type": "text", "text": f"Unknown tool: {tool_name}"}

    except requests.HTTPError as e:
        return {"type": "text", "text": f"HTTP error: {e.response.status_code} — {str(e)}"}
    except Exception as e:
        return {"type": "text", "text": f"Tool error: {str(e)}"}


@app.route("/mcp", methods=["POST"])
def mcp_endpoint():
    body = request.get_json(silent=True) or {}
    method  = body.get("method", "")
    params  = body.get("params", {})
    req_id  = body.get("id", 1)

    if method == "initialize":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "etkm-mcp",
                    "version": "1.2.0",
                    "description": "ETKM AI Operations Hub — skills, prompts, workflows, arc classification, P6 media intake"
                }
            }
        })

    elif method == "tools/list":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": MCP_TOOLS}
        })

    elif method == "tools/call":
        tool_name  = params.get("name", "")
        tool_input = params.get("arguments", {})
        result     = handle_mcp_tool(tool_name, tool_input)
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"content": [result]}
        })

    elif method == "notifications/initialized":
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": {}})

    else:
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"}
        }), 404


@app.route("/mcp", methods=["GET"])
def mcp_sse():
    def event_stream():
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {
                "serverInfo": {
                    "name": "etkm-mcp",
                    "version": "1.2.0"
                }
            }
        })
        yield f"data: {data}\n\n"

    return Response(
        event_stream(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
