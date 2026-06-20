import ast
import copy
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from egress_signed_decision_guard_shared_core import (  # noqa: E402
    collect_common_signed_decision_errors,
)


def _inside_lab(value: str) -> bool:
    return str(value).startswith(str(ROOT))


def _parse_utc(value: str):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def _calls_shared_collector(module_path: Path) -> bool:
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    return any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "collect_common_signed_decision_errors"
        for node in ast.walk(tree)
    )


SCHEMA = {
    "properties": {
        "decision": {"enum": ["deny", "approve_route_preflight_only"]},
        "route_id": {"const": "telemetry_export_gateway"},
        "egress_type": {"const": "telemetry_export"},
        "telemetry_export_allowed": {"const": False},
    }
}
ROUTE = {
    "route_id": "telemetry_export_gateway",
    "egress_type": "telemetry_export",
    "gateway_registration_allowed": False,
    "gateway_start_allowed": False,
    "live_execution_allowed": False,
    "required_gates": ["telemetry_privacy_export_gate_v1"],
}
DECISION = {
    "schema_version": "agent_company.egress_route_signed_decision_intake_contract.v1",
    "decision_id": "telemetry-export-positive",
    "decision": "approve_route_preflight_only",
    "route_id": "telemetry_export_gateway",
    "egress_type": "telemetry_export",
    "source_gateway_docket_path": str(ROOT / "reports" / "gateway.json"),
    "source_gateway_docket_sha256": "abc123",
    "operator_id": "human-operator",
    "operator_attestation": "route-specific attestation",
    "signed_utc": "2026-06-18T04:50:00Z",
    "expires_utc": "2099-01-01T00:00:00Z",
    "allowed_scope": "egress_route_preflight_only:telemetry_export_gateway",
    "allowed_gate_ids": ["telemetry_privacy_export_gate_v1"],
    "approval_is_not_apply": True,
    "gateway_start_allowed": False,
    "telemetry_export_allowed": False,
    "service_requests_updated": 0,
    "runtime_boundary": {
        "gateway_starts": 0,
        "telemetry_export_allowed": False,
    },
}


def _collect(decision: dict) -> list[str]:
    return collect_common_signed_decision_errors(
        schema=SCHEMA,
        decision=decision,
        route=ROUTE,
        required_fields=list(DECISION),
        schema_version="agent_company.egress_route_signed_decision_intake_contract.v1",
        target_route_id="telemetry_export_gateway",
        target_egress_type="telemetry_export",
        evaluation_utc="2026-06-18T05:00:00Z",
        expected_docket_path=str(ROOT / "reports" / "gateway.json"),
        expected_docket_sha256="abc123",
        path_inside_root=_inside_lab,
        parse_utc=_parse_utc,
        schema_false_props=["telemetry_export_allowed"],
        schema_route_error="schema_route_const_must_target_telemetry_export_gateway",
        schema_type_error="schema_egress_type_const_must_target_telemetry_export",
        route_error="route_id_must_match_telemetry_export_gateway",
        type_error="egress_type_must_be_telemetry_export",
        decision_false_fields=["gateway_start_allowed", "telemetry_export_allowed"],
        decision_zero_fields=["service_requests_updated"],
        zero_boundary={"gateway_starts": 0, "telemetry_export_allowed": False},
    )


def test_common_signed_decision_errors_accept_clean_preflight_boundary() -> None:
    assert _collect(copy.deepcopy(DECISION)) == []


def test_common_signed_decision_errors_report_path_time_scope_and_boundary_violations() -> None:
    decision = copy.deepcopy(DECISION)
    decision.pop("approval_is_not_apply")
    decision["source_gateway_docket_path"] = r"C:\Temp\gateway.json"
    decision["source_gateway_docket_sha256"] = "wrong"
    decision["expires_utc"] = "2026-06-18T04:55:00Z"
    decision["allowed_scope"] = "live_apply"
    decision["allowed_gate_ids"] = ["wrong_gate"]
    decision["gateway_start_allowed"] = True
    decision["service_requests_updated"] = 1
    decision["runtime_boundary"]["gateway_starts"] = 1

    errors = _collect(decision)

    assert "missing_required_field:approval_is_not_apply" in errors
    assert "source_gateway_docket_path_must_match" in errors
    assert "source_gateway_docket_path_must_stay_inside_lab" in errors
    assert "source_gateway_docket_sha256_mismatch" in errors
    assert "decision_expired" in errors
    assert "allowed_scope_must_be_exact_preflight_scope" in errors
    assert "allowed_gate_ids_must_match_route_required_gates" in errors
    assert "gateway_start_allowed_must_be_false" in errors
    assert "service_requests_updated_must_be_zero" in errors
    assert "approval_is_not_apply_must_be_true" in errors
    assert "runtime_boundary_gateway_starts_must_equal_0" in errors


def test_signed_decision_guard_cores_use_shared_common_collector() -> None:
    assert _calls_shared_collector(
        ROOT / "tools" / "account_wallet_payment_egress_signed_decision_guard_core.py"
    )
    assert _calls_shared_collector(
        ROOT / "tools" / "telemetry_export_egress_signed_decision_guard_core.py"
    )
