from collections import deque
from datetime import datetime, timezone
from threading import Condition
from typing import Any
from uuid import uuid4


_MAX_LOGS = 500
_logs: deque[dict[str, Any]] = deque(maxlen=_MAX_LOGS)
_condition = Condition()


def add_log(
    message: str,
    level: str = "INFO",
    source: str = "api",
    operation_id: str | None = None,
) -> dict[str, Any]:
    normalized_level = level.upper()
    if normalized_level not in {"INFO", "WARNING", "ERROR", "SUCCESS"}:
        normalized_level = "INFO"

    entry = {
        "id": str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": normalized_level,
        "source": source,
        "message": message,
        "operation_id": operation_id,
    }

    with _condition:
        _logs.append(entry)
        _condition.notify_all()

    return entry


def get_logs(limit: int = 100) -> list[dict[str, Any]]:
    limit = max(1, min(limit, _MAX_LOGS))
    with _condition:
        return list(_logs)[-limit:][::-1]


def wait_for_logs(timeout: float = 15.0) -> None:
    with _condition:
        _condition.wait(timeout=timeout)


def latest_log_id() -> str | None:
    with _condition:
        return _logs[-1]["id"] if _logs else None
