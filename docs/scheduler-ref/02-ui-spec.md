# 02 — UI Spec

Page-by-page UI specification for the **ETKM Social Media Publishing App**,
captured from the 9 screenshots of the Manus deployment and corrected to ETKM
brand standards. All pages share the global chrome described below.

---

## Global chrome — every page

### Header bar (full width, sticky top)

- Background: `#000000` (true black). NOT the mid-gray the Manus build used.
- Height: 56 px desktop / 48 px mobile
- Left: ETKM logotype `ETKM` in red (`#CC0000`), bold, then ` / SOCIAL PUBLISHING` in white at 70% opacity, all caps, letter-spacing 0.08em, 14 px
- Right: nav tabs — `Home`, `Scheduler`, `LinkedIn`, `Meta`, `Dashboard`. Active tab has a black-on-white inverted pill background. Inactive tabs are white text at 50% opacity that brightens on hover.
- No "Made with Manus" pill anywhere.

### Body background

`#000000` solid for the page background. Surfaces (cards, panels) sit on `#111111` with a 1px border in `#222222`.

### Typography

- Headings: system-ui sans (Inter / SF / Helvetica fallback), white, weight 600
- Body: same family, 15 px, white at 90% opacity for primary, 60% for secondary/captions
- Mono blocks (code, IDs, URLs): `SF Mono / Menlo / monospace`, 13 px, white in a `#1a1a1a` box with 1px `#2a2a2a` border

### Accent color rule

Red (`#CC0000`) appears **once per content section maximum**, only on functional accents:
- Primary action buttons
- Active tab indicators
- Step number circles in setup wizards
- Error/expired status pills (a brighter red `#FF3333` for distinction)

Never decorative.

### Responsive

Single-column mobile collapse. The Scheduler calendar is the only
desktop-first surface — on mobile it falls back to Agenda view by default.

### Footer

None. The Manus-build "Made with Manus" floating pill is removed.

---

## Page: Home (`/`)

**Purpose:** Status landing page. Shows whether OAuth is healthy and what's
queued. Replaces the Manus-build's marketing-style landing — Nathan is the
only user, no need to sell him on his own app.

### Layout

Single column, 720 px max-width, centered.

### Components (top to bottom)

1. **Eyebrow** (small, red): `ETKM SOCIAL PUBLISHING` (uppercase, letter-spacing 0.12em)
2. **H1**: `Publishing App` (white, 32 px, weight 700)
3. **Subtitle** (white at 60% opacity, 16 px):
   `Schedule and publish content to Facebook, Instagram, and LinkedIn. Your account credentials below — then the Scheduler holds the calendar.`
4. **Status panel** — replaces the Manus build's hero card. Three rows on `#111111`:

   | Row | Content |
   |---|---|
   | OAuth health | "All credentials current" (green) / "1 credential expiring in 3 days" (orange) / "1 credential expired — re-authorize" (red). Click → `/dashboard`. |
   | Queue depth | "12 posts scheduled · next at Saturday 10:00 AM" |
   | Last published | "Posted to Facebook · 2 hours ago · view" |

5. **Three action cards** in a row (single column on mobile):

   | Card | Icon | Title | Body | Click → |
   |---|---|---|---|---|
   | LinkedIn | LinkedIn glyph (blue, 24 px) | `LinkedIn` | Connect your LinkedIn profile or company page for automated posting. | `/linkedin` |
   | Meta | Facebook + Instagram lockup glyph (purple, 24 px) | `Meta (Facebook & Instagram)` | Connect your Facebook Page and Instagram Business Account. | `/meta` |
   | Dashboard | Gauge glyph (red, 24 px) | `Dashboard` | View and manage all saved credentials, tokens, and expiry status. | `/dashboard` |

   Card style: `#111111` background, `#222222` border, padding 24px, hover lifts the border to `#444444`. **No light backgrounds anywhere — fixes the Manus build's beige hero card.**

