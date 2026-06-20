from __future__ import annotations

from typing import Any, Callable

"""CLI parser and dispatch helpers for registry and service-request commands."""

from agent_company_core.registry import (
    acquire_task,
    claim_lane,
    complete_task,
    create_task,
    record_artifact,
    record_outcome,
    register_agent,
    release_task,
    update_task,
)
from agent_company_core.schema import init_db
from agent_company_core.service_requests import (
    approve_service_request,
    assign_service_request,
    complete_service_request,
    create_service_request,
    reject_service_request,
    scaffold_service_request,
    start_service_request,
    validate_service_request,
)


REGISTRY_SERVICE_REQUEST_COMMANDS = (
    "register-agent",
    "claim-lane",
    "create-task",
    "create-service-request",
    "scaffold-service-request",
    "validate-service-request",
    "approve-service-request",
    "reject-service-request",
    "assign-service-request",
    "start-service-request",
    "complete-service-request",
    "update-task",
    "acquire-task",
    "release-task",
    "complete-task",
    "record-artifact",
    "record-outcome",
)


def add_registry_service_request_commands(sub: Any) -> None:
    register = sub.add_parser("register-agent")
    register.add_argument("--agent-id", required=True)
    register.add_argument("--role-id", required=True)
    register.add_argument("--thread-id")
    register.add_argument("--department-id")

    claim = sub.add_parser("claim-lane")
    claim.add_argument("--lane-id", required=True)
    claim.add_argument("--agent-id", required=True)
    claim.add_argument("--thread-id", required=True)
    claim.add_argument("--force", action="store_true")

    task = sub.add_parser("create-task")
    task.add_argument("--task-id", required=True)
    task.add_argument("--lane-id", required=True)
    task.add_argument("--title", required=True)
    task.add_argument("--priority", type=int, default=50)
    task.add_argument("--owner-agent-id")
    task.add_argument("--duplicate-key")
    task.add_argument("--evidence-required")
    task.add_argument("--next-action")

    req = sub.add_parser("create-service-request")
    req.add_argument("--request-id", required=True)
    req.add_argument("--service-id")
    req.add_argument("--request-type", required=True)
    req.add_argument("--lane-id")
    req.add_argument("--requester-agent-id")
    req.add_argument("--risk-gate", required=True)
    req.add_argument("--requested-action", required=True)
    req.add_argument("--intake-json")
    req.add_argument("--intake-file")
    req.add_argument("--approval-scope")
    req.add_argument("--artifact-path")

    scaffold_req = sub.add_parser("scaffold-service-request")
    scaffold_req.add_argument("--request-id")
    scaffold_req.add_argument("--service-id")
    scaffold_req.add_argument("--request-type")
    scaffold_req.add_argument("--lane-id", required=True)
    scaffold_req.add_argument("--requester-agent-id")
    scaffold_req.add_argument("--task-id")
    scaffold_req.add_argument("--risk-gate")
    scaffold_req.add_argument("--requested-action", required=True)
    scaffold_req.add_argument("--prefill-json")
    scaffold_req.add_argument("--prefill-file")
    scaffold_req.add_argument("--approval-scope")
    scaffold_req.add_argument("--artifact-path")
    scaffold_req.add_argument("--output-dir")
    scaffold_req.add_argument("--create-db-request", action="store_true")

    validate_req = sub.add_parser("validate-service-request")
    validate_req.add_argument("--request-id", required=True)

    approve_req = sub.add_parser("approve-service-request")
    approve_req.add_argument("--request-id", required=True)
    approve_req.add_argument("--approved-by", required=True)
    approve_req.add_argument("--exact-scope", required=True)
    approve_req.add_argument("--approval-id")
    approve_req.add_argument("--expires-at")
    approve_req.add_argument("--decision-note")

    reject_req = sub.add_parser("reject-service-request")
    reject_req.add_argument("--request-id", required=True)
    reject_req.add_argument("--rejected-by", required=True)
    reject_req.add_argument("--reason", required=True)
    reject_req.add_argument("--approval-id")

    assign_req = sub.add_parser("assign-service-request")
    assign_req.add_argument("--request-id", required=True)
    assign_req.add_argument("--agent-id", required=True)
    assign_req.add_argument("--decision-note")
    assign_req.add_argument("--force", action="store_true")

    start_req = sub.add_parser("start-service-request")
    start_req.add_argument("--request-id", required=True)
    start_req.add_argument("--agent-id", required=True)
    start_req.add_argument("--artifact-path")
    start_req.add_argument("--decision-note")
    start_req.add_argument("--force", action="store_true")

    complete_req = sub.add_parser("complete-service-request")
    complete_req.add_argument("--request-id", required=True)
    complete_req.add_argument("--agent-id", required=True)
    complete_req.add_argument("--artifact-path")
    complete_req.add_argument("--decision-note")
    complete_req.add_argument("--force", action="store_true")

    update = sub.add_parser("update-task")
    update.add_argument("--task-id", required=True)
    update.add_argument("--status")
    update.add_argument("--next-action")

    acquire = sub.add_parser("acquire-task")
    acquire.add_argument("--task-id", required=True)
    acquire.add_argument("--agent-id", required=True)
    acquire.add_argument("--lease-minutes", type=int, default=120)
    acquire.add_argument("--force", action="store_true")

    release = sub.add_parser("release-task")
    release.add_argument("--task-id", required=True)
    release.add_argument("--agent-id", required=True)
    release.add_argument("--force", action="store_true")

    complete = sub.add_parser("complete-task")
    complete.add_argument("--task-id", required=True)
    complete.add_argument("--agent-id", required=True)
    complete.add_argument("--next-action")
    complete.add_argument("--force", action="store_true")

    artifact = sub.add_parser("record-artifact")
    artifact.add_argument("--artifact-id", required=True)
    artifact.add_argument("--lane-id")
    artifact.add_argument("--task-id")
    artifact.add_argument("--kind", required=True)
    artifact.add_argument("--path-or-url", required=True)
    artifact.add_argument("--sha256")
    artifact.add_argument("--notes")

    outcome = sub.add_parser("record-outcome")
    outcome.add_argument("--outcome-id", required=True)
    outcome.add_argument("--lane-id", required=True)
    outcome.add_argument("--task-id")
    outcome.add_argument("--outcome-type", required=True)
    outcome.add_argument("--status", required=True)
    outcome.add_argument("--realized-usd", type=float, default=0.0)
    outcome.add_argument("--evidence")
    outcome.add_argument("--next-action")


