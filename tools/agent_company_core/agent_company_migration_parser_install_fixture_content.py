from __future__ import annotations

from typing import Any


def build_parser_install_fixture_suite_content(source_intake_payload: dict[str, Any]) -> dict[str, Any]:
    accepted_install_decision_types = source_intake_payload.get("accepted_install_decision_types", [])
    required_fields = source_intake_payload.get("required_fields", [])
    parser_guards = source_intake_payload.get("parser_guards", [])
    output_states = source_intake_payload.get("output_states", [])
    expected_target_path = source_intake_payload.get("expected_target_path")
    expected_source_artifact_path = source_intake_payload.get("expected_source_artifact_path")
    positive_fixtures = [
        {
            "fixture_id": item["fixture"],
            "kind": "positive",
            "decision": {
                "decision_id": f"fixture-{item['decision_type']}-20260616",
                "operator_name": "fixture_operator",
                "decision_type": item["decision_type"],
                "target_path": expected_target_path,
                "source_artifact_path": expected_source_artifact_path,
                "expires_at": "2026-06-17T00:00:00Z",
                "risk_acknowledgement": "report_only_fixture_no_install_decision_applied",
                "signed_utc": "2026-06-16T00:00:00Z",
            },
            "expected_valid": True,
            "expected_state": item["expected_state"],
            "assertion": "accepted decision type maps to the declared report-only output state",
        }
        for item in source_intake_payload.get("positive_fixtures", [])
    ]
    negative_fixture_specs = [
        ("missing_decision_id", {"decision_id": None}, "guard_required_fields_present"),
        ("unknown_decision_type", {"decision_type": "approve_import_and_live_parse"}, "guard_known_install_decision_type"),
        ("target_path_changed", {"target_path": "E:\\agent-company-lab\\tools\\unexpected_parser.py"}, "guard_target_path_matches_preflight"),
        ("missing_source_artifact", {"source_artifact_path": None}, "guard_source_artifact_matches_preflight"),
        ("expired_decision", {"expires_at": "2026-06-15T00:00:00Z"}, "guard_not_expired"),
        ("unsigned_decision", {"signed_utc": None}, "guard_signed_timestamp_present"),
        ("bundled_live_parse_permission", {"risk_acknowledgement": "also_allows_import_and_live_parse"}, "guard_no_import_or_live_parse_permission"),
    ]
    base_negative_decision = {
        "decision_id": "fixture-negative-base-20260616",
        "operator_name": "fixture_operator",
        "decision_type": "approve_one_file_write_only",
        "target_path": expected_target_path,
        "source_artifact_path": expected_source_artifact_path,
        "expires_at": "2026-06-17T00:00:00Z",
        "risk_acknowledgement": "report_only_fixture_no_install_decision_applied",
        "signed_utc": "2026-06-16T00:00:00Z",
    }
    negative_fixtures = []
    for fixture_id, overrides, expected_guard in negative_fixture_specs:
        decision = dict(base_negative_decision)
        decision.update(overrides)
        negative_fixtures.append(
            {
                "fixture_id": fixture_id,
                "kind": "negative",
                "decision": decision,
                "expected_valid": False,
                "expected_state": "rejected_fixture_input",
                "expected_guard": expected_guard,
                "assertion": f"{fixture_id} is rejected by {expected_guard}",
            }
        )
    fixtures = positive_fixtures + negative_fixtures

    return {
        "accepted_install_decision_types": accepted_install_decision_types,
        "required_fields": required_fields,
        "parser_guards": parser_guards,
        "output_states": output_states,
        "expected_target_path": expected_target_path,
        "expected_source_artifact_path": expected_source_artifact_path,
        "fixtures": fixtures,
        "install_decision_fixture_suite_count": len(fixtures),
        "positive_fixture_count": len(positive_fixtures),
        "negative_fixture_count": len(negative_fixtures),
        "required_field_count": len(required_fields),
        "parser_guard_count": len(parser_guards),
        "output_state_count": len(output_states),
        "fixture_assertion_count": sum(1 for item in fixtures if item.get("assertion")),
    }


__all__ = ["build_parser_install_fixture_suite_content"]
