#!/usr/bin/env python3
"""Generate manual review packets for missing service-worker pool registration."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
PACKET_DIR = REPORTS / "worker-pool-registration-review-packets"

SCHEMA_PATH = ARCH / "worker-pool-registration-review-v1.schema.json"
PREFLIGHT = REPORTS / "worker-pool-assignment-preflight-v1-20260617.json"
POOL_REGISTRATION_PLAN = REPORTS / "service-worker-pool-registration-plan-latest.json"

JSON_OUT = REPORTS / "worker-pool-registration-review-v1-20260617.json"
MD_OUT = REPORTS / "worker-pool-registration-review-v1-20260617.md"
VALIDATION_OUT = REPORTS / "worker-pool-registration-review-v1-validation-20260617.json"

TASK_ID = "task-worker-pool-registration-review-v1-20260617"
REVIEW_ID = "worker-pool-registration-review-agent-company-v1-20260617"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slug(value: str) -> str:
    clean = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return clean or "packet"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def priority_for(packet: dict[str, Any]) -> str:
    worker_type = packet["worker_type"]
    count = int(packet["current_request_count"])
    if worker_type == "browser_read_only" or count >= 2:
        return "high"
    if worker_type in {"legal_kyc_tax_payment_review", "model_api_execution", "public_submission"}:
        return "medium"
    return "low"


def route_for(packet: dict[str, Any]) -> str:
    if priority_for(packet) == "low":
        return "manual_review_hold"
    return "manual_review_register_later"


def review_questions(packet: dict[str, Any]) -> list[str]:
    base = [
        "Is this pool needed before the next approved service request?",
        "Who is allowed to own this pool if registered?",
        "What exact approval scope must exist before assignment?",
    ]
    if packet["worker_type"] in {"browser_read_only", "browser_signed_in_read_only"}:
        base.append("Does the pool require signed-in browser state, and how is session safety verified?")
    if packet["worker_type"] == "model_api_execution":
        base.append("What provider, model, maximum cost, input scope, and output artifact path are approved?")
    if packet["worker_type"] in {"legal_kyc_tax_payment_review", "public_submission"}:
        base.append("What user/CRO/reputation review evidence is required before any public or commitment-adjacent action?")
    return base


def build_review() -> dict[str, Any]:
    preflight = load_json(PREFLIGHT)
    plan = load_json(POOL_REGISTRATION_PLAN)
    packets: list[dict[str, Any]] = []
    must_not_do = [
        "do_not_execute_command_preview",
        "do_not_register_pool_without_manual_user_decision",
        "do_not_assign_service_requests",
        "do_not_start_workers",
        "do_not_open_browser_or_use_accounts",
        "do_not_touch_wallet_payment_kyc_tax_or_legal_commitments",
        "do_not_call_model_or_external_api",
    ]
    for source in plan["registration_packets"]:
        packet_id = "pool-review-" + slug(source["worker_pool_id"])
        packets.append(
            {
                "packet_id": packet_id,
                "worker_pool_id": source["worker_pool_id"],
                "worker_type": source["worker_type"],
                "role_id": source["role_id"],
                "department_id": source["department_id"],
                "current_request_count": int(source["current_request_count"]),
                "priority": priority_for(source),
                "decision_route": route_for(source),
                "manual_command_preview": source["register_agent_command_preview_argv"],
                "must_not_do": must_not_do,
                "review_questions": review_questions(source),
            }
        )
    route_counts = Counter(packet["decision_route"] for packet in packets)
    priority_counts = Counter(packet["priority"] for packet in packets)
    return {
        "schema_version": "agent_company.worker_pool_registration_review.v1",
        "review_id": REVIEW_ID,
        "generated_utc": utc_now(),
        "source_preflight_path": str(PREFLIGHT),
        "source_registration_plan_path": str(POOL_REGISTRATION_PLAN),
        "review_packets": packets,
        "summary": {
            "packet_count": len(packets),
            "high_priority_count": priority_counts["high"],
            "manual_register_later_count": route_counts["manual_review_register_later"],
            "manual_hold_count": route_counts["manual_review_hold"],
            "commands_executed": 0,
        },
        "runtime_boundary": {
            "report_only": True,
            "registers_pools": False,
            "assigns_service_requests": False,
            "starts_workers": False,
            "updates_service_requests": False,
            "calls_apis": False,
            "external_side_effects": False,
        },
        "source_preflight_summary": preflight["summary"],
    }


def validate_review(review: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    packets = review["review_packets"]
    packet_ids = [packet["packet_id"] for packet in packets]
    if len(packet_ids) != len(set(packet_ids)):
        failures.append("duplicate_packet_id")
    summary = review["summary"]
    if summary["packet_count"] != 7:
        failures.append(f"packet_count_expected_7_got_{summary['packet_count']}")
    if summary["high_priority_count"] != 2:
        failures.append(f"high_priority_count_expected_2_got_{summary['high_priority_count']}")
    if summary["manual_register_later_count"] != 5:
        failures.append(f"manual_register_later_count_expected_5_got_{summary['manual_register_later_count']}")
    if summary["manual_hold_count"] != 2:
        failures.append(f"manual_hold_count_expected_2_got_{summary['manual_hold_count']}")
    if summary["commands_executed"] != 0:
        failures.append("commands_executed_nonzero")
    for packet in packets:
        if not packet["manual_command_preview"]:
            failures.append(f"missing_command_preview:{packet['packet_id']}")
        if "do_not_execute_command_preview" not in packet["must_not_do"]:
            failures.append(f"missing_do_not_execute:{packet['packet_id']}")
        if len(packet["review_questions"]) < 3:
            failures.append(f"review_questions_too_short:{packet['packet_id']}")
    for key, value in review["runtime_boundary"].items():
        if key == "report_only":
            if value is not True:
                failures.append("runtime_boundary_report_only_not_true")
        elif value is not False:
            failures.append(f"runtime_boundary_not_false:{key}")
    return {
        "schema_version": "agent_company.worker_pool_registration_review_validation.v1",
        "generated_utc": utc_now(),
        "schema_path": str(SCHEMA_PATH),
        "json_path": str(JSON_OUT),
        "markdown_path": str(MD_OUT),
        "packet_dir": str(PACKET_DIR),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "packet_count": summary["packet_count"],
        "high_priority_count": summary["high_priority_count"],
        "manual_register_later_count": summary["manual_register_later_count"],
        "manual_hold_count": summary["manual_hold_count"],
        "commands_executed": summary["commands_executed"],
        "registers_pools": False,
        "assigns_service_requests": False,
        "starts_workers": False,
        "updates_service_requests": False,
        "calls_apis": False,
        "external_side_effects": False,
        "failures": failures,
    }


def write_packet_files(review: dict[str, Any]) -> None:
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    for packet in review["review_packets"]:
        packet_json = PACKET_DIR / f"{packet['packet_id']}.json"
        packet_md = PACKET_DIR / f"{packet['packet_id']}.md"
        packet_json.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        lines = [
            f"# {packet['worker_pool_id']} Registration Review",
            "",
            f"Packet: `{packet['packet_id']}`",
            f"Worker type: `{packet['worker_type']}`",
            f"Role: `{packet['role_id']}`",
            f"Department: `{packet['department_id']}`",
            f"Current request count: `{packet['current_request_count']}`",
            f"Priority: `{packet['priority']}`",
            f"Decision route: `{packet['decision_route']}`",
            "",
            "## Manual Command Preview",
            "",
            "```powershell",
            " ".join(packet["manual_command_preview"]),
            "```",
            "",
            "## Must Not Do",
            "",
        ]
        lines.extend(f"- `{item}`" for item in packet["must_not_do"])
        lines.extend(["", "## Review Questions", ""])
        lines.extend(f"- {item}" for item in packet["review_questions"])
        packet_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_markdown(review: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Worker Pool Registration Review v1",
        "",
        f"Generated UTC: {review['generated_utc']}",
        f"Review: `{review['review_id']}`",
        f"Task: `{TASK_ID}`",
        f"Schema: `{SCHEMA_PATH}`",
        f"JSON: `{JSON_OUT}`",
        f"Validation: `{VALIDATION_OUT}`",
        f"Packet directory: `{PACKET_DIR}`",
        "",
        "## Summary",
        "",
        f"- Review packets: `{validation['packet_count']}`",
        f"- High priority: `{validation['high_priority_count']}`",
        f"- Manual register-later route: `{validation['manual_register_later_count']}`",
        f"- Manual hold route: `{validation['manual_hold_count']}`",
        f"- Commands executed: `{validation['commands_executed']}`",
        f"- Validation failures: `{validation['failure_count']}`",
        "",
        "## Review Packets",
        "",
        "| Priority | Route | Pool | Type | Requests | Packet |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]
    for packet in review["review_packets"]:
        packet_path = PACKET_DIR / f"{packet['packet_id']}.md"
        lines.append(
            f"| `{packet['priority']}` | `{packet['decision_route']}` | `{packet['worker_pool_id']}` | `{packet['worker_type']}` | `{packet['current_request_count']}` | `{packet_path}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This review is report-only.",
            "- It executes no command previews, registers no pools, assigns no service requests, starts no workers, updates no service requests, calls no APIs, and performs no external side effects.",
        ]
    )
    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    review = build_review()
    validation = validate_review(review)
    JSON_OUT.write_text(json.dumps(review, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_OUT.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_packet_files(review)
    write_markdown(review, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "report": str(MD_OUT)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
