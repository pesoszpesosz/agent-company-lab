#!/usr/bin/env python3
"""Write Wave 11 current-source radar for agent-company platform surfaces."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
JSON_OUT = DATA / "agent-company-current-source-radar-wave11-20260617.json"
CSV_OUT = DATA / "agent-company-current-source-radar-wave11-20260617.csv"
MD_OUT = REPORTS / "agent-company-current-source-radar-wave11-20260617.md"
VALIDATION_OUT = REPORTS / "agent-company-current-source-radar-wave11-validation-20260617.json"

GENERATED_UTC = "2026-06-17T18:05:00Z"

REPO_ROWS: list[dict[str, Any]] = [
    {
        "category": "agent_platform_control_plane",
        "full_name": "agno-agi/agno",
        "html_url": "https://github.com/agno-agi/agno",
        "official_url": "https://www.agno.com/",
        "stars": 40749,
        "pushed_at": "2026-06-17T17:15:36Z",
        "local_decision": "study_control_plane_patterns",
        "why_it_matters": "Directly aligned with running agent platforms with tracing, scheduling, RBAC, and a control plane; compare to our SQLite CEO ledger before any install.",
        "risk_gate": "report_only_no_dependency_install_no_runtime_start",
    },
    {
        "category": "typescript_agent_app_framework",
        "full_name": "mastra-ai/mastra",
        "html_url": "https://github.com/mastra-ai/mastra",
        "official_url": "https://mastra.ai/",
        "stars": 25178,
        "pushed_at": "2026-06-17T18:04:15Z",
        "local_decision": "watch_ts_agent_app_surface",
        "why_it_matters": "Modern TypeScript agent app stack with workflows, agents, memory, and observability; useful if the company needs a web-facing agent app layer.",
        "risk_gate": "report_only_no_node_install_no_server_start",
    },
    {
        "category": "typescript_agent_ops_platform",
        "full_name": "VoltAgent/voltagent",
        "html_url": "https://github.com/voltagent/voltagent",
        "official_url": "https://voltagent.dev/",
        "stars": 9659,
        "pushed_at": "2026-06-08T20:06:55Z",
        "local_decision": "watch_observability_guardrails_evals",
        "why_it_matters": "Combines framework primitives with operations-console ideas: observability, evals, guardrails, deployment, prompts, automation.",
        "risk_gate": "report_only_no_console_no_cloud_no_deploy",
    },
    {
        "category": "production_agent_harness",
        "full_name": "strands-agents/harness-sdk",
        "html_url": "https://github.com/strands-agents/harness-sdk",
        "official_url": "https://strandsagents.com/",
        "stars": 6186,
        "pushed_at": "2026-06-17T17:10:42Z",
        "local_decision": "watch_harness_and_intervention_primitives",
        "why_it_matters": "Production-agent harness direction with Python/TypeScript SDKs; useful as a pattern source for intervention, tools, memory, and multi-agent harnessing.",
        "risk_gate": "report_only_no_sdk_install_no_model_api",
    },
    {
        "category": "agent_app_builder",
        "full_name": "langgenius/dify",
        "html_url": "https://github.com/langgenius/dify",
        "official_url": "https://dify.ai/",
        "stars": 145619,
        "pushed_at": "2026-06-17T17:49:19Z",
        "local_decision": "reference_for_product_studio_and_app_builder",
        "why_it_matters": "Huge adoption signal for visual agent/RAG/app building; useful as a product-studio reference, not as the internal company source of truth.",
        "risk_gate": "report_only_no_container_no_account_no_public_app",
    },
    {
        "category": "agent_app_builder",
        "full_name": "langflow-ai/langflow",
        "html_url": "https://github.com/langflow-ai/langflow",
        "official_url": "https://www.langflow.org/",
        "stars": 149790,
        "pushed_at": "2026-06-17T18:02:48Z",
        "local_decision": "reference_for_visual_flow_patterns",
        "why_it_matters": "Large visual-flow adoption signal; useful for UI/graph inspiration and productization routes, not for autonomous execution gates.",
        "risk_gate": "report_only_no_flow_execution_no_api_keys",
    },
    {
        "category": "workflow_automation",
        "full_name": "n8n-io/n8n",
        "html_url": "https://github.com/n8n-io/n8n",
        "official_url": "https://n8n.io/",
        "stars": 192938,
        "pushed_at": "2026-06-17T17:59:25Z",
        "local_decision": "reference_for_service_worker_workflow_ui",
        "why_it_matters": "Very high adoption for workflow automation and integrations; relevant for service-worker queues, but dangerous around credentials and public actions.",
        "risk_gate": "report_only_no_credentials_no_workflow_execution",
    },
    {
        "category": "workflow_automation",
        "full_name": "activepieces/activepieces",
        "html_url": "https://github.com/activepieces/activepieces",
        "official_url": "https://www.activepieces.com/",
        "stars": 22801,
        "pushed_at": "2026-06-17T17:22:19Z",
        "local_decision": "watch_as_open_workflow_automation_alternative",
        "why_it_matters": "Open workflow automation surface that may inspire service-worker recipes and approval-gated integrations.",
        "risk_gate": "report_only_no_credentials_no_workflow_execution",
    },
    {
        "category": "agent_app_builder",
        "full_name": "FlowiseAI/Flowise",
        "html_url": "https://github.com/FlowiseAI/Flowise",
        "official_url": "https://flowiseai.com/",
        "stars": 53686,
        "pushed_at": "2026-06-16T11:05:50Z",
        "local_decision": "reference_for_low_code_agent_pipeline_ui",
        "why_it_matters": "Mature low-code LLM/agent workflow builder; useful for comparing productized dashboard UX and connector patterns.",
        "risk_gate": "report_only_no_node_install_no_api_keys",
    },
    {
        "category": "coding_agent_harness",
        "full_name": "OpenHands/OpenHands",
        "html_url": "https://github.com/OpenHands/OpenHands",
        "official_url": "https://www.all-hands.dev/",
        "stars": 77538,
        "pushed_at": "2026-06-17T18:04:44Z",
        "local_decision": "sandboxed_code_worker_pattern_candidate",
        "why_it_matters": "High-adoption autonomous coding agent harness; relevant for future code-worker lanes, but only inside strict workspace/sandbox and public-action gates.",
        "risk_gate": "report_only_no_code_execution_no_pr_public_action",
    },
    {
        "category": "sandbox_execution",
        "full_name": "e2b-dev/E2B",
        "html_url": "https://github.com/e2b-dev/E2B",
        "official_url": "https://e2b.dev/",
        "stars": 12632,
        "pushed_at": "2026-06-17T15:50:01Z",
        "local_decision": "sandbox_contract_candidate",
        "why_it_matters": "Agent sandboxing is a likely missing department primitive for untrusted code, generated tools, and reproducible worker runs.",
        "risk_gate": "report_only_no_cloud_sandbox_no_api_key_no_cost",
    },
]

RATE_LIMITED_REPOS = [
    "daytonaio/daytona",
    "BerriAI/litellm",
    "Helicone/helicone",
    "AgentOps-AI/agentops",
    "microsoft/semantic-kernel",
    "Kilo-Org/kilocode",
    "sst/opencode",
    "Significant-Gravitas/AutoGPT",
]

SOURCE_REFERENCES = [
    "https://github.com/agno-agi/agno",
    "https://www.agno.com/",
    "https://github.com/mastra-ai/mastra",
    "https://mastra.ai/",
    "https://github.com/voltagent/voltagent",
    "https://voltagent.dev/",
    "https://github.com/strands-agents/harness-sdk",
    "https://strandsagents.com/",
    "https://github.com/langgenius/dify",
    "https://github.com/langflow-ai/langflow",
    "https://github.com/n8n-io/n8n",
    "https://github.com/activepieces/activepieces",
    "https://github.com/FlowiseAI/Flowise",
    "https://github.com/OpenHands/OpenHands",
    "https://github.com/e2b-dev/E2B",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def recency_score(pushed_at: str) -> int:
    if pushed_at.startswith("2026-06-17"):
        return 5
    if pushed_at.startswith("2026-06"):
        return 4
    if pushed_at.startswith("2026"):
        return 3
    return 1


def star_score(stars: int) -> int:
    if stars >= 100000:
        return 5
    if stars >= 50000:
        return 4
    if stars >= 20000:
        return 3
    if stars >= 5000:
        return 2
    return 1


def enrich_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in REPO_ROWS:
        enriched = dict(row)
        enriched["source_type"] = "github_public_metadata_manual_capture"
        enriched["collected_utc"] = GENERATED_UTC
        enriched["recency_score"] = recency_score(row["pushed_at"])
        enriched["star_score"] = star_score(int(row["stars"]))
        enriched["agent_company_fit_score"] = (
            enriched["recency_score"]
            + enriched["star_score"]
            + (2 if row["category"] in {"agent_platform_control_plane", "production_agent_harness", "sandbox_execution"} else 1)
        )
        rows.append(enriched)
    return sorted(rows, key=lambda item: (item["agent_company_fit_score"], item["stars"]), reverse=True)


def build_payload(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "agent_company.current_source_radar_wave11.v1",
        "generated_utc": utc_now(),
        "capture_utc": GENERATED_UTC,
        "task_id": "task-agent-company-current-source-radar-wave11-20260617",
        "lane_id": "platform_engineering",
        "purpose": "Fresh primary-source radar for production agent-company platform surfaces beyond the Wave 10 runtime/core-infra scan.",
        "source_references": SOURCE_REFERENCES,
        "repo_count": len(rows),
        "rate_limited_repo_count": len(RATE_LIMITED_REPOS),
        "rate_limited_repos": RATE_LIMITED_REPOS,
        "rows": rows,
        "decision_summary": {
            "promote_local_next": [
                {
                    "id": "agent_platform_capability_matrix_v1",
                    "why": "Compare Agno, Mastra, VoltAgent, Strands, and current SQLite control-plane capabilities before any dependency install.",
                },
                {
                    "id": "sandbox_execution_gate_contract_v1",
                    "why": "E2B/OpenHands/Daytona-style workers need a local contract for code execution, secrets, files, network, cost, and teardown.",
                },
                {
                    "id": "workflow_automation_service_worker_manifest_v1",
                    "why": "n8n, Activepieces, Flowise, Dify, and Langflow should inform service-worker recipe UX while all credentials and actions remain gated.",
                },
            ],
            "hold_until_gated": [
                "workflow execution",
                "container or cloud sandbox start",
                "credential/API key use",
                "public app deployment",
                "model/provider execution",
                "public GitHub or marketplace action",
            ],
            "architecture_decision": "Keep SQLite/service-request packets as the source of truth. Use the new platform/app-builder/workflow/sandbox projects as pattern sources and adapter candidates only.",
        },
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


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    if payload["repo_count"] != 11:
        failures.append(f"repo_count_expected_11_got_{payload['repo_count']}")
    if payload["rate_limited_repo_count"] < 1:
        failures.append("rate_limit_boundary_not_recorded")
    categories = {row["category"] for row in payload["rows"]}
    for category in ["agent_platform_control_plane", "workflow_automation", "agent_app_builder", "coding_agent_harness", "sandbox_execution"]:
        if category not in categories:
            failures.append(f"missing_category:{category}")
    for key, expected in payload["runtime_boundary"].items():
        if expected not in (0, False):
            failures.append(f"runtime_boundary_expected_zero_or_false:{key}")
    if len(payload["decision_summary"]["promote_local_next"]) != 3:
        failures.append("expected_three_local_next_builds")
    return {
        "schema_version": "agent_company.current_source_radar_wave11_validation.v1",
        "generated_utc": utc_now(),
        "report_path": str(MD_OUT),
        "json_path": str(JSON_OUT),
        "csv_path": str(CSV_OUT),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "repo_count": payload["repo_count"],
        "rate_limited_repo_count": payload["rate_limited_repo_count"],
        "source_reference_count": len(payload["source_references"]),
        "recommended_local_build_count": len(payload["decision_summary"]["promote_local_next"]),
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


def write_csv(rows: list[dict[str, Any]]) -> None:
    fields = [
        "category",
        "full_name",
        "stars",
        "pushed_at",
        "agent_company_fit_score",
        "local_decision",
        "risk_gate",
        "html_url",
        "official_url",
    ]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})


def write_markdown(payload: dict[str, Any], validation: dict[str, Any]) -> None:
    rows = payload["rows"]
    lines = [
        "# Agent Company Current-Source Radar Wave 11",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Capture UTC: {payload['capture_utc']}",
        f"Task: `{payload['task_id']}`",
        f"Dataset: `{JSON_OUT}`",
        f"CSV: `{CSV_OUT}`",
        f"Validation: `{VALIDATION_OUT}`",
        "",
        "## Purpose",
        "",
        "Refresh the platform radar for the parts of an agent company that sit around the core runtime: control planes, agent app builders, workflow automation, coding-agent harnesses, and sandboxes. This wave is read-only and does not install, execute, deploy, register, submit, or call model APIs.",
        "",
        "## Source Boundary",
        "",
        f"- GitHub/API metadata rows captured: `{payload['repo_count']}`",
        f"- Repos noted but rate-limited before metadata capture: `{payload['rate_limited_repo_count']}`",
        f"- Validation failures: `{validation['failure_count']}`",
        "",
        "Rate-limited follow-ups to revisit later: "
        + ", ".join(f"`{repo}`" for repo in payload["rate_limited_repos"]),
        "",
        "## Ranked Current Signals",
        "",
        "| Fit | Stars | Last Push | Category | Repo | Local Decision | Gate |",
        "| ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['agent_company_fit_score']}` | `{row['stars']}` | `{row['pushed_at']}` | `{row['category']}` | [{row['full_name']}]({row['html_url']}) | `{row['local_decision']}` | `{row['risk_gate']}` |"
        )
    lines.extend(
        [
            "",
            "## Architecture Takeaways",
            "",
            "1. Agent-platform projects are converging on exactly the company primitives we need: control plane, tracing, scheduling, RBAC, intervention, workflow, memory, evals, and deployment. The right move is a local capability matrix, not an immediate framework replacement.",
            "2. Visual app builders and workflow tools have massive adoption, but their default posture is connector execution. They belong behind service-worker manifests, credential gates, and approval scopes.",
            "3. Coding-agent and sandbox projects are strategically important because future money lanes will ask workers to run code, inspect repos, and make patches. That needs a sandbox execution gate contract first.",
            "4. The current SQLite CEO ledger remains the brain. These projects are pattern sources, UI references, and possible adapters.",
            "",
            "## Recommended Local Builds",
            "",
            "| Build | Why |",
            "| --- | --- |",
        ]
    )
    for item in payload["decision_summary"]["promote_local_next"]:
        lines.append(f"| `{item['id']}` | {item['why']} |")
    lines.extend(
        [
            "",
            "## Hold Until Gated",
            "",
        ]
    )
    for item in payload["decision_summary"]["hold_until_gated"]:
        lines.append(f"- `{item}`")
    lines.extend(
        [
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
    rows = enrich_rows()
    payload = build_payload(rows)
    validation = validate_payload(payload)
    JSON_OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_csv(rows)
    VALIDATION_OUT.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(payload, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "report": str(MD_OUT)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
