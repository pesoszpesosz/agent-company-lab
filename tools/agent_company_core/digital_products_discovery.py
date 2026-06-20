from __future__ import annotations

"""Compatibility facade for local digital-product discovery stages."""

from .digital_products_demand_proof import (
    digital_products_demand_questions,
    write_digital_products_local_demand_proof,
)
from .digital_products_demand_memo import (
    digital_products_memo_candidates,
    write_digital_products_local_demand_memo,
)
from .digital_products_build_brief import write_digital_products_local_build_brief
from .digital_products_build_brief_content import (
    digital_products_build_brief_acceptance_criteria,
    digital_products_build_brief_deliverables,
    digital_products_build_brief_sections,
)

__all__ = [
    "digital_products_demand_questions",
    "write_digital_products_local_demand_proof",
    "digital_products_memo_candidates",
    "write_digital_products_local_demand_memo",
    "digital_products_build_brief_sections",
    "digital_products_build_brief_deliverables",
    "digital_products_build_brief_acceptance_criteria",
    "write_digital_products_local_build_brief",
]
