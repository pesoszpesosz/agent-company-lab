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
from agent_company_core.ai_resources_customer_followup_repair_plan import (
    write_ai_resources_customer_followup_repair_plan,
)
from agent_company_core.ai_resources_agent_evolution_repair_packets import (
    write_ai_resources_agent_evolution_repair_packets,
)
from agent_company_core.ai_resources_agent_evolution_repair_evidence import (
    write_ai_resources_agent_evolution_repair_evidence,
)
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
from agent_company_core.goal_evolver_apply_preflight import write_goal_evolver_apply_preflight
from agent_company_core.ceo_restore_cycle import run_ceo_restore_cycle_cli
from agent_company_core.ceo_restore_readiness_audit import write_ceo_restore_readiness_audit_cli
from agent_company_core.ceo_restore_blocker_history import write_ceo_restore_blocker_history_cli
from agent_company_core.ceo_restore_blocker_escalation import write_ceo_restore_blocker_escalation_cli
from agent_company_core.ceo_operator_inbox import write_ceo_operator_inbox_cli
from agent_company_core.ceo_operator_notification import write_ceo_operator_notification_cli
from agent_company_core.ceo_operator_alert_preflight import write_ceo_operator_alert_preflight_cli
from agent_company_core.ceo_gate_pressure_summary import write_ceo_gate_pressure_summary_cli
from agent_company_core.ceo_gate_pressure_history import write_ceo_gate_pressure_history_cli
from agent_company_core.ceo_gate_pressure_escalation import write_ceo_gate_pressure_escalation_cli
from agent_company_core.ceo_restore_continuation_brief import write_ceo_restore_continuation_brief_cli
from agent_company_core.ceo_operator_alert_runner import (
    promote_ceo_operator_alert_approval_draft_cli,
    run_ceo_operator_alert_cli,
    write_ceo_operator_alert_approval_draft_cli,
)
from agent_company_core.ceo_goal_prompt_upgrade_guard import (
    apply_ceo_goal_prompt_upgrade_cli,
    promote_ceo_goal_prompt_upgrade_approval_draft_cli,
    write_ceo_goal_prompt_upgrade_approval_drafts_cli,
)
from agent_company_core.ceo_human_gate_draft_bundle import write_ceo_human_gate_draft_bundle_cli
from agent_company_core.ceo_human_gate_promotion_preflight import write_ceo_human_gate_promotion_preflight_cli
from agent_company_core.ceo_human_gate_surface_audit import write_ceo_human_gate_surface_audit_cli
from agent_company_core.ceo_heartbeat_automation_audit import write_ceo_heartbeat_automation_audit_cli
from agent_company_core.ceo_state_packet import write_ceo_state_packet
from agent_company_core.ceo_worker_bootstrap import write_ceo_worker_bootstrap
from agent_company_core.account_capacity_dispatch_plan import write_account_capacity_dispatch_plan_cli
from agent_company_core.account_capacity_continuity_cycle import run_account_capacity_continuity_cycle_cli
from agent_company_core.account_capacity_lease_reconcile import reconcile_account_capacity_leases_cli
from agent_company_core.account_capacity_refresh_monitor import write_account_capacity_refresh_monitor_cli
from agent_company_core.account_capacity_refresh_signal import (
    apply_account_capacity_refresh_signal_cli,
    promote_account_capacity_refresh_signal_draft_cli,
    write_account_capacity_refresh_signal_drafts_cli,
)
from agent_company_core.codex_thread_goal_inventory import write_codex_thread_goal_inventory_cli
from agent_company_core.runtime_supervisor import write_runtime_supervisor_status_cli
from agent_company_core.lane_runtime_activation_plan import write_lane_runtime_activation_plan_cli
from agent_company_core.lane_runtime_dispatch_drain import write_lane_runtime_dispatch_drain_cli
from agent_company_core.lane_runtime_expired_delivery_reconcile import (
    reconcile_expired_lane_runtime_deliveries_cli,
)
from agent_company_core.lane_runtime_governance_keepalive import write_lane_runtime_governance_keepalive_cli
from agent_company_core.lane_runtime_thread_delivery import (
    apply_lane_runtime_thread_delivery_approval_cli,
    promote_lane_runtime_thread_delivery_approval_draft_cli,
    record_lane_runtime_thread_delivery_cli,
    write_lane_runtime_thread_delivery_approval_drafts_cli,
    write_lane_runtime_thread_delivery_outbox_cli,
    write_lane_runtime_thread_delivery_send_preflight_cli,
)
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
from agent_company_core.continuity_lane_next_task_seed import (
    write_continuity_lane_next_task_seed_cli,
)
from agent_company_core.continuity_lane_next_task_closure import (
    write_continuity_lane_next_task_closure_cli,
)
from agent_company_core.submitted_payout_lane_parking_decision import (
    write_submitted_payout_lane_parking_decision_cli,
)
from agent_company_core.control_plane_capacity_benchmark_runner import write_control_plane_capacity_benchmark_runner
from agent_company_core.premium_customer_followup_escalation import write_premium_customer_followup_escalation
from agent_company_core.premium_customer_followup_monitor import write_premium_customer_followup_monitor
from agent_company_core.premium_customer_followup_synthesizer import write_premium_customer_followup_synthesis
from agent_company_core.premium_customer_intake_router import write_premium_customer_input_route
from agent_company_core.profit_edge_history_ingestion import write_profit_edge_history_ingestion_cli

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
    profit_edge_history_ingestion = sub.add_parser("write-profit-edge-history-ingestion")
    profit_edge_history_ingestion.add_argument("--source-root")
    profit_edge_history_ingestion.add_argument("--now-utc")
    profit_edge_history_ingestion.add_argument("--output-dir")
    profit_edge_history_ingestion.add_argument("--no-db-record", action="store_true")
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
    ai_resources_repair_plan = sub.add_parser("plan-ai-resources-customer-followup-repairs")
    ai_resources_repair_plan.add_argument("--triage-report", required=True)
    ai_resources_repair_plan.add_argument("--now-utc")
    ai_resources_repair_plan.add_argument("--path")
    ai_resources_repair_plan.add_argument("--json-path")
    ai_resources_repair_plan.add_argument("--acknowledgement-path")
    ai_resources_repair_plan.add_argument("--acknowledgement-json-path")
    ai_resources_repair_plan.add_argument("--no-db-record", action="store_true")
    ai_resources_agent_evolution_repair_packets = sub.add_parser("write-ai-resources-agent-evolution-repair-packets")
    ai_resources_agent_evolution_repair_packets.add_argument("--repair-plan", required=True)
    ai_resources_agent_evolution_repair_packets.add_argument("--now-utc")
    ai_resources_agent_evolution_repair_packets.add_argument("--packet-dir")
    ai_resources_agent_evolution_repair_packets.add_argument("--path")
    ai_resources_agent_evolution_repair_packets.add_argument("--json-path")
    ai_resources_agent_evolution_repair_packets.add_argument("--no-db-record", action="store_true")
    ai_resources_agent_evolution_repair_evidence = sub.add_parser("write-ai-resources-agent-evolution-repair-evidence")
    ai_resources_agent_evolution_repair_evidence.add_argument("--packet-report", required=True)
    ai_resources_agent_evolution_repair_evidence.add_argument("--now-utc")
    ai_resources_agent_evolution_repair_evidence.add_argument("--evidence-dir")
    ai_resources_agent_evolution_repair_evidence.add_argument("--path")
    ai_resources_agent_evolution_repair_evidence.add_argument("--json-path")
    ai_resources_agent_evolution_repair_evidence.add_argument("--no-db-record", action="store_true")
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
    goal_evolver_apply_preflight = sub.add_parser("write-goal-evolver-apply-preflight")
    goal_evolver_apply_preflight.add_argument("--draft-path")
    goal_evolver_apply_preflight.add_argument("--now-utc")
    goal_evolver_apply_preflight.add_argument("--path")
    goal_evolver_apply_preflight.add_argument("--json-path")
    goal_evolver_apply_preflight.add_argument("--no-db-record", action="store_true")
    ceo_restore_cycle = sub.add_parser("run-ceo-restore-cycle")
    ceo_restore_cycle.add_argument("--policy-snapshot")
    ceo_restore_cycle.add_argument("--runtime-supervisor-status")
    ceo_restore_cycle.add_argument("--refresh-signal")
    ceo_restore_cycle.add_argument("--refresh-signal-dir", default="state\\account-capacity-refresh-signals")
    ceo_restore_cycle.add_argument("--auto-apply-ready-refresh-signal", action="store_true")
    ceo_restore_cycle.add_argument("--self-observed-codex-capacity-refresh", action="store_true")
    ceo_restore_cycle.add_argument("--self-observed-capacity-session-id")
    ceo_restore_cycle.add_argument("--thread-delivery-approval-signal")
    ceo_restore_cycle.add_argument("--thread-delivery-approval-dir", default="state\\thread-delivery-approvals")
    ceo_restore_cycle.add_argument("--auto-apply-ready-thread-delivery-approval", action="store_true")
    ceo_restore_cycle.add_argument("--auto-wake-local-only-thread-deliveries", action="store_true")
    ceo_restore_cycle.add_argument("--now-utc")
    ceo_restore_cycle.add_argument("--max-lanes", type=int, default=100)
    ceo_restore_cycle.add_argument("--max-dispatches", type=int, default=1)
    ceo_restore_cycle.add_argument("--lease-minutes", type=int, default=120)
    ceo_restore_cycle.add_argument("--executor-agent-id", default="ceo-restore-cycle")
    ceo_restore_cycle.add_argument("--stale-after-minutes", type=int, default=60)
    ceo_restore_cycle.add_argument("--cadence-minutes", type=int, default=15)
    ceo_restore_cycle.add_argument("--open-task-limit", type=int, default=10)
    ceo_restore_cycle.add_argument("--dispatch-limit", type=int, default=10)
    ceo_restore_cycle.add_argument("--drain", action="store_true")
    ceo_restore_cycle.add_argument("--work-dir")
    ceo_restore_cycle.add_argument("--path")
    ceo_restore_cycle.add_argument("--json-path")
    ceo_restore_cycle.add_argument("--lock-dir")
    ceo_restore_cycle.add_argument("--stale-lock-after-seconds", type=int, default=900)
    ceo_restore_cycle.add_argument("--goal-objective-path")
    ceo_restore_cycle.add_argument("--active-goal-path-file")
    ceo_restore_cycle.add_argument("--goal-context-path")
    ceo_restore_cycle.add_argument("--goal-context-path-file")
    ceo_restore_cycle.add_argument("--boot-contract-path")
    ceo_restore_cycle.add_argument("--operator-inbox-path")
    ceo_restore_cycle.add_argument("--operator-inbox-json-path")
    ceo_restore_cycle.add_argument("--operator-inbox-optional-limit", type=int, default=10)
    ceo_restore_cycle.add_argument("--operator-notification-path")
    ceo_restore_cycle.add_argument("--operator-notification-json-path")
    ceo_restore_cycle.add_argument("--operator-notification-repeat-after-minutes", type=int, default=60)
    ceo_restore_cycle.add_argument("--operator-notification-force", action="store_true")
    ceo_restore_cycle.add_argument("--operator-alert-preflight-path")
    ceo_restore_cycle.add_argument("--operator-alert-preflight-json-path")
    ceo_restore_cycle.add_argument("--gate-pressure-summary-path")
    ceo_restore_cycle.add_argument("--gate-pressure-summary-json-path")
    ceo_restore_cycle.add_argument("--gate-pressure-history-path")
    ceo_restore_cycle.add_argument("--gate-pressure-history-json-path")
    ceo_restore_cycle.add_argument("--gate-pressure-escalation-path")
    ceo_restore_cycle.add_argument("--gate-pressure-escalation-json-path")
    ceo_restore_cycle.add_argument("--restore-continuation-brief-path")
    ceo_restore_cycle.add_argument("--restore-continuation-brief-json-path")
    ceo_restore_cycle.add_argument("--restore-blocker-history-path")
    ceo_restore_cycle.add_argument("--restore-blocker-history-json-path")
    ceo_restore_cycle.add_argument("--restore-blocker-escalate-after", type=int, default=3)
    ceo_restore_cycle.add_argument("--restore-blocker-escalation-path")
    ceo_restore_cycle.add_argument("--restore-blocker-escalation-json-path")
    ceo_restore_cycle.add_argument("--heartbeat-automation-path")
    ceo_restore_cycle.add_argument("--heartbeat-automation-audit-path")
    ceo_restore_cycle.add_argument("--heartbeat-automation-audit-json-path")
    ceo_restore_cycle.add_argument("--premium-customer-input-id")
    ceo_restore_cycle.add_argument("--premium-customer-followup-stale-after-minutes", type=int, default=60)
    ceo_restore_cycle.add_argument("--premium-customer-followup-escalation-target", default="ai_resources_lab")
    ceo_restore_cycle.add_argument("--ai-resources-owner-ack-stale-after-minutes", type=int, default=60)
    ceo_restore_cycle.add_argument("--premium-customer-ledger-json")
    ceo_restore_cycle.add_argument("--premium-customer-ledger-md")
    ceo_restore_cycle.add_argument("--premium-customer-update-feed-json")
    ceo_restore_cycle.add_argument("--premium-customer-update-feed-md")
    ceo_restore_cycle.add_argument("--no-db-record", action="store_true")
    ceo_restore_readiness_audit = sub.add_parser("write-ceo-restore-readiness-audit")
    ceo_restore_readiness_audit.add_argument("--restore-cycle")
    ceo_restore_readiness_audit.add_argument("--now-utc")
    ceo_restore_readiness_audit.add_argument("--path")
    ceo_restore_readiness_audit.add_argument("--json-path")
    ceo_restore_readiness_audit.add_argument("--allow-active-lock", action="store_true")
    ceo_restore_readiness_audit.add_argument("--no-db-record", action="store_true")
    ceo_restore_blocker_history = sub.add_parser("write-ceo-restore-blocker-history")
    ceo_restore_blocker_history.add_argument("--restore-cycle")
    ceo_restore_blocker_history.add_argument("--now-utc")
    ceo_restore_blocker_history.add_argument("--path")
    ceo_restore_blocker_history.add_argument("--json-path")
    ceo_restore_blocker_history.add_argument("--escalate-after", type=int, default=3)
    ceo_restore_blocker_history.add_argument("--no-db-record", action="store_true")
    ceo_restore_blocker_escalation = sub.add_parser("write-ceo-restore-blocker-escalation")
    ceo_restore_blocker_escalation.add_argument("--blocker-history")
    ceo_restore_blocker_escalation.add_argument("--operator-inbox")
    ceo_restore_blocker_escalation.add_argument("--now-utc")
    ceo_restore_blocker_escalation.add_argument("--path")
    ceo_restore_blocker_escalation.add_argument("--json-path")
    ceo_restore_blocker_escalation.add_argument("--no-db-record", action="store_true")
    ceo_operator_inbox = sub.add_parser("write-ceo-operator-inbox")
    ceo_operator_inbox.add_argument("--restore-cycle", required=True)
    ceo_operator_inbox.add_argument("--now-utc")
    ceo_operator_inbox.add_argument("--path")
    ceo_operator_inbox.add_argument("--json-path")
    ceo_operator_inbox.add_argument("--optional-overflow-path")
    ceo_operator_inbox.add_argument("--optional-overflow-json-path")
    ceo_operator_inbox.add_argument("--goal-prompt-upgrade-review-path")
    ceo_operator_inbox.add_argument("--goal-prompt-upgrade-review-json-path")
    ceo_operator_inbox.add_argument("--optional-limit", type=int, default=10)
    ceo_operator_inbox.add_argument("--no-db-record", action="store_true")
    ceo_operator_notification = sub.add_parser("write-ceo-operator-notification")
    ceo_operator_notification.add_argument("--operator-inbox")
    ceo_operator_notification.add_argument("--blocker-escalation")
    ceo_operator_notification.add_argument("--gate-pressure-summary")
    ceo_operator_notification.add_argument("--gate-pressure-history")
    ceo_operator_notification.add_argument("--now-utc")
    ceo_operator_notification.add_argument("--path")
    ceo_operator_notification.add_argument("--json-path")
    ceo_operator_notification.add_argument("--repeat-after-minutes", type=int, default=60)
    ceo_operator_notification.add_argument("--force", action="store_true")
    ceo_operator_notification.add_argument("--no-db-record", action="store_true")
    ceo_operator_alert_preflight = sub.add_parser("write-ceo-operator-alert-preflight")
    ceo_operator_alert_preflight.add_argument("--operator-notification")
    ceo_operator_alert_preflight.add_argument("--gate-pressure-escalation")
    ceo_operator_alert_preflight.add_argument("--now-utc")
    ceo_operator_alert_preflight.add_argument("--path")
    ceo_operator_alert_preflight.add_argument("--json-path")
    ceo_operator_alert_preflight.add_argument("--no-db-record", action="store_true")
    gate_pressure_summary = sub.add_parser("write-ceo-gate-pressure-summary")
    gate_pressure_summary.add_argument("--restore-cycle")
    gate_pressure_summary.add_argument("--operator-inbox")
    gate_pressure_summary.add_argument("--operator-notification")
    gate_pressure_summary.add_argument("--operator-alert-preflight")
    gate_pressure_summary.add_argument("--now-utc")
    gate_pressure_summary.add_argument("--path")
    gate_pressure_summary.add_argument("--json-path")
    gate_pressure_summary.add_argument("--daily-report-paths", action="store_true")
    gate_pressure_summary.add_argument("--no-db-record", action="store_true")
    gate_pressure_history = sub.add_parser("write-ceo-gate-pressure-history")
    gate_pressure_history.add_argument("--gate-pressure")
    gate_pressure_history.add_argument("--now-utc")
    gate_pressure_history.add_argument("--path")
    gate_pressure_history.add_argument("--json-path")
    gate_pressure_history.add_argument("--max-observations", type=int, default=50)
    gate_pressure_history.add_argument("--persistent-after", type=int, default=3)
    gate_pressure_history.add_argument("--no-db-record", action="store_true")
    gate_pressure_escalation = sub.add_parser("write-ceo-gate-pressure-escalation")
    gate_pressure_escalation.add_argument("--gate-pressure-history")
    gate_pressure_escalation.add_argument("--operator-notification")
    gate_pressure_escalation.add_argument("--now-utc")
    gate_pressure_escalation.add_argument("--path")
    gate_pressure_escalation.add_argument("--json-path")
    gate_pressure_escalation.add_argument("--no-db-record", action="store_true")
    restore_continuation_brief = sub.add_parser("write-ceo-restore-continuation-brief")
    restore_continuation_brief.add_argument("--restore-cycle")
    restore_continuation_brief.add_argument("--now-utc")
    restore_continuation_brief.add_argument("--path")
    restore_continuation_brief.add_argument("--json-path")
    restore_continuation_brief.add_argument("--no-db-record", action="store_true")
    ceo_operator_alert_approval_draft = sub.add_parser("write-ceo-operator-alert-approval-draft")
    ceo_operator_alert_approval_draft.add_argument("--alert-preflight")
    ceo_operator_alert_approval_draft.add_argument("--draft-dir")
    ceo_operator_alert_approval_draft.add_argument("--now-utc")
    ceo_operator_alert_approval_draft.add_argument("--path")
    ceo_operator_alert_approval_draft.add_argument("--json-path")
    ceo_operator_alert_approval_draft.add_argument("--no-db-record", action="store_true")
    ceo_operator_alert_approval_promotion = sub.add_parser("promote-ceo-operator-alert-approval-draft")
    ceo_operator_alert_approval_promotion.add_argument("--draft-path", required=True)
    ceo_operator_alert_approval_promotion.add_argument("--active-signal-dir")
    ceo_operator_alert_approval_promotion.add_argument("--confirm-reviewed", action="store_true")
    ceo_operator_alert_approval_promotion.add_argument("--now-utc")
    ceo_operator_alert_approval_promotion.add_argument("--path")
    ceo_operator_alert_approval_promotion.add_argument("--json-path")
    ceo_operator_alert_approval_promotion.add_argument("--no-db-record", action="store_true")
    ceo_operator_alert = sub.add_parser("run-ceo-operator-alert")
    ceo_operator_alert.add_argument("--alert-preflight")
    ceo_operator_alert.add_argument("--approval-signal", required=True)
    ceo_operator_alert.add_argument("--confirm-reviewed", action="store_true")
    ceo_operator_alert.add_argument("--execute-window", action="store_true")
    ceo_operator_alert.add_argument("--now-utc")
    ceo_operator_alert.add_argument("--path")
    ceo_operator_alert.add_argument("--json-path")
    ceo_operator_alert.add_argument("--no-db-record", action="store_true")
    ceo_goal_prompt_upgrade_approval_draft = sub.add_parser("write-ceo-goal-prompt-upgrade-approval-draft")
    ceo_goal_prompt_upgrade_approval_draft.add_argument("--review-packet")
    ceo_goal_prompt_upgrade_approval_draft.add_argument("--active-signal-dir")
    ceo_goal_prompt_upgrade_approval_draft.add_argument("--draft-dir")
    ceo_goal_prompt_upgrade_approval_draft.add_argument("--now-utc")
    ceo_goal_prompt_upgrade_approval_draft.add_argument("--path")
    ceo_goal_prompt_upgrade_approval_draft.add_argument("--json-path")
    ceo_goal_prompt_upgrade_approval_draft.add_argument("--no-db-record", action="store_true")
    ceo_goal_prompt_upgrade_approval_promotion = sub.add_parser("promote-ceo-goal-prompt-upgrade-approval-draft")
    ceo_goal_prompt_upgrade_approval_promotion.add_argument("--draft-path", required=True)
    ceo_goal_prompt_upgrade_approval_promotion.add_argument("--active-signal-dir")
    ceo_goal_prompt_upgrade_approval_promotion.add_argument("--confirm-reviewed", action="store_true")
    ceo_goal_prompt_upgrade_approval_promotion.add_argument("--now-utc")
    ceo_goal_prompt_upgrade_approval_promotion.add_argument("--path")
    ceo_goal_prompt_upgrade_approval_promotion.add_argument("--json-path")
    ceo_goal_prompt_upgrade_approval_promotion.add_argument("--no-db-record", action="store_true")
    ceo_goal_prompt_upgrade_apply = sub.add_parser("apply-ceo-goal-prompt-upgrade")
    ceo_goal_prompt_upgrade_apply.add_argument("--review-packet")
    ceo_goal_prompt_upgrade_apply.add_argument("--approval-signal", required=True)
    ceo_goal_prompt_upgrade_apply.add_argument("--confirm-reviewed", action="store_true")
    ceo_goal_prompt_upgrade_apply.add_argument("--apply-goal-edit", action="store_true")
    ceo_goal_prompt_upgrade_apply.add_argument("--backup-dir")
    ceo_goal_prompt_upgrade_apply.add_argument("--now-utc")
    ceo_goal_prompt_upgrade_apply.add_argument("--path")
    ceo_goal_prompt_upgrade_apply.add_argument("--json-path")
    ceo_goal_prompt_upgrade_apply.add_argument("--no-db-record", action="store_true")
    ceo_human_gate_draft_bundle = sub.add_parser("write-ceo-human-gate-draft-bundle")
    ceo_human_gate_draft_bundle.add_argument("--restore-cycle")
    ceo_human_gate_draft_bundle.add_argument("--now-utc")
    ceo_human_gate_draft_bundle.add_argument("--path")
    ceo_human_gate_draft_bundle.add_argument("--json-path")
    ceo_human_gate_draft_bundle.add_argument("--no-db-record", action="store_true")
    ceo_human_gate_promotion_preflight = sub.add_parser("write-ceo-human-gate-promotion-preflight")
    ceo_human_gate_promotion_preflight.add_argument("--operator-inbox")
    ceo_human_gate_promotion_preflight.add_argument("--operator-alert-preflight")
    ceo_human_gate_promotion_preflight.add_argument("--now-utc")
    ceo_human_gate_promotion_preflight.add_argument("--path")
    ceo_human_gate_promotion_preflight.add_argument("--json-path")
    ceo_human_gate_promotion_preflight.add_argument("--no-db-record", action="store_true")
    ceo_human_gate_surface_audit = sub.add_parser("write-ceo-human-gate-surface-audit")
    ceo_human_gate_surface_audit.add_argument("--restore-cycle")
    ceo_human_gate_surface_audit.add_argument("--now-utc")
    ceo_human_gate_surface_audit.add_argument("--path")
    ceo_human_gate_surface_audit.add_argument("--json-path")
    ceo_human_gate_surface_audit.add_argument("--no-db-record", action="store_true")
    ceo_heartbeat_automation_audit = sub.add_parser("write-ceo-heartbeat-automation-audit")
    ceo_heartbeat_automation_audit.add_argument("--automation-path")
    ceo_heartbeat_automation_audit.add_argument("--boot-contract-path")
    ceo_heartbeat_automation_audit.add_argument("--now-utc")
    ceo_heartbeat_automation_audit.add_argument("--path")
    ceo_heartbeat_automation_audit.add_argument("--json-path")
    ceo_heartbeat_automation_audit.add_argument("--no-db-record", action="store_true")
    ceo_state_packet = sub.add_parser("write-ceo-state-packet")
    ceo_state_packet.add_argument("--now-utc")
    ceo_state_packet.add_argument("--path")
    ceo_state_packet.add_argument("--json-path")
    ceo_state_packet.add_argument("--human-action-path")
    ceo_state_packet.add_argument("--human-action-json-path")
    ceo_state_packet.add_argument("--capacity-refresh-monitor")
    ceo_state_packet.add_argument("--thread-delivery-outbox")
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
    account_capacity_dispatch = sub.add_parser("write-account-capacity-dispatch-plan")
    account_capacity_dispatch.add_argument("--capacity-snapshot", required=True)
    account_capacity_dispatch.add_argument("--now-utc")
    account_capacity_dispatch.add_argument("--max-tasks", type=int, default=10)
    account_capacity_dispatch.add_argument("--path")
    account_capacity_dispatch.add_argument("--json-path")
    account_capacity_dispatch.add_argument("--no-db-record", action="store_true")
    account_capacity_reconcile = sub.add_parser("reconcile-account-capacity-leases")
    account_capacity_reconcile.add_argument("--now-utc")
    account_capacity_reconcile.add_argument("--path")
    account_capacity_reconcile.add_argument("--json-path")
    account_capacity_reconcile.add_argument("--no-db-record", action="store_true")
    expired_delivery_reconcile = sub.add_parser("reconcile-expired-lane-runtime-deliveries")
    expired_delivery_reconcile.add_argument("--now-utc")
    expired_delivery_reconcile.add_argument("--path")
    expired_delivery_reconcile.add_argument("--json-path")
    expired_delivery_reconcile.add_argument("--no-db-record", action="store_true")
    account_capacity_refresh = sub.add_parser("apply-account-capacity-refresh-signal")
    account_capacity_refresh.add_argument("--signal-path", required=True)
    account_capacity_refresh.add_argument("--now-utc")
    account_capacity_refresh.add_argument("--path")
    account_capacity_refresh.add_argument("--json-path")
    account_capacity_refresh.add_argument("--no-db-record", action="store_true")
    account_capacity_refresh_drafts = sub.add_parser("write-account-capacity-refresh-signal-drafts")
    account_capacity_refresh_drafts.add_argument("--capacity-refresh-monitor", required=True)
    account_capacity_refresh_drafts.add_argument("--now-utc")
    account_capacity_refresh_drafts.add_argument("--max-signals", type=int, default=10)
    account_capacity_refresh_drafts.add_argument("--draft-dir")
    account_capacity_refresh_drafts.add_argument("--path")
    account_capacity_refresh_drafts.add_argument("--json-path")
    account_capacity_refresh_drafts.add_argument("--no-db-record", action="store_true")
    account_capacity_refresh_promotion = sub.add_parser("promote-account-capacity-refresh-signal-draft")
    account_capacity_refresh_promotion.add_argument("--draft-path", required=True)
    account_capacity_refresh_promotion.add_argument("--active-signal-dir")
    account_capacity_refresh_promotion.add_argument("--confirm-reviewed", action="store_true")
    account_capacity_refresh_promotion.add_argument("--now-utc")
    account_capacity_refresh_promotion.add_argument("--path")
    account_capacity_refresh_promotion.add_argument("--json-path")
    account_capacity_refresh_promotion.add_argument("--no-db-record", action="store_true")
    account_capacity_refresh_monitor = sub.add_parser("write-account-capacity-refresh-monitor")
    account_capacity_refresh_monitor.add_argument("--continuity-cycle", required=True)
    account_capacity_refresh_monitor.add_argument("--refresh-signal-dir")
    account_capacity_refresh_monitor.add_argument("--now-utc")
    account_capacity_refresh_monitor.add_argument("--path")
    account_capacity_refresh_monitor.add_argument("--json-path")
    account_capacity_refresh_monitor.add_argument("--no-db-record", action="store_true")
    account_capacity_continuity_cycle = sub.add_parser("run-account-capacity-continuity-cycle")
    account_capacity_continuity_cycle.add_argument("--policy-snapshot", required=True)
    account_capacity_continuity_cycle.add_argument("--runtime-supervisor-status")
    account_capacity_continuity_cycle.add_argument("--refresh-signal")
    account_capacity_continuity_cycle.add_argument("--refresh-signal-dir")
    account_capacity_continuity_cycle.add_argument("--auto-apply-ready-refresh-signal", action="store_true")
    account_capacity_continuity_cycle.add_argument("--self-observed-codex-capacity-refresh", action="store_true")
    account_capacity_continuity_cycle.add_argument("--self-observed-capacity-session-id")
    account_capacity_continuity_cycle.add_argument("--thread-delivery-approval-signal")
    account_capacity_continuity_cycle.add_argument("--thread-delivery-approval-dir")
    account_capacity_continuity_cycle.add_argument("--auto-apply-ready-thread-delivery-approval", action="store_true")
    account_capacity_continuity_cycle.add_argument("--auto-wake-local-only-thread-deliveries", action="store_true")
    account_capacity_continuity_cycle.add_argument("--now-utc")
    account_capacity_continuity_cycle.add_argument("--max-lanes", type=int, default=100)
    account_capacity_continuity_cycle.add_argument("--max-dispatches", type=int, default=1)
    account_capacity_continuity_cycle.add_argument("--lease-minutes", type=int, default=120)
    account_capacity_continuity_cycle.add_argument("--executor-agent-id", default="account-capacity-continuity-cycle")
    account_capacity_continuity_cycle.add_argument("--stale-after-minutes", type=int, default=60)
    account_capacity_continuity_cycle.add_argument("--cadence-minutes", type=int, default=15)
    account_capacity_continuity_cycle.add_argument("--open-task-limit", type=int, default=10)
    account_capacity_continuity_cycle.add_argument("--dispatch-limit", type=int, default=10)
    account_capacity_continuity_cycle.add_argument("--drain", action="store_true")
    account_capacity_continuity_cycle.add_argument("--work-dir")
    account_capacity_continuity_cycle.add_argument("--path")
    account_capacity_continuity_cycle.add_argument("--json-path")
    account_capacity_continuity_cycle.add_argument("--no-db-record", action="store_true")
    lane_runtime_activation = sub.add_parser("write-lane-runtime-activation-plan")
    lane_runtime_activation.add_argument("--policy-snapshot", required=True)
    lane_runtime_activation.add_argument("--runtime-supervisor-status")
    lane_runtime_activation.add_argument("--now-utc")
    lane_runtime_activation.add_argument("--max-lanes", type=int, default=100)
    lane_runtime_activation.add_argument("--path")
    lane_runtime_activation.add_argument("--json-path")
    lane_runtime_activation.add_argument("--no-db-record", action="store_true")
    lane_runtime_dispatch_drain = sub.add_parser("drain-lane-runtime-dispatch")
    lane_runtime_dispatch_drain.add_argument("--activation-plan", required=True)
    lane_runtime_dispatch_drain.add_argument("--now-utc")
    lane_runtime_dispatch_drain.add_argument("--lease-minutes", type=int, default=120)
    lane_runtime_dispatch_drain.add_argument("--executor-agent-id", default="lane-runtime-dispatch-drain-executor")
    lane_runtime_dispatch_drain.add_argument("--max-dispatches", type=int, default=10)
    lane_runtime_dispatch_drain.add_argument("--packet-dir")
    lane_runtime_dispatch_drain.add_argument("--path")
    lane_runtime_dispatch_drain.add_argument("--json-path")
    lane_runtime_dispatch_drain.add_argument("--dry-run", action="store_true")
    lane_runtime_dispatch_drain.add_argument("--no-db-record", action="store_true")
    lane_runtime_governance_keepalive = sub.add_parser("write-lane-runtime-governance-keepalive")
    lane_runtime_governance_keepalive.add_argument("--now-utc")
    lane_runtime_governance_keepalive.add_argument("--max-keepalives", type=int, default=2)
    lane_runtime_governance_keepalive.add_argument("--lease-minutes", type=int, default=30)
    lane_runtime_governance_keepalive.add_argument("--packet-dir")
    lane_runtime_governance_keepalive.add_argument("--path")
    lane_runtime_governance_keepalive.add_argument("--json-path")
    lane_runtime_governance_keepalive.add_argument("--no-db-record", action="store_true")
    lane_runtime_thread_delivery = sub.add_parser("write-lane-runtime-thread-delivery-outbox")
    lane_runtime_thread_delivery.add_argument("--drain-report", required=True)
    lane_runtime_thread_delivery.add_argument("--now-utc")
    lane_runtime_thread_delivery.add_argument("--outbox-dir")
    lane_runtime_thread_delivery.add_argument("--path")
    lane_runtime_thread_delivery.add_argument("--json-path")
    lane_runtime_thread_delivery.add_argument("--no-db-record", action="store_true")
    lane_runtime_thread_delivery_receipt = sub.add_parser("record-lane-runtime-thread-delivery")
    lane_runtime_thread_delivery_receipt.add_argument("--delivery-id", required=True)
    lane_runtime_thread_delivery_receipt.add_argument("--status", choices=["delivered", "send_failed"], required=True)
    lane_runtime_thread_delivery_receipt.add_argument("--now-utc")
    lane_runtime_thread_delivery_receipt.add_argument("--error")
    lane_runtime_thread_delivery_approval = sub.add_parser("apply-lane-runtime-thread-delivery-approval")
    lane_runtime_thread_delivery_approval.add_argument("--approval-signal", required=True)
    lane_runtime_thread_delivery_approval.add_argument("--now-utc")
    lane_runtime_thread_delivery_approval.add_argument("--path")
    lane_runtime_thread_delivery_approval.add_argument("--json-path")
    lane_runtime_thread_delivery_approval.add_argument("--no-db-record", action="store_true")
    lane_runtime_thread_delivery_approval_drafts = sub.add_parser("write-lane-runtime-thread-delivery-approval-drafts")
    lane_runtime_thread_delivery_approval_drafts.add_argument("--now-utc")
    lane_runtime_thread_delivery_approval_drafts.add_argument("--max-deliveries", type=int, default=10)
    lane_runtime_thread_delivery_approval_drafts.add_argument("--operator", default="matth")
    lane_runtime_thread_delivery_approval_drafts.add_argument("--draft-dir")
    lane_runtime_thread_delivery_approval_drafts.add_argument("--path")
    lane_runtime_thread_delivery_approval_drafts.add_argument("--json-path")
    lane_runtime_thread_delivery_approval_drafts.add_argument("--no-db-record", action="store_true")
    lane_runtime_thread_delivery_approval_promotion = sub.add_parser(
        "promote-lane-runtime-thread-delivery-approval-draft"
    )
    lane_runtime_thread_delivery_approval_promotion.add_argument("--draft-path", required=True)
    lane_runtime_thread_delivery_approval_promotion.add_argument("--active-signal-dir")
    lane_runtime_thread_delivery_approval_promotion.add_argument("--confirm-reviewed", action="store_true")
    lane_runtime_thread_delivery_approval_promotion.add_argument("--now-utc")
    lane_runtime_thread_delivery_approval_promotion.add_argument("--path")
    lane_runtime_thread_delivery_approval_promotion.add_argument("--json-path")
    lane_runtime_thread_delivery_approval_promotion.add_argument("--no-db-record", action="store_true")
    lane_runtime_thread_delivery_send_preflight = sub.add_parser("write-lane-runtime-thread-delivery-send-preflight")
    lane_runtime_thread_delivery_send_preflight.add_argument("--now-utc")
    lane_runtime_thread_delivery_send_preflight.add_argument("--max-deliveries", type=int, default=10)
    lane_runtime_thread_delivery_send_preflight.add_argument("--include-safe-ready-deliveries", action="store_true")
    lane_runtime_thread_delivery_send_preflight.add_argument("--auto-authorize-approved-deliveries", action="store_true")
    lane_runtime_thread_delivery_send_preflight.add_argument("--path")
    lane_runtime_thread_delivery_send_preflight.add_argument("--json-path")
    lane_runtime_thread_delivery_send_preflight.add_argument("--no-db-record", action="store_true")
    codex_thread_goal_inventory = sub.add_parser("write-codex-thread-goal-inventory")
    codex_thread_goal_inventory.add_argument("--thread-snapshot", required=True)
    codex_thread_goal_inventory.add_argument("--now-utc")
    codex_thread_goal_inventory.add_argument("--path")
    codex_thread_goal_inventory.add_argument("--json-path")
    codex_thread_goal_inventory.add_argument("--no-db-record", action="store_true")
    runtime_supervisor = sub.add_parser("write-runtime-supervisor-status")
    runtime_supervisor.add_argument("--thread-snapshot", required=True)
    runtime_supervisor.add_argument("--now-utc")
    runtime_supervisor.add_argument("--path")
    runtime_supervisor.add_argument("--json-path")
    runtime_supervisor.add_argument("--human-action-path")
    runtime_supervisor.add_argument("--human-action-json-path")
    runtime_supervisor.add_argument("--lane-limit", type=int, default=100)
    runtime_supervisor.add_argument("--open-task-limit", type=int, default=250)
    runtime_supervisor.add_argument("--no-db-record", action="store_true")
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
    continuity_lane_next_task_seed = sub.add_parser("write-continuity-lane-next-task-seed")
    continuity_lane_next_task_seed.add_argument("--now-utc")
    continuity_lane_next_task_seed.add_argument("--path")
    continuity_lane_next_task_seed.add_argument("--json-path")
    continuity_lane_next_task_seed.add_argument("--manager-packet-dir")
    continuity_lane_next_task_seed.add_argument("--no-db-record", action="store_true")
    continuity_lane_next_task_closure = sub.add_parser("write-continuity-lane-next-task-closure")
    continuity_lane_next_task_closure.add_argument("--now-utc")
    continuity_lane_next_task_closure.add_argument("--path")
    continuity_lane_next_task_closure.add_argument("--json-path")
    continuity_lane_next_task_closure.add_argument("--proof-root")
    continuity_lane_next_task_closure.add_argument("--no-db-record", action="store_true")
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
        elif args.cmd == "write-profit-edge-history-ingestion":
            init_db(conn)
            write_profit_edge_history_ingestion_cli(conn, args)
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
        elif args.cmd == "plan-ai-resources-customer-followup-repairs":
            init_db(conn)
            write_ai_resources_customer_followup_repair_plan(conn, args)
        elif args.cmd == "write-ai-resources-agent-evolution-repair-packets":
            init_db(conn)
            write_ai_resources_agent_evolution_repair_packets(conn, args)
        elif args.cmd == "write-ai-resources-agent-evolution-repair-evidence":
            init_db(conn)
            write_ai_resources_agent_evolution_repair_evidence(conn, args)
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
        elif args.cmd == "write-goal-evolver-apply-preflight":
            init_db(conn)
            write_goal_evolver_apply_preflight(conn, args)
        elif args.cmd == "run-ceo-restore-cycle":
            init_db(conn)
            run_ceo_restore_cycle_cli(conn, args)
        elif args.cmd == "write-ceo-restore-readiness-audit":
            init_db(conn)
            write_ceo_restore_readiness_audit_cli(conn, args)
        elif args.cmd == "write-ceo-restore-blocker-history":
            init_db(conn)
            write_ceo_restore_blocker_history_cli(conn, args)
        elif args.cmd == "write-ceo-restore-blocker-escalation":
            init_db(conn)
            write_ceo_restore_blocker_escalation_cli(conn, args)
        elif args.cmd == "write-ceo-operator-inbox":
            init_db(conn)
            write_ceo_operator_inbox_cli(conn, args)
        elif args.cmd == "write-ceo-operator-notification":
            init_db(conn)
            write_ceo_operator_notification_cli(conn, args)
        elif args.cmd == "write-ceo-operator-alert-preflight":
            init_db(conn)
            write_ceo_operator_alert_preflight_cli(conn, args)
        elif args.cmd == "write-ceo-gate-pressure-summary":
            init_db(conn)
            write_ceo_gate_pressure_summary_cli(conn, args)
        elif args.cmd == "write-ceo-gate-pressure-history":
            init_db(conn)
            write_ceo_gate_pressure_history_cli(conn, args)
        elif args.cmd == "write-ceo-gate-pressure-escalation":
            init_db(conn)
            write_ceo_gate_pressure_escalation_cli(conn, args)
        elif args.cmd == "write-ceo-restore-continuation-brief":
            init_db(conn)
            write_ceo_restore_continuation_brief_cli(conn, args)
        elif args.cmd == "write-ceo-operator-alert-approval-draft":
            init_db(conn)
            write_ceo_operator_alert_approval_draft_cli(conn, args)
        elif args.cmd == "promote-ceo-operator-alert-approval-draft":
            init_db(conn)
            promote_ceo_operator_alert_approval_draft_cli(conn, args)
        elif args.cmd == "run-ceo-operator-alert":
            init_db(conn)
            run_ceo_operator_alert_cli(conn, args)
        elif args.cmd == "write-ceo-goal-prompt-upgrade-approval-draft":
            init_db(conn)
            write_ceo_goal_prompt_upgrade_approval_drafts_cli(conn, args)
        elif args.cmd == "promote-ceo-goal-prompt-upgrade-approval-draft":
            init_db(conn)
            promote_ceo_goal_prompt_upgrade_approval_draft_cli(conn, args)
        elif args.cmd == "apply-ceo-goal-prompt-upgrade":
            init_db(conn)
            apply_ceo_goal_prompt_upgrade_cli(conn, args)
        elif args.cmd == "write-ceo-human-gate-draft-bundle":
            init_db(conn)
            write_ceo_human_gate_draft_bundle_cli(conn, args)
        elif args.cmd == "write-ceo-human-gate-promotion-preflight":
            init_db(conn)
            write_ceo_human_gate_promotion_preflight_cli(conn, args)
        elif args.cmd == "write-ceo-human-gate-surface-audit":
            init_db(conn)
            write_ceo_human_gate_surface_audit_cli(conn, args)
        elif args.cmd == "write-ceo-heartbeat-automation-audit":
            init_db(conn)
            write_ceo_heartbeat_automation_audit_cli(conn, args)
        elif args.cmd == "write-ceo-state-packet":
            init_db(conn)
            write_ceo_state_packet(conn, args)
        elif args.cmd == "bootstrap-ceo-workers":
            init_db(conn)
            write_ceo_worker_bootstrap(conn, args)
        elif args.cmd == "write-account-capacity-dispatch-plan":
            init_db(conn)
            write_account_capacity_dispatch_plan_cli(conn, args)
        elif args.cmd == "reconcile-account-capacity-leases":
            init_db(conn)
            reconcile_account_capacity_leases_cli(conn, args)
        elif args.cmd == "reconcile-expired-lane-runtime-deliveries":
            init_db(conn)
            reconcile_expired_lane_runtime_deliveries_cli(conn, args)
        elif args.cmd == "apply-account-capacity-refresh-signal":
            init_db(conn)
            apply_account_capacity_refresh_signal_cli(conn, args)
        elif args.cmd == "write-account-capacity-refresh-signal-drafts":
            init_db(conn)
            write_account_capacity_refresh_signal_drafts_cli(conn, args)
        elif args.cmd == "promote-account-capacity-refresh-signal-draft":
            init_db(conn)
            promote_account_capacity_refresh_signal_draft_cli(conn, args)
        elif args.cmd == "write-account-capacity-refresh-monitor":
            init_db(conn)
            write_account_capacity_refresh_monitor_cli(conn, args)
        elif args.cmd == "run-account-capacity-continuity-cycle":
            init_db(conn)
            run_account_capacity_continuity_cycle_cli(conn, args)
        elif args.cmd == "write-lane-runtime-activation-plan":
            init_db(conn)
            write_lane_runtime_activation_plan_cli(conn, args)
        elif args.cmd == "drain-lane-runtime-dispatch":
            init_db(conn)
            write_lane_runtime_dispatch_drain_cli(conn, args)
        elif args.cmd == "write-lane-runtime-governance-keepalive":
            init_db(conn)
            write_lane_runtime_governance_keepalive_cli(conn, args)
        elif args.cmd == "write-lane-runtime-thread-delivery-outbox":
            init_db(conn)
            write_lane_runtime_thread_delivery_outbox_cli(conn, args)
        elif args.cmd == "record-lane-runtime-thread-delivery":
            init_db(conn)
            record_lane_runtime_thread_delivery_cli(conn, args)
        elif args.cmd == "apply-lane-runtime-thread-delivery-approval":
            init_db(conn)
            apply_lane_runtime_thread_delivery_approval_cli(conn, args)
        elif args.cmd == "write-lane-runtime-thread-delivery-approval-drafts":
            init_db(conn)
            write_lane_runtime_thread_delivery_approval_drafts_cli(conn, args)
        elif args.cmd == "promote-lane-runtime-thread-delivery-approval-draft":
            init_db(conn)
            promote_lane_runtime_thread_delivery_approval_draft_cli(conn, args)
        elif args.cmd == "write-lane-runtime-thread-delivery-send-preflight":
            init_db(conn)
            write_lane_runtime_thread_delivery_send_preflight_cli(conn, args)
        elif args.cmd == "write-codex-thread-goal-inventory":
            init_db(conn)
            write_codex_thread_goal_inventory_cli(conn, args)
        elif args.cmd == "write-runtime-supervisor-status":
            init_db(conn)
            write_runtime_supervisor_status_cli(conn, args)
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
        elif args.cmd == "write-continuity-lane-next-task-seed":
            init_db(conn)
            write_continuity_lane_next_task_seed_cli(conn, args)
        elif args.cmd == "write-continuity-lane-next-task-closure":
            init_db(conn)
            write_continuity_lane_next_task_closure_cli(conn, args)
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
