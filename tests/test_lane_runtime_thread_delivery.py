import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.lane_runtime_thread_delivery import (  # noqa: E402
    apply_lane_runtime_thread_delivery_approval_signal,
    promote_lane_runtime_thread_delivery_approval_draft,
    record_lane_runtime_thread_delivery_receipt,
    write_lane_runtime_thread_delivery_approval_drafts,
    write_lane_runtime_thread_delivery_outbox,
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
    assert delivery["lease_expires_at"] == "2026-06-21T18:20:00Z"
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


def test_lane_runtime_thread_delivery_outbox_does_not_resurrect_parked_delivery(tmp_path: Path) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch()])
    first_payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))
    delivery_id = first_payload["deliveries"][0]["delivery_id"]
    conn.execute(
        """
        UPDATE lane_runtime_thread_deliveries
        SET status='superseded_parked',
            delivered_at='2026-06-21T16:30:00Z',
            last_error='superseded by newer delivered thread delivery delivery-newer',
            updated_at='2026-06-21T16:31:00Z'
        WHERE delivery_id=?
        """,
        (delivery_id,),
    )
    conn.commit()

    second_payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))

    assert second_payload["status"] == "no_delivery_needed"
    assert second_payload["counts"]["ready_to_send"] == 0
    assert second_payload["counts"]["already_delivered"] == 1
    assert second_payload["deliveries"][0]["existing_status"] == "superseded_parked"
    row = conn.execute(
        "SELECT status, delivered_at, last_error FROM lane_runtime_thread_deliveries WHERE delivery_id=?",
        (delivery_id,),
    ).fetchone()
    assert dict(row) == {
        "status": "superseded_parked",
        "delivered_at": "2026-06-21T16:30:00Z",
        "last_error": "superseded by newer delivered thread delivery delivery-newer",
    }


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


def test_lane_runtime_thread_delivery_approval_signal_marks_delivery_send_approved(tmp_path: Path) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch()])
    payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))
    delivery = payload["deliveries"][0]
    signal_path = tmp_path / "approval.json"
    signal_path.write_text(
        json.dumps(
            {
                "approval_id": "approval-delivery-task-premium",
                "delivery_id": delivery["delivery_id"],
                "thread_id_for_tool": "owner-thread",
                "decision": "send_approved",
                "approved_utc": "2026-06-21T16:28:00Z",
                "operator": "matth",
                "scope": "Approve sending only the exact prompt_path currently recorded for this delivery.",
                "attestation": "No credential or token is included; this approves only this one local delivery.",
            }
        ),
        encoding="utf-8",
    )

    approval = apply_lane_runtime_thread_delivery_approval_signal(
        conn,
        Namespace(
            approval_signal=str(signal_path),
            now_utc="2026-06-21T16:29:00Z",
            path=str(tmp_path / "approval.md"),
            json_path=str(tmp_path / "approval-result.json"),
            no_db_record=True,
        ),
    )

    assert approval["ok"] is True
    assert approval["status"] == "send_approved"
    assert approval["zero_side_effect_boundary"]["thread_messages_sent"] == 0
    row = conn.execute(
        "SELECT status, delivery_attempts, last_error FROM lane_runtime_thread_deliveries WHERE delivery_id=?",
        (delivery["delivery_id"],),
    ).fetchone()
    assert dict(row) == {"status": "send_approved", "delivery_attempts": 0, "last_error": None}


