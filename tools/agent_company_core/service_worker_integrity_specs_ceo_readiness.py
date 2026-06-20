from __future__ import annotations

from typing import Any

"""Compatibility facade for CEO apply-readiness integrity spec phases."""

from .service_worker_integrity_specs_ceo_readiness_approval import ceo_readiness_approval_integrity_specs
from .service_worker_integrity_specs_ceo_readiness_flow import ceo_readiness_flow_integrity_specs


def ceo_readiness_integrity_specs() -> list[dict[str, Any]]:
    return [
        *ceo_readiness_flow_integrity_specs(),
        *ceo_readiness_approval_integrity_specs(),
    ]


__all__ = [
    "ceo_readiness_integrity_specs",
    "ceo_readiness_flow_integrity_specs",
    "ceo_readiness_approval_integrity_specs",
]
