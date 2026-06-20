from __future__ import annotations

"""Compatibility facade for migration foundation writers."""

from .agent_company_migration_foundation_architecture import (
    write_agent_company_infrastructure_radar,
    write_agent_company_department_architecture_packet,
    write_agent_company_department_schema_plan,
)

from .agent_company_migration_foundation_review import (
    write_agent_company_report_only_migration_draft,
    write_agent_company_migration_apply_preflight,
    write_agent_company_migration_operator_review,
)

__all__ = [
    "write_agent_company_infrastructure_radar",
    "write_agent_company_department_architecture_packet",
    "write_agent_company_department_schema_plan",
    "write_agent_company_report_only_migration_draft",
    "write_agent_company_migration_apply_preflight",
    "write_agent_company_migration_operator_review",
]
