from __future__ import annotations

from typing import Any

"""Service-worker queue, scope, assignment, and decision-control integrity specs."""

from .service_worker_integrity_specs_service_worker_decisions import service_worker_decision_integrity_specs
from .service_worker_integrity_specs_service_worker_lifecycle import service_worker_lifecycle_integrity_specs


def service_worker_control_integrity_specs() -> list[dict[str, Any]]:
    return [
        *service_worker_lifecycle_integrity_specs(),
        *service_worker_decision_integrity_specs(),
    ]


__all__ = [
    "service_worker_control_integrity_specs",
    "service_worker_decision_integrity_specs",
    "service_worker_lifecycle_integrity_specs",
]
