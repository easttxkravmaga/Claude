import logging
import threading
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select

from db import SessionLocal
from models import OAuthCredential, Platform, Post, PostStatus, Provider, RefreshStatus


log = logging.getLogger(__name__)

_scheduler: BackgroundScheduler | None = None
_busy_lock = threading.Lock()
_busy = False
_last_token_refresh_at: datetime | None = None
_last_publish_check_at: datetime | None = None


def is_busy() -> bool:
    return _busy


def status() -> dict:
    return {
        "busy": _busy,
        "next_token_refresh_at": _last_token_refresh_at.isoformat() + "Z"
            if _last_token_refresh_at else None,
        "next_publish_check_at": _last_publish_check_at.isoformat() + "Z"
            if _last_publish_check_at else None,
    }


def _set_busy(value: bool) -> None:
    global _busy
    with _busy_lock:
        _busy = value


# ── Token refresh sweep ────────────────────────────────────────────────────────
def token_refresh_sweep() -> None:
    from auth import linkedin as li_auth, meta as meta_auth

    global _last_token_refresh_at
    _set_busy(True)
    try:
        _last_token_refresh_at = datetime.utcnow()
        with SessionLocal() as session:
            cutoff = datetime.utcnow() + timedelta(days=7)
            expiring = session.query(OAuthCredential).filter(
                OAuthCredential.expires_at.isnot(None),
                OAuthCredential.expires_at < cutoff,
            ).all()

            for cred in expiring:
                try:
                    if cred.provider == Provider.linkedin:
                        li_auth.refresh(cred)
                    elif cred.provider == Provider.meta:
                        meta_auth.refresh(cred)
                except Exception as e:
                    log.exception("Refresh failed for credential id=%s", cred.id)
                    cred.last_refresh_status = RefreshStatus.failed
                    cred.last_refresh_error = str(e)[:500]
                    cred.last_refresh_at = datetime.utcnow()
            session.commit()
    except Exception:
        log.exception("Token refresh sweep failed")
    finally:
        _set_busy(False)


# ── Post publisher ─────────────────────────────────────────────────────────────
def _provider_for_platform(platform: Platform) -> Provider:
    return Provider.linkedin if platform == Platform.linkedin else Provider.meta


def _credential_for(session, platform: Platform) -> OAuthCredential | None:
    return session.scalar(
        select(OAuthCredential).where(
            OAuthCredential.provider == _provider_for_platform(platform)
        )
    )


_MAX_RETRIES = 3


def _publish_one(session, post: Post) -> None:
    """Publish a single Post row.  Updates fields in place; caller commits."""
    from publishers import dispatch, IGProcessingPending, PublishError

    cred = _credential_for(session, post.platform)
    if not cred:
        post.status = PostStatus.failed
        post.error_message = (
            f"No credentials for {post.platform.value}. "
            f"Set up the {post.platform.value} integration first."
        )
        return

    post.status = PostStatus.posting
    session.flush()  # surface the 'posting' state if anyone polls

    try:
        platform_post_id, post_url = dispatch(post, cred)
    except IGProcessingPending as p:
        post.status = PostStatus.processing
        post.platform_post_id = p.creation_id  # stash so we can poll next cycle
        post.error_message = None
        return
    except PublishError as e:
        post.retry_count = (post.retry_count or 0) + 1
        if post.retry_count >= _MAX_RETRIES:
            post.status = PostStatus.failed
            post.error_message = str(e)
        else:
            post.status = PostStatus.scheduled  # let next cycle retry
            post.error_message = str(e)
        return
    except Exception as e:
        log.exception("Unexpected publisher exception for post id=%s", post.id)
        post.status = PostStatus.failed
        post.error_message = f"Unexpected error: {e}"
        return

    post.status = PostStatus.posted
    post.posted_at = datetime.utcnow()
    post.platform_post_id = platform_post_id
    post.post_url = post_url
    post.error_message = None


def _continue_processing(session, post: Post) -> None:
    """For posts in status='processing' (IG ingest pending) — re-check the container."""
    from publishers import continue_ig_processing, IGProcessingPending, PublishError

    cred = _credential_for(session, post.platform)
    if not cred:
        post.status = PostStatus.failed
        post.error_message = "Credential disappeared while post was processing."
        return

    try:
        platform_post_id, post_url = continue_ig_processing(post, cred)
    except IGProcessingPending:
        return  # still pending, leave row as 'processing'
    except PublishError as e:
        post.retry_count = (post.retry_count or 0) + 1
        if post.retry_count >= _MAX_RETRIES:
            post.status = PostStatus.failed
            post.error_message = str(e)
        else:
            post.status = PostStatus.scheduled  # restart from container creation
            post.platform_post_id = None
            post.error_message = str(e)
        return

    post.status = PostStatus.posted
    post.posted_at = datetime.utcnow()
    post.platform_post_id = platform_post_id
    post.post_url = post_url
    post.error_message = None


def publish_due_posts() -> None:
    global _last_publish_check_at
    _set_busy(True)
    try:
        _last_publish_check_at = datetime.utcnow()
        with SessionLocal() as session:
            now = datetime.utcnow()

            # 1. Drive any posts in 'processing' state forward
            processing = session.scalars(
                select(Post).where(Post.status == PostStatus.processing).limit(20)
            ).all()
            for post in processing:
                _continue_processing(session, post)
            session.commit()

            # 2. Publish newly-due scheduled posts
            due = session.scalars(
                select(Post).where(
                    Post.status == PostStatus.scheduled,
                    Post.approved.is_(True),
                    Post.scheduled_at.isnot(None),
                    Post.scheduled_at <= now,
                ).limit(20)
            ).all()
            for post in due:
                _publish_one(session, post)
            session.commit()

    except Exception:
        log.exception("Publish-due-posts sweep failed")
    finally:
        _set_busy(False)


def publish_now(post_id: int) -> None:
    """Synchronous publish — used by /api/posts/<id>/publish.

    The route writes the result; we just dispatch.  Worth noting: IG Reels
    may return IGProcessingPending which leaves the post in 'processing'
    state and the worker picks it up next cycle.
    """
    with SessionLocal() as session:
        post = session.get(Post, post_id)
        if not post:
            return
        _publish_one(session, post)
        session.commit()


# ── Scheduler lifecycle ────────────────────────────────────────────────────────
def start() -> BackgroundScheduler:
    global _scheduler
    if _scheduler is not None:
        return _scheduler

    sched = BackgroundScheduler(daemon=True)
    sched.add_job(
        token_refresh_sweep,
        "interval",
        hours=6,
        id="token_refresh_sweep",
        next_run_time=datetime.utcnow() + timedelta(seconds=30),
    )
    sched.add_job(
        publish_due_posts,
        "interval",
        seconds=60,
        id="publish_due_posts",
        next_run_time=datetime.utcnow() + timedelta(seconds=60),
    )
    sched.start()
    _scheduler = sched
    log.info("APScheduler started: token_refresh_sweep (6h), publish_due_posts (60s)")
    return sched


def stop() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
