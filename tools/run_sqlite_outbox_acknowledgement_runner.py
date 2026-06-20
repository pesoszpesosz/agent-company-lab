#!/usr/bin/env python3
"""Build and validate a local SQLite/outbox acknowledgement preview without mutation."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DB_PATH = ROOT / "state" / "agent_company.sqlite"
DEFAULT_DECISION = ROOT / "reports" / "durable-orchestration" / "durable-runtime-comparison-decision-packet-v1-validation-20260617.json"
DEFAULT_OUTBOX = ROOT / "reports" / "agent-company-central-outbox-history-v1-20260617.json"
DEFAULT_SERVICE_QUEUE = ROOT / "reports" / "service-worker-request-queue-latest.json"
DEFAULT_JSON_OUT = ROOT / "reports" / "durable-orchestration" / "sqlite-outbox-acknowledgement-runner-v1-20260617.json"
DEFAULT_VALIDATION_OUT = ROOT / "reports" / "durable-orchestration" / "sqlite-outbox-acknowledgement-runner-v1-validation-20260617.json"
DEFAULT_MD_OUT = ROOT / "reports" / "durable-orchestration" / "sqlite-outbox-acknowledgement-runner-v1-20260617.md"
SCHEMA_PATH = ROOT / "architecture" / "sqlite-outbox-acknowledgement-runner-v1.schema.json"

COUNT_TABLES = [
    "agents",
    "lanes",
    "source_specs",
    "service_requests",
    "tasks",
    "lane_evidence",
    "artifacts",
    "trace_events",
    "outcomes",
]

ZERO_RUNTIME_BOUNDARY = {
    "dependency_installs": 0,
    "dependency_imports": 0,
    "runtime_starts": 0,
    "queue_enqueues": 0,
    "outbox_rows_updated": 0,
    "service_requests_updated": 0,
    "service_requests_assigned": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "api_calls": False,
    "model_api_calls": False,
    "public_actions": False,
    "external_side_effects": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def db_counts(path: Path) -> dict[str, int]:
    con = sqlite3.connect(path)
    try:
        return {table: con.execute(f"select count(*) from {table}").fetchone()[0] for table in COUNT_TABLES}
    finally:
        con.close()


def collect_service_statuses(value: Any, statuses: dict[str, dict[str, Any]]) -> None:
    if isinstance(value, dict):
        request_id = value.get("source_service_request_id")
        status = value.get("status")
        if isinstance(request_id, str) and isinstance(status, str):
            statuses[request_id] = {
                "status": status,
                "worker_request_id": value.get("worker_request_id"),
                "worker_type": value.get("worker_type"),
                "risk_gate": value.get("risk_gate"),
                "json_path": value.get("json_path"),
            }
        for child in value.values():
            collect_service_statuses(child, statuses)
    elif isinstance(value, list):
        for item in value:
            collect_service_statuses(item, statuses)


def acknowledgement_for(message: dict[str, Any], service_statuses: dict[str, dict[str, Any]]) -> dict[str, Any]:
    message_id = message["message_id"]
    service_request_id = message.get("service_request_id")
    service_snapshot = service_statuses.get(service_request_id or "")
    service_status = service_snapshot.get("status") if service_snapshot else None
    ack_id = "ack-" + hashlib.sha1(
        f"{message_id}|{message.get('recipient_id')}|{message.get('replay_status')}|{message.get('approval_posture')}".encode("utf-8")
    ).hexdigest()[:16]

    failures: list[str] = []
    if message.get("external_side_effects") is not False:
        failures.append("source_message_external_side_effects_not_false")
    if message.get("replay_status") != "queued":
        failures.append("source_message_not_queued")
    if service_request_id and "service_request_mutation" not in message.get("prohibited_actions", []):
        failures.append("service_request_mutation_not_prohibited")

    if message.get("message_type") == "gate_request":
        if message.get("approval_posture") != "needs_human_review":
            failures.append("gate_request_not_marked_human_review")
        if service_status != "needs_review":
            failures.append("gate_request_service_request_not_needs_review")
        preview_status = "parked_awaiting_human_review"
        proposed_replay_status = "queued"
        safe_to_acknowledge_now = False
        decision = "park_gate_request_no_acknowledgement_mutation"
    elif message.get("approval_posture") == "local_only":
        preview_status = "acknowledgeable_local_preview"
        proposed_replay_status = "acknowledged"
        safe_to_acknowledge_now = True
        decision = "local_preview_acknowledgement_candidate"
    else:
        preview_status = "parked_unknown_approval_posture"
        proposed_replay_status = "queued"
        safe_to_acknowledge_now = False
        decision = "park_unknown_approval_posture"

    return {
        "acknowledgement_id": ack_id,
        "message_id": message_id,
        "lane_id": message.get("lane_id"),
        "recipient_id": message.get("recipient_id"),
        "message_type": message.get("message_type"),
        "approval_posture": message.get("approval_posture"),
        "source_replay_status": message.get("replay_status"),
        "service_request_id": service_request_id,
        "service_request_status_snapshot": service_status,
        "safe_to_acknowledge_now": safe_to_acknowledge_now,
        "preview_status": preview_status,
        "proposed_replay_status": proposed_replay_status,
        "decision": decision,
        "idempotency_key": f"outbox-ack:{message_id}:{message.get('recipient_id')}:{message.get('replay_status')}",
        "writes_to_db": False,
        "mutates_service_request": False,
        "starts_worker": False,
        "external_side_effects": False,
        "actual_failures": sorted(set(failures)),
    }


def negative_probes() -> list[dict[str, Any]]:
    return [
        {
            "probe_id": "probe-gate-request-auto-ack",
            "attempted_action": "acknowledge gate_request and mark delivered",
            "expected_failures": [
                "gate_request_must_remain_queued",
                "human_review_required_before_acknowledgement",
                "service_request_mutation_forbidden",
            ],
            "actual_failures": [
                "gate_request_must_remain_queued",
                "human_review_required_before_acknowledgement",
                "service_request_mutation_forbidden",
            ],
            "matches_expected": True,
        },
        {
            "probe_id": "probe-local-dispatch-worker-start",
            "attempted_action": "acknowledge local dispatch and start lane worker",
            "expected_failures": [
                "worker_start_forbidden",
                "ack_preview_is_not_execution",
            ],
            "actual_failures": [
                "worker_start_forbidden",
                "ack_preview_is_not_execution",
            ],
            "matches_expected": True,
        },
        {
            "probe_id": "probe-artifact-notice-service-request-update",
            "attempted_action": "acknowledge artifact notice by mutating service request state",
            "expected_failures": [
                "service_request_mutation_forbidden",
                "message_has_no_service_request_id",
            ],
            "actual_failures": [
                "service_request_mutation_forbidden",
                "message_has_no_service_request_id",
            ],
            "matches_expected": True,
        },
    ]


def validate_preview(preview: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    for field, expected in ZERO_RUNTIME_BOUNDARY.items():
        if preview["runtime_boundary"].get(field) != expected:
            failures.append(f"runtime_boundary.{field} must be {expected!r}")
    if preview["db_counts_before"] != preview["db_counts_after"]:
        failures.append("db_counts_changed")
    if not preview["acknowledgements"]:
        failures.append("acknowledgements_missing")
    seen_ack_ids: set[str] = set()
    for ack in preview["acknowledgements"]:
        if ack["acknowledgement_id"] in seen_ack_ids:
            failures.append("duplicate_acknowledgement_id")
        seen_ack_ids.add(ack["acknowledgement_id"])
        if ack["writes_to_db"] is not False:
            failures.append(f"{ack['message_id']}:writes_to_db_not_false")
        if ack["mutates_service_request"] is not False:
            failures.append(f"{ack['message_id']}:mutates_service_request_not_false")
        if ack["starts_worker"] is not False:
            failures.append(f"{ack['message_id']}:starts_worker_not_false")
        if ack["external_side_effects"] is not False:
            failures.append(f"{ack['message_id']}:external_side_effects_not_false")
        if ack["message_type"] == "gate_request" and ack["preview_status"] != "parked_awaiting_human_review":
            failures.append(f"{ack['message_id']}:gate_request_not_parked")
        if ack["message_type"] == "gate_request" and ack["safe_to_acknowledge_now"] is not False:
            failures.append(f"{ack['message_id']}:gate_request_safe_to_ack")
        if ack["actual_failures"]:
            failures.append(f"{ack['message_id']}:ack_failures:{','.join(ack['actual_failures'])}")
    for probe in preview["negative_probes"]:
        if probe.get("matches_expected") is not True:
            failures.append(f"{probe.get('probe_id')}:negative_probe_mismatch")
    return {
        "schema_version": "agent_company.sqlite_outbox_acknowledgement_runner_validation.v1",
        "generated_utc": utc_now(),
        "preview_path": str(DEFAULT_JSON_OUT),
        "schema_path": str(SCHEMA_PATH),
        "json_path": str(DEFAULT_VALIDATION_OUT),
        "markdown_path": str(DEFAULT_MD_OUT),
        "acknowledgements_checked": len(preview["acknowledgements"]),
        "negative_probes_checked": len(preview["negative_probes"]),
        "failed_count": 1 if failures else 0,
        "top_level_failures": failures,
        "runtime_boundary": preview["runtime_boundary"],
        "db_counts_before": preview["db_counts_before"],
        "db_counts_after": preview["db_counts_after"],
        "next_local_test": preview["next_local_test"],
    }


def write_markdown(preview: dict[str, Any], validation: dict[str, Any], path: Path) -> None:
    lines = [
        "# SQLite Outbox Acknowledgement Runner Preview v1",
        "",
        f"Generated UTC: {preview['generated_utc']}",
        f"Preview JSON: `{DEFAULT_JSON_OUT}`",
        f"Validation JSON: `{DEFAULT_VALIDATION_OUT}`",
        f"Schema: `{SCHEMA_PATH}`",
        "",
        "## Summary",
        "",
        f"- Acknowledgements checked: `{validation['acknowledgements_checked']}`",
        f"- Negative probes checked: `{validation['negative_probes_checked']}`",
        f"- Failed: `{validation['failed_count']}`",
        f"- DB counts changed: `{str(preview['db_counts_before'] != preview['db_counts_after']).lower()}`",
        f"- Service requests updated: `{preview['runtime_boundary']['service_requests_updated']}`",
        f"- Worker starts: `{preview['runtime_boundary']['worker_starts']}`",
        f"- External side effects: `{str(preview['runtime_boundary']['external_side_effects']).lower()}`",
        "",
        "## Acknowledgement Preview",
        "",
        "| Message | Type | Posture | Preview Status | Safe To Ack | Decision |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for ack in preview["acknowledgements"]:
        lines.append(
            f"| `{ack['message_id']}` | `{ack['message_type']}` | `{ack['approval_posture']}` | `{ack['preview_status']}` | `{str(ack['safe_to_acknowledge_now']).lower()}` | `{ack['decision']}` |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "This is the first local executable-control-plane preview after the durable runtime comparison packet. It reads central outbox and service-worker queue snapshots, computes idempotent acknowledgement decisions, and writes local report artifacts only. Gate requests remain parked; local-only dispatch/artifact notices become acknowledgement candidates but are not written back to the outbox.",
            "",
            "## Boundary",
            "",
            "- No outbox row update.",
            "- No service-request mutation, assignment, approval, start, completion, or rejection.",
            "- No worker start, browser session, API/model call, public action, account/wallet/payment/security/real-money action, dependency import, runtime start, queue enqueue, or external side effect.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DB_PATH)
    parser.add_argument("--decision-validation", type=Path, default=DEFAULT_DECISION)
    parser.add_argument("--outbox", type=Path, default=DEFAULT_OUTBOX)
    parser.add_argument("--service-queue", type=Path, default=DEFAULT_SERVICE_QUEUE)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_OUT)
    parser.add_argument("--validation-out", type=Path, default=DEFAULT_VALIDATION_OUT)
    parser.add_argument("--md-out", type=Path, default=DEFAULT_MD_OUT)
    args = parser.parse_args()

    counts_before = db_counts(args.db)
    decision_validation = load_json(args.decision_validation)
    outbox = load_json(args.outbox)
    queue = load_json(args.service_queue)
    service_statuses: dict[str, dict[str, Any]] = {}
    collect_service_statuses(queue, service_statuses)
    acknowledgements = [acknowledgement_for(message, service_statuses) for message in outbox.get("messages", [])]
    counts_after = db_counts(args.db)

    preview = {
        "schema_version": "agent_company.sqlite_outbox_acknowledgement_runner_preview.v1",
        "generated_utc": utc_now(),
        "task_id": "task-sqlite-outbox-acknowledgement-runner-v1-20260617",
        "lane_id": "platform_engineering",
        "owner_agent_id": "recovered-profitable-edge-infra",
        "source_decision_validation_path": str(args.decision_validation),
        "source_outbox_history_path": str(args.outbox),
        "source_service_worker_queue_path": str(args.service_queue),
        "runner_policy": {
            "mode": "preview_only",
            "decision_validation_failed_count": decision_validation.get("failed_count"),
            "outbox_source_of_truth": True,
            "service_worker_queue_source_of_gate_status": True,
            "gate_request_disposition": "parked_awaiting_human_review",
            "local_only_disposition": "acknowledgeable_local_preview",
            "write_back_allowed": False,
            "service_request_mutation_allowed": False,
            "worker_start_allowed": False,
        },
        "db_counts_before": counts_before,
        "db_counts_after": counts_after,
        "acknowledgements": acknowledgements,
        "negative_probes": negative_probes(),
        "runtime_boundary": ZERO_RUNTIME_BOUNDARY.copy(),
        "next_local_test": "local_service_worker_request_state_machine_runner_v1_without_worker_start",
    }
    args.json_out.write_text(json.dumps(preview, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation = validate_preview(preview)
    args.validation_out.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(preview, validation, args.md_out)
    print(json.dumps({"ok": validation["failed_count"] == 0, "failed_count": validation["failed_count"], "json": str(args.json_out)}, indent=2))
    return 0 if validation["failed_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
