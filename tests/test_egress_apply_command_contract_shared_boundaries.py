import copy
import ast
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from egress_apply_command_contract_shared_core import (  # noqa: E402
    collect_common_contract_errors,
)


def _inside_lab(value: str) -> bool:
    return str(value).startswith(str(ROOT))


def _calls_shared_collector(module_path: Path) -> bool:
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "collect_common_contract_errors":
                return True
    return False


BASE_SCHEMA = {
    "properties": {
        "command_type": {"enum": ["deny_noop", "report_only_apply_command_contract"]},
        "target_route_id": {"const": "account_wallet_payment_gateway"},
        "target_egress_type": {"const": "account_wallet_payment"},
        "apply_allowed": {"const": False},
    }
}
BASE_COMMAND = {
    "schema_version": "agent_company.account_wallet_payment_egress_apply_command_contract.v1",
    "command_id": "account-wallet-payment-apply-command-positive-contract",
    "command_type": "report_only_apply_command_contract",
    "target_route_id": "account_wallet_payment_gateway",
    "target_egress_type": "account_wallet_payment",
    "source_guard_validation_path": str(ROOT / "reports" / "guard.json"),
    "target_request_ids": [],
    "allowed_scope": "report_only_apply_command_contract",
    "apply_allowed": False,
    "worker_starts": 0,
    "runtime_boundary": {
        "apply_allowed": False,
        "worker_starts": 0,
    },
}
BASE_SOURCES = {
    "apply_allowed": False,
    "worker_starts": 0,
}


def test_common_contract_errors_accept_clean_report_only_boundary() -> None:
    assert (
        collect_common_contract_errors(
            schema=BASE_SCHEMA,
            command=BASE_COMMAND,
            sources=BASE_SOURCES,
            required_fields=list(BASE_COMMAND),
            schema_version="agent_company.account_wallet_payment_egress_apply_command_contract.v1",
            target_route_id="account_wallet_payment_gateway",
            target_egress_type="account_wallet_payment",
            schema_false_props=["apply_allowed"],
            schema_route_error="schema_target_route_id_must_be_account_wallet_payment_gateway",
            schema_type_error="schema_target_egress_type_must_be_account_wallet_payment",
            route_error="target_route_id_must_match_account_wallet_payment_gateway",
            type_error="target_egress_type_must_be_account_wallet_payment",
            expected_paths={"source_guard_validation_path": str(ROOT / "reports" / "guard.json")},
            path_inside_root=_inside_lab,
            source_false_fields=["apply_allowed"],
            source_zero_fields=["worker_starts"],
            command_false_fields=["apply_allowed"],
            command_zero_fields=["worker_starts"],
            zero_boundary={"apply_allowed": False, "worker_starts": 0},
        )
        == []
    )


def test_common_contract_errors_accept_route_only_contract_without_egress_type() -> None:
    schema = {
        "properties": {
            "command_type": {"enum": ["deny_noop", "report_only_apply_command_contract"]},
            "target_route_id": {"const": "browser_read_only_gateway"},
            "apply_allowed": {"const": False},
        }
    }
    command = {
        "schema_version": "agent_company.egress_route_apply_command_contract.v1",
        "command_id": "egress-route-apply-command-positive-contract",
        "command_type": "report_only_apply_command_contract",
        "target_route_id": "browser_read_only_gateway",
        "source_guard_validation_path": str(ROOT / "reports" / "guard.json"),
        "target_request_ids": [],
        "allowed_scope": "report_only_apply_command_contract",
        "apply_allowed": False,
        "runtime_boundary": {"apply_allowed": False},
    }

    assert (
        collect_common_contract_errors(
            schema=schema,
            command=command,
            sources={"apply_allowed": False},
            required_fields=list(command),
            schema_version="agent_company.egress_route_apply_command_contract.v1",
            target_route_id="browser_read_only_gateway",
            target_egress_type=None,
            schema_false_props=["apply_allowed"],
            schema_route_error="schema_target_route_must_be_browser_read_only_gateway",
            schema_type_error="schema_target_egress_type_must_be_browser_read_only",
            route_error="target_route_id_must_match_browser_read_only_gateway",
            type_error="target_egress_type_must_be_browser_read_only",
            expected_paths={"source_guard_validation_path": str(ROOT / "reports" / "guard.json")},
            path_inside_root=_inside_lab,
            source_false_fields=["apply_allowed"],
            source_zero_fields=[],
            command_false_fields=["apply_allowed"],
            command_zero_fields=[],
            zero_boundary={"apply_allowed": False},
        )
        == []
    )


