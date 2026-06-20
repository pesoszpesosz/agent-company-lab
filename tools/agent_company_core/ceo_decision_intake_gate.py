from __future__ import annotations

"""Compatibility facade for CEO gate-board and blocker-triage writers."""

from .ceo_blocker_triage import write_ceo_blocker_triage
from .ceo_gate_blocker_board import write_ceo_gate_blocker_board

__all__ = [
    "write_ceo_gate_blocker_board",
    "write_ceo_blocker_triage",
]