from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .catalog import department_id
from .constants import LANE_THREAD_MANIFEST_JSON, LANE_THREAD_MANIFEST_MD
from .control_reports import lane_recommendation, suggested_manager_task
from .io import now_utc
from .paths import DB_PATH, LAUNCH_DIR, MANAGER_PACKET_DIR, REPORTS_DIR
from .utils import decode_json_list, md_cell, safe_id_fragment


THREAD_LAUNCH_ORDER = [
    "money_source_discovery",
    "ai_ml_competitions",
    "digital_products_templates_plugins",
    "security_bounty_private_reports",
    "prediction_market_research",
    "paid_code_bounties",
    "content_and_social_growth",
    "web3_airdrops_grants_hackathons",
    "lead_generation_and_sales",
    "local_trading_strategy_research",
]

THREAD_HELD_LANES = {
    "platform_engineering": "This recovered thread is the platform coordinator and should keep ownership here.",
    "submitted_bounty_payouts": "Read-only in this lab. The parallel payout worker owns GitHub/RustChain/Charles payout monitoring.",
}

def write_launch_packets(conn: sqlite3.Connection) -> None:
    LAUNCH_DIR.mkdir(parents=True, exist_ok=True)
    lanes = [dict(row) for row in conn.execute("SELECT * FROM lanes ORDER BY lane_id")]
    written: list[str] = []
    for lane in lanes:
        agent_types = decode_json_list(lane["agent_types_json"])
        examples = decode_json_list(lane["examples_json"])
        promotion_gates = decode_json_list(lane["promotion_gates_json"])
        service_workers = decode_json_list(lane["service_workers_required_json"])
        side_effects = decode_json_list(lane["side_effects_json"])
        global_gates = decode_json_list(lane["global_gates_json"])
        owner_note = ""
        if lane["owner_agent_id"] or lane["owner_thread_id"]:
            owner_note = f"\nCurrent owner: `{lane['owner_agent_id'] or ''}` / `{lane['owner_thread_id'] or ''}`.\n"

        lines = [
            f"# Launch Packet - {lane['lane_id']}",
            "",
            f"Generated UTC: {now_utc()}",
            f"Department: {lane['department']}",
            f"Lane status: {lane['status']}",
            owner_note.strip(),
            "",
            "## Mission",
            "",
            f"Own the `{lane['lane_id']}` lane inside the agent-company system. Work only inside this lane unless a manager explicitly assigns a task from another lane.",
            "",
            "## Allowed Work",
            "",
        ]
        lines.extend([f"- {item}" for item in agent_types] or ["- No agent types configured."])
        lines.extend(["", "## Examples", ""])
        lines.extend([f"- {item}" for item in examples] or ["- No examples configured."])
        lines.extend(["", "## Promotion Gates", ""])
        lines.extend([f"- {item}" for item in promotion_gates] or ["- No promotion gates configured."])
        lines.extend(["", "## Required Service Workers", ""])
        lines.extend([f"- {item}" for item in service_workers] or ["- None configured."])
        lines.extend(["", "## Side Effects", ""])
        if side_effects:
            lines.append("Do not perform these directly unless the control plane task and service-request gate explicitly allow it:")
            lines.extend([f"- {item}" for item in side_effects])
        else:
            lines.append("No side effects configured.")
        lines.extend(["", "## Global Gates", ""])
        lines.extend([f"- {item}" for item in global_gates])
        lines.extend(
            [
                "",
                "## Start Procedure",
                "",
                "1. Read `E:\\agent-company-lab\\README.md`.",
                "2. Run `python E:\\agent-company-lab\\tools\\agent_company.py status`.",
                f"3. If this lane is unowned, register your agent and claim `{lane['lane_id']}`.",
                "4. Create or acquire exactly one task with a duplicate key.",
                "5. Write artifacts under `E:\\agent-company-lab\\reports` or `E:\\agent-company-lab\\data`.",
                "6. Record artifacts and outcomes through `agent_company.py`.",
                "7. Stop at service-request gates for registration, wallet, legal/KYC, payment, public posting, or real-money actions.",
                "",
                "## Suggested Initial Prompt",
                "",
                "```text",
                f"You are the department manager for `{lane['lane_id']}` in `E:\\agent-company-lab`. Read the lab README, run the control-plane status command, avoid duplicate lane ownership, then perform one concrete task that advances this lane. Record all artifacts and outcomes in the control plane. Do not perform gated side effects.",
                "```",
                "",
            ]
        )
        packet_path = LAUNCH_DIR / f"{lane['lane_id']}-launch-packet.md"
        packet_path.write_text("\n".join([line for line in lines if line is not None]) + "\n", encoding="utf-8")
        written.append(str(packet_path))
    print(json.dumps({"ok": True, "count": len(written), "paths": written}, indent=2))
