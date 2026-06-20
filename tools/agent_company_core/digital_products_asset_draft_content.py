"""Reusable local asset draft content for digital products."""

from __future__ import annotations


def digital_products_positioning_answers() -> list[dict[str, str]]:
    return [
        {
            "field_id": "buyer",
            "answer": "Solo AI builder preparing a small product launch without a launch manager, launch checklist, or agency support.",
        },
        {
            "field_id": "current-mess",
            "answer": "Launch work is scattered across notes, screenshots, copy drafts, QA reminders, and follow-up ideas.",
        },
        {
            "field_id": "trigger",
            "answer": "The builder is close enough to launch that missed screenshots, broken links, unclear positioning, or no review loop would cost momentum.",
        },
        {
            "field_id": "promise",
            "answer": "Organize the launch into one practical checklist pack that reduces missed steps and makes review easier, without promising revenue.",
        },
        {
            "field_id": "proof-needed",
            "answer": "A filled example, a screenshot shot list, a QA pass table, and a post-launch review template should make the pack feel immediately usable.",
        },
        {
            "field_id": "included-assets",
            "answer": "Positioning template, launch checklist, screenshot shot list, QA pass, post-launch review, and boundary README.",
        },
        {
            "field_id": "excluded-scope",
            "answer": "No marketplace listing, pricing advice, payment setup, launch agency service, traffic guarantee, or revenue claim.",
        },
        {
            "field_id": "setup-time",
            "answer": "The first positioning pass should take under thirty minutes for a focused builder with a known product.",
        },
        {
            "field_id": "support-risk",
            "answer": "The README must clarify that the pack is a local planning aid, not legal, tax, payment, or marketplace guidance.",
        },
        {
            "field_id": "validation-gate",
            "answer": "Publishing, selling, pricing, seller account setup, payment setup, and live marketplace claims require browser/legal/payment gates first.",
        },
    ]


def digital_products_launch_checklist_rows() -> list[dict[str, str]]:
    return [
        {
            "phase": "pre-launch",
            "task": "Fill the positioning template and mark any claims that need evidence.",
            "evidence": "Completed positioning answers.",
            "status": "draftable_locally",
        },
        {
            "phase": "pre-launch",
            "task": "List screenshots needed for the product page or announcement.",
            "evidence": "Screenshot shot list.",
            "status": "draftable_locally",
        },
        {
            "phase": "pre-launch",
            "task": "Run a QA pass on links, copy, onboarding steps, and release notes.",
            "evidence": "QA pass table.",
            "status": "draftable_locally",
        },
        {
            "phase": "pre-launch",
            "task": "Write a boundary README that avoids revenue claims and live validation claims.",
            "evidence": "Boundary README.",
            "status": "draftable_locally",
        },
        {
            "phase": "gated",
            "task": "Compare live marketplace demand, saturation, and buyer language.",
            "evidence": "Requires approved browser read-only service request.",
            "status": "blocked_by_gate",
        },
        {
            "phase": "gated",
            "task": "Review seller terms, payment setup, refunds, tax, and KYC obligations.",
            "evidence": "Requires legal/KYC/tax/payment approval.",
            "status": "blocked_by_gate",
        },
        {
            "phase": "gated",
            "task": "Create or update any public listing or product page.",
            "evidence": "Requires public-action approval.",
            "status": "blocked_by_gate",
        },
        {
            "phase": "gated",
            "task": "Connect payouts, accept agreements, or configure payment settings.",
            "evidence": "Requires account/payment approval.",
            "status": "blocked_by_gate",
        },
        {
            "phase": "post-launch",
            "task": "After a future approved launch, review traffic, replies, conversion signals, support load, and next iteration.",
            "evidence": "Post-launch review template.",
            "status": "future_only_after_approval",
        },
    ]


def digital_products_asset_boundary_notes() -> list[str]:
    return [
        "This is a local draft artifact only; it is not a marketplace listing or public product page.",
        "No marketplace browsing, seller account setup, pricing, payment, payout, or legal/tax review has been performed.",
        "No revenue, demand, conversion, or buyer-count claim is made by this local draft.",
        "Live validation requires the parked browser/legal/payment/public-action gates to be explicitly approved first.",
    ]

__all__ = [
    "digital_products_asset_boundary_notes",
    "digital_products_launch_checklist_rows",
    "digital_products_positioning_answers",
]
