from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_chapter_depth_rings_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/path-chapter-depth-rings-20260618.png"

    assert asset.is_file()
    assert asset.stat().st_size > 500_000

    assert "function pathChapterDepthRingStats" in app
    assert "function renderPathChapterDepthRings" in app
    assert "path-chapter-depth-rings" in app
    assert "path-chapter-depth-orbit" in app
    assert "path-chapter-depth-ring" in app
    assert "path-chapter-depth-key" in app
    assert "path-chapter-depth-rings-20260618.png" in app
    assert "system-path-chapter-depth-rings" in app
    assert "renderPathChapterDepthRings(lane, chapter, filteredRecords, remaining)" in app
    assert "chapter.counts?.proof" in app
    assert "chapter.counts?.gate" in app
    assert "filteredRecords.length" in app

    assert ".path-chapter-depth-rings" in styles
    assert ".path-chapter-depth-orbit" in styles
    assert ".path-chapter-depth-ring" in styles
    assert ".path-chapter-depth-key" in styles
    assert "path-chapter-depth-rings-20260618.png" in styles

    assert "path-chapter-depth-rings" in index
    assert "Chapter Depth Rings" in readme
    assert "path-chapter-depth-rings-20260618.png" in readme
