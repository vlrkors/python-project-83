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


def test_root_route_returns_json() -> None:
    from page_analyzer import app  # type: ignore

    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.is_json
    data = resp.get_json()
    assert isinstance(data, dict)
    assert data.get("message") == "Hello, Hexlet!"


def test_secret_key_loaded_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SECRET_KEY", "super-secret-key")
    app = _reload_package()
    assert app.config.get("SECRET_KEY") == "super-secret-key"
