from __future__ import annotations

from typing import Any, Callable

"""CLI parser and dispatch helpers for money-path commands."""

from agent_company_core.money_paths import (
    write_first_local_evidence_packets,
    write_first_ranked_manager_proof,
    write_manager_proof_task_packets,
    write_manager_proof_task_promotion_preflight,
    write_manager_proof_task_promotion_queue,
    write_money_path_coverage_audit,
)
from agent_company_core.schema import init_db


MONEY_PATH_CLI_COMMANDS = (
    "write-agent-company-money-path-coverage-audit",
    "write-first-local-evidence-packets",
    "write-manager-proof-task-packets",
    "write-manager-proof-task-promotion-preflight",
    "write-manager-proof-task-promotion-queue",
    "write-first-ranked-manager-proof",
)


def add_money_path_commands(sub: Any) -> None:
    money_path_coverage_audit = sub.add_parser("write-agent-company-money-path-coverage-audit")
    money_path_coverage_audit.add_argument("--path")
    money_path_coverage_audit.add_argument("--json-path")
    money_path_coverage_audit.add_argument("--validation-path")
    first_local_evidence = sub.add_parser("write-first-local-evidence-packets")
    first_local_evidence.add_argument("--path")
    first_local_evidence.add_argument("--json-path")
    first_local_evidence.add_argument("--validation-path")
    first_local_evidence.add_argument("--packet-dir")
    manager_proof_task_packets = sub.add_parser("write-manager-proof-task-packets")
    manager_proof_task_packets.add_argument("--path")
    manager_proof_task_packets.add_argument("--json-path")
    manager_proof_task_packets.add_argument("--validation-path")
    manager_proof_task_packets.add_argument("--packet-dir")
    manager_proof_task_preflight = sub.add_parser("write-manager-proof-task-promotion-preflight")
    manager_proof_task_preflight.add_argument("--path")
    manager_proof_task_preflight.add_argument("--json-path")
    manager_proof_task_preflight.add_argument("--validation-path")
    manager_proof_task_preflight.add_argument("--packets-path")
    manager_proof_task_queue = sub.add_parser("write-manager-proof-task-promotion-queue")
    manager_proof_task_queue.add_argument("--path")
    manager_proof_task_queue.add_argument("--json-path")
    manager_proof_task_queue.add_argument("--validation-path")
    manager_proof_task_queue.add_argument("--preflight-path")
    first_ranked_manager_proof = sub.add_parser("write-first-ranked-manager-proof")
    first_ranked_manager_proof.add_argument("--path")
    first_ranked_manager_proof.add_argument("--json-path")
    first_ranked_manager_proof.add_argument("--validation-path")
    first_ranked_manager_proof.add_argument("--queue-path")


def money_path_command_handlers() -> dict[str, Callable[[Any, Any], None]]:
    return {
        "write-agent-company-money-path-coverage-audit": write_money_path_coverage_audit,
        "write-first-local-evidence-packets": write_first_local_evidence_packets,
        "write-manager-proof-task-packets": write_manager_proof_task_packets,
        "write-manager-proof-task-promotion-preflight": write_manager_proof_task_promotion_preflight,
        "write-manager-proof-task-promotion-queue": write_manager_proof_task_promotion_queue,
        "write-first-ranked-manager-proof": write_first_ranked_manager_proof,
    }


def handle_money_path_command(conn: Any, args: Any) -> bool:
    handler = money_path_command_handlers().get(args.cmd)
    if handler is None:
        return False
    init_db(conn)
    handler(conn, args)
    return True


__all__ = [
    "MONEY_PATH_CLI_COMMANDS",
    "add_money_path_commands",
    "money_path_command_handlers",
    "handle_money_path_command",
]