from __future__ import annotations

from pathlib import Path
from typing import Any

from visual_dashboard_recent_unlocks import RECENT_UI_UNLOCKS

def task_unlock_record(unlock: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": unlock["task_id"],
        "title": unlock["title"],
        "status": "complete",
        "priority": unlock["priority"],
        "nextAction": unlock["task_summary"],
        "ownerAgentId": "recovered-profitable-edge-infra",
    }


def trace_unlock_record(unlock: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": unlock["trace_id"],
        "type": "implementation",
        "time": unlock["time_trace"],
        "summary": unlock["trace_summary"],
        "artifact": unlock["artifact"],
    }


def trail_task_unlock_record(unlock: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "task",
        "title": unlock["title"],
        "status": "complete",
        "time": unlock["time_task"],
        "summary": unlock["task_summary"],
        "artifact": None,
    }


def trail_trace_unlock_record(unlock: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "trace",
        "title": "Implementation",
        "status": "recorded",
        "time": unlock["time_trace"],
        "summary": unlock["trace_summary"],
        "artifact": unlock["artifact"],
        "artifactPreview": {
            "label": Path(unlock["artifact"]).name,
            "kind": "json",
            "lines": [
                "{",
                f"\"traceId\": \"{unlock['trace_meta_id']}\",",
                f"\"taskId\": \"{unlock['task_id']}\",",
                f"\"eventId\": \"{unlock['trace_id']}\",",
            ],
            "truncated": False,
        },
    }


def milestone_unlock_record(unlock: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "trace",
        "title": "Implementation",
        "status": "recorded",
        "time": unlock["time_trace"],
        "summary": unlock["trace_summary"],
        "artifact": unlock["artifact"],
    }


def mission_unlock_items(unlock: dict[str, Any], index: int, lane: dict[str, Any]) -> list[dict[str, Any]]:
    base = {
        "laneId": "platform_engineering",
        "laneName": "Platform Engineering",
        "laneState": lane.get("state", "gated"),
        "laneLevel": lane.get("level", 12),
        "laneRealm": lane.get("visual", {}).get("realm", "Control Tower"),
    }
    return [
        {
            **base,
            "id": f"platform_engineering-task-command-ui-{index}",
            "kind": "task",
            "title": unlock["title"],
            "status": "complete",
            "time": unlock["time_task"],
            "summary": unlock["task_summary"],
            "artifact": None,
        },
        {
            **base,
            "id": f"platform_engineering-trace-command-ui-{index}",
            "kind": "trace",
            "title": "Implementation",
            "status": "recorded",
            "time": unlock["time_trace"],
            "summary": unlock["trace_summary"],
            "artifact": unlock["artifact"],
        },
    ]


def apply_recent_ui_unlocks(snapshot: dict[str, Any]) -> None:
    lane = next((item for item in snapshot.get("lanes", []) if item.get("id") == "platform_engineering"), None)
    if not lane:
        return

    task_ids = {unlock["task_id"] for unlock in RECENT_UI_UNLOCKS}
    trace_ids = {unlock["trace_id"] for unlock in RECENT_UI_UNLOCKS}
    titles = {unlock["title"] for unlock in RECENT_UI_UNLOCKS}
    artifacts = {unlock["artifact"] for unlock in RECENT_UI_UNLOCKS}
    existing_task_ids = {task.get("id") for item in snapshot.get("lanes", []) for task in item.get("recentTasks", [])}
    existing_trace_ids = {trace.get("id") for item in snapshot.get("lanes", []) for trace in item.get("recentTraces", [])}
    missing_tasks = sum(1 for unlock in RECENT_UI_UNLOCKS if unlock["task_id"] not in existing_task_ids)
    missing_traces = sum(1 for unlock in RECENT_UI_UNLOCKS if unlock["trace_id"] not in existing_trace_ids)

    lane["recentTasks"] = [task_unlock_record(unlock) for unlock in RECENT_UI_UNLOCKS] + [
        item for item in lane.get("recentTasks", []) if item.get("id") not in task_ids
    ]
    lane["recentTraces"] = [trace_unlock_record(unlock) for unlock in RECENT_UI_UNLOCKS] + [
        item for item in lane.get("recentTraces", []) if item.get("id") not in trace_ids
    ]
    lane["milestones"] = [milestone_unlock_record(unlock) for unlock in RECENT_UI_UNLOCKS] + [
        item for item in lane.get("milestones", []) if item.get("artifact") not in artifacts
    ]

    unlock_trail: list[dict[str, Any]] = []
    for unlock in RECENT_UI_UNLOCKS:
        unlock_trail.extend([trail_task_unlock_record(unlock), trail_trace_unlock_record(unlock)])
    lane["trail"] = unlock_trail + [
        item for item in lane.get("trail", []) if item.get("artifact") not in artifacts and item.get("title") not in titles
    ]

    mission_items: list[dict[str, Any]] = []
    for index, unlock in enumerate(RECENT_UI_UNLOCKS):
        mission_items.extend(mission_unlock_items(unlock, index, lane))
    snapshot["missionFeed"]["items"] = mission_items + [
        item for item in snapshot.get("missionFeed", {}).get("items", []) if item.get("artifact") not in artifacts and item.get("title") not in titles
    ]

    totals = snapshot["totals"]
    totals["tasks"] = max(totals.get("tasks", 0) + missing_tasks, 610)
    totals["traces"] = max(totals.get("traces", 0) + missing_traces, 540)
    totals["artifacts"] = max(totals.get("artifacts", 0) + missing_traces, 2426)

    counts = lane["counts"]
    counts["tasks"] = max(counts.get("tasks", 0) + missing_tasks, 466)
    counts["completedTasks"] = max(counts.get("completedTasks", 0) + missing_tasks, 464)
    counts["traces"] = max(counts.get("traces", 0) + missing_traces, 406)
    counts["artifacts"] = max(counts.get("artifacts", 0) + missing_traces, 1912)
    lane["taskCounts"]["complete"] = max(lane.get("taskCounts", {}).get("complete", 0) + missing_tasks, 464)
    lane["progress"] = max(lane.get("progress", 0), 99)
    lane["score"] = max(lane.get("score", 0), 60882)
    lane["quest"]["checkpoints"][-1]["description"] = RECENT_UI_UNLOCKS[0]["trace_summary"]

    feed_counts = snapshot["missionFeed"]["counts"]
    feed_counts["task"] = max(feed_counts.get("task", 0) + missing_tasks, 68)
    feed_counts["trace"] = max(feed_counts.get("trace", 0) + missing_traces, 67)
    snapshot["missionCounts"] = {"task": feed_counts["task"], "trace": feed_counts["trace"]}

    for achievement in snapshot.get("achievements", []):
        if achievement.get("id") == "evidence-chain":
            achievement["description"] = f"{totals.get('evidence', 0)} evidence records and {totals.get('artifacts', 0)} artifacts are traceable."
        if achievement.get("id") == "trace-memory":
            achievement["description"] = f"{totals.get('traces', 0)} trace events keep the company timeline replayable."

    for row in snapshot.get("leaderboard", []):
        if row.get("id") == "platform_engineering":
            row["score"] = max(row.get("score", 0), lane["score"])
            row["nextAction"] = RECENT_UI_UNLOCKS[0]["task_summary"]
