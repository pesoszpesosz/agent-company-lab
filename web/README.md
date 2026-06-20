# Agent Company Atlas

Standalone visual dashboard for the Agent Company control plane.

## Run

From the repo root:

```powershell
python tools\generate_visual_dashboard_snapshot.py
python -m http.server 5177 --directory web
```

Open `http://localhost:5177`.

## Data Contract

The app reads `web/data/snapshot.json`. The snapshot generator builds it from:

- `state/agent_company.sqlite`
- `reports/service-worker-gate-map-latest.json`
- `reports/manager-proof-task-promotion-queue-latest.json`
- `web/data/lane-visuals.json`
- `web/data/agent-visuals.json`

The frontend is intentionally static: no npm install, no external service, and no build step. New agent-company repos can replace the SQLite database and reports, rerun the generator, and keep the same UI.
Worlds Future Lane Socket Board replaces the visible Worlds Launch expansion strip with a compact five-socket board for New Lane, Bot Pod, Mini Game, Asset Kit, and Proof Trail. The board is fully data-driven from lane, bot, texture, game-module, gate, and proof counts so cloned repos can add future money paths without hard-coded local assumptions.

Active Lane Level HUD sits at the top of every selected lane detail view, even when compact Path, Overview, Chronicle, or Game views hide the older header. It turns lane progress, gates, proof, completion, latest unlock, bot owner, and next action into one bounded game-status surface so a path reads immediately before deeper scrolling starts.

Active Lane Arena Band adds a five-node animated route inside that same HUD. It derives spawn level, quest progress, proof, gates, and trail depth from each lane, then runs a compact motion bead across the route so the selected path feels active without adding another scroll section.

Active Lane Depth Field adds deterministic lane-colored spark and parallax-grid motion behind the active HUD content. It is generated from lane state, gate pressure, and level data, so cloned repos and future lanes inherit premium motion without needing custom art for every path.

Active Lane Micro Chronicle adds three compact event cards inside the selected lane HUD. It surfaces latest trail state, next action, and gate/proof tone before the operator scrolls into the deeper chronicle.

Active Lane Switch Deck adds a compact level-select strip inside the selected lane HUD. It keeps the current lane first, then surfaces the highest-pressure lanes as one-click chips, reducing dependence on the long lane rail as companies add more money paths.

Active Lane Micro Chronicle adds Latest, Gate, and Next cards inside the selected lane HUD. It pulls from lane trail records, blocker maps, service requests, and next action text so the first clicked-path surface shows what happened, what is blocked, and what to do before opening deeper Trail or Chronicle views.

Active Lane View Portal Dock keeps Overview, Path, Chronicle, Trail, Game, and Comms controls visible inside the selected lane HUD. Compact views can hide the older tab row, but the HUD still works like a command pad for moving between path views without scrolling.
Active Lane View Transition Meter adds a compact animated stage meter inside the selected lane HUD. It shows the mounted view position across Overview, Path, Chronicle, Trail, Game, and Comms, making view changes read like a game-stage transition instead of another abrupt tab swap.
Active Lane Mounted Stage Frame bounds the selected lane body inside the HUD so long Overview, Path, Chronicle, Trail, Game, and Comms views scroll within a visible stage instead of stretching the whole command surface.
Active Lane Control Matrix compacts the selected lane's micro chronicle, view portals, transition meter, and lane switch deck into one command surface inside the HUD.
Active Lane Stage Lens Bar adds a sticky orientation strip inside the mounted lane stage. It keeps the current view, level XP, gate pressure, active work, and trail depth visible while the operator scrolls inside the bounded cockpit surface.
Active Lane Legacy Chrome Collapse removes the older selected-lane title/stat header and duplicate tab row once the HUD and stage lens are mounted, keeping the clicked path focused on the game cockpit instead of redundant page chrome.
Active Lane Holo Board adds a state-driven route overlay inside every mounted lane stage. It turns level, XP, gates, active work, and trail depth into five animated sockets with a moving runner, giving each clicked path a compact game-board layer without adding scroll height.
Active Lane Atmosphere Engine adds deterministic drifting light shards behind every mounted lane stage. The motes are derived from lane identity, level, progress, gates, and traces, so future lanes inherit premium ambience without new hand-authored art or extra scroll height.
Active Lane Objective Beacons add four sticky action cards inside the mounted lane stage. They surface objective, progress, gate pressure, and next choice so each clicked path keeps its current work visible while the operator scrolls.
Active Lane Bot Party Dock adds the selected lane's owner/support bots inside the mounted stage. Callsigns, avatars, command status, and next-action snippets stay visible in the cockpit so the operator can see who to talk to without leaving the path.

Command Cockpit HUD Compression turns the selected-lane HUD into a tighter status bar only inside the Command Cockpit. Avatars, the level meter, stat cells, and bot handoff block shrink, while long HUD subcopy is hidden because the mounted stage already carries the deeper context.

Command Cockpit Stage Lens Compression trims the sticky mounted-stage lens into a thinner status strip only in the Command Cockpit. The lens keeps current view and signal cells visible, but drops the extra meta line and tightens cell padding so the playable lane surface starts sooner.

Command Cockpit Mounted Stage Expansion spends the reclaimed chrome space on the playable lane viewport. The mounted stage grows taller only in the Command Cockpit, trims its internal padding and bottom fade, and starts the first detail section flush so more lane work is visible before internal scrolling.

Command Cockpit Overview Module Compression tightens the default Overview mission module inside the mounted stage. The Overview dock, meter, stage buttons, and detail-section spacing get smaller only in the Command Cockpit so the first selected-lane module reads as a compact mission board.

Command Cockpit Quest Tile Compression tightens the default quest hero tile inside that mission board. The tile uses smaller portrait and level meter sockets, less padding, and one-line objective copy so the first Overview module feels like a dense game card instead of a tall intro block.

Command Cockpit Viewport Lock turns the selected lane surface into a bounded one-screen cockpit stack. The top HUD and Overview module selector stay stable, the mounted stage owns the scrolling, and the active module button gets a moving runner so switching modules reads like a game-board action instead of another page scroll.

Command Cockpit Control Matrix Quick Deck compresses the selected-lane controller only inside the Command Cockpit. Latest/Gate/Next become three quick chips, view portals stay as a compact command row, and the view runner shares the bottom row with quick lane switching so more of the playable mounted stage stays visible.

Command Cockpit Holo Floor turns the selected lane's state-driven holo board into a lower perspective floor only inside the Command Cockpit. The board keeps its level, quest, proof, gate, and trail nodes, but the cockpit version runs under the content as a drifting grid so the lane reads more like a playable board without adding scroll height.

Command Cockpit Signal Rails compresses the mounted-stage Objective and Bot Party docks only inside the Command Cockpit. Long helper copy is hidden, cards shrink into rail cells, and bot avatars become small command pips so objective status and operator presence stay visible without crowding the playable lane stage.

Command Cockpit Quest Command Strips compresses the first Overview Quest module's support cards only inside the Command Cockpit. Signal cells, Next Move, Current Gate, and quick actions become shorter command strips so the default lane module shows current state without feeling like another tall report.

Command Cockpit Runway Level Strip compresses the Milestone Runway only inside the Command Cockpit. Header copy, lens hints, node cards, and PATH/LOG/TRL actions shrink into a tighter level-route strip so the RUN module reads like a compact progression board instead of a tall lane report.

Command Cockpit Crew Deck compresses the Agent Party only inside the Command Cockpit. Bot portrait cards become a tighter two-column crew selector with smaller avatars, summary chips, compact thread pills, and COM/Q/PATH actions so operator presence stays visible without turning the CREW module into a tall roster.

Command Cockpit Mission Console reshapes the default Quest module into a two-column command surface. The duplicate module header, pre-module floor rails, and event chain are hidden only in the bounded cockpit, while the current run, status signals, next move, gate, and quick commands stay visible as one compact mission console. The same pass restores the Command Cockpit to a single-column shell below the tablet breakpoint so the selected lane panel stops drifting off narrow screens.

Command Cockpit Mobile Launch Frame trims the narrow cockpit chrome into a smaller brand row, thinner deck rail, compact lane selector strip, and taller selected-lane stage. The phone view now opens closer to a game screen instead of spending the first viewport on stacked navigation and report framing.

Command Cockpit Mobile Quest Boss Bar turns the current-run tile into a compact live objective on narrow screens. The quest portrait and meter shrink, long summary copy disappears, the signal cells compress, and a runner scan line keeps the mission module feeling active without adding more scroll.
Command Cockpit Mobile Command Fold fixes the narrow Overview first viewport so the mounted stage no longer collapses to a clipped blank field. The mission director, queue socket, compact map, lane skin, crew dock, unlock ladder, run spine, and action row now render as one visible command fold before deeper lane exploration.
Command Cockpit Mobile Signal Glass quiets the compact mobile map behind the command overlays. Background node labels recede, while the realm skin, crew dock, unlock ladder, and run spine get stronger glass treatment so the first viewport reads as a premium control surface instead of visual noise.
Command Cockpit Relay Braid adds a local-only bot communication strip inside the Mission Director. It shows the target bot, queued/history state, thread hint, and COM/Q/COPY controls so the cockpit becomes a command hub without sending messages automatically or adding another scroll panel.
Command Cockpit Quest Camera Rail projects live milestone, blocker, proof, bot, and next-move blips behind the Quest level map. The rail is derived from lane checkpoints, gate pressure, trail proof, and crew state, adding richer animated game-board feedback without creating a new scroll section.
Command Cockpit Route Capsule adds a compact world, level, checkpoint, gate, and next nodes capsule over the Quest map. It uses the existing field-cell roles, highlights current/focused state, and animates a slim beam so the unlock path is readable without another scrolling panel.
Command Cockpit Lane Constellation keeps the active lane and neighboring money paths inside the Quest board as compact selectable chips, so large lane lists stay playable without returning to a report rail.
Command Cockpit Mission Stack turns selected-node context into four compact board stages: Timeline, Blocker, Proof, and Next. It reuses the node lens data, highlights the active lens, and keeps drill-in controls inside the Quest board instead of adding another scrolling report.
Command Cockpit Mission Dossier makes the active Timeline, Blocker, Proof, or Next lens visibly resolve above the Mission Stack. It reuses the same lens depth cards, demotes the older tray, and gives node clicks a clearer in-board payoff without adding page scroll.
Command Cockpit Level Reel turns World, Level, Checkpoint, Gate, and Next into a compact unlock strip inside the Quest board. It reuses the existing Quest node focus contract and shows quest progress without adding another report row.
Command Cockpit Unlock Pulse turns progress, gate pressure, and proof volume into pointer-transparent feedback beside the unlock strip. It follows the active Quest focus so the board feels alive without adding another scrollable panel.
Command Cockpit Focus Director makes the selected mission camera the visual priority while secondary telemetry recedes into the board. It keeps route, bot, unlock, and dossier systems available but lowers their noise so the cockpit reads more like one premium game surface.
Command Cockpit Lane Gate Selector compresses many money paths into a ranked gate selector so active lanes stay prominent while reserve gates remain reachable.
Command Cockpit Lane Expansion Slots reserves compact future money paths directly inside the gate selector. Next Path, Bot Pod, Mini Game, and Research Gate cells make expansion capacity visible without adding another scroll section.
Command Cockpit Lane Expansion Mobile Dock keeps those future slots visible in the first mobile rail as a compact four-cell dock, so phone users see expansion capacity without vertical page growth.
Command Cockpit Path Depth Lens fuses what happened, what blocks it, proof, and next move into one compact in-board HUD strip so a selected path feels deeper without opening another report.
Command Cockpit Premium Motion Governor turns the default cockpit into one premium game board by hiding leftover report rows, promoting the Quest surface, and slowing noisy animation layers.
Command Cockpit Mission Readout adds a compact in-board status strip for quest percent, focus, gate pressure, and next move without adding scroll.
Command Cockpit Unlock Trail adds an ambient level progress beam and unlock nodes behind the Quest board controls so progress reads like a path opening without adding scroll.
Command Cockpit Board Bot Badge marks the lane owner directly inside the Quest board with avatar, readiness, role, and a COM jump so ownership stays visible on the game surface.
Command Cockpit Board Atmosphere adds a data-driven texture and motion layer behind the Quest map. Progress, gate pressure, proof volume, and the focused node now tint the grid, sheen, and spark motion so the board feels premium and alive without adding scroll or stealing clicks.
Command Cockpit Boss Board merges the hero and Mission Director into a compact top HUD and lets the Quest map own the rest of the cockpit. The pass hides leftover report rows, enlarges the animated board surface, and keeps COM/Q/COPY controls usable while reducing stacked micro-panel noise.
Command Cockpit Icon Command Dock replaces the Overview action row's text-only buttons with CSS-drawn map, log, game, comms, and trail symbols. It keeps the same static routing contract and accessible labels while making the cockpit controls feel more like a game HUD.
Command Cockpit Arcade Board Fit turns the reclaimed cockpit space into a stronger first-screen game surface. It deepens the Quest board lighting, slows the scan motion, and pins the mobile icon dock back into the board so the phone view spends its empty glass on playable state instead of dead page area.
Command Cockpit Mobile Immersive Stack compresses the remaining phone chrome above the Quest board. The brand row, deck rail, lane selector, current-run hero, and Mission Director all tighten in Overview so the selected path board starts sooner and reads more like the primary game screen.
Command Cockpit Node Drill Stack adds a compact selected-node telemetry deck inside the Quest board. Focus, milestone, blocker, trail, next, and proof cards now update from the clicked node, making each path feel deeper without adding another scrolling report section.
Command Cockpit Clarity Mode fades secondary board noise, keeps the selected Quest node visually dominant, and pares the in-board drill deck down to Focus, Blocker, and Next in the default cockpit view so the first screen reads as one clear game state instead of a report wall.
Command Cockpit Cinematic Focus Plate replaces that tiny drill rail in the default cockpit with a single mission plate inside the Quest board. The plate binds the selected node, blocker state, and next move into one readable game-camera lock, reducing micro-card clutter without adding scroll.
Command Cockpit Cinematic Focus Tether adds an animated lock line from the selected Quest node column into the focus plate. The tether is driven by the focused node index, so node clicks now feel spatially connected without adding another surface or page height.
Command Cockpit Cinematic Bot Relay adds the responsible bot directly into that focus plate. A compact avatar/callsign/readiness COM chip opens the lane Comms deck, making the selected path feel like a live command surface without adding another panel.
Command Cockpit Cinematic Reward Rail adds proof and unlock feedback directly inside the focus plate. The selected node now exposes compact Proof and Unlock pips with a soft pulse, so achievements and milestone progress stay visible without creating another scroll row.
Command Cockpit Cinematic Event Heartbeat surfaces recent activity inside the same focus plate. It reuses the Quest event packet model to show tiny live pulses for what just happened on the selected path, keeping history visible without reopening the hidden event chain.
Command Cockpit Cinematic Action Sockets embeds Path, Trail, Game, and Comms controls inside the selected-node focus plate. The default cockpit can jump into the useful lane views from the board itself, reducing dependence on lower action rows and keeping the experience closer to a game HUD.
Command Cockpit Secondary Action Dock compresses the older Overview action row into a fallback rail. Path, Trail, Game, and Comms become quiet secondary pips because the focus plate now owns those actions, while Log stays available without competing for the first-screen command surface.
Command Cockpit Board Signal Overlay moves asks, unlocks, events, and score into the Quest board as compact status pips. The older signal row remains in the markup as ghost chrome, but the visible state now lives inside the game surface instead of stacking another HUD row above it.

