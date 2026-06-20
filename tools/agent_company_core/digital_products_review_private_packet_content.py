from __future__ import annotations

"""Reusable local private-review packet definitions for digital products."""

from .constants import (
    DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_REPORT,
    DIGITAL_PRODUCTS_LOCAL_ASSET_OUTLINE_REPORT,
    DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_REPORT,
    DIGITAL_PRODUCTS_LOCAL_COMPLETENESS_CHECK_REPORT,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_REPORT,
    DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_REPORT,
    DIGITAL_PRODUCTS_LOCAL_PACKAGE_FILES_REPORT,
    DIGITAL_PRODUCTS_LOCAL_PACKAGING_MANIFEST_REPORT,
    DIGITAL_PRODUCTS_LOCAL_QUALITY_PASS_REPORT,
    SERVICE_WORKER_CHAIN_INTEGRITY_REPORT,
)


def digital_products_private_review_artifacts() -> list[dict[str, str]]:
    return [
        {"artifact_id": "demand-proof", "path": str(DIGITAL_PRODUCTS_LOCAL_DEMAND_PROOF_REPORT), "purpose": "Initial local demand proof and gates."},
        {"artifact_id": "demand-memo", "path": str(DIGITAL_PRODUCTS_LOCAL_DEMAND_MEMO_REPORT), "purpose": "Candidate selection and local memo."},
        {"artifact_id": "build-brief", "path": str(DIGITAL_PRODUCTS_LOCAL_BUILD_BRIEF_REPORT), "purpose": "Selected candidate build brief."},
        {"artifact_id": "asset-outline", "path": str(DIGITAL_PRODUCTS_LOCAL_ASSET_OUTLINE_REPORT), "purpose": "Asset components and first template outline."},
        {"artifact_id": "asset-draft", "path": str(DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_REPORT), "purpose": "Positioning template and launch checklist draft."},
        {"artifact_id": "quality-pass", "path": str(DIGITAL_PRODUCTS_LOCAL_QUALITY_PASS_REPORT), "purpose": "Local quality checks and revision items."},
        {"artifact_id": "packaging-manifest", "path": str(DIGITAL_PRODUCTS_LOCAL_PACKAGING_MANIFEST_REPORT), "purpose": "Six-file package manifest and README structure."},
        {"artifact_id": "package-files", "path": str(DIGITAL_PRODUCTS_LOCAL_PACKAGE_FILES_REPORT), "purpose": "README, screenshot, QA, and review file drafts."},
        {"artifact_id": "completeness-check", "path": str(DIGITAL_PRODUCTS_LOCAL_COMPLETENESS_CHECK_REPORT), "purpose": "Completeness result for private review."},
        {"artifact_id": "chain-integrity", "path": str(SERVICE_WORKER_CHAIN_INTEGRITY_REPORT), "purpose": "Current chain integrity proof for all local layers."},
    ]


def digital_products_private_review_questions() -> list[dict[str, str]]:
    return [
        {"question_id": "buyer-fit", "question": "Is the buyer specific enough for a first private review?"},
        {"question_id": "promise-safety", "question": "Does the promise avoid revenue, buyer-count, payout, or live-demand claims?"},
        {"question_id": "asset-usability", "question": "Could a solo AI builder use the draft without extra explanation?"},
        {"question_id": "file-coverage", "question": "Do the six manifest files cover the promised workflow?"},
        {"question_id": "readme-boundary", "question": "Does the README boundary language clearly stop legal/payment/marketplace misuse?"},
        {"question_id": "gate-clarity", "question": "Are marketplace, public listing, seller account, and payout gates unambiguous?"},
        {"question_id": "private-review-next", "question": "What should be revised locally before any external validation request?"},
        {"question_id": "kill-or-continue", "question": "Should the lane continue locally, request browser/legal gates, or pause this product candidate?"},
    ]


def digital_products_private_review_decision_options() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "continue-local",
            "meaning": "Continue local packaging and refinement without live marketplace validation.",
            "allowed_next_action": "Draft standalone local files and rerun local completeness checks.",
        },
        {
            "decision_id": "request-browser-gate",
            "meaning": "Ask for explicit read-only browser approval to compare live marketplace demand.",
            "allowed_next_action": "Create or update a service-request decision packet; do not browse until approved.",
        },
        {
            "decision_id": "request-legal-payment-gate",
            "meaning": "Ask for explicit legal/KYC/tax/payment review before any seller-term or payout work.",
            "allowed_next_action": "Create or update a service-request decision packet; do not accept terms or configure payouts.",
        },
        {
            "decision_id": "pause-candidate",
            "meaning": "Park this product candidate and return to broader lane discovery.",
            "allowed_next_action": "Record a kill/pause reason and choose another local-only digital product candidate.",
        },
    ]


__all__ = [
    "digital_products_private_review_artifacts",
    "digital_products_private_review_questions",
    "digital_products_private_review_decision_options",
]
