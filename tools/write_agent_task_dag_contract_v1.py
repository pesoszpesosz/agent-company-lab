#!/usr/bin/env python3
"""Generate a report-only CEO task-DAG contract for agent-company dispatch."""

from __future__ import annotations

import json
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"E:\agent-company-lab")
ARCH = ROOT / "architecture"
REPORTS = ROOT / "reports"
DATA = ROOT / "data"

SCHEMA_PATH = ARCH / "agent-task-dag-contract-v1.schema.json"
JSON_OUT = REPORTS / "agent-task-dag-contract-v1-20260617.json"
MD_OUT = REPORTS / "agent-task-dag-contract-v1-20260617.md"
VALIDATION_OUT = REPORTS / "agent-task-dag-contract-v1-validation-20260617.json"

TASK_ID = "task-agent-task-dag-contract-v1-20260617"
DAG_ID = "dag-agent-company-scaleout-v1-20260617"
OWNER_AGENT_ID = "recovered-profitable-edge-infra"
LANE_ID = "platform_engineering"


SOURCE_GOAL = (
    "Build an expandable company-style AI-agent infrastructure that studies all online money paths, "
    "dispatches agents by lane, manages workers for gated needs such as browser/account/wallet/legal/payment "
    "tasks, keeps CEO-level oversight, and records findings for later use."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def node(
    node_id: str,
    lane_id: str,
    agent_role: str,
    task_type: str,
    title: str,
    status: str,
    allowed_actions: list[str],
    prohibited_actions: list[str],
    inputs: list[str],
    outputs: list[str],
    success_criteria: list[str],
    risk_gate: str,
) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "lane_id": lane_id,
        "agent_role": agent_role,
        "task_type": task_type,
        "title": title,
        "status": status,
        "allowed_actions": allowed_actions,
        "prohibited_actions": prohibited_actions,
        "inputs": inputs,
        "outputs": outputs,
        "success_criteria": success_criteria,
        "risk_gate": risk_gate,
    }


