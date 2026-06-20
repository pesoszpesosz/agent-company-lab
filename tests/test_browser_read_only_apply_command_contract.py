import unittest
from pathlib import Path

from generated_artifact_helpers import (
    assert_clean_fixture_validation,
    assert_false_fields,
    assert_zero_fields,
    run_validator_load_artifacts,
)


ROOT = Path(r"E:\agent-company-lab")
TOOL = ROOT / "tools" / "validate_browser_read_only_apply_command_contract.py"
VALIDATION = ROOT / "reports" / "browser-read-only-apply-command-contract-v1-validation-20260618.json"
REPORT = ROOT / "reports" / "browser-read-only-apply-command-contract-v1-20260618.json"
SCHEMA = ROOT / "architecture" / "browser-read-only-apply-command-contract-v1.schema.json"
FIXTURE_DIR = ROOT / "reports" / "browser-read-only-apply-command-contract-v1-fixtures"


class BrowserReadOnlyApplyCommandContractTest(unittest.TestCase):
    def test_contract_accepts_only_report_only_noop_commands(self) -> None:
        validation, report, schema = run_validator_load_artifacts(
            self,
            root=ROOT,
            tool=TOOL,
            validation_path=VALIDATION,
            report_path=REPORT,
            schema_path=SCHEMA,
        )

        assert_clean_fixture_validation(self, validation, min_fixture_count=22)
        self.assertEqual(validation["accepted_count"], 2)
        self.assertGreaterEqual(validation["rejected_count"], 20)
        self.assertEqual(validation["source_apply_preflight_status"], "blocked_no_real_signed_decision")
        self.assertEqual(validation["source_guard_adapter_contract_gate"], "present_valid_start_blocked")
        assert_false_fields(
            self,
            validation,
            [
                "apply_command_allowed",
                "apply_allowed",
                "assignment_allowed",
                "browser_session_start_allowed",
                "worker_start_allowed",
                "public_actions",
                "external_side_effects",
            ],
        )
        assert_zero_fields(
            self,
            validation,
            [
                "apply_commands_written",
                "apply_commands_executed",
                "decisions_applied",
                "service_requests_assigned",
                "service_requests_mutated",
                "browser_sessions_started",
                "worker_starts",
            ],
        )
        self.assertTrue(FIXTURE_DIR.exists())
        self.assertGreaterEqual(len(list(FIXTURE_DIR.glob("*.json"))), 22)
        self.assertEqual(schema["properties"]["command_type"]["enum"][0], "deny_noop")
        self.assertEqual(report["source_apply_preflight"]["guard_adapter_contract_gate"], "present_valid_start_blocked")
        self.assertEqual(report["positive_authority"]["accepted_scope"], "report_only_apply_command_contract")
        self.assertFalse(report["positive_authority"]["apply_command_allowed"])


if __name__ == "__main__":
    unittest.main()
