import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.lane_runtime_thread_delivery import (  # noqa: E402
    record_lane_runtime_thread_delivery_receipt,
    write_lane_runtime_thread_delivery_outbox,
)
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('department_manager', 'manager', '[]', '[]', '2026-06-21T16:20:00Z', '2026-06-21T16:20:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('owner-agent', 'department_manager', 'codex-thread:owner-thread', 'customer_success', 'active', '[]', '2026-06-21T16:20:00Z', '2026-06-21T16:20:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('lane-manager-ai_resources_lab-20260620', 'department_manager', 'codex-thread:ar', 'ai_resources', 'active', '[]', '2026-06-21T16:20:00Z', '2026-06-21T16:20:00Z')
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
        VALUES('premium_customer_intake', 'Customer', 'active', 'owner-agent', 'codex-thread:owner-thread',
               '[]', '[]', '[]', '[]', '[]', '[]',
               '2026-06-21T16:20:00Z', '2026-06-21T16:20:00Z')
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
        VALUES('ai_resources_lab', 'AI Resources', 'active', 'lane-manager-ai_resources_lab-20260620', 'codex-thread:ar',
               '[]', '[]', '[]', '[]', '[]', '[]',
               '2026-06-21T16:20:00Z', '2026-06-21T16:20:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id,
          duplicate_key, evidence_required, next_action, created_at, updated_at,
          lease_owner_agent_id, lease_expires_at
        )
        VALUES('task-premium', 'premium_customer_intake', 'Task premium', 'in_progress', 95, 'owner-agent',
               'delivery:task-premium', 'evidence', 'do the local work',
               '2026-06-21T16:20:00Z', '2026-06-21T16:20:00Z',
               'owner-agent', '2026-06-21T18:20:00Z')
        """
    )
    conn.commit()
    return conn


def _drain_report(
    tmp_path: Path,
    leased_dispatches: list[dict[str, object]],
) -> Path:
    path = tmp_path / "drain.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": "lane_runtime_dispatch_drain.v1",
                "generated_utc": "2026-06-21T16:20:00Z",
                "status": "dispatch_packets_ready",
                "leased_dispatches": leased_dispatches,
            }
        ),
        encoding="utf-8",
    )
    return path


def _leased_dispatch(owner_thread_id: str | None = "codex-thread:owner-thread") -> dict[str, object]:
    return {
        "session_id": "codex-main",
        "task_id": "task-premium",
        "lane_id": "premium_customer_intake",
        "runtime_mode": "always_on",
        "owner_agent_id": "owner-agent",
        "owner_thread_id": owner_thread_id,
        "lease_owner_agent_id": "owner-agent",
        "lease_expires_at": "2026-06-21T18:20:00Z",
        "evidence_required": "evidence",
        "next_action": "do the local work",
        "packet_path": r"E:\agent-company-lab\reports\packet.md",
    }


def _outbox_args(tmp_path: Path, drain_report: Path, no_db_record: bool = True) -> Namespace:
    return Namespace(
        drain_report=str(drain_report),
        now_utc="2026-06-21T16:25:00Z",
        outbox_dir=str(tmp_path / "outbox"),
        path=str(tmp_path / "outbox.md"),
        json_path=str(tmp_path / "outbox.json"),
        no_db_record=no_db_record,
    )


def test_lane_runtime_thread_delivery_outbox_writes_ready_prompt_and_table_row(tmp_path: Path) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch()])

    payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report, no_db_record=False))

    assert payload["status"] == "ready_to_send"
    assert payload["counts"] == {
        "deliveries_seen": 1,
        "ready_to_send": 1,
        "blocked_no_owner_thread": 0,
        "already_delivered": 0,
    }
    delivery = payload["deliveries"][0]
    assert delivery["status"] == "ready_to_send"
    assert delivery["thread_id_for_tool"] == "owner-thread"
    prompt_path = Path(delivery["prompt_path"])
    assert prompt_path.exists()
    prompt_text = prompt_path.read_text(encoding="utf-8")
    assert "Continue your active lane goal" in prompt_text
    assert "task-premium" in prompt_text
    assert "Do not start browsers" in prompt_text

    row = conn.execute(
        "SELECT status, owner_thread_id, prompt_path FROM lane_runtime_thread_deliveries WHERE delivery_id=?",
        (delivery["delivery_id"],),
    ).fetchone()
    assert dict(row) == {
        "status": "ready_to_send",
        "owner_thread_id": "codex-thread:owner-thread",
        "prompt_path": str(prompt_path),
    }
    audit = conn.execute(
        "SELECT status, evidence_required FROM tasks WHERE task_id='task-lane-runtime-thread-delivery-outbox-v1-20260621'"
    ).fetchone()
    assert dict(audit) == {"status": "complete", "evidence_required": str(tmp_path / "outbox.md")}


def test_lane_runtime_thread_delivery_outbox_blocks_missing_owner_thread(tmp_path: Path) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch(owner_thread_id=None)])

    payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))

    assert payload["status"] == "blocked"
    assert payload["counts"]["ready_to_send"] == 0
    assert payload["counts"]["blocked_no_owner_thread"] == 1
    assert payload["deliveries"][0]["status"] == "blocked_no_owner_thread"
    assert payload["deliveries"][0]["prompt_path"] is None


def test_lane_runtime_thread_delivery_receipt_marks_delivery_delivered(tmp_path: Path) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch()])
    payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))
    delivery_id = payload["deliveries"][0]["delivery_id"]

    receipt = record_lane_runtime_thread_delivery_receipt(
        conn,
        Namespace(
            delivery_id=delivery_id,
            status="delivered",
            now_utc="2026-06-21T16:30:00Z",
            error=None,
        ),
    )

    assert receipt["ok"] is True
    row = conn.execute(
        """
        SELECT status, delivered_at, delivery_attempts, last_error
        FROM lane_runtime_thread_deliveries
        WHERE delivery_id=?
        """,
        (delivery_id,),
    ).fetchone()
    assert dict(row) == {
        "status": "delivered",
        "delivered_at": "2026-06-21T16:30:00Z",
        "delivery_attempts": 1,
        "last_error": None,
    }


def test_lane_runtime_thread_delivery_cli_parser_supports_commands() -> None:
    parser = build_parser()
    outbox = parser.parse_args(
        [
            "write-lane-runtime-thread-delivery-outbox",
            "--drain-report",
            "drain.json",
        ]
    )
    receipt = parser.parse_args(
        [
            "record-lane-runtime-thread-delivery",
            "--delivery-id",
            "delivery-task",
            "--status",
            "delivered",
        ]
    )

    assert outbox.cmd == "write-lane-runtime-thread-delivery-outbox"
    assert outbox.drain_report == "drain.json"
    assert receipt.cmd == "record-lane-runtime-thread-delivery"
    assert receipt.delivery_id == "delivery-task"
    assert receipt.status == "delivered"
