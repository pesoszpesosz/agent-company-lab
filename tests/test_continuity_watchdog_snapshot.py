import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.continuity_watchdog_snapshot import write_continuity_watchdog_snapshot_bundle  # noqa: E402
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
        ("healthy-owner", "thread-healthy"),
        ("missing-thread-owner", None),
        ("continuity-watchdog-worker-20260621", "thread-watchdog"),
    ]:
        conn.execute(
            """
            INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, notes, created_at, updated_at)
            VALUES(?, 'department_manager', ?, 'ai_resources', 'active', '[]', null, '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z')
            """,
            (agent_id, thread_id),
        )
    for lane_id, owner_agent_id in [
        ("ownerless_lane", None),
        ("missing_agent_lane", "missing-agent"),
        ("missing_thread_lane", "missing-thread-owner"),
        ("healthy_lane", "healthy-owner"),
    ]:
        conn.execute(
            """
            INSERT INTO lanes(
              lane_id, department, status, owner_agent_id, owner_thread_id, agent_types_json,
              examples_json, promotion_gates_json, service_workers_required_json,
              side_effects_json, global_gates_json, notes, created_at, updated_at
            )
            VALUES(?, 'Test', 'active', ?, null, '[]', '[]', '[]', '[]', '[]', '[]', null, '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z')
            """,
            (lane_id, owner_agent_id),
        )
    for task_id, lane_id, status, owner, duplicate_key, updated_at, lease_expires_at in [
        ("task-healthy", "healthy_lane", "in_progress", "healthy-owner", "healthy:goal", "2026-06-21T10:55:00Z", None),
        ("task-stale", "healthy_lane", "new", "healthy-owner", "stale:goal", "2026-06-21T08:00:00Z", None),
        ("task-expired", "healthy_lane", "in_progress", "healthy-owner", "expired:lease", "2026-06-21T10:00:00Z", "2026-06-21T10:30:00Z"),
        ("task-open-a", "healthy_lane", "new", "healthy-owner", "open:a", "2026-06-21T10:00:00Z", None),
        ("task-open-b", "missing_thread_lane", "new", "missing-thread-owner", "open:b", "2026-06-21T10:00:00Z", None),
        ("task-stale-ack", "healthy_lane", "new", "healthy-owner", "input:owner-acknowledgement:healthy_lane", "2026-06-21T08:30:00Z", None),
    ]:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
              evidence_required, next_action, created_at, updated_at, lease_expires_at
            )
            VALUES(?, ?, ?, ?, 90, ?, ?, 'evidence', 'next', '2026-06-21T08:00:00Z', ?, ?)
            """,
            (task_id, lane_id, task_id, status, owner, duplicate_key, updated_at, lease_expires_at),
        )
    conn.commit()
    return conn


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        now_utc="2026-06-21T11:00:00Z",
        stale_after_minutes=60,
        cadence_minutes=15,
        path=str(tmp_path / "watchdog.md"),
        json_path=str(tmp_path / "watchdog.json"),
        no_db_record=no_db_record,
    )


def test_continuity_watchdog_snapshot_detects_restore_actions_without_mutating_sources(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_continuity_watchdog_snapshot_bundle(conn, _args(tmp_path))

    assert payload["schema_version"] == "continuity_watchdog_snapshot.v1"
    assert payload["status"] == "restore_ready"
    assert payload["counts"]["ownerless_active_lanes"] == 1
    assert payload["counts"]["missing_owner_agent_lanes"] == 1
    assert payload["counts"]["agents_missing_threads"] == 1
    assert payload["counts"]["duplicate_active_keys"] == 0
    assert payload["counts"]["expired_leases"] == 1
    assert payload["counts"]["stale_owner_acknowledgements"] == 1
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()

    action_kinds = {item["kind"] for item in payload["restore_actions"]}
    assert "repair_ownerless_lane" in action_kinds
    assert "repair_missing_owner_agent" in action_kinds
    assert "attach_agent_thread" in action_kinds
    assert "release_or_reclaim_expired_lease" in action_kinds
    assert "resolve_duplicate_active_key" not in action_kinds
    assert "dispatch_stale_owner_acknowledgement" in action_kinds

    statuses = {
        row["task_id"]: row["status"]
        for row in conn.execute("select task_id,status from tasks where task_id like 'task-%'")
    }
    assert statuses["task-stale-ack"] == "new"
    audit = conn.execute(
        "select status,evidence_required from tasks where task_id='task-continuity-watchdog-snapshot-v1-20260621'"
    ).fetchone()
    assert audit["status"] == "complete"
    assert audit["evidence_required"] == payload["md_path"]


def test_continuity_watchdog_snapshot_report_only_skips_db_record(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_continuity_watchdog_snapshot_bundle(conn, _args(tmp_path, no_db_record=True))

    assert payload["status"] == "restore_ready"
    assert conn.execute("select 1 from tasks where task_id='task-continuity-watchdog-snapshot-v1-20260621'").fetchone() is None


def test_continuity_watchdog_snapshot_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-continuity-watchdog-snapshot",
            "--stale-after-minutes",
            "30",
            "--cadence-minutes",
            "5",
        ]
    )

    assert args.cmd == "write-continuity-watchdog-snapshot"
    assert args.stale_after_minutes == 30
    assert args.cadence_minutes == 5
