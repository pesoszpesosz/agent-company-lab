from __future__ import annotations

from typing import Any

"""Compatibility facade for agent-company migration integrity spec phases."""

from .service_worker_integrity_specs_migration_application import migration_application_integrity_specs
from .service_worker_integrity_specs_migration_approval_response import migration_approval_response_integrity_specs
from .service_worker_integrity_specs_migration_decision import migration_decision_integrity_specs
from .service_worker_integrity_specs_migration_foundation import migration_foundation_integrity_specs
from .service_worker_integrity_specs_migration_parser_install import migration_parser_install_integrity_specs
from .service_worker_integrity_specs_migration_write_decision import migration_write_decision_integrity_specs


def migration_integrity_specs() -> list[dict[str, Any]]:
    return [
        *migration_foundation_integrity_specs(),
        *migration_decision_integrity_specs(),
        *migration_parser_install_integrity_specs(),
        *migration_write_decision_integrity_specs(),
        *migration_approval_response_integrity_specs(),
        *migration_application_integrity_specs(),
    ]


__all__ = [
    "migration_integrity_specs",
    "migration_foundation_integrity_specs",
    "migration_decision_integrity_specs",
    "migration_parser_install_integrity_specs",
    "migration_write_decision_integrity_specs",
    "migration_approval_response_integrity_specs",
    "migration_application_integrity_specs",
]
