from __future__ import annotations

"""Compatibility facade for CEO decision parser report-only fixtures."""

from .ceo_decision_parser_report_only_fixture_suite import write_ceo_decision_parser_fixture_suite
from .ceo_decision_parser_report_only_positive_fixture import write_ceo_decision_parser_positive_fixture

__all__ = [
    "write_ceo_decision_parser_positive_fixture",
    "write_ceo_decision_parser_fixture_suite",
]
