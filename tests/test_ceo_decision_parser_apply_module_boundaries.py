import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_ceo_decision_parser_apply_facade_reexports_phase_modules() -> None:
    from agent_company_core import ceo_decision_parser_apply as apply_facade
    from agent_company_core import ceo_decision_parser_apply_fixtures
    from agent_company_core import ceo_decision_parser_apply_preflight
    from agent_company_core import ceo_decision_parser_apply_runners
    from agent_company_core import ceo_decisions

    assert (
        apply_facade.write_ceo_decision_parser_mutation_preflight
        is ceo_decision_parser_apply_preflight.write_ceo_decision_parser_mutation_preflight
    )
    assert (
        apply_facade.write_ceo_decision_parser_apply_negative_fixtures
        is ceo_decision_parser_apply_fixtures.write_ceo_decision_parser_apply_negative_fixtures
    )
    assert (
        apply_facade.write_ceo_decision_parser_apply_positive_fixture
        is ceo_decision_parser_apply_fixtures.write_ceo_decision_parser_apply_positive_fixture
    )
    assert (
        apply_facade.write_ceo_decision_parser_apply_guard_runner
        is ceo_decision_parser_apply_runners.write_ceo_decision_parser_apply_guard_runner
    )
    assert (
        apply_facade.write_ceo_decision_parser_apply_dry_runner
        is ceo_decision_parser_apply_runners.write_ceo_decision_parser_apply_dry_runner
    )
    assert (
        ceo_decisions.write_ceo_decision_parser_apply_dry_runner
        is apply_facade.write_ceo_decision_parser_apply_dry_runner
    )
def test_ceo_decision_parser_apply_fixture_facade_reexports_fixture_modules() -> None:
    from agent_company_core import ceo_decision_parser_apply_fixtures
    from agent_company_core import ceo_decision_parser_apply_negative_fixtures
    from agent_company_core import ceo_decision_parser_apply_positive_fixture

    assert (
        ceo_decision_parser_apply_fixtures.write_ceo_decision_parser_apply_negative_fixtures
        is ceo_decision_parser_apply_negative_fixtures.write_ceo_decision_parser_apply_negative_fixtures
    )
    assert (
        ceo_decision_parser_apply_fixtures.write_ceo_decision_parser_apply_positive_fixture
        is ceo_decision_parser_apply_positive_fixture.write_ceo_decision_parser_apply_positive_fixture
    )
def test_ceo_decision_parser_apply_runner_facade_reexports_runner_modules() -> None:
    from agent_company_core import ceo_decision_parser_apply_dry_runner
    from agent_company_core import ceo_decision_parser_apply_guard_runner
    from agent_company_core import ceo_decision_parser_apply_runners

    assert (
        ceo_decision_parser_apply_runners.write_ceo_decision_parser_apply_guard_runner
        is ceo_decision_parser_apply_guard_runner.write_ceo_decision_parser_apply_guard_runner
    )
    assert (
        ceo_decision_parser_apply_runners.write_ceo_decision_parser_apply_dry_runner
        is ceo_decision_parser_apply_dry_runner.write_ceo_decision_parser_apply_dry_runner
    )


def test_ceo_decision_parser_apply_evaluator_rejects_guard_scope_drift() -> None:
    from agent_company_core.ceo_decision_parser_apply_evaluator import evaluate_ceo_parser_apply_request

    result = evaluate_ceo_parser_apply_request(
        {
            "explicit_mutation_approval_text": "Read-only browser validation only.",
            "target_service_request_ids": ["req-1"],
            "max_update_count": 1,
            "service_request_status_snapshot_required": True,
            "forbidden_actions_acknowledged": True,
        }
    )

    assert result == {
        "accepted_apply": False,
        "rule_id": "reject_readonly_scope_not_mutation_approval",
    }


def test_ceo_decision_parser_apply_evaluator_accepts_positive_preview() -> None:
    from agent_company_core.ceo_decision_parser_apply_evaluator import evaluate_ceo_parser_positive_apply_preview

    expected_preview = {"request_id": "req-1", "would_update_count": 1, "applied": False}
    result = evaluate_ceo_parser_positive_apply_preview(
        {
            "explicit_mutation_approval_text": "I explicitly approve applying exactly one parser preview mutation, with no open browsers and no account/payment/public actions.",
            "target_service_request_ids": ["req-1"],
            "max_update_count": 1,
            "service_request_status_snapshot_required": True,
            "forbidden_actions_acknowledged": True,
        },
        expected_preview=expected_preview,
    )

    assert result["accepted_apply_preview"] is True
    assert result["rule_id"] is None
    assert result["preview_state"] == "would_update_single_service_request_approval_scope"
    assert result["target_service_request_ids"] == ["req-1"]
    assert result["preview_update"] is expected_preview

