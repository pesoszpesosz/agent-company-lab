from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_chapter_crew_relay_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")

    assert "function pathChapterCrewRecords" in app
    assert "function renderPathChapterCrewRelay" in app
    assert "path-chapter-crew-relay" in app
    assert "path-chapter-crew-agent" in app
    assert "path-chapter-crew-formation" in app
    assert "path-chapter-crew-rank" in app
    assert "path-chapter-crew-readiness" in app
    assert "path-chapter-crew-actions" in app
    assert "renderPathChapterCrewRelay(lane, chapter)" in app
    assert "data-stage-lane-command" in app
    assert 'data-detail-view="comms"' in app

    assert ".path-chapter-crew-relay" in styles
    assert "chapter-crew-formation-20260618.png" in styles
    assert ".path-chapter-crew-formation" in styles
    assert ".path-chapter-crew-rank" in styles
    assert ".path-chapter-crew-readiness" in styles
    assert ".path-chapter-crew-agent" in styles
    assert ".path-chapter-crew-actions" in styles

    assert "path-chapter-crew-formation" in index
    assert "Chapter Crew Formation" in readme
