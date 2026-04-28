---
name: square-integration-intelligence
version: 1.0
updated: 2026-04-28
description: >
  Complete Square API intelligence for building any Square integration — payments,
  customers, invoices, subscriptions, webhooks, and the Pipedrive bidirectional sync.
  Load this skill any time Square is in scope: building n8n workflows that touch Square,
  designing the Pipedrive contact sync, handling missed payments or subscription
  deactivations, configuring Square webhooks, or debugging any Square API behavior.
  Contains decision trees, named protocols, and failure-first rules that prevent the
  most common integration-breaking mistakes.
triggers:
  - "Square"
  - "Square API"
  - "Square customer"
  - "Square payment"
  - "Square invoice"
  - "Square subscription"
  - "Square webhook"
  - "Square integration"
  - "Square Pipedrive"
  - "Pipedrive Square sync"
  - "bidirectional sync"
  - "missed payment"
  - "failed payment"
  - "subscription deactivated"
  - "invoice failed charge"
  - "Square n8n"
  - "Square customer upsert"
  - "Square contact matching"
  - "Square HMAC"
  - "Square signature verification"
  - "Square PAT"
  - "Square OAuth"
  - "ACH payment"
  - "Square sandbox"
  - "Square error"
  - "Square rate limit"
dependencies:
  - n8n-workflow-intelligence (load when building n8n workflows that execute Square calls)
  - etkm-crm-operations (load when Square sync touches Pipedrive pipelines or deal stages)
  - etkm-notion-intelligence (load when Square intelligence records in Notion are in scope)
---

# Square Integration Intelligence

## Purpose

Prevents the integration-breaking mistakes that cost hours to debug. Provides
decision trees for auth, customer matching, webhook handling, and payment state
machines so Claude can build Square integrations correctly on the first attempt.

The Notion record (Platform Intelligence Hub → Square) and the DOCX in Drive
(AI Resources / Platform Intelligence / Square /) hold the full reference. This
skill holds what Claude needs to execute — the operational rules, protocols,
and failure modes that govern every Square build.

---

## When to Load

Load this skill whenever:
- Any Square API endpoint, webhook, or customer operation is in scope
- Building or debugging any n8n workflow that touches Square
- Designing or modifying the Pipedrive ↔ Square bidirectional sync
- Handling missed payments, failed invoices, or deactivated subscriptions
- Setting up Square webhook subscriptions or verifying signatures
- Working with Square customer custom attributes or cross-system ID storage
- Diagnosing a Square API error or unexpected behavior
- Reviewing Square changelog for version impact on existing workflows

---

## Rule 1 — Authentication Decision Tree

**Never guess. Use this tree every time.**

```
What are you doing?
│
├── Managing webhook subscriptions (create/list/delete)?
│   └── USE PAT — OAuth tokens are explicitly REJECTED by Webhook Subscriptions API
│
├── Recovering missed events via Events API?
│   └── USE PAT — same rule, same rejection behavior
│
├── Acting on a third-party seller account (App Marketplace, multi-seller)?
│   └── USE OAuth 2.0 — PAT only covers your own account
│
└── Acting on ETKM's own Square seller account?
    └── PAT is fine — simpler than OAuth for single-account operations
```

**OAuth token lifecycle (non-negotiable):**
- Access tokens expire in 30 days. Refresh proactively every ≤7 days.
- Auth codes expire in 5 minutes — exchange immediately after receipt.
- Refresh tokens are long-lived. Treat like passwords. Rotate if exposed.
- Subscribe to `oauth.authorization.revoked` to detect seller disconnections.

---

## Rule 2 — Customer Matching Protocol

**Always execute in this exact order. Never skip to CreateCustomer.**

```
STEP 1: POST /v2/customers/search
        filter: { email_address: { exact: email.toLowerCase() } }
        ├── 1 match  → use customer_id. DONE.
        ├── 2+ match → STOP. Route to manual review queue. Log conflict.
        └── 0 match  → proceed to STEP 2

STEP 2: POST /v2/customers/search
        filter: { phone_number: { exact: toE164(phone) } }
        ├── 1 match  → use customer_id. DONE.
        ├── 2+ match → STOP. Route to manual review queue. Log conflict.
        └── 0 match  → proceed to STEP 3

STEP 3: CreateCustomer
        idempotency_key: uuidv5(email.toLowerCase())
        → Immediately write cross-system IDs to BOTH systems (see Rule 3)
```

