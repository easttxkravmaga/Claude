# 06 — Bugs and Brand Fixes

Concrete bugs visible in the live Manus build (captured from the 9
screenshots) and ETKM brand-rule violations to correct in the rebuild. Treat
this as a pre-flight checklist — none of these may recur.

---

## Bug 1 — LinkedIn token cannot auto-refresh

### Evidence

Dashboard screenshot, LinkedIn card. Status pill: red "Expired". Bottom of card shows:

> Refresh failed
> No refresh token available. LinkedIn tokens without offline_access scope cannot be automatically refreshed. Please re-authorize.

### Root cause

The Manus build's LinkedIn OAuth scope set was `openid profile email w_member_social` — no `offline_access`. LinkedIn issues access tokens valid 60 days but **no refresh token unless `offline_access` is requested**. After 60 days the token died. With no refresh token, the App couldn't recover automatically.

### Fix in the rebuild

Spec'd in `03-oauth.md` — the LinkedIn authorize endpoint requests:

```
scope=openid profile email w_member_social r_basicprofile offline_access
```

`offline_access` triggers LinkedIn to issue a refresh token with the access token, valid 365 days. The 6-hour refresh job uses it to swap for a new access token before expiry.

### Verification

After rebuild, in `/dashboard` LinkedIn card should display:
- Status pill: green "Active"
- Bottom row: "Last refreshed N hours ago"
- Token-exchange response logged at OAuth callback time should include `refresh_token` field. If absent → the scope wasn't passed correctly. Smoke test before marking deploy complete.

### Migration step Nathan must do once

Re-authorize LinkedIn after deploy — the existing token has no refresh component and can't be salvaged. New `/linkedin` flow with `offline_access` produces a fresh, refreshable credential.

---

## Bug 2 — Notion sync errored on every row

### Evidence

All Posts table screenshot. Every row in the visible 8 has a red "error" pill in the Notion column. Posts still went out to social platforms successfully (visible "View post" links and "posted" status), but the Notion mirror was completely broken.

### Root cause (inferred)

The Manus build attempted to mirror each post to a Notion database after publishing. The mirror failed on every row, suggesting one of:
- Notion integration token wasn't valid / wasn't granted access to the target database
- Schema mismatch — Manus posted properties that didn't exist on the target DB
- Database ID was wrong / pointed to a deleted DB

Nathan confirmed in conversation that the Notion sync had no functional impact — posts published correctly despite the error. The "error" was a side-channel mirror, not in the publish path.

### Fix in the rebuild

**Removed entirely.** The Publishing App does not integrate with Notion. The App owns its own database; Notion stays as Nathan's strategy reference document, untouched.

### Verification

In `/scheduler?tab=all` table, the Notion column from the Manus screenshot is gone. Replaced with an `Errors` column that is **empty** unless the post itself failed to publish (separate from any sync mirror). No persistent red pill on every row.

---

## Bug 3 — Easter Instagram post failed: "Media ID is not available"

### Evidence

All Posts table, fourth visible row:

| Title | Caption | Platform | Status | Errors |
|---|---|---|---|---|
| Easter No Class | Easter is a time to slow down, reflect, and reconnect with w… | instagram | failed / approved | "Media ID is not available" |

The Facebook version (fifth row, "easter") with the same caption posted successfully. Only Instagram failed.

### Root cause

