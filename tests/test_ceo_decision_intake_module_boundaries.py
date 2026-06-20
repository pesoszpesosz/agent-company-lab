import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def test_ceo_decision_intake_gate_facade_reexports_gate_modules():
    from agent_company_core import ceo_blocker_triage
    from agent_company_core import ceo_decision_intake_gate
    from agent_company_core import ceo_gate_blocker_board

    assert ceo_decision_intake_gate.write_ceo_gate_blocker_board is ceo_gate_blocker_board.write_ceo_gate_blocker_board
    assert ceo_decision_intake_gate.write_ceo_blocker_triage is ceo_blocker_triage.write_ceo_blocker_triage


def test_ceo_decision_intake_facade_reexports_phase_modules():
    from agent_company_core import ceo_decision_intake as intake_facade
    from agent_company_core import ceo_decision_intake_drafts
    from agent_company_core import ceo_decision_intake_gate
    from agent_company_core import ceo_decision_intake_guard
    from agent_company_core import ceo_decisions

    assert intake_facade.write_ceo_gate_blocker_board is ceo_decision_intake_gate.write_ceo_gate_blocker_board
    assert intake_facade.write_ceo_blocker_triage is ceo_decision_intake_gate.write_ceo_blocker_triage
    assert (
        intake_facade.write_ceo_decision_packet_drafts
        is ceo_decision_intake_drafts.write_ceo_decision_packet_drafts
    )
    assert (
        intake_facade.write_ceo_decision_intake_guard
        is ceo_decision_intake_guard.write_ceo_decision_intake_guard
    )
    assert (
        intake_facade.write_ceo_decision_intake_negative_fixtures
        is ceo_decision_intake_guard.write_ceo_decision_intake_negative_fixtures
    )
    assert ceo_decisions.write_ceo_decision_intake_negative_fixtures is intake_facade.write_ceo_decision_intake_negative_fixtures
def test_ceo_decision_intake_guard_facade_reexports_guard_modules():
    from agent_company_core import ceo_decision_intake_guard
    from agent_company_core import ceo_decision_intake_guard_core
    from agent_company_core import ceo_decision_intake_negative_fixtures

    assert (
        ceo_decision_intake_guard.write_ceo_decision_intake_guard
        is ceo_decision_intake_guard_core.write_ceo_decision_intake_guard
    )
    assert (
        ceo_decision_intake_guard.write_ceo_decision_intake_negative_fixtures
        is ceo_decision_intake_negative_fixtures.write_ceo_decision_intake_negative_fixtures
    )

def test_ceo_decision_intake_negative_fixture_content_builds_rejection_suite():
    from agent_company_core.ceo_decision_intake_negative_fixture_content import (
        build_ceo_decision_intake_negative_fixture_content,
    )

    content = build_ceo_decision_intake_negative_fixture_content(
        known_packet_ids=["packet-1"],
        known_option_ids=["option-1"],
    )

    assert content["negative_fixture_count"] == 6
    assert content["expected_rejection_count"] == 6
    assert content["accepted_fixture_count"] == 0
    assert content["covered_rule_ids"] == [
        "reject_forbidden_action_conflict",
        "reject_implicit_or_contextual_approval",
        "reject_missing_packet_id",
        "reject_no_expiration_or_review",
        "reject_unbounded_scope",
        "reject_unknown_option",
    ]
    assert content["negative_fixtures"][0]["fixture_id"] == "missing-packet-id"
    assert content["negative_fixtures"][0]["submitted_intake"]["selected_option_id"] == "option-1"
    assert content["negative_fixtures"][1]["submitted_intake"]["decision_packet_id"] == "packet-1"
    assert all(fixture["expected_accepted"] is False for fixture in content["negative_fixtures"])



