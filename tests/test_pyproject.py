from __future__ import annotations

import tomllib


def test_project_name_is_hexlet_code() -> None:
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)

    assert data.get("project", {}).get("name") == "hexlet-code"

