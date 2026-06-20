import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_public_action_egress_apply_preflight_blocker.py"
VALIDATION = ROOT / "reports" / "public-action-egress-apply-preflight-blocker-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "public-action-egress-apply-preflight-blocker-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "public-action-egress-apply-preflight-blocker-v1.schema.json"


class PublicActionEgressApplyPreflightBlockerTest(unittest.TestCase):
    def test_blocker_prevents_public_action_until_real_decision_body_approval_and_contract_exist(self) -> None:
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
        self.assertEqual(validation["target_route_id"], "public_action_gateway")
        self.assertEqual(validation["target_egress_type"], "public_submission")
        self.assertEqual(validation["apply_preflight_status"], "blocked_no_real_signed_decision")
        self.assertEqual(validation["blocker_reason"], "no_real_signed_operator_public_action_egress_decision_artifact")
        self.assertFalse(validation["real_signed_decision_present"])
        self.assertFalse(validation["exact_action_body_approval_present"])
        self.assertFalse(validation["apply_command_contract_present"])
        self.assertFalse(validation["apply_allowed"])
        self.assertEqual(validation["apply_commands_written"], 0)
        self.assertEqual(validation["apply_commands_executed"], 0)
        self.assertFalse(validation["gateway_registration_allowed"])
        self.assertFalse(validation["gateway_start_allowed"])
        self.assertFalse(validation["live_egress_allowed"])
        self.assertFalse(validation["public_action_allowed"])
        self.assertFalse(validation["public_actions"])
        self.assertEqual(validation["posts_created"], 0)
        self.assertEqual(validation["forms_submitted"], 0)
        self.assertEqual(validation["prs_opened"], 0)
        self.assertEqual(validation["bounty_claims"], 0)
        self.assertEqual(validation["messages_sent"], 0)
        self.assertFalse(validation["browser_session_start_allowed"])
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertFalse(validation["account_actions"])
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["external_side_effects"])

        self.assertEqual(schema["properties"]["target_route_id"]["const"], "public_action_gateway")
        self.assertEqual(schema["properties"]["target_egress_type"]["const"], "public_submission")
        self.assertEqual(schema["properties"]["apply_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["public_action_allowed"]["const"], False)

        checks = {item["check_id"]: item for item in report["checks"]}
        for required in [
            "gateway_docket_validation_passes",
            "signed_decision_intake_validation_passes",
            "public_action_signed_decision_guard_passes_for_target_route",
            "agent_egress_event_ledger_validation_passes",
            "service_worker_chain_integrity_passes_without_start",
            "real_signed_decision_absent",
            "exact_action_body_approval_absent",
            "public_action_apply_command_contract_absent",
        ]:
            self.assertIn(required, checks)
            self.assertTrue(checks[required]["passed"])

        self.assertEqual(
            report["next_action"],
            "Provide a real signed operator public_action_gateway decision artifact, exact action-body approval, and public-action apply-command contract before any post, form submission, PR, bounty claim, message send, browser mutation, account action, service-request mutation, or live egress can be considered.",
        )


if __name__ == "__main__":
    unittest.main()
