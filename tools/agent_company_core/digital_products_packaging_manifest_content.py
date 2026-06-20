from __future__ import annotations

"""Reusable local packaging manifest definitions for digital products."""


def digital_products_package_files() -> list[dict[str, str]]:
    return [
        {
            "path": "README.md",
            "purpose": "Explain scope, usage, boundaries, non-claims, and gated validation requirements.",
            "status": "local_manifest_only",
        },
        {
            "path": "positioning-template.md",
            "purpose": "Reusable AI-builder launch positioning worksheet with sample filled answers.",
            "status": "local_manifest_only",
        },
        {
            "path": "launch-checklist.md",
            "purpose": "Pre-launch, gated-validation, and post-launch checklist with owner/status/evidence columns.",
            "status": "local_manifest_only",
        },
        {
            "path": "screenshot-shotlist.md",
            "purpose": "List required screenshots, captions, reuse notes, and missing-asset flags.",
            "status": "local_manifest_only",
        },
        {
            "path": "qa-pass.md",
            "purpose": "Local QA table for links, copy, onboarding, screenshots, release notes, and boundary claims.",
            "status": "local_manifest_only",
        },
        {
            "path": "post-launch-review.md",
            "purpose": "Future review worksheet for traffic, replies, conversion signals, support load, and next iteration after approved launch.",
            "status": "local_manifest_only",
        },
    ]


def digital_products_readme_sections() -> list[dict[str, str]]:
    return [
        {
            "section_id": "what-this-is",
            "content": "A local draft pack for solo AI builders organizing launch positioning, screenshots, QA, and review.",
        },
        {
            "section_id": "who-it-is-for",
            "content": "Solo AI builders and operators preparing a small product launch without a launch manager or agency.",
        },
        {
            "section_id": "included-files",
            "content": "README, positioning template, launch checklist, screenshot shot list, QA pass, and post-launch review worksheet.",
        },
        {
            "section_id": "how-to-use",
            "content": "Fill the positioning template, complete the checklist, prepare screenshots, run the QA pass, and save review notes.",
        },
        {
            "section_id": "boundaries",
            "content": "This is not legal, tax, payment, marketplace, pricing, launch agency, or revenue guidance.",
        },
        {
            "section_id": "non-claims",
            "content": "No revenue, conversion, buyer-count, demand, payout, or marketplace-validation claim is made.",
        },
        {
            "section_id": "gates-before-public-use",
            "content": "Live marketplace research, seller terms, public listings, accounts, payouts, and payment setup require explicit approval gates.",
        },
    ]


__all__ = ["digital_products_package_files", "digital_products_readme_sections"]
