# 03 — OAuth Flows

LinkedIn and Meta OAuth flows in detail, including the `offline_access` fix
that the Manus build skipped (the reason its LinkedIn token went permanently
dead). All examples use placeholder values; real tokens never appear in
this doc or in source code.

---

## LinkedIn — Authorization Code flow with refresh

### What scopes we request and why

The Manus build requested only `openid profile email w_member_social`. That's why the dashboard screenshot shows an expired LinkedIn token with the error "No refresh token available — LinkedIn tokens without offline_access scope cannot be automatically refreshed."

The Publishing App requests:

| Scope | Purpose |
|---|---|
| `openid` | Required for OIDC sign-in |
| `profile` | Returns name + profile data — needed to populate `label` field |
| `email` | Identity verification |
| `w_member_social` | Permission to post on member's behalf |
| **`r_basicprofile`** | Returns the `urn:li:person:XXX` we need as the `author` field on UGC posts |
| **`offline_access`** | Issues a refresh token — this is THE FIX |

Without `offline_access` LinkedIn issues an access token that expires after 60 days with NO refresh token. With it, refresh tokens are issued and last 365 days, refreshable indefinitely as long as the user re-authorizes once a year.

### Redirect URI

Exactly:

```
https://etkm-social-publishing-XXXXX.us-central1.run.app/api/oauth/linkedin/callback
```

Bound to the Cloud Run hostname. Whitelisted in the LinkedIn Developer Portal under the app's **Auth** tab → **OAuth 2.0 settings** → **Authorized redirect URLs**. Any change to the Cloud Run hostname requires re-whitelisting.

### Flow — start

**Endpoint:** `POST /api/oauth/linkedin/start`

**Request body:**
```json
{ "client_id": "<from Compose form>", "client_secret": "<from form>" }
```

**Action:**
1. Persist the credentials in `oauth_credentials` (provider=linkedin, encrypted) so the callback can find them after redirect — Status remains `pending` until callback completes.
2. Generate a CSRF `state` token (random URL-safe 32 bytes), store in user session.
3. Construct authorize URL:
   ```
   https://www.linkedin.com/oauth/v2/authorization
     ?response_type=code
     &client_id=<client_id>
     &redirect_uri=<LINKEDIN_REDIRECT_URI>
     &scope=openid profile email w_member_social r_basicprofile offline_access
     &state=<csrf>
   ```
4. Return 302 to that URL.

### Flow — callback

**Endpoint:** `GET /api/oauth/linkedin/callback?code=<code>&state=<state>`

**Action:**
1. Verify `state` matches the session value. Reject with 400 if not.
2. Exchange the code for tokens — POST to `https://www.linkedin.com/oauth/v2/accessToken`:
   ```
   grant_type=authorization_code
   code=<code>
   redirect_uri=<LINKEDIN_REDIRECT_URI>
   client_id=<client_id>
   client_secret=<client_secret>
   ```
3. Response shape:
   ```json
   {
     "access_token": "AQX...",
     "expires_in": 5184000,
     "refresh_token": "AQX...",
     "refresh_token_expires_in": 31536000,
     "scope": "openid profile email w_member_social r_basicprofile",
     "token_type": "Bearer"
   }
   ```
   Note the `refresh_token` field — only present because we requested `offline_access`. Confirms the fix worked.
4. Fetch the user's profile to capture `person_urn`:
   - GET `https://api.linkedin.com/v2/userinfo` with `Authorization: Bearer <access_token>`
   - Response includes `sub` field — that's the LinkedIn member ID, used to construct `urn:li:person:<sub>`
5. Update the `oauth_credentials` row:
   - `access_token_enc` = Fernet-encrypt(access_token)
   - `refresh_token_enc` = Fernet-encrypt(refresh_token)
   - `expires_at` = now + 60 days (LinkedIn always returns 5,184,000 seconds = 60 days)
   - `person_urn` = `urn:li:person:<sub>`
   - `last_refresh_at` = now
   - `last_refresh_status` = "success"
