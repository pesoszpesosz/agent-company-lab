from __future__ import annotations

from typing import Any

from .control_reports import suggested_manager_task
from .utils import decode_json_list, md_cell


def manager_packet_read_only_note(lane_id: str) -> str:
    if lane_id == "submitted_bounty_payouts":
        return "This lane is read-only in this workspace. Do not monitor, comment, submit, claim, or chase payouts from this thread."
    return ""


def build_manager_packet_lines(
    *,
    lane: dict[str, Any],
    specs: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    tasks: list[dict[str, Any]],
    requests: list[dict[str, Any]],
    outcomes: list[dict[str, Any]],
    service_catalog: list[dict[str, Any]],
    owner: str,
    recommendation: str,
    generated_utc: str,
    read_only_note: str = "",
) -> list[str]:
    lane_id = str(lane["lane_id"])
    agent_types = decode_json_list(lane["agent_types_json"])
    examples = decode_json_list(lane["examples_json"])
    promotion_gates = decode_json_list(lane["promotion_gates_json"])
    service_workers = decode_json_list(lane["service_workers_required_json"])
    side_effects = decode_json_list(lane["side_effects_json"])
    global_gates = decode_json_list(lane["global_gates_json"])

    manager_directive = (
        f"Read-only visibility lane for `{lane_id}`. Do not claim ownership, assign work, start monitoring, or create payout/public-action tasks from this workspace. Use this packet only to inspect imported evidence and preserve the external-owner boundary."
        if read_only_note
        else f"Own only the `{lane_id}` lane. Claim the lane before assigning work unless an owner is already listed. Create or acquire exactly one active task at a time and record artifacts/outcomes in the control plane."
    )
    suggested_prompt = (
        f"You are reviewing the read-only `{lane_id}` packet in `E:\\agent-company-lab`. Do not claim the lane or start payout/public-action work. Inspect local evidence only, preserve the external-owner boundary, and escalate only if the user explicitly reassigns ownership."
        if read_only_note
        else f"You are the department manager for `{lane_id}` in `E:\\agent-company-lab`. Read this manager packet, run the startup commands, claim the lane only if it is unowned, create or acquire one scoped task, produce local artifacts, and record outcomes. Stop at every service-request gate."
    )

    lines = [
        f"# Manager Packet - {lane_id}",
        "",
        f"Generated UTC: {generated_utc}",
        f"Department: {lane['department']}",
        f"Lane status: {lane['status']}",
        f"Current owner: `{owner}`",
        "",
        "## Manager Directive",
        "",
        manager_directive,
    ]
    if read_only_note:
        lines.extend(["", f"**Read-only boundary:** {read_only_note}"])
    lines.extend(
        [
            "",
            "## Recommended Next Task",
            "",
            suggested_manager_task(lane_id),
            "",
            "## CEO Recommendation",
            "",
            recommendation,
            "",
            "## Allowed Worker Types",
            "",
        ]
    )
    lines.extend([f"- {item}" for item in agent_types] or ["- No worker types configured."])
    lines.extend(["", "## Example Work", ""])
    lines.extend([f"- {item}" for item in examples] or ["- No examples configured."])
    lines.extend(["", "## Promotion Gates", ""])
    lines.extend([f"- {item}" for item in promotion_gates] or ["- No promotion gates configured."])
    lines.extend(["", "## Required Service Workers", ""])
    lines.extend([f"- {item}" for item in service_workers] or ["- None configured."])
    lines.extend(
        [
            "",
            "## Service Bureau Catalog",
            "",
            "Use these request types when this lane needs registration, browser, wallet, public action, outreach, trading, model/API, data/API, security-report, payment/legal, or credential support. The catalog defines intake and hard stops; it does not approve the action.",
            "",
            "| Status | Type | Service | Owner Role | Purpose |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for service in service_catalog:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(service["default_status"], 80),
                    md_cell(service["request_type"], 120),
                    f"`{service['service_id']}`",
                    f"`{service['owner_role_id']}`",
                    md_cell(service["purpose"], 260),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Forbidden Direct Side Effects", ""])
    if side_effects:
        lines.append("These require a scoped service request and approval before any execution:")
        lines.extend([f"- {item}" for item in side_effects])
    else:
        lines.append("No lane-specific side effects configured. Global gates still apply.")
    lines.extend(["", "## Global Gates", ""])
    lines.extend([f"- {item}" for item in global_gates] or ["- No global gates configured."])

    lines.extend(["", "## Source Specs", "", "| Spec | Type | Cadence | Gate | Refresh | Outputs |", "| --- | --- | --- | --- | --- | --- |"])
    for spec in specs:
        outputs = "; ".join(str(item) for item in decode_json_list(spec["outputs_json"]))
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{spec['spec_id']}` - {md_cell(spec['name'], 120)}",
                    md_cell(spec["source_type"], 80),
                    md_cell(spec["cadence"], 100),
                    md_cell(spec["risk_gate"], 180),
                    md_cell(spec["refresh_command"], 220),
                    md_cell(outputs, 180),
                ]
            )
            + " |"
        )
    if not specs:
        lines.append("| none |  |  |  |  |  |")

    lines.extend(["", "## Current Evidence", "", "| Status | Evidence | Source | Next Action | Ownership Note |", "| --- | --- | --- | --- | --- |"])
    for item in evidence:
        source = item["source_url"] or item["source_path"] or ""
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(item["status"], 100),
                    f"`{item['evidence_id']}` - {md_cell(item['title'], 160)}",
                    md_cell(source, 180),
                    md_cell(item["next_action"], 220),
                    md_cell(item["ownership_note"], 220),
                ]
            )
            + " |"
        )
    if not evidence:
        lines.append("| none |  |  |  |  |")

    lines.extend(["", "## Tasks", "", "| Priority | Status | Task | Owner | Lease | Evidence Required | Next Action |", "| ---: | --- | --- | --- | --- | --- | --- |"])
    for task in tasks:
        lease = ""
        if task["lease_owner_agent_id"] or task["lease_expires_at"]:
            lease = f"{task['lease_owner_agent_id'] or ''} until {task['lease_expires_at'] or ''}"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(task["priority"]),
                    md_cell(task["status"], 80),
                    f"`{task['task_id']}` - {md_cell(task['title'], 160)}",
                    md_cell(task["owner_agent_id"], 120),
                    md_cell(lease, 120),
                    md_cell(task["evidence_required"], 180),
                    md_cell(task["next_action"], 220),
                ]
            )
            + " |"
        )
    if not tasks:
        lines.append("|  | none |  |  |  |  |  |")

    lines.extend(["", "## Service Requests", "", "| Status | Service | Type | Request | Assigned | Gate | Requested Action | Artifact | Decision |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"])
    for req in requests:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(req["status"], 80),
                    md_cell(req["service_id"], 120),
                    md_cell(req["request_type"], 100),
                    f"`{req['request_id']}`",
                    md_cell(req["assigned_agent_id"], 120),
                    md_cell(req["risk_gate"], 180),
                    md_cell(req["requested_action"], 240),
                    md_cell(req["artifact_path"], 160),
                    md_cell(req["decision_note"], 180),
                ]
            )
            + " |"
        )
    if not requests:
        lines.append("| none |  |  |  |  |  |  |  |  |")

    lines.extend(["", "## Recent Outcomes", "", "| Status | Type | Outcome | Realized USD | Evidence | Next Action |", "| --- | --- | --- | ---: | --- | --- |"])
    for outcome in outcomes:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(outcome["status"], 80),
                    md_cell(outcome["outcome_type"], 120),
                    f"`{outcome['outcome_id']}`",
                    str(outcome["realized_usd"]),
                    md_cell(outcome["evidence"], 180),
                    md_cell(outcome["next_action"], 220),
                ]
            )
            + " |"
        )
    if not outcomes:
        lines.append("| none |  |  | 0 |  |  |")

    lines.extend(
        [
            "",
            "## Startup Commands",
            "",
            "```powershell",
            "python E:\\agent-company-lab\\tools\\agent_company.py status",
            f"python E:\\agent-company-lab\\tools\\agent_company.py list-source-specs --lane-id {lane_id}",
            f"python E:\\agent-company-lab\\tools\\agent_company.py list-evidence --lane-id {lane_id} --limit 25",
            "```",
            "",
            "## Suggested Manager Prompt",
            "",
            "```text",
            suggested_prompt,
            "```",
            "",
        ]
    )
    return lines


__all__ = ["build_manager_packet_lines", "manager_packet_read_only_note"]
