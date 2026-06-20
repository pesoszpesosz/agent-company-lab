from __future__ import annotations


def evaluate_ceo_parser_apply_request(apply_request: dict[str, object]) -> dict[str, object]:
    approval_text = str(apply_request.get("explicit_mutation_approval_text") or "")
    approval_text_lower = approval_text.lower()
    target_ids = apply_request.get("target_service_request_ids") or []
    max_update_count = int(apply_request.get("max_update_count") or 0)
    snapshot_required = bool(apply_request.get("service_request_status_snapshot_required"))
    forbidden_ack = bool(apply_request.get("forbidden_actions_acknowledged"))
    if not approval_text:
        return {"accepted_apply": False, "rule_id": "reject_missing_explicit_mutation_approval"}
    if "read-only" in approval_text_lower or "browser validation" in approval_text_lower:
        return {"accepted_apply": False, "rule_id": "reject_readonly_scope_not_mutation_approval"}
    if not target_ids:
        return {"accepted_apply": False, "rule_id": "reject_missing_target_service_request_ids"}
    if max_update_count != 1:
        return {"accepted_apply": False, "rule_id": "reject_unbounded_or_excessive_update_count"}
    if not forbidden_ack or "listing" in approval_text_lower or "marketplace" in approval_text_lower:
        return {"accepted_apply": False, "rule_id": "reject_forbidden_action_requested"}
    if not snapshot_required:
        return {"accepted_apply": False, "rule_id": "reject_missing_service_request_status_snapshot"}
    return {
        "accepted_apply": True,
        "rule_id": None,
        "would_update_count": max_update_count,
        "target_service_request_ids": target_ids,
    }


def evaluate_ceo_parser_positive_apply_preview(
    apply_request: dict[str, object],
    *,
    expected_preview: dict[str, object],
) -> dict[str, object]:
    approval_text = str(apply_request.get("explicit_mutation_approval_text") or "")
    approval_text_lower = approval_text.lower()
    request_ids = apply_request.get("target_service_request_ids") or []
    max_update_count = int(apply_request.get("max_update_count") or 0)
    if "explicitly approve applying exactly one parser preview mutation" not in approval_text_lower:
        return {"accepted_apply_preview": False, "rule_id": "reject_missing_explicit_mutation_approval"}
    if len(request_ids) != 1 or max_update_count != 1:
        return {"accepted_apply_preview": False, "rule_id": "reject_unbounded_or_excessive_update_count"}
    if not apply_request.get("service_request_status_snapshot_required"):
        return {"accepted_apply_preview": False, "rule_id": "reject_missing_service_request_status_snapshot"}
    if not apply_request.get("forbidden_actions_acknowledged"):
        return {"accepted_apply_preview": False, "rule_id": "reject_forbidden_action_requested"}
    if "open browsers" not in approval_text_lower or "account/payment/public actions" not in approval_text_lower:
        return {"accepted_apply_preview": False, "rule_id": "reject_missing_forbidden_action_boundary"}
    return {
        "accepted_apply_preview": True,
        "rule_id": None,
        "preview_state": "would_update_single_service_request_approval_scope",
        "target_service_request_ids": request_ids,
        "preview_update": expected_preview,
    }
