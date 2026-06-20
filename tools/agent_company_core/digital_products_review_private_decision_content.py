"""Reusable private review decision content for digital products."""

from __future__ import annotations


def digital_products_private_review_answers() -> list[dict[str, str]]:
    return [
        {
            "question_id": "buyer-fit",
            "answer": "The first private-review buyer is specific enough: a solo AI builder packaging a small productized asset before any marketplace validation.",
            "decision_effect": "keep_candidate",
        },
        {
            "question_id": "promise-safety",
            "answer": "The promise avoids revenue, buyer-count, payout, and live-demand claims; keep all copy framed as a local launch checklist pack.",
            "decision_effect": "keep_boundary_language",
        },
        {
            "question_id": "asset-usability",
            "answer": "The draft is usable, but it needs one filled example and a clearer first-run order before external review would be worth requesting.",
            "decision_effect": "revise_locally",
        },
        {
            "question_id": "file-coverage",
            "answer": "The six-file manifest covers the workflow, while the two placeholder stubs should remain explicit until local revision fills them.",
            "decision_effect": "revise_locally",
        },
        {
            "question_id": "readme-boundary",
            "answer": "The README boundary language is clear enough for private review and should be repeated in the QA checklist and listing draft.",
            "decision_effect": "propagate_boundaries",
        },
        {
            "question_id": "gate-clarity",
            "answer": "Marketplace, public listing, seller account, and payout gates are unambiguous and remain blocked without explicit approval.",
            "decision_effect": "preserve_gates",
        },
        {
            "question_id": "private-review-next",
            "answer": "Revise local packaging before requesting browser or legal/payment gates: fill examples, tighten copy, and rerun completeness.",
            "decision_effect": "create_revision_queue",
        },
        {
            "question_id": "kill-or-continue",
            "answer": "Continue locally. The candidate has enough local coherence to justify one refinement pass, but not enough live proof to publish or sell.",
            "decision_effect": "continue_local",
        },
    ]


def digital_products_private_review_revision_items() -> list[dict[str, str]]:
    return [
        {
            "revision_id": "fill-example-checklist",
            "artifact_target": "checklist",
            "action": "Add one filled sample checklist for a hypothetical solo AI-builder product launch.",
            "reason": "Improves asset usability without claiming live demand or outcomes.",
        },
        {
            "revision_id": "tighten-buyer-statement",
            "artifact_target": "readme",
            "action": "Make the first paragraph name the buyer, job-to-be-done, and local-only boundary in plain language.",
            "reason": "Keeps the first private review focused and avoids broad product claims.",
        },
        {
            "revision_id": "propagate-gate-language",
            "artifact_target": "qa-checklist",
            "action": "Repeat the marketplace, account, legal, tax, KYC, payout, and publishing gates in the QA checklist.",
            "reason": "Prevents the package from being mistaken for approval to validate or sell externally.",
        },
        {
            "revision_id": "complete-placeholder-stubs",
            "artifact_target": "package-files",
            "action": "Replace the two placeholder stubs with local draft content or explicit local-review TODOs.",
            "reason": "Raises completeness before any gate request is considered.",
        },
        {
            "revision_id": "add-private-review-scorecard",
            "artifact_target": "review-notes",
            "action": "Add a scorecard for usefulness, clarity, boundary safety, and next local revision.",
            "reason": "Makes the private review repeatable without external submission.",
        },
        {
            "revision_id": "rerun-local-completeness",
            "artifact_target": "validation",
            "action": "Rerun local package completeness after revisions and compare against this decision packet.",
            "reason": "Maintains the trace from packet decision to updated package proof.",
        },
    ]

__all__ = [
    "digital_products_private_review_answers",
    "digital_products_private_review_revision_items",
]