def test_ceo_decision_parser_apply_negative_fixture_content_builds_rejection_suite() -> None:
    from agent_company_core.ceo_decision_parser_apply_negative_fixture_content import (
        build_ceo_decision_parser_apply_negative_fixture_content,
    )

    content = build_ceo_decision_parser_apply_negative_fixture_content(
        preflight_packet={
            "decision_packet_id": "packet-1",
            "operator_confirmation_text": "Read-only browser validation only.",
        },
        runner_validation_path="reports/runner-validation.json",
    )

    assert content["negative_apply_fixture_count"] == 6
    assert content["expected_rejection_count"] == 6
    assert content["accepted_apply_count"] == 0
    assert content["required_apply_field_count"] == 7
    assert content["required_apply_fields"] == [
        "approval_packet_id",
        "explicit_mutation_approval_text",
        "target_service_request_ids",
        "max_update_count",
        "runner_validation_path",
        "service_request_status_snapshot_required",
        "forbidden_actions_acknowledged",
    ]
    assert [item["expected_rule_id"] for item in content["negative_apply_fixtures"]] == [
        "reject_missing_explicit_mutation_approval",
        "reject_readonly_scope_not_mutation_approval",
        "reject_missing_target_service_request_ids",
        "reject_unbounded_or_excessive_update_count",
        "reject_forbidden_action_requested",
        "reject_missing_service_request_status_snapshot",
    ]
    assert content["negative_apply_fixtures"][0]["submitted_apply"]["approval_packet_id"] == "packet-1"
    assert content["negative_apply_fixtures"][1]["submitted_apply"]["explicit_mutation_approval_text"] == "Read-only browser validation only."
    assert content["negative_apply_fixtures"][2]["submitted_apply"]["runner_validation_path"] == "reports/runner-validation.json"
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert "apply no mutation" in content["boundary_text"]



