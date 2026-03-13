---
name: etkm-cloud-run-deployment
description: Standard operating procedure for deploying ETKM Flask backends and webhook handlers to Google Cloud Run. Use this skill whenever a new backend service needs to be deployed, an existing service needs updating, or when migrating away from platforms like Railway or Heroku. Covers Docker build, Artifact Registry push, Cloud Run deployment, and environment variable management.
---

# ETKM Cloud Run Deployment Workflow

This skill defines the standard operating procedure for deploying ETKM backend services (Flask apps, webhook handlers, middleware) to Google Cloud Run. 

**Strategic Context:** ETKM uses Google Cloud Run as its primary hosting layer for backend scripts because it scales to zero (no idle costs), integrates natively with the existing Google Workspace ecosystem, and handles environment variables and ports more reliably than third-party PaaS providers like Railway.

## 1. Prerequisites & Authentication

Before deploying, ensure the environment is authenticated with Google Cloud.

1. **Check auth status:** `gcloud auth list`
2. **If not authenticated:** Do not use the GWS token (it lacks Cloud Run scope). Instead, use the browser auth flow:
   ```bash
   gcloud auth login
   ```
   *Note: If the browser auth flow fails due to process expiration, use a local redirect server approach or ask the user for a service account key.*

## 2. Project Configuration

ETKM's primary Google Cloud project is:
- **Project ID:** `project-9c425f11-39e5-4743-b9d`
- **Region:** `us-central1`

Set these in your shell session:
```bash
export PROJECT_ID="project-9c425f11-39e5-4743-b9d"
export REGION="us-central1"
export REPO_NAME="cloud-run-source-deploy"
export SERVICE_NAME="etkm-backend" # Change based on specific service
export IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:latest"
```

## 3. Dockerfile Requirements

Cloud Run requires the container to listen on the port defined by the `$PORT` environment variable (default 8080).

**Critical Fix:** Do not use the shell form of `CMD` in the Dockerfile if you need variable expansion with gunicorn. Use the `sh -c` exec form:

```dockerfile
# CORRECT
CMD ["sh", "-c", "gunicorn backend.app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60"]

# INCORRECT (Will fail with "$PORT is not a valid port number")
# CMD gunicorn backend.app:app --bind 0.0.0.0:$PORT
```

## 4. Build and Push Workflow (Direct Method)

*Lesson Learned: Do not use `gcloud run deploy --source .` as it relies on Cloud Build, which often has persistent IAM permission issues with storage buckets. Instead, build locally and push directly to Artifact Registry.*

### Step 4.1: Install Docker (if needed)
```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu
sudo systemctl start docker
```

### Step 4.2: Create Artifact Registry Repository (First time only)
```bash
gcloud artifacts repositories create $REPO_NAME \
  --repository-format=docker \
  --location=$REGION \
  --project=$PROJECT_ID \
  --quiet || echo "Repo already exists"
```

### Step 4.3: Build the Image
Use `--network=host` to avoid iptables/bridge networking issues in the sandbox:
```bash
sudo docker build --network=host -t $IMAGE .
```

### Step 4.4: Authenticate Docker and Push
Use the access token method to avoid credential helper path issues:
```bash
ACCESS_TOKEN=$(gcloud auth print-access-token)
echo $ACCESS_TOKEN | sudo docker login -u oauth2accesstoken --password-stdin https://${REGION}-docker.pkg.dev
sudo docker push $IMAGE
```

## 5. Deployment

Deploy the pushed image to Cloud Run:

```bash
gcloud run deploy $SERVICE_NAME \
  --image=$IMAGE \
  --project=$PROJECT_ID \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080 \
  --memory=512Mi \
  --timeout=60 \
  --quiet
```

## 6. Environment Variables

Set environment variables after deployment or during deployment.

```bash
gcloud run services update $SERVICE_NAME \
  --project=$PROJECT_ID \
  --region=$REGION \
  --update-env-vars="VAR1=value1,VAR2=value2" \
  --quiet
```

*Note: For Pipedrive integrations, retrieve the API token from `/home/ubuntu/skills/pipedrive-mcp/scripts/.env.etkm`.*

## 7. Verification

Always verify the deployment by hitting the health check endpoint:
```bash
curl -s https://[SERVICE-URL]/health | python3 -m json.tool
```

## Common Pitfalls to Avoid

1. **Railway/PaaS lock-in:** Default to Cloud Run for ETKM. It's more reliable and already integrated.
2. **CORS:** Cloud Run handles CORS natively. Remove `mode: 'no-cors'` from frontend fetch calls to avoid opaque responses.
3. **GitHub CLI Auth:** If `GH_TOKEN` is empty in the environment, use the browser to download repo ZIPs or ask the user for a PAT. Do not waste time trying to force the CLI to work without a token.
