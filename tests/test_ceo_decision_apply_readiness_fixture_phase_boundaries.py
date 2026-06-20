import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_ceo_decision_apply_readiness_fixture_facade_reexports_phase_modules() -> None:
    from agent_company_core import ceo_decision_apply_readiness_fixtures as facade
    from agent_company_core import ceo_decision_apply_readiness_negative_fixtures
    from agent_company_core import ceo_decision_apply_readiness_guard_runner
    from agent_company_core import ceo_decision_apply_readiness_positive_fixture
    from agent_company_core import ceo_decision_apply_readiness_positive_runner

    assert (
        facade.write_ceo_decision_parser_apply_readiness_negative_fixtures
        is ceo_decision_apply_readiness_negative_fixtures.write_ceo_decision_parser_apply_readiness_negative_fixtures
    )
    assert (
        facade.write_ceo_decision_parser_apply_readiness_guard_runner
        is ceo_decision_apply_readiness_guard_runner.write_ceo_decision_parser_apply_readiness_guard_runner
    )
    assert (
        facade.write_ceo_decision_parser_apply_readiness_positive_fixture
        is ceo_decision_apply_readiness_positive_fixture.write_ceo_decision_parser_apply_readiness_positive_fixture
    )
    assert (
        facade.write_ceo_decision_parser_apply_readiness_positive_runner
        is ceo_decision_apply_readiness_positive_runner.write_ceo_decision_parser_apply_readiness_positive_runner
    )

def test_ceo_apply_readiness_negative_fixture_content_builds_rejection_suite() -> None:
    from agent_company_core.ceo_decision_apply_readiness_negative_fixture_content import (
        build_ceo_apply_readiness_negative_fixture_content,
    )

    readiness_packet = {
        "target_request_id": "req-1",
        "target_status_before": "needs_review",
        "planned_field_updates": {
            "approval_scope": "approve one bounded change",
            "decision_note": "operator reviewed scope",
        },
        "planned_update_sql_shape": {"max_rows": 1, "set_fields": ["approval_scope", "decision_note"]},
        "rollback_snapshot": {"request_id": "req-1", "updated_at": "2026-06-19T00:00:00Z"},
        "rollback_checks": ["restore approval_scope", "restore decision_note"],
        "required_operator_approvals": ["operator_signature", "explicit_apply_approval"],
        "apply_boundary": {"worker_starts": 0, "external_side_effects": False},
    }

    content = build_ceo_apply_readiness_negative_fixture_content(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path="reports/negative.json",
        validation_path="reports/negative-validation.json",
        source_readiness_validation_path="reports/readiness-validation.json",
        lane_id="platform_engineering",
        fixture_task_id="task-fixtures",
        fixture_evidence_id="evidence-fixtures",
        source_readiness_task_id="task-readiness",
        source_readiness_evidence_id="evidence-readiness",
        readiness_packet=readiness_packet,
    )

    payload = content["payload"]
    markdown = content["markdown"]

    assert content["negative_readiness_fixture_count"] == 6
    assert content["expected_rejection_count"] == 6
    assert content["accepted_readiness_count"] == 0
    assert content["required_readiness_field_count"] == 6
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["negative_readiness_fixtures"][0]["fixture_id"] == "missing-operator-approvals"
    assert content["negative_readiness_fixtures"][-1]["expected_rule_id"] == "reject_side_effect_boundary_open"
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert payload["schema_version"] == "agent_company.ceo_decision_parser_apply_readiness_negative_fixtures.v1"
    assert payload["source_readiness_validation_path"] == "reports/readiness-validation.json"
    assert payload["negative_readiness_fixtures"] == content["negative_readiness_fixtures"]
    assert "## Fixtures" in markdown
    assert "missing-operator-approvals" in markdown
    assert "These are local negative fixtures only" in markdown
    assert markdown.endswith("\n")


def test_ceo_apply_readiness_negative_fixtures_writer_imports_content_helper() -> None:
    from agent_company_core import ceo_decision_apply_readiness_negative_fixtures as writer
    from agent_company_core.ceo_decision_apply_readiness_negative_fixture_content import (
        build_ceo_apply_readiness_negative_fixture_content,
    )

    assert writer.build_ceo_apply_readiness_negative_fixture_content is build_ceo_apply_readiness_negative_fixture_content

