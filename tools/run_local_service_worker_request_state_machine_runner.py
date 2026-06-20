#!/usr/bin/env python3
"""Build and validate a local service-worker request state-machine preview."""

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
DEFAULT_DECISION = ROOT / "reports" / "durable-orchestration" / "durable-runtime-comparison-decision-packet-v1-20260617.json"
DEFAULT_ACK_VALIDATION = ROOT / "reports" / "durable-orchestration" / "sqlite-outbox-acknowledgement-runner-v1-validation-20260617.json"
DEFAULT_SERVICE_QUEUE = ROOT / "reports" / "service-worker-request-queue-latest.json"
DEFAULT_JSON_OUT = ROOT / "reports" / "durable-orchestration" / "local-service-worker-request-state-machine-runner-v1-20260617.json"
DEFAULT_VALIDATION_OUT = ROOT / "reports" / "durable-orchestration" / "local-service-worker-request-state-machine-runner-v1-validation-20260617.json"
DEFAULT_MD_OUT = ROOT / "reports" / "durable-orchestration" / "local-service-worker-request-state-machine-runner-v1-20260617.md"
SCHEMA_PATH = ROOT / "architecture" / "local-service-worker-request-state-machine-runner-v1.schema.json"

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

TERMINAL_STATUSES = {"complete", "rejected", "blocked"}
PARKED_STATUSES = {"draft", "needs_review"}
APPROVED_STATUSES = {"approved", "assigned", "in_progress"}

