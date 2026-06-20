import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_mcp_tool_registry_gate.py"
VALIDATION = ROOT / "reports" / "mcp-tool-registry-gate-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "mcp-tool-registry-gate-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "mcp-tool-registry-gate-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "mcp-tool-registry-gate-v1-fixtures"


class McpToolRegistryGateValidatorTest(unittest.TestCase):
    def test_validator_accepts_only_local_report_fixture_and_rejects_tool_risk(self) -> None:
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
        self.assertGreaterEqual(validation["expected_rejected_count"], 18)
        self.assertEqual(validation["rejected_count"], validation["expected_rejected_count"])
        self.assertEqual(validation["mcp_servers_started"], 0)
        self.assertEqual(validation["mcp_servers_installed"], 0)
        self.assertEqual(validation["mcp_servers_enabled"], 0)
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["credentials_created"])
        self.assertFalse(validation["public_actions"])
        self.assertFalse(validation["wallet_actions"])
        self.assertFalse(validation["payment_actions"])
        self.assertFalse(validation["external_side_effects"])
        self.assertTrue(FIXTURE_DIR.exists())
        self.assertGreaterEqual(len(list(FIXTURE_DIR.glob("*.json"))), 19)
        self.assertEqual(schema["properties"]["default_status"]["enum"][0], "disabled")
        self.assertEqual(report["positive_fixture"]["expected_result"], "pass_local_report_only_registry_entry")


if __name__ == "__main__":
    unittest.main()
