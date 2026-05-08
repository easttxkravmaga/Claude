"""Facebook Page publisher — text post, photo post, video post."""

from typing import Optional, Tuple

import requests

from models import OAuthCredential, Post
from security import decrypt


_GRAPH = "https://graph.facebook.com/v19.0"
_TIMEOUT = 60


def _token(cred: OAuthCredential) -> str:
    return decrypt(cred.access_token_enc)


def _post_url_for(page_id: str, post_id: str) -> str:
    if "_" in post_id:
        return f"https://www.facebook.com/{post_id.replace('_', '/posts/')}"
    return f"https://www.facebook.com/{page_id}/posts/{post_id}"


def _video_url_for(video_id: str) -> str:
    return f"https://www.facebook.com/watch/?v={video_id}"


def _raise_for(resp: requests.Response, what: str):
    from . import PublishError
    try:
        body = resp.json()
        err = body.get("error", {})
        msg = err.get("message", resp.text)
    except ValueError:
        msg = resp.text[:500]
    raise PublishError(f"Facebook {what} failed ({resp.status_code}): {msg}")


def publish_text(post: Post, cred: OAuthCredential) -> Tuple[str, Optional[str]]:
    resp = requests.post(
        f"{_GRAPH}/{cred.page_id}/feed",
        data={
            "message": post.caption,
            "access_token": _token(cred),
            "published": "true",
        },
        timeout=_TIMEOUT,
    )
    if resp.status_code != 200:
        _raise_for(resp, "text post")
    pid = resp.json().get("id") or ""
    return pid, _post_url_for(cred.page_id, pid)


def publish_image(post: Post, cred: OAuthCredential, fetch_url: str) -> Tuple[str, Optional[str]]:
    resp = requests.post(
        f"{_GRAPH}/{cred.page_id}/photos",
        data={
            "url": fetch_url,
            "caption": post.caption,
            "access_token": _token(cred),
            "published": "true",
        },
        timeout=_TIMEOUT,
    )
    if resp.status_code != 200:
        _raise_for(resp, "photo post")
    body = resp.json()
    post_id = body.get("post_id") or body.get("id") or ""
    return post_id, _post_url_for(cred.page_id, post_id)


def publish_video(post: Post, cred: OAuthCredential, fetch_url: str) -> Tuple[str, Optional[str]]:
    """Video post via remote URL.  Facebook fetches from the signed GCS URL.

    Note: encoding may continue server-side after Facebook returns — the post
    will be visible once encoding completes (typically 1-30 min).  We don't
    poll Facebook for that here; status is set to 'posted' on receipt of the
    video ID.
    """
    resp = requests.post(
        f"{_GRAPH}/{cred.page_id}/videos",
        data={
            "file_url": fetch_url,
            "description": post.caption,
            "access_token": _token(cred),
            "published": "true",
        },
        timeout=_TIMEOUT * 2,
    )
    if resp.status_code != 200:
        _raise_for(resp, "video post")
    video_id = resp.json().get("id") or ""
    return video_id, _video_url_for(video_id)
