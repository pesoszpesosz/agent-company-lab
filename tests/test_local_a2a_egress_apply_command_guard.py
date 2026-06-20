import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_local_a2a_egress_apply_command_guard.py"
VALIDATION = ROOT / "reports" / "local-a2a-egress-apply-command-guard-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "local-a2a-egress-apply-command-guard-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "local-a2a-egress-apply-command-guard-v1.schema.json"


class LocalA2AEgressApplyCommandGuardTest(unittest.TestCase):
    def test_guard_rejects_local_a2a_apply_commands_without_real_signed_decision(self) -> None:
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
        self.assertGreaterEqual(validation["fixture_count"], 38)
        self.assertEqual(validation["accepted_count"], validation["expected_accepted_count"])
        self.assertEqual(validation["rejected_count"], validation["expected_rejected_count"])
        self.assertEqual(validation["fixture_expectation_mismatch_count"], 0)
        self.assertFalse(validation["apply_command_allowed"])
        self.assertFalse(validation["apply_allowed"])
        self.assertFalse(validation["gateway_registration_allowed"])
        self.assertFalse(validation["gateway_start_allowed"])
        self.assertFalse(validation["live_egress_allowed"])
        self.assertFalse(validation["agent_message_send_allowed"])
        self.assertEqual(validation["agent_messages_sent"], 0)
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertEqual(validation["apply_commands_written"], 0)
        self.assertEqual(validation["apply_commands_executed"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["browser_sessions_started"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["command_type"]["enum"][0], "deny_noop")
        self.assertEqual(schema["properties"]["target_route_id"]["const"], "local_agent_to_agent_report_only")
        self.assertEqual(schema["properties"]["target_egress_type"]["const"], "agent_to_agent")
        self.assertEqual(schema["properties"]["agent_message_send_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        accepted = [item for item in report["results"] if item["result"]["accepted_for_guard_only"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            self.assertEqual(item["result"]["target_route_id"], "local_agent_to_agent_report_only")
            self.assertFalse(item["result"]["apply_command_allowed"])
            self.assertFalse(item["result"]["agent_message_send_allowed"])
            self.assertEqual(item["result"]["agent_messages_sent"], 0)
            self.assertFalse(item["result"]["worker_start_allowed"])

        self.assertEqual(
            report["next_action"],
            "Keep local A2A egress blocked until a real signed operator local A2A egress decision and exact command preview exist; no agent message send, service-request mutation, worker start, or live egress is permitted by this guard.",
        )


if __name__ == "__main__":
    unittest.main()
