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

def lane_launch_hard_stop(lane_id: str) -> str:
    stops = {
        "security_bounty_private_reports": (
            "Read public source and local clones only. No live target testing, report submission, disclosure email, "
            "PR, issue, or account action without an approved service request."
        ),
        "prediction_market_research": (
            "Paper/data-only. No account setup, deposit, withdrawal, order, trade, market manipulation, or advice "
            "framed as a guaranteed profit."
        ),
        "paid_code_bounties": (
            "Scout and rank only. No PR, issue comment, bounty claim, marketplace submission, or maintainer contact "
            "until payout terms, duplicate risk, and ownership are approved."
        ),
        "content_and_social_growth": (
            "Read-only social research. No posts, replies, likes, follows, DMs, profile edits, settings changes, "
            "or Grok/X browser actions unless the service request is approved."
        ),
        "web3_airdrops_grants_hackathons": (
            "Terms/deadline research only. No wallet creation, wallet connection, signature, transaction, deployment, "
            "account registration, or private-key handling."
        ),
        "lead_generation_and_sales": (
            "Design offer and targeting rules only. No outreach account, email, DM, call, form submission, scraping "
            "against site rules, or CRM upload."
        ),
        "local_trading_strategy_research": (
            "Local backtest and paper evidence only. No broker connection, API key use, order routing, live signal, "
            "or real-money execution."
        ),
        "money_source_discovery": (
            "Read-only source mapping only. No signup, claim, application, scraping against rules, API key, payment, "
            "public comment, or browser action unless the service request is approved."
        ),
        "ai_ml_competitions": (
            "Competition research and local baseline planning only. No account creation, competition join, dataset "
            "download, rule acceptance, notebook submission, payment, or public action."
        ),
        "digital_products_templates_plugins": (
            "Product research and local prototype planning only. No marketplace account, listing, upload, purchase, "
            "payment setup, review, message, or public promotion."
        ),
        "platform_engineering": (
            "Coordinator lane only. Do not duplicate lane manager work or run real model/API mode without an approved "
            "provider, model, max cost, lane scope, and artifact path."
        ),
        "submitted_bounty_payouts": (
            "Read-only visibility only. Do not monitor, comment, claim, submit, or chase RustChain/Charles/GitHub "
            "payouts from this lab."
        ),
    }
    return stops.get(
        lane_id,
        "Research, draft, and write local artifacts only. Any account, public, payment, security, browser, or real-money side effect needs an approved service request.",
    )


