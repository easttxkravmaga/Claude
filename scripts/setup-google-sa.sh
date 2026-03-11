#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# ETKM Google Service Account Setup
# Run this ONCE on any machine with gcloud CLI installed.
# Outputs all Railway env vars ready to paste.
# ─────────────────────────────────────────────────────────────────────────────

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}ETKM Google Service Account Setup${NC}"
echo "────────────────────────────────────"

# ── Check gcloud installed ────────────────────────────────────────────────────
if ! command -v gcloud &> /dev/null; then
  echo -e "${RED}ERROR: gcloud CLI not found.${NC}"
  echo "Install it from: https://cloud.google.com/sdk/docs/install"
  exit 1
fi

# ── Variables ─────────────────────────────────────────────────────────────────
SA_NAME="etkm-cowork-watcher"
SA_DISPLAY="ETKM Cowork Watcher"
KEY_FILE="$HOME/.etkm/etkm-cowork-sa-key.json"
mkdir -p "$HOME/.etkm"

# ── Get active project ────────────────────────────────────────────────────────
PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT" ]; then
  echo -e "${YELLOW}No active GCP project. Creating one...${NC}"
  PROJECT="etkm-ai-ops"
  gcloud projects create "$PROJECT" --name="ETKM AI Ops" 2>/dev/null || true
  gcloud config set project "$PROJECT"
  echo -e "${YELLOW}NOTE: You may need to link a billing account at:${NC}"
  echo "  https://console.cloud.google.com/billing/linkedaccount?project=$PROJECT"
fi
echo "Project: $PROJECT"

# ── Enable Drive API ──────────────────────────────────────────────────────────
echo "Enabling Google Drive API..."
gcloud services enable drive.googleapis.com --project="$PROJECT" 2>/dev/null
echo -e "${GREEN}✓ Drive API enabled${NC}"

# ── Create service account ────────────────────────────────────────────────────
SA_EMAIL="${SA_NAME}@${PROJECT}.iam.gserviceaccount.com"

if gcloud iam service-accounts describe "$SA_EMAIL" --project="$PROJECT" &>/dev/null; then
  echo "Service account already exists: $SA_EMAIL"
else
  echo "Creating service account..."
  gcloud iam service-accounts create "$SA_NAME" \
    --display-name="$SA_DISPLAY" \
    --project="$PROJECT"
  echo -e "${GREEN}✓ Service account created: $SA_EMAIL${NC}"
fi

# ── Create/download key ───────────────────────────────────────────────────────
echo "Downloading service account key..."
gcloud iam service-accounts keys create "$KEY_FILE" \
  --iam-account="$SA_EMAIL" \
  --project="$PROJECT"
echo -e "${GREEN}✓ Key saved to: $KEY_FILE${NC}"

# ── Base64 encode ─────────────────────────────────────────────────────────────
CREDS_B64=$(base64 -w 0 "$KEY_FILE" 2>/dev/null || base64 "$KEY_FILE")

# ── Find Briefings folder ID ──────────────────────────────────────────────────
echo ""
echo -e "${YELLOW}ACTION REQUIRED:${NC}"
echo "1. Open Google Drive"
echo "2. Navigate to /ETKM-AI/Briefings/"
echo "3. Copy the folder ID from the URL:"
echo "   https://drive.google.com/drive/folders/FOLDER_ID_IS_HERE"
echo ""
read -p "Paste the /ETKM-AI/Briefings/ folder ID: " FOLDER_ID

# ── Share folder with service account ────────────────────────────────────────
echo ""
echo -e "${YELLOW}ACTION REQUIRED:${NC}"
echo "Share the /ETKM-AI/Briefings/ folder with this email as Editor:"
echo -e "${GREEN}  $SA_EMAIL${NC}"
echo ""
echo "Steps:"
echo "  1. Right-click the Briefings folder in Drive"
echo "  2. Share → Add people → paste: $SA_EMAIL"
echo "  3. Set permission to Editor"
echo "  4. Uncheck 'Notify people'"
echo "  5. Click Share"
echo ""
read -p "Done? Press Enter to continue..."

# ── Output Railway env vars ───────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════════"
echo -e "${GREEN}  RAILWAY ENV VARS — COPY AND PASTE ALL OF THESE${NC}"
echo "════════════════════════════════════════════════════════"
echo ""
echo "GOOGLE_SA_CREDS=$CREDS_B64"
echo ""
echo "GOOGLE_DRIVE_FOLDER=$FOLDER_ID"
echo ""
echo "════════════════════════════════════════════════════════"
echo ""
echo -e "${YELLOW}Also need: NOTION_TOKEN${NC}"
echo "Get it at: https://www.notion.so/my-integrations"
echo "→ New integration → 'ETKM Cowork Watcher' → copy token"
echo "→ Share your Todo List database with it"
echo ""
echo -e "${GREEN}Setup complete. Paste those vars into Railway and deploy.${NC}"

# ── Cleanup key from disk ─────────────────────────────────────────────────────
echo ""
echo "Key file is at: $KEY_FILE"
echo "Once Railway has the var, you can delete it:"
echo "  rm $KEY_FILE"
