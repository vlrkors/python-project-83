from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "page_analyzer" / "url_validator.py"

_validators_stub = ModuleType("validators")
_validators_stub.url = lambda url: True
sys.modules.setdefault("validators", _validators_stub)


def _load_module(module_path: Path):
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError(f"Cannot load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_path.stem] = module
    spec.loader.exec_module(module)
    return module


normalize_url = _load_module(MODULE_PATH).normalize_url


@pytest.mark.parametrize(
    "url, expected",
    [
        pytest.param(
            "http://example.com/path?query=1",
            "http://example.com",
            id="http-standard",
        ),
        pytest.param(
            "https://sub.example.org/resource",
            "https://sub.example.org",
            id="https-subdomain",
        ),
        pytest.param(
            "http://example.com:8080/abc",
            "http://example.com:8080",
            id="port-preserved",
        ),
        pytest.param(
            "https://user:pass@example.net:8443/index",
            "https://user:pass@example.net:8443",
            id="credentials-and-port",
        ),
        pytest.param(
            "http://[2001:db8::1]:9090/path",
            "http://[2001:db8::1]:9090",
            id="ipv6-address",
        ),
    ],
)
def test_normalize_url_expected_values(url: str, expected: str) -> None:
    assert normalize_url(url) == expected


@pytest.mark.parametrize(
    "first, second",
    [
        pytest.param(
            "http://example.com:8080/path",
            "http://example.com:9090/path",
            id="different-ports",
        ),
    ],
)
def test_normalize_url_distinguishes_ports(first: str, second: str) -> None:
    assert normalize_url(first) != normalize_url(second)

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
def test_normalize_url_is_case_insensitive_for_host(first: str, second: str) -> None:
    assert normalize_url(first) == normalize_url(second)