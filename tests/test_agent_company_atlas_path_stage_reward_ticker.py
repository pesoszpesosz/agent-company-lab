from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_reward_ticker_keeps_unlocks_out_of_the_playfield():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-reward-ticker */"
    assert marker in styles
    ticker_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"] .unlock-toast'
    assert scoped in ticker_slice
    assert "grid-template-columns: 42px minmax(0, 1fr);" in ticker_slice
    assert "min-height: 64px;" in ticker_slice
    assert "max-height: 88px;" in ticker_slice
    assert ".unlock-toast-art" in ticker_slice
    assert ".unlock-toast-copy > p:not(.eyebrow)" in ticker_slice
    assert "clip: rect(0 0 0 0);" in ticker_slice
    assert ".unlock-toast-copy h3" in ticker_slice
    assert "padding-right: 126px;" in ticker_slice
    assert "white-space: nowrap;" in ticker_slice
    assert ".unlock-toast-actions" in ticker_slice
    assert ".unlock-toast-actions .trophy-open" in ticker_slice
    assert "@media (max-width: 560px)" in ticker_slice
    assert "padding-right: 128px;" in ticker_slice
    assert "@media (prefers-reduced-motion: reduce)" in ticker_slice

    assert "Path Stage Reward Ticker" in readme
    assert "20260620-path-stage-reward-ticker" in index
