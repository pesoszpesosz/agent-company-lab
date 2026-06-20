from __future__ import annotations

"""Compatibility facade for migration decision parser scaffold writers."""

from .agent_company_migration_parser_module_draft import write_agent_company_migration_decision_parser_module_draft
from .agent_company_migration_parser_scaffold_plan import write_agent_company_migration_decision_parser_scaffold

__all__ = [
    "write_agent_company_migration_decision_parser_scaffold",
    "write_agent_company_migration_decision_parser_module_draft",
]