Instagram's publishing flow requires a multi-step container creation, status polling, then publish (see `04-storage-and-publishing.md`). The error "Media ID is not available" typically means one of:
- The publish call hit before the container finished ingesting the media (Step 2's `IN_PROGRESS` state was not waited out)
- The container was created with an invalid or unreachable `image_url` / `video_url`
- The Page Access Token was missing the `instagram_content_publish` scope (less likely if Facebook with same caption worked)

Most probable: the Manus build's IG publisher fired Step 3 before Step 2 returned `FINISHED`, OR didn't poll Step 2 at all and just hoped the container was ready.

### Fix in the rebuild

Spec'd in `04-storage-and-publishing.md`:
- Step 2 polls `/<creation_id>?fields=status_code` every 3 seconds
- Image containers wait up to 30 seconds for `FINISHED`; Reels wait up to 5 minutes
- If `IN_PROGRESS` exceeds the timeout: raise `PublishError("Instagram failed to ingest the media file.")` and increment `retry_count`
- If `ERROR`: raise `PublishError(<status field>)` immediately
- Only on `FINISHED` does Step 3 fire

Plus: signed-fetch URLs (10-minute TTL) are issued at Step 1 time. The brief 10-minute window covers any reasonable polling delay.

### Verification

Test plan:
- Schedule one IG image post, observe job log shows Step 2 polling completes in <10 sec on `FINISHED`, Step 3 returns media_id.
- Schedule one IG Reel post, observe Step 2 polling completes in 30-90 sec depending on file size, no errors.
- Observability: log Step 2 poll iterations to Cloud Run logs so we can audit timing in production.

---

## Brand violations to fix

### Violation 1 — Light beige hero card on Home page

**Evidence:** Home screenshot. The "Content Scheduler" featured card has a cream/beige background with red border. All other cards on the page are dark; this one stands out as light.

**Why it violates:** ETKM brand kit, locked in `CLAUDE.md`:

> NO light backgrounds, NO white backgrounds on any HTML deliverable

**Fix:** Per `02-ui-spec.md`, the Home page hero is replaced with a black status panel showing OAuth health, queue depth, and last-published. No light-bg cards anywhere.

---

### Violation 2 — Mid-gray header bar instead of true black

**Evidence:** Every page screenshot. The header bar is a light-mid gray (~#888888). Reads as a UI shell separator, not an ETKM surface.

**Why it violates:** Brand kit specifies surfaces at `#000000` or `#111111`. Mid-gray reads as generic and breaks the high-contrast Swiss aesthetic.

**Fix:** Header bar at `#000000`. White text on black.

---

### Violation 3 — "OAUTH MANAGER" header subtitle inconsistent with app identity

**Evidence:** Header on every page reads `ETKM / OAUTH MANAGER`. Home page H1 reads `ETKM Social Agent`. Two different identities for the same app.

**Why it violates:** Inconsistent naming. Brand identity rule: pick one name, use it everywhere.

**Fix:** Header subtitle becomes `SOCIAL PUBLISHING`. Home page eyebrow becomes `ETKM SOCIAL PUBLISHING`. App's full name is `ETKM Social Media Publishing App`. All three line up.

---

### Violation 4 — "Made with Manus" floating watermark

**Evidence:** Bottom-right corner of every page in every screenshot. Small dark pill with the Manus glyph + text "Made with Manus".

**Why it violates:** Third-party branding on an ETKM internal tool. Not ETKM's choice; baked in by the Manus platform.

**Fix:** Removed. The rebuild is on Cloud Run and has no external watermark.

---

### Violation 5 — Plaintext OAuth tokens in Dashboard fields

**Evidence:** Dashboard screenshot. Access Token, Client ID, Client Secret, Person URN visible as fully-formed strings (some masked with bullets but the underlying field is plaintext-readable when revealed).

**Why it violates:** Security violation, not brand strictly — but worth fixing in the rebuild. Storing OAuth tokens in plaintext on disk means anyone with read access to the Manus instance file system could exfiltrate them.

**Fix:** Per `03-oauth.md`, all secrets stored Fernet-encrypted at rest. Dashboard UI masks by default and decrypts server-side only when the user clicks the eye icon. Encryption key is `APP_SECRET_KEY` from Secret Manager.

---

### Violation 6 — "Save credentials to .env" copy on Home

**Evidence:** Home page "How It Works" step 3:

> Credentials are saved to the database. Copy them to your .env file for the posting agent.

**Why it violates:** Implies the Publishing App is a configuration UI for some external "posting agent" — but the App IS the posting agent. The copy is left over from a prior architecture where Manus split the OAuth flow from the publisher.

**Fix:** New step 3 copy:

> Credentials are saved encrypted. The Scheduler then publishes posts at their scheduled time.

---

### Violation 7 — Notion column polluting the All Posts table

**Evidence:** All Posts table has a Notion column showing red "error" on every row.

**Why it violates:** Data noise from a broken side-channel. Trains the user to ignore the column. Worse, it gives a false signal that something is broken when it's not.

**Fix:** Notion column removed entirely. New Errors column is empty unless the post itself failed to publish. Errors are exceptional, not the default.

---

## Implementation checklist for the rebuild

| # | Item | Owner |
|---|---|---|
| 1 | LinkedIn `offline_access` scope in `/api/oauth/linkedin/start` | Backend dev |
| 2 | Smoke test: confirm refresh_token appears in token exchange response | Backend dev |
| 3 | Remove all Notion-related code, env vars, DB columns | Backend dev |
| 4 | IG publisher Step 2 polling with 3-sec interval, 30-sec / 5-min timeouts | Backend dev |
| 5 | Header bar surface = `#000000` true black | Frontend dev |
| 6 | Home page hero = status panel (not light card) | Frontend dev |
| 7 | Header subtitle = `SOCIAL PUBLISHING` | Frontend dev |
| 8 | Strip "Made with Manus" pill from every page | Frontend dev |
| 9 | Encrypt all OAuth secrets at rest with Fernet | Backend dev |
| 10 | "Credentials are saved encrypted" copy on Home | Frontend dev |
| 11 | Errors column on All Posts is empty unless post failed | Frontend dev |

All 11 items are gates on the rebuild's QC pass. None ships unfixed.

---

*Next: `07-assumptions.md` — every guess made during this spec, flagged for Nathan to confirm or correct before code is written.*
