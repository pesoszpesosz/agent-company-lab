from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_command_cockpit_mobile_overview_docks_unlock_toast_as_ticker():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-command-cockpit-mobile-toast-ticker */"
    assert marker in styles
    ticker_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="overview"]'
    toast = f"{scoped} .unlock-toast"

    assert "@media (max-width: 560px)" in ticker_slice
    assert toast in ticker_slice
    assert "grid-template-columns: 40px minmax(0, 1fr);" in ticker_slice
    assert "min-height: 58px;" in ticker_slice
    assert "max-height: 74px;" in ticker_slice
    assert f"{toast}-art" in ticker_slice
    assert f"{toast} .trophy-sprite > span" in ticker_slice
    assert "width: 36px;" in ticker_slice
    assert f"{toast}-copy" in ticker_slice
    assert "padding-right: 102px;" in ticker_slice
    assert f"{toast}-copy h3" in ticker_slice
    assert "white-space: nowrap;" in ticker_slice
    assert f"{toast}-actions" in ticker_slice
    assert "position: absolute;" in ticker_slice
    assert "Command Cockpit Mobile Toast Ticker" in readme
    assert "20260620-command-cockpit-mobile-toast-ticker" in index