6. **"How it works" section** — 3 numbered steps in red circles (24 px), text in white:

   1. Follow the setup guide for each platform to get your Client ID and Secret.
   2. Click Authorize. You'll be redirected back here automatically after approval.
   3. Credentials are saved encrypted. The Scheduler then publishes posts at their scheduled time.

   Manus copy referenced copying credentials into a `.env` file — that's removed because the App stores them encrypted at rest.

---

## Page: Scheduler (`/scheduler`)

**Purpose:** All post management. Five sub-tabs.

### Page header

- H1: `Social Media Scheduler`
- Subtitle: `Plan, compose, and sync content across Facebook, Instagram, and LinkedIn.`
- Stats pills row (live counters, refresh on every tab switch):

  | Pill | Color | Source |
  |---|---|---|
  | `N total` | `#1a1a1a` bg, white text | `posts` row count |
  | `N draft` | `#3a2a00` bg, orange text | `status='draft'` |
  | `N scheduled` | `#1a1a3a` bg, blue text | `status='scheduled'` |
  | `N approved` | `#0a2a0a` bg, green text | `approved=true` |

### Tab bar

Four tabs: **Calendar** (default), **All Posts**, **Compose**, **AI Generator**.

(The Manus build had a fifth tab, **Batch Upload**, which is dropped from v1 — the AI Generator and multi-select Compose cover its use cases. The underlying batch import API endpoint is retained for future automation.)

Active tab: white text on `#111111` with 1px `#333333` border. Inactive: 50% opacity white. No animation on tab switch — instant.

URL pattern: `/scheduler?tab=<calendar|all|compose|ai>`. Server-rendered per tab.

---

### Tab 1 — Calendar

- Card title: `Content Calendar`
- Platform legend (top of card): three colored dots with labels — Facebook (blue `#1877F2`), Instagram (pink `#E4405F`), LinkedIn (blue `#0A66C2`). Used as fill colors on calendar events.
- Toolbar:
  - Left: `Today` `Back` `Next` buttons
  - Center: month/year label, e.g. `May 2026`
  - Right: view toggle — `Month` (default), `Week`, `Day`, `Agenda`
- Body: FullCalendar.js v6 month grid. Each cell shows date number top-left and any scheduled posts as colored event chips with platform tag prefix and truncated caption — `[INSTAGRAM] Calm down...`, `[FACEBOOK] Calm down...`.
- **Click chip** → opens that post in the Compose tab pre-filled (edit mode).
- **Click empty cell** (B3) → opens Compose tab pre-filled with that date+time (defaulted to 9:00 AM on the clicked date). URL: `/scheduler?tab=compose&date=YYYY-MM-DDT09:00`. Saves a tab switch when scheduling.
- Empty cells: render as `#0d0d0d` to distinguish from current month at `#111111`. Hover state: cursor pointer, slight `#1a1a1a` overlay to signal click-to-compose.

---

### Tab 2 — All Posts

- Card title: `All Posts`
- Filters row (top of card):
  - Platform select: All Platforms / Facebook / Instagram / LinkedIn
  - Status select: All Statuses / Draft / Scheduled / Processing / Posted / Failed
  - Result count text: `N posts` (right-aligned)
- Table (full-width, striped rows on `#0d0d0d` / `#111111`):

  | Col | Width | Content |
  |---|---|---|
  | Title / Caption | 35% | Two-line cell — bold title, truncated caption underneath |
  | Platform | 10% | Color-coded pill — `linkedin` (purple), `instagram` (pink), `facebook` (blue) |
  | Status | 12% | Stacked status pills: `posted`/`scheduled`/`failed`/`processing` (top), `approved`/`draft` (below). Status reflects DB `status` field; the second pill shows `approved` checkbox state. |
  | Scheduled | 13% | `MM/DD/YYYY, HH:MM AM/PM` or em-dash if unscheduled |
  | Errors | 10% | If `error_message` present, red pill `error` that opens a tooltip with the full error. **Manus build had every row showing 'error' because Notion sync was broken — that column is now error-only-on-real-error.** |
  | Actions | 20% | Icon buttons in order: edit (pencil) · publish-now (paper plane, green) · approve (checkmark, green) · retry (refresh, only when failed) · delete (trash, red) |

