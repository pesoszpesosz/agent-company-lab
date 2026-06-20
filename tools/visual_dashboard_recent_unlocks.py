#!/usr/bin/env python3
"""Recent UI unlock records overlaid onto the dashboard snapshot."""

from __future__ import annotations

from visual_dashboard_recent_unlocks_20260619 import RECENT_UI_UNLOCKS_20260619

RECENT_UI_UNLOCKS_20260618 = [{'task_id': 'task-agent-company-atlas-command-archive-shelf-v1-20260619',
  'trace_id': 'trace-atlas_command_archive_shelf_added-20260619',
  'trace_meta_id': 'trace-agent-company-atlas-command-archive-shelf-v1-20260619',
  'title': 'Command Archive Shelf',
  'time_task': '2026-06-18T22:44:40Z',
  'time_trace': '2026-06-18T22:44:32Z',
  'priority': 113,
  'task_summary': 'Continue converting long command boards into bounded shelves and playable status surfaces '
                  'instead of page-length stacks.',
  'trace_summary': 'Bounded the lower Command boards into an archive shelf with internal scroll, stable glow '
                   'states, and a much shorter overall command page.',
  'artifact': 'reports/agent-company-atlas-command-archive-shelf-trace-metadata-20260619.json'},
 {'task_id': 'task-agent-company-atlas-command-top-hud-compact-v1-20260619',
  'trace_id': 'trace-atlas_command_top_hud_compact_added-20260619',
  'trace_meta_id': 'trace-agent-company-atlas-command-top-hud-compact-v1-20260619',
  'title': 'Command Top HUD Compact',
  'time_task': '2026-06-18T22:36:24Z',
  'time_trace': '2026-06-18T22:36:17Z',
  'priority': 112,
  'task_summary': 'Continue tightening the top command chrome so the useful game board starts earlier and '
                  'feels less like a scrolling report.',
  'trace_summary': 'Compressed the Command top HUD, deck dock, and button chrome so the active workspace '
                   'starts much closer to the top of the screen.',
  'artifact': 'reports/agent-company-atlas-command-top-hud-compact-trace-metadata-20260619.json'},
 {'task_id': 'task-agent-company-atlas-lane-rail-signal-pips-v1-20260619',
  'trace_id': 'trace-atlas_lane_rail_signal_pips_added-20260619',
  'trace_meta_id': 'trace-agent-company-atlas-lane-rail-signal-pips-v1-20260619',
  'title': 'Lane Rail Signal Pips',
  'time_task': '2026-06-18T22:31:14Z',
  'time_trace': '2026-06-18T22:31:08Z',
  'priority': 111,
  'task_summary': 'Continue making lane selection feel like readable level selection with status signals, '
                  'unlock pressure, and active-lane priority.',
  'trace_summary': 'Added animated lane rail signal pips for level, progress, gates, and completion, with the '
                   'selected lane promoted to the first slot.',
  'artifact': 'reports/agent-company-atlas-lane-rail-signal-pips-trace-metadata-20260619.json'},
 {'task_id': 'task-agent-company-atlas-command-stage-wide-focus-v1-20260619',
  'trace_id': 'trace-atlas_command_stage_wide_focus_added-20260619',
  'trace_meta_id': 'trace-agent-company-atlas-command-stage-wide-focus-v1-20260619',
  'title': 'Command Stage Wide Focus',
  'time_task': '2026-06-18T22:26:10Z',
  'time_trace': '2026-06-18T22:26:03Z',
  'priority': 110,
  'task_summary': 'Continue turning the Command deck into a focused stage where the selected lane and its '
                  'blockers dominate the first viewport.',
  'trace_summary': 'Rebalanced the desktop Command deck around a wide center detail stage, compact lane rail, '
                   'bounded atlas map, and subtle scan motion.',
  'artifact': 'reports/agent-company-atlas-command-stage-wide-focus-trace-metadata-20260619.json'},
 {'task_id': 'task-agent-company-atlas-chronicle-stage-dock-v1-20260618',
  'trace_id': 'trace-atlas_chronicle_stage_dock_added-20260618',
  'trace_meta_id': 'trace-agent-company-atlas-chronicle-stage-dock-v1-20260618',
  'title': 'Chronicle Stage Dock',
  'time_task': '2026-06-18T22:23:02Z',
  'time_trace': '2026-06-18T22:22:55Z',
  'priority': 109,
  'task_summary': 'Continue making lane chronicle views feel like compact playable modules that expand only '
                  'when the operator asks for depth.',
  'trace_summary': 'Added the Chronicle Stage Dock so only the active path module mounts first while deeper '
                   'history stays available through compact stage controls.',
  'artifact': 'reports/agent-company-atlas-chronicle-stage-dock-trace-metadata-20260618.json'}]

RECENT_UI_UNLOCKS = RECENT_UI_UNLOCKS_20260619 + RECENT_UI_UNLOCKS_20260618
