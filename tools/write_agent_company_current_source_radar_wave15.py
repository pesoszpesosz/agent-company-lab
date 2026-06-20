#!/usr/bin/env python3
"""Write Agent Company current-source radar wave 15 from captured primary-source facts."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from atomic_writes import write_json_atomic


ROOT = Path(r"E:\agent-company-lab")
REPORTS = ROOT / "reports"
DATA = ROOT / "data"
REPORT_MD = REPORTS / "agent-company-current-source-radar-wave15-20260617.md"
REPORT_JSON = REPORTS / "agent-company-current-source-radar-wave15-20260617.json"
VALIDATION_JSON = REPORTS / "agent-company-current-source-radar-wave15-validation-20260617.json"
DATA_JSON = DATA / "agent-company-current-source-radar-wave15-20260617.json"
DATA_CSV = DATA / "agent-company-current-source-radar-wave15-20260617.csv"

CAPTURE_UTC = "2026-06-17T20:46:01Z"
TASK_ID = "task-agent-company-current-source-radar-wave15-20260617"

REPOS = [
    {
        "repo": "All-Hands-AI/OpenHands",
        "html_url": "https://github.com/OpenHands/OpenHands",
        "description": "OpenHands: AI-Driven Development",
        "stars": 77551,
        "forks": 9855,
        "open_issues": 332,
        "license": "NOASSERTION",
        "pushed_at": "2026-06-17T19:45:27Z",
        "category": "coding_agent_harness",
        "local_decision": "treat_as_sandboxed_code_worker_reference_not_runtime_dependency",
        "gate": "sandbox_execution_gate_and_github_public_action_gate_required",
        "fit_score": 12,
    },
    {
        "repo": "crewAIInc/crewAI",
        "html_url": "https://github.com/crewAIInc/crewAI",
        "description": "Framework for orchestrating role-playing, autonomous AI agents.",
        "stars": 53815,
        "forks": 7527,
        "open_issues": 475,
        "license": "MIT",
        "pushed_at": "2026-06-17T19:01:37Z",
        "category": "multi_agent_orchestration",
        "local_decision": "study_role_team_patterns_but_keep_shared_state_in_local_db",
        "gate": "no_dependency_install_no_worker_start",
        "fit_score": 11,
    },
    {
        "repo": "langchain-ai/langgraph",
        "html_url": "https://github.com/langchain-ai/langgraph",
        "description": "Build resilient agents.",
        "stars": 35051,
        "forks": 5867,
        "open_issues": 590,
        "license": "MIT",
        "pushed_at": "2026-06-17T20:45:03Z",
        "category": "durable_agent_graph_hitl",
        "local_decision": "reference_interrupt_checkpoint_human_review_pattern",
        "gate": "no_runtime_adoption_until_checkpoint_schema_and_apply_guard",
        "fit_score": 12,
    },
    {
        "repo": "temporalio/temporal",
        "html_url": "https://github.com/temporalio/temporal",
        "description": "Temporal service.",
        "stars": 21029,
        "forks": 1666,
        "open_issues": 770,
        "license": "MIT",
        "pushed_at": "2026-06-17T20:41:36Z",
        "category": "durable_execution_runtime",
        "local_decision": "keep_as_future_durable_orchestration_candidate",
        "gate": "runtime_start_preflight_and_signed_operator_decision_required",
        "fit_score": 12,
    },
    {
        "repo": "google/adk-python",
        "html_url": "https://github.com/google/adk-python",
        "description": "Code-first Python toolkit for building, evaluating, and deploying sophisticated AI agents.",
        "stars": 20157,
        "forks": 3581,
        "open_issues": 797,
        "license": "Apache-2.0",
        "pushed_at": "2026-06-17T20:40:14Z",
        "category": "agent_app_framework",
        "local_decision": "study_eval_deploy_agent_packaging_patterns",
        "gate": "model_api_execution_gate_and_dependency_install_gate_required",
        "fit_score": 10,
    },
    {
        "repo": "microsoft/agent-framework",
        "html_url": "https://github.com/microsoft/agent-framework",
        "description": "Framework for building, orchestrating and deploying AI agents and multi-agent workflows.",
        "stars": 11428,
        "forks": 1919,
        "open_issues": 670,
        "license": "MIT",
        "pushed_at": "2026-06-17T20:18:09Z",
        "category": "multi_agent_workflow_hitl",
        "local_decision": "reference_manager_worker_reviewer_escalation_pattern",
        "gate": "no_foundry_or_cloud_runtime_without_exact_scope_and_cost_gate",
        "fit_score": 11,
    },
    {
        "repo": "restatedev/restate",
        "html_url": "https://github.com/restatedev/restate",
        "description": "Platform for building resilient applications that tolerate infrastructure faults.",
        "stars": 4021,
        "forks": 170,
        "open_issues": 372,
        "license": "NOASSERTION",
        "pushed_at": "2026-06-17T18:08:53Z",
        "category": "durable_agent_runtime",
        "local_decision": "reference_journaled_tool_and_llm_step_recovery_pattern",
        "gate": "no_server_start_no_container_no_cloud_until_runtime_start_preflight",
        "fit_score": 12,
    },
]

DOC_SOURCES = [
    {
        "source_id": "langgraph_overview",
        "title": "LangGraph overview",
        "url": "https://docs.langchain.com/oss/python/langgraph/overview",
        "takeaway": "LangGraph positions durable execution, streaming, and human-in-the-loop as core orchestration primitives.",
        "local_mapping": "Use its checkpoint/interrupt concept as a reference for CEO/CRO decision pauses, while keeping local SQLite as the authority.",
    },
    {
        "source_id": "langchain_hitl",
        "title": "LangChain Human-in-the-loop",
        "url": "https://docs.langchain.com/oss/python/langchain/human-in-the-loop",
        "takeaway": "Tool calls can be paused by policy and resumed after a human decision.",
        "local_mapping": "Matches service-worker signed decision guard plus apply-preflight blocker.",
    },
    {
        "source_id": "temporal_durable_execution",
        "title": "Temporal durable execution guide",
        "url": "https://temporal.io/blog/what-is-durable-execution",
        "takeaway": "Durable execution treats long-running work as crash-proof execution with persisted history.",
        "local_mapping": "Keep our trace_events/outcomes/artifacts as the lightweight history before any Temporal adoption.",
    },
    {
        "source_id": "temporal_workflows",
        "title": "Temporal Workflow documentation",
        "url": "https://docs.temporal.io/workflows",
        "takeaway": "Workflow definitions, executions, schedules, and handlers are separate concepts.",
        "local_mapping": "Use this to split lane manager tasks, service requests, and worker starts in our schema.",
    },
    {
        "source_id": "restate_durable_agents",
        "title": "Restate durable agents",
        "url": "https://docs.restate.dev/ai/patterns/durable-agents",
        "takeaway": "Agent steps such as LLM calls, tool executions, and routing decisions can be durably persisted.",
        "local_mapping": "Promote tool/LLM calls to first-class trace events before runtime execution is allowed.",
    },
    {
        "source_id": "restate_ai_agents",
        "title": "Restate AI agents use case",
        "url": "https://docs.restate.dev/use-cases/ai-agents",
        "takeaway": "The runtime emphasizes retries, persisted progress, and suspension of idle long-running agents.",
        "local_mapping": "Add idle/lease/resume fields before local worker pool activation.",
    },
    {
        "source_id": "microsoft_hitl_sample",
        "title": "Microsoft Agent Framework human-in-the-loop workflow sample",
        "url": "https://github.com/microsoft/agent-framework/blob/main/python/samples/03-workflows/agents/workflow_as_agent_human_in_the_loop.py",
        "takeaway": "A worker/reviewer/manager escalation flow is an explicit sample shape.",
        "local_mapping": "Map to seeker, lane manager, CRO/CEO, and service-worker roles.",
    },
    {
        "source_id": "google_adk_repo",
        "title": "Google ADK Python repository",
        "url": "https://github.com/google/adk-python",
        "takeaway": "ADK is code-first and includes build/evaluate/deploy framing.",
        "local_mapping": "Useful later for eval packaging; blocked until model/API/provider/cost gates are explicit.",
    },
    {
        "source_id": "crewai_dynamic_graph_issue",
        "title": "CrewAI dynamic agent dependency graph issue",
        "url": "https://github.com/crewAIInc/crewAI/issues/6118",
        "takeaway": "Static orchestration is called out as breaking down at scale.",
        "local_mapping": "Reinforces that our task DAG and dispatch docket should support dynamic dependencies.",
    },
    {
        "source_id": "openhands_repo",
        "title": "OpenHands repository",
        "url": "https://github.com/OpenHands/OpenHands",
        "takeaway": "Coding-agent harnesses need repo, issue, token, and public-action boundaries.",
        "local_mapping": "Keep code workers behind sandbox execution and GitHub public-action gates.",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_data() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "agent_company.current_source_radar_wave15_dataset.v1",
        "capture_utc": CAPTURE_UTC,
        "repo_metadata_source": "Public GitHub repository metadata read via https://api.github.com/repos/{owner}/{repo}",
        "repos": REPOS,
        "doc_sources": DOC_SOURCES,
        "public_metadata_api_reads": len(REPOS),
        "execution_api_calls": False,
        "external_side_effects": False,
    }
    write_json_atomic(DATA_JSON, payload)
    with DATA_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "fit_score",
                "stars",
                "pushed_at",
                "category",
                "repo",
                "license",
                "local_decision",
                "gate",
                "html_url",
            ],
        )
        writer.writeheader()
        for row in sorted(REPOS, key=lambda item: (-item["fit_score"], -item["stars"], item["repo"])):
            writer.writerow({field: row[field] for field in writer.fieldnames})


def build_payload() -> tuple[dict[str, Any], dict[str, Any]]:
    failures: list[str] = []
    repo_count = len(REPOS)
    doc_source_count = len(DOC_SOURCES)
    if repo_count < 7:
        failures.append(f"expected_at_least_7_repo_rows_got_{repo_count}")
    if doc_source_count < 10:
        failures.append(f"expected_at_least_10_doc_sources_got_{doc_source_count}")
    if any(not row.get("local_decision") or not row.get("gate") for row in REPOS):
        failures.append("one_or_more_repo_rows_missing_local_decision_or_gate")
    if any(not src.get("url") or not src.get("local_mapping") for src in DOC_SOURCES):
        failures.append("one_or_more_doc_sources_missing_url_or_mapping")
    if any(row["pushed_at"] < "2026-06-17T00:00:00Z" for row in REPOS):
        failures.append("one_or_more_repo_rows_not_pushed_on_2026_06_17")

    generated = utc_now()
    ranked = sorted(REPOS, key=lambda item: (-item["fit_score"], -item["stars"], item["repo"]))
    architecture_decisions = [
        {
            "decision_id": "keep_local_sqlite_control_plane_as_brain",
            "reason": "Every source points toward durable state, checkpoints, and explicit human review. Our current DB already stores tasks, artifacts, outcomes, service requests, and trace events.",
            "next_build": "checkpoint_interrupt_contract_v1 for lane manager handoffs and service-worker decisions.",
        },
        {
            "decision_id": "separate_human_review_from_apply",
            "reason": "LangChain HITL, LangGraph interrupts, Microsoft HITL workflow, and our service-worker guards all converge on pause/review/resume rather than instant execution.",
            "next_build": "signed_decision_apply_command_contract only after a real signed decision artifact exists.",
        },
        {
            "decision_id": "treat_frameworks_as_patterns_before_dependencies",
            "reason": "High-star frameworks are active, but adopting them now would add runtime, credentials, and model/API gates before our local company loop is complete.",
            "next_build": "adapter_candidate_scorecard_v1 covering LangGraph, Temporal, Restate, ADK, Microsoft Agent Framework, CrewAI, and OpenHands.",
        },
    ]
    payload = {
        "schema_version": "agent_company.current_source_radar_wave15.v1",
        "generated_utc": generated,
        "capture_utc": CAPTURE_UTC,
        "task_id": TASK_ID,
        "dataset_json": str(DATA_JSON),
        "dataset_csv": str(DATA_CSV),
        "repo_count": repo_count,
        "doc_source_count": doc_source_count,
        "public_github_metadata_reads": repo_count,
        "execution_api_calls": False,
        "model_api_calls": False,
        "dependency_installs": 0,
        "runtime_starts": 0,
        "worker_starts": 0,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "browser_sessions_started": 0,
        "public_actions": False,
        "payment_actions": False,
        "wallet_actions": False,
        "external_side_effects": False,
        "ranked_repos": ranked,
        "doc_sources": DOC_SOURCES,
        "architecture_decisions": architecture_decisions,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": "Build checkpoint_interrupt_contract_v1 or adapter_candidate_scorecard_v1 before adopting any external agent/runtime framework.",
    }
    validation = {
        "schema_version": "agent_company.current_source_radar_wave15_validation.v1",
        "generated_utc": generated,
        "report_path": str(REPORT_MD),
        "json_path": str(REPORT_JSON),
        "dataset_json": str(DATA_JSON),
        "dataset_csv": str(DATA_CSV),
        "repo_count": repo_count,
        "doc_source_count": doc_source_count,
        "public_github_metadata_reads": repo_count,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "execution_api_calls": False,
        "model_api_calls": False,
        "dependency_installs": 0,
        "runtime_starts": 0,
        "worker_starts": 0,
        "service_requests_assigned": 0,
        "service_requests_updated": 0,
        "browser_sessions_started": 0,
        "public_actions": False,
        "payment_actions": False,
        "wallet_actions": False,
        "external_side_effects": False,
        "failures": failures,
    }
    return payload, validation


def write_markdown(payload: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Agent Company Current-Source Radar Wave 15",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Capture UTC: {payload['capture_utc']}",
        f"Task: `{TASK_ID}`",
        f"Dataset: `{DATA_JSON}`",
        f"CSV: `{DATA_CSV}`",
        f"Validation: `{VALIDATION_JSON}`",
        "",
        "## Purpose",
        "",
        "Refresh the agent-company infrastructure radar using current primary sources for multi-agent orchestration, durable execution, human-in-the-loop approval, and coding-agent harnesses. This wave is read-only: it installs nothing, starts no runtime, approves no service request, and performs no public action.",
        "",
        "## Source Boundary",
        "",
        f"- Repository metadata rows captured: `{payload['repo_count']}`",
        f"- Official/doc/source rows mapped: `{payload['doc_source_count']}`",
        f"- Public GitHub metadata reads: `{payload['public_github_metadata_reads']}`",
        f"- Validation failures: `{validation['failure_count']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Ranked Current Signals",
        "",
        "| Fit | Stars | Last Push | Category | Repo | Local Decision | Gate |",
        "| ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    for row in payload["ranked_repos"]:
        lines.append(
            f"| `{row['fit_score']}` | `{row['stars']}` | `{row['pushed_at']}` | `{row['category']}` | "
            f"[{row['repo']}]({row['html_url']}) | `{row['local_decision']}` | `{row['gate']}` |"
        )
    lines.extend(["", "## Primary-Source Takeaways", "", "| Source | Takeaway | Local Mapping |", "| --- | --- | --- |"])
    for src in payload["doc_sources"]:
        lines.append(f"| [{src['title']}]({src['url']}) | {src['takeaway']} | {src['local_mapping']} |")
    lines.extend(["", "## Architecture Decisions", ""])
    for index, decision in enumerate(payload["architecture_decisions"], start=1):
        lines.append(f"{index}. `{decision['decision_id']}`")
        lines.append(f"   Reason: {decision['reason']}")
        lines.append(f"   Next build: `{decision['next_build']}`")
    lines.extend(
        [
            "",
            "## Hold Until Gated",
            "",
            "- External framework dependency install/import.",
            "- Temporal, Restate, LangGraph, ADK, Microsoft Agent Framework, CrewAI, or OpenHands runtime start.",
            "- Model/provider/API execution.",
            "- Browser/account/public/GitHub/security/payment/wallet action.",
            "- Worker pool registration or assignment.",
            "",
            "## Boundary",
            "",
            f"- Model/API calls: `{validation['model_api_calls']}`",
            f"- Dependency installs: `{validation['dependency_installs']}`",
            f"- Runtime starts: `{validation['runtime_starts']}`",
            f"- Worker starts: `{validation['worker_starts']}`",
            f"- Service requests assigned/updated: `{validation['service_requests_assigned']}` / `{validation['service_requests_updated']}`",
            f"- Browser sessions started: `{validation['browser_sessions_started']}`",
            f"- Public/payment/wallet actions: `{validation['public_actions']}` / `{validation['payment_actions']}` / `{validation['wallet_actions']}`",
            f"- External side effects: `{validation['external_side_effects']}`",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    write_data()
    payload, validation = build_payload()
    write_json_atomic(REPORT_JSON, payload)
    write_json_atomic(VALIDATION_JSON, validation)
    write_markdown(payload, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
