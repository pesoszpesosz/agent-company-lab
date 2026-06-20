import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_agent_company_migration_foundation_review_facade_reexports_phase_modules() -> None:
    from agent_company_core import agent_company_migration_foundation_review as facade
    from agent_company_core import agent_company_migration_report_only_draft
    from agent_company_core import agent_company_migration_apply_preflight
    from agent_company_core import agent_company_migration_operator_review

    assert (
        facade.write_agent_company_report_only_migration_draft
        is agent_company_migration_report_only_draft.write_agent_company_report_only_migration_draft
    )
    assert (
        facade.write_agent_company_migration_apply_preflight
        is agent_company_migration_apply_preflight.write_agent_company_migration_apply_preflight
    )
    assert (
        facade.write_agent_company_migration_operator_review
        is agent_company_migration_operator_review.write_agent_company_migration_operator_review
    )

def test_agent_company_migration_apply_preflight_artifact_builder_renders_payload_and_markdown() -> None:
    from pathlib import Path

    from agent_company_core.agent_company_migration_apply_preflight_content import (
        build_agent_company_migration_apply_preflight_artifacts,
    )

    preflight_checks = [f"preflight_check_{index}" for index in range(9)]
    operator_gates = [f"operator_gate_{index}" for index in range(7)]
    dry_run_steps = [f"dry_run_step_{index}" for index in range(8)]
    apply_command_contract = {
        "command_name": "apply-agent-company-department-schema-migration",
        "default_enabled": False,
        "required_inputs": ["operator_approval_id", "backup_path"],
        "must_refuse_when": ["approval_missing", "backup_missing"],
    }
    rollback_drills = [f"rollback_drill_{index}" for index in range(3)]

    artifacts = build_agent_company_migration_apply_preflight_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path=Path("reports/apply-preflight.json"),
        validation_path=Path("reports/apply-preflight.validation.json"),
        lane_id="platform_engineering",
        preflight_task_id="task-preflight",
        preflight_evidence_id="evidence-preflight",
        source_migration_task_id="task-migration",
        source_migration_evidence_id="evidence-migration",
        preflight_checks=preflight_checks,
        operator_gates=operator_gates,
        dry_run_steps=dry_run_steps,
        apply_command_contract=apply_command_contract,
        rollback_drills=rollback_drills,
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.migration_apply_preflight.v1"
    assert payload["generated_utc"] == "2026-06-20T00:00:00Z"
    assert payload["preflight_lane_id"] == "platform_engineering"
    assert payload["preflight_packet_count"] == 1
    assert payload["preflight_check_count"] == 9
    assert payload["operator_gate_count"] == 7
    assert payload["dry_run_step_count"] == 8
    assert payload["apply_command_contract_count"] == 1
    assert payload["rollback_drill_count"] == 3
    assert payload["runtime_boundary"]["migration_sql_executed"] is False
    assert payload["runtime_boundary"]["apply_command_enabled"] is False
    assert payload["runtime_boundary"]["tables_created"] == 0
    assert payload["local_decision"] == "agent_company_migration_apply_preflight_ready_for_operator_review_packet"
    assert payload["recommended_default"] == "prepare_operator_review_next_without_running_apply_command"
    assert "# Agent Company Migration Apply Preflight" in markdown
    assert "## Dry Run Steps" in markdown
    assert "Default enabled: `False`" in markdown
    assert "This preflight packet does not enable or run an apply command" in markdown
    assert markdown.endswith("\n")

def test_agent_company_migration_operator_review_artifact_builder_renders_payload_and_markdown() -> None:
    from pathlib import Path

    from agent_company_core.agent_company_migration_operator_review_content import (
        build_agent_company_migration_operator_review_artifacts,
    )

    decision_options = [
        {"option": "hold", "effect": "No apply command is enabled.", "default": True},
        {"option": "approve_sandbox_dry_run_only", "effect": "Allow sandbox dry-run only.", "default": False},
        {"option": "request_rework", "effect": "Send the packet back.", "default": False},
        {"option": "reject_migration_path", "effect": "Close this schema path.", "default": False},
    ]
    artifacts = build_agent_company_migration_operator_review_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path=Path("reports/operator-review.json"),
        validation_path=Path("reports/operator-review.validation.json"),
        lane_id="platform_engineering",
        review_task_id="task-review",
        review_evidence_id="evidence-review",
        source_preflight_task_id="task-preflight",
        source_preflight_evidence_id="evidence-preflight",
        decision_options=decision_options,
        approval_conditions=[f"approval_condition_{index}" for index in range(8)],
        refusal_conditions=[f"refusal_condition_{index}" for index in range(8)],
        human_instructions=[f"human_instruction_{index}" for index in range(7)],
        evidence_links=[f"reports/evidence-{index}.json" for index in range(4)],
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.migration_operator_review.v1"
    assert payload["generated_utc"] == "2026-06-20T00:00:00Z"
    assert payload["review_lane_id"] == "platform_engineering"
    assert payload["operator_review_packet_count"] == 1
    assert payload["decision_option_count"] == 4
    assert payload["approval_condition_count"] == 8
    assert payload["refusal_condition_count"] == 8
    assert payload["human_instruction_count"] == 7
    assert payload["evidence_link_count"] == 4
    assert payload["runtime_boundary"]["operator_decision_applied"] is False
    assert payload["runtime_boundary"]["apply_command_enabled"] is False
    assert payload["runtime_boundary"]["tables_created"] == 0
    assert payload["local_decision"] == "agent_company_migration_operator_review_packet_ready_for_signed_decision_or_hold"
    assert payload["recommended_default"] == "hold_without_signed_operator_approval"
    assert "# Agent Company Migration Operator Review" in markdown
    assert "`hold` default" in markdown
    assert "This packet does not apply a decision" in markdown
    assert markdown.endswith("\n")


