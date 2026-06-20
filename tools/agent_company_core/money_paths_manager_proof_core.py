from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any

"""Manager proof task packet, promotion preflight, and queue report writers."""

from .constants import (
    MANAGER_PROOF_TASK_PACKETS_JSON,
    MANAGER_PROOF_TASK_PACKETS_REPORT,
    MANAGER_PROOF_TASK_PACKETS_VALIDATION_JSON,
    MANAGER_PROOF_TASK_PACKET_DIR,
    MANAGER_PROOF_TASK_PROMOTION_PREFLIGHT_JSON,
    MANAGER_PROOF_TASK_PROMOTION_PREFLIGHT_REPORT,
    MANAGER_PROOF_TASK_PROMOTION_PREFLIGHT_VALIDATION_JSON,
    MANAGER_PROOF_TASK_PROMOTION_QUEUE_JSON,
    MANAGER_PROOF_TASK_PROMOTION_QUEUE_REPORT,
    MANAGER_PROOF_TASK_PROMOTION_QUEUE_VALIDATION_JSON,
)
from .io import load_json, now_utc
from .paths import REPORTS_DIR, ROOT
from .service_workers import db_scalar
from .utils import safe_id_fragment


def manager_proof_task_template(lane_id: str) -> tuple[str, str]:
    templates = {
        "digital_products_templates_plugins": (
            "Prepare first local marketplace demand proof packet",
            "Use existing local evidence and source specs to draft a no-account marketplace demand proof packet with target product categories, validation questions, and approval gates.",
        ),
        "security_bounty_private_reports": (
            "Prepare first local private-report route proof packet",
            "Use imported local bounty evidence to draft a private-report route proof packet with scope, duplicate-check checklist, and explicit security-testing gates.",
        ),
        "ai_ml_competitions": (
            "Prepare first local AI/ML competition shortlist proof packet",
            "Use local public-prize source specs to draft a competition shortlist proof packet with eligibility, account gates, timeline, and no-submission boundary.",
        ),
        "content_and_social_growth": (
            "Prepare first local read-only social research proof packet",
            "Use local social-growth source specs to draft a read-only research proof packet with candidate topics, reply/follow gates, and no-posting boundary.",
        ),
        "money_source_discovery": (
            "Prepare first local money-source venue registry proof packet",
            "Use local discovery source specs to draft a venue registry proof packet with source-quality criteria, repeatable scan fields, and no-account boundary.",
        ),
        "paid_code_bounties": (
            "Prepare first local paid-code bounty duplicate-check proof packet",
            "Use imported paid-code evidence to draft a duplicate-check proof packet with repo-readiness checks, payout-gate notes, and no-claim boundary.",
        ),
    }
    return templates.get(
        lane_id,
        (
            f"Prepare first local proof packet for {lane_id}",
            "Use existing local source specs and evidence to draft a narrow proof packet without gated external actions.",
        ),
    )

def manager_proof_task_queue_score(lane_id: str, parked_request_count: int) -> tuple[int, str]:
    base_scores = {
        "paid_code_bounties": (96, "Highest immediate cashflow fit; local duplicate-check proof can reduce claim risk without browser or submission."),
        "digital_products_templates_plugins": (90, "Strong product-market path with three parked gates; local demand proof can clarify the later marketplace/legal decisions."),
        "money_source_discovery": (88, "Company-wide discovery lane compounds by improving future source coverage and venue selection."),
        "security_bounty_private_reports": (84, "High potential value, but later steps are heavier because report routes and security testing stay gated."),
        "ai_ml_competitions": (78, "Useful prize research lane, but eligibility and account gates usually delay first proof-to-money."),
        "content_and_social_growth": (74, "Distribution value is real, but proof-to-money is less direct than bounty/product/source discovery lanes."),
    }
    base, rationale = base_scores.get(
        lane_id,
        (70, "Fallback score for a ready manager proof task with no lane-specific weighting."),
    )
    return base + min(parked_request_count, 5), rationale

