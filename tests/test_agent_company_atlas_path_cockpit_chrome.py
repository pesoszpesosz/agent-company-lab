from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def css_block(styles: str, selector: str) -> str:
    start = styles.index(f"{selector} {{")
    end = styles.index("\n}", start)
    return styles[start:end]


def test_path_view_hides_redundant_detail_header_before_stage():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert ".detail-content.detail-view-path .detail-top" in styles
    detail_top_block = css_block(styles, ".detail-content.detail-view-path .detail-top")
    assert "display: none;" in detail_top_block

    detail_tabs_block = css_block(styles, ".detail-content.detail-view-path .detail-tabs")
    assert "padding-top: 0;" in detail_tabs_block
    assert "margin-bottom: 6px;" in detail_tabs_block

    detail_tab_block = css_block(styles, ".detail-content.detail-view-path .detail-tab")
    assert "min-height: 28px;" in detail_tab_block
    assert "font-size: 0.64rem;" in detail_tab_block

    viewport_block = css_block(styles, ".detail-content.detail-view-path .path-viewport-section")
    assert "padding: 4px 0 0;" in viewport_block

    assert "Path Cockpit Chrome" in readme
    assert "20260618-path-cockpit-chrome" in index
