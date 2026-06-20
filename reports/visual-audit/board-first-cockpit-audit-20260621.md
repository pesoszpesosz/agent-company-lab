# Board-First Cockpit Visual Audit - 2026-06-21

## Scope

This audit supports the next Agent Company Atlas visual iteration: a lower-scroll, premium, game-like Command cockpit where a selected money path reads as one playable board instead of a stacked report.

Local target:

- `http://127.0.0.1:5177/index.html`
- `http://127.0.0.1:5177/index.html#lane=ai_ml_competitions&view=overview&deck=command&stage=cockpit`

Captured evidence:

- `reports/visual-audit/cockpit-desktop-1440x900.png`
- `reports/visual-audit/cockpit-mobile-390x844.png`
- `reports/visual-audit/command-cockpit-desktop-1440x900.png`
- `reports/visual-audit/command-cockpit-mobile-390x844.png`

## Research Signals

The next design should combine:

- Miro-style spatial mapping: a large visual surface that can hold expandable work without forcing a report scroll.
- Linear-style focus: reduce visible noise and keep the current objective, blocker, owner, and next action obvious.
- Trello-style card clarity: each state should have a clear board/card role and a recognizable status.
- Game quest-log patterns: progress, gates, proof, and next moves should appear as level state, not prose-first dashboard copy.

## Current Desktop Findings

Default desktop first viewport:

- Header, deck dock, command ribbon, teleport rail, and control hero consume the opening view before the user reaches the selected lane surface.
- The left half of the viewport is mostly atmospheric empty space.
- Company state appears as a large report card instead of a playable game state.

Command cockpit desktop first viewport:

- The selected lane data is squeezed into a narrow left column.
- The center and right side are mostly empty atmospheric canvas.
- The route/board surface is not the dominant object despite the deck being in cockpit mode.
- The current path, blocker, proof, next action, and bot owner are visible only as dense micro-widgets.

## Current Mobile Findings

Default mobile first viewport:

- The first view spends too much height on brand, snapshot, deck chips, and company summary.
- The bottom stage nav appears before the actual game-like lane board has enough space.
- The experience starts as a report dashboard, not as a path cockpit.

Command cockpit mobile first viewport:

- The cockpit surfaces overlap heavily.
- Text and chips collide across the top of the selected lane stage.
- The large avatar/card art is visually promising, but it is buried under stacked HUD layers.
- Important controls are present, but they read as a pile of labels instead of a clean game interface.

## Design Constraints For The Next Pass

The next implementation should be judged against these constraints:

1. The Command cockpit first viewport must make the selected lane board the largest visible object on desktop.
2. Desktop should not leave a large empty center/right field while the selected lane is cramped into a side rail.
3. Mobile cockpit should show one readable selected-lane board without overlapping HUD text.
4. Navigation rails should become compact launch controls around the board, not stacked page sections.
5. Selected path state should resolve into five stable concepts: progress, blocker, proof, bot owner, and next move.
6. Long history, trail, and archive material should live behind internal drilldown affordances instead of page scroll.
7. Motion should be stateful and calmer: route runner, unlock pulse, focus tether, proof pickup, and bot handoff signal.
8. Future lanes should remain visible as locked sockets or reserve cells without adding page height.
9. The design must remain data-driven from `web/data/snapshot.json`, `lane-visuals.json`, and `agent-visuals.json`.
10. The static app contract must remain intact: no npm install, no build step, no external services.

## Recommended Next Spec

Proceed with a Board-First Cockpit redesign:

- Replace the current Command cockpit composition with a board-dominant layout.
- Promote selected lane route/playfield to the center of the first viewport.
- Collapse lane selector, stage nav, objective readout, and bot handoff into edge rails.
- Turn selected-node detail into a single command card with happened, blocker, proof, next, and owner.
- Treat Path, Trail, Game, and Comms as icon sockets inside the board.
- Add a mobile-specific board stack that reserves a stable viewport for the playfield and removes overlapping HUD slabs.

Approval is still required before implementation.
