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


def _runtime_supervisor_status(tmp_path: Path, runtime_status: str = "blocked_by_human_gate") -> Path:
    path = tmp_path / "runtime-supervisor.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": "worker_runtime_status.v1",
                "lane_runtime_statuses": [
                    {
                        "lane_id": "premium_customer_intake",
                        "runtime_status": runtime_status,
                        "next_action": "Wait for human/account gate before dispatch.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def _args(
    tmp_path: Path,
    policy_snapshot: Path,
    refresh_signal: Path | None = None,
    runtime_supervisor_status: Path | None = None,
    refresh_signal_dir: Path | None = None,
    auto_apply_ready_refresh_signal: bool = False,
    self_observed_codex_capacity_refresh: bool = False,
    self_observed_capacity_session_id: str | None = None,
    thread_delivery_approval_signal: Path | None = None,
    thread_delivery_approval_dir: Path | None = None,
    auto_apply_ready_thread_delivery_approval: bool = False,
    auto_wake_local_only_thread_deliveries: bool = False,
    drain: bool = False,
    no_db_record: bool = True,
) -> Namespace:
    return Namespace(
        policy_snapshot=str(policy_snapshot),
        refresh_signal=str(refresh_signal) if refresh_signal else None,
        runtime_supervisor_status=str(runtime_supervisor_status) if runtime_supervisor_status else None,
        refresh_signal_dir=str(refresh_signal_dir) if refresh_signal_dir else None,
        auto_apply_ready_refresh_signal=auto_apply_ready_refresh_signal,
        self_observed_codex_capacity_refresh=self_observed_codex_capacity_refresh,
        self_observed_capacity_session_id=self_observed_capacity_session_id,
        thread_delivery_approval_signal=(
            str(thread_delivery_approval_signal) if thread_delivery_approval_signal else None
        ),
        thread_delivery_approval_dir=str(thread_delivery_approval_dir) if thread_delivery_approval_dir else None,
        auto_apply_ready_thread_delivery_approval=auto_apply_ready_thread_delivery_approval,
        auto_wake_local_only_thread_deliveries=auto_wake_local_only_thread_deliveries,
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
    assert payload["counts"]["overdue_capacity_sessions"] == 1
    assert payload["counts"]["required_capacity_refresh_actions"] == 1
    assert "Provide a scoped refresh-signal JSON" in payload["next_action"]
    assert payload["zero_side_effect_boundary"]["thread_messages_sent"] == 0
    assert payload["substeps"]["dispatch_drain"]["status"] == "skipped"
    assert payload["substeps"]["capacity_refresh_monitor"]["status"] == "refresh_signal_needed"
    ceo_payload = json.loads(Path(payload["substeps"]["ceo_state_packet"]["json_path"]).read_text(encoding="utf-8"))
    assert ceo_payload["human_action_feed"]["feed_status"] == "human_action_required"
    assert ceo_payload["human_action_feed"]["required_now"][0]["kind"] == "account_capacity_refresh_signal"
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


def test_account_capacity_continuity_cycle_rediscovers_existing_ready_thread_delivery(
    tmp_path: Path,
) -> None:
    conn = _conn()
    policy_snapshot = _policy_snapshot(tmp_path)
    prompt_path = tmp_path / "ready-prompt.md"
    prompt_path.write_text("Ready prompt", encoding="utf-8")
    packet_path = tmp_path / "dispatch-packet.md"
    packet_path.write_text("Dispatch packet", encoding="utf-8")
    conn.execute(
        """
        UPDATE tasks
        SET status = 'in_progress',
            lease_owner_agent_id = 'lane-owner',
            lease_expires_at = '2026-06-21T18:55:00Z'
        WHERE task_id = 'task-premium'
        """
    )
    conn.execute(
        """
        INSERT INTO lane_runtime_thread_deliveries(
          delivery_id, task_id, lane_id, session_id, owner_agent_id, owner_thread_id,
          packet_path, prompt_path, status, delivery_attempts, delivered_at, last_error,
          created_at, updated_at
        )
        VALUES(
          'delivery-task-premium', 'task-premium', 'premium_customer_intake', 'codex-parallel',
          'lane-owner', 'codex-thread:owner-thread', ?, ?, 'ready_to_send', 0, NULL, NULL,
          '2026-06-21T16:55:00Z', '2026-06-21T16:55:00Z'
        )
        """,
        (str(packet_path), str(prompt_path)),
    )
    conn.commit()

    payload = run_account_capacity_continuity_cycle(conn, _args(tmp_path, policy_snapshot))

    assert payload["status"] == "delivery_outbox_ready"
    assert payload["counts"]["ready_thread_deliveries"] == 1
    assert payload["counts"]["active_thread_delivery_leases"] == 1
    assert payload["counts"]["expired_thread_delivery_leases"] == 0
    assert payload["counts"]["unknown_thread_delivery_leases"] == 0
    assert payload["substeps"]["thread_delivery_outbox"]["status"] == "ready_to_send"
    outbox = json.loads(Path(payload["substeps"]["thread_delivery_outbox"]["json_path"]).read_text(encoding="utf-8"))
    assert outbox["deliveries"][0]["thread_id_for_tool"] == "owner-thread"
    assert outbox["deliveries"][0]["lease_expires_at"] == "2026-06-21T18:55:00Z"
    ceo_payload = json.loads(Path(payload["substeps"]["ceo_state_packet"]["json_path"]).read_text(encoding="utf-8"))
    assert ceo_payload["human_action_feed"]["required_now"][0]["kind"] == "thread_delivery_approval"


def test_account_capacity_continuity_cycle_parks_expired_ready_thread_delivery(
    tmp_path: Path,
) -> None:
    conn = _conn()
    policy_snapshot = _policy_snapshot(tmp_path)
    prompt_path = tmp_path / "expired-ready-prompt.md"
    prompt_path.write_text("Expired ready prompt", encoding="utf-8")
    packet_path = tmp_path / "expired-dispatch-packet.md"
    packet_path.write_text("Expired dispatch packet", encoding="utf-8")
    conn.execute(
        """
        UPDATE tasks
        SET status = 'in_progress',
            lease_owner_agent_id = 'lane-owner',
            lease_expires_at = '2026-06-21T10:00:00Z'
        WHERE task_id = 'task-premium'
        """
    )
    conn.execute(
        """
        INSERT INTO lane_runtime_thread_deliveries(
          delivery_id, task_id, lane_id, session_id, owner_agent_id, owner_thread_id,
          packet_path, prompt_path, status, delivery_attempts, delivered_at, last_error,
          created_at, updated_at
        )
        VALUES(
          'delivery-task-premium', 'task-premium', 'premium_customer_intake', 'codex-parallel',
          'lane-owner', 'codex-thread:owner-thread', ?, ?, 'ready_to_send', 0, NULL, NULL,
          '2026-06-21T10:00:00Z', '2026-06-21T10:00:00Z'
        )
        """,
        (str(packet_path), str(prompt_path)),
    )
    conn.commit()

    payload = run_account_capacity_continuity_cycle(
        conn,
        _args(tmp_path, policy_snapshot, no_db_record=False),
    )

    assert payload["status"] == "pending_capacity"
    assert payload["counts"]["expired_ready_deliveries_parked"] == 1
    assert payload["counts"]["expired_delivery_task_leases_released"] == 1
    assert payload["counts"]["expired_delivery_tasks_requeued"] == 1
    assert payload["counts"]["ready_thread_deliveries"] == 0
    assert payload["counts"]["expired_thread_delivery_leases"] == 0
    assert payload["substeps"]["expired_delivery_reconcile"]["status"] == "expired_deliveries_parked"
    delivery = conn.execute(
        "SELECT status, last_error FROM lane_runtime_thread_deliveries WHERE delivery_id='delivery-task-premium'"
    ).fetchone()
    task = conn.execute(
        "SELECT status, lease_owner_agent_id, lease_expires_at FROM tasks WHERE task_id='task-premium'"
    ).fetchone()
    assert delivery["status"] == "lease_expired_parked"
    assert "lease expired" in delivery["last_error"]
    assert dict(task) == {"status": "new", "lease_owner_agent_id": None, "lease_expires_at": None}
    ceo_payload = json.loads(Path(payload["substeps"]["ceo_state_packet"]["json_path"]).read_text(encoding="utf-8"))
    assert ceo_payload["human_action_feed"]["required_now"][0]["kind"] == "account_capacity_refresh_signal"


def test_account_capacity_continuity_cycle_rediscovers_existing_approved_thread_delivery(
    tmp_path: Path,
) -> None:
    conn = _conn()
    policy_snapshot = _policy_snapshot(tmp_path)
    prompt_path = tmp_path / "approved-prompt.md"
    prompt_path.write_text("Approved prompt", encoding="utf-8")
    packet_path = tmp_path / "dispatch-packet.md"
    packet_path.write_text("Dispatch packet", encoding="utf-8")
    conn.execute(
        """
        UPDATE tasks
        SET status = 'in_progress',
            lease_owner_agent_id = 'lane-owner',
            lease_expires_at = '2026-06-21T10:00:00Z'
        WHERE task_id = 'task-premium'
        """
    )
    conn.execute(
        """
        INSERT INTO lane_runtime_thread_deliveries(
          delivery_id, task_id, lane_id, session_id, owner_agent_id, owner_thread_id,
          packet_path, prompt_path, status, delivery_attempts, delivered_at, last_error,
          created_at, updated_at
        )
        VALUES(
          'delivery-task-premium', 'task-premium', 'premium_customer_intake', 'codex-parallel',
          'lane-owner', 'codex-thread:owner-thread', ?, ?, 'send_approved', 0, NULL, NULL,
          '2026-06-21T16:55:00Z', '2026-06-21T16:55:00Z'
        )
        """,
        (str(packet_path), str(prompt_path)),
    )
    conn.commit()

    payload = run_account_capacity_continuity_cycle(conn, _args(tmp_path, policy_snapshot))

    assert payload["status"] == "approved_thread_delivery_pending"
    assert payload["counts"]["ready_thread_deliveries"] == 0
    assert payload["counts"]["approved_thread_deliveries"] == 1
    assert payload["counts"]["active_thread_delivery_leases"] == 0
    assert payload["counts"]["expired_thread_delivery_leases"] == 1
    assert payload["counts"]["unknown_thread_delivery_leases"] == 0
    assert payload["substeps"]["thread_delivery_outbox"]["status"] == "approved_to_send"
    outbox = json.loads(Path(payload["substeps"]["thread_delivery_outbox"]["json_path"]).read_text(encoding="utf-8"))
    assert outbox["counts"]["send_approved"] == 1
    assert outbox["deliveries"][0]["status"] == "send_approved"
    ceo_payload = json.loads(Path(payload["substeps"]["ceo_state_packet"]["json_path"]).read_text(encoding="utf-8"))
    assert ceo_payload["human_action_feed"]["required_now"][0]["kind"] == "thread_delivery_send"
    assert ceo_payload["human_action_feed"]["required_now"][0]["delivery_id"] == "delivery-task-premium"


def test_account_capacity_continuity_cycle_respects_runtime_supervisor_block_before_draining(
    tmp_path: Path,
) -> None:
    conn = _conn()
    policy_snapshot = _policy_snapshot(tmp_path)
    refresh_signal = _refresh_signal(tmp_path)
    runtime_status = _runtime_supervisor_status(tmp_path)

    payload = run_account_capacity_continuity_cycle(
        conn,
        _args(
            tmp_path,
            policy_snapshot,
            refresh_signal=refresh_signal,
            runtime_supervisor_status=runtime_status,
            drain=True,
        ),
    )

    assert payload["status"] == "monitoring_gated_lanes"
    assert payload["next_action"] == (
        "Continue restore monitoring; gated lanes stay parked until scoped approval or a safe local trigger appears."
    )
    assert payload["runtime_supervisor_status"] == str(runtime_status)
    assert payload["counts"]["refresh_signals_applied"] == 1
    assert payload["counts"]["runtime_blocked_lanes"] == 1
    assert payload["counts"]["dispatch_recommendations"] == 0
    assert payload["counts"]["leased_dispatches"] == 0
    assert payload["substeps"]["dispatch_drain"]["status"] == "skipped"
    task = conn.execute(
        "SELECT status, lease_owner_agent_id, lease_expires_at FROM tasks WHERE task_id='task-premium'"
    ).fetchone()
    assert dict(task) == {"status": "new", "lease_owner_agent_id": None, "lease_expires_at": None}


def test_account_capacity_continuity_cycle_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "run-account-capacity-continuity-cycle",
            "--policy-snapshot",
            "policies.json",
            "--refresh-signal",
            "refresh.json",
            "--runtime-supervisor-status",
            "runtime.json",
            "--refresh-signal-dir",
            "signals",
            "--auto-apply-ready-refresh-signal",
            "--self-observed-codex-capacity-refresh",
            "--self-observed-capacity-session-id",
            "codex-parallel",
            "--thread-delivery-approval-signal",
            "approval.json",
            "--thread-delivery-approval-dir",
            "approvals",
            "--auto-apply-ready-thread-delivery-approval",
            "--auto-wake-local-only-thread-deliveries",
            "--drain",
            "--max-dispatches",
            "1",
        ]
    )

    assert args.cmd == "run-account-capacity-continuity-cycle"
    assert args.policy_snapshot == "policies.json"
    assert args.refresh_signal == "refresh.json"
    assert args.runtime_supervisor_status == "runtime.json"
    assert args.refresh_signal_dir == "signals"
    assert args.auto_apply_ready_refresh_signal is True
    assert args.self_observed_codex_capacity_refresh is True
    assert args.self_observed_capacity_session_id == "codex-parallel"
    assert args.thread_delivery_approval_signal == "approval.json"
    assert args.thread_delivery_approval_dir == "approvals"
    assert args.auto_apply_ready_thread_delivery_approval is True
    assert args.auto_wake_local_only_thread_deliveries is True
    assert args.drain is True
    assert args.max_dispatches == 1


