from __future__ import annotations

"""Compatibility facade for service-worker assignment, pool, registration, and gate-map reports."""

from .service_worker_assignment_core import (
    WORKER_TYPE_ASSIGNMENT_ROLES,
    lane_manager_for_row,
    service_worker_assignment_plan_entry,
)
from .service_worker_assignment_plan import write_service_worker_assignment_plan
from .service_worker_pool_registry import (
    service_worker_pool_registry_entries,
    write_service_worker_pool_registry,
)
from .service_worker_pool_registration import (
    service_worker_pool_registration_department,
    service_worker_pool_registration_boundaries,
    service_worker_pool_registration_entry,
    write_service_worker_pool_registration_plan,
)
from .service_worker_gate_map import (
    service_worker_gate_map_entry,
    write_service_worker_gate_map,
)

__all__ = [
    "WORKER_TYPE_ASSIGNMENT_ROLES",
    "lane_manager_for_row",
    "service_worker_assignment_plan_entry",
    "write_service_worker_assignment_plan",
    "service_worker_pool_registry_entries",
    "write_service_worker_pool_registry",
    "service_worker_pool_registration_department",
    "service_worker_pool_registration_boundaries",
    "service_worker_pool_registration_entry",
    "write_service_worker_pool_registration_plan",
    "service_worker_gate_map_entry",
    "write_service_worker_gate_map",
]
