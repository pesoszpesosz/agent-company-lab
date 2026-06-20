from __future__ import annotations

from typing import Any

"""Reusable local demand-memo definitions for digital products."""


def digital_products_memo_candidates() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "ai-builder-launch-checklist-pack",
            "product_shape": "Template pack",
            "buyer": "Solo AI builders and operators preparing small launches.",
            "promise": "Reduce launch setup friction with reusable checklist, positioning, and QA templates.",
            "local_reason": "Matches the lane evidence around reusable digital assets without requiring platform-specific integrations.",
            "needs_live_validation": "Marketplace demand, price bands, saturation, and buyer wording remain behind browser read-only approval.",
        },
        {
            "candidate_id": "agency-client-intake-automation-kit",
            "product_shape": "Plugin/workflow kit",
            "buyer": "Small agencies that need repeatable client onboarding and project intake.",
            "promise": "Turn a messy intake flow into a repeatable prompt, form, and handoff bundle.",
            "local_reason": "Reusable operational assets have a clear time-saved angle and can be drafted locally.",
            "needs_live_validation": "Seller terms, refund obligations, and support expectations remain behind legal/payment review.",
        },
        {
            "candidate_id": "creator-sponsor-tracker-template",
            "product_shape": "Spreadsheet/template bundle",
            "buyer": "Creators tracking sponsors, deliverables, invoices, and renewal follow-ups.",
            "promise": "Give small creators one lightweight operating sheet for sponsor workflow control.",
            "local_reason": "Narrow, low-integration product that can be built and screenshotted locally before any listing.",
            "needs_live_validation": "Public listing, pricing, and platform fit remain gated until marketplace/browser approval.",
        },
    ]


def digital_products_memo_sections() -> list[dict[str, str]]:
    return [
        {
            "section_id": "audience",
            "summary": "Local evidence supports buyers who value reusable templates/plugins that save setup or coordination time.",
        },
        {
            "section_id": "candidate-products",
            "summary": "Three local candidate product shapes are ready for a build brief, but none has live marketplace validation yet.",
        },
        {
            "section_id": "value-promises",
            "summary": "Each candidate should promise time saved, fewer setup mistakes, or clearer handoff rather than broad passive-income language.",
        },
        {
            "section_id": "validation-plan",
            "summary": "Local validation can draft screenshots, contents, support assumptions, and buyer copy before any marketplace browsing.",
        },
        {
            "section_id": "gates",
            "summary": "Marketplace research, seller terms, account setup, payouts, and public listings remain parked behind explicit gates.",
        },
        {
            "section_id": "decision",
            "summary": "Prepare a build brief locally; do not browse marketplaces, list, publish, or configure payment.",
        },
    ]


__all__ = ["digital_products_memo_candidates", "digital_products_memo_sections"]
