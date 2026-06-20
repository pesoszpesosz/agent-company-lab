from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_path_chapter_evidence_vault_contract_is_wired():
    app = read("web/app.js")
    styles = read("web/styles.css")
    index = read("web/index.html")
    readme = read("web/README.md")

    assert "function pathChapterEvidenceItems" in app
    assert "function renderPathChapterEvidenceVault" in app
    assert "path-chapter-evidence-vault" in app
    assert "path-chapter-evidence-card" in app
    assert "path-chapter-evidence-actions" in app
    assert "renderPathChapterEvidenceVault(lane, chapter)" in app
    assert "artifactPreview?.lines" in app
    assert "pathEventKey(item)" in app
    assert "data-path-event-focus" in app
    assert 'data-detail-view="trail"' in app

    assert ".path-chapter-evidence-vault" in styles
    assert ".path-chapter-evidence-card" in styles
    assert ".path-chapter-evidence-actions" in styles

    assert "path-chapter-evidence-vault" in index
    assert "Chapter Evidence Vault" in readme
