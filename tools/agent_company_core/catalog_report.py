from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Service catalog report writer."""

from .constants import SERVICE_CATALOG_REPORT
from .io import now_utc
from .paths import REPORTS_DIR, SERVICE_CATALOG_PATH
from .utils import decode_json_list, md_cell
from .catalog_listing import service_catalog_where

def write_service_catalog_report(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SERVICE_CATALOG_REPORT
    where, params = service_catalog_where(args)
    params.append(args.limit)
    rows = [
        dict(row)
        for row in conn.execute(
            f"""
            SELECT sc.service_id, sc.department_id, d.name AS department_name, sc.name,
                   sc.request_type, sc.owner_role_id, sc.purpose, sc.allowed_actions_json,
                   sc.hard_gates_json, sc.required_intake_json, sc.approval_required_by_json,
                   sc.output_artifacts_json, sc.default_status, sc.notes
            FROM service_catalog sc
            LEFT JOIN departments d ON d.department_id = sc.department_id
            {where}
            ORDER BY sc.request_type, sc.service_id
            LIMIT ?
            """,
            params,
        )
    ]
    counts_by_type: dict[str, int] = {}
    counts_by_owner: dict[str, int] = {}
    counts_by_status: dict[str, int] = {}
    for row in rows:
        counts_by_type[row["request_type"]] = counts_by_type.get(row["request_type"], 0) + 1
        counts_by_owner[row["owner_role_id"]] = counts_by_owner.get(row["owner_role_id"], 0) + 1
        counts_by_status[row["default_status"]] = counts_by_status.get(row["default_status"], 0) + 1

    lines = [
        "# Service Worker Bureau Catalog",
        "",
        f"Generated UTC: {now_utc()}",
        f"Source definition: `{SERVICE_CATALOG_PATH}`",
        "",
        "## Purpose",
        "",
        "This catalog is the company service desk for side-effect-adjacent work. Lane managers use it to create precise service requests for registration, wallet, browser, public-action, outreach, model/API, legal/KYC/payment, security-report, trading, and secret-handling needs.",
        "",
        "The catalog does not approve actions. A real side effect still needs a `service_requests` row plus an exact approved scope.",
        "",
        "## Source-Backed Design Signals",
        "",
        "- Temporal's human-in-the-loop AI workflow docs show a pattern where risky actions pause for approval by signal, wait without consuming compute, use durable timers, and preserve an audit trail: https://docs.temporal.io/ai-cookbook/human-in-the-loop-python",
        "- LangGraph interrupts pause execution with persisted state and warn that side effects before an interrupt must be idempotent: https://docs.langchain.com/oss/python/langgraph/interrupts",
        "- MCP security best practices emphasize consent, authorization, access controls, and privacy-aware tool/resource design: https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices",
        "- OpenAI Agents SDK guardrail docs distinguish agent-level input/output guardrails from per-function-tool guardrails and note that handoffs do not pass through the normal function-tool guardrail pipeline: https://openai.github.io/openai-agents-python/guardrails/",
        "",
        "## Counts",
        "",
        f"- Services in report: `{len(rows)}`",
        f"- By status: `{json.dumps(counts_by_status, sort_keys=True)}`",
        f"- By request type: `{json.dumps(counts_by_type, sort_keys=True)}`",
        f"- By owner role: `{json.dumps(counts_by_owner, sort_keys=True)}`",
        "",
        "## Operating Rule",
        "",
        "Managers may ask service workers to prepare packets, read public documentation, inspect non-sensitive browser state, and write local checklists. They must stop before account creation, identity verification, terms acceptance, payments, credential entry, public posting, bounty/report submission, wallet transactions, or real-money trades unless a specific service request has been approved.",
        "",
        "## Service Index",
        "",
        "| Service | Request Type | Owner Role | Department | Status | Purpose |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['service_id']}` - {md_cell(row['name'], 120)}",
                    md_cell(row["request_type"], 120),
                    f"`{row['owner_role_id']}`",
                    md_cell(row["department_name"] or row["department_id"], 120),
                    md_cell(row["default_status"], 80),
                    md_cell(row["purpose"], 280),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Detail", ""])
    for row in rows:
        allowed = decode_json_list(row["allowed_actions_json"])
        gates = decode_json_list(row["hard_gates_json"])
        intake = decode_json_list(row["required_intake_json"])
        approvers = decode_json_list(row["approval_required_by_json"])
        outputs = decode_json_list(row["output_artifacts_json"])
        lines.extend(
            [
                f"### {row['service_id']}",
                "",
                f"- Name: {row['name']}",
                f"- Request type: `{row['request_type']}`",
                f"- Owner role: `{row['owner_role_id']}`",
                f"- Department: `{row['department_name'] or row['department_id']}`",
                f"- Status: `{row['default_status']}`",
                f"- Purpose: {row['purpose']}",
                f"- Notes: {row['notes'] or ''}",
                "- Allowed preparation:",
            ]
        )
        lines.extend([f"  - {item}" for item in allowed] or ["  - none"])
        lines.append("- Hard gates:")
        lines.extend([f"  - {item}" for item in gates] or ["  - none"])
        lines.append("- Required intake:")
        lines.extend([f"  - `{item}`" for item in intake] or ["  - none"])
        lines.append("- Approval required by:")
        lines.extend([f"  - `{item}`" for item in approvers] or ["  - none"])
        lines.append("- Output artifacts:")
        lines.extend([f"  - `{item}`" for item in outputs] or ["  - none"])
        lines.append("")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(output_path), "count": len(rows)}, indent=2))
