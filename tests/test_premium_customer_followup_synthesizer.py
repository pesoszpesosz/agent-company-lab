import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.premium_customer_followup_synthesizer import (  # noqa: E402
    synthesize_premium_customer_followups,
)
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    ts = "2026-06-20T00:00:00Z"
    for lane_id, owner in [
        ("ai_resources_lab", "lane-manager-ai_resources_lab-20260620"),
        ("youtube_content_channels", "lane-manager-youtube_content_channels-20260620"),
    ]:
        conn.execute(
            """
            INSERT INTO lanes(
              lane_id, department, status, owner_agent_id, owner_thread_id, agent_types_json,
              examples_json, promotion_gates_json, service_workers_required_json,
              side_effects_json, global_gates_json, notes, created_at, updated_at
            )
            VALUES(?, 'Test', 'active', ?, 'thread-test', '[]', '[]', '[]', '[]', '[]', '[]', NULL, ?, ?)
            """,
            (lane_id, owner, ts, ts),
        )
    conn.commit()
    return conn


def _route_packet(path: Path) -> Path:
    packet = {
        "schema_version": "customer_input_route_packet.v2",
        "input_id": "customer-input-followup-test",
        "customer_intent": "Build the CEO company system. Also create YouTube channels.",
        "target_lane_ids": ["ai_resources_lab", "youtube_content_channels"],
        "routes": [
            {"lane_or_surface": "ai_resources_lab", "status": "routed"},
            {"lane_or_surface": "youtube_content_channels", "status": "routed"},
        ],
        "ceo_context_capsule": {
            "why_this_route": "Primary route `ai_resources_lab` selected from deterministic local lane/surface matching plus current DB context.",
            "short_summary": "Build the CEO company system. Also create YouTube channels.",
        },
        "zero_side_effect_boundary": {"external_side_effects": False},
    }
    path.write_text(json.dumps(packet), encoding="utf-8")
    return path


def _ledger(path: Path) -> Path:
    payload = {
        "schema_version": "customer_request_routing_ledger.v1",
        "generated_utc": "2026-06-20T00:00:00Z",
        "owner_agent_id": "premium-customer-intake-agent-20260620",
        "status": "active_local_ledger",
        "ledger_rule": "route everything",
        "entries": [
            {
                "input_id": "customer-input-followup-test",
                "input_class": "new_request",
                "primary_route": "ai_resources_lab",
                "status": "routed",
                "next_artifact": "ai_resources_lab_followup_packet_or_task",
            }
        ],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_followup_synthesizer_creates_idempotent_lane_tasks(tmp_path: Path) -> None:
    conn = _conn()
    route = _route_packet(tmp_path / "route.json")
    ledger = _ledger(tmp_path / "ledger.json")

    args = Namespace(
        route_packet=str(route),
        output_dir=str(tmp_path / "processed"),
        ledger_json=str(ledger),
        ledger_md=str(tmp_path / "ledger.md"),
        update_feed_json=str(tmp_path / "feed.json"),
        update_feed_md=str(tmp_path / "feed.md"),
        no_db_record=False,
    )
    payload = synthesize_premium_customer_followups(conn, args)
    synthesize_premium_customer_followups(conn, args)

    tasks = [
        dict(row)
        for row in conn.execute(
            """
            SELECT task_id, lane_id, status, owner_agent_id, duplicate_key
            FROM tasks
            WHERE duplicate_key LIKE 'customer-input-followup-test:lane-followup:%'
            ORDER BY lane_id
            """
        )
    ]
    ledger_payload = json.loads(ledger.read_text(encoding="utf-8"))

    assert len(tasks) == 2
    assert {task["lane_id"] for task in tasks} == {"ai_resources_lab", "youtube_content_channels"}
    assert all(task["status"] == "new" for task in tasks)
    assert all(task["owner_agent_id"] for task in tasks)
    assert payload["primary_route"] == "ai_resources_lab"
    assert ledger_payload["entries"][0]["status"] == "synthesized"


def test_followup_synthesizer_report_only_mode_writes_packets(tmp_path: Path) -> None:
    route = _route_packet(tmp_path / "route.json")
    payload = synthesize_premium_customer_followups(
        None,
        Namespace(
            route_packet=str(route),
            output_dir=str(tmp_path / "processed"),
            ledger_json=str(tmp_path / "ledger.json"),
            ledger_md=str(tmp_path / "ledger.md"),
            update_feed_json=str(tmp_path / "feed.json"),
            update_feed_md=str(tmp_path / "feed.md"),
            no_db_record=True,
        ),
    )

    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False
    assert len(payload["followup_tasks"]) == 2
