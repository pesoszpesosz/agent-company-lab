from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_stage_mobile_shell_collapse_removes_dead_workspace_band():
    styles = read("web/styles.css")
    readme = read("web/README.md")
    index = read("web/index.html")

    marker = "/* 20260620-path-stage-mobile-shell-collapse */"
    assert marker in styles
    shell_slice = styles[styles.index(marker) :]

    scoped = 'body[data-atlas-deck="command"][data-atlas-stage="cockpit"][data-detail-view="path"]'
    assert "@media (max-width: 560px)" in shell_slice
    assert f"{scoped} .workspace" in shell_slice
    assert "min-height: 0 !important;" in shell_slice
    assert "height: auto;" in shell_slice
    assert "align-content: start;" in shell_slice
    assert f"{scoped} .detail-panel" in shell_slice
    assert "max-height: none;" in shell_slice
    assert "overflow: visible;" in shell_slice
    assert f"{scoped} .detail-content.detail-view-path" in shell_slice
    assert f"{scoped} .active-lane-mounted-stage[data-active-stage-view=\"path\"]" in shell_slice

    assert "Path Stage Mobile Shell Collapse" in readme
    assert "20260620-path-stage-mobile-shell-collapse" in index
