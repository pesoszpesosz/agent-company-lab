from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .utils import compact_text
def read_text_sample(path: Path, max_chars: int = 60000) -> str:
    with path.open("r", encoding="utf-8-sig", errors="replace") as f:
        return f.read(max_chars)


def infer_status(text: str) -> str:
    lower = text.lower()
    if "accepted=true" in lower or '"accepted": true' in lower:
        return "accepted"
    if "submission-ready" in lower or "submission ready" in lower:
        return "submission_ready"
    if "promoted" in lower:
        return "promoted"
    if "watch_only" in lower or "watch-only" in lower or "watch only" in lower:
        return "watch_only"
    if "state=triage" in lower or "in triage" in lower:
        return "triage"
    if "none passed" in lower or "no actionable" in lower or "no clean candidate" in lower:
        return "no_actionable_rows"
    if "reject" in lower:
        return "rejected"
    if "park" in lower or "gated" in lower:
        return "parked_or_gated"
    return "imported"


def markdown_title(path: Path, text: str, title_override: str | None) -> str:
    if title_override:
        return title_override
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or path.stem
    return path.stem.replace("-", " ").title()


def extract_next_action_from_lines(lines: list[str]) -> str | None:
    for line in lines:
        stripped = line.strip().lstrip("-").strip()
        lower = stripped.lower()
        if lower.startswith("next:") or lower.startswith("next action:") or "next action is" in lower:
            return compact_text(stripped, 500)
    return None


def summarize_markdown(path: Path, title_override: str | None) -> dict[str, str | None]:
    text = read_text_sample(path)
    lines = text.splitlines()
    title = markdown_title(path, text, title_override)
    priority_markers = [
        "cashflow:",
        "security report",
        "security advisory",
        "market",
        "prediction",
        "cross-venue",
        "bounty",
        "microbounty",
        "submitted",
        "none passed",
        "watch_only",
        "watch-only",
        "promoted",
        "gate",
    ]
    summary_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.lower().startswith("generated utc"):
            continue
        lower = stripped.lower()
        if any(marker in lower for marker in priority_markers):
            summary_lines.append(compact_text(stripped, 240) or "")
        if len(summary_lines) >= 5:
            break
    if not summary_lines:
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                summary_lines.append(compact_text(stripped, 240) or "")
            if len(summary_lines) >= 3:
                break
    return {
        "title": title,
        "status": infer_status(text),
        "summary": compact_text(" | ".join(summary_lines), 900),
        "next_action": extract_next_action_from_lines(lines),
    }


def find_first_key(obj: Any, keys: set[str]) -> Any:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in keys and value not in (None, ""):
                return value
        for value in obj.values():
            found = find_first_key(value, keys)
            if found not in (None, ""):
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = find_first_key(value, keys)
            if found not in (None, ""):
                return found
    return None


def find_first_url(obj: Any) -> str | None:
    if isinstance(obj, str):
        for token in obj.replace('"', " ").replace("'", " ").split():
            if token.startswith("https://") or token.startswith("http://"):
                return token.rstrip(").,;]")
    if isinstance(obj, dict):
        for value in obj.values():
            found = find_first_url(value)
            if found:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = find_first_url(value)
            if found:
                return found
    return None


def summarize_json(path: Path, title_override: str | None) -> dict[str, str | None]:
    text = read_text_sample(path)
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {
            "title": title_override or path.stem.replace("-", " ").title(),
            "status": "json_parse_error",
            "summary": compact_text(text, 900),
            "next_action": None,
        }
    title = title_override or compact_text(find_first_key(parsed, {"title", "name", "event", "event_id"}) or path.stem, 160)
    next_action = find_first_key(parsed, {"nextAction", "next_action", "next"})
    status_value = find_first_key(parsed, {"status", "decision", "gate", "state"})
    if isinstance(parsed, list):
        summary = f"{len(parsed)} JSON row(s)."
    elif isinstance(parsed, dict):
        keys = ", ".join(list(parsed.keys())[:12])
        summary = f"JSON object keys: {keys}."
    else:
        summary = f"JSON scalar: {parsed!r}."
    if status_value:
        summary = f"{summary} First status-like value: {compact_text(str(status_value), 180)}."
    return {
        "title": str(title),
        "status": compact_text(str(status_value), 80) if status_value else infer_status(text),
        "summary": compact_text(summary, 900),
        "next_action": compact_text(str(next_action), 500) if next_action else None,
    }


def summarize_jsonl(path: Path, title_override: str | None) -> dict[str, str | None]:
    lines = [line for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines() if line.strip()]
    parsed_rows: list[dict[str, Any]] = []
    for line in lines[-5:]:
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            parsed_rows.append(parsed)
    recent_titles = []
    for row in parsed_rows[-3:]:
        recent_titles.append(compact_text(str(row.get("event") or row.get("event_id") or row.get("opportunity") or "row"), 140) or "row")
    next_action = None
    for row in reversed(parsed_rows):
        next_action = compact_text(str(row.get("nextAction") or row.get("next_action") or ""), 500)
        if next_action:
            break
    return {
        "title": title_override or path.stem.replace("-", " ").title(),
        "status": "imported_jsonl",
        "summary": compact_text(f"{len(lines)} JSONL row(s). Recent rows: {' | '.join(recent_titles)}", 900),
        "next_action": next_action,
    }


def summarize_source_file(path: Path, title_override: str | None) -> dict[str, str | None]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return summarize_json(path, title_override)
    if suffix == ".jsonl":
        return summarize_jsonl(path, title_override)
    return summarize_markdown(path, title_override)
