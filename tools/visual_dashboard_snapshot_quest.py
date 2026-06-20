from __future__ import annotations

from typing import Any

def build_quest(
    lane_id: str,
    tasks: list[dict[str, Any]],
    outcomes: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    promotion_candidate: dict[str, Any] | None,
    milestones: list[dict[str, Any]],
) -> dict[str, Any]:
    completed_tasks = sum(1 for task in tasks if task.get("status") in {"complete", "completed"})
    startup_complete = any(outcome.get("outcome_type") == "lane_startup" for outcome in outcomes) or any(
        "startup" in (item.get("title") or "").lower() for item in evidence
    )
    proof_complete = any("proof" in (outcome.get("outcome_type") or "").lower() for outcome in outcomes) or any(
        "proof" in (task.get("title") or "").lower() and task.get("status") in {"complete", "completed"} for task in tasks
    )
    blocker_count = len(gates)
    promotion_ready = bool(promotion_candidate and promotion_candidate.get("ready_for_manual_promotion"))

    checkpoints = [
        {
            "id": f"{lane_id}-startup",
            "title": "Startup Memo",
            "status": "complete" if startup_complete else "active",
            "description": "Lane has a recorded startup memo, owner, or launch context.",
        },
        {
            "id": f"{lane_id}-local-proof",
            "title": "Local Proof",
            "status": "complete" if proof_complete else "active" if completed_tasks else "locked",
            "description": "A local-only proof or useful task reduces uncertainty without side effects.",
        },
        {
            "id": f"{lane_id}-gate-review",
            "title": "Gate Review",
            "status": "gated" if blocker_count else "complete",
            "description": f"{blocker_count} blocking review gates remain visible." if blocker_count else "No active gate-map blocker is recorded.",
        },
        {
            "id": f"{lane_id}-promotion",
            "title": "Promotion",
            "status": "active" if promotion_ready else "locked",
            "description": "A ranked manual promotion candidate is available." if promotion_ready else "No ranked promotion candidate is ready.",
        },
        {
            "id": f"{lane_id}-next-unlock",
            "title": "Next Unlock",
            "status": "active",
            "description": (milestones[0]["summary"] if milestones else "Create the next traceable artifact, proof, or decision packet.")[:240],
        },
    ]
    return {
        "schemaVersion": "agent-company-lane-quest.v1",
        "title": "Lane Quest",
        "currentCheckpoint": next((item["id"] for item in checkpoints if item["status"] in {"active", "gated"}), checkpoints[-1]["id"]),
        "checkpoints": checkpoints,
    }
