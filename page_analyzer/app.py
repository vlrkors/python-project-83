from __future__ import annotations

import os

import psycopg2
import requests
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for

from page_analyzer.data_base import UrlRepository
from page_analyzer.parser import get_data
from page_analyzer.url_validator import normalize_url, validate_url

load_dotenv()

app = Flask(__name__)


def _load_secret_key_from_file(path: str = ".env") -> str | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                # Допускаем SECRET_KEY=val, SECRET_KEY="val", 'SECRET_KEY' = 'val'
                for key_token in ("SECRET_KEY", "'SECRET_KEY'", '"SECRET_KEY"'):
                    if line.startswith(key_token):
                        _, _, rhs = line.partition("=")
                        val = rhs.strip().strip("'\"")
                        return val
    except FileNotFoundError:
        return None
    except Exception:
        return None
    return None


_secret = os.getenv("SECRET_KEY") or _load_secret_key_from_file() or "dev-secret-key"
app.config["SECRET_KEY"] = _secret
DATABASE_URL = os.getenv("DATABASE_URL")


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/urls")
def urls_index():
    form = request.form.to_dict()
    url = form.get("url", "")

    errors = validate_url(url)
    if errors:
        flash("Некорректный URL", "danger")
        return render_template("index.html"), 422

    if not DATABASE_URL:
        flash("Не настроено подключение к базе", "danger")
        return redirect(url_for("index"))

    normalized_url = normalize_url(url)
    repo = UrlRepository(DATABASE_URL)
    try:
        existing = repo.find_url(normalized_url)
    except Exception:  # noqa: BLE001
        flash("Ошибка при обращении к базе", "danger")
        return redirect(url_for("index"))
    if existing is not None:
        flash("Страница уже существует", "warning")
        return redirect(url_for("get_url", id=existing.get("id")))

    try:
        new_id = repo.add_url(normalized_url)
    except Exception:  # noqa: BLE001
        flash("Ошибка при обращении к базе", "danger")
        return redirect(url_for("index"))
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("get_url", id=new_id))


@app.get("/urls/<int:id>")
def get_url(id: int):  # noqa: A002 - route param name
    if not DATABASE_URL:
        flash("Не настроено подключение к базе", "danger")
        return redirect(url_for("index"))

    repo = UrlRepository(DATABASE_URL)
    try:
        url_info = repo.find_id(id)
    except Exception:  # noqa: BLE001
        flash("Ошибка при обращении к базе", "danger")
        return redirect(url_for("index"))
    if not url_info:
        abort(404)

    url_checks = repo.get_url_checks(id)
    return render_template("url.html", url_info=url_info, url_checks=url_checks)


@app.post("/urls/<int:id>/checks")
def run_check(id: int):  # noqa: A002 - route param name
    if not DATABASE_URL:
        flash("Не настроено подключение к базе", "danger")
        return redirect(url_for("index"))

    repo = UrlRepository(DATABASE_URL)
    try:
        url_info = repo.find_id(id)
    except Exception:  # noqa: BLE001
        flash("Ошибка при обращении к базе", "danger")
        return redirect(url_for("index"))
    if not url_info:
        abort(404)

    url = url_info.get("name")
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException:
        flash("Ошибка при запросе страницы", "danger")
        return redirect(url_for("get_url", id=id))

    response.encoding = response.apparent_encoding or "utf-8"
    parsed = get_data(response)
    payload = {
        "status": response.status_code,
        "h1": parsed.get("h1"),
        "title": parsed.get("title"),
        "description": parsed.get("description"),
    }
    try:
        repo.add_url_check(payload, url_info)
    except Exception:  # noqa: BLE001
        flash("Ошибка при обращении к базе", "danger")
        return redirect(url_for("index"))
    flash("Страница успешно проверена", "success")
    return redirect(url_for("get_url", id=id))


@app.get("/urls")
def list_urls():
    if not DATABASE_URL:
        flash("Не настроено подключение к базе", "danger")
        return redirect(url_for("index"))

    repo = UrlRepository(DATABASE_URL)
    try:
        all_urls_checks = repo.get_all_urls_checks()
    except Exception:  # noqa: BLE001
        flash("Ошибка при обращении к базе", "danger")
        return redirect(url_for("index"))
    return render_template("urls.html", all_urls_checks=all_urls_checks)


@app.errorhandler(404)
def page_not_found(error):  # noqa: ARG001 - Flask signature
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):  # noqa: ARG001 - Flask signature
    return render_template("errors/500.html"), 500


@app.get("/health")
def health():
    if not DATABASE_URL:
        return {"status": "error", "message": "DATABASE_URL is not set"}, 503
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return {"status": "ok"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "message": str(exc)}, 503
