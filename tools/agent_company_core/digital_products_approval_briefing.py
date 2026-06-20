from __future__ import annotations

"""Compatibility facade for digital-products approval briefing writers."""

from .digital_products_approval_operator_brief import write_digital_products_local_operator_approval_brief
from .digital_products_approval_request_drafts import (
    digital_products_approval_request_draft_packets,
    write_digital_products_local_approval_request_drafts,
)

__all__ = [
    "digital_products_approval_request_draft_packets",
    "write_digital_products_local_approval_request_drafts",
    "write_digital_products_local_operator_approval_brief",
]
