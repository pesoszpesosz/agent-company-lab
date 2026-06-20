import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_agent_egress_event_ledger.py"
VALIDATION = ROOT / "reports" / "agent-egress-event-ledger-v1-validation-20260617.json"
REPORT = ROOT / "reports" / "agent-egress-event-ledger-v1-20260617.json"
SCHEMA = ROOT / "architecture" / "agent-egress-event-ledger-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "agent-egress-event-ledger-v1-fixtures"


class AgentEgressEventLedgerValidatorTest(unittest.TestCase):
    def test_validator_allows_only_local_report_preflight_and_rejects_external_egress(self) -> None:
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
        self.assertFalse(validation["gateway_started"])
        self.assertFalse(validation["gateway_installed"])
        self.assertFalse(validation["api_keys_created"])
        self.assertEqual(validation["live_egress_events_recorded"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertFalse(validation["external_side_effects"])
        self.assertTrue(FIXTURE_DIR.exists())
        self.assertGreaterEqual(len(list(FIXTURE_DIR.glob("*.json"))), 19)
        self.assertEqual(schema["properties"]["policy_verdict"]["enum"][0], "deny")
        self.assertEqual(report["positive_fixture"]["expected_result"], "pass_report_only_preflight_event")


if __name__ == "__main__":
    unittest.main()
