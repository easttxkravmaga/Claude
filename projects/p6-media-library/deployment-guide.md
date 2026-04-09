# P6 Media Library — Full Deployment Guide

**Date:** April 2026  
**Sequence:** Nathan's actions are marked [NATHAN]. Claude Code actions are marked [DONE].

---

## Prerequisites

Before starting, have these ready:
- Google Cloud project: `project-9c425f11-39e5-4743-b9d` (already exists)
- `gcloud` authenticated: `gcloud auth list` to verify
- Anthropic API key from console.anthropic.com
- Notion workspace with admin access
- n8n instance running (self-hosted or cloud)

---

## Phase 1 — Google Drive Setup [NATHAN]

### 1.1 Create Ingest Folder

1. Open: https://drive.google.com/drive/folders/1ebim51jYgnvAwhypLKwG6f1muQzNK4Is
2. Click `+ New` → **Folder** → Name: `ETKM Media Ingest`
3. Click the folder → copy the ID from the URL:
   `https://drive.google.com/drive/folders/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
   Save this as `GOOGLE_DRIVE_INGEST_FOLDER_ID`

### 1.2 Create Library Folder

1. In the same root, create another folder: `ETKM Media Library`
2. Copy its folder ID
   Save this as `GOOGLE_DRIVE_LIBRARY_FOLDER_ID`

---

## Phase 2 — Notion Database [DONE — instructions in `notion/database-setup.md`]

Follow the full setup guide in `output/p6-media-library/notion/database-setup.md`.

After completing setup, save:
- Database ID → `NOTION_MEDIA_LIBRARY_DB_ID`
- Integration secret → used as n8n Notion credential

---

## Phase 3 — Deploy Cloud Run Microservice [NATHAN + CLOUD RUN]

The source is in `output/p6-media-library/cloud-run/`.

### 3.1 Copy to Deployment Directory

```bash
cp -r output/p6-media-library/cloud-run/ /tmp/etkm-bw-convert/
cd /tmp/etkm-bw-convert/
```

### 3.2 Set Variables

```bash
export PROJECT_ID="project-9c425f11-39e5-4743-b9d"
export REGION="us-central1"
export REPO_NAME="cloud-run-source-deploy"
export SERVICE_NAME="etkm-bw-convert"
export IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:latest"
```

### 3.3 Build and Push

```bash
# Build
sudo docker build --network=host -t $IMAGE .

# Authenticate Docker
ACCESS_TOKEN=$(gcloud auth print-access-token)
echo $ACCESS_TOKEN | sudo docker login -u oauth2accesstoken --password-stdin https://${REGION}-docker.pkg.dev

# Push
sudo docker push $IMAGE
```

### 3.4 Deploy

```bash
gcloud run deploy $SERVICE_NAME \
  --image=$IMAGE \
  --project=$PROJECT_ID \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080 \
  --memory=1Gi \
  --timeout=120 \
  --quiet
```

Note: 1Gi memory is needed for Pillow image processing. The existing `etkm-backend` uses 512Mi — increase for this service.

### 3.5 Verify

```bash
curl -s https://[SERVICE-URL]/health
# Expected: {"status": "ok", "service": "etkm-bw-convert"}
```

Save the service URL as `CLOUD_RUN_BW_SERVICE_URL`.

---

## Phase 4 — n8n Pipeline Setup [NATHAN + n8n]

### 4.1 Set Environment Variables in n8n

In n8n: **Settings → Variables** → add all variables from `n8n/env-vars.md`

### 4.2 Set up Credentials

1. **Google Drive OAuth2:**
   - n8n → Credentials → New → Google Drive OAuth2
   - Follow OAuth flow with `easttxkravmaga@gmail.com`

2. **Notion:**
   - n8n → Credentials → New → Notion Internal Integration
   - Paste the integration secret from Phase 2

### 4.3 Import the Workflow

1. n8n → **Workflows** → **Import from file**
2. Select `output/p6-media-library/n8n/workflow.json`
3. After import, open each node and assign the correct credentials:
   - Google Drive nodes → Google Drive OAuth2
   - Notion node → Notion credential

### 4.4 Activate

Toggle the workflow to **Active**. The trigger polls Drive every minute.

---

## Phase 5 — Smoke Test [NATHAN]

1. Drop a single image into `/ETKM Media Ingest/`
2. Wait up to 2 minutes for the trigger to fire
3. Check n8n execution log — all nodes should show green
4. Verify in Notion: new record created with description, tags, Drive URL
5. Verify in Drive: `bw_[filename].jpg` appears in `/ETKM Media Library/`
6. Verify original is removed from `/ETKM Media Ingest/`

If any node fails, check n8n execution details for the specific error.

---

## Phase 6 — Backlog Processing [NATHAN]

Once smoke test passes:
1. Upload all 100 backlog images to `/ETKM Media Ingest/` in batches of 20–25
2. Let the pipeline run — at 1 image/minute cycle time, 100 images = ~2 hours
3. After each batch, spot-check 3–5 Notion records for accuracy

---

## Common Issues

| Problem | Cause | Fix |
|---|---|---|
| Drive trigger not firing | Polling interval | Wait up to 2 min; check n8n logs |
| Cloud Run returns 413 | Image > 25 MB | Compress before drop, or increase limit in app.py |
| Claude returns invalid JSON | Very unusual image | n8n Code node strips fences; if still fails, check execution log |
| Notion create fails | Missing credential access | Re-share database with integration in Notion |
| Drive delete fails | Permissions | Ensure OAuth user is file owner |

---

## Architecture Reference

```
/ETKM Media Ingest/  →  n8n trigger (1 min poll)
         ↓
   Download original
         ↓
   Cloud Run /convert  →  grayscale JPEG
         ↓
   Claude API (Haiku 4.5)  →  JSON: description, tags, use cases
         ↓
   Notion create record
         ↓
   Drive upload B&W → /ETKM Media Library/
         ↓
   Drive delete original from ingest
```
