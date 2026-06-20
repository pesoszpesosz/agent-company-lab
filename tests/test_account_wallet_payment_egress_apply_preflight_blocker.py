import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "write_account_wallet_payment_egress_apply_preflight_blocker.py"
VALIDATION = ROOT / "reports" / "account-wallet-payment-egress-apply-preflight-blocker-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "account-wallet-payment-egress-apply-preflight-blocker-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "account-wallet-payment-egress-apply-preflight-blocker-v1.schema.json"


class AccountWalletPaymentEgressApplyPreflightBlockerTest(unittest.TestCase):
    def test_blocker_prevents_account_wallet_payment_apply_until_real_decision_and_contract_exist(self) -> None:
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
        self.assertEqual(validation["apply_preflight_status"], "blocked_no_real_signed_decision")
        self.assertEqual(validation["blocker_reason"], "no_real_signed_operator_account_wallet_payment_egress_decision_artifact")
        self.assertFalse(validation["real_signed_decision_present"])
        self.assertFalse(validation["exact_account_wallet_payment_approval_present"])
        self.assertFalse(validation["apply_command_contract_present"])
        self.assertEqual(validation["accepted_guard_decision_count"], 2)
        self.assertGreaterEqual(validation["rejected_guard_decision_count"], 60)
        self.assertFalse(validation["apply_allowed"])
        self.assertEqual(validation["apply_commands_written"], 0)
        self.assertEqual(validation["apply_commands_executed"], 0)
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
        self.assertEqual(validation["terms_accepted"], 0)
        self.assertEqual(validation["wallets_created"], 0)
        self.assertEqual(validation["private_keys_stored"], 0)
        self.assertEqual(validation["seed_phrases_stored"], 0)
        self.assertEqual(validation["funds_transferred"], 0)
        self.assertEqual(validation["payment_methods_changed"], 0)
        self.assertEqual(validation["kyc_submissions"], 0)
        self.assertEqual(validation["tax_forms_submitted"], 0)
        self.assertEqual(validation["payment_addresses_published"], 0)
        self.assertFalse(validation["account_actions"])
        self.assertFalse(validation["wallet_actions"])
        self.assertFalse(validation["payment_actions"])
        self.assertFalse(validation["real_money_actions"])
        self.assertFalse(validation["browser_session_start_allowed"])
        self.assertEqual(validation["browser_sessions_started"], 0)
        self.assertEqual(validation["worker_starts"], 0)
        self.assertEqual(validation["runtime_starts"], 0)
        self.assertEqual(validation["service_requests_assigned"], 0)
        self.assertEqual(validation["service_requests_updated"], 0)
        self.assertFalse(validation["mcp_tool_calls"])
        self.assertFalse(validation["model_api_calls"])
        self.assertFalse(validation["public_actions"])
        self.assertFalse(validation["external_side_effects"])

        self.assertEqual(schema["properties"]["target_route_id"]["const"], "account_wallet_payment_gateway")
        self.assertEqual(schema["properties"]["target_egress_type"]["const"], "account_wallet_payment")
        self.assertEqual(schema["properties"]["apply_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["account_creation_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["wallet_creation_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["payment_action_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["real_money_action_allowed"]["const"], False)

        checks = {item["check_id"]: item for item in report["checks"]}
        for required in [
            "gateway_docket_validation_passes",
            "signed_decision_intake_validation_passes",
            "account_wallet_payment_signed_decision_guard_passes_for_target_route",
            "agent_egress_event_ledger_validation_passes",
            "identity_envelope_validation_passes",
            "service_worker_chain_integrity_passes_without_start",
            "real_signed_decision_absent",
            "exact_account_wallet_payment_approval_absent",
            "account_wallet_payment_apply_command_contract_absent",
        ]:
            self.assertIn(required, checks)
            self.assertTrue(checks[required]["passed"])

        self.assertEqual(
            report["next_action"],
            "Provide a real signed operator account_wallet_payment_gateway decision artifact, exact account/wallet/payment approval, and account/wallet/payment apply-command contract before any account creation, terms acceptance, wallet creation, private-key custody, seed custody, fund transfer, payment method change, KYC/tax/legal action, public payment-address publication, service-request mutation, worker/browser/model/MCP start or call, live egress, or external side effect can be considered.",
        )


if __name__ == "__main__":
    unittest.main()
