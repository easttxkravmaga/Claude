---
name: etkm-pipedrive-manus
description: >
  Use this skill for ANY task involving ETKM's Pipedrive CRM setup, Manus automation
  workflows, email sequence implementation, Calendly integration, deal stage logic,
  or the Manus-to-Claude API connection. Trigger whenever the user is building,
  troubleshooting, or planning any part of ETKM's Pipedrive automation — including
  email triggers, deal stage moves, merge tags, arc classification logic, or the
  Claude API system prompt used by Manus. Also trigger when discussing how Claude
  and Manus divide responsibilities, or when writing prompts that Manus will send
  to Claude.
---

# ETKM Pipedrive + Manus System

This skill is the single source of truth for ETKM's CRM automation architecture.
Load it before building or modifying any Pipedrive automation, Manus workflow,
or Claude API integration for ETKM.

---

## Role Division — Non-Negotiable

| Role | Responsibility |
|---|---|
| **Claude** | Writes ALL email copy. Writes the master system prompt. Writes arc-type variant logic. Never implements automation. |
| **Manus** | Implements ALL Pipedrive automation. Reads Calendly notes. Classifies arc types. Calls Claude API. Fires emails. Never rewrites copy. |

If copy needs to change → goes back to Claude.
If automation logic needs to change → Manus handles it.
These lanes do not cross.

---

## Pipedrive — Merge Tag Format

All merge tags use **square brackets** — Pipedrive native format.
Never use `{{handlebars}}` or `{curly_brace}` format — those are Calendly/external formats
and will render as literal text in Pipedrive emails.

### Native Pipedrive Tags Used in ETKM Emails

| Tag | Data | Used In |
|---|---|---|
| `[person_first_name]` | Prospect's first name | All emails |
| `[person_email]` | Prospect's email address | Internal tracking |
| `[activity_due_date]` | Trial lesson date | Email 1, 2, 3 (after Manus maps from note) |
| `[activity_due_time]` | Trial lesson time | Email 1 (after Manus maps from note) |
| `[user_name]` | Sender name (Nate Lundstrom) | Sign-off |
| `[user_phone]` | Sender phone | Sign-off |

### Calendly Data — NOT Native Tags

Calendly sends data as a **note on the person record**, not as native Pipedrive fields.
Manus must read the note and extract:

- Trial date and time
- Event type (Free Trial Lesson / Phone Consultation / Private Lesson)
- Prospect phone number
- Q&A response (free text from: "Please share anything that will help prepare for our meeting.")

These are then used to populate email copy and to schedule Touch 2 and Touch 3 triggers.

---

## Deal Stage Map

| Stage | Name | What It Means | Emails Triggered |
|---|---|---|---|
| Stage 1 | Contact Made | First contact established | None |
| Stage 2 | Qualified | Prospect vetted and confirmed as viable | None |
| Stage 3 | Free Trial Lesson | Calendly booking confirmed | Email 1 (immediate), Email 2 (24hr before), Email 3 (morning of) |
| Stage 4 | Trial Attended | Nate manually moves after confirmed attendance | No email — await next stage move |
| Stage 5 | No Show | Prospect did not attend scheduled trial | Email 4 |
| Stage 6 | Signed Up | Conversion confirmed. Triggers P2 entry + WF-002. | Triggers WF-002 onboarding sequence |
| Stage 7 | Discussed Membership Options | Post-trial membership conversation happened | None — tracking stage |
| Stage 8 | Decision Pending | Prospect is considering — awaiting decision | Email 5 |

### Labels Used

| Label | Applied When |
|---|---|
| Warm Lead | Calendly booking confirmed |
| Arc: Safety | Q&A classification — safety/fear signals |
| Arc: Parent | Q&A classification — family/kids signals |
| Arc: Fitness | Q&A classification — fitness signals |
| Arc: LE/Mil | Q&A classification — law enforcement/military signals |
| Arc: Former MA | Q&A classification — prior martial arts signals |
| Arc: Default | No Q&A response or unclassifiable |

---

## Email Sequence — Complete Map