def build_contract() -> dict[str, Any]:
    prohibited_external = [
        "register_accounts",
        "accept_terms_or_cla",
        "create_or_control_wallet",
        "submit_public_post_or_comment",
        "submit_bounty_claim_or_security_report",
        "place_real_money_trade",
        "share_payment_details",
        "start_external_runtime_or_browser_worker",
    ]
    nodes = [
        node(
            "node-ceo-intake",
            "platform_engineering",
            "ceo",
            "synthesis",
            "Normalize the user objective into company requirements",
            "ready_local_only",
            ["read local reports", "extract requirements", "write local artifact"],
            prohibited_external,
            ["active goal text", "E:\\agent-company-lab\\README.md", "latest CEO review"],
            ["requirements map", "lane dispatch criteria"],
            ["Explicit lanes, worker types, gates, and evidence requirements are listed"],
            "local_only",
        ),
        node(
            "node-source-radar",
            "platform_engineering",
            "infrastructure_scout",
            "research",
            "Refresh open-source agent infrastructure radar",
            "ready_local_only",
            ["read public docs", "read public GitHub pages", "write local report"],
            prohibited_external,
            ["Wave 11 radar", "Wave 12 execution-governance radar"],
            ["ranked infrastructure source set", "recommended local builds"],
            ["Sources are linked and risk gates are recorded"],
            "public_read_only",
        ),
        node(
            "node-dag-contract",
            "platform_engineering",
            "control_plane_builder",
            "implementation_contract",
            "Create report-only task-DAG dispatch contract",
            "ready_local_only",
            ["write schema", "write sample DAG", "validate acyclicity"],
            prohibited_external,
            ["execution governance radar", "service-worker chain reports"],
            ["agent_task_dag_contract_v1 schema", "validated sample DAG"],
            ["Graph is acyclic and every node has lane, role, outputs, criteria, and gate"],
            "local_only",
        ),
        node(
            "node-money-lane-refresh",
            "money_source_discovery",
            "source_mapper",
            "research",
            "Map currently monetizable source families",
            "blocked_by_gate",
            ["prepare read-only source list", "write local source matrix"],
            prohibited_external,
            ["money-path coverage audit", "profit-edge import"],
            ["source family matrix", "refresh request packet"],
            ["Every source family has venue, expected payout path, account gate, and first proof action"],
            "browser_read_only_or_current_source_gate",
        ),
        node(
            "node-paid-code-proof",
            "paid_code_bounties",
            "repo_triager",
            "local_proof",
            "Triage one clean paid-code candidate into a proof packet",
            "blocked_by_gate",
            ["read local queue", "check duplicate status", "write local decision packet"],
            prohibited_external,
            ["paid-code worksheet", "fresh bounty queue"],
            ["candidate proof packet", "claim/PR gate decision"],
            ["Candidate is open, payout route is explicit, duplicate risk is classified"],
            "public_read_only_or_github_public_action_gate",
        ),
        node(
            "node-security-proof",
            "security_bounty_private_reports",
            "program_rules_reader",
            "local_proof",
            "Promote one security hypothesis to rules-safe proof status",
            "blocked_by_gate",
            ["read public code", "write local patch/repro draft", "write rules review packet"],
            prohibited_external,
            ["security evidence queue", "program scope notes"],
            ["rules-safe proof packet", "submission decision packet"],
            ["Scope, impact, reproduction, and submission gate are explicit"],
            "security_testing_and_report_submission_gate",
        ),
        node(
            "node-digital-product-proof",
            "digital_products_templates_plugins",
            "market_gap_scout",
            "local_proof",
            "Prepare digital product package for private review",
            "ready_local_only",
            ["read local package files", "write checklist", "write private review packet"],
            prohibited_external,
            ["Agent Skill Starter Kit package", "marketplace readiness matrix"],
            ["private review packet", "post-approval simulation plan"],
            ["Package assets, copy, risks, and marketplace gates are complete"],
            "local_only_until_marketplace_gate",
        ),
        node(
            "node-browser-service-request",
            "platform_engineering",
            "browser_action_worker",
            "service_request",
            "Prepare exact-scope browser read-only worker request",
            "blocked_by_gate",
            ["write request packet", "write allowed/prohibited actions", "write expected evidence fields"],
            prohibited_external,
            ["source radar needs", "lane proof blockers"],
            ["service-worker request packet", "exact-scope template"],
            ["Request is ready for human/CRO decision but grants no approval"],
            "human_cro_approval_gate_required",
        ),
        node(
            "node-worker-pool-preflight",
            "platform_engineering",
            "control_plane_builder",
            "review",
            "Verify worker pool and assignment preconditions",
            "ready_local_only",
            ["read pool registry", "read assignment plan", "write preflight result"],
            prohibited_external,
            ["service-worker pool registry", "assignment plan", "gate map"],
            ["assignment preflight result"],
            ["No worker is startable unless approval, scope, pool registration, assignment, and readiness all pass"],
            "local_only",
        ),
        node(
            "node-ceo-synthesis",
            "platform_engineering",
            "ceo",
            "synthesis",
            "Synthesize lane outputs into next dispatch batch",
            "ready_local_only",
            ["read evidence packets", "rank next work", "write CEO dispatch board"],
            prohibited_external,
            ["lane proof packets", "service gate map", "trace report"],
            ["CEO dispatch board", "next DAG revision"],
            ["Each promoted action has evidence, owner, gate, and expected output"],
            "local_only",
        ),
    ]
    edges = [
        {"from": "node-ceo-intake", "to": "node-source-radar", "reason": "Requirements define what sources matter"},
        {"from": "node-source-radar", "to": "node-dag-contract", "reason": "Fresh orchestration signals inform DAG structure"},
        {"from": "node-dag-contract", "to": "node-money-lane-refresh", "reason": "Lane refresh becomes a typed DAG node"},
        {"from": "node-dag-contract", "to": "node-paid-code-proof", "reason": "Paid-code proof follows dispatch contract"},
        {"from": "node-dag-contract", "to": "node-security-proof", "reason": "Security proof follows dispatch contract"},
        {"from": "node-dag-contract", "to": "node-digital-product-proof", "reason": "Product proof follows dispatch contract"},
        {"from": "node-money-lane-refresh", "to": "node-browser-service-request", "reason": "Blocked source refresh needs exact browser scope"},
        {"from": "node-paid-code-proof", "to": "node-browser-service-request", "reason": "Live issue verification needs browser/GitHub read-only gate"},
        {"from": "node-security-proof", "to": "node-browser-service-request", "reason": "Rendered program rules may need browser read-only gate"},
        {"from": "node-browser-service-request", "to": "node-worker-pool-preflight", "reason": "Worker pools are checked only after exact request scope exists"},
        {"from": "node-digital-product-proof", "to": "node-ceo-synthesis", "reason": "Local proof can be synthesized immediately"},
        {"from": "node-worker-pool-preflight", "to": "node-ceo-synthesis", "reason": "Gated work reports readiness or hold reason"},
    ]
    gates = [
        {
            "gate_id": "gate-browser-readonly",
            "gate_type": "browser_read_only_session",
            "blocks_nodes": ["node-money-lane-refresh", "node-paid-code-proof", "node-security-proof", "node-browser-service-request"],
            "approval_required_by": ["human_user", "chief_risk_officer"],
            "reason": "Live browser/GitHub/marketplace verification may touch session state or platform terms.",
        },
        {
            "gate_id": "gate-security-submission",
            "gate_type": "security_report_submission",
            "blocks_nodes": ["node-security-proof"],
            "approval_required_by": ["human_user", "chief_risk_officer"],
            "reason": "Private vulnerability reports and security testing require scope and submission approval.",
        },
        {
            "gate_id": "gate-public-action",
            "gate_type": "public_action_execution",
            "blocks_nodes": ["node-paid-code-proof", "node-digital-product-proof"],
            "approval_required_by": ["human_user", "reputation_review_worker"],
            "reason": "Claims, PR comments, marketplace listings, posts, or submissions create public commitments.",
        },
    ]
    evidence_requirements = [
        {
            "evidence_id": "evidence-node-status",
            "required_for": "every_node",
            "artifact_kind": "json_or_markdown",
            "minimum_fields": ["node_id", "lane_id", "owner_role", "status", "gate", "next_action"],
        },
        {
            "evidence_id": "evidence-gate-decision",
            "required_for": "blocked_by_gate_node",
            "artifact_kind": "decision_packet",
            "minimum_fields": ["requested_action", "allowed_actions", "prohibited_actions", "approval_required_by", "do_not_execute_clause"],
        },
        {
            "evidence_id": "evidence-proof-output",
            "required_for": "local_proof_node",
            "artifact_kind": "proof_packet",
            "minimum_fields": ["source", "method", "result", "confidence", "next_action"],
        },
    ]
    return {
        "schema_version": "agent_company.agent_task_dag_contract.v1",
        "dag_id": DAG_ID,
        "generated_utc": utc_now(),
        "objective": "Create a report-only dispatch DAG for scaling the agent company across money lanes and gated workers.",
        "source_goal": SOURCE_GOAL,
        "owner_agent_id": OWNER_AGENT_ID,
        "nodes": nodes,
        "edges": edges,
        "gates": gates,
        "evidence_requirements": evidence_requirements,
        "runtime_boundary": {
            "report_only": True,
            "approves_actions": False,
            "starts_workers": False,
            "updates_service_requests": False,
            "calls_apis": False,
            "external_side_effects": False,
        },
    }


