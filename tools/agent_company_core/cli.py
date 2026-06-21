from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from datetime import timedelta
from pathlib import Path
from typing import Any

from agent_company_core.catalog import (
    department_id,
    list_evidence,
    list_service_catalog,
    list_source_specs,
    seed,
    seed_service_catalog,
    seed_source_specs,
    upsert_source_spec,
    write_service_catalog_report,
)
from agent_company_core.control_reports import (
    lane_recommendation,
    list_status,
    suggested_manager_task,
    write_ceo_review,
    write_company_expansion_gap_map,
    write_dashboard,
)
from agent_company_core.ai_resources_customer_followup_triage import write_ai_resources_customer_followup_triage
from agent_company_core.ai_resources_owner_acknowledgement_requests import (
    write_ai_resources_owner_acknowledgement_requests,
)
from agent_company_core.ai_resources_owner_acknowledgement_monitor import (
    write_ai_resources_owner_acknowledgement_monitor,
)
from agent_company_core.ai_resources_owner_acknowledgement_dispatch import (
    write_ai_resources_owner_acknowledgement_dispatch,
)
from agent_company_core.ai_resources_owner_acknowledgement_closure import (
    write_ai_resources_owner_acknowledgement_closure,
)
from agent_company_core.goal_evolver_review import write_goal_evolver_review
from agent_company_core.ceo_state_packet import write_ceo_state_packet
from agent_company_core.ceo_worker_bootstrap import write_ceo_worker_bootstrap
from agent_company_core.continuity_watchdog_snapshot import write_continuity_watchdog_snapshot
from agent_company_core.continuity_watchdog_restore_plan import write_continuity_watchdog_restore_plan
from agent_company_core.continuity_watchdog_restore_response_bundle import (
    write_continuity_watchdog_restore_response_bundle_cli,
)
from agent_company_core.continuity_watchdog_owner_response_artifacts import (
    write_continuity_watchdog_owner_response_artifacts_cli,
)
from agent_company_core.continuity_watchdog_owner_response_task_dispatch import (
    write_continuity_watchdog_owner_response_task_dispatch_cli,
)
from agent_company_core.continuity_watchdog_owner_handoff_packets import (
    write_continuity_watchdog_owner_handoff_packets_cli,
)
from agent_company_core.submitted_payout_lane_parking_decision import (
    write_submitted_payout_lane_parking_decision_cli,
)
from agent_company_core.control_plane_capacity_benchmark_runner import write_control_plane_capacity_benchmark_runner
from agent_company_core.premium_customer_followup_escalation import write_premium_customer_followup_escalation
from agent_company_core.premium_customer_followup_monitor import write_premium_customer_followup_monitor
from agent_company_core.premium_customer_followup_synthesizer import write_premium_customer_followup_synthesis
from agent_company_core.premium_customer_intake_router import write_premium_customer_input_route

from agent_company_core.database import connect
from agent_company_core.cli_durable_adapters import add_durable_adapter_commands, handle_durable_adapter_command
from agent_company_core.cli_prompt_eval import add_prompt_eval_commands, handle_prompt_eval_command
from agent_company_core.cli_registry_service_requests import add_registry_service_request_commands, handle_registry_service_request_command
from agent_company_core.cli_service_workers import add_service_worker_commands, handle_service_worker_command
from agent_company_core.cli_digital_products import add_digital_products_commands, handle_digital_products_command
from agent_company_core.cli_ceo_decisions import add_ceo_decision_commands, handle_ceo_decision_command
from agent_company_core.cli_agent_company_migration import add_agent_company_migration_commands, handle_agent_company_migration_command
from agent_company_core.cli_money_paths import add_money_path_commands, handle_money_path_command
from agent_company_core.cli_paid_code import add_paid_code_commands, handle_paid_code_command


from agent_company_core.io import load_json, now_utc, parse_utc
from agent_company_core.launch_packets import (
    write_lane_thread_manifest,
    write_launch_packets,
    write_manager_packets,
)


from agent_company_core.profit_edge_import import import_profit_edge

