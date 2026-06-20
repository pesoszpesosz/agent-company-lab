"""Pure content builders for signed apply-command negative fixtures."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .ceo_decision_signed_apply_command_evaluator import evaluate_signed_apply_command_negative_fixture


def build_signed_apply_command_negative_fixtures() -> list[dict[str, Any]]:
    return [
        {
            "fixture_id": "apply-command-reject-missing-operator-signature",
            "expected_rule_id": "reject_missing_operator_signature",
            "input_overrides": {"operator_signature": None},
            "expected_accepted": False,
        },
        {
            "fixture_id": "apply-command-reject-expired-approval",
            "expected_rule_id": "reject_expired_approval",
            "input_overrides": {"approval_expires_utc": "2026-01-01T00:00:00Z"},
            "expected_accepted": False,
        },
        {
            "fixture_id": "apply-command-reject-stale-target-snapshot",
            "expected_rule_id": "reject_stale_target_snapshot",
            "input_overrides": {"rollback_snapshot_updated_at": "2000-01-01T00:00:00Z"},
            "expected_accepted": False,
        },
        {
            "fixture_id": "apply-command-reject-wrong-target-request-id",
            "expected_rule_id": "reject_wrong_target_request_id",
            "input_overrides": {"target_request_id": "req-not-the-browser-readonly-target"},
            "expected_accepted": False,
        },
        {
            "fixture_id": "apply-command-reject-unapproved-field-set",
            "expected_rule_id": "reject_unapproved_field_set",
            "input_overrides": {"target_update_fields": ["approval_scope", "decision_note", "assigned_agent_id"]},
            "expected_accepted": False,
        },
        {
            "fixture_id": "apply-command-reject-missing-explicit-execution-flag",
            "expected_rule_id": "reject_missing_explicit_execution_flag",
            "input_overrides": {"explicit_apply_execution_flag": False},
            "expected_accepted": False,
        },
    ]


def build_signed_apply_command_negative_fixture_results(
    negative_fixtures: list[dict[str, Any]],
    *,
    target_request_id: str | None,
) -> list[dict[str, Any]]:
    fixture_results = []
    for item in negative_fixtures:
        result = evaluate_signed_apply_command_negative_fixture(item, target_request_id=target_request_id)
        fixture_results.append(
            {
                "fixture_id": item["fixture_id"],
                "expected_accepted": item["expected_accepted"],
                "expected_rule_id": item["expected_rule_id"],
                "execution_attempted": False,
                "actual_accepted": result["accepted"],
                "actual_rule_id": result["rule_id"],
                "matched_expected": (
                    result["accepted"] is item["expected_accepted"]
                    and result["rule_id"] == item["expected_rule_id"]
                    and result["real_mutation_allowed"] is False
                ),
            }
        )
    return fixture_results


def build_signed_apply_command_negative_fixtures_content(
    *,
    negative_fixtures: list[dict[str, Any]],
    target_request_id: str | None,
    target_status_before: str | None,
) -> dict[str, Any]:
    fixture_results = build_signed_apply_command_negative_fixture_results(
        negative_fixtures,
        target_request_id=target_request_id,
    )
    apply_command_execution_count = 0
    approval_granted_by_fixtures = False
    explicit_operator_apply_approval_present = False
    apply_command_enabled = False
    apply_execution_allowed = False
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    target_status_after = target_status_before
    fixture_summary = (
        "Created six local negative fixtures for the signed-decision apply command contract. Each fixture must be rejected before any future apply executor can mutate the target service request."
    )
    fixture_next_action = (
        "Build a report-only guard runner for these negative fixtures before implementing or enabling any apply command execution path."
    )
    runtime_boundary = {
        "browser_sessions_started": 0,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "security_testing_actions": False,
        "real_money_actions": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }

    return {
        "local_decision": "ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures_ready_no_mutation",
        "recommended_default": "reject_apply_command_inputs_until_explicit_operator_apply_approval_is_validated",
        "negative_fixtures": negative_fixtures,
        "fixture_results": fixture_results,
        "apply_command_negative_fixture_count": len(negative_fixtures),
        "expected_rejection_count": sum(1 for item in negative_fixtures if item.get("expected_accepted") is False),
        "unique_rejection_rule_count": len({item.get("expected_rule_id") for item in negative_fixtures}),
        "apply_command_execution_count": apply_command_execution_count,
        "approval_granted_by_fixtures": approval_granted_by_fixtures,
        "explicit_operator_apply_approval_present": explicit_operator_apply_approval_present,
        "apply_command_enabled": apply_command_enabled,
        "apply_execution_allowed": apply_execution_allowed,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "target_request_id": target_request_id,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
        "summary": fixture_summary,
        "next_action": fixture_next_action,
        "runtime_boundary": runtime_boundary,
    }


def build_signed_apply_command_negative_fixture_artifacts(
    *,
    generated_utc: str,
    json_output_path: Path,
    validation_path: Path,
    fixture_lane_id: str,
    fixture_task_id: str,
    fixture_evidence_id: str,
    source_contract_task_id: str,
    source_contract_evidence_id: str,
    source_contract_validation_path: Path,
    fixture_content: dict[str, Any],
) -> dict[str, Any]:
    payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures.v1",
        "generated_utc": generated_utc,
        "fixture_lane_id": fixture_lane_id,
        "fixture_task_id": fixture_task_id,
        "fixture_evidence_id": fixture_evidence_id,
        "source_contract_task_id": source_contract_task_id,
        "source_contract_evidence_id": source_contract_evidence_id,
        "source_contract_validation_path": str(source_contract_validation_path),
        "apply_command_negative_fixture_count": fixture_content["apply_command_negative_fixture_count"],
        "expected_rejection_count": fixture_content["expected_rejection_count"],
        "unique_rejection_rule_count": fixture_content["unique_rejection_rule_count"],
        "apply_command_execution_count": fixture_content["apply_command_execution_count"],
        "negative_fixtures": fixture_content["negative_fixtures"],
        "fixture_results": fixture_content["fixture_results"],
        "approval_granted_by_fixtures": fixture_content["approval_granted_by_fixtures"],
        "explicit_operator_apply_approval_present": fixture_content["explicit_operator_apply_approval_present"],
        "apply_command_enabled": fixture_content["apply_command_enabled"],
        "apply_execution_allowed": fixture_content["apply_execution_allowed"],
        "mutation_applied_count": fixture_content["mutation_applied_count"],
        "queue_mutation_count": fixture_content["queue_mutation_count"],
        "approval_request_count": fixture_content["approval_request_count"],
        "target_request_id": fixture_content["target_request_id"],
        "target_status_before": fixture_content["target_status_before"],
        "target_status_after": fixture_content["target_status_after"],
        "local_decision": fixture_content["local_decision"],
        "recommended_default": fixture_content["recommended_default"],
        "summary": fixture_content["summary"],
        "next_action": fixture_content["next_action"],
        "runtime_boundary": fixture_content["runtime_boundary"],
    }
    md_lines = [
        "# CEO Decision Parser Apply Readiness Signed Decision Apply Command Negative Fixtures",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{fixture_content['local_decision']}`",
        "",
        fixture_content["summary"],
        "",
        "## Fixtures",
        "",
        "| Fixture | Expected Rule | Execution Attempted |",
        "| --- | --- | ---: |",
    ]
    for item in fixture_content["fixture_results"]:
        md_lines.append(f"| `{item['fixture_id']}` | `{item['expected_rule_id']}` | `{item['execution_attempted']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "These are local rejection fixtures only. They do not grant approval, enable apply, mutate service requests, assign work, start workers, call APIs, open browsers, publish, touch accounts, wallets, payments, security testing, or real money.",
            "",
            "## Next Action",
            "",
            fixture_content["next_action"],
            "",
        ]
    )
    return {"payload": payload, "markdown": "\n".join(md_lines) + "\n"}


__all__ = [
    "build_signed_apply_command_negative_fixture_artifacts",
    "build_signed_apply_command_negative_fixture_results",
    "build_signed_apply_command_negative_fixtures_content",
    "build_signed_apply_command_negative_fixtures",
]


