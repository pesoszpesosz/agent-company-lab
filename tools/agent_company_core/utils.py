"""General-purpose helpers shared by Agent Company modules."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .io import load_json


def decode_json_list(value: str | None) -> list[Any]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        return []


def safe_id_fragment(value: str, limit: int = 64) -> str:
    cleaned = []
    for char in value.lower():
        if char.isalnum():
            cleaned.append(char)
        elif char in {"-", "_", "."}:
            cleaned.append(char)
        else:
            cleaned.append("-")
    fragment = "".join(cleaned).strip("-")
    while "--" in fragment:
        fragment = fragment.replace("--", "-")
    return (fragment or "item")[:limit].strip("-")


def compact_text(value: str | None, limit: int = 700) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(str(value).replace("\r", "\n").split())
    return cleaned[:limit].rstrip()


def md_cell(value: str | None, limit: int = 220) -> str:
    return (compact_text(value, limit) or "").replace("|", "\\|")


def parse_json_arg(json_value: str | None, json_file: str | None, default: Any) -> str:
    if json_file:
        parsed = load_json(Path(json_file))
    elif json_value:
        try:
            parsed = json.loads(json_value)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON argument: {exc}") from exc
    else:
        parsed = default
    return json.dumps(parsed, sort_keys=True)


def parse_metadata_arg(metadata_json: str | None, metadata_file: str | None) -> str:
    if metadata_file:
        parsed = load_json(Path(metadata_file))
    elif metadata_json:
        try:
            parsed = json.loads(metadata_json)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid --metadata-json: {exc}") from exc
    else:
        parsed = {}
    return json.dumps(parsed, sort_keys=True)


def read_text_arg(text_value: str | None, text_file: str | None, label: str) -> str:
    if text_file:
        return Path(text_file).read_text(encoding="utf-8")
    if text_value:
        return text_value
    raise SystemExit(f"{label} requires text or file input")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

