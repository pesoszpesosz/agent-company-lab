from __future__ import annotations

from typing import Any, Callable

"""CLI parser and dispatch helpers for durable adapter commands."""

from agent_company_core.durable_adapters import (
    dry_run_durable_service_request_reducer,
    write_durable_adapter_runtime_human_approval_packet,
    write_durable_adapter_runtime_human_decision_intake_packet,
    write_durable_adapter_runtime_implementation_preflight,
    write_durable_adapter_runtime_interface_contract,
    write_durable_adapter_runtime_negative_fixtures,
    write_durable_adapter_runtime_report_only_fixtures,
    write_durable_adapter_runtime_report_only_scaffolding_artifacts,
    write_durable_adapter_runtime_report_only_scaffolding_packet,
    write_durable_adapter_service_worker_integration,
)
from agent_company_core.schema import init_db


DURABLE_ADAPTER_COMMANDS = (
    "dry-run-durable-service-request-reducer",
    "write-durable-adapter-service-worker-integration",
    "write-durable-adapter-runtime-interface-contract",
    "write-durable-adapter-runtime-negative-fixtures",
    "write-durable-adapter-runtime-implementation-preflight",
    "write-durable-adapter-runtime-report-only-fixtures",
    "write-durable-adapter-runtime-report-only-scaffolding-packet",
    "write-durable-adapter-runtime-report-only-scaffolding-artifacts",
    "write-durable-adapter-runtime-human-approval-packet",
    "write-durable-adapter-runtime-human-decision-intake-packet",
)


def add_durable_adapter_commands(sub: Any) -> None:
    durable_dry_run = sub.add_parser("dry-run-durable-service-request-reducer")
    durable_dry_run.add_argument("--fixtures", required=True)
    durable_dry_run.add_argument("--result-path")
    durable_dry_run.add_argument("--json", action="store_true")
    durable_dry_run.add_argument("--check-live-status", action="store_true")
    durable_integration = sub.add_parser("write-durable-adapter-service-worker-integration")
    durable_integration.add_argument("--path")
    durable_integration.add_argument("--json-path")
    durable_integration.add_argument("--validation-path")
    durable_integration.add_argument("--reducer-result-path")
    durable_interface = sub.add_parser("write-durable-adapter-runtime-interface-contract")
    durable_interface.add_argument("--path")
    durable_interface.add_argument("--json-path")
    durable_interface.add_argument("--validation-path")
    durable_interface.add_argument("--reducer-result-path")
    durable_interface.add_argument("--integration-validation-path")
    durable_interface.add_argument("--readiness-validation-path")
    durable_negative = sub.add_parser("write-durable-adapter-runtime-negative-fixtures")
    durable_negative.add_argument("--path")
    durable_negative.add_argument("--json-path")
    durable_negative.add_argument("--validation-path")
    durable_negative.add_argument("--contract-validation-path")
    durable_preflight = sub.add_parser("write-durable-adapter-runtime-implementation-preflight")
    durable_preflight.add_argument("--path")
    durable_preflight.add_argument("--json-path")
    durable_preflight.add_argument("--validation-path")
    durable_preflight.add_argument("--contract-validation-path")
    durable_preflight.add_argument("--negative-validation-path")
    durable_preflight.add_argument("--readiness-validation-path")
    durable_preflight.add_argument("--integration-validation-path")
    durable_report_only = sub.add_parser("write-durable-adapter-runtime-report-only-fixtures")
    durable_report_only.add_argument("--path")
    durable_report_only.add_argument("--json-path")
    durable_report_only.add_argument("--validation-path")
    durable_report_only.add_argument("--preflight-validation-path")
    durable_scaffolding_packet = sub.add_parser("write-durable-adapter-runtime-report-only-scaffolding-packet")
    durable_scaffolding_packet.add_argument("--path")
    durable_scaffolding_packet.add_argument("--json-path")
    durable_scaffolding_packet.add_argument("--validation-path")
    durable_scaffolding_packet.add_argument("--fixtures-path")
    durable_scaffolding_packet.add_argument("--fixtures-validation-path")
    durable_scaffolding_packet.add_argument("--preflight-validation-path")
    durable_scaffolding_artifacts = sub.add_parser("write-durable-adapter-runtime-report-only-scaffolding-artifacts")
    durable_scaffolding_artifacts.add_argument("--path")
    durable_scaffolding_artifacts.add_argument("--json-path")
    durable_scaffolding_artifacts.add_argument("--validation-path")
    durable_scaffolding_artifacts.add_argument("--artifact-dir")
    durable_scaffolding_artifacts.add_argument("--packet-path")
    durable_scaffolding_artifacts.add_argument("--packet-validation-path")
    durable_scaffolding_artifacts.add_argument("--chain-validation-path")
    durable_approval_packet = sub.add_parser("write-durable-adapter-runtime-human-approval-packet")
    durable_approval_packet.add_argument("--path")
    durable_approval_packet.add_argument("--json-path")
    durable_approval_packet.add_argument("--validation-path")
    durable_approval_packet.add_argument("--scaffolding-artifacts-path")
    durable_approval_packet.add_argument("--scaffolding-artifacts-validation-path")
    durable_decision_intake = sub.add_parser("write-durable-adapter-runtime-human-decision-intake-packet")
    durable_decision_intake.add_argument("--path")
    durable_decision_intake.add_argument("--json-path")
    durable_decision_intake.add_argument("--validation-path")
    durable_decision_intake.add_argument("--approval-packet-path")
    durable_decision_intake.add_argument("--approval-validation-path")


def durable_adapter_command_handlers() -> dict[str, Callable[[Any, Any], None]]:
    return {
        "dry-run-durable-service-request-reducer": dry_run_durable_service_request_reducer,
        "write-durable-adapter-service-worker-integration": write_durable_adapter_service_worker_integration,
        "write-durable-adapter-runtime-interface-contract": write_durable_adapter_runtime_interface_contract,
        "write-durable-adapter-runtime-negative-fixtures": write_durable_adapter_runtime_negative_fixtures,
        "write-durable-adapter-runtime-implementation-preflight": write_durable_adapter_runtime_implementation_preflight,
        "write-durable-adapter-runtime-report-only-fixtures": write_durable_adapter_runtime_report_only_fixtures,
        "write-durable-adapter-runtime-report-only-scaffolding-packet": write_durable_adapter_runtime_report_only_scaffolding_packet,
        "write-durable-adapter-runtime-report-only-scaffolding-artifacts": write_durable_adapter_runtime_report_only_scaffolding_artifacts,
        "write-durable-adapter-runtime-human-approval-packet": write_durable_adapter_runtime_human_approval_packet,
        "write-durable-adapter-runtime-human-decision-intake-packet": write_durable_adapter_runtime_human_decision_intake_packet,
    }


def handle_durable_adapter_command(conn: Any, args: Any) -> bool:
    handler = durable_adapter_command_handlers().get(args.cmd)
    if handler is None:
        return False
    init_db(conn)
    handler(conn, args)
    return True


__all__ = [
    "DURABLE_ADAPTER_COMMANDS",
    "add_durable_adapter_commands",
    "durable_adapter_command_handlers",
    "handle_durable_adapter_command",
]