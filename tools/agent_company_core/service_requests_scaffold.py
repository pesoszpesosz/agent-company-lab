"""Catalog-backed service-request lifecycle operations."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .constants import SERVICE_REQUEST_REVIEW_JSON, SERVICE_REQUEST_REVIEW_REPORT
from .io import now_utc
from .paths import DB_PATH, REPORTS_DIR, ROOT
from .utils import decode_json_list, md_cell, parse_json_arg, safe_id_fragment, sha256_file


from .service_requests_core import create_service_request, resolve_service_catalog_entry, validate_service_intake

def generated_service_request_id(service_id: str, lane_id: str, generated_at: str) -> str:
    stamp = (
        generated_at.replace("-", "")
        .replace(":", "")
        .replace("T", "-")
        .replace("Z", "")
    )
    return f"req-{safe_id_fragment(service_id, 48)}-{safe_id_fragment(lane_id, 48)}-{stamp}"


def render_service_request_packet(
    service: sqlite3.Row,
    request_id: str,
    lane_id: str,
    requester_agent_id: str | None,
    requested_action: str,
    risk_gate: str,
    approval_scope: str | None,
    artifact_path: str | None,
    intake: dict[str, Any],
    validation: dict[str, Any],
    generated_at: str,
    create_command: str,
) -> str:
    allowed = decode_json_list(service["allowed_actions_json"])
    gates = decode_json_list(service["hard_gates_json"])
    required = decode_json_list(service["required_intake_json"])
    approvers = decode_json_list(service["approval_required_by_json"])
    outputs = decode_json_list(service["output_artifacts_json"])
    missing = set(validation.get("missing", []))
    lines = [
        "# Service Request Packet",
        "",
        f"Generated UTC: {generated_at}",
        "",
        "## Identity",
        "",
        f"- Request ID: `{request_id}`",
        f"- Service ID: `{service['service_id']}`",
        f"- Request type: `{service['request_type']}`",
        f"- Lane: `{lane_id}`",
        f"- Requester agent: `{requester_agent_id or ''}`",
        f"- Risk gate: `{risk_gate}`",
        f"- Approval scope: {approval_scope or ''}",
        f"- Related artifact: {artifact_path or ''}",
        "",
        "## Service Purpose",
        "",
        str(service["purpose"] or ""),
        "",
        "## Requested Action",
        "",
        requested_action,
        "",
        "## Required Intake",
        "",
        "| Field | Status | Value |",
        "| --- | --- | --- |",
    ]
    for field in required:
        value = intake.get(field)
        status = "missing" if field in missing else "present"
        lines.append(f"| `{field}` | {status} | {md_cell(str(value) if value is not None else '', 180)} |")
    extra_context = intake.get("extra_context")
    if extra_context:
        lines.extend(["", "## Extra Context", "", "```json", json.dumps(extra_context, indent=2, sort_keys=True), "```"])
    lines.extend(
        [
            "",
            "## Allowed Actions",
            "",
            *[f"- {item}" for item in allowed],
            "",
            "## Hard Gates",
            "",
            *[f"- {item}" for item in gates],
            "",
            "## Approval Required By",
            "",
            *[f"- `{item}`" for item in approvers],
            "",
            "## Expected Output Artifacts",
            "",
            *[f"- `{item}`" for item in outputs],
            "",
            "## Creation Command",
            "",
            "Run this only after all required intake fields are present:",
            "",
            "```powershell",
            create_command,
            "```",
            "",
            "## Non-Approval Notice",
            "",
            "This packet does not approve account creation, wallet setup, payment activity, trading, public posts, PRs, comments, browser submissions, API key creation, credential handling, or real-money action. It is a local review artifact only.",
            "",
        ]
    )
    return "\n".join(lines)


def render_service_request_checklist(
    service: sqlite3.Row,
    request_id: str,
    validation: dict[str, Any],
    db_created: bool,
    create_command: str,
) -> str:
    missing = validation.get("missing", [])
    lines = [
        "# Service Request Checklist",
        "",
        f"- Request ID: `{request_id}`",
        f"- Service ID: `{service['service_id']}`",
        f"- Validation OK: `{str(validation.get('ok')).lower()}`",
        f"- DB request created: `{str(db_created).lower()}`",
        "",
        "## Missing Required Fields",
        "",
    ]
    if missing:
        lines.extend(f"- `{field}`" for field in missing)
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            "- Fill missing fields in `intake.json` before requesting worker action.",
            "- Keep all hard gates in `packet.md` intact.",
            "- If complete, create the control-plane service request:",
            "",
            "```powershell",
            create_command,
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def scaffold_service_request(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    if not args.service_id and not args.request_type:
        raise SystemExit("scaffold-service-request requires --service-id or --request-type.")
    request_type = args.request_type or ""
    if args.service_id and not request_type:
        row = conn.execute("SELECT request_type FROM service_catalog WHERE service_id = ?", (args.service_id,)).fetchone()
        if not row:
            raise SystemExit(f"Unknown service_id: {args.service_id}. Run seed-service-catalog first.")
        request_type = row["request_type"]
    service = resolve_service_catalog_entry(conn, args.service_id, request_type)
    if not service:
        raise SystemExit("scaffold-service-request requires a catalog-backed service.")
    lane = conn.execute("SELECT lane_id FROM lanes WHERE lane_id = ?", (args.lane_id,)).fetchone()
    if not lane:
        raise SystemExit(f"Unknown lane_id: {args.lane_id}")
    requester_agent_id_for_db = args.requester_agent_id
    warnings: list[str] = []
    if args.requester_agent_id:
        requester = conn.execute("SELECT agent_id FROM agents WHERE agent_id = ?", (args.requester_agent_id,)).fetchone()
        if not requester:
            requester_agent_id_for_db = None
            warnings.append(
                f"Requester agent `{args.requester_agent_id}` is not registered; packet keeps it as text, DB-linked fields use null."
            )

    prefill_json = parse_json_arg(args.prefill_json, args.prefill_file, {})
    prefill = json.loads(prefill_json)
    if not isinstance(prefill, dict):
        raise SystemExit("--prefill-json/--prefill-file must be a JSON object.")
    prefill_intake = prefill.get("intake") if isinstance(prefill.get("intake"), dict) else prefill
    required = decode_json_list(service["required_intake_json"])
    intake: dict[str, Any] = {field: "" for field in required}
    intake.update({field: prefill_intake.get(field, "") for field in required})
    if "lane_id" in required and not intake.get("lane_id"):
        intake["lane_id"] = args.lane_id
    extra_context = {key: value for key, value in prefill_intake.items() if key not in required}
    if extra_context:
        intake["extra_context"] = extra_context

    generated_at = now_utc()
    request_id = args.request_id or generated_service_request_id(service["service_id"], args.lane_id, generated_at)
    risk_gate = args.risk_gate or "catalog_required_approval_no_external_action"
    output_root = Path(args.output_dir) if args.output_dir else ROOT / "requests" / "service-requests"
    request_dir = output_root / request_id
    request_dir.mkdir(parents=True, exist_ok=True)

    intake_json = json.dumps(intake, indent=2, sort_keys=True)
    compact_intake_json = json.dumps(intake, sort_keys=True)
    validation = validate_service_intake(service, compact_intake_json)
    create_command = (
        f"python E:\\agent-company-lab\\tools\\agent_company.py create-service-request "
        f"--request-id {request_id} "
        f"--service-id {service['service_id']} "
        f"--request-type {service['request_type']} "
        f"--lane-id {args.lane_id} "
        f"--risk-gate \"{risk_gate}\" "
        f"--requested-action \"{args.requested_action}\" "
        f"--intake-file {request_dir / 'intake.json'}"
    )
    if requester_agent_id_for_db:
        create_command += f" --requester-agent-id {requester_agent_id_for_db}"
    if args.approval_scope:
        create_command += f" --approval-scope \"{args.approval_scope}\""
    if args.artifact_path:
        create_command += f" --artifact-path {args.artifact_path}"

    db_created = False
    if args.create_db_request:
        if not validation["ok"]:
            missing = ", ".join(validation.get("missing", []))
            raise SystemExit(
                f"Cannot create DB request; intake is incomplete for `{service['service_id']}`. "
                f"Missing required field(s): {missing}"
            )
        ns = argparse.Namespace(
            request_id=request_id,
            service_id=service["service_id"],
            request_type=service["request_type"],
            lane_id=args.lane_id,
            requester_agent_id=requester_agent_id_for_db,
            risk_gate=risk_gate,
            requested_action=args.requested_action,
            intake_json=compact_intake_json,
            intake_file=None,
            approval_scope=args.approval_scope,
            artifact_path=str(request_dir / "packet.md"),
        )
        create_service_request(conn, ns)
        db_created = True

    packet = render_service_request_packet(
        service,
        request_id,
        args.lane_id,
        args.requester_agent_id,
        args.requested_action,
        risk_gate,
        args.approval_scope,
        args.artifact_path,
        intake,
        validation,
        generated_at,
        create_command,
    )
    checklist = render_service_request_checklist(service, request_id, validation, db_created, create_command)
    metadata = {
        "generated_utc": generated_at,
        "api_calls": False,
        "external_side_effects": False,
        "source": "agent_company.py scaffold-service-request",
        "catalog_service_id": service["service_id"],
        "request_type": service["request_type"],
        "lane_id": args.lane_id,
        "request_id": request_id,
        "validation_ok": validation["ok"],
        "missing_fields": validation.get("missing", []),
        "db_request_created": db_created,
        "warnings": warnings,
    }
    files = {
        "intake.json": intake_json + "\n",
        "packet.md": packet,
        "checklist.md": checklist,
        "metadata.json": json.dumps(metadata, indent=2, sort_keys=True) + "\n",
    }
    for name, content in files.items():
        (request_dir / name).write_text(content, encoding="utf-8")

    artifact_id = f"artifact-{safe_id_fragment(request_id, 80)}-packet"
    trace_id = f"trace-{safe_id_fragment(request_id, 80)}"
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(artifact_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          task_id=excluded.task_id,
          kind=excluded.kind,
          path_or_url=excluded.path_or_url,
          sha256=excluded.sha256,
          notes=excluded.notes
        """,
        (
            artifact_id,
            args.lane_id,
            args.task_id,
            "service_request_packet",
            str(request_dir),
            sha256_file(request_dir / "packet.md"),
            f"Catalog-backed service request packet for {service['service_id']}.",
            ts,
        ),
    )
    conn.execute(
        """
        INSERT INTO trace_events(
          event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
          source, summary, metadata_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(event_id) DO UPDATE SET
          metadata_json=excluded.metadata_json,
          artifact_path=excluded.artifact_path
        """,
        (
            f"trace-event-{safe_id_fragment(request_id, 80)}-scaffolded",
            trace_id,
            args.lane_id,
            args.task_id,
            requester_agent_id_for_db,
            "service_request_packet_scaffolded",
            ts,
            "local_cli",
            f"Scaffolded service request packet {request_id} for {service['service_id']}; validation_ok={validation['ok']}; db_created={db_created}.",
            json.dumps(
                {
                    "span_kind": "internal",
                    "runtime": "local_cli",
                    "api_calls": False,
                    "external_side_effects": False,
                    "service_id": service["service_id"],
                    "validation_ok": validation["ok"],
                    "db_request_created": db_created,
                },
                sort_keys=True,
            ),
            str(request_dir / "packet.md"),
            ts,
        ),
    )
    conn.commit()
    print(
        json.dumps(
            {
                "ok": True,
                "request_id": request_id,
                "service_id": service["service_id"],
                "validation_ok": validation["ok"],
                "missing_fields": validation.get("missing", []),
                "db_request_created": db_created,
                "warnings": warnings,
                "packet_dir": str(request_dir),
                "artifact_id": artifact_id,
            },
            indent=2,
        )
    )
