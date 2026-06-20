import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.ai_resources_owner_acknowledgement_dispatch import (  # noqa: E402
    RESPONSE_OPTIONS,
    dispatch_ai_resources_owner_acknowledgements,
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
        ("paid_code_bounties", "in_progress", old),
        ("prediction_market_research", "complete", old),
        ("local_trading_strategy_research", "new", recent),
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
        json_path=str(tmp_path / "dispatch.json"),
        path=str(tmp_path / "dispatch.md"),
        no_db_record=no_db_record,
    )


def test_owner_acknowledgement_dispatch_writes_response_contract_without_mutating_sources(tmp_path: Path) -> None:
    conn = _conn()
    payload = dispatch_ai_resources_owner_acknowledgements(conn, _args(tmp_path, no_db_record=False))

    assert payload["schema_version"] == "ai_resources_owner_acknowledgement_dispatch.v1"
    assert payload["dispatch_id"] == "ai-resources-owner-acknowledgement-dispatch-v1-customer-input-test"
    assert payload["status"] == "dispatch_ready"
    assert payload["counts"] == {
        "dispatch_items": 2,
        "fresh_open_acknowledgements": 1,
        "terminal_acknowledgements": 1,
        "total_owner_acknowledgements": 4,
    }
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False

    items_by_lane = {item["lane_id"]: item for item in payload["dispatch_items"]}
    assert set(items_by_lane) == {"paid_code_bounties", "youtube_content_channels"}
    for item in items_by_lane.values():
        assert item["response_options"] == RESPONSE_OPTIONS
        assert item["existing_owner_agent_id"].startswith("lane-manager-")
        assert item["source_task_id"].startswith("task-ack-")
        assert item["age_minutes"] == 120
        assert item["next_action"] == "Send this response contract to the existing lane owner; do not create a duplicate agent."

    source_statuses = {
        row["task_id"]: row["status"]
        for row in conn.execute(
            "select task_id,status from tasks where duplicate_key like 'customer-input-test:owner-acknowledgement:%'"
        )
    }
    assert source_statuses == {
        "task-ack-local_trading_strategy_research": "new",
        "task-ack-paid_code_bounties": "in_progress",
        "task-ack-prediction_market_research": "complete",
        "task-ack-youtube_content_channels": "new",
    }

    audit = conn.execute(
        "select lane_id,status,evidence_required from tasks where task_id='task-ai-resources-owner-acknowledgement-dispatch-v1-customer-input-test'"
    ).fetchone()
    assert audit["lane_id"] == "ai_resources_lab"
    assert audit["status"] == "complete"
    assert audit["evidence_required"] == payload["md_path"]

    artifact_count = conn.execute(
        "select count(*) as c from artifacts where task_id='task-ai-resources-owner-acknowledgement-dispatch-v1-customer-input-test'"
    ).fetchone()["c"]
    assert artifact_count == 2


def test_owner_acknowledgement_dispatch_report_only_skips_db_record(tmp_path: Path) -> None:
    conn = _conn()
    payload = dispatch_ai_resources_owner_acknowledgements(conn, _args(tmp_path, no_db_record=True))

    audit = conn.execute(
        "select 1 from tasks where task_id='task-ai-resources-owner-acknowledgement-dispatch-v1-customer-input-test'"
    ).fetchone()
    assert payload["status"] == "dispatch_ready"
    assert audit is None


def test_owner_acknowledgement_dispatch_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-ai-resources-owner-acknowledgement-dispatch",
            "--input-id",
            "customer-input-test",
            "--stale-after-minutes",
            "15",
        ]
    )

    assert args.cmd == "write-ai-resources-owner-acknowledgement-dispatch"
    assert args.input_id == "customer-input-test"
    assert args.stale_after_minutes == 15
