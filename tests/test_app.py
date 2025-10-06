from __future__ import annotations

import importlib
import sys

import pytest
from flask import Flask


def _reload_package() -> Flask:
    """Reload page_analyzer package and return exported app."""
    for name in ("page_analyzer.app", "page_analyzer"):
        if name in sys.modules:
            del sys.modules[name]
    importlib.invalidate_caches()
    import page_analyzer  # type: ignore

    return page_analyzer.app  # type: ignore[attr-defined]


def test_app_is_exported() -> None:
    from page_analyzer import app  # type: ignore

    assert isinstance(app, Flask)


def test_root_route_returns_html() -> None:
    from page_analyzer import app  # type: ignore

    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    # Step 2: root renders HTML template, not JSON
    assert not resp.is_json
    assert "text/html" in resp.headers.get("Content-Type", "")
    body = resp.get_data(as_text=True)
    assert "Анализатор страниц" in body


def test_secret_key_loaded_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SECRET_KEY", "super-secret-key")
    app = _reload_package()
    assert app.config.get("SECRET_KEY") == "super-secret-key"


@pytest.mark.parametrize(
    "first, duplicate",
    [
        pytest.param(
            "https://example.com",
            "https://Example.com",
            id="host-case-insensitive",
        ),
    ],
)
def test_urls_index_warns_about_duplicate_host_case(
    monkeypatch: pytest.MonkeyPatch, first: str, duplicate: str
) -> None:
    monkeypatch.setenv("SECRET_KEY", "integration-secret")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost/testdb")

    app = _reload_package()

    class RepoStub:  # noqa: D401 - simple stub for tests
        """In-memory хранилище URL-ов для имитации репозитория."""

        storage: dict[int, dict[str, object]] = {}
        by_name: dict[str, dict[str, object]] = {}
        next_id: int = 1

        def __init__(self, *_: object) -> None:
            pass

        @classmethod
        def reset(cls) -> None:
            cls.storage = {}
            cls.by_name = {}
            cls.next_id = 1

        def find_url(self, url: str) -> dict[str, object] | None:
            return type(self).by_name.get(url)

        def add_url(self, url: str) -> int:
            cls = type(self)
            if url in cls.by_name:
                raise AssertionError("URL already stored")
            record = {"id": cls.next_id, "name": url, "created_at": None}
            cls.storage[cls.next_id] = record
            cls.by_name[url] = record
            cls.next_id += 1
            return record["id"]

        def find_id(self, url_id: int) -> dict[str, object] | None:
            return type(self).storage.get(url_id)

        def get_url_checks(self, url_id: int) -> list[dict[str, object]]:  # noqa: ARG002
            return []

    RepoStub.reset()
    monkeypatch.setattr("page_analyzer.app.UrlRepository", RepoStub)

    with app.test_client() as client:
        response = client.post(
            "/urls",
            data={"url": first},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert "Страница успешно добавлена" in response.get_data(as_text=True)

        response_dup = client.post(
            "/urls",
            data={"url": duplicate},
            follow_redirects=True,
        )
        assert response_dup.status_code == 200
        assert "Страница уже существует" in response_dup.get_data(as_text=True)
