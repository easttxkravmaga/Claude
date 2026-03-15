# Twilio Sole Proprietor A2P 10DLC Setup — East Texas Krav Maga

Complete step-by-step guide for registering ETKM as a U.S. sole proprietor on Twilio's A2P 10DLC system.

---

## 1. Registration Path

| Field | Value |
|---|---|
| Country | United States |
| Business Type | Sole Proprietor |
| EIN | No EIN available |
| Tax ID Path | Do NOT register as Standard or Low-Volume Standard Brand |
| Registration Route | Twilio Direct Sole Proprietor registration in Console |

This matches Twilio's current sole proprietor guidance for U.S./Canada businesses without a tax ID.

---

## 2. Starter Profile

Enter these fields in the Twilio Console Starter Profile registration:

| Field | Value |
|---|---|
| Profile Name | East Texas Krav Maga - Sole Proprietor |
| First Name | Nathan |
| Last Name | Lundstrom |
| Email | Your main real business/admin email (proper domain preferred) |
| Contact Phone Number | Your regular working phone number |
| Address | Your real U.S. mailing/business address |

**Rules:**
- Do not use a throwaway email.
- Do not invent business details.
- Keep owner/contact identity exactly consistent across all fields.
- As a sole proprietor, the "authorized representative" is you personally.

---

## 3. Sole Proprietor Brand

| Field | Value |
|---|---|
| Brand Type | Sole Proprietor |
| Brand Name | East Texas Krav Maga |
| Business Vertical | Closest fitness/training/education category available |
| Mobile Phone Number (OTP) | Nathan's current T-Mobile cell number |

**CRITICAL:** The OTP verification number must be a valid U.S. or Canadian mobile device you own. It CANNOT be a Twilio-purchased number or any CPaaS number.

---

## 4. Campaign Registration

### Use Case Selection

**Recommended:** MIXED

Reason: ETKM will send trial class follow-ups, student reminders, schedule confirmations, and occasional promos/event announcements. Mixed covers multiple use cases like customer care plus delivery/other categories.

Note: Mixed campaigns can have lower throughput and higher cost than narrower use cases.

**Alternative:** If you want easier approval, choose a customer-care-oriented use case and exclude discounts/promotions from initial campaign description and sample messages.

### Campaign Description

> East Texas Krav Maga uses SMS to communicate with prospects, trial students, current students, and customers who have opted in through our website forms, lead forms, event registrations, in-person signups, or direct request for communication. Messages include trial class follow-up, scheduling and appointment coordination, event reminders, student support, onboarding information, seminar updates, and occasional promotional offers related to classes, memberships, workshops, and special events. Message frequency varies based on the customer's inquiry, enrollment status, and ongoing relationship with the business.

### Message Flow / Consent Description

> Customers opt in by submitting a website form, requesting information about classes or seminars, registering for events, completing a lead form, responding to an invitation to continue the conversation by text, or providing their number in person and agreeing to receive text communication from East Texas Krav Maga. SMS consent is not shared with third parties or affiliates for marketing purposes. Message frequency varies. Message and data rates may apply. Reply STOP to opt out and HELP for help.

### Opt-In Workflow Description

> Opt-in is collected through website contact forms, trial lesson request forms, seminar registration forms, lead capture forms, and direct customer request for text communication. The opt-in language appears near the phone number field and states that by providing a mobile number, the customer agrees to receive SMS messages from East Texas Krav Maga related to inquiries, appointments, classes, updates, and offers. Customers may reply STOP to opt out or HELP for help.

---

## 5. Sample Messages

Submit exactly these:

**Sample 1:**
> Hi [First Name], this is East Texas Krav Maga. Thanks for reaching out about training. We'd be happy to help you get started and answer any questions. Reply STOP to opt out.

**Sample 2:**
> Hi [First Name], this is East Texas Krav Maga reminding you about your upcoming class/trial/seminar on [Date] at [Time]. Reply HELP for help or STOP to opt out.

