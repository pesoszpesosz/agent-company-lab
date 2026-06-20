from __future__ import annotations

from typing import Any


def build_migration_decision_intake_contract_content(
    *,
    generated_utc: str,
    json_output_path: str,
    validation_path: str,
    lane_id: str,
    intake_task_id: str,
    intake_evidence_id: str,
    source_review_task_id: str,
    source_review_evidence_id: str,
    accepted_decision_types: list[str],
) -> dict[str, Any]:
    local_decision = "agent_company_migration_decision_intake_contract_ready_for_report_only_fixture_suite"
    recommended_default = "build_report_only_fixture_suite_next_without_applying_operator_decision"
    required_fields = [
        "decision_id",
        "operator_name",
        "decision_type",
        "scope",
        "artifact_paths",
        "expires_at",
        "risk_acknowledgement",
        "signed_utc",
    ]
    positive_fixtures = [
        {
            "fixture_id": f"positive_{decision_type}",
            "decision_type": decision_type,
            "expected_state": "accepted_for_report_only_routing" if decision_type != "approve_sandbox_dry_run_only" else "accepted_for_sandbox_dry_run_preparation_only",
        }
        for decision_type in accepted_decision_types
    ]
    negative_fixtures = [
        {"fixture_id": "missing_decision_id", "reason": "decision_id is required"},
        {"fixture_id": "unknown_decision_type", "reason": "decision_type must be one of the review options"},
        {"fixture_id": "live_apply_scope", "reason": "live migration SQL apply is outside this contract"},
        {"fixture_id": "missing_artifact_paths", "reason": "artifact_paths must include review and validation artifacts"},
        {"fixture_id": "expired_decision", "reason": "expires_at must be in the future at parse time"},
        {"fixture_id": "unsigned_decision", "reason": "operator signature fields are required"},
        {"fixture_id": "gated_action_bundle", "reason": "browser/account/wallet/payment/public/security actions are forbidden"},
        {"fixture_id": "service_request_mutation", "reason": "service request mutation is forbidden by this intake"},
    ]
    parser_guards = [
        "parse_json_only_no_freeform_commands",
        "require_all_fields_present",
        "reject_unknown_decision_type",
        "reject_live_apply_scope",
        "reject_external_or_gated_action_requests",
        "require_artifact_paths_match_operator_review_packet",
        "require_expiration_and_signed_timestamp",
        "emit_report_only_routing_result",
        "never_apply_decision_inside_parser",
    ]
    output_states = [
        "accepted_hold",
        "accepted_sandbox_dry_run_preparation_only",
        "accepted_rework_request",
        "accepted_rejection_closeout",
    ]
    summary = "Prepared a report-only signed-decision intake contract for the migration operator review, including accepted decision types, required fields, fixtures, parser guards, and output states."
    next_action = "Build the report-only fixture suite next; do not parse or apply live operator decisions yet."
    runtime_boundary = {
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
    payload = {
        "schema_version": "agent_company.migration_decision_intake_contract.v1",
        "generated_utc": generated_utc,
        "intake_lane_id": lane_id,
        "intake_task_id": intake_task_id,
        "intake_evidence_id": intake_evidence_id,
        "source_review_task_id": source_review_task_id,
        "source_review_evidence_id": source_review_evidence_id,
        "decision_intake_contract_count": 1,
        "accepted_decision_type_count": len(accepted_decision_types),
        "required_field_count": len(required_fields),
        "positive_fixture_count": len(positive_fixtures),
        "negative_fixture_count": len(negative_fixtures),
        "parser_guard_count": len(parser_guards),
        "output_state_count": len(output_states),
        "accepted_decision_types": accepted_decision_types,
        "required_fields": required_fields,
        "positive_fixtures": positive_fixtures,
        "negative_fixtures": negative_fixtures,
        "parser_guards": parser_guards,
        "output_states": output_states,
        "local_decision": local_decision,
        "recommended_default": recommended_default,
        "summary": summary,
        "next_action": next_action,
        "runtime_boundary": runtime_boundary,
    }

    md_lines = [
        "# Agent Company Migration Decision Intake Contract",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Decision",
        "",
        f"`{local_decision}`",
        "",
        f"Recommended default: `{recommended_default}`",
        "",
        summary,
        "",
        "## Accepted Decision Types",
        "",
    ]
    md_lines.extend(f"- `{item}`" for item in accepted_decision_types)
    md_lines.extend(["", "## Required Fields", ""])
    md_lines.extend(f"- `{item}`" for item in required_fields)
    md_lines.extend(["", "## Parser Guards", ""])
    md_lines.extend(f"- `{item}`" for item in parser_guards)
    md_lines.extend(["", "## Positive Fixtures", ""])
    md_lines.extend(f"- `{item['fixture_id']}` -> `{item['expected_state']}`" for item in positive_fixtures)
    md_lines.extend(["", "## Negative Fixtures", ""])
    md_lines.extend(f"- `{item['fixture_id']}`: {item['reason']}" for item in negative_fixtures)
    md_lines.extend(["", "## Output States", ""])
    md_lines.extend(f"- `{item}`" for item in output_states)
    md_lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This contract is report-only. It does not parse live decisions, apply a decision, enable an apply command, execute SQL, create tables, start workers, assign service requests, call APIs, open browsers, register accounts, touch wallets or payments, spend money, post publicly, or perform security testing.",
            "",
            "## Next Action",
            "",
            next_action,
            "",
        ]
    )

    return {
        "accepted_decision_type_count": len(accepted_decision_types),
        "accepted_decision_types": accepted_decision_types,
        "decision_intake_contract_count": 1,
        "local_decision": local_decision,
        "markdown": "\n".join(md_lines) + "\n",
        "negative_fixture_count": len(negative_fixtures),
        "negative_fixtures": negative_fixtures,
        "next_action": next_action,
        "output_state_count": len(output_states),
        "output_states": output_states,
        "parser_guard_count": len(parser_guards),
        "parser_guards": parser_guards,
        "payload": payload,
        "positive_fixture_count": len(positive_fixtures),
        "positive_fixtures": positive_fixtures,
        "recommended_default": recommended_default,
        "required_field_count": len(required_fields),
        "required_fields": required_fields,
        "runtime_boundary": runtime_boundary,
        "summary": summary,
    }


__all__ = ["build_migration_decision_intake_contract_content"]
