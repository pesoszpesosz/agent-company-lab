from __future__ import annotations

"""Compatibility facade for catalog seed, list, and report operations."""

from .catalog_listing import list_evidence, list_service_catalog, list_source_specs, service_catalog_where
from .catalog_report import write_service_catalog_report
from .catalog_seed import (
    department_id,
    seed,
    seed_service_catalog,
    seed_source_specs,
    upsert_department,
    upsert_lane,
    upsert_role,
    upsert_service_definition,
    upsert_source_spec,
)


__all__ = [
    "department_id",
    "list_evidence",
    "list_service_catalog",
    "list_source_specs",
    "seed",
    "seed_service_catalog",
    "seed_source_specs",
    "service_catalog_where",
    "upsert_department",
    "upsert_lane",
    "upsert_role",
    "upsert_service_definition",
    "upsert_source_spec",
    "write_service_catalog_report",
]