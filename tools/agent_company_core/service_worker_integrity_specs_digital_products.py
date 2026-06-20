from __future__ import annotations

from typing import Any

"""Digital-product lane integrity spec facade."""

from .service_worker_integrity_specs_digital_products_approval import digital_product_approval_integrity_specs
from .service_worker_integrity_specs_digital_products_assets import digital_product_asset_integrity_specs
from .service_worker_integrity_specs_digital_products_demand import digital_product_demand_integrity_specs
from .service_worker_integrity_specs_digital_products_review import digital_product_review_integrity_specs


def digital_product_integrity_specs() -> list[dict[str, Any]]:
    return [
        *digital_product_demand_integrity_specs(),
        *digital_product_asset_integrity_specs(),
        *digital_product_review_integrity_specs(),
        *digital_product_approval_integrity_specs(),
    ]


__all__ = ["digital_product_integrity_specs"]