def test_ceo_blocker_triage_content_batches_cover_all_blockers_without_approval():
    from agent_company_core.ceo_blocker_triage_content import build_ceo_blocker_triage_content

    blocker_items = [
        {"blocker_id": "dp-catalog", "lane_id": "digital_products_templates_plugins", "risk_gate": "catalog_required_approval_no_external_action"},
        {"blocker_id": "dp-browser", "lane_id": "digital_products_templates_plugins", "risk_gate": "browser_read_only_session"},
        {"blocker_id": "security-scope", "lane_id": "security_bounty_private_reports", "risk_gate": "scope_review"},
        {"blocker_id": "paid-code", "lane_id": "paid_code_bounties", "risk_gate": "browser_read_only_session"},
        {"blocker_id": "ai-ml", "lane_id": "ai_ml_competitions", "risk_gate": "browser_read_only_session"},
        {"blocker_id": "platform-api", "lane_id": "platform_engineering", "risk_gate": "model_api_cost"},
        {"blocker_id": "source-discovery", "lane_id": "money_source_discovery", "risk_gate": "browser_read_only_session"},
        {"blocker_id": "social-browser", "lane_id": "content_and_social_growth", "risk_gate": "browser_read_only_session"},
    ]

    content = build_ceo_blocker_triage_content(blocker_items)

    assert content["triage_batch_count"] == 5
    assert content["high_leverage_batch_count"] == 3
    assert content["covered_blocker_count"] == len(blocker_items)
    assert content["missing_blocker_ids"] == []
    assert content["approval_request_count"] == 0
    assert content["runnable_without_approval_count"] == 0
    assert content["local_decision"] == "ceo_blocker_triage_ready_for_human_review"
    assert content["recommended_default"] == "hold_all_gated_work_until_explicit_approval"
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert content["triage_batches"][0]["batch_id"] == "batch-digital-products-marketplace-validation"
    assert "leaving every gate held" in content["summary"]
    assert "does not authorize any work" in content["next_action"]


