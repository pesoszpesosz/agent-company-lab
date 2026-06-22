import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.premium_customer_followup_monitor import monitor_premium_customer_followups  # noqa: E402
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    ts = "2026-06-20T09:00:00Z"
    conn.execute(
        """
        INSERT INTO lanes(
          lane_id, department, status, owner_agent_id, owner_thread_id, agent_types_json,
          examples_json, promotion_gates_json, service_workers_required_json,
          side_effects_json, global_gates_json, notes, created_at, updated_at
        )
        VALUES('ai_resources_lab', 'AI Resources', 'active', 'lane-manager-ai_resources_lab-20260620',
               'thread-test', '[]', '[]', '[]', '[]', '[]', '[]', NULL, ?, ?)
        """,
        (ts, ts),
    )
    tasks = [
        (
            "task-followup-new",
            "ai_resources_lab",
            "new",
            "lane-manager-ai_resources_lab-20260620",
            "customer-input-test:lane-followup:ai_resources_lab",
            "2026-06-20T10:00:00Z",
        ),
        (
            "task-followup-active",
            "ai_resources_lab",
            "in_progress",
            "lane-manager-ai_resources_lab-20260620",
            "customer-input-test:lane-followup:active",
            "2026-06-20T11:40:00Z",
        ),
        (
            "task-followup-ownerless",
            "missing_lane",
            "new",
            None,
            "customer-input-test:lane-followup:missing_lane",
            "2026-06-20T11:59:00Z",
        ),
    ]
    for task_id, lane_id, status, owner, duplicate_key, updated in tasks:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
              evidence_required, next_action, created_at, updated_at
            )
            VALUES(?, ?, ?, ?, 80, ?, ?, 'route packet', 'do local work', ?, ?)
            """,
            (task_id, lane_id, task_id, status, owner, duplicate_key, updated, updated),
        )
    conn.commit()
    return conn


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        input_id="customer-input-test",
        stale_after_minutes=60,
        now_utc="2026-06-20T12:00:00Z",
        json_path=str(tmp_path / "monitor.json"),
        path=str(tmp_path / "monitor.md"),
        ledger_json=str(tmp_path / "ledger.json"),
        ledger_md=str(tmp_path / "ledger.md"),
        update_feed_json=str(tmp_path / "feed.json"),
        update_feed_md=str(tmp_path / "feed.md"),
        no_db_record=no_db_record,
    )


def test_followup_monitor_classifies_stale_active_and_ownerless(tmp_path: Path) -> None:
    payload = monitor_premium_customer_followups(_conn(), _args(tmp_path, no_db_record=True))
    statuses = {item["task_id"]: item["monitor_status"] for item in payload["followup_tasks"]}

    assert payload["status"] == "attention_needed"
    assert statuses["task-followup-new"] == "stale_unacknowledged"
    assert statuses["task-followup-active"] == "active"
    assert statuses["task-followup-ownerless"] == "ownerless"
    assert payload["counts"]["requires_intake_attention"] == 2
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False


def test_followup_monitor_treats_completed_owner_acknowledgement_as_open_without_attention(
    tmp_path: Path,
) -> None:
    conn = _conn()
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, completed_at
        )
        VALUES(
          'task-owner-ack-ai-resources', 'ai_resources_lab', 'Owner ack', 'complete',
          90, 'lane-manager-ai_resources_lab-20260620',
          'customer-input-test:owner-acknowledgement:ai_resources_lab',
          'ack evidence', 'continue with existing owner',
          '2026-06-20T10:30:00Z', '2026-06-20T11:50:00Z', '2026-06-20T11:50:00Z'
        )
        """
    )
    conn.commit()

    payload = monitor_premium_customer_followups(conn, _args(tmp_path, no_db_record=True))
    item = next(item for item in payload["followup_tasks"] if item["task_id"] == "task-followup-new")

    assert item["monitor_status"] == "owner_acknowledged_open"
    assert item["requires_intake_attention"] is False
    assert item["owner_acknowledgement_task_id"] == "task-owner-ack-ai-resources"
    assert payload["counts"]["owner_acknowledged_open"] == 1
    assert payload["counts"]["requires_intake_attention"] == 1


def test_followup_monitor_records_audit_rows_without_claiming_followups(tmp_path: Path) -> None:
    conn = _conn()
    ledger = {
        "schema_version": "customer_request_routing_ledger.v1",
        "generated_utc": "2026-06-20T09:00:00Z",
        "owner_agent_id": "premium-customer-intake-agent-20260620",
        "status": "active_local_ledger",
        "entries": [{"input_id": "customer-input-test", "input_class": "new_request", "primary_route": "ai_resources_lab", "status": "synthesized", "next_artifact": "x"}],
    }
    Path(tmp_path / "ledger.json").write_text(json.dumps(ledger), encoding="utf-8")

    payload = monitor_premium_customer_followups(conn, _args(tmp_path, no_db_record=False))
    followup_rows = [
        dict(row)
        for row in conn.execute(
            "SELECT task_id, status FROM tasks WHERE duplicate_key LIKE 'customer-input-test:lane-followup:%' ORDER BY task_id"
        )
    ]
    trace = conn.execute(
        "SELECT event_type FROM trace_events WHERE event_type = 'premium_customer_followup_monitor_checked'"
    ).fetchone()
    updated_ledger = json.loads(Path(tmp_path / "ledger.json").read_text(encoding="utf-8"))

    assert payload["counts"]["total"] == 3
    assert [row["status"] for row in followup_rows] == ["in_progress", "new", "new"]
    assert trace is not None
    assert updated_ledger["entries"][0]["followup_monitor"]["status"] == "attention_needed"
