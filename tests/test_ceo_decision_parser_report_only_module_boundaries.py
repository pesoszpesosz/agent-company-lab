import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_ceo_decision_parser_report_only_facade_reexports_phase_modules():
    from agent_company_core import ceo_decision_parser_report_only as report_facade
    from agent_company_core import ceo_decision_parser_report_only_contract
    from agent_company_core import ceo_decision_parser_report_only_fixtures
    from agent_company_core import ceo_decision_parser_report_only_runner
    from agent_company_core import ceo_decisions

    assert (
        report_facade.write_ceo_decision_parser_preflight
        is ceo_decision_parser_report_only_contract.write_ceo_decision_parser_preflight
    )
    assert (
        report_facade.write_ceo_decision_parser_dry_run_contract
        is ceo_decision_parser_report_only_contract.write_ceo_decision_parser_dry_run_contract
    )

    assert (
        report_facade.write_ceo_decision_parser_positive_fixture
        is ceo_decision_parser_report_only_fixtures.write_ceo_decision_parser_positive_fixture
    )
    assert (
        report_facade.write_ceo_decision_parser_fixture_suite
        is ceo_decision_parser_report_only_fixtures.write_ceo_decision_parser_fixture_suite
    )

    assert (
        report_facade.write_ceo_decision_parser_report_only_harness
        is ceo_decision_parser_report_only_runner.write_ceo_decision_parser_report_only_harness
    )
    assert (
        report_facade.write_ceo_decision_parser_report_only_runner
        is ceo_decision_parser_report_only_runner.write_ceo_decision_parser_report_only_runner
    )
    assert (
        ceo_decisions.write_ceo_decision_parser_report_only_runner
        is report_facade.write_ceo_decision_parser_report_only_runner
    )
def test_ceo_decision_parser_report_only_runner_facade_reexports_runner_modules():
    from agent_company_core import ceo_decision_parser_report_only_harness
    from agent_company_core import ceo_decision_parser_report_only_run
    from agent_company_core import ceo_decision_parser_report_only_runner

    assert (
        ceo_decision_parser_report_only_runner.write_ceo_decision_parser_report_only_harness
        is ceo_decision_parser_report_only_harness.write_ceo_decision_parser_report_only_harness
    )
    assert (
        ceo_decision_parser_report_only_runner.write_ceo_decision_parser_report_only_runner
        is ceo_decision_parser_report_only_run.write_ceo_decision_parser_report_only_runner
    )
def test_ceo_decision_parser_report_only_contract_facade_reexports_contract_modules():
    from agent_company_core import ceo_decision_parser_report_only_contract
    from agent_company_core import ceo_decision_parser_report_only_dry_run_contract
    from agent_company_core import ceo_decision_parser_report_only_preflight

    assert (
        ceo_decision_parser_report_only_contract.write_ceo_decision_parser_preflight
        is ceo_decision_parser_report_only_preflight.write_ceo_decision_parser_preflight
    )
    assert (
        ceo_decision_parser_report_only_contract.write_ceo_decision_parser_dry_run_contract
        is ceo_decision_parser_report_only_dry_run_contract.write_ceo_decision_parser_dry_run_contract
    )

def test_ceo_decision_parser_report_only_fixtures_facade_reexports_fixture_modules():
    from agent_company_core import ceo_decision_parser_report_only_fixture_suite
    from agent_company_core import ceo_decision_parser_report_only_fixtures
    from agent_company_core import ceo_decision_parser_report_only_positive_fixture

    assert (
        ceo_decision_parser_report_only_fixtures.write_ceo_decision_parser_positive_fixture
        is ceo_decision_parser_report_only_positive_fixture.write_ceo_decision_parser_positive_fixture
    )
    assert (
        ceo_decision_parser_report_only_fixtures.write_ceo_decision_parser_fixture_suite
        is ceo_decision_parser_report_only_fixture_suite.write_ceo_decision_parser_fixture_suite
    )

def test_ceo_decision_parser_report_only_runner_content_evaluates_fixture_suite():
    from agent_company_core.ceo_decision_parser_report_only_runner_content import (
        build_report_only_parser_runner_content,
        parse_decision_intake,
    )

    negative_fixtures = [
        {
            "fixture_id": "missing-packet-id",
            "expected_accepted": False,
            "expected_rule_id": "reject_missing_packet_id",
            "submitted_intake": {
                "decision_packet_id": None,
                "selected_option_id": "approve_bounded_readonly_scope",
            },
        },
        {
            "fixture_id": "unknown-option",
            "expected_accepted": False,
            "expected_rule_id": "reject_unknown_option",
            "submitted_intake": {
                "decision_packet_id": "packet-1",
                "selected_option_id": "just_go_do_it",
            },
        },
    ]
    positive_fixture = {
        "fixture_id": "positive-readonly",
        "submitted_intake": {
            "decision_packet_id": "packet-1",
            "selected_option_id": "approve_bounded_readonly_scope",
            "approved_blocker_ids": ["req-1"],
            "allowed_action_scope": "Read-only public pages only. No payment, wallet, account settings, personal data, checkout, or listing changes.",
            "forbidden_actions_acknowledged": True,
            "expiration_or_review_time": "2026-06-16T23:59:59Z",
            "operator_confirmation_text": "approve this exact scope",
        },
        "expected_parser_result": {
            "accepted_for_dry_run": True,
            "expected_preview_state": "would_create_bounded_service_request_update",
        },
    }

    accepted = parse_decision_intake(positive_fixture["submitted_intake"])
    content = build_report_only_parser_runner_content(
        negative_fixtures=negative_fixtures,
        positive_fixture=positive_fixture,
        negative_fixture_total=6,
        positive_fixture_total=1,
    )

    assert accepted["accepted_for_dry_run"] is True
    assert accepted["preview_state"] == "would_create_bounded_service_request_update"
    assert content["fixture_suite_count"] == 7
    assert content["negative_fixture_count"] == 2
    assert content["positive_fixture_count"] == 1
    assert content["parser_execution_count"] == 3
    assert content["rejected_decision_count"] == 2
    assert content["accepted_dry_run_preview_count"] == 1
    assert content["expected_rejection_match_count"] == 2
    assert content["expected_preview_match_count"] == 1
    assert content["queue_mutation_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["parser_results"][-1]["matched_expected"] is True
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert "report-only" in content["boundary_text"]


