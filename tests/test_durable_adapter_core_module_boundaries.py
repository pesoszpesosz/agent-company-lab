import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_durable_adapter_core_facade_reexports_phase_modules() -> None:
    from agent_company_core import durable_adapter_core
    from agent_company_core import durable_adapter_paths
    from agent_company_core import durable_adapter_reducer_dry_run
    from agent_company_core import durable_adapter_validation

    assert durable_adapter_core.resolve_durable_adapter_result_path is durable_adapter_paths.resolve_durable_adapter_result_path
    assert durable_adapter_core.add_durable_adapter_validation_error is durable_adapter_validation.add_durable_adapter_validation_error
    assert durable_adapter_core.require_durable_adapter_nonempty_string is durable_adapter_validation.require_durable_adapter_nonempty_string
    assert durable_adapter_core.validate_durable_adapter_fixture_doc is durable_adapter_validation.validate_durable_adapter_fixture_doc
    assert durable_adapter_core.dry_run_durable_service_request_reducer is durable_adapter_reducer_dry_run.dry_run_durable_service_request_reducer


def test_durable_adapter_validation_collects_required_field_failures() -> None:
    import json

    import pytest

    from agent_company_core.durable_adapter_validation import validate_durable_adapter_fixture_doc

    fixture_doc = {"fixture_count": 1}
    with pytest.raises(SystemExit) as excinfo:
        validate_durable_adapter_fixture_doc(fixture_doc, [{}])

    payload = json.loads(str(excinfo.value))
    assert payload["error"] == "durable_adapter_fixture_validation_failed"
    assert payload["failure_count"] > 0
