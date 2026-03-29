---
name: etkm-deployment-doctrine
description: >
  Deployment infrastructure doctrine for East Texas Krav Maga. Load this skill
  before any build session that requires production deployment. Contains the
  tool capability matrix, proven deployment paths, and the pre-build deployment
  gate. The iron rule: Nathan's hands stay clean. If Nathan has to type a
  terminal command, open Cloud Shell, paste gcloud commands, or interact with
  deployment infrastructure — the system failed him. Plan around it from the
  start. Always. Trigger before any Cloud Run deploy, any Make.com scenario
  push, or any time a build session touches production infrastructure.
---

# ETKM Deployment Doctrine

**Version:** 1.0
**Last Updated:** 2026-03-21

This skill exists because a full day was lost to deployment infrastructure
on the quiz system. These rules prevent it from ever happening again.

---

## THE IRON RULE

**Nathan's hands stay clean.**

If Nathan has to type a terminal command, open Cloud Shell, paste gcloud
commands, or interact with deployment infrastructure — the system failed
him. Plan around it from the start. Always.

---

## TOOL CAPABILITY MATRIX (Confirmed March 2026)

### Claude Code
- **CAN reach:** GitHub, npm, PyPI
- **CANNOT reach:** pipedrive.com, *.run.app, *.googleapis.com
- **Use for:** Code writing, GitHub ops, build error fixes

### Manus
- **CAN reach:** Any browser URL
- **CANNOT reliably do:** Type in xterm.js terminals, Make.com API blueprint push
- **Use for:** GitHub PR merges (UI), GCP Console, WordPress, Pipedrive UI

### Google Cloud Shell (browser terminal)
- **CAN reach:** Everything — has full GCP credentials
- **Nathan's role:** Open URL, paste one command, Enter
- **Use for:** Cloud Run deployments — THIS IS THE PROVEN PATH

### Make.com
- **Known limitation:** HTTP modules via API blueprint push fail at runtime
- **Fix:** Build in UI module by module — or use Cloud Run endpoint instead

---

## PROVEN CLOUD RUN DEPLOYMENT COMMAND (ON FILE PERMANENTLY)

Open Cloud Shell at: https://shell.cloud.google.com

Paste this:

```
cd ~ && rm -rf Claude && git clone https://github.com/easttxkravmaga/Claude.git && cd Claude && gcloud run deploy etkm-mcp-server --source . --region us-central1 --project project-9c425f11-39e5-4743-b9d --quiet
```

- **Project:** `project-9c425f11-39e5-4743-b9d`
- **Region:** `us-central1`
- **Service:** `etkm-mcp-server`
- **Live URL:** `https://etkm-mcp-server-323939015759.us-central1.run.app`

---

## PRE-BUILD DEPLOYMENT GATE

Run this checklist before any build session that touches production:

1. **Is the deployment path confirmed?** (specific tool, specific steps)
2. **Can that tool actually reach the target?** (check capability matrix above)
3. **Has this path been proven before?**
4. **Does Nathan have to touch anything?** (answer must be NO)
5. **Is there a fallback if the primary path fails?**

If any answer is wrong — solve deployment FIRST. Build SECOND.

---

## DEPLOYMENT FAILURE PROTOCOL

When a deploy fails:

1. Check build logs for the actual error — not assumptions
2. Fix in code (Claude Code handles this)
3. Push fix to GitHub
4. Re-deploy using the proven path above
5. Never introduce a new deployment path mid-session without running
   the gate checklist first

---

## NON-NEGOTIABLES

- Never assume a tool can reach a target without checking the matrix
- Never hand Nathan a multi-step deployment process
- Never try a new deployment path without a proven fallback ready
- Never start building before deployment is solved
- The proven Cloud Shell command is permanent — do not modify it
  without confirming the new version works end to end
