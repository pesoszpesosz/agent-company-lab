"""Catalog-backed service-request lifecycle operations."""

from __future__ import annotations

from .service_requests_core import (
    create_service_request,
    get_service_request,
    resolve_service_catalog_entry,
    validate_service_intake,
    validate_service_request,
    validate_service_request_record,
)
from .service_requests_review import (
    service_request_recommendation,
    service_request_where,
    write_service_request_review,
)
from .service_requests_scaffold import (
    generated_service_request_id,
    render_service_request_checklist,
    render_service_request_packet,
    scaffold_service_request,
)
from .service_requests_lifecycle import (
    approve_service_request,
    assign_service_request,
    complete_service_request,
    reject_service_request,
    start_service_request,
)

__all__ = [
    "resolve_service_catalog_entry",
    "validate_service_intake",
    "create_service_request",
    "get_service_request",
    "validate_service_request_record",
    "validate_service_request",
    "service_request_where",
    "service_request_recommendation",
    "write_service_request_review",
    "generated_service_request_id",
    "render_service_request_packet",
    "render_service_request_checklist",
    "scaffold_service_request",
    "approve_service_request",
    "reject_service_request",
    "assign_service_request",
    "start_service_request",
    "complete_service_request",
]