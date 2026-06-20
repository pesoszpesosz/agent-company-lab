import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_local_a2a_egress_apply_preflight_blocker.py"
VALIDATION = ROOT / "reports" / "local-a2a-egress-apply-preflight-blocker-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "local-a2a-egress-apply-preflight-blocker-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "local-a2a-egress-apply-preflight-blocker-v1.schema.json"


class LocalA2AEgressApplyPreflightBlockerTest(unittest.TestCase):
    def test_blocker_prevents_local_a2a_apply_until_real_signed_decision_and_apply_contract_exist(self) -> None:
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
        self.assertEqual(validation["apply_preflight_status"], "blocked_no_real_signed_decision")
        self.assertEqual(validation["blocker_reason"], "no_real_signed_operator_local_a2a_egress_decision_artifact")
        self.assertFalse(validation["real_signed_decision_present"])
        self.assertTrue(validation["apply_command_contract_present"])
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
        self.assertEqual(schema["properties"]["target_route_id"]["const"], "local_agent_to_agent_report_only")
        self.assertEqual(schema["properties"]["target_egress_type"]["const"], "agent_to_agent")
        self.assertEqual(schema["properties"]["apply_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["agent_message_send_allowed"]["const"], False)

        checks = {item["check_id"]: item for item in report["checks"]}
        for required in [
            "gateway_docket_validation_passes",
            "signed_decision_intake_validation_passes",
            "local_a2a_signed_decision_guard_passes_for_target_route",
            "agent_egress_event_ledger_validation_passes",
            "identity_envelope_validation_passes",
            "real_signed_decision_absent",
            "local_a2a_apply_command_contract_missing_without_apply",
        ]:
            self.assertIn(required, checks)
            self.assertTrue(checks[required]["passed"])

        self.assertEqual(
            report["next_action"],
            "Provide a real signed operator local A2A egress-route decision artifact, then build a local A2A apply-command contract before any gateway registration, agent message send, service-request mutation, worker start, or live egress can be considered.",
        )


if __name__ == "__main__":
    unittest.main()
