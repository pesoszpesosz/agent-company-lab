from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_operator_identity_bay_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/operator-identity-bay-20260618.png"

    assert "function operatorIdentityBayStats" in app
    assert "function renderOperatorIdentityBay" in app
    assert "renderOperatorIdentityBay(agents)" in app
    assert asset.exists()
    assert asset.stat().st_size > 100_000
    assert "operator-identity-bay-20260618.png" in app
    assert "Operator Identity Bay" in app
    assert "operator-identity-bay" in app
    assert "operator-identity-visual" in app
    assert "operator-identity-strip" in app
    assert "operator-identity-stats" in app
    assert "operator-identity-actions" in app
    assert "state.stagedDispatches" in app
    assert "agentRosterAvatar(agent)" in app
    assert 'data-identity-action="comms"' in app
    assert 'data-identity-action="assets"' in app
    assert 'data-identity-action="forge"' in app

    assert ".operator-identity-bay" in styles
    assert ".operator-identity-visual" in styles
    assert ".operator-identity-strip" in styles
    assert ".operator-identity-stats" in styles
    assert ".operator-identity-actions" in styles
    assert "operator-identity-bay-20260618.png" in styles

    assert "operator-identity-bay" in index
    assert "Operator Identity Bay" in readme
    assert "operator-identity-bay-20260618.png" in readme
