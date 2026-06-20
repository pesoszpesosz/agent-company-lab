import sys
from pathlib import Path

ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_durable_adapter_scaffolding_facade_reexports_stage_modules() -> None:
    from agent_company_core import durable_adapter_scaffolding
    from agent_company_core import durable_adapter_scaffolding_artifacts
    from agent_company_core import durable_adapter_scaffolding_packet

    assert (
        durable_adapter_scaffolding.write_durable_adapter_runtime_report_only_scaffolding_packet
        is durable_adapter_scaffolding_packet.write_durable_adapter_runtime_report_only_scaffolding_packet
    )
    assert (
        durable_adapter_scaffolding.scaffolding_artifact_filename
        is durable_adapter_scaffolding_artifacts.scaffolding_artifact_filename
    )
    assert (
        durable_adapter_scaffolding.materialized_scaffolding_artifact_content
        is durable_adapter_scaffolding_artifacts.materialized_scaffolding_artifact_content
    )
    assert (
        durable_adapter_scaffolding.write_durable_adapter_runtime_report_only_scaffolding_artifacts
        is durable_adapter_scaffolding_artifacts.write_durable_adapter_runtime_report_only_scaffolding_artifacts
    )

def test_durable_adapter_scaffolding_artifact_content_builders_are_report_only() -> None:
    import json

    from agent_company_core.durable_adapter_scaffolding_artifact_content import (
        materialized_scaffolding_artifact_content,
        scaffolding_artifact_filename,
    )

    component = {
        "component_id": "Temporal Runtime Adapter: Worker Plan",
        "source_fixture_id": "fixture-temporal-worker",
        "artifact_kind": "report_json",
        "title": "Temporal Worker Plan",
    }

    assert scaffolding_artifact_filename("Temporal Runtime Adapter: Worker Plan", "report_json").endswith(".json")
    assert scaffolding_artifact_filename("Temporal Runtime Adapter: Worker Plan", "report_markdown").endswith(".md")

    json_content = materialized_scaffolding_artifact_content(
        component,
        "2026-06-19T00:00:00Z",
        Path(r"E:\agent-company-lab\reports\packet.json"),
        Path(r"E:\agent-company-lab\reports\chain-validation.json"),
    )
    payload = json.loads(json_content)

    assert payload["component_id"] == "Temporal Runtime Adapter: Worker Plan"
    assert payload["report_only"] is True
    assert payload["executable_code"] is False
    assert payload["runtime_component"] is False
    assert payload["side_effects_performed"] is False
    assert "No Temporal/Inngest imports" in payload["content"]["runtime_boundary"]

    markdown_content = materialized_scaffolding_artifact_content(
        {**component, "artifact_kind": "report_markdown"},
        "2026-06-19T00:00:00Z",
        Path(r"E:\agent-company-lab\reports\packet.json"),
        Path(r"E:\agent-company-lab\reports\chain-validation.json"),
    )

    assert "# Temporal Worker Plan" in markdown_content
    assert "Executable code: `False`" in markdown_content
    assert "Temporal/Inngest imports: `0`" in markdown_content
    assert "Use this component as planning evidence only" in markdown_content

