from __future__ import annotations

from typing import Any, Callable

"""CLI parser and dispatch helpers for agent-company migration commands."""

from agent_company_core.agent_company_migration import (
    write_agent_company_infrastructure_radar,
    write_agent_company_department_architecture_packet,
    write_agent_company_department_schema_plan,
    write_agent_company_report_only_migration_draft,
    write_agent_company_migration_apply_preflight,
    write_agent_company_migration_operator_review,
    write_agent_company_migration_decision_intake_contract,
    write_agent_company_migration_decision_fixture_suite,
    write_agent_company_migration_decision_fixture_runner,
    write_agent_company_migration_decision_parser_scaffold,
    write_agent_company_migration_decision_parser_module_draft,
    write_agent_company_migration_decision_module_fixture_checks,
    write_agent_company_migration_decision_parser_module_file_draft,
    write_agent_company_migration_decision_parser_static_review,
    write_agent_company_migration_decision_parser_install_preflight,
    write_agent_company_migration_decision_parser_install_review,
    write_agent_company_migration_decision_parser_install_decision_intake_contract,
    write_agent_company_migration_decision_parser_install_decision_fixture_suite,
    write_agent_company_migration_decision_parser_install_decision_runner,
    write_agent_company_migration_decision_parser_install_decision_runner_review,
    write_agent_company_migration_decision_parser_write_decision_intake_contract,
    write_agent_company_migration_decision_parser_write_decision_fixture_suite,
    write_agent_company_migration_decision_parser_write_decision_runner,
    write_agent_company_migration_decision_parser_write_decision_runner_review,
    write_agent_company_migration_decision_parser_write_approval_request,
    write_agent_company_migration_decision_parser_write_approval_response_intake_contract,
    write_agent_company_migration_decision_parser_write_approval_response_fixture_suite,
    write_agent_company_migration_decision_parser_write_approval_response_runner,
    write_agent_company_migration_decision_parser_write_approval_response_runner_review,
    write_agent_company_migration_decision_parser_write_approval_response_application_preflight,
    write_agent_company_migration_decision_parser_write_approval_response_application_packet_contract,
    write_agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite,
    write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner,
    write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review,
)
from agent_company_core.schema import init_db


AGENT_COMPANY_MIGRATION_CLI_COMMANDS = (
    "write-agent-company-infrastructure-radar",
    "write-agent-company-department-architecture-packet",
    "write-agent-company-department-schema-plan",
    "write-agent-company-report-only-migration-draft",
    "write-agent-company-migration-apply-preflight",
    "write-agent-company-migration-operator-review",
    "write-agent-company-migration-decision-intake-contract",
    "write-agent-company-migration-decision-fixture-suite",
    "write-agent-company-migration-decision-fixture-runner",
    "write-agent-company-migration-decision-parser-scaffold",
    "write-agent-company-migration-decision-parser-module-draft",
    "write-agent-company-migration-decision-module-fixture-checks",
    "write-agent-company-migration-decision-parser-module-file-draft",
    "write-agent-company-migration-decision-parser-static-review",
    "write-agent-company-migration-decision-parser-install-preflight",
    "write-agent-company-migration-decision-parser-install-review",
    "write-agent-company-migration-decision-parser-install-decision-intake-contract",
    "write-agent-company-migration-decision-parser-install-decision-fixture-suite",
    "write-agent-company-migration-decision-parser-install-decision-runner",
    "write-agent-company-migration-decision-parser-install-decision-runner-review",
    "write-agent-company-migration-decision-parser-write-decision-intake-contract",
    "write-agent-company-migration-decision-parser-write-decision-fixture-suite",
    "write-agent-company-migration-decision-parser-write-decision-runner",
    "write-agent-company-migration-decision-parser-write-decision-runner-review",
    "write-agent-company-migration-decision-parser-write-approval-request",
    "write-agent-company-migration-decision-parser-write-approval-response-intake-contract",
    "write-agent-company-migration-decision-parser-write-approval-response-fixture-suite",
    "write-agent-company-migration-decision-parser-write-approval-response-runner",
    "write-agent-company-migration-decision-parser-write-approval-response-runner-review",
    "write-agent-company-migration-decision-parser-write-approval-response-application-preflight",
    "write-agent-company-migration-decision-parser-write-approval-response-application-packet-contract",
    "write-agent-company-migration-decision-parser-write-approval-response-application-packet-fixture-suite",
    "write-agent-company-migration-decision-parser-write-approval-response-application-packet-runner",
    "write-agent-company-migration-decision-parser-write-approval-response-application-packet-runner-review",
)


