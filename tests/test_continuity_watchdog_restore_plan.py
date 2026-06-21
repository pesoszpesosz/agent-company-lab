import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.continuity_watchdog_restore_plan import (  # noqa: E402
    write_continuity_watchdog_restore_plan_bundle,
)
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('department_manager', 'manager', '[]', '[]', '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES(
          'continuity-watchdog-worker-20260621', 'department_manager', 'thread-watchdog',
          'ai_resources', 'active', '[]', '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z'
        )
        """
    )
    conn.execute(
        """
        INSERT INTO lanes(
          lane_id, department, status, owner_agent_id, owner_thread_id, agent_types_json,
          examples_json, promotion_gates_json, service_workers_required_json,
          side_effects_json, global_gates_json, created_at, updated_at
        )
        VALUES(
          'ai_resources_lab', 'AI Resources', 'active', 'continuity-watchdog-worker-20260621',
          'thread-watchdog', '[]', '[]', '[]', '[]', '[]', '[]',
          '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z'
        )
        """
    )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at
        )
        VALUES(
          'task-owner-ack-youtube', 'ai_resources_lab', 'ack youtube', 'new', 90,
          'lane-manager-youtube_content_channels-20260620',
          'customer-input-test:owner-acknowledgement:youtube_content_channels',
          'ack packet', 'write local acknowledgement',
          '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z'
        )
        """
    )
    conn.commit()
    return conn


def _snapshot(path: Path) -> Path:
    payload = {
        "schema_version": "continuity_watchdog_snapshot.v1",
        "generated_utc": "2026-06-21T11:00:00Z",
        "status": "restore_ready",
        "counts": {
            "ownerless_active_lanes": 1,
            "stale_owner_acknowledgements": 1,
            "lanes_without_open_tasks": 1,
        },
        "findings": {
            "ownerless_active_lanes": [
                {
                    "lane_id": "submitted_bounty_payouts",
                    "department": "Revenue Collection",
                    "owner_agent_id": None,
                    "owner_thread_id": "old thread note",
                    "status": "active",
                    "updated_at": "2026-06-20T17:05:52Z",
                }
            ],
            "stale_owner_acknowledgements": [
                {
                    "task_id": "task-owner-ack-youtube",
                    "lane_id": "youtube_content_channels",
                    "owner_agent_id": "lane-manager-youtube_content_channels-20260620",
                    "duplicate_key": "customer-input-test:owner-acknowledgement:youtube_content_channels",
                    "status": "new",
                    "age_minutes": 120,
                    "next_action": "Write one local acknowledgement artifact.",
                }
            ],
            "lanes_without_open_tasks": [
                {
                    "lane_id": "content_and_social_growth",
                    "owner_agent_id": "lane-manager-content_and_social_growth-019ec613",
                    "status": "active",
                }
            ],
        },
        "restore_actions": [
            {
                "kind": "repair_ownerless_lane",
                "lane_id": "submitted_bounty_payouts",
                "next_action": "Route to AI Resources for owner selection.",
            },
            {
                "kind": "dispatch_stale_owner_acknowledgement",
                "lane_id": "youtube_content_channels",
                "task_id": "task-owner-ack-youtube",
                "next_action": "Use the owner-acknowledgement dispatch packet.",
            },
            {
                "kind": "request_lane_goal",
                "lane_id": "content_and_social_growth",
                "next_action": "Ask lane owner for one current goal artifact.",
            },
        ],
        "zero_side_effect_boundary": {"external_side_effects": False},
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        snapshot_report=str(_snapshot(tmp_path / "snapshot.json")),
        now_utc="2026-06-21T11:15:00Z",
        json_path=str(tmp_path / "restore-plan.json"),
        path=str(tmp_path / "restore-plan.md"),
        packet_dir=str(tmp_path / "packets"),
        no_db_record=no_db_record,
    )


def test_continuity_watchdog_restore_plan_writes_local_packets_without_mutating_sources(tmp_path: Path) -> None:
    conn = _conn()
    packet_dir = tmp_path / "packets"
    packet_dir.mkdir()
    stale_packet = packet_dir / "continuity-restore-v1-999-stale.md"
    stale_packet.write_text("stale", encoding="utf-8")
    unrelated = packet_dir / "operator-note.txt"
    unrelated.write_text("keep", encoding="utf-8")

    payload = write_continuity_watchdog_restore_plan_bundle(conn, _args(tmp_path))

    assert payload["schema_version"] == "continuity_watchdog_restore_plan.v1"
    assert payload["status"] == "restore_plan_ready"
    assert payload["counts"] == {
        "restore_packets": 3,
        "repair_ownerless_lane": 1,
        "dispatch_stale_owner_acknowledgement": 1,
        "request_lane_goal": 1,
        "manual_restore_review": 0,
    }
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()

    packets = {packet["kind"]: packet for packet in payload["restore_packets"]}
    assert packets["repair_ownerless_lane"]["assigned_surface"] == "ai_resources_lab"
    assert packets["repair_ownerless_lane"]["recommended_owner_agent_id"] == "lane-manager-ai_resources_lab-20260620"
    assert packets["repair_ownerless_lane"]["prohibited_actions"] == [
        "mutate_source_snapshot",
        "create_duplicate_agent_without_overlap_review",
        "start_worker_or_thread_without_explicit_ceo_scope",
        "publish_submit_trade_spend_or_call_external_api",
    ]
    assert packets["dispatch_stale_owner_acknowledgement"]["input_id"] == "customer-input-test"
    assert packets["dispatch_stale_owner_acknowledgement"]["recommended_owner_agent_id"] == (
        "lane-manager-youtube_content_channels-20260620"
    )
    assert packets["request_lane_goal"]["recommended_owner_agent_id"] == "lane-manager-content_and_social_growth-019ec613"

    for packet in packets.values():
        assert Path(packet["packet_json_path"]).exists()
        assert Path(packet["packet_md_path"]).exists()
    assert not stale_packet.exists()
    assert unrelated.exists()
    assert len(list(packet_dir.glob("continuity-restore-v1-*.md"))) == 3

    source = conn.execute("select status from tasks where task_id='task-owner-ack-youtube'").fetchone()
    assert source["status"] == "new"
    audit = conn.execute(
        "select lane_id,status,evidence_required from tasks where task_id='task-continuity-watchdog-restore-plan-v1-20260621'"
    ).fetchone()
    assert audit["lane_id"] == "ai_resources_lab"
    assert audit["status"] == "complete"
    assert audit["evidence_required"] == payload["md_path"]


def test_continuity_watchdog_restore_plan_report_only_skips_db_record(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_continuity_watchdog_restore_plan_bundle(conn, _args(tmp_path, no_db_record=True))

    assert payload["status"] == "restore_plan_ready"
    assert conn.execute(
        "select 1 from tasks where task_id='task-continuity-watchdog-restore-plan-v1-20260621'"
    ).fetchone() is None


def test_continuity_watchdog_restore_plan_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-continuity-watchdog-restore-plan",
            "--snapshot-report",
            "reports/continuity-watchdog-snapshot-v1-20260621.json",
        ]
    )

    assert args.cmd == "write-continuity-watchdog-restore-plan"
    assert args.snapshot_report == "reports/continuity-watchdog-snapshot-v1-20260621.json"
