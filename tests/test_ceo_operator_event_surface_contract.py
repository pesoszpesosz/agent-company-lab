import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_ceo_operator_event_surface_contract.py"
VALIDATION = ROOT / "reports" / "ceo-operator-event-surface-contract-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "ceo-operator-event-surface-contract-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "ceo-operator-event-surface-contract-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "ceo-operator-event-surface-contract-v1-fixtures"


class CeoOperatorEventSurfaceContractTest(unittest.TestCase):
    def test_contract_defines_local_operator_events_without_live_transport_or_side_effects(self) -> None:
        result = subprocess.run(
            [sys.executable, str(TOOL)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            timeout=30,
        )

        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
        report = json.loads(REPORT.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

        self.assertTrue(validation["all_checks_passed"])
        self.assertEqual(validation["failure_count"], 0)
        self.assertEqual(validation["contract_status"], "report_only_event_surface_ready")
        self.assertGreaterEqual(validation["event_type_count"], 12)
        self.assertEqual(validation["accepted_count"], validation["event_type_count"])
        self.assertGreaterEqual(validation["rejected_count"], 12)
        self.assertEqual(validation["fixture_expectation_mismatch_count"], 0)
        self.assertEqual(validation["source_wave20_next_build"], "ceo_operator_event_surface_contract_v1")
        self.assertFalse(validation["event_transport_enabled"])
        self.assertFalse(validation["sse_enabled"])
        self.assertFalse(validation["websocket_enabled"])
        self.assertEqual(validation["operator_events_emitted"], 0)
        self.assertEqual(validation["operator_events_persisted"], 0)
        self.assertEqual(validation["tasks_created"], 0)
        self.assertEqual(validation["tasks_updated"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["runtime_starts"], 0)
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["public_actions"])
        self.assertFalse(validation["account_actions"])
        self.assertFalse(validation["wallet_actions"])
        self.assertFalse(validation["payment_actions"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["event_surface_status"]["const"], "report_only_contract")
        self.assertEqual(schema["properties"]["event_transport_enabled"]["const"], False)
        self.assertEqual(schema["properties"]["sse_enabled"]["const"], False)
        self.assertEqual(schema["properties"]["websocket_enabled"]["const"], False)
        self.assertEqual(schema["properties"]["approval_granted_by_event"]["const"], False)
        self.assertTrue(FIXTURE_DIR.exists())

        required_types = {
            "ceo_review_snapshot",
            "manager_status_update",
            "worker_capability_signal",
            "service_request_gate_ping",
            "tool_auth_request_proposed",
            "approval_decision_needed",
            "route_blocker_changed",
            "artifact_evidence_attached",
            "outcome_realization_recorded",
            "trace_replay_pointer",
            "human_operator_note",
            "dispatch_next_action",
        }
        self.assertEqual(set(report["event_type_ids"]), required_types)

        accepted = [item for item in report["results"] if item["result"]["accepted_for_contract_only"]]
        self.assertEqual(len(accepted), len(required_types))
        for item in accepted:
            payload = item["result"]
            self.assertFalse(payload["event_transport_enabled"])
            self.assertFalse(payload["approval_granted_by_event"])
            self.assertFalse(payload["external_side_effects"])

        self.assertEqual(
            report["next_action"],
            "Use this report-only event surface to design local CEO/manager inbox packets; do not enable SSE, WebSockets, browser sessions, worker starts, service-request mutation, model/MCP calls, public actions, or external side effects.",
        )


if __name__ == "__main__":
    unittest.main()
