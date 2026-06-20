"""Shared invariant checks for report-only signed egress decisions."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from datetime import datetime
from typing import Any


def _append_false_field_errors(
    errors: list[str],
    payload: dict[str, Any],
    fields: Iterable[str],
) -> None:
    for key in fields:
        if payload.get(key) is not False:
            errors.append(f"{key}_must_be_false")


def _append_zero_field_errors(
    errors: list[str],
    payload: dict[str, Any],
    fields: Iterable[str],
) -> None:
    for key in fields:
        if payload.get(key) != 0:
            errors.append(f"{key}_must_be_zero")


def collect_common_signed_decision_errors(
    *,
    schema: dict[str, Any],
    decision: dict[str, Any],
    route: dict[str, Any],
    required_fields: Iterable[str],
    schema_version: str,
    target_route_id: str,
    target_egress_type: str,
    evaluation_utc: str,
    expected_docket_path: str,
    expected_docket_sha256: str,
    path_inside_root: Callable[[str], bool],
    parse_utc: Callable[[str], datetime | None],
    schema_false_props: Iterable[str],
    schema_route_error: str,
    schema_type_error: str,
    route_error: str,
    type_error: str,
    decision_false_fields: Iterable[str],
    decision_zero_fields: Iterable[str],
    zero_boundary: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    evaluation_time = parse_utc(evaluation_utc)
    properties = schema.get("properties", {})

    if properties.get("decision", {}).get("enum", [None])[0] != "deny":
        errors.append("schema_decision_enum_must_start_deny")
    if properties.get("route_id", {}).get("const") != target_route_id:
        errors.append(schema_route_error)
    if properties.get("egress_type", {}).get("const") != target_egress_type:
        errors.append(schema_type_error)
    for prop in schema_false_props:
        if properties.get(prop, {}).get("const") is not False:
            errors.append(f"schema_{prop}_must_be_false")

    for field in required_fields:
        if field not in decision:
            errors.append(f"missing_required_field:{field}")

    decision_value = decision.get("decision")
    if decision_value not in {"deny", "approve_route_preflight_only"}:
        errors.append("decision_must_be_deny_or_preflight_only")
    if decision.get("schema_version") != schema_version:
        errors.append("schema_version_mismatch")
    if decision.get("route_id") != target_route_id:
        errors.append(route_error)
    if decision.get("egress_type") != target_egress_type:
        errors.append(type_error)
    if not decision.get("operator_id"):
        errors.append("operator_id_required")
    if not decision.get("operator_attestation"):
        errors.append("operator_attestation_required")

    signed = parse_utc(str(decision.get("signed_utc", "")))
    expires = parse_utc(str(decision.get("expires_utc", "")))
    if signed is None:
        errors.append("signed_utc_must_be_valid")
    if expires is None:
        errors.append("expires_utc_must_be_valid")
    if signed and expires and expires <= signed:
        errors.append("expires_utc_must_be_after_signed_utc")
    if expires and evaluation_time and expires <= evaluation_time:
        errors.append("decision_expired")

    docket_path = str(decision.get("source_gateway_docket_path", ""))
    if decision.get("source_gateway_docket_path") != expected_docket_path:
        errors.append("source_gateway_docket_path_must_match")
    if not path_inside_root(docket_path):
        errors.append("source_gateway_docket_path_must_stay_inside_lab")
    if decision.get("source_gateway_docket_sha256") != expected_docket_sha256:
        errors.append("source_gateway_docket_sha256_mismatch")

    required_gates = list(route.get("required_gates", []))
    if route.get("egress_type") != target_egress_type:
        errors.append("source_route_egress_type_mismatch")
    if route.get("gateway_registration_allowed") is not False or route.get("gateway_start_allowed") is not False:
        errors.append("source_route_gateway_must_remain_blocked")
    if route.get("live_execution_allowed") is not False:
        errors.append("source_route_live_execution_must_be_false")

    if decision_value == "deny":
        if decision.get("allowed_scope") != "none":
            errors.append("deny_scope_must_be_none")
        if decision.get("allowed_gate_ids") != []:
            errors.append("deny_allowed_gate_ids_must_be_empty")
        if decision.get("operator_attestation") != "deny-all-no-egress":
            errors.append("deny_attestation_must_match")
    elif decision_value == "approve_route_preflight_only":
        if decision.get("allowed_scope") != f"egress_route_preflight_only:{target_route_id}":
            errors.append("allowed_scope_must_be_exact_preflight_scope")
        if decision.get("allowed_gate_ids") != required_gates:
            errors.append("allowed_gate_ids_must_match_route_required_gates")

    _append_false_field_errors(errors, decision, decision_false_fields)
    _append_zero_field_errors(errors, decision, decision_zero_fields)
    if decision.get("approval_is_not_apply") is not True:
        errors.append("approval_is_not_apply_must_be_true")

    boundary = decision.get("runtime_boundary", {})
    if not isinstance(boundary, dict):
        errors.append("runtime_boundary_must_be_object")
        boundary = {}
    for key, expected in zero_boundary.items():
        if boundary.get(key) != expected:
            errors.append(f"runtime_boundary_{key}_must_equal_{expected}")

    return errors
