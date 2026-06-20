from __future__ import annotations

from typing import Any

"""Compatibility facade for durable source-spec and runtime integrity specs."""

from .service_worker_integrity_specs_durable_human_decision import durable_human_decision_integrity_specs
from .service_worker_integrity_specs_durable_runtime import durable_runtime_integrity_specs
from .service_worker_integrity_specs_durable_source_specs import durable_source_spec_integrity_specs


def durable_integrity_specs() -> list[dict[str, Any]]:
    return [
        *durable_source_spec_integrity_specs(),
        *durable_runtime_integrity_specs(),
        *durable_human_decision_integrity_specs(),
    ]


__all__ = [
    "durable_integrity_specs",
    "durable_source_spec_integrity_specs",
    "durable_runtime_integrity_specs",
    "durable_human_decision_integrity_specs",
]