**Phone normalization (required before any Square phone operation):**
- Target format: E.164 — `+19035551234`
- Strip all non-digits, prepend `+1` for US 10-digit numbers
- Pass E.164 strings only. Square rejects other formats silently.

**On UpdateCustomer:** Always pass `version` from the retrieved record.
Mismatched version → CONFLICT / VERSION_MISMATCH error.
Pattern: Retrieve → capture version → update → pass version. Retry once on mismatch.

---

## Rule 3 — Cross-System ID Storage

**Write both directions on first link. Never leave a one-way reference.**

```
Square Customer  →  reference_id = Pipedrive Person ID (string)
                    OR custom attribute 'pipedrive_person_id' (VISIBILITY_HIDDEN)
                    Use custom attribute when reference_id is reserved

Pipedrive Person →  custom field 'square_customer_id' = Square Customer ID
```

**Custom attributes critical note:** NOT returned in standard `RetrieveCustomer`
or `ListCustomers` responses. Must call `ListCustomerCustomAttributes` separately,
or use Square GraphQL which includes custom attributes on the Customer object.

---

## Rule 4 — Webhook Verification Protocol (n8n)

**Failure point: n8n re-serializes the webhook body by default, breaking HMAC.**

**Required n8n Webhook node configuration:**
- Response Mode: Respond Immediately (200 OK — must reply within 10 seconds)
- Raw Body: **ENABLED** ← this is the critical setting. Without it, HMAC always fails.
- Authentication: None (verify manually in Code node)

**HMAC-SHA256 verification Code node:**
```javascript
const crypto = require('crypto');
const sigKey  = $env.SQUARE_WEBHOOK_SIG_KEY;
const url     = 'https://your-n8n-instance.com/webhook/square';

// Raw body preserved because Raw Body mode is ON
const rawBody = $input.first().binary?.data
  ? Buffer.from($input.first().binary.data, 'base64').toString()
  : JSON.stringify($input.first().json.body);

const expected = crypto
  .createHmac('sha256', sigKey)
  .update(url + rawBody)
  .digest('base64');

const received = $input.first().json.headers['x-square-hmacsha256-signature'];

if (!crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(received))) {
  throw new Error('Invalid Square webhook signature');
}
return $input.first();
```

**After verification, always dedup by `event_id`:**
Webhooks fire more than once. Store event IDs for 24+ hours.
Duplicate event_id = skip processing entirely.

---

## Rule 5 — ACH State Machine

**ACH payments are asynchronous. PENDING ≠ confirmed revenue.**

```
On payment.created where status=PENDING:
  → Store payment_id + created_at
  → Log Pipedrive note: "ACH payment initiated — pending bank confirmation"
  → Do NOT count as revenue. Do NOT trigger fulfillment.

On payment.updated where status=COMPLETED:
  → Confirm revenue
  → Log Pipedrive note: "ACH payment confirmed — $[amount] — [date]"
  → Trigger fulfillment if applicable

On payment.updated where status=FAILED:
  → Log Pipedrive note: "ACH payment FAILED — [date]"
  → Set Deal label: Payment Issue
  → Create Activity: Follow up on failed ACH payment
```

Resolution timeline: minutes to days. Never assume a PENDING ACH will complete.

---

## Rule 6 — Missed Payment Architecture

**Wire all three events. Each serves a different failure scenario.**

