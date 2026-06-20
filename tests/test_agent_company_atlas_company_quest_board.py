from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_company_quest_board_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")
    asset = ROOT / "web/assets/system/company-quest-board-20260618.png"

    assert "companyQuestBoard: document.querySelector(\"#company-quest-board\")" in app
    assert "function companyQuestRecords" in app
    assert "function companyQuestBoardStats" in app
    assert "function renderCompanyQuestBoard" in app
    assert "function renderCompanyQuestCard" in app
    assert "renderCompanyQuestBoard()" in app
    assert "Company Quest Board" in app
    assert "company-quest-board-20260618.png" in app
    assert "company-quest-board" in app
    assert "company-quest-visual" in app
    assert "company-quest-stats" in app
    assert "company-quest-track" in app
    assert "company-quest-card" in app
    assert "company-quest-actions" in app
    assert "state.stagedDispatches" in app
    assert 'data-company-quest-action="tasks"' in app
    assert 'data-company-quest-action="gates"' in app
    assert 'data-company-quest-action="wins"' in app
    assert 'data-company-quest-lane' in app

    assert '<section class="company-quest-board-panel" id="company-quest-board"' in index
    assert "operator-identity-bay" in index
    assert asset.exists()
    assert asset.stat().st_size > 100_000

    assert ".company-quest-board-panel" in styles
    assert ".company-quest-visual" in styles
    assert ".company-quest-stats" in styles
    assert ".company-quest-track" in styles
    assert ".company-quest-card" in styles
    assert ".company-quest-actions" in styles
    assert "company-quest-board-20260618.png" in styles

    assert "Company Quest Board" in readme
    assert "company-quest-board-20260618.png" in readme
