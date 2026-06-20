from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_chapter_runway_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")

    assert "pathChapterRunwayLimitByLane" in app
    assert "function pathChapterRunwayStateKey" in app
    assert "function pathChapterRunwayLimit" in app
    assert "function renderPathChapterRunway" in app
    assert "data-path-chapter-runway-focus" in app
    assert "data-path-chapter-runway-reveal" in app
    assert "Chapter Runway" in app
    assert "renderPathChapterRunway(lane, chapter, filteredRecords)" in app

    assert ".path-chapter-runway" in styles
    assert ".path-chapter-runway-node" in styles
    assert ".path-chapter-runway-track" in styles

    assert "Chapter Runway" in readme
