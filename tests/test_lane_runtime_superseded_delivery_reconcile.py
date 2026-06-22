import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.lane_runtime_superseded_delivery_reconcile import (  # noqa: E402
    SUPERSEDED_DELIVERY_STATUS,
    reconcile_superseded_lane_runtime_deliveries,
)
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('department_manager', 'manager', '[]', '[]', '2026-06-22T08:00:00Z', '2026-06-22T08:00:00Z')
        """
    )
    for agent_id, thread_id, department_id in [
        ("owner-agent", "codex-thread:owner-thread", "growth"),
        ("lane-manager-ai_resources_lab-20260620", "codex-thread:ar", "ai_resources"),
    ]:
        conn.execute(
            """
            INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
            VALUES(?, 'department_manager', ?, ?, 'active', '[]', '2026-06-22T08:00:00Z', '2026-06-22T08:00:00Z')
            """,
            (agent_id, thread_id, department_id),
        )
    for lane_id in ["content_and_social_growth", "ai_resources_lab"]:
        conn.execute(
            """
            INSERT INTO lanes(
              lane_id, department, status, owner_agent_id, owner_thread_id,
              agent_types_json, examples_json, promotion_gates_json,
              service_workers_required_json, side_effects_json, global_gates_json,
              created_at, updated_at
            )
            VALUES(?, 'Growth', 'active', 'owner-agent', 'codex-thread:owner-thread',
                   '[]', '[]', '[]', '[]', '[]', '[]',
                   '2026-06-22T08:00:00Z', '2026-06-22T08:00:00Z')
            """,
            (lane_id,),
        )
    for task_id, status, lease_owner, lease_expires_at in [
        ("task-older", "in_progress", "owner-agent", "2026-06-22T10:00:00Z"),
        ("task-newer", "complete", None, None),
    ]:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
              evidence_required, next_action, created_at, updated_at, lease_owner_agent_id, lease_expires_at
            )
            VALUES(?, 'content_and_social_growth', ?, ?, 90, 'owner-agent', ?, 'evidence', 'do local work',
                   '2026-06-22T08:00:00Z', '2026-06-22T08:00:00Z', ?, ?)
            """,
            (task_id, task_id, status, f"superseded-reconcile:{task_id}", lease_owner, lease_expires_at),
        )
    for delivery_id, task_id, delivered_at in [
        ("delivery-older", "task-older", "2026-06-22T08:05:00Z"),
        ("delivery-newer", "task-newer", "2026-06-22T08:10:00Z"),
    ]:
        conn.execute(
            """
            INSERT INTO lane_runtime_thread_deliveries(
              delivery_id, task_id, lane_id, session_id, owner_agent_id, owner_thread_id,
              packet_path, prompt_path, status, delivery_attempts, delivered_at, last_error,
              created_at, updated_at
            )
            VALUES(?, ?, 'content_and_social_growth', 'codex-main', 'owner-agent', 'codex-thread:owner-thread',
                   'packet.md', 'prompt.md', 'delivered', 1, ?, NULL,
                   '2026-06-22T08:00:00Z', ?)
            """,
            (delivery_id, task_id, delivered_at, delivered_at),
        )
    conn.commit()
    return conn


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        now_utc="2026-06-22T08:30:00Z",
        path=str(tmp_path / "superseded.md"),
        json_path=str(tmp_path / "superseded.json"),
        no_db_record=no_db_record,
    )


def test_superseded_delivery_reconcile_parks_older_delivered_task(tmp_path: Path) -> None:
    conn = _conn()

    payload = reconcile_superseded_lane_runtime_deliveries(conn, _args(tmp_path, no_db_record=False))

    assert payload["status"] == "superseded_deliveries_parked"
    assert payload["counts"] == {
        "superseded_deliveries_seen": 1,
        "deliveries_parked": 1,
        "tasks_requeued": 1,
        "task_leases_released": 1,
    }
    older_delivery = conn.execute(
        "SELECT status, last_error FROM lane_runtime_thread_deliveries WHERE delivery_id='delivery-older'"
    ).fetchone()
    newer_delivery = conn.execute(
        "SELECT status FROM lane_runtime_thread_deliveries WHERE delivery_id='delivery-newer'"
    ).fetchone()
    older_task = conn.execute(
        "SELECT status, lease_owner_agent_id, lease_expires_at FROM tasks WHERE task_id='task-older'"
    ).fetchone()

    assert older_delivery["status"] == SUPERSEDED_DELIVERY_STATUS
    assert "superseded by newer delivered thread delivery delivery-newer" in older_delivery["last_error"]
    assert newer_delivery["status"] == "delivered"
    assert dict(older_task) == {"status": "new", "lease_owner_agent_id": None, "lease_expires_at": None}
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()


def test_superseded_delivery_reconcile_report_only_does_not_mutate(tmp_path: Path) -> None:
    conn = _conn()

    payload = reconcile_superseded_lane_runtime_deliveries(conn, _args(tmp_path, no_db_record=True))

    delivery = conn.execute(
        "SELECT status FROM lane_runtime_thread_deliveries WHERE delivery_id='delivery-older'"
    ).fetchone()
    assert payload["status"] == "superseded_deliveries_parked"
    assert payload["zero_side_effect_boundary"]["delivery_status_mutations"] == 0
    assert delivery["status"] == "delivered"


def test_superseded_delivery_reconcile_cli_parser_supports_command() -> None:
    args = build_parser().parse_args(
        ["reconcile-superseded-lane-runtime-deliveries", "--now-utc", "2026-06-22T08:30:00Z"]
    )

    assert args.cmd == "reconcile-superseded-lane-runtime-deliveries"
    assert args.now_utc == "2026-06-22T08:30:00Z"