def test_lane_runtime_thread_delivery_approval_signal_rejects_thread_mismatch(tmp_path: Path) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch()])
    payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))
    delivery = payload["deliveries"][0]
    signal_path = tmp_path / "approval.json"
    signal_path.write_text(
        json.dumps(
            {
                "approval_id": "approval-delivery-task-premium",
                "delivery_id": delivery["delivery_id"],
                "thread_id_for_tool": "wrong-thread",
                "decision": "send_approved",
                "approved_utc": "2026-06-21T16:28:00Z",
                "operator": "matth",
                "scope": "Approve sending only the exact prompt_path currently recorded for this delivery.",
                "attestation": "No credential or token is included; this approves only this one local delivery.",
            }
        ),
        encoding="utf-8",
    )

    approval = apply_lane_runtime_thread_delivery_approval_signal(
        conn,
        Namespace(
            approval_signal=str(signal_path),
            now_utc="2026-06-21T16:29:00Z",
            path=str(tmp_path / "approval.md"),
            json_path=str(tmp_path / "approval-result.json"),
            no_db_record=True,
        ),
    )

    assert approval["ok"] is False
    assert approval["status"] == "rejected"
    assert "thread_id_for_tool mismatch" in approval["reason"]
    row = conn.execute(
        "SELECT status FROM lane_runtime_thread_deliveries WHERE delivery_id=?",
        (delivery["delivery_id"],),
    ).fetchone()
    assert row["status"] == "ready_to_send"


def test_lane_runtime_thread_delivery_approval_drafts_write_review_files_without_approving(
    tmp_path: Path,
) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch()])
    payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))
    delivery = payload["deliveries"][0]

    drafts = write_lane_runtime_thread_delivery_approval_drafts(
        conn,
        Namespace(
            now_utc="2026-06-21T16:30:00Z",
            max_deliveries=10,
            draft_dir=str(tmp_path / "approval-drafts"),
            path=str(tmp_path / "approval-drafts.md"),
            json_path=str(tmp_path / "approval-drafts.json"),
            no_db_record=True,
        ),
    )

    assert drafts["status"] == "approval_drafts_ready"
    assert drafts["counts"] == {
        "ready_deliveries_seen": 1,
        "drafts_written": 2,
        "send_approved_drafts": 1,
        "keep_parked_drafts": 1,
    }
    draft = next(item for item in drafts["drafts"] if item["decision"] == "send_approved")
    parked_draft = next(item for item in drafts["drafts"] if item["decision"] == "keep_parked")
    assert draft["delivery_id"] == delivery["delivery_id"]
    assert draft["thread_id_for_tool"] == "owner-thread"
    assert draft["active_signal_path"].endswith(f"{delivery['delivery_id']}-send-approved.json")
    assert parked_draft["active_signal_path"].endswith(f"{delivery['delivery_id']}-keep-parked.json")
    draft_payload = json.loads(Path(draft["draft_path"]).read_text(encoding="utf-8"))
    assert draft_payload["decision"] == "send_approved"
    assert draft_payload["delivery_id"] == delivery["delivery_id"]
    assert draft_payload["thread_id_for_tool"] == "owner-thread"
    assert draft_payload["attestation"].startswith("No credential")
    parked_payload = json.loads(Path(parked_draft["draft_path"]).read_text(encoding="utf-8"))
    assert parked_payload["decision"] == "keep_parked"
    assert parked_payload["delivery_id"] == delivery["delivery_id"]
    assert "do not send" in parked_payload["scope"]
    assert drafts["zero_side_effect_boundary"]["thread_messages_sent"] == 0
    row = conn.execute(
        "SELECT status, delivery_attempts FROM lane_runtime_thread_deliveries WHERE delivery_id=?",
        (delivery["delivery_id"],),
    ).fetchone()
    assert dict(row) == {"status": "ready_to_send", "delivery_attempts": 0}


