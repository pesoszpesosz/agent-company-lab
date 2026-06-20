from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

from .catalog import upsert_source_spec
from .constants import (
    COMPANY_EXPANSION_GAP_MAP_JSON,
    SOURCE_SPECS_REPORT,
    SOURCE_SPEC_SEED_APPLY_JSON,
    SOURCE_SPEC_SEED_APPLY_REPORT,
    SOURCE_SPEC_SEED_APPLY_VALIDATION_JSON,
    SOURCE_SPEC_SEED_PACKETS_JSON,
    SOURCE_SPEC_SEED_PACKETS_REPORT,
    SOURCE_SPEC_SEED_PACKETS_VALIDATION_JSON,
    SOURCE_SPEC_SEED_PACKET_DIR,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR, SOURCE_SPECS_PATH
from .service_workers import db_scalar, load_report_json_or_error
from .utils import decode_json_list, md_cell

def write_source_specs_report(conn: sqlite3.Connection, path: str | None) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(path) if path else SOURCE_SPECS_REPORT
    rows = [
        dict(row)
        for row in conn.execute(
            """
            SELECT spec_id, lane_id, name, source_type, source_paths_json, refresh_command,
                   cadence, risk_gate, outputs_json, notes
            FROM source_specs
            ORDER BY lane_id, spec_id
            """
        )
    ]
    lines = [
        "# Agent Company Source Specs",
        "",
        f"Generated UTC: {now_utc()}",
        f"Source definition: `{SOURCE_SPECS_PATH}`",
        "",
        "## Boundary",
        "",
        "- Each source spec belongs to exactly one lane.",
        "- Refresh commands are instructions for lane owners, not blanket permission to execute side effects.",
        "- Browser, account, wallet, public-action, legal/KYC/billing, and real-money gates still require service requests.",
        "",
        "## Specs",
        "",
        "| Lane | Spec | Type | Cadence | Gate | Outputs |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        outputs = "; ".join(str(item) for item in decode_json_list(row["outputs_json"]))
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['lane_id']}`",
                    f"`{row['spec_id']}` - {md_cell(row['name'], 160)}",
                    md_cell(row["source_type"], 80),
                    md_cell(row["cadence"], 120),
                    md_cell(row["risk_gate"], 220),
                    md_cell(outputs, 260),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Detail", ""])
    for row in rows:
        source_paths = decode_json_list(row["source_paths_json"])
        outputs = decode_json_list(row["outputs_json"])
        lines.extend(
            [
                f"### {row['spec_id']}",
                "",
                f"- Lane: `{row['lane_id']}`",
                f"- Name: {row['name']}",
                f"- Type: `{row['source_type']}`",
                f"- Cadence: `{row['cadence']}`",
                f"- Gate: `{row['risk_gate']}`",
                f"- Refresh command: `{row['refresh_command'] or ''}`",
                f"- Notes: {row['notes'] or ''}",
                "- Sources:",
            ]
        )
        lines.extend([f"  - `{item}`" for item in source_paths] or ["  - none"])
        lines.append("- Outputs:")
        lines.extend([f"  - `{item}`" for item in outputs] or ["  - none"])
        lines.append("")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(output_path), "count": len(rows)}, indent=2))
