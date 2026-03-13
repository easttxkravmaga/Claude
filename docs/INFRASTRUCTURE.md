# ETKM Infrastructure & Tech Stack

**Owner:** Nathan Lundstrom | East Texas Krav Maga  
**Last Updated:** March 13, 2026  
**Status:** Live

---

## Backend Hosting: Google Cloud Run

**Primary platform for all ETKM backend services.**

| Property | Value |
|---|---|
| Platform | Google Cloud Run |
| Project ID | `project-9c425f11-39e5-4743-b9d` |
| Region | `us-central1` |
| Registry | `us-central1-docker.pkg.dev` |
| Repo | `cloud-run-source-deploy` |

### Why Cloud Run (not Railway)

Railway was the original platform. It was abandoned in March 2026 after persistent deployment failures caused by `$PORT` variable expansion issues in Docker CMD and Cloud Build IAM permission errors. Cloud Run was selected as the replacement because:

- Already integrated with the existing Google Workspace account (`easttxkravmaga@gmail.com`)
- Scales to zero — no idle cost
- `PORT` environment variable is handled natively
- No third-party platform dependency

**Railway fully decommissioned March 2026.** All 5 projects deleted: `etkm-mcp-server`, `desirable-curiosity`, `earnest-miracle`, `energetic-contentment`, `generous-encouragement`.

---

## Live Services

### etkm-backend (Student Intake Form)

| Property | Value |
|---|---|
| Service Name | `etkm-backend` |
| Live URL | `https://etkm-backend-323939015759.us-central1.run.app` |
| Health Check | `GET /health` → `{"status": "ok", "service": "etkm-backend"}` |
| Intake Endpoint | `POST /intake` |
| Source | `easttxkravmaga/Claude` → `/backend/app.py` |
| Deployed | March 13, 2026 |

**Environment Variables (set on Cloud Run service):**

| Variable | Purpose |
|---|---|
| `PIPEDRIVE_API_TOKEN` | Pipedrive API authentication |
| `PIPEDRIVE_PIPELINE_ID` | `1` (Prospects pipeline) |
| `PIPEDRIVE_STAGE_ID` | `3` (Free Trial stage) |
| `FLASK_ENV` | `production` |

**Note:** The app internally reads `PIPEDRIVE_API_KEY` — verify this matches the env var name set on Cloud Run if Pipedrive deal creation fails.

---

### etkm-mcp-server (MCP / Webhook / Arc Classification)

| Property | Value |
|---|---|
| Service Name | `etkm-mcp-server` |
| Live URL | `https://etkm-mcp-server-323939015759.us-central1.run.app` |
| Health Check | `GET /health` → `{"status": "ok", "service": "etkm-backend"}` |
| Endpoints | `POST /classify-arc`, `POST /webhook/square`, `POST /mcp`, `GET /mcp` (SSE) |
| Source | `easttxkravmaga/Claude` → `/backend/app.py` |
| Deployed | March 13, 2026 |

**Environment Variables (set on Cloud Run service):**

| Variable | Purpose | Status |
|---|---|---|
| `PIPEDRIVE_API_KEY` | Pipedrive API authentication | Set ✓ |
| `GITHUB_TOKEN` | GitHub repo access for MCP tools | Set ✓ |
| `ANTHROPIC_API_KEY` | Claude API for arc classification | **Pending — add when available** |
| `FLASK_ENV` | `production` | Set ✓ |

---

## Frontend

### Student Intake Form

| Property | Value |
|---|---|
| File | `etkm-student-intake-form.html` |
| Backend URL | `https://etkm-backend-323939015759.us-central1.run.app/intake` |
| CORS | No `mode: 'no-cors'` — Cloud Run handles CORS natively |

---

## Authentication & Credentials

| Service | Auth Method | Location |
|---|---|---|
| Google Cloud | `gcloud auth login` (OAuth) | `~/.config/gcloud/` |
| Pipedrive | API Token | `/home/ubuntu/skills/pipedrive-mcp/scripts/.env.etkm` |
| GitHub | Browser session (no CLI token stored) | See note below |

**GitHub CLI Note:** `GH_TOKEN` is empty in the Manus environment. Use the browser to access the repo or generate a PAT at github.com/settings/tokens when CLI access is needed.

---

## Deployment SOP

See `/home/ubuntu/skills/etkm-cloud-run-deployment/SKILL.md` for the full step-by-step deployment workflow.

**Quick reference:**
```bash
export PROJECT_ID="project-9c425f11-39e5-4743-b9d"
export REGION="us-central1"
export REPO_NAME="cloud-run-source-deploy"
export SERVICE_NAME="etkm-backend"
export IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:latest"
export PATH="/home/ubuntu/google-cloud-sdk/bin:$PATH"

# Build
sudo docker build --network=host -t $IMAGE .

# Push
ACCESS_TOKEN=$(gcloud auth print-access-token)
echo $ACCESS_TOKEN | sudo docker login -u oauth2accesstoken --password-stdin https://${REGION}-docker.pkg.dev
sudo docker push $IMAGE

# Deploy
gcloud run deploy $SERVICE_NAME --image=$IMAGE --project=$PROJECT_ID --region=$REGION --platform=managed --allow-unauthenticated --port=8080 --quiet
```