def manager_thread_prompt(lane: dict[str, Any], packet_path: Path, recommended_task: str) -> str:
    lane_id = lane["lane_id"]
    dep_id = department_id(lane["department"])
    agent_id = f"lane-manager-{safe_id_fragment(lane_id, 48)}-THREAD"
    task_id = f"task-{safe_id_fragment(lane_id, 48)}-startup-YYYYMMDD"
    artifact_path = f"E:\\agent-company-lab\\reports\\lane-startup\\{lane_id}-startup-YYYYMMDD.md"
    trace_id = f"trace-{safe_id_fragment(lane_id, 48)}-manager-startup-YYYYMMDD"
    return "\n".join(
        [
            f"You are the separate department manager for `{lane_id}` in `E:\\agent-company-lab`.",
            "",
            "This is a parallel lane-manager chat. Stay in this lane. Do not work the submitted GitHub payout lane unless the user explicitly reassigns that lane to you.",
            "",
            "Read first:",
            "- `E:\\agent-company-lab\\README.md`",
            f"- `{packet_path}`",
            "",
            "Before running commands, replace `THREAD`, `THIS_THREAD_ID`, and `YYYYMMDD` with your actual short thread label, Codex thread id, and date.",
            "",
            "Startup commands:",
            "```powershell",
            f"python E:\\agent-company-lab\\tools\\agent_company.py register-agent --agent-id {agent_id} --role-id department_manager --department-id {dep_id} --thread-id THIS_THREAD_ID",
            "python E:\\agent-company-lab\\tools\\agent_company.py status",
            f"python E:\\agent-company-lab\\tools\\agent_company.py list-source-specs --lane-id {lane_id}",
            f"python E:\\agent-company-lab\\tools\\agent_company.py list-evidence --lane-id {lane_id} --limit 25",
            f"python E:\\agent-company-lab\\tools\\agent_company.py claim-lane --lane-id {lane_id} --agent-id {agent_id} --thread-id THIS_THREAD_ID",
            "```",
            "",
            "Your first concrete task:",
            recommended_task,
            "",
            "Create/acquire exactly one scoped task before doing lane work:",
            "```powershell",
            f"python E:\\agent-company-lab\\tools\\agent_company.py create-task --task-id {task_id} --lane-id {lane_id} --title \"Lane startup: read packet, choose first proof task, write local plan\" --priority 70 --owner-agent-id {agent_id} --duplicate-key {lane_id}-startup-YYYYMMDD --evidence-required \"Local startup memo, source list, gates, and one next proof artifact\" --next-action \"Write startup memo, then choose one narrow proof task.\"",
            f"python E:\\agent-company-lab\\tools\\agent_company.py acquire-task --task-id {task_id} --agent-id {agent_id} --lease-minutes 240",
            "```",
            "",
            "Hard stop:",
            lane_launch_hard_stop(lane_id),
            "",
            "Deliverables for this first manager turn:",
            f"- Write `{artifact_path}` with what you learned, what you will test first, and every stop gate.",
            "- Record the artifact in the control plane.",
            "- Record an outcome with `realized_usd=0` unless money has actually arrived.",
            "- Record a trace event tying the decision to the startup artifact.",
            "- Refresh the manager packet and dashboard after the artifact/outcome/trace are recorded.",
            "",
            "Do not claim success from plans, merged-looking signals, or expected value. The lane advances only when it has a saved artifact, reproducible evidence, or an explicitly gated next action.",
            "",
            "Useful recording commands after the startup memo exists:",
            "```powershell",
            f"python E:\\agent-company-lab\\tools\\agent_company.py record-artifact --artifact-id artifact-{safe_id_fragment(lane_id, 48)}-startup-YYYYMMDD --lane-id {lane_id} --task-id {task_id} --kind lane_startup_memo --path-or-url {artifact_path} --notes \"First lane-manager startup memo and gated work plan.\"",
            f"python E:\\agent-company-lab\\tools\\agent_company.py record-outcome --outcome-id outcome-{safe_id_fragment(lane_id, 48)}-startup-YYYYMMDD --lane-id {lane_id} --task-id {task_id} --outcome-type lane_startup --status planned_next_proof --realized-usd 0 --evidence {artifact_path} --next-action \"Execute one approved local proof task only.\"",
            f"python E:\\agent-company-lab\\tools\\agent_company.py record-trace-event --trace-id {trace_id} --lane-id {lane_id} --task-id {task_id} --agent-id {agent_id} --event-type lane_manager_started --summary \"Lane manager started from launch manifest and wrote startup memo.\" --artifact-path {artifact_path}",
            f"python E:\\agent-company-lab\\tools\\agent_company.py complete-task --task-id {task_id} --agent-id {agent_id} --next-action \"Create the first narrow proof task from the startup memo.\"",
            "python E:\\agent-company-lab\\tools\\agent_company.py write-manager-packets",
            "python E:\\agent-company-lab\\tools\\agent_company.py write-dashboard",
            "```",
        ]
    )


