from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_minigame_registry_codex_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/minigame-registry-codex-20260618.png"

    assert "minigameRegistryCodex: document.querySelector(\"#minigame-registry-codex\")" in app
    assert "function minigameRegistryCodexRecords" in app
    assert "function minigameRegistryCodexStats" in app
    assert "function renderMinigameRegistryCodex" in app
    assert "function renderMinigameRegistryCard" in app
    assert "renderMinigameRegistryCodex()" in app
    assert "Minigame Registry Codex" in app
    assert "minigame-registry-codex-20260618.png" in app
    assert "minigame-registry-codex" in app
    assert "minigame-codex-visual" in app
    assert "minigame-codex-stats" in app
    assert "minigame-codex-grid" in app
    assert "minigame-codex-card" in app
    assert "minigame-codex-future" in app
    assert "minigame-codex-actions" in app
    assert 'data-minigame-codex-action="arcade"' in app
    assert 'data-minigame-codex-action="assets"' in app
    assert 'data-minigame-codex-action="forge"' in app
    assert 'data-minigame-codex-lane' in app

    assert '<section class="minigame-registry-codex-panel" id="minigame-registry-codex"' in index
    assert asset.exists()
    assert asset.stat().st_size > 100_000

    assert ".minigame-registry-codex-panel" in styles
    assert ".minigame-codex-visual" in styles
    assert ".minigame-codex-stats" in styles
    assert ".minigame-codex-grid" in styles
    assert ".minigame-codex-card" in styles
    assert ".minigame-codex-future" in styles
    assert ".minigame-codex-actions" in styles
    assert "minigame-registry-codex-20260618.png" in styles

    assert "Minigame Registry Codex" in readme
    assert "minigame-registry-codex-20260618.png" in readme
