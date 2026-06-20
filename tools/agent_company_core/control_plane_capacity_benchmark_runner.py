"""Reusable synthetic capacity benchmark for the Agent Company control plane."""

from __future__ import annotations

import argparse
import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Iterable

from .io import now_utc
from .paths import REPORTS_DIR, ROOT
from .schema import init_db


DEFAULT_ROW_COUNTS = (1_000, 10_000, 100_000)
DEFAULT_WORK_DIR = ROOT / "work" / "capacity-benchmark"
SCHEMA_VERSION = "control_plane_capacity_benchmark_runner.v1"
TARGET_TABLES = ("tasks", "artifacts", "outcomes", "trace_events", "service_requests")
CAPACITY_INDEXES = {
    "tasks": ("idx_tasks_lane_created", "idx_tasks_status_priority_created"),
    "artifacts": ("idx_artifacts_lane_created", "idx_artifacts_task_created"),
    "outcomes": ("idx_outcomes_lane_created", "idx_outcomes_task_created"),
    "service_requests": ("idx_service_requests_status_created", "idx_service_requests_lane_status"),
}
LANES = (
    "platform_engineering",
    "ai_resources_lab",
    "youtube_content_channels",
    "prediction_market_research",
    "paid_code_bounties",
    "premium_customer_intake",
)


def parse_row_counts(value: str | None) -> tuple[int, ...]:
    if not value:
        return DEFAULT_ROW_COUNTS
    counts: list[int] = []
    for raw_part in value.replace(";", ",").split(","):
        part = raw_part.strip()
        if not part:
            continue
        try:
            count = int(part)
        except ValueError as exc:
            raise SystemExit(f"Invalid row count: {part}") from exc
        if count < 1:
            raise SystemExit("Row counts must be positive integers.")
        if count not in counts:
            counts.append(count)
    if not counts:
        raise SystemExit("At least one row count is required.")
    return tuple(counts)


def _timed(label: str, fn) -> dict[str, Any]:
    started = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - started
    return {"label": label, "seconds": round(elapsed, 6), "result": result}


def _created_at(index: int) -> str:
    day = (index % 28) + 1
    hour = index % 24
    minute = index % 60
    second = (index * 7) % 60
    return f"2026-06-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}Z"


def _lane(index: int) -> str:
    return LANES[index % len(LANES)]


def _task_rows(row_count: int) -> Iterable[tuple[Any, ...]]:
    statuses = ("new", "in_progress", "complete", "blocked", "needs_review")
    for i in range(row_count):
        created = _created_at(i)
        task_id = f"bench-task-{i:07d}"
        yield (
            task_id,
            _lane(i),
            f"Synthetic benchmark task {i}",
            statuses[i % len(statuses)],
            (i % 100) + 1,
            f"bench-agent-{i % 24:02d}",
            f"bench-duplicate-{i:07d}",
            "synthetic evidence",
            "measure control-plane query path",
            created,
            created,
        )


def _artifact_rows(row_count: int) -> Iterable[tuple[Any, ...]]:
    kinds = ("benchmark_report", "capacity_trace", "source_packet", "worker_output")
    for i in range(row_count):
        created = _created_at(i)
        yield (
            f"bench-artifact-{i:07d}",
            _lane(i),
            f"bench-task-{i:07d}",
            kinds[i % len(kinds)],
            f"E:/agent-company-lab/work/capacity-benchmark/synthetic-artifact-{i:07d}.json",
            f"{i:064x}"[-64:],
            "synthetic capacity artifact",
            created,
        )


def _outcome_rows(row_count: int) -> Iterable[tuple[Any, ...]]:
    statuses = ("candidate", "validated", "rejected", "needs_followup")
    for i in range(row_count):
        created = _created_at(i)
        yield (
            f"bench-outcome-{i:07d}",
            _lane(i),
            f"bench-task-{i:07d}",
            "capacity_signal",
            statuses[i % len(statuses)],
            0.0,
            f"synthetic evidence for row {i}",
            "keep benchmark non-destructive",
            created,
        )


