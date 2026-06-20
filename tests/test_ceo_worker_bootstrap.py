import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.ceo_worker_bootstrap import bootstrap_ceo_workers  # noqa: E402
from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO lanes(
          lane_id, department, status, owner_agent_id, owner_thread_id, agent_types_json,
          examples_json, promotion_gates_json, service_workers_required_json,
          side_effects_json, global_gates_json, notes, created_at, updated_at
        )
        VALUES(
          'ai_resources_lab', 'Artificial Resources', 'active', null, null, '[]',
          '[]', '[]', '[]', '[]', '[]', 'existing AR lane', '2026-06-21T09:00:00Z', '2026-06-21T09:00:00Z'
        )
        """
    )
    conn.commit()
    return conn


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        now_utc="2026-06-21T12:00:00Z",
        path=str(tmp_path / "roster.md"),
        json_path=str(tmp_path / "roster.json"),
        ar_thread_id="multi-agent:ar-live",
        continuity_thread_id="multi-agent:watchdog-live",
        premium_router_thread_id="multi-agent:router-live",
        no_db_record=no_db_record,
    )


def test_ceo_worker_bootstrap_creates_ar_department_agents_and_active_goals(tmp_path: Path) -> None:
    conn = _conn()
    payload = bootstrap_ceo_workers(conn, _args(tmp_path))
    bootstrap_ceo_workers(conn, _args(tmp_path))

    assert payload["schema_version"] == "ceo_worker_bootstrap.v1"
    assert payload["status"] == "ceo_workers_bootstrapped"
    assert payload["counts"] == {
        "agents": 8,
        "departments": 3,
        "goals": 8,
        "roles": 8,
    }
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False

    ar_department = conn.execute("select name,status,manager_agent_id from departments where department_id='ai_resources'").fetchone()
    assert ar_department["name"] == "Artificial Resources"
    assert ar_department["status"] == "active"
    assert ar_department["manager_agent_id"] == "lane-manager-ai_resources_lab-20260620"

    live_agent = conn.execute(
        "select role_id,thread_id,status from agents where agent_id='lane-manager-ai_resources_lab-20260620'"
    ).fetchone()
    assert live_agent["role_id"] == "ai_resources_manager"
    assert live_agent["thread_id"] == "multi-agent:ar-live"
    assert live_agent["status"] == "active"

    goals = conn.execute(
        "select task_id,status,owner_agent_id from tasks where duplicate_key like 'ceo-worker-bootstrap:%'"
    ).fetchall()
    assert len(goals) == 8
    assert {row["status"] for row in goals} == {"in_progress"}
    assert "continuity-watchdog-worker-20260621" in {row["owner_agent_id"] for row in goals}
    assert "premium-customer-context-router-20260621" in {row["owner_agent_id"] for row in goals}

    lane = conn.execute("select owner_agent_id from lanes where lane_id='ai_resources_lab'").fetchone()
    assert lane["owner_agent_id"] == "lane-manager-ai_resources_lab-20260620"

    artifacts = conn.execute(
        "select count(*) as c from artifacts where task_id='task-ceo-worker-bootstrap-v1-20260621'"
    ).fetchone()
    assert artifacts["c"] == 2


def test_ceo_worker_bootstrap_report_only_does_not_mutate_db(tmp_path: Path) -> None:
    conn = _conn()
    payload = bootstrap_ceo_workers(conn, _args(tmp_path, no_db_record=True))

    assert payload["status"] == "ceo_workers_bootstrapped"
    assert conn.execute("select 1 from agents where agent_id='lane-manager-ai_resources_lab-20260620'").fetchone() is None
    assert conn.execute("select 1 from tasks where task_id='task-ceo-worker-bootstrap-v1-20260621'").fetchone() is None


def test_ceo_worker_bootstrap_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "bootstrap-ceo-workers",
            "--ar-thread-id",
            "multi-agent:ar-live",
            "--continuity-thread-id",
            "multi-agent:watchdog-live",
            "--premium-router-thread-id",
            "multi-agent:router-live",
        ]
    )

    assert args.cmd == "bootstrap-ceo-workers"
    assert args.ar_thread_id == "multi-agent:ar-live"
    assert args.continuity_thread_id == "multi-agent:watchdog-live"
    assert args.premium_router_thread_id == "multi-agent:router-live"