ZERO_RUNTIME_BOUNDARY = {
    "dependency_installs": 0,
    "dependency_imports": 0,
    "runtime_starts": 0,
    "queue_enqueues": 0,
    "outbox_rows_updated": 0,
    "service_requests_updated": 0,
    "service_requests_assigned": 0,
    "service_requests_started": 0,
    "service_requests_completed": 0,
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


def db_counts(path: Path) -> dict[str, int]:
    con = sqlite3.connect(path)
    try:
        return {table: con.execute(f"select count(*) from {table}").fetchone()[0] for table in COUNT_TABLES}
    finally:
        con.close()


def service_request_rows(path: Path) -> dict[str, dict[str, Any]]:
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    try:
        return {row["request_id"]: dict(row) for row in con.execute("select * from service_requests")}
    finally:
        con.close()


def fingerprint(*parts: object) -> str:
    return hashlib.sha1("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:16]


def missing_or_false(value: dict[str, Any], key: str) -> bool:
    return value.get(key) is not False


def approval_scope_is_execution_authority(scope: str | None) -> bool:
    if not scope:
        return False
    lowered = scope.lower()
    blocked_markers = [
        "backfill only",
        "no approval granted",
        "local conversion artifact only",
        "not approved yet",
        "grants no new approval",
    ]
    return not any(marker in lowered for marker in blocked_markers)


def safety_failures(request: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for key in [
        "external_side_effects_allowed",
        "real_money_allowed",
        "public_action_allowed",
        "account_or_identity_action_allowed",
        "model_or_api_cost_allowed",
    ]:
        if missing_or_false(request, key):
            failures.append(f"{key}_not_false")
    if float(request.get("max_cost_usd") or 0) != 0:
        failures.append("max_cost_usd_not_zero")
    if request.get("metadata", {}).get("external_side_effects") is not False:
        failures.append("metadata.external_side_effects_not_false")
    if request.get("metadata", {}).get("browser_opened") is not False:
        failures.append("metadata.browser_opened_not_false")
    if request.get("metadata", {}).get("api_calls") is not False:
        failures.append("metadata.api_calls_not_false")
    return failures


def transition_for(
    item: dict[str, Any],
    db_service_requests: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    request = item.get("request", item)
    worker_request_id = request["worker_request_id"]
    source_service_request_id = request["source_service_request_id"]
    worker_status = request["status"]
    approval_snapshot = request["approval_status_snapshot"]
    db_row = db_service_requests.get(source_service_request_id)
    db_status = db_row.get("status") if db_row else None
    failures: list[str] = []
    warnings: list[str] = []

    if db_row is None:
        failures.append("source_service_request_missing_in_db")
    if db_status and db_status != worker_status:
        failures.append("worker_status_mismatches_db_status")
    if approval_snapshot != worker_status:
        failures.append("approval_status_snapshot_mismatches_worker_status")
    failures.extend(safety_failures(request))

    scope_authorizes_execution = approval_scope_is_execution_authority(request.get("approval_scope"))
    command_preview: list[str] = []

    if worker_status in TERMINAL_STATUSES:
        proposed_state = worker_status
        disposition = "terminal_noop"
        safe_to_preview_assignment = False
        safe_to_preview_start = False
        command_preview = ["no_op_terminal_state"]
    elif worker_status in PARKED_STATUSES:
        proposed_state = worker_status
        disposition = "parked_awaiting_human_review"
        safe_to_preview_assignment = False
        safe_to_preview_start = False
        command_preview = ["keep_parked"]
        if scope_authorizes_execution:
            warnings.append("parked_status_has_execution_like_scope_text")
    elif worker_status in APPROVED_STATUSES:
        if not scope_authorizes_execution:
            failures.append("approved_like_status_without_execution_scope")
        proposed_state = worker_status
        disposition = "preview_assignment_or_start_only" if scope_authorizes_execution else "park_until_scope_fixed"
        safe_to_preview_assignment = worker_status == "approved" and not failures
        safe_to_preview_start = worker_status in {"assigned", "in_progress"} and not failures
        command_preview = ["preview_assign_worker" if safe_to_preview_assignment else "preview_start_or_continue_worker" if safe_to_preview_start else "park_until_scope_fixed"]
    else:
        proposed_state = worker_status
        disposition = "unknown_status_parked"
        safe_to_preview_assignment = False
        safe_to_preview_start = False
        failures.append("unknown_worker_status")

    return {
        "transition_id": "swr-transition-" + fingerprint(worker_request_id, worker_status, source_service_request_id),
        "worker_request_id": worker_request_id,
        "source_service_request_id": source_service_request_id,
        "lane_id": request.get("requesting_lane_id"),
        "worker_type": request.get("worker_type"),
        "service_id": request.get("service_id"),
        "risk_gate": request.get("risk_gate"),
        "source_json_path": item.get("json_path"),
        "db_status_snapshot": db_status,
        "worker_status_snapshot": worker_status,
        "approval_status_snapshot": approval_snapshot,
        "proposed_state": proposed_state,
        "disposition": disposition,
        "safe_to_preview_assignment": safe_to_preview_assignment,
        "safe_to_preview_start": safe_to_preview_start,
        "command_preview": command_preview,
        "writes_to_db": False,
        "mutates_service_request": False,
        "starts_worker": False,
        "external_side_effects": False,
        "actual_failures": sorted(set(failures)),
        "warnings": sorted(set(warnings)),
    }


def make_probe_request(probe_id: str, status: str, approval_scope: str, **overrides: Any) -> dict[str, Any]:
    request: dict[str, Any] = {
        "worker_request_id": f"swr-{probe_id}",
        "source_service_request_id": f"req-{probe_id}",
        "requesting_lane_id": "platform_engineering",
        "worker_type": "browser_read_only",
        "service_id": "browser_read_only_session",
        "risk_gate": "probe_no_external_action",
        "status": status,
        "approval_status_snapshot": status,
        "approval_scope": approval_scope,
        "external_side_effects_allowed": False,
        "real_money_allowed": False,
        "public_action_allowed": False,
        "account_or_identity_action_allowed": False,
        "model_or_api_cost_allowed": False,
        "max_cost_usd": 0,
        "metadata": {
            "external_side_effects": False,
            "browser_opened": False,
            "api_calls": False,
        },
    }
    request.update(overrides)
    return {
        "json_path": f"probe://{probe_id}",
        "request": request,
    }


def policy_probe_cases() -> list[dict[str, Any]]:
    cases = [
        {
            "probe_id": "probe-approved-readonly-preview-only",
            "input_status": "approved",
            "approval_scope": "Explicit read-only browser capture approval for one named URL and one local output artifact.",
            "expected_disposition": "preview_assignment_or_start_only",
            "expected_command": "preview_assign_worker",
        },
        {
            "probe_id": "probe-needs-review-cannot-start",
            "input_status": "needs_review",
            "approval_scope": "Backfill only. No approval granted.",
            "expected_disposition": "parked_awaiting_human_review",
            "expected_command": "keep_parked",
        },
        {
            "probe_id": "probe-complete-never-revives",
            "input_status": "complete",
            "approval_scope": "Terminal ledger row.",
            "expected_disposition": "terminal_noop",
            "expected_command": "no_op_terminal_state",
        },
        {
            "probe_id": "probe-rejected-never-revives",
            "input_status": "rejected",
            "approval_scope": "Terminal rejected ledger row.",
            "expected_disposition": "terminal_noop",
            "expected_command": "no_op_terminal_state",
        },
        {
            "probe_id": "probe-approved-public-action-without-scope-stays-parked",
            "input_status": "approved",
            "approval_scope": "No approval granted. This row is a local conversion artifact only.",
            "expected_disposition": "park_until_scope_fixed",
            "expected_command": "park_until_scope_fixed",
        },
    ]
    probes: list[dict[str, Any]] = []
    for case in cases:
        request = make_probe_request(case["probe_id"], case["input_status"], case["approval_scope"])
        db_snapshot = {
            request["request"]["source_service_request_id"]: {
                "status": case["input_status"],
            }
        }
        transition = transition_for(request, db_snapshot)
        actual_command = transition["command_preview"][0] if transition["command_preview"] else ""
        probes.append(
            {
                **case,
                "actual_disposition": transition["disposition"],
                "actual_command": actual_command,
                "writes_to_db": transition["writes_to_db"],
                "starts_worker": transition["starts_worker"],
                "actual_failures": transition["actual_failures"],
                "matches_expected": (
                    transition["disposition"] == case["expected_disposition"]
                    and actual_command == case["expected_command"]
                    and transition["writes_to_db"] is False
                    and transition["starts_worker"] is False
                ),
            }
        )
    return probes


def validate_preview(preview: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    for field, expected in ZERO_RUNTIME_BOUNDARY.items():
        if preview["runtime_boundary"].get(field) != expected:
            failures.append(f"runtime_boundary.{field} must be {expected!r}")
    if preview["db_counts_before"] != preview["db_counts_after"]:
        failures.append("db_counts_changed")
    if not preview["transition_previews"]:
        failures.append("transition_previews_missing")

    seen_transition_ids: set[str] = set()
    status_counts: dict[str, int] = {}
    disposition_counts: dict[str, int] = {}
    for transition in preview["transition_previews"]:
        seen_transition_ids.add(transition["transition_id"])
        status_counts[transition["worker_status_snapshot"]] = status_counts.get(transition["worker_status_snapshot"], 0) + 1
        disposition_counts[transition["disposition"]] = disposition_counts.get(transition["disposition"], 0) + 1
        for key in ["writes_to_db", "mutates_service_request", "starts_worker", "external_side_effects"]:
            if transition[key] is not False:
                failures.append(f"{transition['worker_request_id']}:{key}_not_false")
        if transition["worker_status_snapshot"] in TERMINAL_STATUSES and transition["disposition"] != "terminal_noop":
            failures.append(f"{transition['worker_request_id']}:terminal_not_noop")
        if transition["worker_status_snapshot"] in PARKED_STATUSES and transition["disposition"] != "parked_awaiting_human_review":
            failures.append(f"{transition['worker_request_id']}:parked_status_not_parked")
        if transition["actual_failures"]:
            failures.append(f"{transition['worker_request_id']}:transition_failures:{','.join(transition['actual_failures'])}")
    if len(seen_transition_ids) != len(preview["transition_previews"]):
        failures.append("duplicate_transition_id")
    for probe in preview["policy_probes"]:
        if probe.get("matches_expected") is not True:
            failures.append(f"{probe.get('probe_id')}:policy_probe_mismatch")

    return {
        "schema_version": "agent_company.local_service_worker_request_state_machine_runner_validation.v1",
        "generated_utc": utc_now(),
        "preview_path": str(DEFAULT_JSON_OUT),
        "schema_path": str(SCHEMA_PATH),
        "json_path": str(DEFAULT_VALIDATION_OUT),
        "markdown_path": str(DEFAULT_MD_OUT),
        "transition_count": len(preview["transition_previews"]),
        "policy_probe_count": len(preview["policy_probes"]),
        "status_counts": status_counts,
        "disposition_counts": disposition_counts,
        "failed_count": 1 if failures else 0,
        "top_level_failures": failures,
        "runtime_boundary": preview["runtime_boundary"],
        "db_counts_before": preview["db_counts_before"],
        "db_counts_after": preview["db_counts_after"],
        "next_local_test": preview["next_local_test"],
    }


def write_markdown(preview: dict[str, Any], validation: dict[str, Any], path: Path) -> None:
    lines = [
        "# Local Service-Worker Request State-Machine Runner Preview v1",
        "",
        f"Generated UTC: {preview['generated_utc']}",
        f"Preview JSON: `{DEFAULT_JSON_OUT}`",
        f"Validation JSON: `{DEFAULT_VALIDATION_OUT}`",
        f"Schema: `{SCHEMA_PATH}`",
        "",
        "## Summary",
        "",
        f"- Transitions checked: `{validation['transition_count']}`",
        f"- Policy probes checked: `{validation['policy_probe_count']}`",
        f"- Failed: `{validation['failed_count']}`",
        f"- DB counts changed: `{str(preview['db_counts_before'] != preview['db_counts_after']).lower()}`",
        f"- Service requests updated: `{preview['runtime_boundary']['service_requests_updated']}`",
        f"- Service requests assigned: `{preview['runtime_boundary']['service_requests_assigned']}`",
        f"- Worker starts: `{preview['runtime_boundary']['worker_starts']}`",
        f"- Browser sessions: `{preview['runtime_boundary']['browser_sessions_started']}`",
        f"- External side effects: `{str(preview['runtime_boundary']['external_side_effects']).lower()}`",
        "",
        "## Transition Preview",
        "",
        "| Worker Request | Status | Disposition | Assignment Preview | Start Preview | Command |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for transition in preview["transition_previews"]:
        lines.append(
            f"| `{transition['worker_request_id']}` | `{transition['worker_status_snapshot']}` | `{transition['disposition']}` | `{str(transition['safe_to_preview_assignment']).lower()}` | `{str(transition['safe_to_preview_start']).lower()}` | `{', '.join(transition['command_preview'])}` |"
        )
    lines.extend(
        [
            "",
            "## Policy Probes",
            "",
            "| Probe | Status | Expected Disposition | Expected Command |",
            "| --- | --- | --- | --- |",
        ]
    )
    for probe in preview["policy_probes"]:
        lines.append(
            f"| `{probe['probe_id']}` | `{probe['input_status']}` | `{probe['expected_disposition']}` | `{probe['expected_command']}` |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "This preview proves the local state-machine semantics before any service-worker execution exists. Current queue rows remain parked or terminal. A future approved row may preview assignment/start commands, but this runner still does not write back to the database or start a worker.",
            "",
            "## Boundary",
            "",
            "- No service-request update, assignment, start, completion, or rejection.",
            "- No worker start, browser session, queue enqueue, outbox update, dependency import/install, runtime start, API/model call, public/account/wallet/payment/security/real-money action, or external side effect.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DB_PATH)
    parser.add_argument("--decision", type=Path, default=DEFAULT_DECISION)
    parser.add_argument("--ack-validation", type=Path, default=DEFAULT_ACK_VALIDATION)
    parser.add_argument("--service-queue", type=Path, default=DEFAULT_SERVICE_QUEUE)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_OUT)
    parser.add_argument("--validation-out", type=Path, default=DEFAULT_VALIDATION_OUT)
    parser.add_argument("--md-out", type=Path, default=DEFAULT_MD_OUT)
    args = parser.parse_args()

    counts_before = db_counts(args.db)
    decision = load_json(args.decision)
    ack_validation = load_json(args.ack_validation)
    queue = load_json(args.service_queue)
    db_service_requests = service_request_rows(args.db)
    transitions = [transition_for(item, db_service_requests) for item in queue.get("worker_requests", [])]
    counts_after = db_counts(args.db)

    preview = {
        "schema_version": "agent_company.local_service_worker_request_state_machine_runner_preview.v1",
        "generated_utc": utc_now(),
        "task_id": "task-local-service-worker-request-state-machine-runner-v1-20260617",
        "lane_id": "platform_engineering",
        "owner_agent_id": "recovered-profitable-edge-infra",
        "source_decision_path": str(args.decision),
        "source_acknowledgement_validation_path": str(args.ack_validation),
        "source_service_worker_queue_path": str(args.service_queue),
        "runner_policy": {
            "mode": "preview_only",
            "decision_status": decision.get("decision_summary", {}).get("status"),
            "ack_validation_failed_count": ack_validation.get("failed_count"),
            "queue_approval_granted_by_report": queue.get("approval_granted_by_report"),
            "approved_request_rule": "preview_assignment_or_start_only",
            "needs_review_rule": "parked_awaiting_human_review",
            "terminal_rule": "terminal_noop_never_revive",
            "write_back_allowed": False,
            "service_request_mutation_allowed": False,
            "worker_start_allowed": False,
        },
        "db_counts_before": counts_before,
        "db_counts_after": counts_after,
        "transition_previews": transitions,
        "policy_probes": policy_probe_cases(),
        "runtime_boundary": ZERO_RUNTIME_BOUNDARY.copy(),
        "next_local_test": "runtime_implementation_human_approval_packet_v2_before_any_external_runtime",
    }
    args.json_out.write_text(json.dumps(preview, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation = validate_preview(preview)
    args.validation_out.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(preview, validation, args.md_out)
    print(json.dumps({"ok": validation["failed_count"] == 0, "failed_count": validation["failed_count"], "json": str(args.json_out)}, indent=2))
    return 0 if validation["failed_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
