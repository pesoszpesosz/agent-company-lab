from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_detail_view_uses_compact_app_chrome():
    app = read("web/app.js")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    assert "document.body.dataset.detailView = state.detailView" in app
    assert "renderDetail() {" in app
    render_detail_block = app[app.index("function renderDetail() {") : app.index("function renderDetailBody")]
    assert "applyAtlasDeck();" in render_detail_block

    for token in [
        'body[data-detail-view="path"] .topbar',
        'body[data-detail-view="path"] .brand-block',
        'body[data-detail-view="path"] .sigil',
        'body[data-detail-view="path"] h1',
        'body[data-detail-view="path"] .atlas-deck-dock',
        'body[data-detail-view="path"] .atlas-deck-button',
        'body[data-detail-view="path"] .atlas-deck-button em',
        'body[data-detail-view="path"] .detail-panel',
    ]:
        assert token in styles

    compact_chrome = styles[styles.index('body[data-detail-view="path"] .topbar') : styles.index('body[data-detail-view="path"] .atlas-deck-button.active::before')]
    assert "min-height: 46px;" in compact_chrome
    assert "width: 34px;" in compact_chrome
    assert "font-size: 1.55rem;" in compact_chrome
    assert "grid-template-columns: repeat(6, minmax(96px, 1fr));" in compact_chrome
    assert "min-height: 38px;" in compact_chrome
    assert "display: none;" in compact_chrome
    assert "max-height: min(586px, calc(100vh - 134px));" in styles

    assert "Compact Path Chrome" in readme
    assert "20260618-compact-path-chrome" in index
