import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.continuity_watchdog_restore_response_bundle import (  # noqa: E402
    write_continuity_watchdog_restore_response_bundle,
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


def _restore_plan(path: Path) -> Path:
    packet_dir = path.parent / "packets"
    payload = {
        "schema_version": "continuity_watchdog_restore_plan.v1",
        "generated_utc": "2026-06-21T11:15:00Z",
        "status": "restore_plan_ready",
        "source_snapshot_path": "snapshot.json",
        "counts": {
            "restore_packets": 3,
            "repair_ownerless_lane": 1,
            "dispatch_stale_owner_acknowledgement": 1,
            "request_lane_goal": 1,
            "manual_restore_review": 0,
        },
        "restore_packets": [
            {
                "restore_packet_id": "continuity-restore-v1-001-repair_ownerless_lane-submitted_bounty_payouts",
                "kind": "repair_ownerless_lane",
                "target_type": "lane",
                "target_id": "submitted_bounty_payouts",
                "lane_id": "submitted_bounty_payouts",
                "assigned_surface": "ai_resources_lab",
                "recommended_owner_agent_id": "lane-manager-ai_resources_lab-20260620",
                "required_evidence": "AI Resources owner-selection, park, or retire packet.",
                "next_action": "AI Resources selects an existing non-overlapping owner.",
                "prohibited_actions": ["mutate_source_snapshot", "publish_submit_trade_spend_or_call_external_api"],
                "packet_json_path": str(packet_dir / "ownerless.json"),
                "packet_md_path": str(packet_dir / "ownerless.md"),
            },
            {
                "restore_packet_id": "continuity-restore-v1-002-dispatch_stale_owner_acknowledgement-task-owner-ack-youtube",
                "kind": "dispatch_stale_owner_acknowledgement",
                "target_type": "task",
                "target_id": "task-owner-ack-youtube",
                "lane_id": "youtube_content_channels",
                "source_task_id": "task-owner-ack-youtube",
                "input_id": "customer-input-test",
                "source_duplicate_key": "customer-input-test:owner-acknowledgement:youtube_content_channels",
                "assigned_surface": "existing_lane_owner",
                "recommended_owner_agent_id": "lane-manager-youtube_content_channels-20260620",
                "required_evidence": "Existing lane owner acknowledgement artifact path.",
                "next_action": "Use the owner-acknowledgement dispatch contract.",
                "prohibited_actions": ["mutate_source_snapshot", "publish_submit_trade_spend_or_call_external_api"],
                "packet_json_path": str(packet_dir / "ack.json"),
                "packet_md_path": str(packet_dir / "ack.md"),
            },
            {
                "restore_packet_id": "continuity-restore-v1-003-request_lane_goal-content_and_social_growth",
                "kind": "request_lane_goal",
                "target_type": "lane",
                "target_id": "content_and_social_growth",
                "lane_id": "content_and_social_growth",
                "assigned_surface": "existing_lane_owner",
                "recommended_owner_agent_id": "lane-manager-content_and_social_growth-019ec613",
                "required_evidence": "One current lane goal artifact.",
                "next_action": "Ask lane owner for one current goal artifact.",
                "prohibited_actions": ["mutate_source_snapshot", "publish_submit_trade_spend_or_call_external_api"],
                "packet_json_path": str(packet_dir / "goal.json"),
                "packet_md_path": str(packet_dir / "goal.md"),
            },
        ],
        "zero_side_effect_boundary": {"external_side_effects": False},
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        restore_plan=str(_restore_plan(tmp_path / "restore-plan.json")),
        now_utc="2026-06-21T11:30:00Z",
        json_path=str(tmp_path / "response-bundle.json"),
        path=str(tmp_path / "response-bundle.md"),
        response_dir=str(tmp_path / "responses"),
        no_db_record=no_db_record,
    )


def test_restore_response_bundle_writes_response_contracts_without_mutating_source_tasks(tmp_path: Path) -> None:
    conn = _conn()
    response_dir = tmp_path / "responses"
    response_dir.mkdir()
    stale_response = response_dir / "continuity-restore-response-v1-999-stale.md"
    stale_response.write_text("stale", encoding="utf-8")
    unrelated = response_dir / "operator-note.txt"
    unrelated.write_text("keep", encoding="utf-8")

    payload = write_continuity_watchdog_restore_response_bundle(conn, _args(tmp_path))

    assert payload["schema_version"] == "continuity_watchdog_restore_response_bundle.v1"
    assert payload["status"] == "responses_ready"
    assert payload["counts"] == {
        "response_items": 3,
        "owner_selection_or_park_required": 1,
        "acknowledgement_response_required": 1,
        "lane_goal_response_required": 1,
        "manual_review_required": 0,
    }
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()

    items = {item["response_type"]: item for item in payload["response_items"]}
    assert items["owner_selection_or_park_required"]["assigned_surface"] == "ai_resources_lab"
    assert items["owner_selection_or_park_required"]["response_contract"]["allowed_responses"] == [
        "assign_existing_owner_after_overlap_review",
        "park_lane_with_revisit_condition",
        "retire_lane_with_rationale",
        "request_ceo_decision_batch_item",
    ]
    assert items["acknowledgement_response_required"]["response_contract"]["allowed_responses"] == [
        "acknowledge_and_start_local_work",
        "park_with_revisit_condition",
        "request_ceo_decision_batch_item",
    ]
    assert items["acknowledgement_response_required"]["input_id"] == "customer-input-test"
    assert items["lane_goal_response_required"]["response_contract"]["allowed_responses"] == [
        "submit_current_goal_artifact",
        "park_lane_with_revisit_condition",
        "request_owner_repair",
    ]

    for item in items.values():
        assert Path(item["response_json_path"]).exists()
        assert Path(item["response_md_path"]).exists()
        assert "mutate_source_restore_packet" in item["response_contract"]["prohibited_actions"]
    assert not stale_response.exists()
    assert unrelated.exists()
    assert len(list(response_dir.glob("continuity-restore-response-v1-*.md"))) == 3

    source = conn.execute("select status from tasks where task_id='task-owner-ack-youtube'").fetchone()
    assert source["status"] == "new"
    audit = conn.execute(
        "select lane_id,status,evidence_required from tasks where task_id='task-continuity-watchdog-restore-response-bundle-v1-20260621'"
    ).fetchone()
    assert audit["lane_id"] == "ai_resources_lab"
    assert audit["status"] == "complete"
    assert audit["evidence_required"] == payload["md_path"]


def test_restore_response_bundle_report_only_skips_db_record(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_continuity_watchdog_restore_response_bundle(conn, _args(tmp_path, no_db_record=True))

    assert payload["status"] == "responses_ready"
    assert conn.execute(
        "select 1 from tasks where task_id='task-continuity-watchdog-restore-response-bundle-v1-20260621'"
    ).fetchone() is None


def test_restore_response_bundle_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-continuity-watchdog-restore-response-bundle",
            "--restore-plan",
            "reports/continuity-watchdog-restore-plan-v1-20260621.json",
        ]
    )

    assert args.cmd == "write-continuity-watchdog-restore-response-bundle"
    assert args.restore_plan == "reports/continuity-watchdog-restore-plan-v1-20260621.json"
