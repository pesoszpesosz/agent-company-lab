#!/usr/bin/env python3
"""
Offline Pydantic AI dry-run evaluation for the agent-company worker contract.

This uses pydantic_ai.models.test.TestModel, so it performs no API calls and
does not require credentials. The goal is to verify that Pydantic AI can carry
our existing typed TaskProposal contract before any model-backed execution is
considered.
"""

from __future__ import annotations

import argparse
import json
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


DEFAULT_LANES = ["prediction_market_research", "submitted_bounty_payouts"]


def run_lane_eval(lane_id: str, worker_agent_id: str, max_evidence: int) -> dict[str, Any]:
    with connect() as conn:
        context = load_lane_context(conn, lane_id, max_evidence)
    expected = proposal_for_context(context, worker_agent_id)
    agent = Agent(
        TestModel(custom_output_args=expected.model_dump()),
        output_type=TaskProposal,
        name=f"agent-company-{lane_id}-dry-run",
        instructions=(
            "Return a TaskProposal that obeys the lane context, blocks gated side effects, "
            "and writes only local artifacts."
        ),
    )
    result = agent.run_sync(
        "Build the next safe local worker proposal from the already-loaded control-plane lane context."
    )
    output = result.output
    checks = {
        "valid_task_proposal": isinstance(output, TaskProposal),
        "lane_matches": output.lane_id == lane_id,
        "blocked_actions_present": bool(output.blocked_actions),
        "has_evidence_or_readonly_boundary": bool(output.evidence_refs)
        or output.mode == "no_action_read_only"
        or bool(output.required_service_requests),
        "no_direct_side_effect_mode": output.mode in {"read_only_local_artifact", "no_action_read_only"},
        "payout_lane_readonly": lane_id != "submitted_bounty_payouts" or output.mode == "no_action_read_only",
    }
    return {
        "lane_id": lane_id,
        "checks": checks,
        "passed": all(checks.values()),
        "output": output.model_dump(),
        "expected": expected.model_dump(),
    }


def write_report(results: list[dict[str, Any]], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "pydantic-ai-eval-latest.json"
    md_path = output_dir / "pydantic-ai-eval-latest.md"
    payload = {
        "generated_at": now_utc(),
        "runtime": "pydantic-ai",
        "pydantic_ai_version": getattr(pydantic_ai, "__version__", "unknown"),
        "model": "pydantic_ai.models.test.TestModel",
        "api_calls": False,
        "results": results,
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Pydantic AI Dry-Run Eval",
        "",
        f"Generated UTC: {payload['generated_at']}",
        f"Pydantic AI version: `{payload['pydantic_ai_version']}`",
        "Model: `pydantic_ai.models.test.TestModel`",
        "API calls: `false`",
        "",
        "## Decision Signal",
        "",
        "Pydantic AI can carry the existing `TaskProposal` output contract in an offline dry-run. It should remain isolated until a real model/API service request is approved.",
        "",
        "## Results",
        "",
        "| Lane | Passed | Mode | Evidence Refs | Failed Checks |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for result in results:
        failed = [name for name, ok in result["checks"].items() if not ok]
        output = result["output"]
        lines.append(
            f"| `{result['lane_id']}` | {str(result['passed']).lower()} | `{output['mode']}` | {len(output['evidence_refs'])} | {', '.join(failed) or ''} |"
        )
    lines.extend(
        [
            "",
            "## Gates",
            "",
            "- This eval used `TestModel`; it made no network or model/API call.",
            "- Real model execution still requires a service request because it can use credentials and incur cost.",
            "- The payout lane must continue to return `no_action_read_only` in this workspace.",
            "",
            "## Recommended Next Step",
            "",
            "Add a model-backed adapter behind a service request only after deciding model/provider, max cost, allowed lanes, and output artifact path.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline Pydantic AI worker dry-run eval")
    parser.add_argument("--lane-id", action="append", dest="lane_ids")
    parser.add_argument("--worker-agent-id", default="pydantic-ai-dry-run-worker")
    parser.add_argument("--max-evidence", type=int, default=8)
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    args = parser.parse_args()

    lane_ids = args.lane_ids or DEFAULT_LANES
    results = [run_lane_eval(lane_id, args.worker_agent_id, args.max_evidence) for lane_id in lane_ids]
    json_path, md_path = write_report(results, Path(args.output_dir))
    print(
        json.dumps(
            {
                "ok": all(item["passed"] for item in results),
                "lanes": lane_ids,
                "json_path": str(json_path),
                "markdown_path": str(md_path),
                "pydantic_ai_version": getattr(pydantic_ai, "__version__", "unknown"),
                "api_calls": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
