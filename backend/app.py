"""
ETKM Backend — Flask App + MCP Server
Deployed on Google Cloud Run. Serves as middleware between Make.com, Pipedrive,
Claude API, Twilio SMS, and any AI agent (Claude, Gemini, Manus) via MCP protocol.
"""

import os
import json
import base64
import hashlib
import hmac
import requests
from flask import Flask, request, jsonify, Response
from datetime import datetime

app = Flask(__name__)

# ─────────────────────────────────────────────
# Register Twilio SMS Blueprints
# ─────────────────────────────────────────────
from backend.twilio_sms import twilio_bp
from backend.pipedrive_sms import pipedrive_sms_bp

app.register_blueprint(twilio_bp)
app.register_blueprint(pipedrive_sms_bp)

# ─────────────────────────────────────────────
# Environment
# ─────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
PIPEDRIVE_API_KEY = os.environ.get("PIPEDRIVE_API_KEY", "")
GITHUB_TOKEN      = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO       = "easttxkravmaga/Claude"
GITHUB_BRANCH     = "main"
GITHUB_API_BASE   = f"https://api.github.com/repos/{GITHUB_REPO}/contents"

# ─────────────────────────────────────────────
# Health
# ─────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "etkm-backend",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })


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
    """Load system prompt from GitHub or fall back to embedded version."""
    if GITHUB_TOKEN:
        try:
            url = f"{GITHUB_API_BASE}/prompts/arc-classification-system-prompt.md"
            resp = requests.get(url, headers={
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3.raw"
            }, timeout=5)
            if resp.status_code == 200:
                # Extract just the system prompt block
                content = resp.text
                start = content.find("```\n") + 4
                end = content.find("\n```", start)
                if start > 4 and end > start:
                    return content[start:end]
        except Exception:
            pass
    # Embedded fallback
    return EMBEDDED_SYSTEM_PROMPT

EMBEDDED_SYSTEM_PROMPT = """You are the email copywriter for East Texas Krav Maga (ETKM), a reality-based self-defense training facility in Tyler, TX. Your job is to write personalized, conversion-focused email copy for prospects who have booked a free trial lesson.

Brand voice: Direct, warm, confident. Never aggressive. Short paragraphs. Plain language.
Prohibited words: mastery, dominate, destroy, killer, beast, crush, elite, warrior.
Format: Open with [person_first_name], — no "Dear" or "Hello". One CTA per email. No markdown.
Sign off: Nate Lundstrom / East Texas Krav Maga / (903) 590-0085 / etxkravmaga.com"""

@app.route("/classify-arc", methods=["POST"])
def classify_arc_endpoint():
    """
    Receive prospect data from Make.com, classify arc, generate personalized email.
    
    Expected body:
    {
        "first_name": "Sarah",
        "email_number": 1,
        "email_name": "Booking Confirmation",
        "arc_type": "Arc: Safety",       // optional — Manus can pre-classify
        "qa_response": "I was attacked...",
        "trial_date": "Thursday, April 17",
        "trial_time": "6:30 PM",
        "word_limit": 200
    }
    """
    data = request.get_json(silent=True) or {}

    first_name   = data.get("first_name", "")
    email_number = data.get("email_number", 1)
    email_name   = data.get("email_name", "Booking Confirmation")
    qa_response  = data.get("qa_response", "")
    trial_date   = data.get("trial_date", "")
    trial_time   = data.get("trial_time", "")
    word_limit   = data.get("word_limit", 200)

    # Arc classification — use provided or auto-classify
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
    """
    Receive Square payment failure event.
    Trigger: Make.com moves contact to P4 (At Risk/Retention) with 'Payment Due' label.
    """
    payload = request.get_json(silent=True) or {}
    event_type = payload.get("type", "")

    if "payment.failed" not in event_type and "subscription" not in event_type.lower():
        return jsonify({"status": "ignored", "event_type": event_type}), 200

    # Extract customer info — Square sends merchant_id + customer_id
    data = payload.get("data", {}).get("object", {})
    customer_id = (
        data.get("payment", {}).get("customer_id") or
        data.get("subscription", {}).get("customer_id") or
        "unknown"
    )

    # Return structured data — Make.com handles the Pipedrive update
    return jsonify({
        "status": "processed",
        "event_type": event_type,
        "customer_id": customer_id,
        "action": "move_to_p4_payment_due",
        "timestamp": datetime.utcnow().isoformat() + "Z"
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
    }
]

def github_get_file(path: str) -> str:
    """Fetch raw file content from GitHub repo."""
    url = f"{GITHUB_API_BASE}/{path}"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.text

def github_list_dir(path: str) -> list:
    """List directory contents from GitHub repo."""
    url = f"{GITHUB_API_BASE}/{path}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

def handle_mcp_tool(tool_name: str, tool_input: dict) -> dict:
    """Execute an MCP tool call and return result."""
    try:
        if tool_name == "list_skills":
            items = github_list_dir("skills")
            skill_names = [item["name"] for item in items if item["type"] == "dir"]
            return {
                "type": "text",
                "text": json.dumps({"skills": skill_names, "count": len(skill_names)})
            }

        elif tool_name == "get_skill":
            skill_name = tool_input.get("skill_name", "")
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

        else:
            return {"type": "text", "text": f"Unknown tool: {tool_name}"}

    except requests.HTTPError as e:
        return {"type": "text", "text": f"GitHub fetch error: {e.response.status_code} — {str(e)}"}
    except Exception as e:
        return {"type": "text", "text": f"Tool error: {str(e)}"}


@app.route("/mcp", methods=["POST"])
def mcp_endpoint():
    """
    MCP protocol endpoint — handles initialize, tools/list, and tools/call.
    Compatible with Claude.ai connector format and standard MCP clients.
    """
    body = request.get_json(silent=True) or {}
    method  = body.get("method", "")
    params  = body.get("params", {})
    req_id  = body.get("id", 1)

    # ── Initialize ──
    if method == "initialize":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "etkm-mcp",
                    "version": "1.0.0",
                    "description": "ETKM AI Operations Hub — skills, prompts, workflows, arc classification"
                }
            }
        })

    # ── List Tools ──
    elif method == "tools/list":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": MCP_TOOLS}
        })

    # ── Call Tool ──
    elif method == "tools/call":
        tool_name  = params.get("name", "")
        tool_input = params.get("arguments", {})
        result     = handle_mcp_tool(tool_name, tool_input)
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"content": [result]}
        })

    # ── SSE Discovery (some MCP clients probe this) ──
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
    """
    SSE endpoint for MCP clients that use server-sent events transport.
    Returns a minimal SSE stream with server info.
    """
    def event_stream():
        # Send server info as first event
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {
                "serverInfo": {
                    "name": "etkm-mcp",
                    "version": "1.0.0"
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
