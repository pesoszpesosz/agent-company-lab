from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_chapter_spoils_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/path-chapter-spoils-20260618.png"

    assert asset.is_file()
    assert asset.stat().st_size > 500_000

    assert "function pathChapterSpoils" in app
    assert "function renderPathChapterSpoils" in app
    assert "path-chapter-spoils" in app
    assert "path-chapter-spoil-badge" in app
    assert "path-chapter-spoil-medal" in app
    assert "system-path-chapter-spoils" in app
    assert "path-chapter-spoils-20260618.png" in app

    assert ".path-chapter-spoils" in styles
    assert ".path-chapter-spoil-badge" in styles
    assert ".path-chapter-spoil-medal" in styles

    assert "path-chapter-spoils" in index
    assert "Chapter Spoils" in readme
    assert "path-chapter-spoils-20260618.png" in readme
