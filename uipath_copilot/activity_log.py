"""Log en memoria para terminal en vivo del panel jurado."""

from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from typing import Any

_MAX = 300
_log: deque[dict[str, Any]] = deque(maxlen=_MAX)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M:%S")


def log_activity(level: str, source: str, message: str, **extra: Any) -> None:
    _log.append(
        {
            "ts": _now(),
            "level": level,
            "source": source,
            "message": message,
            **extra,
        }
    )


def list_activity(limit: int = 80) -> list[dict[str, Any]]:
    items = list(_log)
    return items[-limit:]


def log_connection_check(name: str, ok: bool, detail: str = "") -> None:
    log_activity("ok" if ok else "err", "CONN", f"{name}: {'OK' if ok else 'FAIL'}" + (f" — {detail}" if detail else ""))
