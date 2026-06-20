import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_service_worker_signed_decision_intake_contract.py"
VALIDATION = ROOT / "reports" / "service-worker-signed-decision-intake-contract-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "service-worker-signed-decision-intake-contract-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "service-worker-signed-decision-intake-contract-v1.schema.json"


class ServiceWorkerSignedDecisionIntakeContractTest(unittest.TestCase):
    def test_contract_covers_all_services_and_requests_without_applying_decisions(self) -> None:
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
        self.assertEqual(validation["contract_status"], "report_only_intake_contract_ready")
        self.assertGreaterEqual(validation["service_template_count"], 13)
        self.assertEqual(validation["service_template_count"], validation["service_count"])
        self.assertGreaterEqual(validation["current_request_count"], 14)
        self.assertEqual(validation["current_requests_covered"], validation["current_request_count"])
        self.assertEqual(validation["missing_required_field_count"], 0)
        self.assertEqual(validation["templates_with_exact_scope_required_count"], validation["service_template_count"])
        self.assertEqual(validation["templates_with_attestation_required_count"], validation["service_template_count"])
        self.assertFalse(validation["approval_granted_by_contract"])
        self.assertFalse(validation["decision_authority_granted_by_contract"])
        self.assertFalse(validation["apply_allowed"])
        self.assertEqual(validation["approval_rows_written"], 0)
        self.assertEqual(validation["decisions_applied"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertFalse(validation["browser_sessions_started"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["decision"]["enum"][0], "deny")
        self.assertEqual(report["contract_status"], "report_only_intake_contract_ready")


if __name__ == "__main__":
    unittest.main()
