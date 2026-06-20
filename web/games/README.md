# Lane Minigames

This folder is reserved for lane-specific modules as the Atlas grows.

Current implementation:

- Custom minigames are registered in `MINIGAME_REGISTRY` inside `web/app.js`.
- Each registry entry owns two hooks: `render(lane)` for the game board and `count(lane)` for next/previous step bounds.
- Every lane without a registered renderer falls back to the generic quest checkpoint board.

Contract:

- `web/data/lane-visuals.json` chooses the module with `lanes.<lane-id>.minigame.id`.
- `web/data/snapshot.json` provides lane state, including `trail`, `quest`, `counts`, `serviceRequests`, and optional `promotionCandidate`.
- Optional generated backdrops can be assigned with `lanes.<lane-id>.minigame.texture`; the renderer should copy that into CSS via the lane style contract.
- A lane-specific module should read only snapshot data and local UI state. It must not start workers, mutate service requests, browse, submit, trade, pay, or perform public actions.

## Add A New Minigame

1. Add a `minigame` block for the lane in `web/data/lane-visuals.json`:

   ```json
   {
     "id": "new-lane-module",
     "title": "New Lane Module",
     "mechanic": "Short player-facing mechanic text.",
     "texture": "./assets/games/new-lane-module-bg.png"
   }
   ```

2. Add a generated texture under `web/assets/games/`.

3. Add pure data builders in `web/app.js`, for example:

   ```js
   function buildNewLaneStages(lane) {
     return [
       {
         title: "Stage name",
         status: "active",
         body: compactText(lane.nextAction ?? "Waiting for the next trace.", 180),
       },
     ];
   }
   ```

4. Add a renderer that reads only the passed `lane` object and browser-local state:

   ```js
   function renderNewLaneGame(lane) {
     const stages = buildNewLaneStages(lane);
     const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, Math.max(stages.length - 1, 0));
     return `<section class="detail-section">...</section>`;
   }
   ```

5. Register the module:

   ```js
   const MINIGAME_REGISTRY = {
     "new-lane-module": {
       render: renderNewLaneGame,
       count: (lane) => buildNewLaneStages(lane).length,
     },
   };
   ```

6. Add CSS using the minigame id as the class prefix, then verify at mobile and desktop widths.

7. Record the change through the local control plane: task, artifacts, outcome, trace metadata, and regenerated snapshot.

Future modules can move from inline renderers in `web/app.js` to files under this directory once the project introduces native dynamic imports, a bundler, or a static module loader.