Command Cockpit Board Identity Cartridge moves lane identity and quest progress into the Quest board as a compact animated cartridge. The older hero strip stays in the markup as ghost chrome, reducing first-screen stacking while keeping the selected path, latest discovery, minigame family, and quest percentage visible inside the playable surface.

Command Cockpit Ambient Overlay Hierarchy quiets older realm, crew, and unlock overlays inside the Quest board. Those controls remain clickable, but their glass, sweep, and label layers become ambient until hover or keyboard focus so the identity cartridge and selected-node focus plate read as the main game state.

Command Cockpit Spotlight Node Hierarchy turns unselected Quest nodes into quiet map pips while keeping the focused node readable, animated, and visually dominant. The cockpit keeps every node clickable, but the default board now reads like a selected game target instead of five competing report cards.

Command Cockpit Spotlight Camera Aperture adds a subtle camera-lock aperture over the selected Quest node. It uses the selected node index to position a non-interactive animated reticle layer, making node focus feel more deliberate without adding another panel or scroll surface.

Command Cockpit Mobile Footer Layering lets the mobile Run Spine own the bottom Proof/Gate/Next band. The lower echo rail and older fallback action dock recede under the cockpit breakpoint so the board footer reads as one clear command strip instead of stacked microtext.

Command Cockpit Mobile Launch Chrome Squeeze pulls the Quest board closer to the top of the phone viewport. The deck dock and lane strip get tighter in Cockpit Overview, the mounted stage lifts slightly, and the board gains a taller clamp so the first screen spends more pixels on playable path state.

Command Cockpit Mobile Director Readout keeps the current blocker visible as a compact chip inside the phone Mission Director. The eyebrow recedes, the objective stays on one line, and the blocker/body text becomes a right-side pill so the boss bar remains short without losing context.

Command Cockpit Desktop Board First Lift pulls the desktop Quest board upward so the first viewport spends more room on playable path state. The mission director becomes a short boss bar, secondary director chrome recedes, and the board gets a taller minimum so the cockpit reads less like a scroll page.

Command Cockpit Desktop Stage Chrome Collapse removes duplicated desktop pre-board ribbons from Cockpit Overview. The event ribbon and stage footer rail no longer take vertical space above the Quest board on wide screens, while the playable board keeps the status overlays that already carry level, gate, proof, and next-move state.

Command Cockpit Selected Node Expansion Console adds in-board timeline, blocker, proof, and next-move rows for the currently selected Quest node. The console occupies the unused right-side board lane on desktop and compresses into a 2x2 strip above the focus plate on mobile, giving each clicked node a deeper readout without adding scroll.

Command Cockpit Selected Node Expansion Actions turns those timeline, blocker, proof, and next-move rows into drill-in controls. The rows now open Trail, Path, or Comms directly from the board, with hover/focus motion and reduced-motion handling so the cockpit feels more playable without adding another vertical panel.

Command Cockpit Selected Node Lens Tray keeps the first drilldown inside the board. Timeline, blocker, proof, and next-move clicks now update a compact selected-node lens tray with an explicit Open action for the full Trail, Path, or Comms module, so the cockpit can reveal node context without immediately forcing another tall view.

Command Cockpit Selected Node Lens Depth Cards adds three compact depth cards under the active node lens. Timeline, blocker, proof, and next-move lenses now each show local context cards inside the Quest board, making a clicked node feel like an expandable dossier without adding page scroll.

Command Cockpit Selected Node Lens Reactor adds an active-lens reactor rail behind the selected-node tray. The rail, core pulse, and tone pips make the local dossier feel energized while remaining pointer-transparent and reduced-motion friendly.

Command Cockpit Stage Footer Rail turns the empty floor below the compact Overview mission panel into a live stage status strip. Level, quest progress, gate pressure, and next move now anchor the bottom of the mounted stage with a small animated rail instead of leaving dead glass space.

Command Cockpit Desktop Footer Pin keeps that mounted-stage status rail visible on wide screens too. The Overview stage rail now sticks to the bottom of the scrollable cockpit surface, so level, quest, gates, and next move remain readable instead of falling below the desktop stage.

Command Cockpit Overview HUD Slimline trims the desktop Overview lane header into a launch strip. The bot event copy and nested command matrix stay out of the first-screen cockpit, letting the playable stage move upward while the lane identity, stats, and route pulse remain visible.

Command Cockpit Quest Field Board turns the current-run card stack into a visible milestone field. Overview now renders world, level, checkpoint, gate, and next-move cells on an animated route rail, replacing the taller next/gate report row inside the Command Cockpit stage.

Command Cockpit Stage Holo Floor turns the remaining dark Overview stage floor into an intentional animated arena surface. The mounted stage now projects lane progress, quest, proof, gates, and trail pads behind the mission module so the compact cockpit feels alive without adding scroll.

Command Cockpit Stage Depth Rings adds a lane-colored parallax ring layer inside the bounded Overview stage. The rings use current lane progress to rotate and pulse behind the mission board, giving the selected path a richer game-arena feel without increasing page height or adding another report panel; on narrow screens the heavier holo floor is suppressed so the mission card stays readable.

Command Cockpit World Map Strip replaces the hidden Overview HUD route row with a compact six-node world map. World, Level, Quest, Proof, Gate, and Bot nodes share one animated runner, giving the operator a game-like read of where the selected money path stands before opening deeper lane views.

Command Cockpit Stage Event Ribbon adds a sticky four-cell event strip inside the mounted Overview stage. Latest event, proof count, gate state, and next move stay visible as compact animated pips, making what happened and what is blocked readable without adding another report stack.

Command Cockpit Bot Character Frame turns the selected-lane owner portrait into a compact character socket. Callsign, specialty, accent color, and sprite-sheet cell identity now drive an animated aura, scan line, and tiny sigil inside the existing HUD footprint, so bots feel more like game companions without adding another scroll layer.

Command Cockpit Mission Cartridge adds a generated game-HUD texture behind the selected-lane status bar and tightens the mobile cockpit header. The phone HUD now spends less vertical space on duplicate labels, the world-map strip is shorter, and the new reusable texture is listed in the Visual Asset Vault as standalone system art.

Command Cockpit Stage Compass turns the existing Overview module dock into a compact level selector. The dock now carries an active-stage runner and tiny module sockets using current stage index metadata, so Quest, Runway, Crew, Forge, Gates, and Intel read like playable stage nodes without adding another scroll row.

Command Cockpit Territory Board turns the cockpit lane rail from a long vertical list into a compact two-column mission board. The rail now emits active-lane index metadata, a route line, a moving runner, and lane territory nodes so expanding money paths read as selectable map territories while mobile keeps the fast single-row picker.

Command Cockpit Quest Level Map turns the default Overview Quest field into a compact in-stage level map. The existing World, Level, Checkpoint, Gate, and Next cells now sit on a route bed with node sockets, a progress runner, and a subtle desktop stagger, making the selected lane feel more like a playable path without adding another panel.

Command Cockpit Quest Node Focus adds role and current-state treatment to that level map. World, Level, Checkpoint, Gate, and Next now carry map/XP/active/lock/go glyphs, active checkpoint and blocker nodes pulse, and the narrow cockpit hides extra glyph chrome so the route stays readable.

Command Cockpit Viewport Fit removes the leftover stage-card row from the cockpit Overview and compresses the signal/action strips into HUD-sized readouts. The first view now behaves more like a fitted game command screen: current run, route map, signals, and navigation are visible without the level map being followed by duplicate scroll content.

Command Cockpit Footer Overlay turns the mounted-stage status rail into a compact glass HUD overlay. The footer no longer reserves document height, the status cells compress into two-column readouts, and the first cockpit screen keeps the path state visible without adding another scroll row.

Command Cockpit Unlock Badges turns the Overview signal strip into a compact reward-badge row. Asks, unlocks, events, and score now carry short GATE/WIN/RUN/XP glyphs, state metadata, and a subtle badge sweep so the cockpit reads more like level feedback without adding another scroll row.

Command Cockpit Minigame Sigil adds a lane-specific animated module badge inside the current-run hero. Each selected path now exposes its minigame family as compact game hardware with orbit/glint motion, giving future lanes a distinct first-screen identity without creating another vertical panel.

Command Cockpit Node Focus Lens turns the Quest level map sockets into selectable board nodes. World, Level, Checkpoint, Gate, and Next now update a compact scanner lens inside the board, so clicked paths can reveal deeper current-state detail without adding another scrolling report row.

Command Cockpit Node Signal Packets adds three role-aware telemetry chips inside the selected Quest node lens. World, Level, Checkpoint, Gate, and Next now expose compact state, pressure, and next-action packets so clicked nodes feel deeper without adding another scroll row.

Command Cockpit Node Echo Rail projects four role-aware path signals directly onto the Quest board for the selected node. The rail changes between realm, level, checkpoint, gate, and next-action echoes, giving clicked paths a richer "what happened / what blocks it / what moves next" read without adding another section.

Command Cockpit Insight Ribbon adds a generated HUD strip inside the Quest level map. Clicking World, Level, Checkpoint, Gate, or Next now projects milestone, blocker, bot, proof, and next-move chips from reusable lane, trail, gate, and agent data without adding another scroll row.

Command Cockpit Focus Beam adds a generated reticle texture to the Quest level map. The selected World, Level, Checkpoint, Gate, or Next node now drives a moving in-board focus beam, making clicks feel like a game camera lock without adding another panel or scroll row.

Command Cockpit Crew Relay adds the responsible bot directly into the selected Quest node lens. The relay reuses Agent Party data for avatar, callsign, readiness, and gate/staged tone, then exposes a compact COM jump without adding another crew panel.

Command Cockpit Node Halos adds compact proof, gate, trail, score, crew, and next-move medals directly onto Quest level-map cells. The medals are derived from reusable lane counts and checkpoint data, making path state visible at a glance without adding a scroll row.

Command Cockpit Event Pulse adds a procedural route-pulse texture and live trail packets inside the Quest level map. Recent lane events, blockers, proof, and unlocks now move through the existing board footprint so the selected path feels active without adding another scroll row.

