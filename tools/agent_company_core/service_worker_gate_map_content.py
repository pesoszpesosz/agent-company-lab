from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .utils import md_cell


GATE_ORDER = [
    "packet_valid",
    "human_cro_review_candidate",
    "service_status_approved_or_assigned",
    "scope_compatible_with_packet",
    "pool_registered",
    "execution_readiness_ready",
    "assignable_now",
]

GATE_MAP_EXECUTION_NOTICE = (
    "Gate map only. It grants no approval, registers no pool, assigns no service request, "
    "updates no service request, and starts nothing."
)


def _sorted_counts(entries: list[dict[str, Any]], key: str, unknown_value: str | None = None) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in entries:
        value = entry.get(key)
        if value is None and unknown_value is not None:
            value = unknown_value
        counts[str(value)] = counts.get(str(value), 0) + 1
    return dict(sorted(counts.items()))


def build_service_worker_gate_map_payload(
    *,
    generated_utc: str,
    db_path: Path,
    filters: dict[str, Any],
    entries: list[dict[str, Any]],
    gate_counts: dict[str, int],
    status_counts: dict[str, int],
    worker_type_counts: dict[str, int],
    pool_status_counts: dict[str, int],
    ready_for_assignment_count: int,
) -> dict[str, Any]:
    return {
        "schema_version": "service_worker_gate_map.v1",
        "generated_utc": generated_utc,
        "db": str(db_path),
        "filters": filters,
        "mapped_count": len(entries),
        "ready_for_assignment_count": ready_for_assignment_count,
        "gate_counts": gate_counts,
        "status_counts": status_counts,
        "worker_type_counts": worker_type_counts,
        "pool_status_counts": pool_status_counts,
        "gate_map": entries,
        "gate_order": GATE_ORDER,
        "execution_notice": GATE_MAP_EXECUTION_NOTICE,
        "approval_granted_by_gate_map": False,
        "pools_registered_by_gate_map": 0,
        "service_requests_assigned_by_gate_map": 0,
        "service_requests_updated_by_gate_map": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }


def build_service_worker_gate_map_validation_payload(
    *,
    generated_utc: str,
    json_output_path: Path,
    entries: list[dict[str, Any]],
    gate_counts: dict[str, int],
    status_counts: dict[str, int],
    worker_type_counts: dict[str, int],
    pool_status_counts: dict[str, int],
    ready_for_assignment_count: int,
) -> dict[str, Any]:
    return {
        "schema_version": "service_worker_gate_map_validation.v1",
        "generated_utc": generated_utc,
        "gate_map_path": str(json_output_path),
        "mapped_count": len(entries),
        "ready_for_assignment_count": ready_for_assignment_count,
        "all_rows_no_approval": all(not entry["approval_granted_by_gate_map"] for entry in entries),
        "all_rows_no_registration": all(not entry["pool_registered_by_gate_map"] for entry in entries),
        "all_rows_no_assignment": all(not entry["service_request_assigned_by_gate_map"] for entry in entries),
        "approval_granted_by_gate_map": False,
        "pools_registered_by_gate_map": 0,
        "service_requests_assigned_by_gate_map": 0,
        "service_requests_updated_by_gate_map": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
        "gate_counts": gate_counts,
        "status_counts": status_counts,
        "worker_type_counts": worker_type_counts,
        "pool_status_counts": pool_status_counts,
    }


