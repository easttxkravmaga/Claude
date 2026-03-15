"""
ETKM Pipedrive SMS Integration Layer
Connects Twilio SMS with Pipedrive CRM for contact-based sending and message logging.
"""

import os
import logging
from datetime import datetime, timezone

import requests
from flask import Blueprint, request, jsonify

from .twilio_sms import send_sms, register_opt_in, has_valid_opt_in, is_opted_out
from .message_templates import render_template, list_templates

logger = logging.getLogger(__name__)

PIPEDRIVE_API_KEY = os.environ.get("PIPEDRIVE_API_KEY", "")
PIPEDRIVE_BASE_URL = "https://api.pipedrive.com/v1"

# Custom field keys from Pipedrive (Sakari fields repurposed for Twilio)
PIPEDRIVE_SMS_OPT_IN_FIELD = os.environ.get("PIPEDRIVE_SMS_OPT_IN_FIELD", "8cae8f528afa52fd268f")
PIPEDRIVE_SMS_OPT_OUT_FIELD = os.environ.get("PIPEDRIVE_SMS_OPT_OUT_FIELD", "624eeb304949f6989717")

pipedrive_sms_bp = Blueprint("pipedrive_sms", __name__)


# ─────────────────────────────────────────────
# Pipedrive API Helpers
# ─────────────────────────────────────────────
def pipedrive_get(endpoint, params=None):
    """Make a GET request to Pipedrive API."""
    params = params or {}
    params["api_token"] = PIPEDRIVE_API_KEY
    resp = requests.get(f"{PIPEDRIVE_BASE_URL}/{endpoint}", params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def pipedrive_post(endpoint, data):
    """Make a POST request to Pipedrive API."""
    data["api_token"] = PIPEDRIVE_API_KEY
    resp = requests.post(f"{PIPEDRIVE_BASE_URL}/{endpoint}", json=data, timeout=15)
    resp.raise_for_status()
    return resp.json()


def pipedrive_put(endpoint, data):
    """Make a PUT request to Pipedrive API."""
    params = {"api_token": PIPEDRIVE_API_KEY}
    resp = requests.put(f"{PIPEDRIVE_BASE_URL}/{endpoint}", params=params, json=data, timeout=15)
    resp.raise_for_status()
    return resp.json()


# ─────────────────────────────────────────────
# Contact Lookup
# ─────────────────────────────────────────────
def find_person_by_phone(phone_number):
    """Look up a Pipedrive person by phone number."""
    try:
        result = pipedrive_get("persons/search", {"term": phone_number, "fields": "phone"})
        items = result.get("data", {}).get("items", [])
        if items:
            return items[0].get("item", {})
    except Exception as e:
        logger.error("Pipedrive person search failed: %s", e)
    return None


def get_person_phone(person_id):
    """Get primary phone number for a Pipedrive person."""
    try:
        result = pipedrive_get(f"persons/{person_id}")
        person = result.get("data", {})
        phones = person.get("phone", [])
        if phones:
            return phones[0].get("value", "")
    except Exception as e:
        logger.error("Pipedrive person lookup failed: %s", e)
    return ""


# ─────────────────────────────────────────────
# Activity / Note Logging
# ─────────────────────────────────────────────
def log_sms_to_pipedrive(person_id, direction, body, message_sid="", status=""):
    """Log an SMS as a Pipedrive note on the person record."""
    if not PIPEDRIVE_API_KEY or not person_id:
        return None

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    arrow = "→" if direction == "outbound" else "←"
    note_content = (
        f"SMS {arrow} ({direction}) — {timestamp}\n"
        f"Status: {status}\n"
        f"SID: {message_sid}\n"
        f"---\n"
        f"{body}"
    )

    try:
        result = pipedrive_post("notes", {
            "content": note_content,
            "person_id": person_id,
            "pinned_to_person_flag": 0,
        })
        return result.get("data", {}).get("id")
    except Exception as e:
        logger.error("Failed to log SMS note to Pipedrive: %s", e)
        return None


def update_sms_opt_fields(person_id, opt_type="opt_in"):
    """Update the SMS opt-in/opt-out date fields on a Pipedrive person."""
    if not PIPEDRIVE_API_KEY or not person_id:
        return

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    field_key = PIPEDRIVE_SMS_OPT_IN_FIELD if opt_type == "opt_in" else PIPEDRIVE_SMS_OPT_OUT_FIELD

    try:
        pipedrive_put(f"persons/{person_id}", {field_key: today})
    except Exception as e:
        logger.error("Failed to update Pipedrive SMS field: %s", e)


# ─────────────────────────────────────────────
# API: Send SMS to Pipedrive Contact
# ─────────────────────────────────────────────
@pipedrive_sms_bp.route("/api/pipedrive/send-sms", methods=["POST"])
def send_sms_to_contact():
    """
    Send an SMS to a Pipedrive person by person_id or phone number.

    Expected JSON body:
    {
        "person_id": 123,              // or use "to" with phone number
        "to": "+19035551234",          // optional if person_id provided
        "first_name": "Sarah",
        "template": "lead_followup_initial",  // or use "body" for custom
        "body": "Custom message...",
        "message_type": "lead_followup",
        "date": "Thursday, April 17",  // optional merge field
        "time": "6:30 PM"             // optional merge field
    }
    """
    data = request.get_json(silent=True) or {}
    person_id = data.get("person_id")
    to = data.get("to", "")
    first_name = data.get("first_name", "")
    template_key = data.get("template", "")
    body = data.get("body", "")
    message_type = data.get("message_type", "general")

    # Resolve phone from person_id if needed
    if person_id and not to:
        to = get_person_phone(person_id)
        if not to:
            return jsonify({"error": "No phone number found for person"}), 400

    # Resolve person_id from phone if needed (for logging)
    if to and not person_id:
        person = find_person_by_phone(to)
        if person:
            person_id = person.get("id")
            if not first_name:
                first_name = person.get("name", "").split()[0] if person.get("name") else ""

    if not to:
        return jsonify({"error": "No recipient phone number"}), 400

    # Render template or use custom body
    if template_key:
        rendered = render_template(
            template_key,
            first_name=first_name,
            date=data.get("date", ""),
            time=data.get("time", ""),
            event_name=data.get("event_name", ""),
        )
        if rendered:
            body = rendered["body"]
            message_type = rendered["type"]

    if not body:
        return jsonify({"error": "No message body or template"}), 400

    # Send the SMS
    result = send_sms(to, body, message_type=message_type, first_name=first_name)

    # Log to Pipedrive if send succeeded
    if result.get("success") and person_id:
        log_sms_to_pipedrive(
            person_id=person_id,
            direction="outbound",
            body=body,
            message_sid=result.get("message_sid", ""),
            status=result.get("status", ""),
        )

    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)


