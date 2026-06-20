from __future__ import annotations

"""Compatibility facade for parser write-decision contract phases."""

from .agent_company_migration_write_decision_fixture_suite import (
    write_agent_company_migration_decision_parser_write_decision_fixture_suite,
)
from .agent_company_migration_write_decision_intake_contract import (
    write_agent_company_migration_decision_parser_write_decision_intake_contract,
)

__all__ = [
    "write_agent_company_migration_decision_parser_write_decision_intake_contract",
    "write_agent_company_migration_decision_parser_write_decision_fixture_suite",
]