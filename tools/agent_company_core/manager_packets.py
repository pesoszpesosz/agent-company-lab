from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .catalog import department_id
from .constants import LANE_THREAD_MANIFEST_JSON, LANE_THREAD_MANIFEST_MD
from .control_reports import lane_recommendation, suggested_manager_task
from .io import now_utc
from .manager_packets_content import build_manager_packet_lines, manager_packet_read_only_note
from .paths import DB_PATH, LAUNCH_DIR, MANAGER_PACKET_DIR, REPORTS_DIR
from .utils import decode_json_list, md_cell, safe_id_fragment


THREAD_LAUNCH_ORDER = [
    "money_source_discovery",
    "ai_ml_competitions",
    "digital_products_templates_plugins",
    "security_bounty_private_reports",
    "prediction_market_research",
    "paid_code_bounties",
    "content_and_social_growth",
    "web3_airdrops_grants_hackathons",
    "lead_generation_and_sales",
    "local_trading_strategy_research",
]

THREAD_HELD_LANES = {
    "platform_engineering": "This recovered thread is the platform coordinator and should keep ownership here.",
    "submitted_bounty_payouts": "Read-only in this lab. The parallel payout worker owns GitHub/RustChain/Charles payout monitoring.",
}

def write_manager_packets(conn: sqlite3.Connection, output_dir: str | None) -> None:
    packet_dir = Path(output_dir) if output_dir else MANAGER_PACKET_DIR
    packet_dir.mkdir(parents=True, exist_ok=True)
    lanes = [dict(row) for row in conn.execute("SELECT * FROM lanes ORDER BY lane_id")]
    evidence_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute("SELECT lane_id, COUNT(*) AS count FROM lane_evidence GROUP BY lane_id")
    }
    status_counts_by_lane: dict[str, dict[str, int]] = {}
    for row in conn.execute("SELECT lane_id, status, COUNT(*) AS count FROM lane_evidence GROUP BY lane_id, status"):
        status_counts_by_lane.setdefault(row["lane_id"], {})[row["status"]] = row["count"]
    active_task_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute(
            "SELECT lane_id, COUNT(*) AS count FROM tasks WHERE status NOT IN ('complete', 'cancelled') GROUP BY lane_id"
        )
    }
    service_request_counts = {
        row["lane_id"] or "unassigned": row["count"]
        for row in conn.execute(
            "SELECT COALESCE(lane_id, 'unassigned') AS lane_id, COUNT(*) AS count FROM service_requests WHERE status NOT IN ('complete', 'cancelled') GROUP BY COALESCE(lane_id, 'unassigned')"
        )
    }
    service_catalog = [
        dict(row)
        for row in conn.execute(
            "SELECT service_id, request_type, owner_role_id, default_status, purpose FROM service_catalog ORDER BY request_type, service_id"
        )
    ]

    index_lines = [
        "# Agent Company Manager Packets",
        "",
        f"Generated UTC: {now_utc()}",
        f"Database: `{DB_PATH}`",
        "",
        "## Boundary",
        "",
        "- A manager packet is an instruction and evidence view, not permission to perform gated side effects.",
        "- Each future manager should register an agent, claim an unowned lane, acquire one task, write artifacts, and record outcomes.",
        "- `submitted_bounty_payouts` is read-only in this thread and remains assigned to the parallel payout worker.",
        "",
        "## Index",
        "",
        "| Lane | Department | Owner | Evidence | Open Tasks | Open Service Requests | Packet | Recommendation |",
        "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    written: list[str] = []

    for lane in lanes:
        lane_id = lane["lane_id"]
        specs = [
            dict(row)
            for row in conn.execute(
                """
                SELECT spec_id, name, source_type, cadence, risk_gate, refresh_command, source_paths_json, outputs_json, notes
                FROM source_specs
                WHERE lane_id = ?
                ORDER BY spec_id
                """,
                (lane_id,),
            )
        ]
        evidence = [
            dict(row)
            for row in conn.execute(
                """
                SELECT evidence_id, status, title, source_path, source_url, summary, next_action, ownership_note, updated_at
                FROM lane_evidence
                WHERE lane_id = ?
                ORDER BY
                  CASE
                    WHEN status LIKE '%submission%' THEN 1
                    WHEN status LIKE '%verified%' THEN 2
                    WHEN status LIKE '%promote%' THEN 3
                    WHEN status LIKE '%watch%' THEN 4
                    WHEN status LIKE '%imported%' THEN 5
                    ELSE 6
                  END,
                  updated_at DESC
                LIMIT 12
                """,
                (lane_id,),
            )
        ]
        tasks = [
            dict(row)
            for row in conn.execute(
                """
                SELECT task_id, status, priority, title, owner_agent_id, duplicate_key, evidence_required, next_action,
                       lease_owner_agent_id, lease_expires_at
                FROM tasks
                WHERE lane_id = ?
                ORDER BY
                  CASE WHEN status IN ('complete', 'cancelled') THEN 2 ELSE 1 END,
                  priority DESC,
                  created_at DESC
                LIMIT 12
                """,
                (lane_id,),
            )
        ]
        requests = [
            dict(row)
            for row in conn.execute(
                """
                SELECT request_id, service_id, request_type, status, risk_gate, requested_action, approval_scope,
                       assigned_agent_id, artifact_path, decision_note, updated_at
                FROM service_requests
                WHERE lane_id = ?
                ORDER BY updated_at DESC
                LIMIT 12
                """,
                (lane_id,),
            )
        ]
        outcomes = [
            dict(row)
            for row in conn.execute(
                """
                SELECT outcome_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at
                FROM outcomes
                WHERE lane_id = ?
                ORDER BY created_at DESC
                LIMIT 8
                """,
                (lane_id,),
            )
        ]

        owner = lane["owner_agent_id"] or lane["owner_thread_id"] or "unowned"
        recommendation = lane_recommendation(
            lane_id,
            status_counts_by_lane.get(lane_id, {}),
            active_task_counts.get(lane_id, 0),
            service_request_counts.get(lane_id, 0),
        )
        packet_path = packet_dir / f"{lane_id}-manager-packet.md"
        lines = build_manager_packet_lines(
            lane=lane,
            specs=specs,
            evidence=evidence,
            tasks=tasks,
            requests=requests,
            outcomes=outcomes,
            service_catalog=service_catalog,
            owner=owner,
            recommendation=recommendation,
            generated_utc=now_utc(),
            read_only_note=manager_packet_read_only_note(lane_id),
        )
        packet_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        written.append(str(packet_path))
        index_lines.append(
            "| "
            + " | ".join(
                [
                    f"`{lane_id}`",
                    md_cell(lane["department"], 100),
                    md_cell(owner, 140),
                    str(evidence_counts.get(lane_id, 0)),
                    str(active_task_counts.get(lane_id, 0)),
                    str(service_request_counts.get(lane_id, 0)),
                    f"`{packet_path}`",
                    md_cell(recommendation, 260),
                ]
            )
            + " |"
        )

    index_path = packet_dir / "index.md"
    index_path.write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    written.append(str(index_path))
    print(json.dumps({"ok": True, "count": len(written), "index": str(index_path), "paths": written}, indent=2))

