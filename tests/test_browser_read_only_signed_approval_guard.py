import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_browser_read_only_signed_approval_guard.py"
VALIDATION = ROOT / "reports" / "browser-read-only-signed-approval-guard-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "browser-read-only-signed-approval-guard-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "browser-read-only-signed-approval-guard-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "browser-read-only-signed-approval-guard-v1-fixtures"


class BrowserReadOnlySignedApprovalGuardTest(unittest.TestCase):
    def test_guard_accepts_only_deny_or_preflight_only_browser_approval(self) -> None:
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
        self.assertEqual(validation["accepted_count"], 2)
        self.assertGreaterEqual(validation["rejected_count"], 18)
        self.assertFalse(validation["assignment_allowed"])
        self.assertFalse(validation["browser_session_start_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["approval_rows_written"], 0)
        self.assertEqual(validation["decisions_applied"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_mutated"], 0)
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertFalse(validation["public_actions"])
        self.assertFalse(validation["external_side_effects"])
        self.assertTrue(FIXTURE_DIR.exists())
        self.assertGreaterEqual(len(list(FIXTURE_DIR.glob("*.json"))), 20)
        self.assertEqual(schema["properties"]["decision"]["enum"][0], "deny")
        self.assertEqual(report["positive_authority"]["accepted_scope"], "browser_read_only_assignment_preflight_only")
        self.assertFalse(report["positive_authority"]["browser_session_start_allowed"])
        self.assertEqual(report["source_preflight"]["adapter_contract_gate"], "present_valid_start_blocked")
        self.assertEqual(
            report["source_preflight"]["adapter_contract_validation_path"],
            str(ROOT / "reports" / "browser-worker-adapter-contract-v1-validation-20260618.json"),
        )
        self.assertEqual(
            report["source_preflight"]["adapter_contract_validation"]["contract_verdict"],
            "adapter_contract_valid_start_blocked",
        )
        self.assertFalse(report["source_preflight"]["adapter_contract_validation"]["browser_session_start_allowed"])
        self.assertEqual(validation["adapter_contract_gate"], "present_valid_start_blocked")


if __name__ == "__main__":
    unittest.main()