def registry_service_request_command_handlers() -> dict[str, Callable[[Any, Any], None]]:
    return {
        "create-task": create_task,
        "create-service-request": create_service_request,
        "scaffold-service-request": scaffold_service_request,
        "validate-service-request": validate_service_request,
        "approve-service-request": approve_service_request,
        "reject-service-request": reject_service_request,
        "assign-service-request": assign_service_request,
        "start-service-request": start_service_request,
        "complete-service-request": complete_service_request,
        "update-task": update_task,
        "acquire-task": acquire_task,
        "release-task": release_task,
        "complete-task": complete_task,
        "record-artifact": record_artifact,
        "record-outcome": record_outcome,
    }


def handle_registry_service_request_command(conn: Any, args: Any) -> bool:
    if args.cmd not in REGISTRY_SERVICE_REQUEST_COMMANDS:
        return False
    init_db(conn)
    if args.cmd == "register-agent":
        register_agent(conn, args.agent_id, args.role_id, args.thread_id, args.department_id)
        return True
    if args.cmd == "claim-lane":
        claim_lane(conn, args.lane_id, args.agent_id, args.thread_id, args.force)
        return True
    registry_service_request_command_handlers()[args.cmd](conn, args)
    return True


__all__ = [
    "REGISTRY_SERVICE_REQUEST_COMMANDS",
    "add_registry_service_request_commands",
    "handle_registry_service_request_command",
    "registry_service_request_command_handlers",
]