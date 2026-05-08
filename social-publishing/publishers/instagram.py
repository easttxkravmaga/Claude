"""Instagram publisher — 3-step container/poll/publish flow.

Image flow:
  1. POST /<ig_account_id>/media with image_url + caption → creation_id
  2. Poll GET /<creation_id>?fields=status_code until FINISHED
  3. POST /<ig_account_id>/media_publish with creation_id → media_id

Reel flow: same shape with media_type=REELS + video_url.  Step 2 wait is
longer — up to 5 min for Reels vs 30 sec for images.

Manus build's "Media ID is not available" Easter bug: Step 3 fired before
Step 2 finished IN_PROGRESS.  We poll until FINISHED or raise IGProcessingPending
so the worker tries again next cycle (instead of failing the post).
"""

import time
from typing import Optional, Tuple

import requests

from models import OAuthCredential, Post
from security import decrypt


_GRAPH = "https://graph.facebook.com/v19.0"
_TIMEOUT = 60

# Per-cycle poll budgets — if exceeded, we save the creation_id and re-check
# next worker cycle rather than blocking forever.
_IMAGE_INLINE_POLLS = 10  # 10 × 3s = 30 sec
_REEL_INLINE_POLLS = 4    # 4 × 3s = 12 sec, then bail and recheck next cycle
_POLL_INTERVAL_SEC = 3


def _token(cred: OAuthCredential) -> str:
    return decrypt(cred.access_token_enc)


def _raise_for(resp: requests.Response, what: str):
    from . import PublishError
    try:
        body = resp.json()
        err = body.get("error", {})
        msg = err.get("message", resp.text)
    except ValueError:
        msg = resp.text[:500]
    raise PublishError(f"Instagram {what} failed ({resp.status_code}): {msg}")


def _create_image_container(post: Post, cred: OAuthCredential, image_url: str) -> str:
    resp = requests.post(
        f"{_GRAPH}/{cred.ig_account_id}/media",
        data={
            "image_url": image_url,
            "caption": post.caption,
            "access_token": _token(cred),
        },
        timeout=_TIMEOUT,
    )
    if resp.status_code != 200:
        _raise_for(resp, "create image container")
    return resp.json()["id"]


def _create_reel_container(post: Post, cred: OAuthCredential, video_url: str) -> str:
    resp = requests.post(
        f"{_GRAPH}/{cred.ig_account_id}/media",
        data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": post.caption,
            "share_to_feed": "true",
            "access_token": _token(cred),
        },
        timeout=_TIMEOUT,
    )
    if resp.status_code != 200:
        _raise_for(resp, "create Reel container")
    return resp.json()["id"]


def _poll_status(creation_id: str, token: str) -> str:
    resp = requests.get(
        f"{_GRAPH}/{creation_id}",
        params={"fields": "status_code", "access_token": token},
        timeout=_TIMEOUT,
    )
    if resp.status_code != 200:
        _raise_for(resp, "poll container")
    return resp.json().get("status_code", "UNKNOWN")


def _wait_until_finished(creation_id: str, token: str, max_polls: int) -> bool:
    """True = FINISHED.  False = still IN_PROGRESS (caller raises IGProcessingPending).
    Raises PublishError on ERROR / unknown terminal state."""
    from . import PublishError
    for _ in range(max_polls):
        status = _poll_status(creation_id, token)
        if status == "FINISHED":
            return True
        if status == "ERROR":
            raise PublishError(
                "Instagram failed to ingest the media file. Re-upload may be required."
            )
        if status in ("EXPIRED", "PUBLISHED"):
            # PUBLISHED would mean someone already called media_publish — treat as done
            return status == "PUBLISHED"
        time.sleep(_POLL_INTERVAL_SEC)
    return False


def _publish_container(creation_id: str, ig_account_id: str, token: str) -> str:
    resp = requests.post(
        f"{_GRAPH}/{ig_account_id}/media_publish",
        data={"creation_id": creation_id, "access_token": token},
        timeout=_TIMEOUT,
    )
    if resp.status_code != 200:
        _raise_for(resp, "media_publish")
    return resp.json()["id"]


def _permalink(media_id: str, token: str) -> Optional[str]:
    try:
        resp = requests.get(
            f"{_GRAPH}/{media_id}",
            params={"fields": "permalink", "access_token": token},
            timeout=_TIMEOUT,
        )
        if resp.status_code == 200:
            return resp.json().get("permalink")
    except requests.RequestException:
        pass
    return None


def publish_image(post: Post, cred: OAuthCredential, image_url: str) -> Tuple[str, Optional[str]]:
    from . import IGProcessingPending
    token = _token(cred)
    creation_id = _create_image_container(post, cred, image_url)
    if not _wait_until_finished(creation_id, token, _IMAGE_INLINE_POLLS):
        raise IGProcessingPending(creation_id)
    media_id = _publish_container(creation_id, cred.ig_account_id, token)
    return media_id, _permalink(media_id, token)


def publish_reel(post: Post, cred: OAuthCredential, video_url: str) -> Tuple[str, Optional[str]]:
    from . import IGProcessingPending
    token = _token(cred)
    creation_id = _create_reel_container(post, cred, video_url)
    if not _wait_until_finished(creation_id, token, _REEL_INLINE_POLLS):
        raise IGProcessingPending(creation_id)
    media_id = _publish_container(creation_id, cred.ig_account_id, token)
    return media_id, _permalink(media_id, token)


def finalize_pending(post: Post, cred: OAuthCredential, creation_id: str) -> Tuple[str, Optional[str]]:
    """Called by the worker for posts in status='processing'.  Re-checks the
    container; on FINISHED it publishes; on still-IN_PROGRESS it raises
    IGProcessingPending again to keep waiting; on ERROR/timeout it fails."""
    from . import IGProcessingPending, PublishError
    token = _token(cred)
    status = _poll_status(creation_id, token)
    if status == "FINISHED":
        media_id = _publish_container(creation_id, cred.ig_account_id, token)
        return media_id, _permalink(media_id, token)
    if status == "IN_PROGRESS":
        raise IGProcessingPending(creation_id)
    if status == "PUBLISHED":
        # Already published in a prior cycle — surface the existing media id
        return creation_id, _permalink(creation_id, token)
    raise PublishError(f"Instagram container ended in state {status}")
