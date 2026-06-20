from __future__ import annotations

"""Compatibility facade for manager-proof money-path workflow stages."""

from .money_paths_manager_proof_core import (
    manager_proof_task_template,
    manager_proof_task_queue_score,
)
from .money_paths_manager_proof_packets import write_manager_proof_task_packets
from .money_paths_manager_proof_preflight import write_manager_proof_task_promotion_preflight
from .money_paths_manager_proof_queue import write_manager_proof_task_promotion_queue

__all__ = [
    "manager_proof_task_template",
    "manager_proof_task_queue_score",
    "write_manager_proof_task_packets",
    "write_manager_proof_task_promotion_preflight",
    "write_manager_proof_task_promotion_queue",
]