def add_agent_company_migration_commands(sub: Any) -> None:
    agent_company_infrastructure_radar = sub.add_parser("write-agent-company-infrastructure-radar")
    agent_company_infrastructure_radar.add_argument("--path")
    agent_company_infrastructure_radar.add_argument("--json-path")
    agent_company_infrastructure_radar.add_argument("--validation-path")
    agent_company_department_architecture_packet = sub.add_parser("write-agent-company-department-architecture-packet")
    agent_company_department_architecture_packet.add_argument("--path")
    agent_company_department_architecture_packet.add_argument("--json-path")
    agent_company_department_architecture_packet.add_argument("--validation-path")
    agent_company_department_schema_plan = sub.add_parser("write-agent-company-department-schema-plan")
    agent_company_department_schema_plan.add_argument("--path")
    agent_company_department_schema_plan.add_argument("--json-path")
    agent_company_department_schema_plan.add_argument("--validation-path")
    agent_company_report_only_migration_draft = sub.add_parser("write-agent-company-report-only-migration-draft")
    agent_company_report_only_migration_draft.add_argument("--path")
    agent_company_report_only_migration_draft.add_argument("--json-path")
    agent_company_report_only_migration_draft.add_argument("--validation-path")
    agent_company_migration_apply_preflight = sub.add_parser("write-agent-company-migration-apply-preflight")
    agent_company_migration_apply_preflight.add_argument("--path")
    agent_company_migration_apply_preflight.add_argument("--json-path")
    agent_company_migration_apply_preflight.add_argument("--validation-path")
    agent_company_migration_operator_review = sub.add_parser("write-agent-company-migration-operator-review")
    agent_company_migration_operator_review.add_argument("--path")
    agent_company_migration_operator_review.add_argument("--json-path")
    agent_company_migration_operator_review.add_argument("--validation-path")
    agent_company_migration_decision_intake_contract = sub.add_parser("write-agent-company-migration-decision-intake-contract")
    agent_company_migration_decision_intake_contract.add_argument("--path")
    agent_company_migration_decision_intake_contract.add_argument("--json-path")
    agent_company_migration_decision_intake_contract.add_argument("--validation-path")
    agent_company_migration_decision_fixture_suite = sub.add_parser("write-agent-company-migration-decision-fixture-suite")
    agent_company_migration_decision_fixture_suite.add_argument("--path")
    agent_company_migration_decision_fixture_suite.add_argument("--json-path")
    agent_company_migration_decision_fixture_suite.add_argument("--validation-path")
    agent_company_migration_decision_fixture_runner = sub.add_parser("write-agent-company-migration-decision-fixture-runner")
    agent_company_migration_decision_fixture_runner.add_argument("--path")
    agent_company_migration_decision_fixture_runner.add_argument("--json-path")
    agent_company_migration_decision_fixture_runner.add_argument("--validation-path")
    agent_company_migration_decision_parser_scaffold = sub.add_parser("write-agent-company-migration-decision-parser-scaffold")
    agent_company_migration_decision_parser_scaffold.add_argument("--path")
    agent_company_migration_decision_parser_scaffold.add_argument("--json-path")
    agent_company_migration_decision_parser_scaffold.add_argument("--validation-path")
    agent_company_migration_decision_parser_module_draft = sub.add_parser("write-agent-company-migration-decision-parser-module-draft")
    agent_company_migration_decision_parser_module_draft.add_argument("--path")
    agent_company_migration_decision_parser_module_draft.add_argument("--json-path")
    agent_company_migration_decision_parser_module_draft.add_argument("--validation-path")
    agent_company_migration_decision_module_fixture_checks = sub.add_parser("write-agent-company-migration-decision-module-fixture-checks")
    agent_company_migration_decision_module_fixture_checks.add_argument("--path")
    agent_company_migration_decision_module_fixture_checks.add_argument("--json-path")
    agent_company_migration_decision_module_fixture_checks.add_argument("--validation-path")
    agent_company_migration_decision_parser_module_file_draft = sub.add_parser("write-agent-company-migration-decision-parser-module-file-draft")
    agent_company_migration_decision_parser_module_file_draft.add_argument("--path")
    agent_company_migration_decision_parser_module_file_draft.add_argument("--json-path")
    agent_company_migration_decision_parser_module_file_draft.add_argument("--validation-path")
    agent_company_migration_decision_parser_static_review = sub.add_parser("write-agent-company-migration-decision-parser-static-review")
    agent_company_migration_decision_parser_static_review.add_argument("--path")
    agent_company_migration_decision_parser_static_review.add_argument("--json-path")
    agent_company_migration_decision_parser_static_review.add_argument("--validation-path")
    agent_company_migration_decision_parser_install_preflight = sub.add_parser("write-agent-company-migration-decision-parser-install-preflight")
    agent_company_migration_decision_parser_install_preflight.add_argument("--path")
    agent_company_migration_decision_parser_install_preflight.add_argument("--json-path")
    agent_company_migration_decision_parser_install_preflight.add_argument("--validation-path")
    agent_company_migration_decision_parser_install_review = sub.add_parser("write-agent-company-migration-decision-parser-install-review")
    agent_company_migration_decision_parser_install_review.add_argument("--path")
    agent_company_migration_decision_parser_install_review.add_argument("--json-path")
    agent_company_migration_decision_parser_install_review.add_argument("--validation-path")
    agent_company_migration_decision_parser_install_decision_intake_contract = sub.add_parser("write-agent-company-migration-decision-parser-install-decision-intake-contract")
    agent_company_migration_decision_parser_install_decision_intake_contract.add_argument("--path")
    agent_company_migration_decision_parser_install_decision_intake_contract.add_argument("--json-path")
    agent_company_migration_decision_parser_install_decision_intake_contract.add_argument("--validation-path")
    agent_company_migration_decision_parser_install_decision_fixture_suite = sub.add_parser("write-agent-company-migration-decision-parser-install-decision-fixture-suite")
    agent_company_migration_decision_parser_install_decision_fixture_suite.add_argument("--path")
    agent_company_migration_decision_parser_install_decision_fixture_suite.add_argument("--json-path")
    agent_company_migration_decision_parser_install_decision_fixture_suite.add_argument("--validation-path")
    agent_company_migration_decision_parser_install_decision_runner = sub.add_parser("write-agent-company-migration-decision-parser-install-decision-runner")
    agent_company_migration_decision_parser_install_decision_runner.add_argument("--path")
    agent_company_migration_decision_parser_install_decision_runner.add_argument("--json-path")
    agent_company_migration_decision_parser_install_decision_runner.add_argument("--validation-path")
    agent_company_migration_decision_parser_install_decision_runner_review = sub.add_parser("write-agent-company-migration-decision-parser-install-decision-runner-review")
    agent_company_migration_decision_parser_install_decision_runner_review.add_argument("--path")
    agent_company_migration_decision_parser_install_decision_runner_review.add_argument("--json-path")
    agent_company_migration_decision_parser_install_decision_runner_review.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_decision_intake_contract = sub.add_parser("write-agent-company-migration-decision-parser-write-decision-intake-contract")
    agent_company_migration_decision_parser_write_decision_intake_contract.add_argument("--path")
    agent_company_migration_decision_parser_write_decision_intake_contract.add_argument("--json-path")
    agent_company_migration_decision_parser_write_decision_intake_contract.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_decision_fixture_suite = sub.add_parser("write-agent-company-migration-decision-parser-write-decision-fixture-suite")
    agent_company_migration_decision_parser_write_decision_fixture_suite.add_argument("--path")
    agent_company_migration_decision_parser_write_decision_fixture_suite.add_argument("--json-path")
    agent_company_migration_decision_parser_write_decision_fixture_suite.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_decision_runner = sub.add_parser("write-agent-company-migration-decision-parser-write-decision-runner")
    agent_company_migration_decision_parser_write_decision_runner.add_argument("--path")
    agent_company_migration_decision_parser_write_decision_runner.add_argument("--json-path")
    agent_company_migration_decision_parser_write_decision_runner.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_decision_runner_review = sub.add_parser("write-agent-company-migration-decision-parser-write-decision-runner-review")
    agent_company_migration_decision_parser_write_decision_runner_review.add_argument("--path")
    agent_company_migration_decision_parser_write_decision_runner_review.add_argument("--json-path")
    agent_company_migration_decision_parser_write_decision_runner_review.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_approval_request = sub.add_parser("write-agent-company-migration-decision-parser-write-approval-request")
    agent_company_migration_decision_parser_write_approval_request.add_argument("--path")
    agent_company_migration_decision_parser_write_approval_request.add_argument("--json-path")
    agent_company_migration_decision_parser_write_approval_request.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_approval_response_intake_contract = sub.add_parser("write-agent-company-migration-decision-parser-write-approval-response-intake-contract")
    agent_company_migration_decision_parser_write_approval_response_intake_contract.add_argument("--path")
    agent_company_migration_decision_parser_write_approval_response_intake_contract.add_argument("--json-path")
    agent_company_migration_decision_parser_write_approval_response_intake_contract.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_approval_response_fixture_suite = sub.add_parser("write-agent-company-migration-decision-parser-write-approval-response-fixture-suite")
    agent_company_migration_decision_parser_write_approval_response_fixture_suite.add_argument("--path")
    agent_company_migration_decision_parser_write_approval_response_fixture_suite.add_argument("--json-path")
    agent_company_migration_decision_parser_write_approval_response_fixture_suite.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_approval_response_runner = sub.add_parser("write-agent-company-migration-decision-parser-write-approval-response-runner")
    agent_company_migration_decision_parser_write_approval_response_runner.add_argument("--path")
    agent_company_migration_decision_parser_write_approval_response_runner.add_argument("--json-path")
    agent_company_migration_decision_parser_write_approval_response_runner.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_approval_response_runner_review = sub.add_parser("write-agent-company-migration-decision-parser-write-approval-response-runner-review")
    agent_company_migration_decision_parser_write_approval_response_runner_review.add_argument("--path")
    agent_company_migration_decision_parser_write_approval_response_runner_review.add_argument("--json-path")
    agent_company_migration_decision_parser_write_approval_response_runner_review.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_approval_response_application_preflight = sub.add_parser("write-agent-company-migration-decision-parser-write-approval-response-application-preflight")
    agent_company_migration_decision_parser_write_approval_response_application_preflight.add_argument("--path")
    agent_company_migration_decision_parser_write_approval_response_application_preflight.add_argument("--json-path")
    agent_company_migration_decision_parser_write_approval_response_application_preflight.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_approval_response_application_packet_contract = sub.add_parser("write-agent-company-migration-decision-parser-write-approval-response-application-packet-contract")
    agent_company_migration_decision_parser_write_approval_response_application_packet_contract.add_argument("--path")
    agent_company_migration_decision_parser_write_approval_response_application_packet_contract.add_argument("--json-path")
    agent_company_migration_decision_parser_write_approval_response_application_packet_contract.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite = sub.add_parser("write-agent-company-migration-decision-parser-write-approval-response-application-packet-fixture-suite")
    agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite.add_argument("--path")
    agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite.add_argument("--json-path")
    agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_approval_response_application_packet_runner = sub.add_parser("write-agent-company-migration-decision-parser-write-approval-response-application-packet-runner")
    agent_company_migration_decision_parser_write_approval_response_application_packet_runner.add_argument("--path")
    agent_company_migration_decision_parser_write_approval_response_application_packet_runner.add_argument("--json-path")
    agent_company_migration_decision_parser_write_approval_response_application_packet_runner.add_argument("--validation-path")
    agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review = sub.add_parser("write-agent-company-migration-decision-parser-write-approval-response-application-packet-runner-review")
    agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review.add_argument("--path")
    agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review.add_argument("--json-path")
    agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review.add_argument("--validation-path")


