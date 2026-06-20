from __future__ import annotations

from typing import Any


def build_ceo_apply_readiness_negative_fixture_content(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    source_readiness_validation_path: str,
    lane_id: str,
    fixture_task_id: str,
    fixture_evidence_id: str,
    source_readiness_task_id: str,
    source_readiness_evidence_id: str,
    readiness_packet: dict[str, Any],
) -> dict[str, Any]:
    local_decision = "ceo_decision_parser_apply_readiness_negative_fixtures_ready"
    recommended_default = "reject_apply_readiness_when_packet_or_target_state_drifts"
    accepted_readiness_count = 0
    mutation_applied_count = 0
    queue_mutation_count = 0
    approval_request_count = 0
    update_shape = readiness_packet.get("planned_update_sql_shape", {})
    rollback_snapshot = readiness_packet.get("rollback_snapshot", {})
    planned_updates = readiness_packet.get("planned_field_updates", {})
    required_readiness_fields = [
        "target_request_id",
        "planned_field_updates",
        "planned_update_sql_shape",
        "rollback_snapshot",
        "rollback_checks",
        "required_operator_approvals",
    ]
    negative_readiness_fixtures = [
        {
            "fixture_id": "missing-operator-approvals",
            "expected_accepted": False,
            "expected_rule_id": "reject_missing_operator_approval_bundle",
            "submitted_readiness": {
                **readiness_packet,
                "required_operator_approvals": [],
            },
        },
        {
            "fixture_id": "stale-rollback-snapshot",
            "expected_accepted": False,
            "expected_rule_id": "reject_stale_rollback_snapshot",
            "submitted_readiness": {
                **readiness_packet,
                "rollback_snapshot": {**rollback_snapshot, "updated_at": "2000-01-01T00:00:00Z"},
            },
        },
        {
            "fixture_id": "target-status-drift",
            "expected_accepted": False,
            "expected_rule_id": "reject_target_status_drift",
            "submitted_readiness": {
                **readiness_packet,
                "target_status_before": "complete",
            },
        },
        {
            "fixture_id": "planned-field-drift",
            "expected_accepted": False,
            "expected_rule_id": "reject_planned_field_drift",
            "submitted_readiness": {
                **readiness_packet,
                "planned_field_updates": {**planned_updates, "status": "complete"},
            },
        },
        {
            "fixture_id": "unbounded-update-shape",
            "expected_accepted": False,
            "expected_rule_id": "reject_unbounded_update_shape",
            "submitted_readiness": {
                **readiness_packet,
                "planned_update_sql_shape": {**update_shape, "max_rows": 99},
            },
        },
        {
            "fixture_id": "side-effect-boundary-open",
            "expected_accepted": False,
            "expected_rule_id": "reject_side_effect_boundary_open",
            "submitted_readiness": {
                **readiness_packet,
                "apply_boundary": {
                    **(readiness_packet.get("apply_boundary", {})),
                    "worker_starts": 1,
                    "external_side_effects": True,
                },
            },
        },
    ]
    negative_readiness_fixture_count = len(negative_readiness_fixtures)
    expected_rejection_count = sum(1 for fixture in negative_readiness_fixtures if fixture.get("expected_accepted") is False)
    required_readiness_field_count = len(required_readiness_fields)
    fixture_summary = (
        "Created local negative fixtures for the apply-readiness gate, covering missing operator approvals, stale rollback snapshot, target status drift, planned field drift, unbounded update shape, and open side-effect boundary."
    )
    fixture_next_action = (
        "Use these fixtures before any apply-readiness runner or apply command; every drifted or underspecified readiness packet must be rejected before DB mutation is possible."
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
    payload = {
        "schema_version": "agent_company.ceo_decision_parser_apply_readiness_negative_fixtures.v1",
        "generated_utc": generated_utc,
        "fixture_lane_id": lane_id,
        "fixture_task_id": fixture_task_id,
        "fixture_evidence_id": fixture_evidence_id,
        "source_readiness_task_id": source_readiness_task_id,
        "source_readiness_evidence_id": source_readiness_evidence_id,
        "source_readiness_validation_path": source_readiness_validation_path,
        "negative_readiness_fixture_count": negative_readiness_fixture_count,
        "expected_rejection_count": expected_rejection_count,
        "accepted_readiness_count": accepted_readiness_count,
        "required_readiness_field_count": required_readiness_field_count,
        "required_readiness_fields": required_readiness_fields,
        "negative_readiness_fixtures": negative_readiness_fixtures,
        "mutation_applied_count": mutation_applied_count,
        "queue_mutation_count": queue_mutation_count,
        "approval_request_count": approval_request_count,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": fixture_summary,
        "next_action": fixture_next_action,
        "runtime_boundary": runtime_boundary,
    }
    md_lines = [
        "# CEO Decision Parser Apply Readiness Negative Fixtures",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        fixture_summary,
        "",
        "## Fixtures",
        "",
        "| Fixture | Expected Rule |",
        "| --- | --- |",
    ]
    for fixture in negative_readiness_fixtures:
        md_lines.append(f"| `{fixture['fixture_id']}` | `{fixture['expected_rule_id']}` |")
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "These are local negative fixtures only. They apply no mutation, update no service request, request no approval, start no worker, call no API, open no browser, and perform no account, wallet, payment, public, security-testing, external, or real-money action.",
            "",
            "## Next Action",
            "",
            fixture_next_action,
            "",
        ]
    )
    return {
        "accepted_readiness_count": accepted_readiness_count,
        "approval_request_count": approval_request_count,
        "expected_rejection_count": expected_rejection_count,
        "local_decision": local_decision,
        "markdown": "\n".join(md_lines) + "\n",
        "mutation_applied_count": mutation_applied_count,
        "negative_readiness_fixture_count": negative_readiness_fixture_count,
        "negative_readiness_fixtures": negative_readiness_fixtures,
        "next_action": fixture_next_action,
        "payload": payload,
        "queue_mutation_count": queue_mutation_count,
        "recommended_default": recommended_default,
        "required_readiness_field_count": required_readiness_field_count,
        "required_readiness_fields": required_readiness_fields,
        "runtime_boundary": runtime_boundary,
        "summary": fixture_summary,
    }


__all__ = ["build_ceo_apply_readiness_negative_fixture_content"]