def test_ceo_decision_parser_mutation_preflight_content_builds_payload_and_markdown() -> None:
    from agent_company_core.ceo_decision_parser_apply_preflight_content import (
        build_ceo_decision_parser_mutation_preflight_content,
    )

    content = build_ceo_decision_parser_mutation_preflight_content(
        generated_utc="2026-06-19T21:15:00Z",
        json_output_path="reports/preflight.json",
        validation_path="reports/preflight.validation.json",
        lane_id="platform_engineering",
        preflight_task_id="task-preflight",
        preflight_evidence_id="evidence-preflight",
        source_runner_task_id="task-runner",
        source_runner_evidence_id="evidence-runner",
        source_runner_validation_path="reports/runner.validation.json",
        runner_payload={
            "parser_results": [
                {
                    "fixture_type": "positive",
                    "actual_accepted": True,
                    "actual_preview_state": "would_create_bounded_service_request_update",
                    "matched_expected": True,
                },
                {
                    "fixture_type": "negative",
                    "actual_accepted": False,
                    "actual_preview_state": "rejected",
                    "matched_expected": True,
                },
            ],
        },
        positive_fixture={
            "fixture_id": "positive-approval",
            "submitted_intake": {
                "decision_packet_id": "packet-1",
                "selected_option_id": "option-1",
                "approver_identity": "operator",
                "operator_confirmation_text": "Read-only browser validation only.",
                "allowed_action_scope": "read_only_validation",
                "approved_blocker_ids": ["blocker-a", "blocker-b"],
                "expiration_or_review_time": "2026-06-20T00:00:00Z",
                "forbidden_actions_acknowledged": True,
            },
        },
    )

    assert content["candidate_preview_count"] == 1
    assert content["required_approval_field_count"] == 8
    assert content["required_blocker_count"] == 2
    assert content["forbidden_action_count"] == 10
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["preflight_packet"]["candidate_fixture_id"] == "positive-approval"
    assert content["preflight_packet"]["candidate_preview_state"] == "would_create_bounded_service_request_update"
    assert content["preflight_packet"]["approved_blocker_ids"] == ["blocker-a", "blocker-b"]
    assert content["payload"]["schema_version"] == "agent_company.ceo_decision_parser_mutation_preflight.v1"
    assert content["payload"]["source_runner_validation_path"] == "reports/runner.validation.json"
    assert content["payload"]["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["api_calls"] is False
    assert "# CEO Decision Parser Mutation Preflight" in content["markdown"]
    assert "`decision_packet_id`" in content["markdown"]
    assert "This preflight applies nothing" in content["markdown"]

def test_ceo_decision_parser_apply_positive_fixture_content_builds_payload_and_markdown() -> None:
    from agent_company_core.ceo_decision_parser_apply_positive_fixture_content import (
        build_ceo_decision_parser_apply_positive_fixture_content,
    )

    content = build_ceo_decision_parser_apply_positive_fixture_content(
        generated_utc="2026-06-19T22:15:00Z",
        json_output_path="reports/positive-fixture.json",
        validation_path="reports/positive-fixture.validation.json",
        lane_id="platform_engineering",
        fixture_task_id="task-positive-fixture",
        fixture_evidence_id="evidence-positive-fixture",
        source_guard_runner_task_id="task-guard-runner",
        source_guard_runner_evidence_id="evidence-guard-runner",
        source_guard_runner_validation_path="reports/guard-runner.validation.json",
        preflight_packet={
            "decision_packet_id": "packet-1",
            "allowed_action_scope": "read_only_validation",
        },
        target_request_id="req-1",
        target_status_before="needs_review",
        target_approval_scope_before=None,
        target_decision_note_before=None,
    )

    assert content["positive_apply_fixture_count"] == 1
    assert content["expected_preview_update_count"] == 1
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["target_status_after"] == "needs_review"
    assert content["positive_apply_fixture"]["expected_real_mutation"] is False
    assert content["positive_apply_fixture"]["submitted_apply"]["approval_packet_id"] == "packet-1"
    assert content["positive_apply_fixture"]["submitted_apply"]["target_service_request_ids"] == ["req-1"]
    assert content["preview_update"] == {
        "request_id": "req-1",
        "field_updates": {
            "approval_scope": "read_only_validation",
            "decision_note": "parser_apply_dry_run_preview_only_no_mutation",
        },
        "status_before": "needs_review",
        "status_after": "needs_review",
        "approval_scope_before": None,
        "decision_note_before": None,
        "would_update_count": 1,
        "applied": False,
    }
    assert content["payload"]["schema_version"] == "agent_company.ceo_decision_parser_apply_positive_fixture.v1"
    assert content["payload"]["source_guard_runner_validation_path"] == "reports/guard-runner.validation.json"
    assert content["payload"]["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "# CEO Decision Parser Apply Positive Fixture" in content["markdown"]
    assert "Target request: `req-1`" in content["markdown"]
    assert "applies nothing" in content["markdown"]

def test_ceo_decision_parser_apply_dry_runner_content_builds_payload_and_markdown() -> None:
    from agent_company_core.ceo_decision_parser_apply_dry_runner_content import (
        build_ceo_decision_parser_apply_dry_runner_content,
    )

    expected_preview = {
        "request_id": "req-1",
        "would_update_count": 1,
        "applied": False,
    }
    positive_fixture = {
        "expected_preview_state": "would_update_single_service_request_approval_scope",
        "submitted_apply": {
            "explicit_mutation_approval_text": "I explicitly approve applying exactly one parser preview mutation, with no open browsers and no account/payment/public actions.",
            "target_service_request_ids": ["req-1"],
            "max_update_count": 1,
            "service_request_status_snapshot_required": True,
            "forbidden_actions_acknowledged": True,
        },
    }

    content = build_ceo_decision_parser_apply_dry_runner_content(
        generated_utc="2026-06-19T22:45:00Z",
        json_output_path="reports/apply-dry-runner.json",
        validation_path="reports/apply-dry-runner.validation.json",
        lane_id="platform_engineering",
        runner_task_id="task-runner",
        runner_evidence_id="evidence-runner",
        source_positive_fixture_task_id="task-positive-fixture",
        source_positive_fixture_evidence_id="evidence-positive-fixture",
        source_positive_fixture_validation_path="reports/positive-fixture.validation.json",
        positive_fixture=positive_fixture,
        expected_preview=expected_preview,
        target_request_id="req-1",
        target_status_before="needs_review",
    )

    assert content["positive_apply_fixture_count"] == 1
    assert content["apply_dry_run_execution_count"] == 1
    assert content["accepted_apply_preview_count"] == 1
    assert content["expected_preview_match_count"] == 1
    assert content["preview_update_count"] == 1
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["target_status_after"] == "needs_review"
    assert content["dry_run_result"]["accepted_apply_preview"] is True
    assert content["payload"]["schema_version"] == "agent_company.ceo_decision_parser_apply_dry_runner.v1"
    assert content["payload"]["source_positive_fixture_validation_path"] == "reports/positive-fixture.validation.json"
    assert content["payload"]["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "# CEO Decision Parser Apply Dry Runner" in content["markdown"]
    assert "Target request: `req-1`" in content["markdown"]
    assert "report-only" in content["markdown"]