def write_lane_thread_manifest(conn: sqlite3.Connection, md_path: str | None, json_path: str | None) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_md = Path(md_path) if md_path else LANE_THREAD_MANIFEST_MD
    output_json = Path(json_path) if json_path else LANE_THREAD_MANIFEST_JSON
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)

    lanes = {row["lane_id"]: dict(row) for row in conn.execute("SELECT * FROM lanes ORDER BY lane_id")}
    evidence_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute("SELECT lane_id, COUNT(*) AS count FROM lane_evidence GROUP BY lane_id")
    }
    active_task_counts = {
        row["lane_id"]: row["count"]
        for row in conn.execute(
            "SELECT lane_id, COUNT(*) AS count FROM tasks WHERE status NOT IN ('complete', 'cancelled') GROUP BY lane_id"
        )
    }
    service_request_counts = {
        row["lane_id"] or "unassigned": row["count"]
        for row in conn.execute(
            "SELECT COALESCE(lane_id, 'unassigned') AS lane_id, COUNT(*) AS count FROM service_requests WHERE status NOT IN ('complete', 'cancelled') GROUP BY COALESCE(lane_id, 'unassigned')"
        )
    }
    status_counts_by_lane: dict[str, dict[str, int]] = {}
    for row in conn.execute("SELECT lane_id, status, COUNT(*) AS count FROM lane_evidence GROUP BY lane_id, status"):
        status_counts_by_lane.setdefault(row["lane_id"], {})[row["status"]] = row["count"]

    launch_queue: list[dict[str, Any]] = []
    launched_lane_ids: set[str] = set()
    for priority, lane_id in enumerate(THREAD_LAUNCH_ORDER, start=1):
        lane = lanes.get(lane_id)
        if not lane:
            continue
        launched_lane_ids.add(lane_id)
        packet_path = MANAGER_PACKET_DIR / f"{lane_id}-manager-packet.md"
        recommended_task = suggested_manager_task(lane_id)
        launch_queue.append(
            {
                "launch_rank": priority,
                "lane_id": lane_id,
                "department": lane["department"],
                "mode": "launch_separate_codex_manager_thread",
                "owner": lane["owner_agent_id"] or lane["owner_thread_id"] or "unowned",
                "packet_path": str(packet_path),
                "evidence_count": evidence_counts.get(lane_id, 0),
                "open_task_count": active_task_counts.get(lane_id, 0),
                "open_service_request_count": service_request_counts.get(lane_id, 0),
                "recommended_task": recommended_task,
                "ceo_recommendation": lane_recommendation(
                    lane_id,
                    status_counts_by_lane.get(lane_id, {}),
                    active_task_counts.get(lane_id, 0),
                    service_request_counts.get(lane_id, 0),
                ),
                "hard_stop": lane_launch_hard_stop(lane_id),
                "initial_prompt": manager_thread_prompt(lane, packet_path, recommended_task),
            }
        )

    held_lanes: list[dict[str, Any]] = []
    for lane_id, reason in sorted(THREAD_HELD_LANES.items()):
        lane = lanes.get(lane_id)
        if not lane:
            continue
        held_lanes.append(
            {
                "lane_id": lane_id,
                "department": lane["department"],
                "mode": "do_not_launch_from_this_manifest",
                "owner": lane["owner_agent_id"] or lane["owner_thread_id"] or "unowned",
                "reason": reason,
                "packet_path": str(MANAGER_PACKET_DIR / f"{lane_id}-manager-packet.md"),
                "hard_stop": lane_launch_hard_stop(lane_id),
            }
        )

    for lane_id, lane in sorted(lanes.items()):
        if lane_id in launched_lane_ids or lane_id in THREAD_HELD_LANES:
            continue
        held_lanes.append(
            {
                "lane_id": lane_id,
                "department": lane["department"],
                "mode": "unranked_review_before_launch",
                "owner": lane["owner_agent_id"] or lane["owner_thread_id"] or "unowned",
                "reason": "Lane is not in the approved launch order yet.",
                "packet_path": str(MANAGER_PACKET_DIR / f"{lane_id}-manager-packet.md"),
                "hard_stop": lane_launch_hard_stop(lane_id),
            }
        )

    payload = {
        "generated_utc": now_utc(),
        "database": str(DB_PATH),
        "purpose": "Start separate lane-manager Codex chats without duplicating the platform coordinator or submitted-payout worker.",
        "boundary": [
            "This manifest launches only manager research/proof lanes.",
            "Each manager owns exactly one lane and one active task at a time.",
            "No account, wallet, browser-public, legal/KYC/tax/billing/payment, external security testing, public posting, PR/comment/submission, or real-money action is allowed without an approved service request.",
            "submitted_bounty_payouts remains read-only and assigned to the parallel payout worker.",
        ],
        "launch_queue": launch_queue,
        "held_lanes": held_lanes,
    }
    output_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Lane Manager Thread Launch Manifest",
        "",
        f"Generated UTC: {payload['generated_utc']}",
        f"Database: `{DB_PATH}`",
        f"JSON: `{output_json}`",
        "",
        "## Purpose",
        "",
        "Create separate Codex lane-manager chats from the existing agent-company control plane without merging their work with this platform thread or the parallel submitted-payout worker.",
        "",
        "## Boundaries",
        "",
    ]
    lines.extend([f"- {item}" for item in payload["boundary"]])
    lines.extend(
        [
            "",
            "## Launch Queue",
            "",
            "| Rank | Lane | Department | Owner | Evidence | Open Tasks | Open Service Requests | Packet | First Task | Hard Stop |",
            "| ---: | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |",
        ]
    )
    for item in launch_queue:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(item["launch_rank"]),
                    f"`{item['lane_id']}`",
                    md_cell(item["department"], 120),
                    md_cell(item["owner"], 140),
                    str(item["evidence_count"]),
                    str(item["open_task_count"]),
                    str(item["open_service_request_count"]),
                    f"`{item['packet_path']}`",
                    md_cell(item["recommended_task"], 220),
                    md_cell(item["hard_stop"], 220),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Held Or Excluded Lanes", "", "| Lane | Department | Owner | Reason | Hard Stop |", "| --- | --- | --- | --- | --- |"])
    for item in held_lanes:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['lane_id']}`",
                    md_cell(item["department"], 120),
                    md_cell(item["owner"], 140),
                    md_cell(item["reason"], 260),
                    md_cell(item["hard_stop"], 240),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Initial Prompts", ""])
    for item in launch_queue:
        lines.extend(
            [
                f"### {item['launch_rank']}. {item['lane_id']}",
                "",
                "````text",
                item["initial_prompt"],
                "````",
                "",
            ]
        )

    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "md_path": str(output_md), "json_path": str(output_json), "launch_count": len(launch_queue), "held_count": len(held_lanes)}, indent=2))
