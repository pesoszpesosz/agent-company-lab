import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.catalog import seed  # noqa: E402
from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.runtime_supervisor import write_runtime_supervisor_status_bundle  # noqa: E402
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    seed(conn)
    now = "2026-06-21T17:00:00Z"
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, department_id, status, permissions_json, notes, created_at, updated_at)
        VALUES(
          'lane-manager-ai_resources_lab-20260620', 'ai_resources_manager', 'ai_resources',
          'active', '[]', 'test owner', ?, ?
        )
        ON CONFLICT(agent_id) DO NOTHING
        """,
        (now, now),
    )
    for lane_id, thread_id in [
        ("ai_ml_competitions", "thread-competitions"),
        ("digital_products_templates_plugins", "thread-digital-products"),
        ("content_and_social_growth", "thread-content-growth"),
        ("youtube_content_channels", "thread-youtube"),
    ]:
        conn.execute(
            "UPDATE lanes SET owner_agent_id=?, owner_thread_id=?, updated_at=? WHERE lane_id=?",
            ("lane-manager-ai_resources_lab-20260620", thread_id, now, lane_id),
        )
        conn.execute(
            """
            INSERT INTO lane_runtime_policies(
              lane_id, runtime_mode, cadence_minutes, max_parallel_tasks, capacity_class,
              activation_triggers_json, park_conditions_json, notes, created_at, updated_at
            )
            VALUES(?, 'always_on', 15, 1, 'codex', '[]', '[]', 'test policy', ?, ?)
            ON CONFLICT(lane_id) DO UPDATE SET
              runtime_mode=excluded.runtime_mode,
              cadence_minutes=excluded.cadence_minutes,
              max_parallel_tasks=excluded.max_parallel_tasks,
              capacity_class=excluded.capacity_class,
              updated_at=excluded.updated_at
            """,
            (lane_id, now, now),
        )
    conn.execute(
        """
        INSERT INTO account_capacity_sessions(
          session_id, surface, account_label, status, concurrency_limit, active_lease_count,
          resume_after_utc, last_refresh_utc, last_error, notes, created_at, updated_at
        )
        VALUES(
          'codex-projectless-lane-manager-parallel-pool', 'codex', 'shared-pool',
          'cooling_down', 7, 0, '2026-06-21T18:00:00Z', NULL,
          'shared account is cooling down', 'test cooldown', ?, ?
        )
        """,
        (now, now),
    )
    conn.execute(
        """
        INSERT INTO account_capacity_sessions(
          session_id, surface, account_label, status, concurrency_limit, active_lease_count,
          resume_after_utc, last_refresh_utc, last_error, notes, created_at, updated_at
        )
        VALUES(
          'codex-recovery-executor-low-concurrency', 'codex', 'recovery',
          'available', 1, 1, NULL, '2026-06-21T16:50:00Z',
          NULL, 'already leased', ?, ?
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
          'task-digital-marketplace-first-launch-review-20260621',
          'digital_products_templates_plugins',
          'Review account-gated marketplace launch for Agent Skill Starter Kit',
          'new', 98, 'lane-manager-ai_resources_lab-20260620',
          'marketplace-first-launch-review',
          'Product ZIP and handoff packet',
          'Prepare the marketplace listing locally, then ask the human for account access or explicit approval before login, terms, payout, upload, checkout, or public listing.',
          '2026-06-21T16:55:00Z', '2026-06-21T16:55:00Z'
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
          'task-competition-local-readiness',
          'ai_ml_competitions',
          'Prepare competition local readiness packet',
          'new', 75, 'lane-manager-ai_resources_lab-20260620',
          'competition-local-readiness',
          'local readiness report',
          'Prepare local fixture checks while official account access is pending.',
          '2026-06-21T16:54:00Z', '2026-06-21T16:54:00Z'
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
          'req-kaggle-account-data-access', NULL, 'account_access', 'ai_ml_competitions', NULL,
          'needs_review', 'external_account_or_platform_gate',
          'Use scoped Kaggle account access to fetch official competition rules and data after approval.',
          '{"surface":"Kaggle","forbidden_actions_without_approval":["login","terms","download official data","submit"]}',
          NULL, 'reports/competitions/kaggle-readiness.md', ?, ?
        )
        """,
        (now, now),
    )
    conn.execute(
        """
        INSERT INTO service_requests(
          request_id, service_id, request_type, lane_id, requester_agent_id, status, risk_gate,
          requested_action, intake_json, approval_scope, artifact_path, created_at, updated_at
        )
        VALUES(
          'req-content-readonly-review', NULL, 'browser_research', 'content_and_social_growth', NULL,
          'needs_review', 'catalog_required_approval_no_external_action',
          'Read public content trend pages and capture local notes; no browser side effects.',
          '{"surface":"public web"}',
          NULL, 'reports/content/read-only-review.md', ?, ?
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
          'task-content-growth-warm-monitor',
          'content_and_social_growth',
          'Warm content growth monitor',
          'new', 80, 'lane-manager-ai_resources_lab-20260620',
          'content-growth-warm-monitor',
          'local monitor report',
          'Run local read-only monitoring when Codex capacity is available. Do not publish, submit, trade, spend, call APIs, or contact anyone.',
          '2026-06-21T16:56:00Z', '2026-06-21T16:56:00Z'
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
          'task-youtube-worker-recover',
          'youtube_content_channels',
          'Recover YouTube lane manager',
          'new', 70, 'lane-manager-ai_resources_lab-20260620',
          'youtube-worker-recover',
          'restore packet',
          'Recover the lane manager from its latest local goal context.',
          '2026-06-21T16:57:00Z', '2026-06-21T16:57:00Z'
        )
        """
    )
    conn.commit()
    return conn


def _snapshot(tmp_path: Path) -> Path:
    path = tmp_path / "thread-snapshot.json"
    path.write_text(
        json.dumps(
            {
                "threads": [
                    {
                        "id": "codex-thread:thread-competitions",
                        "title": "AI/ML competitions lane /goal",
                        "status": "idle",
                        "cwd": str(tmp_path),
                    },
                    {
                        "id": "codex-thread:thread-digital-products",
                        "title": "Digital products lane /goal",
                        "status": "notLoaded",
                        "cwd": str(tmp_path),
                    },
                    {
                        "id": "codex-thread:thread-content-growth",
                        "title": "Content growth lane /goal",
                        "status": "notLoaded",
                        "cwd": str(tmp_path),
                    },
                    {
                        "id": "codex-thread:thread-youtube",
                        "title": "YouTube lane /goal",
                        "status": {"type": "systemError"},
                        "cwd": str(tmp_path),
                    },
                ]
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        thread_snapshot=str(_snapshot(tmp_path)),
        now_utc="2026-06-21T17:05:00Z",
        path=str(tmp_path / "runtime-supervisor.md"),
        json_path=str(tmp_path / "runtime-supervisor.json"),
        human_action_path=str(tmp_path / "human-action.md"),
        human_action_json_path=str(tmp_path / "human-action.json"),
        lane_limit=25,
        open_task_limit=25,
        no_db_record=no_db_record,
    )


def test_runtime_supervisor_separates_human_gates_capacity_and_system_errors(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_runtime_supervisor_status_bundle(conn, _args(tmp_path))
    by_lane = {item["lane_id"]: item for item in payload["lane_runtime_statuses"]}

    assert payload["schema_version"] == "worker_runtime_status.v1"
    assert payload["status"] == "attention_required"
    assert by_lane["ai_ml_competitions"]["runtime_status"] == "blocked_by_human_gate"
    assert by_lane["digital_products_templates_plugins"]["runtime_status"] == "blocked_by_human_gate"
    assert by_lane["digital_products_templates_plugins"]["human_gate_count"] == 1
    assert by_lane["content_and_social_growth"]["runtime_status"] == "parked_by_capacity"
    assert by_lane["content_and_social_growth"]["human_gate_count"] == 0
    assert by_lane["youtube_content_channels"]["runtime_status"] == "system_error"
    assert payload["counts"]["blocked_by_human_gate"] == 2
    assert payload["counts"]["parked_by_capacity"] == 1
    assert payload["counts"]["system_error"] == 1
    assert payload["capacity_summary"]["available_slots"] == 0
    assert payload["human_action_feed"]["feed_status"] == "human_gate_action_required"
    assert payload["human_action_feed"]["required_now"][0]["surface"] == "Kaggle"
    assert payload["human_action_feed"]["account_gate_queue"][0]["service_request_id"] == "req-kaggle-account-data-access"
    assert any(
        item.get("service_request_id") == "req-content-readonly-review"
        for item in payload["human_action_feed"]["optional_gate_queue"]
    )
    assert {item["gate_category"] for item in payload["human_action_feed"]["account_gate_queue"]} == {
        "external_account_or_platform_gate"
    }
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert Path(payload["human_action_feed"]["json_path"]).exists()
    assert Path(payload["human_action_feed"]["md_path"]).exists()

    audit = conn.execute(
        "SELECT status, evidence_required FROM tasks WHERE task_id='task-worker-runtime-status-v1-20260621'"
    ).fetchone()
    assert audit["status"] == "complete"
    assert audit["evidence_required"] == payload["md_path"]
    artifact_count = conn.execute(
        "SELECT COUNT(*) FROM artifacts WHERE task_id='task-worker-runtime-status-v1-20260621'"
    ).fetchone()[0]
    assert artifact_count == 4


def test_runtime_supervisor_report_only_skips_db_record(tmp_path: Path) -> None:
    conn = _conn()
    payload = write_runtime_supervisor_status_bundle(conn, _args(tmp_path, no_db_record=True))

    assert payload["status"] == "attention_required"
    audit = conn.execute("SELECT 1 FROM tasks WHERE task_id='task-worker-runtime-status-v1-20260621'").fetchone()
    assert audit is None


def test_runtime_supervisor_keeps_local_prep_gate_mentions_dispatchable(
    tmp_path: Path,
) -> None:
    conn = _conn()
    conn.execute(
        """
        UPDATE tasks
        SET next_action=?
        WHERE task_id='task-digital-marketplace-first-launch-review-20260621'
        """,
        (
            "Prepare a PromptBase-first launch review packet from local ZIP/listing artifacts; "
            "surface exact account/terms/upload/checkout questions; do not log in, upload, list, "
            "publish, create checkout, accept terms, or process customer data.",
        ),
    )
    conn.commit()

    payload = write_runtime_supervisor_status_bundle(conn, _args(tmp_path, no_db_record=True))
    by_lane = {item["lane_id"]: item for item in payload["lane_runtime_statuses"]}

    assert by_lane["digital_products_templates_plugins"]["runtime_status"] == "parked_by_capacity"
    assert by_lane["digital_products_templates_plugins"]["human_gate_count"] == 0
    assert not any(
        item.get("task_id") == "task-digital-marketplace-first-launch-review-20260621"
        for item in payload["human_action_feed"]["required_now"]
    )
    optional_gate = next(
        item
        for item in payload["human_action_feed"]["optional_gate_queue"]
        if item.get("task_id") == "task-digital-marketplace-first-launch-review-20260621"
    )
    assert optional_gate["blocking"] is False
    assert optional_gate["surface"] == "PromptBase"


def test_runtime_supervisor_allows_canonical_local_tasks_in_non_repo_threads(
    tmp_path: Path,
) -> None:
    conn = _conn()
    now = "2026-06-21T17:04:00Z"
    conn.execute("DELETE FROM service_requests WHERE lane_id='ai_ml_competitions'")
    conn.execute(
        """
        UPDATE account_capacity_sessions
        SET status='available', active_lease_count=0, resume_after_utc=NULL
        """
    )
    conn.execute(
        """
        UPDATE tasks
        SET priority=92,
            evidence_required=?,
            next_action=?,
            updated_at=?
        WHERE task_id='task-competition-local-readiness'
        """,
        (
            r"E:\agent-company-lab\reports\ai-ml-competitions\local-readiness.md",
            "Write one compact local continuation packet under E:\\agent-company-lab; "
            "keep all work local and surface account gates before external action.",
            now,
        ),
    )
    conn.commit()

    payload = write_runtime_supervisor_status_bundle(conn, _args(tmp_path, no_db_record=True))
    by_lane = {item["lane_id"]: item for item in payload["lane_runtime_statuses"]}

    assert by_lane["ai_ml_competitions"]["repo_backed"] is False
    assert by_lane["ai_ml_competitions"]["runtime_status"] == "idle_ready"
    assert by_lane["ai_ml_competitions"]["open_task_count"] == 1
    assert all(
        item["lane_id"] != "ai_ml_competitions"
        for item in payload["lane_runtime_statuses"]
        if item["runtime_status"] == "repo_backing_needed"
    )


def test_runtime_supervisor_allows_repo_relative_local_artifacts_in_non_repo_threads(
    tmp_path: Path,
) -> None:
    conn = _conn()
    now = "2026-06-21T17:04:00Z"
    conn.execute("DELETE FROM service_requests WHERE lane_id='ai_ml_competitions'")
    conn.execute(
        """
        UPDATE account_capacity_sessions
        SET status='available', active_lease_count=0, resume_after_utc=NULL
        """
    )
    conn.execute(
        """
        UPDATE tasks
        SET priority=92,
            evidence_required=?,
            next_action=?,
            updated_at=?
        WHERE task_id='task-competition-local-readiness'
        """,
        (
            "reports/ai-ml-competitions/local-readiness.md or equivalent local status artifact",
            "Write one compact local continuation packet; keep all work local and surface account gates before external action.",
            now,
        ),
    )
    conn.commit()

    payload = write_runtime_supervisor_status_bundle(conn, _args(tmp_path, no_db_record=True))
    by_lane = {item["lane_id"]: item for item in payload["lane_runtime_statuses"]}

    assert by_lane["ai_ml_competitions"]["repo_backed"] is False
    assert by_lane["ai_ml_competitions"]["runtime_status"] == "idle_ready"
    assert by_lane["ai_ml_competitions"]["open_task_count"] == 1


def test_runtime_supervisor_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-runtime-supervisor-status",
            "--thread-snapshot",
            "snapshot.json",
            "--lane-limit",
            "12",
            "--open-task-limit",
            "9",
        ]
    )

    assert args.cmd == "write-runtime-supervisor-status"
    assert args.thread_snapshot == "snapshot.json"
    assert args.lane_limit == 12
    assert args.open_task_limit == 9
