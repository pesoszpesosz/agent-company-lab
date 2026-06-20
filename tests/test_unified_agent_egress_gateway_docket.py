import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_unified_agent_egress_gateway_docket.py"
VALIDATION = ROOT / "reports" / "unified-agent-egress-gateway-docket-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "unified-agent-egress-gateway-docket-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "unified-agent-egress-gateway-docket-v1.schema.json"


class UnifiedAgentEgressGatewayDocketTest(unittest.TestCase):
    def test_docket_maps_capability_classes_to_blocked_egress_routes(self) -> None:
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
        self.assertGreaterEqual(validation["source_capability_class_count"], 8)
        self.assertGreaterEqual(validation["route_count"], 8)
        self.assertFalse(validation["gateway_registration_allowed"])
        self.assertFalse(validation["gateway_start_allowed"])
        self.assertFalse(validation["live_egress_allowed"])
        self.assertFalse(validation["worker_registration_allowed"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertFalse(validation["runtime_start_allowed"])
        self.assertFalse(validation["browser_session_start_allowed"])
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["gateway_start_allowed"]["const"], False)

        routes = {item["route_id"]: item for item in report["gateway_routes"]}
        for required in [
            "local_agent_to_agent_report_only",
            "browser_read_only_gateway",
            "mcp_tool_gateway",
            "model_api_gateway",
            "runtime_process_gateway",
            "public_action_gateway",
            "account_wallet_payment_gateway",
            "telemetry_export_gateway",
        ]:
            self.assertIn(required, routes)
            self.assertFalse(routes[required]["live_execution_allowed"])
            self.assertIn("agent_egress_event_ledger_v1", routes[required]["required_gates"])

        self.assertIn("mcp_tool_registry_gate_v1", routes["mcp_tool_gateway"]["required_gates"])
        self.assertIn("browser_read_only_apply_command_contract_v1", routes["browser_read_only_gateway"]["required_gates"])
        self.assertIn("model_api_execution_gate", routes["model_api_gateway"]["required_gates"])
        self.assertIn("runtime_start_preflight_v1", routes["runtime_process_gateway"]["required_gates"])
        self.assertIn("legal_kyc_tax_payment_gate", routes["account_wallet_payment_gateway"]["required_gates"])
        self.assertEqual(
            report["next_action"],
            "Build signed operator decision intake for one exact egress route before any gateway registration, gateway start, or live egress.",
        )


if __name__ == "__main__":
    unittest.main()