def agent_company_migration_command_handlers() -> dict[str, Callable[[Any, Any], None]]:
    return {
        "write-agent-company-infrastructure-radar": write_agent_company_infrastructure_radar,
        "write-agent-company-department-architecture-packet": write_agent_company_department_architecture_packet,
        "write-agent-company-department-schema-plan": write_agent_company_department_schema_plan,
        "write-agent-company-report-only-migration-draft": write_agent_company_report_only_migration_draft,
        "write-agent-company-migration-apply-preflight": write_agent_company_migration_apply_preflight,
        "write-agent-company-migration-operator-review": write_agent_company_migration_operator_review,
        "write-agent-company-migration-decision-intake-contract": write_agent_company_migration_decision_intake_contract,
        "write-agent-company-migration-decision-fixture-suite": write_agent_company_migration_decision_fixture_suite,
        "write-agent-company-migration-decision-fixture-runner": write_agent_company_migration_decision_fixture_runner,
        "write-agent-company-migration-decision-parser-scaffold": write_agent_company_migration_decision_parser_scaffold,
        "write-agent-company-migration-decision-parser-module-draft": write_agent_company_migration_decision_parser_module_draft,
        "write-agent-company-migration-decision-module-fixture-checks": write_agent_company_migration_decision_module_fixture_checks,
        "write-agent-company-migration-decision-parser-module-file-draft": write_agent_company_migration_decision_parser_module_file_draft,
        "write-agent-company-migration-decision-parser-static-review": write_agent_company_migration_decision_parser_static_review,
        "write-agent-company-migration-decision-parser-install-preflight": write_agent_company_migration_decision_parser_install_preflight,
        "write-agent-company-migration-decision-parser-install-review": write_agent_company_migration_decision_parser_install_review,
        "write-agent-company-migration-decision-parser-install-decision-intake-contract": write_agent_company_migration_decision_parser_install_decision_intake_contract,
        "write-agent-company-migration-decision-parser-install-decision-fixture-suite": write_agent_company_migration_decision_parser_install_decision_fixture_suite,
        "write-agent-company-migration-decision-parser-install-decision-runner": write_agent_company_migration_decision_parser_install_decision_runner,
        "write-agent-company-migration-decision-parser-install-decision-runner-review": write_agent_company_migration_decision_parser_install_decision_runner_review,
        "write-agent-company-migration-decision-parser-write-decision-intake-contract": write_agent_company_migration_decision_parser_write_decision_intake_contract,
        "write-agent-company-migration-decision-parser-write-decision-fixture-suite": write_agent_company_migration_decision_parser_write_decision_fixture_suite,
        "write-agent-company-migration-decision-parser-write-decision-runner": write_agent_company_migration_decision_parser_write_decision_runner,
        "write-agent-company-migration-decision-parser-write-decision-runner-review": write_agent_company_migration_decision_parser_write_decision_runner_review,
        "write-agent-company-migration-decision-parser-write-approval-request": write_agent_company_migration_decision_parser_write_approval_request,
        "write-agent-company-migration-decision-parser-write-approval-response-intake-contract": write_agent_company_migration_decision_parser_write_approval_response_intake_contract,
        "write-agent-company-migration-decision-parser-write-approval-response-fixture-suite": write_agent_company_migration_decision_parser_write_approval_response_fixture_suite,
        "write-agent-company-migration-decision-parser-write-approval-response-runner": write_agent_company_migration_decision_parser_write_approval_response_runner,
        "write-agent-company-migration-decision-parser-write-approval-response-runner-review": write_agent_company_migration_decision_parser_write_approval_response_runner_review,
        "write-agent-company-migration-decision-parser-write-approval-response-application-preflight": write_agent_company_migration_decision_parser_write_approval_response_application_preflight,
        "write-agent-company-migration-decision-parser-write-approval-response-application-packet-contract": write_agent_company_migration_decision_parser_write_approval_response_application_packet_contract,
        "write-agent-company-migration-decision-parser-write-approval-response-application-packet-fixture-suite": write_agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite,
        "write-agent-company-migration-decision-parser-write-approval-response-application-packet-runner": write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner,
        "write-agent-company-migration-decision-parser-write-approval-response-application-packet-runner-review": write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review,
    }


def handle_agent_company_migration_command(conn: Any, args: Any) -> bool:
    handler = agent_company_migration_command_handlers().get(args.cmd)
    if handler is None:
        return False
    init_db(conn)
    handler(conn, args)
    return True


__all__ = [
    "AGENT_COMPANY_MIGRATION_CLI_COMMANDS",
    "add_agent_company_migration_commands",
    "agent_company_migration_command_handlers",
    "handle_agent_company_migration_command",
]
