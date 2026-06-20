import unittest
from pathlib import Path

from generated_artifact_helpers import (
    assert_clean_fixture_validation,
    assert_false_fields,
    assert_zero_fields,
    run_validator_load_artifacts,
)


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_account_wallet_payment_egress_apply_command_contract.py"
VALIDATION = ROOT / "reports" / "account-wallet-payment-egress-apply-command-contract-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "account-wallet-payment-egress-apply-command-contract-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "account-wallet-payment-egress-apply-command-contract-v1.schema.json"


class AccountWalletPaymentEgressApplyCommandContractTest(unittest.TestCase):
    def test_contract_rejects_live_account_wallet_payment_apply_commands(self) -> None:
        validation, report, schema = run_validator_load_artifacts(
            self,
            root=ROOT,
            tool=TOOL,
            validation_path=VALIDATION,
            report_path=REPORT,
            schema_path=SCHEMA,
        )

        assert_clean_fixture_validation(self, validation, min_fixture_count=50)
        self.assertEqual(validation["target_route_id"], "account_wallet_payment_gateway")
        self.assertEqual(validation["target_egress_type"], "account_wallet_payment")
        self.assertEqual(validation["accepted_count"], 2)
        self.assertEqual(validation["rejected_count"], validation["fixture_count"] - 2)
        assert_false_fields(
            self,
            validation,
            [
                "apply_command_allowed",
                "apply_allowed",
                "gateway_registration_allowed",
                "gateway_start_allowed",
                "live_egress_allowed",
                "account_creation_allowed",
                "terms_acceptance_allowed",
                "wallet_creation_allowed",
                "private_key_custody_allowed",
                "funds_transfer_allowed",
                "payment_action_allowed",
                "legal_kyc_tax_action_allowed",
                "public_payment_address_allowed",
                "real_money_action_allowed",
                "account_actions",
                "wallet_actions",
                "payment_actions",
                "real_money_actions",
                "browser_session_start_allowed",
                "mcp_tool_calls",
                "model_api_calls",
                "public_actions",
                "external_side_effects",
            ],
        )
        assert_zero_fields(
            self,
            validation,
            [
                "accounts_created",
                "terms_accepted",
                "wallets_created",
                "private_keys_stored",
                "seed_phrases_stored",
                "funds_transferred",
                "payment_methods_changed",
                "kyc_submissions",
                "tax_forms_submitted",
                "payment_addresses_published",
                "browser_sessions_started",
                "service_requests_assigned",
                "service_requests_updated",
                "apply_commands_written",
                "apply_commands_executed",
                "worker_starts",
                "runtime_starts",
            ],
        )

        self.assertEqual(schema["properties"]["command_type"]["enum"][0], "deny_noop")
        self.assertEqual(schema["properties"]["target_route_id"]["const"], "account_wallet_payment_gateway")
        self.assertEqual(schema["properties"]["target_egress_type"]["const"], "account_wallet_payment")
        self.assertEqual(schema["properties"]["account_creation_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["wallet_creation_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["payment_action_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["real_money_action_allowed"]["const"], False)
        self.assertEqual(schema["properties"]["live_egress_allowed"]["const"], False)

        accepted = [item for item in report["results"] if item["result"]["accepted_for_contract_only"]]
        self.assertEqual(len(accepted), 2)
        for item in accepted:
            payload = item["result"]
            self.assertEqual(payload["target_route_id"], "account_wallet_payment_gateway")
            self.assertFalse(payload["apply_command_allowed"])
            self.assertFalse(payload["account_creation_allowed"])
            self.assertFalse(payload["wallet_creation_allowed"])
            self.assertFalse(payload["payment_action_allowed"])
            self.assertFalse(payload["real_money_action_allowed"])

        self.assertEqual(
            report["next_action"],
            "Build account_wallet_payment_gateway apply-command guard only after a real signed operator decision, "
            "exact account/wallet/payment approval, and immutable command preview exist; until then, keep "
            "account/wallet/payment egress blocked.",
        )


if __name__ == "__main__":
    unittest.main()
