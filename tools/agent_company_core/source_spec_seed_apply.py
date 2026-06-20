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

def write_source_spec_seed_apply(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.path) if args.path else SOURCE_SPEC_SEED_APPLY_REPORT
    json_output_path = Path(args.json_path) if args.json_path else SOURCE_SPEC_SEED_APPLY_JSON
    validation_path = Path(args.validation_path) if args.validation_path else SOURCE_SPEC_SEED_APPLY_VALIDATION_JSON
    seed_packets_path = Path(args.seed_packets_path) if args.seed_packets_path else SOURCE_SPEC_SEED_PACKETS_JSON
    generated_utc = now_utc()
    failures: list[str] = []

    seed_manifest, seed_errors = load_report_json_or_error(seed_packets_path)
    failures.extend(seed_errors)
    packet_rows = seed_manifest.get("packet_rows", []) if seed_manifest else []
    if seed_manifest and not isinstance(packet_rows, list):
        failures.append("seed packet manifest packet_rows is not a list")
        packet_rows = []

    table_rows_before = db_scalar(conn, "SELECT COUNT(*) FROM source_specs")
    registry_payload = load_json(SOURCE_SPECS_PATH) if SOURCE_SPECS_PATH.exists() else {"version": "local", "specs": []}
    registry_specs = registry_payload.setdefault("specs", [])
    registry_count_before = len(registry_specs) if isinstance(registry_specs, list) else 0
    if not isinstance(registry_specs, list):
        failures.append("source spec registry field specs is not a list")
        registry_specs = []
        registry_payload["specs"] = registry_specs
    registry_before_text = SOURCE_SPECS_PATH.read_text(encoding="utf-8") if SOURCE_SPECS_PATH.exists() else ""

    applied_specs: list[dict[str, Any]] = []
    for row in packet_rows:
        packet_path = Path(row.get("packet_path", ""))
        packet, packet_errors = load_report_json_or_error(packet_path)
        failures.extend(packet_errors)
        if not packet:
            continue
        if packet.get("schema_version") != "agent_company.source_spec_seed_packet.v1":
            failures.append(f"unexpected source spec seed packet schema: {packet_path}")
            continue
        if packet.get("report_only") is not True or packet.get("registry_insert_allowed") is not False:
            failures.append(f"seed packet is not a report-only draft as expected: {packet_path}")
            continue
        spec = packet.get("proposed_source_spec")
        if not isinstance(spec, dict):
            failures.append(f"seed packet missing proposed_source_spec: {packet_path}")
            continue
        required = ["id", "lane_id", "name", "source_type", "source_paths", "cadence", "risk_gate", "outputs"]
        missing = [key for key in required if key not in spec]
        if missing:
            failures.append(f"proposed source spec missing fields {missing}: {packet_path}")
            continue
        upsert_source_spec(conn, spec)
        existing_index = next((idx for idx, item in enumerate(registry_specs) if item.get("id") == spec["id"]), None)
        if existing_index is None:
            registry_specs.append(spec)
        else:
            registry_specs[existing_index] = spec
        applied_specs.append(
            {
                "spec_id": spec["id"],
                "lane_id": spec["lane_id"],
                "packet_path": str(packet_path),
                "source_type": spec["source_type"],
            }
        )

    registry_specs.sort(key=lambda item: (item.get("lane_id", ""), item.get("id", "")))
    registry_payload["specs"] = registry_specs
    SOURCE_SPECS_PATH.write_text(json.dumps(registry_payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    conn.commit()

    table_rows_after = db_scalar(conn, "SELECT COUNT(*) FROM source_specs")
    registry_after_text = SOURCE_SPECS_PATH.read_text(encoding="utf-8")
    registry_count_after = len(registry_specs)
    registry_file_modified_by_apply = registry_before_text != registry_after_text
    applied_spec_ids = [row["spec_id"] for row in applied_specs]
    db_present_count = db_scalar(
        conn,
        f"SELECT COUNT(*) FROM source_specs WHERE spec_id IN ({','.join('?' for _ in applied_spec_ids)})"
        if applied_spec_ids
        else "SELECT 0",
        tuple(applied_spec_ids),
    )
    registry_ids = {item.get("id") for item in registry_specs}
    all_applied_specs_present_in_registry = all(spec_id in registry_ids for spec_id in applied_spec_ids)
    all_applied_specs_present_in_db = db_present_count == len(applied_spec_ids)
    source_spec_gap_count_after_apply = db_scalar(
        conn,
        """
        SELECT COUNT(*)
        FROM lanes
        WHERE status = 'active'
          AND owner_agent_id IS NOT NULL
          AND lane_id != 'submitted_bounty_payouts'
          AND lane_id NOT IN (SELECT lane_id FROM source_specs)
        """,
    )

    if len(packet_rows) != 3:
        failures.append(f"expected 3 seed packet rows, got {len(packet_rows)}")
    if len(applied_specs) != 3:
        failures.append(f"expected 3 applied specs, got {len(applied_specs)}")
    if table_rows_before != 10:
        failures.append(f"expected 10 source_specs rows before apply, got {table_rows_before}")
    if table_rows_after != 13:
        failures.append(f"expected 13 source_specs rows after apply, got {table_rows_after}")
    if registry_count_before != 10:
        failures.append(f"expected 10 registry specs before apply, got {registry_count_before}")
    if registry_count_after != 13:
        failures.append(f"expected 13 registry specs after apply, got {registry_count_after}")
    if not all_applied_specs_present_in_db:
        failures.append("not all applied specs are present in DB")
    if not all_applied_specs_present_in_registry:
        failures.append("not all applied specs are present in registry")
    if source_spec_gap_count_after_apply != 0:
        failures.append(f"expected 0 source-spec gap lanes after apply, got {source_spec_gap_count_after_apply}")
    if not registry_file_modified_by_apply:
        failures.append("registry file was not modified by apply command")

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
        "schema_version": "agent_company.source_spec_seed_apply.v1",
        "generated_utc": generated_utc,
        "purpose": "Apply validated local source-spec seed packets to the source-spec registry and DB; no refresh commands or external actions are executed.",
        "seed_packets_path": str(seed_packets_path),
        "applied_specs": applied_specs,
        "seed_packet_count": len(packet_rows),
        "applied_spec_count": len(applied_specs),
        "source_specs_table_rows_before": table_rows_before,
        "source_specs_table_rows_after": table_rows_after,
        "source_specs_registry_count_before": registry_count_before,
        "source_specs_registry_count_after": registry_count_after,
        "source_specs_inserted_or_updated": len(applied_specs),
        "all_applied_specs_present_in_db": all_applied_specs_present_in_db,
        "all_applied_specs_present_in_registry": all_applied_specs_present_in_registry,
        "source_spec_gap_count_after_apply": source_spec_gap_count_after_apply,
        "registry_file_modified_by_apply": registry_file_modified_by_apply,
        "runtime_boundary": runtime_boundary,
        "next_action": "Regenerate source-spec, gap-map, and seed-packet reports; missing source-spec count should now be zero.",
    }
    json_output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    all_checks_passed = not failures
    validation_payload = {
        "schema_version": "agent_company.source_spec_seed_apply_validation.v1",
        "generated_utc": generated_utc,
        "apply_report_path": str(json_output_path),
        "seed_packet_count": len(packet_rows),
        "applied_spec_count": len(applied_specs),
        "source_specs_table_rows_before": table_rows_before,
        "source_specs_table_rows_after": table_rows_after,
        "source_specs_registry_count_before": registry_count_before,
        "source_specs_registry_count_after": registry_count_after,
        "source_specs_inserted_or_updated": len(applied_specs),
        "all_applied_specs_present_in_db": all_applied_specs_present_in_db,
        "all_applied_specs_present_in_registry": all_applied_specs_present_in_registry,
        "source_spec_gap_count_after_apply": source_spec_gap_count_after_apply,
        "registry_file_modified_by_apply": registry_file_modified_by_apply,
        "all_checks_passed": all_checks_passed,
        "failure_count": len(failures),
        **runtime_boundary,
        "failures": failures,
    }
    validation_path.write_text(json.dumps(validation_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Source Spec Seed Apply",
        "",
        f"Generated UTC: {generated_utc}",
        f"JSON mirror: `{json_output_path}`",
        f"Validation: `{validation_path}`",
        "",
        "## Summary",
        "",
        f"- Seed packet rows: `{len(packet_rows)}`",
        f"- Applied specs: `{len(applied_specs)}`",
        f"- Source-spec DB rows before: `{table_rows_before}`",
        f"- Source-spec DB rows after: `{table_rows_after}`",
        f"- Registry specs before: `{registry_count_before}`",
        f"- Registry specs after: `{registry_count_after}`",
        f"- Source-spec gaps after apply: `{source_spec_gap_count_after_apply}`",
        "",
        "## Applied Specs",
        "",
        "| Lane | Spec | Source Type | Packet |",
        "| --- | --- | --- | --- |",
    ]
    for spec in applied_specs:
        lines.append(
            f"| `{spec['lane_id']}` | `{spec['spec_id']}` | `{spec['source_type']}` | `{spec['packet_path']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This command only updates local registry and SQLite source-spec rows.",
            "- It does not run refresh commands, browse, register accounts, accept terms, download gated data, publish, submit, touch wallets/payments, mutate service requests, assign workers, start workers, call APIs, or create external side effects.",
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
                "applied_spec_count": len(applied_specs),
                "source_specs_table_rows_after": table_rows_after,
                "source_spec_gap_count_after_apply": source_spec_gap_count_after_apply,
                "failure_count": len(failures),
            },
            indent=2,
        )
    )
