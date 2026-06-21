import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.schema import init_db  # noqa: E402
from agent_company_core.submitted_payout_lane_parking_decision import (  # noqa: E402
    PARKED_STATUS,
    write_submitted_payout_lane_parking_decision,
)


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('ai_resources_manager', 'manager', '[]', '[]', '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES(
          'lane-manager-ai_resources_lab-20260620', 'ai_resources_manager', 'codex-thread:ar',
          'ai_resources', 'active', '[]', '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z'
        )
        """
    )
    for lane_id, department, owner, thread, notes in [
        ("ai_resources_lab", "Artificial Resources", "lane-manager-ai_resources_lab-20260620", "codex-thread:ar", None),
        (
            "submitted_bounty_payouts",
            "Revenue Collection",
            None,
            "other Find profitable edge worker, not this recovered infrastructure thread",
            "other Find profitable edge worker, not this recovered infrastructure thread",
        ),
    ]:
        conn.execute(
            """
            INSERT INTO lanes(
              lane_id, department, status, owner_agent_id, owner_thread_id, agent_types_json,
              examples_json, promotion_gates_json, service_workers_required_json,
              side_effects_json, global_gates_json, notes, created_at, updated_at
            )
            VALUES(?, ?, 'active', ?, ?, '[]', '[]', '[]', '[]', '[]', '[]', ?,
                   '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z')
            """,
            (lane_id, department, owner, thread, notes),
        )
    for task_id, duplicate_key in [
        (
            "task-continuity-owner-response-task-owner_selection_or_park_required-submitted_bounty_payouts",
            "continuity-owner-response-task:owner_selection_or_park_required:submitted_bounty_payouts",
        ),
        (
            "task-continuity-owner-response-task-lane_goal_response_required-submitted_bounty_payouts",
            "continuity-owner-response-task:lane_goal_response_required:submitted_bounty_payouts",
        ),
    ]:
        conn.execute(
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
              evidence_required, next_action, created_at, updated_at
            )
            VALUES(?, 'ai_resources_lab', ?, 'new', 90, 'lane-manager-ai_resources_lab-20260620',
                   ?, 'old evidence', 'decide owner', '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z')
            """,
            (task_id, task_id, duplicate_key),
        )
    conn.commit()
    return conn


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        now_utc="2026-06-21T13:30:00Z",
        path=str(tmp_path / "parking.md"),
        json_path=str(tmp_path / "parking.json"),
        no_db_record=no_db_record,
    )


def test_parking_decision_marks_external_owned_readonly_without_duplicate_owner(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_submitted_payout_lane_parking_decision(conn, _args(tmp_path))

    assert payload["schema_version"] == "submitted_payout_lane_parking_decision.v1"
    assert payload["decision"] == "park_as_external_owned_readonly"
    assert payload["source_state_mutation"]["duplicate_worker_created"] is False
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()

    lane = conn.execute(
        "select status, owner_agent_id, owner_thread_id, notes from lanes where lane_id='submitted_bounty_payouts'"
    ).fetchone()
    assert lane["status"] == PARKED_STATUS
    assert lane["owner_agent_id"] is None
    assert lane["owner_thread_id"] == "external:parallel-payout-worker"
    assert "do not duplicate" in lane["notes"]

    task_rows = conn.execute(
        """
        select task_id, status, evidence_required, completed_at
        from tasks
        where duplicate_key like 'continuity-owner-response-task:%:submitted_bounty_payouts'
        order by task_id
        """
    ).fetchall()
    assert len(task_rows) == 2
    assert {row["status"] for row in task_rows} == {"complete"}
    assert all(row["evidence_required"] == payload["md_path"] for row in task_rows)
    assert all(row["completed_at"] == "2026-06-21T13:30:00Z" for row in task_rows)

    audit = conn.execute(
        "select status, lane_id from tasks where task_id='task-submitted-bounty-payouts-external-owned-parking-decision-v1-20260621'"
    ).fetchone()
    assert audit["status"] == "complete"
    assert audit["lane_id"] == "ai_resources_lab"
    artifact_count = conn.execute(
        "select count(*) as c from artifacts where task_id='task-submitted-bounty-payouts-external-owned-parking-decision-v1-20260621'"
    ).fetchone()["c"]
    assert artifact_count == 2
    assert conn.execute(
        "select 1 from outcomes where outcome_id='outcome-submitted-bounty-payouts-external-owned-parking-decision-v1-20260621'"
    ).fetchone()
    assert conn.execute(
        "select 1 from trace_events where event_id='trace-event-submitted-bounty-payouts-external-owned-parking-decision-v1-20260621'"
    ).fetchone()


def test_parking_decision_report_only_does_not_mutate_db(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_submitted_payout_lane_parking_decision(conn, _args(tmp_path, no_db_record=True))

    assert payload["status"] == "parking_decision_ready"
    lane = conn.execute("select status from lanes where lane_id='submitted_bounty_payouts'").fetchone()
    assert lane["status"] == "active"
    assert conn.execute(
        "select 1 from tasks where task_id='task-submitted-bounty-payouts-external-owned-parking-decision-v1-20260621'"
    ).fetchone() is None


def test_parking_decision_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-submitted-payout-lane-parking-decision",
            "--path",
            "reports/submitted-bounty-payouts-external-owned-parking-decision-v1-20260621.md",
        ]
    )

    assert args.cmd == "write-submitted-payout-lane-parking-decision"
    assert args.path == "reports/submitted-bounty-payouts-external-owned-parking-decision-v1-20260621.md"
