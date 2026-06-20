import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_agent_company_migration_parser_module_files_facade_reexports_phase_modules() -> None:
    from agent_company_core import agent_company_migration_parser_module_files as facade
    from agent_company_core import agent_company_migration_parser_module_fixture_checks
    from agent_company_core import agent_company_migration_parser_module_file_draft
    from agent_company_core import agent_company_migration_parser_static_review

    assert (
        facade.write_agent_company_migration_decision_module_fixture_checks
        is agent_company_migration_parser_module_fixture_checks.write_agent_company_migration_decision_module_fixture_checks
    )
    assert (
        facade.write_agent_company_migration_decision_parser_module_file_draft
        is agent_company_migration_parser_module_file_draft.write_agent_company_migration_decision_parser_module_file_draft
    )
    assert (
        facade.write_agent_company_migration_decision_parser_static_review
        is agent_company_migration_parser_static_review.write_agent_company_migration_decision_parser_static_review
    )


def test_agent_company_migration_parser_module_file_draft_content_builds_report_only_source() -> None:
    from agent_company_core.agent_company_migration_parser_module_file_draft_content import (
        build_parser_module_file_draft_content,
    )

    module_payload = {
        "guard_functions": [
            "guard_json_object_only",
            "guard_required_fields_present",
            "guard_known_decision_type",
            "guard_scope_boundaries",
            "guard_artifact_paths",
            "guard_expiration_and_signature",
            "guard_report_only_result",
            "guard_no_apply_side_effects",
            "guard_fixture_coverage",
        ],
        "accepted_decision_types": ["hold", "approve", "request_rework", "reject"],
        "result_fields": [
            "accepted",
            "decision_type",
            "result_state",
            "refusal_reasons",
            "artifact_paths",
            "expires_at",
            "signed_utc",
            "report_only",
        ],
        "refusal_reasons": [
            "not_json_object",
            "missing_required_fields",
            "unknown_decision_type",
            "forbidden_scope",
            "missing_artifact_paths",
            "unsigned_decision",
            "expired_or_missing_expiration",
            "report_only_boundary",
        ],
        "fixture_coverage": [{"fixture": f"fixture_{index}"} for index in range(12)],
    }

    content = build_parser_module_file_draft_content(module_payload)

    assert content["parser_module_file_draft_count"] == 1
    assert content["module_source_line_count"] == 80
    assert content["guard_function_count"] == 9
    assert content["accepted_decision_type_count"] == 4
    assert content["result_field_count"] == 8
    assert content["refusal_reason_count"] == 8
    assert content["fixture_coverage_count"] == 12
    assert "ALLOWED_DECISION_TYPES = ('hold', 'approve', 'request_rework', 'reject')" in content["module_source"]
    assert "def parse_report_only_decision(decision: object" in content["module_source"]
    assert content["module_source"].endswith("\n")
