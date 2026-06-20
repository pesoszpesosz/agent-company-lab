import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_worker_activation_preflight_chain.py"
VALIDATION = ROOT / "reports" / "worker-activation-preflight-chain-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "worker-activation-preflight-chain-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "worker-activation-preflight-chain-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "worker-activation-preflight-chain-v1-fixtures"


class WorkerActivationPreflightChainValidatorTest(unittest.TestCase):
    def test_validator_composes_identity_egress_and_mcp_gates_without_enabling_workers(self) -> None:
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
        self.assertEqual(validation["worker_pool_id"], "service-worker-local-runtime-adapter-pool")
        self.assertEqual(validation["chain_verdict"], "preflight_passed_registration_blocked")
        self.assertFalse(validation["registration_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertFalse(validation["mcp_tool_call_allowed"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(validation["worker_pools_registered"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["accepted_count"], 1)
        self.assertGreaterEqual(validation["rejected_count"], 8)
        self.assertTrue(FIXTURE_DIR.exists())
        self.assertGreaterEqual(len(list(FIXTURE_DIR.glob("*.json"))), 9)
        self.assertEqual(schema["properties"]["chain_verdict"]["enum"][0], "blocked_missing_validator")
        self.assertEqual(report["composed_validators"]["identity"]["accepted_count"], 1)
        self.assertEqual(report["composed_validators"]["egress"]["accepted_count"], 1)
        self.assertEqual(report["composed_validators"]["mcp_registry"]["accepted_count"], 1)


if __name__ == "__main__":
    unittest.main()
