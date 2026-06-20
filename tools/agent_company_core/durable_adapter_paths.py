"""Durable-adapter filesystem path guards."""

from __future__ import annotations

from pathlib import Path

from .constants import DURABLE_ORCHESTRATION_DIR


def resolve_durable_adapter_result_path(path_value: str | None) -> Path | None:
    if not path_value:
        return None
    base_dir = DURABLE_ORCHESTRATION_DIR.resolve()
    result_path = Path(path_value).resolve()
    if result_path != base_dir and base_dir not in result_path.parents:
        raise SystemExit(
            "Result path must stay inside "
            f"{DURABLE_ORCHESTRATION_DIR}; got {Path(path_value)}"
        )
    return result_path

__all__ = ["resolve_durable_adapter_result_path"]
