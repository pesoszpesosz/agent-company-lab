from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "web" / "app.js"
CSS = ROOT / "web" / "styles.css"
INDEX = ROOT / "web" / "index.html"
README = ROOT / "web" / "README.md"


def test_path_chapter_boss_bar_model_and_mount():
    app = APP.read_text(encoding="utf-8")

    assert "function pathChapterBossBarModel(lane, trail, pathProgress)" in app
    assert "const chapters = pathChapterArchiveItems(trail);" in app
    assert "const focused = focusedPathChapter(lane, chapters);" in app
    assert "const focusCounts = focused?.counts ?? {};" in app
    assert "const nextRecord = focused?.items?.[0] ?? trail[0];" in app
    assert 'id: "chapter"' in app
    assert 'id: "gate"' in app
    assert 'id: "proof"' in app
    assert 'id: "unlock"' in app
    assert 'id: "next"' in app

    assert "function renderPathChapterBossBar(model)" in app
    assert 'class="path-chapter-boss-bar ${escapeHtml(model.tone)}"' in app
    assert 'data-path-chapter-boss-cell="${escapeHtml(cell.id)}"' in app
    assert 'data-path-stage-depth="archive"' in app
    assert 'data-detail-view="trail"' in app
    assert "${renderPathChapterBossBar(chapterBossBar)}" in app

    path_view = app[app.index("function renderPathMapView(lane) {") : app.index("function pathUtilityDockView(lane)")]
    assert "const chapterBossBar = pathChapterBossBarModel(lane, trail, pathProgress);" in path_view
    assert path_view.index("${renderPathStageChapterRadar(chapterRadar)}") < path_view.index("${renderPathChapterBossBar(chapterBossBar)}")
    assert path_view.index("${renderPathChapterBossBar(chapterBossBar)}") < path_view.index("${renderPathCoreDeck")


def test_path_chapter_boss_bar_styles_are_low_scroll_and_motion_safe():
    styles = CSS.read_text(encoding="utf-8")

    marker = "/* 20260620-path-chapter-boss-bar */"
    assert marker in styles
    boss_slice = styles[styles.index(marker) :]
    base = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"] .path-map-board.mission-stage'

    assert f"{base} .path-chapter-boss-bar" in boss_slice
    assert "grid-template-columns: minmax(132px, 0.62fr) repeat(5, minmax(0, 1fr));" in boss_slice
    assert "min-height: 66px;" in boss_slice
    assert ".path-chapter-boss-cell" in boss_slice
    assert "animation: pathChapterBossSweep 7.8s ease-in-out infinite;" in boss_slice
    assert "@keyframes pathChapterBossSweep" in boss_slice
    assert "@media (max-width: 760px)" in boss_slice
    assert "grid-auto-flow: column;" in boss_slice
    assert "grid-auto-columns: minmax(116px, 148px);" in boss_slice
    assert "overflow-x: auto;" in boss_slice
    assert f"{base} .path-chapter-boss-bar::before," in boss_slice
    assert ".path-stage-signal" in boss_slice[boss_slice.rindex("@media (prefers-reduced-motion: reduce)") :]


def test_path_chapter_boss_bar_documented_and_cache_busted():
    readme = README.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")

    assert "Path Chapter Boss Bar" in readme
    assert "selected chapter's gates, proof, unlocks, next record, and archive jumps" in readme
    assert "20260620-path-chapter-boss-bar" in index
    assert "20260620-path-stage-chapter-radar-20260620-path-chapter-boss-bar" in index