#!/usr/bin/env python3
"""
Gated Pydantic AI adapter shell.

Dry-run mode uses Pydantic AI TestModel and writes local artifacts. Real mode is
refused unless the named service request is approved. This keeps model/API cost,
credentials, and provider scope behind the control-plane approval gate.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

import pydantic_ai
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

from typed_worker_runtime import (
    OUTPUT_DIR,
    TaskProposal,
    connect,
    load_lane_context,
    now_utc,
    proposal_for_context,
)


DEFAULT_REQUEST_ID = "req-pydantic-ai-model-backed-adapter-20260614"


def get_service_request(conn: sqlite3.Connection, request_id: str) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM service_requests WHERE request_id = ?", (request_id,)).fetchone()
    if not row:
        raise SystemExit(f"Unknown service request: {request_id}")
    return row


def require_real_mode_approval(conn: sqlite3.Connection, request_id: str, lane_id: str, model: str | None) -> None:
    row = get_service_request(conn, request_id)
    if row["status"] != "approved":
        raise SystemExit(
            f"Refusing real model run: service request {request_id} is {row['status']}. "
            "Approve exact provider, model, max cost, allowed lanes, output artifact path, and credential route first."
        )
    scope = (row["approval_scope"] or "").lower()
    if lane_id.lower() not in scope:
        raise SystemExit(f"Refusing real model run: approved scope does not mention lane {lane_id}.")
    if model and model.lower() not in scope:
        raise SystemExit(f"Refusing real model run: approved scope does not mention model {model}.")


def run_dry_mode(lane_id: str, worker_agent_id: str, max_evidence: int) -> TaskProposal:
    with connect() as conn:
        context = load_lane_context(conn, lane_id, max_evidence)
    expected = proposal_for_context(context, worker_agent_id)
    agent = Agent(
        TestModel(custom_output_args=expected.model_dump()),
        output_type=TaskProposal,
        name=f"agent-company-gated-{lane_id}-dry-run",
        instructions="Return a safe TaskProposal. Do not request external action.",
    )
    return agent.run_sync("Build the next safe local worker proposal.").output


def write_adapter_output(output: TaskProposal, output_dir: Path, mode: str) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"pydantic-ai-adapter-{mode}-{output.lane_id}"
    json_path = output_dir / f"{stem}.json"
    md_path = output_dir / f"{stem}.md"
    payload: dict[str, Any] = {
        "generated_at": now_utc(),
        "runtime": "pydantic-ai",
        "pydantic_ai_version": getattr(pydantic_ai, "__version__", "unknown"),
        "mode": mode,
        "api_calls": False if mode == "dry-run" else "requires_approval",
        "proposal": output.model_dump(),
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        f"# Pydantic AI Adapter Output - {output.lane_id}",
        "",
        f"Generated UTC: {payload['generated_at']}",
        f"Mode: `{mode}`",
        f"Pydantic AI version: `{payload['pydantic_ai_version']}`",
        f"API calls: `{payload['api_calls']}`",
        "",
        "## Proposal",
        "",
        f"- Proposal ID: `{output.proposal_id}`",
        f"- Task title: {output.task_title}",
        f"- Mode: `{output.mode}`",
        f"- Duplicate key: `{output.duplicate_key}`",
        "",
        "## Blocked Actions",
        "",
    ]
    lines.extend([f"- {item}" for item in output.blocked_actions])
    lines.extend(["", "## Evidence Refs", ""])
    lines.extend([f"- `{item}`" for item in output.evidence_refs] or ["- none"])
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Gated Pydantic AI model adapter shell")
    parser.add_argument("--lane-id", default="prediction_market_research")
    parser.add_argument("--worker-agent-id", default="pydantic-ai-gated-adapter")
    parser.add_argument("--max-evidence", type=int, default=8)
    parser.add_argument("--mode", choices=["dry-run", "real"], default="dry-run")
    parser.add_argument("--service-request-id", default=DEFAULT_REQUEST_ID)
    parser.add_argument("--model")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    args = parser.parse_args()

    if args.mode == "real":
        with connect() as conn:
            require_real_mode_approval(conn, args.service_request_id, args.lane_id, args.model)
        raise SystemExit("Real model execution path is gated and not implemented in this offline prototype.")

    output = run_dry_mode(args.lane_id, args.worker_agent_id, args.max_evidence)
    json_path, md_path = write_adapter_output(output, Path(args.output_dir), args.mode)
    print(
        json.dumps(
            {
                "ok": True,
                "mode": args.mode,
                "lane_id": args.lane_id,
                "json_path": str(json_path),
                "markdown_path": str(md_path),
                "api_calls": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