def _trace_rows(row_count: int) -> Iterable[tuple[Any, ...]]:
    event_types = ("task_created", "artifact_recorded", "outcome_recorded", "manager_reviewed")
    for i in range(row_count):
        created = _created_at(i)
        yield (
            f"bench-trace-event-{i:07d}",
            f"bench-trace-{i % 1000:04d}",
            _lane(i),
            f"bench-task-{i:07d}",
            f"bench-agent-{i % 24:02d}",
            event_types[i % len(event_types)],
            created,
            "control_plane_capacity_benchmark_runner",
            f"Synthetic trace event {i}",
            json.dumps({"synthetic": True, "row_index": i}, sort_keys=True),
            f"E:/agent-company-lab/work/capacity-benchmark/synthetic-artifact-{i:07d}.json",
            created,
        )


def _service_request_rows(row_count: int) -> Iterable[tuple[Any, ...]]:
    statuses = ("needs_review", "assigned", "in_progress", "complete", "rejected")
    for i in range(row_count):
        created = _created_at(i)
        yield (
            f"bench-service-request-{i:07d}",
            f"bench-service-{i % 32:02d}",
            "synthetic_capacity_request",
            _lane(i),
            f"bench-agent-{i % 24:02d}",
            statuses[i % len(statuses)],
            "local_only",
            "benchmark synthetic request flow",
            json.dumps({"synthetic": True, "row_index": i}, sort_keys=True),
            "local benchmark only",
            f"E:/agent-company-lab/work/capacity-benchmark/synthetic-request-{i:07d}.json",
            created,
            created,
        )


def _reset_target_tables(conn: sqlite3.Connection) -> None:
    for table in reversed(TARGET_TABLES):
        conn.execute(f"DELETE FROM {table}")
    conn.commit()


def _insert_scenario_rows(conn: sqlite3.Connection, row_count: int) -> dict[str, float]:
    timings: dict[str, float] = {}
    inserts = (
        (
            "tasks",
            """
            INSERT INTO tasks(
              task_id, lane_id, title, status, priority, owner_agent_id, duplicate_key,
              evidence_required, next_action, created_at, updated_at
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            _task_rows(row_count),
        ),
        (
            "artifacts",
            """
            INSERT INTO artifacts(artifact_id, lane_id, task_id, kind, path_or_url, sha256, notes, created_at)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            """,
            _artifact_rows(row_count),
        ),
        (
            "outcomes",
            """
            INSERT INTO outcomes(
              outcome_id, lane_id, task_id, outcome_type, status, realized_usd,
              evidence, next_action, created_at
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            _outcome_rows(row_count),
        ),
        (
            "trace_events",
            """
            INSERT INTO trace_events(
              event_id, trace_id, lane_id, task_id, agent_id, event_type, event_time,
              source, summary, metadata_json, artifact_path, created_at
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            _trace_rows(row_count),
        ),
        (
            "service_requests",
            """
            INSERT INTO service_requests(
              request_id, service_id, request_type, lane_id, requester_agent_id, status,
              risk_gate, requested_action, intake_json, approval_scope, artifact_path,
              created_at, updated_at
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            _service_request_rows(row_count),
        ),
    )
    for table, sql, rows in inserts:
        started = time.perf_counter()
        with conn:
            conn.executemany(sql, rows)
        timings[table] = round(time.perf_counter() - started, 6)
    return timings


def _index_names(conn: sqlite3.Connection, table: str) -> list[str]:
    return sorted(row["name"] for row in conn.execute(f"PRAGMA index_list({table})") if row["name"].startswith("idx_"))


def _table_counts(conn: sqlite3.Connection) -> dict[str, int]:
    return {table: int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]) for table in TARGET_TABLES}


def _query_plan(conn: sqlite3.Connection, sql: str, params: tuple[Any, ...]) -> list[str]:
    return [str(row["detail"]) for row in conn.execute(f"EXPLAIN QUERY PLAN {sql}", params)]


