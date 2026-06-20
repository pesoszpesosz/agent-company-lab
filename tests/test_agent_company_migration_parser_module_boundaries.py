import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_agent_company_migration_parser_module_facades_reexport_phase_modules() -> None:
    import agent_company_core.agent_company_migration as migration_facade
    import agent_company_core.agent_company_migration_parser_module as parser_facade
    from agent_company_core import agent_company_migration_parser_install_ready
    from agent_company_core import agent_company_migration_parser_module_files
    from agent_company_core import agent_company_migration_parser_scaffold

    assert (
        parser_facade.write_agent_company_migration_decision_parser_scaffold
        is agent_company_migration_parser_scaffold.write_agent_company_migration_decision_parser_scaffold
    )
    assert (
        parser_facade.write_agent_company_migration_decision_parser_module_file_draft
        is agent_company_migration_parser_module_files.write_agent_company_migration_decision_parser_module_file_draft
    )
    assert (
        parser_facade.write_agent_company_migration_decision_parser_static_review
        is agent_company_migration_parser_module_files.write_agent_company_migration_decision_parser_static_review
    )
    assert (
        parser_facade.write_agent_company_migration_decision_parser_install_preflight
        is agent_company_migration_parser_install_ready.write_agent_company_migration_decision_parser_install_preflight
    )
    assert (
        migration_facade.write_agent_company_migration_decision_parser_install_review
        is agent_company_migration_parser_install_ready.write_agent_company_migration_decision_parser_install_review
    )
def test_agent_company_migration_parser_scaffold_facade_reexports_phase_modules() -> None:
    from agent_company_core import agent_company_migration_parser_module_draft
    from agent_company_core import agent_company_migration_parser_scaffold
    from agent_company_core import agent_company_migration_parser_scaffold_plan

    assert (
        agent_company_migration_parser_scaffold.write_agent_company_migration_decision_parser_scaffold
        is agent_company_migration_parser_scaffold_plan.write_agent_company_migration_decision_parser_scaffold
    )
    assert (
        agent_company_migration_parser_scaffold.write_agent_company_migration_decision_parser_module_draft
        is agent_company_migration_parser_module_draft.write_agent_company_migration_decision_parser_module_draft
    )
def test_agent_company_migration_parser_install_ready_facade_reexports_phase_modules() -> None:
    from agent_company_core import agent_company_migration_parser_install_preflight
    from agent_company_core import agent_company_migration_parser_install_ready
    from agent_company_core import agent_company_migration_parser_install_review

    assert (
        agent_company_migration_parser_install_ready.write_agent_company_migration_decision_parser_install_preflight
        is agent_company_migration_parser_install_preflight.write_agent_company_migration_decision_parser_install_preflight
    )
    assert (
        agent_company_migration_parser_install_ready.write_agent_company_migration_decision_parser_install_review
        is agent_company_migration_parser_install_review.write_agent_company_migration_decision_parser_install_review
    )


