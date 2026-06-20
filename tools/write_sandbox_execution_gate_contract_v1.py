#!/usr/bin/env python3
"""Write sandbox execution gate contract v1 from the platform capability matrix."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
MATRIX_PATH = REPORTS / "agent-platform-capability-matrix-v1-20260617.json"
SCHEMA_PATH = ARCH / "sandbox-execution-gate-contract-v1.schema.json"
JSON_OUT = REPORTS / "sandbox-execution-gate-contract-v1-20260617.json"
MD_OUT = REPORTS / "sandbox-execution-gate-contract-v1-20260617.md"
VALIDATION_OUT = REPORTS / "sandbox-execution-gate-contract-v1-validation-20260617.json"

ZERO_BOUNDARY = {
    "sandbox_sessions_started": 0,
    "processes_started": 0,
    "commands_executed": 0,
    "files_written_outside_workspace": 0,
    "network_enabled": False,
    "secrets_read": False,
    "api_keys_used": False,
    "cloud_sandbox_started": False,
    "dependency_installs": 0,
    "dependency_imports": 0,
    "runtime_starts": 0,
    "service_requests_updated": 0,
    "service_requests_assigned": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "model_api_calls": False,
    "public_actions": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "security_testing_actions": False,
    "real_money_actions": False,
    "external_side_effects": False,
}

REQUIRED_APPROVAL_FIELDS = [
    "decision_id",
    "approver",
    "signed_utc",
    "expires_utc",
    "lane_id",
    "task_id",
    "sandbox_provider",
    "workspace_root",
    "allowed_commands",
    "allowed_file_roots",
    "network_policy",
    "secret_policy",
    "dependency_policy",
    "time_limit_seconds",
    "cost_limit_usd",
    "artifact_capture_paths",
    "teardown_plan",
    "rollback_plan",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def select_candidates(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in matrix["rows"]:
        if row["recommended_posture"] == "promote_to_sandbox_gate_contract":
            rows.append(
                {
                    "full_name": row["full_name"],
                    "category": row["category"],
                    "html_url": row["html_url"],
                    "official_url": row["official_url"],
                    "risk_gate": row["risk_gate"],
                    "reason": row["why_it_matters"],
                }
            )
    return rows


def default_policy() -> dict[str, Any]:
    return {
        "approval_required": True,
        "sandbox_provider": "none",
        "workspace_root": "none",
        "network_policy": "deny",
        "secret_policy": "deny_all",
        "dependency_policy": "deny_install_and_import",
        "process_policy": "deny",
        "file_write_policy": "deny_outside_named_workspace",
        "public_action_policy": "deny",
        "cloud_cost_policy": "deny",
        "teardown_required": True,
        "artifact_capture_required": True,
    }


def allowed_after_approval() -> dict[str, Any]:
    return {
        "sandbox_provider": "exact_provider_only",
        "workspace_root": "exact_local_or_approved_remote_workspace_only",
        "commands": "exact_allowlist_only",
        "file_roots": "exact_allowlist_only",
        "network": "deny_by_default_allow_explicit_hosts_only",
        "secrets": "deny_by_default_named_secret_route_only",
        "dependencies": "deny_by_default_exact_package_version_only",
        "time_limit_seconds": "required_positive_integer",
        "cost_limit_usd": "required_zero_or_positive_cap",
        "artifact_capture": "required_local_paths",
        "teardown": "required_before_complete",
    }


def hard_denies() -> list[str]:
    return [
        "unbounded_network_access",
        "wildcard_filesystem_write",
        "ambient_secrets_or_environment_dump",
        "unbounded_dependency_install",
        "public_pr_issue_comment_or_submission",
        "browser_or_account_action",
        "wallet_payment_real_money_action",
        "live_security_testing_or_exploitation",
        "service_request_mutation_without_separate_approval",
        "cloud_sandbox_start_without_cost_cap",
    ]


def negative_probes() -> list[dict[str, Any]]:
    probes = [
        ("network_any", {"network_policy": "allow_all"}, "unbounded_network_access"),
        ("workspace_any_write", {"allowed_file_roots": ["*"]}, "wildcard_filesystem_write"),
        ("ambient_secrets", {"secret_policy": "allow_environment"}, "ambient_secrets_or_environment_dump"),
        ("pip_latest", {"dependency_policy": "pip install latest"}, "unbounded_dependency_install"),
        ("public_pr", {"allowed_commands": ["gh pr create"]}, "public_pr_issue_comment_or_submission"),
        ("browser_login", {"allowed_commands": ["open browser and login"]}, "browser_or_account_action"),
        ("wallet_action", {"allowed_commands": ["send wallet transaction"]}, "wallet_payment_real_money_action"),
        ("security_scan_live", {"allowed_commands": ["scan live target"]}, "live_security_testing_or_exploitation"),
        ("service_mutation", {"service_request_mutation": "start req-*"}, "service_request_mutation_without_separate_approval"),
        ("cloud_no_cost_cap", {"sandbox_provider": "e2b", "cost_limit_usd": None}, "cloud_sandbox_start_without_cost_cap"),
    ]
    return [
        {
            "probe_id": probe_id,
            "input": payload,
            "expected_disposition": "reject",
            "required_rejection_reason": reason,
        }
        for probe_id, payload, reason in probes
    ]


def validate_probe(probe: dict[str, Any]) -> dict[str, Any]:
    payload = probe["input"]
    reason = probe["required_rejection_reason"]
    rejected = False
    if reason == "unbounded_network_access" and payload.get("network_policy") == "allow_all":
        rejected = True
    elif reason == "wildcard_filesystem_write" and "*" in payload.get("allowed_file_roots", []):
        rejected = True
    elif reason == "ambient_secrets_or_environment_dump" and payload.get("secret_policy") == "allow_environment":
        rejected = True
    elif reason == "unbounded_dependency_install" and "latest" in payload.get("dependency_policy", ""):
        rejected = True
    elif reason == "public_pr_issue_comment_or_submission" and any("gh pr" in cmd for cmd in payload.get("allowed_commands", [])):
        rejected = True
    elif reason == "browser_or_account_action" and any("browser" in cmd or "login" in cmd for cmd in payload.get("allowed_commands", [])):
        rejected = True
    elif reason == "wallet_payment_real_money_action" and any("wallet" in cmd or "transaction" in cmd for cmd in payload.get("allowed_commands", [])):
        rejected = True
    elif reason == "live_security_testing_or_exploitation" and any("live target" in cmd or "scan" in cmd for cmd in payload.get("allowed_commands", [])):
        rejected = True
    elif reason == "service_request_mutation_without_separate_approval" and payload.get("service_request_mutation"):
        rejected = True
    elif reason == "cloud_sandbox_start_without_cost_cap" and payload.get("sandbox_provider") and payload.get("cost_limit_usd") is None:
        rejected = True
    return {
        "probe_id": probe["probe_id"],
        "passed": rejected,
        "disposition": "reject" if rejected else "unexpected_accept",
        "reason": reason if rejected else "missing_rejection",
    }


def build_contract() -> dict[str, Any]:
    matrix = load_json(MATRIX_PATH)
    return {
        "schema_version": "agent_company.sandbox_execution_gate_contract.v1",
        "generated_utc": utc_now(),
        "task_id": "task-sandbox-execution-gate-contract-v1-20260617",
        "lane_id": "platform_engineering",
        "purpose": "Define the minimum approval contract before any OpenHands/E2B/Daytona-style code worker, cloud sandbox, or generated-tool execution can start.",
        "source_matrix_path": str(MATRIX_PATH),
        "candidate_patterns": select_candidates(matrix),
        "required_approval_fields": REQUIRED_APPROVAL_FIELDS,
        "default_policy": default_policy(),
        "allowed_after_approval": allowed_after_approval(),
        "hard_denies": hard_denies(),
        "negative_probes": negative_probes(),
        "runtime_boundary": ZERO_BOUNDARY.copy(),
        "next_action": "Build a sandbox execution approval packet and fixture runner before any sandbox provider, command execution, dependency install, network access, secret route, or service-worker start.",
    }


def validate_contract(contract: dict[str, Any]) -> dict[str, Any]:
    probe_results = [validate_probe(probe) for probe in contract["negative_probes"]]
    failures: list[str] = []
    if len(contract["candidate_patterns"]) < 2:
        failures.append("expected_at_least_two_sandbox_candidate_patterns")
    if len(contract["required_approval_fields"]) != len(REQUIRED_APPROVAL_FIELDS):
        failures.append("required_approval_field_count_mismatch")
    if len(contract["hard_denies"]) != 10:
        failures.append("hard_deny_count_mismatch")
    if any(not result["passed"] for result in probe_results):
        failures.extend(f"negative_probe_failed:{result['probe_id']}" for result in probe_results if not result["passed"])
    for key, value in contract["runtime_boundary"].items():
        if value not in (0, False):
            failures.append(f"runtime_boundary_nonzero:{key}")
    return {
        "schema_version": "agent_company.sandbox_execution_gate_contract_validation.v1",
        "generated_utc": utc_now(),
        "contract_path": str(JSON_OUT),
        "markdown_path": str(MD_OUT),
        "schema_path": str(SCHEMA_PATH),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "candidate_pattern_count": len(contract["candidate_patterns"]),
        "required_approval_field_count": len(contract["required_approval_fields"]),
        "hard_deny_count": len(contract["hard_denies"]),
        "negative_probe_count": len(contract["negative_probes"]),
        "negative_probe_rejected_count": sum(1 for result in probe_results if result["passed"]),
        "probe_results": probe_results,
        **ZERO_BOUNDARY,
        "failures": failures,
    }


def write_markdown(contract: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Sandbox Execution Gate Contract v1",
        "",
        f"Generated UTC: {contract['generated_utc']}",
        f"Task: `{contract['task_id']}`",
        f"Source matrix: `{MATRIX_PATH}`",
        f"Contract JSON: `{JSON_OUT}`",
        f"Validation: `{VALIDATION_OUT}`",
        f"Schema: `{SCHEMA_PATH}`",
        "",
        "## Summary",
        "",
        f"- Candidate patterns: `{validation['candidate_pattern_count']}`",
        f"- Required approval fields: `{validation['required_approval_field_count']}`",
        f"- Hard denies: `{validation['hard_deny_count']}`",
        f"- Negative probes rejected: `{validation['negative_probe_rejected_count']}` of `{validation['negative_probe_count']}`",
        f"- Validation failures: `{validation['failure_count']}`",
        "",
        "## Candidate Patterns",
        "",
        "| Candidate | Category | Contract Use |",
        "| --- | --- | --- |",
    ]
    for item in contract["candidate_patterns"]:
        lines.append(f"| [{item['full_name']}]({item['html_url']}) | `{item['category']}` | {item['reason']} |")
    lines.extend(["", "## Required Approval Fields", ""])
    for field in contract["required_approval_fields"]:
        lines.append(f"- `{field}`")
    lines.extend(["", "## Hard Denies", ""])
    for item in contract["hard_denies"]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Negative Probes", "", "| Probe | Result | Reason |", "| --- | --- | --- |"])
    for result in validation["probe_results"]:
        lines.append(f"| `{result['probe_id']}` | `{result['disposition']}` | `{result['reason']}` |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- No sandbox session, process, command, dependency install/import, network access, secret use, API key use, cloud sandbox, service-request mutation, worker start, browser session, model/API call, public/account/wallet/payment/security/real-money action, or external side effect occurred.",
        ]
    )
    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    contract = build_contract()
    validation = validate_contract(contract)
    JSON_OUT.write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_OUT.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(contract, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "contract": str(JSON_OUT)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
