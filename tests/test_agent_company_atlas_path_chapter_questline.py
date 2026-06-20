from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_chapter_questline_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/path-chapter-questline-20260618.png"

    assert asset.is_file()
    assert asset.stat().st_size > 500_000

    assert "function pathChapterQuestlineStages" in app
    assert "function renderPathChapterQuestline" in app
    assert "path-chapter-questline" in app
    assert "path-chapter-quest-stage" in app
    assert "path-chapter-quest-meter" in app
    assert "path-chapter-quest-pulse" in app
    assert "path-chapter-quest-spark" in app
    assert "system-path-chapter-questline" in app
    assert "path-chapter-questline-20260618.png" in app
    assert "renderPathChapterQuestline(lane, chapter)" in app
    assert "pathEventKey(item)" in app
    assert "data-path-event-focus" in app
    assert "chapter.counts?.gate" in app
    assert "chapter.counts?.outcome" in app
    assert "chronicleNextAction(lane)" in app

    assert ".path-chapter-questline" in styles
    assert ".path-chapter-quest-stage" in styles
    assert ".path-chapter-quest-meter" in styles
    assert ".path-chapter-quest-pulse" in styles
    assert ".path-chapter-quest-spark" in styles
    assert "@keyframes questlinePulseTrail" in styles
    assert "@keyframes questlineSparkRise" in styles
    assert "prefers-reduced-motion" in styles

    assert "path-chapter-questline-pulse" in index
    assert "Chapter Questline" in readme
    assert "pulse trail" in readme
    assert "path-chapter-questline-20260618.png" in readme
