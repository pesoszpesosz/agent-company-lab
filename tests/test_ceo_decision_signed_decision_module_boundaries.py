import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_signed_decision_fixture_set_facade_reexports_negative_and_positive_modules() -> None:
    from agent_company_core import ceo_decision_signed_decision_fixture_sets
    from agent_company_core import ceo_decision_signed_decision_negative_fixtures
    from agent_company_core import ceo_decision_signed_decision_positive_fixture

    assert (
        ceo_decision_signed_decision_fixture_sets.write_ceo_decision_parser_apply_readiness_signed_decision_negative_fixtures
        is ceo_decision_signed_decision_negative_fixtures.write_ceo_decision_parser_apply_readiness_signed_decision_negative_fixtures
    )
    assert (
        ceo_decision_signed_decision_fixture_sets.write_ceo_decision_parser_apply_readiness_signed_decision_positive_fixture
        is ceo_decision_signed_decision_positive_fixture.write_ceo_decision_parser_apply_readiness_signed_decision_positive_fixture
    )


def test_signed_decision_runner_facade_reexports_guard_and_positive_modules() -> None:
    from agent_company_core import ceo_decision_signed_decision_guard_runner
    from agent_company_core import ceo_decision_signed_decision_positive_runner
    from agent_company_core import ceo_decision_signed_decision_runners

    assert (
        ceo_decision_signed_decision_runners.write_ceo_decision_parser_apply_readiness_signed_decision_guard_runner
        is ceo_decision_signed_decision_guard_runner.write_ceo_decision_parser_apply_readiness_signed_decision_guard_runner
    )
    assert (
        ceo_decision_signed_decision_runners.write_ceo_decision_parser_apply_readiness_signed_decision_positive_runner
        is ceo_decision_signed_decision_positive_runner.write_ceo_decision_parser_apply_readiness_signed_decision_positive_runner
    )


def test_signed_decision_facade_reexports_phase_modules() -> None:
    from agent_company_core import ceo_decision_signed_decision as signed_facade
    from agent_company_core import ceo_decision_signed_decision_fixture_sets
    from agent_company_core import ceo_decision_signed_decision_runners
    from agent_company_core import ceo_decisions

    assert (
        signed_facade.write_ceo_decision_parser_apply_readiness_signed_decision_negative_fixtures
        is ceo_decision_signed_decision_fixture_sets.write_ceo_decision_parser_apply_readiness_signed_decision_negative_fixtures
    )
    assert (
        signed_facade.write_ceo_decision_parser_apply_readiness_signed_decision_positive_fixture
        is ceo_decision_signed_decision_fixture_sets.write_ceo_decision_parser_apply_readiness_signed_decision_positive_fixture
    )
    assert (
        signed_facade.write_ceo_decision_parser_apply_readiness_signed_decision_guard_runner
        is ceo_decision_signed_decision_runners.write_ceo_decision_parser_apply_readiness_signed_decision_guard_runner
    )
    assert (
        signed_facade.write_ceo_decision_parser_apply_readiness_signed_decision_positive_runner
        is ceo_decision_signed_decision_runners.write_ceo_decision_parser_apply_readiness_signed_decision_positive_runner
    )
    assert (
        ceo_decisions.write_ceo_decision_parser_apply_readiness_signed_decision_positive_runner
        is signed_facade.write_ceo_decision_parser_apply_readiness_signed_decision_positive_runner
    )

def test_signed_decision_shared_evaluator_accepts_valid_preview_decision() -> None:
    from agent_company_core.ceo_decision_signed_decision_evaluator import evaluate_ceo_signed_decision

    template = {
        "target_request_id": "req-1",
        "approval_scope_text": "scope",
        "decision_note_text": "note",
        "rollback_snapshot_updated_at": "2026-06-19T00:00:00Z",
    }
    decision = {
        **template,
        "operator_signature": "fixture-signature",
        "approval_expires_utc": "2026-06-20T00:00:00Z",
        "confirms_no_external_side_effects": True,
        "confirms_no_worker_start": True,
        "confirms_no_account_payment_public_security_real_money_action": True,
        "rollback_plan_acknowledged": True,
    }

    result = evaluate_ceo_signed_decision(decision, template, include_preview_state=True)

    assert result["accepted_signed_decision"] is True
    assert result["preview_state"] == "signed_decision_valid_apply_still_disabled"
    assert result["real_mutation_allowed"] is False


