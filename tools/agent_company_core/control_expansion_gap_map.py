from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .constants import (
    CEO_REVIEW_REPORT,
    COMPANY_EXPANSION_GAP_MAP_JSON,
    COMPANY_EXPANSION_GAP_MAP_REPORT,
    COMPANY_EXPANSION_GAP_MAP_VALIDATION_JSON,
)
from .io import now_utc
from .paths import DB_PATH, REPORTS_DIR
from .service_workers import db_scalar
from .utils import md_cell

def suggested_manager_task(lane_id: str) -> str:
    tasks = {
        "platform_engineering": "Use manager packets to launch separate lane-manager chats; keep real model/API execution behind the pending service request.",
        "security_bounty_private_reports": "Rank imported private-report and static-review sources by program scope, evidence quality, payout path, and disclosure route.",
        "prediction_market_research": "Create a paper-only replay task for one imported market edge and define the data source of truth, fees, settlement timing, and no-trade gate.",
        "paid_code_bounties": "Use imported rejected/parked rows as negative samples, then scout fresh explicit-payout issues with duplicate checks before any PR work.",
        "content_and_social_growth": "Prepare a read-only Grok/X research packet through the existing service request; no posts, replies, likes, follows, or settings changes.",
        "web3_airdrops_grants_hackathons": "Scout terms, deadlines, eligibility, and required account/wallet actions; stop before registration, wallet, deployment, or transaction work.",
        "lead_generation_and_sales": "Draft non-spam offer rules, target filters, proof artifacts, and review gates before any outreach account or message action.",
        "local_trading_strategy_research": "Inventory local backtest artifacts and define a paper-only evidence standard; no broker/API/trade action.",
        "money_source_discovery": "Use the starter browser-read-only service request to build a source registry of monetizable venues, payout routes, account gates, and first proof tasks.",
        "ai_ml_competitions": "Use the starter browser-read-only service request to shortlist AI/ML competitions with prize route, deadline, dataset gate, baseline feasibility, and submission/account blockers.",
        "digital_products_templates_plugins": "Use the starter browser-read-only service request to shortlist sellable template/plugin/product ideas with buyer problem, build artifact, marketplace fees, and payment/listing gates.",
        "submitted_bounty_payouts": "Read-only here. Do not assign work from this thread; coordinate with the parallel payout worker if the user explicitly reassigns ownership.",
    }
    return tasks.get(lane_id, "Create one narrow task with evidence requirements, duplicate key, owner, and stop gates before launching seekers.")


