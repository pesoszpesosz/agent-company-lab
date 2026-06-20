from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_chapter_milestone_ladder_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/path-chapter-milestone-ladder-20260618.png"

    assert asset.is_file()
    assert asset.stat().st_size > 500_000

    assert "function pathChapterMilestoneLadderItems" in app
    assert "function renderPathChapterMilestoneLadder" in app
    assert "path-chapter-milestone-ladder" in app
    assert "path-chapter-milestone-rail" in app
    assert "path-chapter-milestone-step" in app
    assert "path-chapter-milestone-orb" in app
    assert "path-chapter-milestone-spark" in app
    assert "path-chapter-milestone-ladder-20260618.png" in app
    assert "system-path-chapter-milestone-ladder" in app
    assert "renderPathChapterMilestoneLadder(lane, chapter)" in app
    assert "pathEventGlyphType(item)" in app
    assert "data-path-event-focus" in app
    assert "item: latestItem," in app
    assert "chapter.counts?.outcome" in app
    assert "chapter.counts?.proof" in app

    assert ".path-chapter-milestone-ladder" in styles
    assert ".path-chapter-milestone-rail" in styles
    assert ".path-chapter-milestone-step" in styles
    assert ".path-chapter-milestone-orb" in styles
    assert ".path-chapter-milestone-spark" in styles
    assert "@keyframes milestoneLadderSpark" in styles
    assert "prefers-reduced-motion" in styles

    assert "path-chapter-milestone-ladder" in index
    assert "Chapter Milestone Ladder" in readme
    assert "path-chapter-milestone-ladder-20260618.png" in readme
