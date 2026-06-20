#!/usr/bin/env python3
"""Synthetic ARC-style toy harness with no official data access."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


Grid = list[list[int]]

DEFAULT_FIXTURE = Path(r"E:\agent-company-lab\reports\ai-ml-competitions\arc-toy-harness-fixture-20260616.json")
DEFAULT_JSON_OUT = Path(r"E:\agent-company-lab\reports\ai-ml-competitions\arc-toy-harness-run-20260616.json")
DEFAULT_MD_OUT = Path(r"E:\agent-company-lab\reports\ai-ml-competitions\arc-toy-harness-run-20260616.md")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clone(grid: Grid) -> Grid:
    return deepcopy(grid)


def crop_nonzero(grid: Grid) -> Grid:
    coords = [(r, c) for r, row in enumerate(grid) for c, value in enumerate(row) if value != 0]
    if not coords:
        return [[]]
    min_r = min(r for r, _ in coords)
    max_r = max(r for r, _ in coords)
    min_c = min(c for _, c in coords)
    max_c = max(c for _, c in coords)
    return [row[min_c : max_c + 1] for row in grid[min_r : max_r + 1]]


def translate(grid: Grid, dx: int, dy: int) -> Grid:
    height = len(grid)
    width = len(grid[0]) if height else 0
    out = [[0 for _ in range(width)] for _ in range(height)]
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 0:
                continue
            nr = r + dy
            nc = c + dx
            if 0 <= nr < height and 0 <= nc < width:
                out[nr][nc] = value
    return out


def recolor(grid: Grid, src: int, dst: int) -> Grid:
    return [[dst if value == src else value for value in row] for row in grid]


def mirror_x(grid: Grid) -> Grid:
    return [list(reversed(row)) for row in grid]


def mirror_y(grid: Grid) -> Grid:
    return list(reversed(clone(grid)))


def tile(grid: Grid, nx: int, ny: int) -> Grid:
    tiled_rows: Grid = []
    for _ in range(ny):
        for row in grid:
            new_row: list[int] = []
            for _ in range(nx):
                new_row.extend(row)
            tiled_rows.append(new_row)
    return tiled_rows


def fill_bbox(grid: Grid, color: int) -> Grid:
    out = clone(grid)
    coords = [(r, c) for r, row in enumerate(grid) for c, value in enumerate(row) if value != 0]
    if not coords:
        return out
    min_r = min(r for r, _ in coords)
    max_r = max(r for r, _ in coords)
    min_c = min(c for _, c in coords)
    max_c = max(c for _, c in coords)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            out[r][c] = color
    return out


def colors(grid: Grid) -> set[int]:
    return {value for row in grid for value in row if value != 0}


def candidate_programs(train_inputs: list[Grid], train_outputs: list[Grid]) -> list[tuple[str, Callable[[Grid], Grid]]]:
    palette = sorted(set().union(*(colors(g) for g in train_inputs), *(colors(g) for g in train_outputs)))
    programs: list[tuple[str, Callable[[Grid], Grid]]] = [
        ("identity", clone),
        ("translate(1, 0)", lambda g: translate(g, 1, 0)),
        ("translate(-1, 0)", lambda g: translate(g, -1, 0)),
        ("translate(0, 1)", lambda g: translate(g, 0, 1)),
        ("translate(0, -1)", lambda g: translate(g, 0, -1)),
        ("mirror(x)", mirror_x),
        ("mirror(y)", mirror_y),
        ("crop_nonzero", crop_nonzero),
        ("compose(crop_nonzero, tile(2, 1))", lambda g: tile(crop_nonzero(g), 2, 1)),
        ("compose(crop_nonzero, tile(1, 2))", lambda g: tile(crop_nonzero(g), 1, 2)),
    ]
    for src in palette:
        for dst in palette:
            if src != dst:
                programs.append((f"recolor({src}, {dst})", lambda g, s=src, d=dst: recolor(g, s, d)))
    for color in palette:
        programs.append((f"fill_bbox({color})", lambda g, c=color: fill_bbox(g, c)))
    return programs


def solve_task(task: dict[str, Any]) -> dict[str, Any]:
    train_inputs = [example["input"] for example in task["train"]]
    train_outputs = [example["output"] for example in task["train"]]
    candidates = candidate_programs(train_inputs, train_outputs)
    inspected: list[dict[str, Any]] = []
    passing: list[tuple[str, Callable[[Grid], Grid]]] = []
    for name, fn in candidates:
        outputs = [fn(grid) for grid in train_inputs]
        matches = sum(1 for actual, expected in zip(outputs, train_outputs) if actual == expected)
        inspected.append({"program": name, "train_matches": matches, "train_total": len(train_outputs)})
        if matches == len(train_outputs):
            passing.append((name, fn))
    if not passing:
        return {
            "task_id": task["task_id"],
            "family": task["family"],
            "selected_program": "no_solution",
            "test_output": None,
            "expected_program": task["expected_program"],
            "expected_test_output": task["expected_test_output"],
            "passed": task["expected_program"] == "no_solution",
            "inspected_candidates": inspected[:12],
        }
    name, fn = passing[0]
    output = fn(task["test_input"])
    return {
        "task_id": task["task_id"],
        "family": task["family"],
        "selected_program": name,
        "test_output": output,
        "expected_program": task["expected_program"],
        "expected_test_output": task["expected_test_output"],
        "passed": name == task["expected_program"] and output == task["expected_test_output"],
        "inspected_candidates": inspected[:12],
    }


def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# ARC Toy Harness Run",
        "",
        f"Generated UTC: {result['generated_utc']}",
        f"Fixture: `{result['fixture_path']}`",
        f"JSON mirror: `{result['json_path']}`",
        "",
        "## Summary",
        "",
        f"- Tasks checked: `{result['tasks_checked']}`",
        f"- Passed: `{result['passed_count']}`",
        f"- Failed: `{result['failed_count']}`",
        f"- Official ARC data used: `{str(result['official_arc_data_used']).lower()}`",
        f"- Kaggle/gated data used: `{str(result['kaggle_or_gated_data_used']).lower()}`",
        f"- External side effects: `{str(result['external_side_effects']).lower()}`",
        "",
        "## Rows",
        "",
        "| Task | Family | Selected Program | Status |",
        "| --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        status = "pass" if row["passed"] else "fail"
        lines.append(f"| `{row['task_id']}` | `{row['family']}` | `{row['selected_program']}` | `{status}` |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Official ARC data: `false`",
            "- Kaggle login/download: `false`",
            "- Paid compute/API: `false`",
            "- Submission/public action: `false`",
            "- External side effects: `false`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_OUT)
    parser.add_argument("--md-out", type=Path, default=DEFAULT_MD_OUT)
    args = parser.parse_args()

    fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
    rows = [solve_task(task) for task in fixture["tasks"]]
    failed_count = sum(1 for row in rows if not row["passed"])
    result = {
        "schema_version": "agent_company.arc_toy_harness_run.v1",
        "generated_utc": utc_now(),
        "fixture_path": str(args.fixture),
        "json_path": str(args.json_out),
        "markdown_path": str(args.md_out),
        "tasks_checked": len(rows),
        "passed_count": len(rows) - failed_count,
        "failed_count": failed_count,
        "official_arc_data_used": False,
        "kaggle_or_gated_data_used": False,
        "paid_compute_or_api": False,
        "external_side_effects": False,
        "rows": rows,
    }
    args.json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(result, args.md_out)
    print(json.dumps({"ok": failed_count == 0, "json": str(args.json_out), "failed_count": failed_count}, indent=2))
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
