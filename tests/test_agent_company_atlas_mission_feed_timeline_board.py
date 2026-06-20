from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_mission_feed_timeline_board_summarizes_current_history_lens():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")

    assert "missionFeedTimelineBoard: document.querySelector(\"#mission-feed-timeline-board\")" in app
    assert "function missionFeedTimelineBoardModel(items)" in app
    assert "function renderMissionFeedTimelineBoard(items)" in app
    assert "renderMissionFeedTimelineBoard(items);" in app
    assert 'id="mission-feed-timeline-board"' in index
    assert 'class="mission-feed-timeline-board"' in index
    assert 'class="timeline-board-cell ${escapeHtml(cell.tone)}"' in app
    assert 'data-feed-timeline-cell="${escapeHtml(cell.id)}"' in app
    assert "Current" in app
    assert "Gates" in app
    assert "Proof" in app
    assert "Wins" in app
    assert "Lanes" in app
    assert "new Set(items.map((item) => item.laneId).filter(Boolean)).size" in app
    assert "items.filter((item) => item.kind === \"service_request\").length" in app
    assert "items.filter((item) => item.kind === \"evidence\").length" in app
    assert "items.filter((item) => item.kind === \"outcome\").length" in app

    marker = "/* 20260620-mission-feed-timeline-board */"
    assert marker in styles
    board_slice = styles[styles.index(marker) :]
    assert ".mission-feed-timeline-board" in board_slice
    assert "grid-template-columns: minmax(210px, 0.82fr) repeat(4, minmax(0, 1fr));" in board_slice
    assert "min-height: 112px;" in board_slice
    assert ".timeline-board-cell" in board_slice
    assert "animation: missionFeedTimelineScan 8.4s ease-in-out infinite;" in board_slice
    assert "@keyframes missionFeedTimelineScan" in board_slice
    assert "@media (max-width: 760px)" in board_slice
    mobile_slice = board_slice[board_slice.index("@media (max-width: 760px)") :]
    assert "grid-auto-flow: column;" in mobile_slice
    assert "grid-auto-columns: minmax(146px, 174px);" in mobile_slice
    assert "overflow-x: auto;" in mobile_slice
    assert "@media (prefers-reduced-motion: reduce)" in board_slice

    assert "20260620-mission-feed-timeline-board" in index
    assert "Mission Feed Timeline Board" in readme