def test_signed_decision_shared_evaluator_rejects_scope_drift() -> None:
    from agent_company_core.ceo_decision_signed_decision_evaluator import evaluate_ceo_signed_decision

    template = {
        "target_request_id": "req-1",
        "approval_scope_text": "scope",
        "decision_note_text": "note",
        "rollback_snapshot_updated_at": "2026-06-19T00:00:00Z",
    }
    decision = {
        **template,
        "approval_scope_text": "changed",
        "operator_signature": "fixture-signature",
        "approval_expires_utc": "2026-06-20T00:00:00Z",
        "confirms_no_external_side_effects": True,
        "confirms_no_worker_start": True,
        "confirms_no_account_payment_public_security_real_money_action": True,
        "rollback_plan_acknowledged": True,
    }

    result = evaluate_ceo_signed_decision(decision, template)

    assert result["accepted_signed_decision"] is False
    assert result["rule_id"] == "reject_approval_scope_text_mismatch"



def test_signed_decision_guard_runner_content_rejects_negative_fixtures_and_builds_artifacts() -> None:
    from agent_company_core.ceo_decision_signed_decision_guard_runner_content import (
        build_signed_decision_guard_runner_content,
    )

    decision_fields_template = {
        "target_request_id": "req-1",
        "approval_scope_text": "scope",
        "decision_note_text": "note",
        "rollback_snapshot_updated_at": "2026-06-19T00:00:00Z",
    }
    valid_decision = {
        **decision_fields_template,
        "operator_signature": "fixture-signature",
        "approval_expires_utc": "2026-06-20T00:00:00Z",
        "confirms_no_external_side_effects": True,
        "confirms_no_worker_start": True,
        "confirms_no_account_payment_public_security_real_money_action": True,
        "rollback_plan_acknowledged": True,
    }
    negative_fixtures = [
        {
            "fixture_id": "missing-signature",
            "submitted_signed_decision": {**valid_decision, "operator_signature": None},
            "expected_accepted": False,
            "expected_rule_id": "reject_missing_operator_signature",
        },
        {
            "fixture_id": "scope-drift",
            "submitted_signed_decision": {**valid_decision, "approval_scope_text": "changed"},
            "expected_accepted": False,
            "expected_rule_id": "reject_approval_scope_text_mismatch",
        },
    ]

    content = build_signed_decision_guard_runner_content(
        generated_utc="2026-06-20T00:00:00Z",
        json_output_path="reports/signed-decision-guard.json",
        validation_path="reports/signed-decision-guard.validation.json",
        source_fixtures_validation_path="reports/signed-decision-negative-fixtures.validation.json",
        lane_id="platform_engineering",
        runner_task_id="task-guard-runner",
        runner_evidence_id="evidence-guard-runner",
        source_fixtures_task_id="task-negative-fixtures",
        source_fixtures_evidence_id="evidence-negative-fixtures",
        signed_decision_fixtures=negative_fixtures,
        decision_fields_template=decision_fields_template,
        target_status_before="needs_review",
    )

    payload = content["payload"]
    markdown = content["markdown"]

    assert content["negative_signed_decision_fixture_count"] == 2
    assert content["signed_decision_guard_execution_count"] == 2
    assert content["rejected_signed_decision_count"] == 2
    assert content["accepted_signed_decision_count"] == 0
    assert content["expected_rejection_match_count"] == 2
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["target_status_after"] == "needs_review"
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert payload["schema_version"] == "agent_company.ceo_decision_parser_apply_readiness_signed_decision_guard_runner.v1"
    assert payload["source_fixtures_validation_path"] == "reports/signed-decision-negative-fixtures.validation.json"
    assert payload["signed_decision_guard_results"][0]["fixture_id"] == "missing-signature"
    assert "# CEO Decision Parser Apply Readiness Signed Decision Guard Runner" in markdown
    assert "missing-signature" in markdown
    assert "scope-drift" in markdown
    assert "This runner is report-only" in markdown
    assert markdown.endswith("\n")

