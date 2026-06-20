"""SQLite connection helpers for the Agent Company control plane."""

from __future__ import annotations

import sqlite3

from .paths import DB_PATH


def connect() -> sqlite3.Connection:
    """Open the durable control-plane database with required pragmas."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn

