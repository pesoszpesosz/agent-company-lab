import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_money_paths_facade_reexports_phase_modules() -> None:
    import agent_company_core.money_paths as facade
    from agent_company_core import money_paths_coverage
    from agent_company_core import money_paths_evidence
    from agent_company_core import money_paths_manager_proof
    from agent_company_core import money_paths_ranked_proof

    assert facade.money_path_lane_assignment is money_paths_coverage.money_path_lane_assignment
    assert facade.write_money_path_coverage_audit is money_paths_coverage.write_money_path_coverage_audit
    assert facade.first_local_evidence_summary is money_paths_evidence.first_local_evidence_summary
    assert facade.write_first_local_evidence_packets is money_paths_evidence.write_first_local_evidence_packets
    assert facade.manager_proof_task_template is money_paths_manager_proof.manager_proof_task_template
    assert (
        facade.write_manager_proof_task_promotion_queue
        is money_paths_manager_proof.write_manager_proof_task_promotion_queue
    )
    assert facade.manager_proof_task_queue_score is money_paths_manager_proof.manager_proof_task_queue_score
    assert facade.write_first_ranked_manager_proof is money_paths_ranked_proof.write_first_ranked_manager_proof

def test_money_paths_coverage_facade_reexports_coverage_modules() -> None:
    from agent_company_core import money_path_coverage_audit
    from agent_company_core import money_path_lane_assignment
    from agent_company_core import money_paths_coverage

    assert money_paths_coverage.money_path_lane_assignment is money_path_lane_assignment.money_path_lane_assignment
    assert money_paths_coverage.write_money_path_coverage_audit is money_path_coverage_audit.write_money_path_coverage_audit

def test_money_path_coverage_facade_reexports_audit_phase_helpers() -> None:
    from agent_company_core import money_path_coverage_model
    from agent_company_core import money_path_coverage_report
    from agent_company_core import money_paths_coverage

    assert money_paths_coverage.build_money_path_coverage_model is money_path_coverage_model.build_money_path_coverage_model
    assert money_paths_coverage.money_path_runtime_boundary is money_path_coverage_model.money_path_runtime_boundary
    assert money_paths_coverage.render_money_path_coverage_report is money_path_coverage_report.render_money_path_coverage_report


def test_money_path_coverage_model_and_report_are_separate_phases(tmp_path) -> None:
    from agent_company_core.money_path_coverage_model import build_money_path_coverage_model
    from agent_company_core.money_path_coverage_report import render_money_path_coverage_report

    lanes = [
        {
            "lane_id": "platform_engineering",
            "department": "Platform",
            "owner_agent_id": "platform-agent",
            "owner_thread_id": "thread-platform",
            "status": "active",
        },
        {
            "lane_id": "money_source_discovery",
            "department": "Revenue",
            "owner_agent_id": "money-agent",
            "owner_thread_id": "thread-money",
            "status": "active",
        },
        {
            "lane_id": "submitted_bounty_payouts",
            "department": "Revenue",
            "owner_agent_id": None,
            "owner_thread_id": "thread-payouts",
            "status": "active",
        },
    ]
    model = build_money_path_coverage_model(
        lanes=lanes,
        evidence_counts={},
        task_counts={},
        source_spec_counts={},
        parked_request_counts={"money_source_discovery": 1},
        trace_counts={},
    )

    assert model["read_only_boundary_preserved"] is True
    assert [row["lane_id"] for row in model["recommended_next_lanes"]] == ["money_source_discovery"]
    assert model["runtime_boundary"]["external_side_effects"] is False

    report = render_money_path_coverage_report(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path=tmp_path / "audit.json",
        validation_path=tmp_path / "validation.json",
        coverage_model=model,
        source_spec_count=0,
        service_request_status_counts={"needs_review": 1},
        payload={"next_action": "Run the local proof wave."},
        failures=[],
    )

    assert "# Agent Company Money-Path Coverage Audit" in report
    assert "`money_source_discovery`" in report
    assert "Run the local proof wave." in report
