import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.lane_runtime_dispatch_drain import (  # noqa: E402
    drain_lane_runtime_dispatch_plan,
)
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('department_manager', 'manager', '[]', '[]', '2026-06-21T16:00:00Z', '2026-06-21T16:00:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('lane-owner', 'department_manager', 'codex-thread:owner-thread', 'ai_resources', 'active', '[]', '2026-06-21T16:00:00Z', '2026-06-21T16:00:00Z')
        """
    )
    for lane_id in ["premium_customer_intake", "youtube_content_channels"]:
        conn.execute(
            """
            INSERT INTO lanes(
              lane_id, department, status, owner_agent_id, owner_thread_id,
              agent_types_json, examples_json, promotion_gates_json,
              service_workers_required_json, side_effects_json, global_gates_json,
              created_at, updated_at
            )
            VALUES(?, 'Test', 'active', 'lane-owner', 'codex-thread:owner-thread',
                   '[]', '[]', '[]', '[]', '[]', '[]',
                   '2026-06-21T16:00:00Z', '2026-06-21T16:00:00Z')
            """,
            (lane_id,),
        )
    for task_id, lane_id, priority in [
        ("task-premium", "premium_customer_intake", 95),
        ("task-youtube", "youtube_content_channels", 90),
    ]:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id,
              duplicate_key, evidence_required, next_action, created_at, updated_at
            )
            VALUES(?, ?, ?, 'new', ?, 'lane-owner', ?, 'evidence', 'do local work', '2026-06-21T16:00:00Z', '2026-06-21T16:00:00Z')
            """,
            (task_id, lane_id, task_id, priority, f"drain:{task_id}"),
        )
    conn.commit()
    return conn


def _insert_capacity_session(
    conn: sqlite3.Connection,
    session_id: str = "codex-main",
    status: str = "available",
    concurrency_limit: int = 2,
    active_lease_count: int = 0,
) -> None:
    conn.execute(
        """
        INSERT INTO account_capacity_sessions(
          session_id, surface, account_label, status, concurrency_limit,
          active_lease_count, created_at, updated_at
        )
        VALUES(?, 'codex', ?, ?, ?, ?, '2026-06-21T16:00:00Z', '2026-06-21T16:00:00Z')
        """,
        (session_id, session_id, status, concurrency_limit, active_lease_count),
    )
    conn.commit()


def _activation_plan(tmp_path: Path, recommendations: list[dict[str, object]]) -> Path:
    path = tmp_path / "activation-plan.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": "lane_runtime_activation_plan.v1",
                "generated_utc": "2026-06-21T16:00:00Z",
                "status": "dispatch_recommended" if recommendations else "monitoring",
                "dispatch_recommendations": recommendations,
            }
        ),
        encoding="utf-8",
    )
    return path


def _recommendation(task_id: str, lane_id: str, session_id: str = "codex-main") -> dict[str, object]:
    return {
        "session_id": session_id,
        "lane_id": lane_id,
        "runtime_mode": "always_on",
        "task_id": task_id,
        "priority": 95,
        "owner_agent_id": "lane-owner",
        "owner_thread_id": "codex-thread:owner-thread",
        "evidence_required": "evidence",
        "next_action": "do local work",
        "recommended_action": "lease_then_dispatch_with_runtime_and_capacity_guard",
    }


def _args(
    tmp_path: Path,
    activation_plan: Path,
    dry_run: bool = False,
    no_db_record: bool = False,
) -> Namespace:
    return Namespace(
        activation_plan=str(activation_plan),
        now_utc="2026-06-21T16:05:00Z",
        lease_minutes=120,
        executor_agent_id="runtime-dispatch-drain-executor",
        max_dispatches=10,
        packet_dir=str(tmp_path / "packets"),
        path=str(tmp_path / "drain.md"),
        json_path=str(tmp_path / "drain.json"),
        dry_run=dry_run,
        no_db_record=no_db_record,
    )