```
invoice.scheduled_charge_failed
  → Auto-payment for invoice or subscription charge failed
  → Action: Note on Person/Deal + Deal label "Payment Issue" + Activity (next biz day)
  → Note: No error detail in payload. Provider doesn't share decline reason.

subscription.updated where status=DEACTIVATED
  → Subscription auto-deactivated by Square
  → Action: Call ListSubscriptionEvents to get deactivation reason FIRST
  → Then: Note + Deal label "At Risk" + Activity
  → Deactivation triggers: email removed, name removed, customer deleted,
    location deactivated, location risk-blocked, persistent billing failure

payment.updated where status=FAILED (non-ACH)
  → Direct card payment declined
  → Action: Note + Activity. Surface to customer — do not auto-retry.
```

---

## Rule 7 — Bidirectional Sync Loop Prevention

**Without a watermark, Square→Pipedrive→Square→Pipedrive loops infinitely.**

```
Write to Square:  store last_pipedrive_sync = ISO timestamp in Customer note
                  or custom attribute
Write to Pipedrive: store last_square_sync = ISO timestamp in Person custom field

On receiving any webhook:
  IF source_system.updated_at ≤ target_system.last_sync_timestamp + 30 seconds
    THEN skip — this is our own echo
  ELSE process normally
```

---

## Rule 8 — n8n Credential & Version Setup

**Every Square HTTP Request node in n8n requires both of these:**

```
Credential: Header Auth
  Name:  Authorization
  Value: Bearer {PAT or OAuth access_token}

Manual header on each node:
  Name:  Square-Version
  Value: 2026-01-22

Storage: n8n Credential Vault — never inline tokens in workflow JSON
Naming:  "Square API - Production" and "Square API - Sandbox" (strictly separate)
```

---

## Rule 9 — Rate Limit Handling

**Square returns HTTP 429. No published rate limit table.**

```
n8n HTTP Request node settings:
  Retry On Fail: true
  Max Tries:     5
  Wait Between:  1000ms base (exponential + ±25% jitter)

Retry on:  429, 500, 503
Terminal:  4xx (except 429) — do not retry, log and alert
Special:   409 VERSION_MISMATCH — re-fetch version, retry once only
```

---

## Rule 10 — Invoice Rules (Non-Negotiable)

- **Cannot pay invoice via API** — buyers must use `public_url` hosted page
- **`public_url` expires** (since 2025-04-16) — re-fetch invoice before every send
- **Link expiry does NOT trigger `invoice.updated`** — do not rely on webhook to detect
- **Always re-fetch before sharing** — never cache public_url

**Overdue detection (Square does not auto-flag):**
After due_date: retrieve invoice, compare `computed_amount_money` vs
`total_completed_amount_money`. If computed > completed → overdue.

---

## Rule 11 — Subscription Status Guards

**COMPLETED subscriptions reject all mutations (API 2025-09-24+)**

```
Before any subscription mutation (pause, resume, swap_plan, cancel):
  IF subscription.status == 'COMPLETED'
    THEN skip — returns HTTP 400 on any mutation attempt
  IF subscription.status == 'DEACTIVATED'
    THEN investigate reason via ListSubscriptionEvents before acting
```

---

## Rule 12 — API Version and Retired Fields

**Always set `Square-Version: 2026-01-22` on every request.**

**Retired and deprecated fields (do not use):**
- `Customer.cards` — retired in API 2025-01-23+. Returns null. Use `ListCards?customer_id=...`
- `labor.shift.*` webhooks — deprecated at 2025-05-21. Use `labor.timecard.*` instead.
- Reader SDK — retired December 31, 2025. Use Mobile Payments SDK.

---

## Key Webhook Events (ETKM-Relevant)

```
customer.created / .updated / .deleted     — contact sync triggers
payment.created / .updated                 — payment lifecycle
invoice.payment_made                       — successful invoice payment
invoice.scheduled_charge_failed            — ← primary missed payment trigger
subscription.created / .updated            — membership lifecycle
payout.sent / .paid / .failed              — banking health monitoring
oauth.authorization.revoked                — seller disconnect detection
```

**PAT required for:** Webhook Subscriptions API, Events API (28-day recovery window)
**Retry schedule:** Up to 11 retries / 24 hours / exponential backoff

---

## Sandbox Reference (Quick)

