import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_account_wallet_payment_egress_signed_decision_guard.py"
VALIDATION = ROOT / "reports" / "account-wallet-payment-egress-signed-decision-guard-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "account-wallet-payment-egress-signed-decision-guard-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "account-wallet-payment-egress-signed-decision-guard-v1.schema.json"


class AccountWalletPaymentEgressSignedDecisionGuardTest(unittest.TestCase):
    def test_guard_accepts_only_report_only_account_wallet_payment_preflight_decisions(self) -> None:
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
        self.assertEqual(validation["target_route_id"], "account_wallet_payment_gateway")
        self.assertEqual(validation["target_egress_type"], "account_wallet_payment")
        self.assertGreaterEqual(validation["fixture_count"], 50)
        self.assertEqual(validation["accepted_count"], 2)
        self.assertEqual(validation["rejected_count"], validation["fixture_count"] - 2)
        self.assertEqual(validation["fixture_expectation_mismatch_count"], 0)
        self.assertFalse(validation["apply_allowed"])
        self.assertEqual(validation["decisions_applied"], 0)
        self.assertEqual(validation["approval_rows_written"], 0)
        self.assertFalse(validation["gateway_registration_allowed"])
        self.assertFalse(validation["gateway_start_allowed"])
        self.assertFalse(validation["live_egress_allowed"])
        self.assertFalse(validation["account_creation_allowed"])
        self.assertFalse(validation["terms_acceptance_allowed"])
        self.assertFalse(validation["wallet_creation_allowed"])
        self.assertFalse(validation["private_key_custody_allowed"])
        self.assertFalse(validation["funds_transfer_allowed"])
        self.assertFalse(validation["payment_action_allowed"])
        self.assertFalse(validation["legal_kyc_tax_action_allowed"])
        self.assertFalse(validation["public_payment_address_allowed"])
        self.assertFalse(validation["real_money_action_allowed"])
        self.assertEqual(validation["accounts_created"], 0)
        self.assertEqual(validation["wallets_created"], 0)
        self.assertEqual(validation["funds_transferred"], 0)
        self.assertFalse(validation["account_actions"])
        self.assertFalse(validation["wallet_actions"])
        self.assertFalse(validation["payment_actions"])
        self.assertFalse(validation["real_money_actions"])
        self.assertFalse(validation["worker_start_allowed"])
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["external_side_effects"])

        self.assertEqual(schema["properties"]["decision"]["enum"][0], "deny")
        self.assertEqual(schema["properties"]["route_id"]["const"], "account_wallet_payment_gateway")
        self.assertEqual(schema["properties"]["egress_type"]["const"], "account_wallet_payment")
        self.assertEqual(schema["properties"]["wallet_creation_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["real_money_action_allowed"]["const"], False)

        required = set(report["target_route_required_gates"])
        self.assertEqual(
            required,
            {
                "account_registration_intake",
                "wallet_setup_packet",
                "wallet_public_address_response",
                "legal_kyc_tax_payment_gate",
                "agent_egress_event_ledger_v1",
            },
        )

        accepted = [item for item in report["results"] if item["result"]["accepted_for_apply_preflight"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            result_payload = item["result"]
            self.assertFalse(result_payload["account_creation_allowed"])
            self.assertFalse(result_payload["wallet_creation_allowed"])
            self.assertFalse(result_payload["private_key_custody_allowed"])
            self.assertFalse(result_payload["funds_transfer_allowed"])
            self.assertFalse(result_payload["payment_action_allowed"])
            self.assertFalse(result_payload["real_money_action_allowed"])

        self.assertEqual(
            report["next_action"],
            "Build account_wallet_payment_gateway apply preflight blocker before any account creation, terms acceptance, wallet creation, private-key custody, fund transfer, payment method change, KYC/tax/legal action, public payment-address publication, service-request mutation, or live egress.",
        )


if __name__ == "__main__":
    unittest.main()