- Pagination at bottom: 25 posts per page default, prev/next, jump to page.
- Sort: clicking column header toggles ascending/descending. Default sort: `scheduled_at` desc.

---

### Tab 3 — Compose

- Card title: `Compose Post`
- Multi-section form. The **top section** is the master form. The **per-platform sections** appear conditionally based on which platforms are ticked.

#### Master section (always visible)

  | Field | Type | Notes |
  |---|---|---|
  | Post Title (internal) | Text input, single line | Placeholder: `e.g. Women's Program Launch`. Required. Never published. Used as the parent label across all platform rows in the group. |
  | Platforms | Three checkboxes side-by-side | `Facebook` · `Instagram` · `LinkedIn`. **Multi-select.** At least one must be ticked. The set of ticked platforms determines which per-platform sections appear below. |
  | Master Caption | Textarea, autoresize | Right-aligned char counter showing the lowest platform limit among ticked platforms (e.g. if FB+IG ticked, shows "X chars left for IG (2,200 max)"). Counter turns red at <10% remaining. **This is the single source caption that auto-fills the per-platform sections** unless overridden. |
  | Media | Drop zone | See Media Upload UX below. Single media file applies to all ticked platforms. |
  | Campaign Tag | Text input | Placeholder: `e.g. fight-back-spring-2026`. Free text. Applied to all rows in the post group. |
  | Status | Dropdown | `Draft` (default) / `Scheduled` |
  | Scheduled Date & Time | Datetime picker | Required when `Status = Scheduled`. Disabled when `Status = Draft`. Validates "must be in future". Pre-filled from `?date=` URL param when arriving from a Calendar click (B3). All ticked platforms publish at this same time. |
  | Approved | Checkbox | Required true for the publisher to fire. Defaults false. Applied to all rows in the group. |
  | Save Post | Primary button (red, full-width) | POSTs to `/api/posts` with the master caption, ticked platforms, and per-platform overrides. Server creates one row per ticked platform under a shared `post_group_id`. |

#### Per-platform sections (B1)

When **2 or more** platforms are ticked, three collapsible sections appear under the Master Caption — one per ticked platform. (When only 1 platform is ticked, the master caption ships as-is with no per-platform section needed.)

Each per-platform section, in order Facebook → Instagram → LinkedIn:

  | Section element | Notes |
  |---|---|
  | Section header | Platform icon (color-coded) + label `Facebook caption` / `Instagram caption` / `LinkedIn caption`. Right side: a `Tailor for {Platform}` button (small, secondary style, with a sparkle icon). |
  | Caption textarea | Pre-filled with the Master Caption on first load. Editable. Char counter showing platform-specific limit (FB 63,206 / IG 2,200 / LI 3,000). |
  | Hashtag inline note | Small grey text under the textarea: `Facebook posts get 2-4 hashtags. Use #ETKMfamily.` etc — guidance, not enforcement. |

**Tailor for X button behavior (B2):**
- Click → POSTs to `/api/ai/tailor-caption` with `{master_caption, target_platform, program?, tone?}`
- Button shows spinner; disabled during call (typically 3-8 sec)
- On success → tailored caption replaces the textarea content. Inline toast: `Tailored for {Platform}.` Auto-dismisses 3 sec.
- On failure → red inline error: `Tailor failed. Try again or write the caption manually.`
- Tailor never auto-saves the post; user clicks Save Post when ready.

**Save behavior:**
- Server reads `master_caption` plus any per-platform caption overrides
- For each ticked platform: if `per_platform_captions[platform]` differs from `master_caption`, that row uses the override; else it uses the master
- All rows share `post_group_id`, `scheduled_at`, `media_*`, `campaign_tag`, `approved`, `status`

#### Media Upload UX

