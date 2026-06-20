from __future__ import annotations

from pathlib import Path
from typing import Any

"""Markdown renderer for money-path coverage audit reports."""

from .utils import md_cell


def render_money_path_coverage_report(
    generated_utc: str,
    json_output_path: Path,
    validation_path: Path,
    coverage_model: dict[str, Any],
    source_spec_count: int,
    service_request_status_counts: dict[str, int],
    payload: dict[str, Any],
    failures: list[str],
) -> str:
    active_lanes = coverage_model["active_lanes"]
    owned_active_lanes = coverage_model["owned_active_lanes"]
    thin_evidence_threshold = coverage_model["thin_evidence_threshold"]
    thin_evidence_rows = coverage_model["thin_evidence_rows"]
    recommended_next_lanes = coverage_model["recommended_next_lanes"]
    lane_rows = coverage_model["lane_rows"]
    read_only_boundary_preserved = coverage_model["read_only_boundary_preserved"]

    lines = [
        "# Agent Company Money-Path Coverage Audit",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Summary",
        "",
        f"- Active lanes: `{len(active_lanes)}`",
        f"- Owned active lanes: `{len(owned_active_lanes)}`",
        f"- Source specs: `{source_spec_count}`",
        f"- Thin-evidence actionable lanes, threshold <= {thin_evidence_threshold}: `{len(thin_evidence_rows)}`",
        f"- Parked service requests: `{service_request_status_counts.get('needs_review', 0)}`",
        f"- Read-only payout boundary preserved: `{read_only_boundary_preserved}`",
        "",
        "## CEO Dispatch Order",
        "",
        "| Rank | Lane | Agent | Evidence | Gate | First Task | Required Proof |",
        "| ---: | --- | --- | ---: | --- | --- | --- |",
    ]
    for rank, row in enumerate(recommended_next_lanes, start=1):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(rank),
                    f"`{row['lane_id']}`",
                    f"`{row['recommended_agent_type']}`",
                    str(row["evidence_count"]),
                    "parked_service_request" if row["blocked_by_service_gate"] else "local_only",
                    md_cell(row["recommended_first_task"], 260),
                    md_cell(row["required_proof_artifact"], 180),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Full Lane Coverage",
            "",
            "| Lane | Sources | Evidence | Tasks | Requests | Traces | Coverage | Urgency | Next Agent |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in sorted(lane_rows, key=lambda item: (item["lane_id"])):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['lane_id']}`",
                    str(row["source_spec_count"]),
                    str(row["evidence_count"]),
                    str(row["task_count"]),
                    str(row["parked_service_request_count"]),
                    str(row["trace_event_count"]),
                    str(row["coverage_score"]),
                    str(row["urgency_score"]),
                    f"`{row['recommended_agent_type']}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This audit is local and report-only except for recording its own task, evidence, artifacts, and trace row.",
            "- It does not start browser sessions, register accounts, touch wallets or payments, perform public actions, run security tests, place trades, mutate service requests, assign workers, start workers, call APIs, or create external side effects.",
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        for failure in failures:
            lines.append(f"- {failure}")
    return "\n".join(lines) + "\n"


__all__ = ["render_money_path_coverage_report"]