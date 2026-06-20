import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_digital_products_approval_facade_reexports_phase_modules():
    from agent_company_core import digital_products as digital_products_facade
    from agent_company_core import digital_products_approval as approval_facade
    from agent_company_core import digital_products_approval_briefing
    from agent_company_core import digital_products_approval_hold
    from agent_company_core import digital_products_approval_polish

    assert approval_facade.digital_products_copy_polish_files is digital_products_approval_polish.digital_products_copy_polish_files
    assert (
        approval_facade.write_digital_products_local_copy_polish
        is digital_products_approval_polish.write_digital_products_local_copy_polish
    )
    assert (
        approval_facade.write_digital_products_local_post_polish_readiness
        is digital_products_approval_polish.write_digital_products_local_post_polish_readiness
    )

    assert (
        approval_facade.digital_products_approval_request_draft_packets
        is digital_products_approval_briefing.digital_products_approval_request_draft_packets
    )
    assert (
        approval_facade.write_digital_products_local_approval_request_drafts
        is digital_products_approval_briefing.write_digital_products_local_approval_request_drafts
    )
    assert (
        approval_facade.write_digital_products_local_operator_approval_brief
        is digital_products_approval_briefing.write_digital_products_local_operator_approval_brief
    )

    assert (
        approval_facade.write_digital_products_local_post_approval_simulation_plan
        is digital_products_approval_hold.write_digital_products_local_post_approval_simulation_plan
    )
    assert (
        approval_facade.write_digital_products_local_gated_hold_register
        is digital_products_approval_hold.write_digital_products_local_gated_hold_register
    )
    assert (
        digital_products_facade.write_digital_products_local_gated_hold_register
        is approval_facade.write_digital_products_local_gated_hold_register
    )
def test_digital_products_approval_hold_facade_reexports_hold_modules():
    from agent_company_core import digital_products_approval_gated_hold
    from agent_company_core import digital_products_approval_hold
    from agent_company_core import digital_products_approval_simulation_plan

    assert (
        digital_products_approval_hold.write_digital_products_local_post_approval_simulation_plan
        is digital_products_approval_simulation_plan.write_digital_products_local_post_approval_simulation_plan
    )
    assert (
        digital_products_approval_hold.write_digital_products_local_gated_hold_register
        is digital_products_approval_gated_hold.write_digital_products_local_gated_hold_register
    )
def test_digital_products_approval_polish_facade_reexports_polish_modules():
    from agent_company_core import digital_products_approval_copy_polish
    from agent_company_core import digital_products_approval_copy_polish_content
    from agent_company_core import digital_products_approval_polish
    from agent_company_core import digital_products_approval_post_polish_readiness

    assert (
        digital_products_approval_polish.digital_products_copy_polish_files
        is digital_products_approval_copy_polish_content.digital_products_copy_polish_files
    )
    assert (
        digital_products_approval_copy_polish.digital_products_copy_polish_files
        is digital_products_approval_copy_polish_content.digital_products_copy_polish_files
    )
    assert (
        digital_products_approval_polish.write_digital_products_local_copy_polish
        is digital_products_approval_copy_polish.write_digital_products_local_copy_polish
    )
    assert (
        digital_products_approval_polish.digital_products_post_polish_readiness_checks
        is digital_products_approval_post_polish_readiness.digital_products_post_polish_readiness_checks
    )
    assert (
        digital_products_approval_polish.write_digital_products_local_post_polish_readiness
        is digital_products_approval_post_polish_readiness.write_digital_products_local_post_polish_readiness
    )

def test_digital_products_approval_briefing_facade_reexports_briefing_modules():
    from agent_company_core import digital_products_approval_briefing
    from agent_company_core import digital_products_approval_operator_brief
    from agent_company_core import digital_products_approval_request_drafts

    assert (
        digital_products_approval_briefing.digital_products_approval_request_draft_packets
        is digital_products_approval_request_drafts.digital_products_approval_request_draft_packets
    )
    assert (
        digital_products_approval_briefing.write_digital_products_local_approval_request_drafts
        is digital_products_approval_request_drafts.write_digital_products_local_approval_request_drafts
    )
    assert (
        digital_products_approval_briefing.write_digital_products_local_operator_approval_brief
        is digital_products_approval_operator_brief.write_digital_products_local_operator_approval_brief
    )


def test_digital_products_copy_polish_content_counts():
    from agent_company_core import digital_products_approval_copy_polish_content

    files = digital_products_approval_copy_polish_content.digital_products_copy_polish_files()
    assert len(files) == 6
    assert {item["filename"] for item in files} >= {"README.md", "launch-checklist.md", "private-review-scorecard.md"}


