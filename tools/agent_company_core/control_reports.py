from __future__ import annotations

"""Compatibility facade for control-plane report writers."""

from .control_ceo_review import lane_recommendation, write_ceo_review
from .control_expansion_gap_map import suggested_manager_task, write_company_expansion_gap_map
from .control_status_reports import list_status, write_dashboard

__all__ = [
    "list_status",
    "write_dashboard",
    "lane_recommendation",
    "write_ceo_review",
    "suggested_manager_task",
    "write_company_expansion_gap_map",
]
