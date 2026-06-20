import ast
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")

APPLY_COMMAND_ARTIFACT_TESTS = [
    "test_account_wallet_payment_egress_apply_command_contract.py",
    "test_browser_read_only_apply_command_contract.py",
    "test_egress_route_apply_command_contract.py",
    "test_local_a2a_egress_apply_command_contract.py",
    "test_model_api_egress_apply_command_contract.py",
    "test_public_action_egress_apply_command_contract.py",
    "test_runtime_process_egress_apply_command_contract.py",
    "test_telemetry_export_egress_apply_command_contract.py",
]


def _calls_helper(module_path: Path, helper_name: str) -> bool:
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == helper_name:
                return True
    return False


def test_apply_command_artifact_tests_use_generated_artifact_loader() -> None:
    for file_name in APPLY_COMMAND_ARTIFACT_TESTS:
        module_path = ROOT / "tests" / file_name

        assert _calls_helper(module_path, "run_validator_load_artifacts"), file_name
