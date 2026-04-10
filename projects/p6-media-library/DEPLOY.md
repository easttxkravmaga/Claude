# P6 Media Library — Deploy Checklist
3 steps. ~20 minutes total. No Cloud Run required.

---

## Step 1 — Import Workflow into n8n (2 min)

1. Go to [etxkravmaga.app.n8n.cloud](https://etxkravmaga.app.n8n.cloud)
2. Click **+** → **Import from file**
3. Download and upload this file:
   `projects/p6-media-library/n8n/workflow.json`
   Direct link: github.com/easttxkravmaga/Claude/blob/claude/setup-etkm-library-043os/projects/p6-media-library/n8n/workflow.json
4. Skip credential assignment for now

---

## Step 2 — Set n8n Variable + Credentials (10 min)

**Variable** (Settings → Variables → Add):

| Variable | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key from console.anthropic.com |

**Credentials** (Settings → Credentials → New):

1. **Google Drive OAuth2** — authorize your Google account
   - Open each Drive node in the workflow, reassign to this credential
2. **Notion (Internal Integration)** — paste your Notion integration token
   - Create token at: notion.so/my-integrations → New integration → copy secret
   - In Notion: open `ETKM Media Library` database → `···` → Connections → add your integration
   - Open the Notion node in the workflow, reassign to this credential

---

## Step 3 — Test and Activate (5 min)

1. Drop one image into your Google Drive root folder (`1ebim51jYgnvAwhypLKwG6f1muQzNK4Is`)
2. In n8n, open the workflow → click **Execute Workflow** to run manually
3. Confirm the image appears in Notion with description and tags
4. If it passes: toggle the workflow **Active**

---

## Notion Database
Already created and ready. ID: `9d79095f-e24a-4490-8fd5-42922196c58f`
No setup needed.

---

**Note:** Images are tagged from the original color file. B&W conversion can be added later once Cloud Run access is resolved.
