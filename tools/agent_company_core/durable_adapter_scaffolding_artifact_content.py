"""Pure content builders for report-only durable adapter scaffolding artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .utils import safe_id_fragment


def scaffolding_artifact_filename(component_id: str, artifact_kind: str) -> str:
    suffix = ".json" if artifact_kind in {"report_json", "validation_json"} else ".md"
    return f"{safe_id_fragment(component_id, 80)}{suffix}"


def materialized_scaffolding_artifact_content(
    component: dict[str, Any],
    generated_utc: str,
    packet_path: Path,
    chain_validation_path: Path,
) -> str:
    component_id = str(component["component_id"])
    artifact_kind = str(component["artifact_kind"])
    title = str(component.get("title") or component_id)
    if artifact_kind in {"report_json", "validation_json"}:
        payload = {
            "schema_version": "temporal_inngest_adapter_runtime_report_only_scaffolding_component.v1",
            "generated_utc": generated_utc,
            "component_id": component_id,
            "source_fixture_id": component.get("source_fixture_id"),
            "artifact_kind": artifact_kind,
            "title": title,
            "report_only": True,
            "executable_code": False,
            "runtime_component": False,
            "runtime_side_effect_component": False,
            "side_effects_performed": False,
            "packet_path": str(packet_path),
            "chain_validation_path": str(chain_validation_path),
            "content": {
                "decision": "local report-only scaffolding",
                "runtime_boundary": "No Temporal/Inngest imports, dependency installs, runtime starts, workflow starts, event emissions, service-request mutations, worker starts, API calls, or external side effects.",
                "next_action": "Use this component as planning evidence only until an explicit runtime implementation approval exists.",
            },
        }
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"
    return "\n".join(
        [
            f"# {title}",
            "",
            f"Generated UTC: {generated_utc}",
            f"Component ID: `{component_id}`",
            f"Source fixture: `{component.get('source_fixture_id')}`",
            f"Artifact kind: `{artifact_kind}`",
            "",
            "## Decision",
            "",
            "This is a local report-only scaffolding artifact. It is planning evidence, not executable Temporal/Inngest adapter code.",
            "",
            "## Boundary",
            "",
            "- Executable code: `False`",
            "- Runtime component: `False`",
            "- Runtime side-effect component: `False`",
            "- Temporal/Inngest imports: `0`",
            "- Dependency installs: `0`",
            "- Runtime starts: `0`",
            "- Workflow starts: `0`",
            "- Event emissions: `0`",
            "- Service request mutations: `0`",
            "- Worker starts: `0`",
            "- API calls: `False`",
            "- External side effects: `False`",
            "",
            "## Source Packet",
            "",
            f"- Packet: `{packet_path}`",
            f"- Chain validation: `{chain_validation_path}`",
            "",
            "## Next Action",
            "",
            "Use this component as planning evidence only until an explicit runtime implementation approval exists.",
            "",
        ]
    )


__all__ = [
    "materialized_scaffolding_artifact_content",
    "scaffolding_artifact_filename",
]
