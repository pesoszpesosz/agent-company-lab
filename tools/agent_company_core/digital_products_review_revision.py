from __future__ import annotations

"""Compatibility facade for digital-products private-review revision writers."""

from .digital_products_review_revised_completeness import (
    digital_products_revised_completeness_checks,
    write_digital_products_local_revised_completeness,
)
from .digital_products_review_revision_pass import write_digital_products_local_revision_pass
from .digital_products_review_revision_pass_content import digital_products_revision_pass_files

__all__ = [
    "digital_products_revision_pass_files",
    "write_digital_products_local_revision_pass",
    "digital_products_revised_completeness_checks",
    "write_digital_products_local_revised_completeness",
]