def test_ceo_gate_blocker_board_content_combines_review_requests_and_holds():
    from agent_company_core.ceo_gate_blocker_board_content import build_ceo_gate_blocker_board_content

    service_request_rows = [
        {
            "request_id": "req-review-1",
            "request_type": "browser_review",
            "lane_id": "money_source_discovery",
            "status": "needs_review",
            "risk_gate": "browser_read_only_session",
            "requested_action": "refresh public page",
            "assigned_agent_id": None,
            "updated_at": "2026-06-19T00:00:00Z",
        },
        {
            "request_id": "req-complete-1",
            "request_type": "local_report",
            "lane_id": "platform_engineering",
            "status": "complete",
            "risk_gate": None,
            "requested_action": "write report",
            "assigned_agent_id": "agent",
            "updated_at": "2026-06-18T00:00:00Z",
        },
    ]
    hold_entries = [
        {
            "hold_id": "hold-1",
            "gate_required": "account_payment_approval",
            "status": "active_hold",
            "resume_command_candidate": "resume paid catalog",
            "resume_trigger": "explicit approval",
            "source_question_id": "q1",
        }
    ]

    content = build_ceo_gate_blocker_board_content(
        service_request_rows=service_request_rows,
        service_request_status_counts={"needs_review": 1, "complete": 1},
        hold_entries=hold_entries,
        register_lane_id="digital_products_templates_plugins",
    )

    assert content["local_decision"] == "ceo_gate_blocker_board_current"
    assert content["recommended_default"] == "hold_all_gated_work_until_explicit_approval"
    assert content["service_request_total_count"] == 2
    assert content["service_request_needs_review_count"] == 1
    assert content["service_request_complete_count"] == 1
    assert content["active_hold_count"] == 1
    assert content["active_blocker_count"] == 2
    assert content["active_blocker_lane_ids"] == ["digital_products_templates_plugins", "money_source_discovery"]
    assert content["runnable_without_approval_count"] == 0
    assert content["approval_request_count"] == 0
    assert [item["blocker_id"] for item in content["blocker_items"]] == ["req-review-1", "hold-1"]
    assert content["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "without approving or executing" in content["summary"]

def test_ceo_decision_intake_guard_content_builds_payload_and_markdown():
    from agent_company_core.ceo_decision_intake_guard_content import build_ceo_decision_intake_guard_content

    content = build_ceo_decision_intake_guard_content(
        generated_utc="2026-06-19T22:30:00Z",
        json_output_path="reports/intake-guard.json",
        validation_path="reports/intake-guard.validation.json",
        lane_id="platform_engineering",
        guard_task_id="task-guard",
        guard_evidence_id="evidence-guard",
        source_drafts_task_id="task-drafts",
        source_drafts_evidence_id="evidence-drafts",
        source_drafts_validation_path="reports/drafts.validation.json",
        packet_drafts=[
            {
                "packet_id": "packet-1",
                "decision_options": [
                    {"option_id": "approve-readonly"},
                    {"option_id": "hold"},
                ],
            },
            {
                "packet_id": "packet-2",
                "decision_options": [
                    {"option_id": "approve-readonly"},
                    {"option_id": "reject"},
                ],
            },
        ],
        source_packet_draft_count=2,
        source_decision_option_count=4,
    )

    assert content["required_field_count"] == 8
    assert content["invalid_decision_rule_count"] == 6
    assert content["accepted_decision_count"] == 0
    assert content["approval_request_count"] == 0
    assert content["runnable_without_approval_count"] == 0
    assert content["known_packet_ids"] == ["packet-1", "packet-2"]
    assert content["known_option_ids"] == ["approve-readonly", "hold", "reject"]
    assert content["required_fields"] == [
        "decision_packet_id",
        "selected_option_id",
        "approved_blocker_ids",
        "allowed_action_scope",
        "forbidden_actions_acknowledged",
        "expiration_or_review_time",
        "approver_identity",
        "operator_confirmation_text",
    ]
    assert content["example_empty_intake"]["accepted"] is False
    assert content["payload"]["schema_version"] == "agent_company.ceo_decision_intake_guard.v1"
    assert content["payload"]["source_drafts_validation_path"] == "reports/drafts.validation.json"
    assert content["payload"]["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "# CEO Decision Intake Guard" in content["markdown"]
    assert "`reject_missing_packet_id`" in content["markdown"]
    assert "accepts no decisions" in content["markdown"]

def test_ceo_decision_packet_drafts_content_builds_payload_and_markdown():
    from agent_company_core.ceo_decision_intake_drafts_content import build_ceo_decision_packet_drafts_content

    content = build_ceo_decision_packet_drafts_content(
        generated_utc="2026-06-20T00:15:00Z",
        json_output_path="reports/packet-drafts.json",
        validation_path="reports/packet-drafts.validation.json",
        source_triage_validation_path="reports/triage.validation.json",
        lane_id="platform_engineering",
        draft_task_id="task-drafts",
        draft_evidence_id="evidence-drafts",
        source_triage_task_id="task-triage",
        source_triage_evidence_id="evidence-triage",
        triage_batches=[
            {
                "batch_id": "marketplace-validation",
                "priority": 1,
                "lane_focus": "digital_products_templates_plugins",
                "blocker_ids": ["blocker-a", "blocker-b"],
                "decision_needed": "Approve readonly marketplace validation?",
                "why_it_matters": "It unlocks a local product proof path.",
                "leverage": "high",
            },
            {
                "batch_id": "later-review",
                "priority": 5,
                "lane_focus": "paid_code_bounties",
                "blocker_ids": ["blocker-c"],
                "decision_needed": "Review later?",
                "why_it_matters": "It can wait.",
                "leverage": "low",
            },
        ],
        source_active_blocker_count=3,
        source_triage_batch_count=2,
        source_high_leverage_batch_count=1,
    )

    assert content["packet_draft_count"] == 1
    assert content["decision_option_count"] == 3
    assert content["approval_request_count"] == 0
    assert content["runnable_without_approval_count"] == 0
    assert content["packet_drafts"][0]["packet_id"] == "decision-packet-marketplace-validation"
    assert content["packet_drafts"][0]["covered_blocker_ids"] == ["blocker-a", "blocker-b"]
    assert [option["option_id"] for option in content["packet_drafts"][0]["decision_options"]] == [
        "approve_bounded_readonly_scope",
        "keep_held",
        "reject_or_park_batch",
    ]
    assert content["payload"]["schema_version"] == "agent_company.ceo_decision_packet_drafts.v1"
    assert content["payload"]["source_triage_validation_path"] == "reports/triage.validation.json"
    assert content["payload"]["runtime_boundary"]["service_requests_updated"] == 0
    assert content["runtime_boundary"]["external_side_effects"] is False
    assert "# CEO Decision Packet Drafts" in content["markdown"]
    assert "decision-packet-marketplace-validation" in content["markdown"]
    assert "These are local decision-packet drafts only" in content["markdown"]
