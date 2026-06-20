from __future__ import annotations

from typing import Any, Callable

"""CLI parser and dispatch helpers for digital-products commands."""

from agent_company_core.digital_products import (
    write_digital_products_local_demand_proof,
    write_digital_products_local_demand_memo,
    write_digital_products_local_build_brief,
    write_digital_products_local_asset_outline,
    write_digital_products_local_asset_draft,
    write_digital_products_local_quality_pass,
    write_digital_products_local_packaging_manifest,
    write_digital_products_local_package_files,
    write_digital_products_local_completeness_check,
    write_digital_products_local_private_review_packet,
    write_digital_products_local_private_review_decision,
    write_digital_products_local_revision_pass,
    write_digital_products_local_revised_completeness,
    write_digital_products_local_gate_decision_packet,
    write_digital_products_local_gate_choice,
    write_digital_products_local_copy_polish,
    write_digital_products_local_post_polish_readiness,
    write_digital_products_local_approval_request_drafts,
    write_digital_products_local_operator_approval_brief,
    write_digital_products_local_post_approval_simulation_plan,
    write_digital_products_local_gated_hold_register,
)
from agent_company_core.schema import init_db


DIGITAL_PRODUCTS_CLI_COMMANDS = (
    "write-digital-products-local-demand-proof",
    "write-digital-products-local-demand-memo",
    "write-digital-products-local-build-brief",
    "write-digital-products-local-asset-outline",
    "write-digital-products-local-asset-draft",
    "write-digital-products-local-quality-pass",
    "write-digital-products-local-packaging-manifest",
    "write-digital-products-local-package-files",
    "write-digital-products-local-completeness-check",
    "write-digital-products-local-private-review-packet",
    "write-digital-products-local-private-review-decision",
    "write-digital-products-local-revision-pass",
    "write-digital-products-local-revised-completeness",
    "write-digital-products-local-gate-decision-packet",
    "write-digital-products-local-gate-choice",
    "write-digital-products-local-copy-polish",
    "write-digital-products-local-post-polish-readiness",
    "write-digital-products-local-approval-request-drafts",
    "write-digital-products-local-operator-approval-brief",
    "write-digital-products-local-post-approval-simulation-plan",
    "write-digital-products-local-gated-hold-register",
)


def add_digital_products_commands(sub: Any) -> None:
    digital_products_local_demand_proof = sub.add_parser("write-digital-products-local-demand-proof")
    digital_products_local_demand_proof.add_argument("--path")
    digital_products_local_demand_proof.add_argument("--json-path")
    digital_products_local_demand_proof.add_argument("--validation-path")
    digital_products_local_demand_memo = sub.add_parser("write-digital-products-local-demand-memo")
    digital_products_local_demand_memo.add_argument("--path")
    digital_products_local_demand_memo.add_argument("--json-path")
    digital_products_local_demand_memo.add_argument("--validation-path")
    digital_products_local_build_brief = sub.add_parser("write-digital-products-local-build-brief")
    digital_products_local_build_brief.add_argument("--path")
    digital_products_local_build_brief.add_argument("--json-path")
    digital_products_local_build_brief.add_argument("--validation-path")
    digital_products_local_asset_outline = sub.add_parser("write-digital-products-local-asset-outline")
    digital_products_local_asset_outline.add_argument("--path")
    digital_products_local_asset_outline.add_argument("--json-path")
    digital_products_local_asset_outline.add_argument("--validation-path")
    digital_products_local_asset_draft = sub.add_parser("write-digital-products-local-asset-draft")
    digital_products_local_asset_draft.add_argument("--path")
    digital_products_local_asset_draft.add_argument("--json-path")
    digital_products_local_asset_draft.add_argument("--validation-path")
    digital_products_local_quality_pass = sub.add_parser("write-digital-products-local-quality-pass")
    digital_products_local_quality_pass.add_argument("--path")
    digital_products_local_quality_pass.add_argument("--json-path")
    digital_products_local_quality_pass.add_argument("--validation-path")
    digital_products_local_packaging_manifest = sub.add_parser("write-digital-products-local-packaging-manifest")
    digital_products_local_packaging_manifest.add_argument("--path")
    digital_products_local_packaging_manifest.add_argument("--json-path")
    digital_products_local_packaging_manifest.add_argument("--validation-path")
    digital_products_local_package_files = sub.add_parser("write-digital-products-local-package-files")
    digital_products_local_package_files.add_argument("--path")
    digital_products_local_package_files.add_argument("--json-path")
    digital_products_local_package_files.add_argument("--validation-path")
    digital_products_local_completeness_check = sub.add_parser("write-digital-products-local-completeness-check")
    digital_products_local_completeness_check.add_argument("--path")
    digital_products_local_completeness_check.add_argument("--json-path")
    digital_products_local_completeness_check.add_argument("--validation-path")
    digital_products_local_private_review_packet = sub.add_parser("write-digital-products-local-private-review-packet")
    digital_products_local_private_review_packet.add_argument("--path")
    digital_products_local_private_review_packet.add_argument("--json-path")
    digital_products_local_private_review_packet.add_argument("--validation-path")
    digital_products_local_private_review_decision = sub.add_parser("write-digital-products-local-private-review-decision")
    digital_products_local_private_review_decision.add_argument("--path")
    digital_products_local_private_review_decision.add_argument("--json-path")
    digital_products_local_private_review_decision.add_argument("--validation-path")
    digital_products_local_revision_pass = sub.add_parser("write-digital-products-local-revision-pass")
    digital_products_local_revision_pass.add_argument("--path")
    digital_products_local_revision_pass.add_argument("--json-path")
    digital_products_local_revision_pass.add_argument("--validation-path")
    digital_products_local_revised_completeness = sub.add_parser("write-digital-products-local-revised-completeness")
    digital_products_local_revised_completeness.add_argument("--path")
    digital_products_local_revised_completeness.add_argument("--json-path")
    digital_products_local_revised_completeness.add_argument("--validation-path")
    digital_products_local_gate_decision_packet = sub.add_parser("write-digital-products-local-gate-decision-packet")
    digital_products_local_gate_decision_packet.add_argument("--path")
    digital_products_local_gate_decision_packet.add_argument("--json-path")
    digital_products_local_gate_decision_packet.add_argument("--validation-path")
    digital_products_local_gate_choice = sub.add_parser("write-digital-products-local-gate-choice")
    digital_products_local_gate_choice.add_argument("--path")
    digital_products_local_gate_choice.add_argument("--json-path")
    digital_products_local_gate_choice.add_argument("--validation-path")
    digital_products_local_copy_polish = sub.add_parser("write-digital-products-local-copy-polish")
    digital_products_local_copy_polish.add_argument("--path")
    digital_products_local_copy_polish.add_argument("--json-path")
    digital_products_local_copy_polish.add_argument("--validation-path")
    digital_products_local_post_polish_readiness = sub.add_parser("write-digital-products-local-post-polish-readiness")
    digital_products_local_post_polish_readiness.add_argument("--path")
    digital_products_local_post_polish_readiness.add_argument("--json-path")
    digital_products_local_post_polish_readiness.add_argument("--validation-path")
    digital_products_local_approval_request_drafts = sub.add_parser("write-digital-products-local-approval-request-drafts")
    digital_products_local_approval_request_drafts.add_argument("--path")
    digital_products_local_approval_request_drafts.add_argument("--json-path")
    digital_products_local_approval_request_drafts.add_argument("--validation-path")
    digital_products_local_operator_approval_brief = sub.add_parser("write-digital-products-local-operator-approval-brief")
    digital_products_local_operator_approval_brief.add_argument("--path")
    digital_products_local_operator_approval_brief.add_argument("--json-path")
    digital_products_local_operator_approval_brief.add_argument("--validation-path")
    digital_products_local_post_approval_simulation_plan = sub.add_parser("write-digital-products-local-post-approval-simulation-plan")
    digital_products_local_post_approval_simulation_plan.add_argument("--path")
    digital_products_local_post_approval_simulation_plan.add_argument("--json-path")
    digital_products_local_post_approval_simulation_plan.add_argument("--validation-path")
    digital_products_local_gated_hold_register = sub.add_parser("write-digital-products-local-gated-hold-register")
    digital_products_local_gated_hold_register.add_argument("--path")
    digital_products_local_gated_hold_register.add_argument("--json-path")
    digital_products_local_gated_hold_register.add_argument("--validation-path")


