import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.ai_resources_customer_followup_triage import triage_ai_resources_customer_followups  # noqa: E402
from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    ts = "2026-06-21T07:00:00Z"
    for lane_id, department, owner in [
        ("ai_resources_lab", "AI Resources", "lane-manager-ai_resources_lab-20260620"),
        ("youtube_content_channels", "Content", "lane-manager-youtube_content_channels-20260620"),
        ("paid_code_bounties", "Paid Code", "lane-manager-paid_code_bounties-20260620"),
        ("prediction_market_research", "Prediction Markets", "lane-manager-prediction_market_research-20260620"),
    ]:
        conn.execute(
            """
            INSERT INTO lanes(
              lane_id, department, status, owner_agent_id, owner_thread_id, agent_types_json,
              examples_json, promotion_gates_json, service_workers_required_json,
              side_effects_json, global_gates_json, notes, created_at, updated_at
            )
            VALUES(?, ?, 'active', ?, 'thread-test', '[]', '[]', '[]', '[]', '[]', '[]', NULL, ?, ?)
            """,
            (lane_id, department, owner, ts, ts),
        )
    for task_id, lane_id, status, owner, monitor_status in [
        ("task-followup-new", "youtube_content_channels", "new", "lane-manager-youtube_content_channels-20260620", "stale_unacknowledged"),
        ("task-followup-active", "paid_code_bounties", "in_progress", "lane-manager-paid_code_bounties-20260620", "stale_active"),
        ("task-followup-other", "prediction_market_research", "needs_clarity", "lane-manager-prediction_market_research-20260620", "stale_other"),
        ("task-followup-blocked", "ai_resources_lab", "blocked", "lane-manager-ai_resources_lab-20260620", "blocked"),
    ]:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
              evidence_required, next_action, created_at, updated_at
            )
            VALUES(?, ?, ?, ?, 80, ?, ?, 'route packet', ?, ?, ?)
            """,
            (
                task_id,
                lane_id,
                f"{monitor_status} followup",
                status,
                owner,
                f"customer-input-test:lane-followup:{lane_id}",
                f"source next action for {task_id}",
                ts,
                ts,
            ),
        )
    conn.commit()
    return conn


def _escalation(path: Path) -> Path:
    payload = {
        "schema_version": "premium_customer_followup_escalation.v1",
        "generated_utc": "2026-06-21T07:30:00Z",
        "status": "escalation_needed",
        "input_id": "customer-input-test",
        "target_surface": "ai_resources_lab",
        "summary": "Four follow-up tasks require AI Resources triage.",
        "escalation_items": [
            {
                "task_id": "task-followup-new",
                "lane_id": "youtube_content_channels",
                "task_status": "new",
                "monitor_status": "stale_unacknowledged",
                "owner_agent_id": "lane-manager-youtube_content_channels-20260620",
                "current_next_action": "source next action for task-followup-new",
                "target_surface": "ai_resources_lab",
            },
            {
                "task_id": "task-followup-active",
                "lane_id": "paid_code_bounties",
                "task_status": "in_progress",
                "monitor_status": "stale_active",
                "owner_agent_id": "lane-manager-paid_code_bounties-20260620",
                "current_next_action": "source next action for task-followup-active",
                "target_surface": "ai_resources_lab",
            },
            {
                "task_id": "task-followup-other",
                "lane_id": "prediction_market_research",
                "task_status": "needs_clarity",
                "monitor_status": "stale_other",
                "owner_agent_id": "lane-manager-prediction_market_research-20260620",
                "current_next_action": "source next action for task-followup-other",
                "target_surface": "ai_resources_lab",
            },
            {
                "task_id": "task-followup-blocked",
                "lane_id": "ai_resources_lab",
                "task_status": "blocked",
                "monitor_status": "blocked",
                "owner_agent_id": "lane-manager-ai_resources_lab-20260620",
                "current_next_action": "source next action for task-followup-blocked",
                "target_surface": "ceo_decision_batch",
            },
        ],
        "zero_side_effect_boundary": {"external_side_effects": False},
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        escalation_report=str(_escalation(tmp_path / "escalation.json")),
        now_utc="2026-06-21T08:00:00Z",
        json_path=str(tmp_path / "triage.json"),
        path=str(tmp_path / "triage.md"),
        no_db_record=no_db_record,
    )


def test_ai_resources_triage_classifies_escalation_items_without_mutating_followups(tmp_path: Path) -> None:
    conn = _conn()
    payload = triage_ai_resources_customer_followups(conn, _args(tmp_path, no_db_record=False))

    assert payload["status"] == "triage_ready"
    assert payload["counts"]["reuse_existing_owner"] == 1
    assert payload["counts"]["evolve_existing_agent"] == 1
    assert payload["counts"]["park_with_revisit_condition"] == 1
    assert payload["counts"]["ceo_decision_batch"] == 1
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False

    source_statuses = {
        row["task_id"]: row["status"]
        for row in conn.execute(
            "select task_id,status from tasks where duplicate_key like 'customer-input-test:lane-followup:%'"
        )
    }
    assert source_statuses == {
        "task-followup-new": "new",
        "task-followup-active": "in_progress",
        "task-followup-other": "needs_clarity",
        "task-followup-blocked": "blocked",
    }

    audit = conn.execute(
        "select lane_id,status,evidence_required from tasks where task_id='task-ai-resources-customer-followup-triage-v1-customer-input-test'"
    ).fetchone()
    assert audit["lane_id"] == "ai_resources_lab"
    assert audit["status"] == "complete"
    assert audit["evidence_required"] == payload["md_path"]


def test_ai_resources_triage_report_only_skips_db_record(tmp_path: Path) -> None:
    conn = _conn()
    payload = triage_ai_resources_customer_followups(conn, _args(tmp_path, no_db_record=True))

    audit = conn.execute(
        "select 1 from tasks where task_id='task-ai-resources-customer-followup-triage-v1-customer-input-test'"
    ).fetchone()
    assert payload["status"] == "triage_ready"
    assert audit is None


def test_ai_resources_triage_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "triage-ai-resources-customer-followups",
            "--escalation-report",
            "reports/customer-followup-escalation-v1-20260620.json",
        ]
    )

    assert args.cmd == "triage-ai-resources-customer-followups"
    assert args.escalation_report.endswith("customer-followup-escalation-v1-20260620.json")