def test_agent_company_migration_parser_install_preflight_artifact_builder_renders_payload_and_markdown() -> None:
    from pathlib import Path

    from agent_company_core.agent_company_migration_parser_install_preflight_content import (
        build_agent_company_migration_decision_parser_install_preflight_artifacts,
    )

    artifacts = build_agent_company_migration_decision_parser_install_preflight_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path=Path("reports/parser-install-preflight.json"),
        validation_path=Path("reports/parser-install-preflight.validation.json"),
        lane_id="platform_engineering",
        preflight_task_id="task-preflight",
        preflight_evidence_id="evidence-preflight",
        source_static_review_task_id="task-static-review",
        source_static_review_evidence_id="evidence-static-review",
        target_files=[
            {
                "target_path": "E:\\agent-company-lab\\tools\\migration_decision_parser.py",
                "source_artifact": "reports/parser-module-file-draft.json",
                "line_count": 120,
                "install_status": "not_written_requires_operator_approval",
            }
        ],
        install_gates=[f"install_gate_{index}" for index in range(9)],
        preflight_checks=[f"preflight_check_{index}" for index in range(10)],
        rollback_steps=[f"rollback_step_{index}" for index in range(5)],
        approval_requirements=[f"approval_requirement_{index}" for index in range(6)],
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.migration_decision_parser_install_preflight.v1"
    assert payload["generated_utc"] == "2026-06-20T00:00:00Z"
    assert payload["preflight_lane_id"] == "platform_engineering"
    assert payload["install_preflight_count"] == 1
    assert payload["install_gate_count"] == 9
    assert payload["preflight_check_count"] == 10
    assert payload["rollback_step_count"] == 5
    assert payload["approval_requirement_count"] == 6
    assert payload["target_file_count"] == 1
    assert payload["runtime_boundary"]["parser_module_file_written"] is False
    assert payload["runtime_boundary"]["tables_created"] == 0
    assert payload["local_decision"] == "agent_company_migration_decision_parser_install_preflight_ready_for_operator_install_review"
    assert payload["recommended_default"] == "hold_without_operator_approval_to_write_parser_module_file"
    assert "# Agent Company Migration Decision Parser Install Preflight" in markdown
    assert "not_written_requires_operator_approval" in markdown
    assert "This is a report-only install preflight." in markdown
    assert markdown.endswith("\n")


def test_agent_company_migration_parser_install_review_artifact_builder_renders_payload_and_markdown() -> None:
    from pathlib import Path

    from agent_company_core.agent_company_migration_parser_install_review_content import (
        build_agent_company_migration_decision_parser_install_review_artifacts,
    )

    decision_options = [
        {"option": "hold", "effect": "Do not write or install the parser module.", "default": True},
        {"option": "approve_one_file_write_only", "effect": "Permit one local file write only.", "default": False},
        {"option": "request_preflight_rework", "effect": "Return the preflight for edits.", "default": False},
        {"option": "reject_parser_install", "effect": "Close the parser install path.", "default": False},
    ]
    artifacts = build_agent_company_migration_decision_parser_install_review_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path=Path("reports/parser-install-review.json"),
        validation_path=Path("reports/parser-install-review.validation.json"),
        lane_id="platform_engineering",
        review_task_id="task-review",
        review_evidence_id="evidence-review",
        source_preflight_task_id="task-preflight",
        source_preflight_evidence_id="evidence-preflight",
        decision_options=decision_options,
        approval_conditions=[f"approval_condition_{index}" for index in range(7)],
        refusal_conditions=[f"refusal_condition_{index}" for index in range(7)],
        evidence_links=[f"reports/evidence-{index}.json" for index in range(4)],
        operator_instructions=[f"operator_instruction_{index}" for index in range(6)],
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.migration_decision_parser_install_review.v1"
    assert payload["generated_utc"] == "2026-06-20T00:00:00Z"
    assert payload["review_lane_id"] == "platform_engineering"
    assert payload["install_review_count"] == 1
    assert payload["decision_option_count"] == 4
    assert payload["approval_condition_count"] == 7
    assert payload["refusal_condition_count"] == 7
    assert payload["evidence_link_count"] == 4
    assert payload["operator_instruction_count"] == 6
    assert payload["runtime_boundary"]["operator_install_decision_applied"] is False
    assert payload["runtime_boundary"]["parser_module_file_written"] is False
    assert payload["runtime_boundary"]["tables_created"] == 0
    assert payload["local_decision"] == "agent_company_migration_decision_parser_install_review_ready_for_signed_install_decision_or_hold"
    assert payload["recommended_default"] == "hold_without_signed_operator_file_write_approval"
    assert "# Agent Company Migration Decision Parser Install Review" in markdown
    assert "`hold` default" in markdown
    assert "This is a report-only operator review packet." in markdown
    assert markdown.endswith("\n")



