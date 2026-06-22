import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.lane_runtime_activation_plan import (  # noqa: E402
    build_lane_runtime_activation_plan,
)
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('department_manager', 'manager', '[]', '[]', '2026-06-21T15:40:00Z', '2026-06-21T15:40:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('lane-owner', 'department_manager', 'codex-thread:owner-thread', 'ai_resources', 'active', '[]', '2026-06-21T15:40:00Z', '2026-06-21T15:40:00Z')
        """
    )
    for lane_id in ["always_lane", "demand_lane", "parked_lane", "idle_demand_lane"]:
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
                   '2026-06-21T15:40:00Z', '2026-06-21T15:40:00Z')
            """,
            (lane_id,),
        )
    for task_id, lane_id, priority, created_at in [
        ("task-always", "always_lane", 95, "2026-06-21T15:41:00Z"),
        ("task-demand", "demand_lane", 90, "2026-06-21T15:42:00Z"),
        ("task-parked", "parked_lane", 99, "2026-06-21T15:43:00Z"),
    ]:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id,
              duplicate_key, evidence_required, next_action, created_at, updated_at
            )
            VALUES(?, ?, ?, 'new', ?, 'lane-owner', ?, 'evidence', 'dispatch me', ?, ?)
            """,
            (task_id, lane_id, task_id, priority, f"runtime:{task_id}", created_at, created_at),
        )
    conn.commit()
    return conn


def _policy_snapshot(tmp_path: Path, policies: list[dict[str, object]]) -> Path:
    path = tmp_path / "lane-runtime-policies.json"
    path.write_text(json.dumps({"policies": policies}), encoding="utf-8")
    return path


def _args(tmp_path: Path, snapshot_path: Path, max_lanes: int = 20, no_db_record: bool = True) -> Namespace:
    return Namespace(
        policy_snapshot=str(snapshot_path),
        runtime_supervisor_status=None,
        now_utc="2026-06-21T15:45:00Z",
        max_lanes=max_lanes,
        path=str(tmp_path / "lane-runtime.md"),
        json_path=str(tmp_path / "lane-runtime.json"),
        no_db_record=no_db_record,
    )


def _insert_capacity_session(
    conn: sqlite3.Connection,
    session_id: str,
    status: str,
    concurrency_limit: int,
    active_lease_count: int = 0,
    resume_after_utc: str | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO account_capacity_sessions(
          session_id, surface, account_label, status, concurrency_limit,
          active_lease_count, resume_after_utc, created_at, updated_at
        )
        VALUES(?, 'codex', ?, ?, ?, ?, ?, '2026-06-21T15:40:00Z', '2026-06-21T15:40:00Z')
        """,
        (session_id, session_id, status, concurrency_limit, active_lease_count, resume_after_utc),
    )
    conn.commit()


def test_lane_runtime_activation_plan_recommends_allowed_lanes_without_mutating_leases(
    tmp_path: Path,
) -> None:
    conn = _conn()
    _insert_capacity_session(conn, "codex-main", "available", concurrency_limit=2)
    snapshot_path = _policy_snapshot(
        tmp_path,
        [
            {
                "lane_id": "always_lane",
                "runtime_mode": "always_on",
                "cadence_minutes": 15,
                "max_parallel_tasks": 1,
                "capacity_class": "codex",
                "activation_triggers": ["continuity_tick"],
            },
            {
                "lane_id": "demand_lane",
                "runtime_mode": "on_demand",
                "max_parallel_tasks": 1,
                "capacity_class": "codex",
                "activation_triggers": ["customer_material"],
            },
            {
                "lane_id": "parked_lane",
                "runtime_mode": "parked",
                "max_parallel_tasks": 1,
                "capacity_class": "codex",
                "park_conditions": ["external_owned_readonly"],
            },
            {
                "lane_id": "idle_demand_lane",
                "runtime_mode": "on_demand",
                "max_parallel_tasks": 1,
                "capacity_class": "codex",
                "activation_triggers": ["customer_material"],
            },
        ],
    )

    payload = build_lane_runtime_activation_plan(conn, _args(tmp_path, snapshot_path))

    assert payload["status"] == "dispatch_recommended"
    assert payload["counts"]["policies_seen"] == 4
    assert payload["counts"]["available_capacity"] == 2
    assert [item["task_id"] for item in payload["dispatch_recommendations"]] == [
        "task-always",
        "task-demand",
    ]
    assert {item["lane_id"] for item in payload["dispatch_recommendations"]} == {
        "always_lane",
        "demand_lane",
    }
    lane_actions = {item["lane_id"]: item["recommended_action"] for item in payload["lane_activation_states"]}
    assert lane_actions["parked_lane"] == "parked_no_dispatch"
    assert lane_actions["idle_demand_lane"] == "monitor_for_trigger"
    assert payload["zero_side_effect_boundary"]["task_leases_mutated"] == 0

    task_rows = conn.execute("SELECT task_id, lease_owner_agent_id FROM tasks ORDER BY task_id").fetchall()
    assert all(row["lease_owner_agent_id"] is None for row in task_rows)
    policy = conn.execute(
        "SELECT runtime_mode, max_parallel_tasks FROM lane_runtime_policies WHERE lane_id='always_lane'"
    ).fetchone()
    assert dict(policy) == {"runtime_mode": "always_on", "max_parallel_tasks": 1}


