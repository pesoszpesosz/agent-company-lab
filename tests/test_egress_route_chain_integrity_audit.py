import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_egress_route_chain_integrity_audit.py"
VALIDATION = ROOT / "reports" / "egress-route-chain-integrity-audit-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "egress-route-chain-integrity-audit-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "egress-route-chain-integrity-audit-v1.schema.json"


class EgressRouteChainIntegrityAuditTest(unittest.TestCase):
    def test_audit_identifies_browser_and_mcp_full_chains_and_remaining_gaps(self) -> None:
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
        self.assertEqual(validation["route_count"], 8)
        self.assertEqual(validation["full_chain_route_count"], 8)
        self.assertEqual(validation["partial_chain_route_count"], 0)
        self.assertNotEqual(validation["recommended_next_route_id"], "browser_read_only_gateway")
        self.assertNotEqual(validation["recommended_next_route_id"], "mcp_tool_gateway")
        self.assertNotEqual(validation["recommended_next_route_id"], "local_agent_to_agent_report_only")
        self.assertNotEqual(validation["recommended_next_route_id"], "model_api_gateway")
        self.assertNotEqual(validation["recommended_next_route_id"], "runtime_process_gateway")
        self.assertNotEqual(validation["recommended_next_route_id"], "account_wallet_payment_gateway")
        self.assertEqual(validation["recommended_next_route_id"], "")
        self.assertEqual(validation["recommended_next_layer"], "")
        self.assertFalse(validation["gateway_registration_allowed"])
        self.assertFalse(validation["gateway_start_allowed"])
        self.assertFalse(validation["live_egress_allowed"])
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertFalse(validation["external_side_effects"])
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        routes = {item["route_id"]: item for item in report["route_audits"]}
        self.assertNotIn(validation["recommended_next_route_id"], routes)
        browser = routes["browser_read_only_gateway"]
        self.assertEqual(browser["chain_status"], "full_report_only_chain")
        self.assertEqual(browser["missing_layers"], [])
        for layer in [
            "unified_gateway_docket",
            "signed_decision_intake_contract",
            "signed_decision_guard",
            "apply_preflight_blocker",
            "apply_command_contract",
        ]:
            self.assertIn(layer, browser["present_layers"])

        mcp = routes["mcp_tool_gateway"]
        self.assertEqual(mcp["chain_status"], "full_report_only_chain")
        self.assertEqual(mcp["missing_layers"], [])
        for layer in [
            "unified_gateway_docket",
            "signed_decision_intake_contract",
            "signed_decision_guard",
            "apply_preflight_blocker",
            "apply_command_guard",
        ]:
            self.assertIn(layer, mcp["present_layers"])
        self.assertEqual(mcp["target_egress_type"], "mcp_tool")
        self.assertEqual(mcp["mcp_servers_started"], 0)
        self.assertEqual(mcp["mcp_servers_enabled"], 0)
        self.assertFalse(mcp["mcp_tool_calls"])
        self.assertFalse(mcp["credential_access_allowed"])

        local_a2a = routes["local_agent_to_agent_report_only"]
        self.assertEqual(local_a2a["chain_status"], "full_report_only_chain")
        self.assertIn("signed_decision_guard", local_a2a["present_layers"])
        self.assertIn("apply_preflight_blocker", local_a2a["present_layers"])
        self.assertIn("apply_command_contract", local_a2a["present_layers"])
        self.assertIn("apply_command_guard", local_a2a["present_layers"])
        self.assertNotIn("signed_decision_guard", local_a2a["missing_layers"])
        self.assertNotIn("apply_preflight_blocker", local_a2a["missing_layers"])
        self.assertNotIn("apply_command_contract", local_a2a["missing_layers"])
        self.assertNotIn("apply_command_guard", local_a2a["missing_layers"])
        self.assertEqual(local_a2a["missing_layers"], [])
        self.assertFalse(local_a2a["agent_message_send_allowed"])
        self.assertEqual(local_a2a["agent_messages_sent"], 0)

        model_api = routes["model_api_gateway"]
        self.assertEqual(model_api["chain_status"], "full_report_only_chain")
        self.assertIn("signed_decision_guard", model_api["present_layers"])
        self.assertIn("apply_preflight_blocker", model_api["present_layers"])
        self.assertIn("apply_command_contract", model_api["present_layers"])
        self.assertNotIn("signed_decision_guard", model_api["missing_layers"])
        self.assertNotIn("apply_preflight_blocker", model_api["missing_layers"])
        self.assertNotIn("apply_command_contract", model_api["missing_layers"])
        self.assertEqual(model_api["missing_layers"], [])
        self.assertFalse(model_api["model_api_call_allowed"])
        self.assertFalse(model_api["model_api_calls"])
        self.assertFalse(model_api["provider_key_use_allowed"])
        self.assertFalse(model_api["provider_keys_used"])
        self.assertFalse(model_api["training_data_upload_allowed"])
        self.assertFalse(model_api["training_data_uploaded"])
        self.assertEqual(model_api["max_cost_usd"], 0)

        runtime_process = routes["runtime_process_gateway"]
        self.assertEqual(runtime_process["chain_status"], "full_report_only_chain")
        self.assertIn("signed_decision_guard", runtime_process["present_layers"])
        self.assertIn("apply_preflight_blocker", runtime_process["present_layers"])
        self.assertIn("apply_command_contract", runtime_process["present_layers"])
        self.assertNotIn("signed_decision_guard", runtime_process["missing_layers"])
        self.assertNotIn("apply_preflight_blocker", runtime_process["missing_layers"])
        self.assertNotIn("apply_command_contract", runtime_process["missing_layers"])
        self.assertEqual(runtime_process["missing_layers"], [])
        self.assertFalse(runtime_process["runtime_start_allowed"])
        self.assertEqual(runtime_process["runtime_starts"], 0)
        self.assertEqual(runtime_process["dependency_installs"], 0)
        self.assertEqual(runtime_process["queue_mutations"], 0)
        self.assertEqual(runtime_process["worker_starts"], 0)

        public_action = routes["public_action_gateway"]
        self.assertEqual(public_action["chain_status"], "full_report_only_chain")
        self.assertIn("signed_decision_guard", public_action["present_layers"])
        self.assertIn("apply_preflight_blocker", public_action["present_layers"])
        self.assertIn("apply_command_contract", public_action["present_layers"])
        self.assertNotIn("signed_decision_guard", public_action["missing_layers"])
        self.assertNotIn("apply_preflight_blocker", public_action["missing_layers"])
        self.assertNotIn("apply_command_contract", public_action["missing_layers"])
        self.assertEqual(public_action["missing_layers"], [])
        self.assertFalse(public_action["public_action_allowed"])
        self.assertFalse(public_action["public_actions"])
        self.assertFalse(public_action["account_actions"])
        self.assertEqual(public_action["browser_sessions_started"], 0)

        account_wallet_payment = routes["account_wallet_payment_gateway"]
        self.assertEqual(account_wallet_payment["chain_status"], "full_report_only_chain")
        self.assertIn("signed_decision_guard", account_wallet_payment["present_layers"])
        self.assertIn("apply_preflight_blocker", account_wallet_payment["present_layers"])
        self.assertIn("apply_command_contract", account_wallet_payment["present_layers"])
        self.assertNotIn("signed_decision_guard", account_wallet_payment["missing_layers"])
        self.assertNotIn("apply_preflight_blocker", account_wallet_payment["missing_layers"])
        self.assertNotIn("apply_command_contract", account_wallet_payment["missing_layers"])
        self.assertEqual(account_wallet_payment["missing_layers"], [])
        self.assertFalse(account_wallet_payment["account_creation_allowed"])
        self.assertFalse(account_wallet_payment["wallet_creation_allowed"])
        self.assertFalse(account_wallet_payment["private_key_custody_allowed"])
        self.assertFalse(account_wallet_payment["funds_transfer_allowed"])
        self.assertFalse(account_wallet_payment["payment_action_allowed"])
        self.assertFalse(account_wallet_payment["legal_kyc_tax_action_allowed"])
        self.assertFalse(account_wallet_payment["public_payment_address_allowed"])
        self.assertFalse(account_wallet_payment["real_money_action_allowed"])
        self.assertFalse(account_wallet_payment["wallet_actions"])
        self.assertFalse(account_wallet_payment["payment_actions"])
        self.assertFalse(account_wallet_payment["real_money_actions"])

        telemetry = routes["telemetry_export_gateway"]
        self.assertEqual(telemetry["chain_status"], "full_report_only_chain")
        self.assertIn("signed_decision_guard", telemetry["present_layers"])
        self.assertIn("apply_preflight_blocker", telemetry["present_layers"])
        self.assertIn("apply_command_contract", telemetry["present_layers"])
        self.assertNotIn("signed_decision_guard", telemetry["missing_layers"])
        self.assertNotIn("apply_preflight_blocker", telemetry["missing_layers"])
        self.assertNotIn("apply_command_contract", telemetry["missing_layers"])
        self.assertEqual(telemetry["missing_layers"], [])
        self.assertFalse(telemetry["telemetry_export_allowed"])
        self.assertEqual(telemetry["telemetry_exports"], 0)
        self.assertFalse(telemetry["external_trace_export_allowed"])
        self.assertEqual(telemetry["external_trace_exports"], 0)
        self.assertFalse(telemetry["private_prompt_upload_allowed"])
        self.assertEqual(telemetry["private_prompts_uploaded"], 0)
        self.assertFalse(telemetry["credential_export_allowed"])
        self.assertEqual(telemetry["credentials_exported"], 0)
        self.assertFalse(telemetry["unredacted_log_sync_allowed"])
        self.assertEqual(telemetry["unredacted_logs_synced"], 0)
        self.assertFalse(telemetry["live_egress_allowed"])
        self.assertFalse(telemetry["external_side_effects"])

        for route_id, route in routes.items():
            self.assertFalse(route["live_egress_allowed"])
            self.assertFalse(route["external_side_effects"])
            self.assertEqual(route["chain_status"], "full_report_only_chain")

        self.assertEqual(
            report["next_action"],
            "All report-only egress route chains have their required non-live guard layers; continue only after a real signed operator decision and route-specific approval evidence exists.",
        )


if __name__ == "__main__":
    unittest.main()
