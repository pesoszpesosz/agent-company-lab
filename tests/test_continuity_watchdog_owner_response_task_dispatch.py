import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.continuity_watchdog_owner_response_task_dispatch import (  # noqa: E402
    write_continuity_watchdog_owner_response_task_dispatch,
)
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('department_manager', 'manager', '[]', '[]', '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z')
        """
    )
    for agent_id in [
        "continuity-watchdog-worker-20260621",
        "lane-manager-ai_resources_lab-20260620",
        "lane-manager-youtube_content_channels-20260620",
        "lane-manager-content_and_social_growth-019ec613",
    ]:
        conn.execute(
            """
            INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
            VALUES(?, 'department_manager', ?, 'ai_resources', 'active', '[]', '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z')
            """,
            (agent_id, f"thread-{agent_id}"),
        )
    for lane_id, owner_agent_id in [
        ("ai_resources_lab", "lane-manager-ai_resources_lab-20260620"),
        ("youtube_content_channels", "lane-manager-youtube_content_channels-20260620"),
        ("content_and_social_growth", "lane-manager-content_and_social_growth-019ec613"),
    ]:
        conn.execute(
            """
            INSERT INTO lanes(
              lane_id, department, status, owner_agent_id, owner_thread_id, agent_types_json,
              examples_json, promotion_gates_json, service_workers_required_json,
              side_effects_json, global_gates_json, created_at, updated_at
            )
            VALUES(?, 'AI Resources', 'active', ?, 'thread-owner', '[]', '[]', '[]', '[]', '[]', '[]',
                   '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z')
            """,
            (lane_id, owner_agent_id),
        )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at
        )
        VALUES(
          'task-owner-ack-youtube', 'ai_resources_lab', 'ack youtube', 'new', 90,
          'lane-manager-youtube_content_channels-20260620',
          'customer-input-test:owner-acknowledgement:youtube_content_channels',
          'ack packet', 'write local acknowledgement',
          '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z'
        )
        """
    )
    conn.commit()
    return conn


def _owner_response_artifacts(path: Path) -> Path:
    artifact_dir = path.parent / "owner-responses"
    payload = {
        "schema_version": "continuity_watchdog_owner_response_artifacts.v1",
        "generated_utc": "2026-06-21T11:45:00Z",
        "status": "owner_response_artifacts_ready",
        "counts": {
            "owner_response_artifacts": 3,
            "owner_selection_or_park_required": 1,
            "acknowledgement_response_required": 1,
            "lane_goal_response_required": 1,
            "manual_review_required": 0,
        },
        "owner_response_artifacts": [
            {
                "owner_response_artifact_id": "continuity-owner-response-v1-001-ownerless",
                "response_type": "owner_selection_or_park_required",
                "selected_response_option": "request_ceo_decision_batch_item",
                "target_type": "lane",
                "target_id": "submitted_bounty_payouts",
                "lane_id": "submitted_bounty_payouts",
                "owner_agent_id_or_decision_owner": "ceo_decision_batch",
                "artifact_md_path": str(artifact_dir / "ownerless.md"),
                "next_action": "Queue submitted_bounty_payouts for owner decision.",
                "source_state_mutated": False,
            },
            {
                "owner_response_artifact_id": "continuity-owner-response-v1-002-ack",
                "response_type": "acknowledgement_response_required",
                "selected_response_option": "acknowledge_and_start_local_work",
                "target_type": "task",
                "target_id": "task-owner-ack-youtube",
                "lane_id": "youtube_content_channels",
                "source_task_id": "task-owner-ack-youtube",
                "owner_agent_id": "lane-manager-youtube_content_channels-20260620",
                "artifact_md_path": str(artifact_dir / "ack.md"),
                "next_action": "Existing owner handles acknowledgement locally.",
                "source_state_mutated": False,
            },
            {
                "owner_response_artifact_id": "continuity-owner-response-v1-003-goal",
                "response_type": "lane_goal_response_required",
                "selected_response_option": "submit_current_goal_artifact",
                "target_type": "lane",
                "target_id": "content_and_social_growth",
                "lane_id": "content_and_social_growth",
                "owner_agent_id": "lane-manager-content_and_social_growth-019ec613",
                "current_goal_statement": "Produce one current local proof artifact for content_and_social_growth.",
                "artifact_md_path": str(artifact_dir / "goal.md"),
                "next_action": "Owner submits lane goal artifact.",
                "source_state_mutated": False,
            },
        ],
        "zero_side_effect_boundary": {"external_side_effects": False},
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        owner_response_artifacts=str(_owner_response_artifacts(tmp_path / "owner-response-artifacts.json")),
        now_utc="2026-06-21T12:15:00Z",
        json_path=str(tmp_path / "task-dispatch.json"),
        path=str(tmp_path / "task-dispatch.md"),
        no_db_record=no_db_record,
    )