def test_common_contract_errors_can_defer_command_shape_checks_to_contract_core() -> None:
    command = copy.deepcopy(BASE_COMMAND)
    command["command_type"] = "execute_live_apply"
    command.pop("allowed_scope")
    command["target_request_ids"] = ["req-live-apply"]

    errors = collect_common_contract_errors(
        schema=BASE_SCHEMA,
        command=command,
        sources=BASE_SOURCES,
        required_fields=["schema_version"],
        schema_version="agent_company.account_wallet_payment_egress_apply_command_contract.v1",
        target_route_id="account_wallet_payment_gateway",
        target_egress_type="account_wallet_payment",
        schema_false_props=["apply_allowed"],
        schema_route_error="schema_target_route_id_must_be_account_wallet_payment_gateway",
        schema_type_error="schema_target_egress_type_must_be_account_wallet_payment",
        route_error="target_route_id_must_match_account_wallet_payment_gateway",
        type_error="target_egress_type_must_be_account_wallet_payment",
        expected_paths={"source_guard_validation_path": str(ROOT / "reports" / "guard.json")},
        path_inside_root=_inside_lab,
        source_false_fields=["apply_allowed"],
        source_zero_fields=["worker_starts"],
        command_false_fields=["apply_allowed"],
        command_zero_fields=["worker_starts"],
        zero_boundary={"apply_allowed": False, "worker_starts": 0},
        check_command_shape=False,
    )

    assert "command_type_must_be_deny_or_report_only_contract" not in errors
    assert "allowed_scope_must_match_command_type" not in errors
    assert "target_request_ids_must_be_empty" not in errors


def test_common_contract_errors_reports_path_source_command_and_boundary_violations() -> None:
    schema = copy.deepcopy(BASE_SCHEMA)
    schema["properties"]["target_route_id"]["const"] = "public_action_gateway"
    command = copy.deepcopy(BASE_COMMAND)
    command.pop("allowed_scope")
    command["source_guard_validation_path"] = r"C:\Temp\guard.json"
    command["target_request_ids"] = ["req-live-apply"]
    command["apply_allowed"] = True
    command["worker_starts"] = 1
    command["runtime_boundary"]["worker_starts"] = 1
    sources = {"apply_allowed": True, "worker_starts": 1}

    errors = collect_common_contract_errors(
        schema=schema,
        command=command,
        sources=sources,
        required_fields=list(BASE_COMMAND),
        schema_version="agent_company.account_wallet_payment_egress_apply_command_contract.v1",
        target_route_id="account_wallet_payment_gateway",
        target_egress_type="account_wallet_payment",
        schema_false_props=["apply_allowed"],
        schema_route_error="schema_target_route_id_must_be_account_wallet_payment_gateway",
        schema_type_error="schema_target_egress_type_must_be_account_wallet_payment",
        route_error="target_route_id_must_match_account_wallet_payment_gateway",
        type_error="target_egress_type_must_be_account_wallet_payment",
        expected_paths={"source_guard_validation_path": str(ROOT / "reports" / "guard.json")},
        path_inside_root=_inside_lab,
        source_false_fields=["apply_allowed"],
        source_zero_fields=["worker_starts"],
        command_false_fields=["apply_allowed"],
        command_zero_fields=["worker_starts"],
        zero_boundary={"apply_allowed": False, "worker_starts": 0},
    )

    assert "schema_target_route_id_must_be_account_wallet_payment_gateway" in errors
    assert "missing_required_field:allowed_scope" in errors
    assert "source_guard_validation_path_must_match_current_source" in errors
    assert "source_guard_validation_path_must_stay_inside_lab" in errors
    assert "target_request_ids_must_be_empty" in errors
    assert "source_apply_allowed_must_be_false" in errors
    assert "source_worker_starts_must_be_zero" in errors
    assert "apply_allowed_must_be_false" in errors
    assert "worker_starts_must_be_zero" in errors
    assert "runtime_boundary_worker_starts_must_equal_0" in errors


def test_model_api_apply_command_contract_uses_shared_common_collector() -> None:
    module_path = ROOT / "tools" / "model_api_egress_apply_command_contract_core.py"

    assert _calls_shared_collector(module_path)


def test_runtime_process_apply_command_contract_uses_shared_common_collector() -> None:
    module_path = ROOT / "tools" / "runtime_process_egress_apply_command_contract_core.py"

    assert _calls_shared_collector(module_path)


def test_public_action_apply_command_contract_uses_shared_common_collector() -> None:
    module_path = ROOT / "tools" / "public_action_egress_apply_command_contract_core.py"

    assert _calls_shared_collector(module_path)


def test_local_a2a_apply_command_contract_uses_shared_common_collector() -> None:
    module_path = ROOT / "tools" / "local_a2a_egress_apply_command_contract_core.py"

    assert _calls_shared_collector(module_path)


def test_egress_route_apply_command_contract_uses_shared_common_collector() -> None:
    module_path = ROOT / "tools" / "egress_route_apply_command_contract_core.py"

    assert _calls_shared_collector(module_path)


def test_browser_read_only_apply_command_contract_uses_shared_common_collector() -> None:
    module_path = ROOT / "tools" / "browser_read_only_apply_command_contract_core.py"

    assert _calls_shared_collector(module_path)
