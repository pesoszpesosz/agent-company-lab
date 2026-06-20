from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_company_chronicle_spine_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/company-chronicle-spine-20260618.png"

    assert "companyChronicleSpine: document.querySelector(\"#company-chronicle-spine\")" in app
    assert "function companyChronicleChapters" in app
    assert "function companyChronicleStats" in app
    assert "function renderCompanyChronicleSpine" in app
    assert "function renderCompanyChronicleChapter" in app
    assert "renderCompanyChronicleSpine(items)" in app
    assert "Company Chronicle Spine" in app
    assert "company-chronicle-spine-20260618.png" in app
    assert "company-chronicle-spine" in app
    assert "company-chronicle-visual" in app
    assert "company-chronicle-stats" in app
    assert "company-chronicle-track" in app
    assert "company-chronicle-chapter" in app
    assert "company-chronicle-actions" in app
    assert 'data-company-chronicle-action="latest"' in app
    assert 'data-company-chronicle-action="proof"' in app
    assert 'data-company-chronicle-action="gates"' in app
    assert 'data-company-chronicle-lane' in app

    assert '<div id="company-chronicle-spine" class="company-chronicle-spine"></div>' in index
    assert asset.exists()
    assert asset.stat().st_size > 100_000

    assert ".company-chronicle-spine" in styles
    assert ".company-chronicle-visual" in styles
    assert ".company-chronicle-stats" in styles
    assert ".company-chronicle-track" in styles
    assert ".company-chronicle-chapter" in styles
    assert ".company-chronicle-actions" in styles
    assert "company-chronicle-spine-20260618.png" in styles

    assert "Company Chronicle Spine" in readme
    assert "company-chronicle-spine-20260618.png" in readme
