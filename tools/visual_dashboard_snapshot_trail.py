from __future__ import annotations

from collections import Counter
from typing import Any

from visual_dashboard_snapshot_core import artifact_preview, clean_label, compact_path

# Keep enough base company events after the recent-UI overlay prepends its
# command unlock records. New operational lanes add traces that should remain
# visible in mission-feed counts instead of being clipped by an old cap.
COMPANY_FEED_EVENT_LIMIT = 120

def trail_item(kind: str, title: str, status: str, time: str | None, summary: str | None, artifact: str | None = None) -> dict[str, Any]:
    item = {
        "kind": kind,
        "title": title,
        "status": status,
        "time": time,
        "summary": summary or "",
        "artifact": compact_path(artifact),
    }
    preview = artifact_preview(artifact)
    if preview:
        item["artifactPreview"] = preview
    return item


def build_trail(
    tasks: list[dict[str, Any]],
    requests: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    outcomes: list[dict[str, Any]],
    traces: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    trail: list[dict[str, Any]] = []
    for task in tasks:
        trail.append(
            trail_item(
                "task",
                task["title"],
                task["status"],
                task.get("updated_at") or task.get("created_at"),
                task.get("next_action") or task.get("evidence_required") or task["task_id"],
            )
        )
    for request in requests:
        trail.append(
            trail_item(
                "service_request",
                clean_label(request["request_type"]),
                request["status"],
                request.get("updated_at") or request.get("created_at"),
                request.get("requested_action") or request.get("risk_gate"),
                request.get("artifact_path"),
            )
        )
    for item in evidence:
        trail.append(
            trail_item(
                "evidence",
                item["title"],
                item["status"],
                item.get("updated_at") or item.get("created_at"),
                item.get("summary") or item.get("next_action") or item["evidence_id"],
                item.get("source_path") or item.get("source_url"),
            )
        )
    for outcome in outcomes:
        trail.append(
            trail_item(
                "outcome",
                clean_label(outcome["outcome_type"]),
                outcome["status"],
                outcome.get("created_at"),
                outcome.get("next_action") or outcome.get("evidence") or outcome["outcome_id"],
                outcome.get("evidence"),
            )
        )
    for trace in traces:
        trail.append(
            trail_item(
                "trace",
                clean_label(trace["event_type"]),
                "recorded",
                trace.get("event_time") or trace.get("created_at"),
                trace["summary"],
                trace.get("artifact_path"),
            )
        )
    trail.sort(key=lambda item: item.get("time") or "", reverse=True)
    return trail[:180]


def build_company_feed(lanes: list[dict[str, Any]]) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for lane in lanes:
        for index, item in enumerate(lane.get("trail", [])[:36]):
            items.append(
                {
                    "id": f"{lane['id']}-{item.get('kind', 'event')}-{index}",
                    "laneId": lane["id"],
                    "laneName": lane["name"],
                    "laneState": lane["state"],
                    "laneLevel": lane["level"],
                    "laneRealm": lane.get("visual", {}).get("realm") or lane["department"],
                    "kind": item.get("kind"),
                    "title": item.get("title"),
                    "status": item.get("status"),
                    "time": item.get("time"),
                    "summary": item.get("summary"),
                    "artifact": item.get("artifact"),
                }
            )
    items.sort(key=lambda item: item.get("time") or "", reverse=True)
    items = items[:COMPANY_FEED_EVENT_LIMIT]
    return {
        "schemaVersion": "agent-company-mission-feed.v1",
        "items": items,
        "counts": dict(Counter(item["kind"] for item in items)),
    }
