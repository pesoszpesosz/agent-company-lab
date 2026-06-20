import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_public_action_egress_signed_decision_guard.py"
VALIDATION = ROOT / "reports" / "public-action-egress-signed-decision-guard-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "public-action-egress-signed-decision-guard-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "public-action-egress-signed-decision-guard-v1.schema.json"


class PublicActionEgressSignedDecisionGuardTest(unittest.TestCase):
    def test_guard_accepts_only_report_only_public_action_preflight_decisions(self) -> None:
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
        self.assertGreaterEqual(validation["fixture_count"], 40)
        self.assertEqual(validation["accepted_count"], 2)
        self.assertEqual(validation["rejected_count"], validation["fixture_count"] - 2)
        self.assertEqual(validation["fixture_expectation_mismatch_count"], 0)
        self.assertFalse(validation["apply_allowed"])
        self.assertEqual(validation["decisions_applied"], 0)
        self.assertEqual(validation["approval_rows_written"], 0)
        self.assertFalse(validation["gateway_registration_allowed"])
        self.assertFalse(validation["gateway_start_allowed"])
        self.assertFalse(validation["live_egress_allowed"])
        self.assertFalse(validation["public_action_allowed"])
        self.assertFalse(validation["public_actions"])
        self.assertFalse(validation["browser_session_start_allowed"])
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertFalse(validation["account_actions"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["external_side_effects"])

        self.assertEqual(schema["properties"]["decision"]["enum"][0], "deny")
        self.assertEqual(schema["properties"]["route_id"]["const"], "public_action_gateway")
        self.assertEqual(schema["properties"]["egress_type"]["const"], "public_submission")
        self.assertEqual(schema["properties"]["public_action_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        required = set(report["target_route_required_gates"])
        self.assertEqual(
            required,
            {
                "public_action_execution_gate",
                "reputation_review_worker",
                "agent_egress_event_ledger_v1",
                "exact_action_body_approval",
            },
        )

        accepted = [item for item in report["results"] if item["result"]["accepted_for_apply_preflight"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            result_payload = item["result"]
            self.assertFalse(result_payload["public_action_allowed"])
            self.assertFalse(result_payload["public_actions"])
            self.assertFalse(result_payload["browser_session_start_allowed"])
            self.assertEqual(result_payload["browser_sessions_started"], 0)
            self.assertFalse(result_payload["account_actions"])

        self.assertEqual(
            report["next_action"],
            "Build public_action_gateway apply preflight blocker before any post, form submission, PR, bounty claim, message send, browser mutation, account action, service-request mutation, or live egress.",
        )


if __name__ == "__main__":
    unittest.main()
