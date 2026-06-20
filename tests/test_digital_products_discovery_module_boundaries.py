import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_digital_products_discovery_facade_reexports_stage_modules() -> None:
    from agent_company_core import digital_products_discovery as facade
    from agent_company_core import digital_products_demand_proof
    from agent_company_core import digital_products_demand_proof_content
    from agent_company_core import digital_products_demand_memo
    from agent_company_core import digital_products_demand_memo_content
    from agent_company_core import digital_products_build_brief
    from agent_company_core import digital_products_build_brief_content

    assert facade.digital_products_demand_questions is digital_products_demand_proof_content.digital_products_demand_questions
    assert digital_products_demand_proof.digital_products_demand_questions is digital_products_demand_proof_content.digital_products_demand_questions
    assert facade.write_digital_products_local_demand_proof is digital_products_demand_proof.write_digital_products_local_demand_proof
    assert facade.digital_products_memo_candidates is digital_products_demand_memo_content.digital_products_memo_candidates
    assert digital_products_demand_memo.digital_products_memo_candidates is digital_products_demand_memo_content.digital_products_memo_candidates
    assert facade.write_digital_products_local_demand_memo is digital_products_demand_memo.write_digital_products_local_demand_memo
    assert facade.digital_products_build_brief_sections is digital_products_build_brief_content.digital_products_build_brief_sections
    assert facade.digital_products_build_brief_deliverables is digital_products_build_brief_content.digital_products_build_brief_deliverables
    assert facade.digital_products_build_brief_acceptance_criteria is digital_products_build_brief_content.digital_products_build_brief_acceptance_criteria
    assert digital_products_build_brief.digital_products_build_brief_sections is digital_products_build_brief_content.digital_products_build_brief_sections
    assert digital_products_build_brief.digital_products_build_brief_deliverables is digital_products_build_brief_content.digital_products_build_brief_deliverables
    assert digital_products_build_brief.digital_products_build_brief_acceptance_criteria is digital_products_build_brief_content.digital_products_build_brief_acceptance_criteria
    assert facade.write_digital_products_local_build_brief is digital_products_build_brief.write_digital_products_local_build_brief


def test_digital_products_build_brief_content_counts() -> None:
    from agent_company_core import digital_products_build_brief_content

    assert len(digital_products_build_brief_content.digital_products_build_brief_sections()) == 7
    assert len(digital_products_build_brief_content.digital_products_build_brief_deliverables()) == 6
    assert len(digital_products_build_brief_content.digital_products_build_brief_acceptance_criteria()) == 5

def test_digital_products_demand_proof_content_counts() -> None:
    from agent_company_core import digital_products_demand_proof_content

    questions = digital_products_demand_proof_content.digital_products_demand_questions()

    assert len(questions) == 8
    assert sum(1 for item in questions if item["mode"] == "local_only") == 4
    assert sum(1 for item in questions if item["mode"] == "blocked_by_gate") == 4
    assert questions[0]["question_id"] == "local-template-audience"
    assert questions[-1]["gate_required"] == "account_payment_approval"

def test_digital_products_demand_memo_content_counts() -> None:
    from agent_company_core import digital_products_demand_memo_content

    candidates = digital_products_demand_memo_content.digital_products_memo_candidates()
    sections = digital_products_demand_memo_content.digital_products_memo_sections()

    assert len(candidates) == 3
    assert len(sections) == 6
    assert candidates[0]["candidate_id"] == "ai-builder-launch-checklist-pack"
    assert candidates[-1]["candidate_id"] == "creator-sponsor-tracker-template"
    assert sections[-1]["section_id"] == "decision"

