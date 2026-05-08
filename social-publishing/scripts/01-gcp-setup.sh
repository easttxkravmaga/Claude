#!/usr/bin/env bash
#
# 01-gcp-setup.sh — Phase B: GCP infra prep for ETKM Social Media Publishing App
#
# Run this from your laptop with gcloud authenticated to easttxkravmaga@gmail.com.
# Idempotent — safe to re-run; existing resources are skipped, not recreated.
#
# Usage:
#   chmod +x social-publishing/scripts/01-gcp-setup.sh
#   ./social-publishing/scripts/01-gcp-setup.sh
#
set -euo pipefail

PROJECT_ID="project-9c425f11-39e5-4743-b9d"
REGION="us-central1"
SERVICE_NAME="etkm-social-publishing"
BUCKET_NAME="etkm-social-media-assets"
SERVICE_ACCOUNT_NAME="etkm-social-publishing"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo
echo "=============================================="
echo "  ETKM Social Publishing — GCP Setup (Phase B)"
echo "=============================================="
echo
echo "  Project:         ${PROJECT_ID}"
echo "  Region:          ${REGION}"
echo "  Cloud Run name:  ${SERVICE_NAME}"
echo "  Bucket name:     ${BUCKET_NAME}"
echo "  Service account: ${SERVICE_ACCOUNT_EMAIL}"
echo
read -r -p "Proceed? [y/N] " confirm
[[ "${confirm,,}" == "y" ]] || { echo "Aborted."; exit 1; }

# ── Set project ────────────────────────────────────────────────────────────────
echo
echo "→ Setting active project..."
gcloud config set project "${PROJECT_ID}"

# ── Enable required APIs ───────────────────────────────────────────────────────
echo
echo "→ Enabling required APIs..."
gcloud services enable \
  run.googleapis.com \
  storage.googleapis.com \
  iam.googleapis.com \
  secretmanager.googleapis.com \
  cloudbuild.googleapis.com \
  --project="${PROJECT_ID}"

# ── Service account ────────────────────────────────────────────────────────────
echo
echo "→ Creating service account (or skipping if exists)..."
if gcloud iam service-accounts describe "${SERVICE_ACCOUNT_EMAIL}" \
    --project="${PROJECT_ID}" >/dev/null 2>&1; then
  echo "   Service account already exists — skipping."
else
  gcloud iam service-accounts create "${SERVICE_ACCOUNT_NAME}" \
    --display-name="ETKM Social Publishing App" \
    --description="Runs the ETKM Social Media Publishing App on Cloud Run" \
    --project="${PROJECT_ID}"
fi

# ── GCS bucket ─────────────────────────────────────────────────────────────────
echo
echo "→ Creating GCS bucket (or skipping if exists)..."
if gcloud storage buckets describe "gs://${BUCKET_NAME}" >/dev/null 2>&1; then
  echo "   Bucket already exists — skipping creation."
else
  gcloud storage buckets create "gs://${BUCKET_NAME}" \
    --location="${REGION}" \
    --uniform-bucket-level-access \
    --public-access-prevention \
    --project="${PROJECT_ID}"
fi

# ── Bucket CORS ────────────────────────────────────────────────────────────────
# Replaced after first Cloud Run deploy with the actual hostname; this initial
# version uses a wildcard placeholder Nathan tightens after Phase I.
echo
echo "→ Applying CORS policy to bucket..."
CORS_FILE="$(mktemp)"
cat > "${CORS_FILE}" <<'JSON'
[
  {
    "origin": ["https://etkm-social-publishing-PLACEHOLDER.us-central1.run.app"],
    "method": ["PUT", "GET", "HEAD"],
    "responseHeader": ["Content-Type", "Content-Length", "ETag"],
    "maxAgeSeconds": 3600
  }
]
JSON
gcloud storage buckets update "gs://${BUCKET_NAME}" --cors-file="${CORS_FILE}"
rm "${CORS_FILE}"
echo "   CORS applied with PLACEHOLDER origin. Update after Phase I deploy."

