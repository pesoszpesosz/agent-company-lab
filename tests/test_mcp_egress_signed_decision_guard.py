import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_mcp_egress_signed_decision_guard.py"
VALIDATION = ROOT / "reports" / "mcp-egress-signed-decision-guard-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "mcp-egress-signed-decision-guard-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "mcp-egress-signed-decision-guard-v1.schema.json"


class McpEgressSignedDecisionGuardTest(unittest.TestCase):
    def test_guard_accepts_only_exact_mcp_route_preflight_decisions(self) -> None:
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
        self.assertEqual(validation["target_route_id"], "mcp_tool_gateway")
        self.assertEqual(validation["target_egress_type"], "mcp_tool")
        self.assertGreaterEqual(validation["fixture_count"], 34)
        self.assertEqual(validation["accepted_count"], validation["expected_accepted_count"])
        self.assertEqual(validation["rejected_count"], validation["expected_rejected_count"])
        self.assertEqual(validation["fixture_expectation_mismatch_count"], 0)
        self.assertEqual(validation["gateway_registrations"], 0)
        self.assertEqual(validation["gateway_starts"], 0)
        self.assertEqual(validation["live_egress_events"], 0)
        self.assertEqual(validation["mcp_servers_started"], 0)
        self.assertEqual(validation["mcp_servers_enabled"], 0)
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["credentials_created"])
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["decisions_applied"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["browser_sessions_started"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["route_id"]["const"], "mcp_tool_gateway")
        self.assertEqual(schema["properties"]["egress_type"]["const"], "mcp_tool")
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        self.assertIn("mcp_tool_registry_gate_v1", report["target_route_required_gates"])
        self.assertIn("agent_egress_event_ledger_v1", report["target_route_required_gates"])
        self.assertIn("local_runtime_adapter_pool_identity_envelope_v1", report["target_route_required_gates"])
        accepted = [item for item in report["results"] if item["result"]["accepted_for_apply_preflight"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            self.assertEqual(item["result"]["route_id"], "mcp_tool_gateway")
            self.assertFalse(item["result"]["gateway_start_allowed"])
            self.assertFalse(item["result"]["live_egress_allowed"])
            self.assertFalse(item["result"]["mcp_tool_call_allowed"])
            self.assertEqual(item["result"]["mcp_servers_started"], 0)
            self.assertEqual(item["result"]["mcp_servers_enabled"], 0)

        self.assertEqual(
            report["next_action"],
            "Build MCP egress apply preflight blocker for the accepted mcp_tool_gateway decision before any gateway registration, MCP server enable/start, MCP tool call, credential access, worker start, or live egress.",
        )


if __name__ == "__main__":
    unittest.main()
