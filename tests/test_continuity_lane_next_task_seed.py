import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.continuity_lane_next_task_seed import (  # noqa: E402
    seed_continuity_lane_next_tasks,
)
from agent_company_core.schema import init_db  # noqa: E402


OLD = "2026-06-21T09:00:00Z"


def _insert_lane(conn: sqlite3.Connection, lane_id: str, status: str = "active") -> None:
    conn.execute(
        """
        INSERT INTO lanes(
          lane_id, department, status, owner_agent_id, owner_thread_id,
          agent_types_json, examples_json, promotion_gates_json,
          service_workers_required_json, side_effects_json, global_gates_json,
          notes, created_at, updated_at
        )
        VALUES(?, 'Test Department', ?, ?, ?, '[]', '[]', '[]', '[]', '[]', '[]', 'test lane', ?, ?)
        """,
        (
            lane_id,
            status,
            f"lane-manager-{lane_id}-20260621",
            f"codex-thread:test-{lane_id}",
            OLD,
            OLD,
        ),
    )


def _conn(tmp_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    evidence = tmp_path / "content-lane-goal.md"
    evidence.write_text("# current goal\n", encoding="utf-8")
    for lane_id, status in [
        ("content_and_social_growth", "active"),
        ("premium_customer_intake", "active"),
        ("lead_generation_and_sales", "active"),
        ("inactive_lane", "parked"),
    ]:
        _insert_lane(conn, lane_id, status)
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
        VALUES('artifact-content-current-goal', 'content_and_social_growth', 'task-content-goal',
               'current_lane_goal_artifact', ?, 'sha', 'current goal', ?)
        """,
        (str(evidence), OLD),
    )
    manager_dir = tmp_path / "manager-packets"
    manager_dir.mkdir()
    (manager_dir / "content_and_social_growth-manager-packet.md").write_text("# content manager\n", encoding="utf-8")
    (manager_dir / "premium_customer_intake-manager-packet.md").write_text("# manager packet\n", encoding="utf-8")
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at
        )
        VALUES('task-existing-lead-open', 'lead_generation_and_sales', 'existing lead task', 'new', 70,
               'lane-manager-lead_generation_and_sales-20260621', 'existing:lead', 'evidence', 'continue', ?, ?)
        """,
        (OLD, OLD),
    )
    conn.commit()
    return conn


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        now_utc="2026-06-21T11:00:00Z",
        json_path=str(tmp_path / "seed.json"),
        path=str(tmp_path / "seed.md"),
        manager_packet_dir=str(tmp_path / "manager-packets"),
        no_db_record=no_db_record,
    )


def test_continuity_lane_next_task_seed_creates_one_task_per_zero_open_owned_lane(tmp_path: Path) -> None:
    conn = _conn(tmp_path)
    payload = seed_continuity_lane_next_tasks(conn, _args(tmp_path))

    assert payload["schema_version"] == "continuity_lane_next_task_seed.v1"
    assert payload["status"] == "seeded"
    assert payload["counts"]["lanes_without_open_tasks"] == 2
    assert payload["counts"]["seed_tasks_created"] == 2
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False

    tasks = [
        dict(row)
        for row in conn.execute(
            """
            SELECT lane_id, task_id, status, duplicate_key, evidence_required, next_action
            FROM tasks
            WHERE duplicate_key LIKE 'continuity:lane-next-task:%'
            ORDER BY lane_id
            """
        )
    ]
    assert [task["lane_id"] for task in tasks] == ["content_and_social_growth", "premium_customer_intake"]
    assert all(task["status"] == "new" for task in tasks)
    assert tasks[0]["evidence_required"].endswith("content-lane-goal.md")
    assert tasks[1]["evidence_required"].endswith("premium_customer_intake-manager-packet.md")
    assert "Do not post" in tasks[0]["next_action"]
    assert "raw material into CEO context" in tasks[1]["next_action"]


