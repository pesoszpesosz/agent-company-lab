from __future__ import annotations

"""Reusable local quality-pass definitions for digital-products assets."""


def digital_products_quality_checks() -> list[dict[str, str]]:
    return [
        {
            "check_id": "single-buyer",
            "status": "pass",
            "finding": "The draft names one buyer: a solo AI builder preparing a small product launch.",
        },
        {
            "check_id": "practical-promise",
            "status": "pass",
            "finding": "The promise is operational: reduce missed launch steps and improve review, without income claims.",
        },
        {
            "check_id": "specific-assets",
            "status": "pass",
            "finding": "The draft names concrete included assets: positioning template, checklist, screenshot list, QA pass, review, and README.",
        },
        {
            "check_id": "fillable-template",
            "status": "pass",
            "finding": "The positioning template has ten filled answers and can be reused as a buyer-facing sample.",
        },
        {
            "check_id": "checklist-coverage",
            "status": "pass",
            "finding": "The checklist covers pre-launch, gated validation, and future post-launch review phases.",
        },
        {
            "check_id": "gate-preservation",
            "status": "pass",
            "finding": "Marketplace browsing, terms/payment review, public listing, and account/payment setup remain blocked by gates.",
        },
        {
            "check_id": "no-live-demand-claim",
            "status": "pass",
            "finding": "Boundary notes explicitly say there is no live marketplace validation, buyer-count claim, or revenue claim.",
        },
        {
            "check_id": "next-local-step",
            "status": "pass",
            "finding": "The next action is local packaging/quality work, not listing, pricing, seller setup, or public sale.",
        },
    ]


def digital_products_quality_revision_items() -> list[dict[str, str]]:
    return [
        {
            "revision_id": "add-readme-structure",
            "priority": "high",
            "instruction": "Turn the boundary notes into a README section with scope, non-claims, gates, and how to use the pack.",
        },
        {
            "revision_id": "split-checklist-columns",
            "priority": "medium",
            "instruction": "Add owner, status, due, and evidence columns to the launch checklist before packaging.",
        },
        {
            "revision_id": "add-screenshot-shotlist",
            "priority": "medium",
            "instruction": "Draft the screenshot shot list named in the pack so the asset set matches the promise.",
        },
        {
            "revision_id": "add-qa-pass-table",
            "priority": "medium",
            "instruction": "Draft the QA pass table for links, copy, onboarding, screenshots, release notes, and boundary claims.",
        },
        {
            "revision_id": "add-local-packaging-manifest",
            "priority": "low",
            "instruction": "Create a local manifest of files that would be included if later approved for marketplace packaging.",
        },
    ]


__all__ = ["digital_products_quality_checks", "digital_products_quality_revision_items"]
