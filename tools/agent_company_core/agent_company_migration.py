from __future__ import annotations

"""Compatibility facade for agent-company migration report writers."""

from .agent_company_migration_foundation import (
    write_agent_company_infrastructure_radar,
    write_agent_company_department_architecture_packet,
    write_agent_company_department_schema_plan,
    write_agent_company_report_only_migration_draft,
    write_agent_company_migration_apply_preflight,
    write_agent_company_migration_operator_review,
)

from .agent_company_migration_decision_contracts import (
    write_agent_company_migration_decision_intake_contract,
    write_agent_company_migration_decision_fixture_suite,
    write_agent_company_migration_decision_fixture_runner,
)

from .agent_company_migration_parser_module import (
    write_agent_company_migration_decision_parser_scaffold,
    write_agent_company_migration_decision_parser_module_draft,
    write_agent_company_migration_decision_module_fixture_checks,
    write_agent_company_migration_decision_parser_module_file_draft,
    write_agent_company_migration_decision_parser_static_review,
    write_agent_company_migration_decision_parser_install_preflight,
    write_agent_company_migration_decision_parser_install_review,
)

from .agent_company_migration_parser_install import (
    write_agent_company_migration_decision_parser_install_decision_intake_contract,
    write_agent_company_migration_decision_parser_install_decision_fixture_suite,
    write_agent_company_migration_decision_parser_install_decision_runner,
    write_agent_company_migration_decision_parser_install_decision_runner_review,
)

from .agent_company_migration_write_decision import (
    write_agent_company_migration_decision_parser_write_decision_intake_contract,
    write_agent_company_migration_decision_parser_write_decision_fixture_suite,
    write_agent_company_migration_decision_parser_write_decision_runner,
    write_agent_company_migration_decision_parser_write_decision_runner_review,
    write_agent_company_migration_decision_parser_write_approval_request,
)

from .agent_company_migration_write_approval_response import (
    write_agent_company_migration_decision_parser_write_approval_response_intake_contract,
    write_agent_company_migration_decision_parser_write_approval_response_fixture_suite,
    write_agent_company_migration_decision_parser_write_approval_response_runner,
    write_agent_company_migration_decision_parser_write_approval_response_runner_review,
)

from .agent_company_migration_write_application import (
    write_agent_company_migration_decision_parser_write_approval_response_application_preflight,
    write_agent_company_migration_decision_parser_write_approval_response_application_packet_contract,
    write_agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite,
    write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner,
    write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review,
)

__all__ = [
    "write_agent_company_infrastructure_radar",
    "write_agent_company_department_architecture_packet",
    "write_agent_company_department_schema_plan",
    "write_agent_company_report_only_migration_draft",
    "write_agent_company_migration_apply_preflight",
    "write_agent_company_migration_operator_review",
    "write_agent_company_migration_decision_intake_contract",
    "write_agent_company_migration_decision_fixture_suite",
    "write_agent_company_migration_decision_fixture_runner",
    "write_agent_company_migration_decision_parser_scaffold",
    "write_agent_company_migration_decision_parser_module_draft",
    "write_agent_company_migration_decision_module_fixture_checks",
    "write_agent_company_migration_decision_parser_module_file_draft",
    "write_agent_company_migration_decision_parser_static_review",
    "write_agent_company_migration_decision_parser_install_preflight",
    "write_agent_company_migration_decision_parser_install_review",
    "write_agent_company_migration_decision_parser_install_decision_intake_contract",
    "write_agent_company_migration_decision_parser_install_decision_fixture_suite",
    "write_agent_company_migration_decision_parser_install_decision_runner",
    "write_agent_company_migration_decision_parser_install_decision_runner_review",
    "write_agent_company_migration_decision_parser_write_decision_intake_contract",
    "write_agent_company_migration_decision_parser_write_decision_fixture_suite",
    "write_agent_company_migration_decision_parser_write_decision_runner",
    "write_agent_company_migration_decision_parser_write_decision_runner_review",
    "write_agent_company_migration_decision_parser_write_approval_request",
    "write_agent_company_migration_decision_parser_write_approval_response_intake_contract",
    "write_agent_company_migration_decision_parser_write_approval_response_fixture_suite",
    "write_agent_company_migration_decision_parser_write_approval_response_runner",
    "write_agent_company_migration_decision_parser_write_approval_response_runner_review",
    "write_agent_company_migration_decision_parser_write_approval_response_application_preflight",
    "write_agent_company_migration_decision_parser_write_approval_response_application_packet_contract",
    "write_agent_company_migration_decision_parser_write_approval_response_application_packet_fixture_suite",
    "write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner",
    "write_agent_company_migration_decision_parser_write_approval_response_application_packet_runner_review",
]
