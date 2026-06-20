import ast
import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from runtime_boundary_shared_core import collect_runtime_boundary_errors  # noqa: E402


def _calls_runtime_boundary_helper(module_path: Path) -> bool:
    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "collect_runtime_boundary_errors":
                return True
    return False


def test_runtime_boundary_helper_reports_changed_and_missing_values() -> None:
    errors = collect_runtime_boundary_errors(
        {"runtime_boundary": {"browser_sessions_started": 1}},
        {"browser_sessions_started": 0, "external_side_effects": False},
    )

    assert errors == [
        "runtime_boundary_browser_sessions_started_must_equal_0",
        "runtime_boundary_external_side_effects_must_equal_False",
    ]


def test_runtime_boundary_helper_reports_non_object_boundary() -> None:
    errors = collect_runtime_boundary_errors(
        {"runtime_boundary": "nope"},
        {"browser_sessions_started": 0},
    )

    assert errors == [
        "runtime_boundary_must_be_object",
        "runtime_boundary_browser_sessions_started_must_equal_0",
    ]


def test_agent_egress_event_ledger_uses_runtime_boundary_helper() -> None:
    module_path = ROOT / "tools" / "agent_egress_event_ledger_core.py"

    assert _calls_runtime_boundary_helper(module_path)


def test_browser_worker_adapter_contract_uses_runtime_boundary_helper() -> None:
    module_path = ROOT / "tools" / "browser_worker_adapter_contract_core.py"

    assert _calls_runtime_boundary_helper(module_path)


def test_browser_read_only_worker_policy_uses_runtime_boundary_helper() -> None:
    module_path = ROOT / "tools" / "browser_read_only_worker_policy_core.py"

    assert _calls_runtime_boundary_helper(module_path)


def test_runtime_start_preflight_uses_runtime_boundary_helper() -> None:
    module_path = ROOT / "tools" / "runtime_start_preflight_core.py"

    assert _calls_runtime_boundary_helper(module_path)


def test_worker_activation_preflight_chain_uses_runtime_boundary_helper() -> None:
    module_path = ROOT / "tools" / "worker_activation_preflight_chain_core.py"

    assert _calls_runtime_boundary_helper(module_path)


def test_checkpoint_interrupt_contract_uses_runtime_boundary_helper() -> None:
    module_path = ROOT / "tools" / "checkpoint_interrupt_contract_core.py"

    assert _calls_runtime_boundary_helper(module_path)