def test_lane_runtime_thread_delivery_approval_draft_promotion_writes_active_signal_without_approving(
    tmp_path: Path,
) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch()])
    payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))
    delivery = payload["deliveries"][0]
    drafts = write_lane_runtime_thread_delivery_approval_drafts(
        conn,
        Namespace(
            now_utc="2026-06-21T16:30:00Z",
            max_deliveries=10,
            draft_dir=str(tmp_path / "approval-drafts"),
            path=str(tmp_path / "approval-drafts.md"),
            json_path=str(tmp_path / "approval-drafts.json"),
            no_db_record=True,
        ),
    )
    draft_path = Path(next(item for item in drafts["drafts"] if item["decision"] == "send_approved")["draft_path"])
    active_dir = tmp_path / "active-approvals"

    promotion = promote_lane_runtime_thread_delivery_approval_draft(
        conn,
        Namespace(
            draft_path=str(draft_path),
            active_signal_dir=str(active_dir),
            confirm_reviewed=True,
            now_utc="2026-06-21T16:31:00Z",
            path=str(tmp_path / "promotion.md"),
            json_path=str(tmp_path / "promotion.json"),
            no_db_record=True,
        ),
    )

    assert promotion["status"] == "approval_signal_ready"
    assert promotion["ok"] is True
    assert promotion["delivery_id"] == delivery["delivery_id"]
    active_signal = Path(promotion["active_signal_path"])
    assert active_signal.exists()
    assert active_signal.parent == active_dir
    active_payload = json.loads(active_signal.read_text(encoding="utf-8"))
    assert active_payload["delivery_id"] == delivery["delivery_id"]
    assert active_payload["thread_id_for_tool"] == "owner-thread"
    assert promotion["zero_side_effect_boundary"]["thread_messages_sent"] == 0
    row = conn.execute(
        "SELECT status, delivery_attempts FROM lane_runtime_thread_deliveries WHERE delivery_id=?",
        (delivery["delivery_id"],),
    ).fetchone()
    assert dict(row) == {"status": "ready_to_send", "delivery_attempts": 0}


def test_lane_runtime_thread_delivery_keep_parked_draft_promotion_can_be_applied(
    tmp_path: Path,
) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch()])
    payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))
    delivery = payload["deliveries"][0]
    drafts = write_lane_runtime_thread_delivery_approval_drafts(
        conn,
        Namespace(
            now_utc="2026-06-21T16:30:00Z",
            max_deliveries=10,
            draft_dir=str(tmp_path / "approval-drafts"),
            path=str(tmp_path / "approval-drafts.md"),
            json_path=str(tmp_path / "approval-drafts.json"),
            no_db_record=True,
        ),
    )
    draft_path = Path(next(item for item in drafts["drafts"] if item["decision"] == "keep_parked")["draft_path"])
    active_dir = tmp_path / "active-approvals"

    promotion = promote_lane_runtime_thread_delivery_approval_draft(
        conn,
        Namespace(
            draft_path=str(draft_path),
            active_signal_dir=str(active_dir),
            confirm_reviewed=True,
            now_utc="2026-06-21T16:31:00Z",
            path=str(tmp_path / "promotion.md"),
            json_path=str(tmp_path / "promotion.json"),
            no_db_record=True,
        ),
    )

    assert promotion["status"] == "approval_signal_ready"
    assert promotion["ok"] is True
    assert promotion["decision"] == "keep_parked"
    active_signal = Path(promotion["active_signal_path"])
    assert active_signal.name.endswith("-keep-parked.json")
    active_payload = json.loads(active_signal.read_text(encoding="utf-8"))
    assert active_payload["decision"] == "keep_parked"
    row_before_apply = conn.execute(
        "SELECT status, delivery_attempts FROM lane_runtime_thread_deliveries WHERE delivery_id=?",
        (delivery["delivery_id"],),
    ).fetchone()
    assert dict(row_before_apply) == {"status": "ready_to_send", "delivery_attempts": 0}

    approval = apply_lane_runtime_thread_delivery_approval_signal(
        conn,
        Namespace(
            approval_signal=str(active_signal),
            now_utc="2026-06-21T16:32:00Z",
            path=str(tmp_path / "approval.md"),
            json_path=str(tmp_path / "approval-result.json"),
            no_db_record=True,
        ),
    )

    assert approval["ok"] is True
    assert approval["status"] == "send_approval_parked"
    assert approval["zero_side_effect_boundary"]["thread_messages_sent"] == 0
    row_after_apply = conn.execute(
        "SELECT status, delivery_attempts, last_error FROM lane_runtime_thread_deliveries WHERE delivery_id=?",
        (delivery["delivery_id"],),
    ).fetchone()
    assert dict(row_after_apply) == {
        "status": "send_approval_parked",
        "delivery_attempts": 0,
        "last_error": "human kept parked through approval signal",
    }


