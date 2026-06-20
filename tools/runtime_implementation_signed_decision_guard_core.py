#!/usr/bin/env python3
"""Validate signed runtime implementation decisions without applying them."""

from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
DURABLE = REPORTS / "durable-orchestration"
SCHEMA_PATH = ARCH / "runtime-implementation-signed-decision-guard-v1.schema.json"
APPROVAL_PACKET = DURABLE / "runtime-implementation-human-approval-packet-v2-20260617.json"
FIXTURE_DIR = DURABLE / "runtime-implementation-signed-decision-guard-v1-fixtures"
GUARD_JSON = DURABLE / "runtime-implementation-signed-decision-guard-v1-20260617.json"
VALIDATION_JSON = DURABLE / "runtime-implementation-signed-decision-guard-v1-validation-20260617.json"
GUARD_MD = DURABLE / "runtime-implementation-signed-decision-guard-v1-20260617.md"

ZERO_BOUNDARY = {
    "decisions_applied": 0,
    "approval_rows_written": 0,
    "dependency_installs": 0,
    "dependency_imports": 0,
    "runtime_starts": 0,
    "server_starts": 0,
    "database_provisioning": False,
    "service_requests_updated": 0,
    "service_requests_assigned": 0,
    "service_requests_started": 0,
    "worker_starts": 0,
    "browser_sessions_started": 0,
    "api_calls": False,
    "model_api_calls": False,
    "public_actions": False,
    "account_actions": False,
    "wallet_actions": False,
    "payment_actions": False,
    "security_testing_actions": False,
    "real_money_actions": False,
    "external_side_effects": False,
}

REQUIRED_FIELDS = [
    "schema_version",
    "decision_id",
    "source_approval_packet_path",
    "decision",
    "approver",
    "signed_utc",
    "expires_utc",
    "selected_runtime_id",
    "approved_question_ids",
    "denied_question_ids",
    "allowed_dependency_names",
    "allowed_runtime_processes",
    "allowed_database_or_cloud_resources",
    "service_request_mutation_scope",
    "provider_model_and_cost_cap",
    "artifact_output_path",
    "rollback_plan",
    "human_notes",
    "signature_attestation",
]

APPROVAL_ATTESTATION = (
    "I understand this signed decision is accepted for later preflight only "
    "and does not apply itself."
)
EVALUATION_UTC = "2026-06-17T18:00:00Z"

