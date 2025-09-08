import os

from dotenv import load_dotenv
from flask import Flask


def create_app() -> Flask:
    # Load .env for local/dev; does not override existing env
    load_dotenv(override=False)
    app = Flask(__name__)

    # Basic config
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")

    # Register routes
    from .routes import bp as routes_bp

    app.register_blueprint(routes_bp)

    @app.get("/health")
    def healthcheck():
        """Liveness/readiness check. Tries DB if configured."""
        db_url = app.config.get("DATABASE_URL")
        if not db_url:
            return {"status": "ok", "db": "not_configured"}

        # Try a lightweight DB connection check.
        try:
            import psycopg2

            with psycopg2.connect(db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1;")
                    cur.fetchone()
            return {"status": "ok", "db": "connected"}
        except Exception as exc:  # pragma: no cover - best-effort
            return {"status": "degraded", "db": f"error: {exc}"}, 503

    return app