def validate_contract(contract: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    node_ids = [node["node_id"] for node in contract["nodes"]]
    node_set = set(node_ids)
    if len(node_set) != len(node_ids):
        failures.append("duplicate_node_id")
    for edge in contract["edges"]:
        if edge["from"] not in node_set:
            failures.append(f"edge_from_missing:{edge['from']}")
        if edge["to"] not in node_set:
            failures.append(f"edge_to_missing:{edge['to']}")
    graph: dict[str, list[str]] = defaultdict(list)
    indegree = {node_id: 0 for node_id in node_ids}
    for edge in contract["edges"]:
        if edge["from"] in node_set and edge["to"] in node_set:
            graph[edge["from"]].append(edge["to"])
            indegree[edge["to"]] += 1
    queue = deque([node_id for node_id, degree in indegree.items() if degree == 0])
    visited: list[str] = []
    while queue:
        current = queue.popleft()
        visited.append(current)
        for target in graph[current]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if len(visited) != len(node_ids):
        failures.append("dag_cycle_detected")
    for item in contract["nodes"]:
        if not item["outputs"]:
            failures.append(f"node_missing_outputs:{item['node_id']}")
        if not item["success_criteria"]:
            failures.append(f"node_missing_success_criteria:{item['node_id']}")
        if item["status"] == "blocked_by_gate" and "gate" not in item["risk_gate"]:
            failures.append(f"blocked_node_gate_label_weak:{item['node_id']}")
        prohibited_text = " ".join(item["prohibited_actions"])
        for required in ["register_accounts", "create_or_control_wallet", "submit_public_post_or_comment", "place_real_money_trade"]:
            if required not in prohibited_text:
                failures.append(f"node_missing_prohibition:{item['node_id']}:{required}")
    gated_nodes = {node_id for gate in contract["gates"] for node_id in gate["blocks_nodes"]}
    for item in contract["nodes"]:
        if item["status"] == "blocked_by_gate" and item["node_id"] not in gated_nodes:
            failures.append(f"blocked_node_not_in_gate:{item['node_id']}")
    for key, expected in contract["runtime_boundary"].items():
        if key == "report_only":
            if expected is not True:
                failures.append("runtime_boundary_report_only_not_true")
        elif expected is not False:
            failures.append(f"runtime_boundary_not_false:{key}")
    return {
        "schema_version": "agent_company.agent_task_dag_contract_validation.v1",
        "generated_utc": utc_now(),
        "schema_path": str(SCHEMA_PATH),
        "json_path": str(JSON_OUT),
        "markdown_path": str(MD_OUT),
        "all_checks_passed": not failures,
        "failure_count": len(failures),
        "node_count": len(contract["nodes"]),
        "edge_count": len(contract["edges"]),
        "gate_count": len(contract["gates"]),
        "evidence_requirement_count": len(contract["evidence_requirements"]),
        "topological_order": visited,
        "approves_actions": False,
        "starts_workers": False,
        "updates_service_requests": False,
        "calls_apis": False,
        "external_side_effects": False,
        "failures": failures,
    }


def write_markdown(contract: dict[str, Any], validation: dict[str, Any]) -> None:
    lines = [
        "# Agent Task DAG Contract v1",
        "",
        f"Generated UTC: {contract['generated_utc']}",
        f"DAG: `{contract['dag_id']}`",
        f"Task: `{TASK_ID}`",
        f"Schema: `{SCHEMA_PATH}`",
        f"JSON: `{JSON_OUT}`",
        f"Validation: `{VALIDATION_OUT}`",
        "",
        "## Purpose",
        "",
        contract["objective"],
        "",
        "## Validation",
        "",
        f"- Nodes: `{validation['node_count']}`",
        f"- Edges: `{validation['edge_count']}`",
        f"- Gates: `{validation['gate_count']}`",
        f"- Evidence requirements: `{validation['evidence_requirement_count']}`",
        f"- Failures: `{validation['failure_count']}`",
        f"- Topological order: {', '.join(f'`{node_id}`' for node_id in validation['topological_order'])}",
        "",
        "## Nodes",
        "",
        "| Node | Lane | Role | Type | Status | Gate | Output |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in contract["nodes"]:
        lines.append(
            f"| `{item['node_id']}` | `{item['lane_id']}` | `{item['agent_role']}` | `{item['task_type']}` | `{item['status']}` | `{item['risk_gate']}` | {', '.join(item['outputs'])} |"
        )
    lines.extend(["", "## Edges", "", "| From | To | Reason |", "| --- | --- | --- |"])
    for edge in contract["edges"]:
        lines.append(f"| `{edge['from']}` | `{edge['to']}` | {edge['reason']} |")
    lines.extend(["", "## Gates", "", "| Gate | Type | Blocks | Required Approval |", "| --- | --- | --- | --- |"])
    for gate in contract["gates"]:
        lines.append(
            f"| `{gate['gate_id']}` | `{gate['gate_type']}` | {', '.join(f'`{node_id}`' for node_id in gate['blocks_nodes'])} | {', '.join(f'`{role}`' for role in gate['approval_required_by'])} |"
        )
    lines.extend(["", "## Evidence Requirements", "", "| Evidence | Required For | Kind | Fields |", "| --- | --- | --- | --- |"])
    for item in contract["evidence_requirements"]:
        lines.append(
            f"| `{item['evidence_id']}` | `{item['required_for']}` | `{item['artifact_kind']}` | {', '.join(f'`{field}`' for field in item['minimum_fields'])} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This contract is report-only.",
            "- It approves no actions, starts no workers, updates no service requests, calls no APIs, and performs no external side effects.",
            "- External browser/account/wallet/payment/public/security/trading actions remain blocked until separate exact-scope approval and readiness checks pass.",
        ]
    )
    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    contract = build_contract()
    validation = validate_contract(contract)
    JSON_OUT.write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    VALIDATION_OUT.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(contract, validation)
    print(json.dumps({"ok": validation["all_checks_passed"], "failure_count": validation["failure_count"], "report": str(MD_OUT)}, indent=2))
    return 0 if validation["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
