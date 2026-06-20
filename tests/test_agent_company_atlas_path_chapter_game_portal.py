from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_chapter_game_portal_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/path-chapter-game-portal-20260618.png"

    assert asset.is_file()
    assert asset.stat().st_size > 500_000

    assert "function pathChapterGamePortalStats" in app
    assert "function renderPathChapterGamePortal" in app
    assert "path-chapter-game-portal" in app
    assert "path-chapter-game-art" in app
    assert "path-chapter-game-stats" in app
    assert "path-chapter-game-actions" in app
    assert "path-chapter-game-portal-20260618.png" in app
    assert "system-path-chapter-game-portal" in app
    assert "renderPathChapterGamePortal(lane, chapter)" in app
    assert "minigameDefinition(lane)" in app
    assert "gameStepCount(lane)" in app
    assert "visualAssetRecords()" in app
    assert 'data-detail-view="game"' in app
    assert 'data-detail-view="overview"' in app
    assert 'data-detail-view="trail"' in app

    assert ".path-chapter-game-portal" in styles
    assert ".path-chapter-game-art" in styles
    assert ".path-chapter-game-stats" in styles
    assert ".path-chapter-game-actions" in styles
    assert "@keyframes gamePortalScan" in styles
    assert "prefers-reduced-motion" in styles

    assert "path-chapter-game-portal" in index
    assert "Chapter Game Portal" in readme
    assert "path-chapter-game-portal-20260618.png" in readme
