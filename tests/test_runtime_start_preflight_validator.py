import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_runtime_start_preflight.py"
VALIDATION = ROOT / "reports" / "runtime-start-preflight-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "runtime-start-preflight-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "runtime-start-preflight-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "runtime-start-preflight-v1-fixtures"


class RuntimeStartPreflightValidatorTest(unittest.TestCase):
    def test_validator_accepts_only_dry_run_preview_and_blocks_process_start(self) -> None:
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
        self.assertEqual(validation["runtime_start_verdict"], "dry_run_preview_valid_start_blocked")
        self.assertFalse(validation["runtime_start_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["runtime_processes_started"], 0)
        self.assertEqual(validation["command_previews_executed"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["browser_sessions_started"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(validation["accepted_count"], 1)
        self.assertGreaterEqual(validation["rejected_count"], 10)
        self.assertTrue(FIXTURE_DIR.exists())
        self.assertGreaterEqual(len(list(FIXTURE_DIR.glob("*.json"))), 11)
        self.assertEqual(schema["properties"]["runtime_start_verdict"]["enum"][0], "blocked_missing_activation_chain")
        self.assertEqual(report["activation_chain"]["chain_verdict"], "preflight_passed_registration_blocked")
        self.assertFalse(report["positive_fixture"]["runtime_start_allowed"])


if __name__ == "__main__":
    unittest.main()
