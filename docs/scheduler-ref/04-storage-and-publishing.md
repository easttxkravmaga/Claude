# 04 — Storage and Publishing

GCS bucket setup, media upload patterns, and per-platform publish flows for
Facebook, Instagram, and LinkedIn — covering image and video for each.

---

## Google Cloud Storage — bucket setup

### Bucket configuration

| Setting | Value |
|---|---|
| Name | `etkm-social-media-assets` |
| Project | `project-9c425f11-39e5-4743-b9d` |
| Location | `us-central1` (regional, same as Cloud Run service) |
| Storage class | Standard |
| Public access | **Prevented** (uniform bucket-level access enabled, all reads via signed URLs) |
| Versioning | Off (we don't edit objects in place — each post gets a unique key) |
| Lifecycle | Delete objects ≥ 365 days old (cost control; rarely fetched after a year) |
| CORS | Allow PUT from the Cloud Run hostname for browser-direct uploads (see below) |

### CORS policy on bucket

Required so the browser can PUT video files directly to GCS via signed URL.

```json
[
  {
    "origin": ["https://etkm-social-publishing-XXXXX.us-central1.run.app"],
    "method": ["PUT", "GET", "HEAD"],
    "responseHeader": ["Content-Type", "Content-Length", "ETag"],
    "maxAgeSeconds": 3600
  }
]
```

Apply with `gcloud storage buckets update gs://etkm-social-media-assets --cors-file=cors.json`.

### IAM

Cloud Run service account `etkm-social-publishing@<project>.iam.gserviceaccount.com` gets `roles/storage.objectAdmin` **scoped to this bucket only**:

```bash
gcloud storage buckets add-iam-policy-binding gs://etkm-social-media-assets \
  --member="serviceAccount:etkm-social-publishing@<project>.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

### Object key convention

`{YYYY}/{MM}/{post_id}-{slug}.{ext}` — e.g. `2026/05/142-fb-women-class-launch.png`. Year/month prefix makes lifecycle rules + manual audit easier.

---

## Media upload — two paths

### Path A — Image upload (≤ 20 MB, direct to App)

**Why direct:** Cloud Run's 32 MB request body limit comfortably accommodates 20 MB images. Direct upload is simpler than signed URLs and the file is immediately verifiable server-side.

**Flow:**

1. Browser POSTs `multipart/form-data` to `/api/media/upload-image`
   - Field: `file` (the binary)
2. Flask receives, validates:
   - MIME in `{image/png, image/jpeg, image/gif, image/webp}`
   - Size ≤ 20 MB
   - Content actually matches MIME (use `python-magic` to sniff first 512 bytes)
3. Flask uploads to GCS via SDK:
   ```python
   blob = bucket.blob(f"2026/05/{post_id}-{slug}.png")
   blob.upload_from_file(file_obj, content_type="image/png")
   ```
4. Flask returns:
   ```json
   {
     "gcs_path": "gs://etkm-social-media-assets/2026/05/142-fb-women-class-launch.png",
     "mime": "image/png",
     "size": 1843204,
     "media_type": "image"
   }
   ```
5. Compose form populates hidden inputs with these values.

### Path B — Video upload (≤ 200 MB, browser direct to GCS)

**Why signed URL:** Cloud Run's 32 MB request body limit is too small for video. The browser uploads directly to GCS, never traversing Cloud Run.

**Flow:**

1. Browser POSTs to `/api/media/sign-upload-url`:
   ```json
   { "filename": "march-trial-reel.mp4", "content_type": "video/mp4", "size": 78643200 }
   ```
2. Flask validates `content_type == "video/mp4"` and `size <= 200_000_000`. Generates GCS object path. Generates a V4 signed PUT URL valid 15 minutes:
   ```python
   blob = bucket.blob(f"2026/05/{post_id}-{slug}.mp4")
   url = blob.generate_signed_url(
       version="v4",
       expiration=datetime.timedelta(minutes=15),
       method="PUT",
       content_type="video/mp4",
   )
   ```
3. Flask returns:
   ```json
   {
     "upload_url": "https://storage.googleapis.com/etkm-social-media-assets/2026/05/142-march-trial-reel.mp4?X-Goog-Algorithm=...",
     "gcs_path": "gs://etkm-social-media-assets/2026/05/142-march-trial-reel.mp4",
     "expires_at": "2026-05-08T20:15:00Z"
   }
   ```
4. Browser PUTs the file:
   ```js
   await fetch(upload_url, {
     method: "PUT",
     body: file,
     headers: { "Content-Type": "video/mp4" }
   });
   ```
   For files > 50 MB the browser should use resumable upload (XHR with progress events) so we can show an upload bar.
5. Browser POSTs to `/api/media/finalize`:
   ```json
   { "gcs_path": "gs://etkm-social-media-assets/2026/05/142-march-trial-reel.mp4" }
   ```
6. Flask reads the GCS object metadata, runs `ffprobe` (only on the metadata header, no full transcode) to extract duration + dimensions:
   ```python
   blob.reload()
   metadata = ffprobe_metadata(blob.download_as_bytes(start=0, end=2_000_000))
   # → { "duration": 47.3, "width": 1080, "height": 1920 }
   ```
7. Flask returns:
   ```json
   {
     "gcs_path": "gs://etkm-social-media-assets/2026/05/142-march-trial-reel.mp4",
     "mime": "video/mp4",
     "size": 78643200,
     "media_type": "video",
     "duration_sec": 47,
     "aspect_ratio": "9:16"
   }
   ```

### Generating a public-but-time-limited fetch URL for platforms

When the publisher fires, it needs to give the platform (Meta, LinkedIn) a URL to download the media. Same V4 signed URL pattern but with `method="GET"` and 10-minute TTL:

```python
fetch_url = blob.generate_signed_url(
    version="v4",
    expiration=datetime.timedelta(minutes=10),
    method="GET",
)
```

10 minutes is enough for any platform to fetch even a 200 MB video. The URL becomes useless after that — closed surface area.

---

## Publishers — per platform, per media type

Each publisher is a small module under `publishers/`. All return either `(platform_post_id, post_url)` on success or raise `PublishError(message)` on failure.

### Facebook

#### Image post — `publishers/facebook.py::publish_image`

```
POST https://graph.facebook.com/v19.0/{page_id}/photos
  ?access_token={page_access_token}
form-data:
  url={signed_fetch_url}
  caption={post.caption}
  published=true
```

Response: `{ "id": "<post_id>", "post_id": "<page_id>_<post_id>" }`. Post URL: `https://www.facebook.com/{post_id}`.

#### Video post — `publishers/facebook.py::publish_video`

For videos < 100 MB, single-call:
```
POST https://graph.facebook.com/v19.0/{page_id}/videos
  ?access_token={page_access_token}
form-data:
  file_url={signed_fetch_url}
  description={post.caption}
  published=true
```

For videos ≥ 100 MB, use resumable upload (3-step start/transfer/finish). Response gives `{"id": "<video_id>"}`. Post URL: `https://www.facebook.com/watch/?v={video_id}`.

**Encoding wait:** Facebook returns the video ID immediately but the post may not be live for 1-30 min while encoding. The publisher does not poll Facebook for this — sets `status="posted"` immediately. If encoding fails, Facebook sends a webhook (out of scope for v1). Manual retry from the UI if needed.

---

### Instagram

Instagram is a 3-step flow for both images and Reels: create a media container, poll for processing, then publish.

#### Image post — `publishers/instagram.py::publish_image`

**Step 1 — Create container:**
```
POST https://graph.facebook.com/v19.0/{ig_account_id}/media
  ?access_token={page_access_token}
form-data:
  image_url={signed_fetch_url}
  caption={post.caption}
```
Response: `{ "id": "<creation_id>" }`.

**Step 2 — Poll status:**
```
GET https://graph.facebook.com/v19.0/{creation_id}?fields=status_code&access_token={page_access_token}
```
Poll every 3 seconds. Statuses:
- `IN_PROGRESS` — keep polling (max 30 sec for images)
- `FINISHED` — proceed to step 3
- `ERROR` — raise `PublishError` with the `status` field

**Step 3 — Publish:**
```
POST https://graph.facebook.com/v19.0/{ig_account_id}/media_publish
  ?access_token={page_access_token}
form-data:
  creation_id={creation_id}
```
Response: `{ "id": "<media_id>" }`. Post URL: `https://www.instagram.com/p/<shortcode>/` — the shortcode is fetched in a follow-up GET on `/{media_id}?fields=permalink`.

#### Video / Reels post — `publishers/instagram.py::publish_reel`

Same 3-step flow with these differences:

**Step 1:**
```
POST https://graph.facebook.com/v19.0/{ig_account_id}/media
form-data:
  media_type=REELS
  video_url={signed_fetch_url}
  caption={post.caption}
  share_to_feed=true
```

**Step 2:** Poll for up to 5 minutes (Reels encoding is slower than image processing). During this wait, the publisher updates the App DB row to `status="processing"` so the UI shows the right state. When `status_code=FINISHED`, advance to Step 3.

**Common error: "Media ID is not available"** — the Easter post bug from the Manus build. This happens when Step 1 responded with a creation_id but the media is still being ingested. Fix in the publisher: if Step 2 returns `IN_PROGRESS` for >5 min, raise `PublishError("Instagram failed to ingest the media file. Re-upload may be required.")` rather than letting it sit forever. Set `retry_count++` and let the worker pick it up next cycle.

**Step 3:** Same as image flow.

---

### LinkedIn

LinkedIn UGC posts have their own ceremony: register an asset upload, PUT the binary to LinkedIn's storage, then create the post referencing the asset URN.

#### Text-only post — `publishers/linkedin.py::publish_text`

```
POST https://api.linkedin.com/v2/ugcPosts
Authorization: Bearer {access_token}
Content-Type: application/json
X-Restli-Protocol-Version: 2.0.0

{
  "author": "{person_urn}",
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": { "text": "{post.caption}" },
      "shareMediaCategory": "NONE"
    }
  },
  "visibility": { "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" }
}
```

Response header: `X-RestLi-Id: {post_urn}`. Post URL: `https://www.linkedin.com/feed/update/{post_urn}`.

#### Image post — `publishers/linkedin.py::publish_image`

**Step 1 — Register asset:**
```
POST https://api.linkedin.com/v2/assets?action=registerUpload
Authorization: Bearer {access_token}

{
  "registerUploadRequest": {
    "owner": "{person_urn}",
    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
    "serviceRelationships": [{
      "relationshipType": "OWNER",
      "identifier": "urn:li:userGeneratedContent"
    }]
  }
}
```
Response includes `value.uploadMechanism["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"].uploadUrl` and `value.asset` (the URN).

**Step 2 — Upload binary:** PUT the image bytes to the upload URL with `Authorization: Bearer {access_token}` header. No body wrapping — raw bytes.

**Step 3 — Create UGC post:**
```
POST https://api.linkedin.com/v2/ugcPosts
{
  "author": "{person_urn}",
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": { "text": "{post.caption}" },
      "shareMediaCategory": "IMAGE",
      "media": [{
        "status": "READY",
        "media": "{asset_urn from step 1}"
      }]
    }
  },
  "visibility": { "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" }
}
```

#### Video post — `publishers/linkedin.py::publish_video`

Same 3-step pattern as image, with these changes:
- `recipes` in step 1: `["urn:li:digitalmediaRecipe:feedshare-video"]`
- Step 2 uses chunked upload for files > 4 MB (LinkedIn's chunk threshold)
- `shareMediaCategory` in step 3: `"VIDEO"`

**LinkedIn video processing:** Like Instagram, LinkedIn processes videos before they're playable. The post is created immediately with the video; LinkedIn handles encoding internally and the video plays once ready (typically 30 sec - 2 min). The publisher does not poll — sets `status="posted"` after Step 3 returns.

---

## Publisher dispatch — `jobs.py::publish_post`

Single entry point called by the background job:

```python
def publish_post(post: Post) -> None:
    cred = get_credential_for(post.platform)
    if not cred:
        raise PublishError(f"No credentials for {post.platform}")

    publisher = {
        ("facebook", "image"):     facebook.publish_image,
        ("facebook", "video"):     facebook.publish_video,
        ("facebook", "none"):      facebook.publish_text,
        ("instagram", "image"):    instagram.publish_image,
        ("instagram", "video"):    instagram.publish_reel,
        ("linkedin", "image"):     linkedin.publish_image,
        ("linkedin", "video"):     linkedin.publish_video,
        ("linkedin", "none"):      linkedin.publish_text,
    }[(post.platform, post.media_type)]

    fetch_url = sign_fetch_url(post.media_gcs_path) if post.media_type != "none" else None

    try:
        platform_post_id, post_url = publisher(post, cred, fetch_url)
    except PublishError as e:
        post.retry_count += 1
        if post.retry_count >= 3:
            post.status = "failed"
            post.error_message = str(e)
        # else: leave as scheduled, next cycle retries
        return

    post.status = "posted"
    post.posted_at = utcnow()
    post.platform_post_id = platform_post_id
    post.post_url = post_url
    post.error_message = None
```

Special-case: Instagram puts the post in `status="processing"` between Step 1 and Step 3. The job tracks this in a separate `_processing_posts` worker queue that polls IG for completion every 30 seconds.

---

## Instagram — text-only posts

**Not supported.** Instagram requires media on every post. If `post.platform == "instagram" AND post.media_type == "none"`, the worker raises `PublishError("Instagram requires an image or video. Add media before publishing.")` and the post moves to `status="failed"` immediately (no retry — it's a config error, not a transient one).

---

## Rate limits — what to expect

| Platform | Limit | Our usage | Risk |
|---|---|---|---|
| Facebook Page | 200 calls/hour/user | 16 posts/week ≈ 0.1 calls/hour | None |
| Instagram Business | 200 calls/hour/user across all IG endpoints | Same | None |
| LinkedIn UGC | 100 posts/day per member | <2 posts/day/member | None |

We don't need rate-limit retry logic in v1. If we ever hit one, the API returns 429 — we catch it, log, set `retry_count++`, and let the next cycle handle it.

---

## What's NOT in v1

- No multi-image carousel posts (Instagram supports up to 10; defer to v2)
- No Stories (requires different API surface; defer to v2)
- No Reels with cover image override (uses auto-generated thumbnail; defer)
- No scheduled publishing via Meta's native scheduler (we publish at the right moment ourselves; this is more reliable)
- No video transcoding (Nathan provides MP4 H.264 / AAC; if format mismatched, the platform error surfaces and Nathan re-exports)

---

*Next: `05-ai-generator.md` — Claude Sonnet 4.6 prompt with ETKM brand voice and the full request/response shape.*
