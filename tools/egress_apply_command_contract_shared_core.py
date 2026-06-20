"""Shared invariant checks for report-only egress apply-command contracts."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any


def _append_false_field_errors(
    errors: list[str],
    payload: dict[str, Any],
    fields: Iterable[str],
    *,
    prefix: str = "",
) -> None:
    for key in fields:
        if payload.get(key) is not False:
            errors.append(f"{prefix}{key}_must_be_false")


def _append_zero_field_errors(
    errors: list[str],
    payload: dict[str, Any],
    fields: Iterable[str],
    *,
    prefix: str = "",
) -> None:
    for key in fields:
        if payload.get(key) != 0:
            errors.append(f"{prefix}{key}_must_be_zero")


def collect_common_contract_errors(
    *,
    schema: dict[str, Any],
    command: dict[str, Any],
    sources: dict[str, Any],
    required_fields: Iterable[str],
    schema_version: str,
    target_route_id: str | None,
    target_egress_type: str | None,
    schema_false_props: Iterable[str],
    schema_route_error: str,
    schema_type_error: str,
    route_error: str,
    type_error: str,
    expected_paths: dict[str, str],
    path_inside_root: Callable[[str], bool],
    source_false_fields: Iterable[str],
    source_zero_fields: Iterable[str],
    command_false_fields: Iterable[str],
    command_zero_fields: Iterable[str],
    zero_boundary: dict[str, Any],
    check_command_shape: bool = True,
) -> list[str]:
    errors: list[str] = []
    properties = schema.get("properties", {})
    if properties.get("command_type", {}).get("enum", [None])[0] != "deny_noop":
        errors.append("schema_command_type_enum_must_start_deny_noop")
    if target_route_id is not None and properties.get("target_route_id", {}).get("const") != target_route_id:
        errors.append(schema_route_error)
    if target_egress_type is not None and properties.get("target_egress_type", {}).get("const") != target_egress_type:
        errors.append(schema_type_error)
    for prop in schema_false_props:
        if properties.get(prop, {}).get("const") is not False:
            errors.append(f"schema_{prop}_must_be_false")

    for field in required_fields:
        if field not in command:
            errors.append(f"missing_required_field:{field}")
    if command.get("schema_version") != schema_version:
        errors.append("schema_version_mismatch")
    if target_route_id is not None and command.get("target_route_id") != target_route_id:
        errors.append(route_error)
    if target_egress_type is not None and command.get("target_egress_type") != target_egress_type:
        errors.append(type_error)
    if check_command_shape:
        if command.get("command_type") not in {"deny_noop", "report_only_apply_command_contract"}:
            errors.append("command_type_must_be_deny_or_report_only_contract")
        expected_scope = "none" if command.get("command_type") == "deny_noop" else "report_only_apply_command_contract"
        if command.get("allowed_scope") != expected_scope:
            errors.append("allowed_scope_must_match_command_type")
        if command.get("target_request_ids") != []:
            errors.append("target_request_ids_must_be_empty")

    for key, expected in expected_paths.items():
        value = str(command.get(key, ""))
        if value != expected:
            errors.append(f"{key}_must_match_current_source")
        if not value or not path_inside_root(value):
            errors.append(f"{key}_must_stay_inside_lab")

    _append_false_field_errors(errors, sources, source_false_fields, prefix="source_")
    _append_zero_field_errors(errors, sources, source_zero_fields, prefix="source_")
    _append_false_field_errors(errors, command, command_false_fields)
    _append_zero_field_errors(errors, command, command_zero_fields)

    boundary = command.get("runtime_boundary", {})
    if not isinstance(boundary, dict):
        errors.append("runtime_boundary_must_be_object")
        boundary = {}
    for key, expected in zero_boundary.items():
        if boundary.get(key) != expected:
            errors.append(f"runtime_boundary_{key}_must_equal_{expected}")
    return errors