**Sample 3:**
> Hi [First Name], East Texas Krav Maga here. We have an upcoming seminar and a limited-time training offer for opted-in contacts. Let us know if you'd like details. Reply STOP to opt out.

**Do NOT submit samples that:**
- Look like personal texting
- Hide the business identity
- Mention OTP/2FA
- Conflict with the chosen campaign type

---

## 6. Phone Number

| Setting | Value |
|---|---|
| Type | Local U.S. long-code number |
| Area Code Preference | 903 (Tyler/East Texas), or nearest local code |
| Capability | SMS + MMS preferred |
| Attach To | ETKM SMS Main Messaging Service |

---

## 7. Messaging Service

| Setting | Value |
|---|---|
| Name | ETKM SMS Main |
| Use Case | One service for all current compliant ETKM texting |
| Sender Pool | The one approved local Twilio number |

---

## 8. Advanced Opt-Out Configuration

Set these on the Messaging Service:

**STOP reply:**
> You've been unsubscribed from East Texas Krav Maga text messages. No more messages will be sent. Reply START to re-subscribe.

**START reply:**
> You've been re-subscribed to East Texas Krav Maga text messages. Reply STOP to opt out or HELP for help.

**HELP reply:**
> East Texas Krav Maga: Reply to this message or contact us directly for help. Reply STOP to opt out.

---

## 9. Website Form Language

Place this near any form that collects a phone number:

> By providing your phone number, you agree to receive text messages from East Texas Krav Maga related to your inquiry, classes, appointments, events, updates, and occasional offers. Message frequency varies. Message and data rates may apply. Reply STOP to unsubscribe and HELP for help.

Add a checkbox:

> [ ] I agree to receive SMS text messages from East Texas Krav Maga.

Add to privacy policy or page:

> SMS consent is not shared with third parties or affiliates for marketing purposes.

---

## 10. Webhook Configuration

| Webhook | URL Path | Method |
|---|---|---|
| Incoming Message | /api/twilio/inbound-sms | POST |
| Status Callback | /api/twilio/status-callback | POST |

Configure the Incoming Message webhook on the Messaging Service in Twilio Console.
Configure the Status Callback URL on each outbound API call (handled automatically by the code).

---

## 11. Environment Variables Required

Set these on Google Cloud Run:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_MESSAGING_SERVICE_SID=MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1903XXXXXXX
APP_BASE_URL=https://your-cloud-run-url.run.app
```

---

## 12. Minimum Twilio Resources Checklist

- [ ] 1 Twilio account/project for ETKM
- [ ] 1 approved Starter Profile
- [ ] 1 approved Sole Proprietor Brand
- [ ] 1 approved Campaign (Mixed use case)
- [ ] 1 Messaging Service (ETKM SMS Main)
- [ ] 1 purchased local Twilio number in the sender pool
- [ ] 1 inbound webhook endpoint configured
- [ ] 1 status callback endpoint configured

---

## 13. Common Mistakes to Avoid

- Do NOT use vague campaign text like "marketing texts"
- Do NOT say customers opt in "verbally only" unless that is truly documented and supported
- Do NOT submit sample messages that don't match the campaign description
- Do NOT use a Twilio number for the sole proprietor OTP mobile verification
- Do NOT send promotional texts to leads who only asked a one-time question unless they actually opted into recurring SMS
- Do NOT rely on manual memory for opt-outs — enforce suppression in code

---

## 14. Acceptance Checklist

- [ ] Twilio sole proprietor registration approved
- [ ] One local number purchased and linked to Messaging Service
- [ ] Campaign approved and attached to sender
- [ ] Inbound SMS received at webhook successfully
- [ ] Outbound status callbacks logged successfully
- [ ] STOP/START/HELP handled correctly
- [ ] One test contact can receive a compliant ETKM text
- [ ] All sends suppressed after STOP
- [ ] Pipedrive-ready outbound and inbound mapping documented
