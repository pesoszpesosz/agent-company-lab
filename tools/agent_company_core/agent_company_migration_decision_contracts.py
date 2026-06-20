from __future__ import annotations

"""Compatibility facade for agent-company migration decision contract writers."""

from .agent_company_migration_decision_intake_contract import write_agent_company_migration_decision_intake_contract
from .agent_company_migration_decision_fixture_suite import write_agent_company_migration_decision_fixture_suite
from .agent_company_migration_decision_fixture_runner import write_agent_company_migration_decision_fixture_runner

__all__ = [
    "write_agent_company_migration_decision_intake_contract",
    "write_agent_company_migration_decision_fixture_suite",
    "write_agent_company_migration_decision_fixture_runner",
]