def test_lane_runtime_activation_plan_marks_eligible_work_pending_capacity(tmp_path: Path) -> None:
    conn = _conn()
    _insert_capacity_session(
        conn,
        "codex-cooling",
        "cooling_down",
        concurrency_limit=3,
        resume_after_utc="2026-06-21T16:00:00Z",
    )
    snapshot_path = _policy_snapshot(
        tmp_path,
        [
            {
                "lane_id": "always_lane",
                "runtime_mode": "always_on",
                "cadence_minutes": 15,
                "max_parallel_tasks": 1,
                "capacity_class": "codex",
                "activation_triggers": ["continuity_tick"],
            }
        ],
    )

    payload = build_lane_runtime_activation_plan(conn, _args(tmp_path, snapshot_path))

    assert payload["status"] == "pending_capacity"
    assert payload["dispatch_recommendations"] == []
    assert payload["next_wakeup_utc"] == "2026-06-21T16:00:00Z"
    assert payload["counts"]["overdue_capacity_sessions"] == 0
    assert payload["lane_activation_states"][0]["recommended_action"] == "pending_capacity"


def test_lane_runtime_activation_plan_marks_past_capacity_wakeup_as_refresh_overdue(tmp_path: Path) -> None:
    conn = _conn()
    _insert_capacity_session(
        conn,
        "codex-cooling",
        "cooling_down",
        concurrency_limit=3,
        resume_after_utc="2026-06-21T16:00:00Z",
    )
    snapshot_path = _policy_snapshot(
        tmp_path,
        [
            {
                "lane_id": "always_lane",
                "runtime_mode": "always_on",
                "cadence_minutes": 15,
                "max_parallel_tasks": 1,
                "capacity_class": "codex",
                "activation_triggers": ["continuity_tick"],
            }
        ],
    )
    args = _args(tmp_path, snapshot_path)
    args.now_utc = "2026-06-21T17:00:00Z"

    payload = build_lane_runtime_activation_plan(conn, args)

    assert payload["status"] == "pending_capacity"
    assert payload["counts"]["overdue_capacity_sessions"] == 1
    assert "refresh signal is overdue" in payload["next_action"]