| # | Email | Trigger | Timing | Word Limit |
|---|---|---|---|---|
| 1 | Booking Confirmation | Calendly note: Free Trial Lesson | Immediate | Under 200 |
| 2 | 24-Hour Reminder | 24hrs before activity date | Automatic | Under 150 |
| 3 | Morning Of | Morning of activity date | 8:00 AM | Under 75 |
| 4 | No-Show Recovery | Nate moves to Stage 5 (No Show) | End of trial day | Under 120 |
| 5 | Post-Visit: Didn't Sign Up | Nate moves to Stage 8 (Decision Pending) | When stage moves | Under 175 |
| 6 | — | **RETIRED — no trigger stage in live system** | — | — |
| 7 | Reschedule Acknowledgment | New Calendly note, different date | Immediate | Under 100 |
| 8 | Cancellation Recovery | Calendly cancellation detected | Immediate | Under 100 |

### Automation Rules

**On reschedule (Email 7):**
Cancel scheduled Touch 2 and Touch 3 tied to old date.
Reschedule Touch 2 to 24hrs before new date.
Reschedule Touch 3 to morning of new date.

**On cancellation (Email 8):**
Cancel all pending Touch 2 and Touch 3 sends immediately.
One email only — no follow-up.
If no rebook in 30 days → move to Stage 5 (No Show).

**On no-show (Email 4):**
One email only.
Nate moves no-show prospects to Stage 5 (No Show), which triggers Email 4.

**Email 6 — Status: RETIRED**
The "Needs Time" stage no longer exists in the live P1 pipeline.
Email 6 has no trigger stage. It is retired pending a decision from
Nate on whether to remap it to Stage 7 (Discussed Membership Options)
or Stage 8 (Decision Pending), or remove it permanently.

**Post-visit tracking (current state):**
Pipedrive has no automatic signal for trial attendance or sign-up.
Nate manually moves deal stage after every trial class.
This is the trigger for all post-visit sequences.

**Post-visit tracking (future state):**
When the ETKM membership intake/waiver form is built, a completed
form submission will become the automatic "Signed Up" trigger.
Build current manual-trigger logic in a way that can be upgraded
without rebuilding the whole sequence.

---

## Google Drive — PDF Asset Hosting

All PDFs delivered via Pipedrive are hosted in Google Drive, not attached to emails.

**Folder structure:**
```
ETKM — Pipedrive Assets/
    ├── Pre-Trial/
    │   └── ETKM_Before_You_Walk_In.pdf
    ├── Post-Trial/
    ├── Onboarding/
    └── Events/
```

**Link format:** Always use `https://drive.google.com/file/d/[FILE_ID]/view`
NOT the `?usp=sharing` version — that can trigger a Google login prompt.

**Permissions:** "Anyone with the link can view" — no Google sign-in required.

**Updating files:** Replace file in Drive using "Manage versions → Upload new version."
The file ID and link stay the same. All future Pipedrive sends automatically
deliver the updated version with no changes to email templates.

**Current assets:**

| File | Drive Folder | Delivered In |
|---|---|---|
| ETKM_Before_You_Walk_In.pdf | Pre-Trial/ | Email 1 |

---

## Manus → Claude API Connection

### Architecture

```
PROSPECT BOOKS
      │
      ▼
MANUS reads Calendly note
      │ extracts: date, time, Q&A
      │ classifies: arc type
      │
      ▼
MANUS calls Claude API ──────────────────────────────────────────────────
      │                                                                  │
      │  POST https://api.anthropic.com/v1/messages                     │
      │  Headers: x-api-key, anthropic-version, content-type            │
      │  Body: model, system prompt, user message with context          │
      │                                                                  │
      ▼                                                                  │
CLAUDE returns personalized email copy ◄──────────────────────────────
      │
      ▼
MANUS inserts copy into Pipedrive email template → sends
```

### API Call Specifications