Command Cockpit Event Lens turns those moving trail packets into selectable in-board explainers. Clicking a packet updates a compact lens with event type, title, and time, so the operator can see what happened without opening another tall event list.

Command Cockpit Low-Scroll Premium Pass turns the Command Cockpit into a tighter first-screen game board. It clamps the cockpit shell, turns the lane rail into a short selector, hides live/archive support surfaces while the cockpit stage is active, and calms the extra glow layers so the selected lane, quest map, blocker state, and next move read before any deeper scrolling.

Command Cockpit Mission Director adds one obvious current objective inside the Quest Cockpit. It combines the selected lane's next move, owner bot, blocker pressure, proof/reward state, and quest progress into a single animated mission band, then suppresses the duplicate Next/Gate card row in cockpit mode so the board has a clearer center of gravity.

Command Cockpit Mission Director Action Sockets make that band operational. Owner, Gate, and Reward chips jump straight to Comms, Path, and Trail for the selected lane, turning the cockpit into a control surface instead of a passive status card.

Command Cockpit Mobile Run Board tightens the phone cockpit into a playable board instead of a long page. The selected lane now names itself as a money-path run, the lane picker returns to a compact horizontal rail for large lane counts, duplicate stage/event rows are suppressed on mobile, the quest map is viewport-bounded, and cockpit overflow is clipped so decorative layers cannot create side-scroll.

Command Cockpit Run Spine adds a compact proof/gate/next overlay inside the level map. The three animated sockets open Trail and Path views, so the cockpit explains what has been proven, what is blocking progress, and what move is queued without adding another scroll section.

Command Cockpit Realm Skin Cartridge makes each lane's current minigame identity visible inside the compact quest map. It reuses `lane.visual.minigame` texture/title/mechanic data, shows custom-vs-template realm state plus gate/win pressure, and opens the lane Game view without adding a new panel.

Command Cockpit Realm Mood Layer gives each selected path a distinct compact game-world mood inside the Quest board. It reads reusable lane visual/minigame data, motion type, gate pressure, and unlock charge so different game worlds are visible without adding another scroll section.

Command Cockpit Lane World Signal makes the lane rail feel expandable: every lane button now carries a tiny textured world chip derived from its minigame id/title, world number, and custom/template state. The chip is non-interactive so lane selection remains simple, but it makes future lane slots read as playable worlds rather than a plain list.
Command Cockpit Lane Unlock Lens adds a compact cockpit-only readiness chip to every lane card. It derives GAME/SEED state, stage count, gate pressure, and readiness fill from `lane.visual.minigame`, `MINIGAME_REGISTRY`, progress, and blockers so expanding lane lists feel like unlockable worlds without changing the data schema.

Command Bot Squadron HUD turns the Bots stage into a more immediate command crew surface. It adds a compact avatar cluster, selected bot readiness orbit, ready/gated/staged/art stats, and priority bot beacons above the card deck without adding another long section.

Agent Constellation Bay adds a generated system texture and live agent beacons to the Agent Sprite Foundry. Bots now orbit a mission core with readiness meters and quick lane selection, making the reusable bot identity layer feel more like a premium command game surface.

Lane Expansion Portal Deck adds a generated socket-board texture inside Worlds Launch so future lanes and lane-specific minigames appear as compact unlock portals. The board reuses existing Worlds, Arcade, Registry, Genesis, and Asset jumps, keeping expansion visible without adding another long-scroll section.

Command Cockpit Stable Board keeps the clicked path in place during Command Cockpit interactions and spends more first-screen space on the playable Quest board. Automatic detail-panel jumps are suppressed only in the cockpit, the overview HUD tightens, and a subtle board scan gives the selected lane a calmer premium game-surface feel without adding more scroll.

Command Cockpit Path Depth Stack adds four compact strata inside the Quest level map. Latest event, level depth, gate pressure, and next move now read as animated layers behind the selected path, making the clicked lane feel expandable without adding another report row.

Command Cockpit Crew Chip Focus turns the desktop Overview bot handoff block into a compact crew chip and adds a soft right-edge focus fade. The selected path keeps its operator identity visible, but the cockpit no longer reads as if another report column is crowding the game stage.

Command Cockpit Lane Cartridge Rail compresses the desktop cockpit lane rail into level-select cartridges. More money paths fit in the first screen, realm copy is deferred until selection, and level/gate/win/live cells plus signal pips keep every lane scannable without making the rail feel like a long report stack.

Command Cockpit Mobile HUD Strip turns the selected-lane HUD into a compact status strip on narrow screens. The core lane card, XP/proof/gate cells, and bot identity stay visible, while the deeper route arena and control matrix defer to the mounted mission console and bottom dock so the first mobile cockpit view stops feeling clipped.

The main dashboard includes a company-level Operator Roster with a generated-art Operator Identity Bay. The bay summarizes active bots, mapped portraits, lane bindings, staged asks, spare expansion slots, and direct COM/ASSET/FORGE jumps before the individual agent cards. Each agent card reads `snapshot.agents[].visual` and `snapshot.agents[].lane`, then links into that lane's Comms deck when an owner lane is known.

The Agent Sprite Foundry uses the generated `agent-sprite-foundry-20260618.png` texture inside the Operator Roster to turn bot portraits into a reusable character-production layer. It summarizes portrait, lane, thread, and future-slot coverage, shows each bot's sprite readiness card, exposes COM/ASSET/FORGE actions, and leaves visible sockets for future agents without changing the snapshot schema.

The Visual Asset Vault reads generated lane avatars, minigame textures, agent portraits, the Operator Identity Bay texture, and system source sheets from the same static data contract. It groups them with local filters under `agent-company-atlas.asset-filter.v1` and lets lane-linked assets drill into the relevant Overview, Game, or Comms view.

Asset Production Board adds a compact coverage strip above the Visual Asset Vault inventory. It tracks lane avatar, bot portrait, game texture, system art, and future-slot coverage so expanding agent companies can see which visual families are complete before opening the full asset grid.

Command Cockpit Viewport Console Governor constrains the selected lane cockpit into a first-screen console on desktop and a tighter board on mobile. The lane rail becomes an internal scroll surface, duplicate detail chrome is suppressed in overview, and a single slow scan animation replaces competing motion so the command deck feels more playable and less like a page-length report.

Command Cockpit Route Minimap adds a compact selected-lane route strip inside the cockpit stage. It derives gate, task, proof, bot, game, and next-command nodes from reusable snapshot data so each lane feels like a playable path without adding another long-scroll report panel.

Command Cockpit Channel Dock centralizes the selected lane's local bot handoff state inside the first cockpit view. It shows owner, queued drafts, blocker pressure, and next ask beside COM/Q actions, keeping bot communication visible without sending messages or adding another scroll-heavy board.

Worlds Expansion Radar adds a compact command instrument inside the Worlds Launch board. It summarizes live worlds, game seeds, bot pods, asset coverage, and future slots in one short animated strip so new agent-company repos can understand expansion readiness without opening another long report panel.

Path Chapter Boss Bar adds a compact selected-level status strip to the Path stage. It summarizes the selected chapter's gates, proof, unlocks, next record, and archive jumps so users can understand the current level before expanding the deeper chapter dossier.

Atlas Command Ribbon adds a compact global command strip below the deck switcher. It summarizes lanes, gates, bots, wins, assets, and next focus, then routes each cell into the relevant deck so the Atlas feels more like a centralized game command HUD and less like separate report pages.

Atlas Motion Conductor adds a compact animated instrument inside the global ribbon. It mirrors the live motion mode, lane focus, gate, proof, test, and unlock charge so the site feels more coordinated and game-like without creating another scroll-heavy panel.

Command Cockpit Control Pad adds a compact in-stage game controller for Path, Gate, Proof, Bot, Game, and Queue actions. It keeps the selected lane's next moves inside the cockpit frame so operators can switch views or stage a bot command without scrolling through report panels.

Command Cockpit Runway Pulse adds a short animated status track under the controller. It visualizes the latest event, task pressure, blockers, proof, and next move as clickable lane pulses so the selected path reads like a live run instead of a hidden report trail.

Command Cockpit Crew Handoff Rail adds a compact bot relay strip inside the selected lane cockpit. It shows owner and support bots, staged queue state, and next command so bot communication is visible without opening the full bot board or a long comms report.

Command Cockpit Unlock Chain adds a compact progression strip for Level, Quest, Gate, Proof, and Reward inside the selected lane cockpit. It makes the next unlock path visible as clickable stages before the deeper route and path panels.

Command Cockpit HUD Stack compresses the controller, run pulse, crew handoff, and unlock chain into one coordinated cockpit grid on desktop while preserving the clean single-column mobile flow. It reduces vertical cockpit chrome without hiding the controls or live lane state.

Command Cockpit Board First Shelf collapses the command HUD into one desktop shelf, trims secondary route and channel microcopy, and gives the reclaimed height back to the Quest board so the first cockpit viewport feels more like a playable command surface than a stacked report.

The Trophy Room reads completed outcome events from `snapshot.missionFeed.items` and lane outcome counts from `snapshot.lanes[].counts`. It renders recent wins as collectible cards with lane art, reward text, tier labels, and click-through Trail links, then shows lane-level trophy tracks for the most outcome-rich lanes. Trophy tier and lane filters are browser-local preferences stored under `agent-company-atlas.trophy-filter.v1`.

The snapshot unlock toast compares the newest completed outcome against the browser-local `agent-company-atlas.last-unlock.v1` key. When the snapshot contains a newly seen outcome, it shows a brief achievement card with medal art, lane identity, XP, dismiss, and Open Trail actions. On phone-sized screens the toast compresses into a reward strip so it celebrates progress without covering the playable board. If storage is unavailable, the Atlas still runs and simply treats unlock memory as optional.

Path Stage Reward Ticker further compresses the same unlock toast only inside the command cockpit path board, turning new wins into a small bottom ticker with medal art, one-line reward text, tiny XP/meta chips, and compact actions so achievement feedback no longer blocks the playable route surface.

The snapshot generator embeds short `artifactPreview` snippets for local text-like artifacts referenced by trail events. It resolves only files inside the repo root, skips URLs and unsupported or binary extensions, and keeps previews compact so the static dashboard can show proof context without reading files from the browser.

The Live Ops Pulse uses the generated `live-ops-pulse-20260618.png` texture under the first-screen hero to show what is happening right now. It fuses latest feed movement, active tasks, blocker gates, ready bot asks, staged local drafts, bot ownership, and lane pulse cards into LATEST/GATES/COMMS/TIMELINE jumps without mutating snapshot data or sending messages.

The Control Runway lives inside the first-screen Company State panel. It uses the generated `control-runway-20260618.png` texture to turn the selected lane plus the highest-pressure active lanes into compact level nodes with gate/win readouts, animated charge bars, and Command-deck drill-through. It is derived from the same lane, feed, task, blocker, dispatch, and staged-draft data as Live Ops Pulse, so new agent-company repos inherit the runway without adding schema fields.

The Path Stage HUD Strip uses the generated `path-stage-hud-strip-20260618.png` texture to make the compact Path Stage Ribbon read like a game route rail. It keeps the same path nodes, gates, unlocks, and future slots, but adds a reusable bitmap layer behind the motion scan so direct Path links feel like a deliberate stage screen instead of plain stacked UI.

The Path Stage Playfield Texture uses the generated `path-stage-playfield-rail-20260620.png` backdrop behind the compact Path Stage route rail. It gives clicked-path level tokens a richer holographic map surface while keeping the asset generic enough for forked agent-company repos and future lane families.

The Path Run Meter HUD uses the generated `path-run-meter-hud-20260618.png` texture behind Mission Glance's five-socket level strip. It gives route, gate, proof, task, and note state a richer game-HUD surface without adding another first-viewport panel.

The Dispatch Console reads `snapshot.dispatchConsole.suggestions`, a per-lane set of local command suggestions built from gates, promotion candidates, active tasks, and next actions. Staged commands are stored only in browser `localStorage` under `agent-company-atlas.dispatch-outbox.v1`; the local operator trace is stored under `agent-company-atlas.dispatch-history.v1`. The Atlas never sends messages or starts workers by itself.

The Command Relay Deck uses the generated `command-relay-deck-20260618.png` texture to centralize bot communication into one global relay board. It composes bot ownership, lane bindings, dispatch suggestions, staged browser-local drafts, blocker gates, threads, and operator history into COM/Q/MATRIX controls, plus future sockets for worker channels, approvals, batch lanes, and operator notes. It remains local-only: Q stages a draft, COM opens the lane Comms deck, and MATRIX jumps to the existing Bot Command Matrix.

The Company Quest Board uses the generated `company-quest-board-20260618.png` texture to turn all lane tasks, blockers, outcomes, dispatch suggestions, and staged drafts into a global mission board. It ranks current lane cards by pressure and movement, shows task/gate/win counts, and exposes TASKS/GATES/WINS lenses that jump into the existing Mission Feed filters without mutating snapshot data.

