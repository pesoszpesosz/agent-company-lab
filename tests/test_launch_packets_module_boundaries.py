import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def test_launch_packets_facade_reexports_packet_modules() -> None:
    from agent_company_core import lane_thread_manifest
    from agent_company_core import launch_packet_files
    from agent_company_core import launch_packets as facade
    from agent_company_core import manager_packets

    assert facade.write_manager_packets is manager_packets.write_manager_packets
    assert facade.write_launch_packets is launch_packet_files.write_launch_packets
    assert facade.write_lane_thread_manifest is lane_thread_manifest.write_lane_thread_manifest
    assert facade.lane_launch_hard_stop is lane_thread_manifest.lane_launch_hard_stop
    assert facade.manager_thread_prompt is lane_thread_manifest.manager_thread_prompt
    assert facade.THREAD_LAUNCH_ORDER is lane_thread_manifest.THREAD_LAUNCH_ORDER
    assert facade.THREAD_HELD_LANES is lane_thread_manifest.THREAD_HELD_LANES

def test_manager_packet_content_builds_lane_packet_sections() -> None:
    from agent_company_core.manager_packets_content import build_manager_packet_lines, manager_packet_read_only_note

    lane = {
        "lane_id": "paid_code_bounties",
        "department": "Revenue",
        "status": "active",
        "agent_types_json": '["researcher", "reviewer"]',
        "examples_json": '["Find scoped bounty"]',
        "promotion_gates_json": '["local evidence first"]',
        "service_workers_required_json": '["browser"]',
        "side_effects_json": '["public submission"]',
        "global_gates_json": '["no account action without approval"]',
    }

    lines = build_manager_packet_lines(
        lane=lane,
        specs=[{
            "spec_id": "spec-1",
            "name": "Source Scan",
            "source_type": "local",
            "cadence": "daily",
            "risk_gate": "approval required",
            "refresh_command": "python scan.py",
            "outputs_json": '["reports/scan.md"]',
        }],
        evidence=[{
            "evidence_id": "ev-1",
            "status": "verified",
            "title": "Proof",
            "source_path": "reports/proof.md",
            "source_url": None,
            "next_action": "continue",
            "ownership_note": "local only",
        }],
        tasks=[{
            "priority": 9,
            "status": "ready",
            "task_id": "task-1",
            "title": "Do one scoped thing",
            "owner_agent_id": "agent-1",
            "lease_owner_agent_id": None,
            "lease_expires_at": None,
            "evidence_required": "artifact",
            "next_action": "write artifact",
        }],
        requests=[{
            "status": "needs_review",
            "service_id": "svc-browser",
            "request_type": "browser",
            "request_id": "req-1",
            "assigned_agent_id": None,
            "risk_gate": "browser approval",
            "requested_action": "open page",
            "artifact_path": "reports/request.md",
            "decision_note": None,
        }],
        outcomes=[{
            "status": "recorded",
            "outcome_type": "lead",
            "outcome_id": "out-1",
            "realized_usd": 0,
            "evidence": "reports/proof.md",
            "next_action": "verify",
        }],
        service_catalog=[{
            "default_status": "needs_review",
            "request_type": "browser",
            "service_id": "svc-browser",
            "owner_role_id": "operator",
            "purpose": "controlled browser work",
        }],
        owner="agent-1",
        recommendation="Keep one active task moving.",
        generated_utc="2026-06-19T00:00:00Z",
        read_only_note=manager_packet_read_only_note("paid_code_bounties"),
    )

    packet = "\n".join(lines)

    assert lines[0] == "# Manager Packet - paid_code_bounties"
    assert "Generated UTC: 2026-06-19T00:00:00Z" in lines
    assert "## Manager Directive" in lines
    assert "Own only the `paid_code_bounties` lane" in packet
    assert "## Service Bureau Catalog" in lines
    assert "`svc-browser`" in packet
    assert "## Forbidden Direct Side Effects" in lines
    assert "public submission" in packet
    assert "## Startup Commands" in lines
    assert "list-source-specs --lane-id paid_code_bounties" in packet
    assert manager_packet_read_only_note("submitted_bounty_payouts").startswith("This lane is read-only")


def test_manager_packets_imports_content_helpers() -> None:
    from agent_company_core import manager_packets
    from agent_company_core.manager_packets_content import build_manager_packet_lines, manager_packet_read_only_note

    assert manager_packets.build_manager_packet_lines is build_manager_packet_lines
    assert manager_packets.manager_packet_read_only_note is manager_packet_read_only_note


def test_submitted_payout_manager_packet_is_read_only_not_claim_instruction() -> None:
    from agent_company_core.manager_packets_content import build_manager_packet_lines, manager_packet_read_only_note

    lane = {
        "lane_id": "submitted_bounty_payouts",
        "department": "Revenue Collection",
        "status": "external_owned_readonly",
        "agent_types_json": '["payout_monitor"]',
        "examples_json": '["RustChain"]',
        "promotion_gates_json": '["owner selection"]',
        "service_workers_required_json": '["wallet_public_address_worker"]',
        "side_effects_json": '["wallet address comment"]',
        "global_gates_json": '["no public action without approval"]',
    }
    lines = build_manager_packet_lines(
        lane=lane,
        specs=[],
        evidence=[],
        tasks=[],
        requests=[],
        outcomes=[],
        service_catalog=[],
        owner="external:parallel-payout-worker",
        recommendation="Read-only visibility only.",
        generated_utc="2026-06-21T00:00:00Z",
        read_only_note=manager_packet_read_only_note("submitted_bounty_payouts"),
    )
    packet = "\n".join(lines)

    assert "Read-only visibility lane for `submitted_bounty_payouts`" in packet
    assert "Do not claim ownership" in packet
    assert "claim the lane only if it is unowned" not in packet