def test_owner_response_task_dispatch_creates_stable_local_tasks_without_mutating_sources(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_continuity_watchdog_owner_response_task_dispatch(conn, _args(tmp_path))

    assert payload["schema_version"] == "continuity_watchdog_owner_response_task_dispatch.v1"
    assert payload["status"] == "dispatch_tasks_ready"
    assert payload["counts"] == {
        "dispatch_tasks": 3,
        "owner_selection_or_park_required": 1,
        "acknowledgement_response_required": 1,
        "lane_goal_response_required": 1,
        "manual_review_required": 0,
    }
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False

    rows = conn.execute(
        """
        SELECT task_id, lane_id, status, priority, owner_agent_id, duplicate_key, evidence_required
        FROM tasks
        WHERE duplicate_key LIKE 'continuity-owner-response-task:%'
        ORDER BY duplicate_key
        """
    ).fetchall()
    assert len(rows) == 3
    by_key = {row["duplicate_key"]: dict(row) for row in rows}
    assert by_key[
        "continuity-owner-response-task:acknowledgement_response_required:task-owner-ack-youtube"
    ]["lane_id"] == "youtube_content_channels"
    assert by_key[
        "continuity-owner-response-task:acknowledgement_response_required:task-owner-ack-youtube"
    ]["owner_agent_id"] == "lane-manager-youtube_content_channels-20260620"
    assert by_key[
        "continuity-owner-response-task:lane_goal_response_required:content_and_social_growth"
    ]["lane_id"] == "content_and_social_growth"
    assert by_key[
        "continuity-owner-response-task:owner_selection_or_park_required:submitted_bounty_payouts"
    ]["lane_id"] == "ai_resources_lab"
    assert by_key[
        "continuity-owner-response-task:owner_selection_or_park_required:submitted_bounty_payouts"
    ]["owner_agent_id"] == "lane-manager-ai_resources_lab-20260620"

    source = conn.execute("select status from tasks where task_id='task-owner-ack-youtube'").fetchone()
    assert source["status"] == "new"
    audit = conn.execute(
        "select lane_id,status,evidence_required from tasks where task_id='task-continuity-watchdog-owner-response-task-dispatch-v1-20260621'"
    ).fetchone()
    assert audit["lane_id"] == "ai_resources_lab"
    assert audit["status"] == "complete"
    assert audit["evidence_required"] == payload["md_path"]

    second = write_continuity_watchdog_owner_response_task_dispatch(conn, _args(tmp_path))
    assert second["status"] == "dispatch_tasks_ready"
    duplicate_count = conn.execute(
        "select count(*) as c from tasks where duplicate_key like 'continuity-owner-response-task:%'"
    ).fetchone()["c"]
    assert duplicate_count == 3


def test_owner_response_task_dispatch_report_only_skips_db_writes(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_continuity_watchdog_owner_response_task_dispatch(conn, _args(tmp_path, no_db_record=True))

    assert payload["status"] == "dispatch_tasks_ready"
    assert conn.execute(
        "select 1 from tasks where duplicate_key like 'continuity-owner-response-task:%'"
    ).fetchone() is None
    assert conn.execute(
        "select 1 from tasks where task_id='task-continuity-watchdog-owner-response-task-dispatch-v1-20260621'"
    ).fetchone() is None


def test_owner_response_task_dispatch_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-continuity-watchdog-owner-response-task-dispatch",
            "--owner-response-artifacts",
            "reports/continuity-watchdog-owner-response-artifacts-v1-20260621.json",
        ]
    )

    assert args.cmd == "write-continuity-watchdog-owner-response-task-dispatch"
    assert args.owner_response_artifacts == "reports/continuity-watchdog-owner-response-artifacts-v1-20260621.json"
