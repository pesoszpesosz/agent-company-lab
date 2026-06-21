import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.continuity_watchdog_owner_response_artifacts import (  # noqa: E402
    write_continuity_watchdog_owner_response_artifacts,
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
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES(
          'continuity-watchdog-worker-20260621', 'department_manager', 'thread-watchdog',
          'ai_resources', 'active', '[]', '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z'
        )
        """
    )
    conn.execute(
        """
        INSERT INTO lanes(
          lane_id, department, status, owner_agent_id, owner_thread_id, agent_types_json,
          examples_json, promotion_gates_json, service_workers_required_json,
          side_effects_json, global_gates_json, created_at, updated_at
        )
        VALUES(
          'ai_resources_lab', 'AI Resources', 'active', 'continuity-watchdog-worker-20260621',
          'thread-watchdog', '[]', '[]', '[]', '[]', '[]', '[]',
          '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z'
        )
        """
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


def _response_bundle(path: Path) -> Path:
    payload = {
        "schema_version": "continuity_watchdog_restore_response_bundle.v1",
        "generated_utc": "2026-06-21T11:30:00Z",
        "status": "responses_ready",
        "source_restore_plan_path": "restore-plan.json",
        "counts": {
            "response_items": 3,
            "owner_selection_or_park_required": 1,
            "acknowledgement_response_required": 1,
            "lane_goal_response_required": 1,
            "manual_review_required": 0,
        },
        "response_items": [
            {
                "response_item_id": "continuity-restore-response-v1-001-ownerless",
                "schema_version": "continuity_restore_response.v1",
                "response_type": "owner_selection_or_park_required",
                "restore_packet_id": "continuity-restore-v1-001-repair_ownerless_lane-submitted_bounty_payouts",
                "target_type": "lane",
                "target_id": "submitted_bounty_payouts",
                "lane_id": "submitted_bounty_payouts",
                "assigned_surface": "ai_resources_lab",
                "recommended_owner_agent_id": "lane-manager-ai_resources_lab-20260620",
                "required_evidence": "AI Resources owner-selection, park, or retire packet.",
                "response_contract": {
                    "allowed_responses": [
                        "assign_existing_owner_after_overlap_review",
                        "park_lane_with_revisit_condition",
                        "retire_lane_with_rationale",
                        "request_ceo_decision_batch_item",
                    ],
                    "required_fields": [],
                    "prohibited_actions": ["mutate_source_task_or_lane"],
                },
            },
            {
                "response_item_id": "continuity-restore-response-v1-002-ack",
                "schema_version": "continuity_restore_response.v1",
                "response_type": "acknowledgement_response_required",
                "restore_packet_id": "continuity-restore-v1-002-dispatch_stale_owner_acknowledgement-task-owner-ack-youtube",
                "target_type": "task",
                "target_id": "task-owner-ack-youtube",
                "lane_id": "youtube_content_channels",
                "source_task_id": "task-owner-ack-youtube",
                "input_id": "customer-input-test",
                "assigned_surface": "existing_lane_owner",
                "recommended_owner_agent_id": "lane-manager-youtube_content_channels-20260620",
                "required_evidence": "Existing lane owner acknowledgement artifact path.",
                "response_contract": {
                    "allowed_responses": [
                        "acknowledge_and_start_local_work",
                        "park_with_revisit_condition",
                        "request_ceo_decision_batch_item",
                    ],
                    "required_fields": [],
                    "prohibited_actions": ["mutate_source_task_or_lane"],
                },
            },
            {
                "response_item_id": "continuity-restore-response-v1-003-goal",
                "schema_version": "continuity_restore_response.v1",
                "response_type": "lane_goal_response_required",
                "restore_packet_id": "continuity-restore-v1-003-request_lane_goal-content_and_social_growth",
                "target_type": "lane",
                "target_id": "content_and_social_growth",
                "lane_id": "content_and_social_growth",
                "assigned_surface": "existing_lane_owner",
                "recommended_owner_agent_id": "lane-manager-content_and_social_growth-019ec613",
                "required_evidence": "One current lane goal artifact.",
                "response_contract": {
                    "allowed_responses": [
                        "submit_current_goal_artifact",
                        "park_lane_with_revisit_condition",
                        "request_owner_repair",
                    ],
                    "required_fields": [],
                    "prohibited_actions": ["mutate_source_task_or_lane"],
                },
            },
        ],
        "zero_side_effect_boundary": {"external_side_effects": False},
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        response_bundle=str(_response_bundle(tmp_path / "response-bundle.json")),
        now_utc="2026-06-21T11:45:00Z",
        json_path=str(tmp_path / "owner-response-artifacts.json"),
        path=str(tmp_path / "owner-response-artifacts.md"),
        artifact_dir=str(tmp_path / "owner-responses"),
        no_db_record=no_db_record,
    )


def test_owner_response_artifacts_write_selected_local_responses_without_mutating_source_tasks(
    tmp_path: Path,
) -> None:
    conn = _conn()
    artifact_dir = tmp_path / "owner-responses"
    artifact_dir.mkdir()
    stale_artifact = artifact_dir / "continuity-owner-response-v1-999-stale.md"
    stale_artifact.write_text("stale", encoding="utf-8")
    unrelated = artifact_dir / "operator-note.txt"
    unrelated.write_text("keep", encoding="utf-8")

    payload = write_continuity_watchdog_owner_response_artifacts(conn, _args(tmp_path))

    assert payload["schema_version"] == "continuity_watchdog_owner_response_artifacts.v1"
    assert payload["status"] == "owner_response_artifacts_ready"
    assert payload["counts"] == {
        "owner_response_artifacts": 3,
        "owner_selection_or_park_required": 1,
        "acknowledgement_response_required": 1,
        "lane_goal_response_required": 1,
        "manual_review_required": 0,
    }
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()

    artifacts = {item["response_type"]: item for item in payload["owner_response_artifacts"]}
    assert artifacts["owner_selection_or_park_required"]["selected_response_option"] == "request_ceo_decision_batch_item"
    assert artifacts["owner_selection_or_park_required"]["owner_agent_id_or_decision_owner"] == "ceo_decision_batch"
    assert artifacts["acknowledgement_response_required"]["selected_response_option"] == "acknowledge_and_start_local_work"
    assert artifacts["acknowledgement_response_required"]["owner_agent_id"] == "lane-manager-youtube_content_channels-20260620"
    assert artifacts["lane_goal_response_required"]["selected_response_option"] == "submit_current_goal_artifact"
    assert "current_goal_statement" in artifacts["lane_goal_response_required"]

    for item in artifacts.values():
        assert Path(item["artifact_json_path"]).exists()
        assert Path(item["artifact_md_path"]).exists()
        assert item["source_state_mutated"] is False
    assert not stale_artifact.exists()
    assert unrelated.exists()
    assert len(list(artifact_dir.glob("continuity-owner-response-v1-*.md"))) == 3

    source = conn.execute("select status from tasks where task_id='task-owner-ack-youtube'").fetchone()
    assert source["status"] == "new"
    audit = conn.execute(
        "select lane_id,status,evidence_required from tasks where task_id='task-continuity-watchdog-owner-response-artifacts-v1-20260621'"
    ).fetchone()
    assert audit["lane_id"] == "ai_resources_lab"
    assert audit["status"] == "complete"
    assert audit["evidence_required"] == payload["md_path"]


def test_owner_response_artifacts_report_only_skips_db_record(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_continuity_watchdog_owner_response_artifacts(conn, _args(tmp_path, no_db_record=True))

    assert payload["status"] == "owner_response_artifacts_ready"
    assert conn.execute(
        "select 1 from tasks where task_id='task-continuity-watchdog-owner-response-artifacts-v1-20260621'"
    ).fetchone() is None


def test_owner_response_artifacts_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-continuity-watchdog-owner-response-artifacts",
            "--response-bundle",
            "reports/continuity-watchdog-restore-response-bundle-v1-20260621.json",
        ]
    )

    assert args.cmd == "write-continuity-watchdog-owner-response-artifacts"
    assert args.response_bundle == "reports/continuity-watchdog-restore-response-bundle-v1-20260621.json"
