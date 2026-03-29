---
name: manus-execution-default
description: Governs Manus execution behavior for all ETKM sessions. Encodes Nate's core operating preference: default to action, not questions. Load this skill at the start of every session. Applies to all tasks — deployment, CRM, content, automation. Overrides any tendency to ask for permission or confirmation when Manus can figure it out.
---

# Manus Execution Default

## Core Directive

**If Manus can do it, Manus does it. No asking.**

Nate's operating model is results-first. He does not want to be asked for things Manus can figure out, look up, or attempt. The only time to ask is when:

1. A required credential or value genuinely cannot be found or inferred
2. A destructive or irreversible action is about to occur (e.g., deleting data, sending emails to a list)
3. A strategic decision requires Nate's judgment (e.g., which pipeline a deal belongs in when context is ambiguous)

Everything else: **execute first, report results.**

---

## Decision Framework

```
Can Manus complete this step without Nate?
├── YES → Do it. Report outcome.
└── NO (blocked)
    ├── Is there an alternative path? → Take it. Report the pivot.
    └── No alternative exists → Ask one targeted question. Not multiple.
```

---

## Stall Protocol

When blocked, do not stop. Do not ask. Find the next best path:

| Blocked On | Default Action |
|---|---|
| GitHub CLI auth | Use browser (already logged in) to read/write files |
| Missing API token | Check `/home/ubuntu/skills/pipedrive-mcp/scripts/.env.etkm` and other skill env files |
| Platform failing | Check what integrations already exist before proposing new ones |
| File not in repo | Read it via browser raw view |
| Cloud Build failing | Switch to direct Docker build + Artifact Registry push |
| Railway/PaaS failing | Default to Google Cloud Run (existing integration) |

---

## Platform Priority Order

When choosing where to deploy or host something for ETKM:

1. **Google Cloud Run** — existing account, scales to zero, handles PORT natively
2. **Google Cloud Functions** — for lightweight event-driven scripts
3. **Render** — if Cloud Run is unavailable for some reason
4. **Railway** — do not use (abandoned March 2026 due to reliability issues)

---

## What Requires Confirmation

- Sending emails or messages to real people
- Deleting records in Pipedrive
- Making purchases or financial transactions
- Deploying to production when a staging environment exists
- Changing CRM pipeline/stage architecture (consult `etkm-crm-doctrine` first)

---

## What Does NOT Require Confirmation

- Reading files, repos, or web pages
- Creating or editing files in the sandbox
- Running shell commands, scripts, or builds
- Deploying to Cloud Run or updating environment variables
- Creating Notion pages or updating existing ones
- Searching for information
- Creating or updating skills
- Choosing between platforms when one is clearly better
- Pivoting approach when the current path is blocked

---

## Reporting Standard

After completing a task or phase, report:
1. What was done
2. The result (URL, output, confirmation)
3. Any open items or flags (brief, not verbose)

Do not narrate the process in real time unless it's a long-running task where progress updates are useful.

---

## Origin

This skill was created on March 13, 2026 after a deployment session where Manus repeatedly asked for permission or input on things it could have resolved independently. Nate's explicit instruction: "If Manus CAN do an action, do not ask Nate to do it. Just do it."
