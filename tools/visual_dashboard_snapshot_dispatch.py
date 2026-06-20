from __future__ import annotations

from collections import Counter
from typing import Any

def dispatch_command(lane: dict[str, Any]) -> str:
    promotion = lane.get("promotionCandidate") or {}
    if promotion.get("command_preview"):
        return promotion["command_preview"]
    owner = lane.get("ownerAgentId") or "lane-manager"
    recent_tasks = lane.get("recentTasks") or []
    recent_outcomes = lane.get("recentOutcomes") or []
    next_action = (
        (recent_tasks[0].get("nextAction") if recent_tasks else None)
        or (recent_outcomes[0].get("nextAction") if recent_outcomes else None)
        or "Create one local proof artifact, record it, and stop at gates."
    )
    return (
        f"To {owner}: Review {lane['id']}, summarize the newest trail records, propose exactly one "
        "local-only next action, and do not run browser, account, wallet, public, payment, security, "
        f"or real-money work. Context: {next_action}"
    )


def dispatch_suggestion(lane: dict[str, Any]) -> dict[str, Any]:
    promotion = lane.get("promotionCandidate") or {}
    counts = lane.get("counts") or {}
    gate = (lane.get("gateMap") or lane.get("serviceRequests") or [None])[0]
    recent_task = (lane.get("recentTasks") or [None])[0]
    recent_outcome = (lane.get("recentOutcomes") or [None])[0]

    if counts.get("blockers"):
        kind = "gate_review"
        urgency = 94
        title = "Review gate before any live action"
        reason = (gate or {}).get("nextAction") or (gate or {}).get("riskGate") or "Lane has blockers or review gates."
    elif promotion.get("ready_for_manual_promotion"):
        kind = "promotion"
        urgency = 88
        title = "Review promotion candidate"
        reason = promotion.get("score_rationale") or promotion.get("next_decision") or "Manual promotion candidate is ranked."
    elif counts.get("activeTasks"):
        kind = "progress_check"
        urgency = 70 + min(14, int(counts.get("activeTasks") or 0))
        title = "Ask for next local proof"
        reason = (recent_task or {}).get("nextAction") or "Active tasks need a bounded local next action."
    elif recent_outcome and recent_outcome.get("nextAction"):
        kind = "follow_up"
        urgency = 62
        title = "Follow up on outcome"
        reason = recent_outcome.get("nextAction")
    else:
        kind = "scout_ping"
        urgency = 48
        title = "Request scouting pulse"
        reason = "Ask the lane manager for one evidence-backed next step."

    return {
        "id": f"dispatch-{lane['id']}-{kind}",
        "laneId": lane["id"],
        "laneName": lane["name"],
        "laneState": lane["state"],
        "laneLevel": lane["level"],
        "laneRealm": lane.get("visual", {}).get("realm") or lane["department"],
        "kind": kind,
        "urgency": urgency,
        "title": title,
        "reason": reason,
        "targetAgentId": lane.get("ownerAgentId"),
        "targetThreadId": lane.get("ownerThreadId"),
        "command": dispatch_command(lane),
    }


def build_dispatch_console(lanes: list[dict[str, Any]]) -> dict[str, Any]:
    suggestions = [dispatch_suggestion(lane) for lane in lanes]
    suggestions.sort(key=lambda item: (item["urgency"], item["laneLevel"]), reverse=True)
    return {
        "schemaVersion": "agent-company-dispatch-console.v1",
        "suggestions": suggestions,
        "counts": dict(Counter(item["kind"] for item in suggestions)),
    }
