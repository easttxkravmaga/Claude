"""LinkedIn UGC publisher — text, image, and video.

Image/video flow is 3-step:
  1. POST /v2/assets?action=registerUpload → get an upload URL + asset URN
  2. PUT the binary bytes to the upload URL
  3. POST /v2/ugcPosts referencing the asset URN

Text-only is one-step.
"""

from typing import Optional, Tuple

import requests

from media.gcs import parse_gcs_uri
from media.gcs import _bucket  # type: ignore  # internal helper, fine for this module
from models import OAuthCredential, Post
from security import decrypt


_LI_API = "https://api.linkedin.com"
_TIMEOUT = 60
_VIDEO_TIMEOUT = 240


def _token(cred: OAuthCredential) -> str:
    return decrypt(cred.access_token_enc)


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }


def _post_url_for(urn: str) -> str:
    # urn:li:share:1234567890 → https://www.linkedin.com/feed/update/urn:li:share:1234567890
    return f"https://www.linkedin.com/feed/update/{urn}"


def _raise_for(resp: requests.Response, what: str):
    from . import PublishError
    try:
        body = resp.json()
        msg = body.get("message", resp.text)
    except ValueError:
        msg = resp.text[:500]
    raise PublishError(f"LinkedIn {what} failed ({resp.status_code}): {msg}")


def _share_payload(author_urn: str, caption: str, media_category: str = "NONE",
                   media: Optional[list] = None) -> dict:
    share_content: dict = {
        "shareCommentary": {"text": caption},
        "shareMediaCategory": media_category,
    }
    if media:
        share_content["media"] = media
    return {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {"com.linkedin.ugc.ShareContent": share_content},
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }


def _post_ugc(payload: dict, token: str) -> str:
    resp = requests.post(
        f"{_LI_API}/v2/ugcPosts",
        json=payload,
        headers=_headers(token),
        timeout=_TIMEOUT,
    )
    if resp.status_code not in (200, 201):
        _raise_for(resp, "ugcPosts create")
    # The created post URN is in the X-RestLi-Id header (and sometimes in the body)
    urn = resp.headers.get("X-RestLi-Id") or resp.json().get("id") or ""
    if not urn:
        from . import PublishError
        raise PublishError("LinkedIn ugcPosts returned no post URN")
    return urn


def _register_upload(author_urn: str, recipe: str, token: str) -> Tuple[str, str]:
    """Returns (upload_url, asset_urn)."""
    body = {
        "registerUploadRequest": {
            "owner": author_urn,
            "recipes": [recipe],
            "serviceRelationships": [
                {"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}
            ],
        }
    }
    resp = requests.post(
        f"{_LI_API}/v2/assets?action=registerUpload",
        json=body,
        headers=_headers(token),
        timeout=_TIMEOUT,
    )
    if resp.status_code != 200:
        _raise_for(resp, "assets registerUpload")
    data = resp.json()["value"]
    upload_url = (
        data["uploadMechanism"]
        ["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]
        ["uploadUrl"]
    )
    asset_urn = data["asset"]
    return upload_url, asset_urn


def _read_blob_bytes(gcs_path: str) -> Tuple[bytes, str]:
    name = parse_gcs_uri(gcs_path)
    blob = _bucket().blob(name)
    blob.reload()
    return blob.download_as_bytes(), (blob.content_type or "application/octet-stream")


def _put_binary(upload_url: str, data: bytes, content_type: str, token: str, timeout: int) -> None:
    resp = requests.put(
        upload_url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": content_type,
        },
        timeout=timeout,
    )
    if resp.status_code not in (200, 201, 202):
        _raise_for(resp, "binary upload")


def publish_text(post: Post, cred: OAuthCredential) -> Tuple[str, Optional[str]]:
    payload = _share_payload(cred.person_urn, post.caption, "NONE")
    urn = _post_ugc(payload, _token(cred))
    return urn, _post_url_for(urn)


def publish_image(post: Post, cred: OAuthCredential, _fetch_url: str) -> Tuple[str, Optional[str]]:
    token = _token(cred)
    upload_url, asset_urn = _register_upload(
        cred.person_urn, "urn:li:digitalmediaRecipe:feedshare-image", token
    )
    data, content_type = _read_blob_bytes(post.media_gcs_path)
    _put_binary(upload_url, data, content_type, token, _TIMEOUT)
    payload = _share_payload(
        cred.person_urn, post.caption, "IMAGE",
        media=[{"status": "READY", "media": asset_urn}],
    )
    urn = _post_ugc(payload, token)
    return urn, _post_url_for(urn)


def publish_video(post: Post, cred: OAuthCredential, _fetch_url: str) -> Tuple[str, Optional[str]]:
    token = _token(cred)
    upload_url, asset_urn = _register_upload(
        cred.person_urn, "urn:li:digitalmediaRecipe:feedshare-video", token
    )
    data, content_type = _read_blob_bytes(post.media_gcs_path)
    _put_binary(upload_url, data, content_type, token, _VIDEO_TIMEOUT)
    payload = _share_payload(
        cred.person_urn, post.caption, "VIDEO",
        media=[{"status": "READY", "media": asset_urn}],
    )
    urn = _post_ugc(payload, token)
    return urn, _post_url_for(urn)
