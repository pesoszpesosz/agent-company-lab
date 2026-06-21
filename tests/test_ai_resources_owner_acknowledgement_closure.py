import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.ai_resources_owner_acknowledgement_closure import (  # noqa: E402
    close_ai_resources_owner_acknowledgements,
)
from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.schema import init_db  # noqa: E402


def _conn(tmp_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    old = "2026-06-21T09:00:00Z"
    evidence_path = tmp_path / "youtube-ack.md"
    evidence_path.write_text("# acknowledgement\n", encoding="utf-8")
    for lane_id, status in [
        ("youtube_content_channels", "new"),
        ("paid_code_bounties", "complete"),
        ("money_source_discovery", "new"),
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
                f"task-customer-input-test-owner-acknowledgement-{lane_id}",
                lane_id,
                f"ack {lane_id}",
                status,
                f"lane-manager-{lane_id}-20260621",
                f"customer-input-test:owner-acknowledgement:{lane_id}",
                old,
                old,
            ),
        )
    response_task_id = (
        "task-continuity-owner-response-task-acknowledgement_response_required-"
        "task-customer-input-test-owner-acknowledgement-youtube_content_channels"
    )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, completed_at
        )
        VALUES(?, 'youtube_content_channels', ?, 'complete', 90, ?, ?, ?, 'done', ?, ?, ?)
        """,
        (
            response_task_id,
            "Handle task-customer-input-test-owner-acknowledgement-youtube_content_channels",
            "lane-manager-youtube_content_channels-20260621",
            "customer-input-test:owner-acknowledgement-response:youtube_content_channels",
            str(evidence_path),
            old,
            old,
            old,
        ),
    )
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
        VALUES('artifact-youtube-ack', 'youtube_content_channels', ?, 'continuity_acknowledgement_next_action', ?, 'sha', 'ok', ?)
        """,
        (response_task_id, str(evidence_path), old),
    )
    conn.commit()
    return conn


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        input_id="customer-input-test",
        now_utc="2026-06-21T11:00:00Z",
        json_path=str(tmp_path / "closure.json"),
        path=str(tmp_path / "closure.md"),
        no_db_record=no_db_record,
    )


def test_owner_acknowledgement_closure_completes_sources_with_existing_evidence(tmp_path: Path) -> None:
    conn = _conn(tmp_path)
    payload = close_ai_resources_owner_acknowledgements(conn, _args(tmp_path))

    assert payload["schema_version"] == "ai_resources_owner_acknowledgement_closure.v1"
    assert payload["status"] == "closure_applied"
    assert payload["counts"] == {
        "source_acknowledgements": 3,
        "closure_candidates": 1,
        "closure_applied": 1,
        "already_terminal": 1,
        "missing_completed_response_evidence": 1,
    }
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False

    statuses = {
        row["lane_id"]: row["status"]
        for row in conn.execute(
            "SELECT lane_id,status FROM tasks WHERE duplicate_key LIKE 'customer-input-test:owner-acknowledgement:%'"
        )
    }
    assert statuses == {
        "money_source_discovery": "new",
        "paid_code_bounties": "complete",
        "youtube_content_channels": "complete",
    }

    linked = conn.execute(
        """
        SELECT kind, task_id FROM artifacts
        WHERE artifact_id='artifact-ai-resources-owner-acknowledgement-closure-evidence-youtube_content_channels-task-customer-input-test-owner-acknowledgement-youtube_content_channel'
        """
    ).fetchone()
    assert linked["kind"] == "owner_acknowledgement_closure_evidence"
    assert linked["task_id"] == "task-customer-input-test-owner-acknowledgement-youtube_content_channels"


def test_owner_acknowledgement_closure_report_only_does_not_mutate_sources(tmp_path: Path) -> None:
    conn = _conn(tmp_path)
    payload = close_ai_resources_owner_acknowledgements(conn, _args(tmp_path, no_db_record=True))

    assert payload["status"] == "closure_ready"
    status = conn.execute(
        "SELECT status FROM tasks WHERE task_id='task-customer-input-test-owner-acknowledgement-youtube_content_channels'"
    ).fetchone()["status"]
    assert status == "new"


def test_owner_acknowledgement_closure_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-ai-resources-owner-acknowledgement-closure",
            "--input-id",
            "customer-input-test",
        ]
    )

    assert args.cmd == "write-ai-resources-owner-acknowledgement-closure"
    assert args.input_id == "customer-input-test"
