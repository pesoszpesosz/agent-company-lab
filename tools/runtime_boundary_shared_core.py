from __future__ import annotations

from typing import Any


def collect_runtime_boundary_errors(
    payload: dict[str, Any],
    zero_boundary: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    boundary = payload.get("runtime_boundary", {})
    if not isinstance(boundary, dict):
        errors.append("runtime_boundary_must_be_object")
        boundary = {}
    for key, expected in zero_boundary.items():
        if boundary.get(key) != expected:
            errors.append(f"runtime_boundary_{key}_must_equal_{expected}")
    return errors
