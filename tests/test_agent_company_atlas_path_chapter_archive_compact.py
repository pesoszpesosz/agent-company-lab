from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_chapter_archive_defaults_to_compact_level_clusters():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "pathChapterArchiveExpandedByLane" in app
    assert "function pathChapterArchiveExpanded" in app
    assert "function renderPathChapterLevelClusters" in app
    assert "path-chapter-level-clusters" in app
    assert "data-path-chapter-expand" in app
    assert "renderPathChapterRecordDeck(lane, focused)" in app
    assert "pathChapterArchiveExpanded(lane)" in app
    assert app.index("renderPathChapterLevelClusters") < app.index("renderPathChapterRecordDeck(lane, focused)")

    for token in [
        ".path-chapter-archive.is-compact",
        ".path-chapter-level-clusters",
        ".path-chapter-level-cluster",
        ".path-chapter-expand",
        "max-height: 920px",
        "overflow-y: auto",
    ]:
        assert token in styles

    assert "Compact Chapter Archive" in readme
    assert "20260618-path-chapter-archive-compact" in index