def test_signed_decision_positive_runner_content_summarizes_preview_only_fixture() -> None:
    from agent_company_core.ceo_decision_signed_decision_positive_runner_content import (
        build_signed_decision_positive_runner_content,
    )

    decision_fields_template = {
        "target_request_id": "req-1",
        "approval_scope_text": "Approve local report-only update.",
        "decision_note_text": "Preview signed decision only.",
        "rollback_snapshot_updated_at": "2026-06-19T00:00:00Z",
    }
    submitted_signed_decision = {
        **decision_fields_template,
        "operator_signature": "fixture-signature",
        "approval_expires_utc": "2026-06-20T00:00:00Z",
        "confirms_no_external_side_effects": True,
        "confirms_no_worker_start": True,
        "confirms_no_account_payment_public_security_real_money_action": True,
        "rollback_plan_acknowledged": True,
    }
    positive_fixture = {
        "fixture_id": "positive-signed-decision",
        "submitted_signed_decision": submitted_signed_decision,
        "expected_accepted": True,
        "expected_preview_state": "signed_decision_valid_apply_still_disabled",
        "expected_real_mutation": False,
    }

    content = build_signed_decision_positive_runner_content(
        positive_fixture=positive_fixture,
        decision_fields_template=decision_fields_template,
        target_status_before="needs_review",
    )

    assert content["positive_signed_decision_fixture_count"] == 1
    assert content["signed_decision_positive_execution_count"] == 1
    assert content["accepted_signed_decision_count"] == 1
    assert content["rejected_signed_decision_count"] == 0
    assert content["expected_acceptance_match_count"] == 1
    assert content["preview_state_match_count"] == 1
    assert content["real_mutation_allowed_count"] == 0
    assert content["apply_command_enabled"] is False
    assert content["approval_granted_by_runner"] is False
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["target_status_after"] == "needs_review"
    assert content["signed_decision_positive_results"][0]["matched_expected"] is True
    assert content["runtime_boundary"]["service_requests_updated"] == 0



def test_signed_decision_positive_runner_artifacts_render_payload_and_markdown() -> None:
    from agent_company_core.ceo_decision_signed_decision_positive_runner_content import (
        build_signed_decision_positive_runner_artifacts,
        build_signed_decision_positive_runner_content,
    )

    decision_fields_template = {
        "target_request_id": "req-1",
        "approval_scope_text": "Approve local report-only update.",
        "decision_note_text": "Preview signed decision only.",
        "rollback_snapshot_updated_at": "2026-06-19T00:00:00Z",
    }
    submitted_signed_decision = {
        **decision_fields_template,
        "operator_signature": "fixture-signature",
        "approval_expires_utc": "2026-06-20T00:00:00Z",
        "confirms_no_external_side_effects": True,
        "confirms_no_worker_start": True,
        "confirms_no_account_payment_public_security_real_money_action": True,
        "rollback_plan_acknowledged": True,
    }
    positive_fixture = {
        "fixture_id": "positive-signed-decision",
        "submitted_signed_decision": submitted_signed_decision,
        "expected_accepted": True,
        "expected_preview_state": "signed_decision_valid_apply_still_disabled",
        "expected_real_mutation": False,
    }
    runner_content = build_signed_decision_positive_runner_content(
        positive_fixture=positive_fixture,
        decision_fields_template=decision_fields_template,
        target_status_before="needs_review",
    )

    artifacts = build_signed_decision_positive_runner_artifacts(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path="reports/signed-decision-positive-runner.json",
        validation_path="reports/signed-decision-positive-runner.validation.json",
        source_fixture_validation_path="reports/signed-decision-positive-fixture.validation.json",
        lane_id="platform_engineering",
        runner_task_id="task-positive-runner",
        runner_evidence_id="evidence-positive-runner",
        source_fixture_task_id="task-positive-fixture",
        source_fixture_evidence_id="evidence-positive-fixture",
        runner_content=runner_content,
    )

    payload = artifacts["payload"]
    markdown = artifacts["markdown"]

    assert payload["schema_version"] == "agent_company.ceo_decision_parser_apply_readiness_signed_decision_positive_runner.v1"
    assert payload["runner_lane_id"] == "platform_engineering"
    assert payload["source_fixture_validation_path"] == "reports/signed-decision-positive-fixture.validation.json"
    assert payload["positive_signed_decision_fixture_count"] == 1
    assert payload["signed_decision_positive_execution_count"] == 1
    assert payload["accepted_signed_decision_count"] == 1
    assert payload["apply_command_enabled"] is False
    assert payload["approval_granted_by_runner"] is False
    assert payload["target_status_after"] == "needs_review"
    assert payload["runtime_boundary"]["service_requests_updated"] == 0
    assert payload["signed_decision_positive_results"][0]["fixture_id"] == "positive-signed-decision"
    assert "# CEO Decision Parser Apply Readiness Signed Decision Positive Runner" in markdown
    assert "`ceo_decision_parser_apply_readiness_signed_decision_positive_runner_passed_preview_only`" in markdown
    assert "| `positive-signed-decision` | `True` | `signed_decision_valid_apply_still_disabled` | `False` | `True` |" in markdown
    assert "This runner is report-only" in markdown
    assert markdown.endswith("\n")

