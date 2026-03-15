"""
ETKM SMS Message Templates
Pre-approved, compliant message templates for East Texas Krav Maga.
All templates identify the business and include opt-out language.
"""

# ─────────────────────────────────────────────
# Message Templates
# ─────────────────────────────────────────────
TEMPLATES = {
    # ── Lead Follow-Up ──
    "lead_followup_initial": {
        "type": "lead_followup",
        "name": "Initial Lead Follow-Up",
        "body": (
            "Hi [First Name], this is East Texas Krav Maga. Thanks for reaching out "
            "about training. We'd be happy to help you get started and answer any "
            "questions. Reply STOP to opt out."
        ),
    },
    "lead_followup_trial": {
        "type": "lead_followup",
        "name": "Trial Class Invitation",
        "body": (
            "Hi [First Name], this is East Texas Krav Maga. We'd love to get you "
            "in for a free trial class. Would you like to schedule one? Reply STOP "
            "to opt out."
        ),
    },

    # ── Appointment / Scheduling ──
    "appointment_reminder": {
        "type": "appointment",
        "name": "Appointment Reminder",
        "body": (
            "Hi [First Name], this is East Texas Krav Maga reminding you about your "
            "upcoming class/trial/seminar on [Date] at [Time]. Reply HELP for help "
            "or STOP to opt out."
        ),
    },
    "appointment_confirmation": {
        "type": "appointment",
        "name": "Appointment Confirmation",
        "body": (
            "Hi [First Name], your session at East Texas Krav Maga is confirmed for "
            "[Date] at [Time]. See you there! Reply STOP to opt out."
        ),
    },

    # ── Student Updates ──
    "student_welcome": {
        "type": "student_update",
        "name": "New Student Welcome",
        "body": (
            "Hi [First Name], welcome to East Texas Krav Maga! We're excited to have "
            "you training with us. Reach out anytime if you have questions. Reply STOP "
            "to opt out."
        ),
    },
    "student_schedule_change": {
        "type": "student_update",
        "name": "Schedule Change Notice",
        "body": (
            "Hi [First Name], East Texas Krav Maga here with an update to the training "
            "schedule. Please check our website or reply for details. Reply STOP to opt out."
        ),
    },

    # ── Promotions / Events ──
    "promotion_seminar": {
        "type": "promotion",
        "name": "Seminar / Training Offer",
        "body": (
            "Hi [First Name], East Texas Krav Maga here. We have an upcoming seminar "
            "and a limited-time training offer for opted-in contacts. Let us know if "
            "you'd like details. Reply STOP to opt out."
        ),
    },
    "event_reminder": {
        "type": "event",
        "name": "Event Reminder",
        "body": (
            "Hi [First Name], East Texas Krav Maga here. Reminder: [Event Name] is "
            "coming up on [Date]. Don't miss it! Reply STOP to opt out."
        ),
    },
    "event_cbltac": {
        "type": "event",
        "name": "CBLTAC Event Notification",
        "body": (
            "Hi [First Name], East Texas Krav Maga here. Our next CBLTAC seminar is "
            "on [Date]. Spots are limited — reply for details or register at "
            "etxkravmaga.com. Reply STOP to opt out."
        ),
    },
}


# ─────────────────────────────────────────────
# Template Helpers
# ─────────────────────────────────────────────
def get_template(template_key):
    """Get a message template by key."""
    return TEMPLATES.get(template_key)


def list_templates(message_type=None):
    """List all templates, optionally filtered by type."""
    if message_type:
        return {k: v for k, v in TEMPLATES.items() if v["type"] == message_type}
    return TEMPLATES


def render_template(template_key, **kwargs):
    """
    Render a template with merge fields.

    Supported merge fields:
        [First Name], [Date], [Time], [Event Name]

    Example:
        render_template("appointment_reminder", first_name="Sarah",
                        date="Thursday, April 17", time="6:30 PM")
    """
    template = TEMPLATES.get(template_key)
    if not template:
        return None

    body = template["body"]
    field_map = {
        "[First Name]": kwargs.get("first_name", "[First Name]"),
        "[Date]": kwargs.get("date", "[Date]"),
        "[Time]": kwargs.get("time", "[Time]"),
        "[Event Name]": kwargs.get("event_name", "[Event Name]"),
    }
    for placeholder, value in field_map.items():
        body = body.replace(placeholder, value)

    return {
        "key": template_key,
        "type": template["type"],
        "name": template["name"],
        "body": body,
    }


# ─────────────────────────────────────────────
# Compliance Auto-Reply Messages
# (Used by Twilio Advanced Opt-Out on Messaging Service)
# ─────────────────────────────────────────────
AUTO_REPLIES = {
    "STOP": (
        "You've been unsubscribed from East Texas Krav Maga text messages. "
        "No more messages will be sent. Reply START to re-subscribe."
    ),
    "START": (
        "You've been re-subscribed to East Texas Krav Maga text messages. "
        "Reply STOP to opt out or HELP for help."
    ),
    "HELP": (
        "East Texas Krav Maga: Reply to this message or contact us directly "
        "for help. Reply STOP to opt out."
    ),
}


# ─────────────────────────────────────────────
# Website Form Disclosure Copy
# ─────────────────────────────────────────────
FORM_DISCLOSURE = (
    "By providing your phone number, you agree to receive text messages from "
    "East Texas Krav Maga related to your inquiry, classes, appointments, events, "
    "updates, and occasional offers. Message frequency varies. Message and data "
    "rates may apply. Reply STOP to unsubscribe and HELP for help."
)

FORM_CHECKBOX = "I agree to receive SMS text messages from East Texas Krav Maga."

PRIVACY_NOTE = (
    "SMS consent is not shared with third parties or affiliates for marketing purposes."
)
