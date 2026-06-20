import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.premium_customer_followup_escalation import escalate_premium_customer_followups  # noqa: E402
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
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at
        )
        VALUES('task-followup-stale', 'ai_resources_lab', 'stale followup', 'new', 80,
               'lane-manager-ai_resources_lab-20260620',
               'customer-input-test:lane-followup:ai_resources_lab',
               'route packet', 'do local work', ?, ?)
        """,
        (ts, ts),
    )
    conn.commit()
    return conn


def _monitor(path: Path, attention: bool = True) -> Path:
    payload = {
        "schema_version": "premium_customer_followup_monitor.v1",
        "generated_utc": "2026-06-20T12:00:00Z",
        "status": "attention_needed" if attention else "clear",
        "input_id": "customer-input-test",
        "counts": {"total": 1, "requires_intake_attention": 1 if attention else 0},
        "followup_tasks": [
            {
                "task_id": "task-followup-stale",
                "lane_id": "ai_resources_lab",
                "status": "new",
                "monitor_status": "stale_unacknowledged" if attention else "unacknowledged",
                "requires_intake_attention": attention,
                "priority": 80,
                "owner_agent_id": "lane-manager-ai_resources_lab-20260620",
                "next_action": "do local work",
                "age_minutes": 120,
            }
        ],
        "zero_side_effect_boundary": {"external_side_effects": False},
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _ledger(path: Path) -> Path:
    payload = {
        "schema_version": "customer_request_routing_ledger.v1",
        "generated_utc": "2026-06-20T09:00:00Z",
        "owner_agent_id": "premium-customer-intake-agent-20260620",
        "status": "active_local_ledger",
        "entries": [{"input_id": "customer-input-test", "input_class": "new_request", "primary_route": "ai_resources_lab", "status": "synthesized", "next_artifact": "x"}],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _args(tmp_path: Path, no_db_record: bool = False, attention: bool = True) -> Namespace:
    return Namespace(
        monitor_report=str(_monitor(tmp_path / "monitor.json", attention=attention)),
        target_surface="ai_resources_lab",
        now_utc="2026-06-20T12:30:00Z",
        json_path=str(tmp_path / "escalation.json"),
        path=str(tmp_path / "escalation.md"),
        ledger_json=str(_ledger(tmp_path / "ledger.json")),
        ledger_md=str(tmp_path / "ledger.md"),
        update_feed_json=str(tmp_path / "feed.json"),
        update_feed_md=str(tmp_path / "feed.md"),
        no_db_record=no_db_record,
    )


def test_followup_escalation_report_only_writes_packet(tmp_path: Path) -> None:
    payload = escalate_premium_customer_followups(_conn(), _args(tmp_path, no_db_record=True))

    assert payload["status"] == "escalation_needed"
    assert payload["escalation_task_id"] is None
    assert payload["escalation_items"][0]["target_surface"] == "ai_resources_lab"
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False


def test_followup_escalation_creates_single_triage_task_without_touching_followups(tmp_path: Path) -> None:
    conn = _conn()
    payload = escalate_premium_customer_followups(conn, _args(tmp_path, no_db_record=False))
    escalate_premium_customer_followups(conn, _args(tmp_path, no_db_record=False))

    followup = conn.execute("SELECT status FROM tasks WHERE task_id = 'task-followup-stale'").fetchone()
    triage_rows = [
        dict(row)
        for row in conn.execute(
            "SELECT task_id, lane_id, status, duplicate_key FROM tasks WHERE duplicate_key = 'customer-input-test:followup-escalation:ai_resources_lab'"
        )
    ]
    trace = conn.execute(
        "SELECT event_type FROM trace_events WHERE event_type = 'premium_customer_followup_escalation_written'"
    ).fetchone()
    ledger = json.loads(Path(tmp_path / "ledger.json").read_text(encoding="utf-8"))

    assert followup["status"] == "new"
    assert len(triage_rows) == 1
    assert triage_rows[0]["lane_id"] == "ai_resources_lab"
    assert triage_rows[0]["status"] == "new"
    assert payload["escalation_task_id"] == triage_rows[0]["task_id"]
    assert trace is not None
    assert ledger["entries"][0]["followup_escalation"]["status"] == "escalation_needed"
