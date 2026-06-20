from __future__ import annotations

from typing import Any, Callable

"""CLI parser and dispatch helpers for service-worker commands."""

from agent_company_core.schema import init_db
from agent_company_core.service_worker_integrity import write_service_worker_chain_integrity
from agent_company_core.service_workers import (
    write_service_worker_approval_review,
    write_service_worker_assignment_plan,
    write_service_worker_decision_authority_matrix,
    write_service_worker_decision_command_safety,
    write_service_worker_decision_drift_guard,
    write_service_worker_decision_preflight,
    write_service_worker_dequeue_plan,
    write_service_worker_execution_readiness,
    write_service_worker_gate_map,
    write_service_worker_human_decision_packets,
    write_service_worker_pool_registration_plan,
    write_service_worker_pool_registry,
    write_service_worker_post_decision_refresh_plan,
    write_service_worker_post_decision_simulation,
    write_service_worker_queue,
    write_service_worker_scope_diff,
    write_service_worker_scope_templates,
)


SERVICE_WORKER_CLI_COMMANDS = (
    "write-service-worker-queue",
    "write-service-worker-dequeue-plan",
    "write-service-worker-execution-readiness",
    "write-service-worker-scope-diff",
    "write-service-worker-scope-templates",
    "write-service-worker-approval-review",
    "write-service-worker-assignment-plan",
    "write-service-worker-pool-registry",
    "write-service-worker-pool-registration-plan",
    "write-service-worker-gate-map",
    "write-service-worker-chain-integrity",
    "write-service-worker-human-decision-packets",
    "write-service-worker-post-decision-simulation",
    "write-service-worker-post-decision-refresh-plan",
    "write-service-worker-decision-drift-guard",
    "write-service-worker-decision-command-safety",
    "write-service-worker-decision-authority-matrix",
    "write-service-worker-decision-preflight",
)


def add_service_worker_commands(sub: Any) -> None:
    service_worker_queue = sub.add_parser("write-service-worker-queue")
    service_worker_queue.add_argument("--path")
    service_worker_queue.add_argument("--json-path")
    service_worker_queue.add_argument("--validation-path")
    service_worker_dequeue = sub.add_parser("write-service-worker-dequeue-plan")
    service_worker_dequeue.add_argument("--path")
    service_worker_dequeue.add_argument("--json-path")
    service_worker_dequeue.add_argument("--validation-path")
    service_worker_dequeue.add_argument("--result-dir")
    service_worker_readiness = sub.add_parser("write-service-worker-execution-readiness")
    service_worker_readiness.add_argument("--path")
    service_worker_readiness.add_argument("--json-path")
    service_worker_readiness.add_argument("--validation-path")
    service_worker_readiness.add_argument("--request-id")
    service_worker_readiness.add_argument("--lane-id")
    service_worker_readiness.add_argument("--status")
    service_worker_readiness.add_argument("--worker-agent-id")
    service_worker_scope_diff = sub.add_parser("write-service-worker-scope-diff")
    service_worker_scope_diff.add_argument("--path")
    service_worker_scope_diff.add_argument("--json-path")
    service_worker_scope_diff.add_argument("--validation-path")
    service_worker_scope_diff.add_argument("--request-id")
    service_worker_scope_diff.add_argument("--lane-id")
    service_worker_scope_diff.add_argument("--status")
    service_worker_scope_templates = sub.add_parser("write-service-worker-scope-templates")
    service_worker_scope_templates.add_argument("--path")
    service_worker_scope_templates.add_argument("--json-path")
    service_worker_scope_templates.add_argument("--validation-path")
    service_worker_scope_templates.add_argument("--request-id")
    service_worker_scope_templates.add_argument("--lane-id")
    service_worker_scope_templates.add_argument("--status")
    service_worker_approval_review = sub.add_parser("write-service-worker-approval-review")
    service_worker_approval_review.add_argument("--path")
    service_worker_approval_review.add_argument("--json-path")
    service_worker_approval_review.add_argument("--validation-path")
    service_worker_approval_review.add_argument("--request-id")
    service_worker_approval_review.add_argument("--lane-id")
    service_worker_approval_review.add_argument("--status")
    service_worker_assignment_plan = sub.add_parser("write-service-worker-assignment-plan")
    service_worker_assignment_plan.add_argument("--path")
    service_worker_assignment_plan.add_argument("--json-path")
    service_worker_assignment_plan.add_argument("--validation-path")
    service_worker_assignment_plan.add_argument("--request-id")
    service_worker_assignment_plan.add_argument("--lane-id")
    service_worker_assignment_plan.add_argument("--status")
    service_worker_pool_registry = sub.add_parser("write-service-worker-pool-registry")
    service_worker_pool_registry.add_argument("--path")
    service_worker_pool_registry.add_argument("--json-path")
    service_worker_pool_registry.add_argument("--validation-path")
    service_worker_pool_registration = sub.add_parser("write-service-worker-pool-registration-plan")
    service_worker_pool_registration.add_argument("--path")
    service_worker_pool_registration.add_argument("--json-path")
    service_worker_pool_registration.add_argument("--validation-path")
    service_worker_gate_map = sub.add_parser("write-service-worker-gate-map")
    service_worker_gate_map.add_argument("--path")
    service_worker_gate_map.add_argument("--json-path")
    service_worker_gate_map.add_argument("--validation-path")
    service_worker_gate_map.add_argument("--request-id")
    service_worker_gate_map.add_argument("--lane-id")
    service_worker_gate_map.add_argument("--status")
    service_worker_chain_integrity = sub.add_parser("write-service-worker-chain-integrity")
    service_worker_chain_integrity.add_argument("--path")
    service_worker_chain_integrity.add_argument("--json-path")
    service_worker_chain_integrity.add_argument("--validation-path")
    service_worker_human_decision_packets = sub.add_parser("write-service-worker-human-decision-packets")
    service_worker_human_decision_packets.add_argument("--path")
    service_worker_human_decision_packets.add_argument("--json-path")
    service_worker_human_decision_packets.add_argument("--validation-path")
    service_worker_human_decision_packets.add_argument("--packet-dir")
    service_worker_post_decision_simulation = sub.add_parser("write-service-worker-post-decision-simulation")
    service_worker_post_decision_simulation.add_argument("--path")
    service_worker_post_decision_simulation.add_argument("--json-path")
    service_worker_post_decision_simulation.add_argument("--validation-path")
    service_worker_post_decision_refresh_plan = sub.add_parser("write-service-worker-post-decision-refresh-plan")
    service_worker_post_decision_refresh_plan.add_argument("--path")
    service_worker_post_decision_refresh_plan.add_argument("--json-path")
    service_worker_post_decision_refresh_plan.add_argument("--validation-path")
    service_worker_decision_drift_guard = sub.add_parser("write-service-worker-decision-drift-guard")
    service_worker_decision_drift_guard.add_argument("--path")
    service_worker_decision_drift_guard.add_argument("--json-path")
    service_worker_decision_drift_guard.add_argument("--validation-path")
    service_worker_decision_command_safety = sub.add_parser("write-service-worker-decision-command-safety")
    service_worker_decision_command_safety.add_argument("--path")
    service_worker_decision_command_safety.add_argument("--json-path")
    service_worker_decision_command_safety.add_argument("--validation-path")
    service_worker_decision_authority_matrix = sub.add_parser("write-service-worker-decision-authority-matrix")
    service_worker_decision_authority_matrix.add_argument("--path")
    service_worker_decision_authority_matrix.add_argument("--json-path")
    service_worker_decision_authority_matrix.add_argument("--validation-path")
    service_worker_decision_preflight = sub.add_parser("write-service-worker-decision-preflight")
    service_worker_decision_preflight.add_argument("--path")
    service_worker_decision_preflight.add_argument("--json-path")
    service_worker_decision_preflight.add_argument("--validation-path")


