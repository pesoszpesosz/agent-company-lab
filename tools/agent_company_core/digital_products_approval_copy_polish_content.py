"""Reusable copy-polish content for digital product approval workflows."""

from __future__ import annotations


def digital_products_copy_polish_files() -> list[dict[str, object]]:
    boundary = "Keep gated: marketplace browsing, seller accounts, legal review, tax/KYC review, payout setup, public listing, publishing, wallets, payments, APIs, and external validation all require explicit approval."
    return [
        {
            "file_id": "readme",
            "filename": "README.md",
            "copy_changes": [
                "Lead with the buyer and local job-to-be-done.",
                "Remove vague launch language and name the no-external-validation boundary.",
            ],
            "polished_copy": [
                "AI Builder Launch Checklist Pack helps a solo AI builder review a small tool, template, or prompt workflow before asking for live validation.",
                "Use it to decide whether the buyer, promise, file set, and private-review notes are clear enough for another local pass.",
                boundary,
            ],
        },
        {
            "file_id": "checklist",
            "filename": "launch-checklist.md",
            "copy_changes": [
                "Turn checklist lines into direct action verbs.",
            ],
            "polished_copy": [
                "Write the buyer in one sentence.",
                "Write the promise without revenue, payout, buyer-count, or live-demand claims.",
                "Confirm the six local files agree with each other.",
                "Stop before any browser, account, legal, payment, or public action unless approval is explicit.",
            ],
        },
        {
            "file_id": "filled-example",
            "filename": "filled-example.md",
            "copy_changes": [
                "Make the sample concrete while keeping it hypothetical.",
                "Clarify the safe next action.",
            ],
            "polished_copy": [
                "Hypothetical buyer: a solo AI builder packaging a prompt workflow for founder interview notes.",
                "Hypothetical promise: a local checklist and scorecard for deciding whether the workflow is coherent enough to request validation later.",
                "Safe next action: polish copy locally, then decide whether to request a separate read-only browser gate.",
            ],
        },
        {
            "file_id": "qa-checklist",
            "filename": "qa-checklist.md",
            "copy_changes": [
                "Group safety checks by claim, file coverage, and gates.",
                "Repeat the key gated actions in plain language.",
            ],
            "polished_copy": [
                "Claim check: no sales, revenue, payout, buyer-count, or live-demand claims.",
                "Coverage check: README, checklist, filled example, QA checklist, private listing draft, and scorecard are present.",
                "Gate check: marketplace, account, legal, tax, KYC, payout, publishing, wallet, payment, API, and public-action gates remain explicit.",
            ],
        },
        {
            "file_id": "private-listing-draft",
            "filename": "private-listing-draft.md",
            "copy_changes": [
                "Make the draft sound like a private review note instead of a public listing.",
            ],
            "polished_copy": [
                "Private review title: AI Builder Launch Checklist Pack.",
                "Private review summary: a local-only package for checking whether a small AI-builder asset is coherent before marketplace, seller, or payment work.",
                boundary,
            ],
        },
        {
            "file_id": "review-scorecard",
            "filename": "private-review-scorecard.md",
            "copy_changes": [
                "Make scoring criteria compact and repeatable.",
            ],
            "polished_copy": [
                "Usefulness: can the buyer complete one local pre-launch review without extra explanation?",
                "Clarity: are buyer, promise, file set, and next action obvious?",
                "Boundary safety: are browser, marketplace, public listing, account, legal, tax, KYC, payout, wallet, payment, and API gates preserved?",
                "Next step: choose one local fix or draft a separate approval-request packet.",
            ],
        },
    ]

__all__ = ["digital_products_copy_polish_files"]
