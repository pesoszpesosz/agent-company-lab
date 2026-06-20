#!/usr/bin/env python3
"""Write a report-only scorecard for external agent/runtime adapter candidates."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
DATA = ROOT / "data"
SCHEMA_PATH = ARCH / "adapter-candidate-scorecard-v1.schema.json"
WAVE15_DATA = DATA / "agent-company-current-source-radar-wave15-20260617.json"
WAVE15_VALIDATION = REPORTS / "agent-company-current-source-radar-wave15-validation-20260617.json"
CHECKPOINT_VALIDATION = REPORTS / "checkpoint-interrupt-contract-v1-validation-20260617.json"
REPORT_JSON = REPORTS / "adapter-candidate-scorecard-v1-20260617.json"
VALIDATION_JSON = REPORTS / "adapter-candidate-scorecard-v1-validation-20260617.json"
REPORT_MD = REPORTS / "adapter-candidate-scorecard-v1-20260617.md"

ZERO_BOUNDARY = {
    "report_only": True,
    "runtime_adoption_allowed": False,
    "dependency_install_allowed": False,
    "worker_start_allowed": False,
    "worker_starts": 0,
    "runtime_starts": 0,
    "dependency_installs": 0,
    "dependency_imports": 0,
    "model_api_calls": False,
    "browser_sessions_started": 0,
    "mcp_tool_calls": False,
    "service_requests_assigned": 0,
    "service_requests_updated": 0,
    "public_actions": False,
    "payment_actions": False,
    "wallet_actions": False,
    "external_side_effects": False,
}

ADAPTER_PROFILES = {
    "langchain-ai/langgraph": {
        "adapter_class": "checkpoint_graph_runtime_candidate",
        "company_fit": 96,
        "integration_risk": 74,
        "first_local_adapter": "checkpoint_interrupt_bridge_fixture",
        "required_gates": [
            "checkpoint_interrupt_contract_v1",
            "runtime_start_preflight",
            "signed_operator_runtime_decision",
            "model_api_execution_gate",
        ],
        "recommendation": "pattern_first_score_high",
    },
    "temporalio/temporal": {
        "adapter_class": "durable_workflow_runtime_candidate",
        "company_fit": 93,
        "integration_risk": 88,
        "first_local_adapter": "service_request_history_replay_manifest",
        "required_gates": [
            "checkpoint_interrupt_contract_v1",
            "runtime_start_preflight",
            "signed_operator_runtime_decision",
            "dependency_install_gate",
        ],
        "recommendation": "defer_until_runtime_adoption_packet",
    },
    "restatedev/restate": {
        "adapter_class": "durable_agent_runtime_candidate",
        "company_fit": 91,
        "integration_risk": 82,
        "first_local_adapter": "journaled_tool_call_fixture",
        "required_gates": [
            "checkpoint_interrupt_contract_v1",
            "runtime_start_preflight",
            "signed_operator_runtime_decision",
            "egress_event_ledger",
        ],
        "recommendation": "pattern_first_score_high",
    },
    "microsoft/agent-framework": {
        "adapter_class": "manager_worker_reviewer_workflow_candidate",
        "company_fit": 87,
        "integration_risk": 79,
        "first_local_adapter": "manager_reviewer_escalation_fixture",
        "required_gates": [
            "checkpoint_interrupt_contract_v1",
            "model_api_execution_gate",
            "cloud_or_foundry_scope_gate",
            "signed_operator_runtime_decision",
        ],
        "recommendation": "study_hitl_workflow_before_runtime",
    },
    "crewAIInc/crewAI": {
        "adapter_class": "role_team_orchestration_candidate",
        "company_fit": 82,
        "integration_risk": 67,
        "first_local_adapter": "role_team_dispatch_fixture",
        "required_gates": [
            "checkpoint_interrupt_contract_v1",
            "dependency_install_gate",
            "model_api_execution_gate",
        ],
        "recommendation": "extract_role_taxonomy_not_runtime",
    },
    "All-Hands-AI/OpenHands": {
        "adapter_class": "coding_agent_harness_candidate",
        "company_fit": 90,
        "integration_risk": 92,
        "first_local_adapter": "sandboxed_code_worker_scope_fixture",
        "required_gates": [
            "sandbox_execution_gate",
            "github_public_action_gate",
            "secrets_credentials_handling_gate",
            "checkpoint_interrupt_contract_v1",
        ],
        "recommendation": "only_after_sandbox_execution_contract",
    },
    "google/adk-python": {
        "adapter_class": "agent_packaging_eval_candidate",
        "company_fit": 78,
        "integration_risk": 70,
        "first_local_adapter": "eval_packaging_manifest_fixture",
        "required_gates": [
            "model_api_execution_gate",
            "dependency_install_gate",
            "credential_scope_gate",
            "checkpoint_interrupt_contract_v1",
        ],
        "recommendation": "study_eval_packaging_later",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_rows(dataset: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for repo in dataset.get("repos", []):
        name = repo["repo"]
        profile = ADAPTER_PROFILES[name]
        score = int(profile["company_fit"]) - int(profile["integration_risk"] * 0.35) + int(repo["fit_score"] * 2)
        rows.append(
            {
                "schema_version": "agent_company.adapter_candidate_scorecard_row.v1",
                "repo": name,
                "url": repo["html_url"],
                "category": repo["category"],
                "adapter_class": profile["adapter_class"],
                "stars": repo["stars"],
                "pushed_at": repo["pushed_at"],
                "license": repo["license"],
                "company_fit": profile["company_fit"],
                "integration_risk": profile["integration_risk"],
                "local_adoption_score": score,
                "first_local_adapter": profile["first_local_adapter"],
                "required_gates": profile["required_gates"],
                "recommendation": profile["recommendation"],
                "runtime_adoption_allowed": False,
                "dependency_install_allowed": False,
                "worker_start_allowed": False,
                "next_local_build": profile["first_local_adapter"],
            }
        )
    rows.sort(key=lambda item: (-item["local_adoption_score"], item["repo"]))
    for index, row in enumerate(rows, start=1):
        row["rank"] = index
    return rows


def build_scorecard() -> tuple[dict[str, Any], dict[str, Any]]:
    schema = load_json(SCHEMA_PATH)
    dataset = load_json(WAVE15_DATA)
    wave15_validation = load_json(WAVE15_VALIDATION)
    checkpoint_validation = load_json(CHECKPOINT_VALIDATION)
    failures: list[str] = []

    if schema.get("properties", {}).get("selected_for_runtime_adoption_count", {}).get("const") != 0:
        failures.append("schema_must_force_zero_runtime_adoptions")
    if wave15_validation.get("all_checks_passed") is not True or wave15_validation.get("repo_count") != 7:
        failures.append("wave15_validation_not_ready")
    if checkpoint_validation.get("all_checks_passed") is not True or checkpoint_validation.get("accepted_count") != 3:
        failures.append("checkpoint_interrupt_contract_not_ready")

    rows = build_rows(dataset)
    if len(rows) != 7:
        failures.append(f"expected_7_candidate_rows_got_{len(rows)}")
    missing = sorted(set(ADAPTER_PROFILES) - {row["repo"] for row in rows})
    if missing:
        failures.append("missing_adapter_profiles:" + ",".join(missing))
    if any(row["runtime_adoption_allowed"] or row["dependency_install_allowed"] or row["worker_start_allowed"] for row in rows):
        failures.append("one_or_more_rows_allows_runtime_dependency_or_worker_start")
    if any("checkpoint_interrupt_contract_v1" not in row["required_gates"] for row in rows):
        failures.append("one_or_more_rows_missing_checkpoint_interrupt_gate")

    generated = utc_now()
    payload = {
        "schema_version": "agent_company.adapter_candidate_scorecard.v1",
        "generated_utc": generated,
        "source_dataset": str(WAVE15_DATA),
        "source_wave15_validation": str(WAVE15_VALIDATION),
        "source_checkpoint_validation": str(CHECKPOINT_VALIDATION),
        "candidate_count": len(rows),
        "selected_for_runtime_adoption_count": 0,
        "runtime_adoption_allowed": False,
        "dependency_install_allowed": False,
        "worker_start_allowed": False,
        "candidate_rows": rows,
        "recommended_next_local_build": rows[0]["first_local_adapter"] if rows else "",
        "recommended_next_candidate": rows[0]["repo"] if rows else "",
        **ZERO_BOUNDARY,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": "Build the top-ranked local adapter fixture only as report-only scaffolding; do not install dependencies or start runtimes.",
    }
    validation = {
        "schema_version": "agent_company.adapter_candidate_scorecard_validation.v1",
        "generated_utc": generated,
        "scorecard_path": str(REPORT_JSON),
        "markdown_path": str(REPORT_MD),
        "schema_path": str(SCHEMA_PATH),
        "candidate_count": len(rows),
        "selected_for_runtime_adoption_count": 0,
        "recommended_next_candidate": payload["recommended_next_candidate"],
        "recommended_next_local_build": payload["recommended_next_local_build"],
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        **ZERO_BOUNDARY,
        "failures": failures,
    }
    return payload, validation


def write_markdown(payload: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Adapter Candidate Scorecard v1",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Scorecard JSON: `{REPORT_JSON}`",
        f"Validation JSON: `{VALIDATION_JSON}`",
        f"Source dataset: `{WAVE15_DATA}`",
        f"Checkpoint validation: `{CHECKPOINT_VALIDATION}`",
        "",
        "## Summary",
        "",
        f"- All checks passed: `{validation['all_checks_passed']}`",
        f"- Candidate count: `{validation['candidate_count']}`",
        f"- Selected for runtime adoption: `{validation['selected_for_runtime_adoption_count']}`",
        f"- Recommended next candidate: `{validation['recommended_next_candidate']}`",
        f"- Recommended next local build: `{validation['recommended_next_local_build']}`",
        f"- Dependency installs: `{validation['dependency_installs']}`",
        f"- Runtime starts: `{validation['runtime_starts']}`",
        f"- Worker starts: `{validation['worker_starts']}`",
        f"- External side effects: `{validation['external_side_effects']}`",
        "",
        "## Ranked Candidates",
        "",
        "| Rank | Score | Candidate | Class | First Local Adapter | Required Gates | Recommendation |",
        "| ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    for row in payload["candidate_rows"]:
        gates = ", ".join(row["required_gates"])
        lines.append(
            f"| {row['rank']} | `{row['local_adoption_score']}` | [{row['repo']}]({row['url']}) | "
            f"`{row['adapter_class']}` | `{row['first_local_adapter']}` | {gates} | `{row['recommendation']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This scorecard selects zero candidates for runtime adoption.",
            "- It installs no dependencies and imports no external frameworks.",
            "- It starts no runtime, worker, browser session, model call, MCP tool, public action, payment, or wallet action.",
            "- Every candidate remains behind checkpoint interrupt, runtime/dependency, credential, cost, sandbox, or public-action gates as applicable.",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    payload, validation = build_scorecard()
    REPORT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(payload, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "validation": str(VALIDATION_JSON)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
