from __future__ import annotations

from typing import Any

"""Reusable local demand-proof questions for digital products."""


def digital_products_demand_questions() -> list[dict[str, Any]]:
    return [
        {
            "question_id": "local-template-audience",
            "mode": "local_only",
            "gate_required": None,
            "question": "Which buyer audience can be inferred from the local source spec without browsing?",
            "answer": "Likely buyers are creators, solo operators, small agencies, and AI-tool builders looking for reusable templates/plugins that save setup time.",
        },
        {
            "question_id": "local-product-shape",
            "mode": "local_only",
            "gate_required": None,
            "question": "What first product shape is plausible from local evidence?",
            "answer": "A small template/plugin pack is the safest first shape: narrow scope, reusable deliverable, and easy to describe before any marketplace account or listing work.",
        },
        {
            "question_id": "local-validation-angle",
            "mode": "local_only",
            "gate_required": None,
            "question": "What can be validated locally before marketplace browsing?",
            "answer": "Validate naming, target persona, promised time saved, screenshots needed, support burden, and whether the asset can be built without protected data or platform dependence.",
        },
        {
            "question_id": "local-go-no-go",
            "mode": "local_only",
            "gate_required": None,
            "question": "What is the local go/no-go decision?",
            "answer": "Go for a local demand memo only. No listing, account, pricing, payment, or public action until marketplace and legal/payment gates are approved.",
        },
        {
            "question_id": "live-marketplace-demand",
            "mode": "blocked_by_gate",
            "gate_required": "browser_read_only_session",
            "question": "Read public marketplace/category pages to compare demand signals, saturation, price bands, and buyer language.",
            "answer": None,
        },
        {
            "question_id": "live-terms-and-fees",
            "mode": "blocked_by_gate",
            "gate_required": "legal_kyc_tax_payment",
            "question": "Review seller terms, tax/KYC/payment setup, refund obligations, and platform fees.",
            "answer": None,
        },
        {
            "question_id": "public-listing-action",
            "mode": "blocked_by_gate",
            "gate_required": "public_action_approval",
            "question": "Create, publish, update, or promote a marketplace listing or public product page.",
            "answer": None,
        },
        {
            "question_id": "account-or-payment-setup",
            "mode": "blocked_by_gate",
            "gate_required": "account_payment_approval",
            "question": "Create seller accounts, connect payouts, accept agreements, or configure payment settings.",
            "answer": None,
        },
    ]


__all__ = ["digital_products_demand_questions"]