# ─────────────────────────────────────────────
# API: Log Inbound SMS to Pipedrive
# ─────────────────────────────────────────────
@pipedrive_sms_bp.route("/api/pipedrive/log-inbound", methods=["POST"])
def log_inbound_to_pipedrive():
    """
    Log an inbound SMS to the matching Pipedrive person.
    Called internally after inbound webhook processes the message.

    Expected JSON body:
    {
        "from": "+19035551234",
        "body": "Yes I'm interested",
        "message_sid": "SM...",
        "classification": "general"
    }
    """
    data = request.get_json(silent=True) or {}
    sender = data.get("from", "")
    body = data.get("body", "")
    message_sid = data.get("message_sid", "")
    classification = data.get("classification", "")

    person = find_person_by_phone(sender)
    if not person:
        return jsonify({"status": "no_match", "phone": sender})

    person_id = person.get("id")
    log_sms_to_pipedrive(
        person_id=person_id,
        direction="inbound",
        body=f"[{classification}] {body}",
        message_sid=message_sid,
        status="received",
    )

    # Update opt fields if applicable
    if classification == "opt_out":
        update_sms_opt_fields(person_id, "opt_out")
    elif classification == "opt_in":
        update_sms_opt_fields(person_id, "opt_in")

    return jsonify({"status": "logged", "person_id": person_id})


# ─────────────────────────────────────────────
# API: List Message Templates
# ─────────────────────────────────────────────
@pipedrive_sms_bp.route("/api/twilio/templates", methods=["GET"])
def get_templates():
    """List available message templates. Optional query: ?type=lead_followup"""
    msg_type = request.args.get("type")
    templates = list_templates(msg_type)
    return jsonify({"templates": templates})
