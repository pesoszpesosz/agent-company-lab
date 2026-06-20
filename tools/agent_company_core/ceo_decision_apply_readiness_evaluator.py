"""Shared evaluator for CEO apply-readiness packets."""

from __future__ import annotations

from typing import Any


def evaluate_ceo_apply_readiness_packet(
    packet: dict[str, Any],
    *,
    require_preview_apply_boundary: bool = False,
) -> dict[str, Any]:
    approvals = packet.get("required_operator_approvals") or []
    snapshot = packet.get("rollback_snapshot") or {}
    planned_updates = packet.get("planned_field_updates") or {}
    update_shape = packet.get("planned_update_sql_shape") or {}
    boundary = packet.get("apply_boundary") or {}
    if len(approvals) < 5:
        return {"accepted_readiness": False, "rule_id": "reject_missing_operator_approval_bundle", "preview_state": None, "real_mutation_allowed": False}
    if snapshot.get("updated_at") != packet.get("target_updated_at_before"):
        return {"accepted_readiness": False, "rule_id": "reject_stale_rollback_snapshot", "preview_state": None, "real_mutation_allowed": False}
    if packet.get("target_status_before") != "needs_review":
        return {"accepted_readiness": False, "rule_id": "reject_target_status_drift", "preview_state": None, "real_mutation_allowed": False}
    if set(planned_updates.keys()) != {"approval_scope", "decision_note"}:
        return {"accepted_readiness": False, "rule_id": "reject_planned_field_drift", "preview_state": None, "real_mutation_allowed": False}
    if update_shape.get("table") != "service_requests" or update_shape.get("max_rows") != 1:
        return {"accepted_readiness": False, "rule_id": "reject_unbounded_update_shape", "preview_state": None, "real_mutation_allowed": False}
    if boundary.get("worker_starts") != 0 or boundary.get("external_side_effects") is not False or boundary.get("service_requests_updated") != 0:
        return {"accepted_readiness": False, "rule_id": "reject_side_effect_boundary_open", "preview_state": None, "real_mutation_allowed": False}
    if require_preview_apply_boundary and (
        boundary.get("apply_allowed_now") is not False
        or boundary.get("requires_explicit_operator_apply_approval") is not True
    ):
        return {"accepted_readiness": False, "rule_id": "reject_apply_boundary_not_preview_only", "preview_state": None, "real_mutation_allowed": False}
    return {
        "accepted_readiness": True,
        "rule_id": None,
        "preview_state": "readiness_packet_valid_apply_still_disabled" if require_preview_apply_boundary else None,
        "real_mutation_allowed": False,
    }


__all__ = ["evaluate_ceo_apply_readiness_packet"]
