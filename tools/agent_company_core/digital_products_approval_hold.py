from __future__ import annotations

"""Compatibility facade for digital-products approval hold writers."""

from .digital_products_approval_gated_hold import write_digital_products_local_gated_hold_register
from .digital_products_approval_simulation_plan import write_digital_products_local_post_approval_simulation_plan

__all__ = [
    "write_digital_products_local_post_approval_simulation_plan",
    "write_digital_products_local_gated_hold_register",
]
