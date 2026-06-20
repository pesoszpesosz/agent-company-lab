#!/usr/bin/env python3
"""Write runtime implementation human approval packet v2 from local runner evidence."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
REPORTS = ROOT / "reports"
DURABLE = REPORTS / "durable-orchestration"
SCHEMA_PATH = ROOT / "architecture" / "runtime-implementation-human-approval-packet-v2.schema.json"
DEFAULT_DECISION = DURABLE / "durable-runtime-comparison-decision-packet-v1-20260617.json"
DEFAULT_ACK_VALIDATION = DURABLE / "sqlite-outbox-acknowledgement-runner-v1-validation-20260617.json"
DEFAULT_STATE_VALIDATION = DURABLE / "local-service-worker-request-state-machine-runner-v1-validation-20260617.json"
DEFAULT_CHAIN_VALIDATION = REPORTS / "service-worker-chain-integrity-validation-latest.json"
DEFAULT_JSON_OUT = DURABLE / "runtime-implementation-human-approval-packet-v2-20260617.json"
DEFAULT_VALIDATION_OUT = DURABLE / "runtime-implementation-human-approval-packet-v2-validation-20260617.json"
DEFAULT_MD_OUT = DURABLE / "runtime-implementation-human-approval-packet-v2-20260617.md"

ZERO_RUNTIME_BOUNDARY = {
    "dependency_installs": 0,
    "dependency_imports": 0,
    "runtime_starts": 0,
    "queue_enqueues": 0,
    "workflow_starts": 0,
    "event_sends": 0,
    "server_starts": 0,
    "database_provisioning": False,
    "service_requests_updated": 0,
    "service_requests_assigned": 0,
    "service_requests_started": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "api_calls": False,
    "model_api_calls": False,
    "public_actions": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "security_testing_actions": False,
    "real_money_actions": False,
    "external_side_effects": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def approval_questions() -> list[dict[str, Any]]:
    specs = [
        ("approve_runtime_candidate", "Which one runtime candidate, if any, is approved for implementation?", "deny_all"),
        ("approve_dependency_install_scope", "May dependencies be installed for the selected runtime?", "no"),
        ("approve_runtime_import_scope", "May selected runtime libraries be imported from executable code?", "no"),
        ("approve_runtime_start_scope", "May local servers, workers, workflows, functions, schedules, or event emitters be started?", "no"),
        ("approve_database_or_cloud_scope", "May databases, cloud services, accounts, endpoints, or service credentials be provisioned or contacted?", "no"),
        ("approve_service_request_mutation_scope", "May runtime code assign, start, complete, reject, or otherwise mutate service_requests rows?", "no"),
        ("approve_worker_pool_registration_scope", "May service-worker pools be registered as executable workers rather than report-only plans?", "no"),
        ("approve_model_api_scope", "May model/API execution be used, including provider, model, data scope, and cost cap?", "no"),
        ("approve_trace_export_scope", "May traces be sent to an observability backend rather than local JSONL/SQLite artifacts?", "no"),
        ("approve_browser_or_public_action_scope", "May browser sessions, public actions, submissions, comments, forms, or account actions occur?", "no"),
        ("approve_wallet_payment_real_money_scope", "May wallet, payment, deposit, withdrawal, trade, payout, or real-money actions occur?", "no"),
        ("approve_security_testing_scope", "May security testing or private-report submission occur beyond local/public-code review?", "no"),
    ]
    return [
        {
            "question_id": question_id,
            "question": question,
            "current_default": default,
            "required_for_any_approval": True,
        }
        for question_id, question, default in specs
    ]


def required_decision_fields(question_ids: list[str]) -> list[dict[str, Any]]:
    return [
        {"field_id": "decision_id", "required": True, "default": "", "purpose": "Stable human decision identifier."},
        {"field_id": "decision", "required": True, "default": "deny", "allowed_values": ["deny", "approve_one_runtime_candidate"], "purpose": "Explicit deny or limited approval."},
        {"field_id": "approver", "required": True, "default": "", "purpose": "Human approver identity."},
        {"field_id": "signed_utc", "required": True, "default": "", "purpose": "Human signature timestamp."},
        {"field_id": "expires_utc", "required": True, "default": "", "purpose": "Approval expiry timestamp."},
        {"field_id": "selected_runtime_id", "required": True, "default": "none", "purpose": "Exactly one runtime candidate or none."},
        {"field_id": "approved_question_ids", "required": True, "default": [], "purpose": "Question IDs explicitly granted."},
        {"field_id": "denied_question_ids", "required": True, "default": question_ids, "purpose": "Question IDs denied or still parked."},
        {"field_id": "allowed_dependency_names", "required": True, "default": [], "purpose": "Exact dependency names and versions if installs are approved."},
        {"field_id": "allowed_runtime_processes", "required": True, "default": [], "purpose": "Exact local server/worker/process commands if starts are approved."},
        {"field_id": "allowed_database_or_cloud_resources", "required": True, "default": [], "purpose": "Exact DB/cloud/account resources if any are approved."},
        {"field_id": "service_request_mutation_scope", "required": True, "default": "none", "purpose": "Exact rows and mutations allowed, otherwise none."},
        {"field_id": "provider_model_and_cost_cap", "required": True, "default": "none", "purpose": "Model/API provider, model, data scope, and cost cap."},
        {"field_id": "artifact_output_path", "required": True, "default": "", "purpose": "Allowed local output artifact path."},
        {"field_id": "rollback_plan", "required": True, "default": "", "purpose": "How to stop/revert approved runtime work."},
        {"field_id": "human_notes", "required": False, "default": "", "purpose": "Optional constraints and rationale."},
    ]


def build_packet(decision: dict[str, Any], ack: dict[str, Any], state: dict[str, Any], chain: dict[str, Any]) -> dict[str, Any]:
    questions = approval_questions()
    runtime_candidates = []
    for item in decision.get("runtime_recommendations", []):
        runtime_candidates.append(
            {
                "runtime_id": item.get("runtime_id"),
                "rank": item.get("rank"),
                "decision": item.get("decision"),
                "score": item.get("score"),
                "implementation_role": item.get("implementation_role"),
                "required_gates_before_execution": item.get("required_gates_before_execution", []),
                "default_packet_posture": "deny_until_signed_human_decision",
            }
        )
    return {
        "schema_version": "agent_company.runtime_implementation_human_approval_packet.v2",
        "generated_utc": utc_now(),
        "task_id": "task-runtime-implementation-human-approval-packet-v2-20260617",
        "lane_id": "platform_engineering",
        "owner_agent_id": "recovered-profitable-edge-infra",
        "purpose": "Human/CRO approval packet v2 for any external or executable runtime implementation after local SQLite/outbox and service-worker state-machine proofs. This packet grants no approval.",
        "source_evidence": {
            "decision_packet": {
                "path": str(DEFAULT_DECISION),
                "status": decision.get("decision_summary", {}).get("status"),
                "approved_now": decision.get("decision_summary", {}).get("approved_now", []),
                "not_approved_now": decision.get("decision_summary", {}).get("not_approved_now", []),
            },
            "outbox_acknowledgement_runner": {
                "path": str(DEFAULT_ACK_VALIDATION),
                "failed_count": ack.get("failed_count"),
                "acknowledgements_checked": ack.get("acknowledgements_checked"),
                "negative_probes_checked": ack.get("negative_probes_checked"),
            },
            "service_worker_state_machine_runner": {
                "path": str(DEFAULT_STATE_VALIDATION),
                "failed_count": state.get("failed_count"),
                "transition_count": state.get("transition_count"),
                "policy_probe_count": state.get("policy_probe_count"),
                "disposition_counts": state.get("disposition_counts"),
            },
            "chain_integrity": {
                "path": str(DEFAULT_CHAIN_VALIDATION),
                "all_checks_passed": chain.get("all_checks_passed"),
                "failure_count": chain.get("failure_count"),
                "checked_report_count": chain.get("checked_report_count"),
            },
        },
        "approval_questions": questions,
        "runtime_candidates": runtime_candidates,
        "required_decision_fields": required_decision_fields([item["question_id"] for item in questions]),
        "runtime_boundary": ZERO_RUNTIME_BOUNDARY.copy(),
        "approval_granted_by_packet": False,
        "runtime_implementation_allowed": False,
        "runtime_code_write_allowed": False,
        "next_action": "A human may fill a separate signed decision artifact. Until then, keep all runtime implementation, dependency, server/cloud, worker-pool, model/API, browser/public/account/wallet/payment/security/real-money, and service-request mutation actions parked.",
    }


def validate_packet(packet: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    evidence = packet["source_evidence"]
    if evidence["outbox_acknowledgement_runner"].get("failed_count") != 0:
        failures.append("outbox_acknowledgement_runner_not_clean")
    if evidence["service_worker_state_machine_runner"].get("failed_count") != 0:
        failures.append("service_worker_state_machine_runner_not_clean")
    if evidence["chain_integrity"].get("all_checks_passed") is not True or evidence["chain_integrity"].get("failure_count") != 0:
        failures.append("chain_integrity_not_clean")
    if len(packet["runtime_candidates"]) != 7:
        failures.append("runtime_candidate_count_not_7")
    if len(packet["approval_questions"]) != 12:
        failures.append("approval_question_count_not_12")
    if len(packet["required_decision_fields"]) != 16:
        failures.append("required_decision_field_count_not_16")
    for key, expected in ZERO_RUNTIME_BOUNDARY.items():
        if packet["runtime_boundary"].get(key) != expected:
            failures.append(f"runtime_boundary.{key}_not_{expected!r}")
    if packet["approval_granted_by_packet"] is not False:
        failures.append("approval_granted_by_packet_not_false")
    if packet["runtime_implementation_allowed"] is not False:
        failures.append("runtime_implementation_allowed_not_false")
    if packet["runtime_code_write_allowed"] is not False:
        failures.append("runtime_code_write_allowed_not_false")

    return {
        "schema_version": "agent_company.runtime_implementation_human_approval_packet_v2_validation.v1",
        "generated_utc": utc_now(),
        "approval_packet_path": str(DEFAULT_JSON_OUT),
        "markdown_path": str(DEFAULT_MD_OUT),
        "schema_path": str(SCHEMA_PATH),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "runtime_candidate_count": len(packet["runtime_candidates"]),
        "approval_question_count": len(packet["approval_questions"]),
        "required_decision_field_count": len(packet["required_decision_fields"]),
        "source_runner_validation_count": 3,
        "source_runner_failure_count": (
            int(evidence["outbox_acknowledgement_runner"].get("failed_count") or 0)
            + int(evidence["service_worker_state_machine_runner"].get("failed_count") or 0)
            + int(evidence["chain_integrity"].get("failure_count") or 0)
        ),
        "approval_granted_by_packet": False,
        "runtime_implementation_allowed": False,
        "runtime_code_write_allowed": False,
        "dependency_installs": 0,
        "dependency_imports": 0,
        "runtime_starts": 0,
        "server_starts": 0,
        "database_provisioning": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "browser_sessions_started": 0,
        "api_calls": False,
        "model_api_calls": False,
        "public_actions": False,
        "external_side_effects": False,
    }


def write_markdown(packet: dict[str, Any], validation: dict[str, Any], path: Path) -> None:
    lines = [
        "# Runtime Implementation Human Approval Packet v2",
        "",
        f"Generated UTC: {packet['generated_utc']}",
        f"Packet JSON: `{DEFAULT_JSON_OUT}`",
        f"Validation JSON: `{DEFAULT_VALIDATION_OUT}`",
        f"Schema: `{SCHEMA_PATH}`",
        "",
        "## Current Decision",
        "",
        f"- Approval granted by this packet: `{str(packet['approval_granted_by_packet']).lower()}`",
        f"- Runtime implementation allowed now: `{str(packet['runtime_implementation_allowed']).lower()}`",
        f"- Runtime code write allowed now: `{str(packet['runtime_code_write_allowed']).lower()}`",
        f"- Validation failures: `{validation['failure_count']}`",
        "",
        "## Source Evidence",
        "",
        f"- Outbox acknowledgement runner failures: `{packet['source_evidence']['outbox_acknowledgement_runner']['failed_count']}`",
        f"- State-machine runner failures: `{packet['source_evidence']['service_worker_state_machine_runner']['failed_count']}`",
        f"- Chain integrity failures: `{packet['source_evidence']['chain_integrity']['failure_count']}`",
        "",
        "## Runtime Candidates",
        "",
        "| Rank | Runtime | Current Decision | Score | Required Gates |",
        "| ---: | --- | --- | ---: | --- |",
    ]
    for candidate in packet["runtime_candidates"]:
        gates = ", ".join(candidate.get("required_gates_before_execution") or ["none_for_local_report_only"])
        lines.append(
            f"| `{candidate['rank']}` | `{candidate['runtime_id']}` | `{candidate['decision']}` | `{candidate['score']}` | {gates} |"
        )
    lines.extend(
        [
            "",
            "## Approval Questions",
            "",
            "| Question ID | Default | Question |",
            "| --- | --- | --- |",
        ]
    )
    for question in packet["approval_questions"]:
        lines.append(f"| `{question['question_id']}` | `{question['current_default']}` | {question['question']} |")
    lines.extend(
        [
            "",
            "## Required Decision Fields",
            "",
            "| Field | Required | Default | Purpose |",
            "| --- | --- | --- | --- |",
        ]
    )
    for field in packet["required_decision_fields"]:
        default = json.dumps(field.get("default"), ensure_ascii=False)
        lines.append(f"| `{field['field_id']}` | `{str(field['required']).lower()}` | `{default}` | {field['purpose']} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This packet does not approve dependency installs, runtime imports, runtime starts, server/cloud/database provisioning, worker-pool registration, model/API calls, browser/public/account/wallet/payment/security/real-money actions, or service-request mutation.",
            "- A separate signed human decision artifact is required before any executable runtime implementation work.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    parser.add_argument("--ack-validation", type=Path, default=DEFAULT_ACK_VALIDATION)
    parser.add_argument("--state-validation", type=Path, default=DEFAULT_STATE_VALIDATION)
    parser.add_argument("--chain-validation", type=Path, default=DEFAULT_CHAIN_VALIDATION)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_OUT)
    parser.add_argument("--validation-out", type=Path, default=DEFAULT_VALIDATION_OUT)
    parser.add_argument("--md-out", type=Path, default=DEFAULT_MD_OUT)
    args = parser.parse_args()

    packet = build_packet(
        load_json(args.decision),
        load_json(args.ack_validation),
        load_json(args.state_validation),
        load_json(args.chain_validation),
    )
    validation = validate_packet(packet)
    args.json_out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.validation_out.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(packet, validation, args.md_out)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "json": str(args.json_out)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
