import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.account_capacity_dispatch_plan import (  # noqa: E402
    build_account_capacity_dispatch_plan,
)
from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('department_manager', 'manager', '[]', '[]', '2026-06-21T15:00:00Z', '2026-06-21T15:00:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('lane-owner', 'department_manager', 'codex-thread:owner-thread', 'ai_resources', 'active', '[]', '2026-06-21T15:00:00Z', '2026-06-21T15:00:00Z')
        """
    )
    for lane_id in ["alpha_lane", "beta_lane", "gamma_lane"]:
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
                   '2026-06-21T15:00:00Z', '2026-06-21T15:00:00Z')
            """,
            (lane_id,),
        )
    for task_id, lane_id, priority, created_at in [
        ("task-low", "alpha_lane", 20, "2026-06-21T15:00:00Z"),
        ("task-high-old", "beta_lane", 90, "2026-06-21T15:01:00Z"),
        ("task-high-new", "gamma_lane", 90, "2026-06-21T15:02:00Z"),
    ]:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id,
              duplicate_key, evidence_required, next_action, created_at, updated_at
            )
            VALUES(?, ?, ?, 'new', ?, 'lane-owner', ?, 'evidence', 'dispatch me', ?, ?)
            """,
            (task_id, lane_id, task_id, priority, f"dispatch:{task_id}", created_at, created_at),
        )
    conn.commit()
    return conn


def _snapshot(tmp_path: Path, sessions: list[dict[str, object]]) -> Path:
    path = tmp_path / "capacity-snapshot.json"
    path.write_text(json.dumps({"sessions": sessions}), encoding="utf-8")
    return path


def _args(tmp_path: Path, snapshot_path: Path, max_tasks: int = 10, no_db_record: bool = True) -> Namespace:
    return Namespace(
        capacity_snapshot=str(snapshot_path),
        now_utc="2026-06-21T15:30:00Z",
        max_tasks=max_tasks,
        path=str(tmp_path / "dispatch.md"),
        json_path=str(tmp_path / "dispatch.json"),
        no_db_record=no_db_record,
    )


def test_account_capacity_dispatch_plan_recommends_priority_tasks_without_mutating_leases(
    tmp_path: Path,
) -> None:
    conn = _conn()
    snapshot_path = _snapshot(
        tmp_path,
        [
            {
                "session_id": "codex-main",
                "surface": "codex",
                "account_label": "main",
                "status": "available",
                "concurrency_limit": 2,
                "active_lease_count": 0,
                "last_refresh_utc": "2026-06-21T15:29:00Z",
            },
            {
                "session_id": "codex-cooling",
                "surface": "codex",
                "account_label": "cooling",
                "status": "cooling_down",
                "concurrency_limit": 4,
                "active_lease_count": 0,
                "resume_after_utc": "2026-06-21T16:00:00Z",
            },
        ],
    )

    payload = build_account_capacity_dispatch_plan(conn, _args(tmp_path, snapshot_path))

    assert payload["status"] == "ready_to_dispatch"
    assert payload["counts"]["available_capacity"] == 2
    assert [item["task_id"] for item in payload["dispatch_recommendations"]] == [
        "task-high-old",
        "task-high-new",
    ]
    assert {item["session_id"] for item in payload["dispatch_recommendations"]} == {"codex-main"}
    assert payload["zero_side_effect_boundary"]["task_leases_mutated"] == 0

    task_rows = conn.execute("SELECT task_id, lease_owner_agent_id FROM tasks ORDER BY task_id").fetchall()
    assert all(row["lease_owner_agent_id"] is None for row in task_rows)
    session = conn.execute(
        "SELECT status, concurrency_limit, active_lease_count FROM account_capacity_sessions WHERE session_id='codex-main'"
    ).fetchone()
    assert dict(session) == {"status": "available", "concurrency_limit": 2, "active_lease_count": 0}


def test_account_capacity_dispatch_plan_waits_for_cooling_capacity(tmp_path: Path) -> None:
    conn = _conn()
    snapshot_path = _snapshot(
        tmp_path,
        [
            {
                "session_id": "codex-cooling-a",
                "surface": "codex",
                "status": "cooling_down",
                "concurrency_limit": 3,
                "active_lease_count": 0,
                "resume_after_utc": "2026-06-21T15:45:00Z",
            },
            {
                "session_id": "codex-cooling-b",
                "surface": "codex",
                "status": "cooling_down",
                "concurrency_limit": 2,
                "active_lease_count": 0,
                "resume_after_utc": "2026-06-21T16:10:00Z",
            },
        ],
    )

    payload = build_account_capacity_dispatch_plan(conn, _args(tmp_path, snapshot_path))

    assert payload["status"] == "waiting_for_capacity"
    assert payload["counts"]["available_capacity"] == 0
    assert payload["dispatch_recommendations"] == []
    assert payload["next_wakeup_utc"] == "2026-06-21T15:45:00Z"
    assert payload["next_action"].startswith("Wait for session refresh")


def test_account_capacity_dispatch_plan_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-account-capacity-dispatch-plan",
            "--capacity-snapshot",
            "capacity.json",
            "--max-tasks",
            "3",
        ]
    )

    assert args.cmd == "write-account-capacity-dispatch-plan"
    assert args.capacity_snapshot == "capacity.json"
    assert args.max_tasks == 3
