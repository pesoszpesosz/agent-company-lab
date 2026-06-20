from __future__ import annotations

from typing import Any

"""Compatibility facade for CEO decision chain integrity spec phases."""

from .service_worker_integrity_specs_ceo_apply import ceo_apply_integrity_specs
from .service_worker_integrity_specs_ceo_apply_command import ceo_apply_command_integrity_specs
from .service_worker_integrity_specs_ceo_intake import ceo_intake_integrity_specs
from .service_worker_integrity_specs_ceo_parser import ceo_parser_integrity_specs
from .service_worker_integrity_specs_ceo_readiness import ceo_readiness_integrity_specs
from .service_worker_integrity_specs_ceo_signed_decision import ceo_signed_decision_integrity_specs


def ceo_integrity_specs() -> list[dict[str, Any]]:
    return [
        *ceo_intake_integrity_specs(),
        *ceo_parser_integrity_specs(),
        *ceo_apply_integrity_specs(),
        *ceo_readiness_integrity_specs(),
        *ceo_signed_decision_integrity_specs(),
        *ceo_apply_command_integrity_specs(),
    ]


__all__ = [
    "ceo_integrity_specs",
    "ceo_intake_integrity_specs",
    "ceo_parser_integrity_specs",
    "ceo_apply_integrity_specs",
    "ceo_readiness_integrity_specs",
    "ceo_signed_decision_integrity_specs",
    "ceo_apply_command_integrity_specs",
]
