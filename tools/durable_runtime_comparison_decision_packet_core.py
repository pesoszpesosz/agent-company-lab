#!/usr/bin/env python3
"""Validate durable runtime comparison decision packets without starting runtimes."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DURABLE_REPORTS = ROOT / "reports" / "durable-orchestration"
DEFAULT_PACKET = DURABLE_REPORTS / "durable-runtime-comparison-decision-packet-v1-20260617.json"
DEFAULT_SCHEMA = ROOT / "architecture" / "durable-runtime-comparison-decision-packet-v1.schema.json"
DEFAULT_JSON_OUT = DURABLE_REPORTS / "durable-runtime-comparison-decision-packet-v1-validation-20260617.json"
DEFAULT_MD_OUT = DURABLE_REPORTS / "durable-runtime-comparison-decision-packet-v1-20260617.md"

REQUIRED_RUNTIME_IDS = {
    "sqlite_control_plane",
    "temporal_python",
    "inngest",
    "dbos_python",
    "pydantic_ai_durable_execution",
    "prefect",
    "restate",
}

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


def source_validation_ok(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing"
    doc = load_json(path)
    if doc.get("failed_count") != 0:
        return False, f"failed_count={doc.get('failed_count')}"
    boundary = doc.get("runtime_boundary") or doc.get("artifact_actions") or {}
    raw = json.dumps(boundary).lower()
    forbidden_true = [
        '"api_calls": true',
        '"model_api_calls": true',
        '"external_side_effects": true',
        '"public_actions": true',
        '"database_provisioning": true',
        '"dbos_launch_called": true',
        '"prefect_cloud_calls": 1',
    ]
    if any(token in raw for token in forbidden_true):
        return False, "runtime boundary contains forbidden true side-effect field"
    return True, "ok"




def build_result(
    packet: dict[str, Any],
    *,
    packet_path: Path,
    schema_path: Path,
    json_path: Path,
    markdown_path: Path,
) -> dict[str, Any]:
    top_failures: list[str] = []
    source_rows = []
    if packet.get("schema_version") != "agent_company.durable_runtime_comparison_decision_packet.v1":
        top_failures.append("schema_version mismatch")
    if packet.get("task_id") != "task-durable-runtime-comparison-decision-packet-v1-20260617":
        top_failures.append("task_id mismatch")
    if not schema_path.exists():
        top_failures.append("schema path is missing")

    for field, expected in ZERO_RUNTIME_BOUNDARY.items():
        if (packet.get("runtime_boundary") or {}).get(field) != expected:
            top_failures.append(f"runtime_boundary.{field} must be {expected!r}")

    for raw_path in packet.get("source_validation_paths", []):
        path = Path(raw_path)
        ok, status = source_validation_ok(path)
        source_rows.append({"path": str(path), "ok": ok, "status": status})
        if not ok:
            top_failures.append(f"source validation not clean: {path} ({status})")

    runtime_rows = packet.get("runtime_recommendations", [])
    runtime_ids = {row.get("runtime_id") for row in runtime_rows}
    missing = sorted(REQUIRED_RUNTIME_IDS - runtime_ids)
    extra = sorted(runtime_ids - REQUIRED_RUNTIME_IDS)
    if missing:
        top_failures.append(f"missing runtime recommendations: {', '.join(missing)}")
    if extra:
        top_failures.append(f"unexpected runtime recommendations: {', '.join(extra)}")

    sqlite_rows = [row for row in runtime_rows if row.get("runtime_id") == "sqlite_control_plane"]
    if not sqlite_rows or sqlite_rows[0].get("rank") != 1 or sqlite_rows[0].get("decision") != "promote_now_local_only":
        top_failures.append("sqlite_control_plane must be rank 1 and promote_now_local_only")

    for row in runtime_rows:
        runtime_id = row.get("runtime_id")
        if runtime_id != "sqlite_control_plane" and not row.get("required_gates_before_execution"):
            top_failures.append(f"{runtime_id} must have approval gates before execution")
        if runtime_id != "sqlite_control_plane" and str(row.get("decision", "")).startswith("promote"):
            top_failures.append(f"{runtime_id} cannot be promoted for execution now")

    first_step = (packet.get("implementation_sequence") or [{}])[0]
    if first_step.get("build_id") != "sqlite_outbox_acknowledgement_runner_v1":
        top_failures.append("first implementation step must be sqlite_outbox_acknowledgement_runner_v1")
    if packet.get("next_local_test") != "sqlite_outbox_acknowledgement_runner_v1_without_service_request_mutation":
        top_failures.append("next_local_test mismatch")

    failed_count = 1 if top_failures else 0
    return {
        "schema_version": "agent_company.durable_runtime_comparison_decision_packet_validation.v1",
        "generated_utc": utc_now(),
        "packet_path": str(packet_path),
        "schema_path": str(schema_path),
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "source_validations_checked": len(source_rows),
        "source_rows": source_rows,
        "runtime_recommendations_checked": len(runtime_rows),
        "failed_count": failed_count,
        "top_level_failures": top_failures,
        "runtime_boundary": packet.get("runtime_boundary"),
        "next_local_test": packet.get("next_local_test"),
    }
