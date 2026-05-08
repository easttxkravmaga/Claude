import calendar as pycal
import logging
import os
from datetime import date, datetime, timedelta

from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy import desc, func, select

from auth_basic import require_basic_auth
from auth import linkedin as li_auth
from auth import meta as meta_auth
from db import SessionLocal, init_db
import jobs
from models import (
    Batch,
    BatchSource,
    MediaType,
    OAuthCredential,
    Platform,
    Post,
    PostStatus,
    Provider,
    RefreshStatus,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)


_PLATFORM_LIMITS = {
    Platform.facebook: 63206,
    Platform.instagram: 2200,
    Platform.linkedin: 3000,
}


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["JSON_SORT_KEYS"] = False
    app.secret_key = os.environ["APP_SECRET_KEY"]

    init_db()

    if os.environ.get("DISABLE_SCHEDULER") != "1":
        jobs.start()

    # ── Health ───────────────────────────────────────────────────────────────
    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "service": "etkm-social-publishing"})

    # ── Pages ────────────────────────────────────────────────────────────────
    @app.route("/")
    @require_basic_auth
    def home():
        return render_template("home.html", status=_home_status())

    @app.route("/scheduler")
    @require_basic_auth
    def scheduler():
        tab = (request.args.get("tab") or "calendar").lower()
        ctx = {"tab": tab, "stats": _post_stats()}

        if tab == "calendar":
            ym = request.args.get("month", "")
            try:
                yr, mo = (int(x) for x in ym.split("-")) if ym else (date.today().year, date.today().month)
            except (ValueError, AttributeError):
                yr, mo = date.today().year, date.today().month
            ctx["calendar"] = _build_calendar(yr, mo)
            return render_template("scheduler_calendar.html", **ctx)

        if tab == "all":
            ctx["posts"] = _list_posts(
                platform=request.args.get("platform"),
                status=request.args.get("status"),
                campaign_tag=request.args.get("campaign_tag"),
                limit=200,
            )
            return render_template("scheduler_all_posts.html", **ctx)

        if tab == "compose":
            ctx["edit_post"] = None
            ctx["prefill_date"] = request.args.get("date")
            ctx["platform_limits"] = {
                "facebook": _PLATFORM_LIMITS[Platform.facebook],
                "instagram": _PLATFORM_LIMITS[Platform.instagram],
                "linkedin": _PLATFORM_LIMITS[Platform.linkedin],
            }
            return render_template("scheduler_compose.html", **ctx)

        if tab == "ai":
            return render_template("scheduler_ai.html", **ctx)

        return redirect(url_for("scheduler"))

    @app.route("/linkedin")
    @require_basic_auth
    def linkedin_setup():
        redirect_uri = os.environ.get(
            "LINKEDIN_REDIRECT_URI",
            "(set LINKEDIN_REDIRECT_URI env var after deploy)",
        )
        return render_template("linkedin.html", redirect_uri=redirect_uri)

    @app.route("/meta")
    @require_basic_auth
    def meta_setup():
        return render_template("meta.html")

    @app.route("/dashboard")
    @require_basic_auth
    def dashboard():
        with SessionLocal() as s:
            rows = s.scalars(select(OAuthCredential).order_by(OAuthCredential.id)).all()
            grouped = {"linkedin": [], "meta": []}
            for r in rows:
                provider = r.provider.value if hasattr(r.provider, "value") else r.provider
                grouped.setdefault(provider, []).append(_serialize_credential(r))
        return render_template("dashboard.html", grouped=grouped)

    # ── Scheduler status JSON ────────────────────────────────────────────────
    @app.route("/api/scheduler/status")
    @require_basic_auth
    def scheduler_status():
        return jsonify(jobs.status())

    # ── OAuth: LinkedIn ──────────────────────────────────────────────────────
    @app.route("/api/oauth/linkedin/start", methods=["POST"])
    @require_basic_auth
    def linkedin_start():
        data = request.get_json(force=True, silent=True) or request.form
        client_id = (data.get("client_id") or "").strip()
        client_secret = (data.get("client_secret") or "").strip()
        if not client_id or not client_secret:
            return jsonify({"ok": False, "error": "client_id and client_secret are required"}), 400

        state = li_auth.new_state()
        session["linkedin_oauth"] = {
            "state": state,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        try:
            authorize_url = li_auth.build_authorize_url(client_id, state)
        except li_auth.LinkedInError as e:
            return jsonify({"ok": False, "error": str(e)}), 500
        return jsonify({"ok": True, "redirect": authorize_url})

    @app.route("/api/oauth/linkedin/callback")
    @require_basic_auth
    def linkedin_callback():
        code = request.args.get("code")
        state = request.args.get("state")
        error = request.args.get("error")
        error_desc = request.args.get("error_description")

        stash = session.pop("linkedin_oauth", None)
        if error:
            return _error_page(f"LinkedIn returned an error: {error} — {error_desc or ''}")
        if not code or not state or not stash:
            return _error_page("Missing code/state, or session expired. Try again from /linkedin.")
        if state != stash["state"]:
            return _error_page("State mismatch. Possible CSRF — request rejected.")

        try:
            token_payload = li_auth.exchange_code(
                code=code,
                client_id=stash["client_id"],
                client_secret=stash["client_secret"],
            )
            person_urn = li_auth.fetch_person_urn(token_payload["access_token"])
            li_auth.store_credential(
                client_id=stash["client_id"],
                client_secret=stash["client_secret"],
                token_payload=token_payload,
                person_urn=person_urn,
            )
        except li_auth.LinkedInError as e:
            return _error_page(str(e))

        return redirect(url_for("dashboard"))

    # ── OAuth: Meta ──────────────────────────────────────────────────────────
    @app.route("/api/oauth/meta/exchange", methods=["POST"])
    @require_basic_auth
    def meta_exchange():
        data = request.get_json(force=True, silent=True) or request.form
        app_id = (data.get("app_id") or "").strip()
        app_secret = (data.get("app_secret") or "").strip()
        short_token = (data.get("short_lived_token") or "").strip()
        if not app_id or not app_secret or not short_token:
            return jsonify({
                "ok": False,
                "error": "app_id, app_secret, and short_lived_token are required",
            }), 400

        try:
            cred = meta_auth.exchange(app_id, app_secret, short_token)
        except meta_auth.MetaError as e:
            return jsonify({"ok": False, "error": str(e)}), 400

        return jsonify({
            "ok": True,
            "credential_id": cred.id,
            "page_id": cred.page_id,
            "ig_account_id": cred.ig_account_id,
            "redirect": url_for("dashboard"),
        })

    # ── Credentials ──────────────────────────────────────────────────────────
    @app.route("/api/credentials")
    @require_basic_auth
    def credentials_list():
        with SessionLocal() as s:
            rows = s.scalars(select(OAuthCredential).order_by(OAuthCredential.id)).all()
            return jsonify({"ok": True, "credentials": [_serialize_credential(r) for r in rows]})

    @app.route("/api/credentials/<int:cred_id>/refresh", methods=["POST"])
    @require_basic_auth
    def credentials_refresh(cred_id: int):
        with SessionLocal() as s:
            cred = s.get(OAuthCredential, cred_id)
            if not cred:
                abort(404)
            try:
                if cred.provider == Provider.linkedin:
                    li_auth.refresh(cred)
                elif cred.provider == Provider.meta:
                    meta_auth.refresh(cred)
            except Exception as e:
                cred.last_refresh_status = RefreshStatus.failed
                cred.last_refresh_error = str(e)[:500]
                cred.last_refresh_at = datetime.utcnow()
            s.commit()
            s.refresh(cred)
            return jsonify({"ok": True, "credential": _serialize_credential(cred)})

    @app.route("/api/credentials/<int:cred_id>", methods=["DELETE"])
    @require_basic_auth
    def credentials_delete(cred_id: int):
        with SessionLocal() as s:
            cred = s.get(OAuthCredential, cred_id)
            if not cred:
                abort(404)
            s.delete(cred)
            s.commit()
            return jsonify({"ok": True})

    # ── Posts ────────────────────────────────────────────────────────────────
    @app.route("/api/posts")
    @require_basic_auth
    def posts_list():
        return jsonify({
            "ok": True,
            "posts": _list_posts(
                platform=request.args.get("platform"),
                status=request.args.get("status"),
                campaign_tag=request.args.get("campaign_tag"),
                group_id=request.args.get("group_id"),
                limit=int(request.args.get("limit", 200)),
                offset=int(request.args.get("offset", 0)),
            ),
        })

    @app.route("/api/posts", methods=["POST"])
    @require_basic_auth
    def posts_create():
        data = request.get_json(force=True, silent=True) or {}
        title = (data.get("title") or "").strip()
        master_caption = (data.get("master_caption") or data.get("caption") or "").strip()
        platforms = data.get("platforms") or []
        per_platform_captions = data.get("per_platform_captions") or {}
        scheduled_at = _parse_dt(data.get("scheduled_at"))
        campaign_tag = (data.get("campaign_tag") or "").strip() or None
        approved = bool(data.get("approved"))
        status_str = (data.get("status") or "draft").lower()
        media = data.get("media") or {}

        if not title:
            return jsonify({"ok": False, "error": "title is required"}), 400
        if not platforms:
            return jsonify({"ok": False, "error": "at least one platform is required"}), 400
        if status_str not in {"draft", "scheduled"}:
            return jsonify({"ok": False, "error": "status must be draft or scheduled"}), 400

        try:
            target_status = PostStatus(status_str)
        except ValueError:
            return jsonify({"ok": False, "error": "invalid status"}), 400

        if target_status == PostStatus.scheduled and not scheduled_at:
            return jsonify({"ok": False, "error": "scheduled_at is required when status=scheduled"}), 400

        valid_platforms = {p.value for p in Platform}
        for p in platforms:
            if p not in valid_platforms:
                return jsonify({"ok": False, "error": f"invalid platform: {p}"}), 400

        import uuid
        group_id = str(uuid.uuid4())
        created_ids = []

        with SessionLocal() as s:
            for p in platforms:
                platform_enum = Platform(p)
                caption = per_platform_captions.get(p) or master_caption
                if len(caption) > _PLATFORM_LIMITS[platform_enum]:
                    return jsonify({
                        "ok": False,
                        "error": f"{p} caption exceeds {_PLATFORM_LIMITS[platform_enum]} char limit",
                    }), 400

                post = Post(
                    post_group_id=group_id,
                    title=title,
                    caption=caption,
                    platform=platform_enum,
                    media_type=MediaType(media.get("media_type", "none")),
                    media_gcs_path=media.get("gcs_path"),
                    media_mime=media.get("mime"),
                    media_size_bytes=media.get("size"),
                    media_duration_sec=media.get("duration_sec"),
                    media_aspect_ratio=media.get("aspect_ratio"),
                    scheduled_at=scheduled_at,
                    campaign_tag=campaign_tag,
                    status=target_status,
                    approved=approved,
                )
                s.add(post)
                s.flush()
                created_ids.append(post.id)
            s.commit()

        return jsonify({
            "ok": True,
            "post_group_id": group_id,
            "post_ids": created_ids,
            "redirect": url_for("scheduler", tab="all"),
        })

    @app.route("/api/posts/<int:post_id>")
    @require_basic_auth
    def posts_get(post_id: int):
        with SessionLocal() as s:
            p = s.get(Post, post_id)
            if not p:
                abort(404)
            return jsonify({"ok": True, "post": _serialize_post(p)})

    @app.route("/api/posts/group/<group_id>")
    @require_basic_auth
    def posts_get_group(group_id: str):
        with SessionLocal() as s:
            rows = s.scalars(
                select(Post).where(Post.post_group_id == group_id).order_by(Post.id)
            ).all()
            return jsonify({"ok": True, "posts": [_serialize_post(p) for p in rows]})

    @app.route("/api/posts/<int:post_id>", methods=["PATCH"])
    @require_basic_auth
    def posts_patch(post_id: int):
        data = request.get_json(force=True, silent=True) or {}
        with SessionLocal() as s:
            p = s.get(Post, post_id)
            if not p:
                abort(404)
            _apply_patch(p, data)
            s.commit()
            s.refresh(p)
            return jsonify({"ok": True, "post": _serialize_post(p)})

    @app.route("/api/posts/<int:post_id>", methods=["DELETE"])
    @require_basic_auth
    def posts_delete(post_id: int):
        with SessionLocal() as s:
            p = s.get(Post, post_id)
            if not p:
                abort(404)
            s.delete(p)
            s.commit()
            return jsonify({"ok": True})

    @app.route("/api/posts/group/<group_id>", methods=["DELETE"])
    @require_basic_auth
    def posts_group_delete(group_id: str):
        with SessionLocal() as s:
            rows = s.scalars(select(Post).where(Post.post_group_id == group_id)).all()
            count = 0
            for p in rows:
                s.delete(p)
                count += 1
            s.commit()
            return jsonify({"ok": True, "deleted": count})

    @app.route("/api/posts/<int:post_id>/approve", methods=["POST"])
    @require_basic_auth
    def posts_approve(post_id: int):
        with SessionLocal() as s:
            p = s.get(Post, post_id)
            if not p:
                abort(404)
            p.approved = True
            s.commit()
            s.refresh(p)
            return jsonify({"ok": True, "post": _serialize_post(p)})

    @app.route("/api/posts/<int:post_id>/retry", methods=["POST"])
    @require_basic_auth
    def posts_retry(post_id: int):
        with SessionLocal() as s:
            p = s.get(Post, post_id)
            if not p:
                abort(404)
            p.status = PostStatus.scheduled
            p.error_message = None
            p.retry_count = 0
            s.commit()
            s.refresh(p)
            return jsonify({"ok": True, "post": _serialize_post(p)})

    return app


# ── Helpers ────────────────────────────────────────────────────────────────────

def _parse_dt(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except (ValueError, AttributeError):
        return None


def _apply_patch(p: Post, data: dict) -> None:
    if "title" in data:
        p.title = data["title"]
    if "caption" in data:
        p.caption = data["caption"]
    if "scheduled_at" in data:
        p.scheduled_at = _parse_dt(data["scheduled_at"])
    if "campaign_tag" in data:
        p.campaign_tag = data["campaign_tag"] or None
    if "approved" in data:
        p.approved = bool(data["approved"])
    if "status" in data and data["status"] in {s.value for s in PostStatus}:
        p.status = PostStatus(data["status"])


def _list_posts(platform=None, status=None, campaign_tag=None, group_id=None, limit=200, offset=0):
    with SessionLocal() as s:
        q = select(Post)
        if platform:
            try:
                q = q.where(Post.platform == Platform(platform))
            except ValueError:
                pass
        if status:
            try:
                q = q.where(Post.status == PostStatus(status))
            except ValueError:
                pass
        if campaign_tag:
            q = q.where(Post.campaign_tag == campaign_tag)
        if group_id:
            q = q.where(Post.post_group_id == group_id)
        q = q.order_by(desc(Post.scheduled_at), desc(Post.id)).limit(limit).offset(offset)
        return [_serialize_post(p) for p in s.scalars(q).all()]


def _post_stats() -> dict:
    with SessionLocal() as s:
        total = s.scalar(select(func.count(Post.id))) or 0
        draft = s.scalar(select(func.count(Post.id)).where(Post.status == PostStatus.draft)) or 0
        scheduled = s.scalar(select(func.count(Post.id)).where(Post.status == PostStatus.scheduled)) or 0
        approved = s.scalar(select(func.count(Post.id)).where(Post.approved.is_(True))) or 0
        return {"total": total, "draft": draft, "scheduled": scheduled, "approved": approved}


def _home_status() -> dict:
    with SessionLocal() as s:
        # OAuth health
        creds = s.scalars(select(OAuthCredential)).all()
        n_credentials = len(creds)
        n_failed = sum(1 for c in creds if c.last_refresh_status == RefreshStatus.failed)
        soon = datetime.utcnow() + timedelta(days=7)
        n_expiring = sum(
            1 for c in creds
            if c.expires_at is not None and c.expires_at < soon and c.last_refresh_status != RefreshStatus.failed
        )
        if n_credentials == 0:
            oauth_text, oauth_class = "No credentials yet", "etkm-pill etkm-pill--neutral"
        elif n_failed:
            oauth_text = f"{n_failed} credential{'s' if n_failed > 1 else ''} expired — re-authorize"
            oauth_class = "etkm-pill etkm-pill--red"
        elif n_expiring:
            oauth_text = f"{n_expiring} credential{'s' if n_expiring > 1 else ''} expiring within 7 days"
            oauth_class = "etkm-pill etkm-pill--orange"
        else:
            oauth_text = "All credentials current"
            oauth_class = "etkm-pill etkm-pill--green"

        # Queue depth
        now = datetime.utcnow()
        upcoming = s.scalars(
            select(Post)
            .where(
                Post.status == PostStatus.scheduled,
                Post.approved.is_(True),
                Post.scheduled_at.isnot(None),
                Post.scheduled_at >= now,
            )
            .order_by(Post.scheduled_at)
            .limit(1)
        ).first()
        n_queued = s.scalar(
            select(func.count(Post.id))
            .where(
                Post.status == PostStatus.scheduled,
                Post.approved.is_(True),
                Post.scheduled_at.isnot(None),
                Post.scheduled_at >= now,
            )
        ) or 0
        if n_queued == 0:
            queue_text = "Nothing scheduled"
        else:
            next_at = upcoming.scheduled_at.strftime("%a %b %-d, %-I:%M %p") if upcoming else "(unknown)"
            queue_text = f"{n_queued} post{'s' if n_queued != 1 else ''} scheduled · next at {next_at}"

        # Last published
        last = s.scalars(
            select(Post).where(Post.status == PostStatus.posted, Post.posted_at.isnot(None))
            .order_by(desc(Post.posted_at)).limit(1)
        ).first()
        if last:
            ago = _humanize_delta(datetime.utcnow() - last.posted_at)
            last_text = f"Posted to {last.platform.value.capitalize()} · {ago} · "
            last_url = last.post_url
        else:
            last_text = "No posts yet"
            last_url = None

        return {
            "oauth_text": oauth_text,
            "oauth_class": oauth_class,
            "queue_text": queue_text,
            "last_text": last_text,
            "last_url": last_url,
        }


def _humanize_delta(d: timedelta) -> str:
    s = int(d.total_seconds())
    if s < 60: return "just now"
    if s < 3600: return f"{s // 60} min ago"
    if s < 86400: return f"{s // 3600} hr ago"
    return f"{s // 86400} days ago"


def _build_calendar(year: int, month: int) -> dict:
    """Server-side month grid generation. Returns weeks of cells."""
    today = date.today()
    cal = pycal.Calendar(firstweekday=6)  # Sunday-first
    weeks = []
    with SessionLocal() as s:
        first = date(year, month, 1)
        # Get bounds of the calendar grid (may include trailing days from
        # adjacent months, so widen by 7 on each side).
        start = first - timedelta(days=14)
        if month == 12:
            end = date(year + 1, 1, 1) + timedelta(days=14)
        else:
            end = date(year, month + 1, 1) + timedelta(days=14)

        rows = s.scalars(
            select(Post).where(
                Post.scheduled_at.isnot(None),
                Post.scheduled_at >= datetime.combine(start, datetime.min.time()),
                Post.scheduled_at <= datetime.combine(end, datetime.max.time()),
            )
        ).all()
        events_by_date: dict[date, list] = {}
        for p in rows:
            dkey = p.scheduled_at.date()
            events_by_date.setdefault(dkey, []).append({
                "id": p.id,
                "platform": p.platform.value,
                "title": p.title,
                "caption": (p.caption or "")[:60],
                "status": p.status.value,
            })

    for week in cal.monthdatescalendar(year, month):
        cells = []
        for d in week:
            cells.append({
                "date": d,
                "iso": d.isoformat(),
                "day": d.day,
                "in_month": d.month == month,
                "is_today": d == today,
                "events": events_by_date.get(d, []),
            })
        weeks.append(cells)

    prev_year = year if month > 1 else year - 1
    prev_month = month - 1 if month > 1 else 12
    next_year = year if month < 12 else year + 1
    next_month = month + 1 if month < 12 else 1

    return {
        "year": year,
        "month": month,
        "month_name": pycal.month_name[month],
        "weeks": weeks,
        "prev": f"{prev_year:04d}-{prev_month:02d}",
        "next_": f"{next_year:04d}-{next_month:02d}",
        "today": f"{today.year:04d}-{today.month:02d}",
    }


def _serialize_credential(cred: OAuthCredential) -> dict:
    expires_at = cred.expires_at
    expiring_soon = (
        expires_at is not None and expires_at < datetime.utcnow() + timedelta(days=7)
    )
    failed = cred.last_refresh_status == RefreshStatus.failed
    if failed:
        status_label, status_class = "Expired", "etkm-pill etkm-pill--red"
    elif expires_at is None:
        status_label, status_class = "Never expires", "etkm-pill etkm-pill--blue"
    elif expiring_soon:
        status_label, status_class = "Expiring soon", "etkm-pill etkm-pill--orange"
    else:
        status_label, status_class = "Active", "etkm-pill etkm-pill--green"

    return {
        "id": cred.id,
        "provider": cred.provider.value if hasattr(cred.provider, "value") else cred.provider,
        "label": cred.label,
        "client_id": cred.client_id,
        "person_urn": cred.person_urn,
        "page_id": cred.page_id,
        "ig_account_id": cred.ig_account_id,
        "expires_at": cred.expires_at.isoformat() + "Z" if cred.expires_at else None,
        "last_refresh_at": cred.last_refresh_at.isoformat() + "Z" if cred.last_refresh_at else None,
        "last_refresh_status": cred.last_refresh_status.value if cred.last_refresh_status else None,
        "last_refresh_error": cred.last_refresh_error,
        "status_label": status_label,
        "status_class": status_class,
        "created_at": cred.created_at.isoformat() + "Z" if cred.created_at else None,
    }


def _serialize_post(p: Post) -> dict:
    return {
        "id": p.id,
        "post_group_id": p.post_group_id,
        "title": p.title,
        "caption": p.caption,
        "platform": p.platform.value,
        "media_type": p.media_type.value if p.media_type else "none",
        "media_gcs_path": p.media_gcs_path,
        "media_mime": p.media_mime,
        "media_aspect_ratio": p.media_aspect_ratio,
        "scheduled_at": p.scheduled_at.isoformat() + "Z" if p.scheduled_at else None,
        "campaign_tag": p.campaign_tag,
        "status": p.status.value,
        "approved": p.approved,
        "platform_post_id": p.platform_post_id,
        "post_url": p.post_url,
        "error_message": p.error_message,
        "retry_count": p.retry_count,
        "posted_at": p.posted_at.isoformat() + "Z" if p.posted_at else None,
    }


def _error_page(message: str) -> tuple[str, int]:
    return render_template("oauth_error.html", message=message), 400


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
