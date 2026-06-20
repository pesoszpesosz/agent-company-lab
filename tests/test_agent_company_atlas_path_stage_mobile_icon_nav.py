from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_mobile_icon_nav_removes_text_heavy_phone_toolbar():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-mobile-icon-nav */"
    assert marker in styles
    nav_slice = styles[styles.index(marker) :]

    assert "@media (max-width: 560px)" in nav_slice
    assert ".path-stage-nav-dock" in nav_slice
    assert "grid-template-columns: auto repeat(6, 16px);" in nav_slice
    assert "border-radius: 999px;" in nav_slice
    assert ".path-stage-nav-meter em" in nav_slice
    assert "clip: rect(0 0 0 0);" in nav_slice
    assert ".path-stage-nav-button::after" in nav_slice
    assert "font-size: 0;" in nav_slice
    assert ".path-stage-nav-button.active" in nav_slice

    assert "Path Stage Mobile Icon Nav" in readme
    assert "20260620-path-stage-mobile-icon-nav" in index
