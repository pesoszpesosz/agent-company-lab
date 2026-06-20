from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_control_runway_contract_is_wired():
    app = read("web/app.js")
    index = read("web/index.html")
    styles = read("web/styles.css")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/control-runway-20260618.png"

    assert 'controlRunway: document.querySelector("#control-runway")' in app
    assert "function controlRunwayRecords(" in app
    assert "function renderControlRunwayNode(record, index)" in app
    assert "function renderControlRunway()" in app
    assert "renderControlRunway();" in app
    assert "data-control-runway-lane" in app
    assert "data-control-runway-view" in app
    assert 'event.target.closest("[data-control-runway-lane]")' in app
    assert 'setAtlasDeck("command", { scroll: false })' in app
    assert "control-runway-20260618.png" in app
    assert "system-control-runway" in app

    assert 'id="control-runway"' in index
    assert 'aria-label="Control level runway"' in index

    for token in [
        ".control-runway",
        ".control-runway-head",
        ".control-runway-stats",
        ".control-runway-track",
        ".control-runway-node",
        "controlRunwayScan",
        "control-runway-20260618.png",
        "--runway-charge",
    ]:
        assert token in styles

    assert "Control Runway" in readme
    assert "control-runway-20260618.png" in readme
    assert "compact level nodes" in readme
    assert asset.exists()
    assert asset.stat().st_size > 100_000
