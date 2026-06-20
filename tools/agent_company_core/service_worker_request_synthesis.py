from __future__ import annotations

from pathlib import Path
from typing import Any

from .paths import ROOT
from .service_worker_policy import (
    SERVICE_WORKER_REQUIRED_FIELDS,
    SERVICE_WORKER_TYPES,
    service_worker_allowed_actions,
    service_worker_boundaries,
    service_worker_data_boundary,
    service_worker_expected_output,
    service_worker_objective,
    service_worker_stop_conditions,
    service_worker_type_for_request,
)

def service_worker_packet_path(request_id: str) -> Path:
    return ROOT / "requests" / "service-requests" / request_id / "service-worker-request-v1.json"


def synthesize_service_worker_request(row: dict[str, Any], generated_utc: str) -> dict[str, Any]:
    worker_type = service_worker_type_for_request(row)
    credentials, account, money, public = service_worker_boundaries(worker_type)
    request_dir = ROOT / "requests" / "service-requests" / row["request_id"]
    artifact_path = row.get("artifact_path") or str(request_dir / "packet.md")
    output = service_worker_expected_output(row, worker_type)
    return {
        "schema_version": "service_worker_request.v1",
        "worker_request_id": "swr-" + (row["request_id"][4:] if row["request_id"].startswith("req-") else row["request_id"]),
        "source_service_request_id": row["request_id"],
        "requesting_lane_id": row["lane_id"],
        "requesting_agent_id": row.get("assigned_agent_id") or "unassigned_requester_or_lane_manager",
        "worker_type": worker_type,
        "service_id": row.get("service_id") or worker_type,
        "risk_gate": row.get("risk_gate") or "unspecified_risk_gate",
        "approval_status_snapshot": row["status"],
        "approval_scope": "Generated queue row only. This row mirrors the service request status and grants no approval or execution authority.",
        "created_utc": generated_utc,
        "objective": service_worker_objective(row, worker_type),
        "allowed_actions": service_worker_allowed_actions(row, worker_type),
        "prohibited_actions": [
            "execute without explicit approval",
            "login unless explicitly approved",
            "signup or account creation",
            "accept terms or legal agreements",
            "enter credentials, OTPs, personal data, private files, payment details, tax/KYC data, or wallet information",
            "submit forms",
            "publish, post, reply, comment, message, list, upload, or contact external parties",
            "purchase, deposit, withdraw, trade, connect wallet, sign wallet messages, or perform real-money actions",
            "change account settings",
            "bypass paywalls, rate limits, access controls, or platform rules",
        ],
        "stop_conditions": service_worker_stop_conditions(row, worker_type),
        "credential_boundary": credentials,
        "account_boundary": account,
        "money_boundary": money,
        "public_action_boundary": public,
        "data_boundary": service_worker_data_boundary(worker_type),
        "external_side_effects_allowed": False,
        "real_money_allowed": False,
        "public_action_allowed": False,
        "account_or_identity_action_allowed": False,
        "model_or_api_cost_allowed": False,
        "max_cost_usd": 0,
        "input_artifacts": [
            {
                "kind": "source_service_request_artifact",
                "path_or_url": artifact_path,
                "required": bool(row.get("artifact_path")),
            }
        ],
        "expected_output_artifacts": [output],
        "execution_plan_path": str(request_dir / "execution-plan-v1.json") if (request_dir / "execution-plan-v1.json").exists() else artifact_path,
        "result_artifact_path": output["path"],
        "replay_policy": {
            "idempotency_key": f"{row['request_id']}:{worker_type}:{row.get('risk_gate') or 'no_risk_gate'}",
            "safe_to_replay_without_reapproval": False,
            "replay_requires_new_approval_when": [
                "any execution would occur",
                "status is not approved or assigned",
                "scope, risk gate, target, or worker type changes",
                "credentials, private data, account, public action, payment, wallet, legal commitment, model/API cost, or real-money activity would be needed",
            ],
        },
        "status": row["status"],
        "metadata": {
            "generated_by": "write-service-worker-queue",
            "decision_note": row.get("decision_note"),
            "assigned_agent_id": row.get("assigned_agent_id"),
            "api_calls": False,
            "browser_opened": False,
            "external_side_effects": False,
            "approval_granted_by_this_artifact": False,
        },
    }


def validate_service_worker_request_object(obj: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in SERVICE_WORKER_REQUIRED_FIELDS:
        if field not in obj:
            errors.append(f"missing:{field}")
    if obj.get("schema_version") != "service_worker_request.v1":
        errors.append("schema_version")
    if obj.get("worker_type") not in SERVICE_WORKER_TYPES:
        errors.append("worker_type")
    for flag in [
        "external_side_effects_allowed",
        "real_money_allowed",
        "public_action_allowed",
        "account_or_identity_action_allowed",
        "model_or_api_cost_allowed",
    ]:
        if obj.get(flag) is not False:
            errors.append(f"{flag}_not_false")
    return errors
