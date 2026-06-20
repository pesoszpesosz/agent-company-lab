from __future__ import annotations

from typing import Any, Callable

"""CLI parser and dispatch helpers for CEO decision commands."""

from agent_company_core.ceo_decisions import (
    write_ceo_gate_blocker_board,
    write_ceo_blocker_triage,
    write_ceo_decision_packet_drafts,
    write_ceo_decision_intake_guard,
    write_ceo_decision_intake_negative_fixtures,
    write_ceo_decision_parser_preflight,
    write_ceo_decision_parser_dry_run_contract,
    write_ceo_decision_parser_positive_fixture,
    write_ceo_decision_parser_fixture_suite,
    write_ceo_decision_parser_report_only_harness,
    write_ceo_decision_parser_report_only_runner,
    write_ceo_decision_parser_mutation_preflight,
    write_ceo_decision_parser_apply_negative_fixtures,
    write_ceo_decision_parser_apply_guard_runner,
    write_ceo_decision_parser_apply_positive_fixture,
    write_ceo_decision_parser_apply_dry_runner,
    write_ceo_decision_parser_apply_readiness,
    write_ceo_decision_parser_apply_readiness_negative_fixtures,
    write_ceo_decision_parser_apply_readiness_guard_runner,
    write_ceo_decision_parser_apply_readiness_positive_fixture,
    write_ceo_decision_parser_apply_readiness_positive_runner,
    write_ceo_decision_parser_apply_readiness_operator_approval_packet,
    write_ceo_decision_parser_apply_readiness_no_approval_blocker,
    write_ceo_decision_parser_apply_readiness_decision_intake_packet,
    write_ceo_decision_parser_apply_readiness_signed_decision_negative_fixtures,
    write_ceo_decision_parser_apply_readiness_signed_decision_guard_runner,
    write_ceo_decision_parser_apply_readiness_signed_decision_positive_fixture,
    write_ceo_decision_parser_apply_readiness_signed_decision_positive_runner,
    write_ceo_decision_parser_apply_readiness_signed_decision_apply_preflight,
    write_ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet,
    write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract,
    write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures,
    write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner,
    write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture,
    write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner,
    write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout,
)
from agent_company_core.schema import init_db


CEO_DECISION_CLI_COMMANDS = (
    "write-ceo-gate-blocker-board",
    "write-ceo-blocker-triage",
    "write-ceo-decision-packet-drafts",
    "write-ceo-decision-intake-guard",
    "write-ceo-decision-intake-negative-fixtures",
    "write-ceo-decision-parser-preflight",
    "write-ceo-decision-parser-dry-run-contract",
    "write-ceo-decision-parser-positive-fixture",
    "write-ceo-decision-parser-fixture-suite",
    "write-ceo-decision-parser-report-only-harness",
    "write-ceo-decision-parser-report-only-runner",
    "write-ceo-decision-parser-mutation-preflight",
    "write-ceo-decision-parser-apply-negative-fixtures",
    "write-ceo-decision-parser-apply-guard-runner",
    "write-ceo-decision-parser-apply-positive-fixture",
    "write-ceo-decision-parser-apply-dry-runner",
    "write-ceo-decision-parser-apply-readiness",
    "write-ceo-decision-parser-apply-readiness-negative-fixtures",
    "write-ceo-decision-parser-apply-readiness-guard-runner",
    "write-ceo-decision-parser-apply-readiness-positive-fixture",
    "write-ceo-decision-parser-apply-readiness-positive-runner",
    "write-ceo-decision-parser-apply-readiness-operator-approval-packet",
    "write-ceo-decision-parser-apply-readiness-no-approval-blocker",
    "write-ceo-decision-parser-apply-readiness-decision-intake-packet",
    "write-ceo-decision-parser-apply-readiness-signed-decision-negative-fixtures",
    "write-ceo-decision-parser-apply-readiness-signed-decision-guard-runner",
    "write-ceo-decision-parser-apply-readiness-signed-decision-positive-fixture",
    "write-ceo-decision-parser-apply-readiness-signed-decision-positive-runner",
    "write-ceo-decision-parser-apply-readiness-signed-decision-apply-preflight",
    "write-ceo-decision-parser-apply-readiness-signed-decision-operator-apply-approval-packet",
    "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-contract",
    "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-negative-fixtures",
    "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-guard-runner",
    "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-positive-fixture",
    "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-positive-runner",
    "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-closeout",
)