# ── Bucket lifecycle (delete after 365 days) ───────────────────────────────────
echo
echo "→ Applying lifecycle rule (delete objects ≥ 365 days old)..."
LIFECYCLE_FILE="$(mktemp)"
cat > "${LIFECYCLE_FILE}" <<'JSON'
{
  "rule": [
    {
      "action": { "type": "Delete" },
      "condition": { "age": 365 }
    }
  ]
}
JSON
gcloud storage buckets update "gs://${BUCKET_NAME}" --lifecycle-file="${LIFECYCLE_FILE}"
rm "${LIFECYCLE_FILE}"

# ── IAM: bucket access ─────────────────────────────────────────────────────────
echo
echo "→ Granting bucket access to service account..."
gcloud storage buckets add-iam-policy-binding "gs://${BUCKET_NAME}" \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/storage.objectAdmin"

# ── IAM: secret manager access (for APP_SECRET_KEY etc.) ───────────────────────
echo
echo "→ Granting Secret Manager access to service account..."
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/secretmanager.secretAccessor"

# ── Generate APP_SECRET_KEY (Fernet) and store in Secret Manager ───────────────
echo
echo "→ Generating APP_SECRET_KEY (Fernet) and storing in Secret Manager..."
if gcloud secrets describe app-secret-key --project="${PROJECT_ID}" >/dev/null 2>&1; then
  echo "   Secret already exists — skipping generation."
else
  FERNET_KEY=$(python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')
  echo -n "${FERNET_KEY}" | gcloud secrets create app-secret-key \
    --data-file=- \
    --replication-policy="automatic" \
    --project="${PROJECT_ID}"
  unset FERNET_KEY
fi

# ── Generate ADMIN_PASS and store ──────────────────────────────────────────────
echo
echo "→ Generating ADMIN_PASS and storing in Secret Manager..."
if gcloud secrets describe admin-pass --project="${PROJECT_ID}" >/dev/null 2>&1; then
  echo "   Secret already exists — skipping generation."
else
  ADMIN_PASS=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
  echo -n "${ADMIN_PASS}" | gcloud secrets create admin-pass \
    --data-file=- \
    --replication-policy="automatic" \
    --project="${PROJECT_ID}"
  echo
  echo "   ⚠ ADMIN_PASS = ${ADMIN_PASS}"
  echo "   ⚠ Save this in your password manager NOW. It will not be shown again."
  echo
  unset ADMIN_PASS
fi

# ── ANTHROPIC_API_KEY: ensure exists (manual step if missing) ──────────────────
echo
echo "→ Checking for ANTHROPIC_API_KEY in Secret Manager..."
if gcloud secrets describe anthropic-api-key --project="${PROJECT_ID}" >/dev/null 2>&1; then
  echo "   anthropic-api-key secret found."
else
  echo
  echo "   ⚠ anthropic-api-key secret NOT found in Secret Manager."
  echo "   ⚠ Create it with:"
  echo "     echo -n 'sk-ant-...' | gcloud secrets create anthropic-api-key \\"
  echo "       --data-file=- --replication-policy=automatic \\"
  echo "       --project=${PROJECT_ID}"
  echo
fi

# ── Done ───────────────────────────────────────────────────────────────────────
echo
echo "=============================================="
echo "  Phase B complete."
echo "=============================================="
echo
echo "Resources created or verified:"
echo "  • Service account:       ${SERVICE_ACCOUNT_EMAIL}"
echo "  • GCS bucket:            gs://${BUCKET_NAME}"
echo "  • Secrets:               app-secret-key, admin-pass"
echo
echo "Next: Phase I (Cloud Run deploy) will pick these up automatically."
echo "      Tighten the bucket CORS origin after deploy gives you the actual hostname."
echo
