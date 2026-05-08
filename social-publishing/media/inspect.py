"""Video metadata inspection via ffprobe (bundled in the Cloud Run image)."""

import json
import logging
import math
import subprocess
from typing import Optional

log = logging.getLogger(__name__)


def gcd_aspect(width: int, height: int) -> str:
    """1920x1080 → '16:9', 1080x1920 → '9:16', 1080x1080 → '1:1'."""
    if not width or not height:
        return ""
    g = math.gcd(width, height)
    return f"{width // g}:{height // g}"


def probe_video(url_or_path: str, timeout: int = 30) -> dict:
    """Run ffprobe against a URL or local path.  Returns {duration_sec, width, height, aspect_ratio}.

    On failure or missing fields, returns the partial dict — callers should treat fields as optional.
    """
    cmd = [
        "ffprobe", "-v", "error",
        "-print_format", "json",
        "-show_format", "-show_streams",
        url_or_path,
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        log.warning("ffprobe failed: %s", e)
        return {}

    if result.returncode != 0:
        log.warning("ffprobe non-zero exit %s: %s", result.returncode, result.stderr[:300])
        return {}

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}

    out: dict = {}
    fmt = data.get("format", {})
    if "duration" in fmt:
        try:
            out["duration_sec"] = int(round(float(fmt["duration"])))
        except (TypeError, ValueError):
            pass

    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video":
            w = stream.get("width")
            h = stream.get("height")
            if w and h:
                out["width"] = w
                out["height"] = h
                out["aspect_ratio"] = gcd_aspect(w, h)
            break

    return out


def is_vertical_for_reels(aspect_ratio: str) -> bool:
    """Instagram Reels expect 9:16.  Anything else triggers the warning."""
    return aspect_ratio == "9:16"


def infer_extension(content_type: str) -> Optional[str]:
    return {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/gif": "gif",
        "image/webp": "webp",
        "video/mp4": "mp4",
        "video/quicktime": "mov",
    }.get((content_type or "").lower())
