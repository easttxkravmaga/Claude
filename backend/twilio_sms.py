"""
ETKM Twilio SMS Module
Handles inbound/outbound SMS, signature verification, opt-out management,
and message logging for East Texas Krav Maga A2P 10DLC compliant messaging.
"""

import os
import json
import hmac
import hashlib
import base64
import logging
from datetime import datetime, timezone
from urllib.parse import urlencode
from functools import wraps

import requests
from flask import Blueprint, request, jsonify, Response

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Environment
# ─────────────────────────────────────────────
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_MESSAGING_SERVICE_SID = os.environ.get("TWILIO_MESSAGING_SERVICE_SID", "")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "")  # E.164 format
PIPEDRIVE_API_KEY = os.environ.get("PIPEDRIVE_API_KEY", "")

# Base URL for webhook signature validation
APP_BASE_URL = os.environ.get("APP_BASE_URL", "")

# ─────────────────────────────────────────────
# In-memory stores (replace with database in production)
# ─────────────────────────────────────────────
# Opt-out list: set of E.164 phone numbers that have opted out
opted_out_numbers = set()

# Message log: list of message records
message_log = []

# Contact opt-in registry: phone -> {"source": str, "timestamp": str}
opt_in_registry = {}

# ─────────────────────────────────────────────
# Blueprint
# ─────────────────────────────────────────────
twilio_bp = Blueprint("twilio", __name__)