def render_service_worker_gate_map_markdown(
    *,
    generated_utc: str,
    db_path: Path,
    json_output_path: Path,
    validation_path: Path,
    entries: list[dict[str, Any]],
    validation_payload: dict[str, Any],
    ready_for_assignment_count: int,
) -> str:
    lines = [
        "# Service Worker Gate Map",
        "",
        f"Generated UTC: {generated_utc}",
        f"Database: `{db_path}`",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Operating Rule",
        "",
        "This report maps each service-worker request to its current blocking gate. It grants no approval and does not register pools, assign, start, complete, enqueue, update, browse, call APIs, post, submit, register accounts, trade, spend, or contact anyone.",
        "",
        f"- Requests mapped: `{len(entries)}`",
        f"- Ready for assignment: `{ready_for_assignment_count}`",
        f"- Gate counts: `{json.dumps(validation_payload['gate_counts'], sort_keys=True)}`",
        f"- Pool status counts: `{json.dumps(validation_payload['pool_status_counts'], sort_keys=True)}`",
        "- Pools registered by gate map: `0`",
        "- Service requests assigned by gate map: `0`",
        "- Worker starts: `0`",
        "- API calls: `False`",
        "- External side effects: `False`",
        "",
        "## Request Gates",
        "",
        "| Status | Blocking Gate | Request | Worker Type | Pool | Pool Status | Next Action |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{entry['service_status']}`",
                    f"`{entry['current_blocking_gate']}`",
                    f"`{entry['source_service_request_id']}`",
                    f"`{entry.get('worker_type') or ''}`",
                    f"`{entry['recommended_worker_pool_id']}`",
                    f"`{entry.get('pool_status') or ''}`",
                    md_cell(entry["next_action"], 260),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Gate Order",
            "",
            "1. Packet must be valid.",
            "2. Human/CRO review must be ready.",
            "3. Service request must be separately approved or assigned.",
            "4. Exact approval scope must be compatible with the packet.",
            "5. Required service-worker pool must be registered.",
            "6. Execution-readiness verifier must pass.",
            "7. Assignment must still be a separate manual action.",
            "",
            "## Next Action",
            "",
            "Use this gate map as the CEO/CRO board for deciding which local preparation step comes next. Current requests should not be assigned or started until every prior gate is explicitly satisfied in the generated reports.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def build_service_worker_gate_map_artifacts(
    *,
    generated_utc: str,
    db_path: Path,
    filters: dict[str, Any],
    entries: list[dict[str, Any]],
    json_output_path: Path,
    validation_path: Path,
) -> dict[str, Any]:
    gate_counts = _sorted_counts(entries, "current_blocking_gate")
    status_counts = _sorted_counts(entries, "service_status")
    worker_type_counts = _sorted_counts(entries, "worker_type", "unknown")
    pool_status_counts = _sorted_counts(entries, "pool_status", "unknown")
    ready_for_assignment_count = gate_counts.get("ready_for_manual_assignment_but_report_grants_no_authority", 0)
    payload = build_service_worker_gate_map_payload(
        generated_utc=generated_utc,
        db_path=db_path,
        filters=filters,
        entries=entries,
        gate_counts=gate_counts,
        status_counts=status_counts,
        worker_type_counts=worker_type_counts,
        pool_status_counts=pool_status_counts,
        ready_for_assignment_count=ready_for_assignment_count,
    )
    validation_payload = build_service_worker_gate_map_validation_payload(
        generated_utc=generated_utc,
        json_output_path=json_output_path,
        entries=entries,
        gate_counts=gate_counts,
        status_counts=status_counts,
        worker_type_counts=worker_type_counts,
        pool_status_counts=pool_status_counts,
        ready_for_assignment_count=ready_for_assignment_count,
    )
    markdown = render_service_worker_gate_map_markdown(
        generated_utc=generated_utc,
        db_path=db_path,
        json_output_path=json_output_path,
        validation_path=validation_path,
        entries=entries,
        validation_payload=validation_payload,
        ready_for_assignment_count=ready_for_assignment_count,
    )
    return {
        "payload": payload,
        "validation_payload": validation_payload,
        "markdown": markdown,
        "ready_for_assignment_count": ready_for_assignment_count,
    }


__all__ = [
    "GATE_MAP_EXECUTION_NOTICE",
    "GATE_ORDER",
    "build_service_worker_gate_map_artifacts",
    "build_service_worker_gate_map_payload",
    "build_service_worker_gate_map_validation_payload",
    "render_service_worker_gate_map_markdown",
]
