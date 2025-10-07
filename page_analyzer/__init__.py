import importlib
from typing import Any, TYPE_CHECKING

try:
    import colorama
except ImportError:  # pragma: no cover - optional dependency
    colorama = None
else:
    ansi_to_win32 = getattr(colorama, "AnsiToWin32", None)
    if ansi_to_win32 is not None and not hasattr(ansi_to_win32, "write"):

        def _write(self, text):
            target = getattr(self, "stream", None) or getattr(self,
                                                              "wrapped", None)
            if target is None:
                return None
            return target.write(text)

        ansi_to_win32.write = _write  # type: ignore[attr-defined]

    if ansi_to_win32 is not None and not hasattr(ansi_to_win32, "flush"):

        def _flush(self):
            target = getattr(self, "stream", None) or getattr(self,
                                                              "wrapped", None)
            flush = getattr(target, "flush", None)
            if callable(flush):
                flush()

        ansi_to_win32.flush = _flush  # type: ignore[attr-defined]

if TYPE_CHECKING:
    from .app import app as _app

    app = _app

__all__ = ["app"]


def __getattr__(name: str) -> Any:
    if name == "app":
        module = importlib.import_module(".app", __name__)
        return module.app
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