The Comms Command Room uses the generated `comms-command-room-20260618.png` texture to turn each lane Comms view into a bot handoff console. It derives owner portrait, command target, lane status, staged queue count, local operator history, blocker count, urgency, thread context, and local Q/C/PATH actions from existing snapshot and browser-local dispatch state; it still only stages or copies local drafts.

Comms Command Inbox Board adds four compact cells inside that command room for queued draft, local log, blocker, and next ask state. It keeps the first Comms viewport scannable as a live bot channel without adding another page-length report section.

The Bot Command Matrix reads `snapshot.agents`, each agent's bound lane, and `snapshot.dispatchConsole.suggestions` to show one command-center card per bot. It surfaces status, lane, thread id, blocker pressure, review gates, urgency, top suggested command, Comms drill-through, and browser-local staging without sending anything by itself.

The Thread Nexus reads the same agent, lane, thread, and dispatch suggestion data as the Bot Command Matrix, then renders it as a node-link command network. It shows which bot owns which lane, which threads are gated or staged, and which command asks are most urgent, while keeping all actions local-only.

The Crew Bridge turns the same bot, lane, thread, and dispatch records into a compact squad-readiness deck. It highlights the selected crew, readiness, gate pressure, urgency, staged state, and quick COM/Q/PATH actions while keeping Q as a browser-local draft stage only.

The Mission Feed reads `snapshot.missionFeed.items`, a cross-lane chronological stream built from each lane's trail. Feed cards can be filtered by event type and open the source lane's Trail view. Each event is rendered as a reusable scene card that derives lane art, realm, accent colors, rarity, status, and XP-style reward text from the existing snapshot fields.

Mission Feed Timeline Board adds a compact replay/status strip above the deeper feed modules. It surfaces the current replay event plus Gates, Proof, Wins, and Lanes cells for the active lens so the history deck reads like a command board before the long event list.

The Company Chronicle Spine uses the generated `company-chronicle-spine-20260618.png` texture inside the Mission Feed to group the current feed lens into global chapter cards. It summarizes event, chapter, lane, proof, and win counts, exposes LATEST/PROOF/GATES actions through existing feed filters, and lets each chapter open the source lane Trail without changing the snapshot schema.

The Experiment Discovery Lab uses the generated `experiment-discovery-lab-20260618.png` texture inside the Mission Feed to turn tested paths, proof captures, blocker gates, outcomes, and traces into a company-wide lab board. It groups the active feed lens by lane, scores each lane by tests/proof/gates/wins, exposes PROOF/GATES/WINS feed actions, opens lane Trail views from lab cards, and leaves future sockets for hypotheses, proof capture, parked tests, and win rituals.

Mission Feed preferences are local-only. The selected filter is stored under `agent-company-atlas.feed-filter.v1`, and saved feed lenses are stored under `agent-company-atlas.feed-saved-views.v1`. Playback is an in-browser visual replay of the currently filtered feed; it also highlights the source lane on the map with a pulse route and HUD, and it does not mutate data.

The lane map uses reusable focus states for hover, keyboard focus, selected lanes, and playback lanes. Route highlights, node aura sparks, and the Lane Focus readout are derived from existing lane fields, so new lanes inherit the same premium map behavior without extra code.

The Path Map detail view reads each lane's quest checkpoints, gate map, service requests, recent outcomes, owner agent, dispatch suggestions, and trail records. It renders a compact horizontal route board with progress, a shared route spine, animated runner, focused-node socket, scroll-snap stage cards for future lane growth, a compact animated Mission Scan for route/gate/proof/task/unlock/future state, a Path Command Strip for next move, active gate, proof, bot, notes, and direct route/proof/archive/queue/comms jumps, blocker radar, route handoff, clickable route nodes, a generated-art Chapter Archive, a Node Intel focus panel, clickable related trail-event stacks, an expandable lane-level Proof Cache, a browser-local Route Replay controller, a focused Event Proof lens with NEWER/OLDER trail navigation and safe local artifact previews, unlock nodes, future slots, browser-local Gate Radar note previews, and an expandable event stream so long-running lanes can keep unfolding without changing the schema. Its Chapter Archive groups the lane trail into date-derived mission-journal chapters, uses the generated `path-chapter-archive-20260618.png` texture as a premium archive-console backdrop, and lets each chapter focus the newest event while revealing enough of the Event Stream to show that chapter. The selected chapter also opens a browser-local record deck with typed glyph cards, per-chapter All/Proof/Unlock/Service/Task/Trace/Gate lenses, a generated `path-chapter-depth-rings-20260618.png` Chapter Depth Rings orbit board that visualizes proof/gate/task/trace density and hidden lens depth, a generated `path-chapter-milestone-ladder-20260618.png` Chapter Milestone Ladder that turns chapter proof/gate/task/unlock/next signals into clickable game-style unlock rungs, a generated `path-chapter-game-portal-20260618.png` Chapter Game Portal that binds the chapter to the lane minigame texture, registry status, stage count, asset coverage, and GAME/FORGE/TRAIL jumps, a Chapter Questline stage strip using `path-chapter-questline-20260618.png` and a reduced-motion-aware pulse trail for spawn/proof/gate/task/unlock/next-move progression, a Chapter Spoils medal shelf using `path-chapter-spoils-20260618.png`, a Chapter Evidence Vault that deduplicates chapter artifacts, safe local previews, proof records, and outcome packets into direct Event Proof focus cards, a Chapter Crew Relay with a generated `chapter-crew-formation-20260618.png` Chapter Crew Formation board that binds the chapter to lane bots, portrait slots, readiness meters, thread context, proof/gate/trace pressure, and local COM/Q handoff controls, a Chapter Command Log with a generated `path-chapter-command-relay-20260618.png` Path Chapter Command Relay console that blends the current suggested draft, staged outbox items, browser-local operator history, chapter context, queue stats, and local Q/COM/TRAIL actions into one compact bot handoff timeline, a Chapter Gate Stack with a generated `path-chapter-gate-heatfield-20260618.png` Chapter Gate Heatfield scan that turns lane gate-map signals, service-request gates, local Gate Radar notes, and chapter gate counts into a compact blocker board, a Chapter Task Board that merges selected-chapter task records with lane recent tasks, status, priority, owner, and next-action cards, a Chapter Runway sequence rail for the active lens, direct Event Proof focus, and reveal-more controls for deeper chapter history. Its Route Replay plays lane history forward through the same Event Proof lens without mutating data, using the generated `route-replay-chronometer-20260618.png` texture as its timeline device backdrop and the generated `route-replay-event-glyph-sheet-20260618.png` sprite sheet for proof, trace, outcome, gate, task, and service stage icons. The Replay Lens filter chips are browser-local and narrow replay playback to event glyph types without changing the snapshot, while the Stage Queue shows the current and upcoming filtered replay stages as direct jump cards. Its Route Handoff card uses the generated `path-handoff-beacon-20260618.png` command-transfer texture and stages only browser-local command drafts through the Dispatch Console outbox; it does not contact agents or start workers.

Mission Glance replaces the old Path Map hero: it compresses current objective, route progress, gate pressure, proof count, active tasks, notes, unlock status, and route/proof/archive/comms jumps into one top control surface so each path reads like a game-state screen before deeper scrolling starts.

Path Run Meter adds a compact five-socket level strip inside Mission Glance for route, gate, proof, tasks, and notes. It turns the top copy area into a readable game HUD without adding another panel or increasing first-pass scroll.

Path Crew Presence adds a compact avatar strip under the Mission Glance run meter. It reuses the lane's mapped bot portraits, readiness, gated/ready/staged state, and callsigns so the first Path viewport shows who is driving the run before opening Comms or the deeper Crew Bridge.

Path Depth Pill turns the default Stage Depth row into a compact floating pill while the cockpit is in one-screen Stage mode. Archive and Tools still expand into deeper panels when selected, but the first Path view gives that space back to the game board.

Path Core Deck compacts the old immediate Path Map stack: Mission Scan, Route Command, and Route Rail now live behind SCAN/COMMAND/ROUTE tabs with one selected panel mounted at a time, keeping the top path screen game-like and reducing first-pass vertical scrolling.

Path Core Snapshot replaces the cramped default Core module body with a compact active-module lens. It keeps Scan/Command/Route choices visible while showing a route arc, three meaningful signal cards, and fast actions instead of a chopped internal scroll panel.

Path Stage Focus Lens adds a compact overlay to the level ribbon that explains the focused gate, checkpoint, unlock, or future slot. It turns the ribbon from tiny labels into an actionable level selector without adding another panel.

Path Stage Atmosphere adds a deterministic procedural bitmap behind the bounded Path cockpit. It gives the route board a richer level-world texture while staying reusable for GitHub clones and avoiding any runtime image-generation dependency.

Path Stage Signal Weather adds a lane-state animation layer to the bounded Path cockpit. Blockers, proof, active work, and notes now appear as subtle drifting signals behind the panels, making the stage feel alive without adding another scroll section.

Path Stage Nav Dock moves the Path view's navigation into the cockpit as a compact HUD strip. The duplicate text tab row is hidden only in Path mode, reducing page chrome while preserving quick access to overview, logs, trail, game, and comms.

Overview Stage Dock makes the lane Overview mount one mission module at a time behind a compact dock. Quest, runway, crew, forge, gates, and intel stay reachable without rendering the whole overview stack at once.

Lane Rail Signal Pips adds compact animated level, progress, and gate signals to each lane rail card. The Command deck can now show path state at a glance without expanding the lane list into another text-heavy panel.

Lane Rail Level Selector turns each lane rail card into a compact level-select tray. Level, XP, gates, wins, and live work sit in four tiny status cells, making the lane rail feel more like choosing a playable money-path level than scanning a long task list.

Command Cockpit Lane Selector Compression lets that selector replace older duplicate rail chrome in the Cockpit stage. Lane cards shrink, avatars tighten, and the old progress bar plus muted summary disappear only there, so the command rail fits more money-path levels before scrolling.

Command Top HUD Compact tightens the Command deck's top chrome into a shorter game HUD. The Atlas mark, snapshot pill, and deck switcher now consume less first-viewport height so the active lane stage starts sooner.

Command Archive Shelf bounds the Command deck's lower relay, dispatch, quest, crew, and roster boards into compact internal viewports. The deep material stays reachable, but the page no longer forces every support board to become another tall scroll segment.

Command Mobile Stage Stack makes the phone-sized Command workspace behave like bounded game layers. The active lane detail stays first, the lane rail becomes a shorter internal selector, and the atlas map becomes a compact tactical slice instead of a tall forced-scroll block.

Command Cinematic Motion adds scoped depth, glints, and slower easing to the Command deck's active lane stage, lane rail pips, and atlas map. It improves the premium game-board feeling without increasing page height or adding another panel.

Command Archive Focus Dock replaces the lower Command deck pile with one focused support board at a time. Relay, Dispatch, Command, Quest, Crew, Threads, Bots, and Operators are still one click away, but the page no longer asks the operator to scroll through every support surface in sequence.

Command Stage Wide Focus makes the Command deck treat the selected lane detail as the center stage on desktop. The lane list becomes a compact rail, the atlas map shifts into a supporting side column, and the active detail surface gets a restrained scan layer so logs, paths, games, and comms feel less like a narrow receipt.

Command Cockpit Stage Gate makes Cockpit and Map feel like separate levels instead of one crowded command stack. Cockpit now hides the atlas map, gives the selected lane stage the main column, and keeps the lane rail in a bounded selector; Map remains available as its own tactical teleport screen.

Chronicle Stage Dock makes each lane Chronicle open as a compact log console. Signal, Route, Gates, and Stream panels are one click away, but only the active Chronicle module mounts first so the event history stays expandable without becoming the first-screen payload.

Game Stage HUD gives every lane minigame a compact arcade navigation shell. Game mode now hides duplicated detail chrome and shows the current module step plus quick jumps to overview, map, log, trail, play, and comms.

Overview Stage Dock turns each lane Overview into a compact mission-select surface. Quest, Runway, Crew, Forge, Gates, and Intel panels stay one click away, but only the active module mounts first so Overview no longer opens as a long idea-board stack.

Path Stage Shell makes direct Path links open as a bounded cockpit first. Mission Glance, the Stage Ribbon, Core Deck, and a compact Stage Depth switcher mount by default; Archive and Tools are explicit depth modes that mount one deeper panel only after the operator chooses it.

Path Core Motion Rail adds a data-driven runner and three module beacons to the compact Core Deck. SCAN, COMMAND, and ROUTE switches now move a premium signal rail tied to the active module without mounting extra panels or adding vertical scroll.

Path Core Live Tokens adds small data-driven motion tokens to the Core rail. Blockers, proof, and active work now drift across the rail as readable status pips, giving the first Path viewport a stronger game-cockpit pulse without adding another section.

