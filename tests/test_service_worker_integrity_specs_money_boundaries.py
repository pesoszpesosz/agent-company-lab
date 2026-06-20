import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def ids(specs: list[dict[str, object]]) -> list[str]:
    return [str(spec["id"]) for spec in specs]


def test_digital_product_integrity_specs_are_grouped_by_workflow_phase() -> None:
    from agent_company_core.service_worker_integrity_specs_digital_products import digital_product_integrity_specs
    from agent_company_core.service_worker_integrity_specs_digital_products_approval import (
        digital_product_approval_integrity_specs,
    )
    from agent_company_core.service_worker_integrity_specs_digital_products_assets import (
        digital_product_asset_integrity_specs,
    )
    from agent_company_core.service_worker_integrity_specs_digital_products_demand import (
        digital_product_demand_integrity_specs,
    )
    from agent_company_core.service_worker_integrity_specs_digital_products_review import (
        digital_product_review_integrity_specs,
    )

    demand_specs = digital_product_demand_integrity_specs()
    asset_specs = digital_product_asset_integrity_specs()
    review_specs = digital_product_review_integrity_specs()
    approval_specs = digital_product_approval_integrity_specs()

    assert digital_product_integrity_specs() == [*demand_specs, *asset_specs, *review_specs, *approval_specs]
    assert ids(demand_specs) == [
        "digital_products_local_demand_proof",
        "digital_products_local_demand_memo",
        "digital_products_local_build_brief",
    ]
    assert ids(asset_specs)[0] == "digital_products_local_asset_outline"
    assert ids(asset_specs)[-1] == "digital_products_local_completeness_check"
    assert ids(review_specs)[0] == "digital_products_local_private_review_packet"
    assert ids(review_specs)[-1] == "digital_products_local_post_polish_readiness"
    assert ids(approval_specs) == [
        "digital_products_local_approval_request_drafts",
        "digital_products_local_operator_approval_brief",
        "digital_products_local_post_approval_simulation_plan",
        "digital_products_local_gated_hold_register",
    ]


def test_money_lane_integrity_specs_are_grouped_by_business_domain() -> None:
    from agent_company_core.service_worker_integrity_specs_money import money_lane_integrity_specs
    from agent_company_core.service_worker_integrity_specs_money_paths import money_path_integrity_specs
    from agent_company_core.service_worker_integrity_specs_paid_code import paid_code_integrity_specs
    from agent_company_core.service_worker_integrity_specs_digital_products import digital_product_integrity_specs

    money_path_specs = money_path_integrity_specs()
    paid_code_specs = paid_code_integrity_specs()
    digital_product_specs = digital_product_integrity_specs()
    combined = [*money_path_specs, *paid_code_specs, *digital_product_specs]

    assert money_lane_integrity_specs() == combined
    assert ids(money_path_specs)[0] == "company_expansion_gap_map"
    assert ids(money_path_specs)[-1] == "first_ranked_manager_proof"
    assert ids(paid_code_specs) == [
        "paid_code_duplicate_check_worksheet",
        "paid_code_local_worksheet_answers",
        "paid_code_browser_refresh_decision_packet",
    ]
    assert ids(digital_product_specs)[0] == "digital_products_local_demand_proof"
    assert ids(digital_product_specs)[-1] == "digital_products_local_gated_hold_register"

def test_digital_product_review_integrity_specs_split_into_review_phases() -> None:
    from agent_company_core.service_worker_integrity_specs_digital_products_review import (
        digital_product_review_integrity_specs,
    )
    from agent_company_core.service_worker_integrity_specs_digital_products_review_gate import (
        digital_product_review_gate_integrity_specs,
    )
    from agent_company_core.service_worker_integrity_specs_digital_products_review_polish import (
        digital_product_review_polish_integrity_specs,
    )
    from agent_company_core.service_worker_integrity_specs_digital_products_review_private import (
        digital_product_review_private_integrity_specs,
    )
    from agent_company_core.service_worker_integrity_specs_digital_products_review_revision import (
        digital_product_review_revision_integrity_specs,
    )

    private_specs = digital_product_review_private_integrity_specs()
    revision_specs = digital_product_review_revision_integrity_specs()
    gate_specs = digital_product_review_gate_integrity_specs()
    polish_specs = digital_product_review_polish_integrity_specs()

    assert ids(private_specs) == [
        "digital_products_local_private_review_packet",
        "digital_products_local_private_review_decision",
    ]
    assert ids(revision_specs) == [
        "digital_products_local_revision_pass",
        "digital_products_local_revised_completeness",
    ]
    assert ids(gate_specs) == [
        "digital_products_local_gate_decision_packet",
        "digital_products_local_gate_choice",
    ]
    assert ids(polish_specs) == [
        "digital_products_local_copy_polish",
        "digital_products_local_post_polish_readiness",
    ]
    assert digital_product_review_integrity_specs() == [*private_specs, *revision_specs, *gate_specs, *polish_specs]
    assert private_specs[0]["expected"]["review_artifact_count"] == 10
    assert revision_specs[-1]["expected"]["passed_check_count"] == 8
    assert gate_specs[0]["expected"]["recommended_option_id"] == "continue-local"
    assert polish_specs[-1]["expected"]["recommended_next_option_id"] == "draft-future-approval-packets"
