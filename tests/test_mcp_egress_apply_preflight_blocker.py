import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_mcp_egress_apply_preflight_blocker.py"
VALIDATION = ROOT / "reports" / "mcp-egress-apply-preflight-blocker-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "mcp-egress-apply-preflight-blocker-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "mcp-egress-apply-preflight-blocker-v1.schema.json"


class McpEgressApplyPreflightBlockerTest(unittest.TestCase):
    def test_blocker_prevents_mcp_apply_until_real_signed_decision_and_apply_guard_exist(self) -> None:
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
        self.assertEqual(validation["apply_preflight_status"], "blocked_no_real_signed_decision")
        self.assertEqual(validation["blocker_reason"], "no_real_signed_operator_mcp_egress_decision_artifact")
        self.assertFalse(validation["real_signed_decision_present"])
        self.assertFalse(validation["apply_allowed"])
        self.assertFalse(validation["gateway_registration_allowed"])
        self.assertFalse(validation["gateway_start_allowed"])
        self.assertFalse(validation["live_egress_allowed"])
        self.assertFalse(validation["mcp_server_enable_allowed"])
        self.assertFalse(validation["mcp_tool_call_allowed"])
        self.assertEqual(validation["mcp_servers_started"], 0)
        self.assertEqual(validation["mcp_servers_enabled"], 0)
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["credentials_created"])
        self.assertFalse(validation["credential_access_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertEqual(validation["apply_commands_written"], 0)
        self.assertEqual(validation["apply_commands_executed"], 0)
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["target_route_id"]["const"], "mcp_tool_gateway")
        self.assertEqual(schema["properties"]["target_egress_type"]["const"], "mcp_tool")
        self.assertEqual(schema["properties"]["apply_allowed"]["const"], False)

        checks = {item["check_id"]: item for item in report["checks"]}
        for required in [
            "gateway_docket_validation_passes",
            "mcp_signed_decision_guard_passes_for_target_route",
            "mcp_registry_gate_validation_passes",
            "agent_egress_event_ledger_validation_passes",
            "identity_envelope_validation_passes",
            "real_signed_decision_absent",
            "mcp_apply_guard_missing_without_apply",
        ]:
            self.assertIn(required, checks)
            self.assertTrue(checks[required]["passed"])

        self.assertEqual(
            report["next_action"],
            "Provide a real signed operator MCP egress-route decision artifact, then build an MCP apply-command guard before any gateway registration, MCP server enable/start, MCP tool call, credential access, worker start, or live egress can be considered.",
        )


if __name__ == "__main__":
    unittest.main()