Compact Chapter Archive is the default Path Map archive mode: it shows horizontal level clusters first and opens the full selected-chapter dossier only after the local expand control, reducing first-pass scroll while preserving every deep history module.

Path Utility Dock is the default lower Path Map mode: it keeps Radar, Intel, Proof, Replay, Handoff, Notes, and Stream as horizontal dock modules and renders only the selected module panel, reducing scroll while keeping every existing lane-control surface reachable.

Path Cockpit Chrome removes the redundant lane detail header only in Path view. Mission Glance becomes the lane header for that screen, the detail tabs tighten, and the stage starts higher without losing Overview/Chronicle/Trail/Game/Comms navigation.

Path Route Focus changes direct Path-link focus to preserve an already-visible cockpit instead of forcing the Path board to the top of the viewport. This keeps the compact tabs, Mission Glance, Stage Ribbon, and Core Deck readable on first load and reduces jumpy page scrolling.

Path Utility Motion Director adds a data-driven motion rail to the dock: the active module sets a progress variable, runner position, and beacon state so tab switches read as a deliberate control-surface transition rather than a generic card fade.

Path Utility Dock is the default lower Path Map mode: it replaces the old vertical stack of blocker radar, node intel, proof cache, replay, handoff, notes, and event stream cards with a single selected console and horizontal module tabs. The dock keeps every module available while cutting the first-pass scroll cost and making each click feel like opening a deliberate control panel.

The Quest Cockpit appears at the top of each lane Overview. It condenses the lane into a game-style current-run panel with world, level, checkpoint, current gate, next move, recent event chain, and direct jumps into Path Map, Chronicle, Game, Comms, and Trail.

The Milestone Runway appears in each lane Overview after the Quest Cockpit. It reads the existing checkpoints, gates, outcomes, and trail records, then renders a horizontal route spine with checkpoint, gate, unlock, event, and future-slot nodes plus Path, Chronicle, and Trail jumps. Its local lens controls filter the same runway into All, Gates, Unlocks, Events, or Future views without mutating snapshot data. It introduces no new schema, so new lane records automatically extend the runway.

The Agent Party appears in each lane Overview after the Milestone Runway. It reads `snapshot.agents`, the selected lane binding, `snapshot.dispatchConsole.suggestions`, and browser-local staged drafts to show a compact party roster with portraits, readiness, gate pressure, thread id, and COM/Q/PATH actions. Q only stages a local draft; it does not contact an agent or send external messages.

The Minigame Forge appears in each lane Overview after the Agent Party. It reads the selected lane's `visual.minigame`, `MINIGAME_REGISTRY`, generated texture, and asset-vault records to show a lane-local blueprint for the current game module. The panel exposes the module type, stage count, asset coverage, extension files, and local GAME/ASSET/ARCADE jumps so future lanes can copy the setup path.

The Gate Radar appears in each lane Overview after the Minigame Forge. It reads `lane.gateMap`, `lane.serviceRequests`, promotion gates, and browser-local staged drafts to render blocker signals as radar pings, pressure stats, gate cards, and COM/Q/PATH actions. Its per-lane filter chips are browser-local preferences stored under `agent-company-atlas.gate-radar-filter.v1`; they classify signals as blocker, review, browser, account, payment, or public-action items without adding schema. Its browser-local operator notes are stored under `agent-company-atlas.gate-radar-notes.v1`, keyed by lane and signal id, and never mutate the snapshot. The Path Map reuses those local notes as route badges and note previews on matching gate nodes. Its realm skin is derived from lane identity fields such as id, department, realm, mood, and minigame id, then crops the generated `gate-radar-realm-skin-sheet-20260618.png` texture atlas into discovery, build, market, risk, revenue, or platform moods. Q only stages a local blocker-review draft.

The Signal Core reads the selected lane, current feed playback item, lane colors, map position, level, blockers, outcomes, and traces to drive the hero signal readout and ambient canvas field. It is purely presentational, honors reduced-motion preferences, and does not change snapshot data.

The Atlas Relay uses a generated system portal artwork as a command hub for the selected lane. It summarizes linked bots, watched gates, route events, and vault artifacts, then offers local jumps into Path Map, Comms, Mission Feed, and the Visual Asset Vault without starting any workers.

The Worlds Launch surface sits at the top of the Worlds deck as a compact level-select dock. It summarizes live worlds, realm spread, gate pressure, custom-game coverage, stage count, and future lane sockets, then exposes direct Loom, Arcade, Registry, Genesis, and Asset jumps plus priority lane buttons that open the deep Path Map. Its animated route-map layer and Lane Expansion Portal Deck render lightweight node links, active-node pulses, future minigame sockets, and route runners with reduced-motion fallbacks, all derived from generic lane/minigame/asset snapshot fields so forked agent-company repos can add lanes without redesigning the hub.

The World Loom uses a generated portal-hall backdrop as a cinematic lane selector. It renders nearby lane worlds as manual, non-autoplay cards with level, gate, unlock, avatar, and realm signals, then jumps into Path Map, Game, Comms, or the system Asset Vault.

The Arcade Deck reads every lane's minigame texture and registry hook to create a company-level game launcher. Each card shows the generated game art, module type, stage count, gate pressure, level progress, animated module stingers, and quick jumps into Game, Path Map, or the game-texture Asset Vault.

The Minigame Registry Codex uses the generated `minigame-registry-codex-20260618.png` texture to turn lane game modules into an expandable system catalog. It shows renderer coverage, texture readiness, stage/gate pressure, future module slots, and ARCADE/ASSET/FORGE actions so new lanes can get their own minigame identity without changing the snapshot schema.

The Motion Forge groups those animated stingers into a motion-language audit surface. It shows each reusable motion personality, which lanes use it, stage/gate pressure, live samples, reduced-motion coverage, and quick jumps back into Arcade Deck, Game, or the game-texture Asset Vault.

The Progression Constellation reads every lane's level, progress, blocker count, pending-review count, completed tasks, outcomes, traces, and registered minigame. It renders a company-level level ladder with clickable lane cards, derived tier labels, status callouts, avatar orbits, and responsive mobile scrolling so expanding lane counts do not flatten the first screen.

The Expansion Realms panel groups lanes into data-derived packs such as Build, Growth, Market, Revenue, Discovery, or a fallback custom department pack. Each pack summarizes levels, gates, outcomes, artifacts, custom minigame coverage, and clickable lane chips so larger agent-company repos can scan lane families without reading every individual path first.

The Expansion Forge turns those realm packs into future-lane blueprint cards. It summarizes live lanes, wired games, realm packs, open slots, minigame coverage, gate pressure, and asset requirements so a new repo can see what to add next before editing JSON.

The Lane Genesis Foundry uses the generated `lane-genesis-foundry-20260618.png` texture to turn future lane setup into a reusable launch pipeline. It connects Expansion Forge blueprints, lane art, minigame modules, bot sockets, proof trails, open slots, and direct FORGE/GAMES/ASSETS/BOTS jumps so larger agent-company repos can add new lanes without losing the game-like setup path.

The Creator Kit turns the extension checklist into a visible setup path. It shows the five build gates a forked repo needs: seed a lane, forge visual identity, wire a minigame, bind the bot, and ship the static template.

## Extension Points

- Add lane-specific minigames by assigning `lanes.<lane-id>.minigame.id` in `web/data/lane-visuals.json`, implementing a renderer in `web/app.js`, and registering it in `MINIGAME_REGISTRY`. Keep module notes and future extracted files under `web/games/`.
- Add a generated minigame texture to `lanes.<lane-id>.minigame.texture` so the Arcade Deck and Visual Asset Vault can expose the lane as a launchable game card.
- Add an Arcade Deck motion personality by extending `arcadeStingerType(lane)` and the matching `data-arcade-stinger` / Motion Forge CSS rules; keep stingers transform/opacity-only and covered by `prefers-reduced-motion`.
- Use the Creator Kit to find the core files for each setup gate and jump to the relevant Atlas surface for live examples.
- Use the Expansion Forge blueprint checklist to add a new lane family: lane visual, minigame id, generated texture, agent portrait, quest data, and Comms ownership.
- Use the Lane Genesis Foundry as the high-level lane launch board: each new path should gain a seed lane, generated art kit, minigame module, bot socket, and proof trail before it feels fully unlocked.
- Add generated lane avatars under `web/assets/lanes/` and lane-specific game textures under `web/assets/games/`.
- Add generated agent portraits under `web/assets/agents/` and map them in `web/data/agent-visuals.json`.
- Register source sheets, spare portraits, trophies, and shared surfaces in the Visual Asset Vault renderer when new global asset families are introduced.
- Update `web/data/lane-visuals.json` to assign each lane an avatar, realm, colors, mood, and minigame slot.
- Update `web/data/agent-visuals.json` to assign each bot an avatar, callsign, specialty, and accent.
- Extend the snapshot generator with new tables while preserving `schemaVersion`.
- Replace the static frontend later with React/Three.js without changing the snapshot shape.

## Minigame Registry

`web/app.js` exposes `MINIGAME_REGISTRY`, a local dispatch table that maps minigame ids to `{ render, count }` hooks. The renderer returns the lane game board; the counter tells the shared controls how many steps the board supports. This keeps new lane modules data-driven and avoids adding another hardcoded branch every time a path gets its own vibe. See `web/games/README.md` for the extension checklist.

## Lane Detail Views

