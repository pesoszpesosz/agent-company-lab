from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .constants import PROMPT_EVAL_REPORT
from .io import now_utc
from .paths import DB_PATH
from .utils import decode_json_list, md_cell, parse_json_arg, read_text_arg, sha256_text

def record_prompt_template(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    ts = now_utc()
    stop_gates = parse_json_arg(args.default_stop_gates_json, args.default_stop_gates_file, [])
    conn.execute(
        """
        INSERT INTO prompt_templates(
          template_id, lane_id, name, purpose, owner_agent_id, default_stop_gates_json,
          created_at, updated_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(template_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          name=excluded.name,
          purpose=excluded.purpose,
          owner_agent_id=excluded.owner_agent_id,
          default_stop_gates_json=excluded.default_stop_gates_json,
          updated_at=excluded.updated_at
        """,
        (
            args.template_id,
            args.lane_id,
            args.name,
            args.purpose,
            args.owner_agent_id,
            stop_gates,
            ts,
            ts,
        ),
    )
    conn.commit()
    print(json.dumps({"ok": True, "template_id": args.template_id}, indent=2))


def record_prompt_version(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    prompt_text = read_text_arg(args.prompt_text, args.prompt_file, "record-prompt-version")
    ts = now_utc()
    digest = sha256_text(prompt_text)
    conn.execute(
        """
        INSERT INTO prompt_versions(
          prompt_version_id, template_id, version_label, prompt_text, source_artifact_path,
          sha256, status, created_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(prompt_version_id) DO UPDATE SET
          template_id=excluded.template_id,
          version_label=excluded.version_label,
          prompt_text=excluded.prompt_text,
          source_artifact_path=excluded.source_artifact_path,
          sha256=excluded.sha256,
          status=excluded.status
        """,
        (
            args.prompt_version_id,
            args.template_id,
            args.version_label,
            prompt_text,
            args.source_artifact_path,
            digest,
            args.status,
            ts,
        ),
    )
    conn.commit()
    print(json.dumps({"ok": True, "prompt_version_id": args.prompt_version_id, "sha256": digest}, indent=2))


def record_eval_dataset(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    ts = now_utc()
    cases = parse_json_arg(args.cases_json, args.cases_file, [])
    conn.execute(
        """
        INSERT INTO eval_datasets(dataset_id, lane_id, name, purpose, cases_json, created_at, updated_at)
        VALUES(?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(dataset_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          name=excluded.name,
          purpose=excluded.purpose,
          cases_json=excluded.cases_json,
          updated_at=excluded.updated_at
        """,
        (args.dataset_id, args.lane_id, args.name, args.purpose, cases, ts, ts),
    )
    conn.commit()
    print(json.dumps({"ok": True, "dataset_id": args.dataset_id}, indent=2))


def record_eval_run(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    ts = now_utc()
    results = parse_json_arg(args.results_json, args.results_file, {})
    conn.execute(
        """
        INSERT INTO eval_runs(
          eval_run_id, dataset_id, prompt_version_id, lane_id, runner_agent_id,
          runtime, status, score, results_json, artifact_path, created_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(eval_run_id) DO UPDATE SET
          dataset_id=excluded.dataset_id,
          prompt_version_id=excluded.prompt_version_id,
          lane_id=excluded.lane_id,
          runner_agent_id=excluded.runner_agent_id,
          runtime=excluded.runtime,
          status=excluded.status,
          score=excluded.score,
          results_json=excluded.results_json,
          artifact_path=excluded.artifact_path
        """,
        (
            args.eval_run_id,
            args.dataset_id,
            args.prompt_version_id,
            args.lane_id,
            args.runner_agent_id,
            args.runtime,
            args.status,
            args.score,
            results,
            args.artifact_path,
            ts,
        ),
    )
    conn.commit()
    print(json.dumps({"ok": True, "eval_run_id": args.eval_run_id}, indent=2))


def record_human_review(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    ts = now_utc()
    conn.execute(
        """
        INSERT INTO human_reviews(
          review_id, lane_id, artifact_id, trace_id, prompt_version_id, reviewer_agent_id,
          status, decision, notes, created_at
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(review_id) DO UPDATE SET
          lane_id=excluded.lane_id,
          artifact_id=excluded.artifact_id,
          trace_id=excluded.trace_id,
          prompt_version_id=excluded.prompt_version_id,
          reviewer_agent_id=excluded.reviewer_agent_id,
          status=excluded.status,
          decision=excluded.decision,
          notes=excluded.notes
        """,
        (
            args.review_id,
            args.lane_id,
            args.artifact_id,
            args.trace_id,
            args.prompt_version_id,
            args.reviewer_agent_id,
            args.status,
            args.decision,
            args.notes,
            ts,
        ),
    )
    conn.commit()
    print(json.dumps({"ok": True, "review_id": args.review_id}, indent=2))


def write_prompt_eval_report(conn: sqlite3.Connection, path: str | None) -> None:
    output_path = Path(path) if path else PROMPT_EVAL_REPORT
    output_path.parent.mkdir(parents=True, exist_ok=True)
    templates = [dict(row) for row in conn.execute("SELECT * FROM prompt_templates ORDER BY lane_id, template_id")]
    versions = [
        dict(row)
        for row in conn.execute(
            """
            SELECT pv.*, pt.lane_id, pt.name AS template_name
            FROM prompt_versions pv
            JOIN prompt_templates pt ON pt.template_id = pv.template_id
            ORDER BY pv.created_at DESC
            """
        )
    ]
    datasets = [dict(row) for row in conn.execute("SELECT * FROM eval_datasets ORDER BY lane_id, dataset_id")]
    runs = [
        dict(row)
        for row in conn.execute(
            """
            SELECT er.*, ed.name AS dataset_name
            FROM eval_runs er
            JOIN eval_datasets ed ON ed.dataset_id = er.dataset_id
            ORDER BY er.created_at DESC
            """
        )
    ]
    reviews = [dict(row) for row in conn.execute("SELECT * FROM human_reviews ORDER BY created_at DESC")]

    lines = [
        "# Agent Company Prompt/Eval/Review Registry",
        "",
        f"Generated UTC: {now_utc()}",
        f"Database: `{DB_PATH}`",
        "",
        "## Boundary",
        "",
        "- Prompt records are not permission to run real model/API calls.",
        "- Eval runs can be dry-run/manual until a model/API service request is approved.",
        "- Human reviews record decisions; they do not bypass account, wallet, public-action, legal/KYC, security, or real-money gates.",
        "",
        "## Counts",
        "",
        f"- Prompt templates: {len(templates)}",
        f"- Prompt versions: {len(versions)}",
        f"- Eval datasets: {len(datasets)}",
        f"- Eval runs: {len(runs)}",
        f"- Human reviews: {len(reviews)}",
        "",
        "## Prompt Templates",
        "",
        "| Lane | Template | Owner | Purpose | Default Stop Gates |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in templates:
        gates = "; ".join(str(item) for item in decode_json_list(row["default_stop_gates_json"]))
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['lane_id'] or ''}`",
                    f"`{row['template_id']}` - {md_cell(row['name'], 120)}",
                    md_cell(row["owner_agent_id"], 120),
                    md_cell(row["purpose"], 220),
                    md_cell(gates, 220),
                ]
            )
            + " |"
        )
    if not templates:
        lines.append("| none |  |  |  |  |")

    lines.extend(["", "## Prompt Versions", "", "| Status | Lane | Version | Template | SHA256 | Source |", "| --- | --- | --- | --- | --- | --- |"])
    for row in versions:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(row["status"], 80),
                    f"`{row['lane_id'] or ''}`",
                    f"`{row['prompt_version_id']}` - {md_cell(row['version_label'], 120)}",
                    f"`{row['template_id']}` - {md_cell(row['template_name'], 120)}",
                    f"`{row['sha256'][:16]}`",
                    md_cell(row["source_artifact_path"], 180),
                ]
            )
            + " |"
        )
    if not versions:
        lines.append("| none |  |  |  |  |  |")

    lines.extend(["", "## Eval Datasets", "", "| Lane | Dataset | Cases | Purpose |", "| --- | --- | ---: | --- |"])
    for row in datasets:
        try:
            cases_count = len(json.loads(row["cases_json"]))
        except json.JSONDecodeError:
            cases_count = 0
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['lane_id'] or ''}`",
                    f"`{row['dataset_id']}` - {md_cell(row['name'], 120)}",
                    str(cases_count),
                    md_cell(row["purpose"], 260),
                ]
            )
            + " |"
        )
    if not datasets:
        lines.append("| none |  | 0 |  |")

    lines.extend(["", "## Eval Runs", "", "| Status | Score | Runtime | Dataset | Prompt Version | Lane | Artifact |", "| --- | ---: | --- | --- | --- | --- | --- |"])
    for row in runs:
        score = "" if row["score"] is None else str(row["score"])
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(row["status"], 80),
                    score,
                    md_cell(row["runtime"], 100),
                    f"`{row['dataset_id']}` - {md_cell(row['dataset_name'], 120)}",
                    f"`{row['prompt_version_id'] or ''}`",
                    f"`{row['lane_id'] or ''}`",
                    md_cell(row["artifact_path"], 180),
                ]
            )
            + " |"
        )
    if not runs:
        lines.append("| none |  |  |  |  |  |  |")

    lines.extend(["", "## Human Reviews", "", "| Status | Decision | Lane | Review | Artifact | Trace | Prompt Version | Notes |", "| --- | --- | --- | --- | --- | --- | --- | --- |"])
    for row in reviews:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(row["status"], 80),
                    md_cell(row["decision"], 120),
                    f"`{row['lane_id'] or ''}`",
                    f"`{row['review_id']}`",
                    f"`{row['artifact_id'] or ''}`",
                    f"`{row['trace_id'] or ''}`",
                    f"`{row['prompt_version_id'] or ''}`",
                    md_cell(row["notes"], 220),
                ]
            )
            + " |"
        )
    if not reviews:
        lines.append("| none |  |  |  |  |  |  |  |")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": True,
                "path": str(output_path),
                "templates": len(templates),
                "versions": len(versions),
                "datasets": len(datasets),
                "runs": len(runs),
                "reviews": len(reviews),
            },
            indent=2,
        )
    )


