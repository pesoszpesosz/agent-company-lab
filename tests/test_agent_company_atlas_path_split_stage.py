from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_splits_mission_and_core_deck_on_wide_viewports():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "path-map-board mission-stage" in app
    assert "renderPathMissionGlance" in app
    assert "renderPathStageRibbon" in app
    assert "renderPathCoreDeck" in app

    stage_block = styles[styles.index(".path-map-board.mission-stage {") : styles.index(".path-map-board.mission-stage::after")]
    assert "grid-template-columns: minmax(420px, 0.92fr) minmax(420px, 1.08fr);" in stage_block
    assert "align-items: start;" in stage_block

    mission_block = styles[styles.index(".path-map-board.mission-stage .path-mission-glance {") : styles.index(".path-stage-ribbon {")]
    assert "grid-column: 1;" in mission_block
    assert "grid-row: 1;" in mission_block
    assert "grid-template-columns: 1fr;" in mission_block
    assert "min-height: 0;" in mission_block

    for token in [
        ".path-map-board.mission-stage .path-glance-main p",
        ".path-map-board.mission-stage .path-glance-card small",
        ".path-map-board.mission-stage .path-glance-card",
        ".path-map-board.mission-stage .path-glance-actions",
    ]:
        assert token in styles
    assert "min-height: 44px;" in styles

    ribbon_block = styles[styles.index(".path-stage-ribbon {") : styles.index(".path-stage-ribbon::before")]
    assert "grid-column: 1;" in ribbon_block
    assert "grid-row: 2;" in ribbon_block
    assert ".path-map-board.mission-stage .path-stage-ribbon" in styles
    assert "height: 66px;" in styles
    assert ".path-map-board.mission-stage .path-stage-node" in styles

    core_block = styles[styles.index(".path-map-board.mission-stage .path-core-deck {") : styles.index(".path-map-board.mission-stage .path-chapter-archive")]
    assert "grid-column: 2;" in core_block
    assert "grid-row: 1 / span 2;" in core_block

    assert ".path-map-board.mission-stage .path-chapter-archive" in styles
    assert ".path-map-board.mission-stage .path-utility-dock" in styles
    assert "grid-column: 1 / -1;" in styles
    assert "Path Split Stage" in readme
    assert "20260618-path-split-stage" in index
