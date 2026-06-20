from __future__ import annotations

"""Compatibility facade for digital product approval workflow writers."""

from .digital_products_approval_briefing import (
    digital_products_approval_request_draft_packets,
    write_digital_products_local_approval_request_drafts,
    write_digital_products_local_operator_approval_brief,
)
from .digital_products_approval_hold import (
    write_digital_products_local_gated_hold_register,
    write_digital_products_local_post_approval_simulation_plan,
)
from .digital_products_approval_polish import (
    digital_products_copy_polish_files,
    digital_products_post_polish_readiness_checks,
    write_digital_products_local_copy_polish,
    write_digital_products_local_post_polish_readiness,
)

__all__ = [
    "digital_products_copy_polish_files",
    "write_digital_products_local_copy_polish",
    "digital_products_post_polish_readiness_checks",
    "write_digital_products_local_post_polish_readiness",
    "digital_products_approval_request_draft_packets",
    "write_digital_products_local_approval_request_drafts",
    "write_digital_products_local_operator_approval_brief",
    "write_digital_products_local_post_approval_simulation_plan",
    "write_digital_products_local_gated_hold_register",
]
