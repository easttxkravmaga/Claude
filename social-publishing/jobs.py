import logging
import threading
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from db import SessionLocal
from models import OAuthCredential, Post, PostStatus, Provider, RefreshStatus


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


def publish_due_posts() -> None:
    global _last_publish_check_at
    _set_busy(True)
    try:
        _last_publish_check_at = datetime.utcnow()
        with SessionLocal() as session:
            now = datetime.utcnow()
            due = session.query(Post).filter(
                Post.status == PostStatus.scheduled,
                Post.approved.is_(True),
                Post.scheduled_at.isnot(None),
                Post.scheduled_at <= now,
            ).limit(20).all()

            for post in due:
                # Phase F fills the publisher dispatch in. For now: log and skip.
                log.info(
                    "Publisher placeholder: would publish post id=%s platform=%s",
                    post.id, post.platform,
                )
    except Exception:
        log.exception("Publish-due-posts sweep failed")
    finally:
        _set_busy(False)


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
