"""Reusable build brief content for local digital products."""

from __future__ import annotations

from typing import Any


def digital_products_build_brief_sections() -> list[dict[str, Any]]:
    return [
        {
            "section_id": "buyer",
            "summary": "Solo AI builders and operators preparing small launches; they need practical launch-control assets rather than broad strategy.",
        },
        {
            "section_id": "problem",
            "summary": "Launch prep spreads across positioning, checklist, screenshots, QA, and follow-up; the first product should reduce missed steps.",
        },
        {
            "section_id": "offer",
            "summary": "A compact AI builder launch checklist pack with templates for positioning, launch QA, screenshot planning, and post-launch review.",
        },
        {
            "section_id": "asset-plan",
            "summary": "Draft the assets locally as markdown/spreadsheet-ready templates before any marketplace, account, listing, or payment action.",
        },
        {
            "section_id": "quality-bar",
            "summary": "The pack must be concrete enough to screenshot and use in one sitting; avoid generic motivation or unverifiable income claims.",
        },
        {
            "section_id": "gates",
            "summary": "Marketplace demand checks, seller terms, public listing, seller account setup, and payout configuration remain gated.",
        },
        {
            "section_id": "next-step",
            "summary": "Create a local asset outline and sample first template; request browser/legal gates only for live demand and seller-term validation.",
        },
    ]


def digital_products_build_brief_deliverables() -> list[dict[str, str]]:
    return [
        {
            "deliverable_id": "positioning-template",
            "format": "markdown",
            "description": "One-page buyer, pain, promise, proof, and scope template for an AI-builder launch.",
        },
        {
            "deliverable_id": "launch-checklist",
            "format": "spreadsheet-ready table",
            "description": "Checklist of pre-launch, launch-day, and post-launch tasks with owner/status columns.",
        },
        {
            "deliverable_id": "screenshot-shotlist",
            "format": "markdown/table",
            "description": "Shot list that maps product states to image needs, captions, and reuse notes.",
        },
        {
            "deliverable_id": "qa-pass-template",
            "format": "markdown/table",
            "description": "Basic QA pass template for links, copy, onboarding, pricing page consistency, and release notes.",
        },
        {
            "deliverable_id": "post-launch-review",
            "format": "markdown",
            "description": "Simple review template for traffic, replies, conversion signals, support load, and next iteration.",
        },
        {
            "deliverable_id": "readme-boundary-note",
            "format": "markdown",
            "description": "Boundary note that avoids revenue promises and says live marketplace validation is not yet performed.",
        },
    ]


def digital_products_build_brief_acceptance_criteria() -> list[str]:
    return [
        "Every asset can be drafted locally without marketplace browsing, seller accounts, protected data, payment setup, or public posting.",
        "The pack names one buyer and one practical job-to-be-done instead of a broad passive-income category.",
        "The first template is specific enough that an AI builder could fill it out in under thirty minutes.",
        "The brief preserves all four live-validation gates from the demand memo.",
        "The next action is a local asset outline, not a listing, account setup, payout setup, public submission, or live sale.",
    ]

__all__ = [
    "digital_products_build_brief_acceptance_criteria",
    "digital_products_build_brief_deliverables",
    "digital_products_build_brief_sections",
]
