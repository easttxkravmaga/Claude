import logging
import os
from datetime import datetime

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
from sqlalchemy import select

from auth_basic import require_basic_auth
from auth import linkedin as li_auth
from auth import meta as meta_auth
from db import SessionLocal, init_db
import jobs
from models import OAuthCredential, Provider, RefreshStatus


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)


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
        return render_template("home.html")

    @app.route("/scheduler")
    @require_basic_auth
    def scheduler():
        return render_template("scheduler.html")

    @app.route("/linkedin")
    @require_basic_auth
    def linkedin_setup():
        return render_template("linkedin.html")

    @app.route("/meta")
    @require_basic_auth
    def meta_setup():
        return render_template("meta.html")

    @app.route("/dashboard")
    @require_basic_auth
    def dashboard():
        return render_template("dashboard.html")

    # ── Scheduler status ─────────────────────────────────────────────────────
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

    return app


def _serialize_credential(cred: OAuthCredential) -> dict:
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
        "created_at": cred.created_at.isoformat() + "Z" if cred.created_at else None,
    }


def _error_page(message: str) -> tuple[str, int]:
    return render_template("oauth_error.html", message=message), 400


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