```
Test nonces (source_id in CreatePayment):
  cnon:card-nonce-ok              → success
  cnon:card-nonce-declined        → CARD_DECLINED
  cnon:card-nonce-rejected-cvv    → CVV_FAILURE

Test card numbers (Web Payments SDK):
  Visa:       4111 1111 1111 1111
  Mastercard: 5105 1051 0510 5100
  Any future expiration, any CVV, postal 94103

Sandbox token rule: NEVER use sandbox tokens in production (returns UNAUTHORIZED)
OAuth Sandbox: must have Sandbox Dashboard open in separate tab for auth flow
```

---

## Error Handling Quick Reference

```
401 ACCESS_TOKEN_EXPIRED    → Refresh OAuth token, retry
401 UNAUTHORIZED            → Check PAT vs OAuth — wrong auth type
403 INSUFFICIENT_SCOPES     → Re-prompt OAuth with broader scope
404 NOT_FOUND               → Safe to create new resource
409 VERSION_MISMATCH        → Re-fetch, retry once
422 IDEMPOTENCY_KEY_REUSED  → Generate new UUID, different body used same key
429 RATE_LIMITED            → Exponential backoff, max 5 retries
5xx                         → Retry with backoff (idempotency key safe)
CARD_DECLINED + variants    → Terminal. Surface to customer. Never auto-retry.
```

---

## The 5 Failures That Kill Square Integrations

1. **Wrong auth for webhooks** — Webhook Subscriptions API rejects OAuth. Use PAT.
2. **n8n Raw Body disabled** — HMAC breaks when body is re-serialized. Enable it.
3. **Missing Square-Version header** — App runs on stale pinned version silently.
4. **CreateCustomer without search** — Square does not deduplicate. Duplicates are permanent.
5. **ACH PENDING treated as complete** — Funds have not moved. Wait for payment.updated COMPLETED.

---

## What Not to Do

- Never use OAuth for the Webhook Subscriptions API or Events API
- Never call CreateCustomer without running the 3-step matching protocol first
- Never inline Square tokens in n8n workflow JSON — use Credential Vault
- Never assume invoice `public_url` is still valid — always re-fetch before sending
- Never treat ACH `PENDING` as confirmed revenue
- Never skip `event_id` deduplication — webhooks fire more than once
- Never build bidirectional sync without the loop prevention watermark
- Never mix Sandbox and Production credentials — name them explicitly
- Never read Customer custom attributes from standard Customer responses — call separately
- Never attempt to pay an invoice via the API — route buyer to `public_url`
- Never mutate a COMPLETED subscription (API 2025-09-24+) — check status first
- Never read `Customer.cards` on API version 2025-01-23+ — field is retired

---

## Recovery

**HMAC verification failing in n8n:**
First check: is Raw Body mode enabled on the Webhook node? This is the cause
90% of the time. Enable it, redeploy, retest.

**Duplicate Square customers appearing:**
SearchCustomers was bypassed or ran against wrong field. Run a search on email
AND phone against the duplicate records. Merge in Square Dashboard (API cannot merge).
Add the correct cross-system IDs to the surviving record.

**Subscription deactivated, reason unknown:**
Call `GET /v2/subscriptions/{id}/events`. Find the DEACTIVATE_SUBSCRIPTION event.
Read `info.reason`. Most common: email removed from customer profile, persistent billing failure.

**VERSION_MISMATCH on UpdateCustomer:**
Do not retry with the cached version. Call `GET /v2/customers/{id}`, capture the
new `version`, then retry the update with the fresh version.

**ACH payment stuck in PENDING:**
Normal — can take minutes to days. Set a monitoring task in Pipedrive. Check back
after 3 business days. If still PENDING after 5 business days, investigate via Square Dashboard.

**Idempotency key reused error:**
A different request body was sent with the same key. Generate a new UUID v4.
Never reuse a key with any modified fields.

---

## Related Skills

Load alongside this skill when relevant:
- `n8n-workflow-intelligence` — always load when building n8n workflows for Square
- `etkm-crm-operations` — load when sync touches Pipedrive pipelines, stages, or labels
- `etkm-notion-intelligence` — load when updating the Platform Intelligence Hub record