NEXT_ACTION = (
    "If a real signed human runtime decision is provided later, run it through this guard, "
    "then build a separate apply preflight before writing runtime code or mutating service_requests."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def question_ids(packet: dict[str, Any]) -> list[str]:
    return [item["question_id"] for item in packet["approval_questions"]]


def runtime_ids(packet: dict[str, Any]) -> set[str]:
    return {item["runtime_id"] for item in packet["runtime_candidates"]}


def runtime_rank(packet: dict[str, Any], runtime_id: str) -> int | None:
    for item in packet["runtime_candidates"]:
        if item["runtime_id"] == runtime_id:
            return int(item["rank"])
    return None


def base_decision(packet: dict[str, Any], decision_id: str, decision: str = "deny") -> dict[str, Any]:
    questions = question_ids(packet)
    selected = "none" if decision == "deny" else "sqlite_control_plane"
    approved = [] if decision == "deny" else ["approve_runtime_candidate"]
    denied = questions if decision == "deny" else [item for item in questions if item not in approved]
    artifact_output_path = ""
    rollback_plan = "No runtime work is applied by this decision guard; keep all executable work parked."
    human_notes = ""
    signature_attestation = "deny-all-no-runtime-work"
    if decision != "deny":
        artifact_output_path = str(
            DURABLE / "runtime-implementation-local-sqlite-control-plane-preflight-YYYYMMDD.json"
        )
        rollback_plan = (
            "Delete generated local preflight artifacts only; no service state, dependency, server, worker, "
            "API, browser, public, wallet, payment, or real-money state may be changed."
        )
        human_notes = "Local SQLite control plane preflight only."
        signature_attestation = APPROVAL_ATTESTATION

    return {
        "schema_version": "agent_company.runtime_implementation_signed_decision_guard.v1",
        "decision_id": decision_id,
        "source_approval_packet_path": str(APPROVAL_PACKET),
        "decision": decision,
        "approver": "human-operator",
        "signed_utc": "2026-06-17T18:00:00Z",
        "expires_utc": "2099-01-01T00:00:00Z",
        "selected_runtime_id": selected,
        "approved_question_ids": approved,
        "denied_question_ids": denied,
        "allowed_dependency_names": [],
        "allowed_runtime_processes": [],
        "allowed_database_or_cloud_resources": [],
        "service_request_mutation_scope": "none",
        "provider_model_and_cost_cap": "none",
        "artifact_output_path": artifact_output_path,
        "rollback_plan": rollback_plan,
        "human_notes": human_notes,
        "signature_attestation": signature_attestation,
    }


def fixture_set(packet: dict[str, Any]) -> list[dict[str, Any]]:
    fixtures: list[dict[str, Any]] = [
        {
            "name": "positive_deny_all",
            "expected": "accepted",
            "decision": base_decision(packet, "decision-positive-deny-all", "deny"),
        },
        {
            "name": "positive_sqlite_control_plane_report_only",
            "expected": "accepted",
            "decision": base_decision(
                packet,
                "decision-positive-sqlite-report-only",
                "approve_one_runtime_candidate",
            ),
        },
    ]

    def negative(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        decision = base_decision(packet, f"decision-negative-{name}", "approve_one_runtime_candidate")
        mutate(decision)
        fixtures.append({"name": f"negative_{name}", "expected": "rejected", "decision": decision})

    def scoped_update(*approved_ids: str, **extra: Any) -> Callable[[dict[str, Any]], None]:
        approved_set = set(approved_ids)

        def mutate(decision: dict[str, Any]) -> None:
            decision.update(
                {
                    "approved_question_ids": list(approved_ids),
                    "denied_question_ids": [q for q in question_ids(packet) if q not in approved_set],
                    **extra,
                }
            )

        return mutate

    negative("missing_approver", lambda d: d.update({"approver": ""}))
    negative("expired_decision", lambda d: d.update({"expires_utc": "2000-01-01T00:00:00Z"}))
    negative("unknown_runtime", lambda d: d.update({"selected_runtime_id": "made_up_runtime"}))
    negative("multiple_runtime_tokens", lambda d: d.update({"selected_runtime_id": "temporal_python,inngest"}))
    negative(
        "approved_without_runtime_question",
        lambda d: d.update({"approved_question_ids": [], "denied_question_ids": question_ids(packet)}),
    )
    negative(
        "dependency_without_names",
        scoped_update("approve_runtime_candidate", "approve_dependency_install_scope"),
    )
    negative(
        "wildcard_dependency",
        scoped_update(
            "approve_runtime_candidate",
            "approve_dependency_install_scope",
            allowed_dependency_names=["*"],
        ),
    )
    negative(
        "runtime_start_without_process",
        scoped_update("approve_runtime_candidate", "approve_runtime_start_scope"),
    )
    negative(
        "wildcard_service_request_mutation",
        scoped_update(
            "approve_runtime_candidate",
            "approve_service_request_mutation_scope",
            service_request_mutation_scope="all service_requests *",
        ),
    )
    negative(
        "model_api_without_cost_cap",
        scoped_update("approve_runtime_candidate", "approve_model_api_scope"),
    )
    negative(
        "browser_public_action_approved",
        scoped_update("approve_runtime_candidate", "approve_browser_or_public_action_scope"),
    )
    negative(
        "wallet_real_money_approved",
        scoped_update("approve_runtime_candidate", "approve_wallet_payment_real_money_scope"),
    )
    negative(
        "security_testing_approved",
        scoped_update("approve_runtime_candidate", "approve_security_testing_scope"),
    )
    negative(
        "non_top_runtime_without_rationale",
        lambda d: d.update({"selected_runtime_id": "temporal_python", "human_notes": ""}),
    )
    negative("missing_rollback_plan", lambda d: d.update({"rollback_plan": ""}))
    negative("overlapping_question_ids", lambda d: d.update({"denied_question_ids": question_ids(packet)}))
    negative("missing_attestation", lambda d: d.update({"signature_attestation": ""}))
    return fixtures

def validate_decision(decision: dict[str, Any], packet: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    questions = set(question_ids(packet))
    runtimes = runtime_ids(packet)
    evaluation_time = parse_utc(EVALUATION_UTC)

    for field in REQUIRED_FIELDS:
        if field not in decision:
            errors.append(f"missing_required_field:{field}")

    if decision.get("schema_version") != "agent_company.runtime_implementation_signed_decision_guard.v1":
        errors.append("schema_version_mismatch")
    if str(decision.get("source_approval_packet_path")) != str(APPROVAL_PACKET):
        errors.append("source_approval_packet_path_mismatch")
    if decision.get("decision") not in {"deny", "approve_one_runtime_candidate"}:
        errors.append("decision_value_invalid")
    for field in ["approver", "signed_utc", "expires_utc", "decision_id"]:
        if not str(decision.get(field, "")).strip():
            errors.append(f"{field}_empty")

    signed = parse_utc(str(decision.get("signed_utc", "")))
    expires = parse_utc(str(decision.get("expires_utc", "")))
    if signed is None:
        errors.append("signed_utc_invalid")
    if expires is None:
        errors.append("expires_utc_invalid")
    if signed and expires and expires <= signed:
        errors.append("expires_not_after_signed")
    if expires and evaluation_time and expires <= evaluation_time:
        errors.append("decision_expired")

    approved = decision.get("approved_question_ids", [])
    denied = decision.get("denied_question_ids", [])
    if not isinstance(approved, list) or not isinstance(denied, list):
        errors.append("question_id_sets_must_be_lists")
        approved = []
        denied = []
    approved_set = set(approved)
    denied_set = set(denied)
    if len(approved) != len(approved_set):
        errors.append("approved_question_ids_not_unique")
    if len(denied) != len(denied_set):
        errors.append("denied_question_ids_not_unique")
    unknown = (approved_set | denied_set) - questions
    if unknown:
        errors.append(f"unknown_question_ids:{','.join(sorted(unknown))}")
    overlap = approved_set & denied_set
    if overlap:
        errors.append(f"overlapping_question_ids:{','.join(sorted(overlap))}")
    if approved_set | denied_set != questions:
        errors.append("question_ids_do_not_partition_source_questions")

    selected_runtime = str(decision.get("selected_runtime_id", ""))
    decision_value = decision.get("decision")
    if decision_value == "deny":
        if selected_runtime != "none":
            errors.append("deny_decision_must_select_none")
        if approved_set:
            errors.append("deny_decision_must_approve_no_questions")
    else:
        if selected_runtime == "none":
            errors.append("approval_requires_selected_runtime")
        if "," in selected_runtime or " " in selected_runtime.strip():
            errors.append("selected_runtime_must_be_single_id")
        if selected_runtime not in runtimes:
            errors.append("selected_runtime_not_in_source_candidates")
        if "approve_runtime_candidate" not in approved_set:
            errors.append("approval_missing_approve_runtime_candidate_question")
        rank = runtime_rank(packet, selected_runtime)
        if rank and rank > 1 and "non-top-rationale:" not in str(decision.get("human_notes", "")):
            errors.append("non_top_runtime_requires_non_top_rationale")
        if decision.get("signature_attestation") != APPROVAL_ATTESTATION:
            errors.append("approval_signature_attestation_missing_or_wrong")

    high_risk_questions = {
        "approve_browser_or_public_action_scope": "browser_public_actions_forbidden_in_runtime_guard",
        "approve_wallet_payment_real_money_scope": "wallet_payment_real_money_forbidden_in_runtime_guard",
        "approve_security_testing_scope": "security_testing_forbidden_in_runtime_guard",
    }
    for question_id, error in high_risk_questions.items():
        if question_id in approved_set:
            errors.append(error)

    dependency_names = decision.get("allowed_dependency_names", [])
    runtime_processes = decision.get("allowed_runtime_processes", [])
    db_resources = decision.get("allowed_database_or_cloud_resources", [])
    if "approve_dependency_install_scope" in approved_set:
        if not dependency_names:
            errors.append("dependency_install_scope_requires_exact_dependency_names")
        if any(item in {"*", "latest", "any"} or "*" in str(item) for item in dependency_names):
            errors.append("dependency_names_must_not_be_wildcard")
    elif dependency_names:
        errors.append("dependency_names_present_without_dependency_approval")
    if "approve_runtime_start_scope" in approved_set:
        if not runtime_processes:
            errors.append("runtime_start_scope_requires_exact_processes")
    elif runtime_processes:
        errors.append("runtime_processes_present_without_runtime_start_approval")
    if "approve_database_or_cloud_scope" in approved_set:
        if not db_resources:
            errors.append("database_or_cloud_scope_requires_exact_resources")
    elif db_resources:
        errors.append("database_or_cloud_resources_present_without_approval")

    mutation_scope = str(decision.get("service_request_mutation_scope", ""))
    if "approve_service_request_mutation_scope" in approved_set:
        if not mutation_scope or mutation_scope == "none":
            errors.append("service_request_mutation_approval_requires_scope")
        if "*" in mutation_scope or "all" in mutation_scope.lower() or "any" in mutation_scope.lower():
            errors.append("service_request_mutation_scope_must_not_be_wildcard")
    elif mutation_scope != "none":
        errors.append("service_request_mutation_scope_present_without_approval")

    model_scope = str(decision.get("provider_model_and_cost_cap", ""))
    if "approve_model_api_scope" in approved_set:
        if not model_scope or model_scope == "none" or "cost" not in model_scope.lower():
            errors.append("model_api_approval_requires_provider_model_and_cost_cap")
    elif model_scope != "none":
        errors.append("provider_model_and_cost_cap_present_without_model_api_approval")

    artifact_path = str(decision.get("artifact_output_path", ""))
    if decision_value == "approve_one_runtime_candidate":
        if not artifact_path:
            errors.append("approval_requires_artifact_output_path")
        elif not artifact_path.startswith(str(ROOT)) or ".." in artifact_path:
            errors.append("artifact_output_path_must_be_inside_agent_company_lab")
        if len(str(decision.get("rollback_plan", "")).strip()) < 20:
            errors.append("approval_requires_specific_rollback_plan")
    elif artifact_path:
        warnings.append("deny_decision_ignores_artifact_output_path")

    accepted = not errors
    return {
        "decision_id": decision.get("decision_id"),
        "decision": decision.get("decision"),
        "selected_runtime_id": selected_runtime,
        "accepted_for_later_preflight": accepted,
        "rejected": not accepted,
        "errors": errors,
        "warnings": warnings,
        "apply_allowed": False,
        "runtime_implementation_allowed": False,
        "runtime_code_write_allowed": False,
        "runtime_boundary": copy.deepcopy(ZERO_BOUNDARY),
    }


def build_guard_report(packet: dict[str, Any], fixtures: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    results: list[dict[str, Any]] = []
    failures: list[str] = []
    for fixture in fixtures:
        decision = (
            copy.deepcopy(fixture["decision"])
            if "decision" in fixture
            else load_json(Path(fixture["path"]))
        )
        result = validate_decision(decision, packet)
        expected_accept = fixture["expected"] == "accepted"
        actual_accept = bool(result["accepted_for_later_preflight"])
        passed = expected_accept == actual_accept
        if not passed:
            failures.append(f"fixture_expectation_failed:{fixture['name']}:expected_{fixture['expected']}")
        results.append({**fixture, "passed": passed, "result": result})

    accepted = sum(1 for item in results if item["result"]["accepted_for_later_preflight"])
    rejected = sum(1 for item in results if item["result"]["rejected"])
    expected_accepted = sum(1 for item in fixtures if item["expected"] == "accepted")
    expected_rejected = sum(1 for item in fixtures if item["expected"] == "rejected")
    if accepted != expected_accepted:
        failures.append(f"accepted_count_expected_{expected_accepted}_got_{accepted}")
    if rejected != expected_rejected:
        failures.append(f"rejected_count_expected_{expected_rejected}_got_{rejected}")

    generated = utc_now()
    report = {
        "schema_version": "agent_company.runtime_implementation_signed_decision_guard_report.v1",
        "generated_utc": generated,
        "source_approval_packet_path": str(APPROVAL_PACKET),
        "source_approval_packet_sha256": sha256_path(APPROVAL_PACKET),
        "schema_path": str(SCHEMA_PATH),
        "fixture_dir": str(FIXTURE_DIR),
        "fixture_count": len(fixtures),
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "accepted_count": accepted,
        "rejected_count": rejected,
        "results": results,
        "guard_boundary": copy.deepcopy(ZERO_BOUNDARY),
        "decisions_applied": 0,
        "runtime_implementation_allowed": False,
        "runtime_code_write_allowed": False,
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "next_action": NEXT_ACTION,
    }
    validation = {
        "schema_version": "agent_company.runtime_implementation_signed_decision_guard_validation.v1",
        "generated_utc": generated,
        "guard_report_path": str(GUARD_JSON),
        "markdown_path": str(GUARD_MD),
        "schema_path": str(SCHEMA_PATH),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "fixture_count": len(fixtures),
        "accepted_count": accepted,
        "rejected_count": rejected,
        "expected_accepted_count": expected_accepted,
        "expected_rejected_count": expected_rejected,
        "decisions_applied": 0,
        "approval_rows_written": 0,
        "runtime_implementation_allowed": False,
        "runtime_code_write_allowed": False,
        "dependency_installs": 0,
        "dependency_imports": 0,
        "runtime_starts": 0,
        "server_starts": 0,
        "database_provisioning": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "service_requests_started": 0,
        "worker_starts": 0,
        "browser_sessions_started": 0,
        "api_calls": False,
        "model_api_calls": False,
        "public_actions": False,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "security_testing_actions": False,
        "real_money_actions": False,
        "external_side_effects": False,
        "failures": failures,
    }
    return report, validation