# ─────────────────────────────────────────────
# Twilio Signature Verification
# ─────────────────────────────────────────────
def validate_twilio_signature(f):
    """Decorator to verify Twilio request signatures."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not TWILIO_AUTH_TOKEN:
            logger.warning("TWILIO_AUTH_TOKEN not set — skipping signature validation")
            return f(*args, **kwargs)

        signature = request.headers.get("X-Twilio-Signature", "")
        url = request.url

        # Build param string for POST requests
        if request.method == "POST":
            params = request.form.to_dict()
            # Sort params and append to URL
            sorted_params = sorted(params.items())
            url_with_params = url + "".join(k + v for k, v in sorted_params)
        else:
            url_with_params = url

        # Compute expected signature
        mac = hmac.new(
            TWILIO_AUTH_TOKEN.encode("utf-8"),
            url_with_params.encode("utf-8"),
            hashlib.sha1,
        )
        expected = base64.b64encode(mac.digest()).decode("utf-8")

        if not hmac.compare_digest(signature, expected):
            logger.warning("Twilio signature validation failed")
            return Response("Forbidden", status=403)

        return f(*args, **kwargs)
    return decorated


# ─────────────────────────────────────────────
# Message Logging
# ─────────────────────────────────────────────
def log_message(direction, phone_number, body, message_sid="",
                status="", message_type="", classification=""):
    """Log an inbound or outbound message."""
    record = {
        "direction": direction,
        "phone_number": phone_number,
        "body": body,
        "message_sid": message_sid,
        "status": status,
        "message_type": message_type,
        "classification": classification,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    message_log.append(record)
    logger.info("SMS %s | %s | SID: %s | Status: %s",
                direction, phone_number, message_sid, status)
    return record


# ─────────────────────────────────────────────
# Opt-Out / Opt-In Management
# ─────────────────────────────────────────────
def classify_inbound(body):
    """Classify inbound message as opt-out, opt-in, help, or general."""
    normalized = body.strip().upper()
    if normalized in ("STOP", "STOPALL", "UNSUBSCRIBE", "CANCEL", "END", "QUIT"):
        return "opt_out"
    if normalized in ("START", "YES", "UNSTOP"):
        return "opt_in"
    if normalized in ("HELP", "INFO"):
        return "help"
    return "general"


def handle_opt_out(phone_number):
    """Mark a number as opted out. Suppresses all future sends."""
    opted_out_numbers.add(phone_number)
    logger.info("Opt-out recorded for %s", phone_number)


def handle_opt_in(phone_number):
    """Re-subscribe a number that previously opted out."""
    opted_out_numbers.discard(phone_number)
    logger.info("Opt-in (re-subscribe) recorded for %s", phone_number)


def is_opted_out(phone_number):
    """Check if a phone number has opted out."""
    return phone_number in opted_out_numbers


def register_opt_in(phone_number, source):
    """Register a valid opt-in source for a contact."""
    opt_in_registry[phone_number] = {
        "source": source,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def has_valid_opt_in(phone_number):
    """Check if a phone number has a recorded opt-in source."""
    return phone_number in opt_in_registry


# ─────────────────────────────────────────────
# Outbound SMS
# ─────────────────────────────────────────────
def send_sms(to, body, message_type="general", first_name=""):
    """
    Send an outbound SMS via Twilio API.

    Args:
        to: Recipient phone number in E.164 format
        body: Message text
        message_type: One of lead_followup, appointment, student_update, promotion, event, general
        first_name: Recipient first name for template merge

    Returns:
        dict with send result or error
    """
    # Rule 1: Never send unless valid opt-in recorded
    if not has_valid_opt_in(to):
        logger.warning("Send blocked — no opt-in source for %s", to)
        return {"error": "no_opt_in", "message": "No valid opt-in source recorded for this number"}

    # Rule 2: Never send to opted-out numbers
    if is_opted_out(to):
        logger.warning("Send blocked — %s is opted out", to)
        return {"error": "opted_out", "message": "Recipient has opted out of SMS"}

    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        return {"error": "config", "message": "Twilio credentials not configured"}

    # Merge first name into body if placeholder present
    if first_name:
        body = body.replace("[First Name]", first_name)

    # Build status callback URL
    status_callback = ""
    if APP_BASE_URL:
        status_callback = f"{APP_BASE_URL}/api/twilio/status-callback"

    # Send via Twilio REST API
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    payload = {
        "To": to,
        "Body": body,
        "MessagingServiceSid": TWILIO_MESSAGING_SERVICE_SID,
    }
    if not TWILIO_MESSAGING_SERVICE_SID and TWILIO_PHONE_NUMBER:
        payload.pop("MessagingServiceSid", None)
        payload["From"] = TWILIO_PHONE_NUMBER

    if status_callback:
        payload["StatusCallback"] = status_callback

    try:
        resp = requests.post(
            url,
            data=payload,
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            timeout=15,
        )
        resp.raise_for_status()
        result = resp.json()

        log_message(
            direction="outbound",
            phone_number=to,
            body=body,
            message_sid=result.get("sid", ""),
            status=result.get("status", "queued"),
            message_type=message_type,
        )

        return {
            "success": True,
            "message_sid": result.get("sid"),
            "status": result.get("status"),
            "to": to,
            "message_type": message_type,
        }

    except requests.RequestException as e:
        logger.error("Twilio send failed: %s", e)
        return {"error": "send_failed", "message": str(e)}


# ─────────────────────────────────────────────
# Webhook: Inbound SMS
# ─────────────────────────────────────────────
@twilio_bp.route("/api/twilio/inbound-sms", methods=["POST"])
@validate_twilio_signature
def inbound_sms():
    """
    Receive inbound SMS from Twilio.
    Captures sender, body, timestamp, SID, and opt-out classification.
    Returns empty TwiML when no auto-reply is needed.
    """
    sender = request.form.get("From", "")
    body = request.form.get("Body", "")
    message_sid = request.form.get("MessageSid", "")

    classification = classify_inbound(body)

    # Handle opt-out/opt-in immediately
    if classification == "opt_out":
        handle_opt_out(sender)
    elif classification == "opt_in":
        handle_opt_in(sender)

    log_message(
        direction="inbound",
        phone_number=sender,
        body=body,
        message_sid=message_sid,
        status="received",
        classification=classification,
    )

    # Return empty TwiML — Twilio Advanced Opt-Out handles STOP/START/HELP replies
    return Response(
        '<?xml version="1.0" encoding="UTF-8"?><Response></Response>',
        content_type="application/xml",
    )


# ─────────────────────────────────────────────
# Webhook: Status Callback
# ─────────────────────────────────────────────
@twilio_bp.route("/api/twilio/status-callback", methods=["POST"])
@validate_twilio_signature
def status_callback():
    """
    Receive outbound message status updates from Twilio.
    Logs delivery status: queued, sent, delivered, undelivered, failed.
    """
    message_sid = request.form.get("MessageSid", "")
    message_status = request.form.get("MessageStatus", "")
    to = request.form.get("To", "")
    error_code = request.form.get("ErrorCode", "")

    log_message(
        direction="status_update",
        phone_number=to,
        body=f"Status: {message_status}" + (f" Error: {error_code}" if error_code else ""),
        message_sid=message_sid,
        status=message_status,
    )

    return Response("", status=204)


# ─────────────────────────────────────────────
# API: Send SMS (internal use / Pipedrive trigger)
# ─────────────────────────────────────────────
@twilio_bp.route("/api/twilio/send", methods=["POST"])
def send_sms_endpoint():
    """
    Internal API to send an SMS.

    Expected JSON body:
    {
        "to": "+19035551234",
        "first_name": "Sarah",
        "body": "Hi [First Name], this is East Texas Krav Maga...",
        "message_type": "lead_followup",
        "opt_in_source": "website_form"  // required if contact not already registered
    }
    """
    data = request.get_json(silent=True) or {}
    to = data.get("to", "")
    first_name = data.get("first_name", "")
    body = data.get("body", "")
    message_type = data.get("message_type", "general")
    opt_in_source = data.get("opt_in_source", "")

    if not to or not body:
        return jsonify({"error": "Missing 'to' or 'body'"}), 400

    # Register opt-in if source provided and not already registered
    if opt_in_source and not has_valid_opt_in(to):
        register_opt_in(to, opt_in_source)

    result = send_sms(to, body, message_type=message_type, first_name=first_name)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result)


# ─────────────────────────────────────────────
# API: Register Opt-In
# ─────────────────────────────────────────────
@twilio_bp.route("/api/twilio/opt-in", methods=["POST"])
def register_opt_in_endpoint():
    """
    Register an opt-in for a phone number.

    Expected JSON body:
    {
        "phone_number": "+19035551234",
        "source": "website_contact_form"
    }
    """
    data = request.get_json(silent=True) or {}
    phone = data.get("phone_number", "")
    source = data.get("source", "")

    if not phone or not source:
        return jsonify({"error": "Missing 'phone_number' or 'source'"}), 400

    register_opt_in(phone, source)
    return jsonify({"status": "registered", "phone_number": phone, "source": source})


# ─────────────────────────────────────────────
# API: Check Opt-Out Status
# ─────────────────────────────────────────────
@twilio_bp.route("/api/twilio/opt-status/<phone>", methods=["GET"])
def opt_status(phone):
    """Check opt-in/opt-out status for a phone number."""
    return jsonify({
        "phone_number": phone,
        "opted_out": is_opted_out(phone),
        "has_opt_in": has_valid_opt_in(phone),
        "opt_in_details": opt_in_registry.get(phone),
    })


# ─────────────────────────────────────────────
# API: Message Log (debug / admin)
# ─────────────────────────────────────────────
@twilio_bp.route("/api/twilio/messages", methods=["GET"])
def get_messages():
    """Return recent message log entries. Query param: ?limit=50"""
    limit = int(request.args.get("limit", 50))
    return jsonify({
        "messages": message_log[-limit:],
        "total": len(message_log),
    })
