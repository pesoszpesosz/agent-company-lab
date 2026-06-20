from __future__ import annotations

"""Compatibility facade for money-path coverage, evidence, and manager-proof writers."""

from .money_paths_coverage import (
    money_path_lane_assignment,
    write_money_path_coverage_audit,
)

from .money_paths_evidence import (
    first_local_evidence_summary,
    write_first_local_evidence_packets,
)

from .money_paths_manager_proof import (
    manager_proof_task_template,
    write_manager_proof_task_packets,
    write_manager_proof_task_promotion_preflight,
    manager_proof_task_queue_score,
    write_manager_proof_task_promotion_queue,
)

from .money_paths_ranked_proof import (
    write_first_ranked_manager_proof,
)

__all__ = [
    "money_path_lane_assignment",
    "write_money_path_coverage_audit",
    "first_local_evidence_summary",
    "write_first_local_evidence_packets",
    "manager_proof_task_template",
    "write_manager_proof_task_packets",
    "write_manager_proof_task_promotion_preflight",
    "manager_proof_task_queue_score",
    "write_manager_proof_task_promotion_queue",
    "write_first_ranked_manager_proof",
]