def add_ceo_decision_commands(sub: Any) -> None:
    ceo_gate_blocker_board = sub.add_parser("write-ceo-gate-blocker-board")
    ceo_gate_blocker_board.add_argument("--path")
    ceo_gate_blocker_board.add_argument("--json-path")
    ceo_gate_blocker_board.add_argument("--validation-path")
    ceo_blocker_triage = sub.add_parser("write-ceo-blocker-triage")
    ceo_blocker_triage.add_argument("--path")
    ceo_blocker_triage.add_argument("--json-path")
    ceo_blocker_triage.add_argument("--validation-path")
    ceo_decision_packet_drafts = sub.add_parser("write-ceo-decision-packet-drafts")
    ceo_decision_packet_drafts.add_argument("--path")
    ceo_decision_packet_drafts.add_argument("--json-path")
    ceo_decision_packet_drafts.add_argument("--validation-path")
    ceo_decision_intake_guard = sub.add_parser("write-ceo-decision-intake-guard")
    ceo_decision_intake_guard.add_argument("--path")
    ceo_decision_intake_guard.add_argument("--json-path")
    ceo_decision_intake_guard.add_argument("--validation-path")
    ceo_decision_intake_negative_fixtures = sub.add_parser("write-ceo-decision-intake-negative-fixtures")
    ceo_decision_intake_negative_fixtures.add_argument("--path")
    ceo_decision_intake_negative_fixtures.add_argument("--json-path")
    ceo_decision_intake_negative_fixtures.add_argument("--validation-path")
    ceo_decision_parser_preflight = sub.add_parser("write-ceo-decision-parser-preflight")
    ceo_decision_parser_preflight.add_argument("--path")
    ceo_decision_parser_preflight.add_argument("--json-path")
    ceo_decision_parser_preflight.add_argument("--validation-path")
    ceo_decision_parser_dry_run_contract = sub.add_parser("write-ceo-decision-parser-dry-run-contract")
    ceo_decision_parser_dry_run_contract.add_argument("--path")
    ceo_decision_parser_dry_run_contract.add_argument("--json-path")
    ceo_decision_parser_dry_run_contract.add_argument("--validation-path")
    ceo_decision_parser_positive_fixture = sub.add_parser("write-ceo-decision-parser-positive-fixture")
    ceo_decision_parser_positive_fixture.add_argument("--path")
    ceo_decision_parser_positive_fixture.add_argument("--json-path")
    ceo_decision_parser_positive_fixture.add_argument("--validation-path")
    ceo_decision_parser_fixture_suite = sub.add_parser("write-ceo-decision-parser-fixture-suite")
    ceo_decision_parser_fixture_suite.add_argument("--path")
    ceo_decision_parser_fixture_suite.add_argument("--json-path")
    ceo_decision_parser_fixture_suite.add_argument("--validation-path")
    ceo_decision_parser_report_only_harness = sub.add_parser("write-ceo-decision-parser-report-only-harness")
    ceo_decision_parser_report_only_harness.add_argument("--path")
    ceo_decision_parser_report_only_harness.add_argument("--json-path")
    ceo_decision_parser_report_only_harness.add_argument("--validation-path")
    ceo_decision_parser_report_only_runner = sub.add_parser("write-ceo-decision-parser-report-only-runner")
    ceo_decision_parser_report_only_runner.add_argument("--path")
    ceo_decision_parser_report_only_runner.add_argument("--json-path")
    ceo_decision_parser_report_only_runner.add_argument("--validation-path")
    ceo_decision_parser_mutation_preflight = sub.add_parser("write-ceo-decision-parser-mutation-preflight")
    ceo_decision_parser_mutation_preflight.add_argument("--path")
    ceo_decision_parser_mutation_preflight.add_argument("--json-path")
    ceo_decision_parser_mutation_preflight.add_argument("--validation-path")
    ceo_decision_parser_apply_negative_fixtures = sub.add_parser("write-ceo-decision-parser-apply-negative-fixtures")
    ceo_decision_parser_apply_negative_fixtures.add_argument("--path")
    ceo_decision_parser_apply_negative_fixtures.add_argument("--json-path")
    ceo_decision_parser_apply_negative_fixtures.add_argument("--validation-path")
    ceo_decision_parser_apply_guard_runner = sub.add_parser("write-ceo-decision-parser-apply-guard-runner")
    ceo_decision_parser_apply_guard_runner.add_argument("--path")
    ceo_decision_parser_apply_guard_runner.add_argument("--json-path")
    ceo_decision_parser_apply_guard_runner.add_argument("--validation-path")
    ceo_decision_parser_apply_positive_fixture = sub.add_parser("write-ceo-decision-parser-apply-positive-fixture")
    ceo_decision_parser_apply_positive_fixture.add_argument("--path")
    ceo_decision_parser_apply_positive_fixture.add_argument("--json-path")
    ceo_decision_parser_apply_positive_fixture.add_argument("--validation-path")
    ceo_decision_parser_apply_dry_runner = sub.add_parser("write-ceo-decision-parser-apply-dry-runner")
    ceo_decision_parser_apply_dry_runner.add_argument("--path")
    ceo_decision_parser_apply_dry_runner.add_argument("--json-path")
    ceo_decision_parser_apply_dry_runner.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness = sub.add_parser("write-ceo-decision-parser-apply-readiness")
    ceo_decision_parser_apply_readiness.add_argument("--path")
    ceo_decision_parser_apply_readiness.add_argument("--json-path")
    ceo_decision_parser_apply_readiness.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_negative_fixtures = sub.add_parser("write-ceo-decision-parser-apply-readiness-negative-fixtures")
    ceo_decision_parser_apply_readiness_negative_fixtures.add_argument("--path")
    ceo_decision_parser_apply_readiness_negative_fixtures.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_negative_fixtures.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_guard_runner = sub.add_parser("write-ceo-decision-parser-apply-readiness-guard-runner")
    ceo_decision_parser_apply_readiness_guard_runner.add_argument("--path")
    ceo_decision_parser_apply_readiness_guard_runner.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_guard_runner.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_positive_fixture = sub.add_parser("write-ceo-decision-parser-apply-readiness-positive-fixture")
    ceo_decision_parser_apply_readiness_positive_fixture.add_argument("--path")
    ceo_decision_parser_apply_readiness_positive_fixture.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_positive_fixture.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_positive_runner = sub.add_parser("write-ceo-decision-parser-apply-readiness-positive-runner")
    ceo_decision_parser_apply_readiness_positive_runner.add_argument("--path")
    ceo_decision_parser_apply_readiness_positive_runner.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_positive_runner.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_operator_approval_packet = sub.add_parser("write-ceo-decision-parser-apply-readiness-operator-approval-packet")
    ceo_decision_parser_apply_readiness_operator_approval_packet.add_argument("--path")
    ceo_decision_parser_apply_readiness_operator_approval_packet.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_operator_approval_packet.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_no_approval_blocker = sub.add_parser("write-ceo-decision-parser-apply-readiness-no-approval-blocker")
    ceo_decision_parser_apply_readiness_no_approval_blocker.add_argument("--path")
    ceo_decision_parser_apply_readiness_no_approval_blocker.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_no_approval_blocker.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_decision_intake_packet = sub.add_parser("write-ceo-decision-parser-apply-readiness-decision-intake-packet")
    ceo_decision_parser_apply_readiness_decision_intake_packet.add_argument("--path")
    ceo_decision_parser_apply_readiness_decision_intake_packet.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_decision_intake_packet.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_signed_decision_negative_fixtures = sub.add_parser("write-ceo-decision-parser-apply-readiness-signed-decision-negative-fixtures")
    ceo_decision_parser_apply_readiness_signed_decision_negative_fixtures.add_argument("--path")
    ceo_decision_parser_apply_readiness_signed_decision_negative_fixtures.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_signed_decision_negative_fixtures.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_signed_decision_guard_runner = sub.add_parser("write-ceo-decision-parser-apply-readiness-signed-decision-guard-runner")
    ceo_decision_parser_apply_readiness_signed_decision_guard_runner.add_argument("--path")
    ceo_decision_parser_apply_readiness_signed_decision_guard_runner.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_signed_decision_guard_runner.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_signed_decision_positive_fixture = sub.add_parser("write-ceo-decision-parser-apply-readiness-signed-decision-positive-fixture")
    ceo_decision_parser_apply_readiness_signed_decision_positive_fixture.add_argument("--path")
    ceo_decision_parser_apply_readiness_signed_decision_positive_fixture.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_signed_decision_positive_fixture.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_signed_decision_positive_runner = sub.add_parser("write-ceo-decision-parser-apply-readiness-signed-decision-positive-runner")
    ceo_decision_parser_apply_readiness_signed_decision_positive_runner.add_argument("--path")
    ceo_decision_parser_apply_readiness_signed_decision_positive_runner.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_signed_decision_positive_runner.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_preflight = sub.add_parser("write-ceo-decision-parser-apply-readiness-signed-decision-apply-preflight")
    ceo_decision_parser_apply_readiness_signed_decision_apply_preflight.add_argument("--path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_preflight.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_preflight.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet = sub.add_parser("write-ceo-decision-parser-apply-readiness-signed-decision-operator-apply-approval-packet")
    ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet.add_argument("--path")
    ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract = sub.add_parser("write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-contract")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract.add_argument("--path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures = sub.add_parser("write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-negative-fixtures")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures.add_argument("--path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner = sub.add_parser("write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-guard-runner")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner.add_argument("--path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture = sub.add_parser("write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-positive-fixture")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture.add_argument("--path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner = sub.add_parser("write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-positive-runner")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner.add_argument("--path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner.add_argument("--validation-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout = sub.add_parser("write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-closeout")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout.add_argument("--path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout.add_argument("--json-path")
    ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout.add_argument("--validation-path")


def ceo_decision_command_handlers() -> dict[str, Callable[[Any, Any], None]]:
    return {
        "write-ceo-gate-blocker-board": write_ceo_gate_blocker_board,
        "write-ceo-blocker-triage": write_ceo_blocker_triage,
        "write-ceo-decision-packet-drafts": write_ceo_decision_packet_drafts,
        "write-ceo-decision-intake-guard": write_ceo_decision_intake_guard,
        "write-ceo-decision-intake-negative-fixtures": write_ceo_decision_intake_negative_fixtures,
        "write-ceo-decision-parser-preflight": write_ceo_decision_parser_preflight,
        "write-ceo-decision-parser-dry-run-contract": write_ceo_decision_parser_dry_run_contract,
        "write-ceo-decision-parser-positive-fixture": write_ceo_decision_parser_positive_fixture,
        "write-ceo-decision-parser-fixture-suite": write_ceo_decision_parser_fixture_suite,
        "write-ceo-decision-parser-report-only-harness": write_ceo_decision_parser_report_only_harness,
        "write-ceo-decision-parser-report-only-runner": write_ceo_decision_parser_report_only_runner,
        "write-ceo-decision-parser-mutation-preflight": write_ceo_decision_parser_mutation_preflight,
        "write-ceo-decision-parser-apply-negative-fixtures": write_ceo_decision_parser_apply_negative_fixtures,
        "write-ceo-decision-parser-apply-guard-runner": write_ceo_decision_parser_apply_guard_runner,
        "write-ceo-decision-parser-apply-positive-fixture": write_ceo_decision_parser_apply_positive_fixture,
        "write-ceo-decision-parser-apply-dry-runner": write_ceo_decision_parser_apply_dry_runner,
        "write-ceo-decision-parser-apply-readiness": write_ceo_decision_parser_apply_readiness,
        "write-ceo-decision-parser-apply-readiness-negative-fixtures": write_ceo_decision_parser_apply_readiness_negative_fixtures,
        "write-ceo-decision-parser-apply-readiness-guard-runner": write_ceo_decision_parser_apply_readiness_guard_runner,
        "write-ceo-decision-parser-apply-readiness-positive-fixture": write_ceo_decision_parser_apply_readiness_positive_fixture,
        "write-ceo-decision-parser-apply-readiness-positive-runner": write_ceo_decision_parser_apply_readiness_positive_runner,
        "write-ceo-decision-parser-apply-readiness-operator-approval-packet": write_ceo_decision_parser_apply_readiness_operator_approval_packet,
        "write-ceo-decision-parser-apply-readiness-no-approval-blocker": write_ceo_decision_parser_apply_readiness_no_approval_blocker,
        "write-ceo-decision-parser-apply-readiness-decision-intake-packet": write_ceo_decision_parser_apply_readiness_decision_intake_packet,
        "write-ceo-decision-parser-apply-readiness-signed-decision-negative-fixtures": write_ceo_decision_parser_apply_readiness_signed_decision_negative_fixtures,
        "write-ceo-decision-parser-apply-readiness-signed-decision-guard-runner": write_ceo_decision_parser_apply_readiness_signed_decision_guard_runner,
        "write-ceo-decision-parser-apply-readiness-signed-decision-positive-fixture": write_ceo_decision_parser_apply_readiness_signed_decision_positive_fixture,
        "write-ceo-decision-parser-apply-readiness-signed-decision-positive-runner": write_ceo_decision_parser_apply_readiness_signed_decision_positive_runner,
        "write-ceo-decision-parser-apply-readiness-signed-decision-apply-preflight": write_ceo_decision_parser_apply_readiness_signed_decision_apply_preflight,
        "write-ceo-decision-parser-apply-readiness-signed-decision-operator-apply-approval-packet": write_ceo_decision_parser_apply_readiness_signed_decision_operator_apply_approval_packet,
        "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-contract": write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_contract,
        "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-negative-fixtures": write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_negative_fixtures,
        "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-guard-runner": write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_guard_runner,
        "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-positive-fixture": write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_fixture,
        "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-positive-runner": write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_positive_runner,
        "write-ceo-decision-parser-apply-readiness-signed-decision-apply-command-closeout": write_ceo_decision_parser_apply_readiness_signed_decision_apply_command_closeout,
    }


def handle_ceo_decision_command(conn: Any, args: Any) -> bool:
    handler = ceo_decision_command_handlers().get(args.cmd)
    if handler is None:
        return False
    init_db(conn)
    handler(conn, args)
    return True


__all__ = [
    "CEO_DECISION_CLI_COMMANDS",
    "add_ceo_decision_commands",
    "ceo_decision_command_handlers",
    "handle_ceo_decision_command",
]
