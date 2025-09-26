from __future__ import annotations

import importlib.util
import pathlib
import sys
from types import ModuleType

import pytest


def _load_url_validator() -> ModuleType:
    module_name = "page_analyzer.url_validator"
    if module_name in sys.modules:
        return sys.modules[module_name]

    module_path = pathlib.Path(__file__).resolve().parents[1] / "page_analyzer" / "url_validator.py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError(f"Cannot load module {module_name}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


url_validator = _load_url_validator()


@pytest.mark.parametrize(
    ("input_url", "expected"),
    [
        pytest.param(
            "https://example.com/path",
            "https://example.com",
            id="basic-https",
        ),
        pytest.param(
            "http://EXAMPLE.com",
            "http://example.com",
            id="uppercase-host",
        ),
        pytest.param(
            "https://example.com:8443/path",
            "https://example.com:8443",
            id="with-port",
        ),
        pytest.param(
            "http://example.com:80",
            "http://example.com:80",
            id="explicit-default-port",
        ),
        pytest.param(
            "https://sub.domain.com",
            "https://sub.domain.com",
            id="subdomain",
        ),
    ],
)
def test_normalize_url(input_url: str, expected: str) -> None:
    assert url_validator.normalize_url(input_url) == expected


@pytest.mark.parametrize(
    ("input_url", "validator_returns", "expected", "expected_calls"),
    [
        pytest.param(
            "",
            True,
            {"url": "URL не может быть пустым"},
            0,
            id="empty-string",
        ),
        pytest.param(
            "a" * 256,
            True,
            {"url": "Превышена максимальная длина URL (до 255 символов)"},
            0,
            id="too-long",
        ),
        pytest.param(
            "invalid",
            False,
            {"url": "Некорректный URL"},
            1,
            id="invalid-format",
        ),
        pytest.param(
            "https://example.com",
            True,
            {},
            1,
            id="valid-https",
        ),
        pytest.param(
            "   ",
            False,
            {"url": "Некорректный URL"},
            1,
            id="whitespace",
        ),
    ],
)
def test_validate_url(
    input_url: str,
    validator_returns: bool,
    expected: dict[str, str],
    expected_calls: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = {"count": 0}

    def fake_validator(value: str) -> bool:  # pragma: no cover - simple stub
        calls["count"] += 1
        return validator_returns

    monkeypatch.setattr(url_validator.validators, "url", fake_validator)

    result = url_validator.validate_url(input_url)

    assert result == expected
    assert calls["count"] == expected_calls
