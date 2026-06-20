import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_service_worker_approval_authority_coverage.py"
VALIDATION = ROOT / "reports" / "service-worker-approval-authority-coverage-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "service-worker-approval-authority-coverage-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "service-worker-approval-authority-coverage-v1.schema.json"


class ServiceWorkerApprovalAuthorityCoverageTest(unittest.TestCase):
    def test_all_services_and_current_requests_have_non_granting_authority_routes(self) -> None:
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
        self.assertGreaterEqual(validation["service_count"], 13)
        self.assertEqual(validation["service_rows_covered"], validation["service_count"])
        self.assertGreaterEqual(validation["current_request_count"], 14)
        self.assertEqual(validation["current_requests_covered"], validation["current_request_count"])
        self.assertEqual(validation["missing_role_count"], 0)
        self.assertEqual(validation["services_requiring_user_count"], 12)
        self.assertEqual(validation["services_requiring_cro_count"], 12)
        self.assertEqual(validation["gated_default_count"], 3)
        self.assertFalse(validation["approval_granted_by_coverage"])
        self.assertFalse(validation["decision_authority_granted_by_coverage"])
        self.assertFalse(validation["rejection_granted_by_coverage"])
        self.assertEqual(validation["authority_commands_run"], 0)
        self.assertEqual(validation["approval_rows_written"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertFalse(validation["browser_sessions_started"])
        self.assertFalse(validation["api_calls"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["coverage_status"]["enum"][0], "report_only_no_authority_granted")
        self.assertEqual(report["coverage_status"], "report_only_no_authority_granted")


if __name__ == "__main__":
    unittest.main()
