from __future__ import annotations

"""Compatibility facade for service-worker scope reports."""

from .service_worker_scope_core import (
    SIDE_EFFECT_SCOPE_RULES,
    NEGATION_MARKERS,
    normalized_scope_text,
    term_present_with_negation_awareness,
    denial_present,
    positive_conflicts,
    concrete_hosts_from_packet,
    host_scope_mentions,
    compact_sequence,
    scope_template_output_paths,
    scope_template_hosts,
    scope_template_starting_urls,
    scope_template_allowed_data,
    scope_template_required_denials,
    join_scope_items,
)
from .service_worker_scope_diff import (
    service_worker_scope_diff_entry,
    write_service_worker_scope_diff,
)
from .service_worker_scope_templates import (
    service_worker_scope_template_entry,
    write_service_worker_scope_templates,
)
from .service_worker_approval_review import (
    service_worker_approval_review_entry,
    write_service_worker_approval_review,
)

__all__ = [
    "SIDE_EFFECT_SCOPE_RULES",
    "NEGATION_MARKERS",
    "normalized_scope_text",
    "term_present_with_negation_awareness",
    "denial_present",
    "positive_conflicts",
    "concrete_hosts_from_packet",
    "host_scope_mentions",
    "compact_sequence",
    "scope_template_output_paths",
    "scope_template_hosts",
    "scope_template_starting_urls",
    "scope_template_allowed_data",
    "scope_template_required_denials",
    "join_scope_items",
    "service_worker_scope_diff_entry",
    "write_service_worker_scope_diff",
    "service_worker_scope_template_entry",
    "write_service_worker_scope_templates",
    "service_worker_approval_review_entry",
    "write_service_worker_approval_review",
]
