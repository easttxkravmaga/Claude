# Twilio SMS Implementation — Technical Reference

## Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────┐
│  Pipedrive CRM  │◄───►│  Flask API   │◄───►│  Twilio API  │
│  (contacts,     │     │  (Cloud Run) │     │  (SMS send/  │
│   notes, deals) │     │              │     │   receive)   │
└─────────────────┘     └──────────────┘     └──────────────┘
                              │
                        ┌─────┴─────┐
                        │ Webhooks  │
                        │ /inbound  │
                        │ /status   │
                        └───────────┘
```

## Files

| File | Purpose |
|---|---|
| `backend/twilio_sms.py` | Core SMS module: webhooks, send logic, opt-out, signature verification |
| `backend/message_templates.py` | Pre-approved message templates and compliance copy |
| `backend/pipedrive_sms.py` | Pipedrive integration: contact lookup, note logging, send-by-person |

## API Endpoints

### Twilio Webhooks (called by Twilio)

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/twilio/inbound-sms` | POST | Receive inbound SMS from Twilio |
| `/api/twilio/status-callback` | POST | Receive delivery status updates |

### Internal / Integration APIs

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/twilio/send` | POST | Send an SMS (direct) |
| `/api/twilio/opt-in` | POST | Register opt-in for a phone number |
| `/api/twilio/opt-status/<phone>` | GET | Check opt-in/opt-out status |
| `/api/twilio/messages` | GET | View message log (?limit=50) |
| `/api/twilio/templates` | GET | List message templates (?type=lead_followup) |
| `/api/pipedrive/send-sms` | POST | Send SMS to Pipedrive contact |
| `/api/pipedrive/log-inbound` | POST | Log inbound SMS to Pipedrive person |

## Send SMS — Direct API

```json
POST /api/twilio/send
{
    "to": "+19035551234",
    "first_name": "Sarah",
    "body": "Hi [First Name], this is East Texas Krav Maga...",
    "message_type": "lead_followup",
    "opt_in_source": "website_form"
}
```

## Send SMS — Via Pipedrive Contact

```json
POST /api/pipedrive/send-sms
{
    "person_id": 123,
    "template": "lead_followup_initial",
    "date": "Thursday, April 17",
    "time": "6:30 PM"
}
```

Or with custom body:

```json
POST /api/pipedrive/send-sms
{
    "to": "+19035551234",
    "first_name": "Sarah",
    "body": "Custom message here. Reply STOP to opt out.",
    "message_type": "student_update"
}
```

## Logic Rules Enforced

1. **Never send without opt-in** — Every send checks `has_valid_opt_in(phone)`. Sends are blocked if no opt-in source is recorded.
2. **Immediate opt-out on STOP** — When STOP is received inbound, the number is added to the suppression set immediately.
3. **START re-subscribe** — When START is received, the number is removed from the suppression set.
4. **Outbound logging** — Every send logs: recipient, body, type, timestamp, status, Twilio SID.
5. **Inbound logging** — Every receive logs: sender, body, timestamp, classification, Twilio SID.
6. **Business identification** — All templates identify "East Texas Krav Maga" by name.

## Message Types

| Type | Use |
|---|---|
| `lead_followup` | Trial class follow-up, initial lead response |
| `appointment` | Scheduling, reminders, confirmations |
| `student_update` | Onboarding, schedule changes, student communication |
| `promotion` | Offers, membership deals (opted-in contacts only) |
| `event` | Seminar announcements, CBLTAC, workshops |
| `general` | Other compliant communication |

## Available Templates

| Key | Type | Description |
|---|---|---|
| `lead_followup_initial` | lead_followup | Initial lead follow-up |
| `lead_followup_trial` | lead_followup | Trial class invitation |
| `appointment_reminder` | appointment | Appointment reminder |
| `appointment_confirmation` | appointment | Appointment confirmation |
| `student_welcome` | student_update | New student welcome |
| `student_schedule_change` | student_update | Schedule change notice |
| `promotion_seminar` | promotion | Seminar / training offer |
| `event_reminder` | event | Event reminder |
| `event_cbltac` | event | CBLTAC event notification |

## Merge Fields

Templates support these placeholders:
- `[First Name]` — Contact first name
- `[Date]` — Date string
- `[Time]` — Time string
- `[Event Name]` — Event name

## Pipedrive Integration

### Outbound Flow
1. Trigger from Pipedrive webhook, Make.com scenario, or direct API call
2. Look up person by ID or phone number
3. Check opt-in status and opt-out suppression
4. Send via Twilio API through Messaging Service
5. Log delivery status back as Pipedrive note on person record
6. Update Sakari Opt In / Opt Out date fields as needed

### Inbound Flow
1. Twilio sends POST to `/api/twilio/inbound-sms`
2. Message classified (opt_out, opt_in, help, general)
3. Opt-out/opt-in handled immediately
4. Forward to `/api/pipedrive/log-inbound` to match sender to Pipedrive person
5. Create note on person record with message content and classification
6. Update SMS opt fields on person record

### Pipedrive Custom Fields Used

| Field | Key | Purpose |
|---|---|---|
| Sakari Opt In | `8cae8f528afa52fd268f` | Date of SMS opt-in |
| Sakari Opt Out | `624eeb304949f6989717` | Date of SMS opt-out |

These existing Pipedrive fields (originally for Sakari) are reused for Twilio SMS consent tracking.

## Security

- All Twilio webhooks verify the `X-Twilio-Signature` header using HMAC-SHA1
- Auth token is stored as environment variable on Cloud Run
- Send API endpoints should be protected with your own auth (API key, internal network, etc.)

## Production Considerations

The current implementation uses in-memory stores for opt-out lists and message logs. For production:

1. **Opt-out list** — Persist to database (Firestore, Cloud SQL, or Pipedrive custom fields)
2. **Message log** — Persist to database or logging service
3. **Opt-in registry** — Persist to database; current Pipedrive Sakari Opt In field can serve as source of truth
4. **Rate limiting** — Add rate limiting to send endpoints
5. **Auth** — Add API key or JWT auth to internal send endpoints