def service_worker_command_handlers() -> dict[str, Callable[[Any, Any], None]]:
    return {
        "write-service-worker-queue": write_service_worker_queue,
        "write-service-worker-dequeue-plan": write_service_worker_dequeue_plan,
        "write-service-worker-execution-readiness": write_service_worker_execution_readiness,
        "write-service-worker-scope-diff": write_service_worker_scope_diff,
        "write-service-worker-scope-templates": write_service_worker_scope_templates,
        "write-service-worker-approval-review": write_service_worker_approval_review,
        "write-service-worker-assignment-plan": write_service_worker_assignment_plan,
        "write-service-worker-pool-registry": write_service_worker_pool_registry,
        "write-service-worker-pool-registration-plan": write_service_worker_pool_registration_plan,
        "write-service-worker-gate-map": write_service_worker_gate_map,
        "write-service-worker-chain-integrity": write_service_worker_chain_integrity,
        "write-service-worker-human-decision-packets": write_service_worker_human_decision_packets,
        "write-service-worker-post-decision-simulation": write_service_worker_post_decision_simulation,
        "write-service-worker-post-decision-refresh-plan": write_service_worker_post_decision_refresh_plan,
        "write-service-worker-decision-drift-guard": write_service_worker_decision_drift_guard,
        "write-service-worker-decision-command-safety": write_service_worker_decision_command_safety,
        "write-service-worker-decision-authority-matrix": write_service_worker_decision_authority_matrix,
        "write-service-worker-decision-preflight": write_service_worker_decision_preflight,
    }


def handle_service_worker_command(conn: Any, args: Any) -> bool:
    handler = service_worker_command_handlers().get(args.cmd)
    if handler is None:
        return False
    init_db(conn)
    handler(conn, args)
    return True


__all__ = [
    "SERVICE_WORKER_CLI_COMMANDS",
    "add_service_worker_commands",
    "handle_service_worker_command",
    "service_worker_command_handlers",
]