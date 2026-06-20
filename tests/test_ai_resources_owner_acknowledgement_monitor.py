import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.ai_resources_owner_acknowledgement_monitor import (  # noqa: E402
    monitor_ai_resources_owner_acknowledgements,
)
from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    old = "2026-06-21T09:00:00Z"
    recent = "2026-06-21T10:50:00Z"
    for lane_id, status, updated_at in [
        ("youtube_content_channels", "new", old),
        ("paid_code_bounties", "in_progress", recent),
        ("prediction_market_research", "complete", old),
        ("ai_resources_lab", "blocked", recent),
    ]:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
              evidence_required, next_action, created_at, updated_at
            )
            VALUES(?, ?, ?, ?, 90, ?, ?, 'ack packet', 'write local acknowledgement', ?, ?)
            """,
            (
                f"task-ack-{lane_id}",
                lane_id,
                f"ack {lane_id}",
                status,
                f"lane-manager-{lane_id}-20260621",
                f"customer-input-test:owner-acknowledgement:{lane_id}",
                old,
                updated_at,
            ),
        )
    conn.commit()
    return conn


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        input_id="customer-input-test",
        stale_after_minutes=60,
        now_utc="2026-06-21T11:00:00Z",
        json_path=str(tmp_path / "monitor.json"),
        path=str(tmp_path / "monitor.md"),
        no_db_record=no_db_record,
    )


def test_owner_acknowledgement_monitor_flags_stale_and_blocked_without_mutating_tasks(tmp_path: Path) -> None:
    conn = _conn()
    payload = monitor_ai_resources_owner_acknowledgements(conn, _args(tmp_path, no_db_record=False))

    assert payload["status"] == "attention_needed"
    assert payload["counts"]["total"] == 4
    assert payload["counts"]["stale_unacknowledged"] == 1
    assert payload["counts"]["active"] == 1
    assert payload["counts"]["complete"] == 1
    assert payload["counts"]["blocked"] == 1
    assert payload["counts"]["requires_ai_resources_attention"] == 2
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False

    source_statuses = {
        row["task_id"]: row["status"]
        for row in conn.execute(
            "select task_id,status from tasks where duplicate_key like 'customer-input-test:owner-acknowledgement:%'"
        )
    }
    assert source_statuses == {
        "task-ack-ai_resources_lab": "blocked",
        "task-ack-paid_code_bounties": "in_progress",
        "task-ack-prediction_market_research": "complete",
        "task-ack-youtube_content_channels": "new",
    }

    audit = conn.execute(
        "select lane_id,status,evidence_required from tasks where task_id='task-ai-resources-owner-acknowledgement-monitor-v1-customer-input-test'"
    ).fetchone()
    assert audit["lane_id"] == "ai_resources_lab"
    assert audit["status"] == "complete"
    assert audit["evidence_required"] == payload["md_path"]


def test_owner_acknowledgement_monitor_report_only_skips_db_record(tmp_path: Path) -> None:
    conn = _conn()
    payload = monitor_ai_resources_owner_acknowledgements(conn, _args(tmp_path, no_db_record=True))

    audit = conn.execute(
        "select 1 from tasks where task_id='task-ai-resources-owner-acknowledgement-monitor-v1-customer-input-test'"
    ).fetchone()
    assert payload["status"] == "attention_needed"
    assert audit is None


def test_owner_acknowledgement_monitor_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "monitor-ai-resources-owner-acknowledgements",
            "--input-id",
            "customer-input-test",
            "--stale-after-minutes",
            "15",
        ]
    )

    assert args.cmd == "monitor-ai-resources-owner-acknowledgements"
    assert args.input_id == "customer-input-test"
    assert args.stale_after_minutes == 15
