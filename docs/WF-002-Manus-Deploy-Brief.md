# WF-002 MANUS DEPLOYMENT BRIEF
**90-Day Student Onboarding Sequence**
Status: APPROVED — Ready to load into Pipedrive
Date: 2026-03-11

---

## YOUR JOB
Load 28 emails into Pipedrive as an automated sequence triggered by Stage 7 (Signed Up).
Do not rewrite, shorten, or modify any copy. Copy is locked and approved by Claude.

---

## TRIGGER
- **Event:** Deal moves to Stage 7 (Signed Up) in Pipedrive P2 pipeline
- **Who triggers it:** Nathan manually moves the deal
- **First email:** I-02 fires immediately (0-delay) upon trigger
- **Day clock:** Trigger date = Day 0. Day N = trigger date + N calendar days

---

## EMAIL SOURCES — WHERE TO GET THE COPY

| Emails | Source Document |
|---|---|
| I-02 (Day 1) | `WF002_Email1_Updated.md` — subject: "You're in. Here's your map." |
| Day 30 transition | `WF002_Complete_Deployment_docx.pdf` — Section 02B |
| Day 60 transition | `WF002_Complete_Deployment_docx.pdf` — Section 02C |
| C-01 (Day 3) | `WF002_Complete_Deployment_docx.pdf` — Section 02A (rewritten version) |
| All other identity emails (I-01, I-03 through I-13) | `ETKM 90-Day Identity Email Sequence DOCX` — match by code and day |
| C-02 through C-13 | `WF002_Complete_Deployment_docx.pdf` — Section 03 |

---

## MASTER SEND SCHEDULE — ALL 28 EMAILS

| Day | Code | Type | Subject Line | Phase |
|---|---|---|---|---|
| 0 | I-01 | Identity | First class follow-up — glad you came in today | 1 |
| 1 | I-02 | Identity | You're in. Here's your map. | 1 |
| 3 | C-01 | Competency | You've seen your training map. Let's talk about where you are right now. | 1 |
| 6 | C-02 | Competency | What's actually happening in class — and why | 1 |
| 7 | I-03 | Identity | Still with us? Good. Here's what I'm watching for. | 1 |
| 10 | C-03 | Competency | You're in the Crawl Phase right now. Here's what that means. | 1 |
| 14 | C-04 | Competency | The thing I teach before I teach anything else | 1 |
| 14 | I-04 | Identity | Two weeks. Let me tell you what I'm noticing. | 1 |
| 18 | C-05 | Competency | Two tactics every new student needs to understand | 1 |
| 21 | I-05 | Identity | Stay focused on your why | 1 |
| 22 | C-06 | Competency | How to think about your first month of training | 1 |
| 28 | C-07 | Competency | Words you'll keep hearing in class — and what they actually mean | 1 |
| 30 | NEW | Identity | One month in — you've crossed a line | 1→2 |
| 35 | I-06 | Identity | Something I want you to notice about the other people in class | 2 |
| 38 | C-08 | Competency | You're making the shift. Here's what to notice. | 2 |
| 42 | I-07 | Identity | Six weeks — what I'm seeing | 2 |
| 47 | C-09 | Competency | Your training partner is your best learning tool. Here's why. | 2 |
| 55 | C-10 | Competency | Let's talk about where you're headed | 2 |
| 58 | I-08 | Identity | You've been quiet — just checking in | 2 |
| 60 | I-09 | Identity | Two months in — let's take a quick look back | 2 |
| 60 | NEW | Identity | You've moved into Phase 3 — here's what that means | 2→3 |
| 63 | I-10 | Identity | Re: your training goals | 3 |
| 67 | C-11 | Competency | What it means to pressure-test your skills | 3 |
| 75 | I-11 | Identity | Let's make sure your training is on track | 3 |
| 76 | C-12 | Competency | Not all drills are the same. Here's how to tell the difference. | 3 |
| 85 | I-12 | Identity | Let's get you ready | 3 |
| 85 | C-13 | Competency | What I'm doing when I tell you to slow down (or push harder) | 3 |
| 90 | I-13 | Identity | 90 days — that's real | 3 |

---

## ⚠ SAME-DAY DOUBLE SEND RULES — CRITICAL

Three days have two emails each. Order matters.

| Day | 9 AM | 1 PM | Rule |
|---|---|---|---|
| Day 14 | C-04 (mindset content) | I-04 (Nathan check-in) | Minimum 4-hour gap |
| Day 60 | I-09 (two months reflection) | Phase 3 transition (NEW) | Minimum 4-hour gap |
| Day 85 | I-12 (Nathan check-in) | C-13 (coaching method) | Minimum 4-hour gap |

---

## SEND SETTINGS

| Setting | Value |
|---|---|
| From name | Nathan \| East Texas Krav Maga |
| Send window | 9:00 AM – 8:00 PM only |
| Outside window | Delay to next 9 AM — do not send early or late |

---

## STOP CONDITIONS — HALT ALL SENDS IMMEDIATELY

Stop all WF-002 sends if any of the following occur:
1. Student replies requesting to stop
2. Deal moved to Lost, Paused, or Churned in Pipedrive
3. Nathan manually adds "Do Not Contact" label to Person record
4. Custom field `Belt Test Passed = TRUE`

---

## VERIFY BEFORE ACTIVATING

Four competency emails link to pages that were flagged for rewrite. Confirm these pages are live before activating the sequence:

| Email | Page | Status |
|---|---|---|
| C-02 (Day 6) | Class Structure — etxkravmaga.com | Verify live |
| C-04 (Day 14) | What is Mindset — etxkravmaga.com | Verify live |
| C-05 (Day 18) | Beginner Tactics — etxkravmaga.com | Verify live |
| C-10 (Day 55) | Goals — etxkravmaga.com | Verify live |

---

## TEST SEND
Before activating, send test emails for Days 0, 1, 14 (both), 30, 60 (both), and 90 to Nathan's email address. Confirm formatting and links are intact.

---

## WHEN COMPLETE
Update Workflow Registry: WF-002 status → LOADED
Then notify Nathan for final activation.
