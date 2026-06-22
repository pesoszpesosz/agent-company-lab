import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.lane_runtime_governance_keepalive import (  # noqa: E402
    write_lane_runtime_governance_keepalive,
)
from agent_company_core.lane_runtime_thread_delivery import (  # noqa: E402
    write_lane_runtime_thread_delivery_send_preflight,
)
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('premium_customer_intake_agent', 'manager', '[]', '[]',
               '2026-06-22T07:30:00Z', '2026-06-22T07:30:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('ai_resources_manager', 'manager', '[]', '[]',
               '2026-06-22T07:30:00Z', '2026-06-22T07:30:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('premium_customer_context_router', 'manager', '[]', '[]',
               '2026-06-22T07:30:00Z', '2026-06-22T07:30:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('continuity_watchdog_worker', 'worker', '[]', '[]',
               '2026-06-22T07:30:00Z', '2026-06-22T07:30:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('premium-customer-intake-agent-20260620', 'premium_customer_intake_agent',
               'codex-thread:premium-thread', 'premium_customer_intake', 'active', '[]',
               '2026-06-22T07:30:00Z', '2026-06-22T07:30:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('lane-manager-ai_resources_lab-20260620', 'ai_resources_manager',
               'codex-thread:ar-thread', 'ai_resources', 'active', '[]',
               '2026-06-22T07:30:00Z', '2026-06-22T07:30:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('premium-customer-context-router-20260621', 'premium_customer_context_router',
               'codex-thread:premium-thread', 'premium_customer_intake', 'active', '[]',
               '2026-06-22T07:30:00Z', '2026-06-22T07:30:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('continuity-watchdog-worker-20260621', 'continuity_watchdog_worker',
               'codex-thread:watchdog-thread', 'ai_resources', 'active', '[]',
               '2026-06-22T07:30:00Z', '2026-06-22T07:30:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO lanes(
          lane_id, department, status, owner_agent_id, owner_thread_id,
          agent_types_json, examples_json, promotion_gates_json,
          service_workers_required_json, side_effects_json, global_gates_json,
          created_at, updated_at
        )
        VALUES('premium_customer_intake', 'Customer', 'active',
               'premium-customer-intake-agent-20260620', 'codex-thread:premium-thread',
               '[]', '[]', '[]', '[]', '[]', '[]',
               '2026-06-22T07:30:00Z', '2026-06-22T07:30:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO lanes(
          lane_id, department, status, owner_agent_id, owner_thread_id,
          agent_types_json, examples_json, promotion_gates_json,
          service_workers_required_json, side_effects_json, global_gates_json,
          created_at, updated_at
        )
        VALUES('ai_resources_lab', 'AI Resources', 'active',
               'lane-manager-ai_resources_lab-20260620', 'codex-thread:ar-thread',
               '[]', '[]', '[]', '[]', '[]', '[]',
               '2026-06-22T07:30:00Z', '2026-06-22T07:30:00Z')
        """
    )
    for lane_id in ["ai_resources_lab", "premium_customer_intake"]:
        conn.execute(
            """
            INSERT INTO lane_runtime_policies(
              lane_id, runtime_mode, cadence_minutes, max_parallel_tasks, capacity_class,
              activation_triggers_json, park_conditions_json, notes, created_at, updated_at
            )
            VALUES(?, 'always_on', 15, 1, 'codex', '[]', '[]', 'test policy',
                   '2026-06-22T07:30:00Z', '2026-06-22T07:30:00Z')
            """,
            (lane_id,),
        )
    conn.execute(
        """
        INSERT INTO account_capacity_sessions(
          session_id, surface, account_label, status, concurrency_limit, active_lease_count,
          resume_after_utc, last_refresh_utc, last_error, notes, created_at, updated_at
        )
        VALUES('codex-main', 'codex', 'main', 'available', 3, 0, NULL,
               '2026-06-22T07:30:00Z', NULL, NULL,
               '2026-06-22T07:30:00Z', '2026-06-22T07:30:00Z')
        """
    )
    conn.commit()
    return conn


def _args(tmp_path: Path, *, now_utc: str = "2026-06-22T07:31:00Z") -> Namespace:
    return Namespace(
        now_utc=now_utc,
        max_keepalives=3,
        lease_minutes=30,
        packet_dir=str(tmp_path / "packets"),
        path=str(tmp_path / "keepalive.md"),
        json_path=str(tmp_path / "keepalive.json"),
        no_db_record=False,
    )


def test_governance_keepalive_creates_safe_ready_deliveries(tmp_path: Path) -> None:
    conn = _conn()

    payload = write_lane_runtime_governance_keepalive(conn, _args(tmp_path))

    assert payload["status"] == "keepalives_ready_to_send"
    assert payload["counts"]["always_on_lanes_seen"] == 2
    assert payload["counts"]["critical_governance_agents_seen"] == 1
    assert payload["counts"]["keepalives_created"] == 3
    row = conn.execute(
        "SELECT status, lease_owner_agent_id, lease_expires_at FROM tasks WHERE lane_id='premium_customer_intake'"
    ).fetchone()
    assert dict(row) == {
        "status": "in_progress",
        "lease_owner_agent_id": "premium-customer-intake-agent-20260620",
        "lease_expires_at": "2026-06-22T08:01:00Z",
    }
    session = conn.execute(
        "SELECT active_lease_count FROM account_capacity_sessions WHERE session_id='codex-main'"
    ).fetchone()
    assert session["active_lease_count"] == 3

    preflight = write_lane_runtime_thread_delivery_send_preflight(
        conn,
        Namespace(
            now_utc="2026-06-22T07:32:00Z",
            max_deliveries=3,
            include_safe_ready_deliveries=True,
            include_active_resume_deliveries=False,
            auto_authorize_approved_deliveries=True,
            path=str(tmp_path / "send.md"),
            json_path=str(tmp_path / "send.json"),
            no_db_record=True,
        ),
    )
    assert preflight["status"] == "auto_wake_sends_ready"
    assert preflight["counts"]["auto_wake_packets_ready"] == 3
    assert {item["thread_id_for_tool"] for item in preflight["send_packets"]} == {
        "ar-thread",
        "premium-thread",
        "watchdog-thread",
    }
    assert all("Do not start browsers, create agents" in item["prompt_text"] for item in preflight["send_packets"])


def test_governance_keepalive_does_not_duplicate_open_keepalive(tmp_path: Path) -> None:
    conn = _conn()
    first = write_lane_runtime_governance_keepalive(conn, _args(tmp_path))
    assert first["counts"]["keepalives_created"] == 3

    second = write_lane_runtime_governance_keepalive(
        conn,
        _args(tmp_path, now_utc="2026-06-22T07:35:00Z"),
    )

    assert second["status"] == "no_keepalives_due"
    assert second["counts"]["keepalives_created"] == 0
    reasons = {item["reason"] for item in second["skipped_lanes"]}
    assert reasons == {"open_keepalive_already_exists"}


def test_governance_keepalive_wakes_critical_watchdog_without_duplicate_router_thread(tmp_path: Path) -> None:
    conn = _conn()

    payload = write_lane_runtime_governance_keepalive(
        conn,
        Namespace(
            now_utc="2026-06-22T07:31:00Z",
            max_keepalives=3,
            lease_minutes=30,
            packet_dir=str(tmp_path / "packets"),
            path=str(tmp_path / "keepalive.md"),
            json_path=str(tmp_path / "keepalive.json"),
            no_db_record=False,
        ),
    )

    assert payload["status"] == "keepalives_ready_to_send"
    assert payload["counts"]["critical_governance_agents_seen"] == 1
    assert payload["counts"]["keepalives_created"] == 3
    assert {item["thread_id_for_tool"] for item in payload["keepalives"]} == {
        "ar-thread",
        "premium-thread",
        "watchdog-thread",
    }
    assert [item["thread_id_for_tool"] for item in payload["keepalives"]].count("premium-thread") == 1
    watchdog = next(item for item in payload["keepalives"] if item["thread_id_for_tool"] == "watchdog-thread")
    assert watchdog["target_kind"] == "critical_governance_agent"
    assert watchdog["target_id"] == "continuity-watchdog-worker-20260621"
