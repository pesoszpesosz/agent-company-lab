from __future__ import annotations

import json
import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "state" / "agent_company.sqlite"
DEFAULT_OUT = ROOT / "web" / "data" / "snapshot.json"
DEFAULT_VISUALS = ROOT / "web" / "data" / "lane-visuals.json"
DEFAULT_AGENT_VISUALS = ROOT / "web" / "data" / "agent-visuals.json"
TEXT_PREVIEW_SUFFIXES = {".md", ".txt", ".json", ".csv", ".tsv", ".py", ".js", ".css", ".html", ".yml", ".yaml"}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(value: str | None, fallback: Any) -> Any:
    if not value:
        return fallback
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return fallback


def rows(conn: sqlite3.Connection, query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    cur = conn.execute(query, params)
    return [dict(row) for row in cur.fetchall()]

def one_value(conn: sqlite3.Connection, query: str, params: tuple[Any, ...] = ()) -> Any:
    return conn.execute(query, params).fetchone()[0]


def clean_label(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").title()


def compact_path(path: str | None) -> str | None:
    if not path:
        return None
    text = path.replace(str(ROOT), ".")
    return text.replace("\\", "/")


def resolve_local_artifact(path: str | None) -> Path | None:
    if not path:
        return None
    text = path.strip()
    if not text or "://" in text:
        return None
    candidate = Path(text)
    if not candidate.is_absolute():
        candidate = ROOT / text.lstrip("./\\")
    try:
        resolved = candidate.resolve()
        resolved.relative_to(ROOT.resolve())
    except (OSError, ValueError):
        return None
    if not resolved.is_file() or resolved.suffix.lower() not in TEXT_PREVIEW_SUFFIXES:
        return None
    return resolved


def clean_preview_line(line: str) -> str:
    text = " ".join(line.strip().split())
    if not text:
        return ""
    if set(text) <= {"-", "|", ":", " "}:
        return ""
    if text.startswith("|") and text.endswith("|"):
        cells = [cell.strip() for cell in text.strip("|").split("|") if cell.strip()]
        text = " | ".join(cells)
    return text.strip("#>*- ")


def artifact_preview(path: str | None, max_lines: int = 4, max_chars: int = 420) -> dict[str, Any] | None:
    artifact_path = resolve_local_artifact(path)
    if not artifact_path:
        return None
    try:
        raw = artifact_path.read_text(encoding="utf-8", errors="replace")[:12000]
    except OSError:
        return None
    lines: list[str] = []
    char_count = 0
    for raw_line in raw.splitlines():
        line = clean_preview_line(raw_line)
        if not line:
            continue
        remaining = max_chars - char_count
        if remaining <= 0:
            break
        line = line[:remaining].strip()
        if not line:
            continue
        lines.append(line)
        char_count += len(line)
        if len(lines) >= max_lines:
            break
    if not lines:
        return None
    return {
        "label": artifact_path.name,
        "kind": artifact_path.suffix.lower().lstrip(".") or "file",
        "lines": lines,
        "truncated": len(raw) >= 12000 or sum(len(line) for line in lines) >= max_chars,
    }


def safe_int(value: Any) -> int:
    return int(value or 0)


def compute_level(score: int) -> int:
    return max(1, min(12, 1 + int(math.sqrt(max(score, 0)) // 4)))


def compute_progress(score: int, level: int) -> int:
    floor = ((level - 1) * 4) ** 2
    ceiling = (level * 4) ** 2
    if ceiling <= floor:
        return 100
    return max(4, min(100, round(((score - floor) / (ceiling - floor)) * 100)))


def table_count(conn: sqlite3.Connection, table: str) -> int:
    return safe_int(one_value(conn, f"select count(*) from {table}"))


def default_visual(lane_id: str, index: int) -> dict[str, Any]:
    color_pairs = [
        ("#44d7c9", "#f4ba55"),
        ("#ff6f61", "#44d7c9"),
        ("#8be06e", "#f4ba55"),
        ("#9a89ff", "#ff6f61"),
        ("#f4ba55", "#8be06e"),
        ("#c4d4cf", "#44d7c9"),
    ]
    accent, accent_alt = color_pairs[index % len(color_pairs)]
    return {
        "avatar": None,
        "realm": clean_label(lane_id),
        "mood": "A configurable lane world waiting for a custom visual identity.",
        "accent": accent,
        "accentAlt": accent_alt,
        "minigame": {
            "id": f"{lane_id}-module",
            "title": "Lane Module",
            "mechanic": "Attach a lane-specific challenge loop here.",
            "status": "empty_slot",
        },
    }