6. Redirect to `/dashboard`.

### Flow — refresh

**When:** Background job (every 6h) finds rows where `expires_at < now() + 7 days`. Or manual via `/api/credentials/<id>/refresh`.

**Action:** POST `https://www.linkedin.com/oauth/v2/accessToken`:
```
grant_type=refresh_token
refresh_token=<decrypted refresh_token>
client_id=<client_id>
client_secret=<decrypted client_secret>
```

Response shape: same as initial token exchange. Update `access_token_enc`, `refresh_token_enc` (LinkedIn returns a new refresh token each time — rotate it), `expires_at`, `last_refresh_at`, `last_refresh_status="success"`.

### Failure modes

| Error | Cause | Handling |
|---|---|---|
| `invalid_grant` on refresh | Refresh token expired (>365 days) or revoked | `last_refresh_status="failed"`, error: `"Refresh token expired. Re-authorize required."`. Dashboard surfaces with `Re-authorize` button. |
| `unauthorized_scope_error` on refresh | Token issued without `offline_access` (legacy from Manus build) | `last_refresh_status="failed"`, error: `"No refresh token available. Re-authorize with offline_access enabled."`. Same UI handling. |
| Network/5xx | Transient | Leave row as-is; next 6h sweep retries |

---

## Meta — Long-Lived Page Token flow

Meta's flow is simpler in shape but has a quirk: we don't run a full OAuth dance. Nathan generates a **short-lived user token** in the Graph API Explorer himself, pastes it into the App, and the App swaps it for a **long-lived Page token** that never expires.

### Why this approach

- Meta long-lived Page tokens are valid forever (no `expires_at`)
- The exchange is a single server-side call, no redirect dance
- Nathan does the manual step once per app rebuild — simpler than wiring full OAuth for a single-user tool

### What scopes Nathan grants in Graph API Explorer

These are pasted in the Setup wizard's Step 3 copy and selected when generating the short-lived token:

| Scope | Purpose |
|---|---|
| `pages_show_list` | List the Pages this user manages — required to find the ETKM Page |
| `pages_read_engagement` | Read post engagement metrics |
| `pages_manage_posts` | Create + delete Page posts (this is THE one that actually publishes) |
| `instagram_basic` | Read IG account metadata |
| `instagram_content_publish` | Publish to IG Business Account (required for Reels and Posts) |
| `business_management` | Confirm the Page belongs to a Business Manager (best practice) |

### Flow — exchange

**Endpoint:** `POST /api/oauth/meta/exchange`

**Request body:**
```json
{
  "app_id": "<from Compose form>",
  "app_secret": "<from form>",
  "short_lived_token": "EAAo2..."
}
```

**Action:**

1. **Step A — Long-lived USER token.** GET `https://graph.facebook.com/v19.0/oauth/access_token`:
   ```
   grant_type=fb_exchange_token
   client_id=<app_id>
   client_secret=<app_secret>
   fb_exchange_token=<short_lived_token>
   ```
   Returns `{ "access_token": "<long-lived user token>", "token_type": "bearer", "expires_in": 5183999 }` (~60 days).

2. **Step B — Find ETKM Page.** GET `https://graph.facebook.com/v19.0/me/accounts?access_token=<long-lived user token>`:
   Returns a list of Pages the user manages:
   ```json
   { "data": [
     {
       "access_token": "<PAGE access token — this is the long-lived one we keep>",
       "category": "Martial Arts School",
       "name": "East Texas Krav Maga",
       "id": "<page_id>",
       "tasks": ["ANALYZE","ADVERTISE","MESSAGING","MODERATE","CREATE_CONTENT","MANAGE"]
     }
   ] }
   ```
   We pick the first Page (only one expected). The `access_token` in this response is the **never-expiring Page token** — that's the gold.

3. **Step C — Get Instagram Business Account ID.** GET `https://graph.facebook.com/v19.0/<page_id>?fields=instagram_business_account&access_token=<page_token>`:
   Returns `{ "instagram_business_account": { "id": "<ig_account_id>" }, "id": "<page_id>" }`.

4. **Persist:** Insert/update `oauth_credentials` row:
   - `provider` = `meta`
   - `label` = `ETKM Meta`
   - `client_id` = `<app_id>`
   - `client_secret_enc` = Fernet-encrypt(`<app_secret>`)
   - `access_token_enc` = Fernet-encrypt(`<page_token>`)
   - `refresh_token_enc` = NULL
   - `expires_at` = NULL (Page tokens never expire)
   - `page_id` = `<page_id>`
   - `ig_account_id` = `<ig_account_id>`
   - `last_refresh_at` = now, `last_refresh_status` = "success"

5. Return 200 with `{ "ok": true, "page_name": "East Texas Krav Maga", "ig_account_id": "<id>" }`. UI redirects to `/dashboard`.

### Failure modes

| Error | Cause | Handling |
|---|---|---|
| `OAuthException code=190` | Short-lived token expired before paste (>1h old) | Return 400 with: `"The short-lived token has expired. Generate a new one in Graph API Explorer." ` |
| `(#10) The Page does not have permission` | Missing `pages_manage_posts` scope | Return 400 with: `"App is missing the pages_manage_posts permission. Re-generate token with the correct scopes."` |
| `Empty data array on /me/accounts` | User isn't admin of any Page | Return 400 with: `"Generated token does not manage any Facebook Page. Confirm the user is an admin of the ETKM Page."` |
| `instagram_business_account` missing on Page | IG Business Account not connected | Return 400 with: `"Facebook Page is not linked to an Instagram Business Account. Connect them in Meta Business Suite first."` |

### What about token refresh?

Meta long-lived **Page** tokens **do not expire**. They only become invalid if:
- The user changes their Facebook password
- The user manually revokes app access
- Meta declares a security event

In all those cases, the token returns `OAuthException code=190` on the next publish. Background job catches that, sets `last_refresh_status="failed"` with `"Page token revoked. Re-authorize required."`, and Nathan re-runs the exchange flow.

We **don't** schedule periodic refreshes for Meta — the background job's `expires_at < now() + 7 days` filter excludes rows with `expires_at IS NULL`, which is correct.

---

## Token storage — encryption

All OAuth secrets are encrypted at rest with Fernet (`cryptography` Python package), keyed by `APP_SECRET_KEY`.

```python
from cryptography.fernet import Fernet
import os

_fernet = Fernet(os.environ["APP_SECRET_KEY"].encode())

def encrypt(plaintext: str) -> str:
    return _fernet.encrypt(plaintext.encode()).decode()

def decrypt(ciphertext: str) -> str:
    return _fernet.decrypt(ciphertext.encode()).decode()
```

`APP_SECRET_KEY` is generated once with `Fernet.generate_key()`, stored in Cloud Run as a Secret Manager-backed env var, never in source code. Rotation requires re-encrypting all stored tokens — handled by a one-shot Alembic data migration when needed.

The Manus build stored tokens in plaintext (visible as fully-formed strings in the Dashboard screenshot). The rebuild fixes this.

---

## Failure surface on Dashboard

Each credential card surfaces refresh status in priority order:

1. If `last_refresh_status == "failed"` → red error block with the error message + `Re-authorize` button (links to `/linkedin` or `/meta`)
2. Else if `expires_at < now() + 7 days` → orange "Expiring soon" pill
3. Else if `expires_at IS NULL` → blue "Never expires" pill
4. Else → green "Active" pill with `last_refresh_at` timestamp

---

*Next: `04-storage-and-publishing.md` — GCS bucket setup, signed-URL upload pattern, per-platform publishers including IG Reels multi-step and LinkedIn UGC asset upload.*