def test_account_capacity_continuity_cycle_surfaces_ready_refresh_signal_without_applying_it(
    tmp_path: Path,
) -> None:
    conn = _conn()
    policy_snapshot = _policy_snapshot(tmp_path)
    signal_dir = tmp_path / "refresh-signals"
    signal_dir.mkdir()
    signal_path = signal_dir / "codex-parallel-usable.json"
    signal_path.write_text(
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

    payload = run_account_capacity_continuity_cycle(
        conn,
        _args(tmp_path, policy_snapshot, refresh_signal_dir=signal_dir),
    )

    assert payload["status"] == "refresh_signal_ready"
    assert payload["counts"]["ready_refresh_signals"] == 1
    assert payload["counts"]["refresh_signals_applied"] == 0
    assert payload["substeps"]["capacity_refresh_monitor"]["status"] == "refresh_signal_ready"
    command = json.loads(
        Path(payload["substeps"]["capacity_refresh_monitor"]["json_path"]).read_text(encoding="utf-8")
    )["recommended_commands"][0]["command"]
    assert str(signal_path) in command
    assert "--refresh-signal" in command
    session = conn.execute(
        "SELECT status, last_refresh_utc FROM account_capacity_sessions WHERE session_id='codex-parallel'"
    ).fetchone()
    assert dict(session) == {"status": "cooling_down", "last_refresh_utc": None}


def test_account_capacity_continuity_cycle_auto_applies_ready_signal_and_drains(
    tmp_path: Path,
) -> None:
    conn = _conn()
    policy_snapshot = _policy_snapshot(tmp_path)
    signal_dir = tmp_path / "refresh-signals"
    signal_dir.mkdir()
    signal_path = signal_dir / "codex-parallel-usable.json"
    signal_path.write_text(
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

    payload = run_account_capacity_continuity_cycle(
        conn,
        _args(
            tmp_path,
            policy_snapshot,
            refresh_signal_dir=signal_dir,
            auto_apply_ready_refresh_signal=True,
            drain=True,
            no_db_record=False,
        ),
    )

    assert payload["status"] == "delivery_outbox_ready"
    assert payload["auto_applied_refresh_signal"] == str(signal_path)
    assert payload["refresh_signal"] == str(signal_path)
    assert payload["counts"]["refresh_signals_applied"] == 1
    assert payload["counts"]["dispatch_recommendations"] == 1
    assert payload["counts"]["leased_dispatches"] == 1
    assert payload["counts"]["ready_thread_deliveries"] == 1
    assert payload["counts"]["ready_refresh_signals"] == 0
    assert payload["substeps"]["refresh_signal"]["status"] == "capacity_available"
    assert payload["substeps"]["thread_delivery_outbox"]["status"] == "ready_to_send"
    task = conn.execute(
        "SELECT status, lease_owner_agent_id FROM tasks WHERE task_id='task-premium'"
    ).fetchone()
    assert dict(task) == {"status": "in_progress", "lease_owner_agent_id": "lane-owner"}
    session = conn.execute(
        "SELECT status, active_lease_count, last_refresh_utc FROM account_capacity_sessions WHERE session_id='codex-parallel'"
    ).fetchone()
    assert dict(session) == {
        "status": "available",
        "active_lease_count": 1,
        "last_refresh_utc": "2026-06-21T16:50:00Z",
    }


def test_account_capacity_continuity_cycle_self_observed_refresh_signal_drains(
    tmp_path: Path,
) -> None:
    conn = _conn()
    policy_snapshot = _policy_snapshot(tmp_path)
    signal_dir = tmp_path / "refresh-signals"

    payload = run_account_capacity_continuity_cycle(
        conn,
        _args(
            tmp_path,
            policy_snapshot,
            refresh_signal_dir=signal_dir,
            auto_apply_ready_refresh_signal=True,
            self_observed_codex_capacity_refresh=True,
            self_observed_capacity_session_id="codex-parallel",
            drain=True,
            no_db_record=False,
        ),
    )

    assert payload["status"] == "delivery_outbox_ready"
    assert payload["self_observed_refresh_signal"]
    assert payload["auto_applied_refresh_signal"] == payload["self_observed_refresh_signal"]
    assert payload["refresh_signal"] == payload["self_observed_refresh_signal"]
    signal = json.loads(Path(payload["self_observed_refresh_signal"]).read_text(encoding="utf-8"))
    assert signal["session_id"] == "codex-parallel"
    assert signal["source"] == "codex_goal_restore_observed"
    assert "token" not in signal
    assert payload["counts"]["refresh_signals_applied"] == 1
    assert payload["counts"]["leased_dispatches"] == 1
    assert payload["counts"]["ready_thread_deliveries"] == 1
    session = conn.execute(
        "SELECT status, active_lease_count, last_refresh_utc FROM account_capacity_sessions WHERE session_id='codex-parallel'"
    ).fetchone()
    assert dict(session) == {
        "status": "available",
        "active_lease_count": 1,
        "last_refresh_utc": "2026-06-21T16:55:00Z",
    }


def test_account_capacity_continuity_cycle_prepares_safe_auto_wake_after_drain(
    tmp_path: Path,
) -> None:
    conn = _conn()
    policy_snapshot = _policy_snapshot(tmp_path)
    signal_dir = tmp_path / "refresh-signals"
    signal_dir.mkdir()
    signal_path = signal_dir / "codex-parallel-usable.json"
    signal_path.write_text(
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

    payload = run_account_capacity_continuity_cycle(
        conn,
        _args(
            tmp_path,
            policy_snapshot,
            refresh_signal_dir=signal_dir,
            auto_apply_ready_refresh_signal=True,
            auto_wake_local_only_thread_deliveries=True,
            drain=True,
            no_db_record=False,
        ),
    )

    assert payload["status"] == "auto_wake_thread_delivery_ready"
    assert payload["counts"]["leased_dispatches"] == 1
    assert payload["counts"]["ready_thread_deliveries"] == 1
    assert payload["counts"]["safe_auto_wake_thread_deliveries"] == 1
    assert payload["counts"]["thread_delivery_send_packets_ready"] == 1
    assert payload["counts"]["thread_messages_sent"] == 0
    assert payload["substeps"]["thread_delivery_send_preflight"]["status"] == "auto_wake_sends_ready"
    preflight = json.loads(
        Path(payload["substeps"]["thread_delivery_send_preflight"]["json_path"]).read_text(encoding="utf-8")
    )
    packet = preflight["send_packets"][0]
    assert packet["auto_wake_authorized"] is True
    assert packet["send_authority"] == "safe_local_continuity_wake"
    assert packet["thread_id_for_tool"] == "owner-thread"
    ceo_payload = json.loads(Path(payload["substeps"]["ceo_state_packet"]["json_path"]).read_text(encoding="utf-8"))
    assert ceo_payload["human_action_feed"]["required_now"] == []


def test_account_capacity_continuity_cycle_rewakes_active_delivered_thread_after_refresh(
    tmp_path: Path,
) -> None:
    conn = _conn()
    policy_snapshot = _policy_snapshot(tmp_path)
    prompt_path = tmp_path / "delivered-prompt.md"
    prompt_path.write_text(
        "\n".join(
            [
                "Continue your active lane goal using this CEO control-plane dispatch.",
                "",
                "Task: `task-premium`",
                "Lane: `premium_customer_intake`",
                "",
                "Boundary:",
                "Do not start browsers, create agents, mutate ownership, approve service requests, publish, submit, trade, spend, call APIs, or contact anyone.",
                "Work locally only and write the required evidence artifact or an explicit park/revisit packet.",
            ]
        ),
        encoding="utf-8",
    )
    packet_path = tmp_path / "dispatch-packet.md"
    packet_path.write_text("Dispatch packet", encoding="utf-8")
    conn.execute(
        """
        UPDATE account_capacity_sessions
        SET status='available',
            active_lease_count=1,
            last_refresh_utc='2026-06-21T17:00:00Z',
            last_error=NULL,
            updated_at='2026-06-21T17:00:00Z'
        WHERE session_id='codex-parallel'
        """
    )
    conn.execute(
        """
        UPDATE tasks
        SET status = 'in_progress',
            lease_owner_agent_id = 'lane-owner',
            lease_expires_at = '2026-06-21T18:55:00Z',
            updated_at = '2026-06-21T16:56:00Z'
        WHERE task_id = 'task-premium'
        """
    )
    conn.execute(
        """
        INSERT INTO lane_runtime_thread_deliveries(
          delivery_id, task_id, lane_id, session_id, owner_agent_id, owner_thread_id,
          packet_path, prompt_path, status, delivery_attempts, delivered_at, last_error,
          created_at, updated_at
        )
        VALUES(
          'delivery-task-premium', 'task-premium', 'premium_customer_intake', 'codex-parallel',
          'lane-owner', 'codex-thread:owner-thread', ?, ?, 'delivered',
          1, '2026-06-21T16:56:00Z', NULL,
          '2026-06-21T16:55:00Z', '2026-06-21T16:56:00Z'
        )
        """,
        (str(packet_path), str(prompt_path)),
    )
    conn.commit()

    payload = run_account_capacity_continuity_cycle(
        conn,
        _args(
            tmp_path,
            policy_snapshot,
            auto_wake_local_only_thread_deliveries=True,
            no_db_record=False,
        ),
    )

    assert payload["status"] == "auto_wake_thread_delivery_ready"
    assert payload["counts"]["dispatch_recommendations"] == 0
    assert payload["counts"]["leased_dispatches"] == 0
    assert payload["counts"]["ready_thread_deliveries"] == 0
    assert payload["counts"]["active_resume_thread_deliveries"] == 1
    assert payload["counts"]["safe_auto_wake_thread_deliveries"] == 1
    assert payload["counts"]["thread_delivery_send_packets_ready"] == 1
    preflight = json.loads(
        Path(payload["substeps"]["thread_delivery_send_preflight"]["json_path"]).read_text(encoding="utf-8")
    )
    packet = preflight["send_packets"][0]
    assert packet["delivery_id"] == "delivery-task-premium"
    assert packet["source_delivery_status"] == "delivered"
    assert packet["thread_id_for_tool"] == "owner-thread"
    assert packet["auto_wake_authorized"] is True


def test_account_capacity_continuity_cycle_auto_applies_ready_thread_delivery_approval(
    tmp_path: Path,
) -> None:
    conn = _conn()
    policy_snapshot = _policy_snapshot(tmp_path)
    approval_dir = tmp_path / "thread-delivery-approvals"
    approval_dir.mkdir()
    prompt_path = tmp_path / "ready-prompt.md"
    prompt_path.write_text("Ready prompt", encoding="utf-8")
    packet_path = tmp_path / "dispatch-packet.md"
    packet_path.write_text("Dispatch packet", encoding="utf-8")
    conn.execute(
        """
        UPDATE tasks
        SET status = 'in_progress',
            lease_owner_agent_id = 'lane-owner',
            lease_expires_at = '2026-06-21T18:55:00Z'
        WHERE task_id = 'task-premium'
        """
    )
    conn.execute(
        """
        INSERT INTO lane_runtime_thread_deliveries(
          delivery_id, task_id, lane_id, session_id, owner_agent_id, owner_thread_id,
          packet_path, prompt_path, status, delivery_attempts, delivered_at, last_error,
          created_at, updated_at
        )
        VALUES(
          'delivery-task-premium', 'task-premium', 'premium_customer_intake', 'codex-parallel',
          'lane-owner', 'codex-thread:owner-thread', ?, ?, 'ready_to_send', 0, NULL, NULL,
          '2026-06-21T16:54:00Z', '2026-06-21T16:54:00Z'
        )
        """,
        (str(packet_path), str(prompt_path)),
    )
    approval_path = approval_dir / "delivery-task-premium-send-approved.json"
    approval_path.write_text(
        json.dumps(
            {
                "approval_id": "approval-delivery-task-premium",
                "delivery_id": "delivery-task-premium",
                "thread_id_for_tool": "owner-thread",
                "decision": "send_approved",
                "approved_utc": "2026-06-21T16:55:00Z",
                "operator": "matth",
                "scope": "Approve sending only the exact prompt_path currently recorded for this delivery.",
                "attestation": "No credential or token is included; this approves only this one local delivery.",
            }
        ),
        encoding="utf-8",
    )
    conn.commit()

    payload = run_account_capacity_continuity_cycle(
        conn,
        _args(
            tmp_path,
            policy_snapshot,
            thread_delivery_approval_dir=approval_dir,
            auto_apply_ready_thread_delivery_approval=True,
        ),
    )

    assert payload["status"] == "approved_thread_delivery_pending"
    assert payload["thread_delivery_approval_signal"] == str(approval_path)
    assert payload["auto_applied_thread_delivery_approval"] == str(approval_path)
    assert payload["counts"]["thread_delivery_approvals_applied"] == 1
    assert payload["counts"]["ready_thread_deliveries"] == 0
    assert payload["counts"]["approved_thread_deliveries"] == 1
    assert payload["counts"]["thread_messages_sent"] == 0
    assert payload["substeps"]["thread_delivery_approval"]["status"] == "send_approved"
    row = conn.execute(
        "SELECT status, delivery_attempts FROM lane_runtime_thread_deliveries WHERE delivery_id='delivery-task-premium'"
    ).fetchone()
    assert dict(row) == {"status": "send_approved", "delivery_attempts": 0}