def test_signed_decision_positive_fixture_content_is_preview_only() -> None:
    from agent_company_core.ceo_decision_signed_decision_positive_fixture_content import (
        build_signed_decision_positive_fixture_content,
    )

    content = build_signed_decision_positive_fixture_content(
        decision_fields_template={
            "target_request_id": "req-1",
            "approval_scope_text": "scope",
            "decision_note_text": "note",
            "operator_signature": None,
            "signed_decision_utc": None,
            "approval_expires_utc": None,
            "rollback_snapshot_updated_at": "2026-06-19T00:00:00Z",
            "confirms_no_external_side_effects": None,
            "confirms_no_worker_start": None,
            "confirms_no_account_payment_public_security_real_money_action": None,
            "artifact_output_path": "reports/intake.json",
            "rollback_plan_acknowledged": None,
        },
        approval_statements=["a", "b", "c", "d", "e"],
        target_status_before="needs_review",
        generated_utc="2026-06-19T01:02:03Z",
    )

    fixture = content["positive_signed_decision_fixture"]
    submitted = fixture["submitted_signed_decision"]

    assert content["positive_signed_decision_fixture_count"] == 1
    assert content["expected_acceptance_count"] == 1
    assert content["decision_field_count"] == 12
    assert content["approval_statement_count"] == 5
    assert content["signed_decision_preview_only"] is True
    assert content["apply_command_enabled"] is False
    assert content["approval_granted_by_fixture"] is False
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["target_status_after"] == "needs_review"
    assert fixture["fixture_id"] == "valid-signed-decision-preview-only"
    assert fixture["expected_accepted"] is True
    assert fixture["expected_preview_state"] == "signed_decision_valid_apply_still_disabled"
    assert fixture["expected_real_mutation"] is False
    assert submitted["target_request_id"] == "req-1"
    assert submitted["operator_signature"] == "operator-approved-local-preview-fixture"
    assert submitted["signed_decision_utc"] == "2026-06-19T01:02:03Z"
    assert submitted["confirms_no_external_side_effects"] is True
    assert content["local_decision"] == "ceo_decision_parser_apply_readiness_signed_decision_positive_fixture_ready_preview_only"
    assert content["recommended_default"] == "positive_signed_decision_fixture_requires_separate_positive_runner"
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "granting no real approval" in content["summary"]




def test_signed_decision_negative_fixtures_content_builds_rejection_suite() -> None:
    from agent_company_core.ceo_decision_signed_decision_negative_fixture_content import (
        build_signed_decision_negative_fixtures_content,
    )

    content = build_signed_decision_negative_fixtures_content(
        decision_fields_template={
            "target_request_id": "req-1",
            "approval_scope_text": "scope",
            "decision_note_text": "note",
            "operator_signature": None,
            "signed_decision_utc": None,
            "approval_expires_utc": None,
            "rollback_snapshot_updated_at": "2026-06-19T00:00:00Z",
            "confirms_no_external_side_effects": None,
            "confirms_no_worker_start": None,
            "confirms_no_account_payment_public_security_real_money_action": None,
            "artifact_output_path": "reports/intake.json",
            "rollback_plan_acknowledged": None,
        },
        approval_statements=["a", "b", "c", "d", "e"],
        target_status_before="needs_review",
        generated_utc="2026-06-19T01:02:03Z",
    )

    fixtures = content["negative_signed_decision_fixtures"]

    assert content["negative_signed_decision_fixture_count"] == 6
    assert content["expected_rejection_count"] == 6
    assert content["decision_field_count"] == 12
    assert content["approval_statement_count"] == 5
    assert content["mutation_applied_count"] == 0
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["target_status_after"] == "needs_review"
    assert [fixture["fixture_id"] for fixture in fixtures] == [
        "missing-operator-signature",
        "wrong-target-request-id",
        "edited-approval-scope-text",
        "stale-rollback-snapshot",
        "missing-scope-expiration",
        "side-effect-confirmation-drift",
    ]
    assert {fixture["expected_rule_id"] for fixture in fixtures} == {
        "reject_missing_operator_signature",
        "reject_target_request_id_mismatch",
        "reject_approval_scope_text_mismatch",
        "reject_rollback_snapshot_mismatch",
        "reject_missing_scope_expiration",
        "reject_side_effect_confirmation_drift",
    }
    assert all(fixture["expected_accepted"] is False for fixture in fixtures)
    assert fixtures[0]["submitted_signed_decision"]["operator_signature"] is None
    assert fixtures[1]["submitted_signed_decision"]["target_request_id"] == "req-wrong-target"
    assert fixtures[5]["submitted_signed_decision"]["confirms_no_external_side_effects"] is False
    assert content["local_decision"] == "ceo_decision_parser_apply_readiness_signed_decision_negative_fixtures_ready"
    assert content["recommended_default"] == "run_signed_decision_guard_before_any_apply_command"
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "six local negative signed-decision fixtures" in content["summary"]


