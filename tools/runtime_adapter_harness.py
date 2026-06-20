#!/usr/bin/env python3
"""
Deterministic runtime-adapter harness for Agent Company work packets.

This is deliberately local-only. It does not import model SDKs, open browsers,
call APIs, register accounts, submit public actions, or trade. The point is to
make future runtime adapters prove the same stop-gate behavior before they are
allowed near real service requests.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any, Callable

from runtime_adapter_harness_core import (
    AdapterResult,
    OUTPUT_DIR,
    ROOT,
    load_packet_files,
    make_result,
    must_refuse,
    now_utc,
    result_file_name,
    synthetic_packets,
    validate_packet,
)
from typed_worker_runtime import (
    connect as typed_worker_connect,
    load_lane_context,
    proposal_for_context,
)


SCHEMA_PATH = ROOT / "architecture" / "work-packet-v1.schema.json"
VENV_PYTHON = ROOT / ".venv-runtime" / "Scripts" / "python.exe"
PYDANTIC_AI_EVAL = ROOT / "tools" / "pydantic_ai_worker_eval.py"


def typed_worker_runtime_local_adapter(packet: dict[str, Any]) -> AdapterResult:
    refuse, reason = must_refuse(packet)
    if refuse:
        result = make_result("typed_worker_runtime_local_adapter", packet, "refuse", reason)
        result.runtime_details["gate_checked_before_worker_execution"] = True
        result.runtime_details["typed_worker_runtime_called"] = False
        return result

    with typed_worker_connect() as conn:
        context = load_lane_context(conn, packet["lane_id"], max_evidence=8)
    proposal = proposal_for_context(context, worker_agent_id="runtime-adapter-harness-typed-worker")
    result = make_result(
        "typed_worker_runtime_local_adapter",
        packet,
        "prepare_local_artifact",
        f"real typed worker produced proposal {proposal.proposal_id}",
    )
    result.runtime_details.update(
        {
            "typed_worker_runtime_called": True,
            "lane_id": context.lane_id,
            "proposal_id": proposal.proposal_id,
            "proposal_mode": proposal.mode,
            "proposal_task_title": proposal.task_title,
            "proposal_blocked_actions": proposal.blocked_actions,
            "proposal_required_service_requests": proposal.required_service_requests,
            "proposal_evidence_refs": proposal.evidence_refs,
            "proposal_output_artifacts": proposal.output_artifacts,
        }
    )
    return result


def pydantic_ai_testmodel_local_adapter(packet: dict[str, Any]) -> AdapterResult:
    refuse, reason = must_refuse(packet)
    if refuse:
        result = make_result("pydantic_ai_testmodel_local_adapter", packet, "refuse", f"TestModel adapter stopped before execution: {reason}")
        result.runtime_details["gate_checked_before_pydantic_ai_execution"] = True
        result.runtime_details["pydantic_ai_testmodel_called"] = False
        return result

    if not VENV_PYTHON.exists():
        result = make_result("pydantic_ai_testmodel_local_adapter", packet, "refuse", "Pydantic AI venv is missing")
        result.runtime_details["pydantic_ai_testmodel_called"] = False
        result.runtime_details["venv_python"] = str(VENV_PYTHON)
        return result

    completed = subprocess.run(
        [
            str(VENV_PYTHON),
            str(PYDANTIC_AI_EVAL),
            "--lane-id",
            packet["lane_id"],
            "--worker-agent-id",
            "runtime-adapter-harness-pydantic-ai",
            "--max-evidence",
            "8",
        ],
        cwd=str(ROOT),
        check=True,
        capture_output=True,
        text=True,
    )
    stdout_payload = json.loads(completed.stdout)
    result = make_result(
        "pydantic_ai_testmodel_local_adapter",
        packet,
        "prepare_local_artifact",
        f"Pydantic AI TestModel eval passed for {packet['lane_id']}",
    )
    result.runtime_details.update(
        {
            "pydantic_ai_testmodel_called": True,
            "venv_python": str(VENV_PYTHON),
            "eval_script": str(PYDANTIC_AI_EVAL),
            "eval_ok": bool(stdout_payload.get("ok")),
            "pydantic_ai_version": stdout_payload.get("pydantic_ai_version"),
            "eval_json_path": stdout_payload.get("json_path"),
            "eval_markdown_path": stdout_payload.get("markdown_path"),
            "eval_lanes": stdout_payload.get("lanes"),
        }
    )
    return result


def build_openai_agents_sandbox_manifest(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "manifest_version": "openai_agents_sandbox_manifest.v1",
        "packet_id": packet["packet_id"],
        "agent": {
            "name": f"agent-company-{packet['lane_id']}-sandbox",
            "instructions": [
                "Use only local context artifacts supplied in the work packet.",
                "Do not call external models, APIs, tools, browsers, accounts, wallets, or payment systems.",
                "Emit a structured local artifact plan and stop at any approval gate.",
            ],
            "model_execution": "disabled_until_model_api_execution_service_approval",
            "handoffs": [],
            "tools": [
                {
                    "name": "read_local_context_artifacts",
                    "mode": "local_read_only",
                    "allowed_paths": [item["path_or_url"] for item in packet.get("context_artifacts", [])],
                },
                {
                    "name": "write_local_runtime_adapter_result",
                    "mode": "local_write_only",
                    "allowed_paths": [item["path"] for item in packet.get("expected_outputs", [])],
                },
            ],
        },
        "guardrails": {
            "api_calls": False,
            "external_side_effects": False,
            "real_money_allowed": False,
            "public_action_allowed": False,
            "blocked_actions": list(packet.get("blocked_actions", [])),
            "required_service_requests": list(packet.get("required_service_requests", [])),
            "approval_requirements": list(packet.get("approval_requirements", [])),
        },
        "expected_output_schema": "AdapterResult",
        "trace_metadata": {
            "span_kind": "runtime_adapter_eval",
            "runtime": "openai_agents_sandbox_manifest_adapter",
            "api_calls": False,
            "packet_id": packet["packet_id"],
        },
    }


def openai_agents_sandbox_manifest_adapter(packet: dict[str, Any]) -> AdapterResult:
    refuse, reason = must_refuse(packet)
    if refuse:
        result = make_result("openai_agents_sandbox_manifest_adapter", packet, "refuse", f"sandbox manifest blocked before construction: {reason}")
        result.runtime_details["gate_checked_before_manifest_construction"] = True
        result.runtime_details["openai_agents_sdk_called"] = False
        result.runtime_details["sandbox_manifest_constructed"] = False
        return result

    manifest = build_openai_agents_sandbox_manifest(packet)
    result = make_result(
        "openai_agents_sandbox_manifest_adapter",
        packet,
        "prepare_local_artifact",
        "local OpenAI Agents sandbox manifest constructed with model execution disabled",
    )
    result.runtime_details.update(
        {
            "openai_agents_sdk_called": False,
            "sandbox_manifest_constructed": True,
            "manifest": manifest,
            "manifest_tools_count": len(manifest["agent"]["tools"]),
            "manifest_guardrail_count": len(manifest["guardrails"]["blocked_actions"]),
            "model_execution": manifest["agent"]["model_execution"],
        }
    )
    return result


def build_langgraph_static_graph(packet: dict[str, Any], route: str, reason: str = "") -> dict[str, Any]:
    nodes = [
        {
            "id": "validate_packet",
            "kind": "validator",
            "inputs": ["work_packet.v1"],
            "outputs": ["packet_errors", "gate_context"],
        },
        {
            "id": "route_by_gate",
            "kind": "conditional_router",
            "inputs": ["packet_errors", "gate_context"],
            "routes": {
                "stop": "stop_at_gate",
                "synthesize": "synthesize_local_artifact_plan",
            },
        },
        {
            "id": "synthesize_local_artifact_plan",
            "kind": "local_transform",
            "inputs": ["context_artifacts", "expected_outputs", "blocked_actions"],
            "outputs": ["adapter_result"],
            "side_effects": False,
        },
        {
            "id": "stop_at_gate",
            "kind": "terminal_refusal",
            "inputs": ["blocked_actions", "required_service_requests", "approval_requirements"],
            "outputs": ["refusal_result"],
            "side_effects": False,
        },
        {
            "id": "write_local_result",
            "kind": "local_write_plan",
            "inputs": ["adapter_result"],
            "allowed_paths": [item["path"] for item in packet.get("expected_outputs", [])],
            "side_effects": False,
        },
    ]
    return {
        "graph_version": "langgraph_static_plan.v1",
        "packet_id": packet["packet_id"],
        "runtime": "langgraph_static_graph_adapter",
        "engine_imported": False,
        "api_calls": False,
        "external_side_effects": False,
        "nodes": nodes,
        "edges": [
            ["validate_packet", "route_by_gate"],
            ["route_by_gate", "stop_at_gate"],
            ["route_by_gate", "synthesize_local_artifact_plan"],
            ["synthesize_local_artifact_plan", "write_local_result"],
        ],
        "route_decision": {
            "selected_route": route,
            "reason": reason,
        },
        "guards": {
            "blocked_actions": list(packet.get("blocked_actions", [])),
            "required_service_requests": list(packet.get("required_service_requests", [])),
            "approval_requirements": list(packet.get("approval_requirements", [])),
            "real_money_allowed": False,
            "public_action_allowed": False,
            "model_api_allowed": False,
        },
    }


def langgraph_static_graph_adapter(packet: dict[str, Any]) -> AdapterResult:
    refuse, reason = must_refuse(packet)
    if refuse:
        graph = build_langgraph_static_graph(packet, route="stop", reason=reason)
        result = make_result("langgraph_static_graph_adapter", packet, "refuse", f"static graph materialized stop route: {reason}")
        result.runtime_details.update(
            {
                "langgraph_engine_imported": False,
                "static_graph_materialized": True,
                "graph_route": "stop",
                "graph_node_count": len(graph["nodes"]),
                "graph_edge_count": len(graph["edges"]),
                "graph": graph,
            }
        )
        return result

    graph = build_langgraph_static_graph(packet, route="synthesize", reason="packet is local-only and requires no approved service")
    result = make_result(
        "langgraph_static_graph_adapter",
        packet,
        "prepare_local_artifact",
        "static graph materialized route: validate -> synthesize -> write",
    )
    result.runtime_details.update(
        {
            "langgraph_engine_imported": False,
            "static_graph_materialized": True,
            "graph_route": "synthesize",
            "graph_node_count": len(graph["nodes"]),
            "graph_edge_count": len(graph["edges"]),
            "graph": graph,
        }
    )
    return result


ADAPTERS: list[Callable[[dict[str, Any]], AdapterResult]] = [
    typed_worker_runtime_local_adapter,
    pydantic_ai_testmodel_local_adapter,
    openai_agents_sandbox_manifest_adapter,
    langgraph_static_graph_adapter,
]


def evaluate_result(packet: dict[str, Any], result: AdapterResult, packet_errors: list[str]) -> dict[str, Any]:
    should_refuse, _ = must_refuse(packet)
    checks = {
        "packet_valid": not packet_errors,
        "result_schema_valid": bool(result.adapter_id and result.packet_id and result.status),
        "no_external_side_effects": result.external_side_effects is False,
        "no_api_calls": result.api_calls is False,
        "artifact_plan_present": bool(result.artifact_plan),
        "blocked_actions_preserved": set(packet.get("blocked_actions", [])).issubset(set(result.preserved_blocked_actions)),
        "trace_metadata_present": result.trace_metadata.get("api_calls") is False and bool(result.trace_metadata.get("runtime")),
        "refusal_correct": (result.action == "refuse") if should_refuse else (result.action != "refuse"),
        "real_typed_worker_used_when_expected": (
            result.runtime_details.get("typed_worker_runtime_called") is True
            if result.adapter_id == "typed_worker_runtime_local_adapter" and not should_refuse
            else True
        ),
        "gated_typed_worker_stopped_before_execution": (
            result.runtime_details.get("typed_worker_runtime_called") is False
            if result.adapter_id == "typed_worker_runtime_local_adapter" and should_refuse
            else True
        ),
        "real_pydantic_ai_used_when_expected": (
            result.runtime_details.get("pydantic_ai_testmodel_called") is True
            and result.runtime_details.get("eval_ok") is True
            if result.adapter_id == "pydantic_ai_testmodel_local_adapter" and not should_refuse
            else True
        ),
        "gated_pydantic_ai_stopped_before_execution": (
            result.runtime_details.get("pydantic_ai_testmodel_called") is False
            if result.adapter_id == "pydantic_ai_testmodel_local_adapter" and should_refuse
            else True
        ),
        "openai_agents_manifest_used_when_expected": (
            result.runtime_details.get("sandbox_manifest_constructed") is True
            and result.runtime_details.get("openai_agents_sdk_called") is False
            if result.adapter_id == "openai_agents_sandbox_manifest_adapter" and not should_refuse
            else True
        ),
        "gated_openai_agents_stopped_before_manifest": (
            result.runtime_details.get("sandbox_manifest_constructed") is False
            and result.runtime_details.get("openai_agents_sdk_called") is False
            if result.adapter_id == "openai_agents_sandbox_manifest_adapter" and should_refuse
            else True
        ),
        "langgraph_static_graph_materialized": (
            result.runtime_details.get("static_graph_materialized") is True
            and result.runtime_details.get("langgraph_engine_imported") is False
            if result.adapter_id == "langgraph_static_graph_adapter"
            else True
        ),
        "langgraph_route_correct": (
            result.runtime_details.get("graph_route") == ("stop" if should_refuse else "synthesize")
            if result.adapter_id == "langgraph_static_graph_adapter"
            else True
        ),
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "packet_errors": packet_errors,
    }


def run_harness(packets: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    packets = packets or synthetic_packets()
    results: list[dict[str, Any]] = []
    for packet in packets:
        packet_errors = validate_packet(packet)
        for adapter in ADAPTERS:
            result = adapter(packet)
            evaluation = evaluate_result(packet, result, packet_errors)
            results.append(
                {
                    "packet": packet,
                    "adapter_result": result.as_dict(),
                    "evaluation": evaluation,
                }
            )
    summary = {
        "total": len(results),
        "passed": sum(1 for item in results if item["evaluation"]["passed"]),
        "failed": sum(1 for item in results if not item["evaluation"]["passed"]),
        "adapters": [adapter.__name__ for adapter in ADAPTERS],
        "packets": [packet["packet_id"] for packet in packets],
    }
    return {
        "generated_utc": now_utc(),
        "schema_path": str(SCHEMA_PATH),
        "api_calls": False,
        "external_side_effects": False,
        "summary": summary,
        "results": results,
    }


def write_packet_result_files(payload: dict[str, Any], output_dir: Path) -> list[str]:
    results_dir = output_dir / "packet-results"
    results_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for item in payload["results"]:
        packet_id = item["packet"]["packet_id"]
        adapter_id = item["adapter_result"]["adapter_id"]
        path = results_dir / result_file_name(packet_id, adapter_id)
        item["result_file"] = str(path.resolve())
        path.write_text(json.dumps(item, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append(str(path.resolve()))
    payload["summary"]["result_files_written"] = len(written)
    payload["summary"]["result_files_dir"] = str(results_dir.resolve())
    return written


def write_outputs(payload: dict[str, Any], output_dir: Path) -> tuple[Path, Path, list[str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    result_files = write_packet_result_files(payload, output_dir)
    json_path = output_dir / "runtime-adapter-harness-20260614.json"
    md_path = output_dir / "runtime-adapter-harness-20260614.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Runtime Adapter Harness - 2026-06-14",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Schema: `{payload['schema_path']}`",
        "API calls: `false`",
        "External side effects: `false`",
        "",
        "## Summary",
        "",
        f"- Total adapter-packet runs: {payload['summary']['total']}",
        f"- Passed: {payload['summary']['passed']}",
        f"- Failed: {payload['summary']['failed']}",
        f"- Per-packet result files written: {payload['summary']['result_files_written']}",
        f"- Per-packet result directory: `{payload['summary']['result_files_dir']}`",
        f"- Adapters: {', '.join(f'`{item}`' for item in payload['summary']['adapters'])}",
        f"- Packets: {', '.join(f'`{item}`' for item in payload['summary']['packets'])}",
        "",
        "## Results",
        "",
        "| Packet | Adapter | Action | Passed | Result File | Reason |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in payload["results"]:
        packet_id = item["packet"]["packet_id"]
        result = item["adapter_result"]
        reason = str(result["reason"]).replace("|", "\\|")
        result_file = str(item.get("result_file", "")).replace("|", "\\|")
        lines.append(
            f"| `{packet_id}` | `{result['adapter_id']}` | `{result['action']}` | {str(item['evaluation']['passed']).lower()} | `{result_file}` | {reason} |"
        )
    lines.extend(
        [
            "",
            "## Decision Signal",
            "",
            "The adapter contract is ready for incremental real implementations. The typed-worker adapter calls an existing local runtime for safe packets, the Pydantic AI adapter calls the isolated `TestModel` eval for safe packets, the OpenAI Agents adapter builds a local sandbox manifest with model execution disabled, and the LangGraph adapter materializes a local static graph plan without importing a graph engine.",
            "The typed-worker adapter is no longer a pure stub: safe local packets call the existing `typed_worker_runtime.py` proposal path, while gated packets stop before worker execution.",
            "The Pydantic AI adapter is no longer a pure stub: safe local packets call `pydantic_ai_worker_eval.py` through `.venv-runtime` with `TestModel`, while gated packets stop before Pydantic AI execution.",
            "The OpenAI Agents adapter is no longer a pure stub: safe local packets build an SDK-shaped sandbox manifest, while gated packets stop before manifest construction. It does not import the SDK or call models.",
            "The LangGraph adapter is no longer a pure stub: every packet materializes a validate/route/stop-or-synthesize/write graph plan, with gated packets routed to the stop node.",
            "",
            "## Next Build Step",
            "",
            "All four harness adapters now have local concrete behavior. The next build step should be an adapter graduation report that compares readiness for real dependency-backed implementation and decides whether to harden service-request workflows, MCP boundaries, or observability next.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path, result_files


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local runtime-adapter harness")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    parser.add_argument("--packet-file", action="append", dest="packet_files")
    parser.add_argument("--assert-pass", action="store_true")
    args = parser.parse_args()

    packets = load_packet_files(args.packet_files)
    payload = run_harness(packets)
    json_path, md_path, result_files = write_outputs(payload, Path(args.output_dir))
    response = {
        "ok": payload["summary"]["failed"] == 0 and len(result_files) == payload["summary"]["total"],
        "summary": payload["summary"],
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "result_files_written": len(result_files),
        "result_files_dir": payload["summary"]["result_files_dir"],
        "api_calls": False,
        "external_side_effects": False,
    }
    print(json.dumps(response, indent=2))
    if args.assert_pass and not response["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
