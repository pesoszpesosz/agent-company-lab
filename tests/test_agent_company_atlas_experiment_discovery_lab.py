from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_experiment_discovery_lab_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/experiment-discovery-lab-20260618.png"

    assert "experimentDiscoveryLab: document.querySelector(\"#experiment-discovery-lab\")" in app
    assert "function experimentDiscoveryLabRecords" in app
    assert "function experimentDiscoveryLabStats" in app
    assert "function renderExperimentDiscoveryLab" in app
    assert "function renderExperimentDiscoveryCard" in app
    assert "function renderExperimentDiscoveryFutureSlots" in app
    assert "renderExperimentDiscoveryLab(items)" in app
    assert "Experiment Discovery Lab" in app
    assert "experiment-discovery-lab-20260618.png" in app
    assert "experiment-discovery-lab" in app
    assert "experiment-lab-visual" in app
    assert "experiment-lab-stats" in app
    assert "experiment-lab-grid" in app
    assert "experiment-lab-card" in app
    assert "experiment-lab-future" in app
    assert "experiment-lab-actions" in app
    assert 'data-experiment-lab-action="proof"' in app
    assert 'data-experiment-lab-action="gates"' in app
    assert 'data-experiment-lab-action="wins"' in app
    assert "data-experiment-lab-lane" in app

    assert '<div id="experiment-discovery-lab" class="experiment-discovery-lab"></div>' in index
    assert "experiment-discovery-lab" in index
    assert asset.exists()
    assert asset.stat().st_size > 100_000

    assert ".experiment-discovery-lab" in styles
    assert ".experiment-lab-visual" in styles
    assert ".experiment-lab-stats" in styles
    assert ".experiment-lab-grid" in styles
    assert ".experiment-lab-card" in styles
    assert ".experiment-lab-future" in styles
    assert ".experiment-lab-actions" in styles
    assert "experiment-discovery-lab-20260618.png" in styles

    assert "Experiment Discovery Lab" in readme
    assert "experiment-discovery-lab-20260618.png" in readme
