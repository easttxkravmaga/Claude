"""Per-platform publisher dispatch.

Each publisher returns (platform_post_id, post_url) on success or raises
PublishError on failure.  Two special cases:

  * Instagram image / Reel — handled in instagram.py via a 3-step container/
    poll/publish flow.  IG Reels may set status='processing' while encoding;
    the worker polls again next cycle until FINISHED.
  * Text-only posts on Instagram — not supported (IG requires media).
"""

from typing import Optional, Tuple

from media.gcs import signed_get_url
from models import MediaType, OAuthCredential, Platform, Post

from . import facebook, instagram, linkedin


class PublishError(Exception):
    """Raised when a platform publish call fails."""


class IGProcessingPending(Exception):
    """Raised when an IG container is still processing — caller leaves the post
    in status='processing' and re-checks next cycle."""

    def __init__(self, creation_id: str):
        super().__init__("Instagram media still processing")
        self.creation_id = creation_id


def fetch_url_for(post: Post) -> Optional[str]:
    if post.media_type == MediaType.none or not post.media_gcs_path:
        return None
    return signed_get_url(post.media_gcs_path, expires_minutes=10)


def dispatch(post: Post, cred: OAuthCredential) -> Tuple[str, Optional[str]]:
    """Run the right publisher for a post.  Returns (platform_post_id, post_url).

    Raises PublishError on platform error, IGProcessingPending if IG is still
    encoding the media.
    """
    fetch_url = fetch_url_for(post)

    if post.platform == Platform.facebook:
        if post.media_type == MediaType.video:
            return facebook.publish_video(post, cred, fetch_url)
        if post.media_type == MediaType.image:
            return facebook.publish_image(post, cred, fetch_url)
        return facebook.publish_text(post, cred)

    if post.platform == Platform.instagram:
        if post.media_type == MediaType.none:
            raise PublishError(
                "Instagram requires an image or video. Add media before publishing."
            )
        if post.media_type == MediaType.video:
            return instagram.publish_reel(post, cred, fetch_url)
        return instagram.publish_image(post, cred, fetch_url)

    if post.platform == Platform.linkedin:
        if post.media_type == MediaType.video:
            return linkedin.publish_video(post, cred, fetch_url)
        if post.media_type == MediaType.image:
            return linkedin.publish_image(post, cred, fetch_url)
        return linkedin.publish_text(post, cred)

    raise PublishError(f"Unsupported platform: {post.platform}")


def continue_ig_processing(post: Post, cred: OAuthCredential) -> Tuple[str, Optional[str]]:
    """Called by the worker when a post is in status='processing' to check the
    IG container and finalize publish if ready."""
    if not post.platform_post_id:
        raise PublishError("Post in processing state but no IG creation_id stored")
    return instagram.finalize_pending(post, cred, post.platform_post_id)
