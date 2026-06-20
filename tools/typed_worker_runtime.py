#!/usr/bin/env python3
"""
Typed worker-runtime prototype for the agent-company lab.

This deliberately avoids model calls and external actions. It tests the local
contract a future Pydantic AI/OpenAI Agents/LangGraph worker should honor:
read one lane context, validate it, produce a scoped proposal, and stop at
service gates.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "state" / "agent_company.sqlite"
OUTPUT_DIR = ROOT / "reports" / "worker-runtime"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def decode_json_list(value: str | None) -> list[str]:
    if not value:
        return []
    parsed = json.loads(value)
    if not isinstance(parsed, list):
        return []
    return [str(item) for item in parsed]


def safe_id_fragment(value: str, limit: int = 72) -> str:
    cleaned = []
    for char in value.lower():
        if char.isalnum():
            cleaned.append(char)
        elif char in {"-", "_", "."}:
            cleaned.append(char)
        else:
            cleaned.append("-")
    fragment = "".join(cleaned).strip("-")
    while "--" in fragment:
        fragment = fragment.replace("--", "-")
    return (fragment or "item")[:limit].strip("-")


def compact(value: str | None, limit: int = 260) -> str:
    if value is None:
        return ""
    return " ".join(str(value).replace("\r", "\n").split())[:limit].rstrip()


def md_cell(value: str | None, limit: int = 220) -> str:
    return compact(value, limit).replace("|", "\\|")


class SourceSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    spec_id: str
    name: str
    source_type: str
    cadence: str
    risk_gate: str
    refresh_command: str | None = None
    source_paths: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    notes: str | None = None


class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_id: str
    status: str
    title: str
    source_path: str | None = None
    source_url: str | None = None
    summary: str | None = None
    next_action: str | None = None
    ownership_note: str | None = None


class LaneContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lane_id: str
    department: str
    status: str
    owner_agent_id: str | None = None
    owner_thread_id: str | None = None
    agent_types: list[str]
    examples: list[str]
    promotion_gates: list[str]
    service_workers_required: list[str]
    side_effects: list[str]
    global_gates: list[str]
    source_specs: list[SourceSpec]
    evidence: list[EvidenceItem]

    @field_validator("lane_id")
    @classmethod
    def lane_id_is_present(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("lane_id cannot be empty")
        return value


class TaskProposal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    generated_at: str
    worker_agent_id: str
    lane_id: str
    proposal_id: str
    task_title: str
    duplicate_key: str
    mode: str
    rationale: str
    evidence_refs: list[str]
    allowed_now: list[str]
    blocked_actions: list[str]
    required_service_requests: list[str]
    output_artifacts: list[str]
    trace_events_to_record: list[str]
    stop_conditions: list[str]
    recommended_cli_commands: list[str]

    @field_validator("mode")
    @classmethod
    def mode_is_safe(cls, value: str) -> str:
        allowed = {"read_only_local_artifact", "service_request_required", "no_action_read_only"}
        if value not in allowed:
            raise ValueError(f"mode must be one of {sorted(allowed)}")
        return value

    @field_validator("blocked_actions")
    @classmethod
    def has_blocks(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("blocked_actions must explicitly list stop gates")
        return value


def load_lane_context(conn: sqlite3.Connection, lane_id: str, max_evidence: int) -> LaneContext:
    lane = conn.execute("SELECT * FROM lanes WHERE lane_id = ?", (lane_id,)).fetchone()
    if not lane:
        raise SystemExit(f"Unknown lane: {lane_id}")
    specs = [
        SourceSpec(
            spec_id=row["spec_id"],
            name=row["name"],
            source_type=row["source_type"],
            cadence=row["cadence"],
            risk_gate=row["risk_gate"],
            refresh_command=row["refresh_command"],
            source_paths=decode_json_list(row["source_paths_json"]),
            outputs=decode_json_list(row["outputs_json"]),
            notes=row["notes"],
        )
        for row in conn.execute(
            """
            SELECT spec_id, name, source_type, cadence, risk_gate, refresh_command,
                   source_paths_json, outputs_json, notes
            FROM source_specs
            WHERE lane_id = ?
            ORDER BY spec_id
            """,
            (lane_id,),
        )
    ]
    evidence = [
        EvidenceItem(
            evidence_id=row["evidence_id"],
            status=row["status"],
            title=row["title"],
            source_path=row["source_path"],
            source_url=row["source_url"],
            summary=row["summary"],
            next_action=row["next_action"],
            ownership_note=row["ownership_note"],
        )
        for row in conn.execute(
            """
            SELECT evidence_id, status, title, source_path, source_url, summary, next_action, ownership_note
            FROM lane_evidence
            WHERE lane_id = ?
            ORDER BY
              CASE
                WHEN status LIKE '%submission%' THEN 1
                WHEN status LIKE '%verified%' THEN 2
                WHEN status LIKE '%watch%' THEN 3
                WHEN status LIKE '%imported%' THEN 4
                ELSE 5
              END,
              updated_at DESC
            LIMIT ?
            """,
            (lane_id, max_evidence),
        )
    ]
    return LaneContext(
        lane_id=lane["lane_id"],
        department=lane["department"],
        status=lane["status"],
        owner_agent_id=lane["owner_agent_id"],
        owner_thread_id=lane["owner_thread_id"],
        agent_types=decode_json_list(lane["agent_types_json"]),
        examples=decode_json_list(lane["examples_json"]),
        promotion_gates=decode_json_list(lane["promotion_gates_json"]),
        service_workers_required=decode_json_list(lane["service_workers_required_json"]),
        side_effects=decode_json_list(lane["side_effects_json"]),
        global_gates=decode_json_list(lane["global_gates_json"]),
        source_specs=specs,
        evidence=evidence,
    )


def proposal_for_context(context: LaneContext, worker_agent_id: str) -> TaskProposal:
    if context.lane_id == "submitted_bounty_payouts":
        mode = "no_action_read_only"
        title = "Read-only payout visibility packet; no work assigned from this thread"
        rationale = "This lane is explicitly owned by the parallel payout worker, so this runtime must not create payout work."
    elif context.side_effects or context.service_workers_required:
        mode = "read_only_local_artifact"
        title = lane_title(context)
        rationale = "The lane has side-effect gates, so the safe prototype output is a local artifact proposal only."
    else:
        mode = "read_only_local_artifact"
        title = lane_title(context)
        rationale = "No side effects are needed for a first local artifact proposal."

    blocked_actions = list(dict.fromkeys(context.side_effects + context.global_gates))
    if context.lane_id == "prediction_market_research":
        blocked_actions.extend(["real-money trade", "venue account action", "eligibility assertion without verification"])
    if context.lane_id == "security_bounty_private_reports":
        blocked_actions.extend(["live security testing", "private report submission", "public vulnerability claim"])
    if context.lane_id == "paid_code_bounties":
        blocked_actions.extend(["PR submission", "GitHub comment", "bounty claim"])
    blocked_actions = list(dict.fromkeys(blocked_actions))

    evidence_refs = [item.evidence_id for item in context.evidence[:5]]
    proposal_id = f"proposal-{safe_id_fragment(context.lane_id)}-{now_utc()[:10].replace('-', '')}"
    duplicate_key = f"{context.lane_id}:typed-worker-prototype:{now_utc()[:10]}"
    output_base = str(OUTPUT_DIR / f"{context.lane_id}-typed-worker-proposal")

    return TaskProposal(
        generated_at=now_utc(),
        worker_agent_id=worker_agent_id,
        lane_id=context.lane_id,
        proposal_id=proposal_id,
        task_title=title,
        duplicate_key=duplicate_key,
        mode=mode,
        rationale=rationale,
        evidence_refs=evidence_refs,
        allowed_now=[
            "read manager packet",
            "read source specs",
            "read local evidence/artifact reports",
            "write local proposal artifacts",
            "record artifacts/outcomes/traces through the control plane",
        ],
        blocked_actions=blocked_actions,
        required_service_requests=context.service_workers_required,
        output_artifacts=[f"{output_base}.json", f"{output_base}.md"],
        trace_events_to_record=[
            "typed_worker_context_loaded",
            "typed_worker_proposal_written",
        ],
        stop_conditions=[
            "lane is already owned by another active worker",
            "next action requires account, wallet, browser, public, legal/KYC/billing, or real-money action",
            "evidence is missing or source scope is unclear",
        ],
        recommended_cli_commands=[
            f"python E:\\agent-company-lab\\tools\\agent_company.py list-source-specs --lane-id {context.lane_id}",
            f"python E:\\agent-company-lab\\tools\\agent_company.py list-evidence --lane-id {context.lane_id} --limit 25",
            f"python E:\\agent-company-lab\\tools\\agent_company.py write-artifacts-report --lane-id {context.lane_id} --path E:\\agent-company-lab\\reports\\artifacts-{context.lane_id}-latest.md",
        ],
    )


def lane_title(context: LaneContext) -> str:
    titles = {
        "prediction_market_research": "Prepare paper-only replay spec for one imported market edge",
        "security_bounty_private_reports": "Rank imported private-report candidates by scope, proof quality, payout path, and route",
        "paid_code_bounties": "Scout fresh explicit-payout code bounties using imported negative samples",
        "content_and_social_growth": "Prepare read-only X/Grok research packet with no public actions",
        "web3_airdrops_grants_hackathons": "Scout terms, deadlines, and eligibility without wallet or registration action",
        "lead_generation_and_sales": "Draft compliant offer and targeting rules before outreach",
        "local_trading_strategy_research": "Inventory local paper/backtest artifacts and define evidence standard",
        "platform_engineering": "Evaluate worker runtime contract against manager, artifact, and trace layers",
    }
    return titles.get(context.lane_id, f"Prepare scoped local artifact proposal for {context.lane_id}")


def write_outputs(context: LaneContext, proposal: TaskProposal, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{context.lane_id}-typed-worker-proposal.json"
    md_path = output_dir / f"{context.lane_id}-typed-worker-proposal.md"
    payload = {
        "context": context.model_dump(),
        "proposal": proposal.model_dump(),
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        f"# Typed Worker Proposal - {context.lane_id}",
        "",
        f"Generated UTC: {proposal.generated_at}",
        f"Worker agent: `{proposal.worker_agent_id}`",
        f"Mode: `{proposal.mode}`",
        "",
        "## Proposal",
        "",
        f"- Proposal ID: `{proposal.proposal_id}`",
        f"- Task title: {proposal.task_title}",
        f"- Duplicate key: `{proposal.duplicate_key}`",
        f"- Rationale: {proposal.rationale}",
        "",
        "## Evidence Refs",
        "",
    ]
    lines.extend([f"- `{item}`" for item in proposal.evidence_refs] or ["- none"])
    lines.extend(["", "## Allowed Now", ""])
    lines.extend([f"- {item}" for item in proposal.allowed_now])
    lines.extend(["", "## Blocked Actions", ""])
    lines.extend([f"- {item}" for item in proposal.blocked_actions])
    lines.extend(["", "## Required Service Requests", ""])
    lines.extend([f"- {item}" for item in proposal.required_service_requests] or ["- none"])
    lines.extend(["", "## Recommended Commands", "", "```powershell"])
    lines.extend(proposal.recommended_cli_commands)
    lines.extend(["```", "", "## Source Specs", "", "| Spec | Type | Gate |", "| --- | --- | --- |"])
    for spec in context.source_specs:
        lines.append(f"| `{spec.spec_id}` | {md_cell(spec.source_type, 80)} | {md_cell(spec.risk_gate, 180)} |")
    if not context.source_specs:
        lines.append("| none |  |  |")
    lines.extend(["", "## Evidence Preview", "", "| Status | Evidence | Source | Next Action |", "| --- | --- | --- | --- |"])
    for item in context.evidence:
        source = item.source_url or item.source_path or ""
        lines.append(
            f"| {md_cell(item.status, 100)} | `{item.evidence_id}` - {md_cell(item.title, 160)} | {md_cell(source, 180)} | {md_cell(item.next_action, 220)} |"
        )
    if not context.evidence:
        lines.append("| none |  |  |  |")
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Typed worker-runtime prototype")
    parser.add_argument("--lane-id", required=True)
    parser.add_argument("--worker-agent-id", default="typed-worker-prototype")
    parser.add_argument("--max-evidence", type=int, default=10)
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    args = parser.parse_args()

    with connect() as conn:
        context = load_lane_context(conn, args.lane_id, args.max_evidence)
    proposal = proposal_for_context(context, args.worker_agent_id)
    json_path, md_path = write_outputs(context, proposal, Path(args.output_dir))
    print(
        json.dumps(
            {
                "ok": True,
                "lane_id": context.lane_id,
                "proposal_id": proposal.proposal_id,
                "mode": proposal.mode,
                "json_path": str(json_path),
                "markdown_path": str(md_path),
                "evidence_refs": len(proposal.evidence_refs),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
