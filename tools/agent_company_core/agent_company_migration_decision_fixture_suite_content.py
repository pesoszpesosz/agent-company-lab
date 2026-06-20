from __future__ import annotations

from typing import Any


def build_migration_decision_fixture_suite_content(
    *,
    intake_payload: dict[str, Any],
    artifact_paths: list[str],
) -> dict[str, Any]:
    parser_guards = intake_payload.get("parser_guards", [])
    output_states = intake_payload.get("output_states", [])
    required_fields = intake_payload.get("required_fields", [])
    positive_fixtures = []
    for item in intake_payload.get("positive_fixtures", []):
        decision_type = item["decision_type"]
        positive_fixtures.append(
            {
                "fixture_id": item["fixture_id"],
                "expected": "accept",
                "expected_state": item["expected_state"],
                "submitted_intake": {
                    "decision_id": f"decision-{decision_type}-20260616",
                    "operator_name": "operator",
                    "decision_type": decision_type,
                    "scope": "report_only_or_sandbox_dry_run_preparation_only",
                    "artifact_paths": artifact_paths,
                    "expires_at": "2026-06-17T00:00:00Z",
                    "risk_acknowledgement": "No live apply, no external actions, no service request mutation.",
                    "signed_utc": "2026-06-16T00:00:00Z",
                },
            }
        )

    negative_fixtures = []
    for item in intake_payload.get("negative_fixtures", []):
        submitted_intake = {
            "decision_id": f"negative-{item['fixture_id']}-20260616",
            "operator_name": "operator",
            "decision_type": "hold",
            "scope": "report_only",
            "artifact_paths": artifact_paths,
            "expires_at": "2026-06-17T00:00:00Z",
            "risk_acknowledgement": "No live apply.",
            "signed_utc": "2026-06-16T00:00:00Z",
        }
        if item["fixture_id"] == "missing_decision_id":
            submitted_intake.pop("decision_id")
        elif item["fixture_id"] == "unknown_decision_type":
            submitted_intake["decision_type"] = "approve_live_apply"
        elif item["fixture_id"] == "live_apply_scope":
            submitted_intake["scope"] = "live_migration_sql_apply"
        elif item["fixture_id"] == "missing_artifact_paths":
            submitted_intake["artifact_paths"] = []
        elif item["fixture_id"] == "expired_decision":
            submitted_intake["expires_at"] = "2026-06-15T00:00:00Z"
        elif item["fixture_id"] == "unsigned_decision":
            submitted_intake.pop("signed_utc")
        elif item["fixture_id"] == "gated_action_bundle":
            submitted_intake["scope"] = "sandbox_dry_run_plus_wallet_and_browser_action"
        elif item["fixture_id"] == "service_request_mutation":
            submitted_intake["scope"] = "update_service_request_and_assign_worker"
        negative_fixtures.append(
            {
                "fixture_id": item["fixture_id"],
                "expected": "reject",
                "expected_reason": item["reason"],
                "submitted_intake": submitted_intake,
            }
        )

    fixtures = positive_fixtures + negative_fixtures
    summary = "Prepared a report-only fixture suite for the migration decision intake contract, with positive and negative submitted-intake cases and expected parser outcomes."
    next_action = "Build the report-only fixture runner next; do not parse live decisions or apply operator decisions."
    runtime_boundary = {
        "fixtures_executed": False,
        "operator_decision_applied": False,
        "migration_sql_executed": False,
        "apply_command_enabled": False,
        "tables_created": 0,
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
        "fixtures": fixtures,
        "positive_fixtures": positive_fixtures,
        "negative_fixtures": negative_fixtures,
        "fixture_suite_count": len(fixtures),
        "positive_fixture_count": len(positive_fixtures),
        "negative_fixture_count": len(negative_fixtures),
        "expected_accept_count": sum(1 for item in fixtures if item["expected"] == "accept"),
        "expected_reject_count": sum(1 for item in fixtures if item["expected"] == "reject"),
        "parser_guards": parser_guards,
        "output_states": output_states,
        "required_fields": required_fields,
        "parser_guard_count": len(parser_guards),
        "output_state_count": len(output_states),
        "required_field_count": len(required_fields),
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }


__all__ = ["build_migration_decision_fixture_suite_content"]
