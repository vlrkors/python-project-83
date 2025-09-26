from __future__ import annotations

import os
from typing import Iterator

import psycopg2
import pytest

from page_analyzer.data_base import UrlRepository


def _connect(url: str):
    return psycopg2.connect(url)


def _exec_sql_file(db_url: str, path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        sql_text = f.read()
    # Naive split by ';' is ok for our simple schema file
    stmts = [s.strip() for s in sql_text.split(";") if s.strip()]
    with _connect(db_url) as conn:
        with conn.cursor() as cur:
            for stmt in stmts:
                cur.execute(stmt)


@pytest.fixture(scope="session")
def test_db_url() -> str:
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL is not set; skipping DB tests")
    # Check connectivity early
    try:
        with _connect(url):
            pass
    except Exception as exc:  # noqa: BLE001 - test-only
        pytest.skip(f"Cannot connect to TEST_DATABASE_URL: {exc}")
    return url


@pytest.fixture(autouse=True)
def setup_schema(test_db_url: str) -> Iterator[None]:
    _exec_sql_file(test_db_url, "database.sql")
    # Clean tables between tests
    with _connect(test_db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE url_checks RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE urls RESTART IDENTITY CASCADE;")
    yield


def test_add_and_find_url(test_db_url: str) -> None:
    repo = UrlRepository(test_db_url)
    name = "https://example.com"
    new_id = repo.add_url(name)
    assert isinstance(new_id, int)
    found = repo.find_url(name)
    assert found is not None
    assert found["id"] == new_id
    assert found["name"] == name


def test_find_id_returns_row(test_db_url: str) -> None:
    repo = UrlRepository(test_db_url)
    url_id = repo.add_url("https://hexlet.io")
    row = repo.find_id(url_id)
    assert row is not None
    assert row["id"] == url_id
    assert row["name"] == "https://hexlet.io"
    # created_at default is set by DB
    assert row["created_at"] is not None


def test_add_check_and_get_checks(test_db_url: str) -> None:
    repo = UrlRepository(test_db_url)
    url_id = repo.add_url("https://site.test")
    url_info = repo.find_id(url_id)
    payload = {
        "status": 200,
        "h1": "Welcome",
        "title": None,  # Will be normalized to ''
        "description": "Short desc",
    }
    repo.add_url_check(payload, url_info)
    checks = repo.get_url_checks(url_id)
    assert len(checks) == 1
    c = checks[0]
    assert c["status_code"] == 200
    assert c["h1"] == "Welcome"
    assert c["title"] == ""
    assert c["description"] == "Short desc"
    assert c["created_at"] is not None


def test_get_all_urls_checks_includes_urls_without_checks(test_db_url: str) -> None:
    repo = UrlRepository(test_db_url)
    a = repo.add_url("https://a.example")
    b = repo.add_url("https://b.example")
    # Add one check only for A
    repo.add_url_check(
        {"status": 404, "h1": None, "title": "Not found", "description": None},
        repo.find_id(a),
    )
    rows = repo.get_all_urls_checks()
    # Expect two rows (A and B)
    ids = [r["id"] for r in rows]
    assert a in ids and b in ids
    # Find B row (without checks)
    row_b = next(r for r in rows if r["id"] == b)
    assert row_b["status_code"] == ""  # normalized for None
    assert row_b["created_at"] == ""


@pytest.mark.parametrize(
    "first, second",
    [
        pytest.param(
            "https://Example.com",
            "https://example.com",
            id="host-case-insensitive",
        ),
    ],
)
def test_repository_reuses_row_for_host_case(first: str, second: str, test_db_url: str) -> None:
    repo = UrlRepository(test_db_url)
    normalized_first = normalize_url(first)
    normalized_second = normalize_url(second)

    assert normalized_first == normalized_second

    first_id = repo.add_url(normalized_first)
    found = repo.find_url(normalized_second)
    assert found is not None
    assert found["id"] == first_id

    with pytest.raises(psycopg2.IntegrityError):
        repo.add_url(normalized_second)