def test_lane_runtime_activation_plan_ignores_low_priority_backlog_for_auto_dispatch(tmp_path: Path) -> None:
    conn = _conn()
    _insert_capacity_session(conn, "codex-main", "available", concurrency_limit=1)
    now = "2026-06-21T15:44:00Z"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id,
          duplicate_key, evidence_required, next_action, created_at, updated_at
        )
        VALUES(
          'task-low-priority', 'always_lane', 'task-low-priority', 'new', 2,
          'lane-owner', 'runtime:task-low-priority', 'evidence', 'nice-to-have backlog', ?, ?
        )
        """,
        (now, now),
    )
    conn.execute("UPDATE tasks SET status='complete' WHERE task_id='task-always'")
    conn.commit()
    snapshot_path = _policy_snapshot(
        tmp_path,
        [
            {
                "lane_id": "always_lane",
                "runtime_mode": "always_on",
                "cadence_minutes": 15,
                "max_parallel_tasks": 1,
                "capacity_class": "codex",
                "activation_triggers": ["continuity_tick"],
            }
        ],
    )

    payload = build_lane_runtime_activation_plan(conn, _args(tmp_path, snapshot_path))

    assert payload["status"] == "monitoring"
    assert payload["dispatch_recommendations"] == []
    assert payload["counts"]["eligible_task_candidates"] == 0
    assert payload["lane_activation_states"][0]["recommended_action"] == "ensure_seed_or_monitor"


def test_lane_runtime_activation_plan_skips_runtime_blocked_or_running_lanes(tmp_path: Path) -> None:
    conn = _conn()
    _insert_capacity_session(conn, "codex-main", "available", concurrency_limit=3)
    now = "2026-06-21T15:44:00Z"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id,
          duplicate_key, evidence_required, next_action, created_at, updated_at
        )
        VALUES(
          'task-idle-ready', 'idle_demand_lane', 'task-idle-ready', 'new', 85,
          'lane-owner', 'runtime:task-idle-ready', 'evidence', 'dispatch me', ?, ?
        )
        """,
        (now, now),
    )
    conn.commit()
    snapshot_path = _policy_snapshot(
        tmp_path,
        [
            {
                "lane_id": "always_lane",
                "runtime_mode": "always_on",
                "cadence_minutes": 15,
                "max_parallel_tasks": 1,
                "capacity_class": "codex",
                "activation_triggers": ["continuity_tick"],
            },
            {
                "lane_id": "demand_lane",
                "runtime_mode": "on_demand",
                "max_parallel_tasks": 1,
                "capacity_class": "codex",
                "activation_triggers": ["customer_material"],
            },
            {
                "lane_id": "idle_demand_lane",
                "runtime_mode": "on_demand",
                "max_parallel_tasks": 1,
                "capacity_class": "codex",
                "activation_triggers": ["customer_material"],
            },
        ],
    )
    runtime_status_path = tmp_path / "runtime-supervisor.json"
    runtime_status_path.write_text(
        json.dumps(
            {
                "schema_version": "worker_runtime_status.v1",
                "lane_runtime_statuses": [
                    {
                        "lane_id": "always_lane",
                        "runtime_status": "blocked_by_human_gate",
                        "next_action": "Ask the human for an account gate.",
                    },
                    {
                        "lane_id": "demand_lane",
                        "runtime_status": "running",
                        "next_action": "Wait for completion packet.",
                    },
                    {
                        "lane_id": "idle_demand_lane",
                        "runtime_status": "idle_ready",
                        "next_action": "Ready for dispatch.",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    args = _args(tmp_path, snapshot_path)
    args.runtime_supervisor_status = str(runtime_status_path)

    payload = build_lane_runtime_activation_plan(conn, args)

    assert payload["status"] == "dispatch_recommended"
    assert [item["task_id"] for item in payload["dispatch_recommendations"]] == ["task-idle-ready"]
    actions = {item["lane_id"]: item["recommended_action"] for item in payload["lane_activation_states"]}
    assert actions["always_lane"] == "runtime_blocked_by_human_gate"
    assert actions["demand_lane"] == "runtime_running"
    assert actions["idle_demand_lane"] == "dispatch_recommended"
    assert payload["counts"]["runtime_blocked_lanes"] == 2
    assert payload["runtime_supervisor_status"] == str(runtime_status_path)


def test_lane_runtime_activation_plan_only_blocks_human_gated_tasks_when_feed_is_available(
    tmp_path: Path,
) -> None:
    conn = _conn()
    _insert_capacity_session(conn, "codex-main", "available", concurrency_limit=2)
    now = "2026-06-21T15:44:00Z"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id,
          duplicate_key, evidence_required, next_action, created_at, updated_at
        )
        VALUES(
          'task-always-local', 'always_lane', 'task-always-local', 'new', 94,
          'lane-owner', 'runtime:task-always-local', 'evidence', 'dispatch local work', ?, ?
        )
        """,
        (now, now),
    )
    conn.commit()
    snapshot_path = _policy_snapshot(
        tmp_path,
        [
            {
                "lane_id": "always_lane",
                "runtime_mode": "always_on",
                "cadence_minutes": 15,
                "max_parallel_tasks": 1,
                "capacity_class": "codex",
                "activation_triggers": ["continuity_tick"],
            }
        ],
    )
    runtime_status_path = tmp_path / "runtime-supervisor.json"
    runtime_status_path.write_text(
        json.dumps(
            {
                "schema_version": "worker_runtime_status.v1",
                "lane_runtime_statuses": [
                    {
                        "lane_id": "always_lane",
                        "runtime_status": "blocked_by_human_gate",
                        "next_action": "Some work requires account approval.",
                    }
                ],
                "human_action_feed": {
                    "account_gate_queue": [
                        {
                            "lane_id": "always_lane",
                            "task_id": "task-always",
                            "blocking": True,
                            "surface": "External account",
                        }
                    ]
                },
            }
        ),
        encoding="utf-8",
    )
    args = _args(tmp_path, snapshot_path)
    args.runtime_supervisor_status = str(runtime_status_path)

    payload = build_lane_runtime_activation_plan(conn, args)

    assert payload["status"] == "dispatch_recommended"
    assert [item["task_id"] for item in payload["dispatch_recommendations"]] == ["task-always-local"]
    state = payload["lane_activation_states"][0]
    assert state["recommended_action"] == "dispatch_recommended"
    assert state["open_task_count"] == 2
    assert state["selected_task_count"] == 1
    assert state["runtime_blocked_task_count"] == 1
    assert payload["counts"]["runtime_blocked_lanes"] == 0


def test_lane_runtime_activation_plan_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-lane-runtime-activation-plan",
            "--policy-snapshot",
            "policies.json",
            "--runtime-supervisor-status",
            "runtime.json",
            "--max-lanes",
            "4",
        ]
    )

    assert args.cmd == "write-lane-runtime-activation-plan"
    assert args.policy_snapshot == "policies.json"
    assert args.runtime_supervisor_status == "runtime.json"
    assert args.max_lanes == 4
