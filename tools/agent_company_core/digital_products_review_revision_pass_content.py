"""Reusable revision-pass file content for digital products."""

from __future__ import annotations


def digital_products_revision_pass_files() -> list[dict[str, object]]:
    boundary_line = "Gates: marketplace browsing, seller accounts, legal/tax/KYC review, payout setup, public listing, pricing, publishing, wallets, payments, APIs, and external validation require explicit approval."
    return [
        {
            "file_id": "readme",
            "filename": "README.md",
            "revision_sources": ["tighten-buyer-statement", "propagate-gate-language"],
            "title": "AI Builder Launch Checklist Pack",
            "content_sections": [
                "For solo AI builders who have a small tool, template, or prompt workflow and need a local pre-launch checklist before any marketplace validation.",
                "Use this pack to clarify buyer, promise, files, private-review questions, boundary language, and next local revision.",
                boundary_line,
            ],
        },
        {
            "file_id": "checklist",
            "filename": "launch-checklist.md",
            "revision_sources": ["fill-example-checklist", "complete-placeholder-stubs"],
            "title": "Local Launch Checklist",
            "content_sections": [
                "Define the buyer in one sentence.",
                "Name the promised workflow without revenue, payout, buyer-count, or live-demand claims.",
                "Confirm all six local files are present and internally consistent.",
                "Run a private review before requesting browser, legal, account, or payment gates.",
            ],
        },
        {
            "file_id": "filled-example",
            "filename": "filled-example.md",
            "revision_sources": ["fill-example-checklist"],
            "title": "Filled Example",
            "content_sections": [
                "Example buyer: a solo AI builder packaging a prompt workflow that helps founders draft customer-interview notes.",
                "Example promise: a local checklist and review worksheet for deciding whether the workflow is clear enough to validate externally.",
                "Example safe next action: improve the README and checklist locally, then rerun local completeness before any gate request.",
            ],
        },
        {
            "file_id": "qa-checklist",
            "filename": "qa-checklist.md",
            "revision_sources": ["propagate-gate-language", "rerun-local-completeness"],
            "title": "QA Checklist",
            "content_sections": [
                "Check that every file avoids sales, revenue, payout, buyer-count, and live-demand claims.",
                "Check that all marketplace, account, legal, tax, KYC, payout, publishing, wallet, payment, API, and public-action gates remain explicit.",
                "Check that every previously empty section now has local draft content or a named local-review TODO.",
            ],
        },
        {
            "file_id": "private-listing-draft",
            "filename": "private-listing-draft.md",
            "revision_sources": ["tighten-buyer-statement", "propagate-gate-language"],
            "title": "Private Listing Draft",
            "content_sections": [
                "Private review title: AI Builder Launch Checklist Pack.",
                "Private review summary: a local-only pack for checking whether a small AI-builder asset is coherent before any marketplace or payment work.",
                boundary_line,
            ],
        },
        {
            "file_id": "review-scorecard",
            "filename": "private-review-scorecard.md",
            "revision_sources": ["add-private-review-scorecard", "rerun-local-completeness"],
            "title": "Private Review Scorecard",
            "content_sections": [
                "Usefulness: can the buyer finish one local pre-launch review without extra explanation?",
                "Clarity: are buyer, promise, files, and next action visible in the first pass?",
                "Boundary safety: are browser, marketplace, public listing, account, legal, tax, KYC, payout, wallet, payment, and API gates preserved?",
                "Next revision: record exactly one local fix before any external validation request.",
            ],
        },
    ]

__all__ = ["digital_products_revision_pass_files"]
