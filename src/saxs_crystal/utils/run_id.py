from __future__ import annotations

from datetime import datetime


def build_run_id(prefix: str = "run") -> str:
    return f"{prefix}-{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