from agent_company_core.schema import init_db
from agent_company_core.registry import record_trace_event
from agent_company_core.reports import (
    list_artifacts,
    list_trace_events,
    write_artifacts_report,
    write_trace_report,
)
from agent_company_core.service_requests import write_service_request_review
from agent_company_core.source_specs import (
    proposed_source_spec_seed,
    write_source_spec_seed_apply,
    write_source_spec_seed_packets,
    write_source_specs_report,
)

from agent_company_core.constants import *  # Transitional compatibility while CLI modules are split.
from agent_company_core.utils import (
    compact_text,
    decode_json_list,
    md_cell,
    parse_json_arg,
    parse_metadata_arg,
    read_text_arg,
    safe_id_fragment,
    sha256_file,
    sha256_text,
)
from agent_company_core.paths import (
    DB_PATH,
    LANE_TAXONOMY_PATH,
    LAUNCH_DIR,
    MANAGER_PACKET_DIR,
    PROFIT_EDGE_ROOT,
    REPORTS_DIR,
    ROLE_REGISTRY_PATH,
    ROOT,
    SERVICE_CATALOG_PATH,
    SOURCE_SPECS_PATH,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agent-company Phase 0 control plane")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init")
    sub.add_parser("seed")
    sub.add_parser("status")
    dashboard = sub.add_parser("write-dashboard")
    dashboard.add_argument("--path")
    ceo_review = sub.add_parser("write-ceo-review")
    ceo_review.add_argument("--path")
    company_gap_map = sub.add_parser("write-company-expansion-gap-map")
    company_gap_map.add_argument("--path")
    company_gap_map.add_argument("--json-path")
    company_gap_map.add_argument("--validation-path")
    capacity_benchmark = sub.add_parser("run-control-plane-capacity-benchmark")
    capacity_benchmark.add_argument("--row-counts")
    capacity_benchmark.add_argument("--run-id")
    capacity_benchmark.add_argument("--work-dir")
    capacity_benchmark.add_argument("--path")
    capacity_benchmark.add_argument("--json-path")
    capacity_benchmark.add_argument("--overwrite", action="store_true")
    premium_customer_route = sub.add_parser("route-premium-customer-input")
    premium_customer_route.add_argument("--input-path")
    premium_customer_route.add_argument("--text")
    premium_customer_route.add_argument("--text-file")
    premium_customer_route.add_argument("--input-id")
    premium_customer_route.add_argument("--title")
    premium_customer_route.add_argument("--owner-agent-id")
    premium_customer_route.add_argument("--dropbox-dir")
    premium_customer_route.add_argument("--routes-dir")
    premium_customer_route.add_argument("--ledger-json")
    premium_customer_route.add_argument("--ledger-md")
    premium_customer_route.add_argument("--update-feed-json")
    premium_customer_route.add_argument("--update-feed-md")
    premium_customer_route.add_argument("--overwrite", action="store_true")
    premium_customer_route.add_argument("--no-db-record", action="store_true")
    premium_customer_followups = sub.add_parser("synthesize-premium-customer-followups")
    premium_customer_followups.add_argument("--route-packet", required=True)
    premium_customer_followups.add_argument("--output-dir")
    premium_customer_followups.add_argument("--ledger-json")
    premium_customer_followups.add_argument("--ledger-md")
    premium_customer_followups.add_argument("--update-feed-json")
    premium_customer_followups.add_argument("--update-feed-md")
    premium_customer_followups.add_argument("--no-db-record", action="store_true")
    premium_customer_monitor = sub.add_parser("monitor-premium-customer-followups")
    premium_customer_monitor.add_argument("--input-id")
    premium_customer_monitor.add_argument("--stale-after-minutes", type=int, default=60)
    premium_customer_monitor.add_argument("--now-utc")
    premium_customer_monitor.add_argument("--path")
    premium_customer_monitor.add_argument("--json-path")
    premium_customer_monitor.add_argument("--ledger-json")
    premium_customer_monitor.add_argument("--ledger-md")
    premium_customer_monitor.add_argument("--update-feed-json")
    premium_customer_monitor.add_argument("--update-feed-md")
    premium_customer_monitor.add_argument("--no-db-record", action="store_true")
    premium_customer_escalation = sub.add_parser("escalate-premium-customer-followups")
    premium_customer_escalation.add_argument("--monitor-report", required=True)
    premium_customer_escalation.add_argument("--target-surface", default="ai_resources_lab")
    premium_customer_escalation.add_argument("--now-utc")
    premium_customer_escalation.add_argument("--path")
    premium_customer_escalation.add_argument("--json-path")
    premium_customer_escalation.add_argument("--ledger-json")
    premium_customer_escalation.add_argument("--ledger-md")
    premium_customer_escalation.add_argument("--update-feed-json")
    premium_customer_escalation.add_argument("--update-feed-md")
    premium_customer_escalation.add_argument("--no-db-record", action="store_true")
    ai_resources_triage = sub.add_parser("triage-ai-resources-customer-followups")
    ai_resources_triage.add_argument("--escalation-report", required=True)
    ai_resources_triage.add_argument("--now-utc")
    ai_resources_triage.add_argument("--path")
    ai_resources_triage.add_argument("--json-path")
    ai_resources_triage.add_argument("--no-db-record", action="store_true")
    ai_resources_ack = sub.add_parser("request-ai-resources-owner-acknowledgements")
    ai_resources_ack.add_argument("--triage-report", required=True)
    ai_resources_ack.add_argument("--now-utc")
    ai_resources_ack.add_argument("--path")
    ai_resources_ack.add_argument("--json-path")
    ai_resources_ack.add_argument("--no-db-record", action="store_true")
    ai_resources_ack_monitor = sub.add_parser("monitor-ai-resources-owner-acknowledgements")
    ai_resources_ack_monitor.add_argument("--input-id")
    ai_resources_ack_monitor.add_argument("--stale-after-minutes", type=int, default=60)
    ai_resources_ack_monitor.add_argument("--now-utc")
    ai_resources_ack_monitor.add_argument("--path")
    ai_resources_ack_monitor.add_argument("--json-path")
    ai_resources_ack_monitor.add_argument("--no-db-record", action="store_true")
    ai_resources_ack_dispatch = sub.add_parser("write-ai-resources-owner-acknowledgement-dispatch")
    ai_resources_ack_dispatch.add_argument("--input-id")
    ai_resources_ack_dispatch.add_argument("--stale-after-minutes", type=int, default=60)
    ai_resources_ack_dispatch.add_argument("--now-utc")
    ai_resources_ack_dispatch.add_argument("--path")
    ai_resources_ack_dispatch.add_argument("--json-path")
    ai_resources_ack_dispatch.add_argument("--no-db-record", action="store_true")
    ai_resources_ack_closure = sub.add_parser("write-ai-resources-owner-acknowledgement-closure")
    ai_resources_ack_closure.add_argument("--input-id")
    ai_resources_ack_closure.add_argument("--now-utc")
    ai_resources_ack_closure.add_argument("--path")
    ai_resources_ack_closure.add_argument("--json-path")
    ai_resources_ack_closure.add_argument("--no-db-record", action="store_true")
    goal_evolver_review = sub.add_parser("write-goal-evolver-review")
    goal_evolver_review.add_argument("--now-utc")
    goal_evolver_review.add_argument("--path")
    goal_evolver_review.add_argument("--json-path")
    goal_evolver_review.add_argument("--goal-md-path")
    goal_evolver_review.add_argument("--goal-json-path")
    goal_evolver_review.add_argument("--agent-charter-path")
    goal_evolver_review.add_argument("--evidence-limit", type=int, default=10)
    goal_evolver_review.add_argument("--no-db-record", action="store_true")
    ceo_state_packet = sub.add_parser("write-ceo-state-packet")
    ceo_state_packet.add_argument("--now-utc")
    ceo_state_packet.add_argument("--path")
    ceo_state_packet.add_argument("--json-path")
    ceo_state_packet.add_argument("--human-action-path")
    ceo_state_packet.add_argument("--human-action-json-path")
    ceo_state_packet.add_argument("--open-task-limit", type=int, default=10)
    ceo_state_packet.add_argument("--dispatch-limit", type=int, default=10)
    ceo_state_packet.add_argument("--no-db-record", action="store_true")
    ceo_worker_bootstrap = sub.add_parser("bootstrap-ceo-workers")
    ceo_worker_bootstrap.add_argument("--now-utc")
    ceo_worker_bootstrap.add_argument("--path")
    ceo_worker_bootstrap.add_argument("--json-path")
    ceo_worker_bootstrap.add_argument("--ar-thread-id")
    ceo_worker_bootstrap.add_argument("--overlap-thread-id")
    ceo_worker_bootstrap.add_argument("--candidate-thread-id")
    ceo_worker_bootstrap.add_argument("--evaluation-thread-id")
    ceo_worker_bootstrap.add_argument("--retirement-thread-id")
    ceo_worker_bootstrap.add_argument("--continuity-thread-id")
    ceo_worker_bootstrap.add_argument("--premium-router-thread-id")
    ceo_worker_bootstrap.add_argument("--browser-ops-thread-id")
    ceo_worker_bootstrap.add_argument("--no-db-record", action="store_true")
    continuity_watchdog_snapshot = sub.add_parser("write-continuity-watchdog-snapshot")
    continuity_watchdog_snapshot.add_argument("--now-utc")
    continuity_watchdog_snapshot.add_argument("--stale-after-minutes", type=int, default=60)
    continuity_watchdog_snapshot.add_argument("--cadence-minutes", type=int, default=15)
    continuity_watchdog_snapshot.add_argument("--path")
    continuity_watchdog_snapshot.add_argument("--json-path")
    continuity_watchdog_snapshot.add_argument("--no-db-record", action="store_true")
    continuity_watchdog_restore_plan = sub.add_parser("write-continuity-watchdog-restore-plan")
    continuity_watchdog_restore_plan.add_argument("--snapshot-report")
    continuity_watchdog_restore_plan.add_argument("--now-utc")
    continuity_watchdog_restore_plan.add_argument("--path")
    continuity_watchdog_restore_plan.add_argument("--json-path")
    continuity_watchdog_restore_plan.add_argument("--packet-dir")
    continuity_watchdog_restore_plan.add_argument("--no-db-record", action="store_true")
    continuity_watchdog_restore_response_bundle = sub.add_parser("write-continuity-watchdog-restore-response-bundle")
    continuity_watchdog_restore_response_bundle.add_argument("--restore-plan")
    continuity_watchdog_restore_response_bundle.add_argument("--now-utc")
    continuity_watchdog_restore_response_bundle.add_argument("--path")
    continuity_watchdog_restore_response_bundle.add_argument("--json-path")
    continuity_watchdog_restore_response_bundle.add_argument("--response-dir")
    continuity_watchdog_restore_response_bundle.add_argument("--no-db-record", action="store_true")
    continuity_watchdog_owner_response_artifacts = sub.add_parser("write-continuity-watchdog-owner-response-artifacts")
    continuity_watchdog_owner_response_artifacts.add_argument("--response-bundle")
    continuity_watchdog_owner_response_artifacts.add_argument("--now-utc")
    continuity_watchdog_owner_response_artifacts.add_argument("--path")
    continuity_watchdog_owner_response_artifacts.add_argument("--json-path")
    continuity_watchdog_owner_response_artifacts.add_argument("--artifact-dir")
    continuity_watchdog_owner_response_artifacts.add_argument("--no-db-record", action="store_true")
    continuity_watchdog_owner_response_task_dispatch = sub.add_parser(
        "write-continuity-watchdog-owner-response-task-dispatch"
    )
    continuity_watchdog_owner_response_task_dispatch.add_argument("--owner-response-artifacts")
    continuity_watchdog_owner_response_task_dispatch.add_argument("--now-utc")
    continuity_watchdog_owner_response_task_dispatch.add_argument("--path")
    continuity_watchdog_owner_response_task_dispatch.add_argument("--json-path")
    continuity_watchdog_owner_response_task_dispatch.add_argument("--no-db-record", action="store_true")
    continuity_watchdog_owner_handoff_packets = sub.add_parser("write-continuity-watchdog-owner-handoff-packets")
    continuity_watchdog_owner_handoff_packets.add_argument("--now-utc")
    continuity_watchdog_owner_handoff_packets.add_argument("--path")
    continuity_watchdog_owner_handoff_packets.add_argument("--json-path")
    continuity_watchdog_owner_handoff_packets.add_argument("--packet-dir")
    continuity_watchdog_owner_handoff_packets.add_argument("--no-db-record", action="store_true")
    submitted_payout_parking = sub.add_parser("write-submitted-payout-lane-parking-decision")
    submitted_payout_parking.add_argument("--now-utc")
    submitted_payout_parking.add_argument("--path")
    submitted_payout_parking.add_argument("--json-path")
    submitted_payout_parking.add_argument("--no-db-record", action="store_true")
    add_money_path_commands(sub)
    add_paid_code_commands(sub)
    add_digital_products_commands(sub)
    add_ceo_decision_commands(sub)
    add_agent_company_migration_commands(sub)
    source_specs_report = sub.add_parser("write-source-specs-report")
    source_specs_report.add_argument("--path")
    source_spec_seed_packets = sub.add_parser("write-source-spec-seed-packets")
    source_spec_seed_packets.add_argument("--path")
    source_spec_seed_packets.add_argument("--json-path")
    source_spec_seed_packets.add_argument("--validation-path")
    source_spec_seed_packets.add_argument("--packet-dir")
    source_spec_seed_packets.add_argument("--gap-map-path")
    source_spec_seed_apply = sub.add_parser("write-source-spec-seed-apply")
    source_spec_seed_apply.add_argument("--path")
    source_spec_seed_apply.add_argument("--json-path")
    source_spec_seed_apply.add_argument("--validation-path")
    source_spec_seed_apply.add_argument("--seed-packets-path")
    service_catalog_report = sub.add_parser("write-service-catalog-report")
    service_catalog_report.add_argument("--path")
    service_catalog_report.add_argument("--service-id")
    service_catalog_report.add_argument("--request-type")
    service_catalog_report.add_argument("--owner-role-id")
    service_catalog_report.add_argument("--status")
    service_catalog_report.add_argument("--limit", type=int, default=100)
    service_request_review = sub.add_parser("write-service-request-review")
    service_request_review.add_argument("--path")
    service_request_review.add_argument("--json-path")
    service_request_review.add_argument("--request-id")
    service_request_review.add_argument("--lane-id")
    service_request_review.add_argument("--service-id")
    service_request_review.add_argument("--request-type")
    service_request_review.add_argument("--status")
    service_request_review.add_argument("--limit", type=int, default=100)
    add_service_worker_commands(sub)
    sub.add_parser("write-launch-packets")
    manager_packets = sub.add_parser("write-manager-packets")
    manager_packets.add_argument("--dir")
    lane_thread_manifest = sub.add_parser("write-lane-thread-manifest")
    lane_thread_manifest.add_argument("--md-path")
    lane_thread_manifest.add_argument("--json-path")
    sub.add_parser("seed-source-specs")
    sub.add_parser("seed-service-catalog")

    import_pe = sub.add_parser("import-profit-edge")
    import_pe.add_argument("--source-root", default=str(PROFIT_EDGE_ROOT))
    import_pe.add_argument("--task-id", default="task-profit-edge-import-bridge-20260614")
    import_pe.add_argument("--ledger-tail", type=int, default=40)

    evidence = sub.add_parser("list-evidence")
    evidence.add_argument("--lane-id")
    evidence.add_argument("--limit", type=int, default=50)

    source_specs = sub.add_parser("list-source-specs")
    source_specs.add_argument("--lane-id")
    source_specs.add_argument("--limit", type=int, default=50)

    service_catalog = sub.add_parser("list-service-catalog")
    service_catalog.add_argument("--service-id")
    service_catalog.add_argument("--request-type")
    service_catalog.add_argument("--owner-role-id")
    service_catalog.add_argument("--status")
    service_catalog.add_argument("--limit", type=int, default=50)

    artifact_list = sub.add_parser("list-artifacts")
    artifact_list.add_argument("--artifact-id")
    artifact_list.add_argument("--lane-id")
    artifact_list.add_argument("--task-id")
    artifact_list.add_argument("--kind")
    artifact_list.add_argument("--contains")
    artifact_list.add_argument("--limit", type=int, default=50)

    artifact_report = sub.add_parser("write-artifacts-report")
    artifact_report.add_argument("--path")
    artifact_report.add_argument("--artifact-id")
    artifact_report.add_argument("--lane-id")
    artifact_report.add_argument("--task-id")
    artifact_report.add_argument("--kind")
    artifact_report.add_argument("--contains")
    artifact_report.add_argument("--limit", type=int, default=100)

    trace_event = sub.add_parser("record-trace-event")
    trace_event.add_argument("--event-id")
    trace_event.add_argument("--trace-id", required=True)
    trace_event.add_argument("--lane-id")
    trace_event.add_argument("--task-id")
    trace_event.add_argument("--agent-id")
    trace_event.add_argument("--event-type", required=True)
    trace_event.add_argument("--event-time")
    trace_event.add_argument("--source")
    trace_event.add_argument("--summary", required=True)
    trace_event.add_argument("--metadata-json")
    trace_event.add_argument("--metadata-file")
    trace_event.add_argument("--artifact-path")

    trace_list = sub.add_parser("list-trace-events")
    trace_list.add_argument("--trace-id")
    trace_list.add_argument("--lane-id")
    trace_list.add_argument("--task-id")
    trace_list.add_argument("--agent-id")
    trace_list.add_argument("--event-type")
    trace_list.add_argument("--limit", type=int, default=50)

    trace_report = sub.add_parser("write-trace-report")
    trace_report.add_argument("--path")
    trace_report.add_argument("--trace-id")
    trace_report.add_argument("--lane-id")
    trace_report.add_argument("--task-id")
    trace_report.add_argument("--agent-id")
    trace_report.add_argument("--event-type")
    trace_report.add_argument("--limit", type=int, default=100)

    add_durable_adapter_commands(sub)

    add_prompt_eval_commands(sub)

    add_registry_service_request_commands(sub)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    with connect() as conn:
        if args.cmd == "init":
            init_db(conn)
            print(json.dumps({"ok": True, "db": str(DB_PATH)}, indent=2))
        elif args.cmd == "seed":
            seed(conn)
            print(json.dumps({"ok": True, "db": str(DB_PATH)}, indent=2))
        elif handle_registry_service_request_command(conn, args):
            pass
        elif args.cmd == "status":
            init_db(conn)
            list_status(conn)
        elif args.cmd == "write-dashboard":
            init_db(conn)
            write_dashboard(conn, args.path)
        elif args.cmd == "write-ceo-review":
            init_db(conn)
            write_ceo_review(conn, args.path)
        elif args.cmd == "write-company-expansion-gap-map":
            init_db(conn)
            write_company_expansion_gap_map(conn, args)
        elif args.cmd == "run-control-plane-capacity-benchmark":
            init_db(conn)
            write_control_plane_capacity_benchmark_runner(conn, args)
        elif args.cmd == "route-premium-customer-input":
            init_db(conn)
            write_premium_customer_input_route(conn, args)
        elif args.cmd == "synthesize-premium-customer-followups":
            init_db(conn)
            write_premium_customer_followup_synthesis(conn, args)
        elif args.cmd == "monitor-premium-customer-followups":
            init_db(conn)
            write_premium_customer_followup_monitor(conn, args)
        elif args.cmd == "escalate-premium-customer-followups":
            init_db(conn)
            write_premium_customer_followup_escalation(conn, args)
        elif args.cmd == "triage-ai-resources-customer-followups":
            init_db(conn)
            write_ai_resources_customer_followup_triage(conn, args)
        elif args.cmd == "request-ai-resources-owner-acknowledgements":
            init_db(conn)
            write_ai_resources_owner_acknowledgement_requests(conn, args)
        elif args.cmd == "monitor-ai-resources-owner-acknowledgements":
            init_db(conn)
            write_ai_resources_owner_acknowledgement_monitor(conn, args)
        elif args.cmd == "write-ai-resources-owner-acknowledgement-dispatch":
            init_db(conn)
            write_ai_resources_owner_acknowledgement_dispatch(conn, args)
        elif args.cmd == "write-ai-resources-owner-acknowledgement-closure":
            init_db(conn)
            write_ai_resources_owner_acknowledgement_closure(conn, args)
        elif args.cmd == "write-goal-evolver-review":
            init_db(conn)
            write_goal_evolver_review(conn, args)
        elif args.cmd == "write-ceo-state-packet":
            init_db(conn)
            write_ceo_state_packet(conn, args)
        elif args.cmd == "bootstrap-ceo-workers":
            init_db(conn)
            write_ceo_worker_bootstrap(conn, args)
        elif args.cmd == "write-continuity-watchdog-snapshot":
            init_db(conn)
            write_continuity_watchdog_snapshot(conn, args)
        elif args.cmd == "write-continuity-watchdog-restore-plan":
            init_db(conn)
            write_continuity_watchdog_restore_plan(conn, args)
        elif args.cmd == "write-continuity-watchdog-restore-response-bundle":
            init_db(conn)
            write_continuity_watchdog_restore_response_bundle_cli(conn, args)
        elif args.cmd == "write-continuity-watchdog-owner-response-artifacts":
            init_db(conn)
            write_continuity_watchdog_owner_response_artifacts_cli(conn, args)
        elif args.cmd == "write-continuity-watchdog-owner-response-task-dispatch":
            init_db(conn)
            write_continuity_watchdog_owner_response_task_dispatch_cli(conn, args)
        elif args.cmd == "write-continuity-watchdog-owner-handoff-packets":
            init_db(conn)
            write_continuity_watchdog_owner_handoff_packets_cli(conn, args)
        elif args.cmd == "write-submitted-payout-lane-parking-decision":
            init_db(conn)
            write_submitted_payout_lane_parking_decision_cli(conn, args)
        elif handle_money_path_command(conn, args):
            pass
        elif handle_paid_code_command(conn, args):
            pass
        elif handle_digital_products_command(conn, args):
            pass
        elif handle_ceo_decision_command(conn, args):
            pass
        elif handle_agent_company_migration_command(conn, args):
            pass
        elif args.cmd == "write-source-specs-report":
            init_db(conn)
            write_source_specs_report(conn, args.path)
        elif args.cmd == "write-source-spec-seed-packets":
            init_db(conn)
            write_source_spec_seed_packets(conn, args)
        elif args.cmd == "write-source-spec-seed-apply":
            init_db(conn)
            write_source_spec_seed_apply(conn, args)
        elif args.cmd == "write-service-catalog-report":
            init_db(conn)
            write_service_catalog_report(conn, args)
        elif args.cmd == "write-service-request-review":
            init_db(conn)
            write_service_request_review(conn, args)
        elif handle_service_worker_command(conn, args):
            pass
        elif args.cmd == "write-launch-packets":
            init_db(conn)
            write_launch_packets(conn)
        elif args.cmd == "write-manager-packets":
            init_db(conn)
            write_manager_packets(conn, args.dir)
        elif args.cmd == "write-lane-thread-manifest":
            init_db(conn)
            write_lane_thread_manifest(conn, args.md_path, args.json_path)
        elif args.cmd == "seed-source-specs":
            init_db(conn)
            seed_source_specs(conn)
            conn.commit()
            print(json.dumps({"ok": True, "path": str(SOURCE_SPECS_PATH)}, indent=2))
        elif args.cmd == "seed-service-catalog":
            init_db(conn)
            seed_service_catalog(conn)
            conn.commit()
            print(json.dumps({"ok": True, "path": str(SERVICE_CATALOG_PATH)}, indent=2))
        elif args.cmd == "import-profit-edge":
            import_profit_edge(conn, args)
        elif args.cmd == "list-evidence":
            init_db(conn)
            list_evidence(conn, args)
        elif args.cmd == "list-source-specs":
            init_db(conn)
            list_source_specs(conn, args)
        elif args.cmd == "list-service-catalog":
            init_db(conn)
            list_service_catalog(conn, args)
        elif args.cmd == "list-artifacts":
            init_db(conn)
            list_artifacts(conn, args)
        elif args.cmd == "write-artifacts-report":
            init_db(conn)
            write_artifacts_report(conn, args)
        elif args.cmd == "record-trace-event":
            init_db(conn)
            record_trace_event(conn, args)
        elif args.cmd == "list-trace-events":
            init_db(conn)
            list_trace_events(conn, args)
        elif args.cmd == "write-trace-report":
            init_db(conn)
            write_trace_report(conn, args)
        elif handle_durable_adapter_command(conn, args):
            pass
        elif handle_prompt_eval_command(conn, args):
            pass
