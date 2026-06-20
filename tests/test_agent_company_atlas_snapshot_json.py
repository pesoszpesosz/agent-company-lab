import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from visual_dashboard_recent_unlocks import RECENT_UI_UNLOCKS


def test_visual_dashboard_snapshot_is_valid_json():
    snapshot = json.loads((ROOT / "web/data/snapshot.json").read_text(encoding="utf-8"))

    assert snapshot["schemaVersion"] == "agent-company-visual-dashboard.snapshot.v1"
    assert snapshot["lanes"]
    assert snapshot["missionFeed"]["items"]
    assert snapshot["dispatchConsole"]["suggestions"]


def test_visual_dashboard_snapshot_keeps_recent_command_unlocks():
    snapshot = json.loads((ROOT / "web/data/snapshot.json").read_text(encoding="utf-8"))
    platform = next(lane for lane in snapshot["lanes"] if lane["id"] == "platform_engineering")
    newest_unlock = RECENT_UI_UNLOCKS[0]

    assert snapshot["totals"]["tasks"] >= 662
    assert snapshot["totals"]["traces"] >= 592
    assert snapshot["totals"]["artifacts"] >= 2478
    assert platform["counts"]["tasks"] >= 518
    assert platform["counts"]["completedTasks"] >= 516
    assert platform["counts"]["traces"] >= 458
    assert platform["counts"]["artifacts"] >= 1964
    assert snapshot["missionFeed"]["counts"]["task"] >= 120
    assert snapshot["missionFeed"]["counts"]["trace"] >= 119
    assert platform["recentTasks"][0]["id"] == newest_unlock["task_id"]
    assert platform["recentTraces"][0]["id"] == newest_unlock["trace_id"]
    assert platform["quest"]["checkpoints"][-1]["description"] == newest_unlock["trace_summary"]
