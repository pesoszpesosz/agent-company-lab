import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.ai_resources_owner_acknowledgement_requests import (  # noqa: E402
    request_ai_resources_owner_acknowledgements,
)
from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    ts = "2026-06-21T09:00:00Z"
    for lane_id, owner in [
        ("youtube_content_channels", "lane-manager-youtube_content_channels-20260620"),
        ("paid_code_bounties", "lane-manager-paid_code_bounties-20260620"),
        ("prediction_market_research", "lane-manager-prediction_market_research-20260620"),
        ("ai_resources_lab", "lane-manager-ai_resources_lab-20260620"),
    ]:
        conn.execute(
            """
            INSERT INTO lanes(
              lane_id, department, status, owner_agent_id, owner_thread_id, agent_types_json,
              examples_json, promotion_gates_json, service_workers_required_json,
              side_effects_json, global_gates_json, notes, created_at, updated_at
            )
            VALUES(?, 'Test', 'active', ?, 'thread-test', '[]', '[]', '[]', '[]', '[]', '[]', NULL, ?, ?)
            """,
            (lane_id, owner, ts, ts),
        )
    for lane_id, status in [
        ("youtube_content_channels", "new"),
        ("paid_code_bounties", "in_progress"),
        ("prediction_market_research", "new"),
    ]:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
              evidence_required, next_action, created_at, updated_at
            )
            VALUES(?, ?, ?, ?, 80, ?, ?, 'source evidence', 'source next action', ?, ?)
            """,
            (
                f"task-followup-{lane_id}",
                lane_id,
                f"source followup {lane_id}",
                status,
                f"lane-manager-{lane_id}-20260620",
                f"customer-input-test:lane-followup:{lane_id}",
                ts,
                ts,
            ),
        )
    conn.commit()
    return conn


def _triage(path: Path) -> Path:
    payload = {
        "schema_version": "ai_resources_customer_followup_triage.v1",
        "generated_utc": "2026-06-21T09:20:00Z",
        "status": "triage_ready",
        "input_id": "customer-input-test",
        "triage_items": [
            {
                "task_id": "task-followup-youtube_content_channels",
                "lane_id": "youtube_content_channels",
                "owner_agent_id": "lane-manager-youtube_content_channels-20260620",
                "task_status": "new",
                "decision": "reuse_existing_owner",
                "recommended_action": "Ask the existing lane owner to acknowledge.",
                "source_next_action": "source next action",
            },
            {
                "task_id": "task-followup-paid_code_bounties",
                "lane_id": "paid_code_bounties",
                "owner_agent_id": "lane-manager-paid_code_bounties-20260620",
                "task_status": "in_progress",
                "decision": "reuse_existing_owner",
                "recommended_action": "Ask the existing lane owner to acknowledge.",
                "source_next_action": "source next action",
            },
            {
                "task_id": "task-followup-prediction_market_research",
                "lane_id": "prediction_market_research",
                "owner_agent_id": "lane-manager-prediction_market_research-20260620",
                "task_status": "new",
                "decision": "park_with_revisit_condition",
                "recommended_action": "Park with revisit condition.",
                "source_next_action": "source next action",
            },
        ],
        "zero_side_effect_boundary": {"external_side_effects": False},
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        triage_report=str(_triage(tmp_path / "triage.json")),
        now_utc="2026-06-21T09:30:00Z",
        json_path=str(tmp_path / "ack.json"),
        path=str(tmp_path / "ack.md"),
        no_db_record=no_db_record,
    )


def test_owner_acknowledgement_requests_create_idempotent_owner_tasks_without_mutating_sources(tmp_path: Path) -> None:
    conn = _conn()
    payload = request_ai_resources_owner_acknowledgements(conn, _args(tmp_path, no_db_record=False))
    request_ai_resources_owner_acknowledgements(conn, _args(tmp_path, no_db_record=False))

    ack_tasks = [
        dict(row)
        for row in conn.execute(
            """
            SELECT task_id, lane_id, status, owner_agent_id, duplicate_key, evidence_required
            FROM tasks
            WHERE duplicate_key LIKE 'customer-input-test:owner-acknowledgement:%'
            ORDER BY lane_id
            """
        )
    ]
    source_statuses = {
        row["task_id"]: row["status"]
        for row in conn.execute(
            """
            SELECT task_id, status
            FROM tasks
            WHERE duplicate_key LIKE 'customer-input-test:lane-followup:%'
            ORDER BY task_id
            """
        )
    }

    assert payload["status"] == "acknowledgement_requests_ready"
    assert payload["counts"] == {"owner_acknowledgement_requested": 2, "skipped": 1, "total": 3}
    assert len(ack_tasks) == 2
    assert {task["lane_id"] for task in ack_tasks} == {"youtube_content_channels", "paid_code_bounties"}
    assert all(task["status"] == "new" for task in ack_tasks)
    assert all(task["owner_agent_id"] for task in ack_tasks)
    assert all(task["evidence_required"] == payload["md_path"] for task in ack_tasks)
    assert source_statuses == {
        "task-followup-paid_code_bounties": "in_progress",
        "task-followup-prediction_market_research": "new",
        "task-followup-youtube_content_channels": "new",
    }
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False


def test_owner_acknowledgement_report_only_writes_packet_without_db_rows(tmp_path: Path) -> None:
    conn = _conn()
    payload = request_ai_resources_owner_acknowledgements(conn, _args(tmp_path, no_db_record=True))

    rows = list(
        conn.execute(
            "SELECT task_id FROM tasks WHERE duplicate_key LIKE 'customer-input-test:owner-acknowledgement:%'"
        )
    )
    assert payload["status"] == "acknowledgement_requests_ready"
    assert rows == []


def test_owner_acknowledgement_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "request-ai-resources-owner-acknowledgements",
            "--triage-report",
            "reports/ai-resources-customer-followup-triage-v1-20260621.json",
        ]
    )

    assert args.cmd == "request-ai-resources-owner-acknowledgements"
    assert args.triage_report.endswith("ai-resources-customer-followup-triage-v1-20260621.json")
