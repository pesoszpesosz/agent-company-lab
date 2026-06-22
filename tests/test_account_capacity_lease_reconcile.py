import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.account_capacity_lease_reconcile import (  # noqa: E402
    reconcile_account_capacity_leases,
)
from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.schema import init_db  # noqa: E402


def _conn(task_status: str = "complete", lease_owner: str | None = None, lease_expires_at: str | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('department_manager', 'manager', '[]', '[]', '2026-06-21T16:40:00Z', '2026-06-21T16:40:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('owner-agent', 'department_manager', 'codex-thread:owner-thread', 'customer_success', 'active', '[]', '2026-06-21T16:40:00Z', '2026-06-21T16:40:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('lane-manager-ai_resources_lab-20260620', 'department_manager', 'codex-thread:ar', 'ai_resources', 'active', '[]', '2026-06-21T16:40:00Z', '2026-06-21T16:40:00Z')
        """
    )
    for lane_id in ["premium_customer_intake", "ai_resources_lab"]:
        conn.execute(
            """
            INSERT INTO lanes(
              lane_id, department, status, owner_agent_id, owner_thread_id,
              agent_types_json, examples_json, promotion_gates_json,
              service_workers_required_json, side_effects_json, global_gates_json,
              created_at, updated_at
            )
            VALUES(?, 'Test', 'active', 'owner-agent', 'codex-thread:owner-thread',
                   '[]', '[]', '[]', '[]', '[]', '[]',
                   '2026-06-21T16:40:00Z', '2026-06-21T16:40:00Z')
            """,
            (lane_id,),
        )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id,
          duplicate_key, evidence_required, next_action, created_at, updated_at,
          lease_owner_agent_id, lease_expires_at
        )
        VALUES('task-premium', 'premium_customer_intake', 'Task premium', ?, 95, 'owner-agent',
               'reconcile:task-premium', 'evidence', 'do the local work',
               '2026-06-21T16:40:00Z', '2026-06-21T16:40:00Z',
               ?, ?)
        """,
        (task_status, lease_owner, lease_expires_at),
    )
    conn.execute(
        """
        INSERT INTO account_capacity_sessions(
          session_id, surface, account_label, status, concurrency_limit,
          active_lease_count, created_at, updated_at
        )
        VALUES('codex-main', 'codex', 'main', 'available', 1, 1, '2026-06-21T16:40:00Z', '2026-06-21T16:40:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO account_capacity_sessions(
          session_id, surface, account_label, status, concurrency_limit,
          active_lease_count, created_at, updated_at
        )
        VALUES('unrelated-session', 'codex', 'other', 'available', 3, 2, '2026-06-21T16:40:00Z', '2026-06-21T16:40:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO lane_runtime_thread_deliveries(
          delivery_id, task_id, lane_id, session_id, owner_agent_id, owner_thread_id,
          packet_path, prompt_path, status, delivery_attempts, delivered_at,
          created_at, updated_at
        )
        VALUES('delivery-task-premium', 'task-premium', 'premium_customer_intake', 'codex-main',
               'owner-agent', 'codex-thread:owner-thread', 'packet.md', 'prompt.md',
               'delivered', 1, '2026-06-21T16:45:00Z',
               '2026-06-21T16:40:00Z', '2026-06-21T16:45:00Z')
        """
    )
    conn.commit()
    return conn


def _args(tmp_path: Path, no_db_record: bool = True) -> Namespace:
    return Namespace(
        now_utc="2026-06-21T16:50:00Z",
        path=str(tmp_path / "reconcile.md"),
        json_path=str(tmp_path / "reconcile.json"),
        no_db_record=no_db_record,
    )


def test_account_capacity_lease_reconcile_releases_capacity_for_completed_delivered_task(tmp_path: Path) -> None:
    conn = _conn(task_status="complete", lease_owner=None, lease_expires_at=None)

    payload = reconcile_account_capacity_leases(conn, _args(tmp_path, no_db_record=False))

    assert payload["status"] == "capacity_released"
    assert payload["counts"]["sessions_reconciled"] == 1
    assert payload["counts"]["capacity_released"] == 1
    session = conn.execute(
        "SELECT active_lease_count FROM account_capacity_sessions WHERE session_id='codex-main'"
    ).fetchone()
    assert session["active_lease_count"] == 0
    unrelated = conn.execute(
        "SELECT active_lease_count FROM account_capacity_sessions WHERE session_id='unrelated-session'"
    ).fetchone()
    assert unrelated["active_lease_count"] == 2
    audit = conn.execute(
        "SELECT status, evidence_required FROM tasks WHERE task_id='task-account-capacity-lease-reconcile-v1-20260621'"
    ).fetchone()
    assert dict(audit) == {"status": "complete", "evidence_required": str(tmp_path / "reconcile.md")}


def test_account_capacity_lease_reconcile_clears_terminal_task_lease_fields(tmp_path: Path) -> None:
    conn = _conn(
        task_status="complete",
        lease_owner="owner-agent",
        lease_expires_at="2026-06-21T18:50:00Z",
    )

    payload = reconcile_account_capacity_leases(conn, _args(tmp_path, no_db_record=False))

    assert payload["status"] == "capacity_released"
    assert payload["counts"]["terminal_task_leases_cleared"] == 1
    assert payload["terminal_task_leases_cleared"][0]["task_id"] == "task-premium"
    task = conn.execute(
        "SELECT lease_owner_agent_id, lease_expires_at FROM tasks WHERE task_id='task-premium'"
    ).fetchone()
    assert dict(task) == {"lease_owner_agent_id": None, "lease_expires_at": None}


def test_account_capacity_lease_reconcile_report_only_keeps_terminal_task_lease_fields(
    tmp_path: Path,
) -> None:
    conn = _conn(
        task_status="complete",
        lease_owner="owner-agent",
        lease_expires_at="2026-06-21T18:50:00Z",
    )

    payload = reconcile_account_capacity_leases(conn, _args(tmp_path, no_db_record=True))

    assert payload["counts"]["terminal_task_leases_cleared"] == 1
    assert payload["zero_side_effect_boundary"]["task_lease_fields_cleared"] == 0
    task = conn.execute(
        "SELECT lease_owner_agent_id, lease_expires_at FROM tasks WHERE task_id='task-premium'"
    ).fetchone()
    assert dict(task) == {
        "lease_owner_agent_id": "owner-agent",
        "lease_expires_at": "2026-06-21T18:50:00Z",
    }


def test_account_capacity_lease_reconcile_keeps_active_unexpired_lease(tmp_path: Path) -> None:
    conn = _conn(
        task_status="in_progress",
        lease_owner="owner-agent",
        lease_expires_at="2026-06-21T18:50:00Z",
    )

    payload = reconcile_account_capacity_leases(conn, _args(tmp_path))

    assert payload["status"] == "already_consistent"
    assert payload["counts"]["capacity_released"] == 0
    session = conn.execute(
        "SELECT active_lease_count FROM account_capacity_sessions WHERE session_id='codex-main'"
    ).fetchone()
    assert session["active_lease_count"] == 1


def test_account_capacity_lease_reconcile_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(["reconcile-account-capacity-leases", "--now-utc", "2026-06-21T16:50:00Z"])

    assert args.cmd == "reconcile-account-capacity-leases"
    assert args.now_utc == "2026-06-21T16:50:00Z"
