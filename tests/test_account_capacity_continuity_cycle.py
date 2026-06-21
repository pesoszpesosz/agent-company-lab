import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.account_capacity_continuity_cycle import (  # noqa: E402
    run_account_capacity_continuity_cycle,
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
        VALUES('department_manager', 'manager', '[]', '[]', '2026-06-21T16:40:00Z', '2026-06-21T16:40:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('lane-owner', 'department_manager', 'codex-thread:owner-thread', 'ai_resources', 'active', '[]', '2026-06-21T16:40:00Z', '2026-06-21T16:40:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('lane-manager-ai_resources_lab-20260620', 'department_manager', 'codex-thread:ar', 'ai_resources', 'active', '[]', '2026-06-21T16:40:00Z', '2026-06-21T16:40:00Z')
        """
    )
    for lane_id in ["premium_customer_intake", "ai_resources_lab"]:
        owner = "lane-owner" if lane_id == "premium_customer_intake" else "lane-manager-ai_resources_lab-20260620"
        thread = "codex-thread:owner-thread" if lane_id == "premium_customer_intake" else "codex-thread:ar"
        conn.execute(
            """
            INSERT INTO lanes(
              lane_id, department, status, owner_agent_id, owner_thread_id,
              agent_types_json, examples_json, promotion_gates_json,
              service_workers_required_json, side_effects_json, global_gates_json,
              created_at, updated_at
            )
            VALUES(?, 'Test', 'active', ?, ?,
                   '[]', '[]', '[]', '[]', '[]', '[]',
                   '2026-06-21T16:40:00Z', '2026-06-21T16:40:00Z')
            """,
            (lane_id, owner, thread),
        )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id,
          duplicate_key, evidence_required, next_action, created_at, updated_at
        )
        VALUES('task-premium', 'premium_customer_intake', 'Task premium', 'new', 95, 'lane-owner',
               'cycle:task-premium', 'evidence', 'do local work',
               '2026-06-21T16:40:00Z', '2026-06-21T16:40:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO account_capacity_sessions(
          session_id, surface, account_label, status, concurrency_limit,
          active_lease_count, resume_after_utc, last_error, created_at, updated_at
        )
        VALUES('codex-parallel', 'codex', 'parallel pool', 'cooling_down', 1, 0,
               '2026-06-21T16:45:00Z', 'usage exhausted',
               '2026-06-21T16:30:00Z', '2026-06-21T16:40:00Z')
        """
    )
    conn.commit()
    return conn


def _policy_snapshot(tmp_path: Path) -> Path:
    path = tmp_path / "policies.json"
    path.write_text(
        json.dumps(
            {
                "policies": [
                    {
                        "lane_id": "premium_customer_intake",
                        "runtime_mode": "always_on",
                        "cadence_minutes": 15,
                        "max_parallel_tasks": 1,
                        "capacity_class": "codex",
                        "activation_triggers": ["continuity_tick"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    return path


def _refresh_signal(tmp_path: Path) -> Path:
    path = tmp_path / "refresh-signal.json"
    path.write_text(
        json.dumps(
            {
                "signal_id": "refresh-signal-codex-parallel",
                "session_id": "codex-parallel",
                "observed_utc": "2026-06-21T16:50:00Z",
                "status": "usable",
                "source": "operator_refresh_watch",
                "evidence": "usable session observed outside repo; no credential stored",
            }
        ),
        encoding="utf-8",
    )
    return path


def _args(
    tmp_path: Path,
    policy_snapshot: Path,
    refresh_signal: Path | None = None,
    drain: bool = False,
    no_db_record: bool = True,
) -> Namespace:
    return Namespace(
        policy_snapshot=str(policy_snapshot),
        refresh_signal=str(refresh_signal) if refresh_signal else None,
        now_utc="2026-06-21T16:55:00Z",
        max_lanes=20,
        max_dispatches=1,
        lease_minutes=120,
        executor_agent_id="account-capacity-continuity-cycle",
        drain=drain,
        path=str(tmp_path / "cycle.md"),
        json_path=str(tmp_path / "cycle.json"),
        work_dir=str(tmp_path / "cycle-work"),
        no_db_record=no_db_record,
    )


def test_account_capacity_continuity_cycle_plans_without_leasing_or_sending(tmp_path: Path) -> None:
    conn = _conn()
    policy_snapshot = _policy_snapshot(tmp_path)

    payload = run_account_capacity_continuity_cycle(conn, _args(tmp_path, policy_snapshot))

    assert payload["status"] == "pending_capacity"
    assert payload["counts"]["refresh_signals_applied"] == 0
    assert payload["counts"]["dispatch_recommendations"] == 0
    assert payload["counts"]["leased_dispatches"] == 0
    assert payload["counts"]["ready_thread_deliveries"] == 0
    assert payload["zero_side_effect_boundary"]["thread_messages_sent"] == 0
    assert payload["substeps"]["dispatch_drain"]["status"] == "skipped"
    task = conn.execute(
        "SELECT status, lease_owner_agent_id, lease_expires_at FROM tasks WHERE task_id='task-premium'"
    ).fetchone()
    assert dict(task) == {"status": "new", "lease_owner_agent_id": None, "lease_expires_at": None}


def test_account_capacity_continuity_cycle_applies_refresh_and_drains_one_local_outbox(
    tmp_path: Path,
) -> None:
    conn = _conn()
    policy_snapshot = _policy_snapshot(tmp_path)
    refresh_signal = _refresh_signal(tmp_path)

    payload = run_account_capacity_continuity_cycle(
        conn,
        _args(tmp_path, policy_snapshot, refresh_signal=refresh_signal, drain=True, no_db_record=False),
    )

    assert payload["status"] == "delivery_outbox_ready"
    assert payload["counts"]["refresh_signals_applied"] == 1
    assert payload["counts"]["dispatch_recommendations"] == 1
    assert payload["counts"]["leased_dispatches"] == 1
    assert payload["counts"]["ready_thread_deliveries"] == 1
    assert payload["zero_side_effect_boundary"]["thread_messages_sent"] == 0
    assert payload["substeps"]["thread_delivery_outbox"]["status"] == "ready_to_send"

    task = conn.execute(
        "SELECT status, lease_owner_agent_id, lease_expires_at FROM tasks WHERE task_id='task-premium'"
    ).fetchone()
    assert dict(task) == {
        "status": "in_progress",
        "lease_owner_agent_id": "lane-owner",
        "lease_expires_at": "2026-06-21T18:55:00Z",
    }
    session = conn.execute(
        """
        SELECT status, active_lease_count, last_refresh_utc, last_error
        FROM account_capacity_sessions
        WHERE session_id='codex-parallel'
        """
    ).fetchone()
    assert dict(session) == {
        "status": "available",
        "active_lease_count": 1,
        "last_refresh_utc": "2026-06-21T16:50:00Z",
        "last_error": None,
    }
    audit = conn.execute(
        "SELECT status, evidence_required FROM tasks WHERE task_id='task-account-capacity-continuity-cycle-v1-20260621'"
    ).fetchone()
    assert dict(audit) == {"status": "complete", "evidence_required": str(tmp_path / "cycle.md")}


def test_account_capacity_continuity_cycle_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "run-account-capacity-continuity-cycle",
            "--policy-snapshot",
            "policies.json",
            "--refresh-signal",
            "refresh.json",
            "--drain",
            "--max-dispatches",
            "1",
        ]
    )

    assert args.cmd == "run-account-capacity-continuity-cycle"
    assert args.policy_snapshot == "policies.json"
    assert args.refresh_signal == "refresh.json"
    assert args.drain is True
    assert args.max_dispatches == 1
