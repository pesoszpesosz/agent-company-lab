from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_chapter_task_board_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")

    assert "function pathChapterTaskBoardItems" in app
    assert "function renderPathChapterTaskBoard" in app
    assert "path-chapter-task-board" in app
    assert "path-chapter-task-card" in app
    assert "path-chapter-task-actions" in app
    assert "renderPathChapterTaskBoard(lane, chapter)" in app
    assert "lane.recentTasks" in app
    assert "pathEventGlyphType(item) === \"task\"" in app
    assert "data-stage-lane-command" in app
    assert 'data-detail-view="comms"' in app

    assert ".path-chapter-task-board" in styles
    assert ".path-chapter-task-card" in styles
    assert ".path-chapter-task-actions" in styles

    assert "path-chapter-task-board" in index
    assert "Chapter Task Board" in readme
