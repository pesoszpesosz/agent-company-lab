import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_local_runtime_adapter_pool_identity_envelope.py"
VALIDATION = ROOT / "reports" / "local-runtime-adapter-pool-identity-envelope-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "local-runtime-adapter-pool-identity-envelope-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "local-runtime-adapter-pool-identity-envelope-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "local-runtime-adapter-pool-identity-envelope-v1-fixtures"


class LocalRuntimeAdapterIdentityEnvelopeValidatorTest(unittest.TestCase):
    def test_validator_accepts_report_only_candidate_and_rejects_negative_fixtures(self) -> None:
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
        self.assertEqual(validation["expected_accepted_count"], 1)
        self.assertEqual(validation["accepted_count"], 1)
        self.assertGreaterEqual(validation["expected_rejected_count"], 20)
        self.assertEqual(validation["rejected_count"], validation["expected_rejected_count"])
        self.assertFalse(validation["registration_allowed"])
        self.assertFalse(validation["assignment_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(validation["worker_pools_registered"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertFalse(validation["browser_sessions_started"])
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertTrue(FIXTURE_DIR.exists())
        self.assertGreaterEqual(len(list(FIXTURE_DIR.glob("*.json"))), 21)
        self.assertEqual(schema["properties"]["worker_pool_id"]["const"], "service-worker-local-runtime-adapter-pool")
        self.assertEqual(report["positive_fixture"]["expected_result"], "pass_identity_candidate_not_registration_approval")


if __name__ == "__main__":
    unittest.main()
