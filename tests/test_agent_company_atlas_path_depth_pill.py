from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_default_stage_depth_controls_float_as_compact_pill():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert 'data-path-stage-depth-active="${escapeHtml(depthView)}"' in app
    assert 'data-path-stage-depth-view="${escapeHtml(depthView)}"' in app

    default_pill = styles[
        styles.index('.path-map-board.mission-stage[data-path-stage-depth-view="stage"] .path-stage-depth-dock')
        : styles.index('.path-map-board.mission-stage[data-path-stage-depth-view="stage"] .path-stage-depth-dock > div:first-child')
    ]
    assert "position: absolute;" in default_pill
    assert "width: clamp(250px, 36vw, 430px);" in default_pill
    assert "min-height: 42px;" in default_pill
    assert "backdrop-filter: blur(18px);" in default_pill
    assert "pathDepthPillScan" in default_pill

    default_label = styles[
        styles.index('.path-map-board.mission-stage[data-path-stage-depth-view="stage"] .path-stage-depth-dock > div:first-child')
        : styles.index('.path-map-board.mission-stage[data-path-stage-depth-view="stage"] .path-stage-depth-cards')
    ]
    assert "display: none;" in default_label

    default_cards = styles[
        styles.index('.path-map-board.mission-stage[data-path-stage-depth-view="stage"] .path-stage-depth-cards')
        : styles.index('.path-map-board.mission-stage[data-path-stage-depth-view="stage"] .path-stage-depth-card {')
    ]
    assert "grid-template-columns: repeat(3, minmax(0, 1fr));" in default_cards
    assert "gap: 4px;" in default_cards

    default_card = styles[
        styles.index('.path-map-board.mission-stage[data-path-stage-depth-view="stage"] .path-stage-depth-card {')
        : styles.index('.path-map-board.mission-stage[data-path-stage-depth-view="stage"] .path-stage-depth-card em')
    ]
    assert "min-height: 32px;" in default_card
    assert "padding: 5px 7px;" in default_card

    default_core_start = styles.index('.path-map-board.mission-stage[data-path-stage-depth-view="stage"] .path-core-deck')
    default_core = styles[default_core_start : styles.index("@media (max-width: 1120px)", default_core_start)]
    assert "align-self: start;" in default_core
    assert "padding-bottom: 7px;" in default_core

    assert "@keyframes pathDepthPillScan" in styles
    assert "Path Depth Pill" in readme
    assert "20260618-path-depth-pill" in index