- `Atlas Deck Dock` turns the page from one long scroll into six compact modes: Control, Worlds, Command, History, Library, and All. It keeps the standalone audit view available while defaulting to less scrolling and a more cockpit-like operator flow.
- `Atlas Teleport Rail` adds compact jump pads for Cockpit, Map, Bots, Feed, Worlds, and Assets. Desktop keeps it sticky under the deck switcher; mobile pins it as a bottom HUD so operators can move between major surfaces without dragging through the full atlas.
- `Deck Stage Compression` bounds each normal deck surface into an internal stage with stable scrollbars and snap points, while leaving the All deck as the full audit/export view. This reduces whole-page scrolling without hiding the expandable panels future operators may need.
- `Deck Stage Frame Glow` adds animated scanline/glow chrome to those bounded stages so the compressed panels feel like live game surfaces instead of plain scroll boxes.
- `Atlas Stage Focus` turns the teleport rail into a true stage selector. Cockpit, Map, Bots, Feed, Worlds, and Assets each reveal only their matching stage in normal decks, while All remains the full expandable audit stack.
- `Command Map Stage Solo` makes the Map teleport open a dedicated atlas board instead of the full cockpit grid, hiding the lane rail and detail panel while the map expands into a bounded game surface on desktop and mobile.
- `Command Map Solo Fill` makes that solo atlas board fit more like a level map: reset zoom fills the stage more aggressively, a subtle animated grid sits beneath the world, and routes gain extra glow so lane paths read as playable routes instead of tiny pins in empty space.
- `Command Map Overlay Dock` compresses the Map stage playback and lane-focus panels into HUD strips so the selected path context remains visible without covering the playable atlas board.
- `Command Bot Command Room` makes the Bots teleport open a focused bot-control stage: the support dock becomes a slim switcher, the bot command matrix gets the taller bounded surface, and bot status chips stay sticky while scanning commands.
- `Command Bot Card Deck` tightens the bot command cards inside that stage: smaller status chips and portraits, compact lane rows, hidden long ask/thread copy, and full-width command buttons so more bot controls fit in the first viewport.
- `Command Workspace First` makes the Command deck open with the active lane workspace before global relay, quest, crew, thread, and bot boards. At medium and small widths the detail panel leads the workspace before the lane list and map, so direct path links reach the selected lane and Path Map without a long command-page scroll.
- `Compact Mission Stage` makes the direct Command/Path entry behave like a bounded cockpit surface: the detail panel stays within the viewport, Mission Glance and Path Core Deck are tightened, and an animated signal layer gives the first screen a more active game-stage feel without mounting another dashboard stack.
- `Path Run Meter` adds a five-socket route/gate/proof/tasks/notes level strip inside Mission Glance, giving the top cockpit a clearer game HUD readout without adding scroll.
- `Path Crew Presence` shows the selected lane's mapped bot portraits, callsigns, readiness bars, and gated/ready/staged state directly inside Mission Glance so the operator sees the crew before opening deeper command panels.
- `Path Depth Pill` floats the Stage/Archive/Tools selector as a compact control in default Stage mode, reducing first-screen vertical weight while keeping deeper archive and utility views one click away.
- `Path Stage Ribbon` shows the first route levels, gates, unlocks, focused node, and future expansion slot directly under Mission Glance, reusing the existing path-node focus controls so milestones are visible before opening the deeper Route module.
- `Path Stage Focus Lens` overlays the Stage Ribbon with the focused level's type, title, and next meaning, making selected gates/checkpoints/unlocks understandable without opening a deeper route panel.
- `Path Stage Atmosphere` adds a procedural cockpit-wide bitmap texture behind the bounded Path board, making the first Path viewport feel more like a game level while keeping the asset repo-local and reusable.
- `Path Stage Signal Weather` turns blockers, proof, work, and notes into subtle cockpit particles, improving animation quality with stateful motion instead of decorative sweeps or extra scroll.
- `Path Stage Nav Dock` removes the duplicated Path-mode detail tab row and replaces it with a compact in-board HUD nav, reducing first-screen chrome while keeping fast jumps to overview, logs, trail, game, and comms.
- `Game Stage HUD` applies the same no-scroll cockpit discipline to minigames by hiding duplicated Game-mode page chrome and adding a compact arcade HUD with current-step context and working cross-view navigation.
- `Path Stage Motion Director` adds a compact scan layer, progress runner, and status-aware node sparks to the Path Stage Ribbon so gates, unlocks, and focused route nodes feel animated without mounting another panel or increasing first-screen scroll.
- `Path Stage HUD Strip` adds a generated bitmap route-stage texture behind the compact Path Stage Ribbon and registers it in the Visual Asset Vault, making direct Path views richer without adding another scroll section.
- `Path Stage Shell` makes direct Path view default to a bounded STAGE cockpit, with ARCHIVE and TOOLS as explicit depth modes so deep history and utility panels stop loading as first-pass scroll.
- `Path Cockpit Chrome` removes the redundant selected-lane header and stats only while Path is active, letting Mission Glance carry lane identity and moving the game stage closer to the top of the viewport.
- `Path Core Live Tokens` turns the Core rail into a compact live-status layer for blockers, proof, and active work, improving animation quality with meaningful motion rather than another decorative sweep.
- `Path Core Snapshot` replaces the default Core panel's cramped full module body with a compact route arc, signal cards, and fast actions, reducing internal scroll while keeping Scan/Command/Route choices in the first viewport.
- `Path Route Focus` stops direct Path links from forcing the stage to the very top when the cockpit is already visible, keeping navigation tabs and the stage in view with less jumpy scrolling.
- `Path Viewport Stage` removes redundant Path Map chrome from the direct Path view, tightens path-only detail padding, and lets Mission Glance, the Stage Ribbon, and the Core Deck start higher in the first viewport.
- `Path Split Stage` lays out Mission Glance and the Stage Ribbon beside the Core Deck on wide viewports, so the main route HUD and active module controls read as one game stage before the deeper archive and utility panels resume full width.
- `Compact Path Chrome` switches the Atlas masthead and deck dock into a dense cockpit header only while a lane Path view is active, cutting the first-screen vertical tax without removing the full brand treatment from broader overview decks.
- `Overview` opens with the Quest Cockpit, then shows lane identity, agent roles, gates, blockers, and recent tasks.
- `Quest Cockpit` turns each lane Overview into a compact game HUD for world, level, checkpoint, next move, current gate, recent event chain, and fast detail-tab jumps.
- `Milestone Runway` compresses checkpoint, gate, unlock, and event nodes into a scrollable lane route spine with future-slot space, local All/Gates/Unlocks/Events/Future lenses, and fast Path, Chronicle, and Trail jumps.
- `Agent Party` turns the selected lane's bound bots into portrait cards with readiness, gate pressure, top ask, thread id, and local COM/Q/PATH actions.
- `Minigame Forge` turns the selected lane's minigame id, texture, renderer hook, asset records, and extension files into a reusable blueprint card with GAME/ASSET/ARCADE jumps.
- `Gate Radar` turns the selected lane's blockers, service requests, and fallback promotion gates into filtered radar pings, pressure stats, realm-skinned scope art, local operator notes, sigil-backed gate cards, and local COM/Q/PATH actions.
- `Path Map` turns quest checkpoints, blockers, outcomes, local Gate Radar notes, owner bot context, and trail events into a compact horizontal route board with a shared route spine, animated runner, focused-node socket, compact animated Mission Scan, Path Command Strip for next move/gate/proof/bot/notes and route/proof/archive/queue/comms jumps, clickable nodes, a generated-art Compact Chapter Archive grouped by trail date with horizontal level clusters and an explicit selected-chapter dossier expansion, a generated-art Chapter Depth Rings orbit board for proof/gate/task/trace density and hidden lens depth, a generated-art Chapter Milestone Ladder for proof/gate/task/unlock/next rungs, a generated-art Chapter Game Portal for lane minigame identity and GAME/FORGE/TRAIL jumps, a generated-art Chapter Questline with a pulse trail for spawn/proof/gate/task/unlock/next-move stage scanning, a Chapter Spoils medal shelf for proof/unlock/gate/service/task/trace rewards, a Chapter Evidence Vault for deduped chapter artifact previews, proof records, and outcome packets, a generated-art Chapter Crew Formation board inside Chapter Crew Relay for bot ownership, portrait slots, readiness meters, thread context, chapter pressure, and local COM/Q handoff, a generated-art Path Chapter Command Relay console inside Chapter Command Log for suggested drafts, staged outbox items, browser-local operator history, selected-chapter context, and local Q/COM/TRAIL actions, a Chapter Gate Stack with a generated-art Chapter Gate Heatfield scan for lane gate-map signals, service-request gates, local Gate Radar notes, chapter gate counts, and blocker-review Q/COM actions, a Chapter Task Board for selected-chapter task records, lane recent tasks, owner, priority, status, and next action, a Chapter Runway sequence rail for the active record lens, and a Path Utility Dock that switches between Node Intel, Proof Cache, Route Replay, Route Handoff, note pins, blocker radar, and event stream without mounting the whole lower stack at once.
- `Chronicle` turns each lane's checkpoints, trail records, blocker gates, event mix, latest milestone, and next action into a reusable quest-board view. It uses the same expandable trail limit as `Trail`, so large lanes can keep revealing more history without a new schema.
- `Path Memory Codex` turns each lane Trail into a generated-art expandable memory archive with All/Gates/Proof/Wins/Tasks/Traces lenses, event cards that drill into Path Map proof/replay focus, future sockets, and a MORE action that reveals deeper raw trail records.
- `Trophy Room` turns completed outcomes into a reusable unlocked-achievement wall with lane-art trophies, tier/lane filters, a snapshot unlock toast, a new-unlock pulse, and lane progress tracks.
- `Visual Asset Vault` turns generated lane art, minigame textures, bot portraits, the Operator Identity Bay texture, and source sheets into a filterable collection with lane drill-through.
- `Company Quest Board` turns all lane tasks, blockers, outcomes, dispatch suggestions, and staged drafts into a generated-art global mission board with pressure-ranked lane cards and TASKS/GATES/WINS feed lenses.
- `Signal Core` turns selected lane and playback state into a live hero readout plus a data-reactive ambient motion field.
- `Live Ops Pulse` turns latest movement, blocker gates, active tasks, bot asks, staged drafts, and lane pulse into a generated-art first-screen current-state board with LATEST/GATES/COMMS/TIMELINE jumps.
- `Atlas Relay` turns the selected lane into a generated command-hub scene with quick jumps to Path, Comms, Mission Feed, and system assets.
- `Worlds Launch` turns the Worlds deck into a compact level-select dock with live stats, module jumps, an animated route-map layer, a generated Lane Expansion Portal Deck for future minigame sockets, and priority lane buttons that open the deep Path Map.
- `Command Cockpit Event Lens` turns recent Quest-map trail packets into selectable in-board explainers for what happened without adding another report row.
- `Command Cockpit Event Pulse` adds a procedural route-pulse texture and data-bound recent-event packets to the Quest level map without increasing the cockpit height.
- `Command Cockpit Node Halos` turns Quest level-map cells into medal sockets for proof, gates, trail, score, crew, and next-move state using reusable lane counts.
- `Command Cockpit Unlock Pulse` turns progress, gate pressure, and proof volume into an in-board pulse layer that makes checkpoint momentum visible without adding another panel.
- `Command Cockpit Crew Relay` turns the selected Quest node lens into a bot handoff chip with avatar, callsign, readiness, and a compact COM jump driven by reusable Agent Party data.
- `Command Cockpit Focus Beam` turns selected Quest level-map nodes into a moving in-board reticle using computed focus-position variables and a generated cockpit beam texture.
- `Command Cockpit Insight Ribbon` turns clicked Quest level-map nodes into compact milestone, blocker, bot, proof, and next-move HUD chips inside the existing board instead of adding another scroll section.
- `World Loom` turns the selected lane neighborhood into a cinematic generated-art lane selector with manual previous/next controls and Path/Game/Comms/Asset jumps.
- `Arcade Deck` turns the lane minigame registry into a textured launcher shelf with Play, Path, Asset jumps, and lightweight animated stingers for every module-ready lane.
- `Minigame Registry Codex` turns lane visual minigame records, texture assets, and `MINIGAME_REGISTRY` hooks into a generated-art module catalog with renderer/stage/gate stats, future slots, and Arcade/Asset/Forge jumps.
- `Motion Forge` turns the stinger registry into a reusable animation audit board with live samples, lane chips, gate/stage counts, and Arcade/Game/Asset jumps.
- `Progression Constellation` turns every lane into a clickable level card with derived gate/reward/scout status, company-level stats, and a responsive scroll rail for future lane growth.
- `Expansion Realms` groups lanes into scalable game-like packs with avatar clusters, pack meters, lane chips, and active-state sync for future company growth.
- `Expansion Forge` shows reusable lane-family blueprints, open slot counts, minigame coverage, asset requirements, and nearest existing-lane references for future expansion.
- `Lane Genesis Foundry` turns those expansion blueprints into a generated-art setup board for lane seeds, art kits, minigame modules, bot sockets, proof paths, open slots, and fast jumps to Forge, Games, Assets, and Bots.
- `Creator Kit` turns the repo setup path into five build gates with file targets, unlock descriptions, and jumps to Forge, Asset Vault, Path Map, Comms, and Mission Feed.
- `Trail` uses `lane.trail` from the snapshot and opens with the generated `Path Memory Codex`, then reveals raw records in chunks so high-activity lanes can keep expanding without overwhelming the first view.
- `Mission Feed` aggregates recent records from every lane trail into a filterable company-wide stream.
- `Company Chronicle Spine` turns the active Mission Feed lens into generated-art global history chapters with event-kind counts, lane drill-through, and LATEST/PROOF/GATES feed actions.
- `Experiment Discovery Lab` turns the active Mission Feed lens into a generated-art lab board for tested paths, proof captures, gates, wins, and future experiment slots.
- `Mission Feed Playback` saves local feed lenses, replays the current filtered timeline, lights up the source lane on the map, renders the current event as a scene card, and preserves source-lane drilldown.
- `Dispatch Console` stages local bot command drafts in a browser-only outbox, builds grouped command batches, keeps a browser-local operator history, and links each staged command back to the lane Comms deck.
- `Command Relay Deck` centralizes bot sends, staged drafts, blocker gates, thread ownership, and local operator history into a generated-art relay board with COM/Q/MATRIX actions and expansion sockets.
- `Company Quest Board` gives the operator a global task/blocker/win board with generated art, pressure-ranked lane cards, lane drill-through, and Mission Feed lenses for tasks, gates, and outcomes.
- `Crew Bridge` gives operators a fast squad-readiness layer across bots, lanes, gates, urgency, and staged command drafts.
- `Agent Sprite Foundry` turns agent portraits, callsigns, specialties, threads, lane bindings, staged asks, and future slots into a generated-art character/sprite readiness board with COM/ASSET/FORGE actions.
- `Agent Constellation Bay` upgrades the Agent Sprite Foundry with a generated cockpit constellation texture and live bot beacons that can quick-select lane-bound agents.
- `Thread Nexus` shows bot-to-lane ownership as a command network with active links, gated/staged thread states, top asks, and quick COM/PATH/Q controls.
- `Bot Command Matrix` gives each active bot a command-center card with its lane state, pressure meter, thread id, suggested send, Comms jump, and local queue action.
- `Game` uses `lane.quest.checkpoints` to render a reusable checkpoint module when a lane-specific module is not implemented yet.
- `Comms` turns lane owners, thread IDs, gates, next actions, and promotion command previews into a local operator command deck with a generated-art Comms Command Room for owner portrait, lane status, staged queue, local history, blocker pressure, urgency, thread context, Q/C/PATH actions, roster, brief packet, and local command draft. It copies drafts only; it does not send messages or start workers.
- Comms rosters prefer each agent's generated portrait and callsign from `agent-visuals.json`, falling back to lane art for unmapped future agents.
- The global Operator Roster opens with the generated-art Operator Identity Bay for active bot counts, portrait coverage, lane bindings, staged asks, spare expansion slots, a portrait strip, and COM/ASSET/FORGE jumps, then shows all active bots with generated portraits, lane assignment, status, level, and next-action preview.
- `ai_ml_competitions` uses the custom `baseline-climb` minigame renderer and a generated benchmark-arena texture.
- `lead_generation_and_sales` uses the custom `offer-route` minigame renderer and a generated deal-room texture.
- `local_trading_strategy_research` uses the custom `paper-trial` minigame renderer and a generated quant-range texture.
- `money_source_discovery` uses the custom `venue-mapper` minigame renderer and a generated source-cartography texture.
- `paid_code_bounties` uses the custom `claim-scout` minigame renderer and a generated bounty-forge texture.
- `platform_engineering` uses the custom `systems-grid` minigame renderer and a generated control-tower texture.
- `prediction_market_research` uses the custom `settlement-replay` minigame renderer and a generated market-observatory texture.
- `security_bounty_private_reports` uses the custom `scope-run` minigame renderer and a generated scope-citadel texture.
- `submitted_bounty_payouts` uses the custom `payout-vault` minigame renderer and a generated revenue-vault texture.
- `web3_airdrops_grants_hackathons` uses the custom `grant-expedition` minigame renderer and a generated portal-map texture.
- `content_and_social_growth` uses the custom `signal-harvest` minigame renderer and a generated signal-garden texture.
- `digital_products_templates_plugins` uses the custom `foundry-run` minigame renderer and a generated foundry texture.

