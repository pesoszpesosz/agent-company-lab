from __future__ import annotations

from typing import Any

"""Digital-product review integrity spec facade."""

from .service_worker_integrity_specs_digital_products_review_gate import digital_product_review_gate_integrity_specs
from .service_worker_integrity_specs_digital_products_review_polish import digital_product_review_polish_integrity_specs
from .service_worker_integrity_specs_digital_products_review_private import digital_product_review_private_integrity_specs
from .service_worker_integrity_specs_digital_products_review_revision import digital_product_review_revision_integrity_specs


def digital_product_review_integrity_specs() -> list[dict[str, Any]]:
    return [
        *digital_product_review_private_integrity_specs(),
        *digital_product_review_revision_integrity_specs(),
        *digital_product_review_gate_integrity_specs(),
        *digital_product_review_polish_integrity_specs(),
    ]


__all__ = [
    "digital_product_review_gate_integrity_specs",
    "digital_product_review_integrity_specs",
    "digital_product_review_polish_integrity_specs",
    "digital_product_review_private_integrity_specs",
    "digital_product_review_revision_integrity_specs",
]
