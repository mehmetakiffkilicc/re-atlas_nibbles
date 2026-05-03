"""SQLite-backed API response cache with TTL."""
import json
import sqlite3
import time
from pathlib import Path

from app.config import CACHE_DIR

DB_PATH = CACHE_DIR / "api_cache.sqlite"
CREATE_SQL = """
CREATE TABLE IF NOT EXISTS api_cache (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    expires_at REAL NOT NULL
)
"""

_conn: sqlite3.Connection | None = None


def _get_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.execute(CREATE_SQL)
        _conn.commit()
    return _conn


def get_cached(key: str) -> dict | None:
    conn = _get_conn()
    row = conn.execute(
        "SELECT value, expires_at FROM api_cache WHERE key=?", (key,)
    ).fetchone()
    if row is None:
        return None
    value_json, expires_at = row
    if time.time() > expires_at:
        conn.execute("DELETE FROM api_cache WHERE key=?", (key,))
        conn.commit()
        return None
    return json.loads(value_json)


def set_cached(key: str, value: dict, ttl_seconds: int = 3600) -> None:
    conn = _get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO api_cache (key, value, expires_at) VALUES (?,?,?)",
        (key, json.dumps(value, ensure_ascii=False), time.time() + ttl_seconds)
    )
    conn.commit()
