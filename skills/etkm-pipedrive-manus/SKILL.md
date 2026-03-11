---
name: etkm-pipedrive-manus
description: >
  Use this skill for ANY task involving ETKM's Pipedrive CRM setup, Manus automation
  workflows, email sequence implementation, Calendly integration, deal stage logic,
  or the Manus-to-Claude API connection. Trigger whenever the user is building,
  troubleshooting, or planning any part of ETKM's Pipedrive automation — including
  email triggers, deal stage moves, merge tags, arc classification logic, or the
  Claude API system prompt used by Manus. Also trigger when discussing how Claude,
  Manus, and Cowork divide responsibilities, or when writing prompts that Manus
  will send to Claude. Load etkm-crm-doctrine for full pipeline and label reference.
---

# ETKM Pipedrive + Manus Automation System

**Version:** 2.0
**Last Updated:** 2026-03-11
**Stage IDs verified against live Pipedrive via API.**

---

## ROLE DIVISION — NON-NEGOTIABLE

| Role | Responsibility |
|------|--------------|
| Claude | Writes ALL email copy. Writes all system prompts. Never implements automation. |
| Manus | Implements ALL Pipedrive automation. Calls Claude API. Fires emails. Never rewrites copy. |
| Claude Code | Builds and maintains Railway/MCP endpoints. Scripts and API integrations. |
| Cowork | Monitors Google Drive /Status/ folder. Confirms receipts. Alerts Nathan. |

Copy changes → Claude. Automation logic changes → Manus. Scripts → Claude Code.

---

## PIPEDRIVE MERGE TAG FORMAT

All merge tags use **[square brackets]** — Pipedrive native format only.
Never use {{handlebars}} or {curly_brace} — those render as literal text.

| Tag | Data |
|-----|------|
| [person_first_name] | Prospect/student first name |
| [person_email] | Email address |
| [activity_due_date] | Trial lesson date |
| [activity_due_time] | Trial lesson time |
| [user_name] | Nate Lundstrom |
| [user_phone] | (903) 590-0085 |

---

## ACQ-WF-001 — PRE-TRIAL FUNNEL

### Trigger Stages (verified P1 IDs)

| Stage ID | Stage Name | Emails Triggered |
|----------|-----------|-----------------|
| 3 | Free Trial Lesson | Email 1 (immediate), Email 2 (24hr before), Email 3 (morning of) |
| 7 | No Show | Email 4 |
| 8 | Trial Attended + 48hr no movement | Email 5 |
| 4 | Discussed Membership Options | Email 6 |
| 3 (reschedule) | New Calendly booking date | Email 7 |
| Calendly cancellation | Cancellation signal | Email 8 |

### Email Sequence Map

| # | Name | Trigger | Timing | Word Limit |
|---|------|---------|--------|-----------|
| 1 | Booking Confirmation + PDF | Stage 3 entry | Immediate | Under 200 |
| 2 | 24-Hour Reminder | 24hrs before trial date | Automatic | Under 150 |
| 3 | Morning Of | Trial date morning | 8:00 AM | Under 75 |
| 4 | No-Show Recovery | Stage 7 entry | End of trial day | Under 120 |
| 5 | Post-Visit: Didn't Sign Up | 48hrs in Stage 8, no movement | 48hr delay | Under 175 |
| 6 | Post-Visit: Needs Time | Stage 4 entry | When stage moves | Under 120 |
| 7 | Reschedule Acknowledgment | New Calendly note, different date | Immediate | Under 100 |
| 8 | Cancellation Recovery | Calendly cancellation | Immediate | Under 100 |

### Arc Classification

Manus reads Q&A response from Calendly note and classifies via Railway endpoint
OR keyword matching. Classification is written to the ETKM Arc Type person field.

| Keywords | Arc | Field Value |
|----------|-----|------------|
| fear, safety, nervous, walking alone, parking lot, attacked, unsafe | Safety | Safety |
| kids, children, family, protect, parent, son, daughter | Parent | Parent |
| fitness, workout, shape, condition, cardio, athletic, weight | Fitness | Fitness |
| military, police, security, officer, law enforcement, veteran, tactical | LE/Mil | LE/Mil |
| krav, BJJ, jiu-jitsu, karate, trained, martial arts, belt | Former MA | Former MA |
| empty or no match | Default | Default |

**Preferred method:** POST to Railway endpoint for AI classification.
**Fallback:** Keyword matching if Railway unavailable.

```
POST https://etkm-backend-production.up.railway.app/classify-arc
Body: { "qa_response": "[raw Q&A text from Calendly note]" }
Response: { "arc": "Parent" }
```

### Automation Rules

On reschedule (Email 7):
Cancel scheduled Emails 2 and 3 tied to old date.
Reschedule Email 2 to 24hrs before new date.
Reschedule Email 3 to morning of new date.

On cancellation (Email 8):
Cancel all pending Email 2 and 3 sends immediately.
One email only — no follow-up.
If no rebook in 30 days → move to Stage 9 (Decision Pending).

