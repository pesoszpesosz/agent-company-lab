import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.continuity_watchdog_owner_handoff_packets import (  # noqa: E402
    write_continuity_watchdog_owner_handoff_packets,
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
    for agent_id, thread_id in [
        ("continuity-watchdog-worker-20260621", "codex-thread:watchdog"),
        ("lane-manager-ai_resources_lab-20260620", "codex-thread:ar"),
        ("lane-manager-youtube_content_channels-20260620", "019ec612-d317-71f1-b02f-c85f2295e320"),
        ("premium-customer-intake-agent-20260620", "codex-current-ceo-thread-20260620"),
    ]:
        conn.execute(
            """
            INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
            VALUES(?, 'department_manager', ?, 'ai_resources', 'active', '[]', '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z')
            """,
            (agent_id, thread_id),
        )
    for lane_id, owner_agent_id, owner_thread_id in [
        ("ai_resources_lab", "lane-manager-ai_resources_lab-20260620", "codex-thread:ar"),
        (
            "youtube_content_channels",
            "lane-manager-youtube_content_channels-20260620",
            "019ec612-d317-71f1-b02f-c85f2295e320",
        ),
        ("premium_customer_intake", "premium-customer-intake-agent-20260620", "codex-current-ceo-thread-20260620"),
    ]:
        conn.execute(
            """
            INSERT INTO lanes(
              lane_id, department, status, owner_agent_id, owner_thread_id, agent_types_json,
              examples_json, promotion_gates_json, service_workers_required_json,
              side_effects_json, global_gates_json, created_at, updated_at
            )
            VALUES(?, 'AI Resources', 'active', ?, ?, '[]', '[]', '[]', '[]', '[]', '[]',
                   '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z')
            """,
            (lane_id, owner_agent_id, owner_thread_id),
        )
    for task_id, lane_id, owner, duplicate_key, priority in [
        (
            "task-ownerless",
            "ai_resources_lab",
            "lane-manager-ai_resources_lab-20260620",
            "continuity-owner-response-task:owner_selection_or_park_required:submitted_bounty_payouts",
            96,
        ),
        (
            "task-ack-youtube",
            "youtube_content_channels",
            "lane-manager-youtube_content_channels-20260620",
            "continuity-owner-response-task:acknowledgement_response_required:task-owner-ack-youtube",
            92,
        ),
        (
            "task-goal-premium",
            "premium_customer_intake",
            "premium-customer-intake-agent-20260620",
            "continuity-owner-response-task:lane_goal_response_required:premium_customer_intake",
            86,
        ),
        (
            "task-complete-ignored",
            "ai_resources_lab",
            "lane-manager-ai_resources_lab-20260620",
            "continuity-owner-response-task:lane_goal_response_required:ignored",
            86,
        ),
    ]:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
              evidence_required, next_action, created_at, updated_at
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, 'evidence path', 'write local owner response',
                   '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z')
            """,
            (
                task_id,
                lane_id,
                task_id,
                "complete" if task_id == "task-complete-ignored" else "new",
                priority,
                owner,
                duplicate_key,
            ),
        )
    conn.commit()
    return conn


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        now_utc="2026-06-21T13:00:00Z",
        path=str(tmp_path / "handoffs.md"),
        json_path=str(tmp_path / "handoffs.json"),
        packet_dir=str(tmp_path / "packets"),
        no_db_record=no_db_record,
    )


def test_owner_handoff_packets_group_open_dispatch_tasks_by_owner(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_continuity_watchdog_owner_handoff_packets(conn, _args(tmp_path))

    assert payload["schema_version"] == "continuity_watchdog_owner_handoff_packets.v1"
    assert payload["status"] == "owner_handoff_packets_ready"
    assert payload["counts"]["owner_packets"] == 3
    assert payload["counts"]["open_dispatch_tasks"] == 3
    assert payload["counts"]["owner_selection_or_park_required"] == 1
    assert payload["counts"]["acknowledgement_response_required"] == 1
    assert payload["counts"]["lane_goal_response_required"] == 1
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False

    packets = {packet["owner_agent_id"]: packet for packet in payload["owner_packets"]}
    assert packets["lane-manager-ai_resources_lab-20260620"]["dispatch_mode"] == "send_to_live_codex_thread"
    assert packets["lane-manager-youtube_content_channels-20260620"]["dispatch_mode"] == "send_to_existing_codex_thread"
    assert (
        packets["premium-customer-intake-agent-20260620"]["dispatch_mode"]
        == "route_through_ceo_or_premium_router_placeholder"
    )
    for packet in payload["owner_packets"]:
        assert Path(packet["packet_path"]).exists()
        assert packet["tasks"][0]["acceptance_criteria"]
        assert "no duplicate worker creation" in packet["tasks"][0]["stop_gates"]

    audit = conn.execute("select status,evidence_required from tasks where task_id=?", ("task-continuity-watchdog-owner-handoff-packets-v1-20260621",)).fetchone()
    assert audit["status"] == "complete"
    assert audit["evidence_required"] == payload["md_path"]
    artifact_count = conn.execute(
        "select count(*) as c from artifacts where task_id='task-continuity-watchdog-owner-handoff-packets-v1-20260621'"
    ).fetchone()["c"]
    assert artifact_count == 5


def test_owner_handoff_packets_report_only_skips_db_writes(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_continuity_watchdog_owner_handoff_packets(conn, _args(tmp_path, no_db_record=True))

    assert payload["status"] == "owner_handoff_packets_ready"
    assert conn.execute(
        "select 1 from tasks where task_id='task-continuity-watchdog-owner-handoff-packets-v1-20260621'"
    ).fetchone() is None
    assert conn.execute(
        "select 1 from artifacts where kind='continuity_owner_handoff_packets_markdown'"
    ).fetchone() is None


def test_owner_handoff_packets_clears_stale_generated_packets(tmp_path: Path) -> None:
    conn = _conn()
    packet_dir = tmp_path / "packets"
    packet_dir.mkdir()
    stale_packet = packet_dir / "continuity-owner-handoff-stale-owner.md"
    unrelated_file = packet_dir / "operator-note.md"
    stale_packet.write_text("stale", encoding="utf-8")
    unrelated_file.write_text("keep", encoding="utf-8")

    payload = write_continuity_watchdog_owner_handoff_packets(conn, _args(tmp_path))

    assert payload["status"] == "owner_handoff_packets_ready"
    assert not stale_packet.exists()
    assert unrelated_file.exists()
    indexed_paths = {Path(packet["packet_path"]) for packet in payload["owner_packets"]}
    assert set(packet_dir.glob("continuity-owner-handoff-*.md")) == indexed_paths


def test_owner_handoff_packets_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-continuity-watchdog-owner-handoff-packets",
            "--packet-dir",
            "reports/continuity-owner-handoffs-v1-20260621",
        ]
    )

    assert args.cmd == "write-continuity-watchdog-owner-handoff-packets"
    assert args.packet_dir == "reports/continuity-owner-handoffs-v1-20260621"
