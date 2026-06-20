import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_browser_read_only_assignment_preflight.py"
VALIDATION = ROOT / "reports" / "browser-read-only-assignment-preflight-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "browser-read-only-assignment-preflight-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "browser-read-only-assignment-preflight-v1.schema.json"


class BrowserReadOnlyAssignmentPreflightValidatorTest(unittest.TestCase):
    def test_preflight_inventories_browser_requests_but_blocks_assignment_without_signed_approval(self) -> None:
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
        self.assertEqual(validation["preflight_verdict"], "candidates_valid_assignment_blocked_no_signed_approval")
        self.assertGreaterEqual(validation["candidate_request_count"], 7)
        self.assertEqual(validation["assignment_allowed_count"], 0)
        self.assertEqual(validation["blocked_no_signed_approval_count"], validation["candidate_request_count"])
        self.assertFalse(validation["operator_signed_approval_present"])
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_mutated"], 0)
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertFalse(validation["public_actions"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["preflight_verdict"]["enum"][0], "blocked_missing_policy_validation")
        self.assertEqual(report["policy_validation"]["policy_verdict"], "public_read_only_plan_valid_start_blocked")
        self.assertEqual(
            report["adapter_contract_validation"]["contract_verdict"],
            "adapter_contract_valid_start_blocked",
        )
        self.assertFalse(report["adapter_contract_validation"]["browser_session_start_allowed"])
        self.assertEqual(report["adapter_contract_validation"]["browser_sessions_started"], 0)
        self.assertEqual(validation["adapter_contract_gate"], "present_valid_start_blocked")


if __name__ == "__main__":
    unittest.main()
