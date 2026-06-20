from __future__ import annotations

"""Compatibility facade for CEO decision intake guard writers."""

from .ceo_decision_intake_guard_core import write_ceo_decision_intake_guard
from .ceo_decision_intake_negative_fixtures import write_ceo_decision_intake_negative_fixtures

__all__ = [
    "write_ceo_decision_intake_guard",
    "write_ceo_decision_intake_negative_fixtures",
]