def test_lane_runtime_thread_delivery_approval_draft_promotion_requires_confirm_reviewed(
    tmp_path: Path,
) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch()])
    write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))
    drafts = write_lane_runtime_thread_delivery_approval_drafts(
        conn,
        Namespace(
            now_utc="2026-06-21T16:30:00Z",
            max_deliveries=10,
            draft_dir=str(tmp_path / "approval-drafts"),
            path=str(tmp_path / "approval-drafts.md"),
            json_path=str(tmp_path / "approval-drafts.json"),
            no_db_record=True,
        ),
    )

    promotion = promote_lane_runtime_thread_delivery_approval_draft(
        conn,
        Namespace(
            draft_path=drafts["drafts"][0]["draft_path"],
            active_signal_dir=str(tmp_path / "active-approvals"),
            confirm_reviewed=False,
            now_utc="2026-06-21T16:31:00Z",
            path=str(tmp_path / "promotion.md"),
            json_path=str(tmp_path / "promotion.json"),
            no_db_record=True,
        ),
    )

    assert promotion["ok"] is False
    assert promotion["status"] == "rejected"
    assert promotion["reason"] == "missing_confirm_reviewed"


def test_lane_runtime_thread_delivery_send_preflight_writes_exact_send_packets_for_approved_delivery(
    tmp_path: Path,
) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch()])
    payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))
    delivery = payload["deliveries"][0]
    prompt_text = Path(delivery["prompt_path"]).read_text(encoding="utf-8")
    conn.execute(
        "UPDATE lane_runtime_thread_deliveries SET status='send_approved' WHERE delivery_id=?",
        (delivery["delivery_id"],),
    )
    conn.commit()

    preflight = write_lane_runtime_thread_delivery_send_preflight(
        conn,
        Namespace(
            now_utc="2026-06-21T16:31:00Z",
            max_deliveries=10,
            path=str(tmp_path / "send-preflight.md"),
            json_path=str(tmp_path / "send-preflight.json"),
            no_db_record=True,
        ),
    )

    assert preflight["status"] == "approved_sends_ready"
    assert preflight["counts"] == {
        "approved_deliveries_seen": 1,
        "send_packets_ready": 1,
        "blocked_missing_prompt": 0,
    }
    packet = preflight["send_packets"][0]
    assert packet["delivery_id"] == delivery["delivery_id"]
    assert packet["thread_id_for_tool"] == "owner-thread"
    assert packet["prompt_path"] == delivery["prompt_path"]
    assert packet["prompt_text"] == prompt_text
    assert packet["send_authority"] == "approved_thread_delivery"
    assert packet["auto_wake_authorized"] is False
    assert packet["receipt_command"].endswith(
        f"record-lane-runtime-thread-delivery --delivery-id {delivery['delivery_id']} --status delivered"
    )
    assert preflight["zero_side_effect_boundary"]["thread_messages_sent"] == 0


