import sqlite3
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.cli import build_parser  # noqa: E402
from agent_company_core.continuity_lane_next_task_closure import (  # noqa: E402
    close_continuity_lane_next_tasks,
)
from agent_company_core.schema import init_db  # noqa: E402


OLD = "2026-06-21T09:00:00Z"


def _insert_lane(conn: sqlite3.Connection, lane_id: str) -> None:
    conn.execute(
        """
        INSERT INTO lanes(
          lane_id, department, status, owner_agent_id, owner_thread_id,
          agent_types_json, examples_json, promotion_gates_json,
          service_workers_required_json, side_effects_json, global_gates_json,
          notes, created_at, updated_at
        )
        VALUES(?, 'Test Department', 'active', ?, ?, '[]', '[]', '[]', '[]', '[]', '[]', 'test lane', ?, ?)
        """,
        (
            lane_id,
            f"lane-manager-{lane_id}-20260621",
            f"codex-thread:test-{lane_id}",
            OLD,
            OLD,
        ),
    )


def _expected(tmp_path: Path, relative: str) -> Path:
    path = tmp_path / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# proof\n", encoding="utf-8")
    return path


def _conn(tmp_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    for lane_id in ["content_and_social_growth", "digital_products_templates_plugins", "ai_resources_lab"]:
        _insert_lane(conn, lane_id)
    content_proof = _expected(
        tmp_path,
        "reports/content-and-social-growth/content-and-social-growth-local-proof-packet-v1-20260621.md",
    )
    digital_proof = _expected(
        tmp_path,
        "reports/digital-products/digital-products-local-readiness-packet-v1-20260621.md",
    )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at
        )
        VALUES('task-continuity-lane-next-task-20260621-content_and_social_growth-001',
               'content_and_social_growth', 'content proof', 'new', 78,
               'lane-manager-content_and_social_growth-20260621',
               'continuity:lane-next-task:content_and_social_growth:20260621:001',
               'seed evidence', 'produce proof', ?, ?)
        """,
        (OLD, OLD),
    )
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
        VALUES('artifact-content-proof', 'content_and_social_growth',
               'task-continuity-lane-next-task-20260621-content_and_social_growth-001',
               'local_proof_packet', ?, 'sha', 'proof', ?)
        """,
        (str(content_proof), OLD),
    )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at
        )
        VALUES('task-continuity-lane-next-task-20260621-digital_products_templates_plugins-001',
               'digital_products_templates_plugins', 'digital proof', 'complete', 78,
               'lane-manager-digital_products_templates_plugins-20260621',
               'continuity:lane-next-task:digital_products_templates_plugins:20260621:001',
               'seed evidence', 'proof done', ?, ?)
        """,
        (OLD, "2026-06-21T10:00:00Z"),
    )
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
        VALUES('artifact-digital-proof', 'digital_products_templates_plugins',
               'task-continuity-lane-next-task-20260621-digital_products_templates_plugins-001',
               'local_product_readiness_packet', ?, 'sha', 'proof', ?)
        """,
        (str(digital_proof), OLD),
    )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at
        )
        VALUES('task-ai-resources-lane-next-evidence-watch-20260621',
               'ai_resources_lab', 'watch lane next evidence', 'new', 86,
               'lane-manager-ai_resources_lab-20260620',
               'ai_resources:lane_next_evidence_watch:20260621',
               'monitor', 'watch', ?, ?)
        """,
        (OLD, OLD),
    )
    conn.commit()
    return conn


def _args(tmp_path: Path, no_db_record: bool = False) -> Namespace:
    return Namespace(
        now_utc="2026-06-21T11:00:00Z",
        json_path=str(tmp_path / "closure.json"),
        path=str(tmp_path / "closure.md"),
        proof_root=str(tmp_path),
        no_db_record=no_db_record,
    )


def test_lane_next_task_closure_closes_ready_tasks_and_ar_watch(tmp_path: Path) -> None:
    conn = _conn(tmp_path)
    payload = close_continuity_lane_next_tasks(conn, _args(tmp_path))

    assert payload["schema_version"] == "continuity_lane_next_task_closure.v1"
    assert payload["status"] == "closure_applied"
    assert payload["counts"]["closed"] == 1
    assert payload["counts"]["completed_at_repaired"] == 1
    assert payload["counts"]["open_lane_next_tasks_after"] == 0
    assert payload["ar_watch_status"] == "closed"
    assert Path(payload["json_path"]).exists()
    assert Path(payload["md_path"]).exists()
    assert payload["zero_side_effect_boundary"]["external_side_effects"] is False

    rows = {
        row["lane_id"]: dict(row)
        for row in conn.execute(
            """
            SELECT lane_id, status, completed_at
            FROM tasks
            WHERE duplicate_key LIKE 'continuity:lane-next-task:%'
            """
        )
    }
    assert rows["content_and_social_growth"]["status"] == "complete"
    assert rows["content_and_social_growth"]["completed_at"] == "2026-06-21T11:00:00Z"
    assert rows["digital_products_templates_plugins"]["completed_at"] == "2026-06-21T10:00:00Z"
    ar_watch = conn.execute(
        "SELECT status, completed_at FROM tasks WHERE task_id='task-ai-resources-lane-next-evidence-watch-20260621'"
    ).fetchone()
    assert ar_watch["status"] == "complete"
    assert ar_watch["completed_at"] == "2026-06-21T11:00:00Z"


def test_lane_next_task_closure_report_only_does_not_mutate_db(tmp_path: Path) -> None:
    conn = _conn(tmp_path)
    payload = close_continuity_lane_next_tasks(conn, _args(tmp_path, no_db_record=True))

    assert payload["status"] == "closure_applied"
    content = conn.execute(
        """
        SELECT status, completed_at
        FROM tasks
        WHERE task_id='task-continuity-lane-next-task-20260621-content_and_social_growth-001'
        """
    ).fetchone()
    assert content["status"] == "new"
    assert content["completed_at"] is None


def test_lane_next_task_closure_uses_followup_expected_artifact_for_second_sequence(tmp_path: Path) -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    _insert_lane(conn, "content_and_social_growth")
    prior_proof = _expected(
        tmp_path,
        "reports/content-and-social-growth/content-and-social-growth-local-proof-packet-v1-20260621.md",
    )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, completed_at
        )
        VALUES('task-continuity-lane-next-task-20260621-content_and_social_growth-002',
               'content_and_social_growth', 'followup task', 'complete', 76,
               'lane-manager-content_and_social_growth-20260621',
               'continuity:lane-next-task:content_and_social_growth:20260621:002',
               ?, 'wrongly closed', ?, ?, ?)
        """,
        (str(prior_proof), OLD, OLD, OLD),
    )
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
        VALUES('artifact-seed-evidence', 'content_and_social_growth',
               'task-continuity-lane-next-task-20260621-content_and_social_growth-002',
               'continuity_lane_next_task_seed_evidence', ?, 'sha', 'seed evidence', ?)
        """,
        (str(prior_proof), OLD),
    )
    conn.commit()

    payload = close_continuity_lane_next_tasks(conn, _args(tmp_path))

    assert payload["status"] == "closure_applied"
    assert payload["counts"]["reopened_missing_proof_artifact"] == 1
    assert payload["counts"]["missing_proof_artifact"] == 0
    row = conn.execute(
        """
        SELECT status, completed_at, next_action
        FROM tasks
        WHERE task_id='task-continuity-lane-next-task-20260621-content_and_social_growth-002'
        """
    ).fetchone()
    assert row["status"] == "new"
    assert row["completed_at"] is None
    assert "reply-target shortlist" in row["next_action"]


def test_lane_next_task_closure_uses_proof_derived_expected_artifact_after_second_sequence(tmp_path: Path) -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    _insert_lane(conn, "content_and_social_growth")
    followup_artifact = _expected(
        tmp_path,
        "reports/content-and-social-growth/ai-builder-reply-target-shortlist-v1-20260621.md",
    )
    proof_derived_artifact = _expected(
        tmp_path,
        "reports/content_and_social_growth/proof-derived-continuation-v1-20260621-003.md",
    )
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, completed_at
        )
        VALUES('task-continuity-lane-next-task-20260621-content_and_social_growth-003',
               'content_and_social_growth', 'proof-derived continuation', 'complete', 72,
               'lane-manager-content_and_social_growth-20260621',
               'continuity:lane-next-task:content_and_social_growth:20260621:003',
               ?, 'proof done', ?, ?, ?)
        """,
        (str(followup_artifact), OLD, "2026-06-21T10:03:00Z", "2026-06-21T10:03:00Z"),
    )
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
        VALUES('artifact-seed-evidence', 'content_and_social_growth',
               'task-continuity-lane-next-task-20260621-content_and_social_growth-003',
               'continuity_lane_next_task_seed_evidence', ?, 'sha', 'seed evidence', ?)
        """,
        (str(followup_artifact), OLD),
    )
    conn.commit()

    payload = close_continuity_lane_next_tasks(conn, _args(tmp_path))

    item = next(item for item in payload["closure_items"] if item["lane_id"] == "content_and_social_growth")
    assert item["closure_status"] == "already_closed"
    assert item["proof_path"] == str(proof_derived_artifact)
    proof = conn.execute(
        """
        SELECT kind, path_or_url
        FROM artifacts
        WHERE task_id='task-continuity-lane-next-task-20260621-content_and_social_growth-003'
          AND kind='continuity_lane_next_task_proof'
        """
    ).fetchone()
    assert proof["path_or_url"] == str(proof_derived_artifact)


def test_lane_next_task_closure_repairs_stale_closure_proof_pointer(tmp_path: Path) -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    _insert_lane(conn, "content_and_social_growth")
    followup_artifact = _expected(
        tmp_path,
        "reports/content-and-social-growth/ai-builder-reply-target-shortlist-v1-20260621.md",
    )
    proof_derived_artifact = _expected(
        tmp_path,
        "reports/content_and_social_growth/proof-derived-continuation-v1-20260621-004.md",
    )
    task_id = "task-continuity-lane-next-task-20260621-content_and_social_growth-004"
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at, completed_at
        )
        VALUES(?, 'content_and_social_growth', 'proof-derived continuation', 'complete', 72,
               'lane-manager-content_and_social_growth-20260621',
               'continuity:lane-next-task:content_and_social_growth:20260621:004',
               ?, 'proof done', ?, ?, ?)
        """,
        (task_id, str(followup_artifact), OLD, "2026-06-21T10:04:00Z", "2026-06-21T10:04:00Z"),
    )
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
        VALUES('artifact-worker-proof', 'content_and_social_growth', ?,
               'proof_derived_continuation_packet', ?, 'sha', 'worker proof', ?)
        """,
        (task_id, str(proof_derived_artifact), "2026-06-21T10:04:00Z"),
    )
    conn.execute(
        """
        INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
        VALUES('artifact-continuity-lane-next-task-proof-content_and_social_growth',
               'content_and_social_growth', ?, 'continuity_lane_next_task_proof', ?, 'sha',
               'stale closure pointer', ?)
        """,
        (task_id, str(followup_artifact), "2026-06-21T10:05:00Z"),
    )
    conn.commit()

    close_continuity_lane_next_tasks(conn, _args(tmp_path))

    proof = conn.execute(
        """
        SELECT path_or_url
        FROM artifacts
        WHERE artifact_id='artifact-continuity-lane-next-task-proof-content_and_social_growth'
        """
    ).fetchone()
    assert proof["path_or_url"] == str(proof_derived_artifact)


def test_lane_next_task_closure_treats_open_tasks_without_proof_as_waiting(tmp_path: Path) -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db(conn)
    _insert_lane(conn, "content_and_social_growth")
    conn.execute(
        """
        INSERT INTO tasks(
          task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
          evidence_required, next_action, created_at, updated_at
        )
        VALUES('task-continuity-lane-next-task-20260621-content_and_social_growth-005',
               'content_and_social_growth', 'open continuation', 'new', 72,
               'lane-manager-content_and_social_growth-20260621',
               'continuity:lane-next-task:content_and_social_growth:20260621:005',
               'seed evidence', 'continue', ?, ?)
        """,
        (OLD, OLD),
    )
    conn.commit()

    payload = close_continuity_lane_next_tasks(conn, _args(tmp_path))

    item = next(item for item in payload["closure_items"] if item["lane_id"] == "content_and_social_growth")
    assert item["closure_status"] == "waiting_for_proof_artifact"
    assert payload["status"] == "waiting_for_lane_next_tasks"
    assert payload["counts"]["missing_proof_artifact"] == 0
    assert payload["counts"]["waiting_for_proof_artifact"] == 1
    task = conn.execute(
        """
        SELECT status, completed_at
        FROM tasks
        WHERE task_id='task-continuity-lane-next-task-20260621-content_and_social_growth-005'
        """
    ).fetchone()
    assert task["status"] == "new"
    assert task["completed_at"] is None


def test_lane_next_task_closure_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "write-continuity-lane-next-task-closure",
            "--proof-root",
            "E:/agent-company-lab",
        ]
    )

    assert args.cmd == "write-continuity-lane-next-task-closure"
    assert args.proof_root == "E:/agent-company-lab"
