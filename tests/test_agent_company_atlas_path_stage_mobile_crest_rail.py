from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_mobile_crest_rail_compresses_top_chrome_before_board():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-mobile-crest-rail */"
    assert marker in styles
    crest_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"]'
    assert "@media (max-width: 560px)" in crest_slice
    assert f"{scoped} .topbar" in crest_slice
    assert "min-height: 32px;" in crest_slice
    assert f"{scoped} .atlas-deck-dock" in crest_slice
    assert "grid-template-columns: repeat(6, minmax(0, 1fr));" in crest_slice
    assert "min-height: 36px;" in crest_slice
    assert "max-height: 38px;" in crest_slice
    assert f"{scoped} .atlas-deck-button span" in crest_slice
    assert "font-size: 0;" in crest_slice
    assert ".atlas-deck-button:nth-child(3) span::before" in crest_slice
    assert 'content: "B";' in crest_slice
    assert f"{scoped} .atlas-deck-button strong" in crest_slice
    assert f"{scoped} .workspace" in crest_slice
    assert "margin-top: 2px;" in crest_slice

    assert "Path Stage Mobile Crest Rail" in readme
    assert "20260620-path-stage-mobile-crest-rail" in index
