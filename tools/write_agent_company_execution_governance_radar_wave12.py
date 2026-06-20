#!/usr/bin/env python3
"""Write Wave 12 execution-governance radar for the agent company."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

JSON_OUT = DATA / "agent-company-execution-governance-radar-wave12-20260617.json"
MD_OUT = REPORTS / "agent-company-execution-governance-radar-wave12-20260617.md"
VALIDATION_OUT = REPORTS / "agent-company-execution-governance-radar-wave12-validation-20260617.json"

TASK_ID = "task-agent-company-execution-governance-radar-wave12-20260617"
LANE_ID = "platform_engineering"
CAPTURE_UTC = "2026-06-17T18:25:00Z"


SOURCE_ROWS: list[dict[str, Any]] = [
    {
        "id": "github_ai_agent_orchestration_article",
        "category": "operating_model_reference",
        "name": "GitHub: What is AI agent orchestration?",
        "url": "https://github.com/resources/articles/what-is-ai-agent-orchestration",
        "signal": "Defines agent orchestration as the control layer for managing execution, shared context, collaboration, guardrails, cost limits, and HITL checkpoints.",
        "agent_company_fit": "Use as language and requirement baseline for CEO/manager/worker architecture.",
        "local_implication": "The company needs a deterministic policy layer around dynamic agent planning, not just task prompts.",
        "recommended_artifact": "agent_company_orchestration_requirement_map_v1",
        "risk_gate": "public_read_only_reference_no_runtime_action",
        "status": "captured",
    },
    {
        "id": "open_multi_agent_goal_to_dag",
        "category": "goal_to_dag_orchestration",
        "name": "open-multi-agent/open-multi-agent",
        "url": "https://github.com/open-multi-agent/open-multi-agent",
        "signal": "Recent TypeScript-native framework that turns a goal into a task DAG, parallelizes independent work, and provides a post-run dashboard.",
        "agent_company_fit": "Direct pattern for turning user goals into lane tasks and manager dispatch graphs.",
        "local_implication": "Add a local report-only task-DAG contract before launching many more lane-agent chats.",
        "recommended_artifact": "agent_task_dag_contract_v1",
        "risk_gate": "report_only_no_node_install_no_model_key_no_runtime_start",
        "status": "captured",
    },
    {
        "id": "cordum_governance_control_plane",
        "category": "governance_control_plane",
        "name": "cordum-io/cordum",
        "url": "https://github.com/cordum-io/cordum",
        "signal": "GitHub topic listing describes an open agent control plane with pre-execution policy enforcement, approval gates, and audit trails.",
        "agent_company_fit": "Closest external signal to the local service-worker gate chain already built.",
        "local_implication": "Promote a policy-kernel comparison against current approval, scope, command-safety, authority, and preflight reports.",
        "recommended_artifact": "agent_governance_policy_kernel_gap_map_v1",
        "risk_gate": "report_only_no_dependency_install_no_policy_runtime",
        "status": "captured",
    },
    {
        "id": "agent_infra_aio_sandbox",
        "category": "computer_use_sandbox",
        "name": "agent-infra/sandbox",
        "url": "https://github.com/agent-infra/sandbox",
        "signal": "All-in-one agent sandbox combining browser, shell, file, MCP operations, VSCode Server, VNC, Jupyter, and terminal in one container.",
        "agent_company_fit": "Pattern for a future unified worker workspace where browser downloads, files, and code execution share one evidence boundary.",
        "local_implication": "Extend the sandbox execution gate contract with browser/file/shell/MCP cross-contamination checks before any container start.",
        "recommended_artifact": "computer_use_sandbox_boundary_matrix_v1",
        "risk_gate": "report_only_no_docker_no_vnc_no_mcp_server_start",
        "status": "captured",
    },
    {
        "id": "browser_use_rust_core",
        "category": "browser_worker_harness",
        "name": "browser-use/browser-use",
        "url": "https://github.com/browser-use/browser-use",
        "signal": "Browser Use 0.13 introduces a beta agent with Rust core, browser harness, persistent tools, and recovery loops inspired by coding agents.",
        "agent_company_fit": "Pattern source for read-only browser workers and future approved public-action browser workers.",
        "local_implication": "Keep browser workers behind exact-scope packets and add recovery-loop logging requirements.",
        "recommended_artifact": "browser_worker_recovery_loop_contract_v1",
        "risk_gate": "report_only_no_browser_start_no_api_key_no_public_action",
        "status": "captured",
    },
    {
        "id": "nvidia_nemo_agent_toolkit",
        "category": "agent_team_optimization",
        "name": "NVIDIA/NeMo-Agent-Toolkit",
        "url": "https://github.com/NVIDIA/NeMo-Agent-Toolkit",
        "signal": "Open-source toolkit for connecting and optimizing teams of AI agents, with instrumentation, observability, continuous learning, MCP publishing, and workflow UI ideas.",
        "agent_company_fit": "Pattern source for agent-team evaluation, reusable workflows, and runtime intelligence.",
        "local_implication": "The local company needs eval/learning loops per lane before it scales worker count.",
        "recommended_artifact": "lane_agent_eval_and_learning_loop_contract_v1",
        "risk_gate": "report_only_no_pip_install_no_workflow_execution_no_model_api",
        "status": "captured",
    },
    {
        "id": "mlflow_agents_engineering_platform",
        "category": "agent_observability_eval",
        "name": "mlflow/mlflow",
        "url": "https://github.com/mlflow/mlflow",
        "signal": "MLflow positions itself as an AI engineering platform for agents with debugging, evaluation, monitoring, OpenTelemetry, MCP, cost, and safety monitoring.",
        "agent_company_fit": "Pattern source for trace export, evaluation, and cost monitoring without committing to a backend.",
        "local_implication": "Promote a local trace-to-eval export contract before integrating Langfuse/Phoenix/MLflow/AgentOps.",
        "recommended_artifact": "agent_trace_eval_export_contract_v1",
        "risk_gate": "report_only_no_backend_no_tracking_server_no_api_key",
        "status": "captured",
    },
    {
        "id": "agent_squad_router",
        "category": "agent_router",
        "name": "2FastLabs/agent-squad",
        "url": "https://github.com/2FastLabs/agent-squad",
        "signal": "Framework for routing among multiple agents and maintaining context across interactions.",
        "agent_company_fit": "Pattern source for manager routing across departments and lane-specific specialists.",
        "local_implication": "Add explicit route-decision evidence rows whenever the CEO sends work to lane managers.",
        "recommended_artifact": "manager_route_decision_contract_v1",
        "risk_gate": "report_only_no_framework_import_no_cloud_deploy",
        "status": "captured",
    },
    {
        "id": "microsoft_agent_governance_toolkit",
        "category": "agent_sre_governance",
        "name": "microsoft/agent-governance-toolkit",
        "url": "https://github.com/microsoft/agent-governance-toolkit",
        "signal": "Search result highlights Agent SRE, OpenTelemetry, Prometheus, and integrations with observability platforms.",
        "agent_company_fit": "Pattern source for production incident response around autonomous workers.",
        "local_implication": "Add local agent-SRE severity, rollback, and pause contracts before enabling worker starts.",
        "recommended_artifact": "agent_sre_pause_and_incident_contract_v1",
        "risk_gate": "report_only_no_agent_sre_runtime_no_prometheus_export",
        "status": "captured_from_search_result",
    },
    {
        "id": "trycua_computer_use",
        "category": "desktop_computer_use",
        "name": "trycua/cua",
        "url": "https://github.com/trycua/cua",
        "signal": "GitHub topic result describes open-source infrastructure for computer-use agents controlling full desktops across operating systems.",
        "agent_company_fit": "Longer-term pattern for high-risk desktop workers.",
        "local_implication": "Desktop-control workers need the strictest service gate: screen recording, action allowlist, credential masking, and kill switch.",
        "recommended_artifact": "desktop_control_worker_hard_gate_v1",
        "risk_gate": "report_only_no_desktop_control_no_vm_start_no_credentials",
        "status": "captured_from_search_result",
    },
    {
        "id": "vercel_agent_browser",
        "category": "browser_worker_harness",
        "name": "vercel-labs/agent-browser",
        "url": "https://github.com/vercel-labs/agent-browser",
        "signal": "New browser automation CLI for AI agents, described as a fast native Rust CLI.",
        "agent_company_fit": "Pattern source for lightweight browser-worker command boundaries.",
        "local_implication": "Browser workers should have a CLI-command safety review similar to service-worker decision command safety.",
        "recommended_artifact": "browser_worker_command_safety_contract_v1",
        "risk_gate": "report_only_no_npm_install_no_chrome_download_no_browser_start",
        "status": "captured_from_search_result",
    },
    {
        "id": "opensandbox_group_opensandbox",
        "category": "sandbox_execution",
        "name": "opensandbox-group/OpenSandbox",
        "url": "https://github.com/opensandbox-group/OpenSandbox",
        "signal": "GitHub result describes a sandbox runtime for AI agents with SDK usage, integrations, browser automation, and training workloads.",
        "agent_company_fit": "Alternative sandbox-runtime pattern to compare against E2B and AIO Sandbox.",
        "local_implication": "Sandbox selection should be delayed until the local boundary matrix and cost/secrets controls are complete.",
        "recommended_artifact": "sandbox_runtime_selection_preflight_v1",
        "risk_gate": "report_only_no_sdk_install_no_sandbox_start",
        "status": "captured_from_search_result",
    },
    {
        "id": "auto_use_desktop_workspace",
        "category": "agent_workspace_safety",
        "name": "auto-use/Auto-Use",
        "url": "https://github.com/auto-use/Auto-Use",
        "signal": "Search result describes sandboxed Bash confined to a desktop workspace with path blocklists, timeouts, and stdin detection plus browser automation.",
        "agent_company_fit": "Practical safety pattern for local task workers.",
        "local_implication": "Our sandbox gate should require path allowlists/blocklists, idle/total timeouts, and interactive-stdin rejection.",
        "recommended_artifact": "local_worker_shell_safety_contract_v1",
        "risk_gate": "report_only_no_shell_harness_install_no_browser_action",
        "status": "captured_from_search_result",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def score(row: dict[str, Any]) -> int:
    category_weight = {
        "governance_control_plane": 10,
        "goal_to_dag_orchestration": 9,
        "operating_model_reference": 8,
        "computer_use_sandbox": 8,
        "agent_sre_governance": 8,
        "browser_worker_harness": 7,
        "agent_observability_eval": 7,
        "agent_team_optimization": 7,
        "agent_router": 6,
        "desktop_computer_use": 6,
        "sandbox_execution": 6,
        "agent_workspace_safety": 6,
    }.get(row["category"], 4)
    if row["status"] == "captured":
        return category_weight + 2
    return category_weight


def build_payload() -> dict[str, Any]:
    rows = sorted([{**row, "priority_score": score(row)} for row in SOURCE_ROWS], key=lambda row: row["priority_score"], reverse=True)
    return {
        "schema_version": "agent_company.execution_governance_radar_wave12.v1",
        "generated_utc": utc_now(),
        "capture_utc": CAPTURE_UTC,
        "task_id": TASK_ID,
        "lane_id": LANE_ID,
        "purpose": "Refresh current open-source and GitHub signals specifically for scalable agent execution governance: goal-to-DAG orchestration, policy control planes, computer/browser-use sandboxes, agent observability, and incident/SRE gates.",
        "github_api_boundary": {
            "api_attempted": True,
            "api_result": "HTTP 403 rate limit exceeded for the selected repo metadata batch",
            "fallback": "Use accessible GitHub pages, GitHub topic/search snippets, and source URLs; preserve rate-limit boundary for later authenticated/current refresh.",
        },
        "rows": rows,
        "source_count": len(rows),
        "status_counts": {
            "captured": sum(1 for row in rows if row["status"] == "captured"),
            "captured_from_search_result": sum(1 for row in rows if row["status"] == "captured_from_search_result"),
        },
        "recommended_local_builds": [
            {
                "id": "agent_task_dag_contract_v1",
                "why": "Before launching many autonomous lane chats, define how one CEO goal becomes tasks, dependencies, assignees, checkpoints, and synthesis evidence.",
                "informed_by": ["open_multi_agent_goal_to_dag", "github_ai_agent_orchestration_article"],
            },
            {
                "id": "agent_governance_policy_kernel_gap_map_v1",
                "why": "Compare the existing approval/scope/authority/preflight chain with external governance-control-plane patterns.",
                "informed_by": ["cordum_governance_control_plane", "microsoft_agent_governance_toolkit"],
            },
            {
                "id": "computer_use_sandbox_boundary_matrix_v1",
                "why": "Browser, shell, file, MCP, VSCode, and desktop-control surfaces must be isolated before external workers can act safely.",
                "informed_by": ["agent_infra_aio_sandbox", "trycua_computer_use", "opensandbox_group_opensandbox", "auto_use_desktop_workspace"],
            },
            {
                "id": "browser_worker_recovery_loop_contract_v1",
                "why": "Browser automation should log recoveries, retries, observed state, and stop reasons before any approved public action worker exists.",
                "informed_by": ["browser_use_rust_core", "vercel_agent_browser"],
            },
            {
                "id": "agent_trace_eval_export_contract_v1",
                "why": "Scale requires per-lane learning/eval loops, cost/safety monitoring, and trace export without immediately adopting a hosted backend.",
                "informed_by": ["mlflow_agents_engineering_platform", "nvidia_nemo_agent_toolkit"],
            },
        ],
        "architecture_decision": "Keep the SQLite CEO ledger and service-request chain as source of truth. Add goal-to-DAG, governance-policy, sandbox-boundary, browser-recovery, and trace/eval contracts before any dependency install or external worker start.",
        "runtime_boundary": {
            "browser_sessions_started": 0,
            "account_actions": False,
            "wallet_actions": False,
            "payment_actions": False,
            "public_actions": False,
            "security_testing_actions": False,
            "real_money_actions": False,
            "model_api_calls": False,
            "dependency_installs": 0,
            "dependency_imports": 0,
            "runtime_starts": 0,
            "service_requests_updated": 0,
            "service_requests_assigned": 0,
            "worker_starts": 0,
            "external_side_effects": False,
        },
    }


def validate(payload: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    if payload["source_count"] != 13:
        failures.append(f"source_count_expected_13_got_{payload['source_count']}")
    if payload["status_counts"]["captured"] < 8:
        failures.append("captured_primary_accessible_sources_less_than_8")
    if len(payload["recommended_local_builds"]) != 5:
        failures.append("recommended_local_build_count_expected_5")
    categories = {row["category"] for row in payload["rows"]}
    for required in [
        "goal_to_dag_orchestration",
        "governance_control_plane",
        "computer_use_sandbox",
        "browser_worker_harness",
        "agent_observability_eval",
        "agent_sre_governance",
    ]:
        if required not in categories:
            failures.append(f"missing_category:{required}")
    for key, value in payload["runtime_boundary"].items():
        if value not in (0, False):
            failures.append(f"runtime_boundary_nonzero:{key}")
    return {
        "schema_version": "agent_company.execution_governance_radar_wave12_validation.v1",
        "generated_utc": utc_now(),
        "json_path": str(JSON_OUT),
        "markdown_path": str(MD_OUT),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "source_count": payload["source_count"],
        "recommended_local_build_count": len(payload["recommended_local_builds"]),
        "github_api_result": payload["github_api_boundary"]["api_result"],
        "browser_sessions_started": 0,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "security_testing_actions": False,
        "real_money_actions": False,
        "model_api_calls": False,
        "dependency_installs": 0,
        "dependency_imports": 0,
        "runtime_starts": 0,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "external_side_effects": False,
        "failures": failures,
    }


def write_markdown(payload: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Agent Company Execution Governance Radar Wave 12",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Capture UTC: {payload['capture_utc']}",
        f"Task: `{payload['task_id']}`",
        f"Dataset: `{JSON_OUT}`",
        f"Validation: `{VALIDATION_OUT}`",
        "",
        "## Purpose",
        "",
        payload["purpose"],
        "",
        "## Source Boundary",
        "",
        f"- Source rows: `{payload['source_count']}`",
        f"- Directly opened/captured source rows: `{payload['status_counts']['captured']}`",
        f"- Search-result captured rows: `{payload['status_counts']['captured_from_search_result']}`",
        f"- GitHub API batch result: `{payload['github_api_boundary']['api_result']}`",
        f"- Validation failures: `{validation['failure_count']}`",
        "",
        "## Ranked Signals",
        "",
        "| Score | Category | Source | Signal | Local Implication | Gate |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| `{row['priority_score']}` | `{row['category']}` | [{row['name']}]({row['url']}) | {row['signal']} | {row['local_implication']} | `{row['risk_gate']}` |"
        )
    lines.extend(
        [
            "",
            "## Recommended Local Builds",
            "",
            "| Build | Why | Informed By |",
            "| --- | --- | --- |",
        ]
    )
    for item in payload["recommended_local_builds"]:
        informed_by = ", ".join(f"`{source}`" for source in item["informed_by"])
        lines.append(f"| `{item['id']}` | {item['why']} | {informed_by} |")
    lines.extend(
        [
            "",
            "## Architecture Decision",
            "",
            payload["architecture_decision"],
            "",
            "## Boundary",
            "",
            "- Browser sessions started: `0`",
            "- Account/wallet/payment/public/security/real-money actions: `false`",
            "- Model/API calls: `false`",
            "- Dependency installs/imports: `0`",
            "- Runtime starts: `0`",
            "- Service requests updated/assigned: `0`",
            "- Worker starts: `0`",
            "- External side effects: `false`",
        ]
    )
    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    validation = validate(payload)
    JSON_OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_OUT.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(payload, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "report": str(MD_OUT)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
