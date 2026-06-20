from __future__ import annotations

from typing import Any

"""Compatibility facade for money-lane service-worker integrity spec domains."""

from .service_worker_integrity_specs_money_paths import money_path_integrity_specs
from .service_worker_integrity_specs_paid_code import paid_code_integrity_specs
from .service_worker_integrity_specs_digital_products import digital_product_integrity_specs


def money_lane_integrity_specs() -> list[dict[str, Any]]:
    return [
        *money_path_integrity_specs(),
        *paid_code_integrity_specs(),
        *digital_product_integrity_specs(),
    ]


__all__ = [
    "money_lane_integrity_specs",
    "money_path_integrity_specs",
    "paid_code_integrity_specs",
    "digital_product_integrity_specs",
]
