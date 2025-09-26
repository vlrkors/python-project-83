from __future__ import annotations

from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    """Context manager for PostgreSQL connections."""

    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self.conn: psycopg2.extensions.connection | None = None

    def __enter__(self) -> psycopg2.extensions.cursor[dict[str, Any]]:
        self.conn = psycopg2.connect(
            self.database_url,
            cursor_factory=RealDictCursor,
        )
        return self.conn.cursor()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> bool:
        if self.conn is None:
            return False
        try:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
        finally:
            self.conn.close()
        return False


class UrlRepository:
    """Repository encapsulating access to URL related tables."""

    def __init__(self, database_url: str) -> None:
        self.cursor = DatabaseConnection(database_url)

    def add_url(self, url: str) -> int:
        query = """
            INSERT INTO urls (name)
            VALUES (%s)
            RETURNING id
        """
        with self.cursor as cur:
            cur.execute(query, (url,))
            return cur.fetchone()["id"]

    def find_url(self, url: str) -> dict[str, Any] | None:
        query = """
            SELECT id, name
            FROM urls
            WHERE name = %s
        """
        with self.cursor as cur:
            cur.execute(query, (url,))
            row = cur.fetchone()
            return row if row else None

    def find_id(self, url_id: int) -> dict[str, Any] | None:
        query = """
            SELECT *
            FROM urls
            WHERE id = %s
        """
        with self.cursor as cur:
            cur.execute(query, (url_id,))
            row = cur.fetchone()
            return row if row else None

    def get_all_urls(self) -> list[dict[str, Any]]:
        query = """
            SELECT *
            FROM urls
            ORDER BY id DESC
        """
        with self.cursor as cur:
            cur.execute(query)
            return cur.fetchall()

    def add_url_check(self, data: dict[str, Any], url_info: dict[str, Any]) -> None:
        query = """
            INSERT INTO url_checks (url_id,
            status_code, h1, title, description)
            VALUES (%s, %s, %s, %s, %s)
        """

        def _norm(val: object | None, allow_null: bool = True) -> str | None:
            if val is None:
                return None if allow_null else ""
            s = str(val)
            return s[:255]

        with self.cursor as cur:
            cur.execute(
                query,
                (
                    url_info.get("id"),
                    data.get("status"),
                    _norm(data.get("h1")),
                    _norm(data.get("title"), allow_null=False),
                    _norm(data.get("description")),
                ),
            )

    def get_url_checks(self, url_id: int) -> list[dict[str, Any]]:
        query = """
            SELECT *
            FROM url_checks
            WHERE url_id = %s
            ORDER BY id DESC
        """
        with self.cursor as cur:
            cur.execute(query, (url_id,))
            rows: list[dict[str, Any]] = cur.fetchall()
            for row in rows:
                if row["status_code"] is None:
                    row["status_code"] = ""
                if row["h1"] is None:
                    row["h1"] = ""
                if row["title"] is None:
                    row["title"] = ""
                if row["description"] is None:
                    row["description"] = ""
            return rows

    def get_all_urls_checks(self) -> list[dict[str, Any]]:
        query = """
            SELECT DISTINCT ON (urls.id)
                urls.id AS id,
                urls.name AS name,
                url_checks.created_at  AS created_at,
                url_checks.status_code AS status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            ORDER BY id, created_at DESC;
        """
        with self.cursor as cur:
            cur.execute(query)
            rows: list[dict[str, Any]] = cur.fetchall()
            for row in rows:
                if row["created_at"] is None:
                    row["created_at"] = ""
                if row["status_code"] is None:
                    row["status_code"] = ""
            return rows
