from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_recent_ui_unlock_catalog_lives_behind_dedicated_module():
    import generate_visual_dashboard_snapshot as snapshot_generator
    import visual_dashboard_recent_unlocks

    assert snapshot_generator.RECENT_UI_UNLOCKS is visual_dashboard_recent_unlocks.RECENT_UI_UNLOCKS
    assert visual_dashboard_recent_unlocks.RECENT_UI_UNLOCKS
    first_unlock = visual_dashboard_recent_unlocks.RECENT_UI_UNLOCKS[0]
    assert first_unlock["task_id"].startswith("task-agent-company-atlas-")
    assert first_unlock["trace_id"].startswith("trace-atlas_")
    assert first_unlock["priority"] >= visual_dashboard_recent_unlocks.RECENT_UI_UNLOCKS[-1]["priority"]
    assert {"task_id", "trace_id", "trace_meta_id", "title", "time_task", "time_trace", "priority", "task_summary", "trace_summary", "artifact"} <= set(first_unlock)


def test_dashboard_snapshot_generator_reuses_focused_helper_modules():
    import generate_visual_dashboard_snapshot as snapshot_generator
    import visual_dashboard_snapshot_core
    import visual_dashboard_snapshot_dispatch
    import visual_dashboard_snapshot_quest
    import visual_dashboard_snapshot_trail
    import visual_dashboard_snapshot_unlocks

    assert snapshot_generator.DEFAULT_DB is visual_dashboard_snapshot_core.DEFAULT_DB
    assert snapshot_generator.DEFAULT_OUT is visual_dashboard_snapshot_core.DEFAULT_OUT
    assert snapshot_generator.rows is visual_dashboard_snapshot_core.rows
    assert snapshot_generator.clean_label is visual_dashboard_snapshot_core.clean_label
    assert snapshot_generator.compact_path is visual_dashboard_snapshot_core.compact_path
    assert snapshot_generator.table_count is visual_dashboard_snapshot_core.table_count
    assert snapshot_generator.default_visual is visual_dashboard_snapshot_core.default_visual

    assert snapshot_generator.build_trail is visual_dashboard_snapshot_trail.build_trail
    assert snapshot_generator.build_company_feed is visual_dashboard_snapshot_trail.build_company_feed
    assert snapshot_generator.build_dispatch_console is visual_dashboard_snapshot_dispatch.build_dispatch_console
    assert snapshot_generator.build_quest is visual_dashboard_snapshot_quest.build_quest
    assert snapshot_generator.apply_recent_ui_unlocks is visual_dashboard_snapshot_unlocks.apply_recent_ui_unlocks

def test_recent_ui_unlocks_split_current_day_catalog_from_public_facade():
    import visual_dashboard_recent_unlocks
    import visual_dashboard_recent_unlocks_20260619

    dated_unlocks = visual_dashboard_recent_unlocks_20260619.RECENT_UI_UNLOCKS_20260619

    assert len(dated_unlocks) == 79
    assert all(unlock["time_task"].startswith("2026-06-19T") for unlock in dated_unlocks)
    assert visual_dashboard_recent_unlocks.RECENT_UI_UNLOCKS[: len(dated_unlocks)] is not dated_unlocks
    assert visual_dashboard_recent_unlocks.RECENT_UI_UNLOCKS[: len(dated_unlocks)] == dated_unlocks
    assert visual_dashboard_recent_unlocks.RECENT_UI_UNLOCKS[len(dated_unlocks)]["time_task"].startswith("2026-06-18T")