Deep links use hash routing:

```text
http://localhost:5177/#lane=paid_code_bounties&view=game
http://localhost:5177/#lane=digital_products_templates_plugins&view=comms
http://localhost:5177/#lane=money_source_discovery&view=path
http://localhost:5177/#lane=platform_engineering&view=chronicle
http://localhost:5177/#lane=platform_engineering&view=trail
```

## Current Visual Assets

- `web/assets/mission-map-bg.png` - generated atlas background.
- `web/assets/system/relay-portal-20260617.png` - generated Atlas Relay command-hub background.
- `web/assets/system/world-loom-portal-20260618.png` - generated World Loom portal-hall background.
- `web/assets/system/comms-command-room-20260618.png` - generated bot command-room texture used by the lane Comms view and Visual Asset Vault.
- `web/assets/system/operator-identity-bay-20260618.png` - generated portrait-bay texture used by the global Operator Roster and Visual Asset Vault.
- `web/assets/system/agent-sprite-foundry-20260618.png` - generated character/sprite pipeline texture used by the Agent Sprite Foundry and Visual Asset Vault.
- `web/assets/system/agent-constellation-bay-20260619.png` - generated bot-constellation cockpit texture used by the Agent Sprite Foundry live beacon layer and Visual Asset Vault.
- `web/assets/system/live-ops-pulse-20260618.png` - generated live-operations texture used by the first-screen Live Ops Pulse and Visual Asset Vault.
- `web/assets/system/command-relay-deck-20260618.png` - generated global command-relay texture used by the Command Relay Deck and Visual Asset Vault.
- `web/assets/system/company-quest-board-20260618.png` - generated global mission-board texture used by the Company Quest Board and Visual Asset Vault.
- `web/assets/system/company-chronicle-spine-20260618.png` - generated global timeline texture used by the Company Chronicle Spine and Visual Asset Vault.
- `web/assets/system/experiment-discovery-lab-20260618.png` - generated global test/proof lab texture used by the Experiment Discovery Lab and Visual Asset Vault.
- `web/assets/system/command-cockpit-event-pulse-20260619.png` - procedural route-pulse texture used by the Command Cockpit Quest level map and Visual Asset Vault.
- `web/assets/system/command-cockpit-node-halos-20260619.png` - generated node-medal texture used by the Command Cockpit Quest level map and Visual Asset Vault.
- `web/assets/system/command-cockpit-crew-relay-20260619.png` - generated bot relay texture used by the Command Cockpit Quest focus lens and Visual Asset Vault.
- `web/assets/system/command-cockpit-focus-beam-20260619.png` - generated selected-node reticle texture used by the Command Cockpit Quest level map and Visual Asset Vault.
- `web/assets/system/command-cockpit-insight-ribbon-20260619.png` - generated focused-node HUD strip used by the Command Cockpit Quest level map and Visual Asset Vault.
- `web/assets/system/lane-expansion-portal-deck-20260619.png` - generated compact lane/minigame socket texture used by Worlds Launch and Visual Asset Vault.
- `web/assets/system/lane-genesis-foundry-20260618.png` - generated lane setup texture used by the Lane Genesis Foundry and Visual Asset Vault.
- `web/assets/system/minigame-registry-codex-20260618.png` - generated module-catalog texture used by the Minigame Registry Codex and Visual Asset Vault.
- `web/assets/system/gate-radar-sigil-sheet-20260618.png` - generated Gate Radar glyph sheet for blocker, review, browser, account, payment, and public-action signals.
- `web/assets/system/gate-radar-realm-skin-sheet-20260618.png` - generated Gate Radar texture atlas for discovery, build, market, risk, revenue, and platform lane-family skins.
- `web/assets/system/path-stage-hud-strip-20260618.png` - generated compact route-stage HUD strip used by the Path Stage Ribbon and Visual Asset Vault.
- `web/assets/system/path-stage-playfield-rail-20260620.png` - generated holographic level-map texture used by the compact Path Stage route rail and Visual Asset Vault.
- `web/assets/system/path-run-meter-hud-20260618.png` - generated Mission Glance level-strip HUD texture used by the Path Run Meter and Visual Asset Vault.
- `web/assets/system/path-handoff-beacon-20260618.png` - generated command-transfer beacon used by the Path Map Route Handoff card and Visual Asset Vault.
- `web/assets/system/path-memory-codex-20260618.png` - generated expandable lane-history texture used by the Trail Path Memory Codex and Visual Asset Vault.
- `web/assets/system/path-chapter-archive-20260618.png` - generated mission-journal archive console used by the Path Map Chapter Archive and Visual Asset Vault.
- `web/assets/system/path-chapter-depth-rings-20260618.png` - generated concentric history-ring texture used by the selected Path Map chapter's Chapter Depth Rings.
- `web/assets/system/path-chapter-milestone-ladder-20260618.png` - generated unlock-ladder texture used by the selected Path Map chapter's Chapter Milestone Ladder and Visual Asset Vault.
- `web/assets/system/path-chapter-game-portal-20260618.png` - generated chapter-to-minigame portal texture used by the Path Map Chapter Game Portal and Visual Asset Vault.
- `web/assets/system/path-chapter-command-relay-20260618.png` - generated bot handoff relay texture used by the Path Map Chapter Command Log and Visual Asset Vault.
- `web/assets/system/path-chapter-questline-20260618.png` - generated six-beacon run-map HUD texture used by the Path Map Chapter Questline and Visual Asset Vault.
- `web/assets/system/path-chapter-spoils-20260618.png` - generated 3x2 achievement medallion sheet used by the Path Map Chapter Spoils shelf and Visual Asset Vault.
- `web/assets/system/path-chapter-gate-heatfield-20260618.png` - generated tactical blocker-radar texture used by the Path Map Chapter Gate Heatfield and Visual Asset Vault.
- `web/assets/system/route-replay-chronometer-20260618.png` - generated timeline chronometer texture used by the Path Map Route Replay card and Visual Asset Vault.
- `web/assets/system/route-replay-event-glyph-sheet-20260618.png` - generated 3x2 event glyph sprite sheet used by Route Replay, Event Proof, Path Map mini-events, and Visual Asset Vault.
- `web/assets/lanes/operator-avatar-sheet-20260616.png` - generated 12-operator source sheet.
- `web/assets/lanes/<lane-id>.png` - cropped 512px lane avatars used by the UI.
- `web/assets/games/baseline-climb-bg-20260617.png` - generated benchmark-arena texture for the Baseline Climb module.
- `web/assets/games/claim-scout-bg-20260617.png` - generated bounty-forge texture for the Claim Scout module.
- `web/assets/games/foundry-run-bg-20260616.png` - generated digital-product foundry texture for the Foundry Run module.
- `web/assets/games/grant-expedition-bg-20260617.png` - generated portal-map texture for the Grant Expedition module.
- `web/assets/games/offer-route-bg-20260617.png` - generated deal-room texture for the Offer Route module.
- `web/assets/games/paper-trial-bg-20260617.png` - generated quant-range texture for the Paper Trial module.
- `web/assets/games/payout-vault-bg-20260617.png` - generated revenue-vault texture for the Payout Vault module.
- `web/assets/games/settlement-replay-bg-20260617.png` - generated market-observatory texture for the Settlement Replay module.
- `web/assets/games/scope-run-bg-20260617.png` - generated scope-citadel texture for the Scope Run module.
- `web/assets/games/signal-harvest-bg-20260617.png` - generated signal-garden texture for the Signal Harvest module.
- `web/assets/games/systems-grid-bg-20260617.png` - generated control-tower texture for the Systems Grid module.
- `web/assets/games/venue-mapper-bg-20260617.png` - generated source-cartography texture for the Venue Mapper module.
- `web/assets/trophies/trophy-medal-sheet-20260617.png` - generated 2x2 Trophy Room medal sheet for mythic, gold, silver, and bronze tiers.
- `web/assets/agents/agent-avatar-sheet-20260616.png` - generated 12-agent source sheet.
- `web/assets/agents/<agent-id>.png` - cropped agent portraits used by Comms rosters.
- `web/assets/agents/spare-agent-operator-20260616.png` - reserved expansion portrait for the next registered agent.
- `web/assets/system/chapter-crew-formation-20260618.png` - generated Chapter Crew Formation backdrop used by the selected Path Map chapter's bot roster.
- Command Cockpit Mission Director - cockpit overlay that keeps one obvious current objective visible above the level-map board.
- Command Cockpit Command Socket - fourth Mission Director chip that stages the best lane dispatch from the cockpit so bot communication is actionable without leaving Overview.
- Command Cockpit Relay Braid - local-only bot relay strip inside Mission Director with target, queue/history state, thread hint, and COM/Q/COPY actions.
- Command Cockpit Crew Presence Dock - compact in-map bot party HUD that uses lane agent visuals and opens Comms without adding another scrolling panel.
- Command Cockpit Unlock Ladder Strip - compact in-map checkpoint ladder that shows cleared levels, current gate/next unlock, and win count while opening Path without adding scroll.
- Command Cockpit Signal Convoy - data-driven event streak layer that makes proof, gates, wins, and live work visibly travel through the quest map without adding layout height.
- Command Cockpit Quest Camera Rail - animated in-board milestone, blocker, proof, bot, and next-move blips behind the Quest level map without extra scroll height.
- Command Cockpit Route Capsule - compact world, level, checkpoint, gate, and next nodes path overlay for reading unlock progression inside the board.
- Command Cockpit Lane Constellation - active lane and neighboring money paths kept as compact in-board selectors.
- Command Cockpit Mission Stack - Timeline, Blocker, Proof, and Next staged inside the Quest board as a compact selected-node control.
- Command Cockpit Mission Dossier - keeps the active Timeline, Blocker, Proof, or Next lens visible inside the Quest board with compact dossier cards.
- Command Cockpit Level Reel - World, Level, Checkpoint, Gate, and Next unlock strip inside the Quest board using existing node focus.
- Command Cockpit Unlock Pulse - progress, gate pressure, and proof volume rendered as compact in-board feedback beside the Level Reel.
- Command Cockpit Focus Director - selected mission camera is promoted while secondary telemetry recedes so the board reads as one calmer game surface.
- Command Cockpit Lane Gate Selector - many money paths collapse into ranked active and reserve gate buttons without losing direct lane access.
- Command Cockpit Lane Expansion Slots - compact future money paths sit inside the lane gate rail as reserved unlock cells for paths, bots, minigames, and research gates.
- Command Cockpit Lane Expansion Mobile Dock - the first mobile rail keeps a four-cell future-slot dock visible while the lane buttons remain horizontally scannable.
- World Seed Cartridge Rail - compact no-wrap Worlds Launch cartridges that show current lane minigames beside future New World, Bot Pod, Mini Game, and Research Gate sockets.
- Worlds Launch Low-Scroll Console - compressed focus, stat, seed, and expansion socket rails so the world selector reads as one game screen instead of a tall stack.
- Path Glance Command Console - compresses the clicked-path mission glance into one command band with a no-wrap signal rail and compact route/proof/archive/comms actions.
- Path Core Compact Control Deck - prevents the hidden stage-mode core panel from reserving tall empty space, leaving the floating depth pill independent while the core controls hug their content.
- Command Cockpit Path Depth Lens - selected path depth collapses happened/blocker/proof/next state into one in-board HUD strip instead of another scrolling report.
- Path Stage Chapter Radar - compact in-board chapter levels for the Path stage so history, proofs, gates, and older records are visible before opening the deeper archive.
- Path Stage Quest Scanner - compact core-deck scanner that keeps happened, blocker, proof, and next-move state visible inside the clicked-path stage without adding another scroll section.
- Path Stage Bot Relay Capsule - embeds the lane owner, thread hint, staged state, and local Q/COM controls into the clicked-path scanner so bot communication is visible without sending anything automatically or adding scroll.
- Path Stage Experiment Fork Signal - adds a Tests scanner cell derived from active tasks, recent tasks, trail task events, and lane minigame metadata so each clicked path exposes what is being tried and what future fork sockets can inherit.
- Path Stage Kinetic Field - upgrades the shared canvas particle field in Path mode with data-reactive gate, proof, test, and unlock ribbons plus moving signal packets, giving clicked paths richer premium motion without adding scroll or schema fields.
- Path Stage Game Board Compact - path mode now prioritizes one playable map surface, hides duplicate header chrome, demotes chapter/depth controls, and keeps scanner details in a slim cockpit strip so clicked paths feel less like stacked reports.
- Path Stage Unlock Cards - route levels now render as game-like unlock cards with framed charge fill, status badges, and gated/unlocked/future meter states instead of empty stretched tiles.
- Path Stage Depth HUD - mobile Path mode turns the Stage/Archive/Tools switcher into a slim board row instead of an overlay, keeping route cards readable and reducing the cramped scrolling feel.
- Path Stage Mobile Fit - mobile Path mode tightens the board, route, and unlock-card proportions so the clicked-path level map lands closer to one viewport instead of a tall stacked page.
- Path Stage Playfield Rail - route levels now sit on a centered traversal rail with compact staggered tokens, state glow, and snap scrolling, reducing the oversized-card feel while preserving the unlock map.
- Path Stage Playfield Texture - adds a generated holographic level-map backdrop to the compact route rail and registers it in the Visual Asset Vault as reusable system art.
- Path Stage Crew Sprites - places existing lane bot avatars as tiny readiness beacons on the clicked-path route playfield so the level map feels staffed without adding scroll or new schema fields.
- Path Stage Progress Badges - route tokens now expose compact gate, test, win, done, spawn, and next chips so blockers, experiments, achievements, and future sockets read at a glance.
- Path Stage Run Pulse - the clicked-path route board now projects a progress-tied glow and runner beacon through the playfield so the active money path reads as a live run without adding markup or scroll.
- Path Stage Event Echoes - route tokens now pulse tiny related trail-event echoes for proofs, blockers, requests, tasks, and outcomes while tightening the stage frame for a lower-scroll game surface.
- Path Stage Mobile Board First - phone path mode collapses the overview holo-board, objective beacon row, and bot dock so the clicked path level board owns the viewport sooner.
- Path Stage Mobile Route First HUD - phone path mode turns the mission glance into a compact overlay so the route playfield claims the first board row instead of starting below another report block.
- Path Stage Focus Drill - the focused level lens now shows compact related trail-event chips so each selected route node exposes happened/proof/gate/task context without opening another panel.
- Path Stage Expansion Sockets - route playfield now shows compact gate/test/proof/next sockets so each clicked path reads as expandable future forks without adding scroll.
- Path Stage Gate Encounter - focused blocker/gate levels now get a warning sweep, lock line, and stronger focused-node aura so current blockers read like compact boss encounters inside the route board.
- Path Stage Encounter Tether - the route board now projects a state-derived camera beam from the focused level coordinate into the encounter lens, making blockers feel spatially connected without adding a new panel or scroll.
- Path Stage Bot Command Beacon - the clicked-path board now promotes the lane owner bot into a compact avatar/readiness/Q/COM beacon beside the encounter so operators can see and contact the responsible bot without leaving the game surface.
- Path Stage Mobile Icon Nav - phone path mode turns the six text-heavy map navigation buttons into a compact dot strip so the board reads cleaner and less scroll-report-like.
- Path Stage Mobile Crest Rail - phone path mode compresses the global Atlas deck switcher into six small command crest cells so the clicked-path board starts sooner and the first screen feels more like a game surface than a stacked dashboard.
- Path Stage Mobile Shell Collapse - phone path mode now lets the command workspace shrink to the actual clicked-path board height, removing the leftover dashboard band below the playfield without affecting other decks.
- Path Stage Mobile Depth Pips - phone path mode turns the Stage/Archive/Tools depth switcher into a compact three-pip game control with hidden long notes, active-mode glow, and a thin scan rail.
- Path Stage Mobile Board Fill - phone path mode lets the clicked-path board claim more safe viewport height above the reward ticker, making the playfield feel larger without restoring page scroll.
- Path Stage Mobile Title Channel - phone path mode reserves a clean title lane beside the route HUD so the clicked-path objective truncates before the nav meter instead of colliding with it.
- Command Cockpit Premium Motion Governor - one premium game board owns the cockpit while duplicate rows vanish and animation timing becomes slower and calmer.
- Command Cockpit Mission Readout - compact in-board quest, focus, gate, and next-move telemetry without adding scroll.
- Command Cockpit Unlock Trail - ambient level progress beam and unlock nodes make level progress readable inside the board.
- Command Cockpit Board Bot Badge - lane owner directly inside the Quest board with avatar, readiness, role, and COM jump.
- Command Cockpit Board Atmosphere - data-driven texture and motion layer that uses progress, gate pressure, proof volume, and focus state to make the board feel alive without stealing clicks.
- Command Cockpit Boss Board - compact hero/director top HUD plus enlarged animated Quest map that removes leftover report rows without adding scroll height.
- Command Cockpit Icon Command Dock - icon-first CSS-drawn map/log/game/comms/trail controls for the boss-board action row.
- Command Cockpit Arcade Board Fit - stronger first-screen board lighting plus a mobile in-board icon dock that reclaims dead glass without adding scroll.
- Command Cockpit Mobile Immersive Stack - tighter phone chrome so the lane board starts earlier and behaves more like the main game surface.
- Command Cockpit Node Drill Stack - selected-node focus/milestone/blocker/trail/next/proof cards inside the Quest board without adding page height.
- Command Cockpit Run Spine - clickable Proof/Gate/Next nodes embedded in the quest map so each lane shows what has been proven, what is blocking progress, and what move is queued.
- Command Cockpit Realm Skin Cartridge - in-map lane identity chip powered by `lane.visual.minigame`, showing each path's custom minigame, texture, and game route without adding scroll.
- Command Cockpit Realm Mood Layer - selected paths project different game worlds inside the Quest board from reusable lane visuals, minigame metadata, gate pressure, and unlock charge.
- Command Cockpit Lane World Signal - lane rail world chips powered by each minigame definition so current and future lane slots read as playable worlds.
- Command Cockpit Lane Unlock Lens - cockpit-only lane-card chip showing GAME/SEED state, stage count, gate pressure, and readiness fill for expandable money-path worlds.
- Command Bot Squadron HUD - compact avatar cluster and readiness cockpit for Bots stage command coverage, gates, staged asks, and future bot identity expansion.