def write_company_expansion_gap_map(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else COMPANY_EXPANSION_GAP_MAP_REPORT
    json_output_path = Path(args.json_path) if args.json_path else COMPANY_EXPANSION_GAP_MAP_JSON
    validation_path = Path(args.validation_path) if args.validation_path else COMPANY_EXPANSION_GAP_MAP_VALIDATION_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    lanes = [
        dict(row)
        for row in conn.execute(
            """
            SELECT lane_id, department, owner_agent_id, owner_thread_id, status
            FROM lanes
            ORDER BY lane_id
            """
        )
    ]
    service_catalog_count = db_scalar(conn, "SELECT COUNT(*) FROM service_catalog")
    service_request_status_counts = {
        row["status"]: row["count"]
        for row in conn.execute("SELECT status, COUNT(*) AS count FROM service_requests GROUP BY status")
    }
    source_spec_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute("SELECT lane_id, COUNT(*) AS count FROM source_specs GROUP BY lane_id")
    }
    evidence_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute("SELECT lane_id, COUNT(*) AS count FROM lane_evidence GROUP BY lane_id")
    }
    trace_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute("SELECT lane_id, COUNT(*) AS count FROM trace_events GROUP BY lane_id")
    }
    parked_request_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute(
            "SELECT lane_id, COUNT(*) AS count FROM service_requests WHERE status = 'needs_review' GROUP BY lane_id"
        )
    }
    open_task_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute(
            "SELECT lane_id, COUNT(*) AS count FROM tasks WHERE status NOT IN ('complete', 'cancelled') GROUP BY lane_id"
        )
    }

    recent_trace_by_lane: dict[str, dict[str, Any]] = {}
    for row in conn.execute(
        """
        SELECT lane_id, event_id, event_type, event_time, summary, artifact_path
        FROM trace_events
        WHERE lane_id IS NOT NULL
        ORDER BY event_time DESC, created_at DESC
        """
    ):
        lane_id = row["lane_id"]
        if lane_id not in recent_trace_by_lane:
            recent_trace_by_lane[lane_id] = dict(row)

    active_lanes = [lane for lane in lanes if lane["status"] == "active"]
    read_only_external_owned_lane_ids = [
        lane["lane_id"]
        for lane in active_lanes
        if lane["lane_id"] == "submitted_bounty_payouts" and lane["owner_agent_id"] is None
    ]
    owned_active_lanes = [
        lane
        for lane in active_lanes
        if lane["owner_agent_id"] and lane["lane_id"] != "submitted_bounty_payouts"
    ]
    owned_non_platform_lanes = [lane for lane in owned_active_lanes if lane["lane_id"] != "platform_engineering"]

    lane_rows: list[dict[str, Any]] = []
    next_test_candidates: list[dict[str, Any]] = []
    for lane in active_lanes:
        lane_id = lane["lane_id"]
        source_count = source_spec_counts.get(lane_id, 0)
        evidence_count = evidence_counts.get(lane_id, 0)
        gap_tags: list[str] = []
        if lane_id == "submitted_bounty_payouts":
            gap_tags.append("keep_read_only_external_owner_boundary")
        if source_count == 0 and lane_id != "submitted_bounty_payouts":
            gap_tags.append("seed_source_spec")
        if evidence_count == 0 and lane_id not in ("platform_engineering", "submitted_bounty_payouts"):
            gap_tags.append("collect_first_local_evidence")
        if parked_request_counts.get(lane_id, 0):
            gap_tags.append("refresh_parked_service_requests")
        if open_task_counts.get(lane_id, 0) == 0 and lane_id != "submitted_bounty_payouts":
            gap_tags.append("create_next_narrow_manager_task")
        if trace_counts.get(lane_id, 0) == 0 and lane_id != "submitted_bounty_payouts":
            gap_tags.append("record_first_trace_event")
        if not gap_tags:
            gap_tags.append("continue_periodic_review")

        if "seed_source_spec" in gap_tags:
            recommended_next_test = "Draft a local source-spec seed packet for this lane; no browser, account, or external action."
        elif "collect_first_local_evidence" in gap_tags:
            recommended_next_test = "Create a first local evidence packet from existing reports or approved public-source scans."
        elif "refresh_parked_service_requests" in gap_tags:
            recommended_next_test = "Refresh the parked service-request review packet and keep action gated."
        elif lane_id == "submitted_bounty_payouts":
            recommended_next_test = "Keep read-only visibility; do not duplicate the external payout worker."
        else:
            recommended_next_test = suggested_manager_task(lane_id)

        lane_row = {
            "lane_id": lane_id,
            "department": lane["department"],
            "owner_agent_id": lane["owner_agent_id"],
            "owner_thread_id": lane["owner_thread_id"],
            "source_spec_count": source_count,
            "evidence_count": evidence_count,
            "parked_service_request_count": parked_request_counts.get(lane_id, 0),
            "open_task_count": open_task_counts.get(lane_id, 0),
            "trace_event_count": trace_counts.get(lane_id, 0),
            "recent_trace_event": recent_trace_by_lane.get(lane_id),
            "gap_tags": gap_tags,
            "recommended_next_test": recommended_next_test,
        }
        lane_rows.append(lane_row)
        next_test_candidates.append(
            {
                "lane_id": lane_id,
                "gap_tags": gap_tags,
                "recommended_next_test": recommended_next_test,
                "allowed_scope": "local_report_only",
                "requires_human_approval_for_side_effects": True,
            }
        )

    source_spec_gap_lane_ids = [
        lane["lane_id"]
        for lane in owned_active_lanes
        if source_spec_counts.get(lane["lane_id"], 0) == 0
    ]
    evidence_gap_lane_ids = [
        lane["lane_id"]
        for lane in owned_non_platform_lanes
        if evidence_counts.get(lane["lane_id"], 0) == 0
    ]
    idle_owned_lane_ids = [
        lane["lane_id"]
        for lane in owned_active_lanes
        if open_task_counts.get(lane["lane_id"], 0) == 0
    ]

    runtime_boundary = {
        "browser_sessions_started": 0,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "security_testing_actions": False,
        "real_money_actions": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }
    all_active_lanes_scanned = len(lane_rows) == len(active_lanes)
    all_active_lanes_have_next_test_candidate = len(next_test_candidates) == len(active_lanes)
    read_only_boundary_preserved = read_only_external_owned_lane_ids == ["submitted_bounty_payouts"]
    if len(active_lanes) != 12:
        failures.append(f"expected 12 active lanes, got {len(active_lanes)}")
    if len(owned_active_lanes) != 11:
        failures.append(f"expected 11 owned active lanes excluding payout boundary, got {len(owned_active_lanes)}")
    if service_catalog_count != 13:
        failures.append(f"expected 13 service catalog entries, got {service_catalog_count}")
    if not read_only_boundary_preserved:
        failures.append("submitted_bounty_payouts read-only ownership boundary was not preserved")
    if not all_active_lanes_scanned:
        failures.append("not all active lanes were scanned")
    if not all_active_lanes_have_next_test_candidate:
        failures.append("not all active lanes received a next-test candidate")

    payload = {
        "schema_version": "agent_company.company_expansion_gap_map.v1",
        "generated_utc": generated_utc,
        "purpose": "Report-only scan of lane, service, source, evidence, and trace coverage to identify the next safe infrastructure tests.",
        "active_lane_count": len(active_lanes),
        "owned_active_lane_count": len(owned_active_lanes),
        "read_only_external_owned_lane_ids": read_only_external_owned_lane_ids,
        "service_catalog_count": service_catalog_count,
        "source_spec_gap_count": len(source_spec_gap_lane_ids),
        "source_spec_gap_lane_ids": source_spec_gap_lane_ids,
        "evidence_gap_count": len(evidence_gap_lane_ids),
        "evidence_gap_lane_ids": evidence_gap_lane_ids,
        "idle_owned_lane_count": len(idle_owned_lane_ids),
        "idle_owned_lane_ids": idle_owned_lane_ids,
        "parked_service_request_count": service_request_status_counts.get("needs_review", 0),
        "service_request_status_counts": service_request_status_counts,
        "all_active_lanes_scanned": all_active_lanes_scanned,
        "all_active_lanes_have_next_test_candidate": all_active_lanes_have_next_test_candidate,
        "lane_rows": lane_rows,
        "next_test_candidates": next_test_candidates,
        "runtime_boundary": runtime_boundary,
        "next_action": "Create source-spec seed packets for owned lanes with missing source specs, then refresh parked service-request review packets without side effects.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.company_expansion_gap_map_validation.v1",
        "generated_utc": generated_utc,
        "gap_map_path": str(json_output_path),
        "active_lane_count": len(active_lanes),
        "owned_active_lane_count": len(owned_active_lanes),
        "read_only_external_owned_lane_count": len(read_only_external_owned_lane_ids),
        "read_only_boundary_preserved": read_only_boundary_preserved,
        "service_catalog_count": service_catalog_count,
        "source_spec_gap_count": len(source_spec_gap_lane_ids),
        "evidence_gap_count": len(evidence_gap_lane_ids),
        "idle_owned_lane_count": len(idle_owned_lane_ids),
        "parked_service_request_count": service_request_status_counts.get("needs_review", 0),
        "all_active_lanes_scanned": all_active_lanes_scanned,
        "all_active_lanes_have_next_test_candidate": all_active_lanes_have_next_test_candidate,
        "next_test_candidate_count": len(next_test_candidates),
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Agent Company Expansion Gap Map",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Summary",
        "",
        f"- Active lanes scanned: `{len(active_lanes)}`",
        f"- Owned active lanes: `{len(owned_active_lanes)}`",
        f"- Service catalog entries: `{service_catalog_count}`",
        f"- Owned lanes missing source specs: `{len(source_spec_gap_lane_ids)}`",
        f"- Owned non-platform lanes missing evidence: `{len(evidence_gap_lane_ids)}`",
        f"- Parked service requests: `{service_request_status_counts.get('needs_review', 0)}`",
        f"- Read-only payout boundary preserved: `{read_only_boundary_preserved}`",
        "",
        "## Lane Gap Rows",
        "",
        "| Lane | Sources | Evidence | Parked Requests | Open Tasks | Traces | Gap Tags | Next Test |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in lane_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['lane_id']}`",
                    str(row["source_spec_count"]),
                    str(row["evidence_count"]),
                    str(row["parked_service_request_count"]),
                    str(row["open_task_count"]),
                    str(row["trace_event_count"]),
                    md_cell(", ".join(row["gap_tags"]), 220),
                    md_cell(row["recommended_next_test"], 320),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This report is local and report-only.",
            "- It does not start browser sessions, register accounts, touch wallets or payments, perform public actions, run security tests, place trades, mutate service requests, assign workers, start workers, call APIs, or create external side effects.",
            "",
            "## Next Action",
            "",
            payload["next_action"],
            "",
        ]
    )
    if failures:
        lines.extend(["## Failures", ""])
        for failure in failures:
            lines.append(f"- {failure}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": all_checks_passed,
                "path": str(output_path),
                "json_path": str(json_output_path),
                "validation_path": str(validation_path),
                "active_lane_count": len(active_lanes),
                "source_spec_gap_count": len(source_spec_gap_lane_ids),
                "evidence_gap_count": len(evidence_gap_lane_ids),
                "next_test_candidate_count": len(next_test_candidates),
                "failure_count": len(failures),
            },
            indent=2,
        )
    )

