from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_mobile_compact_unlock_toast_keeps_reward_feedback_off_the_playfield():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-mobile-compact-unlock-toast */"
    assert marker in styles
    toast_slice = styles[styles.index(marker) :]

    assert "@media (max-width: 560px)" in toast_slice
    assert ".unlock-toast" in toast_slice
    assert "grid-template-columns: 58px minmax(0, 1fr);" in toast_slice
    assert "min-height: 92px;" in toast_slice
    assert "max-height: 168px;" in toast_slice
    assert ".unlock-toast .trophy-sprite > span" in toast_slice
    assert "width: 54px;" in toast_slice
    assert ".unlock-toast-copy > p:not(.eyebrow)" in toast_slice
    assert "clip: rect(0 0 0 0);" in toast_slice
    assert "-webkit-line-clamp: 2;" in toast_slice
    assert ".unlock-toast-meta span:nth-child(3)" in toast_slice
    assert "display: none;" in toast_slice[toast_slice.index(".unlock-toast-meta span:nth-child(3)") :]

    assert "compresses into a reward strip" in readme
    assert "20260620-mobile-compact-unlock-toast" in index
