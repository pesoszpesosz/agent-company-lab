from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .catalog import upsert_source_spec
from .constants import (
    COMPANY_EXPANSION_GAP_MAP_JSON,
    SOURCE_SPECS_REPORT,
    SOURCE_SPEC_SEED_APPLY_JSON,
    SOURCE_SPEC_SEED_APPLY_REPORT,
    SOURCE_SPEC_SEED_APPLY_VALIDATION_JSON,
    SOURCE_SPEC_SEED_PACKETS_JSON,
    SOURCE_SPEC_SEED_PACKETS_REPORT,
    SOURCE_SPEC_SEED_PACKETS_VALIDATION_JSON,
    SOURCE_SPEC_SEED_PACKET_DIR,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR, SOURCE_SPECS_PATH
from .service_workers import db_scalar, load_report_json_or_error
from .utils import decode_json_list, md_cell

def proposed_source_spec_seed(lane_id: str) -> dict[str, Any]:
    seeds: dict[str, dict[str, Any]] = {
        "ai_ml_competitions": {
            "id": "ai_ml_competitions_public_prize_source_seed",
            "name": "AI/ML Competition Public Prize Source Seed",
            "source_type": "public_competition_registry",
            "source_paths": [
                "Kaggle competitions listing",
                "DrivenData competitions listing",
                "EvalAI challenges listing",
                "AICrowd challenges listing",
                "Hugging Face competitions/spaces calls when prize route is explicit",
            ],
            "refresh_command": "Prepare a read-only public listing scan only after lane manager claim; save results to a dated local shortlist artifact.",
            "cadence": "lane_owner_on_demand_or_weekly",
            "risk_gate": "read_only_public_research_no_account_submission_dataset_download_or_terms_acceptance",
            "outputs": [
                "E:\\agent-company-lab\\reports\\ai-ml-competitions\\public-prize-source-refresh-YYYYMMDD.md",
                "lane_evidence",
                "service_request_candidates",
            ],
            "notes": "Use to find prize competitions and benchmark tasks. Account creation, dataset download behind terms, submissions, and paid compute all require separate gates.",
        },
        "digital_products_templates_plugins": {
            "id": "digital_products_marketplace_demand_source_seed",
            "name": "Digital Product Marketplace Demand Source Seed",
            "source_type": "public_marketplace_research",
            "source_paths": [
                "Gumroad public marketplace/search pages",
                "Lemon Squeezy storefront examples",
                "Etsy digital product public category pages",
                "GitHub trending/template/plugin repositories",
                "Codex/OpenAI plugin and skill local product notes",
            ],
            "refresh_command": "Prepare a read-only demand and fee scan only after lane manager claim; no listing, account, checkout, or payment action.",
            "cadence": "lane_owner_on_demand_or_weekly",
            "risk_gate": "read_only_market_research_no_listing_account_payment_or_public_submission",
            "outputs": [
                "E:\\agent-company-lab\\reports\\digital-products-templates-plugins\\marketplace-demand-refresh-YYYYMMDD.md",
                "lane_evidence",
                "legal_kyc_tax_payment_gate_candidates",
            ],
            "notes": "Use to identify sellable template/plugin ideas and marketplace blockers. Publishing/listing/payment setup requires explicit service requests.",
        },
        "money_source_discovery": {
            "id": "money_source_discovery_public_venue_source_seed",
            "name": "Money Source Discovery Public Venue Source Seed",
            "source_type": "public_venue_registry",
            "source_paths": [
                "public bounty and paid-task venue lists",
                "grant and hackathon aggregators",
                "creator-marketplace opportunity lists",
                "AI evaluation and data-labeling opportunity pages",
                "local profit-edge imported negative and parked rows",
            ],
            "refresh_command": "Prepare a read-only source registry scan only after lane manager claim; classify venue, payout route, account gate, and proof artifact.",
            "cadence": "lane_owner_on_demand_or_weekly",
            "risk_gate": "read_only_discovery_no_registration_outreach_wallet_payment_or_submission",
            "outputs": [
                "E:\\agent-company-lab\\reports\\money-source-discovery\\public-venue-source-refresh-YYYYMMDD.md",
                "lane_evidence",
                "service_request_candidates",
            ],
            "notes": "Use to widen the online money-path map. Any registration, outreach, wallet, payment, or public submission remains separately gated.",
        },
    }
    fallback = {
        "id": f"{lane_id}_source_seed",
        "name": f"{lane_id} Source Seed",
        "source_type": "local_report_only_seed",
        "source_paths": ["to be filled by lane manager"],
        "refresh_command": "Draft a source-spec proposal only; do not execute external actions.",
        "cadence": "lane_owner_on_demand",
        "risk_gate": "report_only_until_lane_specific_gate_defined",
        "outputs": ["lane_evidence"],
        "notes": "Fallback seed packet; refine before insertion into source-spec registry.",
    }
    return seeds.get(lane_id, fallback)


def write_source_spec_seed_packets(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    seed_dir = Path(args.packet_dir) if args.packet_dir else SOURCE_SPEC_SEED_PACKET_DIR
    seed_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SOURCE_SPEC_SEED_PACKETS_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SOURCE_SPEC_SEED_PACKETS_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SOURCE_SPEC_SEED_PACKETS_VALIDATION_JSON
    gap_map_path = Path(args.gap_map_path) if args.gap_map_path else COMPANY_EXPANSION_GAP_MAP_JSON
    generated_utc = now_utc()
    failures: list[str] = []
    source_specs_before = db_scalar(conn, "SELECT COUNT(*) FROM source_specs")
    registry_mtime_before = SOURCE_SPECS_PATH.stat().st_mtime if SOURCE_SPECS_PATH.exists() else None

    gap_map, gap_map_errors = load_report_json_or_error(gap_map_path)
    failures.extend(gap_map_errors)
    source_spec_gap_lanes = gap_map.get("source_spec_gap_lane_ids", []) if gap_map else []
    if gap_map and not isinstance(source_spec_gap_lanes, list):
        failures.append("gap map source_spec_gap_lane_ids is not a list")
        source_spec_gap_lanes = []

    db_gap_lanes = [
        row["lane_id"]
        for row in conn.execute(
            """
            SELECT lane_id
            FROM lanes
            WHERE status = 'active'
              AND owner_agent_id IS NOT NULL
              AND lane_id != 'submitted_bounty_payouts'
              AND lane_id NOT IN (SELECT lane_id FROM source_specs)
            ORDER BY lane_id
            """
        )
    ]
    if sorted(source_spec_gap_lanes) != db_gap_lanes:
        failures.append(
            f"gap-map lane list does not match DB source-spec gaps: gap_map={source_spec_gap_lanes}, db={db_gap_lanes}"
        )
        source_spec_gap_lanes = db_gap_lanes

    packet_rows: list[dict[str, Any]] = []
    for lane_id in source_spec_gap_lanes:
        spec = proposed_source_spec_seed(lane_id)
        packet_path = seed_dir / f"{lane_id}-source-spec-seed-20260615.json"
        md_path = seed_dir / f"{lane_id}-source-spec-seed-20260615.md"
        packet = {
            "schema_version": "agent_company.source_spec_seed_packet.v1",
            "generated_utc": generated_utc,
            "lane_id": lane_id,
            "report_only": True,
            "registry_insert_allowed": False,
            "proposed_source_spec": {
                "id": spec["id"],
                "lane_id": lane_id,
                "name": spec["name"],
                "source_type": spec["source_type"],
                "source_paths": spec["source_paths"],
                "refresh_command": spec["refresh_command"],
                "cadence": spec["cadence"],
                "risk_gate": spec["risk_gate"],
                "outputs": spec["outputs"],
                "notes": spec["notes"],
            },
            "forbidden_actions": [
                "Do not insert this packet into source_specs without a separate explicit task.",
                "Do not browse, register accounts, accept terms, download gated datasets, publish listings, submit work, touch wallets/payments, or send outreach from this packet.",
                "Do not mutate service requests or assign workers from this packet.",
            ],
            "next_action": "Review and, if accepted, convert into a source-spec registry row in a separate local-only task.",
        }
        packet_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        md_lines = [
            f"# Source Spec Seed Packet: {lane_id}",
            "",
            f"Generated UTC: {generated_utc}",
            f"JSON mirror: `{packet_path}`",
            "",
            "## Proposed Source Spec",
            "",
            f"- ID: `{spec['id']}`",
            f"- Name: {spec['name']}",
            f"- Type: `{spec['source_type']}`",
            f"- Cadence: `{spec['cadence']}`",
            f"- Risk gate: `{spec['risk_gate']}`",
            "",
            "## Source Paths",
            "",
        ]
        md_lines.extend([f"- {item}" for item in spec["source_paths"]])
        md_lines.extend(["", "## Outputs", ""])
        md_lines.extend([f"- {item}" for item in spec["outputs"]])
        md_lines.extend(
            [
                "",
                "## Boundary",
                "",
                "This packet is report-only. It does not add a source spec, execute refresh commands, browse, register accounts, accept terms, download gated data, publish, submit, touch wallets/payments, mutate service requests, assign workers, call APIs, or create external side effects.",
                "",
                "## Next Action",
                "",
                packet["next_action"],
                "",
            ]
        )
        md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
        packet_rows.append(
            {
                "lane_id": lane_id,
                "packet_path": str(packet_path),
                "markdown_path": str(md_path),
                "proposed_spec_id": spec["id"],
                "report_only": True,
                "registry_insert_allowed": False,
            }
        )

    source_specs_after = db_scalar(conn, "SELECT COUNT(*) FROM source_specs")
    registry_mtime_after = SOURCE_SPECS_PATH.stat().st_mtime if SOURCE_SPECS_PATH.exists() else None
    registry_file_modified_by_packet = registry_mtime_before != registry_mtime_after
    all_gap_lanes_have_seed_packet = sorted(row["lane_id"] for row in packet_rows) == sorted(db_gap_lanes)
    all_seed_packets_report_only = all(row["report_only"] and not row["registry_insert_allowed"] for row in packet_rows)
    if len(packet_rows) != len(db_gap_lanes):
        failures.append(f"expected {len(db_gap_lanes)} seed packets, got {len(packet_rows)}")
    if source_specs_after != source_specs_before:
        failures.append(f"source_specs row count changed from {source_specs_before} to {source_specs_after}")
    if registry_file_modified_by_packet:
        failures.append("source-spec registry file was modified by seed packet generation")
    if not all_gap_lanes_have_seed_packet:
        failures.append("not all source-spec gap lanes have a seed packet")
    if not all_seed_packets_report_only:
        failures.append("not all seed packets are report-only")

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
    payload = {
        "schema_version": "agent_company.source_spec_seed_packets.v1",
        "generated_utc": generated_utc,
        "purpose": "Report-only draft source-spec packets for owned lanes currently missing source specs.",
        "gap_map_path": str(gap_map_path),
        "packet_dir": str(seed_dir),
        "seed_packet_count": len(packet_rows),
        "missing_source_spec_lane_count": len(db_gap_lanes),
        "source_spec_gap_count_from_gap_map": gap_map.get("source_spec_gap_count") if gap_map else None,
        "source_spec_gap_lane_ids": db_gap_lanes,
        "packet_rows": packet_rows,
        "source_specs_table_rows_before": source_specs_before,
        "source_specs_table_rows_after": source_specs_after,
        "source_specs_inserted_by_packet": source_specs_after - source_specs_before,
        "registry_file_modified_by_packet": registry_file_modified_by_packet,
        "all_gap_lanes_have_seed_packet": all_gap_lanes_have_seed_packet,
        "all_seed_packets_report_only": all_seed_packets_report_only,
        "runtime_boundary": runtime_boundary,
        "next_action": "Review these seed packets and convert accepted proposals into source_specs registry rows in a separate local-only task.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.source_spec_seed_packets_validation.v1",
        "generated_utc": generated_utc,
        "seed_packets_path": str(json_output_path),
        "seed_packet_count": len(packet_rows),
        "missing_source_spec_lane_count": len(db_gap_lanes),
        "source_spec_gap_count_from_gap_map": gap_map.get("source_spec_gap_count") if gap_map else None,
        "all_gap_lanes_have_seed_packet": all_gap_lanes_have_seed_packet,
        "all_seed_packets_report_only": all_seed_packets_report_only,
        "source_specs_table_rows_before": source_specs_before,
        "source_specs_table_rows_after": source_specs_after,
        "source_specs_inserted_by_packet": source_specs_after - source_specs_before,
        "registry_file_modified_by_packet": registry_file_modified_by_packet,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Source Spec Seed Packets",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Summary",
        "",
        f"- Missing source-spec lanes: `{len(db_gap_lanes)}`",
        f"- Seed packets generated: `{len(packet_rows)}`",
        f"- Source-spec DB rows before: `{source_specs_before}`",
        f"- Source-spec DB rows after: `{source_specs_after}`",
        f"- Registry file modified: `{registry_file_modified_by_packet}`",
        "",
        "## Packets",
        "",
        "| Lane | Proposed Spec | JSON | Markdown |",
        "| --- | --- | --- | --- |",
    ]
    for row in packet_rows:
        lines.append(
            f"| `{row['lane_id']}` | `{row['proposed_spec_id']}` | `{row['packet_path']}` | `{row['markdown_path']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- These packets are local, report-only drafts.",
            "- They do not insert source_specs rows, modify the source-spec registry, run refresh commands, browse, register accounts, accept terms, download gated data, publish, submit, touch wallets/payments, mutate service requests, assign workers, start workers, call APIs, or create external side effects.",
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
                "packet_dir": str(seed_dir),
                "seed_packet_count": len(packet_rows),
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
