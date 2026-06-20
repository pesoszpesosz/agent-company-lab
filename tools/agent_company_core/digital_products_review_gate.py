from __future__ import annotations

"""Compatibility facade for digital-products gate review writers."""

from .digital_products_review_gate_choice import (
    digital_products_gate_choice_followup_items,
    write_digital_products_local_gate_choice,
)
from .digital_products_review_gate_decision import (
    digital_products_gate_decision_options,
    write_digital_products_local_gate_decision_packet,
)

__all__ = [
    "digital_products_gate_decision_options",
    "write_digital_products_local_gate_decision_packet",
    "digital_products_gate_choice_followup_items",
    "write_digital_products_local_gate_choice",
]