- Command Bot Switchboard - the Bots stage now groups operators into Ready, Gated, Staged, and Watching lanes with compact avatar handoff buttons before the longer bot card rail, making crew state scannable without more scrolling.
- Command Bot Viewport Board - Bots mode now locks into one viewport-height control board, keeps the archive dock thin, and moves the long roster into an internal rail so crew state feels like a playable command room instead of a page scroll.
- Command Bot Low-Scroll Squadron Board - denser bot roster cards and tighter grid rhythm so the Bots stage reads as a command crew board instead of a long scroll report.
- Command Cockpit Mobile Run Board - mobile cockpit pass that pins lane rail, Mission Director, level map, run spine, and action buttons into one playable board instead of a long page.
- Mobile World Chip Lane Rail - phone cockpit lane rail now uses each lane's minigame world chip, world number, and progress underline so current and future lanes read as compact playable worlds instead of clipped text tabs.
- Command Cockpit Mobile Board Viewport - phone overview now gives the active quest board a real bounded viewport, hides duplicate stage chrome, and prevents the board from collapsing into clipped overflow.
- Command Cockpit Mobile Toast Ticker - phone overview compresses new achievement feedback into a slim reward ticker so it celebrates progress without covering the command board.
- Command Cockpit Primary Readout - current move, gate pressure, and quest progress now form one stronger in-board command band while the lower depth lens recedes into supporting context.

- Command Cockpit Mission Control Band - compact first-screen HUD inside the premium quest field, consolidating level progress, latest discovery, blocker state, next move, and bot handoff into one actionable band while older identity/readout overlays recede.
- Command Cockpit Focus Target - selected Quest nodes now read as the playable target, with quiet ambient pips around them and a lower selected-node command card that no longer hides under the readout.
- Command Cockpit Mobile Context HUD - phone overview now shows one selected-node command card, one focused target, and one small progress rail; secondary depth, mission-stack, and cinematic plates recede so the first screen feels less like stacked reports.
- Command Cockpit Mobile Arcade Shell - phone overview compresses the brand row, deck dock, and lane selector into arcade chrome so the playable Quest board starts earlier and owns more of the first viewport.
- Command Cockpit Mobile Objective Bar - the phone Quest board now turns the Mission Director into a slim objective bar and trims selected-node card microcopy so the first board reads more like a game objective than a report header.
- Command Cockpit Premium Route Motion - the Quest board now has scoped route-energy, runner drift, and focused-node sweep animations so the live money-path surface feels more like a premium game board without adding scroll.
- Command Cockpit Mobile Reward Medal Dock - phone achievement feedback now collapses into a small medal dock on the command overview so rewards stay visible without owning the board or reintroducing scroll pressure.
- Command Cockpit Mobile Board Clarity - phone Quest boards now remove the duplicate mission-readout text slab and turn the top score strip into quiet pips so the playable route and focused node carry the screen.
- Command Cockpit Mobile Controller Dock - the phone Quest board now hides the duplicate secondary action row and promotes the level reel into a centered icon controller dock, keeping controls playable without reading as another labeled dashboard strip.
- Command Cockpit Mobile Node Cartridge - the selected-node lens now behaves like a compact game pickup on phones, keeping the node label and OPEN action while removing the extra report subtitle.
- Command Cockpit Mobile Cinematic Focus - phone cockpit playfields now convert noisy depth, route, and event text into compact atmospheric signals so the route board reads more like a game screen than a report stack.
- Command Cockpit Desktop Cinematic Route Focus - desktop cockpit boards now demote duplicate route, insight, depth, and echo labels into low-noise signal pips while keeping the mission readout and selected-node OPEN cartridge readable.
- Command Cockpit Selected Node Bot Handoff - the selected-node cartridge now carries a compact owner bot chip with avatar, readiness, callsign, and a direct COM jump so the cleaner cockpit still answers who to talk to next.

- Path Stage Mobile Story Rail - phone path mode restores happened/blocker/proof/next as a compact in-board story HUD while hiding long scanner copy, keeping the clicked path readable without adding scroll.
- Path Stage Mobile Level Tokens - phone path mode reshapes route cards into compact arcade level tokens with one strong level number, one short title, quieter status pips, and a calmer spotlight pass through the playfield.
- Worlds Mobile Portal Dock - phone Worlds mode compresses seed cartridges and expansion sockets into an icon-first portal dock so future lane slots read as unlockable minigame worlds without adding scroll.
- Asset Vault Inventory Board - Library/Assets now compacts the bot roster into a party strip and turns the generated art database into a bounded inventory board with desktop internal scroll and a two-row mobile collection dock.
- Reward Pickup Dock - Library/Assets now turns achievement notifications into a compact party-strip pickup dock, reserving roster space and keeping the generated asset grid clear on desktop and mobile.
- Worlds Reward Pickup Dock - Worlds Launch now uses a compact top-corner achievement pickup so reward feedback no longer covers the world selector, seed modules, expansion sockets, or lane cards.
- Command Cockpit Lane Arcade Rail - the command cockpit lane selector now behaves like a compact horizontal launch rail with active sweep, reserve cells, and future-slot sockets so the first screen feels more like a game board and less like a scroll list.
- Command Cockpit Mobile Lane Arcade Readability - the phone lane rail now uses readable avatar chips with LIVE/rank cues instead of a blank label plaque, keeping the board compact while making lane switching feel intentional.
- Path Stage Infinite Depth Stack - clicked-path mode now projects happened, blocker, tests, proof, and next-move layers as a compact in-board HUD so the path feels like expandable levels instead of another scrolling report.
- Path Stage Desktop Scanner Collapse - desktop Stage mode now lets the compact depth stack replace the bulky duplicate scanner deck, making clicked paths feel more like one playable board and less like side-by-side reports.
- Path Stage Desktop Objective Bar - desktop clicked-path mode now compresses the mission glance into a slim objective bar, removing the extra report rows so the level board and depth HUD carry the screen.
- Path Stage Realm Cartridge - clicked-path mode now shows a compact texture-backed GAME/SEED cartridge from each lane minigame, making every path feel like its own expandable world without adding scroll.
