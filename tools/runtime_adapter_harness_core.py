"""Deterministic packet and guard primitives for the runtime adapter harness."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "reports" / "runtime-adapters"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def local_path(name: str) -> str:
    return str((OUTPUT_DIR / name).resolve())


def safe_file_fragment(value: str) -> str:
    chars = []
    for char in value.lower():
        if char.isalnum():
            chars.append(char)
        elif char in {"-", "_", "."}:
            chars.append(char)
        else:
            chars.append("-")
    fragment = "".join(chars).strip("-")
    while "--" in fragment:
        fragment = fragment.replace("--", "-")
    return fragment or "item"


def result_file_name(packet_id: str, adapter_id: str) -> str:
    return f"{safe_file_fragment(packet_id)}--{safe_file_fragment(adapter_id)}.json"


def base_packet(packet_id: str, packet_type: str, title: str, objective: str) -> dict[str, Any]:
    return {
        "schema_version": "work_packet.v1",
        "packet_id": packet_id,
        "lane_id": "platform_engineering",
        "task_id": f"task-{packet_id}",
        "requester_agent_id": "runtime-adapter-harness",
        "created_utc": now_utc(),
        "title": title,
        "objective": objective,
        "packet_type": packet_type,
        "execution_mode": "local_only",
        "allowed_actions": [
            "read local files",
            "read local SQLite control plane",
            "write local JSON/Markdown artifacts",
            "emit local trace metadata",
        ],
        "blocked_actions": [
            "browser automation",
            "account login or registration",
            "public posting or submission",
            "wallet or payment action",
            "real-money trade",
            "model/API execution",
        ],
        "required_service_requests": [],
        "approval_requirements": [],
        "context_artifacts": [
            {
                "kind": "report",
                "path_or_url": str((ROOT / "reports" / "agent-company-stack-wave5-20260614.md").resolve()),
                "purpose": "Runtime shortlist and adapter rationale.",
            }
        ],
        "expected_outputs": [
            {
                "kind": "runtime_adapter_result",
                "path": local_path(f"{packet_id}-result.json"),
                "required": True,
            }
        ],
        "success_criteria": [
            "adapter emits a structured result",
            "adapter records no external side effects",
            "adapter preserves all blocked actions",
        ],
        "external_side_effects_allowed": False,
        "real_money_allowed": False,
        "public_action_allowed": False,
        "metadata": {
            "span_kind": "local_eval",
            "runtime": "runtime_adapter_harness",
            "api_calls": False,
        },
    }


def synthetic_packets() -> list[dict[str, Any]]:
    safe = base_packet(
        "packet-safe-local-research",
        "local_research",
        "Safe local research synthesis",
        "Summarize a local report and emit a deterministic adapter result without external actions.",
    )

    browser = base_packet(
        "packet-browser-readonly-needs-review",
        "browser_read_only",
        "Browser read-only request without approval",
        "Attempt to prepare a browser read-only research step that must stop because service approval is missing.",
    )
    browser["execution_mode"] = "requires_service_approval"
    browser["required_service_requests"] = ["req-example-browser-read-only"]
    browser["approval_requirements"] = [
        {
            "gate": "browser_read_only_session",
            "decision_owner": "user_or_cro",
            "approval_status": "needs_review",
            "scope": "Read-only web check; no login, forms, comments, or submissions.",
        }
    ]

    money = base_packet(
        "packet-real-money-public-action-refusal",
        "real_money_action",
        "Real-money public action refusal",
        "Refuse a packet that tries to mix real-money and public action without approvals.",
    )
    money["execution_mode"] = "requires_service_approval"
    money["required_service_requests"] = ["req-example-real-money-trade", "req-example-public-action"]
    money["approval_requirements"] = [
        {
            "gate": "real_money_trade_gate",
            "decision_owner": "user_only",
            "approval_status": "needs_review",
            "scope": "Any trade, deposit, withdrawal, or payment action.",
        },
        {
            "gate": "public_action_execution",
            "decision_owner": "user_or_cro",
            "approval_status": "needs_review",
            "scope": "Any public post, comment, PR, bounty claim, or marketplace submission.",
        },
    ]
    money["blocked_actions"].extend(["deposit", "withdrawal", "public bounty claim"])

    return [safe, browser, money]


def load_packet_file(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Packet file must contain one JSON object: {path}")
    return payload


def load_packet_files(paths: list[str] | None) -> list[dict[str, Any]]:
    if not paths:
        return synthetic_packets()
    return [load_packet_file(Path(path)) for path in paths]


def validate_packet(packet: dict[str, Any]) -> list[str]:
    required = [
        "schema_version",
        "packet_id",
        "lane_id",
        "task_id",
        "requester_agent_id",
        "created_utc",
        "title",
        "objective",
        "packet_type",
        "execution_mode",
        "allowed_actions",
        "blocked_actions",
        "required_service_requests",
        "approval_requirements",
        "context_artifacts",
        "expected_outputs",
        "success_criteria",
        "external_side_effects_allowed",
        "real_money_allowed",
        "public_action_allowed",
        "metadata",
    ]
    errors: list[str] = []
    for key in required:
        if key not in packet:
            errors.append(f"missing:{key}")
    if packet.get("schema_version") != "work_packet.v1":
        errors.append("schema_version_not_work_packet_v1")
    if not packet.get("blocked_actions"):
        errors.append("blocked_actions_empty")
    if packet.get("external_side_effects_allowed") is not False:
        errors.append("external_side_effects_must_default_false")
    if packet.get("real_money_allowed") is not False:
        errors.append("real_money_must_default_false")
    if packet.get("public_action_allowed") is not False:
        errors.append("public_action_must_default_false")
    metadata = packet.get("metadata") or {}
    if metadata.get("api_calls") is not False:
        errors.append("metadata_api_calls_must_be_false")
    if not packet.get("expected_outputs"):
        errors.append("expected_outputs_empty")
    return errors


@dataclass(frozen=True)
class AdapterResult:
    adapter_id: str
    packet_id: str
    status: str
    action: str
    reason: str
    external_side_effects: bool
    api_calls: bool
    artifact_plan: list[str]
    preserved_blocked_actions: list[str]
    trace_metadata: dict[str, Any]
    runtime_details: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "packet_id": self.packet_id,
            "status": self.status,
            "action": self.action,
            "reason": self.reason,
            "external_side_effects": self.external_side_effects,
            "api_calls": self.api_calls,
            "artifact_plan": self.artifact_plan,
            "preserved_blocked_actions": self.preserved_blocked_actions,
            "trace_metadata": self.trace_metadata,
            "runtime_details": self.runtime_details,
        }


def approval_statuses(packet: dict[str, Any]) -> list[str]:
    return [str(item.get("approval_status", "")) for item in packet.get("approval_requirements", [])]


def must_refuse(packet: dict[str, Any]) -> tuple[bool, str]:
    if packet.get("real_money_allowed") or packet.get("public_action_allowed"):
        return True, "packet unexpectedly allows money/public actions"
    if packet.get("packet_type") in {"real_money_action", "public_action", "security_report"}:
        return True, "packet type is externally consequential"
    if packet.get("required_service_requests") and "approved" not in approval_statuses(packet):
        return True, "required service request is not approved"
    return False, ""


def make_result(adapter_id: str, packet: dict[str, Any], action: str, reason: str) -> AdapterResult:
    refused = action == "refuse"
    status = "refused_safely" if refused else "prepared_local_artifact"
    return AdapterResult(
        adapter_id=adapter_id,
        packet_id=packet["packet_id"],
        status=status,
        action=action,
        reason=reason,
        external_side_effects=False,
        api_calls=False,
        artifact_plan=[item["path"] for item in packet.get("expected_outputs", [])],
        preserved_blocked_actions=list(packet.get("blocked_actions", [])),
        trace_metadata={
            "span_kind": "runtime_adapter_eval",
            "runtime": adapter_id,
            "api_calls": False,
            "packet_id": packet["packet_id"],
        },
        runtime_details={},
    )