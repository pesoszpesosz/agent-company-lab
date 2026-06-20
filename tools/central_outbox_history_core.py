#!/usr/bin/env python3
"""Validate central outbox/history fixtures without external side effects."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DEFAULT_FIXTURE = ROOT / "reports" / "agent-company-central-outbox-history-v1-20260617.json"
DEFAULT_JSON_OUT = ROOT / "reports" / "agent-company-central-outbox-history-validation-20260617.json"
DEFAULT_MD_OUT = ROOT / "reports" / "agent-company-central-outbox-history-v1-20260617.md"
DEFAULT_SCHEMA = ROOT / "architecture" / "central-outbox-history-v1.schema.json"

REQUIRED_PROHIBITIONS = {
    "account_action",
    "payment_action",
    "public_action",
    "real_money_action",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_message(message: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if not message["message_id"].startswith("msg-"):
        failures.append("message_id must start with msg-")
    if message.get("external_side_effects") is not False:
        failures.append("external_side_effects must be false")
    prohibited = set(message.get("prohibited_actions") or [])
    missing = sorted(REQUIRED_PROHIBITIONS - prohibited)
    if missing:
        failures.append(f"missing required prohibitions: {', '.join(missing)}")
    if message["approval_posture"] != "local_only" and "service_request_mutation" not in prohibited:
        failures.append("non-local-only messages must prohibit service_request_mutation")
    if message["approval_posture"] in {"needs_human_review", "needs_cro_review", "approved_scope_required"}:
        if not message.get("service_request_id"):
            failures.append("review-gated message should reference a service_request_id")
    if message["recipient_type"] == "agent" and not message["recipient_id"].startswith("lane-manager-"):
        failures.append("agent recipient_id should reference a lane-manager agent")
    if message["replay_status"] not in {"queued", "delivered", "acknowledged", "superseded", "cancelled"}:
        failures.append("invalid replay_status")
    return failures




def build_result(
    fixture: dict[str, Any],
    *,
    fixture_path: Path,
    schema_path: Path,
    json_path: Path,
    markdown_path: Path,
) -> dict[str, Any]:
    rows = []
    ids: set[str] = set()
    for message in fixture["messages"]:
        failures = validate_message(message)
        if message["message_id"] in ids:
            failures.append("duplicate message_id")
        ids.add(message["message_id"])
        rows.append(
            {
                "message_id": message["message_id"],
                "lane_id": message["lane_id"],
                "message_type": message["message_type"],
                "approval_posture": message["approval_posture"],
                "replay_status": message["replay_status"],
                "failures": failures,
            }
        )
    failed_count = sum(1 for row in rows if row["failures"])
    return {
        "schema_version": "agent_company.central_outbox_history_validation.v1",
        "generated_utc": utc_now(),
        "fixture_path": str(fixture_path),
        "schema_path": str(schema_path),
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "messages_checked": len(rows),
        "passed_count": len(rows) - failed_count,
        "failed_count": failed_count,
        "external_side_effects": False,
        "rows": rows,
    }
