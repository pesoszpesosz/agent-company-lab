import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_browser_read_only_worker_policy.py"
VALIDATION = ROOT / "reports" / "browser-read-only-worker-policy-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "browser-read-only-worker-policy-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "browser-read-only-worker-policy-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "browser-read-only-worker-policy-v1-fixtures"


class BrowserReadOnlyWorkerPolicyValidatorTest(unittest.TestCase):
    def test_validator_accepts_only_public_read_only_plan_and_blocks_browser_start(self) -> None:
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
        self.assertEqual(validation["policy_verdict"], "public_read_only_plan_valid_start_blocked")
        self.assertFalse(validation["browser_session_start_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_mutated"], 0)
        self.assertFalse(validation["login_actions"])
        self.assertFalse(validation["form_submit_actions"])
        self.assertFalse(validation["account_actions"])
        self.assertFalse(validation["wallet_actions"])
        self.assertFalse(validation["payment_actions"])
        self.assertFalse(validation["public_actions"])
        self.assertFalse(validation["security_testing_actions"])
        self.assertFalse(validation["file_transfer_actions"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(validation["accepted_count"], 1)
        self.assertGreaterEqual(validation["rejected_count"], 16)
        self.assertTrue(FIXTURE_DIR.exists())
        self.assertGreaterEqual(len(list(FIXTURE_DIR.glob("*.json"))), 17)
        self.assertEqual(schema["properties"]["session_mode"]["enum"][0], "public_read_only_no_login")
        self.assertEqual(report["positive_fixture"]["expected_result"], "pass_read_only_plan_start_blocked")
        self.assertFalse(report["positive_fixture"]["browser_session_start_allowed"])


if __name__ == "__main__":
    unittest.main()
