import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))

from runtime_adapter_harness_core import (  # noqa: E402
    base_packet,
    make_result,
    must_refuse,
    result_file_name,
    synthetic_packets,
    validate_packet,
)


def test_runtime_adapter_packet_core_preserves_local_guard_contract() -> None:
    packet = base_packet(
        "packet-safe-local-research",
        "local_research",
        "Safe local research synthesis",
        "Summarize local context without external actions.",
    )

    assert validate_packet(packet) == []
    assert must_refuse(packet) == (False, "")
    assert packet["external_side_effects_allowed"] is False
    assert packet["real_money_allowed"] is False
    assert packet["public_action_allowed"] is False
    assert packet["metadata"]["api_calls"] is False

    gated = dict(packet)
    gated["required_service_requests"] = ["req-browser-readonly"]
    gated["approval_requirements"] = [{"approval_status": "needs_review"}]
    assert must_refuse(gated) == (True, "required service request is not approved")

    result = make_result("adapter-one", packet, "prepare_local_artifact", "safe local packet")
    payload = result.as_dict()
    assert payload["status"] == "prepared_local_artifact"
    assert payload["external_side_effects"] is False
    assert payload["api_calls"] is False
    assert payload["artifact_plan"] == [packet["expected_outputs"][0]["path"]]
    assert payload["preserved_blocked_actions"] == packet["blocked_actions"]

    packets = synthetic_packets()
    assert [item["packet_id"] for item in packets] == [
        "packet-safe-local-research",
        "packet-browser-readonly-needs-review",
        "packet-real-money-public-action-refusal",
    ]
    assert must_refuse(packets[0]) == (False, "")
    assert must_refuse(packets[1]) == (True, "required service request is not approved")
    assert must_refuse(packets[2]) == (True, "packet type is externally consequential")

    assert result_file_name("Packet: Safe/Local Research!", "Adapter One") == "packet-safe-local-research--adapter-one.json"