def test_lane_runtime_thread_delivery_send_preflight_auto_wakes_safe_ready_delivery(
    tmp_path: Path,
) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch()])
    payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))
    delivery = payload["deliveries"][0]

    preflight = write_lane_runtime_thread_delivery_send_preflight(
        conn,
        Namespace(
            now_utc="2026-06-21T16:31:00Z",
            max_deliveries=10,
            include_safe_ready_deliveries=True,
            auto_authorize_approved_deliveries=False,
            path=str(tmp_path / "safe-auto-wake.md"),
            json_path=str(tmp_path / "safe-auto-wake.json"),
            no_db_record=True,
        ),
    )

    assert preflight["status"] == "auto_wake_sends_ready"
    assert preflight["counts"]["approved_deliveries_seen"] == 0
    assert preflight["counts"]["safe_ready_deliveries_seen"] == 1
    assert preflight["counts"]["auto_wake_packets_ready"] == 1
    packet = preflight["send_packets"][0]
    assert packet["delivery_id"] == delivery["delivery_id"]
    assert packet["send_authority"] == "safe_local_continuity_wake"
    assert packet["auto_wake_authorized"] is True
    assert packet["safety_assessment"]["safe"] is True
    assert "Work locally only" in packet["prompt_text"]


def test_lane_runtime_thread_delivery_send_preflight_ignores_ready_row_with_delivered_at(
    tmp_path: Path,
) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch()])
    payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))
    delivery_id = payload["deliveries"][0]["delivery_id"]
    conn.execute(
        """
        UPDATE lane_runtime_thread_deliveries
        SET delivered_at='2026-06-21T16:30:00Z',
            last_error='superseded but malformed status survived',
            updated_at='2026-06-21T16:31:00Z'
        WHERE delivery_id=?
        """,
        (delivery_id,),
    )
    conn.commit()

    preflight = write_lane_runtime_thread_delivery_send_preflight(
        conn,
        Namespace(
            now_utc="2026-06-21T16:32:00Z",
            max_deliveries=10,
            include_safe_ready_deliveries=True,
            auto_authorize_approved_deliveries=False,
            path=str(tmp_path / "safe-auto-wake.md"),
            json_path=str(tmp_path / "safe-auto-wake.json"),
            no_db_record=True,
        ),
    )

    assert preflight["status"] == "no_approved_sends"
    assert preflight["counts"]["safe_ready_deliveries_seen"] == 0
    assert preflight["counts"]["auto_wake_packets_ready"] == 0
    assert preflight["send_packets"] == []


def test_lane_runtime_thread_delivery_send_preflight_auto_wakes_active_delivered_after_capacity_refresh(
    tmp_path: Path,
) -> None:
    conn = _conn()
    drain_report = _drain_report(tmp_path, [_leased_dispatch()])
    payload = write_lane_runtime_thread_delivery_outbox(conn, _outbox_args(tmp_path, drain_report))
    delivery = payload["deliveries"][0]
    conn.execute(
        """
        INSERT INTO account_capacity_sessions(
          session_id, surface, account_label, status, concurrency_limit,
          active_lease_count, last_refresh_utc, created_at, updated_at
        )
        VALUES('codex-main', 'codex', 'main', 'available', 1, 1,
               '2026-06-21T16:40:00Z', '2026-06-21T16:00:00Z', '2026-06-21T16:40:00Z')
        """
    )
    conn.execute(
        """
        UPDATE lane_runtime_thread_deliveries
        SET status='delivered',
            delivered_at='2026-06-21T16:30:00Z',
            updated_at='2026-06-21T16:30:00Z'
        WHERE delivery_id=?
        """,
        (delivery["delivery_id"],),
    )
    conn.commit()

    preflight = write_lane_runtime_thread_delivery_send_preflight(
        conn,
        Namespace(
            now_utc="2026-06-21T16:41:00Z",
            max_deliveries=10,
            include_safe_ready_deliveries=True,
            include_active_resume_deliveries=True,
            auto_authorize_approved_deliveries=False,
            path=str(tmp_path / "active-resume.md"),
            json_path=str(tmp_path / "active-resume.json"),
            no_db_record=True,
        ),
    )

    assert preflight["status"] == "auto_wake_sends_ready"
    assert preflight["counts"]["safe_ready_deliveries_seen"] == 0
    assert preflight["counts"]["active_resume_deliveries_seen"] == 1
    assert preflight["counts"]["auto_wake_packets_ready"] == 1
    packet = preflight["send_packets"][0]
    assert packet["delivery_id"] == delivery["delivery_id"]
    assert packet["source_delivery_status"] == "delivered"
    assert packet["send_authority"] == "safe_local_continuity_wake"
    assert packet["auto_wake_authorized"] is True


