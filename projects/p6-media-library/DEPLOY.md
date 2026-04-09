# P6 Media Library — Deploy Checklist
4 steps. ~30 minutes total.

---

## Step 1 — Deploy Cloud Run (10 min)
Open [Google Cloud Shell](https://shell.cloud.google.com) and run this one command:

```bash
cd ~ && git clone https://github.com/easttxkravmaga/Claude.git && \
cd Claude && git checkout claude/setup-etkm-library-043os && \
cd projects/p6-media-library/cloud-run && \
gcloud run deploy etkm-bw-convert \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --project project-9c425f11-39e5-4743-b9d
```

When it finishes, copy the **Service URL** it prints. You'll need it in Step 3.

---

## Step 2 — Import Workflow into n8n (5 min)

1. Go to [etxkravmaga.app.n8n.cloud](https://etxkravmaga.app.n8n.cloud)
2. Click **+** → **Import from file**
3. Upload this file from the repo:
   `projects/p6-media-library/n8n/workflow.json`
   (download it from GitHub: repo → branch `claude/setup-etkm-library-043os`)
4. n8n will prompt you to assign credentials — skip for now (you'll add them in Step 3)

---

## Step 3 — Set n8n Variables + Credentials (10 min)

**Variables** (Settings → Variables):

| Variable | Value |
|---|---|
| `CLOUD_RUN_BW_SERVICE_URL` | Service URL from Step 1 (no trailing slash) |
| `ANTHROPIC_API_KEY` | Your Anthropic API key |

**Credentials** (Settings → Credentials → New):

1. **Google Drive OAuth2** — authorize your Google account
   - Go back to the workflow, open each Drive node, reassign to this credential
2. **Notion (Internal Integration)** — paste your Notion integration token
   - Create token at: notion.so/my-integrations → New integration → copy secret
   - In Notion: open `ETKM Media Library` database → `···` → Connections → add your integration
   - Open the Notion node in workflow, reassign to this credential

---

## Step 4 — Test and Activate (5 min)

1. Drop one image into your Google Drive root folder
2. In n8n, open the workflow → click **Execute Workflow** to run manually
3. Confirm the image appears in Notion with tags
4. If it passes: click the toggle to **Activate** the workflow (runs automatically from now on)

---

## Notion Database
Already created and ready. ID: `9d79095f-e24a-4490-8fd5-42922196c58f`
No setup needed.

---

**If anything breaks:** The most likely failure point is the Cloud Run URL not being set in n8n Variables. Check Step 3 first.
