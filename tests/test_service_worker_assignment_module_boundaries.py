import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_service_worker_assignment_facade_reexports_core_and_report_modules() -> None:
    from agent_company_core import service_worker_assignment as facade
    from agent_company_core import service_worker_assignment_core
    from agent_company_core import service_worker_assignment_plan
    from agent_company_core import service_worker_pool_registry
    from agent_company_core import service_worker_pool_registration
    from agent_company_core import service_worker_gate_map

    assert facade.service_worker_assignment_plan_entry is service_worker_assignment_core.service_worker_assignment_plan_entry
    assert facade.write_service_worker_assignment_plan is service_worker_assignment_plan.write_service_worker_assignment_plan
    assert facade.service_worker_pool_registry_entries is service_worker_pool_registry.service_worker_pool_registry_entries
    assert facade.write_service_worker_pool_registry is service_worker_pool_registry.write_service_worker_pool_registry
    assert facade.service_worker_pool_registration_entry is service_worker_pool_registration.service_worker_pool_registration_entry
    assert facade.write_service_worker_pool_registration_plan is service_worker_pool_registration.write_service_worker_pool_registration_plan
    assert facade.service_worker_gate_map_entry is service_worker_gate_map.service_worker_gate_map_entry
    assert facade.write_service_worker_gate_map is service_worker_gate_map.write_service_worker_gate_map

def test_service_worker_gate_map_content_builds_payload_validation_and_markdown() -> None:
    from agent_company_core.service_worker_gate_map_content import build_service_worker_gate_map_artifacts

    entries = [
        {
            "source_service_request_id": "req-alpha",
            "worker_type": "browser_read_only",
            "service_status": "approved",
            "current_blocking_gate": "execution_readiness_required",
            "next_action": "Rerun readiness checks.",
            "recommended_worker_pool_id": "service-worker-browser-read-only-pool",
            "pool_status": "registered",
            "approval_granted_by_gate_map": False,
            "pool_registered_by_gate_map": False,
            "service_request_assigned_by_gate_map": False,
        },
        {
            "source_service_request_id": "req-beta",
            "worker_type": None,
            "service_status": "draft",
            "current_blocking_gate": "human_cro_approval_required",
            "next_action": "Use the CRO queue.",
            "recommended_worker_pool_id": "service-worker-other-gated-work-pool",
            "pool_status": None,
            "approval_granted_by_gate_map": False,
            "pool_registered_by_gate_map": False,
            "service_request_assigned_by_gate_map": False,
        },
    ]

    artifacts = build_service_worker_gate_map_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        db_path=Path("agent_company.db"),
        filters={"request_id": None, "lane_id": "lane-alpha", "status": None},
        entries=entries,
        json_output_path=Path("reports/service-worker-gate-map.json"),
        validation_path=Path("reports/service-worker-gate-map-validation.json"),
    )

    payload = artifacts["payload"]
    validation = artifacts["validation_payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "service_worker_gate_map.v1"
    assert payload["filters"] == {"request_id": None, "lane_id": "lane-alpha", "status": None}
    assert payload["mapped_count"] == 2
    assert payload["ready_for_assignment_count"] == 0
    assert payload["gate_counts"] == {
        "execution_readiness_required": 1,
        "human_cro_approval_required": 1,
    }
    assert payload["worker_type_counts"] == {"browser_read_only": 1, "unknown": 1}
    assert payload["pool_status_counts"] == {"registered": 1, "unknown": 1}
    assert validation["all_rows_no_approval"] is True
    assert validation["all_rows_no_registration"] is True
    assert validation["all_rows_no_assignment"] is True
    assert "# Service Worker Gate Map" in markdown
    assert "| `approved` | `execution_readiness_required` | `req-alpha` |" in markdown
    assert "Gate map only" in payload["execution_notice"]

