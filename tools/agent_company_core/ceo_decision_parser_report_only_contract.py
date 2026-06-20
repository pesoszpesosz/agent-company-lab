from __future__ import annotations

"""Compatibility facade for CEO decision parser report-only contract writers."""

from .ceo_decision_parser_report_only_dry_run_contract import write_ceo_decision_parser_dry_run_contract
from .ceo_decision_parser_report_only_preflight import write_ceo_decision_parser_preflight

__all__ = [
    "write_ceo_decision_parser_preflight",
    "write_ceo_decision_parser_dry_run_contract",
]