def _measure_query(conn: sqlite3.Connection, label: str, sql: str, params: tuple[Any, ...]) -> dict[str, Any]:
    started = time.perf_counter()
    rows = [dict(row) for row in conn.execute(sql, params).fetchall()]
    elapsed = round(time.perf_counter() - started, 6)
    return {
        "label": label,
        "seconds": elapsed,
        "rows_returned": len(rows),
        "plan": _query_plan(conn, sql, params),
    }


def _query_timings(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    queries = (
        (
            "count_open_tasks",
            "SELECT COUNT(*) AS count FROM tasks WHERE status != ?",
            ("complete",),
        ),
        (
            "lane_recent_tasks",
            """
            SELECT task_id, status, priority, created_at
            FROM tasks
            WHERE lane_id = ?
            ORDER BY created_at DESC
            LIMIT 25
            """,
            ("platform_engineering",),
        ),
        (
            "status_priority_backlog",
            """
            SELECT task_id, lane_id, priority, created_at
            FROM tasks
            WHERE status = ?
            ORDER BY priority DESC, created_at ASC
            LIMIT 25
            """,
            ("new",),
        ),
        (
            "lane_recent_artifacts",
            """
            SELECT artifact_id, task_id, kind, created_at
            FROM artifacts
            WHERE lane_id = ?
            ORDER BY created_at DESC
            LIMIT 25
            """,
            ("platform_engineering",),
        ),
        (
            "task_artifact_outcome_join",
            """
            SELECT t.task_id, a.artifact_id, o.outcome_id
            FROM tasks t
            LEFT JOIN artifacts a ON a.task_id = t.task_id
            LEFT JOIN outcomes o ON o.task_id = t.task_id
            WHERE t.lane_id = ?
            ORDER BY t.created_at DESC
            LIMIT 50
            """,
            ("platform_engineering",),
        ),
        (
            "service_request_status_queue",
            """
            SELECT request_id, lane_id, created_at
            FROM service_requests
            WHERE status = ?
            ORDER BY created_at ASC
            LIMIT 25
            """,
            ("needs_review",),
        ),
    )
    return [_measure_query(conn, label, sql, params) for label, sql, params in queries]


def _format_seconds(value: float) -> str:
    return f"{value:.6f}s"


def _write_report(path: Path, result: dict[str, Any]) -> None:
    lines = [
        "# Control Plane Capacity Benchmark Runner V1",
        "",
        f"Generated: `{result['generated_at']}`",
        f"Status: `{result['status']}`",
        f"JSON mirror: `{result['json_path']}`",
        f"Synthetic DB: `{result['synthetic_db_path']}`",
        "",
        "## Non-Destructive Contract",
        "",
        "- Production database rows inserted by benchmark: `0`",
        "- External network/API calls: `false`",
        "- Accounts created: `0`",
        "- Input data: deterministic synthetic rows only",
        "",
        "## Scenario Timings",
        "",
        "| Rows per table | Total insert | Slowest query | Slowest seconds | DB MB |",
        "| ---: | ---: | --- | ---: | ---: |",
    ]
    for scenario in result["scenarios"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(scenario["row_count"]),
                    _format_seconds(scenario["insert_total_seconds"]),
                    scenario["slowest_query"]["label"],
                    _format_seconds(float(scenario["slowest_query"]["seconds"])),
                    f"{scenario['db_size_bytes'] / (1024 * 1024):.2f}",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Applied Index Check",
            "",
        ]
    )
    for table, expected in CAPACITY_INDEXES.items():
        observed = result["index_check"].get(table, [])
        missing = [name for name in expected if name not in observed]
        status = "ok" if not missing else f"missing {', '.join(missing)}"
        lines.append(f"- `{table}`: `{status}` ({', '.join(observed)})")
    lines.extend(
        [
            "",
            "## Query Plans",
            "",
        ]
    )
    for scenario in result["scenarios"]:
        lines.append(f"### {scenario['row_count']} Rows Per Table")
        lines.append("")
        for query in scenario["query_timings"]:
            plan = " / ".join(query["plan"])
            lines.append(f"- `{query['label']}`: `{_format_seconds(float(query['seconds']))}`; plan: {plan}")
        lines.append("")
    lines.extend(
        [
            "## Next Action",
            "",
            "Use this runner after material schema/report changes and before adding durable workflow engines. "
            "Escalate to 500,000 and 1,000,000 rows when the control plane starts queueing real worker volume.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _default_paths(run_id: str, work_dir: Path, report_path: str | None, json_path: str | None) -> tuple[Path, Path, Path]:
    synthetic_db = work_dir / f"control_plane_capacity_benchmark_runner_v1_{run_id}.sqlite"
    report = Path(report_path) if report_path else REPORTS_DIR / f"control-plane-capacity-benchmark-runner-v1-{run_id}.md"
    json_report = Path(json_path) if json_path else REPORTS_DIR / f"control-plane-capacity-benchmark-runner-v1-{run_id}.json"
    return synthetic_db, report, json_report


def run_capacity_benchmark(args: argparse.Namespace) -> dict[str, Any]:
    row_counts = parse_row_counts(args.row_counts)
    generated_at = now_utc()
    run_id = args.run_id or generated_at.replace(":", "").replace("-", "").replace("T", "-").replace("Z", "Z")
    work_dir = Path(args.work_dir) if args.work_dir else DEFAULT_WORK_DIR
    synthetic_db, report_path, json_path = _default_paths(run_id, work_dir, args.path, args.json_path)
    work_dir.mkdir(parents=True, exist_ok=True)
    if synthetic_db.exists() and not args.overwrite:
        raise SystemExit(f"Synthetic DB already exists: {synthetic_db}. Use --overwrite or a different --run-id.")
    if synthetic_db.exists():
        synthetic_db.unlink()

    conn = sqlite3.connect(synthetic_db)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = OFF")
    conn.execute("PRAGMA journal_mode = OFF")
    conn.execute("PRAGMA synchronous = OFF")
    try:
        init_db(conn)
        index_check = {table: _index_names(conn, table) for table in CAPACITY_INDEXES}
        scenarios = []
        for row_count in row_counts:
            _reset_target_tables(conn)
            insert_timings = _insert_scenario_rows(conn, row_count)
            conn.execute("ANALYZE")
            table_counts = _table_counts(conn)
            query_timings = _query_timings(conn)
            slowest_query = max(query_timings, key=lambda item: item["seconds"])
            scenarios.append(
                {
                    "row_count": row_count,
                    "table_counts": table_counts,
                    "insert_timings": insert_timings,
                    "insert_total_seconds": round(sum(insert_timings.values()), 6),
                    "query_timings": query_timings,
                    "slowest_query": slowest_query,
                    "db_size_bytes": synthetic_db.stat().st_size,
                }
            )
    finally:
        conn.close()

    result = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "status": "benchmark_complete_non_destructive",
        "run_id": run_id,
        "row_counts": list(row_counts),
        "target_tables": list(TARGET_TABLES),
        "synthetic_db_path": str(synthetic_db),
        "report_path": str(report_path),
        "json_path": str(json_path),
        "index_check": index_check,
        "scenarios": scenarios,
        "runtime_boundary": {
            "production_rows_inserted_by_benchmark": 0,
            "external_network_calls": False,
            "accounts_created": 0,
            "browser_sessions_started": 0,
            "synthetic_data_only": True,
        },
        "capacity_policy": [
            "Run after schema changes touching tasks, artifacts, outcomes, trace events, or service requests.",
            "Run before introducing external workflow engines or high-volume worker queues.",
            "Use 500000 and 1000000 row scenarios before claiming production-scale readiness.",
        ],
    }
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(report_path, result)
    return result


def write_control_plane_capacity_benchmark_runner(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    del conn
    result = run_capacity_benchmark(args)
    print(
        json.dumps(
            {
                "ok": True,
                "run_id": result["run_id"],
                "report_path": result["report_path"],
                "json_path": result["json_path"],
                "synthetic_db_path": result["synthetic_db_path"],
                "row_counts": result["row_counts"],
            },
            indent=2,
        )
    )
