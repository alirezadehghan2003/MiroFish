"""
本地部署安全辅助函数

Standard-library only so the checks can be unit-tested without Flask.
"""

import os
import re
from typing import Any, Iterable, Mapping, Optional

# Generated IDs look like proj_xxxxxxxxxxxx / sim_xxxxxxxxxxxx / report_xxxxxxxxxxxx.
SAFE_ID_PATTERN = re.compile(r"[A-Za-z0-9_-]{1,128}")

# Request fields whose values are joined into filesystem paths.
PATH_ID_FIELDS = ("project_id", "simulation_id", "report_id")

LOOPBACK_HOSTS = ("localhost", "127.0.0.1", "::1")


def is_safe_id(value: Any) -> bool:
    """Return True when value can be used as a single path component."""
    return isinstance(value, str) and bool(SAFE_ID_PATTERN.fullmatch(value))


def find_unsafe_id(values: Optional[Mapping[str, Any]]) -> Optional[str]:
    """Return the first path-ID field in values that is present but unsafe."""
    if not isinstance(values, Mapping):
        return None
    for field in PATH_ID_FIELDS:
        value = values.get(field)
        if value is not None and not is_safe_id(value):
            return field
    return None


def safe_id_path(base_dir: str, item_id: str, *parts: str) -> str:
    """Join an ID under base_dir, rejecting IDs that could escape it."""
    if not is_safe_id(item_id):
        raise ValueError(f"Invalid ID: {item_id!r}")
    return os.path.join(base_dir, item_id, *parts)


def host_without_port(host_header: str) -> str:
    """Strip the port from a Host header value, keeping IPv6 literals intact."""
    host = (host_header or "").strip().lower()
    if host.startswith("["):
        return host[1:host.find("]")] if "]" in host else host
    if host.count(":") == 1:
        return host.split(":", 1)[0]
    return host


def is_host_allowed(host_header: str, allowed_hosts: Iterable[str]) -> bool:
    """Check a Host header against an allowlist ("*" allows any host)."""
    allowed = [h.strip().lower() for h in allowed_hosts]
    if "*" in allowed:
        return True
    return host_without_port(host_header) in allowed


def is_loopback_host(host: str) -> bool:
    """Return True when a bind address only accepts local connections."""
    return host.strip().lower() in LOOPBACK_HOSTS or host.startswith("127.")
