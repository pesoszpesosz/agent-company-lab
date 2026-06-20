const state = {
  snapshot: null,
  activeAtlasDeck: "control",
  activeAtlasStage: "control",
  commandArchivePanel: "relay",
  selectedLaneId: null,
  filter: "all",
  feedFilter: "all",
  savedFeedViews: [],
  feedPlaybackIndex: 0,
  feedPlaying: false,
  feedPlaybackTimer: null,
  trophyTierFilter: "all",
  trophyLaneFilter: "all",
  assetFilter: "all",
  gateRadarFilterByLane: {},
  gateRadarNotesByLane: {},
  gateRadarNoteFocusByLane: {},
  unlockToast: null,
  unlockToastHold: false,
  unlockToastTimer: null,
  hoveredLaneId: null,
  stagedDispatches: [],
  dispatchHistory: [],
  detailView: "overview",
  overviewStageViewByLane: {},
  questNodeFocusByLane: {},
  questEventFocusByLane: {},
  questExpansionLensByLane: {},
  chronicleStageViewByLane: {},
  milestoneLensByLane: {},
  pathNodeFocusByLane: {},
  pathEventFocusByLane: {},
  pathChapterFocusByLane: {},
  pathChapterArchiveExpandedByLane: {},
  pathCoreDeckViewByLane: {},
  pathStageDepthByLane: {},
  pathUtilityDockViewByLane: {},
  pathChapterRecordLensByLane: {},
  pathChapterRecordLimitByLane: {},
  pathChapterRunwayLimitByLane: {},
  proofLimitByLane: {},
  pathReplayIndexByLane: {},
  pathReplayFilterByLane: {},
  pathReplayPlayingLaneId: null,
  pathReplayTimer: null,
  pathMemoryLensByLane: {},
  trailLimitByLane: {},
  gameStepByLane: {},
  copiedCommandFor: null,
  copiedDispatchFor: null,
  copiedBatch: false,
  manualCopyBuffer: null,
  routeHash: "",
  transform: { x: 0, y: 0, scale: 0.72 },
  dragging: false,
  dragStart: { x: 0, y: 0 },
};

const DISPATCH_STORAGE_KEY = "agent-company-atlas.dispatch-outbox.v1";
const DISPATCH_HISTORY_KEY = "agent-company-atlas.dispatch-history.v1";
const FEED_FILTER_KEY = "agent-company-atlas.feed-filter.v1";
const FEED_SAVED_VIEWS_KEY = "agent-company-atlas.feed-saved-views.v1";
const TROPHY_FILTER_KEY = "agent-company-atlas.trophy-filter.v1";
const ASSET_FILTER_KEY = "agent-company-atlas.asset-filter.v1";
const GATE_RADAR_FILTER_KEY = "agent-company-atlas.gate-radar-filter.v1";
const GATE_RADAR_NOTES_KEY = "agent-company-atlas.gate-radar-notes.v1";
const LAST_UNLOCK_KEY = "agent-company-atlas.last-unlock.v1";
const ATLAS_DECK_KEY = "agent-company-atlas.active-deck.v1";
const COMMAND_ARCHIVE_KEY = "agent-company-atlas.command-archive-panel.v1";

const ATLAS_DECKS = [
  { id: "control", label: "Control", note: "now" },
  { id: "worlds", label: "Worlds", note: "lanes" },
  { id: "command", label: "Command", note: "bots" },
  { id: "history", label: "History", note: "trail" },
  { id: "library", label: "Library", note: "assets" },
  { id: "all", label: "All", note: "audit" },
];

const ATLAS_TELEPORTS = [
  { id: "cockpit", label: "Cockpit", note: "lane", deck: "command", stage: "cockpit", target: "#detail-panel", view: "overview" },
  { id: "map", label: "Map", note: "paths", deck: "command", stage: "map", target: ".map-stage" },
  { id: "bots", label: "Bots", note: "crew", deck: "command", stage: "bots", panel: "bots", target: ".bot-command-panel" },
  { id: "feed", label: "Feed", note: "events", deck: "history", stage: "feed", target: ".mission-feed-panel" },
  { id: "worlds", label: "Worlds", note: "games", deck: "worlds", stage: "worlds", target: "#worlds-launch" },
  { id: "assets", label: "Assets", note: "art", deck: "library", stage: "assets", target: ".asset-vault-panel" },
];

const COMMAND_ARCHIVE_PANELS = ["relay", "dispatch", "command", "quest", "crew", "threads", "bots", "operators"];

const palette = [
  ["#44d7c9", "#f4ba55"],
  ["#ff6f61", "#44d7c9"],
  ["#8be06e", "#f4ba55"],
  ["#9a89ff", "#ff6f61"],
  ["#f4ba55", "#8be06e"],
  ["#c4d4cf", "#44d7c9"],
];

const el = {
  atlasDeckDock: document.querySelector("#atlas-deck-dock"),
  atlasTeleportRail: document.querySelector("#atlas-teleport-rail"),
  atlasCommandRibbon: document.querySelector("#atlas-command-ribbon"),
  snapshotTime: document.querySelector("#snapshot-time"),
  companyTitle: document.querySelector("#company-title"),
  companyCopy: document.querySelector("#company-copy"),
  metricGrid: document.querySelector("#metric-grid"),
  signalCore: document.querySelector("#signal-core"),
  controlRunway: document.querySelector("#control-runway"),
  achievementRail: document.querySelector("#achievement-rail"),
  liveOpsPulse: document.querySelector("#live-ops-pulse"),
  systemRelay: document.querySelector("#system-relay"),
  worldsLaunch: document.querySelector("#worlds-launch"),
  worldLoom: document.querySelector("#world-loom"),
  arcadeDeck: document.querySelector("#arcade-deck"),
  minigameRegistryCodex: document.querySelector("#minigame-registry-codex"),
  motionForge: document.querySelector("#motion-forge"),
  progressionConstellation: document.querySelector("#progression-constellation"),
  realmPackPanel: document.querySelector("#realm-pack-panel"),
  expansionForge: document.querySelector("#expansion-forge"),
  laneGenesisFoundry: document.querySelector("#lane-genesis-foundry"),
  creatorKit: document.querySelector("#creator-kit"),
  achievementWallCount: document.querySelector("#achievement-wall-count"),
  achievementWall: document.querySelector("#achievement-wall"),
  trophyTierFilters: document.querySelector("#trophy-tier-filters"),
  trophyLaneFilter: document.querySelector("#trophy-lane-filter"),
  dispatchCount: document.querySelector("#dispatch-count"),
  dispatchSuggestionCount: document.querySelector("#dispatch-suggestion-count"),
  dispatchSuggestionList: document.querySelector("#dispatch-suggestion-list"),
  dispatchOutboxList: document.querySelector("#dispatch-outbox-list"),
  dispatchBatchCount: document.querySelector("#dispatch-batch-count"),
  dispatchBatchList: document.querySelector("#dispatch-batch-list"),
  dispatchHistoryCount: document.querySelector("#dispatch-history-count"),
  dispatchHistoryList: document.querySelector("#dispatch-history-list"),
  commandRelayDeck: document.querySelector("#command-relay-deck"),
  companyQuestBoard: document.querySelector("#company-quest-board"),
  crewBridgeCount: document.querySelector("#crew-bridge-count"),
  crewBridge: document.querySelector("#crew-bridge"),
  threadNexusCount: document.querySelector("#thread-nexus-count"),
  threadNexus: document.querySelector("#thread-nexus"),
  botCommandCount: document.querySelector("#bot-command-count"),
  botCommandSummary: document.querySelector("#bot-command-summary"),
  botCommandMatrix: document.querySelector("#bot-command-matrix"),
  missionFeedCount: document.querySelector("#mission-feed-count"),
  missionFeedFilter: document.querySelector("#mission-feed-filter"),
  missionFeedTimelineBoard: document.querySelector("#mission-feed-timeline-board"),
  companyChronicleSpine: document.querySelector("#company-chronicle-spine"),
  experimentDiscoveryLab: document.querySelector("#experiment-discovery-lab"),
  feedSavedViews: document.querySelector("#feed-saved-views"),
  feedPlaybackTitle: document.querySelector("#feed-playback-title"),
  feedPlaybackCount: document.querySelector("#feed-playback-count"),
  feedPlaybackCard: document.querySelector("#feed-playback-card"),
  feedPlaybackToggle: document.querySelector("[data-feed-playback='toggle']"),
  missionFeed: document.querySelector("#mission-feed"),
  laneList: document.querySelector("#lane-list"),
  stateFilter: document.querySelector("#state-filter"),
  mapViewport: document.querySelector("#map-viewport"),
  mapWorld: document.querySelector("#map-world"),
  mapPlaybackHud: document.querySelector("#map-playback-hud"),
  mapFocusPanel: document.querySelector("#map-focus-panel"),
  routeSvg: document.querySelector("#route-svg"),
  nodeLayer: document.querySelector("#node-layer"),
  detailPanel: document.querySelector("#detail-panel"),
  agentCount: document.querySelector("#agent-count"),
  agentRoster: document.querySelector("#agent-roster"),
  assetVaultCount: document.querySelector("#asset-vault-count"),
  assetVaultFilters: document.querySelector("#asset-vault-filters"),
  assetProductionBoard: document.querySelector("#asset-production-board"),
  assetVault: document.querySelector("#asset-vault"),
  leaderboard: document.querySelector("#leaderboard"),
  researchList: document.querySelector("#research-list"),
  refreshButton: document.querySelector("#refresh-button"),
  unlockToast: document.querySelector("#unlock-toast"),
  zoomIn: document.querySelector("#zoom-in"),
  zoomOut: document.querySelector("#zoom-out"),
  zoomReset: document.querySelector("#zoom-reset"),
  canvas: document.querySelector("#particle-field"),
};

function formatNumber(value) {
  return new Intl.NumberFormat("en-US").format(value ?? 0);
}

function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value ?? 0);
}

function shortDate(value) {
  if (!value) return "No time";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function compactText(value, max = 150) {
  const text = String(value ?? "").trim();
  if (text.length <= max) return text;
  return `${text.slice(0, max - 1).trim()}...`;
}

function readLocalList(key) {
  try {
    const raw = window.localStorage?.getItem(key);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function readDispatchOutbox() {
  return readLocalList(DISPATCH_STORAGE_KEY)
    .filter((item) => item?.id && item?.command)
    .slice(0, 24);
}

function readDispatchHistory() {
  return readLocalList(DISPATCH_HISTORY_KEY)
    .filter((item) => item?.id && item?.action)
    .slice(0, 40);
}

function feedKinds() {
  return ["all", "task", "service_request", "evidence", "outcome", "trace"];
}

function trophyTiers() {
  return ["all", "mythic", "gold", "silver", "bronze"];
}

function assetKinds() {
  return ["all", "lane", "game", "agent", "system"];
}

function gateRadarFilters() {
  return ["all", "blocker", "review", "browser", "account", "payment", "public"];
}

function readFeedFilter() {
  try {
    const value = window.localStorage?.getItem(FEED_FILTER_KEY);
    return feedKinds().includes(value) ? value : "all";
  } catch {
    return "all";
  }
}

function writeFeedFilter() {
  try {
    window.localStorage?.setItem(FEED_FILTER_KEY, state.feedFilter);
  } catch {
    // Feed preference is optional in static mode.
  }
}

function readSavedFeedViews() {
  return readLocalList(FEED_SAVED_VIEWS_KEY)
    .filter((item) => item?.id && feedKinds().includes(item.filter))
    .slice(0, 12);
}

function writeSavedFeedViews() {
  try {
    window.localStorage?.setItem(FEED_SAVED_VIEWS_KEY, JSON.stringify(state.savedFeedViews.slice(0, 12)));
  } catch {
    // Saved feed views are optional in static mode.
  }
}

function readTrophyFilters() {
  try {
    const parsed = JSON.parse(window.localStorage?.getItem(TROPHY_FILTER_KEY) ?? "{}");
    return {
      tier: trophyTiers().includes(parsed?.tier) ? parsed.tier : "all",
      lane: typeof parsed?.lane === "string" ? parsed.lane : "all",
    };
  } catch {
    return { tier: "all", lane: "all" };
  }
}

function writeTrophyFilters() {
  try {
    window.localStorage?.setItem(TROPHY_FILTER_KEY, JSON.stringify({ tier: state.trophyTierFilter, lane: state.trophyLaneFilter }));
  } catch {
    // Trophy filters are optional in static mode.
  }
}

function readAssetFilter() {
  try {
    const value = window.localStorage?.getItem(ASSET_FILTER_KEY);
    return assetKinds().includes(value) ? value : "all";
  } catch {
    return "all";
  }
}

function writeAssetFilter() {
  try {
    window.localStorage?.setItem(ASSET_FILTER_KEY, state.assetFilter);
  } catch {
    // Asset filters are optional in static mode.
  }
}

function readGateRadarFilters() {
  try {
    const parsed = JSON.parse(window.localStorage?.getItem(GATE_RADAR_FILTER_KEY) ?? "{}");
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return {};
    return Object.fromEntries(
      Object.entries(parsed).filter(([, value]) => gateRadarFilters().includes(value))
    );
  } catch {
    return {};
  }
}

function writeGateRadarFilters() {
  try {
    window.localStorage?.setItem(GATE_RADAR_FILTER_KEY, JSON.stringify(state.gateRadarFilterByLane));
  } catch {
    // Radar filters are optional in static mode.
  }
}

function cleanGateRadarNote(value) {
  return compactText(String(value ?? "").replace(/\s+/g, " ").trim(), 180);
}

function readGateRadarNotes() {
  try {
    const parsed = JSON.parse(window.localStorage?.getItem(GATE_RADAR_NOTES_KEY) ?? "{}");
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return {};
    return Object.fromEntries(
      Object.entries(parsed)
        .filter(([, notes]) => notes && typeof notes === "object" && !Array.isArray(notes))
        .map(([laneId, notes]) => [
          laneId,
          Object.fromEntries(
            Object.entries(notes)
              .map(([noteId, note]) => [noteId, { text: cleanGateRadarNote(note?.text), updatedAt: note?.updatedAt ?? "" }])
              .filter(([, note]) => note.text)
              .slice(0, 16)
          ),
        ])
    );
  } catch {
    return {};
  }
}

function writeGateRadarNotes() {
  try {
    window.localStorage?.setItem(GATE_RADAR_NOTES_KEY, JSON.stringify(state.gateRadarNotesByLane));
  } catch {
    // Radar notes are optional in static mode.
  }
}

function readLastUnlockId() {
  try {
    return window.localStorage?.getItem(LAST_UNLOCK_KEY) ?? null;
  } catch {
    return null;
  }
}

function writeLastUnlockId(id) {
  try {
    if (id) window.localStorage?.setItem(LAST_UNLOCK_KEY, id);
  } catch {
    // Unlock memory is optional in static mode.
  }
}

function validAtlasDeck(deck) {
  return ATLAS_DECKS.some((item) => item.id === deck) ? deck : "control";
}

function validAtlasStage(stage) {
  return ["control", "cockpit", "map", "bots", "feed", "worlds", "assets", "all"].includes(stage) ? stage : "control";
}

function defaultAtlasStageForDeck(deck) {
  if (deck === "command") return "cockpit";
  if (deck === "history") return "feed";
  if (deck === "worlds") return "worlds";
  if (deck === "library") return "assets";
  if (deck === "all") return "all";
  return "control";
}

function validCommandArchivePanel(panel) {
  return COMMAND_ARCHIVE_PANELS.includes(panel) ? panel : "relay";
}

function readAtlasDeck() {
  try {
    return validAtlasDeck(window.localStorage?.getItem(ATLAS_DECK_KEY) ?? "control");
  } catch {
    return "control";
  }
}

function readCommandArchivePanel() {
  try {
    return validCommandArchivePanel(window.localStorage?.getItem(COMMAND_ARCHIVE_KEY) ?? "relay");
  } catch {
    return "relay";
  }
}

function writeAtlasDeck() {
  try {
    window.localStorage?.setItem(ATLAS_DECK_KEY, state.activeAtlasDeck);
  } catch {
    // Deck selection is optional in static mode.
  }
}

function writeCommandArchivePanel() {
  try {
    window.localStorage?.setItem(COMMAND_ARCHIVE_KEY, state.commandArchivePanel);
  } catch {
    // Archive focus is optional in static mode.
  }
}

function applyCommandArchivePanel() {
  const activePanel = validCommandArchivePanel(state.commandArchivePanel);
  document.body.dataset.commandArchivePanel = activePanel;
  document.querySelectorAll("[data-command-archive-button]").forEach((button) => {
    const isActive = button.dataset.commandArchiveButton === activePanel;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-pressed", isActive ? "true" : "false");
  });
}

function applyAtlasDeck() {
  document.body.dataset.atlasDeck = validAtlasDeck(state.activeAtlasDeck);
  document.body.dataset.atlasStage = validAtlasStage(state.activeAtlasStage);
  document.body.dataset.detailView = state.detailView;
  applyCommandArchivePanel();
}

function writeDispatchOutbox() {
  try {
    window.localStorage?.setItem(DISPATCH_STORAGE_KEY, JSON.stringify(state.stagedDispatches.slice(0, 24)));
  } catch {
    // Static mode still works without persistence when storage is unavailable.
  }
}

function writeDispatchHistory() {
  try {
    window.localStorage?.setItem(DISPATCH_HISTORY_KEY, JSON.stringify(state.dispatchHistory.slice(0, 40)));
  } catch {
    // History is an enhancement; dispatch staging continues without it.
  }
}

function recordDispatchHistory(action, detail) {
  state.dispatchHistory = [
    {
      id: `history-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
      action,
      laneName: detail?.laneName ?? "Batch",
      title: detail?.title ?? stateLabel(action),
      count: detail?.count ?? 1,
      time: new Date().toISOString(),
    },
    ...state.dispatchHistory,
  ].slice(0, 40);
  writeDispatchHistory();
}

function stateLabel(value) {
  return String(value ?? "unknown").replaceAll("_", " ");
}

function laneStyle(lane) {
  const visual = lane.visual ?? {};
  const texture = visual.minigame?.texture;
  const accent = escapeHtml(visual.accent ?? "#44d7c9");
  const accentAlt = escapeHtml(visual.accentAlt ?? "#f4ba55");
  const textureStyle = texture ? ` --game-texture:url('${escapeHtml(texture)}');` : "";
  return `--node-a:${accent}; --node-b:${accentAlt}; --lane-accent:${accent}; --lane-accent-alt:${accentAlt};${textureStyle}`;
}

function avatarMarkup(lane, className) {
  const avatar = lane.visual?.avatar;
  if (!avatar) return `<div class="${className} avatar-fallback" aria-hidden="true"></div>`;
  return `<img class="${className}" src="${escapeHtml(avatar)}" alt="" />`;
}

function agentAvatarMarkup(agent, lane, className) {
  const avatar = agent?.visual?.avatar ?? lane.visual?.avatar;
  if (!avatar) return `<div class="${className} avatar-fallback" aria-hidden="true"></div>`;
  return `<img class="${className}" src="${escapeHtml(avatar)}" alt="" />`;
}

function agentCharacterFrame(agent, lane, className) {
  const visual = agent?.visual ?? {};
  const avatar = visual.avatar ?? lane.visual?.avatar;
  const callsign = visual.callsign ?? agent?.name ?? agent?.agent_id ?? lane.ownerAgentId ?? "Lane bot";
  const specialty = visual.specialty ?? lane.visual?.realm ?? lane.department ?? "Lane operator";
  const accent = visual.accent ?? lane.visual?.accent ?? "#44d7c9";
  const sheetCell = Math.max(1, Number(visual.sheetCell ?? 1));
  const frameClass = `${className} agent-character-frame`;
  const portrait = avatar
    ? `<img class="agent-character-portrait" src="${escapeHtml(avatar)}" alt="" />`
    : `<span class="agent-character-portrait avatar-fallback" aria-hidden="true"></span>`;
  return `
    <div class="${frameClass}" style="--agent-a:${escapeHtml(accent)}; --agent-cell:${sheetCell};" aria-label="${escapeHtml(callsign)} character frame" title="${escapeHtml(specialty)}">
      <span class="agent-character-aura" aria-hidden="true"></span>
      ${portrait}
      <span class="agent-character-sigil" aria-hidden="true">${escapeHtml(String(sheetCell).padStart(2, "0"))}</span>
      <span class="agent-character-scan" aria-hidden="true"></span>
    </div>`;
}

function laneForFeedItem(item) {
  return state.snapshot?.lanes?.find((lane) => lane.id === item?.laneId) ?? null;
}

function feedSceneForItem(item) {
  const lane = laneForFeedItem(item);
  const kindScore = {
    outcome: 70,
    evidence: 55,
    trace: 42,
    task: 34,
    service_request: 26,
  };
  const base = kindScore[item.kind] ?? 20;
  const level = Number(item.laneLevel ?? lane?.level ?? 1);
  const xp = base + Math.max(level, 1) * 8;
  const status = item.status === "complete" ? "cleared" : item.status === "blocked" || item.status === "needs_review" ? "gated" : "active";
  const rarity = xp >= 160 ? "legend" : xp >= 125 ? "epic" : xp >= 95 ? "rare" : status === "gated" ? "locked" : "common";
  const scene = {
    lane,
    realm: item.laneRealm ?? lane?.visual?.realm ?? lane?.department ?? "Unmapped lane",
    image: lane?.visual?.avatar ?? "",
    accent: lane?.visual?.accent ?? "#44d7c9",
    accentAlt: lane?.visual?.accentAlt ?? "#f4ba55",
    xp,
    status,
    rarity,
    kindLabel: stateLabel(item.kind),
    statusLabel: stateLabel(item.status),
  };
  return scene;
}

function feedSceneStyle(scene) {
  const image = scene.image ? ` --scene-image:url('${escapeHtml(scene.image)}');` : "";
  return `--feed-accent:${escapeHtml(scene.accent)}; --feed-accent-alt:${escapeHtml(scene.accentAlt)};${image}`;
}

function hexToRgb(value, fallback = [68, 215, 201]) {
  const hex = String(value ?? "").replace("#", "").trim();
  if (!/^[0-9a-f]{6}$/i.test(hex)) return fallback;
  return [0, 2, 4].map((index) => parseInt(hex.slice(index, index + 2), 16));
}

function selectedLane() {
  return state.snapshot?.lanes?.find((lane) => lane.id === state.selectedLaneId) ?? state.snapshot?.lanes?.[0] ?? null;
}

function motionSignal() {
  const playbackItem = state.snapshot ? currentPlaybackItem() : null;
  const playbackLane = state.snapshot?.lanes?.find((lane) => lane.id === playbackItem?.laneId) ?? null;
  const lane = state.feedPlaying && playbackLane ? playbackLane : selectedLane() ?? playbackLane;
  const visual = lane?.visual ?? {};
  const blockers = lane?.counts?.blockers ?? 0;
  const pending = lane?.counts?.pendingRequests ?? 0;
  const outcomes = lane?.counts?.outcomes ?? 0;
  const traces = lane?.counts?.traces ?? 0;
  const proofs = (lane?.counts?.artifacts ?? 0) + traces + outcomes;
  const tests = (lane?.counts?.activeTasks ?? 0) + (lane?.recentTasks?.length ?? 0);
  const pressure = Math.min(100, blockers * 14 + pending * 10 + (state.feedPlaying ? 32 : 0) + Math.min(traces, 30));
  const unlockCharge = Math.min(100, outcomes * 12 + (lane?.level ?? 1) * 6);
  const mode = state.feedPlaying ? "playback" : state.detailView === "path" ? "path" : blockers ? "gated" : outcomes ? "unlock" : "scouting";
  return {
    lane,
    playbackItem,
    mode,
    label: state.feedPlaying ? "Playback live" : state.detailView === "path" ? "Path field" : blockers ? "Gate pressure" : outcomes ? "Unlock charge" : "Scout sweep",
    accent: visual.accent ?? "#44d7c9",
    accentAlt: visual.accentAlt ?? "#f4ba55",
    focusX: Math.max(0.08, Math.min(0.92, (lane?.map?.x ?? 50) / 100)),
    focusY: Math.max(0.08, Math.min(0.92, (lane?.map?.y ?? 50) / 100)),
    pressure,
    unlockCharge,
    gateCharge: Math.min(100, blockers * 24 + pending * 18),
    proofCharge: Math.min(100, proofs * 2.4),
    testCharge: Math.min(100, tests * 12 + (lane?.visual?.minigame?.id ? 16 : 0)),
    intensity: Math.min(1.9, 0.7 + (lane?.level ?? 1) * 0.04 + pressure / 140 + (state.detailView === "path" ? 0.18 : 0)),
  };
}

function kineticFieldRibbons(signal) {
  const laneKey = String(signal.lane?.id ?? "company-field");
  const seed = Array.from(laneKey).reduce((sum, char) => sum + char.charCodeAt(0), 0);
  const charges = [
    { id: "gate", charge: signal.gateCharge, bend: -0.34 },
    { id: "proof", charge: signal.proofCharge, bend: 0.28 },
    { id: "tests", charge: signal.testCharge, bend: -0.18 },
    { id: "unlock", charge: signal.unlockCharge, bend: 0.2 },
  ];
  const ribbonCount = signal.mode === "path" ? 8 : 4;
  return Array.from({ length: ribbonCount }, (_, index) => {
    const charge = charges[index % charges.length];
    const spin = ((seed + index * 47) % 360) * (Math.PI / 180);
    const reach = 0.18 + ((seed + index * 19) % 34) / 100;
    return {
      id: `${charge.id}-${index}`,
      kind: charge.id,
      charge: Math.max(12, charge.charge),
      angle: spin,
      reach,
      bend: charge.bend,
      phase: ((seed + index * 31) % 100) / 100,
    };
  });
}

function applyMotionTheme() {
  const signal = motionSignal();
  document.body.dataset.motionMode = signal.mode;
  document.body.style.setProperty("--motion-a", signal.accent);
  document.body.style.setProperty("--motion-b", signal.accentAlt);
  document.body.style.setProperty("--motion-charge", `${Math.max(8, signal.unlockCharge)}%`);
  document.body.style.setProperty("--motion-test-charge", `${Math.max(8, signal.testCharge)}%`);
  document.body.style.setProperty("--motion-proof-charge", `${Math.max(8, signal.proofCharge)}%`);
}

function renderSignalCore() {
  if (!el.signalCore || !state.snapshot) return;
  const signal = motionSignal();
  const lane = signal.lane;
  applyMotionTheme();
  el.signalCore.innerHTML = `
    <div class="signal-core-orb" aria-hidden="true" style="${lane ? laneStyle(lane) : ""}">
      <span></span>
      <i></i>
    </div>
    <div class="signal-core-copy">
      <p class="eyebrow">Signal Core</p>
      <h3>${escapeHtml(lane?.name ?? "Company field")}</h3>
      <div class="signal-core-meta">
        <span>${escapeHtml(signal.label)}</span>
        <strong>${escapeHtml(lane ? `L${lane.level}` : "L0")}</strong>
        <em>${escapeHtml(signal.playbackItem ? stateLabel(signal.playbackItem.kind) : stateLabel(signal.mode))}</em>
      </div>
    </div>
    <div class="signal-core-bars">
      <span style="--bar:${signal.pressure}%"><i></i><b>Pressure</b></span>
      <span style="--bar:${signal.unlockCharge}%"><i></i><b>Unlock</b></span>
    </div>`;
}

function feedSceneArt(scene, item, mode = "card") {
  const initials = String(item.laneName ?? "?")
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join("")
    .toUpperCase();
  return `
    <div class="feed-scene-art ${escapeHtml(mode)} ${escapeHtml(scene.rarity)}" aria-hidden="true">
      <div class="scene-orbit"></div>
      <div class="scene-frame">
        ${scene.image ? `<img src="${escapeHtml(scene.image)}" alt="" />` : `<strong>${escapeHtml(initials)}</strong>`}
      </div>
      <div class="scene-glint"></div>
    </div>`;
}

function trophyMedalArt(scene, item, tier) {
  return `
    <div class="trophy-sprite ${escapeHtml(tier)}" aria-hidden="true">
      <span></span>
      <i>${feedSceneArt(scene, item, "trophy-lane")}</i>
    </div>`;
}

function latestOutcomeItem() {
  return (state.snapshot?.missionFeed?.items ?? []).find((item) => item.kind === "outcome") ?? null;
}

function trophyTierForOutcome(item, index = 0) {
  const lane = laneForFeedItem(item);
  const countBoost = lane?.counts?.outcomes ?? 0;
  const rank = index + 1;
  return countBoost >= 12 || rank <= 2 ? "mythic" : countBoost >= 8 || rank <= 5 ? "gold" : countBoost >= 4 ? "silver" : "bronze";
}

function collectibleOutcomes(limit = 10) {
  const allTrophies = (state.snapshot?.missionFeed?.items ?? [])
    .filter((item) => item.kind === "outcome")
    .map((item, index) => {
      const scene = feedSceneForItem(item);
      const lane = scene.lane;
      const rank = index + 1;
      const tier = trophyTierForOutcome(item, index);
      return { item, scene, lane, rank, tier };
    });
  return allTrophies
    .filter(({ item, tier }) => state.trophyTierFilter === "all" || tier === state.trophyTierFilter)
    .filter(({ item }) => state.trophyLaneFilter === "all" || item.laneId === state.trophyLaneFilter)
    .slice(0, limit);
}

function trophyOutcomeCountForFilters() {
  return collectibleOutcomes(999).length;
}

function laneTrophyTracks(limit = 6) {
  return [...(state.snapshot?.lanes ?? [])]
    .sort((a, b) => (b.counts?.outcomes ?? 0) - (a.counts?.outcomes ?? 0) || (b.level ?? 0) - (a.level ?? 0))
    .slice(0, limit);
}

function readRoute() {
  const params = new URLSearchParams(window.location.hash.replace(/^#/, ""));
  return {
    lane: params.get("lane"),
    view: params.get("view"),
    deck: params.get("deck"),
    stage: params.get("stage"),
  };
}

function routeIsValidView(view) {
  return ["overview", "path", "chronicle", "trail", "game", "comms"].includes(view);
}

function syncRoute() {
  if (!state.selectedLaneId) return;
  const params = new URLSearchParams();
  params.set("lane", state.selectedLaneId);
  params.set("view", state.detailView);
  params.set("deck", state.activeAtlasDeck);
  params.set("stage", state.activeAtlasStage);
  const nextHash = `#${params.toString()}`;
  state.routeHash = nextHash;
  if (window.location.hash !== nextHash) {
    window.history.replaceState(null, "", nextHash);
  }
}

function applyRouteFromHash() {
  if (!state.snapshot || window.location.hash === state.routeHash) return;
  const route = readRoute();
  if (state.snapshot.lanes.some((lane) => lane.id === route.lane)) {
    state.selectedLaneId = route.lane;
  }
  if (routeIsValidView(route.view)) {
    state.detailView = route.view;
  }
  state.activeAtlasDeck = validAtlasDeck(route.deck ?? state.activeAtlasDeck);
  state.activeAtlasStage = route.stage ? validAtlasStage(route.stage) : defaultAtlasStageForDeck(state.activeAtlasDeck);
  applyAtlasDeck();
  state.routeHash = window.location.hash;
  renderAtlasDeckDock();
  renderAtlasTeleportRail();
  renderLaneList();
  renderMap();
  renderDetail();
  renderSignalCore();
  renderControlRunway();
  renderCompanyQuestBoard();
  renderWorldsLaunch();
  renderWorldLoom();
  renderArcadeDeck();
  renderMinigameRegistryCodex();
  renderMotionForge();
  renderAssetVault();
  renderCrewBridge();
  renderThreadNexus();
  renderBotCommandMatrix();
  focusPathBoardFromRoute(route);
}

function focusPathBoardFromRoute(route = readRoute(), behavior = "auto") {
  if (route.view !== "path") return;
  window.requestAnimationFrame(() => {
    window.requestAnimationFrame(() => {
      document.querySelector(".path-map-board")?.scrollIntoView({ behavior, block: "nearest" });
    });
  });
}

async function loadSnapshot() {
  try {
    const response = await fetch(`./data/snapshot.json?ts=${Date.now()}`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Snapshot request failed: ${response.status}`);
    state.snapshot = await response.json();
    const latestOutcome = latestOutcomeItem();
    const lastUnlockId = readLastUnlockId();
    const forceUnlockToast = new URLSearchParams(window.location.search).get("unlockToast") === "force";
    state.unlockToastHold = forceUnlockToast;
    state.unlockToast = latestOutcome && (forceUnlockToast || latestOutcome.id !== lastUnlockId) ? latestOutcome : null;
    if (latestOutcome) writeLastUnlockId(latestOutcome.id);
    const trophyFilters = readTrophyFilters();
    state.trophyTierFilter = trophyFilters.tier;
    state.trophyLaneFilter = trophyFilters.lane === "all" || state.snapshot.lanes.some((lane) => lane.id === trophyFilters.lane) ? trophyFilters.lane : "all";
    state.assetFilter = readAssetFilter();
    state.commandArchivePanel = readCommandArchivePanel();
    const route = readRoute();
    state.activeAtlasDeck = validAtlasDeck(route.deck ?? readAtlasDeck());
    state.activeAtlasStage = route.stage ? validAtlasStage(route.stage) : defaultAtlasStageForDeck(state.activeAtlasDeck);
    state.gateRadarFilterByLane = readGateRadarFilters();
    state.gateRadarNotesByLane = readGateRadarNotes();
    state.selectedLaneId = state.snapshot.lanes.some((lane) => lane.id === route.lane) ? route.lane : state.snapshot.lanes[0]?.id ?? null;
    state.detailView = routeIsValidView(route.view) ? route.view : "overview";
    renderAll();
    focusPathBoardFromRoute(route);
  } catch (error) {
    el.companyTitle.textContent = "Snapshot unavailable";
    el.companyCopy.textContent = "Run the snapshot generator and serve the web directory locally.";
    el.detailPanel.innerHTML = `<div class="error">${escapeHtml(error.message)}</div>`;
  }
}

function renderAll() {
  applyAtlasDeck();
  renderAtlasDeckDock();
  renderAtlasTeleportRail();
  renderHeader();
  renderMetrics();
  renderSignalCore();
  renderControlRunway();
  renderAchievements();
  renderLiveOpsPulse();
  renderSystemRelay();
  renderWorldsLaunch();
  renderWorldLoom();
  renderArcadeDeck();
  renderMinigameRegistryCodex();
  renderMotionForge();
  renderCrewBridge();
  renderProgressionConstellation();
  renderRealmPacks();
  renderExpansionForge();
  renderLaneGenesisFoundry();
  renderCreatorKit();
  renderAchievementWall();
  renderUnlockToast();
  renderDispatchConsole();
  renderCompanyQuestBoard();
  renderCrewBridge();
  renderThreadNexus();
  renderMissionFeed();
  renderLaneList();
  renderMap();
  renderDetail();
  renderAgentRoster();
  renderAssetVault();
  renderLeaderboard();
  renderResearch();
  resetView(false);
  syncRoute();
}

function atlasDeckMetric(deckId) {
  const totals = state.snapshot?.totals ?? {};
  if (deckId === "control") return `${formatNumber(totals.blockers ?? 0)} gates`;
  if (deckId === "worlds") return `${formatNumber(totals.lanes ?? 0)} lanes`;
  if (deckId === "command") return `${formatNumber((state.snapshot?.agents ?? []).length)} bots`;
  if (deckId === "history") return `${formatNumber(state.snapshot?.missionFeed?.items?.length ?? 0)} events`;
  if (deckId === "library") return `${formatNumber(visualAssetRecords().length)} assets`;
  return "full";
}

function renderAtlasDeckDock() {
  if (!el.atlasDeckDock) return;
  el.atlasDeckDock.innerHTML = ATLAS_DECKS.map(
    (deck) => `
      <button class="atlas-deck-button ${state.activeAtlasDeck === deck.id ? "active" : ""}" type="button" data-atlas-deck="${escapeHtml(deck.id)}" aria-pressed="${state.activeAtlasDeck === deck.id ? "true" : "false"}" title="Show ${escapeHtml(deck.label)} deck">
        <span>${escapeHtml(deck.label)}</span>
        <strong>${escapeHtml(atlasDeckMetric(deck.id))}</strong>
        <em>${escapeHtml(deck.note)}</em>
      </button>`
  ).join("");
}

function atlasMotionConductorModel(signal = motionSignal()) {
  const charges = [
    { id: "gate", label: "Gate", value: signal.gateCharge, tone: signal.gateCharge ? "gated" : "ready" },
    { id: "proof", label: "Proof", value: signal.proofCharge, tone: signal.proofCharge ? "proof" : "scouting" },
    { id: "tests", label: "Tests", value: signal.testCharge, tone: signal.testCharge ? "advancing" : "scouting" },
    { id: "unlock", label: "Unlock", value: signal.unlockCharge, tone: signal.unlockCharge ? "unlocked" : "ready" },
  ];
  const peak = charges.reduce((winner, charge) => (charge.value > winner.value ? charge : winner), charges[0]);
  return {
    mode: signal.mode,
    label: signal.label,
    laneName: signal.lane?.name ?? "Company field",
    intensity: Math.round(signal.intensity * 50),
    focus: `${Math.round(signal.focusX * 100)}:${Math.round(signal.focusY * 100)}`,
    peak,
    charges: charges.map((charge, index) => ({
      ...charge,
      index,
      value: Math.max(8, Math.min(100, Math.round(charge.value))),
    })),
  };
}

function renderAtlasMotionConductor(model) {
  return `
    <div class="atlas-motion-conductor ${escapeHtml(model.mode)}" data-atlas-motion-mode="${escapeHtml(model.mode)}" aria-label="Atlas motion conductor" style="--motion-conductor-charge:${model.peak.value}%;">
      <span class="atlas-motion-orb" aria-hidden="true"><i></i></span>
      <span class="atlas-motion-copy">
        <b>${escapeHtml(model.label)}</b>
        <strong>${escapeHtml(compactText(model.laneName, 30))}</strong>
        <em>${escapeHtml(model.focus)} / ${formatNumber(model.intensity)} pulse</em>
      </span>
      <span class="atlas-motion-charges" aria-label="Motion charge lanes">
        ${model.charges
          .map(
            (charge) => `
              <i class="atlas-motion-charge ${escapeHtml(charge.tone)}" data-atlas-motion-charge="${escapeHtml(charge.id)}" style="--charge:${charge.value}%; --charge-index:${charge.index};" title="${escapeHtml(charge.label)} ${formatNumber(charge.value)}%"></i>`
          )
          .join("")}
      </span>
    </div>`;
}
function atlasCommandRibbonModel() {
  const totals = state.snapshot?.totals ?? {};
  const lanes = state.snapshot?.lanes ?? [];
  const agents = state.snapshot?.agents ?? [];
  const feedItems = state.snapshot?.missionFeed?.items ?? [];
  const assets = visualAssetRecords();
  const gateCount = (totals.blockers ?? 0) + (totals.pendingRequests ?? 0);
  const selected = selectedLane();
  const winCount = feedItems.filter((item) => item.kind === "outcome").length + (totals.outcomes ?? 0);
  const gameCount = lanes.filter((lane) => lane.visual?.minigame).length;
  const liveBotCount = agents.filter((agent) => agent.lane?.id || agent.visual?.avatar).length;
  const nextTitle = selected ? chronicleNextAction(selected) : feedItems[0]?.title ?? "Select a lane";
  const readiness = Math.round(
    Math.min(100, Math.max(8, ((lanes.length + liveBotCount + gameCount + Math.max(1, winCount)) / Math.max(1, lanes.length * 4 + agents.length)) * 100))
  );
  const cells = [
    {
      id: "lanes",
      label: "Lanes",
      value: formatNumber(totals.lanes ?? lanes.length),
      note: `${formatNumber(gameCount)} game seeds`,
      action: "lanes",
      tone: "ready",
      charge: Math.min(100, Math.max(18, lanes.length * 8)),
    },
    {
      id: "gates",
      label: "Gates",
      value: gateCount ? formatNumber(gateCount) : "clear",
      note: gateCount ? "operator review" : "route clear",
      action: "gates",
      tone: gateCount ? "gated" : "unlocked",
      charge: gateCount ? Math.min(100, 28 + gateCount * 10) : 34,
    },
    {
      id: "bots",
      label: "Bots",
      value: formatNumber(liveBotCount),
      note: `${formatNumber(agents.length)} rostered`,
      action: "bots",
      tone: liveBotCount ? "advancing" : "scouting",
      charge: Math.min(100, Math.max(18, liveBotCount * 12)),
    },
    {
      id: "wins",
      label: "Wins",
      value: formatNumber(winCount),
      note: `${formatNumber(feedItems.length)} events`,
      action: "wins",
      tone: winCount ? "unlocked" : "scouting",
      charge: Math.min(100, Math.max(16, winCount * 14)),
    },
    {
      id: "assets",
      label: "Assets",
      value: formatNumber(assets.length),
      note: `${formatNumber(assets.filter((asset) => asset.kind === "agent").length)} avatars`,
      action: "assets",
      tone: assets.length ? "ready" : "scouting",
      charge: Math.min(100, Math.max(18, assets.length * 3)),
    },
    {
      id: "next",
      label: "Next",
      value: selected ? `L${formatNumber(selected.level)}` : "Start",
      note: compactText(nextTitle, 34),
      action: "next",
      tone: gateCount ? "gated" : selected ? "advancing" : "ready",
      charge: selected ? Math.max(18, Math.min(100, selected.progress ?? selected.level * 8)) : readiness,
    },
  ];

  return { readiness, selected, cells };
}

function renderAtlasCommandRibbon() {
  if (!el.atlasCommandRibbon || !state.snapshot) return;
  const model = atlasCommandRibbonModel();
  const conductor = atlasMotionConductorModel();
  el.atlasCommandRibbon.innerHTML = `
    <div class="atlas-command-ribbon-core" aria-label="Company command readiness" style="--atlas-command-readiness:${model.readiness}%;">
      <span>Command Ribbon</span>
      <strong>${formatNumber(model.readiness)}%</strong>
      <em>${escapeHtml(model.selected?.name ?? "Company overview")}</em>
    </div>
    ${renderAtlasMotionConductor(conductor)}
    ${model.cells
      .map(
        (cell, index) => `
          <button
            class="atlas-command-ribbon-cell ${escapeHtml(cell.tone)}"
            type="button"
            data-atlas-command-ribbon-cell="${escapeHtml(cell.id)}"
            data-atlas-command-ribbon-action="${escapeHtml(cell.action)}"
            style="--atlas-ribbon-cell-charge:${Math.max(8, Math.min(100, cell.charge))}%; --atlas-ribbon-index:${index};"
            title="${escapeHtml(cell.label)}: ${escapeHtml(cell.note)}"
          >
            <i aria-hidden="true"></i>
            <span>${escapeHtml(cell.label)}</span>
            <strong>${escapeHtml(cell.value)}</strong>
            <em>${escapeHtml(cell.note)}</em>
          </button>`
      )
      .join("")}`;
}
function activateCockpitControlPad(action, laneId) {
  const lane = state.snapshot?.lanes?.find((item) => item.id === laneId) ?? selectedLane();
  if (!lane) return;
  setAtlasDeck("command", { scroll: false, stage: "cockpit" });
  if (action === "queue") {
    stageDispatch(bestLaneDispatchSuggestion(lane));
    renderDetail();
    return;
  }
  if (action === "path") selectLane(lane.id, "path");
  else if (action === "gate") selectLane(lane.id, "trail");
  else if (action === "proof") selectLane(lane.id, "chronicle");
  else if (action === "bot") selectLane(lane.id, "comms");
  else if (action === "game") selectLane(lane.id, "game");
  else selectLane(lane.id, "overview");
}
function activateAtlasCommandRibbon(action) {
  if (action === "lanes") {
    setAtlasDeck("command", { scroll: false, stage: "map" });
    window.requestAnimationFrame(() => resetView(false));
  } else if (action === "gates") {
    setAtlasDeck("control", { scroll: false, stage: "control" });
    window.requestAnimationFrame(() => document.querySelector("#live-ops-pulse")?.scrollIntoView({ behavior: "smooth", block: "nearest" }));
  } else if (action === "bots") {
    setAtlasDeck("command", { scroll: false, stage: "bots" });
    setCommandArchivePanel("bots");
  } else if (action === "wins") {
    setAtlasDeck("history", { scroll: false, stage: "feed" });
    setFeedFilter("outcome");
  } else if (action === "assets") {
    setAtlasDeck("library", { scroll: false, stage: "assets" });
  } else if (action === "next") {
    const selected = selectedLane();
    setAtlasDeck("command", { scroll: false, stage: "cockpit" });
    if (selected) selectLane(selected.id, "overview");
  }
  renderAtlasCommandRibbon();
  syncRoute();
}
function atlasTeleportMetric(item) {
  const totals = state.snapshot?.totals ?? {};
  if (item.id === "cockpit") return selectedLane()?.visual?.callsign ?? `L${selectedLane()?.level ?? 1}`;
  if (item.id === "map") return `${formatNumber(totals.lanes ?? 0)} lanes`;
  if (item.id === "bots") return `${formatNumber(state.snapshot?.agents?.length ?? 0)} bots`;
  if (item.id === "feed") return `${formatNumber(state.snapshot?.missionFeed?.items?.length ?? 0)} logs`;
  if (item.id === "worlds") return `${formatNumber(totals.lanes ?? 0)} games`;
  if (item.id === "assets") return `${formatNumber(visualAssetRecords().length)} files`;
  return item.note;
}

function renderAtlasTeleportRail() {
  if (!el.atlasTeleportRail) return;
  el.atlasTeleportRail.innerHTML = ATLAS_TELEPORTS.map((item) => {
    const isActive = state.activeAtlasStage === item.stage;
    return `
      <button class="atlas-teleport-pad ${isActive ? "active" : ""}" type="button" data-atlas-teleport="${escapeHtml(item.id)}" aria-pressed="${isActive ? "true" : "false"}" title="Jump to ${escapeHtml(item.label)}">
        <span>${escapeHtml(item.label)}</span>
        <strong>${escapeHtml(atlasTeleportMetric(item))}</strong>
        <em>${escapeHtml(item.note)}</em>
      </button>`;
  }).join("");
}

function activateAtlasTeleport(teleportId) {
  const item = ATLAS_TELEPORTS.find((entry) => entry.id === teleportId);
  if (!item) return;
  if (item.panel) setCommandArchivePanel(item.panel);
  setAtlasDeck(item.deck, { scroll: false, stage: item.stage });
  if (item.view && state.selectedLaneId) {
    state.detailView = item.view;
    renderDetail();
    syncRoute();
  }
  renderAtlasTeleportRail();
  window.requestAnimationFrame(() => {
    document.querySelector(item.target)?.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

function cockpitKeepsViewportStable() {
  return state.activeAtlasDeck === "command" && state.activeAtlasStage === "cockpit";
}

function settleDetailPanelIntoView() {
  if (cockpitKeepsViewportStable()) return;
  document.querySelector("#detail-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function setAtlasDeck(deckId, { scroll = true, stage = null } = {}) {
  const nextDeck = validAtlasDeck(deckId);
  state.activeAtlasDeck = nextDeck;
  state.activeAtlasStage = stage ? validAtlasStage(stage) : defaultAtlasStageForDeck(nextDeck);
  writeAtlasDeck();
  applyAtlasDeck();
  renderAtlasDeckDock();
  renderAtlasTeleportRail();
  syncRoute();
  if (nextDeck === "command" && state.activeAtlasStage === "map") {
    window.requestAnimationFrame(() => resetView());
  }
  if (scroll) {
    document.querySelector("#atlas-deck-dock")?.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function setCommandArchivePanel(panel, { scroll = false } = {}) {
  state.commandArchivePanel = validCommandArchivePanel(panel);
  writeCommandArchivePanel();
  applyCommandArchivePanel();
  if (scroll) {
    document.querySelector(".command-archive-dock")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
}

function renderHeader() {
  const { snapshot } = state;
  const totals = snapshot.totals;
  el.snapshotTime.textContent = `Snapshot ${shortDate(snapshot.generatedUtc)}`;
  el.companyTitle.textContent = `${totals.lanes} money-path lanes, one atlas`;
  el.companyCopy.textContent =
    `${totals.tasks} tasks, ${totals.evidence} evidence records, ${totals.traces} trace events, and ${totals.pendingRequests} review-gated service requests are visible in one place.`;
}

function renderMetrics() {
  const totals = state.snapshot.totals;
  const metrics = [
    ["Lanes", totals.lanes],
    ["Tasks", totals.tasks],
    ["Evidence", totals.evidence],
    ["Artifacts", totals.artifacts],
    ["Blockers", totals.blockers],
    ["Realized", formatCurrency(totals.realizedUsd)],
  ];
  el.metricGrid.innerHTML = metrics
    .map(([label, value]) => `<div class="metric"><strong>${escapeHtml(value)}</strong><span>${escapeHtml(label)}</span></div>`)
    .join("");
}

function renderAchievements() {
  el.achievementRail.innerHTML = state.snapshot.achievements
    .map(
      (achievement) => `
      <article class="achievement ${achievement.unlocked ? "" : "locked"}">
        <p class="eyebrow">${achievement.unlocked ? "Unlocked" : "Locked"}</p>
        <h3>${escapeHtml(achievement.title)}</h3>
        <p>${escapeHtml(achievement.description)}</p>
      </article>`
    )
    .join("");
}

function liveOpsPulseRecords() {
  const feedItems = state.snapshot?.missionFeed?.items ?? [];
  const suggestions = state.snapshot?.dispatchConsole?.suggestions ?? [];
  const botRecords = botCommandRecords();
  return (state.snapshot?.lanes ?? [])
    .map((lane, index) => {
      const counts = lane.counts ?? {};
      const latest = feedItems.find((item) => item.laneId === lane.id) ?? lane.trail?.[0] ?? null;
      const suggestion = suggestions.find((item) => item.laneId === lane.id) ?? laneDispatchSuggestion(lane);
      const bot = botRecords.find((record) => record.lane?.id === lane.id) ?? null;
      const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id || draft.sourceId === suggestion?.id);
      const blockers = counts.blockers ?? 0;
      const pending = counts.pendingRequests ?? 0;
      const activeTasks = counts.activeTasks ?? Math.max(0, (counts.tasks ?? 0) - (counts.completedTasks ?? 0));
      const proof = counts.evidence ?? 0;
      const wins = counts.outcomes ?? 0;
      const traces = counts.traces ?? 0;
      const urgency = suggestion?.urgency ?? 0;
      const recentBoost = latest ? 18 : 0;
      const pulseScore = Math.min(100, urgency * 0.34 + blockers * 18 + pending * 12 + activeTasks * 3 + recentBoost + (staged ? 10 : 0) + Math.min(20, wins * 0.08 + proof * 0.04 + traces * 0.02));
      const mode = staged ? "staged" : blockers || pending ? "gated" : suggestion ? "ready" : latest ? "live" : "scouting";
      return {
        lane,
        index,
        latest,
        suggestion,
        bot,
        staged,
        blockers,
        pending,
        activeTasks,
        proof,
        wins,
        traces,
        urgency,
        pulseScore,
        mode,
        title: latest?.title ?? suggestion?.title ?? lane.quest?.title ?? lane.name,
        summary: suggestion?.reason ?? latest?.summary ?? lane.nextAction ?? "No current pulse for this lane yet.",
      };
    })
    .sort((a, b) => b.pulseScore - a.pulseScore || b.activeTasks - a.activeTasks || b.wins - a.wins)
    .slice(0, 10);
}

function controlRunwayRecords(limit = 6) {
  const selectedRecord = liveOpsPulseRecords().find((record) => record.lane.id === state.selectedLaneId);
  const selectedLane = selectedRecord?.lane ?? (state.snapshot?.lanes ?? []).find((lane) => lane.id === state.selectedLaneId) ?? null;
  const records = liveOpsPulseRecords().filter((record) => record.lane.id !== selectedLane?.id).slice(0, Math.max(0, limit - 1));
  return selectedRecord ? [selectedRecord, ...records] : records.slice(0, limit);
}

function renderControlRunwayNode(record, index) {
  const lane = record.lane;
  const checkpoint = lane.quest?.checkpoint ?? lane.quest?.title ?? record.title;
  const isActive = lane.id === state.selectedLaneId;
  const view = record.blockers || record.pending ? "trail" : "overview";
  return `
    <button
      class="control-runway-node ${escapeHtml(record.mode)} ${isActive ? "active" : ""}"
      type="button"
      data-control-runway-lane="${escapeHtml(lane.id)}"
      data-control-runway-view="${escapeHtml(view)}"
      style="${laneStyle(lane)} --runway-charge:${Math.max(10, Math.round(record.pulseScore))}%; --runway-index:${index};"
      title="Open ${escapeHtml(lane.name)}"
    >
      <i>L${escapeHtml(lane.level ?? index + 1)}</i>
      <strong>${escapeHtml(compactText(lane.name, 32))}</strong>
      <span>${escapeHtml(compactText(checkpoint, 54))}</span>
      <em>${record.blockers + record.pending ? `${formatNumber(record.blockers + record.pending)} gates` : `${formatNumber(record.wins)} wins`}</em>
    </button>`;
}

function renderControlRunway() {
  if (!el.controlRunway || !state.snapshot) return;
  const records = controlRunwayRecords();
  const selected = records.find((record) => record.lane.id === state.selectedLaneId) ?? records[0];
  const gates = records.reduce((sum, record) => sum + record.blockers + record.pending, 0);
  const staged = records.filter((record) => record.staged).length;
  const active = records.filter((record) => record.activeTasks || record.latest || record.suggestion).length;
  const selectedStyle = selected?.lane ? laneStyle(selected.lane) : "";
  el.controlRunway.innerHTML = `
    <div class="control-runway-head" style="${selectedStyle}">
      <div>
        <p class="eyebrow">Control Runway</p>
        <h3>${escapeHtml(selected?.lane?.name ?? "Active lanes")}</h3>
      </div>
      <div class="control-runway-stats" aria-label="Runway stats">
        <span><strong>${formatNumber(active)}</strong><em>active</em></span>
        <span><strong>${formatNumber(gates)}</strong><em>gates</em></span>
        <span><strong>${formatNumber(staged)}</strong><em>staged</em></span>
      </div>
    </div>
    <div class="control-runway-track" aria-label="Priority lane levels">
      ${records.map(renderControlRunwayNode).join("")}
    </div>`;
}

function liveOpsPulseStats(records) {
  const feedItems = state.snapshot?.missionFeed?.items ?? [];
  return [
    { label: "live lanes", value: formatNumber(records.filter((record) => record.latest || record.activeTasks || record.suggestion).length) },
    { label: "latest", value: formatNumber(feedItems.length) },
    { label: "ready asks", value: formatNumber((state.snapshot?.dispatchConsole?.suggestions ?? []).length) },
    { label: "gates", value: formatNumber(records.reduce((sum, record) => sum + record.blockers + record.pending, 0)) },
    { label: "staged", value: formatNumber(state.stagedDispatches.length) },
  ];
}

function renderLiveOpsPulse() {
  if (!el.liveOpsPulse || !state.snapshot) return;
  const records = liveOpsPulseRecords();
  const stats = liveOpsPulseStats(records);
  const focus = records.find((record) => record.lane.id === state.selectedLaneId) ?? records[0];
  const style = focus?.lane ? laneStyle(focus.lane) : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";
  const averagePulse = records.length ? Math.round(records.reduce((sum, record) => sum + record.pulseScore, 0) / records.length) : 0;
  el.liveOpsPulse.innerHTML = `
    <div class="live-ops-visual" style="${style}" aria-hidden="true">
      <img src="./assets/system/live-ops-pulse-20260618.png" alt="" loading="eager" />
      <span class="live-ops-scan"></span>
      <div class="live-ops-core" style="--live-ops-score:${averagePulse}%">
        <strong>${formatNumber(averagePulse)}</strong>
        <span>pulse</span>
      </div>
      <div class="live-ops-beacons">
        ${records
          .slice(0, 8)
          .map(
            (record, index) =>
              `<i class="${escapeHtml(record.mode)}" style="--live-ops-angle:${index * 45}deg; --live-ops-charge:${Math.max(8, record.pulseScore)}%"></i>`
          )
          .join("")}
      </div>
    </div>
    <div class="live-ops-copy" style="${style}">
      <div class="live-ops-head">
        <div>
          <p class="eyebrow">Live Ops Pulse</p>
          <h2>Current runs, gates, sends</h2>
          <p>${escapeHtml(compactText(focus?.summary ?? "A first-screen command pulse for latest movement, blocker gates, bot asks, staged drafts, and active lane work.", 210))}</p>
        </div>
        <span class="badge ${escapeHtml(focus?.mode ?? "ready")}">${escapeHtml(stateLabel(focus?.mode ?? "ready"))}</span>
      </div>
      <div class="live-ops-stats">
        ${stats
          .map(
            (stat) => `
            <span>
              <strong>${escapeHtml(stat.value)}</strong>
              <em>${escapeHtml(stat.label)}</em>
            </span>`
          )
          .join("")}
      </div>
      <div class="live-ops-actions">
        <button class="tool-button" type="button" data-live-ops-action="latest" title="Show latest company events">LATEST</button>
        <button class="tool-button" type="button" data-live-ops-action="gates" title="Show current review gates">GATES</button>
        <button class="tool-button" type="button" data-live-ops-action="comms" title="Jump to the Command Relay Deck">COMMS</button>
        <button class="tool-button" type="button" data-live-ops-action="timeline" title="Jump to Mission Feed playback">TIMELINE</button>
      </div>
      <div class="live-ops-grid" aria-label="Live lane pulses">
        ${records.map(renderLiveOpsPulseCard).join("")}
        ${renderLiveOpsPulseFutureSlots(records)}
      </div>
    </div>`;
}

function renderLiveOpsPulseCard(record) {
  const { lane, bot, latest, mode, pulseScore, staged } = record;
  const botName = bot?.visual?.callsign ?? bot?.agent?.agent_id ?? "unbound bot";
  return `
    <button
      class="live-ops-card ${escapeHtml(mode)} ${staged ? "staged" : ""} ${lane.id === state.selectedLaneId ? "active" : ""}"
      type="button"
      data-live-ops-lane="${escapeHtml(lane.id)}"
      style="${laneStyle(lane)} --live-ops-card-score:${Math.max(8, pulseScore)}%;"
      title="Open this lane trail"
    >
      <div class="live-ops-card-top">
        ${avatarMarkup(lane, "live-ops-avatar")}
        <div>
          <p class="eyebrow">${escapeHtml(stateLabel(mode))}</p>
          <h3>${escapeHtml(compactText(lane.name, 58))}</h3>
          <span>${escapeHtml(compactText(botName, 44))}</span>
        </div>
        <strong>L${formatNumber(lane.level ?? 1)}</strong>
      </div>
      <div class="live-ops-meter" aria-hidden="true"><i></i></div>
      <h4>${escapeHtml(compactText(record.title, 72))}</h4>
      <p>${escapeHtml(compactText(record.summary, 132))}</p>
      <div class="live-ops-card-stats">
        <span><strong>${formatNumber(record.activeTasks)}</strong><em>tasks</em></span>
        <span><strong>${formatNumber(record.blockers + record.pending)}</strong><em>gates</em></span>
        <span><strong>${formatNumber(record.urgency)}</strong><em>ask</em></span>
        <span><strong>${escapeHtml(latest ? stateLabel(latest.kind) : "idle")}</strong><em>latest</em></span>
      </div>
    </button>`;
}

function renderLiveOpsPulseFutureSlots(records) {
  const slots = [
    { label: "live worker feed", detail: "future active worker heartbeat" },
    { label: "approval siren", detail: "future human decision queue" },
    { label: "lane broadcast", detail: "future cross-lane event stream" },
    { label: "profit pulse", detail: "future realized-value ticker" },
  ];
  return slots
    .slice(0, 3)
    .map(
      (slot, index) => `
      <article class="live-ops-future">
        <span></span>
        <strong>${escapeHtml(slot.label)}</strong>
        <p>${escapeHtml(slot.detail)}</p>
        <em>socket ${formatNumber(records.length + index + 1)}</em>
      </article>`
    )
    .join("");
}

function relaySelectedLane() {
  return state.snapshot?.lanes?.find((lane) => lane.id === state.selectedLaneId) ?? state.snapshot?.lanes?.[0] ?? null;
}

function renderSystemRelay() {
  if (!el.systemRelay) return;
  const lane = relaySelectedLane();
  const totals = state.snapshot?.totals ?? {};
  const feedItems = state.snapshot?.missionFeed?.items ?? [];
  const activeAgents = (state.snapshot?.agents ?? []).filter((agent) => agent.status === "active").length;
  const newestEvent = feedItems[0];
  const relayStats = [
    { label: "linked bots", value: formatNumber(activeAgents) },
    { label: "gates watched", value: formatNumber(totals.blockers ?? 0) },
    { label: "route events", value: formatNumber(feedItems.length) },
    { label: "artifact vault", value: formatNumber(totals.artifacts ?? 0) },
  ];
  const nextAction = lane ? chronicleNextAction(lane) : "Select a lane to open its route, command deck, and event history.";
  const laneStyleText = lane ? laneStyle(lane) : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";

  el.systemRelay.innerHTML = `
    <div class="relay-visual" aria-hidden="true">
      <img src="./assets/system/relay-portal-20260617.png" alt="" loading="lazy" />
      <div class="relay-scanline"></div>
    </div>
    <div class="relay-copy" style="${laneStyleText}">
      <p class="eyebrow">Atlas Relay</p>
      <h2>${escapeHtml(lane ? `${lane.name} command route` : "Command route")}</h2>
      <p>${escapeHtml(compactText(nextAction, 190))}</p>
      <div class="relay-stat-grid">
        ${relayStats.map((stat) => `<span><strong>${escapeHtml(stat.value)}</strong><em>${escapeHtml(stat.label)}</em></span>`).join("")}
      </div>
      <div class="relay-actions">
        <button class="tool-button" type="button" data-relay-action="path" title="Open selected lane path map">PATH</button>
        <button class="tool-button" type="button" data-relay-action="comms" title="Open selected lane command deck">COM</button>
        <button class="tool-button" type="button" data-relay-action="feed" title="Show all mission feed records">FEED</button>
        <button class="tool-button" type="button" data-relay-action="assets" title="Show generated system assets">ART</button>
      </div>
      <div class="relay-event-strip">
        <span>${escapeHtml(newestEvent ? stateLabel(newestEvent.kind) : "Waiting")}</span>
        <strong>${escapeHtml(compactText(newestEvent?.title ?? "No mission events yet", 86))}</strong>
      </div>
    </div>`;
}

function worldLoomLanes() {
  const lanes = [...(state.snapshot?.lanes ?? [])].sort((a, b) => b.level - a.level || b.score - a.score || a.name.localeCompare(b.name));
  if (!lanes.length) return [];
  const selectedIndex = Math.max(0, lanes.findIndex((lane) => lane.id === state.selectedLaneId));
  const visibleCount = Math.min(7, lanes.length);
  const start = selectedIndex - Math.floor(visibleCount / 2);
  return Array.from({ length: visibleCount }, (_, offset) => lanes[(start + offset + lanes.length) % lanes.length]);
}

function worldLoomSelectedIndex() {
  const lanes = [...(state.snapshot?.lanes ?? [])].sort((a, b) => b.level - a.level || b.score - a.score || a.name.localeCompare(b.name));
  return Math.max(0, lanes.findIndex((lane) => lane.id === state.selectedLaneId));
}

function worldLoomStep(direction) {
  const lanes = [...(state.snapshot?.lanes ?? [])].sort((a, b) => b.level - a.level || b.score - a.score || a.name.localeCompare(b.name));
  if (!lanes.length) return;
  const currentIndex = worldLoomSelectedIndex();
  const nextIndex = (currentIndex + direction + lanes.length) % lanes.length;
  selectLane(lanes[nextIndex].id, "overview");
}

function worldsLaunchStats() {
  const lanes = state.snapshot?.lanes ?? [];
  const gateCount = lanes.reduce((sum, lane) => sum + (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0), 0);
  const textureCount = lanes.filter((lane) => lane.visual?.minigame?.texture).length;
  const customCount = lanes.filter((lane) => minigameDefinition(lane)).length;
  const stageCount = lanes.reduce((sum, lane) => sum + gameStepCount(lane), 0);
  const realmCount = new Set(lanes.map((lane) => lane.visual?.realm ?? lane.department).filter(Boolean)).size;
  const futureSlots = Math.max(4, Object.keys(MINIGAME_REGISTRY).length + 4 - lanes.length, Math.ceil(lanes.length / 3));
  return { worlds: lanes.length, gates: gateCount, textures: textureCount, custom: customCount, stages: stageCount, realms: realmCount, futureSlots };
}

function worldsLaunchLanes() {
  const lanes = state.snapshot?.lanes ?? [];
  const selected = lanes.find((lane) => lane.id === state.selectedLaneId);
  const ranked = [...lanes].sort((a, b) => {
    const aGate = (a.counts?.blockers ?? 0) + (a.counts?.pendingRequests ?? 0);
    const bGate = (b.counts?.blockers ?? 0) + (b.counts?.pendingRequests ?? 0);
    const customDelta = Number(Boolean(minigameDefinition(b))) - Number(Boolean(minigameDefinition(a)));
    return customDelta || bGate - aGate || b.level - a.level || b.score - a.score || a.name.localeCompare(b.name);
  });
  const laneMap = new Map();
  if (selected) laneMap.set(selected.id, selected);
  ranked.forEach((lane) => {
    if (laneMap.size < 6) laneMap.set(lane.id, lane);
  });
  return [...laneMap.values()];
}

function worldsLaunchActions(stats) {
  return [
    { id: "loom", label: "Loom", value: `${formatNumber(stats.worlds)} worlds`, detail: "lane selector" },
    { id: "arcade", label: "Arcade", value: `${formatNumber(stats.textures)} textures`, detail: "playable modules" },
    { id: "registry", label: "Registry", value: `${formatNumber(stats.custom)} custom`, detail: "renderer coverage" },
    { id: "genesis", label: "Genesis", value: `${formatNumber(stats.futureSlots)} slots`, detail: "new lane path" },
    { id: "library", label: "Assets", value: `${formatNumber(stats.stages)} stages`, detail: "art vault" },
  ];
}

function worldsExpansionPortalSlots(lanes, stats) {
  const moduleStats = {
    worlds: stats.worlds,
    textures: stats.textures,
    custom: stats.custom,
    stages: stats.stages,
    gates: stats.gates,
    slots: stats.futureSlots,
  };
  const families = [
    { id: "discovery", title: "Scout Arcade", action: "arcade", vibe: "fog-of-war test world", accent: "#44d7c9", accentAlt: "#6aa8ff" },
    { id: "build", title: "Builder Trial", action: "genesis", vibe: "prototype lane socket", accent: "#f4ba55", accentAlt: "#8be06e" },
    { id: "market", title: "Market Run", action: "registry", vibe: "offer and proof module", accent: "#ff6f61", accentAlt: "#f4ba55" },
    { id: "risk", title: "Risk Gate", action: "loom", vibe: "blocker boss route", accent: "#6aa8ff", accentAlt: "#44d7c9" },
    { id: "revenue", title: "Payout Loop", action: "library", vibe: "reward asset socket", accent: "#8be06e", accentAlt: "#f4ba55" },
    { id: "platform", title: "Ops Circuit", action: "genesis", vibe: "bot and command slot", accent: "#b48cff", accentAlt: "#44d7c9" },
  ];

  return families.map((family, index) => {
    const lead = lanes[index % Math.max(1, lanes.length)];
    const base = moduleStats[Object.keys(moduleStats)[index % Object.keys(moduleStats).length]] ?? 0;
    const charge = Math.max(14, Math.min(96, 24 + base * 5 + index * 7));
    return {
      ...family,
      lead,
      charge,
      metric: index < 3 ? `${formatNumber(moduleStats.slots)} open` : `${formatNumber(moduleStats.stages)} stages`,
      label: lead ? lead.visual?.realm ?? lead.department : "new realm",
    };
  });
}

function renderWorldsExpansionPortals(lanes, stats) {
  const slots = worldsExpansionPortalSlots(lanes, stats);
  return `
    <div class="worlds-expansion-deck" style="--expansion-art:url('./assets/system/lane-expansion-portal-deck-20260619.png')" aria-label="Expandable lane minigame sockets">
      <div class="worlds-expansion-head">
        <span>Expansion sockets</span>
        <strong>${formatNumber(stats.futureSlots)} ready slots</strong>
      </div>
      <div class="worlds-expansion-track">
        ${slots
          .map(
            (slot, index) => `
              <button
                class="worlds-expansion-portal ${slot.lead ? "seeded" : "empty"}"
                type="button"
                data-worlds-launch-action="${escapeHtml(slot.action)}"
                style="--portal-index:${index}; --portal-charge:${slot.charge}%; --portal-a:${escapeHtml(slot.accent)}; --portal-b:${escapeHtml(slot.accentAlt)};"
                title="${escapeHtml(slot.title)}"
              >
                <span class="worlds-expansion-ring" aria-hidden="true"><i></i></span>
                <strong>${escapeHtml(slot.title)}</strong>
                <em>${escapeHtml(slot.vibe)}</em>
                <small>${escapeHtml(slot.metric)} - ${escapeHtml(slot.label)}</small>
              </button>`
          )
          .join("")}
      </div>
    </div>`;
}

function futureLaneSocketBlueprints(lanes, stats) {
  const agents = state.snapshot?.agents ?? [];
  const botCount = agents.filter((agent) => agent.lane?.id || agent.visual?.avatar).length;
  const proofCount = lanes.reduce(
    (sum, lane) => sum + (lane.counts?.evidence ?? 0) + (lane.counts?.traces ?? 0) + (lane.counts?.outcomes ?? 0) + (lane.counts?.artifacts ?? 0),
    0
  );
  const sockets = [
    {
      id: "lane",
      label: "New Lane",
      value: `+${formatNumber(stats.futureSlots)}`,
      detail: "realm seed",
      action: "genesis",
      tone: "seed",
      charge: Math.min(96, Math.max(22, stats.futureSlots * 12)),
    },
    {
      id: "bot",
      label: "Bot Pod",
      value: formatNumber(botCount),
      detail: "owner slot",
      action: "loom",
      tone: botCount ? "ready" : "seed",
      charge: Math.min(96, Math.max(18, botCount * 8)),
    },
    {
      id: "minigame",
      label: "Mini Game",
      value: `${formatNumber(stats.custom)}/${formatNumber(Math.max(1, stats.worlds))}`,
      detail: "renderer hook",
      action: "registry",
      tone: stats.custom ? "unlocked" : "seed",
      charge: Math.min(96, Math.max(16, Math.round((stats.custom / Math.max(1, stats.worlds)) * 100))),
    },
    {
      id: "asset",
      label: "Asset Kit",
      value: formatNumber(stats.textures),
      detail: "sprite + texture",
      action: "library",
      tone: stats.textures ? "ready" : "seed",
      charge: Math.min(96, Math.max(18, stats.textures * 11)),
    },
    {
      id: "proof",
      label: "Proof Trail",
      value: formatNumber(proofCount),
      detail: "gates + wins",
      action: "arcade",
      tone: proofCount ? "advancing" : "seed",
      charge: Math.min(96, Math.max(20, proofCount * 3 + stats.gates * 5)),
    },
  ];

  return sockets.map((socket, index) => ({
    ...socket,
    index,
    accent: ["#44d7c9", "#6aa8ff", "#f4ba55", "#8be06e", "#ff6f61"][index],
    accentAlt: ["#8be06e", "#b48cff", "#ff6f61", "#44d7c9", "#f4ba55"][index],
  }));
}

function renderFutureLaneSocketBoard(lanes, stats) {
  const sockets = futureLaneSocketBlueprints(lanes, stats);
  return `
    <section class="future-lane-socket-board" aria-label="Future lane creation sockets">
      <div class="future-lane-socket-head">
        <span>Expansion Socket</span>
        <strong>${formatNumber(stats.futureSlots)} open lanes</strong>
      </div>
      <div class="future-lane-socket-track">
        ${sockets
          .map(
            (socket) => `
              <button
                class="future-lane-socket ${escapeHtml(socket.tone)}"
                type="button"
                data-future-lane-socket="${escapeHtml(socket.id)}"
                data-worlds-launch-action="${escapeHtml(socket.action)}"
                style="--socket-index:${socket.index}; --socket-charge:${socket.charge}%; --socket-a:${escapeHtml(socket.accent)}; --socket-b:${escapeHtml(socket.accentAlt)};"
                title="${escapeHtml(socket.label)}"
              >
                <span class="future-lane-socket-ring" aria-hidden="true"><i></i></span>
                <span class="future-lane-socket-copy">
                  <strong>${escapeHtml(socket.label)}</strong>
                  <em>${escapeHtml(socket.detail)}</em>
                </span>
                <b>${escapeHtml(socket.value)}</b>
              </button>`
          )
          .join("")}
      </div>
    </section>`;
}
function worldsExpansionRadarModel(lanes, stats) {
  const agents = state.snapshot?.agents ?? [];
  const assets = visualAssetRecords();
  const gameTextureCount = lanes.filter((lane) => lane.visual?.minigame?.texture).length;
  const botAvatarCount = agents.filter((agent) => agent.visual?.avatar).length;
  const laneAvatarCount = lanes.filter((lane) => lane.visual?.avatar).length;
  const futureCapacity = Math.max(stats.futureSlots, Math.ceil(lanes.length / 2), 4);
  const proofCount = lanes.reduce(
    (sum, lane) => sum + (lane.counts?.evidence ?? 0) + (lane.counts?.traces ?? 0) + (lane.counts?.outcomes ?? 0) + (lane.counts?.artifacts ?? 0),
    0
  );
  const assetCoverage = assets.filter((asset) => ["lane", "game", "agent"].includes(asset.kind)).length;
  const cells = [
    {
      id: "live-worlds",
      label: "Live Worlds",
      value: formatNumber(stats.worlds),
      detail: `${formatNumber(stats.realms)} realms / ${formatNumber(stats.gates)} gates`,
      action: "loom",
      charge: Math.min(96, Math.max(22, Math.round((laneAvatarCount / Math.max(1, stats.worlds)) * 100))),
      accent: "#44d7c9",
      accentAlt: "#8be06e",
    },
    {
      id: "game-seeds",
      label: "Game Seeds",
      value: `${formatNumber(stats.custom)}/${formatNumber(Math.max(1, stats.worlds))}`,
      detail: `${formatNumber(gameTextureCount)} textures / ${formatNumber(stats.stages)} stages`,
      action: "arcade",
      charge: Math.min(96, Math.max(18, Math.round(((stats.custom + gameTextureCount) / Math.max(1, stats.worlds * 2)) * 100))),
      accent: "#6aa8ff",
      accentAlt: "#b48cff",
    },
    {
      id: "bot-pods",
      label: "Bot Pods",
      value: formatNumber(botAvatarCount),
      detail: `${formatNumber(agents.length)} agents / ${formatNumber(assetCoverage)} assets`,
      action: "registry",
      charge: Math.min(96, Math.max(20, Math.round((botAvatarCount / Math.max(1, agents.length || 1)) * 100))),
      accent: "#f4ba55",
      accentAlt: "#ff6f61",
    },
    {
      id: "future-slots",
      label: "Future Slots",
      value: `+${formatNumber(stats.futureSlots)}`,
      detail: `${formatNumber(futureCapacity)} socket capacity / ${formatNumber(proofCount)} proof sparks`,
      action: "genesis",
      charge: Math.min(96, Math.max(24, Math.round((stats.futureSlots / futureCapacity) * 100))),
      accent: "#8be06e",
      accentAlt: "#44d7c9",
    },
  ];

  return cells.map((cell, index) => ({ ...cell, index }));
}

function renderWorldsExpansionRadar(lanes, stats) {
  const cells = worldsExpansionRadarModel(lanes, stats);
  const readiness = Math.round(
    cells.reduce((sum, cell) => sum + cell.charge, 0) / Math.max(1, cells.length)
  );
  return `
    <section class="worlds-expansion-radar" aria-label="World expansion readiness radar" style="--radar-readiness:${readiness}%;">
      <div class="worlds-expansion-radar-core">
        <span>Expansion Radar</span>
        <strong>${formatNumber(readiness)}%</strong>
        <em>live worlds, game seeds, bot pods, asset coverage, and future slots</em>
        <i class="worlds-expansion-radar-orbit" aria-hidden="true"></i>
      </div>
      ${cells
        .map(
          (cell) => `
            <button
              class="worlds-expansion-radar-cell"
              type="button"
              data-worlds-expansion-radar-cell="${escapeHtml(cell.id)}"
              data-worlds-launch-action="${escapeHtml(cell.action)}"
              style="--radar-a:${escapeHtml(cell.accent)}; --radar-b:${escapeHtml(cell.accentAlt)}; --radar-charge:${cell.charge}%; --radar-index:${cell.index};"
              title="${escapeHtml(cell.label)}"
            >
              <span class="worlds-expansion-radar-pip" aria-hidden="true"></span>
              <strong>${escapeHtml(cell.value)}</strong>
              <span>${escapeHtml(cell.label)}</span>
              <em>${escapeHtml(cell.detail)}</em>
            </button>`
        )
        .join("")}
    </section>`;
}
function worldSeedCartridgeRecords(lanes, stats) {
  const current = lanes.slice(0, 5).map((lane, index) => {
    const minigame = lane.visual?.minigame ?? {};
    const definition = minigameDefinition(lane);
    const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
    const stageCount = gameStepCount(lane);
    const texture = Boolean(minigame.texture);
    const charge = Math.min(100, Math.max(12, (texture ? 24 : 0) + (definition ? 28 : 0) + Math.min(32, stageCount * 4) + Math.min(16, lane.level)));
    return {
      lane,
      index,
      title: minigame.title ?? lane.visual?.realm ?? lane.name,
      meta: minigame.mechanic ?? lane.quest?.title ?? "Lane minigame seed",
      label: minigame.id ?? "seed",
      tone: gateCount ? "gated" : definition && texture ? "ready" : "advancing",
      charge,
      action: "arcade",
    };
  });
  const futureCount = Math.min(4, Math.max(2, stats.futureSlots));
  const future = Array.from({ length: futureCount }).map((_, index) => ({
    lane: null,
    index: current.length + index,
    title: ["New World", "Bot Pod", "Mini Game", "Research Gate"][index % 4],
    meta: ["lane visual + texture", "agent owner + sprite", "game renderer hook", "proof gate loop"][index % 4],
    label: "future",
    tone: "future",
    charge: Math.max(12, 22 + index * 11),
    action: index === 2 ? "registry" : "genesis",
  }));
  return [...current, ...future];
}

function renderWorldSeedCartridgeRail(records) {
  return `
    <section class="world-seed-cartridge-rail" aria-label="World seed cartridges">
      <div class="world-seed-cartridge-head">
        <span>Seed Cartridges</span>
        <strong>${formatNumber(records.length)} modules</strong>
      </div>
      <div class="world-seed-cartridge-track">
        ${records
          .map(
            (record) => `
              <button class="world-seed-cartridge ${escapeHtml(record.tone)} ${record.lane?.id === state.selectedLaneId ? "active" : ""}" type="button" ${record.lane ? `data-worlds-launch-lane="${escapeHtml(record.lane.id)}"` : `data-worlds-launch-action="${escapeHtml(record.action)}"`} style="${record.lane ? laneStyle(record.lane) : ""} --seed-index:${record.index}; --seed-charge:${record.charge}%;" title="${escapeHtml(record.title)}">
                <i>${escapeHtml(record.label)}</i>
                <span>
                  <strong>${escapeHtml(compactText(record.title, 34))}</strong>
                  <em>${escapeHtml(compactText(record.meta, 48))}</em>
                </span>
                <b class="world-seed-cartridge-meter" aria-hidden="true"></b>
              </button>`
          )
          .join("")}
      </div>
    </section>`;
}

function renderWorldsLaunch() {
  if (!el.worldsLaunch || !state.snapshot) return;
  const lane = relaySelectedLane();
  const stats = worldsLaunchStats();
  const lanes = worldsLaunchLanes();
  const seedCartridges = worldSeedCartridgeRecords(lanes, stats);
  const style = lane ? laneStyle(lane) : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";
  const nextMove = lane ? compactText(chronicleNextAction(lane), 120) : "Select a world";
  el.worldsLaunch.innerHTML = `
    <div class="worlds-launch-shell" style="${style}">
      <div class="worlds-launch-head">
        <div>
          <p class="eyebrow">Worlds Launch</p>
          <h2>${escapeHtml(lane ? `${lane.visual?.realm ?? lane.department} level select` : "Agent company level select")}</h2>
        </div>
        <div class="worlds-launch-score" aria-label="World readiness">
          <strong>${formatNumber(stats.custom)}/${formatNumber(Math.max(1, stats.worlds))}</strong>
          <span>custom games</span>
        </div>
      </div>
      <div class="worlds-launch-board">
        <div class="worlds-launch-focus">
          ${lane ? avatarMarkup(lane, "worlds-launch-avatar") : ""}
          <div>
            <span>Active world</span>
            <strong>${escapeHtml(lane?.name ?? "No lane selected")}</strong>
            <em>${escapeHtml(nextMove)}</em>
          </div>
        </div>
        <div class="worlds-launch-stats">
          <span><strong>${formatNumber(stats.worlds)}</strong><em>worlds</em></span>
          <span><strong>${formatNumber(stats.realms)}</strong><em>realms</em></span>
          <span><strong>${formatNumber(stats.gates)}</strong><em>gates</em></span>
          <span><strong>${formatNumber(stats.futureSlots)}</strong><em>slots</em></span>
        </div>
        ${renderWorldsExpansionRadar(lanes, stats)}
        ${renderFutureLaneSocketBoard(lanes, stats)}
        ${renderWorldSeedCartridgeRail(seedCartridges)}
      </div>
      <div class="worlds-launch-actions" aria-label="Worlds quick launch">
        ${worldsLaunchActions(stats)
          .map(
            (action) => `
              <button class="worlds-launch-action" type="button" data-worlds-launch-action="${escapeHtml(action.id)}" title="Open ${escapeHtml(action.label)}">
                <span>${escapeHtml(action.label)}</span>
                <strong>${escapeHtml(action.value)}</strong>
                <em>${escapeHtml(action.detail)}</em>
              </button>`
          )
          .join("")}
      </div>
      <div class="worlds-launch-lane-stage">
        ${renderWorldsLaunchRoute(lanes)}
        <div class="worlds-launch-lanes" aria-label="Priority world gates">
          ${lanes.map(renderWorldsLaunchLane).join("")}
        </div>
      </div>
    </div>`;
}

function renderWorldsLaunchRoute(lanes) {
  const activeIndex = Math.max(0, lanes.findIndex((lane) => lane.id === state.selectedLaneId));
  return `
    <div class="worlds-launch-route-map" style="--launch-active-index:${activeIndex}; --launch-node-count:${Math.max(1, lanes.length)};" aria-hidden="true">
      <span class="worlds-launch-route-line"></span>
      <span class="worlds-launch-route-runner"></span>
      ${lanes
        .map((lane, index) => {
          const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
          const position = lanes.length <= 1 ? 50 : Math.round((index / (lanes.length - 1)) * 100);
          return `<span class="worlds-launch-route-node ${lane.id === state.selectedLaneId ? "active" : ""} ${gateCount ? "gated" : "ready"}" style="${laneStyle(lane)} --launch-node-index:${index}; --launch-node-position:${position}%;"></span>`;
        })
        .join("")}
    </div>`;
}

function renderWorldsLaunchLane(lane, index) {
  const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const minigame = lane.visual?.minigame ?? {};
  const custom = Boolean(minigameDefinition(lane));
  const active = lane.id === state.selectedLaneId;
  return `
    <button
      class="worlds-launch-lane ${active ? "active" : ""} ${gateCount ? "gated" : "ready"}"
      type="button"
      data-worlds-launch-lane="${escapeHtml(lane.id)}"
      style="${laneStyle(lane)} --launch-index:${index}; --launch-progress:${Math.max(10, Math.min(100, lane.progress ?? lane.level * 8))}%;"
      title="Open ${escapeHtml(lane.name)}"
    >
      ${avatarMarkup(lane, "worlds-launch-lane-avatar")}
      <span>L${formatNumber(lane.level)}</span>
      <strong>${escapeHtml(lane.name)}</strong>
      <em>${escapeHtml(custom ? minigame.title ?? "custom module" : "checkpoint module")}</em>
      <i>${formatNumber(gateCount)} gates</i>
    </button>`;
}

function renderWorldLoom() {
  if (!el.worldLoom) return;
  const lane = relaySelectedLane();
  const lanes = worldLoomLanes();
  const totals = state.snapshot?.totals ?? {};
  const laneStyleText = lane ? laneStyle(lane) : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";
  const activeActionText = lane ? compactText(chronicleNextAction(lane), 170) : "Select a lane to focus its world card.";
  el.worldLoom.innerHTML = `
    <div class="world-loom-visual" aria-hidden="true">
      <img src="./assets/system/world-loom-portal-20260618.png" alt="" loading="lazy" />
      <span class="world-loom-depth"></span>
    </div>
    <div class="world-loom-copy" style="${laneStyleText}">
      <div class="world-loom-head">
        <div>
          <p class="eyebrow">World Loom</p>
          <h2>${escapeHtml(lane ? `${lane.visual?.realm ?? lane.department} portal` : "Lane world selector")}</h2>
        </div>
        <div class="world-loom-controls">
          <button class="tool-button" type="button" data-world-loom-step="-1" title="Previous world">-</button>
          <button class="tool-button" type="button" data-world-loom-step="1" title="Next world">+</button>
        </div>
      </div>
      <p>${escapeHtml(activeActionText)}</p>
      <div class="world-loom-stats">
        <span><strong>${formatNumber(totals.lanes ?? 0)}</strong><em>worlds</em></span>
        <span><strong>${formatNumber(totals.blockers ?? 0)}</strong><em>gates</em></span>
        <span><strong>${formatNumber(totals.artifacts ?? 0)}</strong><em>assets</em></span>
      </div>
      <div class="world-loom-cards">
        ${lanes.map(renderWorldLoomCard).join("")}
      </div>
      <div class="world-loom-actions">
        <button class="tool-button" type="button" data-world-loom-action="path" title="Open selected lane Path Map">PATH</button>
        <button class="tool-button" type="button" data-world-loom-action="game" title="Open selected lane Game">GAME</button>
        <button class="tool-button" type="button" data-world-loom-action="comms" title="Open selected lane Comms">COM</button>
        <button class="tool-button" type="button" data-world-loom-action="assets" title="Open system assets">ART</button>
      </div>
    </div>`;
}

function renderWorldLoomCard(lane, index) {
  const active = lane.id === state.selectedLaneId;
  const counts = lane.counts ?? {};
  const gateCount = (counts.blockers ?? 0) + (counts.pendingRequests ?? 0);
  return `
    <button
      class="world-loom-card ${active ? "active" : ""} ${gateCount ? "gated" : "ready"}"
      type="button"
      data-world-loom-lane="${escapeHtml(lane.id)}"
      style="${laneStyle(lane)} --loom-index:${index};"
    >
      ${avatarMarkup(lane, "world-loom-avatar")}
      <span class="world-loom-level">L${formatNumber(lane.level)}</span>
      <strong>${escapeHtml(lane.name)}</strong>
      <em>${escapeHtml(lane.visual?.realm ?? lane.department)}</em>
      <span>${formatNumber(gateCount)} gates - ${formatNumber(counts.outcomes ?? 0)} unlocks</span>
    </button>`;
}

function arcadeLanes() {
  return [...(state.snapshot?.lanes ?? [])]
    .filter((lane) => lane.visual?.minigame?.texture)
    .sort((a, b) => {
      const customDelta = Number(Boolean(minigameDefinition(b))) - Number(Boolean(minigameDefinition(a)));
      return customDelta || b.level - a.level || b.score - a.score || a.name.localeCompare(b.name);
    });
}

function arcadeStats(lanes) {
  const customModules = lanes.filter((lane) => minigameDefinition(lane)).length;
  const gatedModules = lanes.filter((lane) => (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0) > 0).length;
  const gameAssets = lanes.filter((lane) => lane.visual?.minigame?.texture).length;
  const coverage = lanes.length ? Math.round((customModules / lanes.length) * 100) : 0;
  return { customModules, gatedModules, gameAssets, coverage };
}

function arcadeStingerType(lane) {
  const id = lane?.visual?.minigame?.id ?? "checkpoint";
  if (/grid|system|baseline|climb/i.test(id)) return "grid";
  if (/foundry|offer|route/i.test(id)) return "route";
  if (/venue|grant|expedition|map/i.test(id)) return "map";
  if (/claim|scope|scout/i.test(id)) return "scan";
  if (/payout|vault|settlement|replay/i.test(id)) return "pulse";
  if (/paper|signal|harvest/i.test(id)) return "drift";
  return "spark";
}

function renderArcadeDeck() {
  if (!el.arcadeDeck) return;
  const lanes = arcadeLanes();
  const lane = relaySelectedLane();
  const stats = arcadeStats(lanes);
  const activeMinigame = lane?.visual?.minigame;
  const laneStyleText = lane ? laneStyle(lane) : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";

  el.arcadeDeck.innerHTML = `
    <div class="arcade-deck-head" style="${laneStyleText}">
      <div>
        <p class="eyebrow">Arcade Deck</p>
        <h2>${escapeHtml(activeMinigame?.title ?? "Lane minigame launcher")}</h2>
        <p>${escapeHtml(compactText(activeMinigame?.mechanic ?? "Browse every lane-specific module, launch the playable surface, or jump to its route and generated texture set.", 190))}</p>
      </div>
      <div class="arcade-stats" aria-label="Minigame coverage">
        <span><strong>${formatNumber(stats.gameAssets)}</strong><em>textures</em></span>
        <span><strong>${formatNumber(stats.customModules)}</strong><em>modules</em></span>
        <span><strong>${formatNumber(stats.gatedModules)}</strong><em>gated</em></span>
        <span><strong>${formatNumber(stats.coverage)}%</strong><em>custom</em></span>
      </div>
    </div>
    <div class="arcade-grid">
      ${lanes.length ? lanes.map(renderArcadeCard).join("") : `<div class="empty-state">Add minigame textures to lane visuals to populate the arcade deck.</div>`}
    </div>`;
}

function renderArcadeCard(lane, index) {
  const minigame = lane.visual?.minigame ?? {};
  const custom = Boolean(minigameDefinition(lane));
  const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const active = lane.id === state.selectedLaneId;
  const moduleCount = gameStepCount(lane);
  const progress = Math.max(8, Math.min(100, lane.progress ?? lane.level * 8));
  const stingerType = arcadeStingerType(lane);
  return `
    <article
      class="arcade-card ${active ? "active" : ""} ${gateCount ? "gated" : "ready"}"
      data-arcade-card-lane="${escapeHtml(lane.id)}"
      data-arcade-stinger="${escapeHtml(stingerType)}"
      style="${laneStyle(lane)} --arcade-index:${index}; --arcade-progress:${progress}%;"
    >
      <div class="arcade-preview">
        <img src="${escapeHtml(minigame.texture)}" alt="" loading="eager" />
        <span class="arcade-stingers" aria-hidden="true">
          <span class="arcade-stinger one"></span>
          <span class="arcade-stinger two"></span>
          <span class="arcade-stinger three"></span>
        </span>
        <span class="arcade-module-badge">${escapeHtml(custom ? "custom module" : "checkpoint module")}</span>
      </div>
      <div class="arcade-card-copy">
        <div class="arcade-title-row">
          ${avatarMarkup(lane, "arcade-avatar")}
          <div>
            <p class="eyebrow">${escapeHtml(lane.visual?.realm ?? lane.department)}</p>
            <h3>${escapeHtml(minigame.title ?? lane.name)}</h3>
          </div>
        </div>
        <p>${escapeHtml(compactText(minigame.mechanic ?? lane.quest?.title ?? lane.nextAction, 122))}</p>
        <div class="arcade-meta">
          <span>L${formatNumber(lane.level)}</span>
          <span>${formatNumber(moduleCount)} stages</span>
          <span>${formatNumber(gateCount)} gates</span>
        </div>
        <div class="arcade-meter" aria-hidden="true"><span></span></div>
        <div class="arcade-card-actions">
          <button class="tool-button" type="button" data-arcade-launch="${escapeHtml(lane.id)}" title="Launch lane minigame">PLAY</button>
          <button class="tool-button" type="button" data-arcade-path="${escapeHtml(lane.id)}" title="Open lane path">PATH</button>
          <button class="tool-button" type="button" data-arcade-asset="${escapeHtml(lane.id)}" title="Show generated game textures">ART</button>
        </div>
      </div>
    </article>`;
}

function minigameRegistryCodexRecords() {
  return arcadeLanes().map((lane) => {
    const minigame = lane.visual?.minigame ?? {};
    const definition = minigameDefinition(lane);
    const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
    const stageCount = gameStepCount(lane);
    const texture = Boolean(minigame.texture);
    const custom = Boolean(definition);
    const readyScore = Math.min(100, (texture ? 28 : 0) + (custom ? 34 : 0) + Math.min(28, stageCount * 4) + Math.min(10, lane.level));
    return {
      lane,
      minigame,
      definition,
      gateCount,
      stageCount,
      texture,
      custom,
      readyScore,
      status: gateCount ? "gated" : custom && texture ? "unlocked" : texture ? "advancing" : "scouting",
    };
  });
}

function minigameRegistryCodexStats(records) {
  const registryIds = Object.keys(MINIGAME_REGISTRY);
  const customCount = records.filter((record) => record.custom).length;
  const textureCount = records.filter((record) => record.texture).length;
  const stageCount = records.reduce((sum, record) => sum + record.stageCount, 0);
  const futureSlots = Math.max(3, registryIds.length + 4 - records.length);
  return [
    { label: "modules", value: formatNumber(records.length) },
    { label: "custom", value: formatNumber(customCount) },
    { label: "textures", value: formatNumber(textureCount) },
    { label: "stages", value: formatNumber(stageCount) },
    { label: "future", value: formatNumber(futureSlots) },
  ];
}

function renderMinigameRegistryCodex() {
  if (!el.minigameRegistryCodex || !state.snapshot) return;
  const records = minigameRegistryCodexRecords();
  const selected = records.find((record) => record.lane.id === state.selectedLaneId) ?? records[0];
  const stats = minigameRegistryCodexStats(records);
  const style = selected?.lane ? laneStyle(selected.lane) : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";
  el.minigameRegistryCodex.innerHTML = `
    <div class="minigame-codex-visual" style="${style}" aria-hidden="true">
      <img src="./assets/system/minigame-registry-codex-20260618.png" alt="" loading="lazy" />
      <span class="minigame-codex-scan"></span>
    </div>
    <div class="minigame-codex-copy" style="${style}">
      <div class="minigame-codex-head">
        <div>
          <p class="eyebrow">Minigame Registry Codex</p>
          <h2>${escapeHtml(selected?.minigame?.title ?? "Lane game modules")}</h2>
          <p>${escapeHtml(compactText(selected?.minigame?.mechanic ?? "A reusable registry for lane-specific games, generated textures, custom renderers, and empty future slots.", 200))}</p>
        </div>
        <span class="badge ${escapeHtml(selected?.status ?? "advancing")}">${escapeHtml(selected?.custom ? "custom renderer" : "texture ready")}</span>
      </div>
      <div class="minigame-codex-stats">
        ${stats
          .map(
            (stat) => `
            <span>
              <strong>${escapeHtml(stat.value)}</strong>
              <em>${escapeHtml(stat.label)}</em>
            </span>`
          )
          .join("")}
      </div>
      <div class="minigame-codex-actions">
        <button class="tool-button" type="button" data-minigame-codex-action="arcade" title="Open Arcade Deck">ARCADE</button>
        <button class="tool-button" type="button" data-minigame-codex-action="assets" title="Show game textures">ASSET</button>
        <button class="tool-button" type="button" data-minigame-codex-action="forge" title="Open Expansion Forge">FORGE</button>
      </div>
      <div class="minigame-codex-grid" aria-label="Registered lane minigames">
        ${records.slice(0, 8).map(renderMinigameRegistryCard).join("")}
        ${renderMinigameRegistryFutureSlots(records)}
      </div>
    </div>`;
}

function renderMinigameRegistryCard(record, index) {
  const { lane, minigame, status, gateCount, stageCount, readyScore } = record;
  return `
    <article
      class="minigame-codex-card ${escapeHtml(status)} ${lane.id === state.selectedLaneId ? "active" : ""}"
      data-minigame-codex-lane="${escapeHtml(lane.id)}"
      style="${laneStyle(lane)} --codex-score:${Math.max(8, readyScore)}%; --codex-index:${index};"
    >
      <div class="minigame-codex-preview">
        <img src="${escapeHtml(minigame.texture ?? lane.visual?.avatar)}" alt="" loading="lazy" />
        <span>${escapeHtml(record.custom ? "custom" : "fallback")}</span>
      </div>
      <div class="minigame-codex-card-copy">
        <p class="eyebrow">${escapeHtml(minigame.id ?? "checkpoint")}</p>
        <h3>${escapeHtml(compactText(minigame.title ?? lane.name, 54))}</h3>
        <p>${escapeHtml(compactText(minigame.mechanic ?? lane.quest?.title ?? lane.nextAction, 108))}</p>
      </div>
      <div class="minigame-codex-meter"><i></i></div>
      <div class="minigame-codex-card-stats">
        <span><strong>${formatNumber(stageCount)}</strong><em>stages</em></span>
        <span><strong>${formatNumber(gateCount)}</strong><em>gates</em></span>
        <span><strong>${formatNumber(lane.level)}</strong><em>level</em></span>
      </div>
    </article>`;
}

function renderMinigameRegistryFutureSlots(records) {
  const futureSlots = Math.max(3, Object.keys(MINIGAME_REGISTRY).length + 4 - records.length);
  return Array.from({ length: Math.min(4, futureSlots) })
    .map(
      (_, index) => `
      <article class="minigame-codex-future" style="--codex-index:${records.length + index};">
        <span>${formatNumber(index + 1)}</span>
        <strong>Future module slot</strong>
        <p>Add lane visual identity, generated game texture, registry hook, renderer, and bot owner.</p>
      </article>`
    )
    .join("");
}

function motionForgeTypes() {
  const lanes = arcadeLanes();
  const groups = new Map();
  lanes.forEach((lane) => {
    const type = arcadeStingerType(lane);
    if (!groups.has(type)) {
      groups.set(type, {
        type,
        lanes: [],
        gates: 0,
        stages: 0,
        custom: 0,
      });
    }
    const group = groups.get(type);
    group.lanes.push(lane);
    group.gates += (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
    group.stages += gameStepCount(lane);
    group.custom += minigameDefinition(lane) ? 1 : 0;
  });
  return [...groups.values()].sort((a, b) => b.lanes.length - a.lanes.length || a.type.localeCompare(b.type));
}

function motionTypeLabel(type) {
  const labels = {
    drift: "Drift",
    grid: "Grid",
    map: "Map",
    pulse: "Pulse",
    route: "Route",
    scan: "Scan",
    spark: "Spark",
  };
  return labels[type] ?? stateLabel(type);
}

function motionTypeSummary(type) {
  const summaries = {
    drift: "Soft lateral signal motion for garden, paper, and harvesting modules.",
    grid: "Structured sweeps for systems, benchmarks, and control-plane modules.",
    map: "Beacon jumps for venue, grant, and expedition routes.",
    pulse: "Expanding rings for vault, replay, and settlement modules.",
    route: "Directional motion for foundry, offer, and deal-route modules.",
    scan: "Fast sweep lines for scout, claim, and scope modules.",
    spark: "Fallback spark for new module ids that need a safe default.",
  };
  return summaries[type] ?? "Reusable transform/opacity motion for module cards.";
}

function renderMotionForge() {
  if (!el.motionForge) return;
  const groups = motionForgeTypes();
  const selectedLane = relaySelectedLane();
  const selectedType = arcadeStingerType(selectedLane);
  const totalLanes = groups.reduce((sum, group) => sum + group.lanes.length, 0);
  const totalStingers = totalLanes * 3;
  const gatedTypes = groups.filter((group) => group.gates > 0).length;
  const laneStyleText = selectedLane ? laneStyle(selectedLane) : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";

  el.motionForge.innerHTML = `
    <div class="motion-forge-head" style="${laneStyleText}">
      <div>
        <p class="eyebrow">Motion Forge</p>
        <h2>${escapeHtml(motionTypeLabel(selectedType))} motion audit</h2>
        <p>${escapeHtml(compactText("A reusable motion-language surface for lane minigames: see which animation personality each path uses, where gates are still pressurized, and how future lanes inherit motion without a custom animation pass.", 230))}</p>
      </div>
      <div class="motion-forge-stats">
        <span><strong>${formatNumber(groups.length)}</strong><em>motion types</em></span>
        <span><strong>${formatNumber(totalLanes)}</strong><em>lane modules</em></span>
        <span><strong>${formatNumber(totalStingers)}</strong><em>live stingers</em></span>
        <span data-motion-contract="reduced"><strong>CSS</strong><em>reduced motion</em></span>
      </div>
    </div>
    <div class="motion-forge-body">
      <article class="motion-forge-orb" style="${laneStyleText}">
        <div class="motion-core-sample ${escapeHtml(selectedType)}" aria-hidden="true">
          <span></span><span></span><span></span>
        </div>
        <div>
          <p class="eyebrow">Selected Lane Signal</p>
          <h3>${escapeHtml(selectedLane?.name ?? "No lane selected")}</h3>
          <p>${escapeHtml(compactText(selectedLane?.visual?.minigame?.mechanic ?? selectedLane?.nextAction ?? "Select a lane to inspect its motion personality.", 180))}</p>
        </div>
        <div class="motion-forge-actions">
          <button class="tool-button" type="button" data-motion-action="arcade" title="Jump to Arcade Deck">ARC</button>
          <button class="tool-button" type="button" data-motion-action="assets" title="Show game texture assets">ART</button>
          <button class="tool-button" type="button" data-motion-action="game" title="Open selected lane game">PLAY</button>
        </div>
      </article>
      <div class="motion-type-grid">
        ${groups.map((group) => renderMotionTypeCard(group, group.type === selectedType)).join("")}
      </div>
    </div>
    <p class="motion-forge-note">${escapeHtml(`${formatNumber(gatedTypes)} motion families include gated lanes; new minigame ids fall back to Spark until a custom personality is added.`)}</p>`;
}

function renderMotionTypeCard(group, active) {
  const leadLane = group.lanes[0];
  return `
    <article class="motion-type-card ${active ? "is-active" : ""}" data-motion-type="${escapeHtml(group.type)}" style="${leadLane ? laneStyle(leadLane) : ""}">
      <div class="motion-sample ${escapeHtml(group.type)}" aria-hidden="true">
        <span></span><span></span><span></span>
      </div>
      <div class="motion-type-copy">
        <p class="eyebrow">${escapeHtml(formatNumber(group.lanes.length))} lanes</p>
        <h3>${escapeHtml(motionTypeLabel(group.type))}</h3>
        <p>${escapeHtml(motionTypeSummary(group.type))}</p>
      </div>
      <div class="motion-type-meta">
        <span>${formatNumber(group.stages)} stages</span>
        <span>${formatNumber(group.gates)} gates</span>
        <span>${formatNumber(group.custom)} custom</span>
      </div>
      <div class="motion-lane-strip">
        ${group.lanes
          .slice(0, 4)
          .map(
            (lane) => `
              <button class="motion-lane-chip ${lane.id === state.selectedLaneId ? "is-active" : ""}" type="button" data-motion-lane="${escapeHtml(lane.id)}" title="Focus ${escapeHtml(lane.name)}">
                ${avatarMarkup(lane, "motion-lane-avatar")}
                <span>${escapeHtml(compactText(lane.name, 30))}</span>
              </button>`
          )
          .join("")}
      </div>
    </article>`;
}

function progressionTier(lane) {
  if ((lane.counts?.blockers ?? 0) > 0 || (lane.counts?.pendingRequests ?? 0) > 0) return "gated";
  if (lane.level >= 10 || (lane.counts?.outcomes ?? 0) >= 8) return "mythic";
  if (lane.progress >= 60 || lane.state === "advancing") return "advancing";
  if ((lane.counts?.evidence ?? 0) > 0 || (lane.counts?.traces ?? 0) > 0) return "scouting";
  return "locked";
}

function progressionCallout(lane) {
  const counts = lane.counts ?? {};
  if ((counts.blockers ?? 0) > 0) return `${counts.blockers} gate lock${counts.blockers === 1 ? "" : "s"}`;
  if ((counts.pendingRequests ?? 0) > 0) return `${counts.pendingRequests} review gate${counts.pendingRequests === 1 ? "" : "s"}`;
  if ((counts.outcomes ?? 0) > 0) return `${counts.outcomes} reward unlock${counts.outcomes === 1 ? "" : "s"}`;
  if ((counts.traces ?? 0) > 0) return `${counts.traces} trace signal${counts.traces === 1 ? "" : "s"}`;
  return "first signal waiting";
}

function renderProgressionConstellation() {
  if (!el.progressionConstellation) return;
  const lanes = [...(state.snapshot?.lanes ?? [])].sort((a, b) => b.level - a.level || b.progress - a.progress || b.score - a.score);
  const maxLevel = Math.max(1, ...lanes.map((lane) => lane.level ?? 1));
  const totalLevel = lanes.reduce((sum, lane) => sum + (lane.level ?? 0), 0);
  const gated = lanes.filter((lane) => (lane.counts?.blockers ?? 0) > 0 || (lane.counts?.pendingRequests ?? 0) > 0).length;
  const customModules = lanes.filter((lane) => Boolean(minigameDefinition(lane))).length;
  const averageProgress = lanes.length ? Math.round(lanes.reduce((sum, lane) => sum + (lane.progress ?? 0), 0) / lanes.length) : 0;
  el.progressionConstellation.innerHTML = `
    <div class="progression-head">
      <div>
        <p class="eyebrow">Progression Constellation</p>
        <h2>Levels, gates, and next unlocks</h2>
      </div>
      <div class="progression-stats">
        <span><strong>${formatNumber(totalLevel)}</strong> total levels</span>
        <span><strong>${formatNumber(customModules)}</strong> custom games</span>
        <span><strong>${formatNumber(gated)}</strong> gated lanes</span>
        <span><strong>${averageProgress}%</strong> average charge</span>
      </div>
    </div>
    <div class="progression-board">
      <div class="progression-axis" aria-hidden="true">
        <span>Scout</span>
        <span>Proof</span>
        <span>Reward</span>
        <span>Scale</span>
      </div>
      <div class="progression-lanes">
        ${lanes.map((lane, index) => renderProgressionLane(lane, index, maxLevel)).join("")}
      </div>
    </div>`;
}

function renderProgressionLane(lane, index, maxLevel) {
  const tier = progressionTier(lane);
  const levelRatio = Math.max(10, Math.min(100, Math.round(((lane.level ?? 1) / maxLevel) * 100)));
  const progress = Math.max(4, Math.min(100, lane.progress ?? 0));
  const counts = lane.counts ?? {};
  return `
    <button
      class="progression-lane ${escapeHtml(tier)} ${lane.id === state.selectedLaneId ? "active" : ""}"
      type="button"
      data-lane-id="${escapeHtml(lane.id)}"
      style="${laneStyle(lane)} --lane-level-ratio:${levelRatio}%; --lane-charge:${progress}%; --lane-index:${index};"
    >
      <span class="progression-lane-rank">${String(index + 1).padStart(2, "0")}</span>
      <span class="progression-orbit" aria-hidden="true">
        <span class="progression-ring"></span>
        ${avatarMarkup(lane, "progression-avatar")}
      </span>
      <span class="progression-lane-copy">
        <strong>${escapeHtml(lane.name)}</strong>
        <em>${escapeHtml(lane.visual?.realm ?? lane.department)}</em>
      </span>
      <span class="progression-level">
        <strong>L${formatNumber(lane.level)}</strong>
        <em>${escapeHtml(stateLabel(tier))}</em>
      </span>
      <span class="progression-meter" aria-hidden="true"><i></i></span>
      <span class="progression-meta">
        <span>${escapeHtml(progressionCallout(lane))}</span>
        <span>${formatNumber(counts.completedTasks ?? 0)} tasks clear</span>
      </span>
    </button>`;
}

function realmFamilyForLane(lane) {
  const text = `${lane.department ?? ""} ${lane.name ?? ""} ${lane.visual?.realm ?? ""}`.toLowerCase();
  if (/platform|engineer|code|security|product|template|plugin/.test(text)) {
    return {
      id: "build-realms",
      title: "Build Realms",
      subtitle: "Systems, products, code, and protected execution paths.",
      tone: "build",
    };
  }
  if (/growth|sales|content|audience|social|lead/.test(text)) {
    return {
      id: "growth-realms",
      title: "Growth Realms",
      subtitle: "Audience loops, offers, social signals, and demand paths.",
      tone: "growth",
    };
  }
  if (/market|trading|quant|prediction|forecast/.test(text)) {
    return {
      id: "market-realms",
      title: "Market Realms",
      subtitle: "Paper trials, forecasts, settlement signals, and research gates.",
      tone: "market",
    };
  }
  if (/revenue|payout|cashflow|bounty|payment/.test(text)) {
    return {
      id: "revenue-realms",
      title: "Revenue Realms",
      subtitle: "Payout proof, bounty claims, and money movement visibility.",
      tone: "revenue",
    };
  }
  if (/source|discover|competition|venture|web3|grant|hackathon|airdrop|prize/.test(text)) {
    return {
      id: "discovery-realms",
      title: "Discovery Realms",
      subtitle: "New opportunity maps, competitions, grants, and exploration loops.",
      tone: "discovery",
    };
  }
  const title = stateLabel(lane.department ?? "Custom Realm");
  return {
    id: `custom-${String(lane.department ?? "realm").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "realm"}`,
    title,
    subtitle: "User-defined expansion pack for future lanes.",
    tone: "custom",
  };
}

function buildRealmPacks() {
  const packs = new Map();
  for (const lane of state.snapshot?.lanes ?? []) {
    const family = realmFamilyForLane(lane);
    if (!packs.has(family.id)) {
      packs.set(family.id, {
        ...family,
        lanes: [],
        levelTotal: 0,
        blockers: 0,
        outcomes: 0,
        artifacts: 0,
        customModules: 0,
      });
    }
    const pack = packs.get(family.id);
    pack.lanes.push(lane);
    pack.levelTotal += lane.level ?? 0;
    pack.blockers += lane.counts?.blockers ?? 0;
    pack.outcomes += lane.counts?.outcomes ?? 0;
    pack.artifacts += lane.counts?.artifacts ?? 0;
    if (minigameDefinition(lane)) pack.customModules += 1;
  }
  return [...packs.values()]
    .map((pack) => ({
      ...pack,
      lanes: pack.lanes.sort((a, b) => b.level - a.level || b.progress - a.progress || b.score - a.score),
      progress: Math.round(pack.lanes.reduce((sum, lane) => sum + (lane.progress ?? 0), 0) / Math.max(pack.lanes.length, 1)),
    }))
    .sort((a, b) => b.levelTotal - a.levelTotal || b.lanes.length - a.lanes.length || a.title.localeCompare(b.title));
}

function renderRealmPacks() {
  if (!el.realmPackPanel) return;
  const packs = buildRealmPacks();
  const selectedPack = packs.find((pack) => pack.lanes.some((lane) => lane.id === state.selectedLaneId));
  const totalBlockers = packs.reduce((sum, pack) => sum + pack.blockers, 0);
  const totalModules = packs.reduce((sum, pack) => sum + pack.customModules, 0);
  el.realmPackPanel.innerHTML = `
    <div class="realm-pack-head">
      <div>
        <p class="eyebrow">Expansion Realms</p>
        <h2>Path packs for future lanes</h2>
      </div>
      <div class="realm-pack-summary">
        <span><strong>${formatNumber(packs.length)}</strong> packs</span>
        <span><strong>${formatNumber(totalModules)}</strong> modules</span>
        <span><strong>${formatNumber(totalBlockers)}</strong> gates</span>
        <span><strong>${escapeHtml(selectedPack?.title ?? "No pack")}</strong> selected</span>
      </div>
    </div>
    <div class="realm-pack-grid">
      ${packs.map(renderRealmPack).join("")}
    </div>`;
}

function renderRealmPack(pack, index) {
  const lead = pack.lanes[0];
  const active = pack.lanes.some((lane) => lane.id === state.selectedLaneId);
  const style = lead ? `${laneStyle(lead)} --realm-index:${index}; --realm-charge:${Math.max(8, pack.progress)}%;` : `--realm-index:${index}; --realm-charge:${Math.max(8, pack.progress)}%;`;
  return `
    <article class="realm-pack ${escapeHtml(pack.tone)} ${active ? "active" : ""}" style="${style}">
      <button class="realm-pack-main" type="button" data-lane-id="${escapeHtml(lead?.id ?? "")}">
        <span class="realm-pack-ring" aria-hidden="true">
          ${pack.lanes.slice(0, 4).map((lane) => avatarMarkup(lane, "realm-pack-avatar")).join("")}
        </span>
        <span class="realm-pack-copy">
          <span class="realm-kicker">${String(index + 1).padStart(2, "0")} / ${escapeHtml(stateLabel(pack.tone))}</span>
          <strong>${escapeHtml(pack.title)}</strong>
          <em>${escapeHtml(pack.subtitle)}</em>
        </span>
        <span class="realm-pack-level">
          <strong>${formatNumber(pack.levelTotal)}</strong>
          <em>levels</em>
        </span>
      </button>
      <div class="realm-pack-meter" aria-hidden="true"><i></i></div>
      <div class="realm-pack-stats">
        <span>${formatNumber(pack.lanes.length)} lanes</span>
        <span>${formatNumber(pack.outcomes)} unlocks</span>
        <span>${formatNumber(pack.blockers)} gates</span>
        <span>${formatNumber(pack.artifacts)} artifacts</span>
      </div>
      <div class="realm-lane-chips">
        ${pack.lanes
          .map(
            (lane) => `
            <button class="realm-lane-chip ${lane.id === state.selectedLaneId ? "active" : ""}" type="button" data-lane-id="${escapeHtml(lane.id)}" style="${laneStyle(lane)}">
              <span>L${formatNumber(lane.level)}</span>
              <strong>${escapeHtml(lane.name)}</strong>
            </button>`
          )
          .join("")}
      </div>
    </article>`;
}

function expansionBlueprints() {
  const packs = buildRealmPacks();
  const currentModuleIds = new Set((state.snapshot?.lanes ?? []).map((lane) => lane.visual?.minigame?.id).filter(Boolean));
  const templates = [
    {
      id: "discovery-scout",
      title: "Opportunity Scout",
      family: "Discovery Realms",
      module: "signal-map",
      mechanic: "Scan new source categories, score promise, and park unsafe actions behind gates.",
      tone: "discovery",
    },
    {
      id: "proof-lab",
      title: "Local Proof Lab",
      family: "Build Realms",
      module: "proof-stack",
      mechanic: "Turn a money path into local evidence, fixtures, and review packets before public action.",
      tone: "build",
    },
    {
      id: "audience-loop",
      title: "Audience Loop",
      family: "Growth Realms",
      module: "signal-loop",
      mechanic: "Track content tests, replies, lead magnets, and conversion gates as a repeatable run.",
      tone: "growth",
    },
    {
      id: "market-sim",
      title: "Market Simulator",
      family: "Market Realms",
      module: "paper-sim",
      mechanic: "Replay paper decisions, settlement checks, risk caps, and no-trade boundaries.",
      tone: "market",
    },
    {
      id: "payout-ladder",
      title: "Payout Ladder",
      family: "Revenue Realms",
      module: "payout-ladder",
      mechanic: "Follow claim readiness, proof state, review locks, payout status, and reinvestment slots.",
      tone: "revenue",
    },
    {
      id: "custom-realm",
      title: "Custom Realm",
      family: "Custom Pack",
      module: "custom-module",
      mechanic: "Start a lane family with its own art, agent, game texture, quest shape, and command deck.",
      tone: "custom",
    },
  ];

  return templates.map((template) => {
    const pack = packs.find((item) => item.title === template.family || item.tone === template.tone);
    const lanes = pack?.lanes ?? [];
    const lead = lanes[0] ?? null;
    const openSlots = Math.max(1, 4 - lanes.length);
    return {
      ...template,
      pack,
      lead,
      laneCount: lanes.length,
      openSlots,
      moduleReady: !currentModuleIds.has(template.module),
      coverage: pack ? Math.round((pack.customModules / Math.max(lanes.length, 1)) * 100) : 0,
      blockers: pack?.blockers ?? 0,
      outcomes: pack?.outcomes ?? 0,
      artifacts: pack?.artifacts ?? 0,
    };
  });
}

function renderExpansionForge() {
  if (!el.expansionForge) return;
  const lanes = state.snapshot?.lanes ?? [];
  const customModules = lanes.filter((lane) => Boolean(minigameDefinition(lane))).length;
  const packs = buildRealmPacks();
  const blueprints = expansionBlueprints();
  const openSlots = blueprints.reduce((sum, blueprint) => sum + blueprint.openSlots, 0);
  el.expansionForge.innerHTML = `
    <div class="forge-head">
      <div>
        <p class="eyebrow">Expansion Forge</p>
        <h2>Future lanes and minigame slots</h2>
      </div>
      <div class="forge-summary">
        <span><strong>${formatNumber(lanes.length)}</strong> lanes live</span>
        <span><strong>${formatNumber(customModules)}</strong> games wired</span>
        <span><strong>${formatNumber(packs.length)}</strong> realm packs</span>
        <span><strong>${formatNumber(openSlots)}</strong> open slots</span>
      </div>
    </div>
    <div class="forge-grid">
      ${blueprints.map(renderExpansionBlueprint).join("")}
    </div>`;
}

function renderExpansionBlueprint(blueprint) {
  const lane = blueprint.lead;
  const style = lane
    ? `${laneStyle(lane)} --forge-charge:${Math.max(8, blueprint.coverage)}%;`
    : `--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55; --forge-charge:${Math.max(8, blueprint.coverage)}%;`;
  return `
    <article class="forge-card ${escapeHtml(blueprint.tone)} ${lane?.id === state.selectedLaneId ? "active" : ""}" style="${style}">
      <div class="forge-card-top">
        <span class="forge-emblem" aria-hidden="true"><i></i></span>
        <div>
          <p class="eyebrow">${escapeHtml(blueprint.family)}</p>
          <h3>${escapeHtml(blueprint.title)}</h3>
        </div>
        <strong>${formatNumber(blueprint.openSlots)}</strong>
      </div>
      <p>${escapeHtml(blueprint.mechanic)}</p>
      <div class="forge-meter" aria-hidden="true"><i></i></div>
      <div class="forge-stats">
        <span>${formatNumber(blueprint.laneCount)} lanes</span>
        <span>${formatNumber(blueprint.coverage)}% game cover</span>
        <span>${formatNumber(blueprint.blockers)} gates</span>
        <span>${formatNumber(blueprint.outcomes)} unlocks</span>
      </div>
      <div class="forge-checklist">
        <span class="${blueprint.moduleReady ? "ready" : "used"}">${escapeHtml(blueprint.module)} id</span>
        <span>lane visual</span>
        <span>game texture</span>
        <span>agent portrait</span>
      </div>
      <div class="forge-actions">
        <button class="tool-button" type="button" ${lane ? `data-forge-lane-id="${escapeHtml(lane.id)}" title="Open the nearest existing lane in this expansion family"` : `disabled title="Add this lane family by creating a new lane JSON entry"`}>${lane ? "OPEN" : "LOCK"}</button>
      </div>
    </article>`;
}

function laneGenesisFoundryRecords() {
  const agents = state.snapshot?.agents ?? [];
  return expansionBlueprints().map((blueprint, index) => {
    const lane = blueprint.lead;
    const owner = lane ? agents.find((agent) => agent.lane?.id === lane.id) : null;
    const hasLaneArt = Boolean(lane?.visual?.avatar);
    const hasGameTexture = Boolean(lane?.visual?.minigame?.texture);
    const hasGameModule = Boolean(lane && minigameDefinition(lane));
    const hasBotSocket = Boolean(owner?.visual?.avatar || owner);
    const proofCount = (lane?.counts?.evidence ?? 0) + (lane?.counts?.traces ?? 0) + (lane?.counts?.outcomes ?? 0);
    const hasProofTrail = proofCount > 0 || blueprint.outcomes > 0 || blueprint.artifacts > 0;
    const steps = [
      {
        id: "lane",
        label: "lane seed",
        ready: Boolean(lane),
        value: lane ? lane.name : "future lane",
      },
      {
        id: "art",
        label: "art kit",
        ready: hasLaneArt && hasGameTexture,
        value: hasLaneArt && hasGameTexture ? "avatar + texture" : "needs art",
      },
      {
        id: "game",
        label: "minigame",
        ready: hasGameModule,
        value: hasGameModule ? lane.visual.minigame.title : blueprint.module,
      },
      {
        id: "bot",
        label: "bot socket",
        ready: hasBotSocket,
        value: owner?.visual?.callsign ?? owner?.name ?? "unbound",
      },
      {
        id: "proof",
        label: "proof path",
        ready: hasProofTrail,
        value: `${formatNumber(proofCount)} signals`,
      },
    ];
    const readyCount = steps.filter((step) => step.ready).length;
    const readiness = Math.round((readyCount / steps.length) * 100);
    const mode = !lane ? "open" : readiness >= 90 ? "ready" : blueprint.blockers > 0 ? "gated" : "wired";
    return {
      ...blueprint,
      index,
      owner,
      proofCount,
      steps,
      readyCount,
      readiness,
      mode,
      slotLabel: lane ? `L${formatNumber(lane.level)}` : `S${String(index + 1).padStart(2, "0")}`,
    };
  });
}

function laneGenesisFoundryStats(records) {
  const liveRecords = records.filter((record) => Boolean(record.lead));
  return [
    ["Blueprints", records.length],
    ["Open slots", records.reduce((sum, record) => sum + record.openSlots, 0)],
    ["Game modules", liveRecords.filter((record) => record.steps.find((step) => step.id === "game")?.ready).length],
    ["Art kits", liveRecords.filter((record) => record.steps.find((step) => step.id === "art")?.ready).length],
    ["Bot sockets", liveRecords.filter((record) => record.steps.find((step) => step.id === "bot")?.ready).length],
  ];
}

function renderLaneGenesisFoundry() {
  if (!el.laneGenesisFoundry) return;
  const records = laneGenesisFoundryRecords();
  const stats = laneGenesisFoundryStats(records);
  const averageReadiness = records.length
    ? Math.round(records.reduce((sum, record) => sum + record.readiness, 0) / records.length)
    : 0;
  el.laneGenesisFoundry.innerHTML = `
    <div class="lane-genesis-visual" aria-hidden="true">
      <img src="./assets/system/lane-genesis-foundry-20260618.png" alt="" loading="eager" />
      <span class="lane-genesis-scan"></span>
      <div class="lane-genesis-orbit">
        ${records
          .slice(0, 6)
          .map(
            (record) =>
              `<i class="${escapeHtml(record.mode)}" style="--genesis-angle:${record.index * 60}deg; --genesis-charge:${Math.max(12, record.readiness)}%"></i>`
          )
          .join("")}
      </div>
    </div>
    <div class="lane-genesis-copy">
      <div class="lane-genesis-head">
        <div>
          <p class="eyebrow">Lane Genesis Foundry</p>
          <h2>Reusable launch pipeline for new worlds</h2>
          <p>Blueprint each new lane as a playable path: seed the data, forge art, wire a minigame, bind a bot, and prove the trail before it graduates.</p>
        </div>
        <div class="lane-genesis-readiness" style="--genesis-readiness:${averageReadiness}%">
          <strong>${formatNumber(averageReadiness)}%</strong>
          <span>company setup</span>
        </div>
      </div>
      <div class="lane-genesis-stats">
        ${stats
          .map(
            ([label, value]) => `
              <span>
                <strong>${formatNumber(value)}</strong>
                <em>${escapeHtml(label)}</em>
              </span>`
          )
          .join("")}
      </div>
      <div class="lane-genesis-actions">
        <button class="tool-button" type="button" data-lane-genesis-action="forge" title="Jump to the Expansion Forge blueprint cards">FORGE</button>
        <button class="tool-button" type="button" data-lane-genesis-action="games" title="Jump to the Minigame Registry Codex">GAMES</button>
        <button class="tool-button" type="button" data-lane-genesis-action="assets" title="Show all generated art in the Visual Asset Vault">ASSETS</button>
        <button class="tool-button" type="button" data-lane-genesis-action="bots" title="Jump to the Operator Roster">BOTS</button>
      </div>
    </div>
    <div class="lane-genesis-grid">
      ${records.map(renderLaneGenesisCard).join("")}
      ${renderLaneGenesisFutureSlots(records)}
    </div>`;
}

function renderLaneGenesisCard(record) {
  const lane = record.lead;
  const style = lane
    ? `${laneStyle(lane)} --genesis-card-charge:${Math.max(6, record.readiness)}%;`
    : `--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55; --genesis-card-charge:${Math.max(6, record.readiness)}%;`;
  const content = `
      <div class="lane-genesis-card-top">
        <span>${escapeHtml(record.slotLabel)}</span>
        <div>
          <p class="eyebrow">${escapeHtml(record.family)}</p>
          <h3>${escapeHtml(record.title)}</h3>
        </div>
        <strong>${escapeHtml(record.mode)}</strong>
      </div>
      <p>${escapeHtml(record.mechanic)}</p>
      <div class="lane-genesis-meter" aria-hidden="true"><i></i></div>
      <div class="lane-genesis-step-row">
        ${record.steps
          .map(
            (step) => `
              <span class="${step.ready ? "ready" : "pending"}">
                <em>${escapeHtml(step.label)}</em>
                <strong>${escapeHtml(compactText(step.value, 34))}</strong>
              </span>`
          )
          .join("")}
      </div>
      <div class="lane-genesis-card-stats">
        <span>${formatNumber(record.openSlots)} slots</span>
        <span>${formatNumber(record.blockers)} gates</span>
        <span>${formatNumber(record.proofCount)} proof</span>
      </div>`;

  if (!lane) {
    return `<article class="lane-genesis-card open" style="${style}" data-lane-genesis-blueprint="${escapeHtml(record.id)}">${content}</article>`;
  }

  return `
    <button class="lane-genesis-card interactive ${lane.id === state.selectedLaneId ? "active" : ""} ${escapeHtml(record.mode)}" type="button" style="${style}" data-lane-genesis-lane="${escapeHtml(lane.id)}" data-lane-genesis-blueprint="${escapeHtml(record.id)}" title="Open this lane's game view">
      ${content}
    </button>`;
}

function renderLaneGenesisFutureSlots(records) {
  const slots = records.flatMap((record) =>
    Array.from({ length: Math.min(record.openSlots, 2) }, (_, index) => ({
      id: `${record.id}-${index}`,
      family: record.family,
      module: record.module,
      label: `${record.title} +${index + 1}`,
    }))
  );
  return slots
    .slice(0, 8)
    .map(
      (slot, index) => `
        <article class="lane-genesis-future" data-lane-genesis-blueprint="${escapeHtml(slot.id)}" style="--future-index:${index}">
          <span></span>
          <div>
            <p class="eyebrow">${escapeHtml(slot.family)}</p>
            <h3>${escapeHtml(slot.label)}</h3>
            <p>${escapeHtml(slot.module)} module socket waiting for lane data, generated art, bot owner, and proof trail.</p>
          </div>
        </article>`
    )
    .join("");
}

function creatorKitSteps() {
  const lanes = state.snapshot?.lanes ?? [];
  const agents = state.snapshot?.agents ?? [];
  const customGames = lanes.filter((lane) => Boolean(minigameDefinition(lane))).length;
  const visualLanes = lanes.filter((lane) => Boolean(lane.visual?.avatar && lane.visual?.minigame?.texture)).length;
  const mappedAgents = agents.filter((agent) => Boolean(agent.visual?.avatar)).length;
  const systemAssets = visualAssetRecords().filter((asset) => asset.kind === "system").length;
  return [
    {
      id: "seed",
      title: "Seed A Lane",
      kicker: "Data Gate",
      status: lanes.length ? "ready" : "empty",
      charge: Math.min(100, lanes.length * 8),
      metric: `${formatNumber(lanes.length)} live`,
      copy: "Start with lane identity, department, owner, promotion gates, and one local-only task.",
      files: ["state/agent_company.sqlite", "tools/agent_company.py", "web/data/snapshot.json"],
      unlock: "A clickable path appears across map, relay, feed, and detail tabs.",
      action: "forge",
      button: "FORGE",
    },
    {
      id: "visuals",
      title: "Forge Visual Identity",
      kicker: "Art Gate",
      status: visualLanes >= lanes.length ? "complete" : "active",
      charge: lanes.length ? Math.round((visualLanes / lanes.length) * 100) : 0,
      metric: `${formatNumber(visualLanes)}/${formatNumber(lanes.length)}`,
      copy: "Add lane avatar, realm name, accent colors, minigame texture, and optional shared system art.",
      files: ["web/data/lane-visuals.json", "web/assets/lanes/", "web/assets/games/", "web/assets/system/"],
      unlock: "The lane gains an avatar, map glow, Path Map backdrop, asset card, and game-world feel.",
      action: "assets",
      button: "ART",
    },
    {
      id: "game",
      title: "Wire A Minigame",
      kicker: "Module Gate",
      status: customGames >= lanes.length ? "complete" : "active",
      charge: lanes.length ? Math.round((customGames / lanes.length) * 100) : 0,
      metric: `${formatNumber(customGames)} wired`,
      copy: "Assign a minigame id, add a renderer/count hook, and let checkpoints become play states.",
      files: ["web/app.js", "MINIGAME_REGISTRY", "web/games/README.md"],
      unlock: "The Game tab becomes a lane-specific module instead of the generic checkpoint board.",
      action: "path",
      button: "PATH",
    },
    {
      id: "bot",
      title: "Bind The Bot",
      kicker: "Comms Gate",
      status: mappedAgents >= agents.length ? "complete" : "active",
      charge: agents.length ? Math.round((mappedAgents / agents.length) * 100) : 0,
      metric: `${formatNumber(mappedAgents)} portraits`,
      copy: "Map agent portrait, callsign, specialty, lane ownership, and safe local command drafts.",
      files: ["web/data/agent-visuals.json", "web/assets/agents/", "snapshot.dispatchConsole"],
      unlock: "The bot receives a command card, Comms roster identity, and queueable local asks.",
      action: "comms",
      button: "COM",
    },
    {
      id: "template",
      title: "Ship The Template",
      kicker: "Repo Gate",
      status: "ready",
      charge: Math.min(100, Math.round((systemAssets / 6) * 100)),
      metric: `${formatNumber(systemAssets)} system`,
      copy: "Keep the frontend static, preserve the snapshot contract, and publish a repo others can fork.",
      files: ["web/README.md", "tools/generate_visual_dashboard_snapshot.py", "web/data/*.json"],
      unlock: "A new agent company can replace the database and reports while keeping the same Atlas.",
      action: "feed",
      button: "FEED",
    },
  ];
}

function renderCreatorKit() {
  if (!el.creatorKit) return;
  const steps = creatorKitSteps();
  const averageCharge = steps.length ? Math.round(steps.reduce((sum, step) => sum + step.charge, 0) / steps.length) : 0;
  const completeSteps = steps.filter((step) => step.status === "complete" || step.status === "ready").length;
  el.creatorKit.innerHTML = `
    <div class="creator-kit-head">
      <div>
        <p class="eyebrow">Creator Kit</p>
        <h2>Standalone agent-company starter path</h2>
        <p>Use these build gates to add a new lane, visual identity, game module, bot owner, and publishable repo shape.</p>
      </div>
      <div class="creator-kit-score" style="--creator-charge:${averageCharge}%">
        <strong>${formatNumber(averageCharge)}%</strong>
        <span>${formatNumber(completeSteps)} / ${formatNumber(steps.length)} gates</span>
      </div>
    </div>
    <div class="creator-kit-track">
      ${steps.map(renderCreatorKitStep).join("")}
    </div>`;
}

function renderCreatorKitStep(step, index) {
  return `
    <article class="creator-step ${escapeHtml(step.status)}" style="--creator-index:${index}; --creator-charge:${Math.max(6, step.charge)}%">
      <div class="creator-step-top">
        <span>${String(index + 1).padStart(2, "0")}</span>
        <div>
          <p class="eyebrow">${escapeHtml(step.kicker)}</p>
          <h3>${escapeHtml(step.title)}</h3>
        </div>
        <strong>${escapeHtml(step.metric)}</strong>
      </div>
      <p>${escapeHtml(step.copy)}</p>
      <div class="creator-meter" aria-hidden="true"><i></i></div>
      <div class="creator-file-grid">
        ${step.files.map((file) => `<span>${escapeHtml(file)}</span>`).join("")}
      </div>
      <div class="creator-unlock">
        <em>Unlock</em>
        <span>${escapeHtml(step.unlock)}</span>
      </div>
      <button class="tool-button" type="button" data-creator-action="${escapeHtml(step.action)}" title="Open related Atlas surface">${escapeHtml(step.button)}</button>
    </article>`;
}

function renderAchievementWall() {
  if (!el.achievementWall) return;
  const trophies = collectibleOutcomes(12);
  const tracks = laneTrophyTracks(6);
  const outcomeTotal = state.snapshot.totals?.outcomes ?? trophies.length;
  const filteredTotal = trophyOutcomeCountForFilters();
  if (el.achievementWallCount) {
    el.achievementWallCount.textContent =
      state.trophyTierFilter === "all" && state.trophyLaneFilter === "all"
        ? `${formatNumber(outcomeTotal)} unlocks`
        : `${formatNumber(filteredTotal)} shown`;
  }
  if (el.trophyTierFilters) {
    el.trophyTierFilters.innerHTML = trophyTiers()
      .map(
        (tier) => `
          <button class="trophy-tier-chip ${state.trophyTierFilter === tier ? "active" : ""}" type="button" data-trophy-tier="${escapeHtml(tier)}">
            <span>${escapeHtml(stateLabel(tier))}</span>
          </button>`
      )
      .join("");
  }
  if (el.trophyLaneFilter) {
    el.trophyLaneFilter.innerHTML = [
      `<option value="all">All lanes</option>`,
      ...state.snapshot.lanes.map((lane) => `<option value="${escapeHtml(lane.id)}">${escapeHtml(lane.name)}</option>`),
    ].join("");
    el.trophyLaneFilter.value = state.trophyLaneFilter;
  }
  const trophyCards = trophies
    .map(({ item, scene, lane, rank, tier }) => {
      const progress = Math.min(100, Math.round(((lane?.counts?.outcomes ?? 0) / Math.max(outcomeTotal, 1)) * 240));
      const isNewest = rank === 1;
      return `
        <article class="trophy-card ${escapeHtml(tier)} ${isNewest ? "new-unlock" : ""}" data-feed-lane-id="${escapeHtml(item.laneId)}" data-trophy-tier="${escapeHtml(tier)}" style="${feedSceneStyle(scene)}">
          <div class="trophy-medal" aria-hidden="true">
            <span>${formatNumber(rank)}</span>
            ${trophyMedalArt(scene, item, tier)}
          </div>
          <div class="trophy-copy">
            <div class="trophy-kicker">
              <span>${escapeHtml(tier)}</span>
              <strong>+${formatNumber(scene.xp)} xp</strong>
              ${isNewest ? `<em>new unlock</em>` : ""}
            </div>
            <h3>${escapeHtml(item.title)}</h3>
            <p>${escapeHtml(compactText(item.summary, 145))}</p>
            <div class="trophy-meta">
              <span>${escapeHtml(item.laneName)}</span>
              <span>${escapeHtml(shortDate(item.time))}</span>
            </div>
            <div class="trophy-progress" style="--trophy-progress:${progress}%"><i></i></div>
            <button class="trophy-open" type="button" data-feed-lane-id="${escapeHtml(item.laneId)}">Open trail</button>
          </div>
        </article>`;
    })
    .join("");
  const trackCards = tracks
    .map((lane) => {
      const outcomes = lane.counts?.outcomes ?? 0;
      const progress = Math.min(100, Math.round((outcomes / Math.max(outcomeTotal, 1)) * 200));
      return `
        <button class="trophy-track" type="button" data-lane-id="${escapeHtml(lane.id)}" style="${laneStyle(lane)}">
          ${avatarMarkup(lane, "trophy-track-avatar")}
          <span>
            <strong>${escapeHtml(lane.name)}</strong>
            <em>${formatNumber(outcomes)} outcomes - Level ${escapeHtml(lane.level)}</em>
          </span>
          <i style="--track-progress:${progress}%"></i>
        </button>`;
    })
    .join("");
  el.achievementWall.innerHTML = `
    <div class="trophy-showcase">
      ${trophyCards || `<div class="dispatch-empty compact"><p>No trophies match this lens.</p></div>`}
    </div>
    <aside class="trophy-lane-board">
      <p class="eyebrow">Lane Trophy Tracks</p>
      ${trackCards}
    </aside>`;
}

function setTrophyTierFilter(tier) {
  if (!trophyTiers().includes(tier)) return;
  state.trophyTierFilter = tier;
  writeTrophyFilters();
  renderAchievementWall();
}

function setTrophyLaneFilter(laneId) {
  if (laneId !== "all" && !state.snapshot.lanes.some((lane) => lane.id === laneId)) return;
  state.trophyLaneFilter = laneId;
  writeTrophyFilters();
  renderAchievementWall();
}

function dismissUnlockToast() {
  if (state.unlockToastTimer) {
    window.clearTimeout(state.unlockToastTimer);
    state.unlockToastTimer = null;
  }
  state.unlockToast = null;
  renderUnlockToast();
}

function renderUnlockToast() {
  if (!el.unlockToast) return;
  if (state.unlockToastTimer) {
    window.clearTimeout(state.unlockToastTimer);
    state.unlockToastTimer = null;
  }
  const item = state.unlockToast;
  if (!item) {
    el.unlockToast.hidden = true;
    el.unlockToast.innerHTML = "";
    state.unlockToastHold = false;
    return;
  }
  const scene = feedSceneForItem(item);
  const tier = trophyTierForOutcome(item, 0);
  el.unlockToast.hidden = false;
  el.unlockToast.innerHTML = `
    <div class="unlock-toast-art" style="${feedSceneStyle(scene)}">
      ${trophyMedalArt(scene, item, tier)}
    </div>
    <div class="unlock-toast-copy">
      <p class="eyebrow">Achievement Unlocked</p>
      <h3>${escapeHtml(item.title)}</h3>
      <p>${escapeHtml(compactText(item.summary, 96))}</p>
      <div class="unlock-toast-meta">
        <span>${escapeHtml(tier)}</span>
        <span>+${formatNumber(scene.xp)} xp</span>
        <span>${escapeHtml(item.laneName)}</span>
      </div>
      <div class="unlock-toast-actions">
        <button class="trophy-open" type="button" data-feed-lane-id="${escapeHtml(item.laneId)}">Open trail</button>
        <button class="tool-button" type="button" data-unlock-toast="dismiss" title="Dismiss unlock notification">OK</button>
      </div>
    </div>`;
  state.unlockToastTimer = window.setTimeout(dismissUnlockToast, state.unlockToastHold ? 60000 : 7600);
}

function dispatchSuggestions() {
  return (state.snapshot.dispatchConsole?.suggestions ?? []).slice(0, 8);
}

function dispatchTone(kind) {
  if (kind === "gate_review") return "gated";
  if (kind === "promotion") return "unlocked";
  if (kind === "progress_check") return "advancing";
  return "scouting";
}

function renderDispatchConsole() {
  const suggestions = dispatchSuggestions();
  el.dispatchCount.textContent = `${formatNumber(state.stagedDispatches.length)} staged`;
  el.dispatchSuggestionCount.textContent = `${formatNumber(suggestions.length)} ready`;
  el.dispatchSuggestionList.innerHTML = suggestions.map(renderDispatchSuggestion).join("");
  el.dispatchOutboxList.innerHTML = state.stagedDispatches.length
    ? state.stagedDispatches.map(renderDispatchOutboxItem).join("")
    : `<div class="dispatch-empty">
        <p class="eyebrow">Queue Empty</p>
        <h3>No staged drafts</h3>
        <p>Stage a suggested send or open a lane Comms deck to create a local command draft.</p>
      </div>`;
  renderDispatchBatches();
  renderDispatchHistory();
  renderLiveOpsPulse();
  renderCommandRelayDeck();
  renderCompanyQuestBoard();
  renderThreadNexus();
  renderCrewBridge();
  renderBotCommandMatrix();
}

function renderDispatchSuggestion(item) {
  const staged = state.stagedDispatches.some((draft) => draft.sourceId === item.id && draft.command === item.command);
  return `
    <article class="dispatch-card ${escapeHtml(item.kind)}" data-dispatch-lane-id="${escapeHtml(item.laneId)}">
      <div class="dispatch-card-top">
        <span class="badge ${escapeHtml(dispatchTone(item.kind))}">${escapeHtml(stateLabel(item.kind))}</span>
        <strong>${formatNumber(item.urgency)}</strong>
      </div>
      <h3>${escapeHtml(item.title)}</h3>
      <p>${escapeHtml(compactText(item.reason, 150))}</p>
      <div class="dispatch-meter" style="--dispatch-urgency:${Math.min(100, Math.max(0, item.urgency ?? 0))}%"><span></span></div>
      <div class="dispatch-card-bottom">
        <span>${escapeHtml(item.laneName)}</span>
        <button class="tool-button" type="button" data-stage-dispatch="${escapeHtml(item.id)}" title="Stage command draft">${staged ? "OK" : "Q"}</button>
      </div>
    </article>`;
}

function renderDispatchOutboxItem(item) {
  const copied = state.copiedDispatchFor === item.id;
  return `
    <article class="outbox-card ${escapeHtml(item.kind)}" data-dispatch-lane-id="${escapeHtml(item.laneId)}">
      <div class="dispatch-card-top">
        <span class="badge ${escapeHtml(dispatchTone(item.kind))}">${escapeHtml(item.laneName)}</span>
        <span>${escapeHtml(shortDate(item.stagedAt))}</span>
      </div>
      <h3>${escapeHtml(item.title)}</h3>
      <p>${escapeHtml(compactText(item.command, 180))}</p>
      <div class="outbox-actions">
        <button class="tool-button" type="button" data-copy-dispatch="${escapeHtml(item.id)}" title="Copy staged command">${copied ? "OK" : "C"}</button>
        <button class="tool-button" type="button" data-remove-dispatch="${escapeHtml(item.id)}" title="Archive staged command">X</button>
      </div>
    </article>`;
}

function groupedDispatches() {
  return state.stagedDispatches.reduce((groups, item) => {
    const key = item.kind ?? "draft";
    groups[key] = groups[key] ?? [];
    groups[key].push(item);
    return groups;
  }, {});
}

function renderDispatchBatches() {
  const groups = groupedDispatches();
  const keys = Object.keys(groups);
  el.dispatchBatchCount.textContent = state.stagedDispatches.length
    ? `${formatNumber(state.stagedDispatches.length)} drafts`
    : "0 lanes";
  el.dispatchBatchList.innerHTML = keys.length
    ? keys
        .map((kind) => {
          const drafts = groups[kind];
          return `
            <article class="batch-group ${escapeHtml(kind)}">
              <div class="dispatch-card-top">
                <span class="badge ${escapeHtml(dispatchTone(kind))}">${escapeHtml(stateLabel(kind))}</span>
                <strong>${formatNumber(drafts.length)}</strong>
              </div>
              <div class="batch-lanes">
                ${drafts.map((draft) => `<button type="button" data-dispatch-lane-id="${escapeHtml(draft.laneId)}">${escapeHtml(draft.laneName)}</button>`).join("")}
              </div>
            </article>`;
        })
        .join("")
    : `<div class="dispatch-empty compact">
        <p class="eyebrow">No Batch</p>
        <h3>Stage commands first</h3>
        <p>Use T3 or ALL to build a local command batch from current suggestions.</p>
      </div>`;
  if (state.manualCopyBuffer) {
    el.dispatchBatchList.innerHTML += `
      <article class="batch-copy-buffer">
        <div class="dispatch-card-top">
          <span class="badge gated">Manual Copy</span>
          <strong>${formatNumber(state.manualCopyBuffer.length)}</strong>
        </div>
        <p>Automatic clipboard access was unavailable. Select this buffer manually if needed.</p>
        <pre>${escapeHtml(state.manualCopyBuffer)}</pre>
      </article>`;
  }
}

function renderDispatchHistory() {
  el.dispatchHistoryCount.textContent = `${formatNumber(state.dispatchHistory.length)} events`;
  el.dispatchHistoryList.innerHTML = state.dispatchHistory.length
    ? state.dispatchHistory
        .slice(0, 8)
        .map(
          (item) => `
          <article class="history-row">
            <span>${escapeHtml(shortDate(item.time))}</span>
            <div>
              <h3>${escapeHtml(stateLabel(item.action))}</h3>
              <p>${escapeHtml(item.count > 1 ? `${item.count} drafts - ${item.title}` : `${item.laneName} - ${item.title}`)}</p>
            </div>
          </article>`
        )
        .join("")
    : `<div class="dispatch-empty compact">
        <p class="eyebrow">Quiet</p>
        <h3>No local actions yet</h3>
        <p>Stage, copy, or archive drafts to build a local operator trace.</p>
      </div>`;
}

function commandRelayDeckRecords() {
  return botCommandRecords()
    .map((record, index) => {
      const lane = record.lane;
      const suggestion = record.suggestion ?? (lane ? laneDispatchSuggestion(lane) : null);
      const staged = state.stagedDispatches.some((draft) => draft.laneId === lane?.id || draft.sourceId === suggestion?.id);
      const history = state.dispatchHistory.find((item) => item.laneId === lane?.id) ?? null;
      const urgency = suggestion?.urgency ?? 0;
      const gates = record.blockers + record.pending;
      const relayScore = urgency + gates * 18 + (staged ? 14 : 0) + (history ? 4 : 0);
      return {
        ...record,
        index,
        suggestion,
        staged,
        history,
        gates,
        relayScore,
        mode: staged ? "staged" : gates ? "gated" : suggestion ? "ready" : "watching",
        title: suggestion?.title ?? lane?.nextAction ?? record.visual?.specialty ?? "Ready for assignment",
        reason: suggestion?.reason ?? lane?.nextAction ?? "Bind a lane and suggestion to create a relay-ready command.",
      };
    })
    .sort((a, b) => b.relayScore - a.relayScore || b.pressure - a.pressure)
    .slice(0, 12);
}

function commandRelayDeckStats(records) {
  const laneIds = new Set(records.map((record) => record.lane?.id).filter(Boolean));
  return [
    { label: "ready asks", value: formatNumber(records.filter((record) => record.suggestion).length) },
    { label: "local drafts", value: formatNumber(state.stagedDispatches.length) },
    { label: "gated", value: formatNumber(records.filter((record) => record.gates).length) },
    { label: "threads", value: formatNumber(records.filter((record) => record.agent?.thread_id).length) },
    { label: "lanes", value: formatNumber(laneIds.size) },
  ];
}

function commandRelayLeadRecord(records = commandRelayDeckRecords()) {
  return records.find((record) => record.lane?.id === state.selectedLaneId) ?? records[0] ?? null;
}

function renderCommandRelayDeck() {
  if (!el.commandRelayDeck || !state.snapshot) return;
  const records = commandRelayDeckRecords();
  const lead = commandRelayLeadRecord(records);
  const stats = commandRelayDeckStats(records);
  const style = lead?.lane
    ? laneStyle(lead.lane)
    : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";
  el.commandRelayDeck.innerHTML = `
    <div class="command-relay-visual" style="${style}">
      <img src="./assets/system/command-relay-deck-20260618.png" alt="" loading="lazy" />
      <span class="command-relay-scan" aria-hidden="true"></span>
    </div>
    <div class="command-relay-copy">
      <div class="command-relay-head">
        <div>
          <p class="eyebrow">Command Relay Deck</p>
          <h2>Bot Sends, Drafts, Gates</h2>
          <p>${escapeHtml(compactText("A single relay board for local bot communication: suggested sends, staged drafts, blocker gates, thread owners, and future command sockets stay visible without starting workers or sending messages.", 220))}</p>
        </div>
        <span class="snapshot-pill">${formatNumber(records.length)} relays</span>
      </div>
      <div class="command-relay-stats">
        ${stats
          .map(
            (stat) => `
            <span>
              <strong>${escapeHtml(stat.value)}</strong>
              <em>${escapeHtml(stat.label)}</em>
            </span>`
          )
          .join("")}
      </div>
      <div class="command-relay-actions">
        <button class="tool-button" type="button" data-command-relay-action="queue" title="Stage the lead relay command">Q</button>
        <button class="tool-button" type="button" data-command-relay-action="comms" title="Open lead relay Comms">COM</button>
        <button class="tool-button" type="button" data-command-relay-action="matrix" title="Open Bot Command Matrix">MATRIX</button>
      </div>
      <div class="command-relay-grid" aria-label="Bot command relays">
        ${records.map(renderCommandRelayCard).join("")}
        ${renderCommandRelayFutureSlots(records)}
      </div>
    </div>`;
}

function renderCommandRelayCard(record) {
  const { agent, lane, suggestion, visual, mode, gates, staged, relayScore } = record;
  const callsign = visual.callsign ?? agent.agent_id;
  const accent = visual.accent ?? lane?.visual?.accent ?? "#44d7c9";
  const accentAlt = lane?.visual?.accentAlt ?? "#f4ba55";
  const active = lane?.id === state.selectedLaneId;
  const laneAttr = lane?.id ? `data-command-relay-lane="${escapeHtml(lane.id)}"` : "";
  const stageAttr = lane?.id ? `data-command-relay-stage="${escapeHtml(lane.id)}"` : "";
  return `
    <article
      class="command-relay-card ${escapeHtml(mode)} ${staged ? "staged" : ""} ${active ? "active" : ""}"
      ${laneAttr}
      style="--relay-a:${escapeHtml(accent)}; --relay-b:${escapeHtml(accentAlt)}; --relay-score:${Math.max(8, Math.min(100, relayScore))}%;"
    >
      <div class="command-relay-card-top">
        ${agentRosterAvatar(agent)}
        <div>
          <p class="eyebrow">${escapeHtml(stateLabel(mode))}</p>
          <h3>${escapeHtml(compactText(callsign, 46))}</h3>
          <span>${escapeHtml(compactText(lane?.name ?? stateLabel(agent.department_id), 68))}</span>
        </div>
        <strong>${formatNumber(suggestion?.urgency ?? 0)}</strong>
      </div>
      <div class="command-relay-meter" aria-hidden="true"><i></i></div>
      <div class="command-relay-card-stats">
        <span><strong>${formatNumber(gates)}</strong><em>gates</em></span>
        <span><strong>${staged ? "Y" : "N"}</strong><em>queued</em></span>
        <span><strong>L${escapeHtml(lane?.level ?? 1)}</strong><em>level</em></span>
      </div>
      <div class="command-relay-ask">
        <span>${escapeHtml(stateLabel(suggestion?.kind ?? "next_action"))}</span>
        <p>${escapeHtml(compactText(record.reason, 150))}</p>
      </div>
      <div class="command-relay-thread">
        <span>${escapeHtml(compactText(agent.thread_id ?? "unbound thread", 54))}</span>
        <button class="tool-button" type="button" ${stageAttr} title="Stage this relay command">${staged ? "OK" : "Q"}</button>
      </div>
    </article>`;
}

function renderCommandRelayFutureSlots(records) {
  const slots = [
    { label: "worker socket", detail: "future live worker channel" },
    { label: "approval lock", detail: "future human sign-off gate" },
    { label: "batch lane", detail: "future grouped send rail" },
    { label: "voice ping", detail: "future operator note input" },
  ];
  const openCount = Math.max(0, slots.length - Math.min(slots.length, records.length % (slots.length + 1)));
  return slots
    .slice(0, Math.max(2, openCount))
    .map(
      (slot, index) => `
      <article class="command-relay-future">
        <span>+</span>
        <strong>${escapeHtml(slot.label)}</strong>
        <p>${escapeHtml(slot.detail)}</p>
        <em>slot ${formatNumber(records.length + index + 1)}</em>
      </article>`
    )
    .join("");
}

function companyQuestRecords() {
  const suggestions = state.snapshot?.dispatchConsole?.suggestions ?? [];
  return (state.snapshot?.lanes ?? [])
    .map((lane) => {
      const counts = lane.counts ?? {};
      const suggestion = suggestions.find((item) => item.laneId === lane.id);
      const gate = lane.gateMap?.[0] ?? lane.serviceRequests?.[0] ?? null;
      const task = lane.recentTasks?.[0] ?? null;
      const newestOutcome = lane.recentOutcomes?.[0] ?? null;
      const newestTrail = lane.trail?.[0] ?? null;
      const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id || draft.sourceId === suggestion?.id);
      const blockers = counts.blockers ?? 0;
      const pending = counts.pendingRequests ?? 0;
      const activeTasks = counts.activeTasks ?? Math.max(0, (counts.tasks ?? 0) - (counts.completedTasks ?? 0));
      const wins = counts.outcomes ?? 0;
      const pressure = Math.min(100, blockers * 22 + pending * 14 + activeTasks * 4 + (suggestion?.urgency ?? 0) * 0.28 + (staged ? 8 : 0));
      const tone = blockers || pending ? "gated" : wins ? "unlocked" : activeTasks ? "advancing" : "scouting";
      return {
        lane,
        suggestion,
        gate,
        task,
        newestOutcome,
        newestTrail,
        staged,
        blockers,
        pending,
        activeTasks,
        wins,
        pressure,
        tone,
        title: task?.title ?? newestOutcome?.title ?? gate?.workerType ?? gate?.type ?? lane.quest?.title ?? lane.name,
        nextAction: gate?.nextAction ?? gate?.requestedAction ?? task?.nextAction ?? suggestion?.reason ?? lane.nextAction ?? newestTrail?.summary ?? "Keep this lane visible while the next proof arrives.",
      };
    })
    .sort((a, b) => b.pressure - a.pressure || b.activeTasks - a.activeTasks || b.wins - a.wins)
    .slice(0, 9);
}

function companyQuestBoardStats(records) {
  const totals = state.snapshot?.totals ?? {};
  return [
    { label: "tasks", value: formatNumber(totals.tasks ?? records.reduce((sum, record) => sum + (record.lane.counts?.tasks ?? 0), 0)) },
    { label: "active", value: formatNumber(records.reduce((sum, record) => sum + record.activeTasks, 0)) },
    { label: "gates", value: formatNumber(totals.blockers ?? records.reduce((sum, record) => sum + record.blockers, 0)) },
    { label: "wins", value: formatNumber(records.reduce((sum, record) => sum + record.wins, 0)) },
    { label: "staged", value: formatNumber(state.stagedDispatches.length) },
  ];
}

function renderCompanyQuestBoard() {
  if (!el.companyQuestBoard || !state.snapshot) return;
  const records = companyQuestRecords();
  const selected = records.find((record) => record.lane.id === state.selectedLaneId) ?? records[0];
  const stats = companyQuestBoardStats(records);
  const style = selected?.lane ? laneStyle(selected.lane) : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";
  el.companyQuestBoard.innerHTML = `
    <div class="company-quest-visual" style="${style}" aria-hidden="true">
      <img src="./assets/system/company-quest-board-20260618.png" alt="" loading="lazy" />
      <span class="company-quest-scan"></span>
    </div>
    <div class="company-quest-copy" style="${style}">
      <div class="company-quest-head">
        <div>
          <p class="eyebrow">Company Quest Board</p>
          <h2>${escapeHtml(selected?.lane?.name ?? "All lanes")}</h2>
          <p>${escapeHtml(compactText(selected?.nextAction ?? "A global quest board for active tasks, blockers, wins, and staged commands.", 190))}</p>
        </div>
        <span class="badge ${escapeHtml(selected?.tone ?? "advancing")}">${escapeHtml(selected ? stateLabel(selected.tone) : "ready")}</span>
      </div>
      <div class="company-quest-stats">
        ${stats
          .map(
            (stat) => `
            <span>
              <strong>${escapeHtml(stat.value)}</strong>
              <em>${escapeHtml(stat.label)}</em>
            </span>`
          )
          .join("")}
      </div>
      <div class="company-quest-actions">
        <button class="tool-button" type="button" data-company-quest-action="tasks" title="Show task feed">TASKS</button>
        <button class="tool-button" type="button" data-company-quest-action="gates" title="Show gate feed">GATES</button>
        <button class="tool-button" type="button" data-company-quest-action="wins" title="Show outcome feed">WINS</button>
      </div>
      <div class="company-quest-track" aria-label="Top company quests">
        ${records.map(renderCompanyQuestCard).join("")}
      </div>
    </div>`;
}

function renderCompanyQuestCard(record, index) {
  const { lane, tone, staged, pressure } = record;
  return `
    <article
      class="company-quest-card ${escapeHtml(tone)} ${staged ? "staged" : ""} ${lane.id === state.selectedLaneId ? "active" : ""}"
      data-company-quest-lane="${escapeHtml(lane.id)}"
      style="${laneStyle(lane)} --quest-pressure:${Math.max(8, pressure)}%; --quest-rank:${index + 1};"
    >
      <div class="company-quest-card-top">
        ${avatarMarkup(lane, "company-quest-avatar")}
        <div>
          <span>${escapeHtml(lane.visual?.realm ?? lane.department)}</span>
          <strong>${escapeHtml(compactText(lane.name, 54))}</strong>
        </div>
        <em>L${formatNumber(lane.level ?? 1)}</em>
      </div>
      <div class="company-quest-meter"><i></i></div>
      <h3>${escapeHtml(compactText(record.title, 72))}</h3>
      <p>${escapeHtml(compactText(record.nextAction, 138))}</p>
      <div class="company-quest-card-stats">
        <span><strong>${formatNumber(record.activeTasks)}</strong><em>tasks</em></span>
        <span><strong>${formatNumber(record.blockers + record.pending)}</strong><em>gates</em></span>
        <span><strong>${formatNumber(record.wins)}</strong><em>wins</em></span>
      </div>
    </article>`;
}

function botCommandRecords() {
  const agents = state.snapshot?.agents ?? [];
  const suggestions = state.snapshot?.dispatchConsole?.suggestions ?? [];
  return agents.map((agent) => {
    const lane = agent.lane ? state.snapshot.lanes.find((item) => item.id === agent.lane.id) ?? agent.lane : null;
    const suggestion = suggestions
      .filter((item) => item.targetAgentId === agent.agent_id || item.laneId === lane?.id)
      .sort((a, b) => (b.urgency ?? 0) - (a.urgency ?? 0))[0];
    const staged = state.stagedDispatches.some((draft) => draft.laneId === lane?.id || draft.sourceId === suggestion?.id);
    const blockers = lane?.counts?.blockers ?? 0;
    const pending = lane?.counts?.pendingRequests ?? 0;
    const pressure = Math.min(100, blockers * 22 + pending * 16 + (suggestion?.urgency ?? 0) * 0.42);
    return {
      agent,
      lane,
      suggestion,
      staged,
      blockers,
      pending,
      pressure,
      visual: agent.visual ?? {},
      status: agent.status ?? "active",
    };
  });
}

function crewReadiness(record) {
  const laneProgress = record.lane?.progress ?? 0;
  const suggestionBoost = record.suggestion ? 12 : 0;
  const stagedBoost = record.staged ? 8 : 0;
  const gateDrag = record.blockers * 8 + record.pending * 6;
  return Math.max(4, Math.min(100, Math.round(laneProgress + suggestionBoost + stagedBoost - gateDrag)));
}

function crewMode(record) {
  if (record.staged) return "staged";
  if (record.blockers || record.pending) return "gated";
  if (record.suggestion) return "ready";
  return "watching";
}

function renderCrewBridge() {
  if (!el.crewBridge || !state.snapshot) return;
  const records = botCommandRecords().sort((a, b) => b.pressure - a.pressure || crewReadiness(b) - crewReadiness(a));
  const selected = records.find((record) => record.lane?.id === state.selectedLaneId) ?? records[0];
  const ready = records.filter((record) => record.suggestion).length;
  const gated = records.filter((record) => record.blockers || record.pending).length;
  const staged = records.filter((record) => record.staged).length;
  const totalUrgency = records.reduce((sum, record) => sum + (record.suggestion?.urgency ?? 0), 0);
  const style = selected?.lane ? laneStyle(selected.lane) : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";

  el.crewBridgeCount.textContent = `${formatNumber(records.length)} crews`;
  el.crewBridge.innerHTML = `
    <article class="crew-bridge-core" style="${style}">
      <div class="crew-core-top">
        <div class="crew-core-avatar">
          ${selected ? agentRosterAvatar(selected.agent) : `<div class="operator-avatar avatar-fallback" aria-hidden="true"></div>`}
          <span aria-hidden="true"></span>
        </div>
        <div>
          <p class="eyebrow">Selected Crew</p>
          <h3>${escapeHtml(selected?.visual?.callsign ?? selected?.agent?.agent_id ?? "No crew selected")}</h3>
          <p>${escapeHtml(compactText(selected?.visual?.specialty ?? selected?.lane?.nextAction ?? "Bind a bot to a lane to open the command bridge.", 170))}</p>
        </div>
        <div class="crew-readiness-orbit" style="--crew-readiness:${selected ? crewReadiness(selected) : 0}%">
          <strong>${selected ? formatNumber(crewReadiness(selected)) : "0"}</strong>
          <span>ready</span>
        </div>
      </div>
      <div class="crew-core-lane">
        <strong>${escapeHtml(selected?.lane?.name ?? "Unassigned")}</strong>
        <span>${escapeHtml(selected?.lane?.visual?.realm ?? selected?.agent?.thread_id ?? "No thread bound")}</span>
      </div>
      <div class="crew-bridge-stats">
        <span><strong>${formatNumber(ready)}</strong><em>asks</em></span>
        <span><strong>${formatNumber(gated)}</strong><em>gated</em></span>
        <span><strong>${formatNumber(staged)}</strong><em>staged</em></span>
        <span><strong>${formatNumber(totalUrgency)}</strong><em>urge</em></span>
      </div>
      <div class="crew-core-actions" ${selected?.lane?.id ? `data-crew-lane="${escapeHtml(selected.lane.id)}"` : ""}>
        <button class="tool-button" type="button" data-crew-action="comms" title="Open selected crew Comms">COM</button>
        <button class="tool-button" type="button" data-crew-action="queue" title="Stage selected crew command">Q</button>
        <button class="tool-button" type="button" data-crew-action="path" title="Open selected crew path">PATH</button>
      </div>
    </article>
    <div class="crew-card-grid">
      ${records.map(renderCrewCard).join("")}
    </div>`;
}

function renderCrewCard(record) {
  const { agent, lane, suggestion, visual, pressure, staged } = record;
  const mode = crewMode(record);
  const callsign = visual.callsign ?? agent.agent_id;
  const accent = visual.accent ?? lane?.visual?.accent ?? "#44d7c9";
  const readiness = crewReadiness(record);
  const active = lane?.id === state.selectedLaneId;
  return `
    <article
      class="crew-card ${escapeHtml(mode)} ${active ? "is-active" : ""}"
      ${lane?.id ? `data-crew-lane="${escapeHtml(lane.id)}"` : ""}
      style="--crew-a:${escapeHtml(accent)}; --crew-pressure:${Math.max(8, pressure)}%; --crew-readiness:${readiness}%;"
    >
      <div class="crew-card-top">
        ${agentRosterAvatar(agent)}
        <div>
          <p class="eyebrow">${escapeHtml(stateLabel(mode))}</p>
          <h3>${escapeHtml(compactText(callsign, 44))}</h3>
          <span>${escapeHtml(compactText(lane?.name ?? stateLabel(agent.department_id), 62))}</span>
        </div>
        <strong>${formatNumber(readiness)}</strong>
      </div>
      <div class="crew-readiness-meter" aria-label="${formatNumber(readiness)} percent readiness"><span></span></div>
      <div class="crew-card-metrics">
        <span><strong>${formatNumber(record.blockers)}</strong><em>gates</em></span>
        <span><strong>${formatNumber(record.pending)}</strong><em>review</em></span>
        <span><strong>${formatNumber(suggestion?.urgency ?? 0)}</strong><em>urge</em></span>
      </div>
      <p>${escapeHtml(compactText(suggestion?.reason ?? lane?.nextAction ?? visual.specialty ?? "Ready for assignment.", 132))}</p>
      <div class="crew-card-actions">
        <button class="tool-button" type="button" data-crew-action="comms" title="Open Comms">COM</button>
        <button class="tool-button" type="button" data-crew-action="queue" title="Stage command">${staged ? "OK" : "Q"}</button>
        <button class="tool-button" type="button" data-crew-action="path" title="Open Path">PATH</button>
      </div>
    </article>`;
}

function threadNexusPositions(records) {
  const count = Math.max(records.length, 1);
  return records.map((record, index) => {
    const angle = -Math.PI / 2 + (index / count) * Math.PI * 2;
    const radiusX = 38;
    const radiusY = 34;
    return {
      ...record,
      x: Math.round((50 + Math.cos(angle) * radiusX) * 10) / 10,
      y: Math.round((50 + Math.sin(angle) * radiusY) * 10) / 10,
      index,
    };
  });
}

function renderThreadNexus() {
  if (!el.threadNexus || !state.snapshot) return;
  const records = threadNexusPositions(botCommandRecords());
  const selected = records.find((record) => record.lane?.id === state.selectedLaneId) ?? records[0];
  const suggestions = state.snapshot.dispatchConsole?.suggestions ?? [];
  const staged = records.filter((record) => record.staged).length;
  const gated = records.filter((record) => record.blockers || record.pending).length;
  const ready = records.filter((record) => record.suggestion).length;
  el.threadNexusCount.textContent = `${formatNumber(records.length)} links`;
  el.threadNexus.innerHTML = `
    <div class="thread-nexus-map" style="${selected?.lane ? laneStyle(selected.lane) : ""}">
      <svg class="thread-links" viewBox="0 0 100 100" aria-hidden="true">
        ${records
          .map(
            (record) =>
              `<line class="${record.lane?.id === state.selectedLaneId ? "active" : ""} ${record.blockers || record.pending ? "gated" : ""}" x1="50" y1="50" x2="${record.x}" y2="${record.y}" />`
          )
          .join("")}
      </svg>
      <div class="thread-hub" aria-hidden="true">
        <strong>${formatNumber(records.length)}</strong>
        <span>bots</span>
      </div>
      ${records.map(renderThreadNode).join("")}
    </div>
    <div class="thread-nexus-console">
      <div class="thread-nexus-stats">
        <span><strong>${formatNumber(ready)}</strong><em>ready</em></span>
        <span><strong>${formatNumber(gated)}</strong><em>gated</em></span>
        <span><strong>${formatNumber(staged)}</strong><em>staged</em></span>
        <span><strong>${formatNumber(suggestions.length)}</strong><em>asks</em></span>
      </div>
      ${selected ? renderThreadFocus(selected) : `<div class="dispatch-empty compact"><p>No agent links yet.</p></div>`}
      <div class="thread-queue">
        <p class="eyebrow">Top Thread Asks</p>
        ${(suggestions.slice(0, 4).map(renderThreadQueueItem).join("")) || `<p class="small-muted">No dispatch suggestions available.</p>`}
      </div>
    </div>`;
}

function renderThreadNode(record) {
  const { agent, lane, visual, pressure, staged } = record;
  const active = lane?.id === state.selectedLaneId;
  const callsign = visual.callsign ?? agent.agent_id;
  const gateClass = record.blockers || record.pending ? "gated" : "ready";
  const laneAttr = lane?.id ? `data-agent-lane-id="${escapeHtml(lane.id)}"` : "disabled";
  return `
    <button
      class="thread-node ${active ? "active" : ""} ${staged ? "staged" : ""} ${escapeHtml(gateClass)}"
      type="button"
      ${laneAttr}
      style="--thread-x:${record.x}%; --thread-y:${record.y}%; --thread-a:${escapeHtml(visual.accent ?? lane?.visual?.accent ?? "#44d7c9")}; --thread-pressure:${Math.max(8, pressure)}%;"
      title="Open ${escapeHtml(callsign)} Comms deck"
    >
      ${agentRosterAvatar(agent)}
      <span>${escapeHtml(compactText(callsign, 24))}</span>
    </button>`;
}

function renderThreadFocus(record) {
  const { agent, lane, suggestion, visual, staged } = record;
  const callsign = visual.callsign ?? agent.agent_id;
  return `
    <article class="thread-focus-card ${escapeHtml(lane?.state ?? "scouting")}" style="--thread-a:${escapeHtml(visual.accent ?? lane?.visual?.accent ?? "#44d7c9")}">
      <div class="thread-focus-top">
        ${agentRosterAvatar(agent)}
        <div>
          <p class="eyebrow">${escapeHtml(stateLabel(agent.status))}</p>
          <h3>${escapeHtml(callsign)}</h3>
          <span>${escapeHtml(compactText(agent.thread_id ?? "No thread", 56))}</span>
        </div>
        <span class="badge ${escapeHtml(lane?.state ?? "scouting")}">${escapeHtml(lane ? stateLabel(lane.state) : "unassigned")}</span>
      </div>
      <div class="thread-focus-lane">
        <strong>${escapeHtml(lane?.name ?? stateLabel(agent.department_id))}</strong>
        <span>${escapeHtml(lane?.visual?.realm ?? visual.specialty ?? "No lane bound")}</span>
      </div>
      <p>${escapeHtml(compactText(suggestion?.reason ?? lane?.nextAction ?? visual.specialty ?? "Ready for assignment.", 170))}</p>
      <div class="thread-focus-actions">
        <button class="tool-button" type="button" ${lane?.id ? `data-agent-lane-id="${escapeHtml(lane.id)}"` : ""} title="Open Comms deck">COM</button>
        <button class="tool-button" type="button" ${lane?.id ? `data-thread-path-lane="${escapeHtml(lane.id)}"` : ""} title="Open Path Map">PATH</button>
        <button class="tool-button" type="button" ${lane?.id ? `data-bot-stage-lane="${escapeHtml(lane.id)}"` : ""} title="Stage suggested command">${staged ? "OK" : "Q"}</button>
      </div>
    </article>`;
}

function renderThreadQueueItem(item) {
  return `
    <button class="thread-queue-item ${escapeHtml(item.kind)}" type="button" data-dispatch-lane-id="${escapeHtml(item.laneId)}">
      <span>${escapeHtml(stateLabel(item.kind))}</span>
      <strong>${escapeHtml(compactText(item.laneName, 48))}</strong>
      <em>${formatNumber(item.urgency ?? 0)}</em>
    </button>`;
}

function botSquadronHudModel(records) {
  const sorted = [...records].sort((a, b) => b.pressure - a.pressure || crewReadiness(b) - crewReadiness(a));
  const focus = sorted.find((record) => record.lane?.id === state.selectedLaneId) ?? sorted[0] ?? null;
  const readiness = focus ? crewReadiness(focus) : 0;
  const mode = focus ? crewMode(focus) : "watching";
  const ready = records.filter((record) => record.suggestion).length;
  const gated = records.filter((record) => record.blockers || record.pending).length;
  const staged = records.filter((record) => record.staged).length;
  const avatarCoverage = records.filter((record) => record.visual?.avatar).length;
  const totalPressure = records.reduce((sum, record) => sum + record.pressure, 0);
  const beacons = sorted.slice(0, 8).map((record, index) => ({
    record,
    index,
    mode: crewMode(record),
    readiness: crewReadiness(record),
  }));
  return {
    focus,
    readiness,
    mode,
    pressure: Math.round(records.length ? totalPressure / records.length : 0),
    stats: [
      { label: "bots", value: records.length },
      { label: "ready", value: ready },
      { label: "gated", value: gated },
      { label: "staged", value: staged },
      { label: "art", value: avatarCoverage },
    ],
    beacons,
  };
}

function renderBotSquadronHud(model) {
  const focus = model.focus;
  const lane = focus?.lane;
  const callsign = focus?.visual?.callsign ?? focus?.agent?.agent_id ?? "No bot selected";
  const specialty = focus?.visual?.specialty ?? lane?.nextAction ?? "Bot crew sockets are ready for lane assignments.";
  const laneName = lane?.name ?? focus?.agent?.department_id ?? "Unassigned lane";
  const style = lane ? laneStyle(lane) : `--node-a:${escapeHtml(focus?.visual?.accent ?? "#44d7c9")}; --node-b:#f4ba55; --lane-accent:${escapeHtml(focus?.visual?.accent ?? "#44d7c9")}; --lane-accent-alt:#f4ba55;`;
  return `
    <section class="bot-squadron-hud" data-bot-squadron-mode="${escapeHtml(model.mode)}" style="${style} --bot-squadron-ready:${model.readiness}%; --bot-squadron-pressure:${Math.max(8, model.pressure)}%;" aria-label="Bot squadron command HUD">
      <div class="bot-squadron-orbit" aria-hidden="true">
        ${focus ? agentRosterAvatar(focus.agent) : `<span class="operator-avatar avatar-fallback" aria-hidden="true"></span>`}
        <i></i>
      </div>
      <div class="bot-squadron-copy">
        <p class="eyebrow">Bot Squadron</p>
        <h3>${escapeHtml(compactText(callsign, 42))}</h3>
        <span>${escapeHtml(compactText(`${laneName} - ${specialty}`, 120))}</span>
      </div>
      <div class="bot-squadron-stats" aria-label="Bot squadron stats">
        ${model.stats
          .map(
            (stat) => `
              <span>
                <strong>${formatNumber(stat.value)}</strong>
                <em>${escapeHtml(stat.label)}</em>
              </span>`
          )
          .join("")}
      </div>
      <div class="bot-squadron-beacons" aria-label="Priority bot avatars">
        ${model.beacons
          .map(
            ({ record, index, mode, readiness }) => `
              <button class="bot-squadron-beacon ${escapeHtml(mode)} ${record.lane?.id === state.selectedLaneId ? "active" : ""}" type="button" ${record.lane?.id ? `data-agent-lane-id="${escapeHtml(record.lane.id)}"` : "disabled"} style="--bot-beacon-index:${index}; --bot-beacon-ready:${Math.max(8, readiness)}%; --bot-beacon-a:${escapeHtml(record.visual?.accent ?? record.lane?.visual?.accent ?? "#44d7c9")};" title="${escapeHtml(record.visual?.callsign ?? record.agent.agent_id)}">
                ${agentRosterAvatar(record.agent)}
                <i aria-hidden="true"></i>
              </button>`
          )
          .join("")}
      </div>
    </section>`;
}

function botCommandSwitchboardGroups(records) {
  const sorted = [...records].sort((a, b) => {
    const modeOrder = { gated: 4, ready: 3, staged: 2, watching: 1 };
    return (modeOrder[crewMode(b)] ?? 0) - (modeOrder[crewMode(a)] ?? 0) || b.pressure - a.pressure || crewReadiness(b) - crewReadiness(a);
  });
  const groupDefinitions = [
    { id: "ready", label: "Ready", detail: "sendable asks", tone: "ready" },
    { id: "gated", label: "Gated", detail: "needs decision", tone: "gated" },
    { id: "staged", label: "Staged", detail: "queued handoff", tone: "staged" },
    { id: "watching", label: "Watching", detail: "monitoring", tone: "watching" },
  ];
  return groupDefinitions.map((group) => {
    const groupRecords = sorted.filter((record) => crewMode(record) === group.id);
    const fallbackRecords = groupRecords.length ? groupRecords : sorted.filter((record) => record.lane).slice(0, 2);
    return {
      ...group,
      count: groupRecords.length,
      records: fallbackRecords.slice(0, 3),
      charge: Math.min(100, Math.max(10, groupRecords.reduce((sum, record) => sum + crewReadiness(record), 0) / Math.max(1, groupRecords.length))),
    };
  });
}

function renderBotCommandSwitchboard(records) {
  const groups = botCommandSwitchboardGroups(records);
  return `
    <section class="bot-command-switchboard" aria-label="Bot command switchboard">
      ${groups
        .map(
          (group, groupIndex) => `
            <article class="bot-switchboard-group ${escapeHtml(group.id)}" data-bot-switchboard-mode="${escapeHtml(group.id)}" style="--switch-group-index:${groupIndex}; --switch-charge:${Math.round(group.charge)}%;">
              <div class="bot-switchboard-head">
                <span>${escapeHtml(group.label)}</span>
                <strong>${formatNumber(group.count)}</strong>
                <em>${escapeHtml(group.detail)}</em>
              </div>
              <div class="bot-switchboard-agents">
                ${group.records
                  .map((record, index) => {
                    const callsign = record.visual?.callsign ?? record.agent.agent_id;
                    const laneName = record.lane?.name ?? stateLabel(record.agent.department_id);
                    const readiness = crewReadiness(record);
                    const laneAttr = record.lane?.id ? `data-agent-lane-id="${escapeHtml(record.lane.id)}"` : "disabled";
                    return `
                      <button class="bot-switchboard-agent ${escapeHtml(crewMode(record))} ${record.lane?.id === state.selectedLaneId ? "active" : ""}" type="button" ${laneAttr} style="--switch-agent-index:${index}; --switch-agent-ready:${Math.max(8, readiness)}%; --switch-agent-a:${escapeHtml(record.visual?.accent ?? record.lane?.visual?.accent ?? "#44d7c9")};" title="${escapeHtml(callsign)} - ${escapeHtml(laneName)}">
                        ${agentRosterAvatar(record.agent)}
                        <span>
                          <strong>${escapeHtml(compactText(callsign, 22))}</strong>
                          <em>${escapeHtml(compactText(laneName, 28))}</em>
                        </span>
                        <b>${formatNumber(readiness)}</b>
                      </button>`;
                  })
                  .join("") || `<span class="bot-switchboard-empty">No bots</span>`}
              </div>
            </article>`
        )
        .join("")}
    </section>`;
}
function renderBotCommandMatrix() {
  if (!el.botCommandMatrix || !state.snapshot) return;
  const records = botCommandRecords();
  const gated = records.filter((record) => record.blockers || record.pending).length;
  const ready = records.filter((record) => record.suggestion).length;
  const staged = records.filter((record) => record.staged).length;
  const squadronHud = botSquadronHudModel(records);
  el.botCommandCount.textContent = `${formatNumber(records.length)} bots`;
  el.botCommandSummary.innerHTML = [
    ["online", records.length],
    ["ready sends", ready],
    ["gated", gated],
    ["staged", staged],
  ]
    .map(
      ([label, value]) => `
        <span>
          <strong>${formatNumber(value)}</strong>
          <em>${escapeHtml(label)}</em>
        </span>`
    )
    .join("");
  el.botCommandMatrix.innerHTML = `${renderBotSquadronHud(squadronHud)}${renderBotCommandSwitchboard(records)}<div class="bot-command-card-rail">${records.map(renderBotCommandCard).join("")}</div>`;
}

function renderBotCommandCard(record) {
  const { agent, lane, suggestion, staged, visual, pressure } = record;
  const callsign = visual.callsign ?? agent.agent_id;
  const laneState = lane?.state ?? "scouting";
  const accent = visual.accent ?? lane?.visual?.accent ?? "#44d7c9";
  const stageAttr = lane?.id ? `data-bot-stage-lane="${escapeHtml(lane.id)}"` : "";
  const laneAttr = lane?.id ? `data-agent-lane-id="${escapeHtml(lane.id)}"` : "";
  return `
    <article class="bot-command-card ${escapeHtml(laneState)} ${staged ? "staged" : ""}" style="--bot-a:${escapeHtml(accent)}; --bot-pressure:${Math.max(8, pressure)}%;">
      <div class="bot-command-top">
        ${agentRosterAvatar(agent)}
        <div>
          <p class="eyebrow">${escapeHtml(stateLabel(agent.status))}</p>
          <h3>${escapeHtml(callsign)}</h3>
          <p>${escapeHtml(compactText(visual.specialty ?? stateLabel(agent.role_id), 92))}</p>
        </div>
        <span class="badge ${escapeHtml(laneState)}">${escapeHtml(lane ? stateLabel(laneState) : "unassigned")}</span>
      </div>
      <div class="bot-command-lane">
        <strong>${escapeHtml(lane?.name ?? stateLabel(agent.department_id))}</strong>
        <span>${escapeHtml(lane?.visual?.realm ?? agent.thread_id ?? "No lane bound")}</span>
      </div>
      <div class="bot-command-pressure" aria-hidden="true"><i></i></div>
      <div class="bot-command-stats">
        <span><strong>L${escapeHtml(lane?.level ?? 1)}</strong><em>level</em></span>
        <span><strong>${formatNumber(record.blockers)}</strong><em>gates</em></span>
        <span><strong>${formatNumber(record.pending)}</strong><em>review</em></span>
        <span><strong>${formatNumber(suggestion?.urgency ?? 0)}</strong><em>urge</em></span>
      </div>
      <div class="bot-command-ask">
        <span>${escapeHtml(suggestion ? stateLabel(suggestion.kind) : "next action")}</span>
        <p>${escapeHtml(compactText(suggestion?.reason ?? lane?.nextAction ?? "Ready for assignment.", 150))}</p>
      </div>
      <div class="bot-command-thread">
        <span>${escapeHtml(compactText(agent.thread_id ?? "no thread", 44))}</span>
      </div>
      <div class="bot-command-actions">
        <button class="tool-button" type="button" ${laneAttr} title="Open this bot's Comms deck">COM</button>
        <button class="tool-button" type="button" ${stageAttr} title="Stage this bot's top command">${staged ? "OK" : "Q"}</button>
      </div>
    </article>`;
}

function batchCommandText() {
  return state.stagedDispatches
    .map(
      (item, index) =>
        `[${index + 1}] ${item.laneName} - ${stateLabel(item.kind)}\n${item.command}`
    )
    .join("\n\n---\n\n");
}

function laneDispatchSuggestion(lane) {
  const status = commandStatus(lane);
  return {
    id: `lane-comms-${lane.id}`,
    laneId: lane.id,
    laneName: lane.name,
    kind: lane.counts.blockers ? "gate_review" : lane.promotionCandidate?.ready_for_manual_promotion ? "promotion" : "progress_check",
    urgency: lane.counts.blockers ? 94 : lane.promotionCandidate?.ready_for_manual_promotion ? 88 : 72,
    title: status.label,
    reason: buildBriefLines(lane)[1]?.value ?? "Stage a bounded local command draft.",
    command: commandPreview(lane),
  };
}

function bestLaneDispatchSuggestion(lane) {
  return state.snapshot?.dispatchConsole?.suggestions?.find((item) => item.laneId === lane.id) ?? laneDispatchSuggestion(lane);
}

function stageDispatch(item, options = {}) {
  const alreadyStaged = state.stagedDispatches.find((draft) => draft.sourceId === item.id && draft.command === item.command);
  if (alreadyStaged) {
    alreadyStaged.stagedAt = new Date().toISOString();
    state.stagedDispatches = [alreadyStaged, ...state.stagedDispatches.filter((draft) => draft.id !== alreadyStaged.id)];
    if (!options.silent) recordDispatchHistory("refreshed", alreadyStaged);
  } else {
    const draft = {
      id: `dispatch-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
      sourceId: item.id,
      laneId: item.laneId,
      laneName: item.laneName,
      kind: item.kind,
      title: item.title,
      command: item.command,
      stagedAt: new Date().toISOString(),
    };
    state.stagedDispatches = [draft, ...state.stagedDispatches].slice(0, 24);
    if (!options.silent) recordDispatchHistory("staged", draft);
  }
  writeDispatchOutbox();
  if (!options.deferRender) renderDispatchConsole();
}

function filteredFeedItems() {
  const items = state.snapshot.missionFeed?.items ?? [];
  if (state.feedFilter === "all") return items;
  return items.filter((item) => item.kind === state.feedFilter);
}

function currentPlaybackItem(items = filteredFeedItems()) {
  if (!items.length) return null;
  return items[state.feedPlaybackIndex] ?? items[0];
}

function missionFeedTimelineBoardModel(items) {
  const current = currentPlaybackItem(items) ?? items[0] ?? null;
  const counts = items.reduce((acc, item) => {
    acc[item.kind] = (acc[item.kind] ?? 0) + 1;
    return acc;
  }, {});
  const lanes = new Set(items.map((item) => item.laneId).filter(Boolean)).size;
  const latestLane = current ? laneForFeedItem(current) : null;
  const progress = items.length > 1 ? Math.round((state.feedPlaybackIndex / (items.length - 1)) * 100) : items.length ? 100 : 0;
  const cells = [
    {
      id: "gates",
      label: "Gates",
      value: items.filter((item) => item.kind === "service_request").length,
      tone: counts.service_request ? "gated" : "clear",
      body: counts.service_request ? "Blockers waiting for operator review" : "No gates in this lens",
    },
    {
      id: "proof",
      label: "Proof",
      value: items.filter((item) => item.kind === "evidence").length,
      tone: counts.evidence ? "proof" : "quiet",
      body: counts.evidence ? "Evidence packets captured" : "No proof selected",
    },
    {
      id: "wins",
      label: "Wins",
      value: items.filter((item) => item.kind === "outcome").length,
      tone: counts.outcome ? "won" : "quiet",
      body: counts.outcome ? "Unlocked outcomes in view" : "No wins in this lens",
    },
    {
      id: "lanes",
      label: "Lanes",
      value: lanes,
      tone: lanes > 1 ? "spread" : "focused",
      body: lanes > 1 ? "Multiple paths are speaking" : latestLane?.name ?? "No lane signal",
    },
  ];
  return {
    current,
    latestLane,
    progress,
    count: items.length,
    filter: state.feedFilter,
    cells,
  };
}

function renderMissionFeedTimelineBoard(items) {
  if (!el.missionFeedTimelineBoard) return;
  const model = missionFeedTimelineBoardModel(items);
  const style = model.latestLane ? laneStyle(model.latestLane) : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";
  el.missionFeedTimelineBoard.innerHTML = `
    <article class="timeline-board-current ${escapeHtml(model.current?.kind ?? "empty")}" style="${style}; --timeline-progress:${model.progress}%;">
      <div>
        <span>Current</span>
        <strong>${escapeHtml(compactText(model.current?.title ?? "Timeline idle", 62))}</strong>
        <p>${escapeHtml(compactText(model.current?.summary ?? "Filtered company events will appear here as a compact replay board.", 118))}</p>
      </div>
      <em>${formatNumber(model.count)} ${escapeHtml(stateLabel(model.filter))}</em>
      <i aria-hidden="true"></i>
    </article>
    ${model.cells
      .map(
        (cell, index) => `
          <article class="timeline-board-cell ${escapeHtml(cell.tone)}" data-feed-timeline-cell="${escapeHtml(cell.id)}" style="--timeline-cell-index:${index};">
            <span>${escapeHtml(cell.label)}</span>
            <strong>${formatNumber(cell.value)}</strong>
            <p>${escapeHtml(compactText(cell.body, 64))}</p>
          </article>`,
      )
      .join("")}`;
}
function renderMissionFeed() {
  const items = filteredFeedItems();
  const total = state.snapshot.missionFeed?.items?.length ?? 0;
  el.missionFeedCount.textContent = state.feedFilter === "all" ? `${formatNumber(total)} events` : `${formatNumber(items.length)} ${stateLabel(state.feedFilter)}`;
  state.feedPlaybackIndex = Math.min(state.feedPlaybackIndex, Math.max(items.length - 1, 0));
  renderFeedSavedViews();
  renderFeedPlayback(items);
  renderMissionFeedTimelineBoard(items);
  renderCompanyChronicleSpine(items);
  renderExperimentDiscoveryLab(items);
  renderSignalCore();
  el.missionFeed.innerHTML = items
    .slice(0, 18)
    .map(renderMissionFeedItem)
    .join("");
  renderMap();
}

function defaultFeedViews() {
  return [
    { id: "feed-view-all", label: "All", filter: "all", fixed: true },
    { id: "feed-view-gates", label: "Gates", filter: "service_request", fixed: true },
    { id: "feed-view-proof", label: "Proof", filter: "evidence", fixed: true },
    { id: "feed-view-wins", label: "Wins", filter: "outcome", fixed: true },
    { id: "feed-view-traces", label: "Traces", filter: "trace", fixed: true },
  ];
}

function companyChronicleChapters(items) {
  const chunkSize = state.feedFilter === "all" ? 6 : 5;
  const chapters = [];
  for (let index = 0; index < items.length && chapters.length < 5; index += chunkSize) {
    const chapterItems = items.slice(index, index + chunkSize);
    if (!chapterItems.length) continue;
    const counts = chapterItems.reduce((acc, item) => {
      acc[item.kind] = (acc[item.kind] ?? 0) + 1;
      return acc;
    }, {});
    const lanes = [...new Set(chapterItems.map((item) => item.laneId).filter(Boolean))];
    const newest = chapterItems[0];
    const anchorLane = state.snapshot?.lanes?.find((lane) => lane.id === newest?.laneId) ?? null;
    const dominantKind = Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0] ?? "trace";
    const tone = counts.service_request ? "gated" : counts.outcome ? "unlocked" : counts.task ? "advancing" : "scouting";
    chapters.push({
      id: `chronicle-${chapters.length}-${newest?.id ?? index}`,
      index: chapters.length,
      newest,
      oldest: chapterItems[chapterItems.length - 1],
      items: chapterItems,
      counts,
      lanes,
      anchorLane,
      dominantKind,
      tone,
    });
  }
  return chapters;
}

function companyChronicleStats(items, chapters) {
  const counts = items.reduce((acc, item) => {
    acc[item.kind] = (acc[item.kind] ?? 0) + 1;
    return acc;
  }, {});
  return [
    { label: "events", value: formatNumber(items.length) },
    { label: "chapters", value: formatNumber(chapters.length) },
    { label: "lanes", value: formatNumber(new Set(items.map((item) => item.laneId).filter(Boolean)).size) },
    { label: "proof", value: formatNumber(counts.evidence ?? 0) },
    { label: "wins", value: formatNumber(counts.outcome ?? 0) },
  ];
}

function renderCompanyChronicleSpine(items) {
  if (!el.companyChronicleSpine) return;
  const chapters = companyChronicleChapters(items);
  const stats = companyChronicleStats(items, chapters);
  const focus = chapters[0];
  const style = focus?.anchorLane ? laneStyle(focus.anchorLane) : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";
  el.companyChronicleSpine.innerHTML = `
    <div class="company-chronicle-visual" style="${style}" aria-hidden="true">
      <img src="./assets/system/company-chronicle-spine-20260618.png" alt="" loading="lazy" />
      <span class="company-chronicle-scan"></span>
    </div>
    <div class="company-chronicle-copy" style="${style}">
      <div class="company-chronicle-head">
        <div>
          <p class="eyebrow">Company Chronicle Spine</p>
          <h3>${escapeHtml(focus?.newest?.title ?? "No global history yet")}</h3>
          <p>${escapeHtml(compactText(focus?.newest?.summary ?? "Filtered feed events become chapter cards as the company grows.", 180))}</p>
        </div>
        <span class="badge ${escapeHtml(focus?.tone ?? "scouting")}">${escapeHtml(stateLabel(state.feedFilter))}</span>
      </div>
      <div class="company-chronicle-stats">
        ${stats
          .map(
            (stat) => `
            <span>
              <strong>${escapeHtml(stat.value)}</strong>
              <em>${escapeHtml(stat.label)}</em>
            </span>`
          )
          .join("")}
      </div>
      <div class="company-chronicle-actions">
        <button class="tool-button" type="button" data-company-chronicle-action="latest" title="Show latest events">LATEST</button>
        <button class="tool-button" type="button" data-company-chronicle-action="proof" title="Show proof events">PROOF</button>
        <button class="tool-button" type="button" data-company-chronicle-action="gates" title="Show gate events">GATES</button>
      </div>
      <div class="company-chronicle-track" aria-label="Company history chapters">
        ${chapters.length ? chapters.map(renderCompanyChronicleChapter).join("") : `<article class="company-chronicle-chapter scouting"><strong>No chapters yet</strong><p>New tasks, traces, proof, blockers, and outcomes will appear here.</p></article>`}
      </div>
    </div>`;
}

function renderCompanyChronicleChapter(chapter) {
  const lane = chapter.anchorLane;
  const style = lane ? laneStyle(lane) : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";
  const counts = chapter.counts;
  return `
    <article class="company-chronicle-chapter ${escapeHtml(chapter.tone)} kind-${escapeHtml(chapter.dominantKind)}" style="${style}" ${lane?.id ? `data-company-chronicle-lane="${escapeHtml(lane.id)}"` : ""}>
      <div class="company-chronicle-chapter-top">
        <span>${escapeHtml(shortDate(chapter.newest?.time))}</span>
        <strong>${escapeHtml(formatNumber(chapter.items.length))}</strong>
      </div>
      <h3>${escapeHtml(compactText(chapter.newest?.title ?? "Chronicle chapter", 74))}</h3>
      <p>${escapeHtml(compactText(chapter.newest?.summary ?? chapter.oldest?.summary ?? "Global history packet.", 132))}</p>
      <div class="company-chronicle-kind-row">
        <span><strong>${formatNumber(counts.task ?? 0)}</strong><em>task</em></span>
        <span><strong>${formatNumber(counts.service_request ?? 0)}</strong><em>gate</em></span>
        <span><strong>${formatNumber(counts.evidence ?? 0)}</strong><em>proof</em></span>
        <span><strong>${formatNumber(counts.outcome ?? 0)}</strong><em>win</em></span>
        <span><strong>${formatNumber(counts.trace ?? 0)}</strong><em>trace</em></span>
      </div>
      <div class="company-chronicle-meta">
        <span>${escapeHtml(chapter.lanes.length)} lanes</span>
        <span>${escapeHtml(lane?.name ?? chapter.newest?.laneName ?? "global")}</span>
      </div>
    </article>`;
}

function experimentDiscoveryLabRecords(items = state.snapshot?.missionFeed?.items ?? []) {
  const byLane = new Map();
  (state.snapshot?.lanes ?? []).forEach((lane) => {
    byLane.set(lane.id, {
      lane,
      items: [],
      counts: { task: 0, evidence: 0, service_request: 0, outcome: 0, trace: 0 },
    });
  });
  items.forEach((item) => {
    if (!item.laneId) return;
    const bucket = byLane.get(item.laneId);
    if (!bucket) return;
    bucket.items.push(item);
    bucket.counts[item.kind] = (bucket.counts[item.kind] ?? 0) + 1;
  });
  return [...byLane.values()]
    .map((record) => {
      const { lane, counts, items: laneItems } = record;
      const proof = counts.evidence ?? 0;
      const wins = counts.outcome ?? 0;
      const gates = (counts.service_request ?? 0) + (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
      const tests = (counts.task ?? 0) + proof + (counts.trace ?? 0);
      const labScore = wins * 28 + proof * 22 + (counts.trace ?? 0) * 10 + (counts.task ?? 0) * 8 + gates * 6 + (lane.progress ?? 0) * 0.28;
      const mode = wins ? "validated" : gates ? "blocked" : proof || tests ? "testing" : "scouting";
      const latest = laneItems[0] ?? lane.trail?.[0] ?? lane.recentTasks?.[0] ?? null;
      return {
        ...record,
        latest,
        proof,
        wins,
        gates,
        tests,
        labScore,
        mode,
        stage: wins ? "validated route" : gates ? "blocked test" : proof ? "proof captured" : tests ? "active test" : "empty bench",
      };
    })
    .sort((a, b) => b.labScore - a.labScore || b.items.length - a.items.length)
    .slice(0, 12);
}

function experimentDiscoveryLabStats(records) {
  return [
    { label: "experiments", value: formatNumber(records.reduce((sum, record) => sum + record.tests, 0)) },
    { label: "proof", value: formatNumber(records.reduce((sum, record) => sum + record.proof, 0)) },
    { label: "wins", value: formatNumber(records.reduce((sum, record) => sum + record.wins, 0)) },
    { label: "gates", value: formatNumber(records.reduce((sum, record) => sum + record.gates, 0)) },
    { label: "lanes", value: formatNumber(records.filter((record) => record.items.length || record.tests || record.gates || record.wins).length) },
  ];
}

function renderExperimentDiscoveryLab(items) {
  if (!el.experimentDiscoveryLab || !state.snapshot) return;
  const records = experimentDiscoveryLabRecords(items);
  const stats = experimentDiscoveryLabStats(records);
  const focus = records.find((record) => record.lane.id === state.selectedLaneId) ?? records[0];
  const style = focus?.lane ? laneStyle(focus.lane) : "--node-a:#44d7c9; --node-b:#f4ba55; --lane-accent:#44d7c9; --lane-accent-alt:#f4ba55;";
  el.experimentDiscoveryLab.innerHTML = `
    <div class="experiment-lab-visual" style="${style}" aria-hidden="true">
      <img src="./assets/system/experiment-discovery-lab-20260618.png" alt="" loading="lazy" />
      <span class="experiment-lab-scan"></span>
    </div>
    <div class="experiment-lab-copy" style="${style}">
      <div class="experiment-lab-head">
        <div>
          <p class="eyebrow">Experiment Discovery Lab</p>
          <h3>${escapeHtml(focus?.latest?.title ?? "Tests waiting for signal")}</h3>
          <p>${escapeHtml(compactText("A company-wide lab board for what has been tested, what produced proof, what is blocked, and which paths unlocked wins. It uses the current Mission Feed lens, so Evidence, Gates, and Outcomes become playable lab views.", 220))}</p>
        </div>
        <span class="badge ${escapeHtml(focus?.mode ?? "scouting")}">${escapeHtml(stateLabel(focus?.mode ?? "scouting"))}</span>
      </div>
      <div class="experiment-lab-stats">
        ${stats
          .map(
            (stat) => `
            <span>
              <strong>${escapeHtml(stat.value)}</strong>
              <em>${escapeHtml(stat.label)}</em>
            </span>`
          )
          .join("")}
      </div>
      <div class="experiment-lab-actions">
        <button class="tool-button" type="button" data-experiment-lab-action="proof" title="Show proof experiments">PROOF</button>
        <button class="tool-button" type="button" data-experiment-lab-action="gates" title="Show blocked experiments">GATES</button>
        <button class="tool-button" type="button" data-experiment-lab-action="wins" title="Show validated outcomes">WINS</button>
      </div>
      <div class="experiment-lab-grid" aria-label="Experiment discovery lanes">
        ${records.map(renderExperimentDiscoveryCard).join("")}
        ${renderExperimentDiscoveryFutureSlots(records)}
      </div>
    </div>`;
}

function renderExperimentDiscoveryCard(record) {
  const { lane, counts, latest, mode, labScore } = record;
  const progress = Math.max(8, Math.min(100, Math.round(labScore)));
  return `
    <article
      class="experiment-lab-card ${escapeHtml(mode)} ${lane.id === state.selectedLaneId ? "active" : ""}"
      data-experiment-lab-lane="${escapeHtml(lane.id)}"
      style="${laneStyle(lane)} --experiment-progress:${progress}%;"
    >
      <div class="experiment-lab-card-top">
        ${avatarMarkup(lane, "experiment-lab-avatar")}
        <div>
          <p class="eyebrow">${escapeHtml(record.stage)}</p>
          <h3>${escapeHtml(compactText(lane.name, 58))}</h3>
          <span>${escapeHtml(lane.visual?.realm ?? lane.department)}</span>
        </div>
        <strong>L${formatNumber(lane.level ?? 1)}</strong>
      </div>
      <div class="experiment-lab-meter" aria-hidden="true"><i></i></div>
      <p>${escapeHtml(compactText(latest?.summary ?? lane.nextAction ?? lane.visual?.mood ?? "No experiment has lit up this lane yet.", 150))}</p>
      <div class="experiment-lab-card-stats">
        <span><strong>${formatNumber(counts.task ?? 0)}</strong><em>tests</em></span>
        <span><strong>${formatNumber(record.proof)}</strong><em>proof</em></span>
        <span><strong>${formatNumber(record.gates)}</strong><em>gates</em></span>
        <span><strong>${formatNumber(record.wins)}</strong><em>wins</em></span>
      </div>
    </article>`;
}

function renderExperimentDiscoveryFutureSlots(records) {
  const slots = [
    { label: "hypothesis slot", detail: "future test design" },
    { label: "proof socket", detail: "future evidence capture" },
    { label: "kill switch", detail: "future parked path marker" },
    { label: "win ritual", detail: "future unlock ceremony" },
  ];
  return slots
    .slice(0, 3)
    .map(
      (slot, index) => `
      <article class="experiment-lab-future">
        <span>+</span>
        <strong>${escapeHtml(slot.label)}</strong>
        <p>${escapeHtml(slot.detail)}</p>
        <em>bench ${formatNumber(records.length + index + 1)}</em>
      </article>`
    )
    .join("");
}

function allFeedViews() {
  return [...defaultFeedViews(), ...state.savedFeedViews];
}

function renderFeedSavedViews() {
  el.missionFeedFilter.value = state.feedFilter;
  el.feedSavedViews.innerHTML = allFeedViews()
    .map(
      (view) => `
        <button class="feed-view-chip ${view.filter === state.feedFilter ? "active" : ""}" type="button" data-feed-view="${escapeHtml(view.id)}">
          <span>${escapeHtml(view.label)}</span>
          <strong>${escapeHtml(stateLabel(view.filter))}</strong>
        </button>`
    )
    .join("");
}

function renderFeedPlayback(items) {
  if (el.feedPlaybackToggle) el.feedPlaybackToggle.textContent = state.feedPlaying ? "II" : "P";
  if (!items.length) {
    el.feedPlaybackTitle.textContent = "Timeline idle";
    el.feedPlaybackCount.textContent = "0/0";
    el.feedPlaybackCard.innerHTML = `
      <div class="feed-playback-empty">
        <p class="eyebrow">No Events</p>
        <h3>${escapeHtml(stateLabel(state.feedFilter))}</h3>
      </div>`;
    return;
  }
  const item = currentPlaybackItem(items);
  const scene = feedSceneForItem(item);
  const progress = items.length > 1 ? Math.round((state.feedPlaybackIndex / (items.length - 1)) * 100) : 100;
  el.feedPlaybackTitle.textContent = item.laneName ?? "Timeline event";
  el.feedPlaybackCount.textContent = `${formatNumber(state.feedPlaybackIndex + 1)}/${formatNumber(items.length)}`;
  el.feedPlaybackCard.innerHTML = `
    <div class="playback-rail" style="--playback-progress:${progress}%"><span></span></div>
    <article class="playback-event feed-scene-card ${escapeHtml(item.kind)} ${escapeHtml(scene.rarity)}" data-feed-lane-id="${escapeHtml(item.laneId)}" style="${feedSceneStyle(scene)}">
      ${feedSceneArt(scene, item, "playback")}
      <div class="feed-scene-copy">
        <div class="feed-item-top">
          <span class="badge ${escapeHtml(item.laneState)}">L${escapeHtml(item.laneLevel)} ${escapeHtml(stateLabel(item.laneState))}</span>
          <span>${escapeHtml(shortDate(item.time))}</span>
        </div>
        <div class="scene-reward-row">
          <strong>${escapeHtml(scene.rarity)}</strong>
          <span>+${formatNumber(scene.xp)} xp</span>
          <em>${escapeHtml(scene.status)}</em>
        </div>
        <h3>${escapeHtml(item.title)}</h3>
        <p>${escapeHtml(compactText(item.summary, 190))}</p>
        <div class="feed-meta">
          <strong>${escapeHtml(scene.realm)}</strong>
          <span>${escapeHtml(scene.kindLabel)} - ${escapeHtml(scene.statusLabel)}</span>
        </div>
      </div>
    </article>`;
}

function saveCurrentFeedView() {
  const id = `feed-view-${state.feedFilter}-${Date.now()}`;
  const label = `${stateLabel(state.feedFilter)} lens`;
  const existing = state.savedFeedViews.filter((view) => view.filter !== state.feedFilter);
  state.savedFeedViews = [{ id, label, filter: state.feedFilter }, ...existing].slice(0, 8);
  writeSavedFeedViews();
  renderMissionFeed();
}

function setFeedFilter(filter) {
  if (!feedKinds().includes(filter)) return;
  state.feedFilter = filter;
  state.feedPlaybackIndex = 0;
  writeFeedFilter();
  renderMissionFeed();
}

function stopFeedPlayback() {
  state.feedPlaying = false;
  if (state.feedPlaybackTimer) {
    clearInterval(state.feedPlaybackTimer);
    state.feedPlaybackTimer = null;
  }
}

function stepFeedPlayback(delta) {
  const items = filteredFeedItems();
  if (!items.length) return;
  state.feedPlaybackIndex = (state.feedPlaybackIndex + delta + items.length) % items.length;
  renderMissionFeed();
}

function renderMissionFeedItem(item) {
  const scene = feedSceneForItem(item);
  return `
    <article class="feed-item feed-scene-card ${escapeHtml(item.kind)} ${escapeHtml(scene.rarity)}" data-feed-lane-id="${escapeHtml(item.laneId)}" style="${feedSceneStyle(scene)}">
      ${feedSceneArt(scene, item)}
      <div class="feed-scene-copy">
        <div class="feed-item-top">
          <span class="badge ${escapeHtml(item.laneState)}">L${escapeHtml(item.laneLevel)} ${escapeHtml(stateLabel(item.laneState))}</span>
          <span>${escapeHtml(shortDate(item.time))}</span>
        </div>
        <div class="scene-reward-row">
          <strong>${escapeHtml(scene.rarity)}</strong>
          <span>+${formatNumber(scene.xp)} xp</span>
          <em>${escapeHtml(scene.status)}</em>
        </div>
        <h3>${escapeHtml(item.title)}</h3>
        <p>${escapeHtml(compactText(item.summary, 170))}</p>
        <div class="feed-meta">
          <strong>${escapeHtml(item.laneName)}</strong>
          <span>${escapeHtml(scene.realm)} - ${escapeHtml(scene.kindLabel)} - ${escapeHtml(scene.statusLabel)}</span>
        </div>
      </div>
    </article>`;
}

function filteredLanes() {
  const lanes = state.snapshot.lanes;
  if (state.filter === "all") return lanes;
  return lanes.filter((lane) => lane.state === state.filter);
}

function boundedProgress(value) {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return 0;
  return Math.max(0, Math.min(100, numeric));
}

function orderedLaneRailLanes(lanes) {
  const selected = lanes.find((lane) => lane.id === state.selectedLaneId);
  if (!selected) return lanes;
  return [selected, ...lanes.filter((lane) => lane.id !== state.selectedLaneId)];
}

function laneRailLevelSelectorMarkup(lane) {
  const counts = lane.counts ?? {};
  const gateCount = (counts.blockers ?? 0) + (counts.pendingRequests ?? 0);
  const rewardCount = counts.outcomes ?? 0;
  const activeCount = counts.activeTasks ?? 0;
  return `
        <span class="lane-level-selector" aria-label="Lane selector status">
          <span class="lane-level-cell level">
            <strong>L${escapeHtml(lane.level)}</strong>
            <em>${formatNumber(boundedProgress(lane.progress ?? 0))}%</em>
          </span>
          <span class="lane-level-cell gate ${gateCount ? "gated" : "clear"}">
            <strong>${formatNumber(gateCount)}</strong>
            <em>Gates</em>
          </span>
          <span class="lane-level-cell reward">
            <strong>${formatNumber(rewardCount)}</strong>
            <em>Wins</em>
          </span>
          <span class="lane-level-cell active">
            <strong>${formatNumber(activeCount)}</strong>
            <em>Live</em>
          </span>
        </span>`;
}

function laneRailSignalMarkup(lane) {
  const counts = lane.counts ?? {};
  const gateCount = (counts.blockers ?? 0) + (counts.pendingRequests ?? 0);
  return `
        <span class="lane-rail-signal" aria-hidden="true">
          <i class="lane-rail-pip level" style="--pip-fill:${boundedProgress((lane.level / 12) * 100)}%"></i>
          <i class="lane-rail-pip progress" style="--pip-fill:${boundedProgress(lane.progress ?? 0)}%"></i>
          <i class="lane-rail-pip gates" style="--pip-fill:${gateCount ? 100 : 12}%"></i>
        </span>`;
}

function laneRailWorldSignalMarkup(lane, index, total) {
  const minigame = lane.visual?.minigame ?? {};
  const title = minigame.title ?? lane.visual?.realm ?? lane.name;
  const custom = Boolean(minigameDefinition(lane));
  const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const initials =
    String(title)
      .split(/\s+/)
      .filter(Boolean)
      .slice(0, 2)
      .map((word) => word[0])
      .join("")
      .toUpperCase() || "W";
  return `
        <span class="lane-world-signal ${custom ? "custom" : "template"} ${gateCount ? "gated" : "ready"}" data-lane-world-signal="${escapeHtml(minigame.id ?? lane.id)}" aria-label="${escapeHtml(title)} world ${index + 1} of ${total}">
          <i>${escapeHtml(initials)}</i>
          <strong>${String(index + 1).padStart(2, "0")}</strong>
          <em>${escapeHtml(custom ? "play" : "seed")}</em>
        </span>`;
}

function laneRailUnlockLensMarkup(lane) {
  const custom = Boolean(minigameDefinition(lane));
  const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const stepCount = gameStepCount(lane);
  const ready = Math.round(((custom ? 35 : 12) + boundedProgress(lane.progress ?? 0) * 0.45 + Math.min(stepCount, 9) * 5) - Math.min(gateCount, 5) * 7);
  const tone = gateCount ? "gated" : custom && ready >= 70 ? "ready" : custom ? "wired" : "seed";
  return `
        <span class="lane-unlock-lens ${escapeHtml(tone)}" aria-hidden="true" style="--lane-unlock-ready:${boundedProgress(ready)}%;">
          <i>${escapeHtml(custom ? "GAME" : "SEED")}</i>
          <strong>${formatNumber(stepCount)}</strong>
          <em>${escapeHtml(gateCount ? `${formatNumber(gateCount)} gate` : `${formatNumber(Math.max(0, ready))}%`)}</em>
        </span>`;
}

function laneExpansionSlots(lanes) {
  const laneCount = lanes.length;
  const reserveCount = Math.max(0, laneCount - 7);
  const slotSeed = [
    ["path", "Next Path", "New lane", "PATH"],
    ["bot", "Bot Pod", "Operator", "BOT"],
    ["minigame", "Mini Game", "Custom vibe", "PLAY"],
    ["research", "Research Gate", "Signals", "SCAN"],
  ];

  return slotSeed.map(([id, title, caption, short], index) => {
    const readiness = boundedProgress(18 + index * 11 + Math.min(reserveCount, 6) * 4);
    return {
      id,
      title,
      caption,
      short,
      readiness,
      world: laneCount + index + 1,
      tone: readiness >= 58 ? "primed" : "seed",
    };
  });
}

function renderLaneList() {
  const lanes = orderedLaneRailLanes(filteredLanes());
  const expansionSlots = laneExpansionSlots(lanes);
  const activeIndex = Math.max(0, lanes.findIndex((lane) => lane.id === state.selectedLaneId));
  const overflowCount = Math.max(0, lanes.length - 7);
  el.laneList.dataset.laneSelectorMode = "gate";
  el.laneList.dataset.laneOverflowCount = String(Math.max(0, lanes.length - 7));
  el.laneList.dataset.laneExpansionSlots = String(expansionSlots.length);
  el.laneList.closest(".lane-list-panel")?.setAttribute("data-lane-overflow-count", String(overflowCount));
  el.laneList.closest(".lane-list-panel")?.setAttribute("data-lane-expansion-slots", String(expansionSlots.length));
  el.laneList.style.setProperty("--lane-board-active-index", activeIndex);
  el.laneList.style.setProperty("--lane-board-count", Math.max(1, lanes.length));
  el.laneList.style.setProperty("--lane-expansion-count", expansionSlots.length);
  el.laneList.innerHTML = `
    <div class="lane-territory-route" aria-hidden="true">
      <span class="lane-territory-route-line"></span>
      <span class="lane-territory-runner"></span>
      ${lanes
        .map(
          (lane, index) => `
            <i class="lane-territory-node ${lane.id === state.selectedLaneId ? "active" : ""} ${escapeHtml(lane.state)}" style="--lane-board-node-index:${index};"></i>`
        )
        .join("")}
    </div>` + lanes
    .map(
      (lane, index) => `
      <button class="lane-button ${lane.id === state.selectedLaneId ? "active" : ""} ${index > 6 ? "reserve" : ""}" type="button" data-lane-id="${escapeHtml(lane.id)}" data-lane-state="${escapeHtml(lane.state)}" data-lane-gate-rank="${index}" style="${laneStyle(lane)} --lane-progress:${boundedProgress(lane.progress ?? 0)}%; --lane-gate-offset:${index};">
        <div class="lane-button-top">
          <div class="lane-button-identity">
            ${avatarMarkup(lane, "lane-button-avatar")}
            <div>
            <h3>${escapeHtml(lane.name)}</h3>
              <p>${escapeHtml(lane.visual?.realm ?? lane.department)}</p>
            </div>
          </div>
          <span class="badge ${escapeHtml(lane.state)}">${escapeHtml(stateLabel(lane.state))}</span>
        </div>
        ${laneRailWorldSignalMarkup(lane, index, lanes.length)}
        ${laneRailUnlockLensMarkup(lane)}
        ${laneRailLevelSelectorMarkup(lane)}
        ${laneRailSignalMarkup(lane)}
        <div class="progress-track"><div class="progress-fill" style="width:${lane.progress}%"></div></div>
        <p class="small-muted">Level ${lane.level} - ${lane.counts.completedTasks} complete - ${lane.counts.blockers} blockers</p>
      </button>`
    )
    .join("") + `
    <div class="lane-expansion-slots" role="list" aria-label="Reserved future money path expansion slots">
      ${expansionSlots
        .map(
          (slot, index) => `
            <span class="lane-expansion-slot ${escapeHtml(slot.tone)}" role="listitem" data-lane-expansion-slot="${escapeHtml(slot.id)}" data-lane-expansion-rank="${index}" style="--lane-expansion-rank:${index}; --lane-expansion-ready:${slot.readiness}%;">
              <i>${escapeHtml(slot.short)}</i>
              <strong>${escapeHtml(slot.title)}</strong>
              <em>W${formatNumber(slot.world)} - ${escapeHtml(slot.caption)}</em>
            </span>`
        )
        .join("")}
    </div>`;
}

function renderMap() {
  const lanes = state.snapshot.lanes;
  const sorted = [...lanes].sort((a, b) => b.score - a.score);
  const home = { x: 50, y: 50 };
  const playbackItem = currentPlaybackItem();
  const playbackLane = lanes.find((lane) => lane.id === playbackItem?.laneId);

  if (el.mapPlaybackHud) {
    el.mapPlaybackHud.innerHTML = playbackItem
      ? `
        <p class="eyebrow">Playback Signal</p>
        <h3>${escapeHtml(playbackItem.laneName)}</h3>
        <span>${escapeHtml(stateLabel(playbackItem.kind))} - ${escapeHtml(compactText(playbackItem.title, 62))}</span>`
      : `
        <p class="eyebrow">Playback Signal</p>
        <h3>Timeline idle</h3>
        <span>No event selected</span>`;
  }

  el.routeSvg.innerHTML = lanes
    .map((lane, index) => {
      const hot = sorted.slice(0, 4).some((item) => item.id === lane.id);
      const playbackHot = lane.id === playbackLane?.id;
      const midX = (home.x + lane.map.x) / 2 + (index % 2 ? 8 : -8);
      const midY = (home.y + lane.map.y) / 2 + (index % 3 ? -5 : 6);
      return `<path class="route-line ${hot ? "hot" : ""} ${playbackHot ? "playback-route" : ""}" data-route-lane-id="${escapeHtml(lane.id)}" d="M ${home.x} ${home.y} Q ${midX} ${midY} ${lane.map.x} ${lane.map.y}" />`;
    })
    .join("");

  el.nodeLayer.innerHTML = lanes
    .map((lane, index) => {
      const colors = palette[index % palette.length];
      const playbackHot = lane.id === playbackLane?.id;
      return `
        <button
          class="lane-node ${lane.id === state.selectedLaneId ? "active" : ""} ${playbackHot ? "playback-hot" : ""}"
          type="button"
          data-lane-id="${escapeHtml(lane.id)}"
          data-playback-kind="${escapeHtml(playbackHot ? playbackItem.kind : "")}"
          style="left:${lane.map.x}%; top:${lane.map.y}%; --node-a:${lane.visual?.accent ?? colors[0]}; --node-b:${lane.visual?.accentAlt ?? colors[1]};"
        >
          <span class="node-aura" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
          ${playbackHot ? `<i class="node-pulse" aria-hidden="true"></i><em class="playback-chip">${escapeHtml(stateLabel(playbackItem.kind))}</em>` : ""}
          <span class="node-level">L${lane.level}</span>
          ${avatarMarkup(lane, "node-avatar")}
          <strong>${escapeHtml(lane.name)}</strong>
          <span>${escapeHtml(lane.visual?.realm ?? lane.department)}</span>
        </button>`;
    })
    .join("");
  renderMapFocus();
}

function mapFocusLane() {
  const focusId = state.hoveredLaneId ?? state.selectedLaneId;
  return state.snapshot?.lanes?.find((lane) => lane.id === focusId) ?? null;
}

function renderMapFocus() {
  const lane = mapFocusLane();
  el.routeSvg?.querySelectorAll("[data-route-lane-id]").forEach((route) => {
    route.classList.toggle("map-focus-route", Boolean(lane && route.dataset.routeLaneId === lane.id));
  });
  el.nodeLayer?.querySelectorAll("[data-lane-id]").forEach((node) => {
    node.classList.toggle("map-focus", Boolean(lane && node.dataset.laneId === lane.id));
  });
  if (!el.mapFocusPanel) return;
  if (!lane) {
    el.mapFocusPanel.hidden = true;
    el.mapFocusPanel.innerHTML = "";
    return;
  }
  el.mapFocusPanel.hidden = false;
  el.mapFocusPanel.setAttribute("style", laneStyle(lane));
  el.mapFocusPanel.innerHTML = `
    <p class="eyebrow">Lane Focus</p>
    <h3>${escapeHtml(lane.name)}</h3>
    <div class="map-focus-stats">
      <span>L${escapeHtml(lane.level)}</span>
      <span>${escapeHtml(stateLabel(lane.state))}</span>
      <span>${formatNumber(lane.counts?.outcomes ?? 0)} unlocks</span>
    </div>
    <p>${escapeHtml(compactText(lane.visual?.mood || lane.notes || lane.examples?.join(", "), 120))}</p>`;
}

function setMapHover(laneId) {
  if (state.hoveredLaneId === laneId) return;
  state.hoveredLaneId = laneId;
  renderMapFocus();
}

function renderActiveLaneLevelHud(lane) {
  const trail = chronicleTrail(lane);
  const phase = chroniclePhase(lane, trail);
  const newest = trail[0];
  const nextAction = chronicleNextAction(lane);
  const ownerAgent = laneAgents(lane)[0];
  const botName = ownerAgent?.visual?.callsign ?? ownerAgent?.name ?? lane.ownerAgentId ?? "Lane bot";
  const specialty = ownerAgent?.visual?.specialty ?? lane.visual?.realm ?? lane.department ?? "Active lane";
  const laneXp = Math.max(0, Math.min(100, Number(lane.progress ?? 0)));
  const completed = lane.counts?.completedTasks ?? Math.max(0, (lane.counts?.tasks ?? 0) - (lane.counts?.activeTasks ?? 0));
  const taskTotal = lane.counts?.tasks ?? 0;
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const trackSignals = [
    { label: "XP", value: `${formatNumber(laneXp)}%`, tone: laneXp >= 90 ? "unlocked" : "advancing" },
    { label: "Proof", value: formatNumber(lane.counts?.evidence ?? 0), tone: "scouting" },
    { label: "Cleared", value: `${formatNumber(completed)}/${formatNumber(taskTotal)}`, tone: "unlocked" },
    { label: "Gates", value: formatNumber(blockerPressure), tone: blockerPressure ? "gated" : "unlocked" },
  ];
  const latestTitle = newest?.title ?? newest?.type ?? newest?.kind ?? "No lane event yet";
  const latestMeta = newest ? `${stateLabel(newest.kind ?? newest.type ?? "event")} | ${shortDate(newest.time ?? newest.createdAt)}` : "Waiting for first recorded unlock";
  const arenaNodes = activeLaneArenaNodes(lane, trail, phase, blockerPressure);
  const sparks = activeLaneHudSparks(lane, blockerPressure);
  const switchRecords = activeLaneSwitchRecords(lane);
  const microChronicleCards = activeLaneMicroChronicleCards(lane, trail, nextAction);
  const viewPortals = activeLaneViewPortalRecords(lane);
  const viewTransition = activeLaneViewTransition(lane, viewPortals);
  const worldMapNodes = activeLaneWorldMapNodes(lane, trail, phase, blockerPressure, ownerAgent, nextAction);

  return `
    <section class="active-lane-level-hud" style="${laneStyle(lane)} --hud-progress:${laneXp}%;" aria-label="Active lane level HUD">
      <div class="active-lane-hud-depth-field" aria-hidden="true">
        ${sparks
          .map(
            (spark) =>
              `<span class="active-lane-hud-spark" data-spark-tone="${escapeHtml(spark.tone)}" style="--spark-x:${spark.x}%; --spark-y:${spark.y}%; --spark-size:${spark.size}px; --spark-delay:${spark.delay}ms;"></span>`
          )
          .join("")}
      </div>
      <div class="active-lane-hud-core">
        ${avatarMarkup(lane, "active-lane-hud-avatar")}
        <div class="active-lane-hud-title">
          <span>${escapeHtml(phase.label)}</span>
          <strong>${escapeHtml(lane.name)}</strong>
          <em>${escapeHtml(compactText(lane.visual?.mood ?? lane.notes ?? phase.summary, 92))}</em>
        </div>
        <div class="active-lane-hud-meter" aria-label="Lane progress ${escapeHtml(laneXp)} percent">
          <span></span>
          <b>L${escapeHtml(lane.level)}</b>
        </div>
      </div>
      <div class="active-lane-hud-track">
        ${trackSignals
          .map(
            (signal, index) => `
              <div class="active-lane-hud-signal ${escapeHtml(signal.tone)}" style="--signal-index:${index}">
                <strong>${escapeHtml(signal.value)}</strong>
                <span>${escapeHtml(signal.label)}</span>
              </div>`
          )
          .join("")}
      </div>
      <div class="active-lane-hud-bot">
        ${agentCharacterFrame(ownerAgent, lane, "active-lane-hud-bot-avatar")}
        <div class="active-lane-hud-bot-copy">
          <span>${escapeHtml(botName)}</span>
          <strong>${escapeHtml(compactText(specialty, 46))}</strong>
        </div>
        <div class="active-lane-hud-next">
          <span>${escapeHtml(latestMeta)}</span>
          <strong>${escapeHtml(compactText(latestTitle, 58))}</strong>
          <em>${escapeHtml(compactText(nextAction, 88))}</em>
        </div>
      </div>
      <div class="active-lane-hud-arena" aria-label="Lane run route">
        <div class="active-lane-hud-route">
          <span class="active-lane-hud-runner"></span>
          ${arenaNodes
            .map(
              (node, index) => `
                <div class="active-lane-hud-node ${escapeHtml(node.tone)}" style="--arena-index:${index}">
                  <span>${escapeHtml(node.label)}</span>
                  <strong>${escapeHtml(node.value)}</strong>
                </div>`
            )
          .join("")}
        </div>
      </div>
      <div class="active-lane-world-map" style="--world-progress:${laneXp}%;" aria-label="Selected lane world map">
        <span class="active-lane-world-runner" aria-hidden="true"></span>
        ${worldMapNodes
          .map(
            (node, index) => `
              <article class="active-lane-world-node ${escapeHtml(node.tone)}" style="--world-index:${index}">
                <span>${escapeHtml(node.label)}</span>
                <strong>${escapeHtml(node.value)}</strong>
                <em>${escapeHtml(node.body)}</em>
              </article>`
          )
          .join("")}
      </div>
      <div class="active-lane-control-matrix" aria-label="Active lane command matrix">
        <span class="active-lane-control-matrix-rail" aria-hidden="true"></span>
        <div class="active-lane-micro-chronicle" data-matrix-area="chronicle" aria-label="Lane micro chronicle">
          ${microChronicleCards
            .map(
              (card) => `
                <article class="active-lane-micro-card" data-micro-tone="${escapeHtml(card.tone)}">
                  <span>${escapeHtml(card.label)}</span>
                  <strong>${escapeHtml(card.title)}</strong>
                  <em>${escapeHtml(card.body)}</em>
                </article>`
            )
            .join("")}
        </div>
        <nav class="active-lane-view-portals" data-matrix-area="views" aria-label="Lane view portals">
          ${viewPortals
            .map(
              (portal) => `
                <button class="active-lane-view-portal ${state.detailView === portal.id ? "active" : ""} ${escapeHtml(portal.tone)}" type="button" data-detail-view="${escapeHtml(portal.id)}" aria-pressed="${state.detailView === portal.id ? "true" : "false"}">
                  <span>${escapeHtml(portal.label)}</span>
                  <strong>${escapeHtml(portal.value)}</strong>
                </button>`
            )
            .join("")}
        </nav>
        <div class="active-lane-view-transition" data-matrix-area="transition" style="--view-step:${viewTransition.step}; --view-count:${viewTransition.count};" aria-label="Active view transition">
          <span>${escapeHtml(viewTransition.label)}</span>
          <div class="active-lane-view-transition-track" aria-hidden="true">
            <i class="active-lane-view-transition-runner"></i>
          </div>
          <strong>${escapeHtml(viewTransition.meta)}</strong>
        </div>
        <nav class="active-lane-switch-deck" data-matrix-area="switch" aria-label="Quick lane switch">
          ${switchRecords
            .map(
              (record) => `
                <button class="active-lane-switch-chip ${record.id === lane.id ? "active" : ""} ${escapeHtml(record.tone)}" type="button" data-lane-id="${escapeHtml(record.id)}" aria-pressed="${record.id === lane.id ? "true" : "false"}" style="${laneStyle(record)}">
                  <span>${escapeHtml(record.shortName)}</span>
                  <strong>L${escapeHtml(record.level)}</strong>
                  <em>${escapeHtml(record.meta)}</em>
                </button>`
            )
            .join("")}
        </nav>
      </div>
    </section>`;
}

function activeLaneWorldMapNodes(lane, trail, phase, blockerPressure, ownerAgent, nextAction) {
  const checkpoints = lane.quest?.checkpoints ?? [];
  const completedCheckpoints = checkpoints.filter((checkpoint) => checkpoint.status === "complete").length;
  const activeCheckpoint = checkpoints.find((checkpoint) => checkpoint.status !== "complete") ?? checkpoints.at(-1);
  const proofCount = lane.counts?.evidence ?? 0;
  const botName = ownerAgent?.visual?.callsign ?? ownerAgent?.name ?? lane.ownerAgentId ?? "Lane bot";
  const latest = trail[0];
  const latestLabel = latest ? stateLabel(latest.kind ?? latest.type ?? "event") : phase.label;
  return [
    {
      label: "World",
      value: compactText(lane.visual?.realm ?? lane.department ?? lane.name, 20),
      body: `${formatNumber(lane.counts?.traces ?? 0)} traces`,
      tone: trail.length ? "advancing" : "scouting",
    },
    {
      label: "Level",
      value: `L${formatNumber(lane.level ?? 0)}`,
      body: `${formatNumber(lane.progress ?? 0)}% xp`,
      tone: (lane.progress ?? 0) >= 90 ? "unlocked" : "advancing",
    },
    {
      label: "Quest",
      value: checkpoints.length ? `${formatNumber(completedCheckpoints)}/${formatNumber(checkpoints.length)}` : latestLabel,
      body: compactText(activeCheckpoint?.title ?? activeCheckpoint?.label ?? latestLabel, 30),
      tone: checkpoints.length && completedCheckpoints >= checkpoints.length ? "unlocked" : phase.tone,
    },
    {
      label: "Proof",
      value: formatNumber(proofCount),
      body: proofCount ? "evidence bank" : "needs proof",
      tone: proofCount ? "unlocked" : "scouting",
    },
    {
      label: "Gate",
      value: formatNumber(blockerPressure),
      body: blockerPressure ? "operator needed" : "clear",
      tone: blockerPressure ? "gated" : "unlocked",
    },
    {
      label: "Bot",
      value: compactText(botName, 18),
      body: compactText(nextAction, 34),
      tone: blockerPressure ? "gated" : "advancing",
    },
  ];
}

function activeLaneArenaNodes(lane, trail, phase, blockerPressure) {
  const checkpoints = lane.quest?.checkpoints ?? [];
  const completedCheckpoints = checkpoints.filter((checkpoint) => checkpoint.status === "complete").length;
  return [
    { label: "Spawn", value: `L${formatNumber(lane.level ?? 0)}`, tone: "unlocked" },
    { label: "Quest", value: checkpoints.length ? `${formatNumber(completedCheckpoints)}/${formatNumber(checkpoints.length)}` : phase.label, tone: phase.tone },
    { label: "Proof", value: formatNumber(lane.counts?.evidence ?? 0), tone: "scouting" },
    { label: "Gate", value: formatNumber(blockerPressure), tone: blockerPressure ? "gated" : "unlocked" },
    { label: "Trail", value: formatNumber(trail.length), tone: trail.length ? "advancing" : "scouting" },
  ];
}

function activeLaneHudSparks(lane, blockerPressure) {
  const seed = String(lane.id ?? lane.name ?? "lane")
    .split("")
    .reduce((total, letter) => total + letter.charCodeAt(0), 0);
  const tone = blockerPressure ? "gated" : lane.promotionCandidate?.ready_for_manual_promotion ? "unlocked" : "advancing";
  return Array.from({ length: 9 }, (_, index) => {
    const mixed = seed + index * 37 + (lane.level ?? 0) * 11;
    return {
      x: 8 + (mixed % 84),
      y: 12 + ((mixed * 7) % 72),
      size: 2 + (mixed % 4),
      delay: index * 170,
      tone,
    };
  });
}

function activeLaneSwitchRecords(lane) {
  const lanes = state.snapshot?.lanes ?? [];
  const ranked = lanes
    .filter((item) => item.id !== lane.id)
    .map((item) => ({
      lane: item,
      rank: (item.counts?.blockers ?? 0) * 28 + (item.counts?.activeTasks ?? 0) * 10 + (item.counts?.pendingRequests ?? 0) * 8 + (item.level ?? 0),
    }))
    .sort((a, b) => b.rank - a.rank)
    .slice(0, 5)
    .map((item) => item.lane);
  return [lane, ...ranked].map((item) => ({
    ...item,
    shortName: compactText(item.name, 24),
    tone: commandStatus(item).tone,
    meta: item.counts?.blockers ? `${formatNumber(item.counts.blockers)} gates` : `${formatNumber(item.progress ?? 0)}% xp`,
  }));
}

function activeLaneMicroChronicleCards(lane, trail, nextAction) {
  const gate = lane.gateMap?.[0] ?? lane.serviceRequests?.find((request) => request.status === "needs_review") ?? lane.serviceRequests?.[0];
  const latest = trail[0] ?? lane.recentTasks?.[0] ?? lane.recentOutcomes?.[0];
  const latestTitle = latest?.title ?? latest?.type ?? latest?.kind ?? "Awaiting first event";
  const latestBody = latest?.summary ?? latest?.nextAction ?? latest?.evidence ?? "No recent lane record is visible yet.";
  const gateTitle = gate?.workerType ?? gate?.type ?? gate?.id ?? "Gate clear";
  const gateBody = gate?.nextAction ?? gate?.requestedAction ?? gate?.gate ?? gate?.riskGate ?? "No active blocker is recorded in the current snapshot.";
  return [
    { label: "Latest", title: compactText(latestTitle, 44), body: compactText(latestBody, 92), tone: latest ? "advancing" : "scouting" },
    { label: "Gate", title: compactText(gateTitle, 44), body: compactText(gateBody, 92), tone: gate ? "gated" : "unlocked" },
    { label: "Next", title: "Operator move", body: compactText(nextAction, 104), tone: gate ? "gated" : "advancing" },
  ];
}

function activeLaneViewPortalRecords(lane) {
  const counts = lane.counts ?? {};
  return [
    { id: "overview", label: "Overview", value: `L${formatNumber(lane.level ?? 0)}`, tone: "scouting" },
    { id: "path", label: "Path", value: `${formatNumber(lane.progress ?? 0)}%`, tone: "advancing" },
    { id: "chronicle", label: "Chronicle", value: formatNumber((lane.trail ?? lane.milestones ?? []).length), tone: "advancing" },
    { id: "trail", label: "Trail", value: formatNumber(counts.traces ?? 0), tone: "scouting" },
    { id: "game", label: "Game", value: formatNumber(gameStepCount(lane)), tone: "unlocked" },
    { id: "comms", label: "Comms", value: formatNumber(laneAgents(lane).length || 1), tone: (counts.blockers ?? 0) ? "gated" : "unlocked" },
  ];
}

function activeLaneViewTransition(lane, viewPortals) {
  const count = Math.max(1, viewPortals.length);
  const step = Math.max(0, viewPortals.findIndex((portal) => portal.id === state.detailView));
  const active = viewPortals[Math.max(0, step)] ?? viewPortals[0];
  return {
    step,
    count,
    label: active?.label ?? stateLabel(state.detailView),
    meta: active ? `${active.value} ${active.id}` : lane.visual?.realm ?? lane.department ?? "view",
  };
}

function activeLaneStageLens(lane) {
  const trailDepth = (lane.trail ?? lane.milestones ?? []).length;
  const gatePressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const activeWork = (lane.counts?.activeTasks ?? 0) + (lane.counts?.serviceRequests ?? 0);
  return {
    label: stateLabel(state.detailView),
    title: lane.visual?.realm ?? lane.department ?? lane.name,
    meta: `L${formatNumber(lane.level ?? 0)} / ${formatNumber(lane.progress ?? 0)}% XP`,
    signals: [
      { label: "gates", value: formatNumber(gatePressure), tone: gatePressure ? "gated" : "unlocked" },
      { label: "work", value: formatNumber(activeWork), tone: activeWork ? "advancing" : "scouting" },
      { label: "trail", value: formatNumber(trailDepth), tone: trailDepth ? "advancing" : "scouting" },
    ],
  };
}

function activeLaneHoloBoardNodes(lane) {
  const counts = lane.counts ?? {};
  const trailDepth = (lane.trail ?? lane.milestones ?? []).length;
  const gatePressure = (counts.blockers ?? 0) + (counts.pendingRequests ?? 0);
  const activeWork = (counts.activeTasks ?? 0) + (counts.serviceRequests ?? 0);
  return [
    { label: "Spawn", value: `L${formatNumber(lane.level ?? 0)}`, tone: "unlocked" },
    { label: "XP", value: `${formatNumber(lane.progress ?? 0)}%`, tone: (lane.progress ?? 0) > 70 ? "unlocked" : "advancing" },
    { label: "Gate", value: formatNumber(gatePressure), tone: gatePressure ? "gated" : "unlocked" },
    { label: "Work", value: formatNumber(activeWork), tone: activeWork ? "advancing" : "scouting" },
    { label: "Trail", value: formatNumber(trailDepth), tone: trailDepth ? "advancing" : "scouting" },
  ].map((node, index) => ({ ...node, index }));
}

function activeLaneStageMotes(lane) {
  const seedText = `${lane.id}:${lane.level ?? 0}:${lane.progress ?? 0}:${lane.counts?.blockers ?? 0}:${lane.counts?.traces ?? 0}`;
  const seed = Array.from(seedText).reduce((sum, char) => sum + char.charCodeAt(0), 0);
  const gatePressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  return Array.from({ length: 9 }, (_, index) => {
    const drift = seed + index * 37;
    return {
      index,
      x: 7 + (drift * 17) % 86,
      y: 10 + (drift * 23) % 74,
      size: 4 + (drift % 9),
      delay: -1 * ((drift * 19) % 4600),
      tone: gatePressure && index % 3 === 0 ? "gated" : index % 2 === 0 ? "unlocked" : "advancing",
    };
  });
}

function activeLaneStageHoloFloor(lane) {
  const counts = lane.counts ?? {};
  const gatePressure = (counts.blockers ?? 0) + (counts.pendingRequests ?? 0);
  const checkpoints = lane.quest?.checkpoints ?? [];
  const completedCheckpoints = checkpoints.filter((checkpoint) => checkpoint.status === "complete").length;
  const questProgress = checkpoints.length ? `${formatNumber(completedCheckpoints)}/${formatNumber(checkpoints.length)}` : `${formatNumber(lane.progress ?? 0)}%`;
  return {
    progress: Math.max(4, Math.min(96, lane.progress ?? 0)),
    pads: [
      { label: "Level", value: `L${formatNumber(lane.level ?? 0)}`, tone: "unlocked" },
      { label: "Quest", value: questProgress, tone: checkpoints.length && completedCheckpoints < checkpoints.length ? "advancing" : "unlocked" },
      { label: "Proof", value: formatNumber(counts.evidence ?? 0), tone: (counts.evidence ?? 0) ? "unlocked" : "scouting" },
      { label: "Gates", value: formatNumber(gatePressure), tone: gatePressure ? "gated" : "unlocked" },
      { label: "Trail", value: formatNumber(counts.traces ?? 0), tone: (counts.traces ?? 0) ? "advancing" : "scouting" },
    ],
  };
}

function activeLaneObjectiveBeacons(lane) {
  const counts = lane.counts ?? {};
  const gatePressure = (counts.blockers ?? 0) + (counts.pendingRequests ?? 0);
  const activeWork = (counts.activeTasks ?? 0) + (counts.serviceRequests ?? 0);
  return [
    {
      label: "objective",
      value: compactText(lane.visual?.realm ?? lane.department ?? lane.name, 30),
      body: compactText(lane.visual?.mood ?? lane.notes ?? "Advance this lane toward verified money-path proof.", 86),
      tone: "scouting",
    },
    {
      label: "progress",
      value: `${formatNumber(lane.progress ?? 0)}%`,
      body: `Level ${formatNumber(lane.level ?? 0)} / ${formatNumber(counts.completedTasks ?? 0)} clears`,
      tone: (lane.progress ?? 0) >= 80 ? "unlocked" : "advancing",
    },
    {
      label: "gates",
      value: formatNumber(gatePressure),
      body: gatePressure ? "Blockers need proof or operator decision." : "No active gate pressure.",
      tone: gatePressure ? "gated" : "unlocked",
    },
    {
      label: "choice",
      value: activeWork ? `${formatNumber(activeWork)} live` : "next",
      body: compactText(chronicleNextAction(lane), 92),
      tone: activeWork ? "advancing" : "scouting",
    },
  ];
}

function activeLaneBotPartyRecords(lane) {
  const status = commandStatus(lane);
  const agents = laneAgents(lane).slice(0, 3);
  const fallback = agents.length ? agents : [{ agent_id: lane.ownerAgentId ?? "lane-bot", name: lane.ownerAgentId ?? "Lane bot", visual: {} }];
  const nextAction = chronicleNextAction(lane);
  return fallback.map((agent, index) => ({
    agent,
    callsign: agent.visual?.callsign ?? agent.name ?? agent.agent_id ?? `Bot ${index + 1}`,
    status: index === 0 ? status.label : agent.visual?.specialty ?? lane.visual?.realm ?? "Support",
    action: compactText(index === 0 ? nextAction : agent.visual?.specialty ?? lane.department ?? nextAction, 72),
    tone: index === 0 ? status.tone : (lane.counts?.blockers ?? 0) ? "gated" : "advancing",
  }));
}

function activeLaneStageEventRibbon(lane) {
  const trail = chronicleTrail(lane);
  const latest = trail[0] ?? lane.recentTasks?.[0] ?? lane.recentOutcomes?.[0];
  const gate = lane.gateMap?.[0] ?? lane.serviceRequests?.find((request) => request.status === "needs_review") ?? lane.serviceRequests?.[0];
  const proofCount = lane.counts?.evidence ?? 0;
  const nextAction = chronicleNextAction(lane);
  const cells = [
    {
      label: "event",
      value: compactText(latest?.title ?? latest?.type ?? latest?.kind ?? "waiting", 22),
      body: latest ? shortDate(latest.time ?? latest.createdAt) : "no record",
      tone: latest ? "advancing" : "scouting",
    },
    {
      label: "proof",
      value: formatNumber(proofCount),
      body: proofCount ? "evidence" : "needed",
      tone: proofCount ? "unlocked" : "scouting",
    },
    {
      label: "gate",
      value: gate ? "blocked" : "clear",
      body: compactText(gate?.nextAction ?? gate?.requestedAction ?? gate?.gate ?? "ready", 24),
      tone: gate ? "gated" : "unlocked",
    },
    {
      label: "next",
      value: "move",
      body: compactText(nextAction, 28),
      tone: gate ? "gated" : "advancing",
    },
  ];

  return `
        <div class="active-lane-stage-event-ribbon" aria-label="Mounted stage event ribbon">
          <span class="active-lane-stage-event-runner" aria-hidden="true"></span>
          ${cells
            .map(
              (cell, index) => `
                <span class="active-lane-stage-event-cell ${escapeHtml(cell.tone)}" style="--event-index:${index}">
                  <b>${escapeHtml(cell.label)}</b>
                  <strong>${escapeHtml(cell.value)}</strong>
                  <i>${escapeHtml(cell.body)}</i>
                </span>`
            )
            .join("")}
        </div>`;
}

function activeLaneStageFooterRail(lane) {
  const checkpoints = lane.quest?.checkpoints ?? [];
  const completedCheckpoints = checkpoints.filter((checkpoint) => checkpoint.status === "complete").length;
  const questProgress = checkpoints.length ? Math.round((completedCheckpoints / checkpoints.length) * 100) : lane.progress ?? 0;
  const gatePressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const nextAction = chronicleNextAction(lane);
  const cells = [
    { label: "level", value: `L${formatNumber(lane.level ?? 0)}`, body: `${formatNumber(lane.progress ?? 0)}% xp`, tone: "unlocked" },
    { label: "quest", value: `${formatNumber(questProgress)}%`, body: `${formatNumber(completedCheckpoints)}/${formatNumber(checkpoints.length || 1)} gates`, tone: questProgress >= 100 ? "unlocked" : "advancing" },
    { label: "gates", value: formatNumber(gatePressure), body: gatePressure ? "pressure" : "clear", tone: gatePressure ? "gated" : "unlocked" },
    { label: "next", value: "move", body: compactText(nextAction, 54), tone: gatePressure ? "gated" : "scouting" },
  ];

  return `
        <div class="active-lane-stage-footer-rail" aria-label="Mounted stage status rail">
          ${cells
            .map(
              (cell, index) => `
                <span class="active-lane-stage-footer-cell ${escapeHtml(cell.tone)}" style="--footer-index:${index}">
                  <b>${escapeHtml(cell.value)}</b>
                  <strong>${escapeHtml(cell.label)}</strong>
                  <i>${escapeHtml(cell.body)}</i>
                </span>`
            )
            .join("")}
        </div>`;
}

function cockpitControlPadModel(lane) {
  const agents = state.snapshot?.agents ?? [];
  const owner = agents.find((agent) => agent.lane === lane.id || agent.laneId === lane.id || agent.boundLaneId === lane.id || agent.ownerLaneId === lane.id);
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);
  const gameCount = gameStepCount(lane);
  const suggestion = bestLaneDispatchSuggestion(lane);
  const actions = [
    {
      id: "path",
      label: "Path",
      value: `L${formatNumber(lane.level ?? 0)}`,
      meta: `${formatNumber(lane.progress ?? 0)}% run`,
      tone: "advancing",
      view: "path",
    },
    {
      id: "gate",
      label: "Gate",
      value: blockerPressure ? formatNumber(blockerPressure) : "clear",
      meta: blockerPressure ? "review" : "open",
      tone: blockerPressure ? "gated" : "ready",
      view: "trail",
    },
    {
      id: "proof",
      label: "Proof",
      value: formatNumber(proofCount),
      meta: proofCount ? "captured" : "needed",
      tone: proofCount ? "unlocked" : "scouting",
      view: "chronicle",
    },
    {
      id: "bot",
      label: "Bot",
      value: owner ? compactText(owner.callsign ?? owner.name ?? owner.id, 10) : "slot",
      meta: owner ? "online" : "open",
      tone: owner ? "ready" : "scouting",
      view: "comms",
    },
    {
      id: "game",
      label: "Game",
      value: gameCount ? formatNumber(gameCount) : "seed",
      meta: lane.visual?.minigame?.title ? compactText(lane.visual.minigame.title, 14) : "arcade",
      tone: gameCount ? "advancing" : "ready",
      view: "game",
    },
    {
      id: "queue",
      label: "Queue",
      value: suggestion ? "Q" : "scan",
      meta: suggestion ? compactText(suggestion.kind ?? suggestion.title ?? suggestion.command, 14) : "next",
      tone: suggestion ? "staged" : "ready",
      command: true,
    },
  ];

  return {
    laneId: lane.id,
    laneName: lane.name,
    tone: blockerPressure ? "gated" : suggestion ? "ready" : "scouting",
    progress: Math.max(8, Math.min(100, lane.progress ?? 0)),
    actions,
  };
}

function renderCockpitControlPad(model) {
  return `
        <nav class="cockpit-control-pad" data-cockpit-control-tone="${escapeHtml(model.tone)}" aria-label="${escapeHtml(model.laneName)} cockpit controls" style="--cockpit-control-progress:${model.progress}%;">
          ${model.actions
            .map(
              (action, index) => `
                <button class="cockpit-control-action ${escapeHtml(action.tone)}" type="button" data-cockpit-control-action="${escapeHtml(action.id)}" data-cockpit-control-lane="${escapeHtml(model.laneId)}" data-cockpit-control-tone="${escapeHtml(action.tone)}" style="--cockpit-control-index:${index};" title="${escapeHtml(action.label)}: ${escapeHtml(action.meta)}">
                  <span>${escapeHtml(action.label)}</span>
                  <strong>${escapeHtml(action.value)}</strong>
                  <em>${escapeHtml(action.meta)}</em>
                </button>`
            )
            .join("")}
        </nav>`;
}
function cockpitRunwayPulseModel(lane) {
  const trail = chronicleTrail(lane);
  const latest = trail[0];
  const suggestion = bestLaneDispatchSuggestion(lane);
  const taskCount = lane.counts?.tasks ?? 0;
  const blockerCount = lane.counts?.blockers ?? 0;
  const pendingCount = lane.counts?.pendingRequests ?? 0;
  const proofCount = lane.counts?.evidence ?? 0;
  const outcomeCount = lane.counts?.outcomes ?? 0;
  const blockerPressure = blockerCount + pendingCount;
  const nextMove = chronicleNextAction(lane);
  const pulses = [
    {
      id: "latest",
      label: "Latest",
      value: latest?.title ? compactText(latest?.title, 28) : "No event yet",
      meta: latest ? shortDate(latest.time ?? latest.createdAt) : "waiting",
      tone: latest ? "live" : "seed",
      view: "trail",
    },
    {
      id: "task",
      label: "Tasks",
      value: taskCount ? formatNumber(taskCount) : "idle",
      meta: taskCount ? "active" : "open slot",
      tone: taskCount ? "advancing" : "scouting",
      view: "path",
    },
    {
      id: "blocker",
      label: "Gate",
      value: blockerPressure ? formatNumber(blockerPressure) : "clear",
      meta: blockerPressure ? "needs review" : "route open",
      tone: blockerPressure ? "gated" : "ready",
      view: "trail",
    },
    {
      id: "proof",
      label: "Proof",
      value: proofCount + outcomeCount ? formatNumber(proofCount + outcomeCount) : "0",
      meta: proofCount || outcomeCount ? "signals" : "needed",
      tone: proofCount || outcomeCount ? "unlocked" : "scouting",
      view: "chronicle",
    },
    {
      id: "next",
      label: "Next",
      value: suggestion ? "queue" : "move",
      meta: suggestion ? compactText(suggestion.kind ?? suggestion.title ?? suggestion.command, 26) : compactText(chronicleNextAction(lane), 26),
      tone: suggestion ? "staged" : "advancing",
      view: suggestion ? "comms" : "overview",
    },
  ];

  return {
    laneId: lane.id,
    tone: blockerPressure ? "gated" : latest ? "live" : "seed",
    progress: Math.max(8, Math.min(100, lane.progress ?? 0)),
    nextMove,
    pulses,
  };
}

function renderCockpitRunwayPulse(model) {
  return `
        <div class="cockpit-runway-pulse" data-cockpit-runway-tone="${escapeHtml(model.tone)}" aria-label="Cockpit runway pulse" style="--cockpit-runway-progress:${model.progress}%;">
          <span class="cockpit-runway-core" aria-label="${escapeHtml(compactText(model.nextMove, 80))}">
            <b>Runway</b>
            <strong>${formatNumber(model.progress)}%</strong>
          </span>
          ${model.pulses
            .map(
              (pulse, index) => `
                <button class="cockpit-runway-node ${escapeHtml(pulse.tone)}" type="button" data-detail-view="${escapeHtml(pulse.view)}" data-cockpit-runway-pulse="${escapeHtml(pulse.id)}" style="--cockpit-runway-index:${index};" title="${escapeHtml(pulse.label)}: ${escapeHtml(pulse.meta)}">
                  <i aria-hidden="true"></i>
                  <span>${escapeHtml(pulse.label)}</span>
                  <strong>${escapeHtml(pulse.value)}</strong>
                  <em>${escapeHtml(pulse.meta)}</em>
                </button>`
            )
            .join("")}
        </div>`;
}
function cockpitCrewHandoffRailModel(lane) {
  const agents = laneAgents(lane).slice(0, 3);
  const suggestion = bestLaneDispatchSuggestion(lane);
  const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id || draft.sourceId === suggestion.id);
  const fallback = agents.length ? agents : [{ agent_id: lane.ownerAgentId ?? "lane-bot", name: lane.ownerAgentId ?? "Lane bot", visual: {} }];
  const handoffs = fallback.map((agent, index) => {
    const isOwner = index === 0;
    return {
      id: agent.agent_id ?? agent.id ?? `agent-${index}`,
      agent,
      callsign: compactText(agent.visual?.callsign ?? agent.callsign ?? agent.name ?? agent.agent_id ?? `Bot ${index + 1}`, 14),
      status: isOwner ? (staged ? "Queued" : "Owner") : compactText(agent.visual?.specialty ?? agent.role_id ?? "Support", 18),
      action: compactText(isOwner ? suggestion.reason ?? suggestion.title ?? suggestion.command : agent.thread_id ?? lane.visual?.realm ?? lane.department, 34),
      tone: isOwner && staged ? "staged" : isOwner ? "ready" : (lane.counts?.blockers ?? 0) ? "gated" : "advancing",
    };
  });

  return {
    lane,
    laneId: lane.id,
    staged,
    tone: staged ? "staged" : (lane.counts?.blockers ?? 0) ? "gated" : "ready",
    queueLabel: staged ? "staged" : suggestion ? "ready" : "idle",
    nextCommand: compactText(suggestion?.title ?? suggestion?.kind ?? chronicleNextAction(lane), 28),
    handoffs: handoffs,
  };
}

function renderCockpitCrewHandoffRail(model) {
  return `
        <section class="cockpit-crew-handoff-rail" data-cockpit-crew-handoff-tone="${escapeHtml(model.tone)}" aria-label="Cockpit crew handoff rail">
          <button class="cockpit-crew-handoff-core ${model.staged ? "staged" : ""}" type="button" data-cockpit-control-action="queue" data-cockpit-control-lane="${escapeHtml(model.laneId)}" title="Stage selected lane handoff">
            <span>Handoff</span>
            <strong>${escapeHtml(model.queueLabel)}</strong>
            <em>${escapeHtml(model.nextCommand)}</em>
          </button>
          ${model.handoffs
            .map(
              (record, index) => `
                <button class="cockpit-crew-handoff-card ${escapeHtml(record.tone)}" type="button" data-detail-view="comms" data-cockpit-crew-handoff="${escapeHtml(record.id)}" style="--crew-handoff-index:${index};" title="${escapeHtml(record.callsign)}: ${escapeHtml(record.action)}">
                  ${agentAvatarMarkup(record.agent, model.lane, "cockpit-crew-handoff-avatar")}
                  <span>
                    <b>${escapeHtml(record.callsign)}</b>
                    <strong>${escapeHtml(record.status)}</strong>
                    <em>${escapeHtml(record.action)}</em>
                  </span>
                </button>`
            )
            .join("")}
        </section>`;
}
function cockpitUnlockChainModel(lane) {
  const checkpoints = lane.quest?.checkpoints ?? [];
  const completedCheckpoints = checkpoints.filter((checkpoint) => checkpoint.status === "complete").length;
  const activeCheckpoint = checkpoints.find((checkpoint) => checkpoint.status !== "complete") ?? checkpoints.at(-1);
  const trail = chronicleTrail(lane);
  const latestOutcome = trail.find((item) => item.kind === "outcome" || item.type === "outcome");
  const outcomeCount = lane.counts?.outcomes ?? 0;
  const proofCount = lane.counts?.evidence ?? 0;
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const questValue = checkpoints.length ? `${formatNumber(completedCheckpoints)}/${formatNumber(checkpoints.length)}` : `${formatNumber(lane.progress ?? 0)}%`;
  const stages = [
    {
      id: "level",
      label: "Level",
      value: `L${formatNumber(lane.level ?? 0)}`,
      meta: `${formatNumber(lane.progress ?? 0)}% XP`,
      tone: "unlocked",
      view: "overview",
    },
    {
      id: "quest",
      label: "Quest",
      value: questValue,
      meta: compactText(activeCheckpoint?.title ?? lane.quest?.title ?? "checkpoint chain", 28),
      tone: checkpoints.length && completedCheckpoints >= checkpoints.length ? "unlocked" : "advancing",
      view: "path",
    },
    {
      id: "gate",
      label: "Gate",
      value: blockerPressure ? formatNumber(blockerPressure) : "clear",
      meta: blockerPressure ? "operator review" : "open lane",
      tone: blockerPressure ? "gated" : "ready",
      view: "trail",
    },
    {
      id: "proof",
      label: "Proof",
      value: proofCount ? formatNumber(proofCount) : "0",
      meta: proofCount ? "evidence" : "needed",
      tone: proofCount ? "unlocked" : "scouting",
      view: "chronicle",
    },
    {
      id: "reward",
      label: "Reward",
      value: outcomeCount ? formatNumber(outcomeCount) : "seed",
      meta: compactText(latestOutcome?.title ?? "next unlock", 28),
      tone: outcomeCount ? "unlocked" : "scouting",
      view: "trail",
    },
  ];

  return {
    laneId: lane.id,
    tone: blockerPressure ? "gated" : outcomeCount ? "unlocked" : "advancing",
    progress: Math.max(8, Math.min(100, lane.progress ?? 0)),
    stages,
  };
}

function renderCockpitUnlockChain(model) {
  return `
        <nav class="cockpit-unlock-chain" data-cockpit-unlock-tone="${escapeHtml(model.tone)}" aria-label="Cockpit unlock chain" style="--cockpit-unlock-progress:${model.progress}%;">
          ${model.stages
            .map(
              (stage, index) => `
                <button class="cockpit-unlock-stage ${escapeHtml(stage.tone)}" type="button" data-detail-view="${escapeHtml(stage.view)}" data-cockpit-unlock-stage="${escapeHtml(stage.id)}" style="--cockpit-unlock-index:${index};" title="${escapeHtml(stage.label)}: ${escapeHtml(stage.meta)}">
                  <span>${escapeHtml(stage.label)}</span>
                  <strong>${escapeHtml(stage.value)}</strong>
                  <em>${escapeHtml(stage.meta)}</em>
                </button>`
            )
            .join("")}
        </nav>`;
}
function commandCockpitRouteMinimap(lane) {
  const suggestion = bestLaneDispatchSuggestion(lane);
  const owner = (state.snapshot?.agents ?? []).find((agent) => agent.lane === lane.id || agent.laneId === lane.id || agent.boundLaneId === lane.id || agent.ownerLaneId === lane.id);
  const gateCount = lane.counts?.blockers ?? 0;
  const taskCount = lane.counts?.tasks ?? 0;
  const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);
  const gameStages = gameStepCount(lane);
  return {
    level: `L${formatNumber(lane.level ?? 0)}`,
    progress: `${formatNumber(lane.progress ?? 0)}%`,
    title: lane.visual?.realm ?? lane.department ?? lane.name,
    nodes: [
      {
        id: "gate",
        label: "Gate",
        value: gateCount ? formatNumber(gateCount) : "clear",
        meta: gateCount ? "blockers" : "open",
        tone: gateCount ? "gated" : "ready",
        view: "trail",
      },
      {
        id: "tasks",
        label: "Tasks",
        value: formatNumber(taskCount),
        meta: taskCount ? "active" : "idle",
        tone: taskCount ? "live" : "open",
        view: "path",
      },
      {
        id: "proof",
        label: "Proof",
        value: formatNumber(proofCount),
        meta: proofCount ? "captured" : "needed",
        tone: proofCount ? "ready" : "open",
        view: "chronicle",
      },
      {
        id: "bot",
        label: "Bot",
        value: owner ? compactText(owner.callsign ?? owner.name ?? owner.id, 10) : "slot",
        meta: owner ? "assigned" : "open",
        tone: owner ? "ready" : "open",
        view: "comms",
      },
      {
        id: "game",
        label: "Game",
        value: gameStages ? formatNumber(gameStages) : "seed",
        meta: lane.visual?.minigame?.title ? compactText(lane.visual.minigame.title, 16) : "minigame",
        tone: gameStages ? "live" : "open",
        view: "game",
      },
      {
        id: "next",
        label: "Next",
        value: suggestion ? "Q" : "scan",
        meta: suggestion ? compactText(suggestion.kind ?? suggestion.command ?? suggestion.title, 18) : compactText(chronicleNextAction(lane), 18),
        tone: suggestion ? "staged" : "live",
        view: suggestion ? "comms" : "overview",
      },
    ],
  };
}

function renderCommandCockpitRouteMinimap(lane) {
  if (!lane) return "";
  const model = commandCockpitRouteMinimap(lane);
  return `
    <nav class="command-route-minimap" aria-label="Selected lane route minimap">
      <div class="command-route-core">
        <span>${escapeHtml(model.level)}</span>
        <strong>${escapeHtml(compactText(model.title, 22))}</strong>
        <em>${escapeHtml(model.progress)} route</em>
      </div>
      ${model.nodes
        .map(
          (node, index) => `
            <button class="command-route-node ${escapeHtml(node.tone)}" type="button" data-detail-view="${escapeHtml(node.view)}" data-command-route-node="${escapeHtml(node.id)}" style="--route-node-index:${index};" title="Open ${escapeHtml(node.label)} lane view">
              <span>${escapeHtml(node.label)}</span>
              <strong>${escapeHtml(node.value)}</strong>
              <em>${escapeHtml(node.meta)}</em>
            </button>`
        )
        .join("")}
    </nav>`;
}
function commandCockpitChannelDock(lane) {
  const agents = state.snapshot?.agents ?? [];
  const owner = agents.find((agent) => agent.lane === lane.id || agent.laneId === lane.id || agent.boundLaneId === lane.id || agent.ownerLaneId === lane.id);
  const suggestion = bestLaneDispatchSuggestion(lane);
  const stagedDrafts = state.stagedDispatches.filter((draft) => draft.laneId === lane.id || draft.sourceId === suggestion?.id);
  const blockers = lane.counts?.blockers ?? 0;
  const pending = lane.counts?.pendingRequests ?? lane.counts?.pending ?? 0;
  const tone = blockers ? "gated" : stagedDrafts.length ? "staged" : suggestion ? "ready" : "watching";
  return {
    owner,
    tone,
    ownerLabel: owner ? compactText(owner.callsign ?? owner.name ?? owner.id, 18) : "Unassigned",
    ownerMeta: owner ? compactText(owner.thread_id ?? owner.role ?? "bot channel", 24) : "open bot slot",
    cells: [
      {
        id: "queued",
        label: "Queued",
        value: stagedDrafts.length ? formatNumber(stagedDrafts.length) : "0",
        meta: stagedDrafts.length ? "local drafts" : "empty",
        tone: stagedDrafts.length ? "staged" : "open",
      },
      {
        id: "blocker",
        label: "Blocker",
        value: blockers ? formatNumber(blockers) : "clear",
        meta: pending ? `${formatNumber(pending)} review` : "no review",
        tone: blockers ? "gated" : "ready",
      },
      {
        id: "next",
        label: "Next Ask",
        value: suggestion ? compactText(stateLabel(suggestion.kind), 12) : "scan",
        meta: suggestion ? compactText(suggestion.reason ?? suggestion.title ?? suggestion.command, 26) : compactText(chronicleNextAction(lane), 26),
        tone: suggestion ? "ready" : "open",
      },
    ],
  };
}

function renderCommandCockpitChannelDock(lane) {
  if (!lane) return "";
  const model = commandCockpitChannelDock(lane);
  return `
    <section class="command-channel-dock" aria-label="Selected lane command channel">
      <div class="command-channel-agent ${escapeHtml(model.tone)}">
        ${model.owner ? agentAvatarMarkup(model.owner, lane, "command-channel-avatar") : avatarMarkup(lane, "command-channel-avatar")}
        <span>
          <b>Owner</b>
          <strong>${escapeHtml(model.ownerLabel)}</strong>
          <em>${escapeHtml(model.ownerMeta)}</em>
        </span>
      </div>
      ${model.cells
        .map(
          (cell, index) => `
            <div class="command-channel-cell ${escapeHtml(cell.tone)}" data-command-channel-cell="${escapeHtml(cell.id)}" style="--channel-cell-index:${index};">
              <b>${escapeHtml(cell.label)}</b>
              <strong>${escapeHtml(cell.value)}</strong>
              <em>${escapeHtml(cell.meta)}</em>
            </div>`
        )
        .join("")}
      <div class="command-channel-actions">
        <button class="tool-button" type="button" data-detail-view="comms" title="Open selected lane Comms deck">COM</button>
        <button class="tool-button" type="button" data-stage-lane-command="${escapeHtml(lane.id)}" title="Stage local command draft">Q</button>
      </div>
    </section>`;
}
function renderDetail() {
  applyAtlasDeck();
  const lane = state.snapshot.lanes.find((item) => item.id === state.selectedLaneId);
  if (!lane) return;
  const stageLens = activeLaneStageLens(lane);
  const holoNodes = activeLaneHoloBoardNodes(lane);
  const stageMotes = activeLaneStageMotes(lane);
  const stageHoloFloor = activeLaneStageHoloFloor(lane);
  const objectiveBeacons = activeLaneObjectiveBeacons(lane);
  const botPartyRecords = activeLaneBotPartyRecords(lane);
  const stageFooterRail = activeLaneStageFooterRail(lane);
  const stageEventRibbon = activeLaneStageEventRibbon(lane);
  const cockpitControlPad = cockpitControlPadModel(lane);
  const cockpitRunwayPulse = cockpitRunwayPulseModel(lane);
  const cockpitCrewHandoffRail = cockpitCrewHandoffRailModel(lane);
  const cockpitUnlockChain = cockpitUnlockChainModel(lane);

  const statRows = [
    ["Level", lane.level],
    ["Score", formatNumber(lane.score)],
    ["Tasks", lane.counts.tasks],
    ["Evidence", lane.counts.evidence],
    ["Gates", lane.counts.blockers],
    ["Traces", lane.counts.traces],
  ];

  el.detailPanel.innerHTML = `
    <div class="detail-content detail-view-${escapeHtml(state.detailView)}">
      ${renderActiveLaneLevelHud(lane)}
      <div class="detail-top">
        <div class="detail-title-row">
          <div class="detail-identity">
            ${avatarMarkup(lane, "detail-avatar")}
            <div>
            <p class="eyebrow">${escapeHtml(lane.visual?.realm ?? lane.department)}</p>
            <h2>${escapeHtml(lane.name)}</h2>
              <p class="detail-copy">${escapeHtml(compactText(lane.visual?.mood || lane.notes || lane.examples.join(", "), 210))}</p>
            </div>
          </div>
          <div class="level-ring" style="--ring:${lane.progress}%"><span>L${lane.level}</span></div>
        </div>
        <span class="badge ${escapeHtml(lane.state)}">${escapeHtml(stateLabel(lane.state))}</span>
        <div class="stat-row">
          ${statRows
            .map(([label, value]) => `<div class="mini-stat"><strong>${escapeHtml(value)}</strong><span>${escapeHtml(label)}</span></div>`)
            .join("")}
        </div>
      </div>

      <div class="detail-tabs" role="tablist" aria-label="Lane detail view">
        ${["overview", "path", "chronicle", "trail", "game", "comms"]
          .map(
            (view) =>
              `<button class="detail-tab ${state.detailView === view ? "active" : ""}" type="button" data-detail-view="${view}">${escapeHtml(stateLabel(view))}</button>`
          )
          .join("")}
      </div>

      <section class="active-lane-mounted-stage" data-active-stage-view="${escapeHtml(state.detailView)}" style="${laneStyle(lane)}" aria-label="${escapeHtml(stateLabel(state.detailView))} mounted lane stage">
        <div class="active-lane-mounted-stage-scan" aria-hidden="true"></div>
        <div class="active-lane-stage-atmosphere" aria-hidden="true">
          <div class="active-lane-stage-depth-rings" style="--stage-depth-progress:${stageHoloFloor.progress}%;">
            <span class="active-lane-stage-depth-ring primary"></span>
            <span class="active-lane-stage-depth-ring secondary"></span>
            <span class="active-lane-stage-depth-ring signal"></span>
          </div>
          <div class="active-lane-stage-holo-floor" style="--floor-progress:${stageHoloFloor.progress}%;">
            <span class="active-lane-stage-holo-runner"></span>
            ${stageHoloFloor.pads
              .map(
                (pad, index) => `
                  <span class="active-lane-stage-holo-pad ${escapeHtml(pad.tone)}" style="--floor-pad-index:${index};">
                    <b>${escapeHtml(pad.value)}</b>
                    <i>${escapeHtml(pad.label)}</i>
                  </span>`
              )
              .join("")}
          </div>
          ${stageMotes
            .map(
              (mote) => `
                <span class="active-lane-stage-mote ${escapeHtml(mote.tone)}" style="--mote-x:${mote.x}%; --mote-y:${mote.y}%; --mote-size:${mote.size}px; --mote-delay:${mote.delay}ms;"></span>`
            )
            .join("")}
        </div>
        <div class="cockpit-command-stack" data-cockpit-command-stack="${escapeHtml(state.detailView)}" aria-label="Cockpit command HUD stack">
          ${renderCockpitControlPad(cockpitControlPad)}
          ${renderCockpitRunwayPulse(cockpitRunwayPulse)}
          ${renderCockpitCrewHandoffRail(cockpitCrewHandoffRail)}
          ${renderCockpitUnlockChain(cockpitUnlockChain)}
        </div>
        ${renderCommandCockpitRouteMinimap(lane)}
        ${renderCommandCockpitChannelDock(lane)}
        <div class="active-lane-stage-lens" data-stage-lens-view="${escapeHtml(state.detailView)}" aria-label="Mounted stage lens">
          <div class="active-lane-stage-lens-copy">
            <span>${escapeHtml(stageLens.label)}</span>
            <strong>${escapeHtml(stageLens.title)}</strong>
            <em>${escapeHtml(stageLens.meta)}</em>
          </div>
          <div class="active-lane-stage-lens-signals">
            ${stageLens.signals
              .map(
                (signal) => `
                  <span class="active-lane-stage-lens-signal ${escapeHtml(signal.tone)}">
                    <b>${escapeHtml(signal.value)}</b>
                    <i>${escapeHtml(signal.label)}</i>
                  </span>`
              )
              .join("")}
          </div>
        </div>
        ${stageEventRibbon}
        <div class="active-lane-holo-board" aria-hidden="true">
          <span class="active-lane-holo-runner"></span>
          ${holoNodes
            .map(
              (node) => `
                <span class="active-lane-holo-node ${escapeHtml(node.tone)}" style="--holo-index:${node.index};">
                  <b>${escapeHtml(node.value)}</b>
                  <i>${escapeHtml(node.label)}</i>
                </span>`
            )
            .join("")}
        </div>
        <div class="active-lane-objective-beacons" aria-label="Active lane objective beacons">
          ${objectiveBeacons
            .map(
              (beacon) => `
                <span class="active-lane-objective-beacon ${escapeHtml(beacon.tone)}">
                  <b>${escapeHtml(beacon.label)}</b>
                  <strong>${escapeHtml(beacon.value)}</strong>
                  <i>${escapeHtml(beacon.body)}</i>
                </span>`
            )
            .join("")}
        </div>
        <div class="active-lane-bot-party-dock" aria-label="Active lane bot party">
          ${botPartyRecords
            .map(
              (record) => `
                <span class="active-lane-bot-party-card ${escapeHtml(record.tone)}">
                  ${agentAvatarMarkup(record.agent, lane, "active-lane-bot-party-avatar")}
                  <b>${escapeHtml(record.callsign)}</b>
                  <strong>${escapeHtml(record.status)}</strong>
                  <i>${escapeHtml(record.action)}</i>
                </span>`
            )
            .join("")}
        </div>
        ${renderDetailBody(lane)}
        ${stageFooterRail}
      </section>
    </div>`;
}

function renderDetailBody(lane) {
  if (state.detailView === "path") return renderPathMapView(lane);
  if (state.detailView === "chronicle") return renderChronicleView(lane);
  if (state.detailView === "trail") return renderTrailView(lane);
  if (state.detailView === "game") return renderGameView(lane);
  if (state.detailView === "comms") return renderCommsView(lane);
  return renderOverviewView(lane);
}

function questCockpitData(lane) {
  const trail = chronicleTrail(lane);
  const phase = chroniclePhase(lane, trail);
  const newest = trail[0];
  const checkpoints = lane.quest?.checkpoints ?? [];
  const activeCheckpoint = checkpoints.find((checkpoint) => checkpoint.status !== "complete") ?? checkpoints.at(-1);
  const gate = lane.gateMap?.[0] ?? lane.serviceRequests?.find((request) => request.status === "needs_review") ?? lane.serviceRequests?.[0];
  const nextAction = chronicleNextAction(lane);
  const checkpointProgress = checkpoints.length
    ? Math.round((checkpoints.filter((checkpoint) => checkpoint.status === "complete").length / checkpoints.length) * 100)
    : lane.progress ?? 0;
  const stageRows = [
    {
      label: "World",
      title: lane.visual?.realm ?? lane.department,
      meta: `${formatNumber(lane.counts?.traces ?? 0)} traces`,
      status: "mapped",
    },
    {
      label: "Level",
      title: `Level ${formatNumber(lane.level)}`,
      meta: `${formatNumber(lane.progress ?? 0)}% lane XP`,
      status: lane.progress >= 100 ? "capped" : "charging",
    },
    {
      label: "Checkpoint",
      title: activeCheckpoint?.title ?? newest?.title ?? phase.label,
      meta: `${formatNumber(checkpointProgress)}% quest`,
      status: activeCheckpoint?.status ?? phase.tone,
    },
  ];
  return { trail, phase, newest, gate, nextAction, checkpointProgress, stageRows };
}

function questMinigameSigil(lane) {
  const minigame = lane.visual?.minigame ?? {};
  const title = minigame.title ?? lane.visual?.realm ?? lane.department ?? "Lane module";
  const id = minigame.id ?? "checkpoint";
  const initials = String(title)
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((word) => word[0])
    .join("")
    .toUpperCase() || "LG";
  const stinger = arcadeStingerType(lane);
  return `
    <div class="quest-minigame-sigil" data-quest-minigame="${escapeHtml(stinger)}" title="${escapeHtml(title)}" aria-label="${escapeHtml(title)} lane module">
      <span class="quest-minigame-orbit" aria-hidden="true"></span>
      <strong>${escapeHtml(initials)}</strong>
      <em>${escapeHtml(compactText(id, 14))}</em>
    </div>`;
}

function questDepthLayers(lane, data, gateTitle) {
  const checkpoints = lane.quest?.checkpoints ?? [];
  const completeCheckpoints = checkpoints.filter((checkpoint) => checkpoint.status === "complete").length;
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  return [
    { label: "latest", value: data.newest?.type ?? "seed", tone: data.newest ? "live" : "seed", summary: data.newest?.title ?? lane.name },
    { label: "levels", value: `${formatNumber(completeCheckpoints)}/${formatNumber(Math.max(checkpoints.length, 1))}`, tone: data.checkpointProgress >= 70 ? "earned" : "live", summary: lane.quest?.title ?? lane.name },
    { label: "gates", value: formatNumber(blockerPressure), tone: blockerPressure ? "gated" : "clear", summary: gateTitle },
    { label: "next", value: data.nextAction ? "queued" : "open", tone: data.nextAction ? "live" : "clear", summary: data.nextAction ?? "No next action queued" },
  ];
}

function renderQuestDepthStack(layers) {
  return `
    <div class="quest-depth-stack" aria-label="Expandable path depth">
      ${layers
        .map(
          (layer, index) => `
            <span class="quest-depth-layer" data-depth-tone="${escapeHtml(layer.tone)}" style="--quest-depth-index:${index};">
              <i>${escapeHtml(layer.label)}</i>
              <strong>${escapeHtml(layer.value)}</strong>
              <em>${escapeHtml(compactText(layer.summary, 34))}</em>
            </span>`
        )
        .join("")}
    </div>`;
}

function renderQuestFocusBeam(cell, index, count) {
  const focusX = count ? ((index + 0.5) / count) * 100 : 50;
  const focusW = count ? 100 / count : 20;
  return `
    <span class="quest-focus-beam" data-quest-focus-beam="${escapeHtml(cell?.role ?? "checkpoint")}" data-quest-focus-tone="${escapeHtml(cell?.tone ?? "live")}" aria-hidden="true" style="--quest-focus-x:${focusX.toFixed(2)}%; --quest-focus-w:${focusW.toFixed(2)}%; --quest-focus-beam-art:url('./assets/system/command-cockpit-focus-beam-20260619.png');"></span>`;
}

function renderQuestSpotlightCameraAperture(cell, index, count) {
  const focusX = count ? ((index + 0.5) / count) * 100 : 50;
  const focusW = count ? 100 / count : 20;
  return `
    <span class="quest-spotlight-camera-aperture" data-quest-aperture-role="${escapeHtml(cell?.role ?? "checkpoint")}" data-quest-aperture-tone="${escapeHtml(cell?.tone ?? "live")}" aria-hidden="true" style="--quest-aperture-x:${focusX.toFixed(2)}%; --quest-aperture-w:${focusW.toFixed(2)}%;"></span>`;
}

function questEventPulseTone(item) {
  const raw = `${item?.kind ?? ""} ${item?.type ?? ""} ${item?.status ?? ""}`.toLowerCase();
  if (/gate|block|request|review|risk/.test(raw)) return "gated";
  if (/outcome|unlock|complete|win|proof/.test(raw)) return "earned";
  if (/task|trace|active|running|progress/.test(raw)) return "live";
  return "seed";
}

function questEventPulsePackets(lane, data, focusedCell) {
  const roleCenters = { world: 11, level: 30, checkpoint: 50, gate: 70, next: 89 };
  const source =
    data.trail.length > 0
      ? data.trail.slice(0, 5)
      : [
          {
            kind: data.gate ? "service_request" : "seed",
            title: data.gate ? data.gate.workerType ?? data.gate.type ?? "Gate review" : data.phase.label,
            status: data.gate ? "needs_review" : "queued",
            time: data.newest?.time,
          },
        ];
  const focusCenter = roleCenters[focusedCell?.role] ?? 50;
  return source.map((item, index) => {
    const spread = source.length > 1 ? index / (source.length - 1) : 0.5;
    const baseX = 11 + spread * 78;
    const laneNudge = ((lane.level ?? 1) * 3 + index * 7) % 9;
    const focusNudge = (focusCenter - 50) * 0.08;
    const x = Math.max(8, Math.min(92, baseX + laneNudge - 4 + focusNudge));
    const y = 50 + ((index % 3) - 1) * 18;
    return {
      index,
      label: stateLabel(item.kind ?? item.type ?? item.status ?? "event"),
      title: compactText(item.title ?? item.summary ?? lane.name, 30),
      meta: item.time ? shortDate(item.time) : stateLabel(item.status ?? data.phase.tone),
      tone: questEventPulseTone(item),
      x,
      y: Math.max(18, Math.min(82, y)),
      delay: index * 170,
    };
  });
}

function renderQuestEventPulse(packets, cell, activeIndex = 0) {
  const activePacket = packets[Math.max(0, Math.min(packets.length - 1, activeIndex))] ?? packets[0];
  return `
    <span class="quest-event-pulse" data-quest-event-pulse-role="${escapeHtml(cell?.role ?? "checkpoint")}" aria-label="${escapeHtml(cell?.label ?? "Quest")} recent event pulse" style="--quest-event-pulse-art:url('./assets/system/command-cockpit-event-pulse-20260619.png');">
      ${
        activePacket
          ? `
            <span class="quest-event-lens" data-event-pulse-tone="${escapeHtml(activePacket.tone)}" style="--event-pulse-x:${activePacket.x.toFixed(2)}%; --event-pulse-y:${activePacket.y.toFixed(2)}%;">
              <i>${escapeHtml(activePacket.label)}</i>
              <strong>${escapeHtml(activePacket.title)}</strong>
              <em>${escapeHtml(activePacket.meta)}</em>
            </span>`
          : ""
      }
      ${renderQuestSignalConvoy(packets)}
      ${packets
        .map(
          (packet, index) => `
            <button class="quest-event-packet" type="button" data-quest-event-focus="${index}" data-event-pulse-tone="${escapeHtml(packet.tone)}" data-event-pulse-active="${index === activeIndex ? "true" : "false"}" title="${escapeHtml(`${packet.label}: ${packet.title}`)}" style="--event-pulse-x:${packet.x.toFixed(2)}%; --event-pulse-y:${packet.y.toFixed(2)}%; --event-pulse-index:${index}; --event-pulse-delay:${packet.delay}ms;">
              <i>${escapeHtml(packet.label)}</i>
              <strong>${escapeHtml(packet.title)}</strong>
              <em>${escapeHtml(packet.meta)}</em>
            </button>`
        )
        .join("")}
    </span>`;
}

function renderQuestSignalConvoy(packets) {
  if (!packets.length) return "";
  return `
    <span class="quest-event-convoy" aria-hidden="true">
      ${packets
        .map(
          (packet, index) => `
            <span class="quest-event-convoy-trail" data-convoy-tone="${escapeHtml(packet.tone)}" style="--event-pulse-x:${packet.x.toFixed(2)}%; --event-pulse-y:${packet.y.toFixed(2)}%; --event-pulse-index:${index}; --event-pulse-delay:${packet.delay}ms;"></span>`
        )
        .join("")}
    </span>`;
}

function questCameraRailSignals(lane, data, focusedCell) {
  const checkpoints = lane.quest?.checkpoints ?? [];
  const completeCheckpoints = checkpoints.filter((checkpoint) => checkpoint.status === "complete").length;
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);
  const crew = questCrewRelayRecord(lane);
  const focusXByRole = { world: 13, level: 31, checkpoint: 50, gate: 69, next: 87 };
  const focusX = focusXByRole[focusedCell?.role] ?? 50;
  const signals = [
    {
      label: "MS",
      value: checkpoints.length ? `${formatNumber(completeCheckpoints)}/${formatNumber(checkpoints.length)}` : `${formatNumber(data.checkpointProgress)}%`,
      tone: data.checkpointProgress >= 70 ? "earned" : "live",
      x: 16,
      y: 36,
    },
    {
      label: "BK",
      value: blockerPressure ? formatNumber(blockerPressure) : "OK",
      tone: blockerPressure ? "gated" : "clear",
      x: 70,
      y: 62,
    },
    {
      label: "PR",
      value: formatNumber(proofCount),
      tone: proofCount ? "earned" : "seed",
      x: 39,
      y: 70,
    },
    {
      label: "BT",
      value: compactText(crew?.callsign ?? `${formatNumber(agentPartyRecords(lane).length)} bot`, 10),
      tone: crew?.tone ?? "seed",
      x: 28,
      y: 24,
    },
    {
      label: "NX",
      value: data.nextAction ? "Q" : "OPN",
      tone: data.nextAction ? "live" : "clear",
      x: 86,
      y: 34,
    },
  ];
  return {
    focusX,
    signals: signals.map((signal, index) => ({
      ...signal,
      x: Math.max(8, Math.min(92, signal.x + ((lane.level ?? 0) % 3) - 1)),
      delay: index * 150,
    })),
  };
}

function renderQuestCameraRail(cameraRail, cell) {
  return `
    <span class="quest-camera-rail" aria-label="${escapeHtml(cell?.label ?? "Quest")} live camera rail" style="--quest-camera-focus-x:${cameraRail.focusX}%;">
      <i class="quest-camera-sweep" aria-hidden="true"></i>
      <i class="quest-camera-orbit" aria-hidden="true"></i>
      ${cameraRail.signals
        .map(
          (signal, index) => `
            <span class="quest-camera-blip" data-camera-tone="${escapeHtml(signal.tone)}" style="--camera-x:${signal.x}%; --camera-y:${signal.y}%; --camera-index:${index}; --camera-delay:${signal.delay}ms;" aria-label="${escapeHtml(signal.label)} ${escapeHtml(signal.value)}">
              <i>${escapeHtml(signal.label)}</i>
              <strong>${escapeHtml(signal.value)}</strong>
            </span>`
        )
        .join("")}
    </span>`;
}

function questRouteCapsules(fieldCells, focusedRole) {
  return fieldCells.map((cell, index) => ({
    role: cell.role,
    label: cell.label,
    glyph: cell.glyph,
    tone: cell.tone,
    current: Boolean(cell.current),
    focused: cell.role === focusedRole || Boolean(cell.focused),
    index,
  }));
}

function renderQuestRouteCapsule(routeCapsules, focusedCell) {
  if (!routeCapsules.length) return "";
  return `
    <span class="quest-route-capsule" aria-label="${escapeHtml(focusedCell?.label ?? "Quest")} unlock route capsule" style="--route-node-count:${routeCapsules.length};">
      <i class="quest-route-capsule-beam" aria-hidden="true"></i>
      ${routeCapsules
        .map(
          (node, index) => `
            <span class="quest-route-capsule-node" data-route-role="${escapeHtml(node.role)}" data-route-tone="${escapeHtml(node.tone)}" data-route-current="${node.current ? "true" : "false"}" data-route-focused="${node.focused ? "true" : "false"}" style="--route-node-index:${index};">
              <i>${escapeHtml(node.glyph)}</i>
              <b>${escapeHtml(node.label)}</b>
            </span>`
        )
        .join("")}
    </span>`;
}

function questLevelReelNodes(lane, data, cells, focusedIndex) {
  const levelCell = cells.find((cell) => cell.role === "level") ?? cells[1] ?? cells[0];
  const checkpointCell = cells.find((cell) => cell.role === "checkpoint") ?? cells[focusedIndex] ?? cells[0];
  const gateCell = cells.find((cell) => cell.role === "gate") ?? cells[cells.length - 2] ?? cells[0];
  const nextCell = cells.find((cell) => cell.role === "next") ?? cells[cells.length - 1] ?? cells[0];
  const worldCell = cells.find((cell) => cell.role === "world") ?? cells[0];
  return [
    { ...worldCell, label: "World", value: compactText(lane.visual?.realm ?? lane.department ?? lane.name, 18) },
    { ...levelCell, label: "Level", value: `L${formatNumber(lane.level ?? 0)}` },
    { ...checkpointCell, label: "Quest", value: `${formatNumber(data.checkpointProgress)}%` },
    { ...gateCell, label: "Gate", value: gateCell?.current ? "LOCK" : "OPEN" },
    { ...nextCell, label: "Next", value: compactText(data.nextAction ?? "Queued", 18) },
  ].filter(Boolean);
}

function renderQuestLevelReel(lane, data, cells, focusedIndex) {
  const reelNodes = questLevelReelNodes(lane, data, cells, focusedIndex);
  if (!reelNodes.length) return "";
  return `
    <nav class="quest-level-reel" data-level-reel-focus="${escapeHtml(reelNodes[1]?.role ?? "checkpoint")}" aria-label="World, Level, Checkpoint, Gate, and Next unlock reel" style="--level-reel-progress:${data.checkpointProgress}%; --level-reel-count:${reelNodes.length};">
      <span class="quest-level-reel-progress" aria-hidden="true"></span>
      ${reelNodes
        .map(
          (node, index) => `
            <button class="quest-level-reel-node ${escapeHtml(node.tone)}" type="button" data-quest-focus-node="${escapeHtml(node.role)}" data-level-reel-current="${node.current ? "true" : "false"}" data-level-reel-focused="${node.focused ? "true" : "false"}" aria-pressed="${node.focused ? "true" : "false"}" title="Focus ${escapeHtml(node.label)}" style="--level-reel-index:${index};">
              <i>${escapeHtml(node.glyph ?? node.label.slice(0, 2).toUpperCase())}</i>
              <span>
                <em>${escapeHtml(node.label)}</em>
                <strong>${escapeHtml(compactText(node.value ?? node.title, 20))}</strong>
              </span>
            </button>`
        )
        .join("")}
    </nav>`;
}

function renderQuestUnlockTrail(lane, data, reelNodes, focusedIndex) {
  if (!reelNodes?.length) return "";
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const unlockProgress = Math.max(6, Math.min(100, data.checkpointProgress));
  return `
    <span class="quest-unlock-trail" data-unlock-trail-gate="${blockerPressure ? "locked" : "open"}" aria-label="${escapeHtml(lane.name)} level progress unlock trail" style="--unlock-trail-progress:${data.checkpointProgress}%; --unlock-trail-count:${reelNodes.length}; --unlock-trail-focus:${focusedIndex};">
      <i class="quest-unlock-trail-beam" aria-hidden="true"></i>
      ${reelNodes
        .map(
          (node, index) => `
            <b class="quest-unlock-trail-node ${escapeHtml(node.tone)}" data-unlock-trail-node="${escapeHtml(node.role)}" data-unlock-trail-current="${node.current ? "true" : "false"}" data-unlock-trail-focused="${node.focused ? "true" : "false"}" style="--unlock-trail-index:${index}; --unlock-trail-node-progress:${Math.max(8, Math.min(100, unlockProgress - index * 9))}%;">
              <i>${escapeHtml(node.glyph ?? node.label.slice(0, 2).toUpperCase())}</i>
              <span>${escapeHtml(compactText(node.label, 12))}</span>
            </b>`
        )
        .join("")}
    </span>`;
}

function renderQuestUnlockPulse(lane, data, focusedCell) {
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);
  const orbs = [
    { label: "Proof", value: formatNumber(proofCount), tone: proofCount ? "earned" : "seed" },
    { label: "Gate", value: blockerPressure ? formatNumber(blockerPressure) : "open", tone: blockerPressure ? "gated" : "clear" },
    { label: "Next", value: data.nextAction ? "queued" : "open", tone: data.phase.tone },
  ];
  return `
    <span class="quest-unlock-pulse" data-unlock-pulse-focus="${escapeHtml(focusedCell?.role ?? "checkpoint")}" data-unlock-pulse-gate="${blockerPressure ? "locked" : "open"}" aria-label="Quest unlock pulse feedback" style="--unlock-pulse-progress:${data.checkpointProgress}%; --unlock-pulse-pressure:${Math.min(1, blockerPressure / 6).toFixed(2)}; --unlock-pulse-proof:${Math.min(1, proofCount / 24).toFixed(2)};">
      <i class="quest-unlock-pulse-ring" aria-hidden="true"></i>
      ${orbs
        .map(
          (orb, index) => `
            <b class="quest-unlock-pulse-orb" data-unlock-orb-tone="${escapeHtml(orb.tone)}" style="--unlock-orb-index:${index};">
              <span>${escapeHtml(orb.label)}</span>
              <strong>${escapeHtml(orb.value)}</strong>
            </b>`
        )
        .join("")}
    </span>`;
}

function renderQuestBoardAtmosphere(lane, data, focusedCell) {
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);
  const sparks = [
    { label: "gate", tone: blockerPressure ? "gated" : "clear", x: 18, y: 34 },
    { label: "proof", tone: proofCount ? "earned" : "seed", x: 42, y: 68 },
    { label: "quest", tone: data.phase.tone, x: 64, y: 28 },
    { label: "next", tone: data.nextAction ? "live" : "clear", x: 84, y: 56 },
  ];
  return `
    <span class="quest-board-atmosphere" data-board-atmosphere-tone="${escapeHtml(focusedCell?.tone ?? data.phase.tone)}" data-board-atmosphere-focus="${escapeHtml(focusedCell?.role ?? "checkpoint")}" style="--board-atmosphere-progress:${data.checkpointProgress}%; --board-atmosphere-pressure:${Math.min(1, blockerPressure / 6).toFixed(2)}; --board-atmosphere-proof:${Math.min(1, proofCount / 18).toFixed(2)}; --board-atmosphere-art:url('./assets/system/command-cockpit-event-pulse-20260619.png');" aria-hidden="true">
      <i class="quest-board-atmosphere-grid"></i>
      <i class="quest-board-atmosphere-sheen"></i>
      ${sparks
        .map(
          (spark, index) => `
            <b class="quest-board-atmosphere-spark" data-atmosphere-spark="${escapeHtml(spark.label)}" data-atmosphere-spark-tone="${escapeHtml(spark.tone)}" style="--atmosphere-spark-x:${spark.x}%; --atmosphere-spark-y:${spark.y}%; --atmosphere-spark-index:${index};"></b>`
        )
        .join("")}
    </span>`;
}

function questLaneConstellationLanes(activeLane) {
  const lanes = orderedLaneRailLanes(state.snapshot?.lanes ?? []);
  const activeFirst = lanes.some((item) => item.id === activeLane?.id) ? lanes : activeLane ? [activeLane, ...lanes] : lanes;
  return activeFirst.slice(0, 5);
}

function renderQuestLaneConstellation(activeLane) {
  const lanes = questLaneConstellationLanes(activeLane);
  if (!lanes.length || !activeLane) return "";
  const total = state.snapshot?.lanes?.length ?? lanes.length;
  const overflow = Math.max(0, total - lanes.length);
  return `
    <span class="quest-lane-constellation" aria-label="Active lane and neighboring money paths" style="--lane-constellation-count:${lanes.length};">
      ${lanes
        .map(
          (item, index) => `
            <button class="quest-lane-constellation-chip ${item.id === activeLane.id ? "active" : "neighbor"} ${escapeHtml(item.state)}" type="button" data-lane-id="${escapeHtml(item.id)}" data-constellation-role="${item.id === activeLane.id ? "active" : "neighbor"}" aria-pressed="${item.id === activeLane.id ? "true" : "false"}" title="Focus ${escapeHtml(item.name)}" style="${laneStyle(item)} --lane-constellation-index:${index}; --lane-constellation-progress:${boundedProgress(item.progress ?? 0)}%;">
              ${avatarMarkup(item, "quest-lane-constellation-avatar")}
              <span>
                <strong>L${escapeHtml(item.level)}</strong>
                <em>${escapeHtml(compactText(item.visual?.realm ?? item.department ?? item.name, 14))}</em>
              </span>
            </button>`
        )
        .join("")}
      ${overflow ? `<span class="quest-lane-constellation-more" aria-label="${formatNumber(overflow)} more money paths">+${formatNumber(overflow)}</span>` : ""}
    </span>`;
}

function questCrewRelayRecord(lane) {
  const records = agentPartyRecords(lane);
  const record =
    records.find((item) => item.agent.agent_id === lane.ownerAgentId || /owner|lead|operator/i.test(item.agent.role_id ?? "")) ??
    records[0];
  if (!record) return null;
  const readiness = crewReadiness(record);
  const callsign = record.visual?.callsign ?? record.agent.agent_id;
  const specialty = record.visual?.specialty ?? record.agent.role_id ?? "operator";
  const tone = record.staged ? "staged" : record.blockers || record.pending ? "gated" : readiness >= 72 ? "ready" : "live";
  return {
    ...record,
    callsign,
    specialty,
    readiness,
    tone,
  };
}

function renderQuestBoardBotBadge(crew, lane, focusedCell) {
  if (!crew || !lane) return "";
  const readiness = crewReadiness(crew);
  const tone = crew.tone ?? (readiness >= 72 ? "ready" : crew.blockers || crew.pending ? "gated" : "live");
  const callsign = crew.callsign ?? crew.visual?.callsign ?? crew.agent.agent_id;
  const specialty = crew.specialty ?? crew.visual?.specialty ?? crew.agent.role_id ?? "operator";
  return `
    <button class="quest-board-bot-badge ${escapeHtml(tone)}" type="button" data-board-bot-tone="${escapeHtml(tone)}" data-board-bot-focus="${escapeHtml(focusedCell?.role ?? "checkpoint")}" data-detail-view="comms" title="Open ${escapeHtml(callsign)} Comms" aria-label="Open lane owner ${escapeHtml(callsign)} Comms" style="--board-bot-readiness:${Math.max(8, Math.min(100, readiness))}%;">
      ${agentAvatarMarkup(crew.agent, lane, "quest-board-bot-avatar")}
      <span class="quest-board-bot-copy">
        <em>${formatNumber(readiness)}% owner</em>
        <strong>${escapeHtml(compactText(callsign, 18))}</strong>
        <b>${escapeHtml(compactText(specialty, 24))}</b>
      </span>
      <span class="quest-board-bot-link" aria-hidden="true">COM</span>
    </button>`;
}
function renderQuestCrewRelay(record, lane) {
  const avatar = record ? agentAvatarMarkup(record.agent, lane, "quest-crew-relay-avatar") : avatarMarkup(lane, "quest-crew-relay-avatar");
  const callsign = record?.callsign ?? "unassigned";
  const specialty = record?.specialty ?? "bot socket";
  const readiness = record?.readiness ?? lane.progress ?? 0;
  const tone = record?.tone ?? "seed";
  return `
    <span class="quest-crew-relay ${escapeHtml(tone)}" data-quest-crew-tone="${escapeHtml(tone)}" aria-label="${escapeHtml(callsign)} crew relay" style="--quest-crew-art:url('./assets/system/command-cockpit-crew-relay-20260619.png');">
      ${avatar}
      <span>
        <i>${formatNumber(readiness)}% crew</i>
        <strong>${escapeHtml(compactText(callsign, 18))}</strong>
        <em>${escapeHtml(compactText(specialty, 24))}</em>
      </span>
      <button class="quest-crew-relay-action" type="button" data-detail-view="comms" title="Open selected lane Comms">COM</button>
    </span>`;
}

function renderQuestCrewPresenceDock(lane) {
  const records = agentPartyRecords(lane).sort((a, b) => crewReadiness(b) - crewReadiness(a) || b.pressure - a.pressure);
  const owner =
    records.find((record) => record.agent.agent_id === lane.ownerAgentId || /owner|lead|operator/i.test(record.agent.role_id ?? "")) ??
    records[0];
  const visibleRecords = records.slice(0, 3);
  const readiness = records.length
    ? Math.round(records.reduce((sum, record) => sum + crewReadiness(record), 0) / records.length)
    : lane.progress ?? 0;
  const blockers = records.reduce((sum, record) => sum + (record.blockers ?? 0) + (record.pending ?? 0), 0);
  const staged = records.filter((record) => record.staged).length;
  const tone = blockers ? "gated" : staged ? "staged" : readiness >= 74 ? "ready" : "live";
  const callsign = owner?.visual?.callsign ?? owner?.agent.agent_id ?? lane.ownerAgentId ?? "Crew socket";
  const specialty = owner?.visual?.specialty ?? owner?.agent.role_id ?? "lane bots";
  return `
    <button class="quest-crew-presence-dock ${escapeHtml(tone)}" type="button" data-quest-crew-presence="${escapeHtml(lane.id)}" data-quest-overlay-density="ambient-crew" data-detail-view="comms" title="Open ${escapeHtml(lane.name)} crew Comms" aria-label="Open ${escapeHtml(lane.name)} crew Comms">
      <span class="quest-crew-presence-stack" aria-hidden="true">
        ${
          visibleRecords.length
            ? visibleRecords
                .map(
                  (record, index) => `
                    <span class="quest-crew-presence-agent ${escapeHtml(crewMode(record))}" style="--crew-presence-index:${index}; --crew-presence-ready:${crewReadiness(record)}%;">
                      ${agentAvatarMarkup(record.agent, lane, "quest-crew-presence-avatar")}
                    </span>`
                )
                .join("")
            : `<span class="quest-crew-presence-agent seed" style="--crew-presence-index:0; --crew-presence-ready:${Math.max(8, readiness)}%;">${avatarMarkup(lane, "quest-crew-presence-avatar")}</span>`
        }
      </span>
      <span class="quest-crew-presence-copy">
        <i>${formatNumber(records.length)} bot${records.length === 1 ? "" : "s"} - ${formatNumber(readiness)}%</i>
        <strong>${escapeHtml(compactText(callsign, 20))}</strong>
        <em>${escapeHtml(compactText(blockers ? `${formatNumber(blockers)} gate asks` : specialty, 28))}</em>
      </span>
    </button>`;
}

function questCommandSocket(lane) {
  const suggestion = bestLaneDispatchSuggestion(lane);
  const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id || draft.sourceId === suggestion.id);
  const typeLabel = stateLabel(suggestion.kind).replace(/\b(review|check)\b/gi, "").trim() || stateLabel(suggestion.kind);
  return {
    suggestion,
    staged,
    value: staged ? "staged" : compactText(typeLabel, 12),
    meta: staged ? `${formatNumber(state.stagedDispatches.filter((draft) => draft.laneId === lane.id).length || 1)} queued` : compactText(suggestion.reason ?? suggestion.title, 32),
    tone: staged ? "unlocked" : dispatchTone(suggestion.kind),
  };
}

function renderQuestRelayBraid(lane, crew, commandSocket) {
  const stagedCount = state.stagedDispatches.filter((draft) => draft.laneId === lane.id).length;
  const historyCount = state.dispatchHistory.filter((item) => item.laneName === lane.name).length;
  const target = crew?.callsign ?? lane.ownerAgentId ?? "Open bot";
  const thread = crew?.agent?.thread_id ?? lane.ownerThreadId ?? "local relay";
  const copyLabel = state.copiedCommandFor === lane.id ? "OK" : state.copiedCommandFor === `manual:${lane.id}` ? "SEL" : "C";
  const relayMeta = stagedCount
    ? `${formatNumber(stagedCount)} queued`
    : historyCount
      ? `${formatNumber(historyCount)} local logs`
      : compactText(commandSocket.suggestion.reason ?? commandSocket.suggestion.title, 28);
  const tone = commandSocket.staged ? "staged" : (lane.counts?.blockers ?? 0) || (lane.counts?.pendingRequests ?? 0) ? "gated" : "live";
  return `
    <div class="quest-relay-braid ${escapeHtml(tone)}" aria-label="Local bot relay for ${escapeHtml(lane.name)}">
      <span class="quest-relay-pulse" aria-hidden="true"><b></b><i></i></span>
      <span class="quest-relay-copy">
        <i>Relay</i>
        <strong>${escapeHtml(compactText(target, 24))}</strong>
        <em>${escapeHtml(compactText(`${relayMeta} - ${thread}`, 46))}</em>
      </span>
      <span class="quest-relay-actions">
        <button type="button" data-detail-view="comms" title="Open Comms">COM</button>
        <button type="button" data-stage-lane-command="${escapeHtml(lane.id)}" title="Stage local command">${commandSocket.staged ? "OK" : "Q"}</button>
        <button type="button" data-copy-command="${escapeHtml(lane.id)}" title="Copy local command draft">${escapeHtml(copyLabel)}</button>
      </span>
    </div>`;
}

function renderQuestUnlockLadder(lane, data) {
  const checkpoints = lane.quest?.checkpoints ?? [];
  const visibleCheckpoints = checkpoints.slice(0, 5);
  const completed = checkpoints.filter((checkpoint) => checkpoint.status === "complete").length;
  const activeIndex = checkpoints.findIndex((checkpoint) => checkpoint.status !== "complete");
  const activeCheckpoint = checkpoints[activeIndex >= 0 ? activeIndex : checkpoints.length - 1];
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const unlocks = lane.counts?.outcomes ?? 0;
  const progress = checkpoints.length ? Math.round((completed / checkpoints.length) * 100) : data.checkpointProgress;
  const tone = blockerPressure ? "gated" : progress >= 100 || unlocks ? "earned" : "live";
  const fallbackNodes = [
    { title: "World", status: "complete" },
    { title: "Level", status: "complete" },
    { title: "Next", status: data.nextAction ? "active" : "ready" },
  ];
  const nodes = visibleCheckpoints.length ? visibleCheckpoints : fallbackNodes;
  const currentTitle = activeCheckpoint?.title ?? data.nextAction ?? lane.quest?.title ?? "Next unlock";
  return `
    <button class="quest-unlock-ladder ${escapeHtml(tone)}" type="button" data-quest-unlock-ladder="${escapeHtml(lane.id)}" data-quest-overlay-density="ambient-unlock" data-detail-view="path" style="--quest-unlock-progress:${Math.max(8, Math.min(100, progress))}%;" title="Open checkpoint path">
      <span class="quest-unlock-ladder-copy">
        <i>${formatNumber(completed)}/${formatNumber(Math.max(checkpoints.length, 1))} clear</i>
        <strong>${escapeHtml(compactText(currentTitle, 28))}</strong>
      </span>
      <span class="quest-unlock-ladder-pips" aria-hidden="true">
        ${nodes
          .map(
            (checkpoint, index) => `
              <b data-unlock-state="${escapeHtml(checkpoint.status ?? "active")}" data-unlock-current="${index === activeIndex ? "true" : "false"}" style="--unlock-pip-index:${index};">
                <i>${formatNumber(index + 1)}</i>
              </b>`
          )
          .join("")}
      </span>
      <em>${formatNumber(unlocks)} win${unlocks === 1 ? "" : "s"}</em>
    </button>`;
}

function renderQuestMissionDirector(lane, data, gateTitle, gateBody) {
  const crew = questCrewRelayRecord(lane);
  const commandSocket = questCommandSocket(lane);
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);
  const outcomeCount = lane.counts?.outcomes ?? 0;
  const tone = blockerPressure ? "gated" : data.checkpointProgress >= 80 || outcomeCount ? "unlocked" : "advancing";
  const owner = crew?.callsign ?? lane.ownerAgentId ?? "Open seat";
  const ownerMeta = crew ? `${formatNumber(crew.readiness)}% ${crew.specialty}` : "assign bot";
  const reward = outcomeCount ? `${formatNumber(outcomeCount)} wins` : proofCount ? `${formatNumber(proofCount)} proofs` : `L${formatNumber(lane.level ?? 0)} route`;
  const gateLabel = blockerPressure ? `${formatNumber(blockerPressure)} ask${blockerPressure === 1 ? "" : "s"}` : "clear";
  const chips = [
    { label: "Owner", value: owner, meta: ownerMeta, tone: crew?.tone ?? "seed", view: "comms" },
    { label: "Queue", value: commandSocket.value, meta: commandSocket.meta, tone: commandSocket.tone, queue: true },
    { label: "Gate", value: gateLabel, meta: blockerPressure ? gateTitle : "open path", tone: blockerPressure ? "gated" : "clear", view: "path" },
    { label: "Reward", value: reward, meta: `${formatNumber(data.checkpointProgress)}% quest`, tone: outcomeCount ? "unlocked" : proofCount ? "advancing" : "scouting", view: "trail" },
  ];
  return `
    <section class="quest-mission-director ${escapeHtml(tone)}" data-quest-director-tone="${escapeHtml(tone)}" aria-label="Mission Director">
      <div class="quest-director-current">
        <p class="eyebrow">Mission Director</p>
        <h3>${escapeHtml(compactText(data.nextAction, 104))}</h3>
        <p>${escapeHtml(compactText(blockerPressure ? gateBody : data.phase.summary, 138))}</p>
        <span class="quest-director-progress" aria-hidden="true" style="--director-progress:${Math.max(0, Math.min(100, data.checkpointProgress))}%"><i></i></span>
        ${renderQuestRelayBraid(lane, crew, commandSocket)}
      </div>
      <div class="quest-director-chips" aria-label="Mission owner, gate, and reward">
        ${chips
          .map(
            (chip) => `
              <button class="quest-director-chip ${escapeHtml(chip.tone)} ${chip.queue ? "queue" : ""}" type="button" data-quest-director-action="${escapeHtml(chip.label.toLowerCase())}" ${chip.queue ? `data-stage-lane-command="${escapeHtml(lane.id)}"` : `data-detail-view="${escapeHtml(chip.view)}"`} title="${chip.queue ? "Stage lane command" : `Open ${escapeHtml(chip.label)}`}">
                <i>${escapeHtml(chip.label)}</i>
                <strong>${escapeHtml(compactText(chip.value, 24))}</strong>
                <em>${escapeHtml(compactText(chip.meta, 32))}</em>
              </button>`
          )
          .join("")}
      </div>
    </section>`;
}

function questFocusedRole(lane, fieldCells) {
  const requested = state.questNodeFocusByLane[lane.id];
  if (fieldCells.some((cell) => cell.role === requested)) return requested;
  return fieldCells.find((cell) => cell.current)?.role ?? fieldCells[0]?.role ?? "world";
}

function questFocusPackets(lane, data, cell) {
  const checkpoints = lane.quest?.checkpoints ?? [];
  const completeCheckpoints = checkpoints.filter((checkpoint) => checkpoint.status === "complete").length;
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const packetSets = {
    world: [
      { label: "realm", value: compactText(lane.visual?.realm ?? lane.department, 10), tone: "live" },
      { label: "traces", value: formatNumber(lane.counts?.traces ?? 0), tone: "live" },
      { label: "crew", value: formatNumber(lane.agentTypes?.length ?? 0), tone: "clear" },
    ],
    level: [
      { label: "level", value: `L${formatNumber(lane.level ?? 0)}`, tone: "earned" },
      { label: "xp", value: `${formatNumber(lane.progress ?? 0)}%`, tone: "live" },
      { label: "score", value: formatNumber(lane.score ?? 0), tone: (lane.score ?? 0) >= 70 ? "earned" : "live" },
    ],
    checkpoint: [
      { label: "quest", value: `${formatNumber(data.checkpointProgress)}%`, tone: data.checkpointProgress >= 70 ? "earned" : "live" },
      { label: "nodes", value: `${formatNumber(completeCheckpoints)}/${formatNumber(Math.max(checkpoints.length, 1))}`, tone: "live" },
      { label: "events", value: formatNumber(data.trail.length), tone: data.trail.length ? "live" : "seed" },
    ],
    gate: [
      { label: "gates", value: formatNumber(blockerPressure), tone: blockerPressure ? "gated" : "clear" },
      { label: "ask", value: formatNumber(lane.counts?.pendingRequests ?? 0), tone: (lane.counts?.pendingRequests ?? 0) ? "gated" : "clear" },
      { label: "state", value: data.gate ? "review" : "clear", tone: data.gate ? "gated" : "clear" },
    ],
    next: [
      { label: "move", value: data.nextAction ? "queued" : "open", tone: data.nextAction ? "live" : "clear" },
      { label: "phase", value: compactText(data.phase.label, 10), tone: data.phase.tone },
      { label: "trail", value: formatNumber(data.trail.length), tone: data.trail.length ? "live" : "seed" },
    ],
  };
  return packetSets[cell?.role] ?? [
    { label: "node", value: cell?.label ?? "open", tone: cell?.tone ?? "live" },
    { label: "lane", value: `L${formatNumber(lane.level ?? 0)}`, tone: "earned" },
    { label: "events", value: formatNumber(data.trail.length), tone: "live" },
  ];
}

function questNodeEchoes(lane, data, cell, gateTitle, gateBody) {
  const latestTrail = data.trail[0]?.title ?? data.newest?.title ?? lane.name;
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const checkpointCount = lane.quest?.checkpoints?.length ?? 0;
  const echoSets = {
    world: [
      { label: "realm", value: lane.visual?.realm ?? lane.department, tone: "live" },
      { label: "agents", value: `${formatNumber(lane.agentTypes?.length ?? 0)} crew`, tone: "clear" },
      { label: "assets", value: `${formatNumber(lane.counts?.artifacts ?? 0)} files`, tone: "earned" },
      { label: "latest", value: latestTrail, tone: "live" },
    ],
    level: [
      { label: "level", value: `Level ${formatNumber(lane.level ?? 0)}`, tone: "earned" },
      { label: "xp", value: `${formatNumber(lane.progress ?? 0)}% charged`, tone: "live" },
      { label: "score", value: `${formatNumber(lane.score ?? 0)} score`, tone: (lane.score ?? 0) >= 70 ? "earned" : "live" },
      { label: "proof", value: `${formatNumber(lane.counts?.evidence ?? 0)} proof`, tone: "clear" },
    ],
    checkpoint: [
      { label: "quest", value: `${formatNumber(data.checkpointProgress)}% mapped`, tone: data.checkpointProgress >= 70 ? "earned" : "live" },
      { label: "nodes", value: `${formatNumber(checkpointCount)} checkpoints`, tone: "live" },
      { label: "trail", value: `${formatNumber(data.trail.length)} events`, tone: data.trail.length ? "live" : "seed" },
      { label: "latest", value: latestTrail, tone: "live" },
    ],
    gate: [
      { label: "gate", value: gateTitle, tone: data.gate ? "gated" : "clear" },
      { label: "pressure", value: `${formatNumber(blockerPressure)} locks`, tone: blockerPressure ? "gated" : "clear" },
      { label: "request", value: `${formatNumber(lane.counts?.pendingRequests ?? 0)} asks`, tone: (lane.counts?.pendingRequests ?? 0) ? "gated" : "clear" },
      { label: "brief", value: gateBody, tone: data.gate ? "gated" : "clear" },
    ],
    next: [
      { label: "move", value: data.nextAction ?? "Open exploration", tone: data.nextAction ? "live" : "clear" },
      { label: "phase", value: data.phase.label, tone: data.phase.tone },
      { label: "handoff", value: `${formatNumber(data.trail.length)} trail events`, tone: data.trail.length ? "live" : "seed" },
      { label: "reward", value: `${formatNumber(lane.counts?.outcomes ?? 0)} unlocks`, tone: (lane.counts?.outcomes ?? 0) ? "earned" : "seed" },
    ],
  };
  return (echoSets[cell?.role] ?? echoSets.checkpoint).map((echo) => ({
    ...echo,
    value: compactText(echo.value, 34),
  }));
}

function questInsightRibbonSignals(lane, data, cell, gateTitle, gateBody) {
  const laneAgents = (state.snapshot?.agents ?? []).filter((agent) => agent.lane?.id === lane.id);
  const owner = laneAgents.find((agent) => /owner|lead|operator/i.test(agent.role_id ?? "")) ?? laneAgents[0];
  const latestTitle = data.trail[0]?.title ?? data.newest?.title ?? lane.quest?.title ?? lane.name;
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);
  const nodeLabel = cell?.label ?? "Node";
  return [
    { label: "node", glyph: nodeLabel.slice(0, 2).toUpperCase(), value: nodeLabel, detail: cell?.title ?? lane.name, tone: cell?.tone ?? "live" },
    { label: "milestone", glyph: "MS", value: compactText(latestTitle, 28), detail: `${formatNumber(data.trail.length)} trail events`, tone: data.trail.length ? "live" : "seed" },
    { label: "blocker", glyph: blockerPressure ? "BK" : "OK", value: blockerPressure ? compactText(gateTitle, 24) : "clear", detail: compactText(gateBody, 38), tone: blockerPressure ? "gated" : "clear" },
    { label: "bot", glyph: "BT", value: compactText(owner?.visual?.callsign ?? owner?.agent_id ?? "unassigned", 18), detail: owner?.visual?.specialty ?? "bot socket", tone: owner ? "live" : "seed" },
    { label: "proof", glyph: "PR", value: `${formatNumber(proofCount)} proof`, detail: `${formatNumber(lane.counts?.artifacts ?? 0)} assets`, tone: proofCount ? "earned" : "seed" },
    { label: "next", glyph: "GO", value: data.nextAction ? "queued" : "open", detail: data.nextAction ?? "No next action queued", tone: data.nextAction ? "live" : "clear" },
  ];
}

function renderQuestInsightRibbon(signals, cell) {
  return `
    <div class="quest-insight-ribbon" data-quest-insight-role="${escapeHtml(cell?.role ?? "checkpoint")}" aria-label="${escapeHtml(cell?.label ?? "Quest")} node insight ribbon" style="--quest-insight-art:url('./assets/system/command-cockpit-insight-ribbon-20260619.png');">
      ${signals
        .map(
          (signal, index) => `
            <span class="quest-insight-chip" data-insight-tone="${escapeHtml(signal.tone)}" style="--quest-insight-index:${index};">
              <i>${escapeHtml(signal.glyph)}</i>
              <strong>${escapeHtml(signal.value)}</strong>
              <em>${escapeHtml(compactText(signal.detail, 34))}</em>
            </span>`
        )
        .join("")}
    </div>`;
}

function renderQuestNodeEchoRail(echoes, cell) {
  return `
    <div class="quest-node-echo-rail" data-quest-echo-role="${escapeHtml(cell?.role ?? "checkpoint")}" aria-label="${escapeHtml(cell?.label ?? "Quest")} node recent signals">
      ${echoes
        .map(
          (echo, index) => `
            <span class="quest-node-echo" data-echo-tone="${escapeHtml(echo.tone)}" style="--quest-echo-index:${index};">
              <i>${escapeHtml(echo.label)}</i>
              <strong>${escapeHtml(echo.value)}</strong>
            </span>`
        )
        .join("")}
    </div>`;
}

function renderQuestRunSpine(lane, data, gateTitle, gateBody) {
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);
  const latestTrail = data.trail[0]?.title ?? data.newest?.title ?? "No trail yet";
  const nodes = [
    {
      label: "Proof",
      value: proofCount ? `${formatNumber(proofCount)} proofs` : compactText(latestTrail, 26),
      meta: `${formatNumber(data.trail.length)} trail events`,
      view: "trail",
      tone: proofCount ? "earned" : data.trail.length ? "live" : "seed",
    },
    {
      label: "Gate",
      value: blockerPressure ? `${formatNumber(blockerPressure)} asks` : "clear",
      meta: blockerPressure ? gateTitle : "open path",
      view: "path",
      tone: blockerPressure ? "gated" : "clear",
    },
    {
      label: "Next",
      value: data.nextAction ? "queued" : "open",
      meta: data.nextAction ?? gateBody,
      view: "path",
      tone: data.nextAction ? data.phase.tone : "clear",
    },
  ];
  return `
    <div class="quest-run-spine" aria-label="Run proof, gate, and next move">
      ${nodes
        .map(
          (node, index) => `
            <button class="quest-run-spine-node ${escapeHtml(node.tone)}" type="button" data-quest-run-spine="${escapeHtml(node.label.toLowerCase())}" data-detail-view="${escapeHtml(node.view)}" style="--quest-run-index:${index};" title="Open ${escapeHtml(node.label)}">
              <i>${escapeHtml(node.label)}</i>
              <strong>${escapeHtml(compactText(node.value, 20))}</strong>
              <em>${escapeHtml(compactText(node.meta, 34))}</em>
            </button>`
        )
        .join("")}
    </div>`;
}

function questNodeDrillCards(lane, data, cell, gateTitle, gateBody) {
  const checkpoints = lane.quest?.checkpoints ?? [];
  const completeCheckpoints = checkpoints.filter((checkpoint) => checkpoint.status === "complete").length;
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);
  const latestTrail = data.trail[0]?.title ?? data.newest?.title ?? lane.name;
  const currentMilestone = checkpoints.find((checkpoint) => checkpoint.status !== "complete") ?? checkpoints.at(-1);
  const role = cell?.role ?? "checkpoint";
  const roleLead = {
    world: lane.visual?.realm ?? lane.department ?? lane.name,
    level: `Level ${formatNumber(lane.level ?? 0)} - ${formatNumber(lane.progress ?? 0)}% XP`,
    checkpoint: currentMilestone?.title ?? cell?.title ?? lane.quest?.title ?? lane.name,
    gate: blockerPressure ? gateTitle : "No active gate",
    next: data.nextAction ?? "Open exploration",
  }[role];
  return [
    {
      label: "Focus",
      value: roleLead,
      meta: `${cell?.label ?? "Node"} selected`,
      tone: cell?.tone ?? "live",
      glyph: (cell?.glyph ?? "ACT").slice(0, 3),
    },
    {
      label: "Milestone",
      value: checkpoints.length ? `${formatNumber(completeCheckpoints)}/${formatNumber(checkpoints.length)} clear` : `${formatNumber(data.checkpointProgress)}% quest`,
      meta: currentMilestone?.title ?? latestTrail,
      tone: data.checkpointProgress >= 70 ? "earned" : "live",
      glyph: "MS",
    },
    {
      label: "Blocker",
      value: blockerPressure ? `${formatNumber(blockerPressure)} asks` : "clear",
      meta: blockerPressure ? gateBody : "No gate blocking this node",
      tone: blockerPressure ? "gated" : "clear",
      glyph: blockerPressure ? "BK" : "OK",
    },
    {
      label: "Trail",
      value: `${formatNumber(data.trail.length)} events`,
      meta: latestTrail,
      tone: data.trail.length ? "live" : "seed",
      glyph: "TR",
    },
    {
      label: "Next",
      value: data.nextAction ? "queued" : "open",
      meta: data.nextAction ?? "Waiting for a new lane move",
      tone: data.nextAction ? data.phase.tone : "clear",
      glyph: "GO",
    },
    {
      label: "Proof",
      value: `${formatNumber(proofCount)} proof`,
      meta: `${formatNumber(lane.counts?.artifacts ?? 0)} assets`,
      tone: proofCount ? "earned" : "seed",
      glyph: "PR",
    },
  ];
}

function questNodeDrillPriority(card) {
  const criticalLabels = new Set(["Focus", "Blocker", "Next"]);
  if (card.label === "Focus") return "primary";
  return criticalLabels.has(card.label) ? "signal" : "archive";
}

function questCinematicHeartbeatPackets(lane, data, cell) {
  return questEventPulsePackets(lane, data, cell)
    .slice(0, 3)
    .map((packet, index) => ({
      index,
      label: packet.label,
      title: packet.title,
      tone: packet.tone,
      delay: packet.delay + index * 120,
    }));
}

function questSelectedNodeExpansionRows(lane, data, cell, cards) {
  const byLabel = new Map(cards.map((card) => [card.label, card]));
  const blocker = byLabel.get("Blocker");
  const proof = byLabel.get("Proof");
  const next = byLabel.get("Next");
  const latest = data.trail[0];
  const roleLabel = cell?.label ?? "Quest";
  return [
    {
      label: "Timeline",
      value: `${formatNumber(data.trail.length)} events`,
      meta: latest?.title ?? data.newest?.title ?? `${roleLabel} waiting for first event`,
      tone: data.trail.length ? "live" : "seed",
      glyph: "TL",
      view: "trail",
    },
    {
      label: "Blocker",
      value: blocker?.value ?? "clear",
      meta: blocker?.meta ?? "No gate blocking this node",
      tone: blocker?.tone ?? "clear",
      glyph: "BK",
      view: "path",
    },
    {
      label: "Proof",
      value: proof?.value ?? "0 proof",
      meta: proof?.meta ?? `${formatNumber(lane.counts?.artifacts ?? 0)} assets`,
      tone: proof?.tone ?? "seed",
      glyph: "PR",
      view: "trail",
    },
    {
      label: "Next",
      value: next?.value ?? (data.nextAction ? "queued" : "open"),
      meta: next?.meta ?? data.nextAction ?? "Waiting for a new lane move",
      tone: next?.tone ?? (data.nextAction ? data.phase.tone : "clear"),
      glyph: "GO",
      view: "comms",
    },
  ];
}

function questCinematicActionSockets() {
  const sockets = [
    { view: "path", label: "Path", icon: "map", title: "Open Path Map" },
    { view: "trail", label: "Trail", icon: "trail", title: "Open Trail" },
    { view: "game", label: "Game", icon: "game", title: "Open Game module" },
    { view: "comms", label: "Comms", icon: "comms", title: "Open Comms deck" },
  ];
  return `
    <span class="quest-cinematic-action-sockets" aria-label="Selected node quick view sockets">
      ${sockets
        .map(
          (socket, index) => `
            <button class="quest-cinematic-action-socket quest-action-button" type="button" data-detail-view="${escapeHtml(socket.view)}" data-action-icon="${escapeHtml(socket.icon)}" title="${escapeHtml(socket.title)}" aria-label="${escapeHtml(socket.title)}" style="--socket-index:${index};">
              <span class="quest-action-icon" aria-hidden="true"><i></i></span>
              <span>${escapeHtml(socket.label)}</span>
            </button>`
        )
        .join("")}
    </span>`;
}

function questCinematicFocusPlateModel(lane, data, cell, cards, focusIndex, focusCount, crew) {
  const byLabel = new Map(cards.map((card) => [card.label, card]));
  const focus = byLabel.get("Focus") ?? cards[0];
  const blocker = byLabel.get("Blocker");
  const next = byLabel.get("Next");
  const proof = byLabel.get("Proof");
  const milestone = byLabel.get("Milestone");
  return {
    role: cell?.role ?? "checkpoint",
    tone: cell?.tone ?? focus?.tone ?? data.phase.tone,
    glyph: (cell?.glyph ?? focus?.glyph ?? "RUN").slice(0, 3),
    kicker: "Node Lock",
    title: focus?.value ?? cell?.title ?? lane.name,
    subtitle: cell?.title ?? data.phase.summary ?? lane.name,
    blocker: blocker?.value ?? "clear",
    blockerMeta: blocker?.meta ?? "No gate blocking this node",
    next: next?.meta ?? data.nextAction ?? "Waiting for the next lane move",
    rewardProof: proof?.value ?? "0 proof",
    rewardMilestone: milestone?.value ?? `${formatNumber(data.checkpointProgress)}% quest`,
    eventHeartbeat: questCinematicHeartbeatPackets(lane, data, cell),
    focusIndex: Math.max(0, focusIndex),
    focusCount: Math.max(1, focusCount),
    botAvatar: crew ? agentAvatarMarkup(crew.agent, lane, "quest-cinematic-bot-avatar") : avatarMarkup(lane, "quest-cinematic-bot-avatar"),
    botLensAvatar: crew ? agentAvatarMarkup(crew.agent, lane, "quest-selected-node-lens-bot-avatar") : avatarMarkup(lane, "quest-selected-node-lens-bot-avatar"),
    botCallsign: crew?.callsign ?? lane.ownerAgentId ?? "Unassigned",
    botStatus: crew ? `${formatNumber(crew.readiness)}% ready` : "open seat",
    botSpecialty: crew?.specialty ?? lane.visual?.realm ?? "bot socket",
    botTone: crew?.tone ?? "seed",
    expansionRows: questSelectedNodeExpansionRows(lane, data, cell, cards),
  };
}

function renderQuestCinematicFocusPlate(model) {
  return `
    <div class="quest-cinematic-focus-plate ${escapeHtml(model.tone)}" data-quest-cinematic-role="${escapeHtml(model.role)}" aria-label="${escapeHtml(model.title)} cinematic focus" style="--quest-cinematic-lock-index:${model.focusIndex}; --quest-cinematic-lock-count:${model.focusCount};">
      <i class="quest-cinematic-focus-rune" aria-hidden="true">${escapeHtml(model.glyph)}</i>
      <span class="quest-cinematic-focus-copy">
        <em>${escapeHtml(model.kicker)}</em>
        <strong>${escapeHtml(compactText(model.title, 46))}</strong>
        <b>${escapeHtml(compactText(model.subtitle, 64))}</b>
        <span class="quest-cinematic-reward-rail" aria-label="Selected node proof and unlock progress">
          <span><em>Proof</em><strong>${escapeHtml(compactText(model.rewardProof, 16))}</strong></span>
          <span><em>Unlock</em><strong>${escapeHtml(compactText(model.rewardMilestone, 18))}</strong></span>
        </span>
      </span>
      <button class="quest-cinematic-bot-relay ${escapeHtml(model.botTone)}" type="button" data-detail-view="comms" title="Open ${escapeHtml(model.botCallsign)} Comms" aria-label="Open ${escapeHtml(model.botCallsign)} Comms">
        ${model.botAvatar}
        <span>
          <em>${escapeHtml(compactText(model.botStatus, 16))}</em>
          <strong>${escapeHtml(compactText(model.botCallsign, 18))}</strong>
          <b>${escapeHtml(compactText(model.botSpecialty, 22))}</b>
        </span>
        <i aria-hidden="true">COM</i>
      </button>
      <span class="quest-cinematic-focus-stats" aria-label="Selected node blocker and next move">
        <span><em>Blocker</em><strong>${escapeHtml(compactText(model.blocker, 18))}</strong></span>
        <span><em>Next</em><strong>${escapeHtml(compactText(model.next, 30))}</strong></span>
      </span>
      <span class="quest-cinematic-event-heartbeat" aria-label="Selected node recent activity heartbeat">
        <i aria-hidden="true">Live</i>
        ${model.eventHeartbeat
          .map(
            (packet, index) => `
              <span data-heartbeat-tone="${escapeHtml(packet.tone)}" style="--heartbeat-index:${index}; --heartbeat-delay:${packet.delay}ms;">
                <em>${escapeHtml(compactText(packet.label, 12))}</em>
                <strong>${escapeHtml(compactText(packet.title, 20))}</strong>
              </span>`
          )
          .join("")}
      </span>
      ${questCinematicActionSockets()}
    </div>`;
}

function renderQuestSelectedNodeExpansionConsole(model) {
  const rows = model.expansionRows ?? [];
  return `
    <div class="quest-selected-node-expansion-console ${escapeHtml(model.tone)}" data-quest-expansion-role="${escapeHtml(model.role)}" aria-label="${escapeHtml(model.title)} selected node expansion console">
      <span class="quest-selected-node-expansion-head">
        <em>Expanded Node</em>
        <strong>${escapeHtml(compactText(model.title, 34))}</strong>
      </span>
      ${rows
        .map(
          (row, index) => `
            <button class="quest-selected-node-expansion-row" type="button" data-expansion-tone="${escapeHtml(row.tone)}" data-expansion-active="${row.label.toLowerCase() === model.activeLens ? "true" : "false"}" data-detail-view="${escapeHtml(row.view)}" data-quest-expansion-lens="${escapeHtml(row.label.toLowerCase())}" data-quest-expansion-action="${escapeHtml(row.label.toLowerCase())}" title="Open ${escapeHtml(row.label)}" aria-label="Open ${escapeHtml(row.label)} for ${escapeHtml(model.title)}" style="--quest-expansion-index:${index};">
              <i>${escapeHtml(row.glyph)}</i>
              <span>
                <em>${escapeHtml(row.label)}</em>
                <strong>${escapeHtml(compactText(row.value, 20))}</strong>
                <b>${escapeHtml(compactText(row.meta, 42))}</b>
              </span>
            </button>`
        )
        .join("")}
    </div>`;
}

function renderQuestMissionStack(model) {
  const rows = model.expansionRows ?? [];
  const activeLens = model.activeLens ?? "timeline";
  const missionStackRows = rows.slice(0, 4);
  if (!missionStackRows.length) return "";
  return `
    <nav class="quest-mission-stack ${escapeHtml(model.tone)}" data-mission-stack-role="${escapeHtml(model.role)}" aria-label="${escapeHtml(model.title)} Timeline, Blocker, Proof, and Next mission stack">
      <span class="quest-mission-stack-trace" aria-hidden="true"></span>
      ${missionStackRows
        .map(
          (row, index) => `
            <button class="quest-mission-stack-stage" type="button" data-mission-stage-tone="${escapeHtml(row.tone)}" data-mission-stage-active="${row.label.toLowerCase() === activeLens ? "true" : "false"}" data-mission-stack-view="${escapeHtml(row.view)}" data-quest-expansion-lens="${escapeHtml(row.label.toLowerCase())}" data-quest-expansion-action="${escapeHtml(row.label.toLowerCase())}" title="Focus ${escapeHtml(row.label)} node context" aria-label="Focus ${escapeHtml(row.label)} for ${escapeHtml(model.title)}" style="--mission-stack-index:${index};">
              <i>${escapeHtml(row.glyph)}</i>
              <span>
                <em>${escapeHtml(row.label)}</em>
                <strong>${escapeHtml(compactText(row.value, 18))}</strong>
              </span>
              <b class="quest-mission-stack-link" aria-hidden="true">${escapeHtml(row.view.toUpperCase().slice(0, 3))}</b>
            </button>`
        )
        .join("")}
    </nav>`;
}

function renderQuestMissionDossier(model) {
  const rows = model.lensRows ?? model.expansionRows ?? [];
  const activeLens = model.activeLens ?? "timeline";
  const activeRow = rows.find((row) => row.label.toLowerCase() === activeLens) ?? rows[0];
  const depthCards = (model.lensDepthCards ?? []).slice(0, 3);
  if (!activeRow) return "";
  return `
    <section class="quest-mission-dossier ${escapeHtml(model.tone)}" data-mission-dossier-lens="${escapeHtml(activeRow.label.toLowerCase())}" data-mission-dossier-role="${escapeHtml(model.role)}" aria-label="${escapeHtml(activeRow.label)} mission dossier">
      <span class="quest-mission-dossier-head">
        <i>${escapeHtml(activeRow.glyph)}</i>
        <span>
          <em>${escapeHtml(activeRow.label)} Lens</em>
          <strong>${escapeHtml(compactText(activeRow.value, 28))}</strong>
          <b>${escapeHtml(compactText(activeRow.meta, 66))}</b>
        </span>
      </span>
      <span class="quest-mission-dossier-cards" aria-label="${escapeHtml(activeRow.label)} compact dossier cards">
        ${depthCards
          .map(
            (card, index) => `
              <span class="quest-mission-dossier-card" data-dossier-card-tone="${escapeHtml(card.tone)}" data-dossier-card-kind="${escapeHtml(card.kind)}" style="--mission-dossier-index:${index};">
                <em>${escapeHtml(card.label)}</em>
                <strong>${escapeHtml(compactText(card.value, 22))}</strong>
              </span>`
          )
          .join("")}
      </span>
    </section>`;
}

function questSelectedNodeLensDepthCards(lane, data, activeLens, gateTitle, gateBody) {
  const latest = data.trail[0];
  const second = data.trail[1];
  const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);
  const blockerCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const cardsByLens = {
    timeline: [
      { kind: "latest", tone: latest ? "live" : "seed", label: "Latest", value: latest?.title ?? "No event yet", meta: latest ? shortDate(latest.time) : "Waiting for trail" },
      { kind: "prior", tone: second ? "live" : "seed", label: "Before", value: second?.title ?? data.phase.label, meta: second ? shortDate(second.time) : data.phase.summary },
      { kind: "count", tone: data.trail.length ? "earned" : "seed", label: "Depth", value: `${formatNumber(data.trail.length)} events`, meta: "Open Trail for full run memory" },
    ],
    blocker: [
      { kind: "gate", tone: blockerCount ? "gated" : "clear", label: "Gate", value: gateTitle, meta: compactText(gateBody, 86) },
      { kind: "asks", tone: blockerCount ? "gated" : "clear", label: "Asks", value: `${formatNumber(blockerCount)} open`, meta: lane.serviceRequests?.[0]?.requestedAction ?? "No pending service request" },
      { kind: "route", tone: "live", label: "Route", value: "Path Map", meta: "Use Open when this node needs route context" },
    ],
    proof: [
      { kind: "proof", tone: proofCount ? "earned" : "seed", label: "Proof", value: `${formatNumber(proofCount)} signals`, meta: latest?.artifactPreview?.title ?? latest?.title ?? "No proof artifact attached" },
      { kind: "assets", tone: (lane.counts?.artifacts ?? 0) ? "earned" : "seed", label: "Assets", value: `${formatNumber(lane.counts?.artifacts ?? 0)} files`, meta: "Proof cards and generated textures stay reusable" },
      { kind: "wins", tone: (lane.counts?.outcomes ?? 0) ? "earned" : "seed", label: "Wins", value: `${formatNumber(lane.counts?.outcomes ?? 0)} outcomes`, meta: "Unlocked outcomes feed the trophy room" },
    ],
    next: [
      { kind: "move", tone: data.nextAction ? data.phase.tone : "seed", label: "Move", value: data.nextAction ?? "No next move", meta: data.phase.summary },
      { kind: "bot", tone: lane.ownerAgentId ? "live" : "seed", label: "Bot", value: lane.ownerAgentId ?? "Open seat", meta: lane.ownerThreadId ?? "Assign a lane operator" },
      { kind: "queue", tone: "live", label: "Queue", value: "Comms", meta: "Open the handoff console when ready" },
    ],
  };
  return cardsByLens[activeLens] ?? cardsByLens.timeline;
}

function renderQuestSelectedNodeLensReactor(activeRow, depthCards) {
  const pipCards = depthCards.length ? depthCards : [activeRow];
  return `
      <span class="quest-selected-node-lens-reactor" data-lens-reactor="${escapeHtml(activeRow.label.toLowerCase())}" aria-hidden="true">
        <i class="quest-selected-node-lens-core"></i>
        <span class="quest-selected-node-lens-rail"></span>
        ${pipCards
          .map(
            (card, index) => `
              <b class="quest-selected-node-lens-pip" data-lens-pip-tone="${escapeHtml(card.tone)}" style="--lens-pip-index:${index}; --lens-pip-count:${pipCards.length};"></b>`
          )
          .join("")}
      </span>`;
}

function renderQuestSelectedNodeLensTray(model) {
  const rows = model.lensRows ?? model.expansionRows ?? [];
  const activeLens = model.activeLens ?? "timeline";
  const activeRow = rows.find((row) => row.label.toLowerCase() === activeLens) ?? rows[0];
  const depthCards = model.lensDepthCards ?? [];
  if (!activeRow) return "";
  return `
    <section class="quest-selected-node-lens-tray ${escapeHtml(model.tone)}" data-quest-active-lens="${escapeHtml(activeRow.label.toLowerCase())}" data-expansion-tone="${escapeHtml(activeRow.tone)}" data-quest-lens-bot-ready="true" aria-label="${escapeHtml(activeRow.label)} node lens">
      ${renderQuestSelectedNodeLensReactor(activeRow, depthCards)}
      <span class="quest-selected-node-lens-copy">
        <em>${escapeHtml(activeRow.label)} Lens</em>
        <strong>${escapeHtml(compactText(activeRow.value, 28))}</strong>
        <b>${escapeHtml(compactText(activeRow.meta, 76))}</b>
      </span>
      <button class="quest-selected-node-lens-bot ${escapeHtml(model.botTone ?? "seed")}" type="button" data-detail-view="comms" data-quest-lens-bot="${escapeHtml(model.botCallsign)}" title="Open ${escapeHtml(model.botCallsign)} Comms" aria-label="Open ${escapeHtml(model.botCallsign)} Comms">
        ${model.botLensAvatar ?? ""}
        <span>
          <em>${escapeHtml(compactText(model.botStatus ?? "open seat", 14))}</em>
          <strong>${escapeHtml(compactText(model.botCallsign ?? "Unassigned", 16))}</strong>
        </span>
        <i aria-hidden="true">COM</i>
      </button>
      <button class="quest-selected-node-lens-jump" type="button" data-detail-view="${escapeHtml(activeRow.view)}" title="Open full ${escapeHtml(activeRow.label)} view" aria-label="Open full ${escapeHtml(activeRow.label)} view">
        Open
      </button>
      <span class="quest-selected-node-lens-depth" aria-label="${escapeHtml(activeRow.label)} local depth cards">
        ${depthCards
          .map(
            (card, index) => `
              <span class="quest-selected-node-lens-card" data-lens-card-tone="${escapeHtml(card.tone)}" data-lens-card-kind="${escapeHtml(card.kind)}" style="--lens-card-index:${index};">
                <em>${escapeHtml(card.label)}</em>
                <strong>${escapeHtml(compactText(card.value, 24))}</strong>
                <b>${escapeHtml(compactText(card.meta, 46))}</b>
              </span>`
          )
          .join("")}
      </span>
    </section>`;
}

function renderQuestNodeDrillStack(cards, cell) {
  return `
    <div class="quest-node-drill-stack" data-quest-drill-role="${escapeHtml(cell?.role ?? "checkpoint")}" aria-label="${escapeHtml(cell?.label ?? "Quest")} selected node drill stack">
      ${cards
        .map(
          (card, index) => `
            <span class="quest-node-drill-card" data-drill-tone="${escapeHtml(card.tone)}" data-drill-priority="${escapeHtml(questNodeDrillPriority(card))}" style="--quest-drill-index:${index};">
              <i>${escapeHtml(card.glyph)}</i>
              <span>
                <em>${escapeHtml(card.label)}</em>
                <strong>${escapeHtml(compactText(card.value, 28))}</strong>
                <b>${escapeHtml(compactText(card.meta, 44))}</b>
              </span>
            </span>`
        )
        .join("")}
    </div>`;
}

function renderQuestRealmSkinCartridge(lane, data) {
  const minigame = lane.visual?.minigame ?? {};
  const title = minigame.title ?? lane.visual?.realm ?? lane.name;
  const realm = lane.visual?.realm ?? lane.department ?? "Custom realm";
  const custom = Boolean(minigameDefinition(lane));
  const gatePressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const unlocks = lane.counts?.outcomes ?? 0;
  const motion = arcadeStingerType(lane);
  const art = minigame.texture ?? lane.visual?.avatar;
  const artStyle = art ? `--realm-skin-art:url('${escapeHtml(art)}');` : "";
  return `
    <button class="quest-realm-skin-cartridge ${custom ? "custom" : "template"} ${gatePressure ? "gated" : "ready"}" type="button" data-quest-realm-skin="${escapeHtml(minigame.id ?? lane.id)}" data-quest-overlay-density="ambient-realm" data-detail-view="game" style="${artStyle} --realm-skin-charge:${Math.max(8, Math.min(100, data.checkpointProgress))}%;" title="Open ${escapeHtml(title)} minigame">
      <span class="quest-realm-skin-thumb" aria-hidden="true"></span>
      <span class="quest-realm-skin-copy">
        <i>${escapeHtml(custom ? "Custom Realm" : "Realm Skin")}</i>
        <strong>${escapeHtml(compactText(title, 28))}</strong>
        <em>${escapeHtml(compactText(`${realm} - ${motion}`, 34))}</em>
      </span>
      <b aria-label="${formatNumber(gatePressure)} gates and ${formatNumber(unlocks)} unlocks">${gatePressure ? `G${formatNumber(gatePressure)}` : `W${formatNumber(unlocks)}`}</b>
    </button>`;
}

function questRealmMoodModel(lane, data) {
  const minigame = lane.visual?.minigame ?? {};
  const definition = minigameDefinition(lane);
  const realm = lane.visual?.realm ?? lane.department ?? "Custom realm";
  const title = minigame.title ?? realm;
  const mood = arcadeStingerType(lane);
  const gatePressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const unlocks = lane.counts?.outcomes ?? 0;
  const custom = Boolean(definition);
  const charge = boundedProgress((data.checkpointProgress ?? lane.progress ?? 0) * 0.62 + Math.min(unlocks, 8) * 6 - Math.min(gatePressure, 6) * 5 + (custom ? 14 : 4));
  return {
    realm,
    title,
    mood,
    custom,
    gatePressure,
    unlocks,
    charge: Math.round(charge),
    texture: minigame.texture ?? lane.visual?.avatar ?? "",
    chips: [
      { label: "Realm", value: realm, tone: custom ? "custom" : "template" },
      { label: "Mood", value: mood, tone: gatePressure ? "gated" : "live" },
      { label: "Game", value: custom ? "wired" : "seed", tone: custom ? "ready" : "seed" },
      { label: gatePressure ? "Gate" : "Wins", value: gatePressure ? `G${formatNumber(gatePressure)}` : `W${formatNumber(unlocks)}`, tone: gatePressure ? "gated" : "earned" },
    ],
  };
}

function renderQuestRealmMoodLayer(model) {
  const artStyle = model.texture ? ` --realm-mood-art:url('${escapeHtml(model.texture)}');` : "";
  return `
    <span class="quest-realm-mood-layer" data-realm-mood="${escapeHtml(model.mood)}" data-realm-custom="${model.custom ? "true" : "false"}" aria-label="${escapeHtml(model.title)} realm mood layer" style="--realm-mood-charge:${model.charge}%;${artStyle}">
      <i class="quest-realm-mood-orbit" aria-hidden="true"></i>
      <strong>${escapeHtml(compactText(model.title, 28))}</strong>
      <em>${escapeHtml(compactText(model.realm, 30))}</em>
      <span class="quest-realm-mood-chips" aria-hidden="true">
        ${model.chips
          .map(
            (chip) => `
              <b class="quest-realm-mood-chip" data-realm-mood-chip="${escapeHtml(chip.tone)}">
                <i>${escapeHtml(chip.label)}</i>
                <span>${escapeHtml(compactText(chip.value, 14))}</span>
              </b>`
          )
          .join("")}
      </span>
    </span>`;
}

function renderQuestFocusLens(cell, lane, data) {
  if (!cell) return "";
  const packets = questFocusPackets(lane, data, cell);
  const crew = questCrewRelayRecord(lane);
  return `
    <div class="quest-focus-lens ${escapeHtml(cell.tone)}" data-quest-focus-tone="${escapeHtml(cell.tone)}" aria-live="polite">
      <span class="quest-focus-rune" aria-hidden="true">${escapeHtml(cell.glyph)}</span>
      <span class="quest-focus-copy">
        <i>${escapeHtml(cell.label)} node</i>
        <strong>${escapeHtml(compactText(cell.title, 62))}</strong>
      </span>
      ${renderQuestCrewRelay(crew, lane)}
      <span class="quest-focus-packets" aria-label="${escapeHtml(cell.label)} node signals">
        ${packets
          .map(
            (packet) => `
              <b class="quest-focus-packet" data-packet-tone="${escapeHtml(packet.tone)}">
                <i>${escapeHtml(packet.label)}</i>
                <strong>${escapeHtml(packet.value)}</strong>
              </b>`
          )
          .join("")}
      </span>
      <em>${escapeHtml(compactText(cell.meta, 72))}</em>
    </div>`;
}

function renderQuestActionDock() {
  const actions = [
    { view: "path", label: "Path", icon: "map", title: "Open Path Map", priority: "plate" },
    { view: "chronicle", label: "Log", icon: "log", title: "Open Chronicle", priority: "archive" },
    { view: "game", label: "Game", icon: "game", title: "Open Game module", priority: "plate" },
    { view: "comms", label: "Comms", icon: "comms", title: "Open Comms deck", priority: "plate" },
    { view: "trail", label: "Trail", icon: "trail", title: "Open full trail", priority: "plate" },
  ];
  return `
        <div class="quest-action-row" data-quest-dock-density="secondary" aria-label="Quest view controls">
          ${actions
            .map(
              (action) => `
                <button class="tool-button quest-action-button" type="button" data-detail-view="${escapeHtml(action.view)}" data-action-icon="${escapeHtml(action.icon)}" data-quest-action-priority="${escapeHtml(action.priority)}" title="${escapeHtml(action.title)}" aria-label="${escapeHtml(action.title)}">
                  <span class="quest-action-icon" aria-hidden="true"><i></i></span>
                  <span>${escapeHtml(action.label)}</span>
                </button>`
            )
            .join("")}
        </div>`;
}

function renderQuestBoardSignalOverlay(signals) {
  return `
    <span class="quest-board-signal-overlay" aria-label="Quest board score and pressure overlay">
      ${signals
        .map(
          (signal, index) => `
            <span class="quest-board-signal-chip ${escapeHtml(signal.tone)}" data-quest-board-signal-state="${escapeHtml(signal.state)}" style="--board-signal-index:${index};">
              <i aria-hidden="true">${escapeHtml(signal.glyph)}</i>
              <strong>${escapeHtml(signal.value)}</strong>
              <em>${escapeHtml(signal.label)}</em>
            </span>`
        )
        .join("")}
    </span>`;
}

function renderQuestBoardIdentityCartridge(lane, data, minigameSigil) {
  return `
    <span class="quest-board-identity-cartridge" aria-label="Quest board lane identity cartridge">
      <span class="quest-board-identity-avatar" aria-hidden="true">
        ${avatarMarkup(lane, "quest-avatar")}
      </span>
      <span class="quest-board-identity-copy">
        <em>Latest</em>
        <strong>${escapeHtml(compactText(data.newest?.title ?? lane.name, 38))}</strong>
        <b>${escapeHtml(compactText(data.newest?.summary ?? data.phase.summary, 52))}</b>
      </span>
      <span class="quest-board-identity-game" aria-hidden="true">${minigameSigil}</span>
      <span class="quest-board-identity-meter" aria-label="${formatNumber(data.checkpointProgress)} percent quest progress">
        <strong>${formatNumber(data.checkpointProgress)}%</strong>
        <em>quest</em>
      </span>
    </span>`;
}

function renderQuestMissionReadout(lane, data, focusedCell, gateTitle) {
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const nextMove = data.nextAction ?? "Awaiting next lane move";
  return `
    <span class="quest-mission-readout" data-quest-readout-tone="${escapeHtml(focusedCell?.tone ?? data.phase.tone)}" aria-label="${escapeHtml(lane.name)} mission readout">
      <span class="quest-mission-readout-cell" data-readout-cell="quest">
        <i>Quest</i>
        <strong>${formatNumber(data.checkpointProgress)}%</strong>
        <em>${escapeHtml(compactText(focusedCell?.label ?? data.phase.label, 18))}</em>
      </span>
      <span class="quest-mission-readout-core">
        <i>${escapeHtml(compactText(focusedCell?.label ?? "Focus", 18))}</i>
        <strong>${escapeHtml(compactText(nextMove, 58))}</strong>
        <em>${escapeHtml(compactText(data.newest?.title ?? data.phase.summary, 52))}</em>
      </span>
      <span class="quest-mission-readout-cell" data-readout-cell="gate">
        <i>${blockerPressure ? "Gate" : "Open"}</i>
        <strong>${blockerPressure ? `G${formatNumber(blockerPressure)}` : "Clear"}</strong>
        <em>${escapeHtml(compactText(gateTitle, 20))}</em>
      </span>
    </span>`;
}

function questMissionControlBandModel(lane, data, focusedCell, gateTitle, gateBody, crew) {
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const botCallsign = crew?.callsign ?? lane.ownerAgentId ?? "open bot";
  const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0) + (lane.counts?.artifacts ?? 0);
  const nextMove = data.nextAction ?? "Waiting for next move";
  const latestTitle = data.newest?.title ?? data.phase.label ?? lane.name;
  const gateValue = blockerPressure ? `${formatNumber(blockerPressure)} gated` : "clear";
  const cells = [
    {
      id: "latest",
      label: "Latest",
      value: latestTitle,
      meta: data.newest?.summary ?? data.phase.summary,
      tone: data.newest ? "live" : "seed",
      glyph: "LOG",
      view: "trail",
    },
    {
      id: "blocker",
      label: blockerPressure ? "Blocker" : "Open",
      value: gateValue,
      meta: blockerPressure ? gateBody : gateTitle,
      tone: blockerPressure ? "gated" : "clear",
      glyph: blockerPressure ? "GAT" : "OK",
      view: blockerPressure ? "trail" : "path",
    },
    {
      id: "next",
      label: "Next",
      value: nextMove,
      meta: focusedCell?.title ?? data.phase.summary,
      tone: focusedCell?.tone ?? data.phase.tone,
      glyph: "GO",
      view: "path",
    },
    {
      id: "bot",
      label: "Bot",
      value: botCallsign,
      meta: crew ? `${formatNumber(crew.readiness)}% ready` : "socket open",
      tone: crew?.tone ?? "seed",
      glyph: "COM",
      view: "comms",
    },
  ];

  return {
    lane,
    progress: data.checkpointProgress,
    tone: blockerPressure ? "gated" : data.phase.tone,
    level: lane.level ?? 1,
    score: lane.score ?? 0,
    proofCount,
    phase: data.phase.label,
    cells,
  };
}

function renderQuestMissionControlBand(model) {
  return `
    <span class="quest-mission-control-band" data-mission-control-tone="${escapeHtml(model.tone)}" aria-label="${escapeHtml(model.lane.name)} mission control" style="--mission-control-progress:${model.progress}%;">
      <span class="quest-mission-control-level" aria-label="Level ${formatNumber(model.level)} and ${formatNumber(model.progress)} percent quest progress">
        <i>LV ${formatNumber(model.level)}</i>
        <strong>${formatNumber(model.progress)}%</strong>
        <em>${formatNumber(model.proofCount)} proof</em>
      </span>
      ${model.cells
        .map(
          (cell, index) => `
            <button class="quest-mission-control-cell ${escapeHtml(cell.tone)}" type="button" data-mission-control-cell="${escapeHtml(cell.id)}" data-detail-view="${escapeHtml(cell.view)}" title="${escapeHtml(cell.label)}: ${escapeHtml(cell.value)}" style="--mission-control-index:${index};">
              <i>${escapeHtml(cell.glyph)}</i>
              <span>
                <em>${escapeHtml(cell.label)}</em>
                <strong>${escapeHtml(compactText(cell.value, 34))}</strong>
                <b>${escapeHtml(compactText(cell.meta, 40))}</b>
              </span>
            </button>`
        )
        .join("")}
    </span>`;
}
function questPathDepthLensModel(lane, data, focusedCell, gateTitle, gateBody) {
  const latest = data.trail[0] ?? data.newest;
  const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const cells = [
    ["happened", "Happened", latest?.title ?? "No event yet", latest?.summary ?? data.phase.summary, latest ? "live" : "seed"],
    ["blocker", "Blocker", blockerPressure ? `${formatNumber(blockerPressure)} active` : "Clear", blockerPressure ? gateBody : "No active blocker recorded", blockerPressure ? "gated" : "clear"],
    ["proof", "Proof", `${formatNumber(proofCount)} signals`, `${formatNumber(lane.counts?.artifacts ?? 0)} reusable assets`, proofCount ? "earned" : "seed"],
    ["next", "Next", data.nextAction ? "Queued" : "Open", data.nextAction ?? "Waiting for a fresh lane move", data.nextAction ? data.phase.tone : "clear"],
  ];
  return {
    focus: focusedCell?.role ?? "checkpoint",
    tone: focusedCell?.tone ?? data.phase.tone,
    gate: gateTitle,
    cells: cells.map(([id, label, value, meta, tone]) => ({ id, label, value, meta, tone })),
  };
}

function renderQuestPathDepthLens(model) {
  return `
    <span class="quest-path-depth-lens" data-path-depth-tone="${escapeHtml(model.tone)}" data-path-depth-focus="${escapeHtml(model.focus)}" aria-label="Selected path depth lens">
      ${model.cells
        .map(
          (cell, index) => `
            <span class="quest-path-depth-cell" data-path-depth-cell="${escapeHtml(cell.id)}" data-path-depth-tone="${escapeHtml(cell.tone)}" style="--path-depth-index:${index};">
              <i>${escapeHtml(cell.label)}</i>
              <strong>${escapeHtml(compactText(cell.value, 24))}</strong>
              <em>${escapeHtml(compactText(cell.meta, 44))}</em>
            </span>`
        )
        .join("")}
    </span>`;
}

function renderQuestCockpit(lane) {
  const data = questCockpitData(lane);
  const minigameSigil = questMinigameSigil(lane);
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const signals = [
    { label: "asks", value: formatNumber(blockerPressure), tone: "gated", glyph: blockerPressure ? "GATE" : "OPEN", state: blockerPressure ? "locked" : "clear" },
    { label: "unlocks", value: formatNumber(lane.counts?.outcomes ?? 0), tone: "unlocked", glyph: "WIN", state: (lane.counts?.outcomes ?? 0) ? "earned" : "seed" },
    { label: "events", value: formatNumber(data.trail.length), tone: "advancing", glyph: "RUN", state: data.trail.length ? "live" : "seed" },
    { label: "score", value: formatNumber(lane.score ?? 0), tone: "scouting", glyph: "XP", state: (lane.score ?? 0) >= 70 ? "high" : "scout" },
  ];
  const visibleEvents = data.trail.slice(0, 4);
  const gateTitle = data.gate?.workerType ?? data.gate?.type ?? data.gate?.id ?? "Gate clear";
  const gateBody = data.gate?.nextAction ?? data.gate?.requestedAction ?? data.gate?.gate ?? data.gate?.riskGate ?? "No active blocker cells in the current snapshot.";
  const depthLayers = questDepthLayers(lane, data, gateTitle);
  const fieldCells = questFieldCells(lane, data, gateTitle, gateBody);
  const focusedRole = questFocusedRole(lane, fieldCells);
  const focusedCell = fieldCells.find((cell) => cell.role === focusedRole) ?? fieldCells[0];
  const focusedFieldCells = fieldCells.map((cell) => ({ ...cell, focused: cell.role === focusedRole }));
  const focusedIndex = Math.max(0, focusedFieldCells.findIndex((cell) => cell.role === focusedCell?.role));
  const focusedEchoes = questNodeEchoes(lane, data, focusedCell, gateTitle, gateBody);
  const focusedInsights = questInsightRibbonSignals(lane, data, focusedCell, gateTitle, gateBody);
  const focusedDrillCards = questNodeDrillCards(lane, data, focusedCell, gateTitle, gateBody);
  const crew = questCrewRelayRecord(lane);
  const cinematicFocus = questCinematicFocusPlateModel(lane, data, focusedCell, focusedDrillCards, focusedIndex, focusedFieldCells.length, crew);
  const activeExpansionLens = state.questExpansionLensByLane[lane.id] ?? "timeline";
  const questLensTrayData = {
    lensRows: cinematicFocus.expansionRows,
    activeLens: activeExpansionLens,
    lensDepthCards: questSelectedNodeLensDepthCards(lane, data, activeExpansionLens, gateTitle, gateBody),
  };
  Object.assign(cinematicFocus, questLensTrayData);
  const model = cinematicFocus;
  const eventPulsePackets = questEventPulsePackets(lane, data, focusedCell);
  const eventPulseIndex = Math.max(0, Math.min(eventPulsePackets.length - 1, state.questEventFocusByLane[lane.id] ?? 0));
  const cameraRail = questCameraRailSignals(lane, data, focusedCell);
  const routeCapsules = questRouteCapsules(focusedFieldCells, focusedRole);
  const levelReelNodes = questLevelReelNodes(lane, data, focusedFieldCells, focusedIndex);
  const pathDepthLens = questPathDepthLensModel(lane, data, focusedCell, gateTitle, gateBody);
  const realmMood = questRealmMoodModel(lane, data);
  const missionControlBand = questMissionControlBandModel(lane, data, focusedCell, gateTitle, gateBody, crew);
  return `
    <section class="detail-section">
      <div class="lane-button-top">
        <div>
          <p class="eyebrow">Money Path Run</p>
          <h3>${escapeHtml(compactText(lane.name, 78))}</h3>
        </div>
        <span class="badge ${escapeHtml(data.phase.tone)}">${escapeHtml(stateLabel(lane.state))}</span>
      </div>
      <div class="quest-cockpit" data-quest-motion-quality="premium" style="${laneStyle(lane)} --quest-progress:${data.checkpointProgress}%">
        <div class="quest-cockpit-hero" data-quest-hero-density="ghost">
          ${avatarMarkup(lane, "quest-avatar")}
          <div>
            <p class="eyebrow">Latest Discovery</p>
            <h3>${escapeHtml(compactText(data.newest?.title ?? lane.name, 92))}</h3>
            <p>${escapeHtml(compactText(data.newest?.summary ?? data.phase.summary, 190))}</p>
          </div>
          ${minigameSigil}
          <div class="quest-meter" aria-label="${formatNumber(data.checkpointProgress)} percent quest progress">
            <strong>${formatNumber(data.checkpointProgress)}%</strong>
            <span>quest</span>
          </div>
        </div>

        ${renderQuestMissionDirector(lane, data, gateTitle, gateBody)}

        <div class="quest-stage-grid">
          ${data.stageRows.map(renderQuestStage).join("")}
        </div>

        <div class="quest-signal-row" data-quest-signal-density="ghost">
          ${signals.map(renderQuestSignal).join("")}
        </div>

        <div class="quest-board-stack" aria-label="Interactive quest node stack">
          <div class="quest-field" data-quest-clarity-mode="focus" data-quest-board-focus-mode="spotlight" data-quest-board-director="camera" data-quest-motion-quality="premium" aria-label="Quest level map" style="--quest-field-count:${fieldCells.length};">
            <span class="quest-field-map-route" aria-hidden="true"></span>
            <span class="quest-field-runner" aria-hidden="true"></span>
            ${renderQuestBoardAtmosphere(lane, data, focusedCell)}
            ${renderQuestRealmMoodLayer(realmMood)}
            ${renderQuestBoardSignalOverlay(signals)}
            ${renderQuestBoardIdentityCartridge(lane, data, minigameSigil)}
            ${renderQuestMissionControlBand(missionControlBand)}
            ${renderQuestMissionReadout(lane, data, focusedCell, gateTitle)}
            ${renderQuestUnlockTrail(lane, data, levelReelNodes, focusedIndex)}
            ${renderQuestLaneConstellation(lane)}
            ${renderQuestBoardBotBadge(crew, lane, focusedCell)}
            ${renderQuestCameraRail(cameraRail, focusedCell)}
            ${renderQuestRouteCapsule(routeCapsules, focusedCell)}
            ${renderQuestUnlockPulse(lane, data, focusedCell)}
            ${renderQuestLevelReel(lane, data, focusedFieldCells, focusedIndex)}
            ${renderQuestEventPulse(eventPulsePackets, focusedCell, eventPulseIndex)}
            ${renderQuestRealmSkinCartridge(lane, data)}
            ${renderQuestCrewPresenceDock(lane)}
            ${renderQuestUnlockLadder(lane, data)}
            ${renderQuestDepthStack(depthLayers)}
            ${renderQuestSpotlightCameraAperture(focusedCell, focusedIndex, focusedFieldCells.length)}
            ${renderQuestFocusBeam(focusedCell, focusedIndex, focusedFieldCells.length)}
            ${focusedFieldCells.map(renderQuestFieldCell).join("")}
            ${renderQuestPathDepthLens(pathDepthLens)}
            ${renderQuestInsightRibbon(focusedInsights, focusedCell)}
            ${renderQuestNodeEchoRail(focusedEchoes, focusedCell)}
            ${renderQuestCinematicFocusPlate(cinematicFocus)}
            ${renderQuestMissionStack(model)}
            ${renderQuestMissionDossier(model)}
            ${renderQuestSelectedNodeExpansionConsole(cinematicFocus)}
            ${renderQuestSelectedNodeLensTray(cinematicFocus)}
            ${renderQuestNodeDrillStack(focusedDrillCards, focusedCell)}
            ${renderQuestRunSpine(lane, data, gateTitle, gateBody)}
          </div>
          ${renderQuestFocusLens(focusedCell, lane, data)}
        </div>

        <div class="quest-command-grid">
          <article class="quest-next-card">
            <p class="eyebrow">Next Move</p>
            <h3>${escapeHtml(compactText(data.nextAction, 96))}</h3>
            <p>${escapeHtml(compactText(data.phase.summary, 160))}</p>
          </article>
          <article class="quest-gate-card">
            <p class="eyebrow">Current Gate</p>
            <h3>${escapeHtml(compactText(gateTitle, 72))}</h3>
            <p>${escapeHtml(compactText(gateBody, 170))}</p>
          </article>
        </div>

        <div class="quest-event-chain">
          ${visibleEvents.map(renderQuestEvent).join("") || `<p class="small-muted">No lane events recorded yet. Future bot work will light up this chain.</p>`}
        </div>

        ${renderQuestActionDock()}
      </div>
    </section>`;
}

function questNodeHalos(lane, data, role) {
  const blockerPressure = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount = (lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0);
  const checkpoints = lane.quest?.checkpoints ?? [];
  const completeCheckpoints = checkpoints.filter((checkpoint) => checkpoint.status === "complete").length;
  const haloSets = {
    world: [
      { label: "traces", value: formatNumber(lane.counts?.traces ?? 0), tone: "live" },
      { label: "crew", value: formatNumber(lane.agentTypes?.length ?? 0), tone: "ready" },
    ],
    level: [
      { label: "xp", value: `${formatNumber(lane.progress ?? 0)}%`, tone: (lane.progress ?? 0) >= 70 ? "earned" : "live" },
      { label: "score", value: formatNumber(lane.score ?? 0), tone: (lane.score ?? 0) >= 70 ? "earned" : "live" },
    ],
    checkpoint: [
      { label: "quest", value: `${formatNumber(completeCheckpoints)}/${formatNumber(Math.max(checkpoints.length, 1))}`, tone: data.checkpointProgress >= 70 ? "earned" : "live" },
      { label: "trail", value: formatNumber(data.trail.length), tone: data.trail.length ? "live" : "seed" },
    ],
    gate: [
      { label: "locks", value: formatNumber(blockerPressure), tone: blockerPressure ? "gated" : "clear" },
      { label: "asks", value: formatNumber(lane.counts?.pendingRequests ?? 0), tone: (lane.counts?.pendingRequests ?? 0) ? "gated" : "clear" },
    ],
    next: [
      { label: "next", value: data.nextAction ? "Q" : "open", tone: data.nextAction ? "live" : "clear" },
      { label: "proof", value: formatNumber(proofCount), tone: proofCount ? "earned" : "seed" },
    ],
  };
  return haloSets[role] ?? [];
}

function questFieldCells(lane, data, gateTitle, gateBody) {
  return [
    ...data.stageRows.map((stage) => ({
      label: stage.label,
      title: stage.title,
      meta: stage.meta,
      tone: stage.status,
      role: stage.label.toLowerCase(),
      glyph: stage.label === "Checkpoint" ? "ACT" : stage.label === "Level" ? "XP" : "MAP",
      current: stage.label === "Checkpoint",
      halos: questNodeHalos(lane, data, stage.label.toLowerCase()),
    })),
    {
      label: "Gate",
      title: gateTitle,
      meta: gateBody,
      tone: data.gate ? "gated" : "complete",
      role: "gate",
      glyph: data.gate ? "LOCK" : "OK",
      current: Boolean(data.gate),
      halos: questNodeHalos(lane, data, "gate"),
    },
    {
      label: "Next",
      title: data.nextAction,
      meta: data.phase.label,
      tone: data.phase.tone,
      role: "next",
      glyph: "GO",
      current: false,
      halos: questNodeHalos(lane, data, "next"),
    },
  ];
}

function renderQuestFieldCell(cell, index) {
  return `
    <button class="quest-field-cell ${escapeHtml(cell.tone)}" type="button" data-quest-focus-node="${escapeHtml(cell.role)}" data-quest-node="${escapeHtml(cell.role)}" data-quest-current="${cell.current ? "true" : "false"}" data-quest-focused="${cell.focused ? "true" : "false"}" aria-pressed="${cell.focused ? "true" : "false"}" title="${escapeHtml(cell.title)}" style="--quest-cell-index:${index}; --quest-cell-depth:${index % 2};">
      <b class="quest-field-socket" aria-hidden="true"></b>
      <i class="quest-field-glyph" aria-hidden="true">${escapeHtml(cell.glyph)}</i>
      <span>${escapeHtml(cell.label)}</span>
      <strong>${escapeHtml(compactText(cell.title, 42))}</strong>
      <em>${escapeHtml(compactText(cell.meta, 54))}</em>
      <small class="quest-node-halos" aria-label="${escapeHtml(cell.label)} node status medals" style="--quest-node-halo-art:url('./assets/system/command-cockpit-node-halos-20260619.png');">
        ${(cell.halos ?? [])
          .map(
            (halo, haloIndex) => `
              <b class="quest-node-halo" data-node-halo-tone="${escapeHtml(halo.tone)}" style="--quest-node-halo-index:${haloIndex};">
                <i>${escapeHtml(halo.label)}</i>
                <strong>${escapeHtml(halo.value)}</strong>
              </b>`
          )
          .join("")}
      </small>
    </button>`;
}

function renderQuestStage(stage) {
  return `
    <article class="quest-stage ${escapeHtml(stage.status)}">
      <span>${escapeHtml(stage.label)}</span>
      <h3>${escapeHtml(compactText(stage.title, 54))}</h3>
      <p>${escapeHtml(stage.meta)}</p>
    </article>`;
}

function renderQuestSignal(signal, index) {
  return `
    <span class="quest-signal ${escapeHtml(signal.tone)}" data-quest-signal-state="${escapeHtml(signal.state)}" style="--quest-signal-index:${index};">
      <i class="quest-signal-glyph" aria-hidden="true">${escapeHtml(signal.glyph)}</i>
      <strong>${escapeHtml(signal.value)}</strong>
      <em>${escapeHtml(signal.label)}</em>
      <b class="quest-signal-shine" aria-hidden="true"></b>
    </span>`;
}

function renderQuestEvent(item, index) {
  return `
    <article class="quest-event ${escapeHtml(item.kind)}" style="--quest-event-index:${index}">
      <span>${escapeHtml(stateLabel(item.kind))}</span>
      <h3>${escapeHtml(compactText(item.title, 64))}</h3>
      <p>${escapeHtml(shortDate(item.time))} - ${escapeHtml(stateLabel(item.status))}</p>
    </article>`;
}

function milestoneRunwayNodes(lane) {
  const trail = chronicleTrail(lane);
  const baseNodes = pathMapNodes(lane)
    .filter((node) => node.kind !== "spawn")
    .slice(0, 9)
    .map((node, index) => ({
      kind: node.kind === "gate" ? "gate" : node.kind === "unlock" ? "unlock" : "checkpoint",
      status: node.status ?? "active",
      title: node.title,
      meta: node.meta,
      body: node.body,
      time: null,
      sourceIndex: index,
    }));
  const eventNodes = trail.slice(0, 5).map((item, index) => ({
    kind: "event",
    status: item.status ?? "recorded",
    title: item.title,
    meta: `${stateLabel(item.kind)} - ${shortDate(item.time)}`,
    body: item.summary ?? item.artifact ?? "Recorded lane event.",
    time: item.time,
    sourceIndex: baseNodes.length + index,
  }));
  return [...baseNodes, ...eventNodes].slice(0, 14);
}

function milestoneNodeMatchesLens(node, lens) {
  if (lens === "blockers") {
    return ["gate", "gated", "blocked", "needs_review"].includes(node.kind) || ["gated", "blocked", "needs_review"].includes(node.status);
  }
  if (lens === "unlocks") return node.kind === "unlock" || (node.kind !== "event" && node.status === "complete_read_only_money_path_map_ready");
  if (lens === "events") return node.kind === "event";
  return true;
}

function milestoneLensForLane(lane) {
  return state.milestoneLensByLane[lane.id] ?? "all";
}

function milestoneLensOptions(nodes) {
  return [
    { id: "all", label: "All", count: nodes.length + 1, hint: "full route" },
    { id: "blockers", label: "Gates", count: nodes.filter((node) => milestoneNodeMatchesLens(node, "blockers")).length, hint: "pressure" },
    { id: "unlocks", label: "Unlocks", count: nodes.filter((node) => milestoneNodeMatchesLens(node, "unlocks")).length, hint: "rewards" },
    { id: "events", label: "Events", count: nodes.filter((node) => milestoneNodeMatchesLens(node, "events")).length, hint: "log" },
    { id: "future", label: "Future", count: 1, hint: "next slot" },
  ];
}

function renderMilestoneRunway(lane) {
  const nodes = milestoneRunwayNodes(lane);
  const activeLens = milestoneLensForLane(lane);
  const lensOptions = milestoneLensOptions(nodes);
  const visibleNodes = activeLens === "future" ? [] : nodes.filter((node) => activeLens === "all" || milestoneNodeMatchesLens(node, activeLens));
  const showFutureSlot = activeLens === "all" || activeLens === "future";
  const trail = chronicleTrail(lane);
  const checkpoints = lane.quest?.checkpoints ?? [];
  const completeCheckpoints = checkpoints.filter((checkpoint) => checkpoint.status === "complete").length;
  const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const progress = checkpoints.length ? Math.round((completeCheckpoints / checkpoints.length) * 100) : lane.progress ?? 0;
  const stats = [
    { label: "route", value: `${formatNumber(progress)}%` },
    { label: "nodes", value: formatNumber(nodes.length) },
    { label: "gates", value: formatNumber(gateCount) },
    { label: "events", value: formatNumber(trail.length) },
  ];
  return `
    <section class="detail-section" id="milestone-runway" data-active-milestone-lens="${escapeHtml(activeLens)}" aria-label="Milestone runway">
      <div class="lane-button-top">
        <div>
          <p class="eyebrow">Milestone Runway</p>
          <h3>${escapeHtml(lane.name)} route spine</h3>
        </div>
        <span class="badge ${gateCount ? "gated" : "advancing"}">${formatNumber(progress)}% mapped</span>
      </div>
      <div class="milestone-runway ${activeLens !== "all" ? "is-lensed" : ""}" data-active-milestone-lens="${escapeHtml(activeLens)}" style="${laneStyle(lane)} --milestone-progress:${progress}%">
        <div class="milestone-runway-head">
          <div>
            <p class="eyebrow">Infinite Path Preview</p>
            <h3>${escapeHtml(compactText(chronicleNextAction(lane), 110))}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic ?? lane.visual?.mood ?? lane.notes, 170))}</p>
          </div>
          <div class="milestone-runway-stats">
            ${stats.map((stat) => `<span><strong>${escapeHtml(stat.value)}</strong><em>${escapeHtml(stat.label)}</em></span>`).join("")}
          </div>
        </div>
        <div class="milestone-lens-row" aria-label="Milestone runway lenses">
          ${lensOptions
            .map(
              (lens) => `
                <button class="milestone-lens ${activeLens === lens.id ? "active" : ""}" type="button" data-milestone-lens="${escapeHtml(lens.id)}" aria-pressed="${activeLens === lens.id}">
                  <strong data-milestone-lens-count="${escapeHtml(lens.id)}">${formatNumber(lens.count)}</strong>
                  <span>${escapeHtml(lens.label)}</span>
                  <em>${escapeHtml(lens.hint)}</em>
                </button>`
            )
            .join("")}
        </div>
        <div class="milestone-track" aria-label="Selected lane milestones">
          ${visibleNodes.map(renderMilestoneNode).join("")}
          ${
            showFutureSlot
              ? `<article class="milestone-node future">
                  <i>${formatNumber(nodes.length + 1)}</i>
                  <div>
                    <span>future slot</span>
                    <h3>Next Recorded Move</h3>
                    <p>Future tasks, gates, traces, and outcomes will extend this runway automatically.</p>
                  </div>
                </article>`
              : ""
          }
          ${
            !visibleNodes.length && !showFutureSlot
              ? `<article class="milestone-empty">
                  <span>${escapeHtml(stateLabel(activeLens))}</span>
                  <h3>No nodes in this lens yet</h3>
                  <p>As the lane records matching gates, unlocks, or events, this filtered route will populate automatically.</p>
                </article>`
              : ""
          }
        </div>
        <div class="milestone-runway-actions">
          <button class="tool-button" type="button" data-milestone-action="path" title="Open full Path Map">PATH</button>
          <button class="tool-button" type="button" data-milestone-action="chronicle" title="Open Chronicle">LOG</button>
          <button class="tool-button" type="button" data-milestone-action="trail" title="Open Trail">TRL</button>
        </div>
      </div>
    </section>`;
}

function renderMilestoneNode(node, index) {
  return `
    <article class="milestone-node ${escapeHtml(node.kind)} ${escapeHtml(node.status)}" style="--milestone-index:${index}">
      <i>${formatNumber(index + 1)}</i>
      <div>
        <span>${escapeHtml(node.meta ?? stateLabel(node.kind))}</span>
        <h3>${escapeHtml(compactText(node.title, 62))}</h3>
        <p>${escapeHtml(compactText(node.body, 128))}</p>
      </div>
    </article>`;
}

function agentPartyRecords(lane) {
  const records = botCommandRecords().filter((record) => record.lane?.id === lane.id || record.agent.agent_id === lane.ownerAgentId);
  if (records.length) return records;
  return laneAgents(lane).map((agent) => {
    const suggestion =
      state.snapshot.dispatchConsole?.suggestions?.find((item) => item.targetAgentId === agent.agent_id || item.laneId === lane.id) ??
      laneDispatchSuggestion(lane);
    const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id || draft.sourceId === suggestion?.id);
    const blockers = lane.counts?.blockers ?? 0;
    const pending = lane.counts?.pendingRequests ?? 0;
    const pressure = Math.min(100, blockers * 22 + pending * 16 + (suggestion?.urgency ?? 0) * 0.42);
    return {
      agent,
      lane,
      suggestion,
      staged,
      blockers,
      pending,
      pressure,
      visual: agent.visual ?? {},
      status: agent.status ?? "active",
    };
  });
}

function renderAgentParty(lane) {
  const records = agentPartyRecords(lane);
  const staged = records.filter((record) => record.staged).length;
  const gated = records.filter((record) => record.blockers || record.pending).length;
  const readiness = records.length ? Math.round(records.reduce((sum, record) => sum + crewReadiness(record), 0) / records.length) : lane.progress ?? 0;
  const suggestionCount = records.filter((record) => record.suggestion).length;
  return `
    <section class="detail-section" id="agent-party" aria-label="Agent party">
      <div class="lane-button-top">
        <div>
          <p class="eyebrow">Agent Party</p>
          <h3>${escapeHtml(lane.name)} command crew</h3>
        </div>
        <span class="badge ${gated ? "gated" : staged ? "staged" : "advancing"}">${formatNumber(readiness)} readiness</span>
      </div>
      <div class="agent-party-board" style="${laneStyle(lane)} --party-readiness:${readiness}%">
        <div class="agent-party-summary">
          <span><strong>${formatNumber(records.length)}</strong><em>bots</em></span>
          <span><strong>${formatNumber(gated)}</strong><em>gated</em></span>
          <span><strong>${formatNumber(suggestionCount)}</strong><em>asks</em></span>
          <span><strong>${formatNumber(staged)}</strong><em>staged</em></span>
        </div>
        <div class="agent-party-grid">
          ${records.length ? records.map(renderAgentPartyCard).join("") : renderAgentPartyFallback(lane)}
        </div>
      </div>
    </section>`;
}

function renderAgentPartyCard(record) {
  const { agent, lane, suggestion, staged, visual, pressure } = record;
  const callsign = visual.callsign ?? agent.agent_id;
  const readiness = crewReadiness(record);
  const mode = crewMode(record);
  const accent = visual.accent ?? lane?.visual?.accent ?? "#44d7c9";
  return `
    <article
      class="agent-party-card ${escapeHtml(mode)} ${staged ? "staged" : ""}"
      data-agent-party-lane="${escapeHtml(lane.id)}"
      style="--party-a:${escapeHtml(accent)}; --party-pressure:${Math.max(8, pressure)}%; --party-ready:${readiness}%;"
    >
      <div class="agent-party-top">
        ${agentRosterAvatar(agent)}
        <div>
          <p class="eyebrow">${escapeHtml(stateLabel(mode))}</p>
          <h3>${escapeHtml(compactText(callsign, 46))}</h3>
          <span>${escapeHtml(compactText(visual.specialty ?? stateLabel(agent.role_id), 82))}</span>
        </div>
        <strong>${formatNumber(readiness)}</strong>
      </div>
      <div class="agent-party-meter" aria-label="${formatNumber(readiness)} percent readiness"><span></span></div>
      <div class="agent-party-stats">
        <span><strong>L${escapeHtml(lane.level ?? 1)}</strong><em>level</em></span>
        <span><strong>${formatNumber(record.blockers)}</strong><em>gates</em></span>
        <span><strong>${formatNumber(record.pending)}</strong><em>review</em></span>
        <span><strong>${formatNumber(suggestion?.urgency ?? 0)}</strong><em>urge</em></span>
      </div>
      <p>${escapeHtml(compactText(suggestion?.reason ?? lane.nextAction ?? visual.specialty ?? "Ready for assignment.", 150))}</p>
      <div class="agent-party-thread">
        <span>${escapeHtml(compactText(agent.thread_id ?? lane.ownerThreadId ?? "No thread", 54))}</span>
      </div>
      <div class="agent-party-actions">
        <button class="tool-button" type="button" data-agent-party-action="comms" title="Open Comms">COM</button>
        <button class="tool-button" type="button" data-agent-party-action="queue" title="Stage command">${staged ? "OK" : "Q"}</button>
        <button class="tool-button" type="button" data-agent-party-action="path" title="Open Path">PATH</button>
      </div>
    </article>`;
}

function renderAgentPartyFallback(lane) {
  return `
    <article class="agent-party-card missing" data-agent-party-lane="${escapeHtml(lane.id)}">
      <div class="agent-party-top">
        ${avatarMarkup(lane, "operator-avatar")}
        <div>
          <p class="eyebrow">unassigned</p>
          <h3>${escapeHtml(lane.ownerAgentId ?? "No owner assigned")}</h3>
          <span>${escapeHtml(lane.ownerThreadId ?? "No thread")}</span>
        </div>
        <strong>0</strong>
      </div>
      <p>Bind an agent in the control plane and this lane party will populate automatically.</p>
    </article>`;
}

function minigameForgeFiles(lane) {
  return [
    { label: "visual", path: "web/data/lane-visuals.json", state: lane.visual?.minigame?.texture ? "complete" : "active" },
    { label: "registry", path: "MINIGAME_REGISTRY", state: minigameDefinition(lane) ? "complete" : "gated" },
    { label: "module", path: "web/app.js", state: minigameDefinition(lane) ? "complete" : "active" },
    { label: "guide", path: "web/games/README.md", state: "scouting" },
  ];
}

function minigameForgeStats(lane) {
  const minigame = lane.visual?.minigame ?? {};
  const custom = Boolean(minigameDefinition(lane));
  const stages = gameStepCount(lane);
  const assets = visualAssetRecords().filter((asset) => asset.laneId === lane.id && (asset.kind === "game" || asset.kind === "lane")).length;
  return [
    { label: "module", value: custom ? "custom" : "fallback" },
    { label: "stages", value: formatNumber(stages) },
    { label: "assets", value: formatNumber(assets) },
    { label: "status", value: stateLabel(minigame.status ?? "slot_ready") },
  ];
}

function renderMinigameForge(lane) {
  const minigame = lane.visual?.minigame ?? {};
  const custom = Boolean(minigameDefinition(lane));
  const files = minigameForgeFiles(lane);
  const stats = minigameForgeStats(lane);
  const texture = minigame.texture ?? lane.visual?.avatar;
  return `
    <section class="detail-section" id="minigame-forge" aria-label="Minigame forge">
      <div class="lane-button-top">
        <div>
          <p class="eyebrow">Minigame Forge</p>
          <h3>${escapeHtml(minigame.title ?? `${lane.name} module`)}</h3>
        </div>
        <span class="badge ${custom ? "unlocked" : "scouting"}">${escapeHtml(custom ? "custom renderer" : "checkpoint fallback")}</span>
      </div>
      <div class="minigame-forge-board" style="${laneStyle(lane)}">
        <div class="minigame-forge-art">
          ${texture ? `<img src="${escapeHtml(texture)}" alt="" loading="eager" />` : avatarMarkup(lane, "minigame-forge-fallback")}
          <span>${escapeHtml(minigame.id ?? "checkpoint")}</span>
        </div>
        <div class="minigame-forge-copy">
          <p class="eyebrow">Lane Module Blueprint</p>
          <h3>${escapeHtml(compactText(minigame.mechanic ?? lane.quest?.title ?? lane.visual?.mood, 120))}</h3>
          <p>${escapeHtml(compactText("Future lanes inherit this setup path: choose a minigame id, add a generated texture, register a renderer, and verify the Game, Arcade, and Asset Vault surfaces.", 190))}</p>
          <div class="minigame-forge-stats">
            ${stats
              .map(
                (stat) => `
                  <span class="minigame-forge-stat">
                    <strong>${escapeHtml(stat.value)}</strong>
                    <em>${escapeHtml(stat.label)}</em>
                  </span>`
              )
              .join("")}
          </div>
          <div class="minigame-forge-files" aria-label="Minigame extension files">
            ${files
              .map(
                (file) => `
                  <span class="minigame-forge-file ${escapeHtml(file.state)}">
                    <strong>${escapeHtml(file.label)}</strong>
                    <em>${escapeHtml(file.path)}</em>
                  </span>`
              )
              .join("")}
          </div>
          <div class="minigame-forge-actions">
            <button class="tool-button" type="button" data-minigame-forge-action="game" title="Open lane Game module">GAME</button>
            <button class="tool-button" type="button" data-minigame-forge-action="asset" title="Open game assets">ASSET</button>
            <button class="tool-button" type="button" data-minigame-forge-action="arcade" title="Open Arcade Deck">ARCADE</button>
          </div>
        </div>
      </div>
    </section>`;
}

function gateRadarItems(lane) {
  const gateItems = (lane.gateMap ?? []).map((gate, index) => ({
    id: gate.id ?? `gate-${index}`,
    kind: "gate",
    tone: lane.counts?.blockers ? "gated" : "review",
    title: gate.workerType ?? gate.type ?? gate.id ?? `Gate ${index + 1}`,
    label: gate.route ?? "blocked",
    body: gate.gate ?? gate.riskGate ?? "Gate requires operator review.",
    nextAction: gate.nextAction ?? gate.requestedAction ?? "Review and choose the next safe local step.",
    urgency: 92 - index * 8,
  }));
  const requestItems = (lane.serviceRequests ?? [])
    .filter((request) => !gateItems.some((gate) => gate.id === request.id))
    .map((request, index) => ({
      id: request.id ?? `request-${index}`,
      kind: "request",
      tone: request.status === "needs_review" ? "gated" : "review",
      title: request.type ?? request.id ?? `Request ${index + 1}`,
      label: request.status ?? "needs_review",
      body: request.riskGate ?? "Service request needs review.",
      nextAction: request.requestedAction ?? "Approve, reject, or narrow the request before work continues.",
      urgency: 78 - index * 6,
    }));
  const promotionItems = !gateItems.length && !requestItems.length
    ? (lane.promotionGates ?? []).slice(0, 3).map((gate, index) => ({
        id: `promotion-${index}`,
        kind: "promotion",
        tone: "scouting",
        title: `Promotion Gate ${index + 1}`,
        label: "watch",
        body: gate,
        nextAction: "Keep this gate visible while the lane gathers proof.",
        urgency: 44 - index * 4,
      }))
    : [];
  return [...gateItems, ...requestItems, ...promotionItems].slice(0, 6).map(enrichGateRadarItem);
}

function gateRadarCategory(item) {
  const text = `${item.title} ${item.label} ${item.body} ${item.nextAction}`.toLowerCase();
  if (/account|login|kyc|credential|seller|profile|oauth/.test(text)) return "account";
  if (/payment|wallet|payout|deposit|withdraw|treasury|trade|real-money|real money|billing/.test(text)) return "payment";
  if (/browser|session|live|website|marketplace|portal|browse|external/.test(text)) return "browser";
  if (/public|submit|submission|post|publish|contact|message|reply|pr|pull request|listing|upload/.test(text)) return "public";
  if (item.tone === "gated" || /block|gate|approval|signed|review required/.test(text)) return "blocker";
  return "review";
}

function enrichGateRadarItem(item) {
  const category = gateRadarCategory(item);
  const severity = item.tone === "gated" || item.urgency >= 82 ? "blocker" : item.tone === "scouting" ? "watch" : "review";
  return { ...item, category, severity };
}

function gateRadarFilterForLane(lane) {
  const value = state.gateRadarFilterByLane[lane.id] ?? "all";
  return gateRadarFilters().includes(value) ? value : "all";
}

function filteredGateRadarItems(items, activeFilter) {
  if (activeFilter === "all") return items;
  if (activeFilter === "blocker") return items.filter((item) => item.severity === "blocker" || item.category === "blocker");
  if (activeFilter === "review") return items.filter((item) => item.severity === "review" || item.category === "review");
  return items.filter((item) => item.category === activeFilter);
}

function gateRadarNotesForLane(lane) {
  return state.gateRadarNotesByLane[lane.id] ?? {};
}

function gateRadarNoteForItem(lane, item) {
  return gateRadarNotesForLane(lane)[item.id] ?? null;
}

function gateRadarSkin(lane) {
  const text = `${lane.id} ${lane.name} ${lane.department} ${lane.visual?.realm} ${lane.visual?.minigame?.id} ${lane.visual?.mood}`.toLowerCase();
  if (/platform|control|systems|runtime|adapter|gateway|worker/.test(text)) {
    return { id: "platform", label: "Control Tower", summary: "Circuit lattice skin for infrastructure gates and orchestration pressure." };
  }
  if (/security|scope|citadel|bounty private|web3|grant|hackathon|venture/.test(text)) {
    return { id: "risk", label: "Scope Citadel", summary: "Fortified grid skin for approval, safety, and scope boundaries." };
  }
  if (/payout|revenue|paid|bounty|sales|deal|lead/.test(text)) {
    return { id: "revenue", label: "Revenue Vault", summary: "Gold pulse skin for payout, claim, and commercial route gates." };
  }
  if (/trading|prediction|market|quant|observatory|competition|prize|baseline/.test(text)) {
    return { id: "market", label: "Market Observatory", summary: "Data-arc skin for paper markets, benchmarks, and measured experiments." };
  }
  if (/product|foundry|template|plugin|build|forge/.test(text)) {
    return { id: "build", label: "Product Foundry", summary: "Forge-heat skin for build lanes, bundles, and asset-readiness gates." };
  }
  return { id: "discovery", label: lane.visual?.realm ?? "Discovery Map", summary: "Cartography skin for source scouting, opportunity fog, and new-route blockers." };
}

function gateRadarStats(lane, items) {
  return [
    { label: "gates", value: formatNumber(lane.counts?.blockers ?? items.filter((item) => item.tone === "gated").length) },
    { label: "review", value: formatNumber(lane.counts?.pendingRequests ?? items.filter((item) => item.label === "needs_review").length) },
    { label: "requests", value: formatNumber(lane.counts?.serviceRequests ?? lane.serviceRequests?.length ?? 0) },
    { label: "pressure", value: `${formatNumber(Math.min(100, Math.max(...items.map((item) => item.urgency), 0)))}%` },
  ];
}

function renderGateRadar(lane) {
  const items = gateRadarItems(lane);
  const skin = gateRadarSkin(lane);
  const activeFilter = gateRadarFilterForLane(lane);
  const filteredItems = filteredGateRadarItems(items, activeFilter);
  const notes = gateRadarNotesForLane(lane);
  const notedCount = items.filter((item) => notes[item.id]?.text).length;
  const filterOptions = gateRadarFilters().filter((filter) => filter === "all" || items.some((item) => item.category === filter || item.severity === filter));
  const stats = gateRadarStats(lane, items);
  const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id);
  const pressure = Math.min(100, Math.max(...items.map((item) => item.urgency), lane.counts?.blockers ? 82 : 28));
  return `
    <section class="detail-section" id="gate-radar" aria-label="Gate radar">
      <div class="lane-button-top">
        <div>
          <p class="eyebrow">Gate Radar</p>
          <h3>${escapeHtml(filteredItems[0]?.title ?? items[0]?.title ?? "No active gates")}</h3>
        </div>
        <div class="gate-radar-title-badges">
          <span class="gate-radar-skin-pill skin-${escapeHtml(skin.id)}">${escapeHtml(skin.label)}</span>
          <span class="badge ${items.some((item) => item.tone === "gated") ? "gated" : "scouting"}">${formatNumber(filteredItems.length)} / ${formatNumber(items.length)} signals</span>
        </div>
      </div>
      <div class="gate-radar-filters" aria-label="Gate radar filters">
        ${filterOptions
          .map(
            (filter) => `
              <button
                class="gate-radar-filter ${activeFilter === filter ? "active" : ""}"
                type="button"
                data-gate-radar-filter="${escapeHtml(filter)}"
                aria-pressed="${activeFilter === filter ? "true" : "false"}"
              >
                ${escapeHtml(stateLabel(filter))}
              </button>`
          )
          .join("")}
      </div>
      <div class="gate-radar-board skin-${escapeHtml(skin.id)}" style="${laneStyle(lane)} --gate-pressure:${pressure}%; --gate-sigil:url('./assets/system/gate-radar-sigil-sheet-20260618.png'); --gate-realm:url('./assets/system/gate-radar-realm-skin-sheet-20260618.png')">
        <div class="gate-radar-scope" aria-label="Gate pressure radar">
          <div class="gate-radar-core">
            <strong>${formatNumber(pressure)}</strong>
            <span>pressure</span>
          </div>
          ${filteredItems.map(renderGateRadarPing).join("")}
        </div>
        <div class="gate-radar-console">
          <div class="gate-radar-stats">
            ${stats
              .map(
                (stat) => `
                  <span class="gate-radar-stat">
                    <strong>${escapeHtml(stat.value)}</strong>
                    <em>${escapeHtml(stat.label)}</em>
                  </span>`
              )
              .join("")}
          </div>
          <article class="gate-radar-skin-card skin-${escapeHtml(skin.id)}">
            <span>Realm Skin</span>
            <strong>${escapeHtml(skin.label)}</strong>
            <em>${escapeHtml(skin.summary)}</em>
          </article>
          ${renderGateRadarNotePanel(lane, items, notedCount)}
          <div class="gate-radar-cards">
            ${
              filteredItems.map((item) => renderGateRadarCard(lane, item)).join("") ||
              `<article class="gate-radar-card scouting"><h3>No matching signals</h3><p>This lane has no ${escapeHtml(stateLabel(activeFilter))} radar items in the current snapshot.</p></article>`
            }
          </div>
          <div class="gate-radar-actions">
            <button class="tool-button" type="button" data-gate-radar-action="comms" title="Open Comms">COM</button>
            <button class="tool-button" type="button" data-gate-radar-action="queue" title="Stage blocker review">${staged ? "OK" : "Q"}</button>
            <button class="tool-button" type="button" data-gate-radar-action="path" title="Open Path Map">PATH</button>
          </div>
        </div>
      </div>
    </section>`;
}

function renderGateRadarNotePanel(lane, items, notedCount) {
  const notes = gateRadarNotesForLane(lane);
  const focusedId = state.gateRadarNoteFocusByLane[lane.id];
  const first = items.find((item) => item.id === focusedId) ?? items.find((item) => notes[item.id]?.text) ?? items[0];
  const note = first ? notes[first.id]?.text ?? "" : "";
  return `
    <article class="gate-radar-note-panel">
      <div class="lane-button-top">
        <div>
          <span>Operator Notes</span>
          <strong>${formatNumber(notedCount)} pinned</strong>
        </div>
        <span class="badge scouting">local only</span>
      </div>
      <label>
        <span>${escapeHtml(first ? compactText(first.title, 40) : "No signal selected")}</span>
        <textarea data-gate-note-input="${escapeHtml(first?.id ?? "")}" maxlength="180" rows="2" placeholder="Add a private blocker note...">${escapeHtml(note)}</textarea>
      </label>
      <div class="gate-radar-note-actions">
        <button class="tool-button" type="button" data-gate-note-action="save" data-gate-note-id="${escapeHtml(first?.id ?? "")}" title="Save local note">SAVE</button>
        <button class="tool-button" type="button" data-gate-note-action="clear" data-gate-note-id="${escapeHtml(first?.id ?? "")}" title="Clear local note">CLEAR</button>
      </div>
    </article>`;
}

function renderGateRadarPing(item, index) {
  const angle = -42 + index * 38;
  const radius = Math.min(42, 18 + item.urgency * 0.24);
  const x = Math.round((50 + Math.cos((angle * Math.PI) / 180) * radius) * 10) / 10;
  const y = Math.round((50 + Math.sin((angle * Math.PI) / 180) * radius) * 10) / 10;
  return `
    <span
      class="gate-radar-ping ${escapeHtml(item.tone)} ${escapeHtml(item.kind)}"
      style="--gate-x:${x}%; --gate-y:${y}%; --gate-delay:${index * 130}ms;"
      title="${escapeHtml(item.title)}"
    >
      <i>${formatNumber(index + 1)}</i>
    </span>`;
}

function renderGateRadarCard(lane, item) {
  const note = gateRadarNoteForItem(lane, item);
  return `
    <article class="gate-radar-card ${escapeHtml(item.tone)} ${escapeHtml(item.kind)} category-${escapeHtml(item.category)} ${note ? "noted" : ""}">
      <div class="lane-button-top">
        <span class="gate-radar-sigil category-${escapeHtml(item.category)}" aria-hidden="true"></span>
        <h3>${escapeHtml(compactText(item.title, 54))}</h3>
        <span class="badge ${escapeHtml(item.tone)}">${escapeHtml(stateLabel(item.category))}</span>
      </div>
      <p>${escapeHtml(compactText(item.body, 140))}</p>
      <p>${escapeHtml(compactText(item.nextAction, 150))}</p>
      ${note ? `<p class="gate-radar-note-preview">${escapeHtml(note.text)}</p>` : ""}
      <div class="gate-radar-card-actions">
        <button class="tool-button" type="button" data-gate-note-focus="${escapeHtml(item.id)}" title="Focus local note">${note ? "NOTE" : "ADD"}</button>
      </div>
    </article>`;
}

function renderOverviewView(lane) {
  const stages = overviewStageDefinitions(lane);
  const requestedStage = state.overviewStageViewByLane[lane.id] ?? "quest";
  const activeStage = stages.some((stage) => stage.id === requestedStage) ? requestedStage : "quest";
  return `
    ${renderOverviewStageDock(lane, activeStage)}
    ${renderOverviewStagePanel(lane, activeStage)}`;
}

function overviewStageDefinitions(lane) {
  const owner = laneAgents(lane)[0];
  const minigame = lane.visual?.minigame ?? {};
  return [
    { id: "quest", label: "QUEST", title: "Current run", value: `L${lane.level}` },
    { id: "runway", label: "RUN", title: "Milestone runway", value: formatNumber(lane.quest?.checkpoints?.length ?? 0) },
    { id: "crew", label: "CREW", title: "Agent party", value: owner ? "1+" : "0" },
    { id: "forge", label: "FORGE", title: "Minigame forge", value: compactText(minigame.id ?? "base", 7).toUpperCase() },
    { id: "gates", label: "GATES", title: "Gate radar", value: formatNumber(lane.counts.blockers) },
    { id: "intel", label: "INTEL", title: "Lane intel", value: formatNumber(lane.recentTasks.length) },
  ];
}

function renderOverviewStageDock(lane, activeStage) {
  const stages = overviewStageDefinitions(lane);
  const activeIndex = Math.max(0, stages.findIndex((stage) => stage.id === activeStage));
  return `
    <section class="overview-stage-dock" aria-label="Overview mission module dock" style="${laneStyle(lane)} --overview-stage-index:${activeIndex}; --overview-stage-count:${stages.length};">
      <div class="overview-stage-meter">
        <strong>${escapeHtml(lane.visual?.realm ?? lane.department)}</strong>
        <span>L${escapeHtml(lane.level)} / ${escapeHtml(stateLabel(lane.state))}</span>
      </div>
      <div class="overview-stage-buttons" role="tablist" aria-label="Overview modules">
        <span class="overview-stage-compass-runner" aria-hidden="true"></span>
        ${stages
          .map(
            (stage, index) => `
              <button class="overview-stage-button ${stage.id === activeStage ? "active" : ""}" type="button" role="tab" aria-selected="${stage.id === activeStage ? "true" : "false"}" data-overview-stage="${escapeHtml(stage.id)}" style="--overview-stage-button-index:${index};" title="${escapeHtml(stage.title)}">
                <strong>${escapeHtml(stage.label)}</strong>
                <span>${escapeHtml(stage.value)}</span>
              </button>`
          )
          .join("")}
      </div>
    </section>`;
}

function renderOverviewStagePanel(lane, activeStage) {
  if (activeStage === "runway") return renderMilestoneRunway(lane);
  if (activeStage === "crew") return renderAgentParty(lane);
  if (activeStage === "forge") return renderMinigameForge(lane);
  if (activeStage === "gates") return renderGateRadar(lane);
  if (activeStage === "intel") return renderOverviewIntelPanel(lane);
  return renderQuestCockpit(lane);
}

function renderOverviewIntelPanel(lane) {
  return `
    <div class="overview-intel-panel">
    <section class="detail-section">
      <p class="eyebrow">World Module</p>
      ${renderWorldModule(lane)}
    </section>

    <section class="detail-section">
      <p class="eyebrow">Agents</p>
      <div class="tag-row">
        ${lane.agentTypes.map((tag) => `<span class="badge">${escapeHtml(stateLabel(tag))}</span>`).join("")}
      </div>
    </section>

    <section class="detail-section">
      <p class="eyebrow">Promotion Gates</p>
      <div class="tag-row">
        ${lane.promotionGates.map((tag) => `<span class="badge scouting">${escapeHtml(tag)}</span>`).join("")}
      </div>
    </section>

    <section class="detail-section">
      <p class="eyebrow">Current Blockers</p>
      <div class="request-grid">
        ${renderGateRows(lane)}
      </div>
    </section>

    <section class="detail-section">
      <p class="eyebrow">Recent Tasks</p>
      <div class="request-grid">
        ${lane.recentTasks.map(renderTaskRow).join("") || `<p class="small-muted">No recent tasks.</p>`}
      </div>
    </section>
    </div>`;
}

function renderWorldModule(lane) {
  const minigame = lane.visual?.minigame ?? {};
  return `
    <article class="world-module" style="${laneStyle(lane)}">
      <div class="world-orbit" aria-hidden="true">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <div>
        <div class="lane-button-top">
          <h3>${escapeHtml(minigame.title ?? "Lane Module")}</h3>
          <span class="badge advancing">${escapeHtml(stateLabel(minigame.status ?? "ready"))}</span>
        </div>
        <p>${escapeHtml(compactText(minigame.mechanic, 220))}</p>
      </div>
    </article>`;
}

function laneAgents(lane) {
  const agents = state.snapshot.agents ?? [];
  const direct = agents.filter((agent) => agent.agent_id === lane.ownerAgentId);
  if (direct.length) return direct;
  const departmentKey = String(lane.department ?? "").toLowerCase().replaceAll(" ", "_");
  return agents.filter((agent) => agent.department_id === departmentKey || agent.agent_id?.includes(lane.id));
}

function commandStatus(lane) {
  if (lane.counts.blockers) return { label: "Gated Draft", tone: "gated" };
  if (lane.promotionCandidate?.ready_for_manual_promotion) return { label: "Promotion Ready", tone: "unlocked" };
  if (lane.counts.activeTasks) return { label: "In Flight", tone: "advancing" };
  return { label: "Local Ready", tone: "scouting" };
}

function commandPreview(lane) {
  if (lane.promotionCandidate?.command_preview) return lane.promotionCandidate.command_preview;
  const owner = lane.ownerAgentId ?? "lane-manager";
  const next = lane.recentTasks?.[0]?.nextAction ?? lane.recentOutcomes?.[0]?.nextAction ?? "Create one local proof artifact, record it, and stop at gates.";
  return `To ${owner}: Review ${lane.id}, summarize the newest trail records, propose exactly one local-only next action, and do not run browser, account, wallet, public, payment, security, or real-money work. Context: ${next}`;
}

function buildBriefLines(lane) {
  const nextAction = lane.recentTasks?.[0]?.nextAction ?? lane.recentOutcomes?.[0]?.nextAction ?? lane.promotionCandidate?.next_decision;
  const gate = lane.gateMap?.[0] ?? lane.serviceRequests?.[0];
  return [
    {
      label: "Mission",
      value: lane.visual?.mood ?? lane.notes ?? `${lane.name} is tracking local proof, blockers, and promotion readiness.`,
    },
    {
      label: "Next Ask",
      value: nextAction ?? "Ask the lane manager for one evidence-backed local step.",
    },
    {
      label: "Boundary",
      value: gate?.nextAction ?? gate?.riskGate ?? "No side-effecting action without a recorded service request and explicit approval.",
    },
  ];
}

function commsCommandRoomStats(lane, ownerAgent) {
  const suggestion = bestLaneDispatchSuggestion(lane);
  const stagedCount = state.stagedDispatches.filter((draft) => draft.laneId === lane.id).length;
  const historyCount = state.dispatchHistory.filter((item) => item.laneName === lane.name).length;
  const linkedAgents = laneAgents(lane).length || (ownerAgent ? 1 : 0);
  return [
    { label: "bot", value: linkedAgents },
    { label: "queue", value: stagedCount },
    { label: "local log", value: historyCount },
    { label: "gates", value: lane.counts?.blockers ?? 0 },
    { label: "urgency", value: suggestion.urgency ?? 0 },
  ];
}

function commsCommandInboxItems(lane, ownerAgent, command) {
  const suggestion = bestLaneDispatchSuggestion(lane);
  const stagedDrafts = state.stagedDispatches.filter((draft) => draft.laneId === lane.id);
  const localHistory = state.dispatchHistory.filter((item) => item.laneName === lane.name);
  const gate = lane.gateMap?.[0] ?? lane.serviceRequests?.[0] ?? null;
  const nextAsk =
    lane.recentTasks?.[0]?.nextAction ??
    lane.recentOutcomes?.[0]?.nextAction ??
    lane.promotionCandidate?.next_decision ??
    suggestion.reason ??
    command;
  return [
    {
      id: "queued",
      label: "Queued",
      value: stagedDrafts.length,
      tone: stagedDrafts.length ? "staged" : "ready",
      body: stagedDrafts[0]?.reason ?? stagedDrafts[0]?.command ?? "No local draft is staged for this lane.",
      charge: stagedDrafts.length ? 100 : 18,
    },
    {
      id: "history",
      label: "Local Log",
      value: localHistory.length,
      tone: localHistory.length ? "logged" : "quiet",
      body: localHistory[0]?.command ?? localHistory[0]?.result ?? ownerAgent?.thread_id ?? lane.ownerThreadId ?? "No local command history yet.",
      charge: Math.min(100, localHistory.length * 24),
    },
    {
      id: "blocker",
      label: "Blocker",
      value: lane.counts?.blockers ?? 0,
      tone: lane.counts?.blockers ? "gated" : "clear",
      body: gate?.nextAction ?? gate?.riskGate ?? "No blocker is currently stopping the next local ask.",
      charge: Math.min(100, Math.max(10, (lane.counts?.blockers ?? 0) * 34)),
    },
    {
      id: "next",
      label: "Next Ask",
      value: suggestion.urgency ?? lane.counts?.activeTasks ?? 0,
      tone: suggestion.urgency || lane.counts?.activeTasks ? "active" : "ready",
      body: nextAsk,
      charge: Math.min(100, Math.max(18, suggestion.urgency ?? (lane.counts?.activeTasks ?? 0) * 18)),
    },
  ];
}

function renderCommsCommandInbox(lane, ownerAgent, command) {
  const items = commsCommandInboxItems(lane, ownerAgent, command);
  return `
        <div class="comms-command-inbox" aria-label="Comms command inbox">
          ${items
            .map(
              (item, index) => `
                <article class="comms-inbox-cell ${escapeHtml(item.tone)}" data-comms-inbox-cell="${escapeHtml(item.id)}" style="--inbox-cell-index:${index}; --inbox-charge:${Math.round(item.charge)}%;">
                  <i aria-hidden="true"></i>
                  <span>${escapeHtml(item.label)}</span>
                  <strong>${formatNumber(item.value)}</strong>
                  <p>${escapeHtml(compactText(item.body, 74))}</p>
                </article>`,
            )
            .join("")}
        </div>`;
}
function renderCommsCommandRoom(lane, ownerAgent, status, command) {
  const stats = commsCommandRoomStats(lane, ownerAgent);
  const suggestion = bestLaneDispatchSuggestion(lane);
  const copyLabel = state.copiedCommandFor === lane.id ? "OK" : state.copiedCommandFor === `manual:${lane.id}` ? "SEL" : "C";
  const target = ownerAgent?.visual?.callsign ?? lane.ownerAgentId ?? "Unassigned lane manager";
  const specialty = ownerAgent?.visual?.specialty ?? lane.visual?.realm ?? "Local command target";
  const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id);
  return `
    <article class="comms-command-room ${escapeHtml(status.tone)}" aria-label="Comms Command Room" style="${laneStyle(lane)} --comms-room-art:url('./assets/system/comms-command-room-20260618.png')">
      <div class="comms-command-visual">
        ${ownerAgent ? agentAvatarMarkup(ownerAgent, lane, "comms-command-avatar") : avatarMarkup(lane, "comms-command-avatar")}
        <span class="comms-command-signal" aria-hidden="true"></span>
      </div>
      <div class="comms-command-copy">
        <div class="comms-command-head">
          <div>
            <span>Comms Command Room</span>
            <strong>${escapeHtml(compactText(target, 58))}</strong>
          </div>
          <em>${escapeHtml(status.label)}</em>
        </div>
        <p>${escapeHtml(compactText(suggestion.reason ?? command, 190))}</p>
        <div class="comms-command-stats">
          ${stats.map((stat) => `<span><strong>${formatNumber(stat.value)}</strong><em>${escapeHtml(stat.label)}</em></span>`).join("")}
        </div>
        <div class="comms-command-thread">
          <strong>${escapeHtml(compactText(specialty, 76))}</strong>
          <span>${escapeHtml(compactText(ownerAgent?.thread_id ?? lane.ownerThreadId ?? "No thread bound yet", 96))}</span>
        </div>
        ${renderCommsCommandInbox(lane, ownerAgent, command)}
        <div class="comms-command-actions">
          <button class="tool-button" type="button" data-stage-lane-command="${escapeHtml(lane.id)}" title="Stage command in outbox">${staged ? "OK" : "Q"}</button>
          <button class="tool-button" type="button" data-copy-command="${escapeHtml(lane.id)}" title="Copy local command draft">${escapeHtml(copyLabel)}</button>
          <button class="tool-button" type="button" data-detail-view="path" title="Open Path Map">PATH</button>
        </div>
      </div>
    </article>`;
}

function renderCommsView(lane) {
  const agents = laneAgents(lane);
  const ownerAgent = agents[0];
  const status = commandStatus(lane);
  const command = commandPreview(lane);
  const copyLabel = state.copiedCommandFor === lane.id ? "OK" : state.copiedCommandFor === `manual:${lane.id}` ? "SEL" : "C";
  const briefLines = buildBriefLines(lane);
  const draftTarget = ownerAgent?.visual?.callsign ?? lane.ownerAgentId ?? "Unassigned lane manager";
  return `
    <section class="detail-section">
      <div class="lane-button-top">
        <div>
          <p class="eyebrow">Agent Comms</p>
          <h3>Command deck</h3>
        </div>
        <span class="badge ${escapeHtml(status.tone)}">${escapeHtml(status.label)}</span>
      </div>
      ${renderCommsCommandRoom(lane, ownerAgent, status, command)}
      <div class="comms-console" style="${laneStyle(lane)}">
        <div class="comms-beam" aria-hidden="true"></div>
        <div class="comms-grid">
          <article class="comms-roster">
            <div class="comms-section-head">
              <p class="eyebrow">Roster</p>
              <strong>${formatNumber(agents.length || (lane.ownerAgentId ? 1 : 0))}</strong>
            </div>
            <div class="agent-stack">
              ${agents.length ? agents.map((agent) => renderAgentChip(agent, lane)).join("") : renderMissingAgent(lane)}
            </div>
          </article>
          <article class="comms-brief">
            <div class="comms-section-head">
              <p class="eyebrow">Brief Packet</p>
              <strong>${escapeHtml(lane.ownerThreadId ? "Thread" : "Local")}</strong>
            </div>
            ${briefLines.map(renderBriefLine).join("")}
          </article>
        </div>
        <article class="command-draft">
          <div class="command-draft-top">
            <div>
              <p class="eyebrow">Draft To Bot</p>
              <h3>${escapeHtml(draftTarget)}</h3>
            </div>
            <div class="command-action-row">
              <button class="tool-button" type="button" data-stage-lane-command="${escapeHtml(lane.id)}" title="Stage command in outbox">Q</button>
              <button class="tool-button" type="button" data-copy-command="${escapeHtml(lane.id)}" title="Copy local command draft">${escapeHtml(copyLabel)}</button>
            </div>
          </div>
          <pre>${escapeHtml(command)}</pre>
        </article>
      </div>
    </section>`;
}

function renderAgentChip(agent, lane) {
  const visual = agent.visual ?? {};
  const callsign = visual.callsign ?? agent.agent_id;
  const specialty = visual.specialty ?? `${stateLabel(agent.role_id)} - ${stateLabel(agent.status)}`;
  return `
    <div class="agent-chip" style="--agent-a:${escapeHtml(visual.accent ?? lane.visual?.accent ?? "#44d7c9")}">
      ${agentAvatarMarkup(agent, lane, "agent-chip-avatar")}
      <div>
        <h3>${escapeHtml(callsign)}</h3>
        <p>${escapeHtml(specialty)}</p>
        <span>${escapeHtml(agent.thread_id ?? lane.ownerThreadId ?? "No thread")}</span>
      </div>
    </div>`;
}

function renderMissingAgent(lane) {
  return `
    <div class="agent-chip">
      ${avatarMarkup(lane, "agent-chip-avatar")}
      <div>
        <h3>${escapeHtml(lane.ownerAgentId ?? "No owner assigned")}</h3>
        <p>${escapeHtml(lane.ownerAgentId ? "Owner listed on lane" : "Waiting for lane owner")}</p>
        <span>${escapeHtml(lane.ownerThreadId ?? "No thread")}</span>
      </div>
    </div>`;
}

function renderBriefLine(item) {
  return `
    <div class="brief-line">
      <span>${escapeHtml(item.label)}</span>
      <p>${escapeHtml(compactText(item.value, 210))}</p>
    </div>`;
}

async function copyText(text) {
  const field = document.createElement("textarea");
  field.value = text;
  field.setAttribute("readonly", "");
  field.style.position = "fixed";
  field.style.opacity = "0";
  document.body.appendChild(field);
  field.select();
  const localCopyOk = document.execCommand("copy");
  field.remove();
  if (localCopyOk) return true;

  if (navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      // Fall through to the static-page fallback below.
    }
  }
  return false;
}

function chronicleTrail(lane) {
  return lane.trail?.length ? lane.trail : lane.milestones ?? [];
}

function chronicleKindCounts(trail) {
  return trail.reduce((counts, item) => {
    counts[item.kind] = (counts[item.kind] ?? 0) + 1;
    return counts;
  }, {});
}

function chroniclePhase(lane, trail) {
  if (lane.counts?.blockers) return { label: "Gate Chamber", tone: "gated", summary: `${formatNumber(lane.counts.blockers)} blockers need operator review.` };
  if (lane.promotionCandidate?.ready_for_manual_promotion) return { label: "Boss Door", tone: "unlocked", summary: "Promotion candidate is ready for manual decision." };
  if (lane.counts?.activeTasks) return { label: "Live Run", tone: "advancing", summary: `${formatNumber(lane.counts.activeTasks)} tasks are moving.` };
  if (trail.length) return { label: "Archive Run", tone: "scouting", summary: "Trail is mapped and ready for the next local proof." };
  return { label: "Spawn Point", tone: "scouting", summary: "Waiting for first recorded lane event." };
}

function chronicleNextAction(lane) {
  return (
    lane.gateMap?.[0]?.nextAction ??
    lane.recentTasks?.[0]?.nextAction ??
    lane.recentOutcomes?.[0]?.nextAction ??
    lane.promotionCandidate?.next_decision ??
    "Ask the lane owner for one narrow local proof step."
  );
}

function pathMapNodes(lane) {
  const checkpoints = lane.quest?.checkpoints ?? [];
  const gates = gateRadarItems(lane);
  const unlocks = lane.recentOutcomes ?? [];
  const nodes = [
    {
      id: "spawn",
      kind: "spawn",
      status: "complete",
      title: "Spawn",
      meta: "lane initialized",
      body: lane.visual?.mood ?? lane.notes ?? "Lane world is ready for recorded progress.",
      level: lane.level,
    },
  ];

  checkpoints.slice(0, 5).forEach((checkpoint, index) => {
    nodes.push({
      id: checkpoint.id ?? `checkpoint-${index}`,
      kind: "checkpoint",
      status: checkpoint.status ?? "active",
      title: checkpoint.title ?? `Checkpoint ${index + 1}`,
      meta: `stage ${index + 1}`,
      body: checkpoint.description ?? "Advance this lane with one recorded proof step.",
      level: index + 1,
    });
  });

  gates.slice(0, 3).forEach((gate, index) => {
    const note = gateRadarNoteForItem(lane, gate);
    nodes.push({
      id: gate.id ?? `gate-${index}`,
      kind: "gate",
      status: gate.tone === "gated" || lane.counts?.blockers ? "gated" : "review",
      title: gate.title ?? gate.id ?? `Gate ${index + 1}`,
      meta: stateLabel(gate.category ?? "blocker"),
      body: gate.nextAction ?? gate.body ?? "Needs explicit review before side-effecting work.",
      level: checkpoints.length + index + 1,
      note,
    });
  });

  unlocks.slice(0, 3).forEach((outcome, index) => {
    nodes.push({
      id: outcome.id ?? `unlock-${index}`,
      kind: "unlock",
      status: outcome.status ?? "recorded",
      title: outcome.type ?? outcome.title ?? `Unlock ${index + 1}`,
      meta: shortDate(outcome.createdAt ?? outcome.time),
      body: outcome.nextAction ?? outcome.evidence ?? "Outcome is recorded in the lane ledger.",
      level: checkpoints.length + gates.length + index + 1,
    });
  });

  return nodes;
}

function focusedPathNode(lane, nodes) {
  const focusedId = state.pathNodeFocusByLane[lane.id];
  return (
    nodes.find((node) => node.id === focusedId) ??
    nodes.find((node) => node.kind === "gate") ??
    nodes.find((node) => node.status !== "complete") ??
    nodes[0]
  );
}

function pathNodeSearchTerms(node) {
  const source = [node.id, node.kind, node.status, node.title, node.meta, node.body, node.note?.text].filter(Boolean).join(" ");
  return [...new Set(source.toLowerCase().split(/[^a-z0-9_]+/).flatMap((term) => term.split("_")).filter((term) => term.length >= 4))];
}

function pathNodeRelatedEvents(lane, node, limit = 3) {
  const trail = chronicleTrail(lane);
  if (!node || !trail.length) return [];
  const nodeTitle = String(node.title ?? "").toLowerCase();
  const nodeId = String(node.id ?? "").toLowerCase();
  const terms = pathNodeSearchTerms(node);
  const scored = trail
    .map((item, index) => {
      const haystack = [item.kind, item.title, item.status, item.summary, item.artifact].filter(Boolean).join(" ").toLowerCase();
      let score = 0;
      if (nodeTitle && haystack.includes(nodeTitle)) score += 5;
      if (nodeId && haystack.includes(nodeId)) score += 5;
      if (node.kind === "gate" && ["service_request", "request", "blocker"].some((term) => haystack.includes(term))) score += 2;
      if (node.kind === "unlock" && ["outcome", "unlock", "complete"].some((term) => haystack.includes(term))) score += 2;
      terms.forEach((term) => {
        if (haystack.includes(term)) score += 1;
      });
      return { item, index, score };
    })
    .filter((entry) => entry.score > 0)
    .sort((a, b) => b.score - a.score || a.index - b.index)
    .slice(0, limit)
    .map((entry) => entry.item);

  return scored.length ? scored : trail.slice(0, limit);
}

function pathEventKey(item) {
  const source = [item.kind, item.time, item.status, item.title, item.artifact].filter(Boolean).join("-");
  return (
    source
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 140) || "event"
  );
}

function focusedPathEvent(lane, relatedEvents) {
  const focusedKey = state.pathEventFocusByLane[lane.id];
  return relatedEvents.find((item) => pathEventKey(item) === focusedKey) ?? chronicleTrail(lane).find((item) => pathEventKey(item) === focusedKey) ?? relatedEvents[0] ?? null;
}

function pathEventContext(lane, relatedEvents) {
  const trail = chronicleTrail(lane);
  const focusedEvent = focusedPathEvent(lane, relatedEvents);
  if (!focusedEvent) return null;
  const focusedKey = pathEventKey(focusedEvent);
  const trailIndex = Math.max(0, trail.findIndex((item) => pathEventKey(item) === focusedKey));
  const newer = trail[trailIndex - 1] ?? null;
  const older = trail[trailIndex + 1] ?? null;
  return {
    item: focusedEvent,
    key: focusedKey,
    index: trailIndex,
    total: trail.length,
    newerKey: newer ? pathEventKey(newer) : "",
    olderKey: older ? pathEventKey(older) : "",
  };
}

function pathMapNoteItems(lane) {
  return gateRadarItems(lane)
    .map((item) => ({ item, note: gateRadarNoteForItem(lane, item) }))
    .filter((entry) => entry.note?.text)
    .slice(0, 5);
}

function pathMapStatus(lane) {
  if (lane.counts?.blockers) return { label: "Gate Lock", tone: "gated" };
  if (lane.promotionCandidate?.ready_for_manual_promotion) return { label: "Boss Door", tone: "unlocked" };
  if (lane.counts?.activeTasks) return { label: "Active Run", tone: "advancing" };
  return { label: "Scout Route", tone: "scouting" };
}

function pathMissionGlanceCards(lane, trail, focusedNode, pathNotes, pathProgress) {
  const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount = pathProofItems(lane).length || trail.filter((item) => pathEventGlyphType(item) === "proof").length;
  const unlockCount = lane.counts?.outcomes ?? trail.filter((item) => pathEventGlyphType(item) === "outcome").length;
  const taskCount = lane.counts?.activeTasks ?? trail.filter((item) => pathEventGlyphType(item) === "task").length;
  const bossReady = lane.promotionCandidate?.ready_for_manual_promotion;
  return [
    {
      id: "level",
      label: "level",
      value: `${formatNumber(pathProgress)}%`,
      note: focusedNode?.title ?? lane.quest?.title ?? "route mapped",
      tone: bossReady ? "unlocked" : "advancing",
    },
    {
      id: "gate",
      label: "gate",
      value: gateCount ? formatNumber(gateCount) : "clear",
      note: gateCount ? lane.gateMap?.[0]?.nextAction ?? lane.serviceRequests?.[0]?.requestedAction ?? "blocker active" : "no blocker lock",
      tone: gateCount ? "gated" : "ready",
    },
    {
      id: "proof",
      label: "proof",
      value: formatNumber(proofCount),
      note: proofCount ? "evidence cache" : "needs capture",
      tone: proofCount ? "unlocked" : "scouting",
    },
    {
      id: "tasks",
      label: "tasks",
      value: formatNumber(taskCount),
      note: lane.recentTasks?.[0]?.title ?? lane.nextAction ?? "task runway",
      tone: taskCount ? "advancing" : "scouting",
    },
    {
      id: "notes",
      label: "notes",
      value: formatNumber(pathNotes.length),
      note: pathNotes[0]?.note?.text ?? `${formatNumber(unlockCount)} wins logged`,
      tone: pathNotes.length ? "gated" : unlockCount ? "unlocked" : "scouting",
    },
  ];
}

function renderPathMissionRunMeter(cards, pathProgress) {
  const activeIndex = Math.max(
    0,
    cards.findIndex((card) => card.tone === "gated" || card.tone === "advancing" || card.tone === "unlocked" || card.tone === "ready")
  );
  return `
    <div class="path-run-meter" aria-label="Mission run meter" style="--path-run-art:url('./assets/system/path-run-meter-hud-20260618.png'); --path-run-progress:${pathProgress}%; --path-run-count:${cards.length}; --path-run-active:${activeIndex};">
      <span class="path-run-track" aria-hidden="true"></span>
      ${cards
        .map(
          (card, index) => `
            <span class="path-run-step ${escapeHtml(card.tone)} ${index === activeIndex ? "active" : ""}" style="--path-run-step-index:${index};" title="${escapeHtml(card.label)}: ${escapeHtml(compactText(card.note, 54))}">
              <i>${formatNumber(index + 1)}</i>
              <em>${escapeHtml(card.label)}</em>
            </span>`
        )
        .join("")}
    </div>`;
}

function pathMissionCrewTokens(lane) {
  const records = agentPartyRecords(lane);
  if (records.length) return records.slice(0, 3);
  return [];
}

function renderPathMissionCrewPresence(lane) {
  const records = pathMissionCrewTokens(lane);
  if (!records.length) {
    return `
      <div class="path-crew-presence empty" aria-label="Path crew presence">
        <span class="path-crew-empty">crew slot open</span>
      </div>`;
  }
  return `
    <div class="path-crew-presence" aria-label="Path crew presence">
      ${records
        .map((record, index) => {
          const mode = crewMode(record);
          const readiness = crewReadiness(record);
          const callsign = record.visual?.callsign ?? record.agent?.agent_id ?? "unassigned";
          return `
            <span class="path-crew-token ${escapeHtml(mode)}" style="--path-crew-index:${index}; --path-crew-ready:${readiness}%; --path-crew-accent:${escapeHtml(record.visual?.accent ?? lane.visual?.accent ?? "#44d7c9")};" title="${escapeHtml(callsign)}: ${formatNumber(readiness)} readiness">
              ${agentRosterAvatar(record.agent)}
              <i></i>
              <em>${escapeHtml(compactText(callsign, 18))}</em>
            </span>`;
        })
        .join("")}
    </div>`;
}

function renderPathMissionGlance(lane, trail, focusedNode, pathNotes, pathProgress) {
  const status = pathMapStatus(lane);
  const cards = pathMissionGlanceCards(lane, trail, focusedNode, pathNotes, pathProgress);
  const nextAction = chronicleNextAction(lane);
  const stageLabel = lane.promotionCandidate?.ready_for_manual_promotion ? "Boss Door Ready" : status.label;
  return `
    <section class="path-mission-glance" aria-label="Mission glance" style="${laneStyle(lane)} --path-progress:${pathProgress}%;">
      <span class="path-glance-pulse" aria-hidden="true"></span>
      <div class="path-glance-main">
        ${avatarMarkup(lane, "path-map-avatar")}
        <div class="path-glance-copy">
          <p class="eyebrow">Mission Glance</p>
          <h3>${escapeHtml(compactText(nextAction, 96))}</h3>
          <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic ?? lane.quest?.title ?? lane.visual?.mood, 142))}</p>
          ${renderPathMissionRunMeter(cards, pathProgress)}
          ${renderPathMissionCrewPresence(lane)}
        </div>
        <div class="path-map-gauge" aria-label="${formatNumber(pathProgress)} percent mapped">
          <strong>${formatNumber(pathProgress)}%</strong>
          <span>route</span>
        </div>
      </div>
      <div class="path-glance-command-console">
        <div class="path-glance-cards">
          ${cards
            .map(
              (card) => `
                <span class="path-glance-card ${escapeHtml(card.tone)}">
                  <strong>${escapeHtml(card.value)}</strong>
                  <em>${escapeHtml(card.label)}</em>
                  <small>${escapeHtml(compactText(card.note, 48))}</small>
                </span>`
            )
            .join("")}
        </div>
        <div class="path-glance-actions" aria-label="Mission glance actions">
          <span class="badge ${escapeHtml(status.tone)}">${escapeHtml(stageLabel)}</span>
          <button class="tool-button" type="button" data-path-glance-jump="route" title="Open route rail">ROUTE</button>
          <button class="tool-button" type="button" data-path-glance-jump="proof" title="Open proof cache">PROOF</button>
          <button class="tool-button" type="button" data-path-glance-jump="archive" title="Open chapter archive">ARCH</button>
          <button class="tool-button primary" type="button" data-detail-view="comms" title="Open command deck">COM</button>
        </div>
      </div>
    </section>`;
}

function pathCoreDeckView(lane) {
  const stored = state.pathCoreDeckViewByLane[lane.id];
  const validViews = new Set(["scan", "command", "route"]);
  if (validViews.has(stored)) return stored;
  if (lane.counts?.blockers || lane.counts?.pendingRequests) return "scan";
  if (lane.counts?.activeTasks) return "command";
  return "scan";
}

function renderPathRouteRail(lane, nodes, focusedNode) {
  return `
    <div class="path-route" aria-label="Lane route map" style="${laneStyle(lane)} --path-route-count:${nodes.length + 1}; --path-route-active:${Math.max(0, nodes.findIndex((node) => node.id === focusedNode?.id))};">
      <span class="path-route-spine" aria-hidden="true"></span>
      <span class="path-route-runner" aria-hidden="true"></span>
      ${nodes.map((node, index) => renderPathMapNode(node, index, focusedNode?.id)).join("")}
      <article class="path-node future" style="--path-index:${nodes.length}; --path-node-charge:28%;">
        <i>${formatNumber(nodes.length + 1)}</i>
        <div>
          <span>future</span>
          <h3>Next Unlock Slot</h3>
          <p>New bot records, tasks, traces, and outcomes will extend this route automatically.</p>
        </div>
      </article>
    </div>`;
}

function renderPathStageFocusLens(lane, focusedNode, pathProgress) {
  const node = focusedNode ?? {
    kind: "future",
    status: "future",
    title: "Next unlock slot",
    meta: "future",
    body: "This path will expand as new proof, blockers, and milestones are recorded.",
  };
  const note = node.note?.text ?? node.body ?? node.meta ?? "Selected level is ready for review.";
  const title = String(node.title ?? "Selected level").replace(/[_-]+/g, " ");
  const events = pathStageNodeEchoEvents(lane, node);
  return `
    <aside class="path-stage-focus-lens ${escapeHtml(node.kind)} ${escapeHtml(node.status)}" style="--path-focus-progress:${pathProgress}%" aria-label="Focused path level">
      <span class="path-stage-focus-beam" aria-hidden="true"></span>
      <i>${escapeHtml(stateLabel(node.kind))}</i>
      <strong>${escapeHtml(compactText(title, 42))}</strong>
      <em>${escapeHtml(compactText(note, 58))}</em>
      ${
        events.length
          ? `<span class="path-stage-focus-drill" aria-label="Focused level trail events">
              ${events
                .map((item, index) => {
                  const tone = pathEventGlyphType(item);
                  const label = stateLabel(tone);
                  const detail = compactText(item?.title ?? item?.summary ?? item?.status ?? label, 34);
                  return `<b class="${escapeHtml(tone)}" style="--path-focus-drill-index:${index};"><i>${escapeHtml(label.slice(0, 2))}</i><span>${escapeHtml(detail)}</span></b>`;
                })
                .join("")}
            </span>`
          : ""
      }
    </aside>`;
}

function renderPathStageEncounterTether(focusedNode) {
  return `
        <span class="path-stage-encounter-tether ${escapeHtml(focusedNode?.kind ?? "future")} ${escapeHtml(focusedNode?.status ?? "future")}" aria-hidden="true">
          <i></i>
          <b></b>
        </span>`;
}

function pathStageBotCommandBeaconModel(lane) {
  const records = pathMissionCrewTokens(lane);
  const record = records[0];
  const owner = record?.agent ?? laneAgents(lane)[0];
  const suggestion = bestLaneDispatchSuggestion(lane);
  const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id || draft.sourceId === suggestion.id);
  const callsign = record?.visual?.callsign ?? owner?.visual?.callsign ?? owner?.name ?? lane.ownerAgentId ?? "Lane bot";
  const specialty = record?.visual?.specialty ?? owner?.visual?.specialty ?? suggestion.label ?? lane.nextAction ?? "local command";
  return {
    laneId: lane.id,
    agent: owner,
    callsign,
    specialty,
    staged,
    mode: record ? crewMode(record) : staged ? "staged" : lane.counts?.blockers || lane.counts?.pendingRequests ? "gated" : "watching",
    readiness: record ? crewReadiness(record) : lane.progress ?? 0,
    thread: lane.ownerThreadId ?? owner?.thread_id ?? "No thread",
    accent: record?.visual?.accent ?? owner?.visual?.accent ?? lane.visual?.accent ?? "#44d7c9",
  };
}

function renderPathStageBotCommandBeacon(lane) {
  const model = pathStageBotCommandBeaconModel(lane);
  return `
        <div class="path-stage-bot-command-beacon ${escapeHtml(model.mode)} ${model.staged ? "staged" : ""}" style="--path-stage-bot-ready:${model.readiness}%; --path-stage-bot-accent:${escapeHtml(model.accent)};" aria-label="Path bot command beacon">
          ${model.agent ? agentRosterAvatar(model.agent) : `<span class="operator-avatar avatar-fallback" aria-hidden="true"></span>`}
          <span>
            <strong>${escapeHtml(compactText(model.callsign, 18))}</strong>
            <em>${escapeHtml(compactText(model.staged ? "handoff staged" : model.specialty, 28))}</em>
          </span>
          <button class="tool-button" type="button" data-path-handoff-stage="${escapeHtml(model.laneId)}" title="Stage local bot handoff">${model.staged ? "OK" : "Q"}</button>
          <button class="tool-button primary" type="button" data-detail-view="comms" title="Open bot command room">COM</button>
          <i>${formatNumber(model.readiness)}</i>
        </div>`;
}

function renderPathStageCrewSprites(lane, pathProgress) {
  const records = pathMissionCrewTokens(lane).slice(0, 3);
  if (!records.length) return "";
  return `
      <span class="path-stage-crew-sprites" aria-label="Path route crew sprites" style="--path-stage-crew-progress:${pathProgress}%;">
        ${records
          .map((record, index) => {
            const readiness = crewReadiness(record);
            const mode = crewMode(record);
            const callsign = record.visual?.callsign ?? record.agent?.agent_id ?? `Bot ${index + 1}`;
            return `
              <span class="path-stage-crew-sprite ${escapeHtml(mode)}" style="--path-stage-crew-index:${index}; --path-stage-crew-ready:${readiness}%; --path-stage-crew-accent:${escapeHtml(record.visual?.accent ?? lane.visual?.accent ?? "#44d7c9")};" title="${escapeHtml(callsign)}: ${formatNumber(readiness)} readiness">
                ${agentRosterAvatar(record.agent)}
                <i>${escapeHtml(compactText(callsign, 10))}</i>
              </span>`;
          })
          .join("")}
      </span>`;
}

function pathStageNodeBadgeModel(node) {
  const kind = node?.kind ?? "future";
  const status = node?.status ?? "future";
  const badges = [];
  if (kind === "gate" || status === "gated") badges.push({ tone: "gate", label: "gate" });
  if (kind === "unlock" || status === "unlocked" || status === "recorded") badges.push({ tone: "unlock", label: "win" });
  if (kind === "checkpoint" || status === "active" || status === "review") badges.push({ tone: "proof", label: "test" });
  if (status === "complete" || status === "ready") badges.push({ tone: "done", label: "done" });
  if (kind === "spawn") badges.push({ tone: "spawn", label: "spawn" });
  if (kind === "future" || status === "future") badges.push({ tone: "future", label: "next" });
  return badges.slice(0, 2);
}

function renderPathStageNodeBadges(node) {
  const badges = pathStageNodeBadgeModel(node);
  if (!badges.length) return "";
  return `
              <span class="path-stage-node-badges" aria-hidden="true">
                ${badges
                  .map(
                    (badge) => `
                      <b class="path-stage-node-badge ${escapeHtml(badge.tone)}">${escapeHtml(badge.label)}</b>`
                  )
                  .join("")}
              </span>`;
}

function pathStageNodeEchoEvents(lane, node) {
  if (!lane || !node || node.kind === "future" || node.status === "future") return [];
  return pathNodeRelatedEvents(lane, node, 3);
}

function renderPathStageNodeEchoes(lane, node) {
  const events = pathStageNodeEchoEvents(lane, node);
  if (!events.length) return "";
  return `
              <span class="path-stage-node-echoes" aria-label="${formatNumber(events.length)} related path events">
                ${events
                  .map((item, index) => {
                    const tone = pathEventGlyphType(item);
                    const label = stateLabel(tone);
                    const title = compactText(item?.title ?? item?.summary ?? item?.status ?? label, 54);
                    return `<b class="path-stage-node-echo ${escapeHtml(tone)}" style="--path-stage-echo-index:${index};" title="${escapeHtml(label)}: ${escapeHtml(title)}"><i>${escapeHtml(label.slice(0, 3))}</i></b>`;
                  })
                  .join("")}
              </span>`;
}

function pathStageExpansionSocketModel(lane, focusedNode, hidden) {
  const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const taskCount = (lane.counts?.activeTasks ?? 0) + (lane.recentTasks?.length ?? 0);
  const proofCount = (lane.counts?.artifacts ?? 0) + (lane.counts?.traces ?? 0) + (lane.counts?.outcomes ?? 0);
  const eventCount = pathStageNodeEchoEvents(lane, focusedNode).length;
  const hasTrailSeed = eventCount || (lane.trail?.length ?? 0) ? 1 : 0;
  const openCount = hidden + Math.max(1, hasTrailSeed);
  return [
    { id: "gate", tone: gateCount ? "gate" : "future", label: "gate", value: gateCount ? formatNumber(gateCount) : "open", note: "blockers and approvals" },
    { id: "test", tone: taskCount ? "task" : "future", label: "test", value: taskCount ? formatNumber(taskCount) : "seed", note: "active work forks" },
    { id: "proof", tone: proofCount ? "proof" : "future", label: "proof", value: proofCount ? formatNumber(proofCount) : "slot", note: "evidence and outcomes" },
    { id: "next", tone: "future", label: "next", value: hidden ? `+${formatNumber(hidden)}` : formatNumber(openCount), note: "future expansion socket" },
  ];
}

function renderPathStageExpansionSockets(lane, focusedNode, hidden) {
  const sockets = pathStageExpansionSocketModel(lane, focusedNode, hidden);
  return `
      <span class="path-stage-expansion-sockets" aria-label="Path expansion sockets">
        ${sockets
          .map(
            (socket, index) => `
              <b class="path-stage-expansion-socket ${escapeHtml(socket.tone)}" style="--path-stage-expansion-index:${index};" title="${escapeHtml(socket.label)}: ${escapeHtml(socket.note)}">
                <i>${escapeHtml(socket.value)}</i>
                <span>${escapeHtml(socket.label)}</span>
              </b>`
          )
          .join("")}
      </span>`;
}

function pathStageInfiniteDepthLayers(lane, trail, nodes, focusedNode, pathProgress, mapStats, pathNotes) {
  const routeDepth = mapStats.find((stat) => stat.label === "route depth")?.value ?? formatNumber(trail.length);
  const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const testCount = (lane.counts?.activeTasks ?? 0) + (lane.recentTasks?.length ?? 0) + trail.filter((event) => event.kind === "task").length;
  const proofCount = (lane.counts?.artifacts ?? 0) + (lane.counts?.traces ?? 0) + (lane.counts?.outcomes ?? 0);
  const liveNodes = nodes.filter((node) => node.status === "active" || node.status === "ready" || node.status === "unlocked").length;
  const nextAction = compactText(chronicleNextAction(lane), 38);
  const nextNote = compactText(pathNotes[0]?.note?.summary ?? focusedNode?.meta ?? pathMapStatus(lane).label, 42);

  return [
    {
      id: "happened",
      tone: "happened",
      label: "Happened",
      value: routeDepth,
      title: compactText(focusedNode?.title ?? lane.name, 34),
      note: `${formatNumber(trail.length)} path events discovered`,
    },
    {
      id: "blocker",
      tone: gateCount ? "blocker" : "clear",
      label: "Blocker",
      value: gateCount ? formatNumber(gateCount) : "clear",
      title: gateCount ? "Gate pressure" : "No hard gate",
      note: gateCount ? "approval, risk, or missing input" : `${formatNumber(pathProgress)}% mapped`,
    },
    {
      id: "tests",
      tone: testCount ? "tests" : "seed",
      label: "Tests",
      value: testCount ? formatNumber(testCount) : "seed",
      title: lane.visual?.minigame?.name ?? "Experiment fork",
      note: testCount ? "active trials and task forks" : "ready for a lane minigame",
    },
    {
      id: "proof",
      tone: proofCount ? "proof" : "empty",
      label: "Proof",
      value: proofCount ? formatNumber(proofCount) : "slot",
      title: proofCount ? "Evidence attached" : "Proof socket",
      note: `${formatNumber(Math.max(proofCount, liveNodes))} signals can unlock`,
    },
    {
      id: "next",
      tone: liveNodes ? "next" : "future",
      label: "Next",
      value: liveNodes ? formatNumber(liveNodes) : "+1",
      title: nextAction,
      note: nextNote,
    },
  ];
}

function renderPathStageInfiniteDepthStack(lane, trail, nodes, focusedNode, pathProgress, mapStats, pathNotes) {
  const layers = pathStageInfiniteDepthLayers(lane, trail, nodes, focusedNode, pathProgress, mapStats, pathNotes);
  return `
        <aside class="path-stage-infinite-depth-stack" aria-label="Path infinite depth stack" style="--path-depth-progress:${pathProgress}%; --path-depth-count:${layers.length};">
          ${layers
            .map(
              (layer, index) => `
                <span class="path-stage-depth-layer ${escapeHtml(layer.tone)}" data-path-depth-layer="${escapeHtml(layer.id)}" style="--path-depth-index:${index};" title="${escapeHtml(layer.label)}: ${escapeHtml(layer.note)}">
                  <i>${escapeHtml(layer.label)}</i>
                  <strong>${escapeHtml(compactText(layer.value, 12))}</strong>
                  <em>${escapeHtml(compactText(layer.title, 28))}</em>
                  <b>${escapeHtml(compactText(layer.note, 36))}</b>
                </span>`
            )
            .join("")}
        </aside>`;
}
function renderPathStageRibbon(lane, nodes, focusedNode, pathProgress) {
  const visibleNodes = nodes.slice(0, 8);
  const hidden = Math.max(0, nodes.length - visibleNodes.length);
  const focusedIndex = Math.max(0, visibleNodes.findIndex((node) => node.id === focusedNode?.id));
  return `
    <section class="path-stage-ribbon" aria-label="Path stage ribbon" style="${laneStyle(lane)} --path-stage-art:url('./assets/system/path-stage-hud-strip-20260618.png'); --path-progress:${pathProgress}%; --path-stage-progress:${pathProgress}%; --path-stage-count:${visibleNodes.length + 1}; --path-stage-active:${focusedIndex};">
      <span class="path-stage-motion" aria-hidden="true">
        <span class="path-stage-motion-scan"></span>
        <span class="path-stage-motion-runner"></span>
      </span>
      <span class="path-stage-progress" aria-hidden="true"></span>
      ${renderPathStageCrewSprites(lane, pathProgress)}
      ${visibleNodes
        .map((node, index) => {
          const active = node.id === focusedNode?.id;
          const stageCharge = Math.min(100, 28 + index * 8 + (node.status === "complete" || node.status === "unlocked" ? 28 : node.status === "active" || active ? 18 : 0));
          return `
            <button class="path-stage-node ${escapeHtml(node.kind)} ${escapeHtml(node.status)} ${active ? "is-focused" : ""}" type="button" data-path-node-focus="${escapeHtml(node.id)}" data-stage-kind="${escapeHtml(node.kind)}" data-stage-status="${escapeHtml(node.status)}" aria-pressed="${active ? "true" : "false"}" style="--stage-index:${index}; --stage-charge:${stageCharge}%;" title="Focus ${escapeHtml(node.title)}">
              <span class="path-stage-node-frame" aria-hidden="true"></span>
              <span class="path-stage-node-spark" aria-hidden="true"></span>
              <i>${formatNumber(index + 1)}</i>
              <em class="path-stage-node-status">${escapeHtml(stateLabel(node.status))}</em>
              ${renderPathStageNodeBadges(node)}
              ${renderPathStageNodeEchoes(lane, node)}
              <span>${escapeHtml(stateLabel(node.kind))}</span>
              <strong>${escapeHtml(compactText(node.title, 26))}</strong>
              <small class="path-stage-node-meter">${escapeHtml(stateLabel(node.kind))}</small>
            </button>`;
        })
        .join("")}
      <article class="path-stage-node future" data-stage-kind="future" data-stage-status="future" style="--stage-index:${visibleNodes.length}; --stage-charge:18%;">
        <span class="path-stage-node-frame" aria-hidden="true"></span>
        <span class="path-stage-node-spark" aria-hidden="true"></span>
        <i>${hidden ? `+${formatNumber(hidden)}` : formatNumber(visibleNodes.length + 1)}</i>
        <em class="path-stage-node-status">locked</em>
        ${renderPathStageNodeBadges({ kind: "future", status: "future" })}
        <span>future</span>
        <strong>${hidden ? "More stages" : "Next slot"}</strong>
        <small class="path-stage-node-meter">socket</small>
      </article>
      ${renderPathStageExpansionSockets(lane, focusedNode, hidden)}
      ${renderPathStageFocusLens(lane, focusedNode, pathProgress)}
    </section>`;
}

function pathCoreDeckModules(lane, trail, nodes, focusedNode, mapStats, pathProgress, pathNotes) {
  const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  return [
    {
      id: "scan",
      label: "Scan",
      note: gateCount ? `${formatNumber(gateCount)} gates` : `${formatNumber(pathProgress)}% route`,
      tone: gateCount ? "gated" : "advancing",
      content: () => renderPathMissionScan(lane, trail, nodes, focusedNode, mapStats, pathProgress),
    },
    {
      id: "command",
      label: "Command",
      note: compactText(chronicleNextAction(lane), 34),
      tone: state.stagedDispatches.some((draft) => draft.laneId === lane.id || draft.sourceId === bestLaneDispatchSuggestion(lane).id) ? "unlocked" : "advancing",
      content: () => renderPathCommandStrip(lane, trail, focusedNode, pathNotes),
    },
    {
      id: "route",
      label: "Route",
      note: `${formatNumber(nodes.length)} nodes`,
      tone: focusedNode?.status ?? "scouting",
      content: () => renderPathRouteRail(lane, nodes, focusedNode),
    },
  ];
}

function pathCoreMotionMeta(modules, activeModule) {
  const activeIndex = Math.max(0, modules.findIndex((module) => module.id === activeModule.id));
  const maxIndex = Math.max(1, modules.length - 1);
  return {
    activeIndex,
    progress: Math.round((activeIndex / maxIndex) * 100),
    beacons: modules.map((module, index) => ({
      id: module.id,
      label: module.label,
      tone: module.tone,
      index,
      active: module.id === activeModule.id,
    })),
  };
}

function pathCoreLiveTokens(lane, trail, nodes, pathNotes) {
  const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount = (lane.counts?.artifacts ?? 0) + (lane.counts?.traces ?? 0) + (lane.counts?.outcomes ?? 0);
  const workCount = (lane.counts?.activeTasks ?? 0) + state.stagedDispatches.filter((draft) => draft.laneId === lane.id).length;
  const freshTrail = trail.filter((event) => event.kind === "trace" || event.kind === "evidence" || event.kind === "outcome").length;
  const activeNodes = nodes.filter((node) => node.status === "active" || node.status === "ready" || node.status === "unlocked").length;
  const tokens = [];

  if (gateCount) {
    tokens.push({
      id: "blockers",
      kind: "blocker",
      label: "Gate",
      value: gateCount,
      title: `${formatNumber(gateCount)} blockers or requests need attention`,
    });
  }

  if (proofCount || freshTrail) {
    const value = Math.max(proofCount, freshTrail);
    tokens.push({
      id: "proof",
      kind: "proof",
      label: "Proof",
      value,
      title: `${formatNumber(value)} proof signals are attached to this path`,
    });
  }

  if (workCount || activeNodes) {
    const value = Math.max(workCount, activeNodes);
    tokens.push({
      id: "work",
      kind: "work",
      label: "Work",
      value,
      title: `${formatNumber(value)} active work signals are moving through this path`,
    });
  }

  if (pathNotes.length) {
    tokens.push({
      id: "notes",
      kind: "work",
      label: "Notes",
      value: pathNotes.length,
      title: `${formatNumber(pathNotes.length)} operator notes are attached to this path`,
    });
  }

  if (!tokens.length) {
    tokens.push({
      id: "seed",
      kind: "work",
      label: "Seed",
      value: 1,
      title: "First path signal is ready for expansion",
    });
  }

  return tokens.slice(0, 4);
}

function pathStageWeatherSignals(lane, trail, nodes, pathNotes) {
  const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount =
    (lane.counts?.artifacts ?? 0) +
    (lane.counts?.traces ?? 0) +
    (lane.counts?.outcomes ?? 0) +
    trail.filter((event) => event.kind === "trace" || event.kind === "evidence" || event.kind === "outcome").length;
  const workCount =
    (lane.counts?.activeTasks ?? 0) +
    state.stagedDispatches.filter((draft) => draft.laneId === lane.id).length +
    nodes.filter((node) => node.status === "active" || node.status === "ready" || node.status === "unlocked").length;
  const noteCount = pathNotes.length;
  const groups = [
    { id: "gate", kind: "gate", label: "Gate", value: gateCount },
    { id: "proof", kind: "proof", label: "Proof", value: proofCount },
    { id: "work", kind: "work", label: "Work", value: workCount },
    { id: "note", kind: "note", label: "Note", value: noteCount },
  ].filter((group) => group.value > 0);
  const activeGroups = groups.length ? groups : [{ id: "seed", kind: "work", label: "Seed", value: 1 }];
  const signals = [];

  activeGroups.forEach((group, groupIndex) => {
    const copies = Math.min(3, Math.max(1, Math.ceil(Math.log2(group.value + 1))));
    for (let copy = 0; copy < copies; copy += 1) {
      const signalIndex = signals.length;
      signals.push({
        ...group,
        id: `${group.id}-${copy}`,
        x: 8 + ((signalIndex * 23 + groupIndex * 17 + copy * 11) % 84),
        y: 10 + ((signalIndex * 29 + groupIndex * 13 + copy * 7) % 74),
        size: 17 + ((group.value + signalIndex + copy) % 9),
        delay: -0.42 * signalIndex,
      });
    }
  });

  return signals.slice(0, 9);
}

function renderPathStageSignalWeather(lane, trail, nodes, pathNotes) {
  const signals = pathStageWeatherSignals(lane, trail, nodes, pathNotes);
  return `
    <div class="path-stage-weather" aria-hidden="true">
      ${signals
        .map(
          (signal, index) => `
            <span class="path-stage-signal ${escapeHtml(signal.kind)}" style="--weather-x:${signal.x}%; --weather-y:${signal.y}%; --weather-size:${signal.size}px; --weather-delay:${signal.delay}s; --weather-index:${index};">
              <i></i>
              <em>${escapeHtml(signal.label)}</em>
            </span>`
        )
        .join("")}
    </div>`;
}

function renderPathStageNavDock(pathProgress) {
  const views = [
    { id: "overview", label: "OVR", title: "Open overview" },
    { id: "path", label: "MAP", title: "Stay on Path Map" },
    { id: "chronicle", label: "LOG", title: "Open chronicle" },
    { id: "trail", label: "TRL", title: "Open full trail" },
    { id: "game", label: "PLAY", title: "Open game module" },
    { id: "comms", label: "COM", title: "Open command deck" },
  ];
  return `
    <nav class="path-stage-nav-dock" aria-label="Path cockpit navigation">
      <span class="path-stage-nav-meter">
        <strong>${formatNumber(pathProgress)}%</strong>
        <em>map</em>
      </span>
      ${views
        .map(
          (view) => `
            <button class="path-stage-nav-button ${view.id === "path" ? "active" : ""}" type="button" data-detail-view="${escapeHtml(view.id)}" title="${escapeHtml(view.title)}" aria-current="${view.id === "path" ? "page" : "false"}">${escapeHtml(view.label)}</button>`
        )
        .join("")}
    </nav>`;
}

function pathCoreSnapshotItems(lane, trail, nodes, focusedNode, pathNotes) {
  const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount = (lane.counts?.artifacts ?? 0) + (lane.counts?.traces ?? 0) + (lane.counts?.outcomes ?? 0);
  const workCount = (lane.counts?.activeTasks ?? 0) + (lane.counts?.queuedTasks ?? 0);
  return [
    {
      label: gateCount ? "Gate Lock" : "Route",
      value: gateCount ? formatNumber(gateCount) : `${formatNumber(nodes.length)}N`,
      note: gateCount ? compactText(lane.gateMap?.[0]?.nextAction ?? "Needs review", 44) : compactText(focusedNode?.title ?? "Mapped", 44),
      tone: gateCount ? "gated" : "ready",
    },
    {
      label: "Proof",
      value: formatNumber(proofCount),
      note: compactText(trail.find((event) => event.kind === "evidence" || event.kind === "trace")?.title ?? "Evidence trail", 44),
      tone: proofCount ? "unlocked" : "scouting",
    },
    {
      label: workCount ? "Work" : "Notes",
      value: formatNumber(workCount || pathNotes.length || 1),
      note: compactText(chronicleNextAction(lane), 48),
      tone: workCount ? "advancing" : pathNotes.length ? "ready" : "scouting",
    },
  ];
}

function renderPathCoreSnapshot(lane, modules, activeModule, liveTokens, trail, nodes, focusedNode, mapStats, pathProgress, pathNotes) {
  const activeIndex = Math.max(0, modules.findIndex((module) => module.id === activeModule.id));
  const items = pathCoreSnapshotItems(lane, trail, nodes, focusedNode, pathNotes);
  const activeTitle =
    activeModule.id === "scan"
      ? focusedNode?.title ?? lane.visual?.realm ?? "Lane scan"
      : activeModule.id === "command"
        ? chronicleNextAction(lane)
        : focusedNode?.title ?? `${formatNumber(nodes.length)} route nodes`;
  const activeNote =
    activeModule.id === "scan"
      ? `${formatNumber(trail.length)} records / ${formatNumber(pathNotes.length)} notes`
      : activeModule.id === "command"
        ? `${formatNumber(lane.counts?.activeTasks ?? 0)} active tasks / ${formatNumber(liveTokens.length)} signals`
        : `${formatNumber(nodes.length)} nodes / ${formatNumber(pathProgress)}% mapped`;
  return `
    <section class="path-core-snapshot ${escapeHtml(activeModule.tone)}" data-path-core-snapshot="${escapeHtml(activeModule.id)}" style="--path-core-snapshot-index:${activeIndex}; --path-core-snapshot-progress:${pathProgress}%;" aria-label="Compact path core snapshot">
      <div class="path-core-snapshot-head">
        <span>${escapeHtml(activeModule.label)} Core</span>
        <strong>${escapeHtml(compactText(activeTitle, 74))}</strong>
        <em>${escapeHtml(activeNote)}</em>
      </div>
      <div class="path-core-snapshot-arc" aria-hidden="true">
        <i></i>
        <b></b>
        <span>${escapeHtml(mapStats[1]?.value ?? `${formatNumber(pathProgress)}%`)}</span>
      </div>
      <div class="path-core-snapshot-grid">
        ${items
          .map(
            (item, index) => `
              <span class="path-core-snapshot-card ${escapeHtml(item.tone)}" style="--path-core-snapshot-card:${index};">
                <strong>${escapeHtml(item.value)}</strong>
                <em>${escapeHtml(item.label)}</em>
                <small>${escapeHtml(item.note)}</small>
              </span>`
          )
          .join("")}
      </div>
      <div class="path-core-snapshot-actions" aria-label="Core snapshot actions">
        <button class="tool-button" type="button" data-path-glance-jump="route" title="Open route rail">ROUTE</button>
        <button class="tool-button" type="button" data-path-glance-jump="proof" title="Open proof cache">PROOF</button>
        <button class="tool-button primary" type="button" data-detail-view="comms" title="Open command deck">COM</button>
      </div>
    </section>`;
}

function renderPathCoreDeck(lane, trail, nodes, focusedNode, mapStats, pathProgress, pathNotes) {
  const modules = pathCoreDeckModules(lane, trail, nodes, focusedNode, mapStats, pathProgress, pathNotes);
  const activeId = pathCoreDeckView(lane);
  const activeModule = modules.find((module) => module.id === activeId) ?? modules[0];
  const motion = pathCoreMotionMeta(modules, activeModule);
  const liveTokens = pathCoreLiveTokens(lane, trail, nodes, pathNotes);
  const questScanner = pathStageQuestScannerModel(lane, trail, nodes, focusedNode, pathNotes, pathProgress);
  return `
    <section class="path-core-deck" aria-label="Path core deck" style="${laneStyle(lane)} --path-core-index:${motion.activeIndex}; --path-core-progress:${motion.progress}%; --path-core-live-count:${liveTokens.length};" data-path-core-active="${escapeHtml(activeModule.id)}">
      <div class="path-core-tabs" role="tablist" aria-label="Path core modules">
        ${modules
          .map(
            (module) => `
              <button class="path-core-tab ${module.id === activeModule.id ? "active" : ""} ${escapeHtml(module.tone)}" type="button" role="tab" aria-selected="${module.id === activeModule.id ? "true" : "false"}" data-path-core-view="${escapeHtml(module.id)}" data-path-core-lane="${escapeHtml(lane.id)}" title="Open ${escapeHtml(module.label)} core module">
                <strong>${escapeHtml(module.label)}</strong>
                <span>${escapeHtml(module.note)}</span>
              </button>`
          )
          .join("")}
      </div>
      <div class="path-core-motion-rail" aria-hidden="true">
        <span class="path-core-motion-track"></span>
        <span class="path-core-motion-sweep"></span>
        <span class="path-core-motion-runner"></span>
        ${liveTokens.map(
            (token, index) => `
              <span class="path-core-live-token ${escapeHtml(token.kind)}" data-path-core-live-token="${escapeHtml(token.id)}" style="--path-core-live-index:${index};" title="${escapeHtml(token.title)}">
                <i>${formatNumber(token.value)}</i>
                <em>${escapeHtml(token.label)}</em>
              </span>`
          ).join("")}
        ${motion.beacons
          .map(
            (beacon) => `
              <span class="path-core-beacon ${beacon.active ? "active" : ""} ${escapeHtml(beacon.tone)}" style="--path-core-beacon-index:${beacon.index};" data-path-core-beacon="${escapeHtml(beacon.id)}">
                <i></i>
                <em>${escapeHtml(beacon.label)}</em>
              </span>`
          )
          .join("")}
      </div>
      ${renderPathStageQuestScanner(questScanner)}
      <div class="path-core-panel" role="tabpanel">
        ${renderPathCoreSnapshot(lane, modules, activeModule, liveTokens, trail, nodes, focusedNode, mapStats, pathProgress, pathNotes)}
      </div>
    </section>`;
}

function pathStageRealmCartridgeModel(lane, pathProgress, gateCount) {
  const visual = lane.visual ?? {};
  const minigame = visual.minigame ?? {};
  const definition = minigameDefinition(lane);
  const stageCount = definition?.count?.(lane) ?? lane.quest?.checkpoints?.length ?? 0;
  const texture = minigame.texture ?? visual.avatar ?? "";
  const ready = Boolean(minigame.id && texture);
  return {
    id: minigame.id ?? lane.id,
    title: minigame.title ?? visual.realm ?? lane.name,
    realm: visual.realm ?? lane.department ?? lane.name,
    mechanic: minigame.mechanic ?? visual.mood ?? lane.quest?.title ?? "Lane game seed",
    texture,
    status: gateCount ? "gated" : ready ? "ready" : "seed",
    badge: ready ? "GAME" : "SEED",
    stageCount,
    charge: Math.max(8, Math.min(100, Math.round(pathProgress) + Math.min(24, stageCount * 3))),
  };
}

function renderPathStageRealmCartridge(lane, pathProgress, gateCount) {
  const model = pathStageRealmCartridgeModel(lane, pathProgress, gateCount);
  const artStyle = model.texture ? `--path-realm-art:url('${escapeHtml(model.texture)}');` : "";
  return `
        <button class="path-stage-realm-cartridge ${escapeHtml(model.status)}" type="button" data-detail-view="game" data-path-stage-realm="${escapeHtml(model.id)}" style="${artStyle} --path-realm-charge:${model.charge}%;" title="Open ${escapeHtml(model.title)} game module">
          <span class="path-stage-realm-thumb" aria-hidden="true"></span>
          <span class="path-stage-realm-copy">
            <i>${escapeHtml(model.badge)}</i>
            <strong>${escapeHtml(compactText(model.title, 24))}</strong>
            <em>${escapeHtml(compactText(model.realm, 28))}</em>
          </span>
          <b>${formatNumber(model.stageCount)}</b>
        </button>`;
}
function pathStageDepthView(lane) {
  const stored = state.pathStageDepthByLane[lane.id];
  const validViews = new Set(["stage", "archive", "utility"]);
  if (validViews.has(stored)) return stored;
  return "stage";
}

function renderPathStageDepthDock(lane, trail, pathNotes, gateCount, depthView, pathProgress) {
  const chapters = pathChapterArchiveItems(trail);
  const activeUtility = pathUtilityDockView(lane);
  const proofCount = pathProofItems(lane).length;
  const cards = [
    {
      id: "stage",
      label: "Stage",
      value: `${formatNumber(pathProgress)}%`,
      note: "cockpit only",
      tone: "ready",
    },
    {
      id: "archive",
      label: "Archive",
      value: formatNumber(chapters.length),
      note: `${formatNumber(trail.length)} records`,
      tone: chapters.length ? "advancing" : "scouting",
    },
    {
      id: "utility",
      label: "Tools",
      value: formatNumber(gateCount + proofCount + pathNotes.length),
      note: `${stateLabel(activeUtility)} dock`,
      tone: gateCount ? "gated" : proofCount ? "unlocked" : "ready",
    },
  ];

  return `
    <section class="path-stage-depth-dock" aria-label="Path stage depth dock" data-path-stage-depth-active="${escapeHtml(depthView)}">
      <div>
        <p class="eyebrow">Stage Depth</p>
        <h3>${depthView === "stage" ? "One-screen cockpit" : depthView === "archive" ? "Archive open" : "Tools open"}</h3>
      </div>
      <div class="path-stage-depth-cards" role="tablist" aria-label="Path depth modes">
        ${cards
          .map(
            (card) => `
              <button class="path-stage-depth-card ${card.id === depthView ? "active" : ""} ${escapeHtml(card.tone)}" type="button" role="tab" aria-selected="${card.id === depthView ? "true" : "false"}" data-path-stage-depth="${escapeHtml(card.id)}" data-path-stage-depth-lane="${escapeHtml(lane.id)}" title="Open ${escapeHtml(card.label)} depth">
                <span>${escapeHtml(card.label)}</span>
                <strong>${escapeHtml(card.value)}</strong>
                <em>${escapeHtml(card.note)}</em>
              </button>`
          )
          .join("")}
      </div>
    </section>`;
}

function pathStageChapterRadarModel(lane, trail) {
  const chapters = pathChapterArchiveItems(trail);
  const focused = focusedPathChapter(lane, chapters);
  const visible = chapters.slice(0, 6);
  const totalRecords = chapters.reduce((sum, chapter) => sum + chapter.items.length, 0);
  const hidden = Math.max(0, chapters.length - visible.length);
  return {
    lane,
    chapters,
    focused,
    hidden,
    totalRecords,
    items: visible.map((chapter, index) => {
      const active = focused?.key === chapter.key;
      const gates = (chapter.counts.gate ?? 0) + (chapter.counts.service ?? 0);
      const proofs = chapter.counts.proof ?? 0;
      return {
        key: chapter.key,
        label: chapter.label,
        index,
        active,
        tone: pathChapterTone(chapter),
        count: chapter.items.length,
        gates,
        proofs,
        charge: Math.max(8, Math.min(100, Math.round((chapter.items.length / Math.max(totalRecords, 1)) * 280))),
      };
    }),
  };
}

function renderPathStageChapterRadar(model) {
  const { lane, chapters, focused, hidden, totalRecords, items } = model;
  return `
    <section class="path-stage-chapter-radar ${escapeHtml(focused ? pathChapterTone(focused) : "scouting")}" aria-label="Path chapter radar" style="--path-chapter-radar-count:${Math.max(1, items.length)};">
      <div class="path-stage-chapter-radar-head">
        <span>Chapter Radar</span>
        <strong>${formatNumber(chapters.length)} levels</strong>
        <em>${formatNumber(totalRecords)} records</em>
      </div>
      <div class="path-stage-chapter-rail">
        ${
          items
            .map(
              (item) => `
                <button class="path-stage-chapter-node ${escapeHtml(item.tone)} ${item.active ? "active" : ""}" type="button" data-path-stage-chapter-focus="${escapeHtml(item.key)}" data-path-stage-chapter-lane="${escapeHtml(lane.id)}" aria-pressed="${item.active ? "true" : "false"}" style="--path-chapter-charge:${item.charge}%; --path-chapter-index:${item.index};" title="Open ${escapeHtml(item.label)} chapter archive">
                  <i>${formatNumber(item.index + 1)}</i>
                  <span>
                    <strong>${escapeHtml(item.label)}</strong>
                    <em>${formatNumber(item.count)} rec / ${formatNumber(item.proofs)} proof / ${formatNumber(item.gates)} gate</em>
                  </span>
                </button>`
            )
            .join("") ||
          `<span class="path-stage-chapter-empty"><strong>No chapters</strong><em>History levels appear as the lane records events.</em></span>`
        }
        ${hidden ? `<span class="path-stage-chapter-more">+${formatNumber(hidden)}</span>` : ""}
      </div>
    </section>`;
}

function pathChapterBossBarModel(lane, trail, pathProgress) {
  const chapters = pathChapterArchiveItems(trail);
  const focused = focusedPathChapter(lane, chapters);
  const focusCounts = focused?.counts ?? {};
  const nextRecord = focused?.items?.[0] ?? trail[0];
  const gateCount = (focusCounts.gate ?? 0) + (focusCounts.service ?? 0);
  const proofCount = focusCounts.proof ?? 0;
  const unlockCount = focusCounts.outcome ?? 0;
  const taskCount = focusCounts.task ?? 0;
  const selectedIndex = Math.max(0, chapters.findIndex((chapter) => chapter.key === focused?.key));
  const totalRecords = chapters.reduce((sum, chapter) => sum + chapter.items.length, 0);
  const bossCharge = focused ? Math.max(12, Math.min(100, Math.round((focused.items.length / Math.max(1, totalRecords)) * 300))) : Math.max(8, pathProgress);
  const tone = gateCount ? "gated" : unlockCount ? "unlocked" : proofCount ? "proof" : focused ? pathChapterTone(focused) : "scouting";
  const cells = [
    {
      id: "chapter",
      label: "Chapter",
      value: focused ? `${formatNumber(selectedIndex + 1)}/${formatNumber(Math.max(1, chapters.length))}` : "Seed",
      title: focused?.label ?? "No chapter yet",
      note: `${formatNumber(focused?.items.length ?? 0)} of ${formatNumber(totalRecords)} records`,
      tone: focused ? pathChapterTone(focused) : "scouting",
      charge: bossCharge,
      depth: "archive",
    },
    {
      id: "gate",
      label: "Gate",
      value: gateCount ? formatNumber(gateCount) : "clear",
      title: gateCount ? "Boss pressure" : "No chapter gate",
      note: gateCount ? "approval or blocker records" : `${formatNumber(pathProgress)}% route mapped`,
      tone: gateCount ? "gated" : "ready",
      charge: gateCount ? Math.min(100, 32 + gateCount * 18) : Math.max(18, pathProgress),
      depth: "archive",
    },
    {
      id: "proof",
      label: "Proof",
      value: proofCount ? formatNumber(proofCount) : "slot",
      title: proofCount ? "Proof captured" : "Proof socket",
      note: `${formatNumber(taskCount)} tasks in this level`,
      tone: proofCount ? "proof" : "scouting",
      charge: proofCount ? Math.min(100, 28 + proofCount * 16) : 18,
      depth: "archive",
    },
    {
      id: "unlock",
      label: "Unlock",
      value: unlockCount ? formatNumber(unlockCount) : "+1",
      title: unlockCount ? "Reward opened" : "Reward slot",
      note: `${formatNumber(focused?.counts.trace ?? 0)} trace sparks`,
      tone: unlockCount ? "unlocked" : "ready",
      charge: unlockCount ? Math.min(100, 38 + unlockCount * 20) : Math.max(16, bossCharge / 2),
      depth: "archive",
    },
    {
      id: "next",
      label: "Next",
      value: nextRecord ? stateLabel(pathEventGlyphType(nextRecord)).slice(0, 7) : "Queue",
      title: nextRecord?.title ?? chronicleNextAction(lane),
      note: nextRecord ? shortDate(nextRecord.time ?? nextRecord.createdAt) : "future chapter record",
      tone: gateCount ? "gated" : nextRecord ? "advancing" : "ready",
      charge: Math.max(18, Math.min(100, bossCharge + (nextRecord ? 8 : 0))),
      depth: "archive",
      view: "trail",
    },
  ];

  return { lane, focused, tone, bossCharge, cells };
}

function renderPathChapterBossBar(model) {
  return `
    <section class="path-chapter-boss-bar ${escapeHtml(model.tone)}" aria-label="Selected chapter boss bar" style="--path-chapter-boss-charge:${model.bossCharge}%;">
      <div class="path-chapter-boss-core">
        <span>Chapter Boss</span>
        <strong>${escapeHtml(compactText(model.focused?.label ?? "Future chapter", 28))}</strong>
        <em>${escapeHtml(model.focused ? `${formatNumber(model.focused.items.length)} route records` : "History level socket")}</em>
      </div>
      ${model.cells
        .map(
          (cell, index) => `
            <button
              class="path-chapter-boss-cell ${escapeHtml(cell.tone)}"
              type="button"
              data-path-chapter-boss-cell="${escapeHtml(cell.id)}"
              data-path-stage-depth="archive"
              data-path-stage-depth-lane="${escapeHtml(model.lane.id)}"
              ${cell.view ? `data-detail-view="trail"` : ""}
              style="--path-boss-cell-charge:${Math.max(8, Math.min(100, cell.charge))}%; --path-boss-cell-index:${index};"
              title="${escapeHtml(cell.label)}: ${escapeHtml(cell.title)}"
            >
              <i aria-hidden="true"></i>
              <span>${escapeHtml(cell.label)}</span>
              <strong>${escapeHtml(compactText(cell.value, 12))}</strong>
              <em>${escapeHtml(compactText(cell.title, 30))}</em>
              <b>${escapeHtml(compactText(cell.note, 36))}</b>
            </button>`
        )
        .join("")}
    </section>`;
}
function pathStageQuestScannerModel(lane, trail, nodes, focusedNode, pathNotes, pathProgress) {
  const latest = trail[0];
  const gate = lane.gateMap?.[0] ?? lane.serviceRequests?.find((request) => request.status === "needs_review") ?? lane.serviceRequests?.[0];
  const proofCount = pathProofItems(lane).length + trail.filter((event) => event.kind === "evidence" || event.kind === "trace" || event.kind === "outcome").length;
  const workCount = (lane.counts?.activeTasks ?? 0) + (lane.counts?.queuedTasks ?? 0) + nodes.filter((node) => node.status === "active" || node.status === "ready").length;
  const nextAction = chronicleNextAction(lane);
  const gateTitle = gate?.workerType ?? gate?.type ?? gate?.id ?? "Gate clear";
  const gateBody = gate?.nextAction ?? gate?.requestedAction ?? gate?.gate ?? gate?.riskGate ?? "No active blocker in this lane.";
  const minigame = lane.visual?.minigame ?? {};
  const testCount =
    (lane.counts?.activeTasks ?? 0) +
    (lane.recentTasks?.length ?? 0) +
    trail.filter((event) => pathEventGlyphType(event) === "task").length;
  const experimentTitle = minigame.title ?? lane.quest?.title ?? "Experiment forks";
  const experimentMeta = minigame.mechanic ?? `${formatNumber(testCount)} live tests / future sockets primed`;
  const owner = laneAgents(lane)[0];
  const suggestion = bestLaneDispatchSuggestion(lane);
  const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id || draft.sourceId === suggestion.id);
  const botName = owner?.visual?.callsign ?? owner?.name ?? lane.ownerAgentId ?? "Lane bot";
  const botSpecialty = owner?.visual?.specialty ?? suggestion.label ?? "local command";
  const cells = [
    {
      id: "happened",
      label: "Happened",
      value: latest ? stateLabel(latest.kind ?? latest.type ?? "event") : "Seed",
      title: latest?.title ?? focusedNode?.title ?? "Awaiting first recorded move",
      meta: latest ? shortDate(latest.time ?? latest.createdAt) : `${formatNumber(pathProgress)}% mapped`,
      tone: latest ? "advancing" : "scouting",
    },
    {
      id: "blocker",
      label: "Blocker",
      value: gate ? "Locked" : "Clear",
      title: gateTitle,
      meta: gateBody,
      tone: gate ? "gated" : "unlocked",
    },
    {
      id: "proof",
      label: "Proof",
      value: formatNumber(proofCount),
      title: proofCount ? "Signals captured" : "Proof needed",
      meta: `${formatNumber(lane.counts?.artifacts ?? 0)} artifacts / ${formatNumber(pathNotes.length)} notes`,
      tone: proofCount ? "unlocked" : "scouting",
    },
    {
      id: "tests",
      label: "Tests",
      value: testCount ? formatNumber(testCount) : minigame.id ? "Seed" : "Open",
      title: experimentTitle,
      meta: experimentMeta,
      tone: testCount ? "advancing" : minigame.id ? "ready" : "scouting",
    },
    {
      id: "bot",
      label: "Bot",
      value: staged ? "Queued" : "Live",
      title: botName,
      meta: staged ? "local draft staged" : botSpecialty,
      tone: staged ? "unlocked" : gate ? "gated" : "advancing",
    },
    {
      id: "next",
      label: "Next",
      value: workCount ? `${formatNumber(workCount)} live` : "Queue",
      title: nextAction,
      meta: focusedNode?.meta ?? pathMapStatus(lane).label,
      tone: gate ? "gated" : workCount ? "advancing" : "ready",
    },
  ];

  return {
    tone: gate ? "gated" : proofCount ? "unlocked" : "advancing",
    progress: pathProgress,
    focus: compactText(focusedNode?.title ?? latest?.title ?? lane.name, 42),
    relay: {
      laneId: lane.id,
      lane,
      staged,
      owner,
      botName,
      specialty: botSpecialty,
      thread: lane.ownerThreadId ?? owner?.thread_id ?? "No thread",
      urgency: suggestion.urgency ?? 0,
    },
    cells,
  };
}

function renderPathStageQuestScanner(model) {
  return `
    <section class="path-stage-quest-scanner ${escapeHtml(model.tone)}" aria-label="Path quest scanner" style="--path-scanner-progress:${model.progress}%;">
      <span class="path-stage-quest-scanner-sweep" aria-hidden="true"></span>
      <div class="path-stage-quest-scanner-head">
        <span>Quest Scanner</span>
        <strong>${escapeHtml(model.focus)}</strong>
        <div class="path-stage-quest-scanner-relay ${model.relay.staged ? "staged" : ""}" aria-label="Path bot relay">
          ${model.relay.owner ? agentAvatarMarkup(model.relay.owner, model.relay.lane, "path-stage-quest-scanner-avatar") : `<span class="path-stage-quest-scanner-avatar">${escapeHtml(String(model.relay.botName).slice(0, 2).toUpperCase())}</span>`}
          <span>
            <b>${escapeHtml(compactText(model.relay.botName, 22))}</b>
            <em>${escapeHtml(compactText(model.relay.thread, 28))}</em>
          </span>
          <button class="tool-button" type="button" data-path-handoff-stage="${escapeHtml(model.relay.laneId)}" title="Stage local bot handoff">${model.relay.staged ? "OK" : "Q"}</button>
          <button class="tool-button primary" type="button" data-detail-view="comms" title="Open bot command room">COM</button>
        </div>
      </div>
      <div class="path-stage-quest-scanner-grid">
        ${model.cells
          .map(
            (cell, index) => `
              <span class="path-stage-quest-scan-cell ${escapeHtml(cell.tone)}" data-path-quest-scan="${escapeHtml(cell.id)}" style="--path-scanner-cell:${index};">
                <i>${escapeHtml(cell.label)}</i>
                <strong>${escapeHtml(compactText(cell.value, 18))}</strong>
                <em>${escapeHtml(compactText(cell.title, 36))}</em>
                <b>${escapeHtml(compactText(cell.meta, 34))}</b>
              </span>`
          )
          .join("")}
      </div>
    </section>`;
}

function renderPathMapView(lane) {
  const trail = chronicleTrail(lane);
  const limit = state.trailLimitByLane[lane.id] ?? 18;
  const visibleTrail = trail.slice(0, limit);
  const nodes = pathMapNodes(lane);
  const focusedNode = focusedPathNode(lane, nodes);
  const pathNotes = pathMapNoteItems(lane);
  const status = pathMapStatus(lane);
  const gateCount = lane.counts?.blockers ?? 0;
  const completeCheckpoints = (lane.quest?.checkpoints ?? []).filter((checkpoint) => checkpoint.status === "complete").length;
  const totalCheckpoints = lane.quest?.checkpoints?.length ?? 0;
  const pathProgress = totalCheckpoints ? Math.round((completeCheckpoints / totalCheckpoints) * 100) : lane.progress ?? 0;
  const mapStats = [
    { label: "route depth", value: formatNumber(trail.length) },
    { label: "checkpoints", value: `${formatNumber(completeCheckpoints)}/${formatNumber(totalCheckpoints)}` },
    { label: "gates", value: formatNumber(gateCount) },
    { label: "notes", value: formatNumber(pathNotes.length) },
    { label: "unlocks", value: formatNumber(lane.counts?.outcomes ?? 0) },
  ];
  const depthView = pathStageDepthView(lane);
  const chapterRadar = pathStageChapterRadarModel(lane, trail);
  const chapterBossBar = pathChapterBossBarModel(lane, trail, pathProgress);
  const visibleStageNodes = nodes.slice(0, 8);
  const focusedStageIndex = Math.max(0, visibleStageNodes.findIndex((node) => node.id === focusedNode?.id));
  const pathStageFocusX = Math.round(((focusedStageIndex + 0.5) / Math.max(1, visibleStageNodes.length + 1)) * 100);
  const questScanner = pathStageQuestScannerModel(lane, trail, nodes, focusedNode, pathNotes, pathProgress);

  return `
    <section class="detail-section path-viewport-section">
      <div class="lane-button-top path-viewport-header">
        <div>
          <p class="eyebrow">Path Map</p>
          <h3>${escapeHtml(status.label)}</h3>
        </div>
        <span class="badge ${escapeHtml(status.tone)}">${formatNumber(pathProgress)}% mapped</span>
      </div>
      <div class="path-map-board mission-stage" data-path-stage-depth-view="${escapeHtml(depthView)}" style="${laneStyle(lane)} --path-progress:${pathProgress}%; --path-stage-focus-x:${pathStageFocusX}%; --path-stage-atmosphere:url('./assets/system/path-stage-atmosphere-20260618.png'); --path-playfield-art:url('./assets/system/path-stage-playfield-rail-20260620.png')">
        ${renderPathStageNavDock(pathProgress)}

        ${renderPathStageSignalWeather(lane, trail, nodes, pathNotes)}

        ${renderPathMissionGlance(lane, trail, focusedNode, pathNotes, pathProgress)}

        ${renderPathStageRealmCartridge(lane, pathProgress, gateCount)}

        ${renderPathStageEncounterTether(focusedNode)}

        ${renderPathStageBotCommandBeacon(lane)}

        ${renderPathStageInfiniteDepthStack(lane, trail, nodes, focusedNode, pathProgress, mapStats, pathNotes)}

        <div class="path-stage-mobile-story-rail-shell">
          ${renderPathStageQuestScanner(questScanner)}
        </div>

        ${renderPathStageFocusLens(lane, focusedNode, pathProgress)}

        ${renderPathStageRibbon(lane, nodes, focusedNode, pathProgress)}

        ${renderPathStageChapterRadar(chapterRadar)}

        ${renderPathChapterBossBar(chapterBossBar)}

        ${renderPathCoreDeck(lane, trail, nodes, focusedNode, mapStats, pathProgress, pathNotes)}

        ${renderPathStageDepthDock(lane, trail, pathNotes, gateCount, depthView, pathProgress)}

        ${depthView === "archive" ? renderPathChapterArchive(lane, trail) : ""}

        ${depthView === "utility" ? renderPathUtilityDock(lane, focusedNode, nodes, pathNotes, visibleTrail, trail, gateCount) : ""}
      </div>
    </section>`;
}

function pathUtilityDockView(lane) {
  const stored = state.pathUtilityDockViewByLane[lane.id];
  const validViews = new Set(["radar", "intel", "proof", "replay", "handoff", "notes", "stream"]);
  if (validViews.has(stored)) return stored;
  if (lane.counts?.blockers || lane.serviceRequests?.length) return "radar";
  if (pathProofItems(lane).length) return "proof";
  return "replay";
}

function renderPathBlockerRadarCard(lane, gateCount) {
  return `
    <article class="path-brief-card path-blocker-radar-card">
      <p class="eyebrow">Blocker Radar</p>
      <h3>${gateCount ? `${formatNumber(gateCount)} gates need review` : "No active blocker cells"}</h3>
      <p>${escapeHtml(compactText(lane.gateMap?.[0]?.nextAction ?? lane.serviceRequests?.[0]?.requestedAction ?? "Route is clear for local-only proof work.", 190))}</p>
      <button class="tool-button" type="button" data-detail-view="comms" title="Open command deck">COM</button>
    </article>`;
}

function renderPathEventStreamCard(lane, visibleTrail, trail) {
  return `
    <article class="path-brief-card path-event-stream-card">
      <p class="eyebrow">Event Stream</p>
      <h3>${formatNumber(visibleTrail.length)} of ${formatNumber(trail.length)} visible</h3>
      <div class="path-mini-stream">
        ${visibleTrail.map(renderPathMiniEvent).join("") || `<span>No events yet</span>`}
      </div>
      ${
        visibleTrail.length < trail.length
          ? `<button class="expand-button" type="button" data-expand-trail="${escapeHtml(lane.id)}">Reveal ${Math.min(18, trail.length - visibleTrail.length)} more route events</button>`
          : `<p class="small-muted trail-end">Route map is caught up to this snapshot.</p>`
      }
    </article>`;
}

function pathUtilityDockModules(lane, focusedNode, nodes, pathNotes, visibleTrail, trail, gateCount) {
  const proofs = pathProofItems(lane);
  return [
    {
      id: "radar",
      label: "Radar",
      note: gateCount ? `${formatNumber(gateCount)} gates` : "clear",
      tone: gateCount ? "gated" : "ready",
      content: renderPathBlockerRadarCard(lane, gateCount),
    },
    {
      id: "intel",
      label: "Intel",
      note: focusedNode?.title ?? "node",
      tone: focusedNode?.status ?? "advancing",
      content: renderPathNodeIntel(lane, focusedNode, nodes),
    },
    {
      id: "proof",
      label: "Proof",
      note: `${formatNumber(proofs.length)} cards`,
      tone: proofs.length ? "unlocked" : "scouting",
      content: renderPathProofCache(lane),
    },
    {
      id: "replay",
      label: "Replay",
      note: `${formatNumber(pathReplayItems(lane).length)} stages`,
      tone: state.pathReplayPlayingLaneId === lane.id ? "advancing" : "scouting",
      content: renderPathRouteReplay(lane),
    },
    {
      id: "handoff",
      label: "Handoff",
      note: bestLaneDispatchSuggestion(lane).label ?? "queue",
      tone: state.stagedDispatches.some((draft) => draft.laneId === lane.id || draft.sourceId === bestLaneDispatchSuggestion(lane).id) ? "unlocked" : "advancing",
      content: renderPathHandoffPanel(lane, pathNotes),
    },
    {
      id: "notes",
      label: "Notes",
      note: `${formatNumber(pathNotes.length)} pins`,
      tone: pathNotes.length ? "noted" : "scouting",
      content: renderPathNotePanel(pathNotes),
    },
    {
      id: "stream",
      label: "Stream",
      note: `${formatNumber(visibleTrail.length)}/${formatNumber(trail.length)}`,
      tone: trail.length ? "advancing" : "scouting",
      content: renderPathEventStreamCard(lane, visibleTrail, trail),
    },
  ];
}

function pathUtilityMotionMeta(modules, activeModule) {
  const activeIndex = Math.max(0, modules.findIndex((module) => module.id === activeModule?.id));
  const count = Math.max(1, modules.length);
  const progress = count > 1 ? Math.round((activeIndex / (count - 1)) * 100) : 0;
  return { activeIndex, count, progress };
}

function renderPathUtilityDock(lane, focusedNode, nodes, pathNotes, visibleTrail, trail, gateCount) {
  const modules = pathUtilityDockModules(lane, focusedNode, nodes, pathNotes, visibleTrail, trail, gateCount);
  const activeId = pathUtilityDockView(lane);
  const activeModule = modules.find((module) => module.id === activeId) ?? modules[0];
  const motion = pathUtilityMotionMeta(modules, activeModule);
  return `
    <section class="path-utility-dock" aria-label="Path utility dock" data-path-utility-motion="${escapeHtml(activeModule.id)}" style="${laneStyle(lane)} --utility-active-index:${motion.activeIndex}; --utility-count:${motion.count}; --utility-progress:${motion.progress}%;">
      <div class="path-utility-head">
        <div>
          <p class="eyebrow">Path Utility Dock</p>
          <h3>${escapeHtml(activeModule.label)} Console</h3>
        </div>
        <span class="badge ${escapeHtml(activeModule.tone)}">${escapeHtml(compactText(activeModule.note, 28))}</span>
      </div>
      <div class="path-utility-tabs" role="tablist" aria-label="Path utility modules">
        ${modules
          .map(
            (module) => `
              <button class="path-utility-tab ${module.id === activeModule.id ? "active" : ""} ${escapeHtml(module.tone)}" type="button" role="tab" aria-selected="${module.id === activeModule.id ? "true" : "false"}" data-path-utility-view="${escapeHtml(module.id)}" data-path-utility-lane="${escapeHtml(lane.id)}" title="Open ${escapeHtml(module.label)} module">
                <strong>${escapeHtml(module.label)}</strong>
                <span>${escapeHtml(compactText(module.note, 32))}</span>
              </button>`
          )
          .join("")}
      </div>
      <div class="path-utility-motion" aria-label="Path utility motion selector">
        <span class="path-utility-runner"></span>
        <div class="path-utility-beacons">
          ${modules
            .map(
              (module, index) => `
                <button class="path-utility-beacon ${module.id === activeModule.id ? "active" : ""} ${escapeHtml(module.tone)}" type="button" tabindex="-1" data-path-utility-view="${escapeHtml(module.id)}" data-path-utility-lane="${escapeHtml(lane.id)}" data-path-utility-beacon="${escapeHtml(module.id)}" style="--utility-beacon-index:${index};" title="Open ${escapeHtml(module.label)} module">
                  <span>${escapeHtml(module.label)}</span>
                </button>`
            )
            .join("")}
        </div>
      </div>
      <div class="path-utility-panel" role="tabpanel">
        ${activeModule.content}
      </div>
    </section>`;
}

function pathCommandStripCells(lane, trail, focusedNode, pathNotes) {
  const gates = gateRadarItems(lane);
  const owner = laneAgents(lane)[0];
  const proofs = pathProofItems(lane);
  const suggestion = bestLaneDispatchSuggestion(lane);
  const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id || draft.sourceId === suggestion.id);
  const latest = trail[0];
  return [
    {
      id: "node",
      label: "focus",
      value: focusedNode?.title ?? lane.quest?.title ?? lane.name,
      note: focusedNode?.meta ?? "selected route node",
      tone: focusedNode?.status ?? "advancing",
    },
    {
      id: "gate",
      label: gates.length ? "gate" : "clear",
      value: gates[0]?.title ?? "No active blockers",
      note: gates[0]?.nextAction ?? "ready for proof work",
      tone: gates.length ? "gated" : "ready",
    },
    {
      id: "proof",
      label: "proof",
      value: proofs[0]?.artifactPreview?.label ?? latest?.title ?? "Awaiting proof",
      note: proofs[0]?.artifactPreview?.lines?.[0] ?? latest?.summary ?? "new evidence will appear here",
      tone: proofs.length ? "unlocked" : "scouting",
    },
    {
      id: "crew",
      label: staged ? "queued" : "bot",
      value: owner?.visual?.callsign ?? lane.ownerAgentId ?? "Unassigned",
      note: staged ? "local command staged" : suggestion.title,
      tone: staged ? "unlocked" : "advancing",
    },
    {
      id: "notes",
      label: "notes",
      value: pathNotes.length ? `${formatNumber(pathNotes.length)} operator pins` : "No local pins",
      note: pathNotes[0]?.text ?? "Gate Radar notes surface here",
      tone: pathNotes.length ? "noted" : "future",
    },
  ];
}

function renderPathCommandStrip(lane, trail, focusedNode, pathNotes) {
  const cells = pathCommandStripCells(lane, trail, focusedNode, pathNotes);
  const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id || draft.sourceId === bestLaneDispatchSuggestion(lane).id);
  return `
    <section class="path-command-strip" aria-label="Path command strip" style="${laneStyle(lane)}">
      <div class="path-command-strip-head">
        <div>
          <p class="eyebrow">Route Command</p>
          <h3>${escapeHtml(compactText(chronicleNextAction(lane), 74))}</h3>
        </div>
        <span class="badge ${staged ? "unlocked" : "advancing"}">${staged ? "queued" : "live"}</span>
      </div>
      <div class="path-command-cells">
        ${cells
          .map(
            (cell) => `
              <span class="path-command-cell ${escapeHtml(cell.tone)}">
                <strong>${escapeHtml(cell.label)}</strong>
                <em>${escapeHtml(compactText(cell.value, 42))}</em>
                <small>${escapeHtml(compactText(cell.note, 56))}</small>
              </span>`
          )
          .join("")}
      </div>
      <div class="path-command-actions">
        <button class="tool-button" type="button" data-path-command-jump="route" title="Jump to route rail">ROUTE</button>
        <button class="tool-button" type="button" data-path-command-jump="proof" title="Jump to proof cache">PROOF</button>
        <button class="tool-button" type="button" data-path-command-jump="archive" title="Jump to chapter archive">ARCH</button>
        <button class="tool-button" type="button" data-path-handoff-stage="${escapeHtml(lane.id)}" title="Stage local command">${staged ? "OK" : "Q"}</button>
        <button class="tool-button primary" type="button" data-detail-view="comms" title="Open command deck">COM</button>
      </div>
    </section>`;
}

function pathMissionScanStages(lane, trail, nodes, focusedNode) {
  const gateCount = (lane.counts?.blockers ?? 0) + (lane.counts?.pendingRequests ?? 0);
  const proofCount = trail.filter((item) => pathEventGlyphType(item) === "proof").length;
  const taskCount = lane.counts?.activeTasks ?? trail.filter((item) => pathEventGlyphType(item) === "task").length;
  const unlockCount = lane.counts?.outcomes ?? trail.filter((item) => pathEventGlyphType(item) === "outcome").length;
  const focusIndex = Math.max(0, nodes.findIndex((node) => node.id === focusedNode?.id));
  const focusNode = focusedNode ?? nodes[0];
  return [
    {
      id: "focus",
      label: "focus",
      title: focusNode?.title ?? "Route start",
      meta: `${formatNumber(focusIndex + 1)}/${formatNumber(Math.max(1, nodes.length))} nodes`,
      tone: focusNode?.status ?? "advancing",
      active: true,
    },
    {
      id: "gate",
      label: "gate",
      title: gateCount ? `${formatNumber(gateCount)} blocker cells` : "Clear route",
      meta: compactText(lane.gateMap?.[0]?.nextAction ?? lane.serviceRequests?.[0]?.requestedAction ?? "No active blocker", 54),
      tone: gateCount ? "gated" : "ready",
      active: gateCount > 0,
    },
    {
      id: "proof",
      label: "proof",
      title: `${formatNumber(proofCount)} proof pings`,
      meta: "evidence trail",
      tone: proofCount ? "unlocked" : "scouting",
    },
    {
      id: "tasks",
      label: "tasks",
      title: `${formatNumber(taskCount)} active tasks`,
      meta: compactText(lane.recentTasks?.[0]?.title ?? lane.nextAction ?? "waiting for task signal", 54),
      tone: taskCount ? "advancing" : "scouting",
    },
    {
      id: "unlock",
      label: "unlock",
      title: `${formatNumber(unlockCount)} wins`,
      meta: lane.promotionCandidate?.ready_for_manual_promotion ? "boss door ready" : "reward track",
      tone: unlockCount ? "unlocked" : "scouting",
    },
    {
      id: "future",
      label: "future",
      title: "Next socket",
      meta: "route expands with new trail records",
      tone: "future",
    },
  ];
}

function renderPathMissionScan(lane, trail, nodes, focusedNode, mapStats, pathProgress) {
  const stages = pathMissionScanStages(lane, trail, nodes, focusedNode);
  const activeStageIndex = Math.max(0, stages.findIndex((stage) => stage.active));
  return `
    <section class="path-mission-scan" aria-label="Path mission scan" style="${laneStyle(lane)} --path-progress:${pathProgress}%; --path-scan-active:${activeStageIndex}; --path-scan-count:${stages.length};">
      <div class="path-mission-scan-head">
        <div>
          <span>Mission Scan</span>
          <strong>${escapeHtml(compactText(lane.visual?.realm ?? lane.department ?? "Lane route", 44))}</strong>
        </div>
        <em>${formatNumber(trail.length)} records</em>
      </div>
      <div class="path-mission-scan-core" aria-hidden="true">
        <span class="path-mission-orbit one"></span>
        <span class="path-mission-orbit two"></span>
        <span class="path-mission-runner"></span>
        <span class="path-mission-progress"></span>
      </div>
      <div class="path-mission-stats">
        ${mapStats.map((stat) => `<span><strong>${escapeHtml(stat.value)}</strong><em>${escapeHtml(stat.label)}</em></span>`).join("")}
      </div>
      <div class="path-mission-stages">
        ${stages
          .map(
            (stage, index) => `
              <span class="path-mission-stage ${escapeHtml(stage.tone)} ${stage.active ? "active" : ""}" style="--path-stage-index:${index};">
                <i>${formatNumber(index + 1)}</i>
                <strong>${escapeHtml(stage.label)}</strong>
                <em>${escapeHtml(compactText(stage.title, 42))}</em>
                <small>${escapeHtml(compactText(stage.meta, 52))}</small>
              </span>`
          )
          .join("")}
      </div>
    </section>`;
}

function pathChapterKey(item, fallbackIndex = 0) {
  const time = String(item?.time ?? "");
  const day = time.slice(0, 10);
  return /^\d{4}-\d{2}-\d{2}$/.test(day) ? day : `undated-${fallbackIndex}`;
}

function pathChapterLabel(key) {
  if (key.startsWith("undated")) return "Undated";
  const [, month, day] = key.split("-");
  return `${month}/${day}`;
}

function pathChapterTone(chapter) {
  const counts = chapter.counts ?? {};
  if ((counts.gate ?? 0) || (counts.service ?? 0)) return "gated";
  if ((counts.outcome ?? 0) || (counts.proof ?? 0)) return "unlocked";
  if ((counts.task ?? 0) || (counts.trace ?? 0)) return "advancing";
  return "scouting";
}

function pathChapterArchiveItems(trail) {
  const chapters = [];
  const byKey = new Map();
  trail.forEach((item, index) => {
    const key = pathChapterKey(item, index);
    if (!byKey.has(key)) {
      const chapter = {
        key,
        label: pathChapterLabel(key),
        items: [],
        firstIndex: index,
        endIndex: index,
        counts: {},
      };
      byKey.set(key, chapter);
      chapters.push(chapter);
    }
    const chapter = byKey.get(key);
    const type = pathEventGlyphType(item);
    chapter.items.push(item);
    chapter.endIndex = index;
    chapter.counts[type] = (chapter.counts[type] ?? 0) + 1;
  });
  return chapters;
}

function focusedPathChapter(lane, chapters) {
  if (!chapters.length) return null;
  const stored = state.pathChapterFocusByLane[lane.id];
  const focusedEvent = state.pathEventFocusByLane[lane.id];
  return (
    chapters.find((chapter) => chapter.key === stored) ??
    chapters.find((chapter) => focusedEvent && chapter.items.some((item) => pathEventKey(item) === focusedEvent)) ??
    chapters[0]
  );
}

function focusPathChapter(lane, chapter) {
  if (!lane || !chapter?.items?.length) return;
  const focusItem = chapter.items[0];
  const focusKey = pathEventKey(focusItem);
  state.pathChapterFocusByLane = { ...state.pathChapterFocusByLane, [lane.id]: chapter.key };
  state.pathEventFocusByLane = { ...state.pathEventFocusByLane, [lane.id]: focusKey };
  state.trailLimitByLane = { ...state.trailLimitByLane, [lane.id]: Math.max(state.trailLimitByLane[lane.id] ?? 18, chapter.endIndex + 1) };
  const replayIndex = pathReplayItems(lane).findIndex((item) => pathEventKey(item) === focusKey);
  if (replayIndex >= 0) {
    state.pathReplayIndexByLane = { ...state.pathReplayIndexByLane, [lane.id]: replayIndex };
  }
}

function pathChapterRecordLensStateKey(lane, chapter) {
  return `${lane.id}:${chapter?.key ?? "none"}`;
}

function pathChapterRecordLens(lane, chapter) {
  return state.pathChapterRecordLensByLane[pathChapterRecordLensStateKey(lane, chapter)] ?? "all";
}

function pathChapterRecordStateKey(lane, chapter, lens = pathChapterRecordLens(lane, chapter)) {
  return `${lane.id}:${chapter?.key ?? "none"}:${lens}`;
}

function pathChapterRecordLimit(lane, chapter, lens = pathChapterRecordLens(lane, chapter)) {
  if (!chapter) return 0;
  return state.pathChapterRecordLimitByLane[pathChapterRecordStateKey(lane, chapter, lens)] ?? 4;
}

function pathChapterRunwayStateKey(lane, chapter, lens = pathChapterRecordLens(lane, chapter)) {
  return `${lane.id}:${chapter?.key ?? "none"}:${lens}`;
}

function pathChapterRunwayLimit(lane, chapter, lens = pathChapterRecordLens(lane, chapter)) {
  if (!chapter) return 0;
  return state.pathChapterRunwayLimitByLane[pathChapterRunwayStateKey(lane, chapter, lens)] ?? 12;
}

function pathChapterArchiveExpanded(lane) {
  return Boolean(state.pathChapterArchiveExpandedByLane[lane.id]);
}

function pathChapterRecordLensOptions(chapter) {
  const counts = (chapter?.items ?? []).reduce((acc, item) => {
    const type = pathEventGlyphType(item);
    acc[type] = (acc[type] ?? 0) + 1;
    return acc;
  }, {});
  return [
    { id: "all", label: "All", count: chapter?.items?.length ?? 0, icon: "trace" },
    { id: "proof", label: "Proof", count: counts.proof ?? 0 },
    { id: "outcome", label: "Unlock", count: counts.outcome ?? 0 },
    { id: "service", label: "Service", count: counts.service ?? 0 },
    { id: "task", label: "Task", count: counts.task ?? 0 },
    { id: "trace", label: "Trace", count: counts.trace ?? 0 },
    { id: "gate", label: "Gate", count: counts.gate ?? 0 },
  ];
}

function pathChapterFirstItemOfTypes(chapter, types) {
  return (chapter?.items ?? []).find((item) => types.includes(pathEventGlyphType(item)));
}

function pathChapterQuestlineStages(lane, chapter) {
  const gateCount = (chapter.counts?.gate ?? 0) + (chapter.counts?.service ?? 0);
  const proofCount = chapter.counts?.proof ?? 0;
  const taskCount = chapter.counts?.task ?? 0;
  const outcomeCount = chapter.counts?.outcome ?? 0;
  const traceCount = chapter.counts?.trace ?? 0;
  const startItem = chapter.items?.[chapter.items.length - 1] ?? chapter.items?.[0];
  const latestItem = chapter.items?.[0];
  const proofItem = pathChapterFirstItemOfTypes(chapter, ["proof"]);
  const gateItem = pathChapterFirstItemOfTypes(chapter, ["gate", "service"]);
  const taskItem = pathChapterFirstItemOfTypes(chapter, ["task"]);
  const outcomeItem = pathChapterFirstItemOfTypes(chapter, ["outcome"]);
  return [
    {
      id: "spawn",
      label: "Spawn",
      tone: "unlocked",
      count: chapter.items?.length ?? 0,
      icon: "trace",
      item: startItem,
      body: "Chapter opened from the lane trail.",
    },
    {
      id: "proof",
      label: "Proof",
      tone: proofCount ? "unlocked" : "locked",
      count: proofCount,
      icon: "proof",
      item: proofItem,
      body: proofCount ? "Evidence was captured in this chapter." : "No proof record in this chapter yet.",
    },
    {
      id: "gate",
      label: "Gate",
      tone: gateCount ? "gated" : "clear",
      count: gateCount,
      icon: "gate",
      item: gateItem,
      body: gateCount ? "Blocker or service gate is active here." : "No gate signal in this chapter.",
    },
    {
      id: "tasks",
      label: "Tasks",
      tone: taskCount ? "advancing" : "locked",
      count: taskCount,
      icon: "task",
      item: taskItem,
      body: taskCount ? "Runnable work items exist here." : "No task record in this chapter yet.",
    },
    {
      id: "unlock",
      label: "Unlock",
      tone: outcomeCount ? "unlocked" : "locked",
      count: outcomeCount,
      icon: "outcome",
      item: outcomeItem,
      body: outcomeCount ? "Outcome or unlock recorded." : "No unlock has landed in this chapter yet.",
    },
    {
      id: "next",
      label: "Next",
      tone: gateCount ? "gated" : taskCount || traceCount ? "advancing" : proofCount || outcomeCount ? "unlocked" : "scouting",
      count: Math.max(taskCount, traceCount, proofCount, outcomeCount, gateCount),
      icon: gateCount ? "gate" : taskCount ? "task" : outcomeCount ? "outcome" : proofCount ? "proof" : "trace",
      item: latestItem,
      body: chronicleNextAction(lane),
    },
  ];
}

function renderPathChapterQuestline(lane, chapter) {
  if (!chapter) return "";
  const stages = pathChapterQuestlineStages(lane, chapter);
  const activeStages = stages.filter((stage) => stage.tone !== "locked").length;
  const progress = Math.round((activeStages / Math.max(stages.length, 1)) * 100);
  const gateCount = (chapter.counts?.gate ?? 0) + (chapter.counts?.service ?? 0);
  const outcomeCount = chapter.counts?.outcome ?? 0;
  const proofCount = chapter.counts?.proof ?? 0;
  return `
    <section class="path-chapter-questline ${escapeHtml(pathChapterTone(chapter))}" aria-label="Chapter Questline" style="--questline-a:${escapeHtml(lane.visual?.accent ?? "#44d7c9")}; --questline-b:${escapeHtml(lane.visual?.accentAlt ?? "#f4ba55")}; --questline-progress:${progress}%; --questline-art:url('./assets/system/path-chapter-questline-20260618.png')">
      <div class="path-chapter-quest-head">
        <div>
          <span>Chapter Questline</span>
          <strong>${escapeHtml(chapter.label)} run map</strong>
        </div>
        <em>${formatNumber(proofCount + outcomeCount)} wins / ${formatNumber(gateCount)} gates</em>
      </div>
      <div class="path-chapter-quest-meter" aria-hidden="true"><i></i><b class="path-chapter-quest-pulse"></b></div>
      <div class="path-chapter-quest-stages">
        ${stages
          .map((stage, index) => {
            const item = stage.item;
            const glyph = pathEventGlyphMarkup(item ?? stage.icon, "path-chapter-quest-glyph");
            const body = compactText(stage.body, 98);
            const label = `${formatNumber(index + 1)}. ${stage.label}`;
            return item
              ? `<button class="path-chapter-quest-stage ${escapeHtml(stage.tone)} ${escapeHtml(stage.id)}" type="button" data-path-event-focus="${escapeHtml(pathEventKey(item))}" title="Focus ${escapeHtml(stage.label)} stage">
                  ${glyph}
                  <span>
                    <strong>${escapeHtml(label)}</strong>
                    <em>${escapeHtml(body)}</em>
                    <small>${formatNumber(stage.count)} ${stage.count === 1 ? "signal" : "signals"}</small>
                  </span>
                  <b class="path-chapter-quest-spark" aria-hidden="true"></b>
                </button>`
              : `<span class="path-chapter-quest-stage ${escapeHtml(stage.tone)} ${escapeHtml(stage.id)}">
                  ${glyph}
                  <span>
                    <strong>${escapeHtml(label)}</strong>
                    <em>${escapeHtml(body)}</em>
                    <small>${formatNumber(stage.count)} ${stage.count === 1 ? "signal" : "signals"}</small>
                  </span>
                  <b class="path-chapter-quest-spark" aria-hidden="true"></b>
                </span>`;
          })
          .join("")}
      </div>
    </section>`;
}

function pathChapterMilestoneLadderItems(lane, chapter) {
  const proofItem = pathChapterFirstItemOfTypes(chapter, ["proof"]);
  const gateItem = pathChapterFirstItemOfTypes(chapter, ["gate", "service"]);
  const taskItem = pathChapterFirstItemOfTypes(chapter, ["task"]);
  const outcomeItem = pathChapterFirstItemOfTypes(chapter, ["outcome"]);
  const latestItem = chapter.items?.[0];
  const counts = chapter.counts ?? {};
  const gateCount = (counts.gate ?? 0) + (counts.service ?? 0);
  const proofCount = counts.proof ?? 0;
  const taskCount = counts.task ?? 0;
  const outcomeCount = counts.outcome ?? 0;
  return [
    {
      id: "chapter-open",
      label: "Chapter",
      tone: "unlocked",
      count: chapter.items?.length ?? 0,
      item: latestItem,
      body: "Trail records grouped into a playable chapter.",
    },
    {
      id: "proof-seal",
      label: "Proof",
      tone: proofCount ? "unlocked" : "locked",
      count: proofCount,
      item: proofItem,
      body: proofCount ? "Local evidence has landed here." : "Waiting for chapter proof.",
    },
    {
      id: "gate-check",
      label: "Gate",
      tone: gateCount ? "gated" : "clear",
      count: gateCount,
      item: gateItem,
      body: gateCount ? "Review gate is visible before escalation." : "No blocker gate in this chapter.",
    },
    {
      id: "task-chain",
      label: "Tasks",
      tone: taskCount ? "advancing" : "locked",
      count: taskCount,
      item: taskItem,
      body: taskCount ? "Runnable work exists in this chapter." : "No task chain yet.",
    },
    {
      id: "unlock-drop",
      label: "Unlock",
      tone: outcomeCount ? "unlocked" : "locked",
      count: outcomeCount,
      item: outcomeItem,
      body: outcomeCount ? "Outcome or unlock is recorded." : "Outcome still locked.",
    },
    {
      id: "next-rung",
      label: "Next",
      tone: gateCount ? "gated" : taskCount || proofCount || outcomeCount ? "advancing" : "scouting",
      count: Math.max(gateCount, taskCount, proofCount, outcomeCount, counts.trace ?? 0),
      item: latestItem,
      body: chronicleNextAction(lane),
    },
  ];
}

function renderPathChapterMilestoneLadder(lane, chapter) {
  if (!chapter) return "";
  const items = pathChapterMilestoneLadderItems(lane, chapter);
  const activeCount = items.filter((item) => item.tone !== "locked").length;
  const progress = Math.round((activeCount / Math.max(items.length, 1)) * 100);
  const winCount = (chapter.counts?.proof ?? 0) + (chapter.counts?.outcome ?? 0);
  return `
    <section class="path-chapter-milestone-ladder ${escapeHtml(pathChapterTone(chapter))}" aria-label="Chapter Milestone Ladder" style="--milestone-a:${escapeHtml(lane.visual?.accent ?? "#44d7c9")}; --milestone-b:${escapeHtml(lane.visual?.accentAlt ?? "#f4ba55")}; --milestone-progress:${progress}%; --milestone-art:url('./assets/system/path-chapter-milestone-ladder-20260618.png')">
      <div class="path-chapter-milestone-head">
        <div>
          <span>Chapter Milestone Ladder</span>
          <strong>${escapeHtml(chapter.label)} unlock path</strong>
        </div>
        <em>${formatNumber(winCount)} wins / ${formatNumber(items.length)} rungs</em>
      </div>
      <div class="path-chapter-milestone-rail" aria-hidden="true"><i></i></div>
      <div class="path-chapter-milestone-steps">
        ${items
          .map((step, index) => {
            const glyph = pathEventGlyphMarkup(step.item ?? step.id, "path-chapter-milestone-orb");
            const body = compactText(step.body, 82);
            const label = `${formatNumber(index + 1)}. ${step.label}`;
            return step.item
              ? `<button class="path-chapter-milestone-step ${escapeHtml(step.tone)} ${escapeHtml(step.id)}" type="button" data-path-event-focus="${escapeHtml(pathEventKey(step.item))}" title="Focus ${escapeHtml(step.label)} milestone">
                  ${glyph}
                  <span>
                    <strong>${escapeHtml(label)}</strong>
                    <em>${escapeHtml(body)}</em>
                    <small>${formatNumber(step.count)} ${step.count === 1 ? "signal" : "signals"}</small>
                  </span>
                  <b class="path-chapter-milestone-spark" aria-hidden="true"></b>
                </button>`
              : `<span class="path-chapter-milestone-step ${escapeHtml(step.tone)} ${escapeHtml(step.id)}">
                  ${glyph}
                  <span>
                    <strong>${escapeHtml(label)}</strong>
                    <em>${escapeHtml(body)}</em>
                    <small>${formatNumber(step.count)} ${step.count === 1 ? "signal" : "signals"}</small>
                  </span>
                  <b class="path-chapter-milestone-spark" aria-hidden="true"></b>
                </span>`;
          })
          .join("")}
      </div>
    </section>`;
}

function pathChapterGamePortalStats(lane, chapter) {
  const minigame = lane.visual?.minigame ?? {};
  const custom = Boolean(minigameDefinition(lane));
  const assets = visualAssetRecords().filter((asset) => asset.laneId === lane.id && (asset.kind === "game" || asset.kind === "lane")).length;
  const gateCount = (chapter?.counts?.gate ?? 0) + (chapter?.counts?.service ?? 0);
  return [
    { label: "module", value: custom ? "custom" : "fallback" },
    { label: "stages", value: formatNumber(gameStepCount(lane)) },
    { label: "assets", value: formatNumber(assets) },
    { label: "chapter", value: `${formatNumber(chapter?.items?.length ?? 0)} rec` },
    { label: "gates", value: formatNumber(gateCount) },
    { label: "status", value: stateLabel(minigame.status ?? "slot_ready") },
  ];
}

function renderPathChapterGamePortal(lane, chapter) {
  if (!chapter) return "";
  const minigame = lane.visual?.minigame ?? {};
  const custom = Boolean(minigameDefinition(lane));
  const texture = minigame.texture ?? lane.visual?.avatar;
  const stats = pathChapterGamePortalStats(lane, chapter);
  const gateCount = (chapter.counts?.gate ?? 0) + (chapter.counts?.service ?? 0);
  return `
    <section class="path-chapter-game-portal ${custom ? "custom" : "fallback"} ${gateCount ? "gated" : "ready"}" aria-label="Chapter Game Portal" style="--game-portal-a:${escapeHtml(lane.visual?.accent ?? "#44d7c9")}; --game-portal-b:${escapeHtml(lane.visual?.accentAlt ?? "#f4ba55")}; --game-portal-art:url('./assets/system/path-chapter-game-portal-20260618.png')">
      <div class="path-chapter-game-art">
        ${texture ? `<img src="${escapeHtml(texture)}" alt="" loading="eager" />` : avatarMarkup(lane, "path-chapter-game-avatar")}
        <span>${escapeHtml(minigame.id ?? "checkpoint")}</span>
      </div>
      <div class="path-chapter-game-copy">
        <div class="path-chapter-game-head">
          <div>
            <span>Chapter Game Portal</span>
            <strong>${escapeHtml(compactText(minigame.title ?? `${lane.name} module`, 54))}</strong>
          </div>
          <em>${escapeHtml(custom ? "custom renderer" : "checkpoint fallback")}</em>
        </div>
        <p>${escapeHtml(compactText(minigame.mechanic ?? lane.quest?.title ?? lane.visual?.mood ?? "Advance through lane checkpoints as a playable module.", 154))}</p>
        <div class="path-chapter-game-stats">
          ${stats
            .map(
              (stat) => `
                <span>
                  <strong>${escapeHtml(stat.value)}</strong>
                  <em>${escapeHtml(stat.label)}</em>
                </span>`
            )
            .join("")}
        </div>
        <div class="path-chapter-game-actions">
          <button class="tool-button" type="button" data-detail-view="game" title="Open lane game">GAME</button>
          <button class="tool-button" type="button" data-detail-view="overview" title="Open Minigame Forge">FORGE</button>
          <button class="tool-button" type="button" data-detail-view="trail" title="Open full lane trail">TRAIL</button>
        </div>
      </div>
    </section>`;
}

function pathChapterSpoils(chapter) {
  const counts = chapter?.counts ?? {};
  return [
    {
      id: "proof",
      label: "Proof Seal",
      count: counts.proof ?? 0,
      body: "Local evidence recorded in this chapter.",
    },
    {
      id: "outcome",
      label: "Unlock Coin",
      count: counts.outcome ?? 0,
      body: "Chapter events that moved the lane forward.",
    },
    {
      id: "gate",
      label: "Gate Lock",
      count: counts.gate ?? 0,
      body: "Explicit blockers or stop conditions found.",
    },
    {
      id: "service",
      label: "Service Writ",
      count: counts.service ?? 0,
      body: "Service-worker or approval-path records.",
    },
    {
      id: "task",
      label: "Task Token",
      count: counts.task ?? 0,
      body: "Runnable work items inside the chapter.",
    },
    {
      id: "trace",
      label: "Trace Crystal",
      count: counts.trace ?? 0,
      body: "System trace and event-log evidence.",
    },
  ];
}

function renderPathChapterSpoils(chapter) {
  if (!chapter) return "";
  const spoils = pathChapterSpoils(chapter);
  const earned = spoils.filter((item) => item.count > 0).length;
  return `
    <div class="path-chapter-spoils" aria-label="Chapter Spoils" style="--chapter-spoils-art:url('./assets/system/path-chapter-spoils-20260618.png')">
      <div class="path-chapter-spoils-head">
        <div>
          <span>Chapter Spoils</span>
          <strong>${formatNumber(earned)} of ${formatNumber(spoils.length)} earned</strong>
        </div>
        <em>${escapeHtml(chapter.label)}</em>
      </div>
      <div class="path-chapter-spoils-list">
        ${spoils
          .map(
            (spoil) => `
              <span class="path-chapter-spoil-badge ${escapeHtml(spoil.id)} ${spoil.count ? "earned" : "locked"}" title="${escapeHtml(spoil.body)}">
                <i class="path-chapter-spoil-medal ${escapeHtml(spoil.id)}" aria-hidden="true"></i>
                <span>
                  <strong>${escapeHtml(spoil.label)}</strong>
                  <em>${formatNumber(spoil.count)} ${spoil.count === 1 ? "record" : "records"}</em>
                </span>
              </span>`
          )
          .join("")}
      </div>
    </div>`;
}

function pathChapterDepthRingStats(chapter, filteredRecords, remaining) {
  const total = Math.max(1, chapter?.items?.length ?? 0);
  const counts = chapter?.counts ?? {};
  const ringStats = [
    { id: "proof", label: "Proof", count: (counts.proof ?? 0) + (counts.outcome ?? 0), tone: "unlocked" },
    { id: "gate", label: "Gates", count: (counts.gate ?? 0) + (counts.service ?? 0), tone: "gated" },
    { id: "task", label: "Tasks", count: counts.task ?? 0, tone: "advancing" },
    { id: "trace", label: "Traces", count: counts.trace ?? 0, tone: "scouting" },
  ];
  return ringStats.map((stat, index) => ({
    ...stat,
    index,
    percent: Math.max(8, Math.min(100, Math.round((stat.count / total) * 100))),
    visible: filteredRecords.length,
    remaining,
    total,
  }));
}

function renderPathChapterDepthRings(lane, chapter, filteredRecords, remaining) {
  if (!chapter) return "";
  const stats = pathChapterDepthRingStats(chapter, filteredRecords, remaining);
  const total = chapter.items?.length ?? 0;
  const signalCount = stats.reduce((sum, stat) => sum + stat.count, 0);
  const depthPercent = Math.max(12, Math.min(100, Math.round((filteredRecords.length / Math.max(1, total)) * 100)));
  return `
    <section class="path-chapter-depth-rings ${escapeHtml(pathChapterTone(chapter))}" aria-label="Chapter Depth Rings" style="--depth-a:${escapeHtml(lane.visual?.accent ?? "#44d7c9")}; --depth-b:${escapeHtml(lane.visual?.accentAlt ?? "#f4ba55")}; --depth-progress:${depthPercent}%">
      <div class="path-chapter-depth-copy">
        <span>Chapter Depth Rings</span>
        <strong>${formatNumber(total)} record orbit</strong>
        <em>${remaining ? `${formatNumber(remaining)} more hidden behind the active lens` : "current lens fully open"}</em>
      </div>
      <div class="path-chapter-depth-orbit" aria-hidden="true">
        ${stats
          .map(
            (stat) => `
              <span class="path-chapter-depth-ring ${escapeHtml(stat.id)} ${escapeHtml(stat.tone)}" style="--depth-ring:${stat.percent}%; --depth-ring-index:${stat.index}">
                <i></i>
              </span>`
          )
          .join("")}
        <strong>${formatNumber(signalCount)}</strong>
        <em>signals</em>
      </div>
      <div class="path-chapter-depth-key">
        ${stats
          .map(
            (stat) => `
              <span class="${escapeHtml(stat.id)}">
                <strong>${formatNumber(stat.count)}</strong>
                <em>${escapeHtml(stat.label)}</em>
                <small>${formatNumber(stat.percent)}%</small>
              </span>`
          )
          .join("")}
      </div>
    </section>`;
}

function pathChapterEvidenceItems(lane, chapter) {
  const chapterEvidence = (chapter?.items ?? []).filter((item) => {
    const type = pathEventGlyphType(item);
    return item.artifactPreview?.lines?.length || item.artifact || type === "proof" || type === "outcome";
  });
  const seen = new Set();
  return [...chapterEvidence, ...pathProofItems(lane)]
    .filter((item) => {
      const key = pathEventKey(item);
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    })
    .slice(0, 4);
}

function renderPathChapterEvidenceVault(lane, chapter) {
  if (!chapter) return "";
  const items = pathChapterEvidenceItems(lane, chapter);
  const previewCount = items.filter((item) => item.artifactPreview?.lines?.length).length;
  const artifactCount = items.filter((item) => item.artifact || item.artifactPreview?.label).length;
  const proofCount = items.filter((item) => pathEventGlyphType(item) === "proof").length;
  return `
    <section class="path-chapter-evidence-vault ${items.length ? "unlocked" : "scouting"}" aria-label="Chapter Evidence Vault" style="--evidence-a:${escapeHtml(lane.visual?.accent ?? "#44d7c9")}; --evidence-b:${escapeHtml(lane.visual?.accentAlt ?? "#f4ba55")}">
      <div class="path-chapter-evidence-head">
        <div>
          <span>Chapter Evidence Vault</span>
          <strong>${escapeHtml(items.length ? `${formatNumber(items.length)} proof cards surfaced` : "No local proof cards yet")}</strong>
        </div>
        <em>${escapeHtml(compactText(chapter.label, 34))}</em>
      </div>
      <div class="path-chapter-evidence-stats">
        <span><strong>${formatNumber(previewCount)}</strong><em>previews</em></span>
        <span><strong>${formatNumber(artifactCount)}</strong><em>artifacts</em></span>
        <span><strong>${formatNumber(proofCount)}</strong><em>proofs</em></span>
      </div>
      <div class="path-chapter-evidence-list">
        ${
          items.length
            ? items
                .map((item) => {
                  const eventKey = pathEventKey(item);
                  const type = pathEventGlyphType(item);
                  const previewLine = item.artifactPreview?.lines?.[0] ?? item.summary ?? item.artifact ?? "Local evidence record";
                  const compactPreview = item.artifactPreview?.lines?.length
                    ? {
                        ...item.artifactPreview,
                        lines: item.artifactPreview.lines.slice(0, 2),
                        truncated: item.artifactPreview.truncated || item.artifactPreview.lines.length > 2,
                      }
                    : null;
                  return `
                    <button class="path-chapter-evidence-card ${escapeHtml(type)}" type="button" data-path-event-focus="${escapeHtml(eventKey)}" title="Inspect chapter evidence">
                      ${pathEventGlyphMarkup(item, "path-chapter-evidence-glyph")}
                      <span>
                        <strong>${escapeHtml(compactText(item.artifactPreview?.label ?? item.title ?? "Evidence artifact", 62))}</strong>
                        <em>${escapeHtml(compactText(previewLine, 118))}</em>
                        <small>${escapeHtml(stateLabel(item.kind))} - ${escapeHtml(shortDate(item.time))}</small>
                      </span>
                      ${renderPathArtifactPreview(compactPreview)}
                    </button>`;
                })
                .join("")
            : `<span class="path-chapter-evidence-empty"><strong>Vault waiting</strong><em>Artifact previews, proof records, and outcome packets will appear here when this chapter earns them.</em></span>`
        }
      </div>
      <div class="path-chapter-evidence-actions">
        <button class="tool-button" type="button" data-detail-view="trail" title="Open full evidence trail">TRL</button>
        <button class="tool-button" type="button" data-detail-view="chronicle" title="Open chronicle log">LOG</button>
      </div>
    </section>`;
}

function pathChapterCrewRecords(lane, chapter) {
  const agents = laneAgents(lane);
  const suggestion = bestLaneDispatchSuggestion(lane);
  const chapterKinds = new Set((chapter?.items ?? []).map((item) => pathEventGlyphType(item)));
  const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id || draft.sourceId === suggestion.id);
  const gatePressure = (chapter?.counts?.gate ?? 0) + (lane.counts?.blockers ?? 0);
  const proofPressure = (chapter?.counts?.proof ?? 0) + (chapter?.counts?.outcome ?? 0);
  const tracePressure = chapter?.counts?.trace ?? 0;
  const rankLabels = ["Lead", "Relay", "Watch"];
  const fallbackAgent = {
    agent_id: lane.ownerAgentId ?? `lane-relay-${lane.id}`,
    role_id: "lane_manager",
    thread_id: lane.ownerThreadId ?? null,
    status: "unassigned",
    visual: {
      callsign: lane.ownerAgentId ? stateLabel(lane.ownerAgentId) : "Unassigned relay",
      specialty: "Waiting for a bound lane bot",
      accent: lane.visual?.accent,
    },
  };
  const crew = agents.length ? agents : [fallbackAgent];
  return crew.slice(0, 3).map((agent, index) => {
    const visual = agent.visual ?? {};
    const chapterBias = chapterKinds.has("gate") || lane.counts?.blockers ? "gate watch" : chapterKinds.has("outcome") || chapterKinds.has("proof") ? "unlock review" : "chapter relay";
    return {
      agent,
      lane,
      suggestion,
      staged,
      index,
      chapterBias,
      callsign: visual.callsign ?? stateLabel(agent.agent_id ?? "relay bot"),
      specialty: visual.specialty ?? stateLabel(agent.role_id ?? "operator"),
      thread: agent.thread_id ?? lane.ownerThreadId ?? "No thread linked",
      accent: visual.accent ?? lane.visual?.accent ?? "#44d7c9",
      rankLabel: rankLabels[index] ?? "Aux",
      readiness: Math.max(16, Math.min(98, 56 + proofPressure * 7 + tracePressure * 2 - gatePressure * 5 + (staged ? 6 : 0) - index * 4)),
      pressureLabel: gatePressure > proofPressure ? "gate pressure" : staged ? "queued relay" : "ready link",
    };
  });
}

function renderPathChapterCrewRelay(lane, chapter) {
  if (!chapter) return "";
  const records = pathChapterCrewRecords(lane, chapter);
  const suggestion = records[0]?.suggestion ?? laneDispatchSuggestion(lane);
  const staged = records.some((record) => record.staged);
  const gateCount = (chapter.counts?.gate ?? 0) + (lane.counts?.blockers ?? 0);
  const proofCount = (chapter.counts?.proof ?? 0) + (chapter.counts?.outcome ?? 0);
  const traceCount = chapter.counts?.trace ?? 0;
  return `
    <section class="path-chapter-crew-relay ${staged ? "staged" : ""}" aria-label="Chapter Crew Relay" style="--crew-a:${escapeHtml(lane.visual?.accent ?? "#44d7c9")}; --crew-b:${escapeHtml(lane.visual?.accentAlt ?? "#f4ba55")}">
      <div class="path-chapter-crew-head">
        <div>
          <span>Chapter Crew Relay</span>
          <strong>${escapeHtml(compactText(chapter.label, 48))} handoff</strong>
        </div>
        <em>${staged ? "queued" : "local"}</em>
      </div>
      <div class="path-chapter-crew-formation" aria-label="Chapter Crew Formation">
        <div class="path-chapter-crew-formation-copy">
          <span>Chapter Crew Formation</span>
          <strong>${formatNumber(records.length)} ${records.length === 1 ? "operator" : "operators"} synced</strong>
          <em>${escapeHtml(compactText(suggestion.title ?? suggestion.reason ?? chronicleNextAction(lane), 88))}</em>
        </div>
        <div class="path-chapter-crew-stack">
          ${records
            .map(
              (record) => `
                <article class="path-chapter-crew-slot" style="--crew-agent:${escapeHtml(record.accent)}; --crew-ready:${record.readiness}%">
                  <span class="path-chapter-crew-rank">${escapeHtml(record.rankLabel)}</span>
                  ${agentAvatarMarkup(record.agent, lane, "path-chapter-crew-formation-avatar")}
                  <span class="path-chapter-crew-readiness" aria-label="${escapeHtml(`${record.callsign} readiness ${record.readiness}%`)}"><i></i></span>
                  <small>${formatNumber(record.readiness)}% - ${escapeHtml(record.pressureLabel)}</small>
                </article>`
            )
            .join("")}
        </div>
      </div>
      <div class="path-chapter-crew-grid">
        <div class="path-chapter-crew-agents">
          ${records
            .map(
              (record) => `
                <article class="path-chapter-crew-agent" style="--crew-agent:${escapeHtml(record.accent)}">
                  ${agentAvatarMarkup(record.agent, lane, "path-chapter-crew-avatar")}
                  <div>
                    <span>${escapeHtml(record.chapterBias)}</span>
                    <strong>${escapeHtml(compactText(record.callsign, 42))}</strong>
                    <em>${escapeHtml(compactText(record.specialty, 72))}</em>
                    <small>${escapeHtml(compactText(record.thread, 48))}</small>
                  </div>
                </article>`
            )
            .join("")}
        </div>
        <article class="path-chapter-crew-brief">
          <div class="path-chapter-crew-stats">
            <span><strong>${formatNumber(proofCount)}</strong><em>proof</em></span>
            <span><strong>${formatNumber(gateCount)}</strong><em>gates</em></span>
            <span><strong>${formatNumber(traceCount)}</strong><em>traces</em></span>
            <span><strong>${formatNumber(suggestion.urgency ?? 0)}</strong><em>urge</em></span>
          </div>
          <p>${escapeHtml(compactText(suggestion.reason ?? chronicleNextAction(lane), 178))}</p>
          <div class="path-chapter-crew-actions">
            <button class="tool-button" type="button" data-stage-lane-command="${escapeHtml(lane.id)}" title="Stage chapter relay command">${staged ? "OK" : "Q"}</button>
            <button class="tool-button" type="button" data-detail-view="comms" title="Open command deck">COM</button>
            <button class="tool-button" type="button" data-detail-view="trail" title="Open full trail">TRL</button>
          </div>
        </article>
      </div>
    </section>`;
}

function pathChapterCommandLogRecords(lane, chapter) {
  const suggestion = bestLaneDispatchSuggestion(lane);
  const stagedDrafts = state.stagedDispatches
    .filter((draft) => draft.laneId === lane.id)
    .slice(0, 2)
    .map((draft) => ({
      id: draft.id,
      kind: "queued",
      tone: dispatchTone(draft.kind),
      title: draft.title ?? "Queued local draft",
      body: draft.command,
      meta: shortDate(draft.stagedAt),
    }));
  const historyItems = state.dispatchHistory
    .filter((item) => item.laneName === lane.name)
    .slice(0, 2)
    .map((item) => ({
      id: item.id,
      kind: item.action,
      tone: item.action === "archived" ? "gated" : item.action === "copied" ? "unlocked" : "advancing",
      title: item.title ?? stateLabel(item.action),
      body: `${stateLabel(item.action)} - ${item.count > 1 ? `${formatNumber(item.count)} drafts` : lane.name}`,
      meta: shortDate(item.time),
    }));
  const chapterLead = chapter?.items?.[0];
  return [
    {
      id: `suggestion-${suggestion.id}`,
      kind: suggestion.kind,
      tone: dispatchTone(suggestion.kind),
      title: suggestion.title ?? "Suggested local command",
      body: suggestion.command,
      meta: `${formatNumber(suggestion.urgency ?? 0)} urgency`,
    },
    ...stagedDrafts,
    ...historyItems,
    {
      id: `chapter-${chapter?.key ?? lane.id}`,
      kind: "chapter_context",
      tone: pathChapterTone(chapter),
      title: chapterLead?.title ?? `${chapter?.label ?? "Chapter"} context`,
      body: chapterLead?.summary ?? chapterLead?.artifact ?? "Use the selected chapter records as context before staging another local draft.",
      meta: chapter?.label ?? "chapter",
    },
  ].slice(0, 5);
}

function pathChapterCommandRelayStats(lane, chapter, records) {
  const stagedCount = state.stagedDispatches.filter((draft) => draft.laneId === lane.id).length;
  const historyCount = state.dispatchHistory.filter((item) => item.laneName === lane.name).length;
  const suggestion = bestLaneDispatchSuggestion(lane);
  const chapterContextCount = chapter?.items?.length ?? 0;
  const gatedCount = (records ?? []).filter((record) => record.tone === "gated").length;
  return [
    { label: "queue", value: stagedCount },
    { label: "local log", value: historyCount },
    { label: "urgency", value: suggestion.urgency ?? 0 },
    { label: "chapter", value: chapterContextCount },
    { label: "gates", value: gatedCount },
  ];
}

function renderPathChapterCommandLog(lane, chapter) {
  if (!chapter) return "";
  const records = pathChapterCommandLogRecords(lane, chapter);
  const stagedCount = state.stagedDispatches.filter((draft) => draft.laneId === lane.id).length;
  const historyCount = state.dispatchHistory.filter((item) => item.laneName === lane.name).length;
  const suggestion = bestLaneDispatchSuggestion(lane);
  const stats = pathChapterCommandRelayStats(lane, chapter, records);
  return `
    <section class="path-chapter-command-log" aria-label="Chapter Command Log" style="--command-a:${escapeHtml(lane.visual?.accent ?? "#44d7c9")}; --command-b:${escapeHtml(lane.visual?.accentAlt ?? "#f4ba55")}; --command-art:url('./assets/system/path-chapter-command-relay-20260618.png')">
      <div class="path-chapter-command-visual" aria-hidden="true">
        <span class="path-chapter-command-signal"></span>
        <i>${escapeHtml(stateLabel(suggestion.kind).slice(0, 3).toUpperCase())}</i>
      </div>
      <div class="path-chapter-command-head">
        <div>
          <span>Chapter Command Log</span>
          <strong>${escapeHtml(compactText(suggestion.title ?? "Local command loop", 52))}</strong>
        </div>
        <em>${formatNumber(stagedCount)} queued</em>
      </div>
      <div class="path-chapter-command-summary">
        <span><strong>${formatNumber(records.length)}</strong><em>shown</em></span>
        ${stats
          .slice(0, 5)
          .map((stat) => `<span><strong>${formatNumber(stat.value)}</strong><em>${escapeHtml(stat.label)}</em></span>`)
          .join("")}
      </div>
      <div class="path-chapter-command-feed">
        ${records
          .map(
            (record) => `
              <article class="path-chapter-command-entry ${escapeHtml(record.tone)}">
                <i>${escapeHtml(stateLabel(record.kind).slice(0, 2).toUpperCase())}</i>
                <div>
                  <span>${escapeHtml(record.meta)}</span>
                  <strong>${escapeHtml(compactText(record.title, 58))}</strong>
                  <em>${escapeHtml(compactText(record.body, 128))}</em>
                </div>
              </article>`
          )
          .join("")}
      </div>
      <div class="path-chapter-command-actions">
        <button class="tool-button" type="button" data-stage-lane-command="${escapeHtml(lane.id)}" title="Stage command in outbox">${stagedCount ? "OK" : "Q"}</button>
        <button class="tool-button" type="button" data-detail-view="comms" title="Open command deck">COM</button>
        <button class="tool-button" type="button" data-detail-view="trail" title="Open full lane trail">TRL</button>
      </div>
    </section>`;
}

function pathChapterGateStackItems(lane, chapter) {
  const gateItems = gateRadarItems(lane);
  const chapterGateCount = (chapter?.counts?.gate ?? 0) + (chapter?.counts?.service ?? 0);
  const chapterLead = (chapter?.items ?? []).find((item) => ["gate", "service"].includes(pathEventGlyphType(item)));
  const visibleGates = gateItems.length
    ? gateItems.slice(0, 4)
    : [
        {
          id: `chapter-clear-${lane.id}`,
          kind: "clear",
          tone: "scouting",
          severity: "watch",
          category: "review",
          title: "No active gate signals",
          label: "clear",
          body: chapterLead?.summary ?? "This chapter has no active blocker records in the current snapshot.",
          nextAction: "Keep watching new service requests and blocker records as the lane expands.",
          urgency: Math.max(18, chapterGateCount * 12),
        },
      ];
  return visibleGates.map((item, index) => {
    const note = gateRadarNoteForItem(lane, item);
    return {
      ...item,
      note,
      rank: index + 1,
      chapterGateCount,
      chapterTitle: chapterLead?.title,
    };
  });
}

function pathChapterGateHeatfieldItems(lane, chapter, items) {
  const slots = [
    { x: 18, y: 58 },
    { x: 42, y: 24 },
    { x: 66, y: 68 },
    { x: 82, y: 38 },
    { x: 31, y: 78 },
  ];
  const chapterGateCount = (chapter?.counts?.gate ?? 0) + (chapter?.counts?.service ?? 0);
  const laneShift = (lane?.id ?? "")
    .split("")
    .reduce((total, char) => total + char.charCodeAt(0), 0);
  return (items?.length ? items : pathChapterGateStackItems(lane, chapter)).slice(0, 5).map((item, index) => {
    const slot = slots[index % slots.length];
    const pressure = Math.min(
      100,
      Math.max(16, Math.round(item.urgency ?? chapterGateCount * 14 + (index + 1) * 11))
    );
    const severity =
      item.severity === "blocker" || item.tone === "gated"
        ? "blocker"
        : item.severity === "review" || item.category === "review"
          ? "review"
          : "watch";
    return {
      ...item,
      pressure,
      size: Math.round(20 + pressure * 0.14),
      severity,
      x: Math.max(9, Math.min(91, slot.x + ((laneShift + index * 7) % 9) - 4)),
      y: Math.max(12, Math.min(88, slot.y + ((laneShift + index * 5) % 11) - 5)),
      signal: stateLabel(item.category ?? item.kind ?? severity),
      shortLabel: compactText(item.label ?? item.title ?? item.category ?? "Gate", 24),
    };
  });
}

function renderPathChapterGateHeatfield(lane, chapter, items, peakPressure) {
  const heatItems = pathChapterGateHeatfieldItems(lane, chapter, items);
  const blockerCount = heatItems.filter((item) => item.severity === "blocker").length;
  const reviewCount = heatItems.filter((item) => item.severity === "review").length;
  const chapterGateCount = (chapter?.counts?.gate ?? 0) + (chapter?.counts?.service ?? 0);
  const heatLabel = blockerCount
    ? `${formatNumber(blockerCount)} hot ping${blockerCount === 1 ? "" : "s"}`
    : reviewCount
      ? `${formatNumber(reviewCount)} review ping${reviewCount === 1 ? "" : "s"}`
      : "watch field clear";
  return `
    <div class="path-chapter-gate-heatfield" aria-label="Chapter Gate Heatfield" style="--gate-heat-art:url('./assets/system/path-chapter-gate-heatfield-20260618.png'); --gate-heat-pressure:${Math.min(100, peakPressure ?? 0)}%">
      <div class="path-chapter-gate-heat-copy">
        <span>Chapter Gate Heatfield</span>
        <strong>${escapeHtml(heatLabel)}</strong>
        <em>${formatNumber(chapterGateCount)} chapter gates scanned</em>
      </div>
      <div class="path-chapter-gate-scan" aria-hidden="true">
        <b class="path-chapter-gate-sweep"></b>
        ${heatItems
          .map(
            (item) => `
              <span class="path-chapter-gate-ping ${escapeHtml(item.severity)}" style="--gate-x:${item.x}%; --gate-y:${item.y}%; --gate-p:${item.pressure}%; --gate-size:${item.size}px">
                <i>${formatNumber(item.rank ?? item.index ?? 1)}</i>
              </span>`
          )
          .join("")}
      </div>
      <div class="path-chapter-gate-heat-key">
        ${heatItems
          .map(
            (item) => `
              <span class="${escapeHtml(item.severity)}">
                <strong>${escapeHtml(item.shortLabel)}</strong>
                <em>${escapeHtml(item.signal)} / ${formatNumber(item.pressure)}</em>
              </span>`
          )
          .join("")}
      </div>
    </div>`;
}

function renderPathChapterGateStack(lane, chapter) {
  if (!chapter) return "";
  const items = pathChapterGateStackItems(lane, chapter);
  const blockerCount = items.filter((item) => item.severity === "blocker" || item.tone === "gated").length;
  const reviewCount = items.filter((item) => item.severity === "review" || item.category === "review").length;
  const chapterGateCount = (chapter.counts?.gate ?? 0) + (chapter.counts?.service ?? 0);
  const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id);
  const peakPressure = Math.max(...items.map((item) => item.urgency ?? 0), 0);
  return `
    <section class="path-chapter-gate-stack ${blockerCount ? "gated" : "scouting"}" aria-label="Chapter Gate Stack" style="--gate-stack-a:${escapeHtml(lane.visual?.accent ?? "#44d7c9")}; --gate-stack-b:${escapeHtml(lane.visual?.accentAlt ?? "#f4ba55")}; --gate-stack-pressure:${Math.min(100, peakPressure)}%">
      <div class="path-chapter-gate-head">
        <div>
          <span>Chapter Gate Stack</span>
          <strong>${escapeHtml(blockerCount ? `${formatNumber(blockerCount)} blocker signals` : "Route watch clear")}</strong>
        </div>
        <em>${formatNumber(chapterGateCount)} chapter gates</em>
      </div>
      <div class="path-chapter-gate-meter" aria-hidden="true"><i></i></div>
      <div class="path-chapter-gate-stats">
        <span><strong>${formatNumber(blockerCount)}</strong><em>block</em></span>
        <span><strong>${formatNumber(reviewCount)}</strong><em>review</em></span>
        <span><strong>${formatNumber(peakPressure)}</strong><em>pressure</em></span>
      </div>
      ${renderPathChapterGateHeatfield(lane, chapter, items, peakPressure)}
      <div class="path-chapter-gate-list">
        ${items
          .map(
            (item) => `
              <article class="path-chapter-gate-card ${escapeHtml(item.severity ?? item.tone)} ${escapeHtml(item.category ?? "review")}">
                <i>${formatNumber(item.rank)}</i>
                <div>
                  <span>${escapeHtml(stateLabel(item.category ?? item.kind))} - ${escapeHtml(stateLabel(item.tone))}</span>
                  <strong>${escapeHtml(compactText(item.title, 58))}</strong>
                  <em>${escapeHtml(compactText(item.nextAction ?? item.body, 126))}</em>
                  ${item.note?.text ? `<small>${escapeHtml(compactText(item.note.text, 96))}</small>` : ""}
                </div>
              </article>`
          )
          .join("")}
      </div>
      <div class="path-chapter-gate-actions">
        <button class="tool-button" type="button" data-detail-view="overview" title="Open Gate Radar">GATE</button>
        <button class="tool-button" type="button" data-stage-lane-command="${escapeHtml(lane.id)}" title="Stage blocker review">${staged ? "OK" : "Q"}</button>
        <button class="tool-button" type="button" data-detail-view="comms" title="Open command deck">COM</button>
      </div>
    </section>`;
}

function pathChapterTaskBoardItems(lane, chapter) {
  const chapterTasks = (chapter?.items ?? [])
    .filter((item) => pathEventGlyphType(item) === "task")
    .map((item) => ({
      id: item.id ?? pathEventKey(item),
      title: item.title ?? "Chapter task",
      status: item.status ?? "recorded",
      priority: item.priority ?? 64,
      nextAction: item.summary ?? item.artifact ?? "Review this chapter task record.",
      ownerAgentId: lane.ownerAgentId,
      source: "chapter",
      time: item.time,
    }));
  const recentTasks = (lane.recentTasks ?? []).map((task) => ({
    id: task.id,
    title: task.title,
    status: task.status,
    priority: task.priority,
    nextAction: task.nextAction,
    ownerAgentId: task.ownerAgentId ?? lane.ownerAgentId,
    source: "lane",
    time: task.updatedAt ?? task.createdAt,
  }));
  const seen = new Set();
  return [...chapterTasks, ...recentTasks]
    .filter((task) => {
      const key = task.id ?? task.title;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    })
    .slice(0, 5);
}

function taskBoardTone(task) {
  if (task.status === "complete" || task.status === "completed") return "unlocked";
  if (task.status === "blocked" || task.status === "needs_review") return "gated";
  if (task.status === "active" || task.status === "in_progress" || task.status === "running") return "advancing";
  return "scouting";
}

function renderPathChapterTaskBoard(lane, chapter) {
  if (!chapter) return "";
  const tasks = pathChapterTaskBoardItems(lane, chapter);
  const completeCount = tasks.filter((task) => taskBoardTone(task) === "unlocked").length;
  const gatedCount = tasks.filter((task) => taskBoardTone(task) === "gated").length;
  const activeCount = tasks.filter((task) => taskBoardTone(task) === "advancing").length;
  const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id);
  const owner = laneAgents(lane)[0];
  return `
    <section class="path-chapter-task-board ${gatedCount ? "gated" : activeCount ? "advancing" : "scouting"}" aria-label="Chapter Task Board" style="--task-board-a:${escapeHtml(lane.visual?.accent ?? "#44d7c9")}; --task-board-b:${escapeHtml(lane.visual?.accentAlt ?? "#f4ba55")}">
      <div class="path-chapter-task-head">
        <div>
          <span>Chapter Task Board</span>
          <strong>${escapeHtml(tasks.length ? `${formatNumber(tasks.length)} tracked tasks` : "No task cards yet")}</strong>
        </div>
        <em>${escapeHtml(owner?.visual?.callsign ?? lane.ownerAgentId ?? "local")}</em>
      </div>
      <div class="path-chapter-task-stats">
        <span><strong>${formatNumber(activeCount)}</strong><em>active</em></span>
        <span><strong>${formatNumber(gatedCount)}</strong><em>gated</em></span>
        <span><strong>${formatNumber(completeCount)}</strong><em>done</em></span>
      </div>
      <div class="path-chapter-task-list">
        ${
          tasks.length
            ? tasks
                .map((task, index) => {
                  const tone = taskBoardTone(task);
                  return `
                    <article class="path-chapter-task-card ${escapeHtml(tone)}">
                      <i>${formatNumber(index + 1)}</i>
                      <div>
                        <span>${escapeHtml(stateLabel(task.status))} - P${formatNumber(task.priority ?? 0)} - ${escapeHtml(task.source)}</span>
                        <strong>${escapeHtml(compactText(task.title, 62))}</strong>
                        <em>${escapeHtml(compactText(task.nextAction ?? "No next action recorded.", 132))}</em>
                        <small>${escapeHtml(compactText(task.ownerAgentId ?? lane.ownerAgentId ?? "unassigned", 66))}</small>
                      </div>
                    </article>`;
                })
                .join("")
            : `<article class="path-chapter-task-card scouting"><i>0</i><div><span>watch</span><strong>No task records</strong><em>Future chapter task records and lane recentTasks will appear here.</em></div></article>`
        }
      </div>
      <div class="path-chapter-task-actions">
        <button class="tool-button" type="button" data-detail-view="trail" title="Open full lane trail">TRL</button>
        <button class="tool-button" type="button" data-stage-lane-command="${escapeHtml(lane.id)}" title="Stage task review">${staged ? "OK" : "Q"}</button>
        <button class="tool-button" type="button" data-detail-view="comms" title="Open command deck">COM</button>
      </div>
    </section>`;
}

function pathChapterFilteredRecords(lane, chapter) {
  const lens = pathChapterRecordLens(lane, chapter);
  if (lens === "all") return chapter?.items ?? [];
  return (chapter?.items ?? []).filter((item) => pathEventGlyphType(item) === lens);
}

function renderPathChapterRunway(lane, chapter, filteredRecords) {
  if (!chapter) return "";
  const lens = pathChapterRecordLens(lane, chapter);
  const limit = pathChapterRunwayLimit(lane, chapter, lens);
  const visible = filteredRecords.slice(0, limit);
  const remaining = Math.max(0, filteredRecords.length - visible.length);
  const focusedKey = state.pathEventFocusByLane[lane.id];
  const focusedIndex = filteredRecords.findIndex((item) => pathEventKey(item) === focusedKey);
  const activeIndex = Math.max(0, focusedIndex);
  const activeKey = focusedIndex >= 0 ? focusedKey : pathEventKey(filteredRecords[0]);
  const completePercent = filteredRecords.length ? Math.round(((Math.min(activeIndex + 1, filteredRecords.length)) / filteredRecords.length) * 100) : 0;
  return `
    <div class="path-chapter-runway" aria-label="Chapter Runway" style="--chapter-runway-progress:${completePercent}%">
      <div class="path-chapter-runway-head">
        <div>
          <span>Chapter Runway</span>
          <strong>${escapeHtml(lens === "all" ? "Full event chain" : `${stateLabel(lens)} chain`)}</strong>
        </div>
        <em>${filteredRecords.length ? `${formatNumber(activeIndex + 1)} / ${formatNumber(filteredRecords.length)}` : "0 / 0"}</em>
      </div>
      <div class="path-chapter-runway-track" aria-hidden="true"><i></i></div>
      <div class="path-chapter-runway-list">
        ${
          visible.length
            ? visible
                .map((item, index) => {
                  const eventKey = pathEventKey(item);
                  const type = pathEventGlyphType(item);
                  const active = eventKey === activeKey;
                  const passed = filteredRecords.findIndex((record) => pathEventKey(record) === eventKey) <= activeIndex;
                  return `
                    <button class="path-chapter-runway-node ${escapeHtml(type)} ${active ? "active" : ""} ${passed ? "passed" : ""}" type="button" data-path-chapter-runway-focus="${escapeHtml(eventKey)}" data-path-chapter-runway-lane="${escapeHtml(lane.id)}" data-path-chapter-key="${escapeHtml(chapter.key)}" aria-pressed="${active ? "true" : "false"}" title="Focus chapter runway stage ${formatNumber(index + 1)}">
                      ${pathEventGlyphMarkup(item, "path-chapter-runway-glyph")}
                      <span>
                        <strong>${formatNumber(index + 1)}</strong>
                        <em>${escapeHtml(stateLabel(type))}</em>
                      </span>
                    </button>`;
                })
                .join("")
            : `<span class="path-chapter-runway-empty"><strong>No stages</strong><em>The active chapter lens has no sequence records.</em></span>`
        }
      </div>
      <div class="path-chapter-runway-actions">
        ${
          remaining
            ? `<button class="expand-button" type="button" data-path-chapter-runway-reveal="${escapeHtml(chapter.key)}" data-path-chapter-runway-lane="${escapeHtml(lane.id)}">Extend runway by ${formatNumber(Math.min(12, remaining))}</button>`
            : `<p class="small-muted trail-end">Runway is fully charted for this lens.</p>`
        }
      </div>
    </div>`;
}

function renderPathChapterLevelClusters(lane, chapters, focused, visible, hidden, expanded) {
  const focusIndex = Math.max(0, chapters.findIndex((chapter) => chapter.key === focused?.key));
  const totalRecords = chapters.reduce((sum, chapter) => sum + chapter.items.length, 0);
  return `
    <div class="path-chapter-level-clusters" aria-label="Compact chapter level clusters">
      <div class="path-chapter-cluster-head">
        <div>
          <span>Level Clusters</span>
          <strong>${formatNumber(Math.max(1, focusIndex + 1))} / ${formatNumber(Math.max(1, chapters.length))} selected</strong>
        </div>
        <em>${formatNumber(totalRecords)} records indexed</em>
      </div>
      <div class="path-chapter-cluster-rail">
        ${
          visible
            .map((chapter, index) => {
              const active = focused?.key === chapter.key;
              const tone = pathChapterTone(chapter);
              const progress = Math.max(8, Math.min(100, Math.round((chapter.items.length / Math.max(totalRecords, 1)) * 260)));
              return `
                <button class="path-chapter-level-cluster ${escapeHtml(tone)} ${active ? "active" : ""}" type="button" data-path-chapter-focus="${escapeHtml(chapter.key)}" data-path-chapter-lane="${escapeHtml(lane.id)}" aria-pressed="${active ? "true" : "false"}" style="--chapter-cluster-progress:${progress}%;" title="Focus ${escapeHtml(chapter.label)} cluster">
                  <i>${formatNumber(index + 1)}</i>
                  <span>
                    <strong>${escapeHtml(chapter.label)}</strong>
                    <em>${formatNumber(chapter.items.length)} records</em>
                  </span>
                </button>`;
            })
            .join("") ||
          `<span class="path-chapter-empty"><strong>Archive idle</strong><em>Chapter clusters appear after this lane records trail events.</em></span>`
        }
        ${hidden ? `<span class="path-chapter-more">+${formatNumber(hidden)} older</span>` : ""}
      </div>
    </div>`;
}

function renderPathChapterArchive(lane, trail) {
  const chapters = pathChapterArchiveItems(trail);
  const focused = focusedPathChapter(lane, chapters);
  const visible = chapters.slice(0, 7);
  const newest = focused?.items?.[0];
  const focusCounts = focused?.counts ?? {};
  const focusTone = focused ? pathChapterTone(focused) : "scouting";
  const hidden = Math.max(0, chapters.length - visible.length);
  const expanded = pathChapterArchiveExpanded(lane);
  return `
    <article class="path-chapter-archive ${escapeHtml(focusTone)} ${expanded ? "is-expanded" : "is-compact"}" style="--chapter-archive-art:url('./assets/system/path-chapter-archive-20260618.png')">
      <div class="path-chapter-archive-copy">
        <div class="lane-button-top">
          <div>
            <p class="eyebrow">Chapter Archive</p>
            <h3>${focused ? `${escapeHtml(focused.label)} - ${formatNumber(focused.items.length)} route records` : "No chapters yet"}</h3>
          </div>
          <span class="badge ${escapeHtml(focusTone)}">${focused ? stateLabel(focusTone) : "empty"}</span>
        </div>
        <p>${escapeHtml(compactText(newest?.summary ?? newest?.title ?? "As new tasks, proofs, blockers, and outcomes arrive, this archive will split the lane trail into playable chapters.", 190))}</p>
        <div class="path-chapter-stats">
          <span><strong>${formatNumber(chapters.length)}</strong><em>chapters</em></span>
          <span><strong>${formatNumber(focusCounts.proof ?? 0)}</strong><em>proofs</em></span>
          <span><strong>${formatNumber((focusCounts.gate ?? 0) + (focusCounts.service ?? 0))}</strong><em>gates</em></span>
          <span><strong>${formatNumber(focusCounts.outcome ?? 0)}</strong><em>unlocks</em></span>
        </div>
        <div class="path-chapter-expand">
          <button class="expand-button" type="button" data-path-chapter-expand="${expanded ? "collapse" : "expand"}" data-path-chapter-lane="${escapeHtml(lane.id)}">
            ${expanded ? "Collapse dossier" : "Expand selected chapter dossier"}
          </button>
          <button class="tool-button" type="button" data-detail-view="trail" title="Open full lane trail">TRL</button>
        </div>
      </div>
      <div class="path-chapter-list" aria-label="Path history chapters">
        ${
          visible
            .map((chapter, index) => {
              const active = focused?.key === chapter.key;
              const tone = pathChapterTone(chapter);
              const lead = chapter.items[0];
              return `
                <button class="path-chapter-card ${escapeHtml(tone)} ${active ? "active" : ""}" type="button" data-path-chapter-focus="${escapeHtml(chapter.key)}" data-path-chapter-lane="${escapeHtml(lane.id)}" aria-pressed="${active ? "true" : "false"}" title="Open ${escapeHtml(chapter.label)} chapter">
                  <i>${formatNumber(index + 1)}</i>
                  <span>
                    <strong>${escapeHtml(chapter.label)}</strong>
                    <em>${escapeHtml(compactText(lead?.title ?? "Route chapter", 48))}</em>
                    <small>${formatNumber(chapter.items.length)} records - ${formatNumber(chapter.counts.proof ?? 0)} proofs</small>
                  </span>
                </button>`;
            })
            .join("") ||
          `<span class="path-chapter-empty"><strong>Archive idle</strong><em>Chapter cards appear after this lane records trail events.</em></span>`
        }
        ${hidden ? `<span class="path-chapter-more">+${formatNumber(hidden)} older chapters in Trail</span>` : ""}
      </div>
      ${renderPathChapterLevelClusters(lane, chapters, focused, visible, hidden, expanded)}
      ${expanded ? renderPathChapterRecordDeck(lane, focused) : ""}
    </article>`;
}

function renderPathChapterRecordDeck(lane, chapter) {
  if (!chapter) return "";
  const focusedKey = state.pathEventFocusByLane[lane.id];
  const lens = pathChapterRecordLens(lane, chapter);
  const lensOptions = pathChapterRecordLensOptions(chapter);
  const filteredRecords = pathChapterFilteredRecords(lane, chapter);
  const limit = pathChapterRecordLimit(lane, chapter, lens);
  const records = filteredRecords.slice(0, limit);
  const remaining = Math.max(0, filteredRecords.length - records.length);
  return `
    <div class="path-chapter-record-deck" aria-label="Selected chapter records">
      <div class="path-chapter-record-head">
        <div>
          <span>Chapter Records</span>
          <strong>${escapeHtml(chapter.label)} dossier</strong>
        </div>
        <em>${formatNumber(records.length)} / ${formatNumber(filteredRecords.length)}</em>
      </div>
      <div class="path-chapter-record-lenses" aria-label="Filter selected chapter records">
        ${lensOptions
          .map(
            (option) => `
              <button class="path-chapter-lens ${lens === option.id ? "active" : ""}" type="button" data-path-chapter-lens="${escapeHtml(option.id)}" data-path-chapter-lane="${escapeHtml(lane.id)}" data-path-chapter-key="${escapeHtml(chapter.key)}" aria-pressed="${lens === option.id ? "true" : "false"}" ${option.count ? "" : "disabled"} title="Show ${escapeHtml(option.label)} records in this chapter">
                ${pathEventGlyphMarkup(option.icon ?? option.id, "path-chapter-lens-glyph")}
                <span>${escapeHtml(option.label)}</span>
                <strong>${formatNumber(option.count)}</strong>
              </button>`
          )
          .join("")}
      </div>
      ${renderPathChapterDepthRings(lane, chapter, filteredRecords, remaining)}
      ${renderPathChapterMilestoneLadder(lane, chapter)}
      ${renderPathChapterGamePortal(lane, chapter)}
      ${renderPathChapterQuestline(lane, chapter)}
      ${renderPathChapterSpoils(chapter)}
      ${renderPathChapterEvidenceVault(lane, chapter)}
      ${renderPathChapterCrewRelay(lane, chapter)}
      ${renderPathChapterCommandLog(lane, chapter)}
      ${renderPathChapterGateStack(lane, chapter)}
      ${renderPathChapterTaskBoard(lane, chapter)}
      ${renderPathChapterRunway(lane, chapter, filteredRecords)}
      <div class="path-chapter-record-list">
        ${
          records.length
            ? records
                .map((item, index) => {
                  const eventKey = pathEventKey(item);
                  const active = eventKey === focusedKey;
                  return `
                    <button class="path-chapter-record ${escapeHtml(pathEventGlyphType(item))} ${active ? "active" : ""}" type="button" data-path-event-focus="${escapeHtml(eventKey)}" aria-pressed="${active ? "true" : "false"}" title="Inspect chapter record">
                      ${pathEventGlyphMarkup(item, "path-chapter-record-glyph")}
                      <span>
                        <strong>${formatNumber(index + 1)}. ${escapeHtml(compactText(item.title, 56))}</strong>
                        <em>${escapeHtml(compactText(item.summary ?? item.artifact ?? "Recorded in this chapter.", 96))}</em>
                        <small>${escapeHtml(stateLabel(item.kind))} - ${escapeHtml(shortDate(item.time))}</small>
                      </span>
                    </button>`;
                })
                .join("")
            : `<span class="path-chapter-record-empty"><strong>No ${escapeHtml(stateLabel(lens))} records</strong><em>This chapter has no events for the active lens.</em></span>`
        }
      </div>
      <div class="path-chapter-record-actions">
        ${
          remaining
            ? `<button class="expand-button" type="button" data-path-chapter-reveal="${escapeHtml(chapter.key)}" data-path-chapter-lane="${escapeHtml(lane.id)}">Reveal ${formatNumber(Math.min(4, remaining))} more ${lens === "all" ? "chapter" : stateLabel(lens)} records</button>`
            : `<p class="small-muted trail-end">Chapter dossier is fully open.</p>`
        }
        <button class="tool-button" type="button" data-detail-view="trail" title="Open full lane trail">TRL</button>
      </div>
    </div>`;
}

function renderPathNodeIntel(lane, node, nodes) {
  if (!node) return "";
  const nodeIndex = Math.max(0, nodes.findIndex((item) => item.id === node.id));
  const relatedEvents = pathNodeRelatedEvents(lane, node);
  const eventContext = pathEventContext(lane, relatedEvents);
  const focusedEventKey = eventContext?.key ?? "";
  const visibleEvents = eventContext?.item && !relatedEvents.some((eventItem) => pathEventKey(eventItem) === focusedEventKey) ? [eventContext.item, ...relatedEvents].slice(0, 4) : relatedEvents;
  const actionLabel = node.kind === "gate" ? "RADAR" : node.kind === "unlock" ? "LOG" : "COM";
  const actionView = node.kind === "gate" ? "overview" : node.kind === "unlock" ? "chronicle" : "comms";
  return `
    <article class="path-brief-card path-node-intel ${escapeHtml(node.kind)} ${escapeHtml(node.status)}">
      <div class="lane-button-top">
        <div>
          <p class="eyebrow">Node Intel</p>
          <h3>${escapeHtml(compactText(node.title, 62))}</h3>
        </div>
        <span class="badge ${node.kind === "gate" ? "gated" : node.kind === "unlock" ? "unlocked" : "advancing"}">${formatNumber(nodeIndex + 1)} / ${formatNumber(nodes.length)}</span>
      </div>
      <div class="path-intel-meter">
        <span style="--path-intel-progress:${Math.round(((nodeIndex + 1) / Math.max(nodes.length, 1)) * 100)}%"></span>
      </div>
      <div class="path-intel-tags">
        <span>${escapeHtml(stateLabel(node.kind))}</span>
        <span>${escapeHtml(stateLabel(node.status))}</span>
        <span>level ${formatNumber(node.level ?? nodeIndex + 1)}</span>
      </div>
      <p>${escapeHtml(compactText(node.body, 190))}</p>
      ${node.note ? `<p class="path-note-preview">${escapeHtml(compactText(node.note.text, 128))}</p>` : ""}
      <div class="path-intel-events">
        <div class="path-intel-events-head">
          <span>Related Events</span>
          <strong>${formatNumber(visibleEvents.length)}</strong>
        </div>
        <div class="path-intel-event-list">
          ${visibleEvents.map((eventItem) => renderPathIntelEvent(eventItem, focusedEventKey)).join("") || `<span class="path-intel-event empty"><strong>No trail match</strong><em>Future lane records will appear here.</em></span>`}
        </div>
      </div>
      ${renderPathEventLens(eventContext)}
      <div class="path-intel-actions">
        <button class="tool-button" type="button" data-detail-view="${escapeHtml(actionView)}" title="Open related view">${escapeHtml(actionLabel)}</button>
        <button class="tool-button" type="button" data-detail-view="trail" title="Open lane trail">TRL</button>
        <button class="tool-button" type="button" data-path-node-focus="${escapeHtml(nodes[(nodeIndex + 1) % nodes.length]?.id ?? node.id)}" title="Focus next route node">NEXT</button>
      </div>
    </article>`;
}

function pathProofItems(lane) {
  return chronicleTrail(lane)
    .filter((item) => item.artifactPreview?.lines?.length)
}

function visiblePathProofItems(lane) {
  const limit = state.proofLimitByLane[lane.id] ?? 3;
  return pathProofItems(lane).slice(0, limit);
}

function renderPathProofCache(lane) {
  const allProofs = pathProofItems(lane);
  const proofs = visiblePathProofItems(lane);
  const remaining = Math.max(0, allProofs.length - proofs.length);
  return `
    <article class="path-brief-card path-proof-cache">
      <div class="lane-button-top">
        <div>
          <p class="eyebrow">Proof Cache</p>
          <h3>${allProofs.length ? `${formatNumber(proofs.length)} of ${formatNumber(allProofs.length)} previews visible` : "No artifact previews yet"}</h3>
        </div>
        <span class="badge ${proofs.length ? "unlocked" : "scouting"}">${proofs.length ? "proof" : "empty"}</span>
      </div>
      <div class="path-proof-list">
        ${
          proofs
            .map(
              (item) => `
                <button class="path-proof-item ${escapeHtml(item.kind)}" type="button" data-path-event-focus="${escapeHtml(pathEventKey(item))}" title="Inspect proof event">
                  <strong>${escapeHtml(compactText(item.artifactPreview.label ?? item.title, 48))}</strong>
                  <em>${escapeHtml(compactText(item.artifactPreview.lines[0] ?? item.summary, 82))}</em>
                </button>`
            )
            .join("") ||
          `<span class="path-proof-item empty"><strong>Awaiting local proof</strong><em>Text-like artifacts inside the repo root will appear here after snapshot generation.</em></span>`
        }
      </div>
      <div class="path-proof-actions">
        ${
          remaining
            ? `<button class="expand-button" type="button" data-expand-proof-cache="${escapeHtml(lane.id)}">Reveal ${formatNumber(Math.min(3, remaining))} more proof cards</button>`
            : `<p class="small-muted trail-end">Proof cache is caught up to this snapshot.</p>`
        }
        <button class="tool-button" type="button" data-detail-view="trail" title="Open full trail">TRL</button>
      </div>
    </article>`;
}

function pathReplayItems(lane) {
  const filter = state.pathReplayFilterByLane[lane.id] ?? "all";
  const items = [...chronicleTrail(lane)].reverse();
  if (filter === "all") return items;
  return items.filter((item) => pathEventGlyphType(item) === filter);
}

function pathReplayAllItems(lane) {
  return [...chronicleTrail(lane)].reverse();
}

function pathReplayFilterOptions(lane) {
  const items = pathReplayAllItems(lane);
  const counts = items.reduce((acc, item) => {
    const type = pathEventGlyphType(item);
    acc[type] = (acc[type] ?? 0) + 1;
    return acc;
  }, {});
  return [
    { id: "all", label: "All", count: items.length, icon: "trace" },
    { id: "proof", label: "Proof", count: counts.proof ?? 0 },
    { id: "service", label: "Service", count: counts.service ?? 0 },
    { id: "outcome", label: "Outcome", count: counts.outcome ?? 0 },
    { id: "task", label: "Task", count: counts.task ?? 0 },
    { id: "gate", label: "Gate", count: counts.gate ?? 0 },
    { id: "trace", label: "Trace", count: counts.trace ?? 0 },
  ];
}

function pathReplayQueueItems(items, index, limit = 4) {
  if (!items.length) return [];
  const count = Math.min(limit, items.length);
  return Array.from({ length: count }, (_, offset) => {
    const queueIndex = (index + offset) % items.length;
    return {
      item: items[queueIndex],
      index: queueIndex,
      current: offset === 0,
    };
  });
}

function pathReplayIndex(lane, total = pathReplayItems(lane).length) {
  if (!total) return 0;
  const stored = Number(state.pathReplayIndexByLane[lane.id]);
  if (Number.isFinite(stored)) return Math.min(Math.max(Math.round(stored), 0), total - 1);
  const focusedKey = state.pathEventFocusByLane[lane.id];
  const focusedIndex = focusedKey ? pathReplayItems(lane).findIndex((item) => pathEventKey(item) === focusedKey) : -1;
  return focusedIndex >= 0 ? focusedIndex : 0;
}

function setPathReplayIndex(lane, nextIndex, focusEvent = true) {
  const items = pathReplayItems(lane);
  if (!items.length) return null;
  const index = Math.min(Math.max(nextIndex, 0), items.length - 1);
  const item = items[index];
  state.pathReplayIndexByLane = { ...state.pathReplayIndexByLane, [lane.id]: index };
  if (focusEvent) {
    state.pathEventFocusByLane = { ...state.pathEventFocusByLane, [lane.id]: pathEventKey(item) };
  }
  return item;
}

function stopPathReplay(render = true) {
  if (state.pathReplayTimer) {
    clearInterval(state.pathReplayTimer);
    state.pathReplayTimer = null;
  }
  state.pathReplayPlayingLaneId = null;
  if (render) renderDetail();
}

function startPathReplay(laneId) {
  stopPathReplay(false);
  state.pathReplayPlayingLaneId = laneId;
  state.pathReplayTimer = window.setInterval(() => {
    const lane = state.snapshot?.lanes?.find((item) => item.id === state.pathReplayPlayingLaneId);
    if (!lane) {
      stopPathReplay(false);
      return;
    }
    const items = pathReplayItems(lane);
    if (!items.length) {
      stopPathReplay();
      return;
    }
    const current = pathReplayIndex(lane, items.length);
    setPathReplayIndex(lane, current >= items.length - 1 ? 0 : current + 1);
    renderDetail();
  }, 1700);
  renderDetail();
}

function pathEventGlyphType(item) {
  const kind = String(typeof item === "string" ? item : item?.kind ?? "").toLowerCase();
  const source = String(typeof item === "string" ? item : `${item?.kind ?? ""} ${item?.status ?? ""} ${item?.title ?? ""}`).toLowerCase();
  if (/evidence|proof/.test(kind)) return "proof";
  if (/outcome|unlock|trophy|complete/.test(source)) return "outcome";
  if (/service|request|approval|browser/.test(source)) return "service";
  if (/gate|blocker|risk|hold|review/.test(source)) return "gate";
  if (/task|checkpoint|job|work/.test(source)) return "task";
  if (/trace|event|trail|route/.test(kind || source)) return "trace";
  if (item?.artifactPreview || /artifact|packet|report/.test(source)) return "proof";
  return "trace";
}

function pathEventGlyphMarkup(item, className = "") {
  return `<i class="path-event-glyph glyph-${escapeHtml(pathEventGlyphType(item))} ${escapeHtml(className)}" aria-hidden="true"></i>`;
}

function renderPathRouteReplay(lane) {
  const items = pathReplayItems(lane);
  const total = items.length;
  const index = pathReplayIndex(lane, total);
  const item = items[index];
  const playing = state.pathReplayPlayingLaneId === lane.id;
  const filter = state.pathReplayFilterByLane[lane.id] ?? "all";
  const allTotal = pathReplayAllItems(lane).length;
  const filterOptions = pathReplayFilterOptions(lane);
  const queueItems = pathReplayQueueItems(items, index);
  const progress = total > 1 ? Math.round((index / (total - 1)) * 100) : total ? 100 : 0;
  const markerCount = Math.min(9, total);
  const markerIndexes = markerCount
    ? [...new Set(Array.from({ length: markerCount }, (_, markerIndex) => (markerCount === 1 ? 0 : Math.round((markerIndex / (markerCount - 1)) * (total - 1)))))]
    : [];
  return `
    <article class="path-brief-card path-route-replay ${playing ? "playing" : ""}" style="--route-replay-art:url('./assets/system/route-replay-chronometer-20260618.png')">
      <div class="lane-button-top">
        <div>
          <p class="eyebrow">Route Replay</p>
          <h3>${item ? `Stage ${formatNumber(index + 1)} of ${formatNumber(total)}` : filter === "all" ? "No route events yet" : `No ${escapeHtml(stateLabel(filter))} stages`}</h3>
        </div>
        <span class="badge ${playing ? "advancing" : filter !== "all" ? "unlocked" : item?.artifactPreview ? "unlocked" : "scouting"}">${playing ? "playing" : filter !== "all" ? stateLabel(filter) : item?.artifactPreview ? "proof" : "idle"}</span>
      </div>
      <div class="path-replay-filters" aria-label="Filter Route Replay stages">
        ${filterOptions
          .map(
            (option) => `
              <button class="path-replay-filter ${filter === option.id ? "active" : ""}" type="button" data-path-replay-filter="${escapeHtml(option.id)}" data-path-replay-lane="${escapeHtml(lane.id)}" aria-pressed="${filter === option.id ? "true" : "false"}" ${option.count ? "" : "disabled"} title="Show ${escapeHtml(option.label)} replay stages">
                ${pathEventGlyphMarkup(option.icon ?? option.id, "path-replay-filter-glyph")}
                <span>${escapeHtml(option.label)}</span>
                <strong>${formatNumber(option.count)}</strong>
              </button>`
          )
          .join("")}
      </div>
      <div class="path-replay-track" aria-hidden="true">
        <span style="--replay-progress:${progress}%"></span>
        ${markerIndexes
          .map((markerIndex) => {
            const markerItem = items[markerIndex];
            return `<i class="${markerIndex <= index ? "passed" : ""} ${markerIndex === index ? "current" : ""} ${escapeHtml(markerItem?.kind ?? "event")}" style="--marker-left:${total > 1 ? Math.round((markerIndex / (total - 1)) * 100) : 0}%"></i>`;
          })
          .join("")}
      </div>
      ${
        item
          ? `<button class="path-replay-event ${escapeHtml(item.kind)}" type="button" data-path-event-focus="${escapeHtml(pathEventKey(item))}" title="Inspect replay event">
              ${pathEventGlyphMarkup(item, "path-replay-glyph")}
              <span class="path-replay-event-copy">
                <strong>${escapeHtml(compactText(item.title, 62))}</strong>
                <em>${escapeHtml(compactText(item.summary ?? item.artifact ?? "Recorded in this lane route.", 120))}</em>
                <span>${escapeHtml(stateLabel(item.kind))} - ${escapeHtml(shortDate(item.time))}</span>
              </span>
            </button>`
          : `<div class="path-replay-event empty"><strong>Waiting for lane history</strong><em>Tasks, traces, outcomes, and proof artifacts will become playable route stages.</em></div>`
      }
      <div class="path-replay-queue" aria-label="Route Replay stage queue">
        <div class="path-replay-queue-head">
          <span>Stage Queue</span>
          <em>${formatNumber(queueItems.length)} queued</em>
        </div>
        <div class="path-replay-queue-list">
          ${
            queueItems.length
              ? queueItems
                  .map(
                    ({ item: queueItem, index: queueIndex, current }) => `
                      <button class="path-replay-queue-item ${current ? "current" : ""}" type="button" data-path-replay-jump="${queueIndex}" data-path-replay-lane="${escapeHtml(lane.id)}" title="Jump to stage ${formatNumber(queueIndex + 1)}">
                        ${pathEventGlyphMarkup(queueItem, "path-replay-queue-glyph")}
                        <span>
                          <strong>${current ? "Now" : `Stage ${formatNumber(queueIndex + 1)}`}</strong>
                          <em>${escapeHtml(compactText(queueItem.title, 48))}</em>
                          <small>${escapeHtml(stateLabel(queueItem.kind))} - ${escapeHtml(shortDate(queueItem.time))}</small>
                        </span>
                      </button>`
                  )
                  .join("")
              : `<div class="path-replay-queue-empty"><strong>Queue idle</strong><em>Replay stages will appear here as this lane builds history.</em></div>`
          }
        </div>
      </div>
      <div class="path-replay-stats">
        <span><strong>${formatNumber(total)}</strong><em>${filter === "all" ? "events" : "shown"}</em></span>
        <span><strong>${formatNumber(pathProofItems(lane).length)}</strong><em>proofs</em></span>
        <span><strong>${filter === "all" ? `${formatNumber(progress)}%` : `${formatNumber(total)}/${formatNumber(allTotal)}`}</strong><em>${filter === "all" ? "run" : "lens"}</em></span>
      </div>
      <div class="path-replay-controls">
        <button class="tool-button" type="button" data-path-replay-action="start" data-path-replay-lane="${escapeHtml(lane.id)}" ${total ? "" : "disabled"} title="Jump to first route event">I&lt;</button>
        <button class="tool-button" type="button" data-path-replay-action="back" data-path-replay-lane="${escapeHtml(lane.id)}" ${total ? "" : "disabled"} title="Step back one route event">BACK</button>
        <button class="tool-button primary" type="button" data-path-replay-action="toggle" data-path-replay-lane="${escapeHtml(lane.id)}" ${total ? "" : "disabled"} title="${playing ? "Pause route replay" : "Play route replay"}">${playing ? "PAUSE" : "PLAY"}</button>
        <button class="tool-button" type="button" data-path-replay-action="next" data-path-replay-lane="${escapeHtml(lane.id)}" ${total ? "" : "disabled"} title="Step forward one route event">NEXT</button>
        <button class="tool-button" type="button" data-path-replay-action="latest" data-path-replay-lane="${escapeHtml(lane.id)}" ${total ? "" : "disabled"} title="Jump to latest route event">&gt;I</button>
      </div>
    </article>`;
}

function renderPathIntelEvent(item, focusedEventKey) {
  const summary = item.summary ?? item.artifact ?? "Recorded in the lane trail.";
  const eventKey = pathEventKey(item);
  const selected = eventKey === focusedEventKey;
  return `
    <button class="path-intel-event ${escapeHtml(item.kind)} ${selected ? "is-selected" : ""}" type="button" data-path-event-focus="${escapeHtml(eventKey)}" aria-pressed="${selected ? "true" : "false"}" title="Inspect this related event">
      <strong>${escapeHtml(stateLabel(item.kind))} - ${escapeHtml(shortDate(item.time))}</strong>
      <em>${escapeHtml(compactText(item.title, 56))}</em>
      <small>${escapeHtml(compactText(summary, 92))}</small>
    </button>`;
}

function renderPathEventLens(context) {
  if (!context?.item) return "";
  const item = context.item;
  const artifact = item.artifact ? compactText(item.artifact, 104) : "No artifact linked";
  return `
    <div class="path-event-lens ${escapeHtml(item.kind)}">
      <div class="path-event-lens-head">
        ${pathEventGlyphMarkup(item, "path-event-lens-glyph")}
        <div>
          <span>Event Proof</span>
          <strong>${escapeHtml(compactText(item.title, 64))}</strong>
        </div>
        <em>${escapeHtml(stateLabel(item.status ?? item.kind))}</em>
      </div>
      <p>${escapeHtml(compactText(item.summary ?? "Recorded in the lane trail.", 170))}</p>
      <div class="path-event-proof-grid">
        <span><strong>${escapeHtml(stateLabel(item.kind))}</strong><em>type</em></span>
        <span><strong>${escapeHtml(shortDate(item.time))}</strong><em>time</em></span>
      </div>
      <code>${escapeHtml(artifact)}</code>
      ${renderPathArtifactPreview(item.artifactPreview)}
      <div class="path-event-nav">
        <button class="tool-button" type="button" data-path-event-step="newer" data-path-event-focus="${escapeHtml(context.newerKey)}" ${context.newerKey ? "" : "disabled"} title="Inspect newer trail event">NEWER</button>
        <span class="path-event-position">${formatNumber(context.index + 1)} / ${formatNumber(context.total || 1)}</span>
        <button class="tool-button" type="button" data-path-event-step="older" data-path-event-focus="${escapeHtml(context.olderKey)}" ${context.olderKey ? "" : "disabled"} title="Inspect older trail event">OLDER</button>
      </div>
    </div>`;
}

function renderPathArtifactPreview(preview) {
  if (!preview?.lines?.length) return "";
  return `
    <div class="path-artifact-preview">
      <div class="path-artifact-preview-head">
        <span>Artifact Preview</span>
        <strong>${escapeHtml(compactText(preview.label ?? "artifact", 38))}</strong>
      </div>
      <ul>
        ${preview.lines.map((line) => `<li>${escapeHtml(compactText(line, 112))}</li>`).join("")}
      </ul>
      <em>${escapeHtml(stateLabel(preview.kind ?? "file"))}${preview.truncated ? " preview" : ""}</em>
    </div>`;
}

function renderPathHandoffPanel(lane, pathNotes) {
  const agents = laneAgents(lane);
  const owner = agents[0];
  const suggestion = bestLaneDispatchSuggestion(lane);
  const staged = state.stagedDispatches.some((draft) => draft.laneId === lane.id || draft.sourceId === suggestion.id);
  const callsign = owner?.visual?.callsign ?? lane.ownerAgentId ?? "Unassigned lane manager";
  const specialty = owner?.visual?.specialty ?? (owner ? stateLabel(owner.role_id) : "Local command target");
  const gateCount = lane.counts?.blockers ?? gateRadarItems(lane).filter((item) => item.tone === "gated").length;
  const noteCount = pathNotes.length;
  return `
    <article class="path-brief-card path-handoff-panel ${staged ? "staged" : ""}" style="--path-handoff-beacon:url('./assets/system/path-handoff-beacon-20260618.png')">
      <div class="lane-button-top">
        <div>
          <p class="eyebrow">Route Handoff</p>
          <h3>${escapeHtml(compactText(callsign, 54))}</h3>
        </div>
        <span class="badge ${staged ? "staged" : gateCount ? "gated" : "advancing"}">${staged ? "staged" : "ready"}</span>
      </div>
      <div class="path-handoff-agent">
        ${owner ? agentAvatarMarkup(owner, lane, "path-handoff-avatar") : avatarMarkup(lane, "path-handoff-avatar")}
        <div>
          <strong>${escapeHtml(compactText(specialty, 72))}</strong>
          <span>${escapeHtml(lane.ownerThreadId ?? owner?.thread_id ?? "No thread linked")}</span>
        </div>
      </div>
      <div class="path-handoff-stats">
        <span><strong>${formatNumber(gateCount)}</strong><em>gates</em></span>
        <span><strong>${formatNumber(noteCount)}</strong><em>notes</em></span>
        <span><strong>${formatNumber(suggestion.urgency ?? 0)}</strong><em>urgency</em></span>
      </div>
      <p>${escapeHtml(compactText(suggestion.reason ?? chronicleNextAction(lane), 170))}</p>
      <div class="path-handoff-actions">
        <button class="tool-button" type="button" data-path-handoff-stage="${escapeHtml(lane.id)}" title="Stage local route handoff">${staged ? "OK" : "Q"}</button>
        <button class="tool-button" type="button" data-detail-view="comms" title="Open command deck">COM</button>
      </div>
    </article>`;
}

function renderPathNotePanel(pathNotes) {
  return `
    <article class="path-brief-card path-note-panel">
      <div class="lane-button-top">
        <div>
          <p class="eyebrow">Path Notes</p>
          <h3>${pathNotes.length ? `${formatNumber(pathNotes.length)} local pins on this route` : "No local pins yet"}</h3>
        </div>
        <span class="badge scouting">local only</span>
      </div>
      <div class="path-note-list">
        ${
          pathNotes
            .map(
              ({ item, note }) => `
                <span class="path-note-item ${escapeHtml(item.tone)}">
                  <strong>${escapeHtml(compactText(item.title, 44))}</strong>
                  <em>${escapeHtml(compactText(note.text, 96))}</em>
                </span>`
            )
            .join("") ||
          `<span class="path-note-item empty"><strong>Gate Radar</strong><em>Add notes to blocker signals and they will appear on this route board.</em></span>`
        }
      </div>
      <button class="tool-button" type="button" data-detail-view="overview" title="Open Gate Radar">RADAR</button>
    </article>`;
}

function renderPathMapNode(node, index, focusedId) {
  const active = node.id === focusedId;
  const charge = node.status === "complete" ? 100 : node.kind === "gate" || node.status === "gated" ? 48 : node.kind === "unlock" ? 86 : 64;
  return `
    <button class="path-node ${escapeHtml(node.kind)} ${escapeHtml(node.status)} ${node.note ? "noted" : ""} ${active ? "is-focused" : ""}" type="button" data-path-node-focus="${escapeHtml(node.id)}" style="--path-index:${index}; --path-node-charge:${charge}%;" aria-pressed="${active ? "true" : "false"}">
      <i>${formatNumber(index + 1)}</i>
      <div>
        <div class="path-node-meta">
          <span>${escapeHtml(node.meta)}</span>
          ${node.note ? `<b class="path-note-badge">note</b>` : ""}
        </div>
        <h3>${escapeHtml(compactText(node.title, 58))}</h3>
        <p>${escapeHtml(compactText(node.body, 126))}</p>
        ${node.note ? `<p class="path-note-preview">${escapeHtml(compactText(node.note.text, 118))}</p>` : ""}
      </div>
    </button>`;
}

function renderPathMiniEvent(item) {
  return `
    <span class="${escapeHtml(item.kind)}">
      ${pathEventGlyphMarkup(item, "path-mini-glyph")}
      <span>
        <strong>${escapeHtml(stateLabel(item.kind))}</strong>
        <em>${escapeHtml(compactText(item.title, 48))}</em>
      </span>
    </span>`;
}

function renderChronicleView(lane) {
  const chronicle = chronicleViewModel(lane);
  const requestedStage = state.chronicleStageViewByLane[lane.id] ?? "signal";
  const activeStage = chronicle.stages.some((stage) => stage.id === requestedStage) ? requestedStage : "signal";
  return `
    ${renderChronicleStageDock(lane, activeStage, chronicle.counts)}
    ${renderChronicleStagePanel(lane, activeStage, chronicle)}`;
}

function chronicleViewModel(lane) {
  const trail = chronicleTrail(lane);
  const visibleLimit = state.trailLimitByLane[lane.id] ?? 18;
  const visibleTrail = trail.slice(0, visibleLimit);
  const kindCounts = chronicleKindCounts(trail);
  const phase = chroniclePhase(lane, trail);
  const checkpoints = lane.quest?.checkpoints ?? [];
  const gates = lane.gateMap?.slice(0, 4) ?? [];
  const newest = trail[0];
  const nextAction = chronicleNextAction(lane);
  const checkpointProgress = checkpoints.length
    ? Math.round((checkpoints.filter((checkpoint) => checkpoint.status === "complete").length / checkpoints.length) * 100)
    : lane.progress ?? 0;
  const signalCards = [
    { label: "Trail Depth", value: formatNumber(trail.length), note: "recorded steps" },
    { label: "Unlocks", value: formatNumber(lane.counts?.outcomes ?? 0), note: "outcomes banked" },
    { label: "Gates", value: formatNumber(lane.counts?.blockers ?? 0), note: "blockers visible" },
    { label: "XP", value: formatNumber(lane.score ?? 0), note: `level ${lane.level}` },
  ];
  const eventTotal = Object.values(kindCounts).reduce((sum, count) => sum + count, 0);
  return {
    trail,
    visibleTrail,
    visibleLimit,
    kindCounts,
    phase,
    checkpoints,
    gates,
    newest,
    nextAction,
    checkpointProgress,
    signalCards,
    eventTotal,
    counts: {
      trail: trail.length,
      checkpoints: checkpoints.length,
      gates: gates.length || lane.counts?.blockers || 0,
      stream: visibleTrail.length,
    },
    stages: [
      { id: "signal", label: "SIGNAL", title: "Current run signal", value: formatNumber(trail.length) },
      { id: "route", label: "ROUTE", title: "Checkpoint route", value: `${formatNumber(checkpointProgress)}%` },
      { id: "gates", label: "GATES", title: "Blocker gates", value: formatNumber(gates.length || lane.counts?.blockers || 0) },
      { id: "stream", label: "STREAM", title: "Event stream", value: formatNumber(visibleTrail.length) },
    ],
  };
}

function renderChronicleStageDock(lane, activeStage, counts) {
  const stages = [
    { id: "signal", label: "SIGNAL", title: "Current run signal", value: formatNumber(counts.trail) },
    { id: "route", label: "ROUTE", title: "Checkpoint route", value: formatNumber(counts.checkpoints) },
    { id: "gates", label: "GATES", title: "Blocker gates", value: formatNumber(counts.gates) },
    { id: "stream", label: "STREAM", title: "Event stream", value: formatNumber(counts.stream) },
  ];
  return `
    <section class="chronicle-stage-dock" aria-label="Chronicle stage dock" style="${laneStyle(lane)}">
      <div class="chronicle-stage-meter">
        <strong>${escapeHtml(lane.visual?.realm ?? lane.department)}</strong>
        <span>${formatNumber(counts.trail)} logs / ${formatNumber(counts.gates)} gates</span>
      </div>
      <div class="chronicle-stage-buttons" role="tablist" aria-label="Chronicle modules">
        ${stages
          .map(
            (stage) => `
              <button class="chronicle-stage-button ${stage.id === activeStage ? "active" : ""}" type="button" role="tab" aria-selected="${stage.id === activeStage ? "true" : "false"}" data-chronicle-stage="${escapeHtml(stage.id)}" title="${escapeHtml(stage.title)}">
                <strong>${escapeHtml(stage.label)}</strong>
                <span>${escapeHtml(stage.value)}</span>
              </button>`
          )
          .join("")}
      </div>
    </section>`;
}

function renderChronicleStagePanel(lane, activeStage, chronicle) {
  const {
    visibleTrail,
    kindCounts,
    phase,
    checkpoints,
    gates,
    newest,
    nextAction,
    checkpointProgress,
    signalCards,
    eventTotal,
    trail,
  } = chronicle;
  const signalPanel = `
        <div class="chronicle-hero">
          ${avatarMarkup(lane, "chronicle-avatar")}
          <div>
            <p class="eyebrow">Current Run</p>
            <h3>${escapeHtml(newest?.title ?? lane.name)}</h3>
            <p>${escapeHtml(compactText(newest?.summary ?? phase.summary, 220))}</p>
          </div>
          <div class="chronicle-progress" style="--chronicle-progress:${checkpointProgress}%">
            <strong>${formatNumber(checkpointProgress)}%</strong>
            <span>quest</span>
          </div>
        </div>

        <div class="chronicle-signal-grid">
          ${signalCards.map(renderChronicleSignal).join("")}
        </div>`;
  const panels = {
    signal: signalPanel,
    route: `
        <div class="chronicle-mapline" style="--chronicle-progress:${checkpointProgress}%">
          ${checkpoints.map(renderChronicleCheckpoint).join("") || `<p class="small-muted">No checkpoints yet. New lanes can inherit this board once quest data exists.</p>`}
        </div>`,
    gates: `
        <div class="chronicle-gates">
          ${gates.length ? gates.map(renderChronicleGate).join("") : `<article class="chronicle-gate cleared"><strong>No active blocker cells</strong><span>This lane has no gate-map blockers in the current snapshot.</span></article>`}
        </div>`,
    stream: `
        <div class="chronicle-stream">
          ${visibleTrail.map(renderChronicleStreamItem).join("") || `<p class="small-muted">No recorded lane events yet.</p>`}
        </div>
        ${
          visibleTrail.length < trail.length
            ? `<button class="expand-button" type="button" data-expand-trail="${escapeHtml(lane.id)}">Reveal ${Math.min(18, trail.length - visibleTrail.length)} more chronicle steps</button>`
            : `<p class="small-muted trail-end">Chronicle is caught up to the current snapshot. Future bot records will extend it automatically.</p>`
        }`,
  };
  return `
    <section class="detail-section chronicle-stage-panel" data-chronicle-stage-view="${escapeHtml(activeStage)}">
      <div class="lane-button-top">
        <div>
          <p class="eyebrow">Lane Chronicle</p>
          <h3>${escapeHtml(phase.label)}</h3>
        </div>
        <span class="badge ${escapeHtml(phase.tone)}">${escapeHtml(stateLabel(lane.state))}</span>
      </div>
      <div class="chronicle-board" style="${laneStyle(lane)}">
        ${panels[activeStage] ?? panels.signal}
      </div>
    </section>`;
}

function renderChronicleSignal(signal) {
  return `
    <article class="chronicle-signal">
      <strong>${escapeHtml(signal.value)}</strong>
      <span>${escapeHtml(signal.label)}</span>
      <em>${escapeHtml(signal.note)}</em>
    </article>`;
}

function renderChronicleCheckpoint(checkpoint, index) {
  return `
    <article class="chronicle-node ${escapeHtml(checkpoint.status)}">
      <span>${index + 1}</span>
      <h3>${escapeHtml(checkpoint.title)}</h3>
      <p>${escapeHtml(compactText(checkpoint.description, 110))}</p>
    </article>`;
}

function renderChronicleKindBar(kind, count, total) {
  const width = total ? Math.max(6, Math.round((count / total) * 100)) : 0;
  return `
    <div class="chronicle-kind ${escapeHtml(kind)}" style="--kind-progress:${width}%">
      <span>${escapeHtml(stateLabel(kind))}</span>
      <strong>${formatNumber(count)}</strong>
      <i></i>
    </div>`;
}

function renderChronicleGate(gate) {
  return `
    <article class="chronicle-gate">
      <strong>${escapeHtml(compactText(gate.workerType || gate.id, 48))}</strong>
      <span>${escapeHtml(compactText(gate.gate, 92))}</span>
      <em>${escapeHtml(compactText(gate.nextAction || gate.route, 120))}</em>
    </article>`;
}

function renderChronicleStreamItem(item, index) {
  return `
    <article class="chronicle-stream-item ${escapeHtml(item.kind)}" style="--trail-index:${index}">
      <span>${escapeHtml(stateLabel(item.kind))}</span>
      <div>
        <h3>${escapeHtml(compactText(item.title, 74))}</h3>
        <p>${escapeHtml(shortDate(item.time))} - ${escapeHtml(stateLabel(item.status))}</p>
      </div>
    </article>`;
}

function pathMemoryLensOptions(trail) {
  const countFor = (predicate) => trail.filter((item) => predicate(pathEventGlyphType(item))).length;
  return [
    { id: "all", label: "All", count: trail.length, predicate: () => true },
    { id: "gates", label: "Gates", count: countFor((type) => type === "gate" || type === "service"), predicate: (type) => type === "gate" || type === "service" },
    { id: "proof", label: "Proof", count: countFor((type) => type === "proof"), predicate: (type) => type === "proof" },
    { id: "wins", label: "Wins", count: countFor((type) => type === "outcome"), predicate: (type) => type === "outcome" },
    { id: "tasks", label: "Tasks", count: countFor((type) => type === "task"), predicate: (type) => type === "task" },
    { id: "traces", label: "Traces", count: countFor((type) => type === "trace"), predicate: (type) => type === "trace" },
  ];
}

function pathMemoryFilteredItems(lane, trail) {
  const lens = state.pathMemoryLensByLane[lane.id] ?? "all";
  const option = pathMemoryLensOptions(trail).find((item) => item.id === lens) ?? pathMemoryLensOptions(trail)[0];
  return trail.filter((item) => option.predicate(pathEventGlyphType(item)));
}

function pathMemoryStats(lane, trail) {
  const chapters = pathChapterArchiveItems(trail);
  const kindCounts = chronicleKindCounts(trail);
  return [
    { label: "steps", value: formatNumber(trail.length), note: "recorded" },
    { label: "chapters", value: formatNumber(chapters.length), note: "grouped" },
    { label: "gates", value: formatNumber(lane.counts?.blockers ?? kindCounts.service_request ?? 0), note: "review" },
    { label: "proof", value: formatNumber((lane.counts?.evidence ?? 0) + (lane.counts?.outcomes ?? 0)), note: "packets" },
    { label: "level", value: `L${formatNumber(lane.level ?? 1)}`, note: `${formatNumber(lane.progress ?? 0)}%` },
  ];
}

function renderPathMemoryCodex(lane, trail) {
  const lens = state.pathMemoryLensByLane[lane.id] ?? "all";
  const options = pathMemoryLensOptions(trail);
  const filtered = pathMemoryFilteredItems(lane, trail);
  const cards = filtered.slice(0, 10);
  const stats = pathMemoryStats(lane, trail);
  const latest = trail[0];
  const hidden = Math.max(0, filtered.length - cards.length);
  const phase = chroniclePhase(lane, trail);
  const progress = Math.max(6, Math.min(100, lane.progress ?? (trail.length ? 24 : 6)));
  return `
    <article class="path-memory-codex" id="path-memory-codex" style="${laneStyle(lane)} --path-memory-progress:${progress}%">
      <div class="path-memory-visual" aria-hidden="true">
        <img src="./assets/system/path-memory-codex-20260618.png" alt="" loading="eager" />
        <span class="path-memory-scan"></span>
        <span class="path-memory-core"><strong>${formatNumber(trail.length)}</strong><em>steps</em></span>
        <span class="path-memory-thread one"></span>
        <span class="path-memory-thread two"></span>
        <span class="path-memory-thread three"></span>
      </div>
      <div class="path-memory-copy">
        <div class="path-memory-head">
          <div>
            <p class="eyebrow">Path Memory Codex</p>
            <h3>${escapeHtml(phase.label)}</h3>
            <p>${escapeHtml(compactText(latest?.summary ?? chronicleNextAction(lane), 170))}</p>
          </div>
          <span class="badge ${escapeHtml(phase.tone)}">${escapeHtml(stateLabel(lens))}</span>
        </div>
        <div class="path-memory-stats">
          ${stats.map((stat) => `<span><strong>${escapeHtml(stat.value)}</strong><em>${escapeHtml(stat.label)}</em><small>${escapeHtml(stat.note)}</small></span>`).join("")}
        </div>
        <div class="path-memory-lenses" aria-label="Filter Path Memory Codex records">
          ${options
            .map(
              (option) => `
                <button class="path-memory-lens ${lens === option.id ? "active" : ""}" type="button" data-path-memory-action="${escapeHtml(option.id)}" data-path-memory-lane="${escapeHtml(lane.id)}" aria-pressed="${lens === option.id ? "true" : "false"}" ${option.count ? "" : "disabled"} title="Show ${escapeHtml(option.label)} memory records">
                  ${pathEventGlyphMarkup(option.id, "path-memory-lens-glyph")}
                  <span>${escapeHtml(option.label)}</span>
                  <strong>${formatNumber(option.count)}</strong>
                </button>`
            )
            .join("")}
        </div>
        <div class="path-memory-actions">
          <button class="tool-button" type="button" data-path-memory-jump="path" data-path-memory-lane="${escapeHtml(lane.id)}" title="Open Path Map">PATH</button>
          <button class="tool-button" type="button" data-path-memory-jump="comms" data-path-memory-lane="${escapeHtml(lane.id)}" title="Open lane Comms">COM</button>
          <button class="tool-button primary" type="button" data-path-memory-jump="more" data-path-memory-lane="${escapeHtml(lane.id)}" title="Reveal more raw Trail records">MORE</button>
        </div>
      </div>
      <div class="path-memory-grid" aria-label="Filtered path memory records">
        ${
          cards.length
            ? cards.map((item, index) => renderPathMemoryCard(lane, item, index)).join("")
            : `<article class="path-memory-empty"><strong>No ${escapeHtml(stateLabel(lens))} records yet</strong><span>New lane activity will fill this memory lane automatically.</span></article>`
        }
        ${renderPathMemoryFutureSlots(lane, hidden)}
      </div>
    </article>`;
}

function renderPathMemoryCard(lane, item, index) {
  const type = pathEventGlyphType(item);
  const eventKey = pathEventKey(item);
  const summary = item.summary ?? item.artifact ?? "Recorded in this lane trail.";
  return `
    <button class="path-memory-card ${escapeHtml(type)}" type="button" data-path-memory-event="${escapeHtml(eventKey)}" data-path-memory-lane="${escapeHtml(lane.id)}" style="--path-memory-index:${index}" title="Inspect this memory record in Path Map">
      ${pathEventGlyphMarkup(item, "path-memory-card-glyph")}
      <span class="path-memory-card-copy">
        <strong>${escapeHtml(compactText(item.title, 74))}</strong>
        <em>${escapeHtml(compactText(summary, 126))}</em>
      </span>
      <span class="path-memory-card-meta">
        <small>${escapeHtml(shortDate(item.time))}</small>
        <i>${escapeHtml(stateLabel(type))}</i>
      </span>
    </button>`;
}

function renderPathMemoryFutureSlots(lane, hidden) {
  const slots = [
    { title: hidden ? `${formatNumber(hidden)} older records` : "Older chapter socket", meta: hidden ? "Reveal from Trail" : "Ready for future history", tone: "trace" },
    { title: lane.counts?.blockers ? "Blocker review socket" : "Next gate socket", meta: lane.counts?.blockers ? `${formatNumber(lane.counts.blockers)} gates active` : "Waiting for signal", tone: "gate" },
    { title: "Proof packet socket", meta: "Artifacts and wins attach here", tone: "proof" },
    { title: "Unlock socket", meta: "Next outcome becomes a reward card", tone: "outcome" },
  ];
  return slots
    .map(
      (slot) => `
        <article class="path-memory-future ${escapeHtml(slot.tone)}">
          ${pathEventGlyphMarkup(slot.tone, "path-memory-future-glyph")}
          <strong>${escapeHtml(slot.title)}</strong>
          <span>${escapeHtml(slot.meta)}</span>
        </article>`
    )
    .join("");
}

function renderTrailView(lane) {
  const trail = chronicleTrail(lane);
  const limit = state.trailLimitByLane[lane.id] ?? 18;
  const visible = trail.slice(0, limit);
  return `
    <section class="detail-section">
      <div class="lane-button-top">
        <div>
          <p class="eyebrow">Expanding Trail</p>
          <h3>${formatNumber(trail.length)} recorded steps</h3>
        </div>
        <span class="badge advancing">${formatNumber(visible.length)} visible</span>
      </div>
      ${renderPathMemoryCodex(lane, trail)}
      <div class="trail-legend">
        ${["task", "service_request", "evidence", "outcome", "trace"].map((kind) => `<span>${escapeHtml(stateLabel(kind))}</span>`).join("")}
      </div>
      <div class="timeline deep-trail">
        ${visible.map(renderTrailItem).join("") || `<p class="small-muted">No trail records yet.</p>`}
      </div>
      ${
        visible.length < trail.length
          ? `<button class="expand-button" type="button" data-expand-trail="${escapeHtml(lane.id)}">Reveal ${Math.min(18, trail.length - visible.length)} more steps</button>`
          : `<p class="small-muted trail-end">Full available trail is visible. New artifacts will extend this path automatically.</p>`
      }
    </section>`;
}

function renderTrailItem(item, index) {
  return `
    <article class="timeline-item trail-item ${escapeHtml(item.kind)}" style="--trail-index:${index}">
      <h3>${escapeHtml(item.title)}</h3>
      <p>${escapeHtml(shortDate(item.time))} - ${escapeHtml(stateLabel(item.kind))} - ${escapeHtml(stateLabel(item.status))}</p>
      <p>${escapeHtml(compactText(item.summary, 260))}</p>
      ${item.artifact ? `<a href="${escapeHtml(item.artifact)}">${escapeHtml(item.artifact)}</a>` : ""}
    </article>`;
}

const MINIGAME_REGISTRY = {
  "baseline-climb": {
    render: renderBaselineClimbGame,
    count: (lane) => buildBaselineClimbStages(lane).length,
  },
  "venue-mapper": {
    render: renderVenueMapperGame,
    count: (lane) => buildVenueMapperSites(lane).length,
  },
  "offer-route": {
    render: renderOfferRouteGame,
    count: (lane) => buildOfferRouteStages(lane).length,
  },
  "paper-trial": {
    render: renderPaperTrialGame,
    count: (lane) => buildPaperTrialStages(lane).length,
  },
  "settlement-replay": {
    render: renderSettlementReplayGame,
    count: (lane) => buildSettlementReplayStages(lane).length,
  },
  "grant-expedition": {
    render: renderGrantExpeditionGame,
    count: (lane) => buildGrantExpeditionSites(lane).length,
  },
  "scope-run": {
    render: renderScopeRunGame,
    count: (lane) => buildScopeRunStations(lane).length,
  },
  "payout-vault": {
    render: renderPayoutVaultGame,
    count: (lane) => buildPayoutVaultStages(lane).length,
  },
  "claim-scout": {
    render: renderClaimScoutGame,
    count: (lane) => buildClaimScoutCards(lane).length,
  },
  "signal-harvest": {
    render: renderSignalHarvestGame,
    count: (lane) => buildSignalHarvestBeds(lane).length,
  },
  "systems-grid": {
    render: renderSystemsGridGame,
    count: (lane) => buildSystemsGridCells(lane).length,
  },
  "foundry-run": {
    render: renderFoundryRunGame,
    count: (lane) => buildFoundryStages(lane).length,
  },
};

function minigameDefinition(lane) {
  if (!lane) return null;
  return MINIGAME_REGISTRY[lane.visual?.minigame?.id] ?? null;
}

function renderGameView(lane) {
  return `
    ${renderGameStageHud(lane)}
    ${minigameDefinition(lane)?.render(lane) ?? renderCheckpointGame(lane)}`;
}

function gameStepCount(lane) {
  if (!lane) return 1;
  return minigameDefinition(lane)?.count(lane) ?? lane.quest?.checkpoints?.length ?? 1;
}

function renderGameStageHud(lane) {
  const stepCount = gameStepCount(lane);
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, Math.max(stepCount - 1, 0));
  const minigame = lane.visual?.minigame ?? {};
  const views = [
    { id: "overview", label: "OVR", title: "Open overview" },
    { id: "path", label: "MAP", title: "Open Path Map" },
    { id: "chronicle", label: "LOG", title: "Open chronicle" },
    { id: "trail", label: "TRL", title: "Open full trail" },
    { id: "game", label: "PLAY", title: "Stay in game module" },
    { id: "comms", label: "COM", title: "Open command deck" },
  ];
  return `
    <nav class="game-stage-hud" aria-label="Game stage navigation" style="${laneStyle(lane)}">
      <span class="game-stage-hud-meter">
        <strong>${formatNumber(currentStep + 1)}/${formatNumber(stepCount)}</strong>
        <em>${escapeHtml(compactText(minigame.title ?? lane.visual?.realm ?? "module", 22))}</em>
      </span>
      ${views
        .map(
          (view) => `
            <button class="game-stage-hud-button ${view.id === "game" ? "active" : ""}" type="button" data-detail-view="${escapeHtml(view.id)}" title="${escapeHtml(view.title)}" aria-current="${view.id === "game" ? "page" : "false"}">${escapeHtml(view.label)}</button>`
        )
        .join("")}
    </nav>`;
}

function renderCheckpointGame(lane) {
  const checkpoints = lane.quest?.checkpoints ?? [];
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, Math.max(checkpoints.length - 1, 0));
  const current = checkpoints[currentStep];
  const progress = checkpoints.length > 1 ? Math.round((currentStep / (checkpoints.length - 1)) * 100) : 100;
  return `
    <section class="detail-section">
      <p class="eyebrow">Playable Lane Module</p>
      <div class="game-board" style="${laneStyle(lane)}">
        <div class="game-head">
          ${avatarMarkup(lane, "game-avatar")}
          <div>
            <h3>${escapeHtml(lane.visual?.minigame?.title ?? lane.quest?.title ?? "Lane Quest")}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic ?? "Advance through real lane checkpoints.", 180))}</p>
          </div>
        </div>
        <div class="game-track" style="--game-progress:${progress}%">
          ${checkpoints.map((checkpoint, index) => renderCheckpoint(checkpoint, index, currentStep)).join("")}
        </div>
        <div class="game-status">
          <div>
            <p class="eyebrow">Current Checkpoint</p>
            <h3>${escapeHtml(current?.title ?? "No checkpoint")}</h3>
            <p>${escapeHtml(current?.description ?? "This lane is waiting for its first playable checkpoint.")}</p>
          </div>
          <div class="game-actions">
            <button class="tool-button" type="button" data-game-action="reset" title="Reset lane module">0</button>
            <button class="tool-button" type="button" data-game-action="prev" title="Previous checkpoint">-</button>
            <button class="tool-button" type="button" data-game-action="next" title="Next checkpoint">+</button>
          </div>
        </div>
      </div>
    </section>`;
}

function buildBaselineClimbStages(lane) {
  const trail = lane.trail ?? [];
  const counts = lane.counts ?? {};
  const gate = lane.serviceRequests?.[0] ?? lane.gateMap?.[0];
  const eligibilityHits = trail.filter((item) => /eligib|rules|terms|deadline|prize|competition|category/i.test(`${item.title} ${item.summary}`)).length;
  const datasetHits = trail.filter((item) => /dataset|data|sample|benchmark|metric|evaluation|score/i.test(`${item.title} ${item.summary}`)).length;
  const baselineHits = trail.filter((item) => /baseline|model|notebook|prototype|local|proof|experiment/i.test(`${item.title} ${item.summary}`)).length;
  const submissionHits = trail.filter((item) => /submit|submission|account|public|upload|register|approval|gate/i.test(`${item.title} ${item.summary}`)).length;
  const taskProgress = counts.tasks ? Math.round(((counts.completedTasks ?? 0) / counts.tasks) * 100) : 0;
  const eligibilityScore = Math.min(96, Math.round(36 + eligibilityHits * 9 + (counts.evidence ?? 0) * 3.2));
  const datasetScore = Math.min(96, Math.round(34 + datasetHits * 8 + (counts.artifacts ?? 0) * 1.2));
  const baselineScore = Math.min(98, Math.round(32 + baselineHits * 8 + taskProgress * 0.42));
  const leaderboardScore = Math.min(95, Math.round(30 + (counts.outcomes ?? 0) * 6 + (counts.traces ?? 0) * 3.2));
  const gateScore = Math.max(10, 88 - (counts.pendingRequests ?? 0) * 22 - (counts.blockers ?? 0) * 18 - submissionHits * 2);
  return [
    {
      id: "eligibility",
      title: "Eligibility Gate",
      score: eligibilityScore,
      status: eligibilityScore >= 72 ? "cleared" : "scouting",
      body: `${eligibilityHits} rules, deadline, or competition-fit signals are visible in the lane trail.`,
    },
    {
      id: "dataset",
      title: "Dataset Lock",
      score: datasetScore,
      status: datasetScore >= 72 ? "mapped" : "indexing",
      body: `${datasetHits} dataset, metric, benchmark, or evaluation records support the climb route.`,
    },
    {
      id: "baseline",
      title: "Baseline Run",
      score: baselineScore,
      status: baselineScore >= 76 ? "running" : "queued",
      body: `${baselineHits} baseline, model, notebook, local proof, or experiment signals are feeding the first run.`,
    },
    {
      id: "leaderboard",
      title: "Leaderboard Step",
      score: leaderboardScore,
      status: leaderboardScore >= 74 ? "climbing" : "warming",
      body: `${counts.outcomes ?? 0} outcomes and ${counts.traces ?? 0} traces create a local score trail before any public action.`,
    },
    {
      id: "submission",
      title: "Submission Lock",
      score: gateScore,
      status: (counts.blockers ?? 0) ? "gated" : "clear",
      body: gate
        ? `${gate.status ?? gate.route}: ${gate.riskGate ?? gate.gate}`
        : "No submission gate is attached, but uploads, accounts, and public entries still require explicit approval.",
    },
  ];
}

function renderBaselineClimbGame(lane) {
  const stages = buildBaselineClimbStages(lane);
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, stages.length - 1);
  const current = stages[currentStep];
  const altitude = Math.round(stages.reduce((sum, stage) => sum + stage.score, 0) / stages.length);
  const verdict = lane.counts.blockers ? "Gate Camp" : altitude >= 74 ? "Climb Ready" : "Train More";
  return `
    <section class="detail-section">
      <p class="eyebrow">Lane-Specific Minigame</p>
      <div class="baseline-climb-board" style="${laneStyle(lane)}">
        <div class="baseline-summit-glow" aria-hidden="true"></div>
        <div class="baseline-hero">
          ${avatarMarkup(lane, "game-avatar")}
          <div>
            <h3>${escapeHtml(lane.visual?.minigame?.title ?? "Baseline Climb")}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic, 190))}</p>
          </div>
          <div class="baseline-verdict">
            <strong>${escapeHtml(verdict)}</strong>
            <span>${altitude}% altitude</span>
          </div>
        </div>
        <div class="baseline-ascent" style="--baseline-altitude:${altitude}%" aria-hidden="true">
          <div class="ascent-route"></div>
          ${stages
            .map(
              (stage, index) =>
                `<span class="ascent-node ${index === currentStep ? "active" : ""}" style="--ascent-x:${12 + index * 19}%; --ascent-y:${74 - index * 12 - (stage.score % 18)}%; --ascent-score:${stage.score}%"></span>`
            )
            .join("")}
        </div>
        <div class="baseline-stage-grid">
          ${stages.map((stage, index) => renderBaselineStage(stage, index, currentStep)).join("")}
        </div>
        <div class="game-status">
          <div>
            <p class="eyebrow">Focused Station</p>
            <h3>${escapeHtml(current.title)}</h3>
            <p>${escapeHtml(compactText(current.body, 230))}</p>
          </div>
          <div class="game-actions">
            <button class="tool-button" type="button" data-game-action="reset" title="Reset baseline climb focus">0</button>
            <button class="tool-button" type="button" data-game-action="prev" title="Previous baseline station">-</button>
            <button class="tool-button" type="button" data-game-action="next" title="Next baseline station">+</button>
          </div>
        </div>
      </div>
    </section>`;
}

function renderBaselineStage(stage, index, currentStep) {
  return `
    <article class="baseline-stage ${escapeHtml(stage.status)} ${index === currentStep ? "is-current" : ""}">
      <div class="foundry-stage-top">
        <span>${index + 1}</span>
        <strong>${escapeHtml(stateLabel(stage.status))}</strong>
      </div>
      <h3>${escapeHtml(stage.title)}</h3>
      <div class="baseline-meter" style="--baseline-score:${stage.score}%"><span></span></div>
      <p>${escapeHtml(compactText(stage.body, 150))}</p>
    </article>`;
}

function buildVenueMapperSites(lane) {
  const trail = lane.trail ?? [];
  const counts = lane.counts ?? {};
  const gate = lane.serviceRequests?.[0] ?? lane.gateMap?.[0];
  const sourceHits = trail.filter((item) => /source|venue|registry|catalog|directory|platform|marketplace|opportunity|training/i.test(`${item.title} ${item.summary}`)).length;
  const payoutHits = trail.filter((item) => /payout|paid|bounty|grant|prize|revenue|money|cash|monetiz/i.test(`${item.title} ${item.summary}`)).length;
  const proofHits = trail.filter((item) => /proof|evidence|local|packet|sample|worksheet|artifact|matrix/i.test(`${item.title} ${item.summary}`)).length;
  const freshnessHits = trail.filter((item) => /refresh|fresh|scan|latest|current|delta|update|read-only|browser/i.test(`${item.title} ${item.summary}`)).length;
  const gateHits = trail.filter((item) => /gate|account|browser|approval|public|payment|wallet|kyc|terms|legal/i.test(`${item.title} ${item.summary}`)).length;
  const taskProgress = counts.tasks ? Math.round(((counts.completedTasks ?? 0) / counts.tasks) * 100) : 0;
  const sourceScore = Math.min(98, Math.round(34 + sourceHits * 8 + (counts.evidence ?? 0) * 3.4));
  const payoutScore = Math.min(96, Math.round(28 + payoutHits * 9 + (counts.outcomes ?? 0) * 4.8));
  const proofScore = Math.min(96, Math.round(30 + proofHits * 6 + (counts.artifacts ?? 0) * 1.25 + taskProgress * 0.18));
  const freshnessScore = Math.min(94, Math.round(36 + freshnessHits * 8 + (counts.traces ?? 0) * 2.6));
  const gateScore = Math.max(10, 88 - (counts.pendingRequests ?? 0) * 22 - (counts.blockers ?? 0) * 18 - gateHits * 2);
  return [
    {
      id: "source",
      title: "Source Beacon",
      score: sourceScore,
      status: sourceScore >= 72 ? "mapped" : "scouting",
      x: 16,
      y: 62,
      body: `${sourceHits} source, venue, platform, or catalog signals are visible in this lane trail.`,
    },
    {
      id: "payout",
      title: "Payout Signal",
      score: payoutScore,
      status: payoutScore >= 72 ? "priced" : "fogged",
      x: 34,
      y: 35,
      body: `${payoutHits} payout, money, prize, grant, or monetization records support the reward route.`,
    },
    {
      id: "proof",
      title: "First Proof Route",
      score: proofScore,
      status: proofScore >= 74 ? "charted" : "building",
      x: 54,
      y: 58,
      body: `${proofHits} proof-like records and ${counts.artifacts ?? 0} artifacts make the first local test easier to repeat.`,
    },
    {
      id: "freshness",
      title: "Freshness Sweep",
      score: freshnessScore,
      status: freshnessScore >= 72 ? "live" : "stale-risk",
      x: 74,
      y: 30,
      body: `${freshnessHits} refresh, browser, or scan signals and ${counts.traces ?? 0} traces show how recently the map was checked.`,
    },
    {
      id: "gate",
      title: "Access Gate",
      score: gateScore,
      status: (counts.blockers ?? 0) ? "gated" : "clear",
      x: 84,
      y: 68,
      body: gate
        ? `${gate.status ?? gate.route}: ${gate.riskGate ?? gate.gate}`
        : "No access gate is attached, but accounts, payments, and public actions still require explicit review.",
    },
  ];
}

function renderVenueMapperGame(lane) {
  const sites = buildVenueMapperSites(lane);
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, sites.length - 1);
  const current = sites[currentStep];
  const mapClarity = Math.round(sites.reduce((sum, site) => sum + site.score, 0) / sites.length);
  const verdict = lane.counts.blockers ? "Fog Hold" : mapClarity >= 72 ? "Map Ready" : "Scout More";
  return `
    <section class="detail-section">
      <p class="eyebrow">Lane-Specific Minigame</p>
      <div class="venue-mapper-board" style="${laneStyle(lane)}">
        <div class="venue-fog-glow" aria-hidden="true"></div>
        <div class="venue-hero">
          ${avatarMarkup(lane, "game-avatar")}
          <div>
            <h3>${escapeHtml(lane.visual?.minigame?.title ?? "Venue Mapper")}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic, 190))}</p>
          </div>
          <div class="venue-verdict">
            <strong>${escapeHtml(verdict)}</strong>
            <span>${mapClarity}% clarity</span>
          </div>
        </div>
        <div class="venue-map" style="--venue-clarity:${mapClarity}%" aria-hidden="true">
          <div class="venue-route-line"></div>
          ${sites
            .map(
              (site, index) =>
                `<span class="venue-beacon ${escapeHtml(site.status)} ${index === currentStep ? "active" : ""}" style="--venue-x:${site.x}%; --venue-y:${site.y}%; --venue-score:${site.score}%"></span>`
            )
            .join("")}
          <i></i><i></i><i></i>
        </div>
        <div class="venue-site-grid">
          ${sites.map((site, index) => renderVenueSite(site, index, currentStep)).join("")}
        </div>
        <div class="game-status">
          <div>
            <p class="eyebrow">Focused Beacon</p>
            <h3>${escapeHtml(current.title)}</h3>
            <p>${escapeHtml(compactText(current.body, 230))}</p>
          </div>
          <div class="game-actions">
            <button class="tool-button" type="button" data-game-action="reset" title="Reset venue map focus">0</button>
            <button class="tool-button" type="button" data-game-action="prev" title="Previous venue beacon">-</button>
            <button class="tool-button" type="button" data-game-action="next" title="Next venue beacon">+</button>
          </div>
        </div>
      </div>
    </section>`;
}

function renderVenueSite(site, index, currentStep) {
  return `
    <article class="venue-site ${escapeHtml(site.status)} ${index === currentStep ? "is-current" : ""}">
      <div class="foundry-stage-top">
        <span>${index + 1}</span>
        <strong>${escapeHtml(stateLabel(site.status))}</strong>
      </div>
      <h3>${escapeHtml(site.title)}</h3>
      <div class="venue-meter" style="--venue-score:${site.score}%"><span></span></div>
      <p>${escapeHtml(compactText(site.body, 150))}</p>
    </article>`;
}

function buildOfferRouteStages(lane) {
  const trail = lane.trail ?? [];
  const counts = lane.counts ?? {};
  const gate = lane.serviceRequests?.[0] ?? lane.gateMap?.[0];
  const offerHits = trail.filter((item) => /offer|packet|profile|proposal|package|tier|service|audit/i.test(`${item.title} ${item.summary}`)).length;
  const icpHits = trail.filter((item) => /ICP|lead|client|agency|target|qualification|fit|marketplace/i.test(`${item.title} ${item.summary}`)).length;
  const proofHits = trail.filter((item) => /proof|evidence|local|asset|report|draft|synthetic|sample/i.test(`${item.title} ${item.summary}`)).length;
  const safetyHits = trail.filter((item) => /spam|privacy|contract|data|payment|gate|approval|truthful|opt-out|policy/i.test(`${item.title} ${item.summary}`)).length;
  const closeHits = trail.filter((item) => /close|send|submit|account|public|marketplace|proposal|payment|contract/i.test(`${item.title} ${item.summary}`)).length;
  const taskProgress = counts.tasks ? Math.round(((counts.completedTasks ?? 0) / counts.tasks) * 100) : 0;
  const offerScore = Math.min(98, Math.round(34 + offerHits * 7 + (counts.evidence ?? 0) * 4.8));
  const icpScore = Math.min(94, Math.round(30 + icpHits * 9 + (counts.outcomes ?? 0) * 4.2));
  const proofScore = Math.min(96, Math.round(32 + proofHits * 7 + (counts.artifacts ?? 0) * 1.8 + taskProgress * 0.16));
  const safetyScore = Math.min(96, Math.round(40 + safetyHits * 6 + (counts.traces ?? 0) * 3.6));
  const gateScore = Math.max(10, 90 - (counts.pendingRequests ?? 0) * 22 - (counts.blockers ?? 0) * 20 - closeHits * 2);
  return [
    {
      id: "offer",
      title: "Offer Packet",
      score: offerScore,
      status: offerScore >= 72 ? "packaged" : "drafting",
      x: 10,
      y: 68,
      body: `${offerHits} offer, packet, service, profile, proposal, or package signals define what can be sold.`,
    },
    {
      id: "icp",
      title: "ICP Fit",
      score: icpScore,
      status: icpScore >= 72 ? "qualified" : "sorting",
      x: 30,
      y: 38,
      body: `${icpHits} lead, client, agency, target, marketplace, or qualification signals shape the audience route.`,
    },
    {
      id: "proof",
      title: "Proof Asset",
      score: proofScore,
      status: proofScore >= 74 ? "ready" : "building",
      x: 52,
      y: 58,
      body: `${proofHits} proof-like records and ${counts.artifacts ?? 0} artifacts support a non-handwavy offer.`,
    },
    {
      id: "safety",
      title: "Channel Safety",
      score: safetyScore,
      status: safetyScore >= 74 ? "guarded" : "reviewing",
      x: 72,
      y: 34,
      body: `${safetyHits} privacy, contract, data, payment, spam, approval, or policy signals keep outreach careful.`,
    },
    {
      id: "close",
      title: "Close Gate",
      score: gateScore,
      status: (counts.blockers ?? 0) ? "gated" : gate ? "review" : "clear",
      x: 88,
      y: 66,
      body: gate
        ? `${gate.status ?? gate.route}: ${gate.riskGate ?? gate.gate}`
        : "No active close gate is attached, but accounts, submissions, contracts, and payments remain explicit-action boundaries.",
    },
  ];
}

function renderOfferRouteGame(lane) {
  const stages = buildOfferRouteStages(lane);
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, stages.length - 1);
  const current = stages[currentStep];
  const routeScore = Math.round(stages.reduce((sum, stage) => sum + stage.score, 0) / stages.length);
  const verdict = lane.counts.blockers ? "Gate Hold" : routeScore >= 74 ? "Route Warm" : "Shape Offer";
  return `
    <section class="detail-section">
      <p class="eyebrow">Lane-Specific Minigame</p>
      <div class="offer-route-board" style="${laneStyle(lane)}">
        <div class="offer-route-glow" aria-hidden="true"></div>
        <div class="offer-hero">
          ${avatarMarkup(lane, "game-avatar")}
          <div>
            <h3>${escapeHtml(lane.visual?.minigame?.title ?? "Offer Route")}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic, 190))}</p>
          </div>
          <div class="offer-verdict">
            <strong>${escapeHtml(verdict)}</strong>
            <span>${routeScore}% route</span>
          </div>
        </div>
        <div class="offer-pipeline" style="--offer-route-score:${routeScore}%" aria-hidden="true">
          <div class="offer-route-line"></div>
          ${stages
            .map(
              (stage, index) =>
                `<span class="offer-node ${escapeHtml(stage.status)} ${index === currentStep ? "active" : ""}" style="--offer-x:${stage.x}%; --offer-y:${stage.y}%; --offer-score:${stage.score}%"></span>`
            )
            .join("")}
          <i></i><i></i><i></i>
        </div>
        <div class="offer-stage-grid">
          ${stages.map((stage, index) => renderOfferStage(stage, index, currentStep)).join("")}
        </div>
        <div class="game-status">
          <div>
            <p class="eyebrow">Focused Route</p>
            <h3>${escapeHtml(current.title)}</h3>
            <p>${escapeHtml(compactText(current.body, 230))}</p>
          </div>
          <div class="game-actions">
            <button class="tool-button" type="button" data-game-action="reset" title="Reset offer route focus">0</button>
            <button class="tool-button" type="button" data-game-action="prev" title="Previous offer route stage">-</button>
            <button class="tool-button" type="button" data-game-action="next" title="Next offer route stage">+</button>
          </div>
        </div>
      </div>
    </section>`;
}

function renderOfferStage(stage, index, currentStep) {
  return `
    <article class="offer-stage ${escapeHtml(stage.status)} ${index === currentStep ? "is-current" : ""}">
      <div class="foundry-stage-top">
        <span>${index + 1}</span>
        <strong>${escapeHtml(stateLabel(stage.status))}</strong>
      </div>
      <h3>${escapeHtml(stage.title)}</h3>
      <div class="offer-meter" style="--offer-score:${stage.score}%"><span></span></div>
      <p>${escapeHtml(compactText(stage.body, 150))}</p>
    </article>`;
}

function buildPaperTrialStages(lane) {
  const trail = lane.trail ?? [];
  const counts = lane.counts ?? {};
  const gate = lane.serviceRequests?.[0] ?? lane.gateMap?.[0];
  const dataHits = trail.filter((item) => /data|source|inventory|raw|rows|ledger|history|artifact/i.test(`${item.title} ${item.summary}`)).length;
  const paperHits = trail.filter((item) => /paper|dry-run|simulation|backtest|replay|watch|local/i.test(`${item.title} ${item.summary}`)).length;
  const validationHits = trail.filter((item) => /out-of-sample|validation|standard|evidence|proof|reconciled|closed-event|sequential/i.test(`${item.title} ${item.summary}`)).length;
  const riskHits = trail.filter((item) => /risk|drawdown|slippage|overlap|readiness|blocker|gate|lock/i.test(`${item.title} ${item.summary}`)).length;
  const liveHits = trail.filter((item) => /broker|API|order|live|real-money|credential|account|trade/i.test(`${item.title} ${item.summary}`)).length;
  const taskProgress = counts.tasks ? Math.round(((counts.completedTasks ?? 0) / counts.tasks) * 100) : 0;
  const dataScore = Math.min(96, Math.round(34 + dataHits * 8 + (counts.artifacts ?? 0) * 3.2));
  const paperScore = Math.min(98, Math.round(36 + paperHits * 8 + (counts.evidence ?? 0) * 6.5));
  const validationScore = Math.min(96, Math.round(30 + validationHits * 8 + (counts.traces ?? 0) * 6 + taskProgress * 0.18));
  const riskScore = Math.min(94, Math.round(28 + riskHits * 7 + (counts.outcomes ?? 0) * 6.5));
  const gateScore = Math.max(10, 92 - (counts.pendingRequests ?? 0) * 24 - (counts.blockers ?? 0) * 20 - liveHits * 2);
  return [
    {
      id: "data",
      title: "Data Range",
      score: dataScore,
      status: dataScore >= 72 ? "indexed" : "sampling",
      x: 12,
      y: 68,
      body: `${dataHits} data, source, inventory, row, history, or ledger signals define the paper range.`,
    },
    {
      id: "paper",
      title: "Paper Replay",
      score: paperScore,
      status: paperScore >= 74 ? "running" : "queued",
      x: 32,
      y: 36,
      body: `${paperHits} paper, dry-run, backtest, replay, watch, simulation, or local-only signals keep the trial non-live.`,
    },
    {
      id: "validation",
      title: "Validation Split",
      score: validationScore,
      status: validationScore >= 72 ? "checked" : "testing",
      x: 53,
      y: 58,
      body: `${validationHits} validation, evidence-standard, proof, reconciliation, or closed-event signals support the test split.`,
    },
    {
      id: "risk",
      title: "Risk Band",
      score: riskScore,
      status: riskScore >= 70 ? "bounded" : "wide",
      x: 73,
      y: 34,
      body: `${riskHits} risk, drawdown, slippage, overlap, gate, lock, or readiness signals shape the risk rail.`,
    },
    {
      id: "live",
      title: "Live Vault",
      score: gateScore,
      status: liveHits || gate ? "sealed" : "sealed",
      x: 88,
      y: 68,
      body: gate
        ? `${gate.status ?? gate.route}: ${gate.riskGate ?? gate.gate}`
        : `${liveHits} broker, API, order, live, account, credential, or real-money boundary signals are visible and must remain sealed.`,
    },
  ];
}

function renderPaperTrialGame(lane) {
  const stages = buildPaperTrialStages(lane);
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, stages.length - 1);
  const current = stages[currentStep];
  const trialScore = Math.round(stages.reduce((sum, stage) => sum + stage.score, 0) / stages.length);
  const verdict = lane.counts.blockers ? "Gate Lock" : trialScore >= 74 ? "Paper Ready" : "Replay More";
  return `
    <section class="detail-section">
      <p class="eyebrow">Lane-Specific Minigame</p>
      <div class="paper-trial-board" style="${laneStyle(lane)}">
        <div class="paper-trial-glow" aria-hidden="true"></div>
        <div class="paper-hero">
          ${avatarMarkup(lane, "game-avatar")}
          <div>
            <h3>${escapeHtml(lane.visual?.minigame?.title ?? "Paper Trial")}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic, 190))}</p>
          </div>
          <div class="paper-verdict">
            <strong>${escapeHtml(verdict)}</strong>
            <span>${trialScore}% trial</span>
          </div>
        </div>
        <div class="paper-sim" style="--paper-trial-score:${trialScore}%" aria-hidden="true">
          <div class="paper-track-line"></div>
          ${stages
            .map(
              (stage, index) =>
                `<span class="paper-node ${escapeHtml(stage.status)} ${index === currentStep ? "active" : ""}" style="--paper-x:${stage.x}%; --paper-y:${stage.y}%; --paper-score:${stage.score}%"></span>`
            )
            .join("")}
          <i></i><i></i><i></i>
        </div>
        <div class="paper-stage-grid">
          ${stages.map((stage, index) => renderPaperStage(stage, index, currentStep)).join("")}
        </div>
        <div class="game-status">
          <div>
            <p class="eyebrow">Focused Trial</p>
            <h3>${escapeHtml(current.title)}</h3>
            <p>${escapeHtml(compactText(current.body, 230))}</p>
          </div>
          <div class="game-actions">
            <button class="tool-button" type="button" data-game-action="reset" title="Reset paper trial focus">0</button>
            <button class="tool-button" type="button" data-game-action="prev" title="Previous paper trial stage">-</button>
            <button class="tool-button" type="button" data-game-action="next" title="Next paper trial stage">+</button>
          </div>
        </div>
      </div>
    </section>`;
}

function renderPaperStage(stage, index, currentStep) {
  return `
    <article class="paper-stage ${escapeHtml(stage.status)} ${index === currentStep ? "is-current" : ""}">
      <div class="foundry-stage-top">
        <span>${index + 1}</span>
        <strong>${escapeHtml(stateLabel(stage.status))}</strong>
      </div>
      <h3>${escapeHtml(stage.title)}</h3>
      <div class="paper-meter" style="--paper-score:${stage.score}%"><span></span></div>
      <p>${escapeHtml(compactText(stage.body, 150))}</p>
    </article>`;
}

function buildSettlementReplayStages(lane) {
  const trail = lane.trail ?? [];
  const counts = lane.counts ?? {};
  const gate = lane.serviceRequests?.[0] ?? lane.gateMap?.[0];
  const packetHits = trail.filter((item) => /packet|parser|checker|rows|archived|imported|scan|data/i.test(`${item.title} ${item.summary}`)).length;
  const replayHits = trail.filter((item) => /replay|paper|hypothesis|candidate|watch|simulat|data-only|local/i.test(`${item.title} ${item.summary}`)).length;
  const rulesHits = trail.filter((item) => /rule|resolution|settlement|source|truth|close-window|clause|mismatch/i.test(`${item.title} ${item.summary}`)).length;
  const marketHits = trail.filter((item) => /eligib|fee|liquidity|spread|volume|venue|kalshi|polymarket|treasury/i.test(`${item.title} ${item.summary}`)).length;
  const tradeHits = trail.filter((item) => /no-trade|trade|order|account|credential|deposit|withdrawal|API|KYC|real-money/i.test(`${item.title} ${item.summary}`)).length;
  const taskProgress = counts.tasks ? Math.round(((counts.completedTasks ?? 0) / counts.tasks) * 100) : 0;
  const packetScore = Math.min(96, Math.round(34 + packetHits * 8 + (counts.evidence ?? 0) * 2.8));
  const replayScore = Math.min(98, Math.round(36 + replayHits * 8 + (counts.outcomes ?? 0) * 6.5));
  const rulesScore = Math.min(96, Math.round(30 + rulesHits * 8 + (counts.traces ?? 0) * 6 + taskProgress * 0.18));
  const marketScore = Math.min(94, Math.round(28 + marketHits * 7 + (counts.artifacts ?? 0) * 4));
  const gateScore = Math.max(10, 92 - (counts.pendingRequests ?? 0) * 24 - (counts.blockers ?? 0) * 20 - tradeHits * 2);
  return [
    {
      id: "packets",
      title: "Packet Archive",
      score: packetScore,
      status: packetScore >= 72 ? "indexed" : "sampling",
      x: 12,
      y: 68,
      body: `${packetHits} archived packet, parser, checker, row, import, scan, or data signals define the replay chamber.`,
    },
    {
      id: "replay",
      title: "Paper Replay",
      score: replayScore,
      status: replayScore >= 74 ? "running" : "queued",
      x: 32,
      y: 36,
      body: `${replayHits} paper, hypothesis, candidate, watch, simulation, data-only, or local replay signals keep the module non-live.`,
    },
    {
      id: "rules",
      title: "Rules Clock",
      score: rulesScore,
      status: rulesScore >= 72 ? "synced" : "checking",
      x: 53,
      y: 58,
      body: `${rulesHits} resolution, settlement, source-of-truth, close-window, clause, or mismatch signals anchor the outcome clock.`,
    },
    {
      id: "market",
      title: "Venue Friction",
      score: marketScore,
      status: marketScore >= 70 ? "mapped" : "watch",
      x: 73,
      y: 34,
      body: `${marketHits} eligibility, fee, liquidity, spread, venue, market, or treasury signals show why paper profit still needs friction checks.`,
    },
    {
      id: "trade",
      title: "No-Trade Vault",
      score: gateScore,
      status: "sealed",
      x: 88,
      y: 68,
      body: gate
        ? `${gate.status ?? gate.route}: ${gate.riskGate ?? gate.gate}`
        : `${tradeHits} account, credential, API, order, deposit, withdrawal, KYC, live, or real-money boundaries remain sealed.`,
    },
  ];
}

function renderSettlementReplayGame(lane) {
  const stages = buildSettlementReplayStages(lane);
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, stages.length - 1);
  const current = stages[currentStep];
  const replayScore = Math.round(stages.reduce((sum, stage) => sum + stage.score, 0) / stages.length);
  const verdict = lane.counts.blockers ? "Gate Lock" : replayScore >= 74 ? "Replay Clean" : "Replay More";
  return `
    <section class="detail-section">
      <p class="eyebrow">Lane-Specific Minigame</p>
      <div class="settlement-replay-board" style="${laneStyle(lane)}">
        <div class="settlement-replay-glow" aria-hidden="true"></div>
        <div class="settlement-hero">
          ${avatarMarkup(lane, "game-avatar")}
          <div>
            <h3>${escapeHtml(lane.visual?.minigame?.title ?? "Settlement Replay")}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic, 190))}</p>
          </div>
          <div class="settlement-verdict">
            <strong>${escapeHtml(verdict)}</strong>
            <span>${replayScore}% sealed</span>
          </div>
        </div>
        <div class="settlement-sim" style="--settlement-replay-score:${replayScore}%" aria-hidden="true">
          <div class="settlement-orbit-line"></div>
          <div class="settlement-clock-sweep"></div>
          ${stages
            .map(
              (stage, index) =>
                `<span class="settlement-node ${escapeHtml(stage.status)} ${index === currentStep ? "active" : ""}" style="--settlement-x:${stage.x}%; --settlement-y:${stage.y}%; --settlement-score:${stage.score}%"></span>`
            )
            .join("")}
          <i></i><i></i><i></i>
        </div>
        <div class="settlement-stage-grid">
          ${stages.map((stage, index) => renderSettlementStage(stage, index, currentStep)).join("")}
        </div>
        <div class="game-status">
          <div>
            <p class="eyebrow">Focused Replay</p>
            <h3>${escapeHtml(current.title)}</h3>
            <p>${escapeHtml(compactText(current.body, 230))}</p>
          </div>
          <div class="game-actions">
            <button class="tool-button" type="button" data-game-action="reset" title="Reset settlement replay focus">0</button>
            <button class="tool-button" type="button" data-game-action="prev" title="Previous settlement station">-</button>
            <button class="tool-button" type="button" data-game-action="next" title="Next settlement station">+</button>
          </div>
        </div>
      </div>
    </section>`;
}

function renderSettlementStage(stage, index, currentStep) {
  return `
    <article class="settlement-stage ${escapeHtml(stage.status)} ${index === currentStep ? "is-current" : ""}">
      <div class="foundry-stage-top">
        <span>${index + 1}</span>
        <strong>${escapeHtml(stateLabel(stage.status))}</strong>
      </div>
      <h3>${escapeHtml(stage.title)}</h3>
      <div class="settlement-meter" style="--settlement-score:${stage.score}%"><span></span></div>
      <p>${escapeHtml(compactText(stage.body, 150))}</p>
    </article>`;
}

function buildGrantExpeditionSites(lane) {
  const trail = lane.trail ?? [];
  const counts = lane.counts ?? {};
  const gate = lane.serviceRequests?.[0] ?? lane.gateMap?.[0];
  const sourceHits = trail.filter((item) => /source|refresh|wishlist|RFP|grant|hackathon|bounty|airdrop|portal|calendar|official/i.test(`${item.title} ${item.summary}`)).length;
  const fitHits = trail.filter((item) => /fit|classifier|score|rubric|criteria|eligib|duplicate|sweep|rank|route/i.test(`${item.title} ${item.summary}`)).length;
  const prototypeHits = trail.filter((item) => /prototype|packet|memo|proof|artifact|local|blueprint|build|sample|proposal/i.test(`${item.title} ${item.summary}`)).length;
  const deadlineHits = trail.filter((item) => /deadline|calendar|submission|judge|judging|milestone|read-only|browser|ingestion|refresh/i.test(`${item.title} ${item.summary}`)).length;
  const walletHits = trail.filter((item) => /wallet|deploy|deployment|account|quest|transaction|payment|public|submit|application|legal/i.test(`${item.title} ${item.summary}`)).length;
  const taskProgress = counts.tasks ? Math.round(((counts.completedTasks ?? 0) / counts.tasks) * 100) : 0;
  const sourceScore = Math.min(98, Math.round(34 + sourceHits * 7 + (counts.evidence ?? 0) * 4.2));
  const fitScore = Math.min(96, Math.round(32 + fitHits * 7 + (counts.outcomes ?? 0) * 4.4));
  const prototypeScore = Math.min(98, Math.round(32 + prototypeHits * 6 + (counts.artifacts ?? 0) * 2.4 + taskProgress * 0.16));
  const deadlineScore = Math.min(94, Math.round(30 + deadlineHits * 7 + (counts.traces ?? 0) * 4.2));
  const gateScore = Math.max(10, 92 - (counts.pendingRequests ?? 0) * 24 - (counts.blockers ?? 0) * 20 - walletHits * 2);
  return [
    {
      id: "source",
      title: "Source Atlas",
      score: sourceScore,
      status: sourceScore >= 72 ? "mapped" : "scouting",
      x: 12,
      y: 66,
      body: `${sourceHits} grant, hackathon, bounty, wishlist, RFP, official-source, refresh, or calendar signals shape the expedition map.`,
    },
    {
      id: "fit",
      title: "Grant Fit",
      score: fitScore,
      status: fitScore >= 72 ? "matched" : "sorting",
      x: 32,
      y: 36,
      body: `${fitHits} fit, classifier, scoring, eligibility, duplicate-sweep, rubric, or route signals decide which portal deserves attention.`,
    },
    {
      id: "prototype",
      title: "Prototype Camp",
      score: prototypeScore,
      status: prototypeScore >= 74 ? "built" : "drafting",
      x: 53,
      y: 58,
      body: `${prototypeHits} prototype, proof, packet, memo, artifact, proposal, blueprint, or local-build signals keep the path tangible.`,
    },
    {
      id: "deadline",
      title: "Deadline Route",
      score: deadlineScore,
      status: deadlineScore >= 70 ? "charted" : "watch",
      x: 73,
      y: 34,
      body: `${deadlineHits} deadline, calendar, judging, milestone, submission, read-only, browser, ingestion, or refresh signals define route timing.`,
    },
    {
      id: "wallet",
      title: "Wallet Gate",
      score: gateScore,
      status: "sealed",
      x: 88,
      y: 68,
      body: gate
        ? `${gate.status ?? gate.route}: ${gate.riskGate ?? gate.gate}`
        : `${walletHits} wallet, deployment, account, quest, transaction, payment, public, application, or submission boundaries remain sealed.`,
    },
  ];
}

function renderGrantExpeditionGame(lane) {
  const sites = buildGrantExpeditionSites(lane);
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, sites.length - 1);
  const current = sites[currentStep];
  const routePower = Math.round(sites.reduce((sum, site) => sum + site.score, 0) / sites.length);
  const verdict = lane.counts.blockers ? "Gate Camp" : routePower >= 74 ? "Route Ready" : "Scout More";
  return `
    <section class="detail-section">
      <p class="eyebrow">Lane-Specific Minigame</p>
      <div class="grant-expedition-board" style="${laneStyle(lane)}">
        <div class="grant-expedition-glow" aria-hidden="true"></div>
        <div class="grant-hero">
          ${avatarMarkup(lane, "game-avatar")}
          <div>
            <h3>${escapeHtml(lane.visual?.minigame?.title ?? "Grant Expedition")}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic, 190))}</p>
          </div>
          <div class="grant-verdict">
            <strong>${escapeHtml(verdict)}</strong>
            <span>${routePower}% route</span>
          </div>
        </div>
        <div class="grant-map" style="--grant-route-power:${routePower}%" aria-hidden="true">
          <div class="grant-route-line"></div>
          ${sites
            .map(
              (site, index) =>
                `<span class="grant-portal ${escapeHtml(site.status)} ${index === currentStep ? "active" : ""}" style="--grant-x:${site.x}%; --grant-y:${site.y}%; --grant-score:${site.score}%"></span>`
            )
            .join("")}
          <i></i><i></i><i></i>
        </div>
        <div class="grant-site-grid">
          ${sites.map((site, index) => renderGrantSite(site, index, currentStep)).join("")}
        </div>
        <div class="game-status">
          <div>
            <p class="eyebrow">Focused Route</p>
            <h3>${escapeHtml(current.title)}</h3>
            <p>${escapeHtml(compactText(current.body, 230))}</p>
          </div>
          <div class="game-actions">
            <button class="tool-button" type="button" data-game-action="reset" title="Reset grant expedition focus">0</button>
            <button class="tool-button" type="button" data-game-action="prev" title="Previous grant route">-</button>
            <button class="tool-button" type="button" data-game-action="next" title="Next grant route">+</button>
          </div>
        </div>
      </div>
    </section>`;
}

function renderGrantSite(site, index, currentStep) {
  return `
    <article class="grant-site ${escapeHtml(site.status)} ${index === currentStep ? "is-current" : ""}">
      <div class="foundry-stage-top">
        <span>${index + 1}</span>
        <strong>${escapeHtml(stateLabel(site.status))}</strong>
      </div>
      <h3>${escapeHtml(site.title)}</h3>
      <div class="grant-meter" style="--grant-score:${site.score}%"><span></span></div>
      <p>${escapeHtml(compactText(site.body, 150))}</p>
    </article>`;
}

function buildScopeRunStations(lane) {
  const trail = lane.trail ?? [];
  const counts = lane.counts ?? {};
  const gate = lane.serviceRequests?.[0] ?? lane.gateMap?.[0];
  const scopeHits = trail.filter((item) => /scope|rules|program|rendered|route|VRP|OSS|reachability|source-only/i.test(`${item.title} ${item.summary}`)).length;
  const duplicateHits = trail.filter((item) => /duplicate|dupe|stale|prior|existing|advisory|monitor|rejected|triage/i.test(`${item.title} ${item.summary}`)).length;
  const proofHits = trail.filter((item) => /static|proof|local|source|packet|artifact|Bazel|Java|reproduction|review/i.test(`${item.title} ${item.summary}`)).length;
  const privateHits = trail.filter((item) => /private|report|submission|disclosure|route|readiness|maintainer|acceptance|severity/i.test(`${item.title} ${item.summary}`)).length;
  const actionHits = trail.filter((item) => /account|submission|submit|external|public|testing|live|exploit|payout|approval|browser/i.test(`${item.title} ${item.summary}`)).length;
  const taskProgress = counts.tasks ? Math.round(((counts.completedTasks ?? 0) / counts.tasks) * 100) : 0;
  const scopeScore = Math.min(96, Math.round(34 + scopeHits * 8 + (counts.evidence ?? 0) * 1.6));
  const duplicateScore = Math.max(12, Math.min(94, Math.round(82 - duplicateHits * 4 + (counts.traces ?? 0) * 4)));
  const proofScore = Math.min(98, Math.round(32 + proofHits * 7 + (counts.artifacts ?? 0) * 3.2 + taskProgress * 0.16));
  const privateScore = Math.min(94, Math.round(30 + privateHits * 6 + (counts.outcomes ?? 0) * 6));
  const gateScore = Math.max(10, 92 - (counts.pendingRequests ?? 0) * 24 - (counts.blockers ?? 0) * 20 - actionHits * 2);
  return [
    {
      id: "scope",
      title: "Scope Wall",
      score: scopeScore,
      status: scopeScore >= 72 ? "verified" : "checking",
      x: 12,
      y: 64,
      body: `${scopeHits} scope, rule, program, rendered-route, VRP, OSS, source-only, or reachability signals define the safe boundary.`,
    },
    {
      id: "duplicate",
      title: "Duplicate Sweep",
      score: duplicateScore,
      status: duplicateHits ? "watch" : "clear",
      x: 32,
      y: 36,
      body: `${duplicateHits} duplicate, stale, existing, advisory, monitor, rejection, or triage signals are visible before any report route.`,
    },
    {
      id: "proof",
      title: "Static Proof",
      score: proofScore,
      status: proofScore >= 74 ? "sealed" : "building",
      x: 53,
      y: 58,
      body: `${proofHits} static, local, source, packet, artifact, toolchain, reproduction, or review signals support a no-touch proof path.`,
    },
    {
      id: "private",
      title: "Private Route",
      score: privateScore,
      status: privateScore >= 70 ? "ready" : "drafting",
      x: 73,
      y: 34,
      body: `${privateHits} private-report, disclosure, submission-route, maintainer, acceptance, severity, or readiness signals shape the report corridor.`,
    },
    {
      id: "approval",
      title: "Approval Gate",
      score: gateScore,
      status: "locked",
      x: 88,
      y: 68,
      body: gate
        ? `${gate.status ?? gate.route}: ${gate.riskGate ?? gate.gate}`
        : `${actionHits} account, submission, external, public, testing, exploit, payout, approval, or browser boundaries remain locked.`,
    },
  ];
}

function renderScopeRunGame(lane) {
  const stations = buildScopeRunStations(lane);
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, stations.length - 1);
  const current = stations[currentStep];
  const integrity = Math.round(stations.reduce((sum, station) => sum + station.score, 0) / stations.length);
  const verdict = lane.counts.blockers ? "Approval Hold" : integrity >= 74 ? "Route Safe" : "Check Scope";
  return `
    <section class="detail-section">
      <p class="eyebrow">Lane-Specific Minigame</p>
      <div class="scope-run-board" style="${laneStyle(lane)}">
        <div class="scope-run-glow" aria-hidden="true"></div>
        <div class="scope-hero">
          ${avatarMarkup(lane, "game-avatar")}
          <div>
            <h3>${escapeHtml(lane.visual?.minigame?.title ?? "Scope Run")}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic, 190))}</p>
          </div>
          <div class="scope-verdict">
            <strong>${escapeHtml(verdict)}</strong>
            <span>${integrity}% guarded</span>
          </div>
        </div>
        <div class="scope-citadel" style="--scope-integrity:${integrity}%" aria-hidden="true">
          <div class="scope-wall-line"></div>
          ${stations
            .map(
              (station, index) =>
                `<span class="scope-sentinel ${escapeHtml(station.status)} ${index === currentStep ? "active" : ""}" style="--scope-x:${station.x}%; --scope-y:${station.y}%; --scope-score:${station.score}%"></span>`
            )
            .join("")}
          <i></i><i></i><i></i>
        </div>
        <div class="scope-station-grid">
          ${stations.map((station, index) => renderScopeStation(station, index, currentStep)).join("")}
        </div>
        <div class="game-status">
          <div>
            <p class="eyebrow">Focused Guard</p>
            <h3>${escapeHtml(current.title)}</h3>
            <p>${escapeHtml(compactText(current.body, 230))}</p>
          </div>
          <div class="game-actions">
            <button class="tool-button" type="button" data-game-action="reset" title="Reset scope run focus">0</button>
            <button class="tool-button" type="button" data-game-action="prev" title="Previous scope station">-</button>
            <button class="tool-button" type="button" data-game-action="next" title="Next scope station">+</button>
          </div>
        </div>
      </div>
    </section>`;
}

function renderScopeStation(station, index, currentStep) {
  return `
    <article class="scope-station ${escapeHtml(station.status)} ${index === currentStep ? "is-current" : ""}">
      <div class="foundry-stage-top">
        <span>${index + 1}</span>
        <strong>${escapeHtml(stateLabel(station.status))}</strong>
      </div>
      <h3>${escapeHtml(station.title)}</h3>
      <div class="scope-meter" style="--scope-score:${station.score}%"><span></span></div>
      <p>${escapeHtml(compactText(station.body, 150))}</p>
    </article>`;
}

function buildPayoutVaultStages(lane) {
  const trail = lane.trail ?? [];
  const counts = lane.counts ?? {};
  const gate = lane.serviceRequests?.[0] ?? lane.gateMap?.[0];
  const submittedHits = trail.filter((item) => /submit|submitted|PR|pull request|issue|microbounty|bounty|solver|work|attempt/i.test(`${item.title} ${item.summary}`)).length;
  const ownerWatchHits = trail.filter((item) => /owner|award|selected|selection|accepted|maintainer|review|request signal|merge|mergeable/i.test(`${item.title} ${item.summary}`)).length;
  const ownerHits = trail.filter((item) => {
    const text = `${item.title} ${item.summary}`;
    const hasPositiveSignal = /owner selected|owner selection confirmed|selected solver|awarded to|bounty awarded|award confirmed|accepted by owner|accepted by maintainer|merged by maintainer|merged upstream|mergeable by maintainer|maintainer accepted|maintainer requested payout details|request signal received/i.test(text);
    const hasMonitorOnlySignal = /no owner|no .*award|no .*payment|no .*request signal|requires bounty owner selection|monitor[_ -]?only|keep_monitoring|monitor .*owner award|for owner award|owner award\/payment|payout clarification|until owner/i.test(text);
    return hasPositiveSignal && !hasMonitorOnlySignal;
  }).length;
  const evidenceHits = trail.filter((item) => /payment|payout|paid|RTC|cashflow|monitor|evidence|ledger|artifact|status/i.test(`${item.title} ${item.summary}`)).length;
  const collisionHits = trail.filter((item) => /competing|collision|other lead|attribution|duplicate|crowded|non-maintainer|low-trust/i.test(`${item.title} ${item.summary}`)).length;
  const detailHits = trail.filter((item) => /wallet|payment detail|payout detail|bank|invoice|tax|kyc|public|response|comment|account|approval/i.test(`${item.title} ${item.summary}`)).length;
  const taskProgress = counts.tasks ? Math.round(((counts.completedTasks ?? 0) / counts.tasks) * 100) : 0;
  const submittedScore = Math.min(96, Math.round(34 + submittedHits * 6 + (counts.evidence ?? 0) * 1.8));
  const ownerScore = Math.min(94, Math.round(22 + ownerHits * 18 + taskProgress * 0.22));
  const evidenceScore = Math.min(96, Math.round(30 + evidenceHits * 5 + (counts.artifacts ?? 0) * 3 + (counts.outcomes ?? 0) * 5));
  const collisionScore = Math.max(12, Math.min(92, Math.round(84 - collisionHits * 5 + (counts.evidence ?? 0) * 0.8)));
  const gateScore = Math.max(10, 92 - (counts.pendingRequests ?? 0) * 24 - (counts.blockers ?? 0) * 20 - detailHits * 3);
  return [
    {
      id: "submitted",
      title: "Submitted Work",
      score: submittedScore,
      status: submittedScore >= 72 ? "indexed" : "watching",
      x: 12,
      y: 66,
      body: `${submittedHits} submitted-work, issue, PR, microbounty, bounty, solver, or attempt signals are visible in the payout trail.`,
    },
    {
      id: "owner",
      title: "Owner Signal",
      score: ownerScore,
      status: ownerHits > 0 && ownerScore >= 72 ? "awarded" : "monitoring",
      x: 32,
      y: 36,
      body: `${ownerHits} positive owner-selection signals and ${ownerWatchHits} watched owner, award, maintainer, review, merge, or request-signal mentions are visible before payout handling.`,
    },
    {
      id: "evidence",
      title: "Payment Evidence",
      score: evidenceScore,
      status: evidenceScore >= 72 ? "logged" : "empty",
      x: 53,
      y: 58,
      body: `${evidenceHits} payment, payout, cashflow, monitor, evidence, ledger, artifact, or status records are indexed for local review.`,
    },
    {
      id: "collision",
      title: "Collision Check",
      score: collisionScore,
      status: collisionHits ? "watch" : "clear",
      x: 73,
      y: 34,
      body: `${collisionHits} competing, attribution, duplicate, crowded, other-lead, non-maintainer, or low-trust signals affect the claim route.`,
    },
    {
      id: "gate",
      title: "Payout Detail Gate",
      score: gateScore,
      status: "locked",
      x: 88,
      y: 68,
      body: gate
        ? `${gate.status ?? gate.route}: ${gate.riskGate ?? gate.gate}`
        : `${detailHits} wallet, bank, invoice, tax, public response, account, or approval boundaries remain locked until the owner confirms them.`,
    },
  ];
}

function renderPayoutVaultGame(lane) {
  const stages = buildPayoutVaultStages(lane);
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, stages.length - 1);
  const current = stages[currentStep];
  const vaultScore = Math.round(stages.reduce((sum, stage) => sum + stage.score, 0) / stages.length);
  const ownerReady = stages.some((stage) => stage.id === "owner" && stage.status === "awarded");
  const verdict = lane.counts.blockers ? "Gate Hold" : ownerReady ? "Payout Watch" : "Monitor Only";
  return `
    <section class="detail-section">
      <p class="eyebrow">Lane-Specific Minigame</p>
      <div class="payout-vault-board" style="${laneStyle(lane)}">
        <div class="payout-vault-glow" aria-hidden="true"></div>
        <div class="payout-hero">
          ${avatarMarkup(lane, "game-avatar")}
          <div>
            <h3>${escapeHtml(lane.visual?.minigame?.title ?? "Payout Vault")}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic, 190))}</p>
          </div>
          <div class="payout-verdict">
            <strong>${escapeHtml(verdict)}</strong>
            <span>${vaultScore}% sealed</span>
          </div>
        </div>
        <div class="payout-vault-sim" style="--payout-score:${vaultScore}%" aria-hidden="true">
          <div class="payout-route-line"></div>
          ${stages
            .map(
              (stage, index) =>
                `<span class="payout-lock ${escapeHtml(stage.status)} ${index === currentStep ? "active" : ""}" style="--payout-x:${stage.x}%; --payout-y:${stage.y}%; --payout-stage-score:${stage.score}%"></span>`
            )
            .join("")}
          <i></i><i></i><i></i>
        </div>
        <div class="payout-stage-grid">
          ${stages.map((stage, index) => renderPayoutStage(stage, index, currentStep)).join("")}
        </div>
        <div class="game-status">
          <div>
            <p class="eyebrow">Focused Vault</p>
            <h3>${escapeHtml(current.title)}</h3>
            <p>${escapeHtml(compactText(current.body, 230))}</p>
          </div>
          <div class="game-actions">
            <button class="tool-button" type="button" data-game-action="reset" title="Reset payout vault focus">0</button>
            <button class="tool-button" type="button" data-game-action="prev" title="Previous payout vault station">-</button>
            <button class="tool-button" type="button" data-game-action="next" title="Next payout vault station">+</button>
          </div>
        </div>
      </div>
    </section>`;
}

function renderPayoutStage(stage, index, currentStep) {
  return `
    <article class="payout-stage ${escapeHtml(stage.status)} ${index === currentStep ? "is-current" : ""}">
      <div class="foundry-stage-top">
        <span>${index + 1}</span>
        <strong>${escapeHtml(stateLabel(stage.status))}</strong>
      </div>
      <h3>${escapeHtml(stage.title)}</h3>
      <div class="payout-meter" style="--payout-stage-score:${stage.score}%"><span></span></div>
      <p>${escapeHtml(compactText(stage.body, 150))}</p>
    </article>`;
}

function buildClaimScoutCards(lane) {
  const promotion = lane.promotionCandidate ?? {};
  const hasLocalProof = lane.quest?.checkpoints?.some((checkpoint) => checkpoint.title === "Local Proof" && checkpoint.status === "complete");
  const browserRequest = lane.serviceRequests?.find((request) => request.type?.includes("browser")) ?? lane.serviceRequests?.[0];
  const duplicateSignals = (lane.trail ?? []).filter((item) => /duplicate|claim|PR|pull request|competing/i.test(`${item.title} ${item.summary}`)).length;
  return [
    {
      id: "target",
      title: "Target Signal",
      score: promotion.score ?? Math.max(42, Math.min(96, Math.round(lane.score / 18))),
      status: promotion.ready_for_manual_promotion ? "ranked" : "scouting",
      body: promotion.score_rationale ?? "Use local evidence to decide whether the bounty deserves a live refresh.",
    },
    {
      id: "duplicate",
      title: "Duplicate Risk",
      score: Math.max(8, 100 - duplicateSignals * 8),
      status: duplicateSignals ? "watch" : "clear",
      body: duplicateSignals
        ? `${duplicateSignals} local duplicate or claim-risk signals found in the trail.`
        : "No duplicate-risk terms are visible in the current local trail.",
    },
    {
      id: "proof",
      title: "Local Proof",
      score: hasLocalProof ? 88 : 36,
      status: hasLocalProof ? "complete" : "needed",
      body: hasLocalProof
        ? "A local proof exists, so the lane can reason before touching external surfaces."
        : "Create a local proof before any browser, public claim, or payout route.",
    },
    {
      id: "gate",
      title: "Live Gate",
      score: lane.counts.blockers ? 24 : 82,
      status: lane.counts.blockers ? "blocked" : "open",
      body: browserRequest
        ? `${browserRequest.status}: ${browserRequest.riskGate}`
        : "No live browser/public-action gate is currently attached.",
    },
  ];
}

function renderClaimScoutGame(lane) {
  const cards = buildClaimScoutCards(lane);
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, cards.length - 1);
  const current = cards[currentStep];
  const totalScore = Math.round(cards.reduce((sum, card) => sum + card.score, 0) / cards.length);
  const goNoGo = lane.counts.blockers ? "Parked" : totalScore >= 70 ? "Scoutable" : "Needs Proof";
  return `
    <section class="detail-section">
      <p class="eyebrow">Lane-Specific Minigame</p>
      <div class="claim-scout-board" style="${laneStyle(lane)}">
        <div class="claim-scout-hero">
          ${avatarMarkup(lane, "game-avatar")}
          <div>
            <h3>${escapeHtml(lane.visual?.minigame?.title ?? "Claim Scout")}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic, 180))}</p>
          </div>
          <div class="scout-verdict">
            <strong>${escapeHtml(goNoGo)}</strong>
            <span>${totalScore}/100</span>
          </div>
        </div>
        <div class="scout-radar" aria-hidden="true">
          <div class="radar-sweep"></div>
          ${cards.map((card, index) => `<span class="radar-dot ${index === currentStep ? "active" : ""}" style="--dot-angle:${index * 82 + 18}deg; --dot-distance:${34 + (card.score % 24)}px"></span>`).join("")}
        </div>
        <div class="scout-card-grid">
          ${cards.map((card, index) => renderScoutCard(card, index, currentStep)).join("")}
        </div>
        <div class="game-status">
          <div>
            <p class="eyebrow">Focused Scan</p>
            <h3>${escapeHtml(current.title)}</h3>
            <p>${escapeHtml(compactText(current.body, 220))}</p>
          </div>
          <div class="game-actions">
            <button class="tool-button" type="button" data-game-action="reset" title="Reset scout focus">0</button>
            <button class="tool-button" type="button" data-game-action="prev" title="Previous scout card">-</button>
            <button class="tool-button" type="button" data-game-action="next" title="Next scout card">+</button>
          </div>
        </div>
      </div>
    </section>`;
}

function renderScoutCard(card, index, currentStep) {
  return `
    <article class="scout-card ${escapeHtml(card.status)} ${index === currentStep ? "is-current" : ""}">
      <div class="lane-button-top">
        <h3>${escapeHtml(card.title)}</h3>
        <span class="badge ${card.status === "blocked" ? "gated" : card.status === "complete" ? "unlocked" : "advancing"}">${escapeHtml(stateLabel(card.status))}</span>
      </div>
      <div class="scout-meter" style="--scout-score:${card.score}%"><span></span></div>
      <p>${escapeHtml(compactText(card.body, 150))}</p>
    </article>`;
}

function buildSystemsGridCells(lane) {
  const trail = lane.trail ?? [];
  const counts = lane.counts ?? {};
  const gates = lane.gateMap ?? [];
  const requests = lane.serviceRequests ?? [];
  const text = (item) => `${item.title} ${item.summary}`;
  const schemaHits = trail.filter((item) => /schema|migration|source spec|service catalog|contract|fixture|adapter|runtime/i.test(text(item))).length;
  const queueHits = trail.filter((item) => /queue|service request|worker|dequeue|outbox|state-machine|assignment|pool/i.test(text(item))).length;
  const traceHits = trail.filter((item) => /trace|audit|ledger|event|validation|runner|replay|snapshot/i.test(text(item))).length;
  const gateHits = trail.filter((item) => /gate|guard|approval|review|blocked|rejected|requires|safety|no external/i.test(text(item))).length;
  const coverageHits = trail.filter((item) => /coverage|dispatch|department|lane|money path|next-lane|expansion|manager|CEO/i.test(text(item))).length;
  const taskProgress = counts.tasks ? Math.round(((counts.completedTasks ?? 0) / counts.tasks) * 100) : 0;
  const taskScore = Math.max(20, taskProgress);
  const artifactScore = Math.min(98, Math.round(34 + (counts.artifacts ?? 0) * 0.06 + (counts.evidence ?? 0) * 0.22 + schemaHits * 1.3));
  const queueScore = Math.max(12, Math.min(96, Math.round(82 + queueHits * 0.9 - (counts.pendingRequests ?? 0) * 9 - (counts.blockers ?? 0) * 4)));
  const traceScore = Math.min(98, Math.round(32 + (counts.traces ?? 0) * 0.18 + (counts.outcomes ?? 0) * 0.14 + traceHits * 0.9));
  const gateScore = Math.max(10, Math.min(92, Math.round(88 - (counts.blockers ?? 0) * 14 - (counts.pendingRequests ?? 0) * 10 + gateHits * 0.7)));
  const routerScore = Math.min(96, Math.round(36 + coverageHits * 4 + (counts.outcomes ?? 0) * 0.06 + (counts.traces ?? 0) * 0.04));
  return [
    {
      id: "tasks",
      title: "Task Engine",
      score: taskScore,
      status: taskProgress >= 96 ? "synchronized" : "balancing",
      x: 13,
      y: 62,
      body: `${counts.completedTasks ?? 0}/${counts.tasks ?? 0} tasks are closed, turning platform work into visible company progress.`,
    },
    {
      id: "artifacts",
      title: "Artifact Matrix",
      score: artifactScore,
      status: artifactScore >= 78 ? "indexed" : "mapping",
      x: 29,
      y: 35,
      body: `${counts.artifacts ?? 0} artifacts, ${counts.evidence ?? 0} evidence records, and ${schemaHits} schema or contract signals feed the reusable knowledge layer.`,
    },
    {
      id: "queue",
      title: "Service Queue",
      score: queueScore,
      status: (counts.pendingRequests ?? 0) ? "reviewing" : "flowing",
      x: 45,
      y: 66,
      body: `${requests.length} service requests, ${counts.pendingRequests ?? 0} pending reviews, and ${queueHits} queue or worker signals define the execution corridor.`,
    },
    {
      id: "traces",
      title: "Trace Spine",
      score: traceScore,
      status: traceScore >= 76 ? "replaying" : "recording",
      x: 61,
      y: 34,
      body: `${counts.traces ?? 0} traces, ${counts.outcomes ?? 0} outcomes, and ${traceHits} audit or validation signals make the company history inspectable.`,
    },
    {
      id: "gates",
      title: "Safety Gates",
      score: gateScore,
      status: (counts.blockers ?? 0) ? "gated" : "guarded",
      x: 77,
      y: 63,
      body: gates.length
        ? `${counts.blockers ?? 0} blockers and ${counts.pendingRequests ?? 0} pending requests remain explicit: ${compactText(gates[0].gate ?? gates[0].route ?? gates[0].id, 110)}.`
        : `${gateHits} gate, guard, approval, review, or safety signals keep risky execution visible.`,
    },
    {
      id: "router",
      title: "Expansion Router",
      score: routerScore,
      status: coverageHits >= 4 ? "routing" : "warming",
      x: 90,
      y: 38,
      body: `${coverageHits} coverage, dispatch, department, lane, or expansion signals help new lanes inherit the same control-plane pattern.`,
    },
  ];
}

function renderSystemsGridGame(lane) {
  const cells = buildSystemsGridCells(lane);
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, cells.length - 1);
  const current = cells[currentStep];
  const stability = Math.round(cells.reduce((sum, cell) => sum + cell.score, 0) / cells.length);
  const verdict = lane.counts.blockers ? "Guarded Core" : stability >= 78 ? "Grid Stable" : "Tune Grid";
  return `
    <section class="detail-section">
      <p class="eyebrow">Lane-Specific Minigame</p>
      <div class="systems-grid-board" style="${laneStyle(lane)}">
        <div class="systems-grid-glow" aria-hidden="true"></div>
        <div class="systems-hero">
          ${avatarMarkup(lane, "game-avatar")}
          <div>
            <h3>${escapeHtml(lane.visual?.minigame?.title ?? "Systems Grid")}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic, 190))}</p>
          </div>
          <div class="systems-verdict">
            <strong>${escapeHtml(verdict)}</strong>
            <span>${stability}% stable</span>
          </div>
        </div>
        <div class="systems-control-plane" style="--systems-stability:${stability}%" aria-hidden="true">
          <div class="systems-core"></div>
          <div class="systems-spine"></div>
          ${cells
            .map(
              (cell, index) =>
                `<span class="systems-node ${escapeHtml(cell.status)} ${index === currentStep ? "active" : ""}" style="--systems-x:${cell.x}%; --systems-y:${cell.y}%; --systems-score:${cell.score}%"></span>`
            )
            .join("")}
          <i></i><i></i><i></i><i></i>
        </div>
        <div class="systems-cell-grid">
          ${cells.map((cell, index) => renderSystemsCell(cell, index, currentStep)).join("")}
        </div>
        <div class="game-status">
          <div>
            <p class="eyebrow">Focused System</p>
            <h3>${escapeHtml(current.title)}</h3>
            <p>${escapeHtml(compactText(current.body, 230))}</p>
          </div>
          <div class="game-actions">
            <button class="tool-button" type="button" data-game-action="reset" title="Reset systems grid focus">0</button>
            <button class="tool-button" type="button" data-game-action="prev" title="Previous systems cell">-</button>
            <button class="tool-button" type="button" data-game-action="next" title="Next systems cell">+</button>
          </div>
        </div>
      </div>
    </section>`;
}

function renderSystemsCell(cell, index, currentStep) {
  return `
    <article class="systems-cell ${escapeHtml(cell.status)} ${index === currentStep ? "is-current" : ""}">
      <div class="foundry-stage-top">
        <span>${index + 1}</span>
        <strong>${escapeHtml(stateLabel(cell.status))}</strong>
      </div>
      <h3>${escapeHtml(cell.title)}</h3>
      <div class="systems-meter" style="--systems-score:${cell.score}%"><span></span></div>
      <p>${escapeHtml(compactText(cell.body, 145))}</p>
    </article>`;
}

function buildSignalHarvestBeds(lane) {
  const trail = lane.trail ?? [];
  const counts = lane.counts ?? {};
  const gate = lane.serviceRequests?.[0] ?? lane.gateMap?.[0];
  const topicHits = trail.filter((item) => /topic|trend|content|post|reply|audience|social|growth|signal/i.test(`${item.title} ${item.summary}`)).length;
  const proofHits = trail.filter((item) => /proof|evidence|local|sample|packet|research/i.test(`${item.title} ${item.summary}`)).length;
  const voiceHits = trail.filter((item) => /voice|spam|account|post|reply|follow|public|policy/i.test(`${item.title} ${item.summary}`)).length;
  const harvestScore = Math.min(98, Math.round(28 + (counts.evidence ?? 0) * 8 + topicHits * 4 + (counts.outcomes ?? 0) * 7));
  const proofScore = Math.min(96, Math.round(32 + proofHits * 9 + (counts.artifacts ?? 0) * 2.4));
  const voiceScore = Math.max(14, 92 - voiceHits * 9 - (counts.blockers ?? 0) * 18);
  const trendScore = Math.min(94, Math.round(36 + topicHits * 7 + (counts.traces ?? 0) * 4));
  const gateScore = Math.max(12, 88 - (counts.pendingRequests ?? 0) * 24 - (counts.blockers ?? 0) * 18);
  return [
    {
      id: "topics",
      title: "Topic Bloom",
      score: harvestScore,
      status: harvestScore >= 72 ? "ripe" : "sprouting",
      body: `${topicHits} topic or social-growth trail signals are feeding the next content angle.`,
    },
    {
      id: "proof",
      title: "Proof Compost",
      score: proofScore,
      status: proofScore >= 74 ? "rich" : "building",
      body: `${proofHits} proof-like records and ${counts.artifacts ?? 0} artifacts can support non-generic public ideas later.`,
    },
    {
      id: "voice",
      title: "Voice Shield",
      score: voiceScore,
      status: voiceScore >= 70 ? "clean" : "sensitive",
      body: voiceHits
        ? `${voiceHits} voice, posting, account, or policy-sensitive signals keep this lane careful.`
        : "No obvious voice or account-action hazards are dominant in the current trail.",
    },
    {
      id: "timing",
      title: "Trend Window",
      score: trendScore,
      status: trendScore >= 70 ? "open" : "watching",
      body: `${counts.traces ?? 0} trace records and ${topicHits} signal hits help decide when a topic is worth harvesting.`,
    },
    {
      id: "gate",
      title: "Account Gate",
      score: gateScore,
      status: (counts.blockers ?? 0) ? "gated" : "clear",
      body: gate
        ? `${gate.status ?? gate.route}: ${gate.riskGate ?? gate.gate}`
        : "No account-action gate is attached, but public posting still requires explicit approval.",
    },
  ];
}

function renderSignalHarvestGame(lane) {
  const beds = buildSignalHarvestBeds(lane);
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, beds.length - 1);
  const current = beds[currentStep];
  const vitality = Math.round(beds.reduce((sum, bed) => sum + bed.score, 0) / beds.length);
  const verdict = lane.counts.blockers ? "Gate Bloom" : vitality >= 72 ? "Harvest Ready" : "Seed More";
  return `
    <section class="detail-section">
      <p class="eyebrow">Lane-Specific Minigame</p>
      <div class="signal-harvest-board" style="${laneStyle(lane)}">
        <div class="signal-garden-glow" aria-hidden="true"></div>
        <div class="signal-harvest-hero">
          ${avatarMarkup(lane, "game-avatar")}
          <div>
            <h3>${escapeHtml(lane.visual?.minigame?.title ?? "Signal Harvest")}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic, 190))}</p>
          </div>
          <div class="harvest-verdict">
            <strong>${escapeHtml(verdict)}</strong>
            <span>${vitality}% vitality</span>
          </div>
        </div>
        <div class="harvest-garden" aria-hidden="true">
          ${beds
            .map(
              (bed, index) =>
                `<span class="harvest-bloom ${index === currentStep ? "active" : ""}" style="--bloom-x:${14 + index * 18}%; --bloom-y:${68 - (bed.score % 38)}%; --bloom-score:${bed.score}%"></span>`
            )
            .join("")}
          <i></i><i></i><i></i>
        </div>
        <div class="harvest-bed-grid">
          ${beds.map((bed, index) => renderHarvestBed(bed, index, currentStep)).join("")}
        </div>
        <div class="game-status">
          <div>
            <p class="eyebrow">Focused Bed</p>
            <h3>${escapeHtml(current.title)}</h3>
            <p>${escapeHtml(compactText(current.body, 230))}</p>
          </div>
          <div class="game-actions">
            <button class="tool-button" type="button" data-game-action="reset" title="Reset signal harvest focus">0</button>
            <button class="tool-button" type="button" data-game-action="prev" title="Previous signal bed">-</button>
            <button class="tool-button" type="button" data-game-action="next" title="Next signal bed">+</button>
          </div>
        </div>
      </div>
    </section>`;
}

function renderHarvestBed(bed, index, currentStep) {
  return `
    <article class="harvest-bed ${escapeHtml(bed.status)} ${index === currentStep ? "is-current" : ""}">
      <div class="foundry-stage-top">
        <span>${index + 1}</span>
        <strong>${escapeHtml(stateLabel(bed.status))}</strong>
      </div>
      <h3>${escapeHtml(bed.title)}</h3>
      <div class="harvest-meter" style="--harvest-score:${bed.score}%"><span></span></div>
      <p>${escapeHtml(compactText(bed.body, 150))}</p>
    </article>`;
}

function buildFoundryStages(lane) {
  const trail = lane.trail ?? [];
  const counts = lane.counts ?? {};
  const blockers = counts.blockers ?? 0;
  const pendingRequests = counts.pendingRequests ?? 0;
  const serviceRequest = lane.serviceRequests?.[0];
  const promotion = lane.promotionCandidate ?? {};
  const proofHits = trail.filter((item) => /proof|evidence|local|test|validated/i.test(`${item.title} ${item.summary}`)).length;
  const qualityHits = trail.filter((item) => /quality|gate|hold|register|complete|package|ready/i.test(`${item.title} ${item.summary}`)).length;
  const taskProgress = counts.tasks ? Math.round(((counts.completedTasks ?? 0) / counts.tasks) * 100) : 0;
  const artifactScore = Math.min(96, Math.round(36 + (counts.artifacts ?? 0) * 0.75));
  const gateScore = Math.max(12, 92 - blockers * 22 - pendingRequests * 8);
  return [
    {
      id: "demand",
      title: "Demand Proof",
      score: Math.min(96, Math.round(38 + (counts.evidence ?? 0) * 1.8 + proofHits * 2.2)),
      status: proofHits || counts.evidence > 4 ? "forged" : "warming",
      body: `${counts.evidence ?? 0} evidence records and ${proofHits} local proof signals are feeding the product read.`,
    },
    {
      id: "brief",
      title: "Build Brief",
      score: Math.max(24, taskProgress),
      status: taskProgress >= 90 ? "forged" : "active",
      body: `${counts.completedTasks ?? 0}/${counts.tasks ?? 0} lane tasks are closed, shaping the next reusable packet.`,
    },
    {
      id: "pack",
      title: "Asset Pack",
      score: artifactScore,
      status: (counts.artifacts ?? 0) > 30 ? "forged" : "active",
      body: `${counts.artifacts ?? 0} artifacts are available for bundling into templates, plugins, docs, or QA notes.`,
    },
    {
      id: "quality",
      title: "Quality Pass",
      score: Math.min(94, Math.round(30 + qualityHits * 7 + (counts.outcomes ?? 0) * 4)),
      status: qualityHits > 3 ? "forged" : "active",
      body: `${qualityHits} trail signals mention gates, holds, package readiness, or quality decisions.`,
    },
    {
      id: "gate",
      title: "Listing Gate",
      score: gateScore,
      status: blockers ? "blocked" : promotion.ready_for_manual_promotion ? "ready" : "queued",
      body: serviceRequest
        ? `${serviceRequest.status}: ${serviceRequest.riskGate}`
        : "No live marketplace gate is attached, so the foundry stays local-only until one appears.",
    },
  ];
}

function renderFoundryRunGame(lane) {
  const stages = buildFoundryStages(lane);
  const currentStep = Math.min(state.gameStepByLane[lane.id] ?? 0, stages.length - 1);
  const current = stages[currentStep];
  const heat = Math.round(stages.reduce((sum, stage) => sum + stage.score, 0) / stages.length);
  const verdict = lane.counts.blockers ? "Gate Hold" : heat >= 75 ? "Ship Packet" : "Keep Forging";
  return `
    <section class="detail-section">
      <p class="eyebrow">Lane-Specific Minigame</p>
      <div class="foundry-board" style="${laneStyle(lane)}">
        <div class="foundry-glow" aria-hidden="true"></div>
        <div class="foundry-hero">
          ${avatarMarkup(lane, "game-avatar")}
          <div>
            <h3>${escapeHtml(lane.visual?.minigame?.title ?? "Foundry Run")}</h3>
            <p>${escapeHtml(compactText(lane.visual?.minigame?.mechanic, 190))}</p>
          </div>
          <div class="foundry-verdict">
            <strong>${escapeHtml(verdict)}</strong>
            <span>${heat}% heat</span>
          </div>
        </div>
        <div class="foundry-rail" style="--foundry-heat:${heat}%">
          ${stages.map((stage, index) => `<span class="${index === currentStep ? "active" : ""}" style="--stage-score:${stage.score}%"></span>`).join("")}
        </div>
        <div class="foundry-stage-grid">
          ${stages.map((stage, index) => renderFoundryStage(stage, index, currentStep)).join("")}
        </div>
        <div class="game-status">
          <div>
            <p class="eyebrow">Focused Station</p>
            <h3>${escapeHtml(current.title)}</h3>
            <p>${escapeHtml(compactText(current.body, 230))}</p>
          </div>
          <div class="game-actions">
            <button class="tool-button" type="button" data-game-action="reset" title="Reset foundry focus">0</button>
            <button class="tool-button" type="button" data-game-action="prev" title="Previous foundry station">-</button>
            <button class="tool-button" type="button" data-game-action="next" title="Next foundry station">+</button>
          </div>
        </div>
      </div>
    </section>`;
}

function renderFoundryStage(stage, index, currentStep) {
  return `
    <article class="foundry-stage ${escapeHtml(stage.status)} ${index === currentStep ? "is-current" : ""}">
      <div class="foundry-stage-top">
        <span>${index + 1}</span>
        <strong>${escapeHtml(stateLabel(stage.status))}</strong>
      </div>
      <h3>${escapeHtml(stage.title)}</h3>
      <div class="foundry-meter" style="--forge-score:${stage.score}%"><span></span></div>
      <p>${escapeHtml(compactText(stage.body, 150))}</p>
    </article>`;
}

function renderCheckpoint(checkpoint, index, currentStep) {
  const active = index === currentStep ? "is-current" : "";
  const cleared = index < currentStep ? "cleared" : "";
  return `
    <article class="checkpoint ${escapeHtml(checkpoint.status)} ${active} ${cleared}">
      <span>${index + 1}</span>
      <h3>${escapeHtml(checkpoint.title)}</h3>
      <p>${escapeHtml(stateLabel(checkpoint.status))}</p>
    </article>`;
}

function renderGateRows(lane) {
  const gates = lane.gateMap.length
    ? lane.gateMap
    : lane.serviceRequests.map((request) => ({
        id: request.id,
        gate: request.riskGate,
        route: request.status,
        workerType: request.type,
        nextAction: request.requestedAction,
      }));

  if (!gates.length) return `<p class="small-muted">No blockers recorded for this lane.</p>`;
  return gates
    .map(
      (gate) => `
      <article class="request-row">
        <div class="lane-button-top">
          <h3>${escapeHtml(compactText(gate.workerType || gate.id, 56))}</h3>
          <span class="badge gated">${escapeHtml(stateLabel(gate.route || "blocked"))}</span>
        </div>
        <p>${escapeHtml(compactText(gate.gate, 160))}</p>
        <p>${escapeHtml(compactText(gate.nextAction, 180))}</p>
      </article>`
    )
    .join("");
}

function renderTimeline(lane) {
  if (!lane.milestones.length) return `<p class="small-muted">No milestones yet.</p>`;
  return lane.milestones
    .map(
      (item) => `
      <article class="timeline-item">
        <h3>${escapeHtml(item.title)}</h3>
        <p>${escapeHtml(shortDate(item.time))} - ${escapeHtml(stateLabel(item.kind))} - ${escapeHtml(stateLabel(item.status))}</p>
        <p>${escapeHtml(compactText(item.summary, 220))}</p>
        ${item.artifact ? `<a href="${escapeHtml(item.artifact)}">${escapeHtml(item.artifact)}</a>` : ""}
      </article>`
    )
    .join("");
}

function renderTaskRow(task) {
  return `
    <article class="request-row">
      <div class="lane-button-top">
        <h3>${escapeHtml(compactText(task.title, 72))}</h3>
        <span class="badge ${task.status === "complete" ? "unlocked" : "advancing"}">${escapeHtml(stateLabel(task.status))}</span>
      </div>
      <p>${escapeHtml(compactText(task.nextAction, 210))}</p>
    </article>`;
}

function renderAgentRoster() {
  const agents = state.snapshot.agents ?? [];
  el.agentCount.textContent = `${formatNumber(agents.length)} online`;
  el.agentRoster.innerHTML = `${renderAgentSpriteFoundry(agents)}${renderOperatorIdentityBay(agents)}${agents.map(renderAgentRosterCard).join("")}`;
}

function operatorIdentityBayStats(agents) {
  const lanes = state.snapshot?.lanes ?? [];
  const activeAgents = agents.filter((agent) => agent.status === "active").length;
  const portraitCount = agents.filter((agent) => Boolean(agent.visual?.avatar)).length;
  const laneBindings = agents.filter((agent) => Boolean(agent.lane?.id)).length;
  const stagedAsks = state.stagedDispatches.length;
  const spareCapacity = Math.max(1, lanes.length + 4 - agents.length);
  return [
    { label: "Active bots", value: activeAgents },
    { label: "Portraits", value: portraitCount },
    { label: "Lane binds", value: laneBindings },
    { label: "Staged asks", value: stagedAsks },
    { label: "Spare slots", value: spareCapacity },
  ];
}

function renderOperatorIdentityBay(agents) {
  const lanes = state.snapshot?.lanes ?? [];
  const leadAgent =
    agents.find((agent) => agent.lane?.id === state.selectedLaneId) ??
    agents.find((agent) => Boolean(agent.lane?.id)) ??
    agents[0];
  const leadLane = leadAgent?.lane ?? lanes.find((lane) => lane.id === state.selectedLaneId) ?? lanes[0];
  const accent = leadAgent?.visual?.accent ?? leadLane?.visual?.accent ?? "#44d7c9";
  const accentAlt = leadLane?.visual?.accentAlt ?? "#f4ba55";
  const stripAgents = agents.slice(0, 7);
  const identityStats = operatorIdentityBayStats(agents);
  return `
    <section class="operator-identity-bay" style="--identity-a:${escapeHtml(accent)}; --identity-b:${escapeHtml(accentAlt)}; --identity-art:url('./assets/system/operator-identity-bay-20260618.png')" aria-label="Operator Identity Bay">
      <div class="operator-identity-visual" aria-hidden="true">
        <div class="operator-identity-scanline"></div>
      </div>
      <div class="operator-identity-copy">
        <p class="eyebrow">Operator Identity Bay</p>
        <h3>${escapeHtml(leadAgent?.visual?.callsign ?? leadAgent?.agent_id ?? "Ready for new operators")}</h3>
        <p>${escapeHtml(compactText(leadAgent?.visual?.specialty ?? leadLane?.nextAction ?? "Portrait slots, lane bindings, and command links stay visible as the company expands.", 170))}</p>
        <div class="operator-identity-stats">
          ${identityStats
            .map(
              (stat) => `
              <div>
                <strong>${escapeHtml(formatNumber(stat.value))}</strong>
                <span>${escapeHtml(stat.label)}</span>
              </div>`
            )
            .join("")}
        </div>
        <div class="operator-identity-strip" aria-label="Mapped operator portraits">
          ${stripAgents
            .map(
              (agent) => `
              <button class="operator-identity-token" type="button" ${agent.lane?.id ? `data-agent-lane-id="${escapeHtml(agent.lane.id)}"` : ""} title="${escapeHtml(agent.visual?.callsign ?? agent.agent_id)}">
                ${agentRosterAvatar(agent)}
                <span>${escapeHtml(agent.visual?.callsign ?? agent.agent_id)}</span>
              </button>`
            )
            .join("")}
        </div>
        <div class="operator-identity-actions">
          <button class="tool-button" type="button" data-identity-action="comms">COM</button>
          <button class="tool-button" type="button" data-identity-action="assets">ASSET</button>
          <button class="tool-button" type="button" data-identity-action="forge">FORGE</button>
        </div>
      </div>
    </section>`;
}

function agentSpriteFoundryRecords(agents) {
  const suggestions = state.snapshot?.dispatchConsole?.suggestions ?? [];
  return agents
    .map((agent) => {
      const lane = agent.lane ? state.snapshot.lanes.find((item) => item.id === agent.lane.id) ?? agent.lane : null;
      const visual = agent.visual ?? {};
      const suggestion = suggestions
        .filter((item) => item.targetAgentId === agent.agent_id || item.laneId === lane?.id)
        .sort((a, b) => (b.urgency ?? 0) - (a.urgency ?? 0))[0];
      const staged = state.stagedDispatches.some((draft) => draft.laneId === lane?.id || draft.sourceId === suggestion?.id);
      const readyScore =
        (visual.avatar ? 28 : 0) +
        (visual.callsign ? 14 : 0) +
        (visual.specialty ? 14 : 0) +
        (lane?.id ? 18 : 0) +
        (agent.thread_id ? 14 : 0) +
        (suggestion ? 8 : 0) +
        (staged ? 4 : 0);
      return {
        agent,
        lane,
        visual,
        suggestion,
        staged,
        readyScore: Math.min(100, readyScore),
        tone: staged ? "staged" : suggestion ? "ready" : lane?.counts?.blockers ? "gated" : visual.avatar ? "mapped" : "open",
      };
    })
    .sort((a, b) => b.readyScore - a.readyScore || Number(Boolean(b.lane)) - Number(Boolean(a.lane)));
}

function agentSpriteFoundryStats(records) {
  const lanes = state.snapshot?.lanes ?? [];
  const portraitCount = records.filter((record) => Boolean(record.visual.avatar)).length;
  const laneBindings = records.filter((record) => Boolean(record.lane?.id)).length;
  const threadCount = records.filter((record) => Boolean(record.agent.thread_id)).length;
  const spareSlots = Math.max(4, lanes.length + 4 - records.length);
  return [
    { label: "bots", value: records.length },
    { label: "portraits", value: portraitCount },
    { label: "lane binds", value: laneBindings },
    { label: "threads", value: threadCount },
    { label: "future slots", value: spareSlots },
  ];
}

function agentConstellationBeacons(records) {
  const positions = [
    [50, 18],
    [66, 28],
    [78, 50],
    [64, 70],
    [50, 80],
    [34, 70],
    [22, 50],
    [34, 28],
  ];
  return records
    .filter((record) => Boolean(record.visual.avatar))
    .slice(0, positions.length)
    .map((record, index) => renderAgentConstellationBeacon(record, index, positions[index]))
    .join("");
}

function renderAgentConstellationBeacon(record, index, position) {
  const { agent, lane, visual, readyScore, tone } = record;
  const callsign = visual.callsign ?? agent.agent_id;
  const laneAttr = lane?.id ? `data-agent-sprite-lane="${escapeHtml(lane.id)}"` : "";
  return `
    <button
      class="agent-constellation-beacon ${escapeHtml(tone)} ${lane?.id === state.selectedLaneId ? "active" : ""}"
      type="button"
      ${laneAttr}
      data-agent-constellation-agent="${escapeHtml(agent.agent_id)}"
      style="--beacon-x:${position[0]}%; --beacon-y:${position[1]}%; --agent-a:${escapeHtml(visual.accent ?? lane?.visual?.accent ?? "#44d7c9")}; --agent-ready:${Math.max(8, readyScore)}%; --beacon-index:${index};"
      title="${escapeHtml(visual.specialty ?? lane?.name ?? callsign)}"
    >
      ${agentRosterAvatar(agent)}
      <span><strong>${escapeHtml(compactText(callsign, 28))}</strong><em>${escapeHtml(lane ? `L${formatNumber(lane.level ?? 1)}` : stateLabel(agent.status ?? "active"))}</em></span>
      <i aria-hidden="true"></i>
    </button>`;
}

function renderAgentSpriteFoundry(agents) {
  const records = agentSpriteFoundryRecords(agents);
  const selected =
    records.find((record) => record.lane?.id === state.selectedLaneId) ??
    records.find((record) => record.lane?.id) ??
    records[0];
  const stats = agentSpriteFoundryStats(records);
  const accent = selected?.visual?.accent ?? selected?.lane?.visual?.accent ?? "#44d7c9";
  const accentAlt = selected?.lane?.visual?.accentAlt ?? "#f4ba55";
  const style = `--sprite-a:${escapeHtml(accent)}; --sprite-b:${escapeHtml(accentAlt)}; --sprite-art:url('./assets/system/agent-constellation-bay-20260619.png')`;
  return `
    <section class="agent-sprite-foundry" style="${style}" aria-label="Agent Sprite Foundry">
      <div class="agent-sprite-visual">
        <img src="./assets/system/agent-constellation-bay-20260619.png" alt="" loading="lazy" />
        <div class="agent-constellation-overlay" aria-label="Agent constellation quick-select">
          ${agentConstellationBeacons(records)}
        </div>
        <span class="agent-sprite-scan"></span>
      </div>
      <div class="agent-sprite-copy">
        <div class="agent-sprite-head">
          <div>
            <p class="eyebrow">Agent Sprite Foundry</p>
            <h3>${escapeHtml(selected?.visual?.callsign ?? selected?.agent?.agent_id ?? "Bot character slots")}</h3>
            <p>${escapeHtml(compactText(selected?.visual?.specialty ?? selected?.lane?.nextAction ?? "A reusable character-production layer for portraits, sprite readiness, lane bindings, thread identity, and future bot slots.", 190))}</p>
          </div>
          <span class="badge ${escapeHtml(selected?.tone ?? "ready")}">${escapeHtml(selected ? stateLabel(selected.tone) : "ready")}</span>
        </div>
        <div class="agent-sprite-stats">
          ${stats
            .map(
              (stat) => `
              <span>
                <strong>${escapeHtml(formatNumber(stat.value))}</strong>
                <em>${escapeHtml(stat.label)}</em>
              </span>`
            )
            .join("")}
        </div>
        <div class="agent-sprite-actions">
          <button class="tool-button" type="button" data-agent-sprite-action="comms" title="Open selected bot Comms">COM</button>
          <button class="tool-button" type="button" data-agent-sprite-action="assets" title="Show agent portraits">ASSET</button>
          <button class="tool-button" type="button" data-agent-sprite-action="forge" title="Open creator bot gate">FORGE</button>
        </div>
        <div class="agent-sprite-grid" aria-label="Agent sprite readiness">
          ${records.slice(0, 12).map(renderAgentSpriteCard).join("")}
          ${renderAgentSpriteFutureSlots(records)}
        </div>
      </div>
    </section>`;
}

function renderAgentSpriteCard(record) {
  const { agent, lane, visual, suggestion, staged, readyScore, tone } = record;
  const callsign = visual.callsign ?? agent.agent_id;
  const laneAttr = lane?.id ? `data-agent-sprite-lane="${escapeHtml(lane.id)}"` : "";
  return `
    <article
      class="agent-sprite-card ${escapeHtml(tone)} ${lane?.id === state.selectedLaneId ? "active" : ""}"
      ${laneAttr}
      data-agent-sprite-agent="${escapeHtml(agent.agent_id)}"
      style="--agent-ready:${Math.max(8, readyScore)}%; --agent-a:${escapeHtml(visual.accent ?? lane?.visual?.accent ?? "#44d7c9")};"
    >
      <div class="agent-sprite-frame">
        ${agentRosterAvatar(agent)}
        <span aria-hidden="true"></span>
      </div>
      <div class="agent-sprite-card-copy">
        <p class="eyebrow">${escapeHtml(stateLabel(agent.status ?? "active"))}</p>
        <h4>${escapeHtml(compactText(callsign, 46))}</h4>
        <p>${escapeHtml(compactText(visual.specialty ?? suggestion?.reason ?? stateLabel(agent.role_id), 96))}</p>
      </div>
      <div class="agent-sprite-meter"><i></i></div>
      <div class="agent-sprite-card-stats">
        <span><strong>${visual.avatar ? "Y" : "N"}</strong><em>art</em></span>
        <span><strong>${lane ? `L${formatNumber(lane.level ?? 1)}` : "--"}</strong><em>lane</em></span>
        <span><strong>${staged ? "Q" : suggestion ? "A" : "--"}</strong><em>ask</em></span>
      </div>
    </article>`;
}

function renderAgentSpriteFutureSlots(records) {
  const laneCount = state.snapshot?.lanes?.length ?? 0;
  const spareSlots = Math.max(4, laneCount + 4 - records.length);
  return Array.from({ length: Math.min(4, spareSlots) }, (_, index) => {
    const slotNumber = records.length + index + 1;
    return `
      <article class="agent-sprite-future" style="--slot-index:${slotNumber};">
        <strong>Future bot slot ${formatNumber(slotNumber)}</strong>
        <span>Add portrait, callsign, specialty, thread, lane bind, and optional sprite frames.</span>
        <em>open socket</em>
      </article>`;
  }).join("");
}

function renderAgentRosterCard(agent) {
  const visual = agent.visual ?? {};
  const lane = agent.lane;
  const callsign = visual.callsign ?? agent.agent_id;
  const specialty = visual.specialty ?? stateLabel(agent.role_id);
  const laneState = lane?.state ?? "scouting";
  const laneAttr = lane?.id ? ` data-agent-lane-id="${escapeHtml(lane.id)}"` : "";
  return `
    <article class="operator-card" style="--agent-a:${escapeHtml(visual.accent ?? "#44d7c9")};"${laneAttr}>
      <div class="operator-card-top">
        ${agentRosterAvatar(agent)}
        <div>
          <p class="eyebrow">${escapeHtml(stateLabel(agent.status))}</p>
          <h3>${escapeHtml(callsign)}</h3>
          <p>${escapeHtml(compactText(specialty, 96))}</p>
        </div>
      </div>
      <div class="operator-lane">
        <span class="badge ${escapeHtml(laneState)}">${escapeHtml(lane ? stateLabel(laneState) : "unassigned")}</span>
        <strong>${escapeHtml(lane?.name ?? stateLabel(agent.department_id))}</strong>
      </div>
      <div class="operator-progress">
        <span>L${escapeHtml(lane?.level ?? 1)}</span>
        <div class="progress-track"><div class="progress-fill" style="width:${lane ? Math.max(8, Math.min(100, lane.level * 8)) : 8}%"></div></div>
      </div>
      <p class="operator-next">${escapeHtml(compactText(lane?.nextAction ?? agent.thread_id ?? "Ready for assignment.", 150))}</p>
    </article>`;
}

function visualAssetRecords() {
  const lanes = state.snapshot?.lanes ?? [];
  const agents = state.snapshot?.agents ?? [];
  const records = [];

  lanes.forEach((lane) => {
    const visual = lane.visual ?? {};
    if (visual.avatar) {
      records.push({
        id: `lane-${lane.id}`,
        kind: "lane",
        title: `${lane.name} avatar`,
        subtitle: visual.realm ?? lane.department,
        image: visual.avatar,
        laneId: lane.id,
        view: "overview",
        badge: `L${lane.level}`,
        meta: `${stateLabel(lane.state)} path - ${formatNumber(lane.counts?.tasks ?? 0)} tasks`,
        accent: visual.accent ?? "#44d7c9",
        accentAlt: visual.accentAlt ?? "#f4ba55",
      });
    }

    const minigame = visual.minigame ?? {};
    if (minigame.texture) {
      records.push({
        id: `game-${lane.id}`,
        kind: "game",
        title: `${minigame.title ?? lane.name} texture`,
        subtitle: minigame.mechanic ?? "Lane minigame backdrop",
        image: minigame.texture,
        laneId: lane.id,
        view: "game",
        badge: minigame.id ?? "game",
        meta: `${lane.name} module - ${minigameDefinition(lane) ? "custom renderer" : "checkpoint renderer"}`,
        accent: visual.accent ?? "#44d7c9",
        accentAlt: visual.accentAlt ?? "#f4ba55",
      });
    }
  });

  agents.forEach((agent) => {
    const visual = agent.visual ?? {};
    if (!visual.avatar) return;
    const lane = agent.lane;
    records.push({
      id: `agent-${agent.agent_id}`,
      kind: "agent",
      title: `${visual.callsign ?? agent.agent_id} portrait`,
      subtitle: visual.specialty ?? stateLabel(agent.role_id),
      image: visual.avatar,
      laneId: lane?.id ?? null,
      view: "comms",
      badge: lane ? `L${lane.level}` : "agent",
      meta: lane ? `${lane.name} - ${stateLabel(lane.state)}` : `${stateLabel(agent.department_id)} - ${stateLabel(agent.status)}`,
      accent: visual.accent ?? lane?.visual?.accent ?? "#44d7c9",
      accentAlt: lane?.visual?.accentAlt ?? "#f4ba55",
    });
  });

  return [
    ...records,
    {
      id: "system-mission-map",
      kind: "system",
      title: "Mission map background",
      subtitle: "Shared atlas surface",
      image: "./assets/mission-map-bg.png",
      badge: "map",
      meta: "Global route and node backdrop",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-command-cockpit-mission-cartridge",
      kind: "system",
      title: "Command Cockpit Mission Cartridge",
      subtitle: "Compact selected-lane HUD texture",
      image: "./assets/system/command-cockpit-mission-cartridge-20260619.png",
      badge: "cockpit",
      meta: "Generated game-HUD texture used by the Command Cockpit selected-lane status cartridge",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-command-cockpit-insight-ribbon",
      kind: "system",
      title: "Command Cockpit Insight Ribbon",
      subtitle: "Focused Quest node HUD strip",
      image: "./assets/system/command-cockpit-insight-ribbon-20260619.png",
      badge: "ribbon",
      meta: "Generated HUD strip used by focused Quest nodes to show milestone, blocker, bot, proof, and next-move signals",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-command-cockpit-focus-beam",
      kind: "system",
      title: "Command Cockpit Focus Beam",
      subtitle: "Selected Quest node reticle",
      image: "./assets/system/command-cockpit-focus-beam-20260619.png",
      badge: "beam",
      meta: "Generated Quest-board focus beam used to lock the cockpit camera onto selected World, Level, Checkpoint, Gate, and Next nodes",
      accent: "#44d7c9",
      accentAlt: "#689fff",
    },
    {
      id: "system-command-cockpit-crew-relay",
      kind: "system",
      title: "Command Cockpit Crew Relay",
      subtitle: "Selected-lane bot relay chip",
      image: "./assets/system/command-cockpit-crew-relay-20260619.png",
      badge: "crew",
      meta: "Generated bot relay texture used by the Command Cockpit focus lens to show the responsible crew member and Comms jump",
      accent: "#44d7c9",
      accentAlt: "#86f36b",
    },
    {
      id: "system-command-cockpit-node-halos",
      kind: "system",
      title: "Command Cockpit Node Halos",
      subtitle: "Quest node proof and gate medals",
      image: "./assets/system/command-cockpit-node-halos-20260619.png",
      badge: "halo",
      meta: "Generated node-medal texture used by Quest level-map cells to show proof, gates, trail, score, crew, and next-move state",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-command-cockpit-event-pulse",
      kind: "system",
      title: "Command Cockpit Event Pulse",
      subtitle: "Recent trail packet texture",
      image: "./assets/system/command-cockpit-event-pulse-20260619.png",
      badge: "pulse",
      meta: "Procedural route-pulse texture used by the Quest level map to animate recent trail events, blockers, proof, and unlocks inside the existing board footprint",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-relay-portal",
      kind: "system",
      title: "Atlas relay portal",
      subtitle: "Command route backdrop",
      image: "./assets/system/relay-portal-20260617.png",
      badge: "relay",
      meta: "Generated command hub artwork for route maps and system surfaces",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-world-loom-portal",
      kind: "system",
      title: "World Loom portal hall",
      subtitle: "Lane world selector backdrop",
      image: "./assets/system/world-loom-portal-20260618.png",
      badge: "loom",
      meta: "Generated portal hall artwork for cinematic lane selection",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-lane-expansion-portal-deck",
      kind: "system",
      title: "Lane Expansion Portal Deck",
      subtitle: "Future lane socket board texture",
      image: "./assets/system/lane-expansion-portal-deck-20260619.png",
      badge: "slots",
      meta: "Generated compact socket-board texture used by Worlds Launch to show future lane and minigame expansion capacity",
      accent: "#44d7c9",
      accentAlt: "#6aa8ff",
    },
    {
      id: "system-gate-radar-sigil-sheet",
      kind: "system",
      title: "Gate Radar sigil sheet",
      subtitle: "Blocker category glyphs",
      image: "./assets/system/gate-radar-sigil-sheet-20260618.png",
      badge: "radar",
      meta: "Generated glyph sheet for blocker, review, account, browser, payment, and public-action signals",
      accent: "#44d7c9",
      accentAlt: "#ff6f61",
    },
    {
      id: "system-gate-radar-realm-skin-sheet",
      kind: "system",
      title: "Gate Radar realm skin sheet",
      subtitle: "Lane-family radar atmospheres",
      image: "./assets/system/gate-radar-realm-skin-sheet-20260618.png",
      badge: "realm",
      meta: "Generated 3x2 texture atlas for discovery, build, market, risk, revenue, and platform radar skins",
      accent: "#6aa8ff",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-path-handoff-beacon",
      kind: "system",
      title: "Path Handoff beacon",
      subtitle: "Route-to-bot transfer texture",
      image: "./assets/system/path-handoff-beacon-20260618.png",
      badge: "handoff",
      meta: "Generated command-transfer beacon used by the Path Map Route Handoff card",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-route-replay-chronometer",
      kind: "system",
      title: "Route Replay chronometer",
      subtitle: "Playable path-history texture",
      image: "./assets/system/route-replay-chronometer-20260618.png",
      badge: "replay",
      meta: "Generated timeline chronometer artwork used by the Path Map Route Replay panel",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-route-replay-event-glyph-sheet",
      kind: "system",
      title: "Route Replay event glyph sheet",
      subtitle: "Proof, trace, outcome, gate, task, and service icons",
      image: "./assets/system/route-replay-event-glyph-sheet-20260618.png",
      badge: "glyphs",
      meta: "Generated 3x2 sprite sheet used by replay stages, Event Proof, and Path Map mini-events",
      accent: "#44d7c9",
      accentAlt: "#8be06e",
    },
    {
      id: "system-path-memory-codex",
      kind: "system",
      title: "Path Memory Codex",
      subtitle: "Lane trail memory texture",
      image: "./assets/system/path-memory-codex-20260618.png",
      badge: "memory",
      meta: "Generated archive texture used by every lane Trail view for filtered path history",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-path-chapter-archive",
      kind: "system",
      title: "Path Chapter Archive",
      subtitle: "Mission-journal chapter texture",
      image: "./assets/system/path-chapter-archive-20260618.png",
      badge: "archive",
      meta: "Generated archive-console artwork used by the Path Map Chapter Archive",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-path-chapter-spoils",
      kind: "system",
      title: "Path Chapter Spoils",
      subtitle: "Chapter reward medal sheet",
      image: "./assets/system/path-chapter-spoils-20260618.png",
      badge: "spoils",
      meta: "Generated 3x2 achievement medallion sheet used by the Path Map Chapter Spoils shelf",
      accent: "#f4ba55",
      accentAlt: "#44d7c9",
    },
    {
      id: "system-path-chapter-questline",
      kind: "system",
      title: "Path Chapter Questline",
      subtitle: "Chapter run-map HUD texture",
      image: "./assets/system/path-chapter-questline-20260618.png",
      badge: "quest",
      meta: "Generated six-beacon route texture used by the Path Map Chapter Questline",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-path-chapter-depth-rings",
      kind: "system",
      title: "Path Chapter Depth Rings",
      subtitle: "Chapter history orbit texture",
      image: "./assets/system/path-chapter-depth-rings-20260618.png",
      badge: "depth",
      meta: "Generated concentric history-ring texture used by the selected Path Map chapter dossier",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-path-chapter-milestone-ladder",
      kind: "system",
      title: "Path Chapter Milestone Ladder",
      subtitle: "Chapter unlock progression texture",
      image: "./assets/system/path-chapter-milestone-ladder-20260618.png",
      badge: "unlock",
      meta: "Generated unlock ladder texture used by the selected Path Map chapter's Chapter Milestone Ladder",
      accent: "#44d7c9",
      accentAlt: "#8be06e",
    },
    {
      id: "system-path-chapter-game-portal",
      kind: "system",
      title: "Path Chapter Game Portal",
      subtitle: "Chapter-to-minigame launch texture",
      image: "./assets/system/path-chapter-game-portal-20260618.png",
      badge: "game",
      meta: "Generated portal texture used by the selected Path Map chapter's Chapter Game Portal",
      accent: "#44d7c9",
      accentAlt: "#8be06e",
    },
    {
      id: "system-path-chapter-command-relay",
      kind: "system",
      title: "Path Chapter Command Relay",
      subtitle: "Chapter-to-bot relay texture",
      image: "./assets/system/path-chapter-command-relay-20260618.png",
      badge: "relay",
      meta: "Generated command relay texture used by the selected Path Map chapter's Chapter Command Log",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-comms-command-room",
      kind: "system",
      title: "Comms Command Room",
      subtitle: "Lane bot command-room texture",
      image: "./assets/system/comms-command-room-20260618.png",
      badge: "comms",
      meta: "Generated command room texture used by the lane Comms view",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-operator-identity-bay",
      kind: "system",
      title: "Operator Identity Bay",
      subtitle: "Global bot identity roster texture",
      image: "./assets/system/operator-identity-bay-20260618.png",
      badge: "agents",
      meta: "Generated portrait-bay texture used by the global Operator Roster",
      accent: "#44d7c9",
      accentAlt: "#9a89ff",
    },
    {
      id: "system-agent-sprite-foundry",
      kind: "system",
      title: "Agent Sprite Foundry",
      subtitle: "Bot character and sprite pipeline texture",
      image: "./assets/system/agent-sprite-foundry-20260618.png",
      badge: "sprites",
      meta: "Generated character foundry texture used by the global Operator Roster",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-agent-constellation-bay",
      kind: "system",
      title: "Agent Constellation Bay",
      subtitle: "Live bot identity cockpit texture",
      image: "./assets/system/agent-constellation-bay-20260619.png",
      badge: "agents",
      meta: "Procedural bitmap constellation used by the Agent Sprite Foundry live bot beacon layer",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-command-relay-deck",
      kind: "system",
      title: "Command Relay Deck",
      subtitle: "Global bot command relay texture",
      image: "./assets/system/command-relay-deck-20260618.png",
      badge: "relay",
      meta: "Generated relay-deck texture used by the global bot communication surface",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-experiment-discovery-lab",
      kind: "system",
      title: "Experiment Discovery Lab",
      subtitle: "Global test and proof lab texture",
      image: "./assets/system/experiment-discovery-lab-20260618.png",
      badge: "lab",
      meta: "Generated lab texture used by the global experiment and discovery board",
      accent: "#44d7c9",
      accentAlt: "#8be06e",
    },
    {
      id: "system-lane-genesis-foundry",
      kind: "system",
      title: "Lane Genesis Foundry",
      subtitle: "Future lane and minigame setup texture",
      image: "./assets/system/lane-genesis-foundry-20260618.png",
      badge: "genesis",
      meta: "Generated setup-forge texture used by the lane expansion pipeline",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-live-ops-pulse",
      kind: "system",
      title: "Live Ops Pulse",
      subtitle: "Current runs and bot signal texture",
      image: "./assets/system/live-ops-pulse-20260618.png",
      badge: "ops",
      meta: "Generated live-operations texture used by the first-screen current-state pulse board",
      accent: "#8be06e",
      accentAlt: "#44d7c9",
    },
    {
      id: "system-control-runway",
      kind: "system",
      title: "Control Runway",
      subtitle: "First-screen lane level-track texture",
      image: "./assets/system/control-runway-20260618.png",
      badge: "runway",
      meta: "Procedural bitmap runway texture used by the first-screen Control deck level track",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-path-stage-hud-strip",
      kind: "system",
      title: "Path Stage HUD Strip",
      subtitle: "Compact route-stage texture",
      image: "./assets/system/path-stage-hud-strip-20260618.png",
      badge: "stage",
      meta: "Generated compact HUD strip used by the Path Stage Ribbon",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-path-stage-atmosphere",
      kind: "system",
      title: "Path Stage Atmosphere",
      subtitle: "Full cockpit level-world texture",
      image: "./assets/system/path-stage-atmosphere-20260618.png",
      badge: "stage",
      meta: "Procedural bitmap atmosphere used behind the bounded Path cockpit board",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-path-stage-playfield-rail",
      kind: "system",
      title: "Path Stage Playfield Rail",
      subtitle: "Generated level-map playfield texture",
      image: "./assets/system/path-stage-playfield-rail-20260620.png",
      badge: "rail",
      meta: "Generated reusable holographic path texture used by the compact Path Stage route playfield",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-path-run-meter-hud",
      kind: "system",
      title: "Path Run Meter HUD",
      subtitle: "Mission Glance level-strip texture",
      image: "./assets/system/path-run-meter-hud-20260618.png",
      badge: "meter",
      meta: "Generated compact HUD texture used by the Mission Glance Path Run Meter",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-company-quest-board",
      kind: "system",
      title: "Company Quest Board",
      subtitle: "Global task and blocker board texture",
      image: "./assets/system/company-quest-board-20260618.png",
      badge: "quests",
      meta: "Generated mission-board texture used by the company-level task and blocker board",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-company-chronicle-spine",
      kind: "system",
      title: "Company Chronicle Spine",
      subtitle: "Global timeline chapter texture",
      image: "./assets/system/company-chronicle-spine-20260618.png",
      badge: "history",
      meta: "Generated global timeline texture used by the Mission Feed Company Chronicle Spine",
      accent: "#44d7c9",
      accentAlt: "#8be06e",
    },
    {
      id: "system-minigame-registry-codex",
      kind: "system",
      title: "Minigame Registry Codex",
      subtitle: "Lane game-module catalog texture",
      image: "./assets/system/minigame-registry-codex-20260618.png",
      badge: "games",
      meta: "Generated module-catalog texture used by the global Minigame Registry Codex",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-path-chapter-gate-heatfield",
      kind: "system",
      title: "Path Chapter Gate Heatfield",
      subtitle: "Blocker radar scan texture",
      image: "./assets/system/path-chapter-gate-heatfield-20260618.png",
      badge: "gates",
      meta: "Generated tactical heatfield texture used by the selected Path Map chapter's Chapter Gate Stack",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-chapter-crew-formation",
      kind: "system",
      title: "Chapter Crew Formation",
      subtitle: "Bot roster command texture",
      image: "./assets/system/chapter-crew-formation-20260618.png",
      badge: "crew",
      meta: "Generated tactical formation backdrop used by the Path Map Chapter Crew Relay",
      accent: "#44d7c9",
      accentAlt: "#f4ba55",
    },
    {
      id: "system-lane-sheet",
      kind: "system",
      title: "Operator avatar source sheet",
      subtitle: "Lane avatar generation sheet",
      image: "./assets/lanes/operator-avatar-sheet-20260616.png",
      badge: "sheet",
      meta: `${formatNumber(lanes.length)} lane crops in use`,
      accent: "#8be06e",
      accentAlt: "#44d7c9",
    },
    {
      id: "system-agent-sheet",
      kind: "system",
      title: "Agent portrait source sheet",
      subtitle: "Bot character generation sheet",
      image: "./assets/agents/agent-avatar-sheet-20260616.png",
      badge: "sheet",
      meta: `${formatNumber(agents.length)} active portraits mapped`,
      accent: "#9a89ff",
      accentAlt: "#ff6f61",
    },
    {
      id: "system-trophy-sheet",
      kind: "system",
      title: "Trophy medal source sheet",
      subtitle: "Outcome rarity medals",
      image: "./assets/trophies/trophy-medal-sheet-20260617.png",
      badge: "trophy",
      meta: "Mythic, gold, silver, and bronze rewards",
      accent: "#f4ba55",
      accentAlt: "#ff6f61",
    },
    {
      id: "system-spare-agent",
      kind: "system",
      title: "Reserved expansion portrait",
      subtitle: "Next-agent placeholder",
      image: "./assets/agents/spare-agent-operator-20260616.png",
      badge: "spare",
      meta: "Ready for the next registered bot",
      accent: "#c4d4cf",
      accentAlt: "#44d7c9",
    },
  ];
}

function assetStyle(asset) {
  return `--asset-a:${escapeHtml(asset.accent ?? "#44d7c9")}; --asset-b:${escapeHtml(asset.accentAlt ?? "#f4ba55")};`;
}

function assetProductionBoardModel(assets) {
  const laneAvatarCount = assets.filter((asset) => asset.kind === "lane").length;
  const botPortraitCount = assets.filter((asset) => asset.kind === "agent").length;
  const gameTextureCount = assets.filter((asset) => asset.kind === "game").length;
  const systemArtCount = assets.filter((asset) => asset.kind === "system").length;
  const laneCount = state.snapshot?.lanes?.length ?? 0;
  const agentCount = state.snapshot?.agents?.length ?? 0;
  const futureSlots = Math.max(4, (state.snapshot?.lanes?.length ?? 0) + 4 - assets.filter((asset) => asset.kind === "game").length);
  const totalNeeded = Math.max(1, laneCount + agentCount + laneCount + futureSlots);
  const coverage = Math.round(((laneAvatarCount + botPortraitCount + gameTextureCount) / totalNeeded) * 100);
  return {
    coverage,
    total: assets.length,
    cells: [
      {
        id: "lane-avatars",
        label: "Lane Avatars",
        value: laneAvatarCount,
        tone: laneAvatarCount >= laneCount ? "complete" : "open",
        body: `${formatNumber(laneAvatarCount)} / ${formatNumber(laneCount)} paths skinned`,
      },
      {
        id: "bot-portraits",
        label: "Bot Portraits",
        value: botPortraitCount,
        tone: botPortraitCount >= agentCount ? "complete" : "open",
        body: `${formatNumber(botPortraitCount)} / ${formatNumber(agentCount)} operators visible`,
      },
      {
        id: "game-textures",
        label: "Game Textures",
        value: gameTextureCount,
        tone: gameTextureCount >= laneCount ? "complete" : "building",
        body: `${formatNumber(gameTextureCount)} minigame worlds generated`,
      },
      {
        id: "system-art",
        label: "System Art",
        value: systemArtCount,
        tone: systemArtCount ? "complete" : "open",
        body: "Reusable HUDs, boards, and source sheets",
      },
      {
        id: "future-slots",
        label: "Future Slots",
        value: futureSlots,
        tone: "future",
        body: "Reserved sockets for new lanes, bots, and minigames",
      },
    ],
  };
}

function renderAssetProductionBoard(assets) {
  if (!el.assetProductionBoard) return;
  const model = assetProductionBoardModel(assets);
  el.assetProductionBoard.innerHTML = `
    <article class="asset-production-core" style="--asset-production:${model.coverage}%">
      <span>Asset Production</span>
      <strong>${formatNumber(model.coverage)}%</strong>
      <p>${formatNumber(model.total)} files registered across avatars, games, system textures, and future sockets.</p>
      <i aria-hidden="true"></i>
    </article>
    ${model.cells
      .map(
        (cell, index) => `
          <article class="asset-production-cell ${escapeHtml(cell.tone)}" data-asset-production-cell="${escapeHtml(cell.id)}" style="--asset-production-index:${index};">
            <span>${escapeHtml(cell.label)}</span>
            <strong>${formatNumber(cell.value)}</strong>
            <p>${escapeHtml(compactText(cell.body, 68))}</p>
          </article>`,
      )
      .join("")}`;
}
function renderAssetVault() {
  if (!el.assetVault) return;
  const assets = visualAssetRecords();
  const filtered = state.assetFilter === "all" ? assets : assets.filter((asset) => asset.kind === state.assetFilter);
  renderAssetProductionBoard(assets);
  const counts = assetKinds().reduce((acc, kind) => {
    acc[kind] = kind === "all" ? assets.length : assets.filter((asset) => asset.kind === kind).length;
    return acc;
  }, {});

  el.assetVaultCount.textContent =
    state.assetFilter === "all"
      ? `${formatNumber(assets.length)} assets`
      : `${formatNumber(filtered.length)} / ${formatNumber(assets.length)} ${stateLabel(state.assetFilter)}`;
  el.assetVaultFilters.innerHTML = assetKinds()
    .map(
      (kind) => `
        <button class="asset-filter-chip ${state.assetFilter === kind ? "active" : ""}" type="button" data-asset-filter="${kind}">
          <span>${escapeHtml(stateLabel(kind))}</span>
          <strong>${formatNumber(counts[kind])}</strong>
        </button>`
    )
    .join("");
  el.assetVault.innerHTML = filtered.length
    ? filtered.map(renderAssetCard).join("")
    : `<div class="empty-state">No assets in this collection yet.</div>`;
}

function renderAssetCard(asset) {
  const isActive = asset.laneId && asset.laneId === state.selectedLaneId;
  const content = `
      <span class="asset-preview" aria-hidden="true">
        <img src="${escapeHtml(asset.image)}" alt="" loading="eager" />
        <span>${escapeHtml(stateLabel(asset.kind))}</span>
      </span>
      <span class="asset-card-copy">
        <span class="asset-card-topline">
          <em>${escapeHtml(asset.badge ?? asset.kind)}</em>
          <strong>${escapeHtml(asset.subtitle ?? stateLabel(asset.kind))}</strong>
        </span>
        <span class="asset-card-title">${escapeHtml(compactText(asset.title, 78))}</span>
        <span class="asset-card-meta">${escapeHtml(compactText(asset.meta, 118))}</span>
      </span>`;

  if (!asset.laneId) {
    return `<article class="asset-card system" style="${assetStyle(asset)}">${content}</article>`;
  }

  return `
    <button class="asset-card interactive ${isActive ? "active" : ""}" type="button" data-asset-lane-id="${escapeHtml(asset.laneId)}" data-asset-view="${escapeHtml(asset.view ?? "overview")}" style="${assetStyle(asset)}">
      ${content}
    </button>`;
}

function agentRosterAvatar(agent) {
  const avatar = agent.visual?.avatar;
  if (!avatar) return `<div class="operator-avatar avatar-fallback" aria-hidden="true"></div>`;
  return `<img class="operator-avatar" src="${escapeHtml(avatar)}" alt="" />`;
}

function renderLeaderboard() {
  el.leaderboard.innerHTML = state.snapshot.leaderboard
    .map(
      (lane, index) => `
      <article class="leader-row">
        <div class="rank">${index + 1}</div>
        <div>
          <h3>${escapeHtml(lane.name)}</h3>
          <p>${escapeHtml(lane.department)} - Level ${lane.level} - ${escapeHtml(stateLabel(lane.state))}</p>
        </div>
        <div class="score">${formatNumber(lane.score)}</div>
      </article>`
    )
    .join("");
}

function renderResearch() {
  el.researchList.innerHTML = state.snapshot.researchInfluences
    .map(
      (item) => `
      <article class="research-item">
        <h3><a href="${escapeHtml(item.url)}">${escapeHtml(item.name)}</a></h3>
        <p>${escapeHtml(item.takeaway)}</p>
      </article>`
    )
    .join("");
}

function selectLane(laneId, detailView = state.detailView) {
  if (state.pathReplayPlayingLaneId && state.pathReplayPlayingLaneId !== laneId) stopPathReplay(false);
  state.selectedLaneId = laneId;
  state.detailView = detailView;
  state.trailLimitByLane[laneId] = state.trailLimitByLane[laneId] ?? 18;
  state.gameStepByLane[laneId] = state.gameStepByLane[laneId] ?? 0;
  renderSystemRelay();
  renderWorldsLaunch();
  renderWorldLoom();
  renderArcadeDeck();
  renderMinigameRegistryCodex();
  renderMotionForge();
  renderCrewBridge();
  renderProgressionConstellation();
  renderRealmPacks();
  renderExpansionForge();
  renderLaneGenesisFoundry();
  renderLaneList();
  renderMap();
  renderDetail();
  renderSignalCore();
  renderControlRunway();
  renderLiveOpsPulse();
  renderCompanyQuestBoard();
  renderAgentRoster();
  renderAssetVault();
  renderThreadNexus();
  renderBotCommandMatrix();
  syncRoute();
}

function openPathStageDepth(lane, options = {}) {
  const pathStageDepth = options.pathStageDepth ?? "stage";
  const validViews = new Set(["stage", "archive", "utility"]);
  if (!lane || !validViews.has(pathStageDepth)) return;
  state.pathStageDepthByLane = { ...state.pathStageDepthByLane, [lane.id]: pathStageDepth };
  if (options.utilityView) {
    state.pathUtilityDockViewByLane = { ...state.pathUtilityDockViewByLane, [lane.id]: options.utilityView };
  }
  renderDetail();
  const selector = pathStageDepth === "archive" ? ".path-chapter-archive" : pathStageDepth === "utility" ? ".path-utility-dock" : ".path-map-board";
  window.setTimeout(() => document.querySelector(selector)?.scrollIntoView({ behavior: "smooth", block: pathStageDepth === "stage" ? "nearest" : "start" }), 0);
}

function resetView(animate = true) {
  const viewport = el.mapViewport.getBoundingClientRect();
  const worldWidth = el.mapWorld.offsetWidth || 1600;
  const worldHeight = el.mapWorld.offsetHeight || 1000;
  const isSoloMapStage = document.body.dataset.atlasDeck === "command" && document.body.dataset.atlasStage === "map";
  const minScale = isSoloMapStage ? 0.52 : 0.42;
  const scaleBoost = isSoloMapStage ? 1.32 : 1.08;
  const maxScale = isSoloMapStage ? 0.96 : 0.82;
  const scale = Math.min(maxScale, Math.max(minScale, Math.min(viewport.width / worldWidth, viewport.height / worldHeight) * scaleBoost));
  state.transform.scale = scale;
  state.transform.x = (viewport.width - worldWidth * scale) / 2;
  state.transform.y = (viewport.height - worldHeight * scale) / 2;
  applyTransform(animate);
}

function applyTransform(animate = true) {
  el.mapWorld.style.transition = animate ? "transform 120ms ease-out" : "none";
  el.mapWorld.style.transform = `translate(${state.transform.x}px, ${state.transform.y}px) scale(${state.transform.scale})`;
}

function zoom(delta) {
  const oldScale = state.transform.scale;
  const nextScale = Math.min(1.6, Math.max(0.36, oldScale + delta));
  const viewport = el.mapViewport.getBoundingClientRect();
  const centerX = viewport.width / 2;
  const centerY = viewport.height / 2;
  const worldX = (centerX - state.transform.x) / oldScale;
  const worldY = (centerY - state.transform.y) / oldScale;
  state.transform.scale = nextScale;
  state.transform.x = centerX - worldX * nextScale;
  state.transform.y = centerY - worldY * nextScale;
  applyTransform();
}

function setupEvents() {
  document.addEventListener("click", async (event) => {
    const atlasDeckButton = event.target.closest("#atlas-deck-dock [data-atlas-deck]");
    if (atlasDeckButton) {
      setAtlasDeck(atlasDeckButton.dataset.atlasDeck ?? "control");
      syncRoute();
      return;
    }

    const atlasCommandRibbonButton = event.target.closest("[data-atlas-command-ribbon-action]");
    if (atlasCommandRibbonButton) {
      activateAtlasCommandRibbon(atlasCommandRibbonButton.dataset.atlasCommandRibbonAction);
      return;
    }
    const cockpitControlButton = event.target.closest("[data-cockpit-control-action]");
    if (cockpitControlButton) {
      activateCockpitControlPad(cockpitControlButton.dataset.cockpitControlAction, cockpitControlButton.dataset.cockpitControlLane);
      return;
    }

    const atlasTeleportButton = event.target.closest("#atlas-teleport-rail [data-atlas-teleport]");
    if (atlasTeleportButton) {
      activateAtlasTeleport(atlasTeleportButton.dataset.atlasTeleport);
      return;
    }

    const commandArchiveButton = event.target.closest("[data-command-archive-button]");
    if (commandArchiveButton) {
      setCommandArchivePanel(commandArchiveButton.dataset.commandArchiveButton ?? "relay");
      return;
    }

    const controlRunwayLane = event.target.closest("[data-control-runway-lane]");
    if (controlRunwayLane) {
      setAtlasDeck("command", { scroll: false });
      selectLane(controlRunwayLane.dataset.controlRunwayLane, controlRunwayLane.dataset.controlRunwayView || "overview");
      settleDetailPanelIntoView();
      return;
    }

    const stageButton = event.target.closest("[data-stage-dispatch]");
    if (stageButton) {
      const suggestion = state.snapshot.dispatchConsole?.suggestions?.find((item) => item.id === stageButton.dataset.stageDispatch);
      if (suggestion) stageDispatch(suggestion);
      return;
    }

    const batchButton = event.target.closest("[data-dispatch-batch]");
    if (batchButton) {
      const action = batchButton.dataset.dispatchBatch;
      const suggestions = dispatchSuggestions();
      if (action === "top3" || action === "visible") {
        const picked = action === "top3" ? suggestions.slice(0, 3) : suggestions;
        picked.forEach((item) => stageDispatch(item, { silent: true, deferRender: true }));
        if (picked.length) recordDispatchHistory(action === "top3" ? "batch_top3" : "batch_visible", { title: "Staged suggested commands", count: picked.length });
        writeDispatchOutbox();
        renderDispatchConsole();
      }
      if (action === "copy") {
        if (state.stagedDispatches.length) {
          const copied = await copyText(batchCommandText());
          state.copiedBatch = copied;
          state.manualCopyBuffer = copied ? null : batchCommandText();
          recordDispatchHistory(copied ? "batch_copied" : "batch_copy_failed", { title: "Copied staged command batch", count: state.stagedDispatches.length });
          renderDispatchConsole();
        }
      }
      if (action === "clear") {
        const count = state.stagedDispatches.length;
        if (count) {
          state.stagedDispatches = [];
          state.manualCopyBuffer = null;
          writeDispatchOutbox();
          recordDispatchHistory("batch_archived", { title: "Archived staged command batch", count });
          renderDispatchConsole();
        }
      }
      if (action === "clearHistory") {
        state.dispatchHistory = [];
        writeDispatchHistory();
        renderDispatchConsole();
      }
      return;
    }

    const stageLaneButton = event.target.closest("[data-stage-lane-command]");
    if (stageLaneButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === stageLaneButton.dataset.stageLaneCommand);
      if (lane) {
        stageDispatch(bestLaneDispatchSuggestion(lane));
        renderDetail();
      }
      return;
    }

    const pathCommandJumpButton = event.target.closest("[data-path-command-jump]");
    if (pathCommandJumpButton) {
      if (pathCommandJumpButton.dataset.pathCommandJump === "route") {
        const lane = selectedLane();
        if (lane) {
          state.pathCoreDeckViewByLane = { ...state.pathCoreDeckViewByLane, [lane.id]: "route" };
          state.pathStageDepthByLane = { ...state.pathStageDepthByLane, [lane.id]: "stage" };
          renderDetail();
          window.setTimeout(() => document.querySelector(".path-core-deck")?.scrollIntoView({ behavior: "smooth", block: "start" }), 0);
        }
        return;
      }
      const utilityViews = {
        proof: "proof",
        replay: "replay",
        intel: "intel",
      };
      const utilityView = utilityViews[pathCommandJumpButton.dataset.pathCommandJump];
      if (utilityView) {
        const lane = selectedLane();
        if (lane) {
          openPathStageDepth(lane, { pathStageDepth: "utility", utilityView });
        }
        return;
      }
      const targets = {
        route: ".path-route",
        proof: ".path-proof-cache",
        archive: ".path-chapter-archive",
        replay: ".path-route-replay",
        intel: ".path-node-intel",
      };
      const selector = targets[pathCommandJumpButton.dataset.pathCommandJump];
      if (selector) {
        document.querySelector(selector)?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const pathGlanceJumpButton = event.target.closest("[data-path-glance-jump]");
    if (pathGlanceJumpButton) {
      if (pathGlanceJumpButton.dataset.pathGlanceJump === "route") {
        const lane = selectedLane();
        if (lane) {
          state.pathCoreDeckViewByLane = { ...state.pathCoreDeckViewByLane, [lane.id]: "route" };
          state.pathStageDepthByLane = { ...state.pathStageDepthByLane, [lane.id]: "stage" };
          renderDetail();
          window.setTimeout(() => document.querySelector(".path-core-deck")?.scrollIntoView({ behavior: "smooth", block: "start" }), 0);
        }
        return;
      }
      if (pathGlanceJumpButton.dataset.pathGlanceJump === "archive") {
        const lane = selectedLane();
        if (lane) openPathStageDepth(lane, { pathStageDepth: "archive" });
        return;
      }
      if (pathGlanceJumpButton.dataset.pathGlanceJump === "proof") {
        const lane = selectedLane();
        if (lane) openPathStageDepth(lane, { pathStageDepth: "utility", utilityView: "proof" });
        return;
      }
      const targets = {
        route: ".path-route",
        archive: ".path-chapter-archive",
      };
      const selector = targets[pathGlanceJumpButton.dataset.pathGlanceJump];
      if (selector) {
        document.querySelector(selector)?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const pathStageDepthButton = event.target.closest("[data-path-stage-depth]");
    if (pathStageDepthButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathStageDepthButton.dataset.pathStageDepthLane) ?? selectedLane();
      if (lane) {
        openPathStageDepth(lane, { pathStageDepth: pathStageDepthButton.dataset.pathStageDepth });
      }
      return;
    }

    const pathCoreViewButton = event.target.closest("[data-path-core-view]");
    if (pathCoreViewButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathCoreViewButton.dataset.pathCoreLane) ?? selectedLane();
      if (lane) {
        state.pathCoreDeckViewByLane = {
          ...state.pathCoreDeckViewByLane,
          [lane.id]: pathCoreViewButton.dataset.pathCoreView,
        };
        renderDetail();
        document.querySelector(".path-core-deck")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
      return;
    }

    const pathUtilityViewButton = event.target.closest("[data-path-utility-view]");
    if (pathUtilityViewButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathUtilityViewButton.dataset.pathUtilityLane) ?? selectedLane();
      if (lane) {
        state.pathStageDepthByLane = { ...state.pathStageDepthByLane, [lane.id]: "utility" };
        state.pathUtilityDockViewByLane = {
          ...state.pathUtilityDockViewByLane,
          [lane.id]: pathUtilityViewButton.dataset.pathUtilityView,
        };
        renderDetail();
        document.querySelector(".path-utility-dock")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
      return;
    }

    const pathHandoffStageButton = event.target.closest("[data-path-handoff-stage]");
    if (pathHandoffStageButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathHandoffStageButton.dataset.pathHandoffStage);
      if (lane) {
        stageDispatch(bestLaneDispatchSuggestion(lane));
        renderDetail();
      }
      return;
    }

    const pathChapterExpandButton = event.target.closest("[data-path-chapter-expand]");
    if (pathChapterExpandButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathChapterExpandButton.dataset.pathChapterLane) ?? selectedLane();
      if (lane) {
        state.pathChapterArchiveExpandedByLane = {
          ...state.pathChapterArchiveExpandedByLane,
          [lane.id]: pathChapterExpandButton.dataset.pathChapterExpand === "expand",
        };
        renderDetail();
        document.querySelector(".path-chapter-archive")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const pathStageChapterButton = event.target.closest("[data-path-stage-chapter-focus]");
    if (pathStageChapterButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathStageChapterButton.dataset.pathStageChapterLane) ?? selectedLane();
      if (lane) {
        const trail = chronicleTrail(lane);
        const chapter = pathChapterArchiveItems(trail).find((item) => item.key === pathStageChapterButton.dataset.pathStageChapterFocus);
        focusPathChapter(lane, chapter);
        state.pathStageDepthByLane = { ...state.pathStageDepthByLane, [lane.id]: "archive" };
        renderDetail();
        document.querySelector(".path-chapter-archive")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
      return;
    }

    const pathChapterButton = event.target.closest("[data-path-chapter-focus]");
    if (pathChapterButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathChapterButton.dataset.pathChapterLane) ?? selectedLane();
      if (lane) {
        const trail = chronicleTrail(lane);
        const chapter = pathChapterArchiveItems(trail).find((item) => item.key === pathChapterButton.dataset.pathChapterFocus);
        focusPathChapter(lane, chapter);
        renderDetail();
      }
      return;
    }

    const pathChapterLensButton = event.target.closest("[data-path-chapter-lens]");
    if (pathChapterLensButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathChapterLensButton.dataset.pathChapterLane) ?? selectedLane();
      if (lane) {
        const trail = chronicleTrail(lane);
        const chapter = pathChapterArchiveItems(trail).find((item) => item.key === pathChapterLensButton.dataset.pathChapterKey);
        if (chapter) {
          const lens = pathChapterLensButton.dataset.pathChapterLens ?? "all";
          const lensStateKey = pathChapterRecordLensStateKey(lane, chapter);
          const limitStateKey = pathChapterRecordStateKey(lane, chapter, lens);
          state.pathChapterFocusByLane = { ...state.pathChapterFocusByLane, [lane.id]: chapter.key };
          state.pathChapterRecordLensByLane = { ...state.pathChapterRecordLensByLane, [lensStateKey]: lens };
          state.pathChapterRecordLimitByLane = { ...state.pathChapterRecordLimitByLane, [limitStateKey]: 4 };
          const records = lens === "all" ? chapter.items : chapter.items.filter((item) => pathEventGlyphType(item) === lens);
          const focusedKey = state.pathEventFocusByLane[lane.id];
          if (records.length && !records.some((item) => pathEventKey(item) === focusedKey)) {
            const focusKey = pathEventKey(records[0]);
            state.pathEventFocusByLane = { ...state.pathEventFocusByLane, [lane.id]: focusKey };
            const replayIndex = pathReplayItems(lane).findIndex((item) => pathEventKey(item) === focusKey);
            if (replayIndex >= 0) {
              state.pathReplayIndexByLane = { ...state.pathReplayIndexByLane, [lane.id]: replayIndex };
            }
          }
        }
        renderDetail();
      }
      return;
    }

    const pathChapterRevealButton = event.target.closest("[data-path-chapter-reveal]");
    if (pathChapterRevealButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathChapterRevealButton.dataset.pathChapterLane) ?? selectedLane();
      if (lane) {
        const trail = chronicleTrail(lane);
        const chapter = pathChapterArchiveItems(trail).find((item) => item.key === pathChapterRevealButton.dataset.pathChapterReveal);
        if (chapter) {
          const stateKey = pathChapterRecordStateKey(lane, chapter);
          const current = pathChapterRecordLimit(lane, chapter);
          state.pathChapterFocusByLane = { ...state.pathChapterFocusByLane, [lane.id]: chapter.key };
          state.pathChapterRecordLimitByLane = { ...state.pathChapterRecordLimitByLane, [stateKey]: current + 4 };
          state.trailLimitByLane = { ...state.trailLimitByLane, [lane.id]: Math.max(state.trailLimitByLane[lane.id] ?? 18, chapter.endIndex + 1) };
        }
        renderDetail();
      }
      return;
    }

    const pathChapterRunwayRevealButton = event.target.closest("[data-path-chapter-runway-reveal]");
    if (pathChapterRunwayRevealButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathChapterRunwayRevealButton.dataset.pathChapterRunwayLane) ?? selectedLane();
      if (lane) {
        const trail = chronicleTrail(lane);
        const chapter = pathChapterArchiveItems(trail).find((item) => item.key === pathChapterRunwayRevealButton.dataset.pathChapterRunwayReveal);
        if (chapter) {
          const stateKey = pathChapterRunwayStateKey(lane, chapter);
          const current = pathChapterRunwayLimit(lane, chapter);
          state.pathChapterFocusByLane = { ...state.pathChapterFocusByLane, [lane.id]: chapter.key };
          state.pathChapterRunwayLimitByLane = { ...state.pathChapterRunwayLimitByLane, [stateKey]: current + 12 };
          state.trailLimitByLane = { ...state.trailLimitByLane, [lane.id]: Math.max(state.trailLimitByLane[lane.id] ?? 18, chapter.endIndex + 1) };
        }
        renderDetail();
      }
      return;
    }

    const pathNodeFocusButton = event.target.closest("[data-path-node-focus]");
    if (pathNodeFocusButton) {
      const lane = selectedLane();
      if (lane) {
        state.pathNodeFocusByLane = { ...state.pathNodeFocusByLane, [lane.id]: pathNodeFocusButton.dataset.pathNodeFocus };
        renderDetail();
      }
      return;
    }

    const pathMemoryActionButton = event.target.closest("[data-path-memory-action]");
    if (pathMemoryActionButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathMemoryActionButton.dataset.pathMemoryLane) ?? selectedLane();
      if (lane) {
        state.pathMemoryLensByLane = { ...state.pathMemoryLensByLane, [lane.id]: pathMemoryActionButton.dataset.pathMemoryAction ?? "all" };
        renderDetail();
        document.querySelector("#path-memory-codex")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const pathMemoryJumpButton = event.target.closest("[data-path-memory-jump]");
    if (pathMemoryJumpButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathMemoryJumpButton.dataset.pathMemoryLane) ?? selectedLane();
      const action = pathMemoryJumpButton.dataset.pathMemoryJump;
      if (lane && action === "more") {
        state.trailLimitByLane = { ...state.trailLimitByLane, [lane.id]: (state.trailLimitByLane[lane.id] ?? 18) + 18 };
        renderDetail();
        document.querySelector(".deep-trail")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (lane && action === "path") {
        const latest = chronicleTrail(lane)[0];
        if (latest) state.pathEventFocusByLane = { ...state.pathEventFocusByLane, [lane.id]: pathEventKey(latest) };
        selectLane(lane.id, "path");
        settleDetailPanelIntoView();
      }
      if (lane && action === "comms") {
        selectLane(lane.id, "comms");
        settleDetailPanelIntoView();
      }
      return;
    }

    const pathMemoryEventButton = event.target.closest("[data-path-memory-event]");
    if (pathMemoryEventButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathMemoryEventButton.dataset.pathMemoryLane) ?? selectedLane();
      const focusKey = pathMemoryEventButton.dataset.pathMemoryEvent;
      if (lane && focusKey) {
        const trail = chronicleTrail(lane);
        const chapter = pathChapterArchiveItems(trail).find((item) => item.items.some((record) => pathEventKey(record) === focusKey));
        state.pathEventFocusByLane = { ...state.pathEventFocusByLane, [lane.id]: focusKey };
        if (chapter) state.pathChapterFocusByLane = { ...state.pathChapterFocusByLane, [lane.id]: chapter.key };
        const replayIndex = pathReplayItems(lane).findIndex((item) => pathEventKey(item) === focusKey);
        if (replayIndex >= 0) {
          state.pathReplayIndexByLane = { ...state.pathReplayIndexByLane, [lane.id]: replayIndex };
        }
        selectLane(lane.id, "path");
        settleDetailPanelIntoView();
      }
      return;
    }

    const pathEventFocusButton = event.target.closest("[data-path-event-focus]");
    if (pathEventFocusButton) {
      const lane = selectedLane();
      if (lane && pathEventFocusButton.dataset.pathEventFocus) {
        state.pathEventFocusByLane = { ...state.pathEventFocusByLane, [lane.id]: pathEventFocusButton.dataset.pathEventFocus };
        const replayIndex = pathReplayItems(lane).findIndex((item) => pathEventKey(item) === pathEventFocusButton.dataset.pathEventFocus);
        if (replayIndex >= 0) {
          state.pathReplayIndexByLane = { ...state.pathReplayIndexByLane, [lane.id]: replayIndex };
        }
        renderDetail();
      }
      return;
    }

    const pathChapterRunwayFocusButton = event.target.closest("[data-path-chapter-runway-focus]");
    if (pathChapterRunwayFocusButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathChapterRunwayFocusButton.dataset.pathChapterRunwayLane) ?? selectedLane();
      const focusKey = pathChapterRunwayFocusButton.dataset.pathChapterRunwayFocus;
      if (lane && focusKey) {
        state.pathChapterFocusByLane = { ...state.pathChapterFocusByLane, [lane.id]: pathChapterRunwayFocusButton.dataset.pathChapterKey ?? state.pathChapterFocusByLane[lane.id] };
        state.pathEventFocusByLane = { ...state.pathEventFocusByLane, [lane.id]: focusKey };
        const replayIndex = pathReplayItems(lane).findIndex((item) => pathEventKey(item) === focusKey);
        if (replayIndex >= 0) {
          state.pathReplayIndexByLane = { ...state.pathReplayIndexByLane, [lane.id]: replayIndex };
        }
        renderDetail();
      }
      return;
    }

    const pathReplayFilterButton = event.target.closest("[data-path-replay-filter]");
    if (pathReplayFilterButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathReplayFilterButton.dataset.pathReplayLane) ?? selectedLane();
      if (lane) {
        const nextFilter = pathReplayFilterButton.dataset.pathReplayFilter ?? "all";
        state.pathReplayFilterByLane = { ...state.pathReplayFilterByLane, [lane.id]: nextFilter };
        setPathReplayIndex(lane, 0);
        renderDetail();
      }
      return;
    }

    const pathReplayJumpButton = event.target.closest("[data-path-replay-jump]");
    if (pathReplayJumpButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathReplayJumpButton.dataset.pathReplayLane) ?? selectedLane();
      if (lane) {
        const nextIndex = Number(pathReplayJumpButton.dataset.pathReplayJump);
        if (Number.isFinite(nextIndex)) setPathReplayIndex(lane, nextIndex);
        renderDetail();
      }
      return;
    }

    const pathReplayButton = event.target.closest("[data-path-replay-action]");
    if (pathReplayButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === pathReplayButton.dataset.pathReplayLane) ?? selectedLane();
      if (lane) {
        const items = pathReplayItems(lane);
        const current = pathReplayIndex(lane, items.length);
        const action = pathReplayButton.dataset.pathReplayAction;
        if (action === "toggle") {
          if (state.pathReplayPlayingLaneId === lane.id) {
            stopPathReplay();
          } else {
            startPathReplay(lane.id);
          }
          return;
        }
        if (action === "start") setPathReplayIndex(lane, 0);
        if (action === "back") setPathReplayIndex(lane, current <= 0 ? Math.max(items.length - 1, 0) : current - 1);
        if (action === "next") setPathReplayIndex(lane, current >= items.length - 1 ? 0 : current + 1);
        if (action === "latest") setPathReplayIndex(lane, Math.max(items.length - 1, 0));
        renderDetail();
      }
      return;
    }

    const proofExpandButton = event.target.closest("[data-expand-proof-cache]");
    if (proofExpandButton) {
      const laneId = proofExpandButton.dataset.expandProofCache;
      const current = state.proofLimitByLane[laneId] ?? 3;
      state.proofLimitByLane = { ...state.proofLimitByLane, [laneId]: current + 3 };
      renderDetail();
      return;
    }

    const botStageButton = event.target.closest("[data-bot-stage-lane]");
    if (botStageButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === botStageButton.dataset.botStageLane);
      const suggestion =
        state.snapshot.dispatchConsole?.suggestions?.find((item) => item.laneId === botStageButton.dataset.botStageLane) ??
        (lane ? laneDispatchSuggestion(lane) : null);
      if (suggestion) stageDispatch(suggestion);
      return;
    }

    const copyDispatchButton = event.target.closest("[data-copy-dispatch]");
    if (copyDispatchButton) {
      const item = state.stagedDispatches.find((draft) => draft.id === copyDispatchButton.dataset.copyDispatch);
      if (item) {
        const copied = await copyText(item.command);
        state.copiedDispatchFor = copied ? item.id : null;
        recordDispatchHistory(copied ? "copied" : "copy_failed", item);
        renderDispatchConsole();
      }
      return;
    }

    const removeDispatchButton = event.target.closest("[data-remove-dispatch]");
    if (removeDispatchButton) {
      const removed = state.stagedDispatches.find((draft) => draft.id === removeDispatchButton.dataset.removeDispatch);
      state.stagedDispatches = state.stagedDispatches.filter((draft) => draft.id !== removeDispatchButton.dataset.removeDispatch);
      writeDispatchOutbox();
      if (removed) recordDispatchHistory("archived", removed);
      renderDispatchConsole();
      return;
    }

    const dispatchLaneButton = event.target.closest("[data-dispatch-lane-id]");
    if (dispatchLaneButton) {
      selectLane(dispatchLaneButton.dataset.dispatchLaneId, "comms");
      return;
    }

    const commandRelayStage = event.target.closest("[data-command-relay-stage]");
    if (commandRelayStage) {
      const lane = state.snapshot.lanes.find((item) => item.id === commandRelayStage.dataset.commandRelayStage);
      const suggestion =
        state.snapshot.dispatchConsole?.suggestions?.find((item) => item.laneId === commandRelayStage.dataset.commandRelayStage) ??
        (lane ? laneDispatchSuggestion(lane) : null);
      if (suggestion) stageDispatch(suggestion);
      return;
    }

    const commandRelayAction = event.target.closest("[data-command-relay-action]");
    if (commandRelayAction) {
      const records = commandRelayDeckRecords();
      const lead = commandRelayLeadRecord(records);
      const action = commandRelayAction.dataset.commandRelayAction;
      if (action === "queue" && lead?.suggestion) {
        stageDispatch(lead.suggestion);
      }
      if (action === "comms" && lead?.lane) {
        setAtlasDeck("command", { scroll: false });
        selectLane(lead.lane.id, "comms");
        settleDetailPanelIntoView();
      }
      if (action === "matrix") {
        setAtlasDeck("command", { scroll: false });
        setCommandArchivePanel("bots", { scroll: true });
      }
      return;
    }

    const commandRelayLane = event.target.closest("[data-command-relay-lane]");
    if (commandRelayLane) {
      setAtlasDeck("command", { scroll: false });
      selectLane(commandRelayLane.dataset.commandRelayLane, "comms");
      settleDetailPanelIntoView();
      return;
    }

    const liveOpsAction = event.target.closest("[data-live-ops-action]");
    if (liveOpsAction) {
      const action = liveOpsAction.dataset.liveOpsAction;
      if (action === "latest") {
        setAtlasDeck("history", { scroll: false });
        setFeedFilter("all");
        document.querySelector(".mission-feed-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "gates") {
        setAtlasDeck("history", { scroll: false });
        setFeedFilter("service_request");
        document.querySelector(".mission-feed-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "comms") {
        setAtlasDeck("command", { scroll: false });
        setCommandArchivePanel("command", { scroll: true });
      }
      if (action === "timeline") {
        setAtlasDeck("history", { scroll: false });
        document.querySelector(".feed-playback-console")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const liveOpsLane = event.target.closest("[data-live-ops-lane]");
    if (liveOpsLane) {
      setAtlasDeck("command", { scroll: false });
      selectLane(liveOpsLane.dataset.liveOpsLane, "trail");
      settleDetailPanelIntoView();
      return;
    }

    const companyQuestAction = event.target.closest("[data-company-quest-action]");
    if (companyQuestAction) {
      const action = companyQuestAction.dataset.companyQuestAction;
      if (action === "tasks") setFeedFilter("task");
      if (action === "gates") setFeedFilter("service_request");
      if (action === "wins") setFeedFilter("outcome");
      setAtlasDeck("history", { scroll: false });
      document.querySelector(".mission-feed-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }

    const companyQuestLane = event.target.closest("[data-company-quest-lane]");
    if (companyQuestLane) {
      setAtlasDeck("command", { scroll: false });
      selectLane(companyQuestLane.dataset.companyQuestLane, "overview");
      settleDetailPanelIntoView();
      return;
    }

    const companyChronicleAction = event.target.closest("[data-company-chronicle-action]");
    if (companyChronicleAction) {
      const action = companyChronicleAction.dataset.companyChronicleAction;
      if (action === "latest") setFeedFilter("all");
      if (action === "proof") setFeedFilter("evidence");
      if (action === "gates") setFeedFilter("service_request");
      setAtlasDeck("history", { scroll: false });
      document.querySelector(".mission-feed-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }

    const companyChronicleLane = event.target.closest("[data-company-chronicle-lane]");
    if (companyChronicleLane) {
      setAtlasDeck("command", { scroll: false });
      selectLane(companyChronicleLane.dataset.companyChronicleLane, "trail");
      settleDetailPanelIntoView();
      return;
    }

    const experimentLabAction = event.target.closest("[data-experiment-lab-action]");
    if (experimentLabAction) {
      const action = experimentLabAction.dataset.experimentLabAction;
      if (action === "proof") setFeedFilter("evidence");
      if (action === "gates") setFeedFilter("service_request");
      if (action === "wins") setFeedFilter("outcome");
      setAtlasDeck("history", { scroll: false });
      document.querySelector(".mission-feed-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }

    const experimentLabLane = event.target.closest("[data-experiment-lab-lane]");
    if (experimentLabLane) {
      setAtlasDeck("command", { scroll: false });
      selectLane(experimentLabLane.dataset.experimentLabLane, "trail");
      settleDetailPanelIntoView();
      return;
    }

    const minigameCodexAction = event.target.closest("[data-minigame-codex-action]");
    if (minigameCodexAction) {
      const action = minigameCodexAction.dataset.minigameCodexAction;
      if (action === "arcade") {
        setAtlasDeck("worlds", { scroll: false });
        document.querySelector("#arcade-deck")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "assets") {
        setAtlasDeck("library", { scroll: false });
        state.assetFilter = "game";
        writeAssetFilter();
        renderAssetVault();
        document.querySelector(".asset-vault-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "forge") {
        setAtlasDeck("library", { scroll: false });
        document.querySelector("#expansion-forge")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const minigameCodexLane = event.target.closest("[data-minigame-codex-lane]");
    if (minigameCodexLane) {
      setAtlasDeck("command", { scroll: false });
      selectLane(minigameCodexLane.dataset.minigameCodexLane, "game");
      settleDetailPanelIntoView();
      return;
    }

    const crewActionButton = event.target.closest("[data-crew-action]");
    if (crewActionButton) {
      const crewLane = crewActionButton.closest("[data-crew-lane]");
      const laneId = crewLane?.dataset.crewLane;
      const lane = state.snapshot.lanes.find((item) => item.id === laneId);
      const action = crewActionButton.dataset.crewAction;
      if (action === "comms" && lane) {
        selectLane(lane.id, "comms");
        settleDetailPanelIntoView();
      }
      if (action === "path" && lane) {
        selectLane(lane.id, "path");
        settleDetailPanelIntoView();
      }
      if (action === "queue" && lane) {
        const suggestion =
          state.snapshot.dispatchConsole?.suggestions?.find((item) => item.laneId === lane.id) ??
          laneDispatchSuggestion(lane);
        stageDispatch(suggestion);
      }
      return;
    }

    const milestoneAction = event.target.closest("[data-milestone-action]");
    if (milestoneAction) {
      const action = milestoneAction.dataset.milestoneAction;
      if (["path", "chronicle", "trail"].includes(action)) {
        state.detailView = action;
        renderDetail();
        syncRoute();
        settleDetailPanelIntoView();
      }
      return;
    }

    const milestoneLens = event.target.closest("[data-milestone-lens]");
    if (milestoneLens) {
      const lane = selectedLane();
      const lens = milestoneLens.dataset.milestoneLens;
      if (lane && ["all", "blockers", "unlocks", "events", "future"].includes(lens)) {
        state.milestoneLensByLane[lane.id] = lens;
        renderDetail();
        document.querySelector("#milestone-runway")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
      return;
    }

    const agentPartyAction = event.target.closest("[data-agent-party-action]");
    if (agentPartyAction) {
      const laneId = agentPartyAction.closest("[data-agent-party-lane]")?.dataset.agentPartyLane;
      const lane = state.snapshot.lanes.find((item) => item.id === laneId);
      const action = agentPartyAction.dataset.agentPartyAction;
      if (action === "comms" && lane) {
        selectLane(lane.id, "comms");
        settleDetailPanelIntoView();
      }
      if (action === "path" && lane) {
        selectLane(lane.id, "path");
        settleDetailPanelIntoView();
      }
      if (action === "queue" && lane) {
        const suggestion =
          state.snapshot.dispatchConsole?.suggestions?.find((item) => item.laneId === lane.id) ??
          laneDispatchSuggestion(lane);
        stageDispatch(suggestion);
        renderDetail();
      }
      return;
    }

    const minigameForgeAction = event.target.closest("[data-minigame-forge-action]");
    if (minigameForgeAction) {
      const lane = selectedLane();
      const action = minigameForgeAction.dataset.minigameForgeAction;
      if (action === "game" && lane) {
        selectLane(lane.id, "game");
        settleDetailPanelIntoView();
      }
      if (action === "asset") {
        state.assetFilter = "game";
        writeAssetFilter();
        renderAssetVault();
        document.querySelector(".asset-vault-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "arcade") {
        document.querySelector("#arcade-deck")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const gateRadarAction = event.target.closest("[data-gate-radar-action]");
    if (gateRadarAction) {
      const lane = selectedLane();
      const action = gateRadarAction.dataset.gateRadarAction;
      if (action === "comms" && lane) {
        selectLane(lane.id, "comms");
        settleDetailPanelIntoView();
      }
      if (action === "path" && lane) {
        selectLane(lane.id, "path");
        settleDetailPanelIntoView();
      }
      if (action === "queue" && lane) {
        stageDispatch(laneDispatchSuggestion(lane));
        renderDetail();
      }
      return;
    }

    const gateRadarFilter = event.target.closest("[data-gate-radar-filter]");
    if (gateRadarFilter) {
      const lane = selectedLane();
      const nextFilter = gateRadarFilter.dataset.gateRadarFilter;
      if (lane && gateRadarFilters().includes(nextFilter)) {
        state.gateRadarFilterByLane = { ...state.gateRadarFilterByLane, [lane.id]: nextFilter };
        writeGateRadarFilters();
        renderDetail();
      }
      return;
    }

    const gateNoteFocus = event.target.closest("[data-gate-note-focus]");
    if (gateNoteFocus) {
      const lane = selectedLane();
      if (lane) {
        state.gateRadarNoteFocusByLane = { ...state.gateRadarNoteFocusByLane, [lane.id]: gateNoteFocus.dataset.gateNoteFocus };
        renderDetail();
        document.querySelector("[data-gate-note-input]")?.focus();
      }
      return;
    }

    const gateNoteAction = event.target.closest("[data-gate-note-action]");
    if (gateNoteAction) {
      const lane = selectedLane();
      const noteId = gateNoteAction.dataset.gateNoteId;
      if (lane && noteId) {
        const notes = { ...(state.gateRadarNotesByLane[lane.id] ?? {}) };
        if (gateNoteAction.dataset.gateNoteAction === "clear") {
          delete notes[noteId];
        } else {
          const input = document.querySelector(`[data-gate-note-input="${CSS.escape(noteId)}"]`);
          const text = cleanGateRadarNote(input?.value);
          if (text) {
            notes[noteId] = { text, updatedAt: new Date().toISOString() };
          } else {
            delete notes[noteId];
          }
        }
        state.gateRadarNotesByLane = { ...state.gateRadarNotesByLane, [lane.id]: notes };
        state.gateRadarNoteFocusByLane = { ...state.gateRadarNoteFocusByLane, [lane.id]: noteId };
        writeGateRadarNotes();
        renderDetail();
      }
      return;
    }

    const forgeLaneButton = event.target.closest("[data-forge-lane-id]");
    if (forgeLaneButton) {
      selectLane(forgeLaneButton.dataset.forgeLaneId, "game");
      return;
    }

    const relayAction = event.target.closest("[data-relay-action]");
    if (relayAction) {
      const lane = relaySelectedLane();
      const action = relayAction.dataset.relayAction;
      if (action === "path" && lane) selectLane(lane.id, "path");
      if (action === "comms" && lane) selectLane(lane.id, "comms");
      if (action === "feed") {
        setFeedFilter("all");
        document.querySelector(".mission-feed-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "assets") {
        state.assetFilter = "system";
        writeAssetFilter();
        renderAssetVault();
        document.querySelector(".asset-vault-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const worldsLaunchAction = event.target.closest("[data-worlds-launch-action]");
    if (worldsLaunchAction) {
      const action = worldsLaunchAction.dataset.worldsLaunchAction;
      if (action === "loom") {
        setAtlasDeck("worlds", { scroll: false });
        document.querySelector("#world-loom")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "arcade") {
        setAtlasDeck("worlds", { scroll: false });
        document.querySelector("#arcade-deck")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "registry") {
        setAtlasDeck("worlds", { scroll: false });
        document.querySelector("#minigame-registry-codex")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "genesis") {
        setAtlasDeck("library", { scroll: false });
        document.querySelector("#lane-genesis-foundry")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "library") {
        setAtlasDeck("library", { scroll: false });
        state.assetFilter = "game";
        writeAssetFilter();
        renderAssetVault();
        document.querySelector(".asset-vault-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const worldsLaunchLane = event.target.closest("[data-worlds-launch-lane]");
    if (worldsLaunchLane) {
      setAtlasDeck("command", { scroll: false });
      selectLane(worldsLaunchLane.dataset.worldsLaunchLane, "path");
      settleDetailPanelIntoView();
      return;
    }

    const worldLoomStepButton = event.target.closest("[data-world-loom-step]");
    if (worldLoomStepButton) {
      worldLoomStep(Number(worldLoomStepButton.dataset.worldLoomStep || 0));
      return;
    }

    const worldLoomAction = event.target.closest("[data-world-loom-action]");
    if (worldLoomAction) {
      const lane = relaySelectedLane();
      const action = worldLoomAction.dataset.worldLoomAction;
      if (action === "path" && lane) selectLane(lane.id, "path");
      if (action === "game" && lane) selectLane(lane.id, "game");
      if (action === "comms" && lane) selectLane(lane.id, "comms");
      if (action === "assets") {
        state.assetFilter = "system";
        writeAssetFilter();
        renderAssetVault();
        document.querySelector(".asset-vault-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const worldLoomLane = event.target.closest("[data-world-loom-lane]");
    if (worldLoomLane) {
      setAtlasDeck("command", { scroll: false });
      selectLane(worldLoomLane.dataset.worldLoomLane, "overview");
      settleDetailPanelIntoView();
      return;
    }

    const arcadeLaunchButton = event.target.closest("[data-arcade-launch]");
    if (arcadeLaunchButton) {
      setAtlasDeck("command", { scroll: false });
      selectLane(arcadeLaunchButton.dataset.arcadeLaunch, "game");
      settleDetailPanelIntoView();
      return;
    }

    const arcadePathButton = event.target.closest("[data-arcade-path]");
    if (arcadePathButton) {
      setAtlasDeck("command", { scroll: false });
      selectLane(arcadePathButton.dataset.arcadePath, "path");
      settleDetailPanelIntoView();
      return;
    }

    const arcadeAssetButton = event.target.closest("[data-arcade-asset]");
    if (arcadeAssetButton) {
      selectLane(arcadeAssetButton.dataset.arcadeAsset, "overview");
      state.assetFilter = "game";
      writeAssetFilter();
      renderAssetVault();
      document.querySelector(".asset-vault-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }

    const motionLaneButton = event.target.closest("[data-motion-lane]");
    if (motionLaneButton) {
      setAtlasDeck("command", { scroll: false });
      selectLane(motionLaneButton.dataset.motionLane, "overview");
      settleDetailPanelIntoView();
      return;
    }

    const motionAction = event.target.closest("[data-motion-action]");
    if (motionAction) {
      const lane = relaySelectedLane();
      const action = motionAction.dataset.motionAction;
      if (action === "arcade") {
        document.querySelector("#arcade-deck")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "assets") {
        state.assetFilter = "game";
        writeAssetFilter();
        renderAssetVault();
        document.querySelector(".asset-vault-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "game" && lane) {
        setAtlasDeck("command", { scroll: false });
        selectLane(lane.id, "game");
        settleDetailPanelIntoView();
      }
      return;
    }

    const laneGenesisAction = event.target.closest("[data-lane-genesis-action]");
    if (laneGenesisAction) {
      const action = laneGenesisAction.dataset.laneGenesisAction;
      if (action === "forge") {
        document.querySelector("#expansion-forge")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "games") {
        document.querySelector("#minigame-registry-codex")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "assets") {
        state.assetFilter = "all";
        writeAssetFilter();
        renderAssetVault();
        document.querySelector(".asset-vault-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "bots") {
        setAtlasDeck("command", { scroll: false });
        setCommandArchivePanel("operators", { scroll: true });
      }
      return;
    }

    const laneGenesisLane = event.target.closest("[data-lane-genesis-lane]");
    if (laneGenesisLane) {
      setAtlasDeck("command", { scroll: false });
      selectLane(laneGenesisLane.dataset.laneGenesisLane, "game");
      settleDetailPanelIntoView();
      return;
    }

    const creatorAction = event.target.closest("[data-creator-action]");
    if (creatorAction) {
      const lane = relaySelectedLane();
      const action = creatorAction.dataset.creatorAction;
      if (action === "forge") {
        document.querySelector("#expansion-forge")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "assets") {
        state.assetFilter = "all";
        writeAssetFilter();
        renderAssetVault();
        document.querySelector(".asset-vault-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "path" && lane) selectLane(lane.id, "path");
      if (action === "comms" && lane) selectLane(lane.id, "comms");
      if (action === "feed") {
        setFeedFilter("all");
        document.querySelector(".mission-feed-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const feedViewButton = event.target.closest("[data-feed-view]");
    if (feedViewButton) {
      const view = allFeedViews().find((item) => item.id === feedViewButton.dataset.feedView);
      if (view) setFeedFilter(view.filter);
      return;
    }

    const trophyTierButton = event.target.closest(".trophy-tier-chip[data-trophy-tier]");
    if (trophyTierButton) {
      setTrophyTierFilter(trophyTierButton.dataset.trophyTier);
      return;
    }

    const unlockToastButton = event.target.closest("[data-unlock-toast]");
    if (unlockToastButton?.dataset.unlockToast === "dismiss") {
      dismissUnlockToast();
      return;
    }

    const feedViewAction = event.target.closest("[data-feed-view-action]");
    if (feedViewAction) {
      if (feedViewAction.dataset.feedViewAction === "save") saveCurrentFeedView();
      if (feedViewAction.dataset.feedViewAction === "reset") {
        stopFeedPlayback();
        state.savedFeedViews = [];
        writeSavedFeedViews();
        setFeedFilter("all");
      }
      return;
    }

    const feedPlaybackButton = event.target.closest("[data-feed-playback]");
    if (feedPlaybackButton) {
      const action = feedPlaybackButton.dataset.feedPlayback;
      if (action === "prev") {
        stopFeedPlayback();
        stepFeedPlayback(-1);
      }
      if (action === "next") {
        stopFeedPlayback();
        stepFeedPlayback(1);
      }
      if (action === "toggle") {
        if (state.feedPlaying) {
          stopFeedPlayback();
        } else {
          state.feedPlaying = true;
          state.feedPlaybackTimer = window.setInterval(() => stepFeedPlayback(1), 1600);
        }
        renderMissionFeed();
      }
      return;
    }

    const feedItem = event.target.closest("[data-feed-lane-id]");
    if (feedItem) {
      selectLane(feedItem.dataset.feedLaneId, "trail");
      if (feedItem.closest("#unlock-toast")) dismissUnlockToast();
    }

    const assetFilterButton = event.target.closest("[data-asset-filter]");
    if (assetFilterButton) {
      const nextFilter = assetFilterButton.dataset.assetFilter;
      if (assetKinds().includes(nextFilter)) {
        state.assetFilter = nextFilter;
        writeAssetFilter();
        renderAssetVault();
      }
      return;
    }

    const assetLaneCard = event.target.closest("[data-asset-lane-id]");
    if (assetLaneCard) {
      selectLane(assetLaneCard.dataset.assetLaneId, assetLaneCard.dataset.assetView || "overview");
      return;
    }

    const identityAction = event.target.closest("[data-identity-action]");
    if (identityAction) {
      const action = identityAction.dataset.identityAction;
      const leadLaneId =
        state.selectedLaneId ??
        state.snapshot.agents?.find((agent) => Boolean(agent.lane?.id))?.lane?.id ??
        state.snapshot.lanes?.[0]?.id;
      if (action === "comms" && leadLaneId) {
        selectLane(leadLaneId, "comms");
        settleDetailPanelIntoView();
      }
      if (action === "assets") {
        state.assetFilter = "agent";
        writeAssetFilter();
        renderAssetVault();
        document.querySelector(".asset-vault-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "forge") {
        document.querySelector("#creator-kit, #expansion-forge")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const agentSpriteAction = event.target.closest("[data-agent-sprite-action]");
    if (agentSpriteAction) {
      const action = agentSpriteAction.dataset.agentSpriteAction;
      const leadLaneId =
        state.selectedLaneId ??
        state.snapshot.agents?.find((agent) => Boolean(agent.lane?.id))?.lane?.id ??
        state.snapshot.lanes?.[0]?.id;
      if (action === "comms" && leadLaneId) {
        selectLane(leadLaneId, "comms");
        settleDetailPanelIntoView();
      }
      if (action === "assets") {
        state.assetFilter = "agent";
        writeAssetFilter();
        renderAssetVault();
        document.querySelector(".asset-vault-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      if (action === "forge") {
        document.querySelector("#creator-kit")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      return;
    }

    const agentSpriteLane = event.target.closest("[data-agent-sprite-lane]");
    if (agentSpriteLane) {
      selectLane(agentSpriteLane.dataset.agentSpriteLane, "comms");
      settleDetailPanelIntoView();
      return;
    }

    const agentLaneButton = event.target.closest("[data-agent-lane-id]");
    if (agentLaneButton) {
      selectLane(agentLaneButton.dataset.agentLaneId, "comms");
      return;
    }

    const threadPathButton = event.target.closest("[data-thread-path-lane]");
    if (threadPathButton) {
      selectLane(threadPathButton.dataset.threadPathLane, "path");
      return;
    }

    const questEventFocus = event.target.closest("[data-quest-event-focus]");
    if (questEventFocus && state.selectedLaneId) {
      const focusIndex = Number(questEventFocus.dataset.questEventFocus ?? 0);
      state.questEventFocusByLane = { ...state.questEventFocusByLane, [state.selectedLaneId]: Number.isFinite(focusIndex) ? focusIndex : 0 };
      renderDetail();
      return;
    }

    const questFocusNode = event.target.closest("[data-quest-focus-node]");
    if (questFocusNode && state.selectedLaneId) {
      state.questNodeFocusByLane = { ...state.questNodeFocusByLane, [state.selectedLaneId]: questFocusNode.dataset.questFocusNode };
      renderDetail();
      return;
    }

    const questExpansionLens = event.target.closest("[data-quest-expansion-lens]");
    const questExpansionLaneId = state.selectedLaneId ?? selectedLane()?.id;
    if (questExpansionLens && questExpansionLaneId) {
      state.questExpansionLensByLane = { ...state.questExpansionLensByLane, [questExpansionLaneId]: questExpansionLens.dataset.questExpansionLens };
      renderDetail();
      return;
    }

    const laneButton = event.target.closest("[data-lane-id]");
    if (laneButton) {
      selectLane(laneButton.dataset.laneId);
      return;
    }

    const overviewStageButton = event.target.closest("[data-overview-stage]");
    if (overviewStageButton && state.selectedLaneId) {
      const stage = overviewStageButton.dataset.overviewStage;
      const lane = selectedLane();
      if (lane && overviewStageDefinitions(lane).some((item) => item.id === stage)) {
        state.overviewStageViewByLane = { ...state.overviewStageViewByLane, [lane.id]: stage };
        renderDetail();
        document.querySelector(".overview-stage-dock")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
      return;
    }

    const chronicleStageButton = event.target.closest("[data-chronicle-stage]");
    if (chronicleStageButton && state.selectedLaneId) {
      const stage = chronicleStageButton.dataset.chronicleStage;
      const lane = selectedLane();
      if (lane && chronicleViewModel(lane).stages.some((item) => item.id === stage)) {
        state.chronicleStageViewByLane = { ...state.chronicleStageViewByLane, [lane.id]: stage };
        renderDetail();
        document.querySelector(".chronicle-stage-dock")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
      return;
    }

    const viewButton = event.target.closest("[data-detail-view]");
    if (viewButton) {
      state.detailView = viewButton.dataset.detailView;
      renderDetail();
      syncRoute();
      focusPathBoardFromRoute({ view: state.detailView }, "smooth");
    }

    const expandButton = event.target.closest("[data-expand-trail]");
    if (expandButton) {
      const laneId = expandButton.dataset.expandTrail;
      state.trailLimitByLane[laneId] = (state.trailLimitByLane[laneId] ?? 18) + 18;
      renderDetail();
    }

    const copyButton = event.target.closest("[data-copy-command]");
    if (copyButton) {
      const lane = state.snapshot.lanes.find((item) => item.id === copyButton.dataset.copyCommand);
      if (lane) {
        const copied = await copyText(commandPreview(lane));
        state.copiedCommandFor = copied ? lane.id : `manual:${lane.id}`;
        renderDetail();
      }
    }

    const gameButton = event.target.closest("[data-game-action]");
    if (gameButton && state.selectedLaneId) {
      const lane = state.snapshot.lanes.find((item) => item.id === state.selectedLaneId);
      const max = Math.max(gameStepCount(lane) - 1, 0);
      const current = state.gameStepByLane[state.selectedLaneId] ?? 0;
      if (gameButton.dataset.gameAction === "reset") state.gameStepByLane[state.selectedLaneId] = 0;
      if (gameButton.dataset.gameAction === "prev") state.gameStepByLane[state.selectedLaneId] = Math.max(0, current - 1);
      if (gameButton.dataset.gameAction === "next") state.gameStepByLane[state.selectedLaneId] = Math.min(max, current + 1);
      renderDetail();
    }
  });

  el.stateFilter.addEventListener("change", () => {
    state.filter = el.stateFilter.value;
    const lanes = filteredLanes();
    if (!lanes.some((lane) => lane.id === state.selectedLaneId)) {
      state.selectedLaneId = lanes[0]?.id ?? state.snapshot.lanes[0]?.id;
    }
    renderProgressionConstellation();
    renderRealmPacks();
    renderLaneList();
    renderDetail();
  });

  el.missionFeedFilter.addEventListener("change", () => {
    stopFeedPlayback();
    setFeedFilter(el.missionFeedFilter.value);
  });

  el.trophyLaneFilter?.addEventListener("change", () => {
    setTrophyLaneFilter(el.trophyLaneFilter.value);
  });

  el.refreshButton.addEventListener("click", loadSnapshot);
  el.zoomIn.addEventListener("click", () => zoom(0.12));
  el.zoomOut.addEventListener("click", () => zoom(-0.12));
  el.zoomReset.addEventListener("click", () => resetView());

  el.mapViewport.addEventListener("pointerdown", (event) => {
    state.dragging = true;
    state.dragStart = {
      x: event.clientX - state.transform.x,
      y: event.clientY - state.transform.y,
    };
    el.mapViewport.setPointerCapture(event.pointerId);
    el.mapViewport.classList.add("dragging");
  });

  el.mapViewport.addEventListener("pointermove", (event) => {
    if (!state.dragging) return;
    state.transform.x = event.clientX - state.dragStart.x;
    state.transform.y = event.clientY - state.dragStart.y;
    applyTransform(false);
  });

  el.mapViewport.addEventListener("pointerup", (event) => {
    state.dragging = false;
    el.mapViewport.releasePointerCapture(event.pointerId);
    el.mapViewport.classList.remove("dragging");
  });

  el.nodeLayer.addEventListener("pointerover", (event) => {
    const node = event.target.closest(".lane-node[data-lane-id]");
    if (node) setMapHover(node.dataset.laneId);
  });

  el.nodeLayer.addEventListener("pointerout", (event) => {
    const node = event.target.closest(".lane-node[data-lane-id]");
    if (node && !node.contains(event.relatedTarget)) setMapHover(null);
  });

  el.nodeLayer.addEventListener("focusin", (event) => {
    const node = event.target.closest(".lane-node[data-lane-id]");
    if (node) setMapHover(node.dataset.laneId);
  });

  el.nodeLayer.addEventListener("focusout", (event) => {
    const node = event.target.closest(".lane-node[data-lane-id]");
    if (node && !node.contains(event.relatedTarget)) setMapHover(null);
  });

  el.mapViewport.addEventListener(
    "wheel",
    (event) => {
      event.preventDefault();
      zoom(event.deltaY > 0 ? -0.08 : 0.08);
    },
    { passive: false }
  );

  window.addEventListener("resize", () => {
    resizeParticles();
    resetView(false);
  });

  window.addEventListener("hashchange", () => {
    applyRouteFromHash();
  });

  window.setInterval(applyRouteFromHash, 400);
}

function resizeParticles() {
  const dpr = window.devicePixelRatio || 1;
  el.canvas.width = Math.floor(window.innerWidth * dpr);
  el.canvas.height = Math.floor(window.innerHeight * dpr);
  el.canvas.style.width = `${window.innerWidth}px`;
  el.canvas.style.height = `${window.innerHeight}px`;
}

function runParticles() {
  const ctx = el.canvas.getContext("2d");
  const reduceMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches ?? false;
  const particles = Array.from({ length: 118 }, (_, index) => ({
    x: Math.random(),
    y: Math.random(),
    r: 0.6 + Math.random() * 1.8,
    speed: 0.00012 + Math.random() * 0.00034,
    drift: 0.00003 + Math.random() * 0.00012,
    phase: Math.random() * Math.PI * 2,
    hue: index % 4,
  }));

  function draw(time = 0) {
    const dpr = window.devicePixelRatio || 1;
    const signal = motionSignal();
    const primary = hexToRgb(signal.accent, [68, 215, 201]);
    const secondary = hexToRgb(signal.accentAlt, [244, 186, 85]);
    const danger = signal.mode === "gated" ? [255, 111, 97] : [139, 224, 110];
    const focusX = signal.focusX * el.canvas.width;
    const focusY = signal.focusY * el.canvas.height;
    const speedBoost = reduceMotion ? 0 : signal.intensity;
    const ribbons = kineticFieldRibbons(signal);

    ctx.clearRect(0, 0, el.canvas.width, el.canvas.height);
    ctx.save();
    ctx.globalCompositeOperation = "lighter";

    const focusGradient = ctx.createRadialGradient(focusX, focusY, 0, focusX, focusY, Math.min(el.canvas.width, el.canvas.height) * 0.28);
    focusGradient.addColorStop(0, `rgba(${primary.join(",")}, ${reduceMotion ? 0.08 : 0.16})`);
    focusGradient.addColorStop(0.48, `rgba(${secondary.join(",")}, ${reduceMotion ? 0.035 : 0.08})`);
    focusGradient.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = focusGradient;
    ctx.fillRect(0, 0, el.canvas.width, el.canvas.height);

    if (signal.mode === "path" || signal.mode === "playback") {
      for (const ribbon of ribbons) {
        const color =
          ribbon.kind === "gate"
            ? [255, 111, 97]
            : ribbon.kind === "proof"
              ? [139, 224, 110]
              : ribbon.kind === "tests"
                ? secondary
                : primary;
        const distance = Math.min(el.canvas.width, el.canvas.height) * ribbon.reach;
        const startAngle = ribbon.angle + time * 0.00008 * (reduceMotion ? 0 : 1);
        const endX = focusX + Math.cos(startAngle) * distance;
        const endY = focusY + Math.sin(startAngle) * distance * 0.62;
        const controlX = focusX + Math.cos(startAngle + ribbon.bend) * distance * 0.52;
        const controlY = focusY + Math.sin(startAngle + ribbon.bend) * distance * 0.38;
        const alpha = (0.08 + ribbon.charge / 520) * (reduceMotion ? 0.55 : 1);

        ctx.strokeStyle = `rgba(${color.join(",")}, ${alpha})`;
        ctx.lineWidth = Math.max(1, dpr * (0.8 + ribbon.charge / 160));
        ctx.beginPath();
        ctx.moveTo(focusX, focusY);
        ctx.quadraticCurveTo(controlX, controlY, endX, endY);
        ctx.stroke();

        if (!reduceMotion) {
          const travel = (time * 0.00018 + ribbon.phase) % 1;
          const oneMinus = 1 - travel;
          const packetX = oneMinus * oneMinus * focusX + 2 * oneMinus * travel * controlX + travel * travel * endX;
          const packetY = oneMinus * oneMinus * focusY + 2 * oneMinus * travel * controlY + travel * travel * endY;
          const packetSize = Math.max(3, dpr * (2.4 + ribbon.charge / 42));
          ctx.save();
          ctx.translate(packetX, packetY);
          ctx.rotate(startAngle + Math.PI / 4);
          ctx.fillStyle = `rgba(${color.join(",")}, ${Math.min(0.72, 0.28 + ribbon.charge / 180)})`;
          ctx.fillRect(-packetSize / 2, -packetSize / 2, packetSize, packetSize);
          ctx.restore();
        }
      }
    }

    for (const particle of particles) {
      const dx = signal.focusX - particle.x;
      const dy = signal.focusY - particle.y;
      particle.y -= particle.speed * 16 * speedBoost;
      particle.x += Math.sin(time * 0.00028 + particle.phase + particle.y * 9) * particle.drift * speedBoost;
      particle.x += dx * 0.0007 * speedBoost;
      particle.y += dy * 0.00032 * speedBoost;
      if (particle.y < -0.02) {
        particle.y = 1.02;
        particle.x = Math.random();
      }
      if (particle.x < -0.02) particle.x = 1.02;
      if (particle.x > 1.02) particle.x = -0.02;
      const x = particle.x * el.canvas.width;
      const y = particle.y * el.canvas.height;
      const color = particle.hue === 0 ? primary : particle.hue === 1 ? secondary : particle.hue === 2 ? danger : [196, 212, 207];
      const distance = Math.hypot(x - focusX, y - focusY) / Math.max(el.canvas.width, el.canvas.height);
      const alpha = Math.max(0.12, 0.34 - distance * 0.54) * (reduceMotion ? 0.5 : 1);
      ctx.beginPath();
      ctx.fillStyle = `rgba(${color.join(",")}, ${alpha})`;
      ctx.arc(x, y, particle.r * dpr * (signal.mode === "playback" ? 1.22 : 1), 0, Math.PI * 2);
      ctx.fill();
    }

    if (!reduceMotion) {
      ctx.strokeStyle = `rgba(${secondary.join(",")}, ${signal.mode === "playback" ? 0.32 : 0.18})`;
      ctx.lineWidth = Math.max(1, dpr);
      ctx.beginPath();
      const orbit = (Math.sin(time * 0.0012) + 1) * 0.5;
      ctx.ellipse(focusX, focusY, (42 + orbit * 24) * dpr, (18 + orbit * 10) * dpr, time * 0.00045, 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.restore();
  }

  function frame(time) {
    draw(time);
    if (reduceMotion) return;
    requestAnimationFrame(frame);
  }

  resizeParticles();
  if (reduceMotion) {
    draw();
  } else {
    requestAnimationFrame(frame);
  }
}

state.stagedDispatches = readDispatchOutbox();
state.dispatchHistory = readDispatchHistory();
state.feedFilter = readFeedFilter();
state.savedFeedViews = readSavedFeedViews();
state.commandArchivePanel = readCommandArchivePanel();
setupEvents();
runParticles();
loadSnapshot();








