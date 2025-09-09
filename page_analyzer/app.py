from __future__ import annotations

import os

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.data_base import UrlRepository
from page_analyzer.parser import get_data
from page_analyzer.url_validator import normalize_url, validate_url

load_dotenv(override=False)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
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

    normalized_url = normalize_url(url)
    repo = UrlRepository(DATABASE_URL)
    existing = repo.find_url(normalized_url)
    if existing is not None:
        flash("Страница уже существует", "warning")
        return redirect(url_for("get_url", id=existing.get("id")))

    new_id = repo.add_url(normalized_url)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("get_url", id=new_id))


@app.get("/urls/<int:id>")
def get_url(id: int):  # noqa: A002 - route param name
    repo = UrlRepository(DATABASE_URL)
    url_info = repo.find_id(id)
    if not url_info:
        abort(404)

    url_checks = repo.get_url_checks(id)
    return render_template("url.html", url_info=url_info, url_checks=url_checks)


@app.post("/urls/<int:id>/checks")
def run_check(id: int):  # noqa: A002 - route param name
    repo = UrlRepository(DATABASE_URL)
    url_info = repo.find_id(id)
    if not url_info:
        abort(404)

    try:
        resp = requests.get(url_info.get("name"), timeout=0.3)
        resp.raise_for_status()
    except requests.RequestException:
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for("get_url", id=id))

    payload = get_data(resp)
    payload["status"] = resp.status_code
    repo.add_url_check(payload, url_info)
    flash("Страница успешно проверена", "success")
    return redirect(url_for("get_url", id=id))


@app.get("/urls")
def list_urls():
    repo = UrlRepository(DATABASE_URL)
    all_urls_checks = repo.get_all_urls_checks()
    return render_template("urls.html", all_urls_checks=all_urls_checks)


@app.errorhandler(404)
def page_not_found(error):  # noqa: ARG001 - Flask signature
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):  # noqa: ARG001 - Flask signature
    return render_template("errors/500.html"), 500
