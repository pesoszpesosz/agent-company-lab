import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.catalog import seed  # noqa: E402
from agent_company_core.ceo_state_packet import write_ceo_state_packet_bundle  # noqa: E402
from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    seed(conn)
    now = "2026-06-21T10:00:00Z"
    for agent_id, role_id, department_id in [
        ("lane-manager-ai_resources_lab-20260620", "ai_resources_manager", "ai_resources"),
        ("human-action-desk-worker-20260620", "human_action_desk_worker", "human_action_desk"),
    ]:
        conn.execute(
            """
            INSERT INTO agents(agent_id, role_id, department_id, status, permissions_json, notes, created_at, updated_at)
            VALUES(?, ?, ?, 'active', '[]', 'test agent', ?, ?)
            """,
            (agent_id, role_id, department_id, now, now),
        )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at
        )
        VALUES(
          'task-owner-ack-youtube', 'youtube_content_channels', 'Owner acknowledgement for YouTube material',
          'new', 95, 'lane-manager-ai_resources_lab-20260620',
          'customer-input-test:owner-acknowledgement:youtube_content_channels',
          'ack packet', 'acknowledge, park, or request CEO decision',
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
          'task-local-proof', 'ai_resources_lab', 'Create local proof packet',
          'new', 80, 'lane-manager-ai_resources_lab-20260620',
          'local-proof', 'proof packet', 'write the smallest local proof artifact',
          '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z'
        )
        """
    )
    conn.execute(
        """
        INSERT INTO service_requests(
          request_id, service_id, request_type, lane_id, requester_agent_id, status, risk_gate,
          requested_action, intake_json, approval_scope, artifact_path, created_at, updated_at
        )
        VALUES(
          'req-readonly-market-review', NULL, 'browser_readonly', 'ai_resources_lab', NULL,
          'needs_review', 'browser_read_only', 'Read public marketplace terms for route viability',
          '{}', NULL, 'reports/market-review.md', ?, ?
        )
        """,
        (now, now),
    )
    conn.execute(
        """
        INSERT INTO outcomes(outcome_id, lane_id, task_id, outcome_type, status, realized_usd, evidence, next_action, created_at)
        VALUES(
          'outcome-local-proof', 'ai_resources_lab', 'task-local-proof', 'local_proof',
          'complete', 0, 'reports/local-proof.md', 'promote local proof into dispatch queue', ?
        )
        """,
        (now,),
    )
    conn.commit()
    return conn


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        now_utc="2026-06-21T11:00:00Z",
        path=str(tmp_path / "ceo-state.md"),
        json_path=str(tmp_path / "ceo-state.json"),
        human_action_path=str(tmp_path / "human-action.md"),
        human_action_json_path=str(tmp_path / "human-action.json"),
        open_task_limit=5,
        dispatch_limit=5,
        no_db_record=no_db_record,
    )


def test_ceo_state_packet_writes_compact_state_and_human_action_feed_without_mutating_work(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_ceo_state_packet_bundle(conn, _args(tmp_path))

    assert payload["schema_version"] == "ceo_state_packet.v1"
    assert payload["packet_id"] == "ceo-state-packet-v1-20260621"
    assert payload["company_counts"]["tasks"] >= 2
    assert payload["active_blockers_and_gates"]["service_requests_needing_review"] == 1
    assert payload["active_blockers_and_gates"]["stale_owner_acknowledgement_count"] == 1
    assert payload["human_action_feed"]["feed_status"] == "optional_gate_review_available"
    assert payload["human_action_feed"]["required_now"] == []
    assert payload["human_action_feed"]["optional_gate_queue"][0]["request_id"] == "req-readonly-market-review"
    assert payload["metrics_since_last_packet"]["tasks_delta"] is None
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert Path(payload["human_action_feed"]["json_path"]).exists()
    assert Path(payload["human_action_feed"]["md_path"]).exists()

    source_request = conn.execute(
        "select status from service_requests where request_id='req-readonly-market-review'"
    ).fetchone()
    source_task = conn.execute("select status from tasks where task_id='task-owner-ack-youtube'").fetchone()
    assert source_request["status"] == "needs_review"
    assert source_task["status"] == "new"

    audit = conn.execute(
        "select lane_id,status,evidence_required from tasks where task_id='task-ceo-state-packet-v1-20260621'"
    ).fetchone()
    assert audit["lane_id"] == "ai_resources_lab"
    assert audit["status"] == "complete"
    assert audit["evidence_required"] == payload["md_path"]

    artifacts = conn.execute(
        "select count(*) from artifacts where task_id='task-ceo-state-packet-v1-20260621'"
    ).fetchone()[0]
    assert artifacts == 4


def test_ceo_state_packet_report_only_skips_db_record(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_ceo_state_packet_bundle(conn, _args(tmp_path, no_db_record=True))

    audit = conn.execute("select 1 from tasks where task_id='task-ceo-state-packet-v1-20260621'").fetchone()
    assert payload["packet_id"] == "ceo-state-packet-v1-20260621"
    assert audit is None


def test_ceo_state_packet_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(["write-ceo-state-packet", "--open-task-limit", "3", "--dispatch-limit", "4"])

    assert args.cmd == "write-ceo-state-packet"
    assert args.open_task_limit == 3
    assert args.dispatch_limit == 4
