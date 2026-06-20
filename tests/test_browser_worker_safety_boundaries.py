import copy
import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from browser_worker_safety_core import (  # noqa: E402
    DEFAULT_FIXTURE,
    DEFAULT_JSON_OUT,
    DEFAULT_MD_OUT,
    DEFAULT_SCHEMA,
    build_result,
    classify,
    load_json,
    validate_case,
)


def test_browser_worker_safety_core_blocks_wallet_actions() -> None:
    fixture = load_json(DEFAULT_FIXTURE)
    safe_case = next(case for case in fixture["cases"] if case["expected_classification"] == "public_read_only")
    wallet_case = next(
        case
        for case in fixture["cases"]
        if case["expected_classification"] == "wallet_or_payment_action"
    )

    assert classify(safe_case)[:3] == (
        "public_read_only",
        "allow_after_approval",
        "browser_read_only_session",
    )
    assert validate_case(safe_case)["failures"] == []

    negative = copy.deepcopy(safe_case)
    negative["action_text"] = "Connect wallet and claim airdrop from the bounty page"
    negative["expected_classification"] = "public_read_only"
    negative_result = validate_case(negative)

    assert "wallet_action" in classify(wallet_case)[3]
    assert any("classification expected public_read_only" in failure for failure in negative_result["failures"])

    result = build_result(
        fixture,
        fixture_path=DEFAULT_FIXTURE,
        schema_path=DEFAULT_SCHEMA,
        json_path=DEFAULT_JSON_OUT,
        markdown_path=DEFAULT_MD_OUT,
    )

    assert result["schema_version"] == "agent_company.browser_worker_safety_validation.v1"
    assert result["fixture_path"] == str(DEFAULT_FIXTURE)
    assert result["schema_path"] == str(DEFAULT_SCHEMA)
    assert result["cases_checked"] == len(fixture["cases"])
    assert result["passed_count"] == len(fixture["cases"])
    assert result["failed_count"] == 0
    assert result["browser_sessions_started"] == 0
    assert result["external_side_effects"] is False