- Drop zone is a `#0d0d0d` rectangle, 1px `#222222` dashed border, 200 px tall, centered icon and copy: image/video glyph + `Click to upload or drop a file here` + `PNG, JPG, GIF, WebP up to 20 MB · MP4 up to 200 MB`
- Click opens file picker. Accept: `image/png, image/jpeg, image/gif, image/webp, video/mp4`
- On image selected:
  - Browser POSTs to `/api/media/upload-image`
  - Replace drop zone with image preview (max 320 px tall) + "Replace" / "Remove" buttons
  - Hidden form values populated
- On video selected:
  - Browser requests signed URL from `/api/media/sign-upload-url`
  - Progress bar appears (red fill on `#0d0d0d` track)
  - Browser PUTs file to GCS signed URL with multipart-resumable for files > 50 MB
  - On success: POST `/api/media/finalize` returns metadata
  - Replace drop zone with video preview (`<video controls muted>`, max 320 px tall) + duration + dimensions + "Replace" / "Remove" buttons
- **Aspect ratio warning** (the IG Reels gotcha):
  - When platform = Instagram AND uploaded video is not 9:16: show inline warning beneath preview in orange (`#FFB800`):
    `⚠ Instagram Reels expect 9:16 vertical video. This video is 16:9 — Instagram will publish it with black bars on the sides. Re-export at 1080×1920 to fix.`
  - Warning only — does not block save.

---

### Tab 4 — AI Generator

(The Manus build had a Batch Upload tab in this slot. Dropped from v1 — the AI Generator and multi-select Compose cover its use cases. Underlying API endpoint `POST /api/posts/batch` is retained for future automation.)

- Card title: `AI Campaign Generator`
- Form fields (two-column where indicated):

  | Field | Type | Notes |
  |---|---|---|
  | Program / Topic | **Text input + 5 quick-fill buttons** | Free-text input, 1-120 chars. Below the input, a row of 5 small secondary buttons: `Adult Krav Maga` · `Women's Self-Defense` · `Youth Program` · `LE / Security` · `General`. Click a button → fills the text input with that value. User can also type anything else (e.g. "CBLTAC course", "summer camp"). No coupling to Notion's tag list. |
  | Tone | Dropdown | `Direct & confident` (default), `Educational`, `Inspirational`, `Conversational`. The brand voice rules apply regardless. |
  | Campaign Goal | Textarea, 3 rows | Placeholder: `e.g. Drive sign-ups for the March Fight Back ETX workshop` |
  | Platforms | Checkbox row | Facebook / Instagram / LinkedIn — at least one required |
  | Start Date | Date picker | Required |
  | End Date | Date picker | Required, must be ≥ Start Date |
  | Posts per Platform | Number input | Default 3, min 1, max 14 (one per day for two weeks) |
  | Campaign Tag | Text input | Placeholder: `e.g. fight-back-march-2026`. Auto-suggests from program + month. |
  | Generate Campaign Posts | Primary button, full-width | POSTs to `/api/ai/generate-campaign`. Shows spinner while Claude responds (typically 8-25 sec). |

- On success: returns to All Posts tab filtered to the new campaign tag, with a green banner: `Generated N drafts. Review and approve before they publish.`
- On error: red banner with the API error.

---

## Page: LinkedIn Setup (`/linkedin`)

**Purpose:** Step-by-step wizard to connect a LinkedIn account. Same shape as
the Manus build's wizard, with the **`offline_access` scope fix** baked into
step 2.

### Layout

Single column, 640 px max-width, centered.

### Components

1. **Card header**: small LinkedIn icon (blue, 32 px) + H1 `LinkedIn API Setup` + subtitle `Connect your LinkedIn account for automated posting.`

