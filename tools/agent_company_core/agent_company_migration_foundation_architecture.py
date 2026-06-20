from __future__ import annotations

"""Compatibility facade for agent-company migration foundation architecture writers."""

from .agent_company_migration_infrastructure_radar import write_agent_company_infrastructure_radar
from .agent_company_migration_department_architecture import write_agent_company_department_architecture_packet
from .agent_company_migration_department_schema import write_agent_company_department_schema_plan

__all__ = [
    "write_agent_company_infrastructure_radar",
    "write_agent_company_department_architecture_packet",
    "write_agent_company_department_schema_plan",
]
