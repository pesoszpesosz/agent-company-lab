from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_chapter_radar_surfaces_history_levels_inside_stage():
    index = read("web/index.html")
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "20260620-path-stage-chapter-radar" in index
    assert "20260620-path-stage-chapter-radar" in index.split('href="./styles.css?v=', 1)[1]
    assert "20260620-path-stage-chapter-radar" in index.split('<script src="./app.js?v=', 1)[1]

    assert "function pathStageChapterRadarModel(lane, trail)" in app
    assert "function renderPathStageChapterRadar(model)" in app
    assert "function focusPathChapter(lane, chapter)" in app
    assert "const chapterRadar = pathStageChapterRadarModel(lane, trail);" in app
    assert "${renderPathStageChapterRadar(chapterRadar)}" in app
    assert 'class="path-stage-chapter-radar' in app
    assert 'class="path-stage-chapter-node ${escapeHtml(item.tone)} ${item.active ? "active" : ""}"' in app
    assert 'data-path-stage-chapter-focus="${escapeHtml(item.key)}"' in app
    assert "const pathStageChapterButton = event.target.closest(\"[data-path-stage-chapter-focus]\");" in app
    assert '[lane.id]: "archive"' in app

    marker = "/* 20260620-path-stage-chapter-radar */"
    assert marker in styles
    radar_slice = styles[styles.index(marker):]
    assert ".path-stage-chapter-radar" in radar_slice
    assert ".path-stage-chapter-radar::before" in radar_slice
    assert ".path-stage-chapter-rail" in radar_slice
    assert ".path-stage-chapter-node" in radar_slice
    assert ".path-stage-chapter-node.active" in radar_slice
    assert ".path-stage-chapter-more" in radar_slice
    assert "@keyframes pathStageChapterRadarSweep" in radar_slice
    assert "@media (max-width: 860px)" in radar_slice

    assert "Path Stage Chapter Radar" in readme