2. **Four numbered steps**, each in a `#111111` panel with a red circle (with white step number, 28 px) at left and step content at right:

   **Step 1 — Create a LinkedIn Developer App**
   `Go to the LinkedIn Developer Portal. Create a new app, select your ETKM company page, and accept the terms.`
   Link: `https://www.linkedin.com/developers/apps/new` (opens in new tab)

   **Step 2 — Request Products** *(this is the bug fix from the live build)*
   `In your app's Products tab, request access to: Share on LinkedIn, Sign In with LinkedIn using OpenID Connect, AND request the offline_access scope under OAuth 2.0 settings.`
   Then: `Without offline_access, the token cannot be auto-refreshed and you'll have to re-authorize manually every 60 days.`

   **Step 3 — Add Redirect URL**
   `In the Auth tab under OAuth 2.0 settings, add this redirect URL:`
   Mono block: `https://etkm-social-publishing-XXXXX.us-central1.run.app/api/oauth/linkedin/callback` (the actual hostname is filled in server-side from `LINKEDIN_REDIRECT_URI` env var)

   **Step 4 — Enter Credentials & Authorize**
   `Paste your Client ID and Client Secret below, then click Authorize.`

3. **Credentials card** (`YOUR APP CREDENTIALS`):
   - Client ID input (text)
   - Client Secret input (password type, shows masked)
   - Redirect URI display (read-only, mono, copyable)
   - **Authorize with LinkedIn** button — full-width, LinkedIn brand blue (`#0A66C2`), LinkedIn glyph + label. POSTs Client ID/Secret to `/api/oauth/linkedin/start`, then 302 redirects to LinkedIn consent screen with `scope=openid profile email w_member_social offline_access`.

---

## Page: Meta Setup (`/meta`)

**Purpose:** Step-by-step wizard to connect Facebook + Instagram via short-lived → long-lived token exchange.

### Layout

Same as LinkedIn page.

### Components

1. **Card header**: Meta lockup icon (purple, 32 px) + H1 `Meta API Setup` + subtitle `Connect Facebook Page and Instagram Business Account.`

2. **Four numbered steps**:

   **Step 1 — Create a Meta Developer App**
   `Go to Meta for Developers. Create a new app with type Business, named ETKM Social Agent.`
   Link: `https://developers.facebook.com/apps/`

   **Step 2 — Add Products**
   `In your app dashboard, add: Instagram Graph API and Facebook Login for Business.`

   **Step 3 — Get a Short-Lived Token**
   `Go to the Graph API Explorer. Select your app, add permissions: pages_show_list, pages_read_engagement, pages_manage_posts, instagram_basic, instagram_content_publish, business_management. Click Generate Access Token.`
   Link: `https://developers.facebook.com/tools/explorer/`

   **Step 4 — Paste Credentials Below**
   `Enter your App ID, App Secret, and the short-lived token. We'll exchange it for a permanent Page Access Token automatically.`

3. **Exchange card** (`EXCHANGE TOKEN`):
   - App ID input (text)
   - App Secret input (password)
   - Short-Lived User Access Token input (text, large) — placeholder `EAAo2...`
   - **Exchange for Long-Lived Token** button — full-width, purple Meta brand color (`#5C5CFF`). POSTs to `/api/oauth/meta/exchange`. On success → Dashboard with the new Meta credential card visible.

---

## Page: Credential Dashboard (`/dashboard`)

**Purpose:** View and manage all saved OAuth tokens. Auto-refresh status and manual refresh trigger.

### Layout

Full-width with 1280 px max content area.

### Page header

- H1: `Credential Dashboard`
- Subtitle: `All saved OAuth tokens · auto-refreshes every 6 hours.`
- Right side, three controls in a row:
  - Status pill: `Scheduler busy` (orange) when a refresh job is mid-run, otherwise `Scheduler idle` (gray). Polled from `/api/scheduler/status` every 30 sec.
  - `Refresh All Expiring` button (secondary): triggers a manual sweep of all credentials expiring within 7 days
  - `Reload` button (secondary): re-fetches the dashboard data

### Info banner (`#0d0d0d` bg, 1px `#222222` border, white text)

`The background scheduler checks for tokens expiring within 7 days every 6 hours and refreshes them automatically. You will receive an in-app notification on success or failure. Use 'Refresh Now' to trigger a manual refresh on any credential.`

### Sections (one per provider)

