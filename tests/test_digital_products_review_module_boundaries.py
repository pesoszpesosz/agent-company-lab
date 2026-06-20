import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_digital_products_review_facade_reexports_phase_modules():
    from agent_company_core import digital_products as digital_products_facade
    from agent_company_core import digital_products_review as review_facade
    from agent_company_core import digital_products_review_gate
    from agent_company_core import digital_products_review_private
    from agent_company_core import digital_products_review_revision

    assert (
        review_facade.digital_products_private_review_artifacts
        is digital_products_review_private.digital_products_private_review_artifacts
    )
    assert (
        review_facade.write_digital_products_local_private_review_packet
        is digital_products_review_private.write_digital_products_local_private_review_packet
    )
    assert (
        review_facade.write_digital_products_local_private_review_decision
        is digital_products_review_private.write_digital_products_local_private_review_decision
    )

    assert review_facade.digital_products_revision_pass_files is digital_products_review_revision.digital_products_revision_pass_files
    assert (
        review_facade.write_digital_products_local_revision_pass
        is digital_products_review_revision.write_digital_products_local_revision_pass
    )
    assert (
        review_facade.write_digital_products_local_revised_completeness
        is digital_products_review_revision.write_digital_products_local_revised_completeness
    )

    assert review_facade.digital_products_gate_decision_options is digital_products_review_gate.digital_products_gate_decision_options
    assert (
        review_facade.write_digital_products_local_gate_decision_packet
        is digital_products_review_gate.write_digital_products_local_gate_decision_packet
    )
    assert (
        review_facade.write_digital_products_local_gate_choice
        is digital_products_review_gate.write_digital_products_local_gate_choice
    )
    assert (
        digital_products_facade.write_digital_products_local_gate_choice
        is review_facade.write_digital_products_local_gate_choice
    )
def test_digital_products_private_review_facade_reexports_private_review_modules():
    from agent_company_core import digital_products_review_private
    from agent_company_core import digital_products_review_private_decision
    from agent_company_core import digital_products_review_private_decision_content
    from agent_company_core import digital_products_review_private_packet
    from agent_company_core import digital_products_review_private_packet_content

    assert (
        digital_products_review_private.digital_products_private_review_artifacts
        is digital_products_review_private_packet_content.digital_products_private_review_artifacts
    )
    assert (
        digital_products_review_private.digital_products_private_review_questions
        is digital_products_review_private_packet_content.digital_products_private_review_questions
    )
    assert (
        digital_products_review_private.digital_products_private_review_decision_options
        is digital_products_review_private_packet_content.digital_products_private_review_decision_options
    )
    assert (
        digital_products_review_private_packet.digital_products_private_review_artifacts
        is digital_products_review_private_packet_content.digital_products_private_review_artifacts
    )
    assert (
        digital_products_review_private_packet.digital_products_private_review_questions
        is digital_products_review_private_packet_content.digital_products_private_review_questions
    )
    assert (
        digital_products_review_private_packet.digital_products_private_review_decision_options
        is digital_products_review_private_packet_content.digital_products_private_review_decision_options
    )
    assert (
        digital_products_review_private.write_digital_products_local_private_review_packet
        is digital_products_review_private_packet.write_digital_products_local_private_review_packet
    )
    assert (
        digital_products_review_private.digital_products_private_review_answers
        is digital_products_review_private_decision_content.digital_products_private_review_answers
    )
    assert (
        digital_products_review_private.digital_products_private_review_revision_items
        is digital_products_review_private_decision_content.digital_products_private_review_revision_items
    )
    assert (
        digital_products_review_private_decision.digital_products_private_review_answers
        is digital_products_review_private_decision_content.digital_products_private_review_answers
    )
    assert (
        digital_products_review_private_decision.digital_products_private_review_revision_items
        is digital_products_review_private_decision_content.digital_products_private_review_revision_items
    )
    assert (
        digital_products_review_private.write_digital_products_local_private_review_decision
        is digital_products_review_private_decision.write_digital_products_local_private_review_decision
    )
def test_digital_products_review_revision_facade_reexports_revision_modules():
    from agent_company_core import digital_products_review_revised_completeness
    from agent_company_core import digital_products_review_revision
    from agent_company_core import digital_products_review_revision_pass
    from agent_company_core import digital_products_review_revision_pass_content

    assert (
        digital_products_review_revision.digital_products_revision_pass_files
        is digital_products_review_revision_pass_content.digital_products_revision_pass_files
    )
    assert (
        digital_products_review_revision_pass.digital_products_revision_pass_files
        is digital_products_review_revision_pass_content.digital_products_revision_pass_files
    )
    assert (
        digital_products_review_revision.write_digital_products_local_revision_pass
        is digital_products_review_revision_pass.write_digital_products_local_revision_pass
    )
    assert (
        digital_products_review_revision.digital_products_revised_completeness_checks
        is digital_products_review_revised_completeness.digital_products_revised_completeness_checks
    )
    assert (
        digital_products_review_revision.write_digital_products_local_revised_completeness
        is digital_products_review_revised_completeness.write_digital_products_local_revised_completeness
    )

def test_digital_products_review_gate_facade_reexports_gate_modules():
    from agent_company_core import digital_products_review_gate
    from agent_company_core import digital_products_review_gate_choice
    from agent_company_core import digital_products_review_gate_decision

    assert (
        digital_products_review_gate.digital_products_gate_decision_options
        is digital_products_review_gate_decision.digital_products_gate_decision_options
    )
    assert (
        digital_products_review_gate.write_digital_products_local_gate_decision_packet
        is digital_products_review_gate_decision.write_digital_products_local_gate_decision_packet
    )
    assert (
        digital_products_review_gate.digital_products_gate_choice_followup_items
        is digital_products_review_gate_choice.digital_products_gate_choice_followup_items
    )
    assert (
        digital_products_review_gate.write_digital_products_local_gate_choice
        is digital_products_review_gate_choice.write_digital_products_local_gate_choice
    )


def test_digital_products_private_review_decision_content_counts():
    from agent_company_core import digital_products_review_private_decision_content

    assert len(digital_products_review_private_decision_content.digital_products_private_review_answers()) == 8
    assert len(digital_products_review_private_decision_content.digital_products_private_review_revision_items()) == 6


def test_digital_products_revision_pass_content_counts():
    from agent_company_core import digital_products_review_revision_pass_content

    files = digital_products_review_revision_pass_content.digital_products_revision_pass_files()
    assert len(files) == 6
    assert {item["filename"] for item in files} >= {"README.md", "launch-checklist.md", "private-review-scorecard.md"}

def test_digital_products_private_review_packet_content_counts():
    from agent_company_core import digital_products_review_private_packet_content

    artifacts = digital_products_review_private_packet_content.digital_products_private_review_artifacts()
    questions = digital_products_review_private_packet_content.digital_products_private_review_questions()
    options = digital_products_review_private_packet_content.digital_products_private_review_decision_options()

    assert len(artifacts) == 10
    assert len(questions) == 8
    assert len(options) == 4
    assert artifacts[-1]["artifact_id"] == "chain-integrity"
    assert questions[-1]["question_id"] == "kill-or-continue"
    assert {item["decision_id"] for item in options} == {
        "continue-local",
        "request-browser-gate",
        "request-legal-payment-gate",
        "pause-candidate",
    }

