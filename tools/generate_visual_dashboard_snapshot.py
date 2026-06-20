#!/usr/bin/env python3
"""Build the standalone web dashboard data snapshot from the control plane."""

from __future__ import annotations

import argparse
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from visual_dashboard_recent_unlocks import RECENT_UI_UNLOCKS
from visual_dashboard_snapshot_core import (
    DEFAULT_AGENT_VISUALS,
    DEFAULT_DB,
    DEFAULT_OUT,
    DEFAULT_VISUALS,
    ROOT,
    clean_label,
    compact_path,
    compute_level,
    compute_progress,
    default_visual,
    load_json,
    now_utc,
    rows,
    table_count,
)
from visual_dashboard_snapshot_dispatch import build_dispatch_console
from visual_dashboard_snapshot_quest import build_quest
from visual_dashboard_snapshot_trail import build_company_feed, build_trail
from visual_dashboard_snapshot_unlocks import apply_recent_ui_unlocks

def build_snapshot(db_path: Path) -> dict[str, Any]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    lanes_raw = rows(conn, "select * from lanes order by lane_id")
    departments = rows(conn, "select * from departments order by department_id")
    agents = rows(conn, "select * from agents order by agent_id")
    agent_visuals_raw = load_json(DEFAULT_AGENT_VISUALS.read_text(encoding="utf-8"), {}) if DEFAULT_AGENT_VISUALS.exists() else {}
    agent_visuals_by_id = agent_visuals_raw.get("agents", {})
    for agent in agents:
        agent["visual"] = agent_visuals_by_id.get(agent["agent_id"], {})

    tasks_by_lane: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for task in rows(conn, "select * from tasks order by priority desc, updated_at desc"):
        tasks_by_lane[task["lane_id"]].append(task)

    requests_by_lane: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for request in rows(conn, "select * from service_requests order by updated_at desc"):
        if request.get("lane_id"):
            requests_by_lane[request["lane_id"]].append(request)

    evidence_by_lane: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for evidence in rows(conn, "select * from lane_evidence order by updated_at desc"):
        evidence_by_lane[evidence["lane_id"]].append(evidence)

    outcomes_by_lane: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for outcome in rows(conn, "select * from outcomes order by created_at desc"):
        outcomes_by_lane[outcome["lane_id"]].append(outcome)

    traces_by_lane: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for trace in rows(conn, "select * from trace_events order by event_time desc"):
        if trace.get("lane_id"):
            trace["metadata"] = load_json(trace.get("metadata_json"), {})
            traces_by_lane[trace["lane_id"]].append(trace)

    artifacts_by_lane: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for artifact in rows(conn, "select * from artifacts order by created_at desc"):
        if artifact.get("lane_id"):
            artifacts_by_lane[artifact["lane_id"]].append(artifact)

    gate_map_path = ROOT / "reports" / "service-worker-gate-map-latest.json"
    gate_map = load_json(gate_map_path.read_text(encoding="utf-8"), {}) if gate_map_path.exists() else {}
    gates_by_lane: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for gate in gate_map.get("gate_map", []):
        if gate.get("lane_id"):
            gates_by_lane[gate["lane_id"]].append(gate)

    promotion_path = ROOT / "reports" / "manager-proof-task-promotion-queue-latest.json"
    promotion = load_json(promotion_path.read_text(encoding="utf-8"), {}) if promotion_path.exists() else {}
    promo_by_lane = {entry.get("lane_id"): entry for entry in promotion.get("queue_entries", [])}
    visuals_raw = load_json(DEFAULT_VISUALS.read_text(encoding="utf-8"), {}) if DEFAULT_VISUALS.exists() else {}
    visuals_by_lane = visuals_raw.get("lanes", {})

    lanes: list[dict[str, Any]] = []
    for index, lane in enumerate(lanes_raw):
        lane_id = lane["lane_id"]
        visual = default_visual(lane_id, index)
        visual.update(visuals_by_lane.get(lane_id, {}))
        tasks = tasks_by_lane.get(lane_id, [])
        requests = requests_by_lane.get(lane_id, [])
        evidence = evidence_by_lane.get(lane_id, [])
        outcomes = outcomes_by_lane.get(lane_id, [])
        traces = traces_by_lane.get(lane_id, [])
        artifacts = artifacts_by_lane.get(lane_id, [])
        gates = gates_by_lane.get(lane_id, [])

        task_counts = Counter(task["status"] for task in tasks)
        request_counts = Counter(request["status"] for request in requests)
        blocker_count = sum(1 for gate in gates if "approval_required" in str(gate.get("current_blocking_gate", "")))
        completed_count = task_counts.get("complete", 0) + task_counts.get("completed", 0)
        active_count = sum(task_counts.get(status, 0) for status in ("new", "active", "in_progress", "blocked"))
        realized_usd = sum(float(outcome.get("realized_usd") or 0) for outcome in outcomes)
        score = (
            completed_count * 40
            + len(evidence) * 35
            + len(outcomes) * 50
            + len(traces) * 25
            + len(artifacts) * 8
            + active_count * 18
            - blocker_count * 20
        )
        level = compute_level(score)

        milestones: list[dict[str, Any]] = []
        for outcome in outcomes[:8]:
            milestones.append(
                {
                    "kind": "outcome",
                    "title": clean_label(outcome["outcome_type"]),
                    "status": outcome["status"],
                    "time": outcome["created_at"],
                    "summary": outcome.get("next_action") or outcome.get("evidence") or outcome["outcome_id"],
                    "artifact": compact_path(outcome.get("evidence")),
                }
            )
        for item in evidence[:8]:
            milestones.append(
                {
                    "kind": "evidence",
                    "title": item["title"],
                    "status": item["status"],
                    "time": item["updated_at"],
                    "summary": item.get("summary") or item.get("next_action") or item["evidence_id"],
                    "artifact": compact_path(item.get("source_path") or item.get("source_url")),
                }
            )
        for trace in traces[:8]:
            milestones.append(
                {
                    "kind": "trace",
                    "title": clean_label(trace["event_type"]),
                    "status": "recorded",
                    "time": trace["event_time"],
                    "summary": trace["summary"],
                    "artifact": compact_path(trace.get("artifact_path")),
                }
            )
        milestones.sort(key=lambda item: item.get("time") or "", reverse=True)
        trail = build_trail(tasks, requests, evidence, outcomes, traces)
        quest = build_quest(lane_id, tasks, outcomes, evidence, gates, promo_by_lane.get(lane_id), milestones)

        request_types = Counter(request["request_type"] for request in requests)
        lane_state = "gated" if blocker_count else "advancing" if active_count else "unlocked"
        if not evidence and not outcomes:
            lane_state = "scouting"

        lanes.append(
            {
                "id": lane_id,
                "name": clean_label(lane_id),
                "department": lane["department"],
                "status": lane["status"],
                "state": lane_state,
                "ownerAgentId": lane.get("owner_agent_id"),
                "ownerThreadId": lane.get("owner_thread_id"),
                "agentTypes": load_json(lane.get("agent_types_json"), []),
                "examples": load_json(lane.get("examples_json"), []),
                "promotionGates": load_json(lane.get("promotion_gates_json"), []),
                "serviceWorkersRequired": load_json(lane.get("service_workers_required_json"), []),
                "sideEffects": load_json(lane.get("side_effects_json"), []),
                "globalGates": load_json(lane.get("global_gates_json"), []),
                "notes": lane.get("notes"),
                "visual": visual,
                "map": {
                    "x": 12 + (index % 4) * 25 + (6 if index % 2 else 0),
                    "y": 18 + (index // 4) * 25 + ((index % 3) * 2),
                },
                "score": score,
                "level": level,
                "progress": compute_progress(score, level),
                "realizedUsd": realized_usd,
                "counts": {
                    "tasks": len(tasks),
                    "completedTasks": completed_count,
                    "activeTasks": active_count,
                    "serviceRequests": len(requests),
                    "pendingRequests": request_counts.get("needs_review", 0),
                    "evidence": len(evidence),
                    "outcomes": len(outcomes),
                    "traces": len(traces),
                    "artifacts": len(artifacts),
                    "blockers": blocker_count,
                },
                "taskCounts": dict(task_counts),
                "requestCounts": dict(request_counts),
                "requestTypes": dict(request_types),
                "recentTasks": [
                    {
                        "id": task["task_id"],
                        "title": task["title"],
                        "status": task["status"],
                        "priority": task["priority"],
                        "nextAction": task.get("next_action"),
                        "ownerAgentId": task.get("owner_agent_id"),
                    }
                    for task in tasks[:8]
                ],
                "serviceRequests": [
                    {
                        "id": request["request_id"],
                        "type": request["request_type"],
                        "status": request["status"],
                        "riskGate": request["risk_gate"],
                        "requestedAction": request["requested_action"],
                        "artifact": compact_path(request.get("artifact_path")),
                    }
                    for request in requests[:10]
                ],
                "gateMap": [
                    {
                        "id": gate.get("source_service_request_id"),
                        "gate": gate.get("current_blocking_gate"),
                        "route": gate.get("approval_review_route"),
                        "workerType": gate.get("worker_type"),
                        "nextAction": gate.get("next_action"),
                    }
                    for gate in gates[:8]
                ],
                "recentEvidence": [
                    {
                        "id": item["evidence_id"],
                        "title": item["title"],
                        "status": item["status"],
                        "nextAction": item.get("next_action"),
                        "artifact": compact_path(item.get("source_path") or item.get("source_url")),
                    }
                    for item in evidence[:8]
                ],
                "recentOutcomes": [
                    {
                        "id": outcome["outcome_id"],
                        "type": outcome["outcome_type"],
                        "status": outcome["status"],
                        "realizedUsd": float(outcome.get("realized_usd") or 0),
                        "nextAction": outcome.get("next_action"),
                        "artifact": compact_path(outcome.get("evidence")),
                    }
                    for outcome in outcomes[:8]
                ],
                "recentTraces": [
                    {
                        "id": trace["event_id"],
                        "type": trace["event_type"],
                        "time": trace["event_time"],
                        "summary": trace["summary"],
                        "artifact": compact_path(trace.get("artifact_path")),
                    }
                    for trace in traces[:10]
                ],
                "milestones": milestones[:18],
                "trail": trail,
                "quest": quest,
                "promotionCandidate": promo_by_lane.get(lane_id),
            }
        )

    lanes_by_owner = {lane["ownerAgentId"]: lane for lane in lanes if lane.get("ownerAgentId")}
    for agent in agents:
        lane = lanes_by_owner.get(agent["agent_id"])
        agent["lane"] = (
            {
                "id": lane["id"],
                "name": lane["name"],
                "state": lane["state"],
                "level": lane["level"],
                "score": lane["score"],
                "nextAction": lane["recentOutcomes"][0]["nextAction"] if lane["recentOutcomes"] else None,
            }
            if lane
            else None
        )

    totals = {
        "lanes": len(lanes),
        "departments": len(departments),
        "agents": len(agents),
        "tasks": table_count(conn, "tasks"),
        "serviceRequests": table_count(conn, "service_requests"),
        "evidence": table_count(conn, "lane_evidence"),
        "outcomes": table_count(conn, "outcomes"),
        "traces": table_count(conn, "trace_events"),
        "artifacts": table_count(conn, "artifacts"),
        "pendingRequests": sum(lane["counts"]["pendingRequests"] for lane in lanes),
        "blockers": sum(lane["counts"]["blockers"] for lane in lanes),
        "realizedUsd": sum(lane["realizedUsd"] for lane in lanes),
    }

    top_lanes = sorted(lanes, key=lambda lane: lane["score"], reverse=True)
    mission_feed = build_company_feed(lanes)
    dispatch_console = build_dispatch_console(lanes)
    achievements = [
        {
            "id": "control-plane-online",
            "title": "Control Plane Online",
            "description": f"{totals['lanes']} lanes are visible from one command surface.",
            "unlocked": totals["lanes"] > 0 and totals["tasks"] > 0,
        },
        {
            "id": "evidence-chain",
            "title": "Evidence Chain",
            "description": f"{totals['evidence']} evidence records and {totals['artifacts']} artifacts are traceable.",
            "unlocked": totals["evidence"] >= 10,
        },
        {
            "id": "gate-discipline",
            "title": "Gate Discipline",
            "description": f"{totals['pendingRequests']} requests are parked behind explicit review instead of being run blindly.",
            "unlocked": totals["pendingRequests"] > 0,
        },
        {
            "id": "promotion-queue",
            "title": "Promotion Queue",
            "description": f"{promotion.get('ready_queue_count', 0)} manual promotion candidates are ranked.",
            "unlocked": promotion.get("ready_queue_count", 0) > 0,
        },
        {
            "id": "trace-memory",
            "title": "Trace Memory",
            "description": f"{totals['traces']} trace events keep the company timeline replayable.",
            "unlocked": totals["traces"] >= 25,
        },
    ]

    snapshot = {
        "schemaVersion": "agent-company-visual-dashboard.snapshot.v1",
        "generatedUtc": now_utc(),
        "database": str(db_path),
        "sources": {
            "sqlite": compact_path(str(db_path)),
            "gateMap": compact_path(str(gate_map_path)) if gate_map_path.exists() else None,
            "promotionQueue": compact_path(str(promotion_path)) if promotion_path.exists() else None,
            "laneVisuals": compact_path(str(DEFAULT_VISUALS)) if DEFAULT_VISUALS.exists() else None,
            "agentVisuals": compact_path(str(DEFAULT_AGENT_VISUALS)) if DEFAULT_AGENT_VISUALS.exists() else None,
        },
        "totals": totals,
        "achievements": achievements,
        "departments": departments,
        "agents": agents,
        "lanes": lanes,
        "missionFeed": mission_feed,
        "dispatchConsole": dispatch_console,
        "leaderboard": [
            {
                "id": lane["id"],
                "name": lane["name"],
                "department": lane["department"],
                "score": lane["score"],
                "level": lane["level"],
                "state": lane["state"],
                "nextAction": (lane["recentOutcomes"][0]["nextAction"] if lane["recentOutcomes"] else None),
            }
            for lane in top_lanes[:8]
        ],
        "researchInfluences": [
            {
                "name": "Command-center hierarchy",
                "takeaway": "A dashboard should surface the right data at the right hierarchy with minimal visual noise.",
                "url": "https://muz.li/blog/best-dashboard-design-examples-inspirations-for-2026/",
            },
            {
                "name": "Agent UX override loop",
                "takeaway": "Agent interfaces should show what the agent is doing, why, and how the operator can override or recover.",
                "url": "https://fuselabcreative.com/ui-design-for-ai-agents/",
            },
            {
                "name": "Milestone communication",
                "takeaway": "Milestone charts give stakeholders a simplified view of major transition points without losing progress context.",
                "url": "https://www.atlassian.com/work-management/project-management/project-planning/milestone-chart",
            },
        ],
    }
    apply_recent_ui_unlocks(snapshot)
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    snapshot = build_snapshot(args.db)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(args.out), "lanes": len(snapshot["lanes"]), "generatedUtc": snapshot["generatedUtc"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