Each section starts with a small section header:
- Provider icon + label + count: `LinkedIn (1)`, `Meta — Facebook & Instagram (1)`

Then one credential card per row (full-width, `#111111` bg, padding 24 px):

#### Card structure

- **Top row**: provider icon · label (`ETKM LinkedIn`) · ID (`LinkedIn · ID #1`) · status pill on right · trash icon

  Status pills (locked colors):
  - `Active` — green `#1A6E2F`, white text
  - `Expiring soon` — orange `#A65A00`, white text
  - `Expired` — red `#A60C0C`, white text
  - `Never expires` — blue `#1A4E7A`, white text (for Meta long-lived Page tokens)

- **Field rows**, mono input style, copy button at right of each:
  - **Access Token** — masked by default, eye icon toggles reveal, copy icon copies the cleartext (which the App decrypts on demand server-side, never sends to browser unless explicitly revealed)
  - **Client ID** — readable text
  - **Provider-specific extra fields**:
    - LinkedIn: Person URN
    - Meta: Facebook Page ID, Instagram Account ID

- **Bottom row** — refresh status + refresh button:
  - Left: text status — "Last refreshed 3 hours ago" / "Refresh failed" / "No expiry"
  - Right: `Refresh Now` button — POSTs to `/api/credentials/<id>/refresh`. Shows spinner while refreshing.

- **Error block** (only when refresh failed) — red border, red text:
  - For LinkedIn without `offline_access`:
    `No refresh token available. LinkedIn tokens without offline_access scope cannot be automatically refreshed. Please re-authorize with offline_access enabled.`
  - With a `Re-authorize` button that takes the user back to `/linkedin`.

### Empty state

When no credentials saved: `No credentials yet. Set up LinkedIn or Meta to get started.` with two button links to `/linkedin` and `/meta`.

---

## Pages NOT in v1 (deliberately)

- No public-facing landing page
- No multi-user account system
- No team/role management
- No webhook receivers (the App polls at scheduled time; it doesn't need to receive notifications)
- No analytics page (post-engagement metrics) — defer to v2

---

## Brand-fix delta from the Manus build

| Manus had | Publishing App has |
|---|---|
| Mid-gray header bar | True black `#000000` |
| "OAUTH MANAGER" subtitle in header | `SOCIAL PUBLISHING` subtitle (consistent with Home eyebrow + page title) |
| Light beige hero card on Home | Black status panel showing OAuth health, queue depth, last published |
| "Made with Manus" floating pill | Removed |
| Generic "How It Works" with "save credentials to .env file" copy | Updated copy reflecting encrypted-at-rest storage |
| Plaintext token fields visible in Dashboard | Tokens masked by default, server-side decrypt only on reveal |
| Notion column on All Posts table (every row "error") | Removed entirely. Errors column is error-only-on-real-error. |
| No aspect-ratio warning on video upload | Inline warning when uploading non-9:16 video to Instagram |

## Product improvements over the Manus build

| Manus had | Publishing App has |
|---|---|
| Single-select platform per post (had to recompose to post to FB+IG+LI) | **Multi-select** Platforms checkbox group; one save creates N rows under a shared `post_group_id` |
| One caption shared across all platforms | **B1: Per-platform caption editing.** When 2+ platforms ticked, each platform gets its own caption box pre-filled from the master, editable per platform |
| No way to adapt copy per platform | **B2: AI "Tailor for X" buttons** in each per-platform section. Claude rewrites the master caption with platform-appropriate length, hooks, hashtag count |
| Calendar tab was view-only | **B3: Click empty cell** opens Compose pre-filled with that date+time |
| Batch Upload tab (CSV/XLSX) | **Dropped.** AI Generator and multi-select Compose cover the use cases. CSV import API endpoint retained for future automation. |
| Notion-mirrored Program/Topic dropdown (7 fixed values) | Free-text Program/Topic field with 5 quick-fill buttons + type-anything override |

---

*Next: `03-oauth.md` — LinkedIn (with `offline_access` scope) + Meta short→long token flows.*