def test_lane_runtime_dispatch_drain_leases_recommended_tasks_and_increments_capacity(
    tmp_path: Path,
) -> None:
    conn = _conn()
    _insert_capacity_session(conn, concurrency_limit=2, active_lease_count=0)
    activation_plan = _activation_plan(
        tmp_path,
        [
            _recommendation("task-premium", "premium_customer_intake"),
            _recommendation("task-youtube", "youtube_content_channels"),
        ],
    )

    payload = drain_lane_runtime_dispatch_plan(conn, _args(tmp_path, activation_plan))

    assert payload["status"] == "dispatch_packets_ready"
    assert payload["counts"]["leased_dispatches"] == 2
    assert payload["counts"]["skipped_dispatches"] == 0
    assert payload["zero_side_effect_boundary"]["task_leases_mutated"] == 2
    assert payload["zero_side_effect_boundary"]["thread_messages_sent"] == 0

    rows = conn.execute(
        """
        SELECT task_id, status, lease_owner_agent_id, lease_expires_at
        FROM tasks
        WHERE task_id IN ('task-premium', 'task-youtube')
        ORDER BY task_id
        """
    ).fetchall()
    assert [dict(row) for row in rows] == [
        {
            "task_id": "task-premium",
            "status": "in_progress",
            "lease_owner_agent_id": "lane-owner",
            "lease_expires_at": "2026-06-21T18:05:00Z",
        },
        {
            "task_id": "task-youtube",
            "status": "in_progress",
            "lease_owner_agent_id": "lane-owner",
            "lease_expires_at": "2026-06-21T18:05:00Z",
        },
    ]
    session = conn.execute(
        "SELECT active_lease_count FROM account_capacity_sessions WHERE session_id='codex-main'"
    ).fetchone()
    assert session["active_lease_count"] == 2
    assert all(Path(item["packet_path"]).exists() for item in payload["leased_dispatches"])

    audit = conn.execute(
        "SELECT status, evidence_required FROM tasks WHERE task_id='task-lane-runtime-dispatch-drain-v1-20260621'"
    ).fetchone()
    assert dict(audit) == {"status": "complete", "evidence_required": str(tmp_path / "drain.md")}


def test_lane_runtime_dispatch_drain_skips_when_capacity_is_full(tmp_path: Path) -> None:
    conn = _conn()
    _insert_capacity_session(conn, concurrency_limit=1, active_lease_count=1)
    activation_plan = _activation_plan(
        tmp_path,
        [_recommendation("task-premium", "premium_customer_intake")],
    )

    payload = drain_lane_runtime_dispatch_plan(conn, _args(tmp_path, activation_plan, no_db_record=True))

    assert payload["status"] == "no_dispatches_leased"
    assert payload["counts"]["leased_dispatches"] == 0
    assert payload["skipped_dispatches"][0]["reason"] == "capacity_full"
    task = conn.execute(
        "SELECT status, lease_owner_agent_id, lease_expires_at FROM tasks WHERE task_id='task-premium'"
    ).fetchone()
    assert dict(task) == {"status": "new", "lease_owner_agent_id": None, "lease_expires_at": None}
    session = conn.execute(
        "SELECT active_lease_count FROM account_capacity_sessions WHERE session_id='codex-main'"
    ).fetchone()
    assert session["active_lease_count"] == 1


def test_lane_runtime_dispatch_drain_dry_run_writes_packets_without_mutating_leases(
    tmp_path: Path,
) -> None:
    conn = _conn()
    _insert_capacity_session(conn, concurrency_limit=1, active_lease_count=0)
    activation_plan = _activation_plan(
        tmp_path,
        [_recommendation("task-premium", "premium_customer_intake")],
    )

    payload = drain_lane_runtime_dispatch_plan(conn, _args(tmp_path, activation_plan, dry_run=True))

    assert payload["status"] == "dry_run_dispatch_packets_ready"
    assert payload["counts"]["leased_dispatches"] == 1
    assert payload["zero_side_effect_boundary"]["task_leases_mutated"] == 0
    task = conn.execute(
        "SELECT status, lease_owner_agent_id, lease_expires_at FROM tasks WHERE task_id='task-premium'"
    ).fetchone()
    assert dict(task) == {"status": "new", "lease_owner_agent_id": None, "lease_expires_at": None}
    session = conn.execute(
        "SELECT active_lease_count FROM account_capacity_sessions WHERE session_id='codex-main'"
    ).fetchone()
    assert session["active_lease_count"] == 0


def test_lane_runtime_dispatch_drain_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "drain-lane-runtime-dispatch",
            "--activation-plan",
            "activation.json",
            "--lease-minutes",
            "45",
            "--max-dispatches",
            "3",
            "--dry-run",
        ]
    )

    assert args.cmd == "drain-lane-runtime-dispatch"
    assert args.activation_plan == "activation.json"
    assert args.lease_minutes == 45
    assert args.max_dispatches == 3
    assert args.dry_run is True
