"""Reusable package-file content for local digital products."""

from __future__ import annotations


def digital_products_screenshot_rows() -> list[dict[str, str]]:
    return [
        {
            "shot_id": "homepage-or-product-core",
            "state": "Core product or landing surface",
            "caption": "Show what the builder is launching in one glance.",
            "status": "draft_prompt_only",
        },
        {
            "shot_id": "setup-flow",
            "state": "First-use or setup flow",
            "caption": "Show how a new user reaches value without confusion.",
            "status": "draft_prompt_only",
        },
        {
            "shot_id": "before-after",
            "state": "Before/after or input/output example",
            "caption": "Show the practical difference the product creates.",
            "status": "draft_prompt_only",
        },
        {
            "shot_id": "pricing-or-boundary",
            "state": "Pricing/scope placeholder",
            "caption": "Only draft locally; real pricing and public listing are gated.",
            "status": "blocked_until_public_gate",
        },
        {
            "shot_id": "proof-or-demo",
            "state": "Demo artifact or sample result",
            "caption": "Use local sample proof, not buyer-count or revenue claims.",
            "status": "draft_prompt_only",
        },
        {
            "shot_id": "support-or-faq",
            "state": "Support/FAQ section",
            "caption": "Pre-answer common setup and misuse questions.",
            "status": "draft_prompt_only",
        },
    ]


def digital_products_qa_rows() -> list[dict[str, str]]:
    return [
        {"area": "links", "check": "All internal references point to files present in the local manifest.", "status": "local_check"},
        {"area": "copy", "check": "No revenue, conversion, payout, buyer-count, or live-demand claim is present.", "status": "local_check"},
        {"area": "scope", "check": "README says the pack is a planning aid, not legal/tax/payment/marketplace advice.", "status": "local_check"},
        {"area": "screenshots", "check": "Every promised screenshot has a shot-list row before packaging.", "status": "local_check"},
        {"area": "checklist", "check": "Launch checklist contains owner, status, due, and evidence columns before packaging.", "status": "local_check"},
        {"area": "gates", "check": "Marketplace browsing, seller terms, public listing, and payout setup are visibly gated.", "status": "local_check"},
        {"area": "distribution", "check": "No distribution, listing, upload, price, or payment action has been performed.", "status": "local_check"},
    ]


def digital_products_post_launch_prompts() -> list[dict[str, str]]:
    return [
        {"prompt_id": "traffic", "prompt": "What traffic or attention source was used after an approved launch?"},
        {"prompt_id": "replies", "prompt": "What replies, objections, questions, or support requests appeared?"},
        {"prompt_id": "conversion", "prompt": "What non-sensitive conversion signal can be recorded without exposing private data?"},
        {"prompt_id": "support-load", "prompt": "What support burden did the pack create?"},
        {"prompt_id": "buyer-language", "prompt": "What exact buyer language should shape the next revision?"},
        {"prompt_id": "next-iteration", "prompt": "What should be changed, killed, or validated next?"},
    ]

__all__ = [
    "digital_products_post_launch_prompts",
    "digital_products_qa_rows",
    "digital_products_screenshot_rows",
]
