import json
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from agent_company_core.premium_customer_intake_router import route_premium_customer_input  # noqa: E402


def test_premium_customer_router_preserves_raw_and_routes_youtube_material(tmp_path: Path) -> None:
    raw = tmp_path / "source.md"
    raw.write_text(
        "Useful YouTube material: https://youtu.be/example123\n"
        "Please send this to the YouTube lane for script and thumbnail extraction.\n"
        "RAW_SENTINEL_AT_END " * 80,
        encoding="utf-8",
    )

    result = route_premium_customer_input(
        None,
        Namespace(
            input_path=str(raw),
            text=None,
            text_file=None,
            input_id="customer-input-youtube-material-test",
            title=None,
            owner_agent_id=None,
            received_utc="2026-06-20T00:00:00Z",
            dropbox_dir=str(tmp_path / "dropbox"),
            routes_dir=str(tmp_path / "routes"),
            ledger_json=str(tmp_path / "ledger.json"),
            ledger_md=str(tmp_path / "ledger.md"),
            update_feed_json=str(tmp_path / "feed.json"),
            update_feed_md=str(tmp_path / "feed.md"),
            overwrite=True,
            no_db_record=True,
        ),
    )

    packet = json.loads(Path(result["route_json"]).read_text(encoding="utf-8"))
    route_md = Path(result["route_md"]).read_text(encoding="utf-8")
    preserved = Path(result["preserved_raw_path"]).read_text(encoding="utf-8")

    assert "youtube_content_channels" in packet["target_lane_ids"]
    assert packet["input_class"] == "lane_material"
    assert packet["zero_side_effect_boundary"]["external_side_effects"] is False
    assert "RAW_SENTINEL_AT_END" in preserved
    assert route_md.count("RAW_SENTINEL_AT_END") < 3
    assert packet["raw_material_paths"]["preserved_raw_path"] == result["preserved_raw_path"]


def test_premium_customer_router_uses_money_discovery_fallback(tmp_path: Path) -> None:
    result = route_premium_customer_input(
        None,
        Namespace(
            input_path=None,
            text="Found a weird monetization idea but no lane is obvious yet.",
            text_file=None,
            input_id="customer-input-ambiguous-test",
            title=None,
            owner_agent_id=None,
            received_utc="2026-06-20T00:00:00Z",
            dropbox_dir=str(tmp_path / "dropbox"),
            routes_dir=str(tmp_path / "routes"),
            ledger_json=str(tmp_path / "ledger.json"),
            ledger_md=str(tmp_path / "ledger.md"),
            update_feed_json=str(tmp_path / "feed.json"),
            update_feed_md=str(tmp_path / "feed.md"),
            overwrite=True,
            no_db_record=True,
        ),
    )

    packet = json.loads(Path(result["route_json"]).read_text(encoding="utf-8"))

    assert packet["target_lane_ids"] == ["money_source_discovery"]
    assert any(route["status"] == "parked_with_revisit_condition" for route in packet["routes"])
