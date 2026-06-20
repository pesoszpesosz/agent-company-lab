import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_browser_worker_adapter_contract.py"
VALIDATION = ROOT / "reports" / "browser-worker-adapter-contract-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "browser-worker-adapter-contract-v1-20260618.json"
TRACE_METADATA = ROOT / "reports" / "browser-worker-adapter-contract-v1-trace-metadata-20260618.json"
SCHEMA = ROOT / "architecture" / "browser-worker-adapter-contract-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "browser-worker-adapter-contract-v1-fixtures"


class BrowserWorkerAdapterContractTest(unittest.TestCase):
    def test_contract_accepts_playwright_read_only_adapter_and_blocks_runtime_start(self) -> None:
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
        trace_metadata = json.loads(TRACE_METADATA.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

        self.assertTrue(validation["all_checks_passed"])
        self.assertEqual(validation["failure_count"], 0)
        self.assertEqual(validation["accepted_count"], 1)
        self.assertGreaterEqual(validation["rejected_count"], 18)
        self.assertEqual(validation["contract_verdict"], "adapter_contract_valid_start_blocked")
        self.assertFalse(validation["browser_session_start_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertEqual(validation["workers_started"], 0)
        self.assertEqual(validation["mcp_servers_started"], 0)
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
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["adapter_kind"]["enum"][0], "playwright_deterministic")
        self.assertEqual(report["positive_fixture"]["adapter_kind"], "playwright_deterministic")
        self.assertFalse(report["positive_fixture"]["browser_session_start_allowed"])
        self.assertEqual(trace_metadata["trace_id"], "trace-browser-worker-adapter-contract-v1-20260618")
        self.assertFalse(trace_metadata["browser_actions"])
        self.assertFalse(trace_metadata["external_side_effects"])
        self.assertTrue(FIXTURE_DIR.exists())
        self.assertGreaterEqual(len(list(FIXTURE_DIR.glob("*.json"))), 19)


if __name__ == "__main__":
    unittest.main()
