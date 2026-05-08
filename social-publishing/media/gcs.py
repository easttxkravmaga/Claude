"""Google Cloud Storage helpers — bucket access, signed URLs, blob metadata."""

import os
import re
from datetime import timedelta
from typing import Optional

from google.cloud import storage


_BUCKET_NAME = os.environ.get("GCS_BUCKET", "etkm-social-media-assets")
_PROJECT_ID = os.environ.get("GCS_PROJECT_ID")

_client: Optional[storage.Client] = None


def _get_client() -> storage.Client:
    global _client
    if _client is None:
        _client = storage.Client(project=_PROJECT_ID) if _PROJECT_ID else storage.Client()
    return _client


def _bucket():
    return _get_client().bucket(_BUCKET_NAME)


def slugify(value: str, max_len: int = 40) -> str:
    """URL-safe slug for object keys."""
    s = re.sub(r"[^a-zA-Z0-9-]+", "-", (value or "").lower()).strip("-")
    return (s or "post")[:max_len]


def object_path(year: int, month: int, post_id: int | str, slug: str, ext: str) -> str:
    """Build a deterministic object key.  Used for all uploads."""
    return f"{year:04d}/{month:02d}/{post_id}-{slug}.{ext.lstrip('.')}"


def gcs_uri(object_name: str) -> str:
    return f"gs://{_BUCKET_NAME}/{object_name}"


def parse_gcs_uri(uri: str) -> str:
    """gs://bucket/path → path."""
    if not uri.startswith("gs://"):
        return uri
    rest = uri[len("gs://"):]
    parts = rest.split("/", 1)
    if len(parts) != 2:
        raise ValueError(f"Malformed GCS URI: {uri}")
    return parts[1]


def upload_bytes(object_name: str, data: bytes, content_type: str) -> None:
    blob = _bucket().blob(object_name)
    blob.upload_from_string(data, content_type=content_type)


def signed_put_url(object_name: str, content_type: str, expires_minutes: int = 15) -> str:
    """Generate a V4 signed PUT URL — used by the browser for direct video upload.

    The browser must include the SAME `Content-Type` header it requested when
    PUTting, otherwise GCS will reject the signature.
    """
    blob = _bucket().blob(object_name)
    return blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expires_minutes),
        method="PUT",
        content_type=content_type,
    )


def signed_get_url(object_name_or_uri: str, expires_minutes: int = 10) -> str:
    """Generate a V4 signed GET URL — used at publish time so platforms can fetch the media."""
    name = parse_gcs_uri(object_name_or_uri)
    blob = _bucket().blob(name)
    return blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expires_minutes),
        method="GET",
    )


def get_blob_metadata(object_name_or_uri: str) -> dict:
    """Return {size, content_type, exists}.  Reloads blob to fetch latest server-side fields."""
    name = parse_gcs_uri(object_name_or_uri)
    blob = _bucket().blob(name)
    blob.reload()
    return {
        "size": blob.size,
        "content_type": blob.content_type,
        "exists": True,
    }


def delete_blob(object_name_or_uri: str) -> bool:
    name = parse_gcs_uri(object_name_or_uri)
    blob = _bucket().blob(name)
    if not blob.exists():
        return False
    blob.delete()
    return True
