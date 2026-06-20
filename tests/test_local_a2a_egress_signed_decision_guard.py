import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_local_a2a_egress_signed_decision_guard.py"
VALIDATION = ROOT / "reports" / "local-a2a-egress-signed-decision-guard-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "local-a2a-egress-signed-decision-guard-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "local-a2a-egress-signed-decision-guard-v1.schema.json"


class LocalA2AEgressSignedDecisionGuardTest(unittest.TestCase):
    def test_guard_accepts_only_exact_local_a2a_report_only_preflight_decisions(self) -> None:
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
        self.assertEqual(validation["target_route_id"], "local_agent_to_agent_report_only")
        self.assertEqual(validation["target_egress_type"], "agent_to_agent")
        self.assertGreaterEqual(validation["fixture_count"], 34)
        self.assertEqual(validation["accepted_count"], validation["expected_accepted_count"])
        self.assertEqual(validation["rejected_count"], validation["expected_rejected_count"])
        self.assertEqual(validation["fixture_expectation_mismatch_count"], 0)
        self.assertEqual(validation["gateway_registrations"], 0)
        self.assertEqual(validation["gateway_starts"], 0)
        self.assertEqual(validation["live_egress_events"], 0)
        self.assertEqual(validation["agent_messages_sent"], 0)
        self.assertFalse(validation["agent_message_send_allowed"])
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertEqual(validation["decisions_applied"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["browser_sessions_started"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["route_id"]["const"], "local_agent_to_agent_report_only")
        self.assertEqual(schema["properties"]["egress_type"]["const"], "agent_to_agent")
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        self.assertIn("agent_egress_event_ledger_v1", report["target_route_required_gates"])
        self.assertIn("local_runtime_adapter_pool_identity_envelope_v1", report["target_route_required_gates"])
        accepted = [item for item in report["results"] if item["result"]["accepted_for_apply_preflight"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            self.assertEqual(item["result"]["route_id"], "local_agent_to_agent_report_only")
            self.assertFalse(item["result"]["gateway_start_allowed"])
            self.assertFalse(item["result"]["live_egress_allowed"])
            self.assertFalse(item["result"]["agent_message_send_allowed"])
            self.assertEqual(item["result"]["agent_messages_sent"], 0)

        self.assertEqual(
            report["next_action"],
            "Build local A2A egress apply preflight blocker for the accepted local_agent_to_agent_report_only decision before any gateway registration, agent message send, service-request mutation, worker start, or live egress.",
        )


if __name__ == "__main__":
    unittest.main()