def test_agent_company_migration_parser_scaffold_artifact_builder_renders_payload_and_markdown() -> None:
    from agent_company_core.agent_company_migration_parser_scaffold_plan_content import (
        build_agent_company_migration_decision_parser_scaffold_artifacts,
    )

    artifacts = build_agent_company_migration_decision_parser_scaffold_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path=Path("reports/parser-scaffold.json"),
        validation_path=Path("reports/parser-scaffold.validation.json"),
        lane_id="platform_engineering",
        scaffold_task_id="task-agent-company-migration-decision-parser-scaffold-20260616",
        scaffold_evidence_id="agent-company-migration-decision-parser-scaffold-20260616",
        source_runner_task_id="task-agent-company-migration-decision-fixture-runner-20260616",
        source_runner_evidence_id="agent-company-migration-decision-fixture-runner-20260616",
        fixture_coverage=["valid-hold", "reject-live-apply"],
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.migration_decision_parser_scaffold.v1"
    assert payload["generated_utc"] == "2026-06-20T00:00:00Z"
    assert payload["parser_stage_count"] == 7
    assert payload["guard_function_count"] == 9
    assert payload["accepted_decision_type_count"] == 4
    assert payload["result_field_count"] == 8
    assert payload["refusal_reason_count"] == 8
    assert payload["fixture_coverage_count"] == 2
    assert payload["fixture_coverage"] == ["valid-hold", "reject-live-apply"]
    assert payload["runtime_boundary"]["operator_decision_applied"] is False
    assert payload["runtime_boundary"]["tables_created"] == 0
    assert payload["recommended_default"] == "draft_report_only_parser_module_next_without_live_decision_intake"
    assert "# Agent Company Migration Decision Parser Scaffold" in markdown
    assert "`guard_no_live_apply_scope`" in markdown
    assert "This scaffold is report-only." in markdown
    assert "Draft the report-only parser module next" in markdown


def test_agent_company_migration_parser_module_draft_artifact_builder_renders_payload_and_markdown() -> None:
    from pathlib import Path

    from agent_company_core.agent_company_migration_parser_module_draft_content import (
        build_agent_company_migration_decision_parser_module_draft_artifacts,
    )

    artifacts = build_agent_company_migration_decision_parser_module_draft_artifacts(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path=Path("reports/parser-module-draft.json"),
        validation_path=Path("reports/parser-module-draft.validation.json"),
        lane_id="platform_engineering",
        module_task_id="task-module",
        module_evidence_id="evidence-module",
        source_scaffold_task_id="task-scaffold",
        source_scaffold_evidence_id="evidence-scaffold",
        guard_functions=[f"guard_{index}" for index in range(9)],
        accepted_decision_types=["hold", "approve", "rework", "reject"],
        result_fields=[f"field_{index}" for index in range(8)],
        refusal_reasons=[f"reason_{index}" for index in range(8)],
        fixture_coverage=[f"fixture-{index}" for index in range(12)],
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.migration_decision_parser_module_draft.v1"
    assert payload["generated_utc"] == "2026-06-20T00:00:00Z"
    assert payload["module_lane_id"] == "platform_engineering"
    assert payload["parser_module_draft_count"] == 1
    assert payload["module_section_count"] == 8
    assert payload["function_block_count"] == 9
    assert payload["guard_function_count"] == 9
    assert payload["accepted_decision_type_count"] == 4
    assert payload["result_field_count"] == 8
    assert payload["refusal_reason_count"] == 8
    assert payload["fixture_coverage_count"] == 12
    assert payload["runtime_boundary"]["parser_module_file_written"] is False
    assert payload["runtime_boundary"]["tables_created"] == 0
    assert payload["local_decision"] == "agent_company_migration_decision_parser_module_draft_ready_for_report_only_module_fixtures"
    assert payload["recommended_default"] == "draft_report_only_module_fixture_check_next_without_installing_parser_module"
    assert "# Agent Company Migration Decision Parser Module Draft" in markdown
    assert "parse_report_only_decision" in markdown
    assert "This is a report-only parser module draft." in markdown
    assert markdown.endswith("\n")