```
Endpoint:  https://api.anthropic.com/v1/messages
Method:    POST
Headers:
  x-api-key:          [ANTHROPIC_API_KEY — stored as Manus secure variable]
  anthropic-version:  2023-06-01
  content-type:       application/json

Body:
  model:      claude-sonnet-4-6
  max_tokens: 1024
  system:     [ETKM Master System Prompt — see below]
  messages:   [{ role: "user", content: [Manus-constructed prompt] }]
```

### What Manus Sends to Claude (User Message Structure)

```
You are writing [EMAIL NAME] for East Texas Krav Maga.

PROSPECT CONTEXT:
- First name: [person_first_name from Pipedrive]
- Arc type: [classification from Q&A — e.g. "Safety / Adult Women"]
- Q&A response: [raw text from Calendly note, or "none"]
- Trial date: [extracted from Calendly note]
- Trial time: [extracted from Calendly note]
- Email number: [1-8]
- Sequence position: [e.g. "24 hours before trial"]

TASK:
Write Email [number] — [email name] — exactly as specified in the
ETKM email sequence. Apply the arc-type personalization if arc is
not Default. Follow all brand voice rules. Stay under [word count] words.
Sign off as Nate Lundstrom, East Texas Krav Maga, (903) 590-0085.

Return only the email — subject line first, then body. No preamble,
no explanation, no markdown formatting.
```

### API Key Setup

- Create at: console.anthropic.com
- Store as: secure environment variable in Manus — `ANTHROPIC_API_KEY`
- Never hardcode in workflow logic or expose in logs
- Recommended model: `claude-sonnet-4-6` — fast, capable, cost-efficient for email copy

### Error Handling (Manus responsibility)

If Claude API call fails:
- Retry once after 30 seconds
- If second attempt fails: send the static default template (non-personalized version)
- Log the failure for review
- Do not delay the email send — fallback to static copy immediately on second failure

---

## Arc Classification Logic

Manus reads the Q&A response from the Calendly note and classifies
using keyword signal matching. Store classification as a label on
the person record.

| Signal Keywords | Arc Label | Personalization Direction |
|---|---|---|
| fear, safety, nervous, walking alone, parking lot, attacked, unsafe, threatened | Arc: Safety | Safe environment framing — no egos, respected from Day 1 |
| kids, children, family, protect, parent, son, daughter | Arc: Parent | Capability-for-family angle |
| fitness, workout, shape, condition, cardio, athletic, weight | Arc: Fitness | Purpose-built fitness angle |
| military, police, security, officer, law enforcement, guard, veteran, tactical | Arc: LE/Mil | Peer-level, operational tone — no motivational language |
| krav, BJJ, jiu-jitsu, karate, trained, used to train, martial arts, belt | Arc: Former MA | Gap-filling angle — what's different here |
| empty / no match | Arc: Default | Standard sequence, no personalization |

---

## Static Contact Information (Use in All Emails)

```
Nate Lundstrom
East Texas Krav Maga
2918 E. Grande Blvd., Tyler, TX 75707
(903) 590-0085
etxkravmaga.com
```

Note: URL is `etxkravmaga.com` — NOT `easttxkravmaga.com` (common misspelling).

---

## Prohibited Words — All Emails

**Never use:** mastery, dominate, destroy, killer, beast, crush, elite,
warrior (unless directly quoting a student)

**Always use instead:** capable, proficient, prepared, confident, effective,
practical, real, structured

**Format rules:**
- Open every email with `[person_first_name],` — never "Dear" or "Hello"
- No bullet lists in body copy — short paragraphs only
- One CTA per email — never two asks
- No pricing or membership details in Emails 1, 2, 3, 7, or 8
- Sign off as Nate Lundstrom every time

---

## Reference Documents

| Document | Location | Purpose |
|---|---|---|
| ETKM_Trial_Email_Sequence_Complete.docx | Google Drive / Pipedrive Assets | All 8 emails + Manus instructions |
| ETKM_Before_You_Walk_In.pdf | Google Drive / Pre-Trial | Delivered in Email 1 |
| etkm-brand-foundation skill | /mnt/skills/user/ | Brand voice, StoryBrand framework |
| etkm-audience-map skill | /mnt/skills/user/ | All 14 audience segments |