def test_lane_runtime_thread_delivery_send_preflight_blocks_unsafe_ready_prompt(
    tmp_path: Path,
) -> None:
    conn = _conn()
    prompt_path = tmp_path / "manual-prompt.md"
    prompt_path.write_text("Manual prompt without the continuity boundary", encoding="utf-8")
    conn.execute(
        """
        INSERT INTO lane_runtime_thread_deliveries(
          delivery_id, task_id, lane_id, session_id, owner_agent_id, owner_thread_id,
          packet_path, prompt_path, status, delivery_attempts, delivered_at, last_error,
          created_at, updated_at
        )
        VALUES(
          'delivery-manual', 'task-premium', 'premium_customer_intake', 'codex-main',
          'owner-agent', 'codex-thread:owner-thread', 'packet.md', ?, 'ready_to_send',
          0, NULL, NULL, '2026-06-21T16:30:00Z', '2026-06-21T16:30:00Z'
        )
        """,
        (str(prompt_path),),
    )
    conn.commit()

    preflight = write_lane_runtime_thread_delivery_send_preflight(
        conn,
        Namespace(
            now_utc="2026-06-21T16:31:00Z",
            max_deliveries=10,
            include_safe_ready_deliveries=True,
            auto_authorize_approved_deliveries=False,
            path=str(tmp_path / "unsafe-auto-wake.md"),
            json_path=str(tmp_path / "unsafe-auto-wake.json"),
            no_db_record=True,
        ),
    )

    assert preflight["status"] == "blocked"
    assert preflight["counts"]["send_packets_ready"] == 0
    assert preflight["counts"]["blocked_auto_wake_safety"] == 1
    blocked = preflight["blocked_deliveries"][0]
    assert blocked["reason"] == "prompt_not_generated_by_local_continuity_delivery_contract"


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
    approval = parser.parse_args(
        [
            "apply-lane-runtime-thread-delivery-approval",
            "--approval-signal",
            "approval.json",
        ]
    )
    send_preflight = parser.parse_args(
        [
            "write-lane-runtime-thread-delivery-send-preflight",
            "--max-deliveries",
            "3",
            "--include-safe-ready-deliveries",
            "--auto-authorize-approved-deliveries",
        ]
    )
    approval_drafts = parser.parse_args(
        [
            "write-lane-runtime-thread-delivery-approval-drafts",
            "--max-deliveries",
            "4",
        ]
    )
    promotion = parser.parse_args(
        [
            "promote-lane-runtime-thread-delivery-approval-draft",
            "--draft-path",
            "draft.json",
            "--confirm-reviewed",
        ]
    )

    assert outbox.cmd == "write-lane-runtime-thread-delivery-outbox"
    assert outbox.drain_report == "drain.json"
    assert receipt.cmd == "record-lane-runtime-thread-delivery"
    assert receipt.delivery_id == "delivery-task"
    assert receipt.status == "delivered"
    assert approval.cmd == "apply-lane-runtime-thread-delivery-approval"
    assert approval.approval_signal == "approval.json"
    assert send_preflight.cmd == "write-lane-runtime-thread-delivery-send-preflight"
    assert send_preflight.max_deliveries == 3
    assert send_preflight.include_safe_ready_deliveries is True
    assert send_preflight.auto_authorize_approved_deliveries is True
    assert approval_drafts.cmd == "write-lane-runtime-thread-delivery-approval-drafts"
    assert approval_drafts.max_deliveries == 4
    assert promotion.cmd == "promote-lane-runtime-thread-delivery-approval-draft"
    assert promotion.draft_path == "draft.json"
    assert promotion.confirm_reviewed is True