def test_digital_products_post_approval_simulation_plan_content_is_hold_only():
    from agent_company_core.digital_products_approval_simulation_plan_content import (
        build_digital_products_post_approval_simulation_plan_content,
    )

    content = build_digital_products_post_approval_simulation_plan_content(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path="reports/plan.json",
        validation_path="reports/plan-validation.json",
        source_brief_validation_path="reports/brief-validation.json",
        lane_id="digital_products_templates_plugins",
        plan_task_id="task-plan",
        plan_evidence_id="evidence-plan",
        source_brief_task_id="task-brief",
        source_brief_evidence_id="evidence-brief",
        selected_candidate_id="ai-builder-launch-checklist-pack",
        blocked_questions=[
            {"question_id": "browser", "gate_required": "browser_read_only_session"},
            {"question_id": "legal", "gate_required": "legal_kyc_tax_payment"},
            {"question_id": "pricing", "gate_required": "operator_choice"},
            {"question_id": "publish", "gate_required": "public_action"},
        ],
        requires_explicit_approval_count=2,
    )

    payload = content["payload"]
    markdown = content["markdown"]

    assert content["local_decision"] == "post_approval_simulation_plan_ready_not_executed"
    assert content["recommended_default"] == "hold_until_explicit_user_approval"
    assert content["approval_request_count"] == 0
    assert content["simulation_scenario_count"] == 2
    assert content["simulated_browser_sessions"] == 0
    assert content["simulated_legal_payment_reviews"] == 0
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert payload["schema_version"] == "agent_company.digital_products_local_post_approval_simulation_plan.v1"
    assert payload["blocked_by_gate_count"] == 4
    assert payload["simulation_scenarios"][0]["scenario_id"] == "if-read-only-browser-validation-approved"
    assert payload["simulation_scenarios"][1]["gate_required"] == "legal_kyc_tax_payment"
    assert payload["simulation_scenarios"][0]["execution_status"] == "not_executed"
    assert "Do not treat simulated approval as actual approval." in markdown
    assert "This is a local simulation plan only" in markdown
    assert markdown.endswith("\n")


def test_digital_products_approval_simulation_plan_imports_content_helper():
    from agent_company_core import digital_products_approval_simulation_plan as simulation_plan
    from agent_company_core.digital_products_approval_simulation_plan_content import (
        build_digital_products_post_approval_simulation_plan_content,
    )

    assert (
        simulation_plan.build_digital_products_post_approval_simulation_plan_content
        is build_digital_products_post_approval_simulation_plan_content
    )

def test_digital_products_gated_hold_register_content_is_hold_only():
    from agent_company_core.digital_products_approval_gated_hold_content import (
        build_digital_products_gated_hold_register_content,
    )

    content = build_digital_products_gated_hold_register_content(
        generated_utc="2026-06-19T00:00:00Z",
        json_output_path="reports/hold.json",
        validation_path="reports/hold-validation.json",
        source_plan_validation_path="reports/plan-validation.json",
        lane_id="digital_products_templates_plugins",
        register_task_id="task-hold",
        register_evidence_id="evidence-hold",
        source_plan_task_id="task-plan",
        source_plan_evidence_id="evidence-plan",
        selected_candidate_id="ai-builder-launch-checklist-pack",
        blocked_questions=[
            {"question_id": "live-marketplace-demand", "gate_required": "browser_read_only_session"},
            {"question_id": "live-terms-and-fees", "gate_required": "legal_kyc_tax_payment"},
            {"question_id": "public-listing-action", "gate_required": "public_action_approval"},
            {"question_id": "account-or-payment-setup", "gate_required": "account_payment_approval"},
        ],
        source_simulation_scenario_count=2,
    )

    payload = content["payload"]
    markdown = content["markdown"]

    assert content["local_decision"] == "gated_hold_register_active"
    assert content["recommended_default"] == "hold_until_explicit_user_approval"
    assert content["approval_request_count"] == 0
    assert content["hold_entry_count"] == 4
    assert content["active_hold_count"] == 4
    assert content["explicit_approval_required_count"] == 4
    assert content["runnable_without_approval_count"] == 0
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert payload["schema_version"] == "agent_company.digital_products_local_gated_hold_register.v1"
    assert payload["blocked_by_gate_count"] == 4
    assert payload["hold_entries"][0]["hold_id"] == "hold-live-marketplace-demand"
    assert payload["hold_entries"][1]["gate_required"] == "legal_kyc_tax_payment"
    assert "This is a local hold register only" in markdown
    assert "hold-public-listing-action" in markdown
    assert markdown.endswith("\n")


def test_digital_products_gated_hold_writer_imports_content_helper():
    from agent_company_core import digital_products_approval_gated_hold as gated_hold
    from agent_company_core.digital_products_approval_gated_hold_content import (
        build_digital_products_gated_hold_register_content,
    )

    assert gated_hold.build_digital_products_gated_hold_register_content is build_digital_products_gated_hold_register_content

