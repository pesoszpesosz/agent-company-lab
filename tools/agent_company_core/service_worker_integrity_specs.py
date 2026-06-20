from __future__ import annotations

from typing import Any

"""Compatibility facade for service-worker chain-integrity spec families."""

from .service_worker_integrity_specs_service_workers import service_worker_control_integrity_specs
from .service_worker_integrity_specs_money import money_lane_integrity_specs
from .service_worker_integrity_specs_ceo import ceo_integrity_specs
from .service_worker_integrity_specs_migration import migration_integrity_specs
from .service_worker_integrity_specs_durable import durable_integrity_specs
from .service_worker_integrity_specs_runtime import runtime_integrity_specs


def service_worker_chain_integrity_specs() -> list[dict[str, Any]]:
    return [
        *service_worker_control_integrity_specs(),
        *money_lane_integrity_specs(),
        *ceo_integrity_specs(),
        *migration_integrity_specs(),
        *durable_integrity_specs(),
        *runtime_integrity_specs(),
    ]


__all__ = [
    "service_worker_chain_integrity_specs",
    "service_worker_control_integrity_specs",
    "money_lane_integrity_specs",
    "ceo_integrity_specs",
    "migration_integrity_specs",
    "durable_integrity_specs",
    "runtime_integrity_specs",
]