def digital_products_command_handlers() -> dict[str, Callable[[Any, Any], None]]:
    return {
        "write-digital-products-local-demand-proof": write_digital_products_local_demand_proof,
        "write-digital-products-local-demand-memo": write_digital_products_local_demand_memo,
        "write-digital-products-local-build-brief": write_digital_products_local_build_brief,
        "write-digital-products-local-asset-outline": write_digital_products_local_asset_outline,
        "write-digital-products-local-asset-draft": write_digital_products_local_asset_draft,
        "write-digital-products-local-quality-pass": write_digital_products_local_quality_pass,
        "write-digital-products-local-packaging-manifest": write_digital_products_local_packaging_manifest,
        "write-digital-products-local-package-files": write_digital_products_local_package_files,
        "write-digital-products-local-completeness-check": write_digital_products_local_completeness_check,
        "write-digital-products-local-private-review-packet": write_digital_products_local_private_review_packet,
        "write-digital-products-local-private-review-decision": write_digital_products_local_private_review_decision,
        "write-digital-products-local-revision-pass": write_digital_products_local_revision_pass,
        "write-digital-products-local-revised-completeness": write_digital_products_local_revised_completeness,
        "write-digital-products-local-gate-decision-packet": write_digital_products_local_gate_decision_packet,
        "write-digital-products-local-gate-choice": write_digital_products_local_gate_choice,
        "write-digital-products-local-copy-polish": write_digital_products_local_copy_polish,
        "write-digital-products-local-post-polish-readiness": write_digital_products_local_post_polish_readiness,
        "write-digital-products-local-approval-request-drafts": write_digital_products_local_approval_request_drafts,
        "write-digital-products-local-operator-approval-brief": write_digital_products_local_operator_approval_brief,
        "write-digital-products-local-post-approval-simulation-plan": write_digital_products_local_post_approval_simulation_plan,
        "write-digital-products-local-gated-hold-register": write_digital_products_local_gated_hold_register,
    }


def handle_digital_products_command(conn: Any, args: Any) -> bool:
    handler = digital_products_command_handlers().get(args.cmd)
    if handler is None:
        return False
    init_db(conn)
    handler(conn, args)
    return True


__all__ = [
    "DIGITAL_PRODUCTS_CLI_COMMANDS",
    "add_digital_products_commands",
    "digital_products_command_handlers",
    "handle_digital_products_command",
]
