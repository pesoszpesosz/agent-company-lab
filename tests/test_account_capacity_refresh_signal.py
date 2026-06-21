import json
import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.account_capacity_refresh_signal import (  # noqa: E402
    apply_account_capacity_refresh_signal,
)
from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.schema import init_db  # noqa: E402


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    conn.execute(
        """
        INSERT INTO roles(role_id, level, responsibilities_json, must_not_do_json, created_at, updated_at)
        VALUES('department_manager', 'manager', '[]', '[]', '2026-06-21T16:00:00Z', '2026-06-21T16:00:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO agents(agent_id, role_id, thread_id, department_id, status, permissions_json, created_at, updated_at)
        VALUES('lane-manager-ai_resources_lab-20260620', 'department_manager', 'codex-thread:ar', 'ai_resources', 'active', '[]', '2026-06-21T16:00:00Z', '2026-06-21T16:00:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO lanes(
          lane_id, department, status, owner_agent_id, owner_thread_id,
          agent_types_json, examples_json, promotion_gates_json,
          service_workers_required_json, side_effects_json, global_gates_json,
          created_at, updated_at
        )
        VALUES('ai_resources_lab', 'AI Resources', 'active', 'lane-manager-ai_resources_lab-20260620', 'codex-thread:ar',
               '[]', '[]', '[]', '[]', '[]', '[]',
               '2026-06-21T16:00:00Z', '2026-06-21T16:00:00Z')
        """
    )
    conn.execute(
        """
        INSERT INTO account_capacity_sessions(
          session_id, surface, account_label, status, concurrency_limit,
          active_lease_count, resume_after_utc, last_refresh_utc, last_error,
          notes, created_at, updated_at
        )
        VALUES('codex-parallel', 'codex', 'parallel pool', 'cooling_down', 7, 0,
               '2026-06-21T16:00:00Z', NULL, 'usage exhausted',
               'wait for explicit refresh signal', '2026-06-21T15:30:00Z', '2026-06-21T16:00:00Z')
        """
    )
    conn.commit()
    return conn


def _write_signal(path: Path, observed_utc: str, status: str = "usable") -> Path:
    path.write_text(
        json.dumps(
            {
                "signal_id": "refresh-signal-codex-parallel",
                "session_id": "codex-parallel",
                "observed_utc": observed_utc,
                "status": status,
                "source": "operator_refresh_watch",
                "evidence": "new usable session was observed outside repo; no token stored",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def _args(tmp_path: Path, signal_path: Path, no_db_record: bool = True) -> Namespace:
    return Namespace(
        signal_path=str(signal_path),
        now_utc="2026-06-21T16:30:00Z",
        path=str(tmp_path / "refresh.md"),
        json_path=str(tmp_path / "refresh.json"),
        no_db_record=no_db_record,
    )


def test_account_capacity_refresh_signal_marks_cooling_down_session_available(tmp_path: Path) -> None:
    conn = _conn()
    signal_path = _write_signal(tmp_path / "signal.json", "2026-06-21T16:25:00Z")

    payload = apply_account_capacity_refresh_signal(conn, _args(tmp_path, signal_path, no_db_record=False))

    assert payload["status"] == "capacity_available"
    assert payload["counts"]["sessions_available"] == 1
    assert payload["counts"]["stale_signals"] == 0
    session = conn.execute(
        """
        SELECT status, active_lease_count, resume_after_utc, last_refresh_utc, last_error
        FROM account_capacity_sessions
        WHERE session_id='codex-parallel'
        """
    ).fetchone()
    assert dict(session) == {
        "status": "available",
        "active_lease_count": 0,
        "resume_after_utc": None,
        "last_refresh_utc": "2026-06-21T16:25:00Z",
        "last_error": None,
    }
    audit = conn.execute(
        "SELECT status, evidence_required FROM tasks WHERE task_id='task-account-capacity-refresh-signal-v1-20260621'"
    ).fetchone()
    assert dict(audit) == {"status": "complete", "evidence_required": str(tmp_path / "refresh.md")}


def test_account_capacity_refresh_signal_ignores_stale_signal(tmp_path: Path) -> None:
    conn = _conn()
    signal_path = _write_signal(tmp_path / "signal.json", "2026-06-21T15:59:00Z")

    payload = apply_account_capacity_refresh_signal(conn, _args(tmp_path, signal_path))

    assert payload["status"] == "ignored"
    assert payload["counts"]["sessions_available"] == 0
    assert payload["counts"]["stale_signals"] == 1
    session = conn.execute(
        """
        SELECT status, resume_after_utc, last_refresh_utc, last_error
        FROM account_capacity_sessions
        WHERE session_id='codex-parallel'
        """
    ).fetchone()
    assert dict(session) == {
        "status": "cooling_down",
        "resume_after_utc": "2026-06-21T16:00:00Z",
        "last_refresh_utc": None,
        "last_error": "usage exhausted",
    }


def test_account_capacity_refresh_signal_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "apply-account-capacity-refresh-signal",
            "--signal-path",
            "refresh-signal.json",
            "--now-utc",
            "2026-06-21T16:30:00Z",
        ]
    )

    assert args.cmd == "apply-account-capacity-refresh-signal"
    assert args.signal_path == "refresh-signal.json"
    assert args.now_utc == "2026-06-21T16:30:00Z"
