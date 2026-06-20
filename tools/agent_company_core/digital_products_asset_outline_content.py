from __future__ import annotations

"""Reusable local digital-products asset outline definitions."""


def digital_products_asset_outline_components() -> list[dict[str, str]]:
    return [
        {
            "component_id": "positioning-template",
            "title": "AI Builder Launch Positioning Template",
            "purpose": "Clarify buyer, problem, promise, proof, scope, and launch risk before any public page exists.",
        },
        {
            "component_id": "launch-checklist",
            "title": "Launch Checklist Table",
            "purpose": "Track pre-launch, launch-day, and post-launch tasks with owner, status, and evidence columns.",
        },
        {
            "component_id": "screenshot-shotlist",
            "title": "Screenshot Shot List",
            "purpose": "Map the product states that need screenshots to caption, reuse, and missing-asset notes.",
        },
        {
            "component_id": "qa-pass-template",
            "title": "Launch QA Pass",
            "purpose": "Check links, copy, onboarding, pricing consistency, screenshots, and release notes locally.",
        },
        {
            "component_id": "post-launch-review",
            "title": "Post-Launch Review",
            "purpose": "Summarize traffic, replies, conversions, support load, and next iteration after a future approved launch.",
        },
        {
            "component_id": "boundary-readme",
            "title": "Boundary README",
            "purpose": "State that the pack is locally drafted and has no live marketplace validation or payout setup yet.",
        },
    ]


def digital_products_positioning_template_fields() -> list[dict[str, str]]:
    return [
        {"field_id": "buyer", "prompt": "Who is the exact AI builder/operator this launch helps?"},
        {"field_id": "current-mess", "prompt": "What launch-prep mess or risk are they trying to avoid?"},
        {"field_id": "trigger", "prompt": "What moment makes them need this template pack now?"},
        {"field_id": "promise", "prompt": "What practical time-saving or mistake-reducing promise can we make without income claims?"},
        {"field_id": "proof-needed", "prompt": "What local proof, example, screenshot, or checklist evidence would make the promise believable?"},
        {"field_id": "included-assets", "prompt": "Which concrete files/templates are included in this first version?"},
        {"field_id": "excluded-scope", "prompt": "What does the pack deliberately not do?"},
        {"field_id": "setup-time", "prompt": "How long should a buyer need to fill out the first template?"},
        {"field_id": "support-risk", "prompt": "What support questions or misuse risks should the README pre-answer?"},
        {"field_id": "validation-gate", "prompt": "Which live marketplace/legal/payment gate is required before publishing or selling?"},
    ]


def digital_products_sample_positioning_sections() -> list[dict[str, str]]:
    return [
        {
            "section_id": "buyer",
            "sample_text": "Solo AI builder preparing a small product launch without a launch manager or agency.",
        },
        {
            "section_id": "problem",
            "sample_text": "Launch prep lives in scattered notes, and the builder risks missing screenshots, QA checks, or follow-up review.",
        },
        {
            "section_id": "promise",
            "sample_text": "One compact checklist pack to organize positioning, screenshots, QA, and post-launch learning before launch day.",
        },
        {
            "section_id": "included-assets",
            "sample_text": "Positioning template, launch checklist, screenshot shot list, QA pass, post-launch review, and boundary README.",
        },
        {
            "section_id": "boundary",
            "sample_text": "Locally drafted only. No marketplace validation, listing, account setup, payout configuration, or revenue claim has been performed.",
        },
    ]


__all__ = [
    "digital_products_asset_outline_components",
    "digital_products_positioning_template_fields",
    "digital_products_sample_positioning_sections",
]
