import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.codex_thread_goal_inventory import (  # noqa: E402
    build_codex_thread_goal_inventory,
)
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO lanes(
          lane_id, department, status, owner_agent_id, owner_thread_id,
          agent_types_json, examples_json, promotion_gates_json,
          service_workers_required_json, side_effects_json, global_gates_json,
          notes, created_at, updated_at
        )
        VALUES('content_and_social_growth', 'Content', 'active', 'lane-manager-content',
               'codex-thread:registered-thread', '[]', '[]', '[]', '[]', '[]', '[]',
               'test', '2026-06-21T14:00:00Z', '2026-06-21T14:00:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('agent-with-thread', 'worker', 'codex-thread:agent-thread', 'ai_resources_lab',
               'active', '[]', '2026-06-21T14:00:00Z', '2026-06-21T14:00:00Z')
        """
    )
    conn.commit()
    return conn


def test_codex_thread_goal_inventory_flags_unmonitored_and_system_error_goal_threads(tmp_path: Path) -> None:
    registered_cwd = tmp_path / "registered-thread"
    unmonitored_cwd = tmp_path / "unmonitored-thread"
    plain_cwd = tmp_path / "plain-thread"
    for path in [registered_cwd, unmonitored_cwd, plain_cwd]:
        path.mkdir()
    snapshot = {
        "schemaVersion": 1,
        "threads": [
            {
                "id": "registered-thread",
                "title": "Agent Company - Content Social Growth",
                "preview": "/goal Own the content lane",
                "status": "systemError",
                "cwd": str(registered_cwd),
            },
            {
                "id": "new-goal-thread",
                "title": "Experimental Money Path",
                "preview": "Active goal: test a new money lane locally",
                "status": "idle",
                "cwd": str(unmonitored_cwd),
            },
            {
                "id": "plain-chat",
                "title": "Notes",
                "preview": "No active work here",
                "status": "idle",
                "cwd": str(plain_cwd),
            },
        ],
    }
    snapshot_path = tmp_path / "threads.json"
    snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")

    payload = build_codex_thread_goal_inventory(
        _conn(),
        Namespace(
            thread_snapshot=str(snapshot_path),
            now_utc="2026-06-21T15:00:00Z",
            json_path=str(tmp_path / "inventory.json"),
            path=str(tmp_path / "inventory.md"),
            no_db_record=True,
        ),
    )

    assert payload["counts"]["threads_seen"] == 3
    assert payload["counts"]["goal_threads"] == 2
    assert payload["counts"]["monitored_goal_threads"] == 1
    assert payload["counts"]["unmonitored_goal_threads"] == 1
    assert payload["counts"]["system_error_goal_threads"] == 1
    assert payload["counts"]["non_repo_goal_threads"] == 2

    unmonitored = next(item for item in payload["threads"] if item["thread_id"] == "new-goal-thread")
    assert unmonitored["has_goal_signal"] is True
    assert unmonitored["monitor_status"] == "unmonitored_goal_thread"
    assert "register_goal_thread" in unmonitored["recommended_actions"]

    system_error = next(item for item in payload["threads"] if item["thread_id"] == "registered-thread")
    assert system_error["monitor_status"] == "monitored"
    assert "recover_system_error_thread" in system_error["recommended_actions"]


def test_codex_thread_goal_inventory_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(["write-codex-thread-goal-inventory", "--thread-snapshot", "threads.json"])

    assert args.cmd == "write-codex-thread-goal-inventory"
    assert args.thread_snapshot == "threads.json"


def test_codex_thread_goal_inventory_next_action_mentions_repo_backing_when_all_goals_are_monitored(
    tmp_path: Path,
) -> None:
    monitored_cwd = tmp_path / "monitored-non-repo-thread"
    monitored_cwd.mkdir()
    snapshot = {
        "threads": [
            {
                "id": "registered-thread",
                "title": "Agent Company - Content Social Growth",
                "preview": "/goal Own the content lane",
                "status": "idle",
                "cwd": str(monitored_cwd),
            }
        ],
    }
    snapshot_path = tmp_path / "threads.json"
    snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")

    payload = build_codex_thread_goal_inventory(
        _conn(),
        Namespace(
            thread_snapshot=str(snapshot_path),
            now_utc="2026-06-21T15:12:00Z",
            json_path=str(tmp_path / "inventory.json"),
            path=str(tmp_path / "inventory.md"),
            no_db_record=True,
        ),
    )

    assert payload["status"] == "repo_backing_recommended"
    assert "repo-backed" in payload["next_action"]
