from __future__ import annotations

from typing import Any

"""Compatibility facade for decision and parser-module migration integrity specs."""

from .service_worker_integrity_specs_migration_decision_fixtures import migration_decision_fixture_integrity_specs
from .service_worker_integrity_specs_migration_decision_parser_module import (
    migration_decision_parser_module_integrity_specs,
)


def migration_decision_integrity_specs() -> list[dict[str, Any]]:
    return [
        *migration_decision_fixture_integrity_specs(),
        *migration_decision_parser_module_integrity_specs(),
    ]


__all__ = [
    "migration_decision_integrity_specs",
    "migration_decision_fixture_integrity_specs",
    "migration_decision_parser_module_integrity_specs",
]
