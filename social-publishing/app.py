import logging
import os

from flask import Flask, jsonify, render_template

from auth_basic import require_basic_auth
from db import init_db
import jobs


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["JSON_SORT_KEYS"] = False

    init_db()

    if os.environ.get("DISABLE_SCHEDULER") != "1":
        jobs.start()

    # ── Health (unauthenticated for Cloud Run probes) ────────────────────────
    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "service": "etkm-social-publishing"})

    # ── Pages (placeholders — Phase E fills in) ──────────────────────────────
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

    # ── Scheduler status (drives the orange "Scheduler busy" pill) ───────────
    @app.route("/api/scheduler/status")
    @require_basic_auth
    def scheduler_status():
        return jsonify(jobs.status())

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