On no-show (Email 4):
One email only.
If no response or rebook in 7 days → move to Stage 9.

---

## ACQ-WF-002 — 90-DAY ONBOARDING SEQUENCE

### Trigger
P1 Stage 6 (Signed Up) → P2 Stage 11 (Orientation) deal created.
Sequence fires from P2 Stage 11 entry.

### Structure — 28 Emails

| Phase | Days | Emails | Focus |
|-------|------|--------|-------|
| Phase 1: Belonging | 1–30 | I-01 through I-05 | Identity — you belong here |
| Phase 2: Noticing | 31–60 | I-06 through I-09 | Awareness — noticing your growth |
| Phase 3: Becoming | 61–90 | I-10 through I-15 | Identity — you are becoming |
| Competency Layer | Throughout | C-01 through C-13 | Skill-building touchpoints |

### Critical Double-Send Days

| Day | Send 1 | Time | Send 2 | Time |
|-----|--------|------|--------|------|
| 14 | C-04 | 9 AM | I-04 | 1 PM |
| 60 | I-09 | 9 AM | Phase 3 transition | 1 PM |
| 85 | I-12 | 9 AM | C-13 | 1 PM |

### Phase Transition Emails

Day 30 transition: appreciation + what's ahead in Noticing phase.
Day 60 transition: recognition + what's ahead in Becoming phase.
Both fire at 1 PM on transition days.

### Verify Before Activating

Four pages must be live before sequence activates:
- etxkravmaga.com/class-structure/
- etxkravmaga.com/mindset/
- etxkravmaga.com/beginner-tactics/
- etxkravmaga.com/goals/

---

## MANUS → CLAUDE API CONNECTION

### Architecture

```
CALENDLY BOOKING
      ↓
MANUS reads note → extracts Q&A, date, time
      ↓
POST to Railway /classify-arc endpoint
      ↓
Arc label written to Pipedrive person (ETKM Arc Type field)
      ↓
Arc-specific email sequence fires from Pipedrive
```

### API Specification

```
Endpoint:  https://api.anthropic.com/v1/messages
Method:    POST
Headers:
  x-api-key:         [ANTHROPIC_API_KEY — Manus secure variable]
  anthropic-version: 2023-06-01
  content-type:      application/json

Body:
  model:      claude-sonnet-4-6
  max_tokens: 1024
  system:     [ETKM Master System Prompt]
  messages:   [{ "role": "user", "content": [Manus prompt] }]
```

### What Manus Sends to Claude

```
You are writing [EMAIL NAME] for East Texas Krav Maga.

PROSPECT CONTEXT:
- First name: [person_first_name]
- Arc type: [from ETKM Arc Type field]
- Q&A response: [raw text or "none"]
- Trial date: [extracted from Calendly note]
- Trial time: [extracted from Calendly note]
- Email number: [1-8]

TASK:
Write Email [number] — [email name] — per ETKM sequence spec.
Apply arc personalization. Follow brand voice. Under [word count] words.
Sign off as Nate Lundstrom, East Texas Krav Maga, (903) 590-0085.
Return only: subject line first, then body. No preamble, no markdown.
```

### Error Handling

If Claude API fails:
1. Retry once after 30 seconds
2. If second attempt fails: send static default template (non-personalized)
3. Log failure for review
4. Do not delay email send — fallback immediately on second failure

---

## COMPLETION RECEIPT PROTOCOL

When Manus completes any build or load task:
Write a receipt file to Google Drive /ETKM-AI/Status/[ID]-COMPLETE.md

Receipt format:
```
# [PROJECT-WF-###] COMPLETE
Date: [date]
Task: [brief description]
Verified: [what was confirmed live/working]
Issues: [any open items or flags]
```

Cowork monitors this folder and alerts Nathan when receipt is detected.
Do not mark a workflow LIVE until receipt is confirmed.

---

## GOOGLE DRIVE PDF HOSTING

All PDFs delivered via Pipedrive are hosted in Google Drive.
Link format: https://drive.google.com/file/d/[FILE_ID]/view
NOT the ?usp=sharing version — can trigger Google login prompt.
Permissions: "Anyone with the link can view" — no sign-in required.

---

## STATIC CONTACT INFO (ALL EMAILS)

```
Nate Lundstrom
East Texas Krav Maga
2918 E. Grande Blvd., Tyler, TX 75707
(903) 590-0085
etxkravmaga.com
```

Note: etxkravmaga.com — NOT easttxkravmaga.com.

---

## PROHIBITED WORDS — ALL EMAILS

Never use: mastery, dominate, destroy, killer, beast, crush, elite, warrior

Use instead: capable, proficient, prepared, confident, effective, practical, real, structured

Format rules:
- Open with [person_first_name], — never "Dear" or "Hello"
- No bullet lists in body — short paragraphs only
- One CTA per email — never two asks
- No pricing in Emails 1, 2, 3, 7, or 8
- Sign off as Nate Lundstrom every time
