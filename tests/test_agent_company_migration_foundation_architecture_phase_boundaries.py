import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_agent_company_migration_foundation_architecture_facade_reexports_phase_modules() -> None:
    from agent_company_core import agent_company_migration_foundation_architecture as facade
    from agent_company_core import agent_company_migration_infrastructure_radar
    from agent_company_core import agent_company_migration_department_architecture
    from agent_company_core import agent_company_migration_department_schema

    assert (
        facade.write_agent_company_infrastructure_radar
        is agent_company_migration_infrastructure_radar.write_agent_company_infrastructure_radar
    )
    assert (
        facade.write_agent_company_department_architecture_packet
        is agent_company_migration_department_architecture.write_agent_company_department_architecture_packet
    )
    assert (
        facade.write_agent_company_department_schema_plan
        is agent_company_migration_department_schema.write_agent_company_department_schema_plan
    )

def test_agent_company_infrastructure_radar_content_model_counts_and_gates() -> None:
    from agent_company_core.agent_company_migration_infrastructure_radar_content import (
        build_agent_company_infrastructure_radar_model,
    )

    model = build_agent_company_infrastructure_radar_model()

    assert model["infrastructure_radar_count"] == 1
    assert model["primary_source_count"] == 5
    assert model["candidate_count"] == 5
    assert model["architecture_mapping_count"] == 7
    assert model["recommended_spine_count"] == 4
    assert model["cashflow_lane_mapping_count"] == 8
    assert model["approval_gate_count"] == 6
    assert model["primary_sources"][0]["source_id"] == "langgraph_github"
    assert model["candidates"][0]["candidate_id"] == "temporal_durable_spine"
    assert model["architecture_mappings"][0]["layer"] == "CEO"
    assert "Temporal-style durable service request lifecycle for every path and worker action." in model["recommended_spine"]
    assert model["cashflow_lane_mappings"][0]["lane"] == "paid_code_bounties"
    assert "real_money_trade_or_spend" in model["approval_gates"]

def test_agent_company_department_architecture_packet_content_model_counts_and_defaults() -> None:
    from agent_company_core.agent_company_migration_department_architecture_content import (
        build_agent_company_department_architecture_packet_model,
    )

    model = build_agent_company_department_architecture_packet_model()

    assert model["department_architecture_packet_count"] == 1
    assert model["department_count"] == 7
    assert model["table_blueprint_count"] == 10
    assert model["service_request_type_count"] == 12
    assert model["thread_template_count"] == 8
    assert model["worker_pool_interface_count"] == 7
    assert model["approval_gate_count"] == 6
    assert model["departments"][0]["department_id"] == "ceo_office"
    assert model["departments"][-1]["department_id"] == "compliance_and_approvals"
    assert model["table_blueprints"][0]["table"] == "agent_threads"
    assert "request_real_money_action" in model["service_request_types"]
    assert model["worker_pool_interfaces"][-1]["pool_id"] == "observability_pool"
    assert "public_submission_or_marketplace_post" in model["approval_gates"]
    assert model["runtime_boundary"] == {
        "browser_sessions_started": 0,
        "account_actions": False,
        "wallet_actions": False,
        "payment_actions": False,
        "public_actions": False,
        "security_testing_actions": False,
        "real_money_actions": False,
        "service_requests_updated": 0,
        "service_requests_assigned": 0,
        "worker_starts": 0,
        "api_calls": False,
        "external_side_effects": False,
    }


def test_agent_company_department_architecture_packet_markdown_lines_cover_packet_sections() -> None:
    from agent_company_core.agent_company_migration_department_architecture_content import (
        build_agent_company_department_architecture_packet_model,
        build_agent_company_department_architecture_packet_markdown_lines,
    )

    model = build_agent_company_department_architecture_packet_model(["custom_gate"])
    lines = build_agent_company_department_architecture_packet_markdown_lines(
        model=model,
        generated_utc="2026-06-19T20:05:00Z",
        json_output_path=Path("packet.json"),
        validation_path=Path("validation.json"),
    )

    assert lines[:3] == [
        "# Agent Company Department Architecture Packet",
        "",
        "Generated UTC: 2026-06-19T20:05:00Z",
    ]
    assert "| `platform_engineering` | `platform_manager` | Schemas, orchestration, worker pools, evidence integrity, observability. | Temporal, OpenAI Agents SDK |" in lines
    assert "- `approval_gates`: Durable gate records for login, wallet, payment, public action, security testing, and personal data." in lines
    assert "- `request_security_scope_review`" in lines
    assert "- `custom_gate`" in lines
    assert lines[-2] == "Materialize a schema plan for these tables and request types next, without starting workers or taking external actions."