def test_continuity_lane_next_task_seed_rerun_reuses_open_seed_tasks(tmp_path: Path) -> None:
    conn = _conn(tmp_path)
    first = seed_continuity_lane_next_tasks(conn, _args(tmp_path))
    second = seed_continuity_lane_next_tasks(conn, _args(tmp_path))

    assert first["counts"]["seed_tasks_created"] == 2
    assert second["status"] == "no_zero_open_lanes"
    assert second["counts"]["lanes_without_open_tasks"] == 0
    count = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE duplicate_key LIKE 'continuity:lane-next-task:%'"
    ).fetchone()[0]
    assert count == 2


def test_continuity_lane_next_task_seed_report_only_does_not_mutate_db(tmp_path: Path) -> None:
    conn = _conn(tmp_path)
    payload = seed_continuity_lane_next_tasks(conn, _args(tmp_path, no_db_record=True))

    assert payload["status"] == "planned_report_only"
    count = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE duplicate_key LIKE 'continuity:lane-next-task:%'"
    ).fetchone()[0]
    assert count == 0


def test_continuity_lane_next_task_seed_repairs_open_seed_missing_evidence(tmp_path: Path) -> None:
    conn = _conn(tmp_path)
    seed_continuity_lane_next_tasks(conn, _args(tmp_path))
    missing = tmp_path / "missing-lane-goal.md"
    conn.execute(
        """
        UPDATE tasks
        SET evidence_required = ?
        WHERE duplicate_key LIKE 'continuity:lane-next-task:content_and_social_growth:%'
        """,
        (str(missing),),
    )
    conn.commit()

    payload = seed_continuity_lane_next_tasks(conn, _args(tmp_path))

    assert payload["status"] == "repaired_existing_seed_evidence"
    assert payload["counts"]["open_seed_evidence_repaired"] == 1
    row = conn.execute(
        """
        SELECT evidence_required FROM tasks
        WHERE duplicate_key LIKE 'continuity:lane-next-task:content_and_social_growth:%'
        """
    ).fetchone()
    assert row["evidence_required"].endswith("content_and_social_growth-manager-packet.md")


def test_continuity_lane_next_task_seed_uses_completed_proof_for_followup(tmp_path: Path) -> None:
    conn = _conn(tmp_path)
    proof = tmp_path / "content-proof.md"
    proof.write_text("# proof\n", encoding="utf-8")
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, completed_at
        )
        VALUES('task-continuity-lane-next-task-20260621-content_and_social_growth-001',
               'content_and_social_growth', 'old proof task', 'complete', 78,
               'lane-manager-content_and_social_growth-20260621',
               'continuity:lane-next-task:content_and_social_growth:20260621:001',
               'seed evidence', 'proof done', ?, ?, ?)
        """,
        ("2026-06-21T10:00:00Z", "2026-06-21T10:00:00Z", "2026-06-21T10:00:00Z"),
    )
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
        VALUES('artifact-content-proof', 'content_and_social_growth',
               'task-continuity-lane-next-task-20260621-content_and_social_growth-001',
               'local_proof_packet', ?, 'sha', 'proof', ?)
        """,
        (str(proof), "2026-06-21T10:00:00Z"),
    )
    conn.commit()

    payload = seed_continuity_lane_next_tasks(conn, _args(tmp_path))

    item = next(item for item in payload["seed_items"] if item["lane_id"] == "content_and_social_growth")
    assert item["profile_stage"] == "proof_followup"
    assert item["task_id"].endswith("-002")
    assert item["evidence_path"] == str(proof)
    task = conn.execute(
        """
        SELECT title, evidence_required, next_action
        FROM tasks
        WHERE task_id=?
        """,
        (item["task_id"],),
    ).fetchone()
    assert task["title"] == "Continue local content reply-target shortlist"
    assert task["evidence_required"] == str(proof)
    assert "reply-target shortlist" in task["next_action"]


def test_continuity_lane_next_task_seed_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-continuity-lane-next-task-seed",
            "--manager-packet-dir",
            "reports/manager-packets",
        ]
    )

    assert args.cmd == "write-continuity-lane-next-task-seed"
    assert args.manager_packet_dir == "reports/manager-packets"
