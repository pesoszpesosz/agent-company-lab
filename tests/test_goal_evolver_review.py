import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.catalog import seed  # noqa: E402
from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.goal_evolver_review import write_goal_evolver_review_packet  # noqa: E402
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    seed(conn)
    now = "2026-06-21T11:00:00Z"
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, department_id, status, permissions_json, notes, created_at, updated_at)
        VALUES(
          'goal-evolver-agent-20260620', 'goal_evolver_agent', 'ai_resources', 'active', '[]',
          'Reviews CEO operating goal against company evidence and writes proposed diffs only.',
          ?, ?
        )
        """,
        (now, now),
    )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at
        )
        VALUES(
          'task-stale-owner-ack-youtube', 'youtube_content_channels', 'Acknowledge routed CEO goal material',
          'new', 90, 'lane-manager-youtube_content_channels-20260620',
          'customer-input-test:owner-acknowledgement:youtube_content_channels',
          'owner acknowledgement packet', 'acknowledge or park the routed goal material',
          '2026-06-21T08:00:00Z', '2026-06-21T08:00:00Z'
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
          'task-blocked-human-action-feed', 'ai_resources_lab', 'Create human action feed schema',
          'blocked', 85, 'lane-manager-ai_resources_lab-20260620',
          'human-action-feed-v1', 'human action feed packet', 'write exact user-only feed contract',
          '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z'
        )
        """
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(
          'outcome-owner-ack-monitor-test', 'ai_resources_lab', 'task-blocked-human-action-feed',
          'ai_resources_owner_acknowledgement_monitor', 'attention_needed', 0,
          'reports/ai-resources-owner-acknowledgement-monitor-v1-20260621.md',
          'escalate stale owner acknowledgements', '2026-06-21T10:00:00Z'
        )
        """
    )
    conn.commit()
    return conn


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        now_utc="2026-06-21T11:30:00Z",
        path=str(tmp_path / "goal-evolver-review.md"),
        json_path=str(tmp_path / "goal-evolver-review.json"),
        goal_md_path=str(ROOT / "architecture" / "ceo-operating-goal-v1.md"),
        goal_json_path=str(ROOT / "architecture" / "ceo-operating-goal-v1.json"),
        agent_charter_path=str(ROOT / "architecture" / "goal-evolver-agent-v1.md"),
        evidence_limit=5,
        no_db_record=no_db_record,
    )


def test_goal_evolver_review_writes_evidence_backed_proposal_without_mutating_goal_or_tasks(tmp_path: Path) -> None:
    conn = _conn()
    args = _args(tmp_path)
    before_goal = Path(args.goal_md_path).read_text(encoding="utf-8")

    payload = write_goal_evolver_review_packet(conn, args)

    assert payload["schema_version"] == "goal_evolver_review.v1"
    assert payload["review_id"] == "goal-evolver-review-v1-20260621"
    assert payload["apply_recommendation"] == "apply_after_review"
    assert payload["risk_boundary_changes"] == []
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False
    assert payload["source_goal_path"] == args.goal_md_path
    assert args.agent_charter_path in payload["evidence_paths"]
    assert payload["company_signals"]["stale_owner_acknowledgement_count"] == 1
    assert payload["company_signals"]["blocked_task_count"] == 1
    assert any("owner acknowledgement" in item.lower() for item in payload["proposed_diff_summary"])
    assert any("stale_owner_acknowledgement_count" in item for item in payload["recommended_additions"])
    assert any("do not apply changes automatically" in item.lower() for item in payload["guardrails_preserved"])
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()

    assert Path(args.goal_md_path).read_text(encoding="utf-8") == before_goal
    source_task = conn.execute("select status from tasks where task_id='task-stale-owner-ack-youtube'").fetchone()
    assert source_task["status"] == "new"

    audit = conn.execute(
        "select lane_id,status,owner_agent_id,evidence_required from tasks where task_id='task-goal-evolver-review-v1-20260621'"
    ).fetchone()
    assert audit["lane_id"] == "ai_resources_lab"
    assert audit["status"] == "complete"
    assert audit["owner_agent_id"] == "goal-evolver-agent-20260620"
    assert audit["evidence_required"] == payload["md_path"]


def test_goal_evolver_review_report_only_skips_db_record(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_goal_evolver_review_packet(conn, _args(tmp_path, no_db_record=True))

    audit = conn.execute("select 1 from tasks where task_id='task-goal-evolver-review-v1-20260621'").fetchone()
    assert payload["review_id"] == "goal-evolver-review-v1-20260621"
    assert audit is None


def test_goal_evolver_review_allows_cross_date_reruns_without_duplicate_key_collision(tmp_path: Path) -> None:
    conn = _conn()
    first_args = _args(tmp_path / "first")
    second_args = _args(tmp_path / "second")
    first_args.now_utc = "2026-06-20T23:55:00Z"
    second_args.now_utc = "2026-06-21T00:05:00Z"

    first = write_goal_evolver_review_packet(conn, first_args)
    second = write_goal_evolver_review_packet(conn, second_args)

    assert first["review_id"] == "goal-evolver-review-v1-20260620"
    assert second["review_id"] == "goal-evolver-review-v1-20260621"
    rows = conn.execute(
        """
        select task_id, duplicate_key
        from tasks
        where task_id in ('task-goal-evolver-review-v1-20260620', 'task-goal-evolver-review-v1-20260621')
        order by task_id
        """
    ).fetchall()
    assert [row["duplicate_key"] for row in rows] == [
        "goal-evolver-review-v1-20260620",
        "goal-evolver-review-v1-20260621",
    ]


def test_goal_evolver_review_rerun_reassigns_existing_outcome_to_current_review_task(tmp_path: Path) -> None:
    conn = _conn()
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, completed_at
        )
        VALUES(
          'task-goal-evolver-review-v1-20260620', 'ai_resources_lab',
          'Old Goal Evolver review packet', 'complete', 92, 'goal-evolver-agent-20260620',
          'goal-evolver-review-v1-20260620', 'old packet', 'superseded by June 21 review',
          '2026-06-20T23:55:00Z', '2026-06-20T23:55:00Z', '2026-06-20T23:55:00Z'
        )
        """
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(
          'outcome-goal-evolver-review-v1-20260621', 'ai_resources_lab',
          'task-goal-evolver-review-v1-20260620', 'goal_evolver_review',
          'apply_after_review', 0, 'old', 'old', '2026-06-20T23:55:00Z'
        )
        """
    )
    conn.commit()
    args = _args(tmp_path)
    args.now_utc = "2026-06-21T00:05:00Z"

    write_goal_evolver_review_packet(conn, args)

    outcome = conn.execute(
        "select task_id, evidence from outcomes where outcome_id='outcome-goal-evolver-review-v1-20260621'"
    ).fetchone()
    assert outcome["task_id"] == "task-goal-evolver-review-v1-20260621"
    assert outcome["evidence"] == str(tmp_path / "goal-evolver-review.md")


def test_goal_evolver_review_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(["write-goal-evolver-review", "--evidence-limit", "7"])

    assert args.cmd == "write-goal-evolver-review"
    assert args.evidence_limit == 7
