# Account Wallet Payment Egress Apply Command Contract v1

Generated UTC: 2026-06-20T21:07:26Z
Target route: `account_wallet_payment_gateway`
Report JSON: `E:\agent-company-lab\reports\account-wallet-payment-egress-apply-command-contract-v1-20260618.json`
Validation JSON: `E:\agent-company-lab\reports\account-wallet-payment-egress-apply-command-contract-v1-validation-20260618.json`

## Summary

- All checks passed: `True`
- Accepted fixtures: `2`
- Rejected fixtures: `69`
- Apply command allowed: `False`
- Account creation allowed: `False`
- Wallet creation allowed: `False`
- Payment action allowed: `False`
- Real-money action allowed: `False`
- Accounts created: `0`
- Wallets created: `0`
- Funds transferred: `0`
- KYC submissions: `0`
- Service requests updated: `0`
- External side effects: `False`

## Fixture Results

| Fixture | Expected | Accepted | Passed | Primary Errors |
| --- | --- | --- | --- | --- |
| `positive_deny_noop` | `accepted` | `True` | `True` |  |
| `positive_report_only_contract` | `accepted` | `True` | `True` |  |
| `negative_target_route_id` | `rejected` | `False` | `True` | target_route_id_must_match_account_wallet_payment_gateway |
| `negative_target_egress_type` | `rejected` | `False` | `True` | target_egress_type_must_be_account_wallet_payment |
| `negative_source_apply_preflight_blocker_path` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source, source_apply_preflight_blocker_path_must_stay_inside_lab |
| `negative_source_guard_validation_path` | `rejected` | `False` | `True` | source_guard_validation_path_must_match_current_source |
| `negative_source_intake_validation_path` | `rejected` | `False` | `True` | source_intake_validation_path_must_match_current_source |
| `negative_source_gateway_docket_validation_path` | `rejected` | `False` | `True` | source_gateway_docket_validation_path_must_match_current_source |
| `negative_source_egress_ledger_validation_path` | `rejected` | `False` | `True` | source_egress_ledger_validation_path_must_match_current_source |
| `negative_source_identity_validation_path` | `rejected` | `False` | `True` | source_identity_validation_path_must_match_current_source |
| `negative_expected_source_apply_preflight_status` | `rejected` | `False` | `True` | expected_source_apply_preflight_status_must_match |
| `negative_real_signed_decision_present` | `rejected` | `False` | `True` | real_signed_decision_must_be_absent |
| `negative_exact_account_wallet_payment_approval_present` | `rejected` | `False` | `True` | exact_account_wallet_payment_approval_must_be_absent |
| `negative_command_type` | `rejected` | `False` | `True` | command_type_must_be_deny_or_report_only_contract |
| `negative_allowed_scope` | `rejected` | `False` | `True` | allowed_scope_must_match_command_type |
| `negative_immutable_command_preview_sha256` | `rejected` | `False` | `True` | immutable_command_preview_sha256_must_be_empty_without_approval |
| `negative_apply_command_allowed` | `rejected` | `False` | `True` | apply_command_allowed_must_be_false |
| `negative_apply_allowed` | `rejected` | `False` | `True` | apply_allowed_must_be_false |
| `negative_gateway_registration_allowed` | `rejected` | `False` | `True` | gateway_registration_allowed_must_be_false |
| `negative_gateway_start_allowed` | `rejected` | `False` | `True` | gateway_start_allowed_must_be_false |
| `negative_live_egress_allowed` | `rejected` | `False` | `True` | live_egress_allowed_must_be_false |
| `negative_account_creation_allowed` | `rejected` | `False` | `True` | account_creation_allowed_must_be_false |
| `negative_terms_acceptance_allowed` | `rejected` | `False` | `True` | terms_acceptance_allowed_must_be_false |
| `negative_wallet_creation_allowed` | `rejected` | `False` | `True` | wallet_creation_allowed_must_be_false |
| `negative_private_key_custody_allowed` | `rejected` | `False` | `True` | private_key_custody_allowed_must_be_false |
| `negative_funds_transfer_allowed` | `rejected` | `False` | `True` | funds_transfer_allowed_must_be_false |
| `negative_payment_action_allowed` | `rejected` | `False` | `True` | payment_action_allowed_must_be_false |
| `negative_legal_kyc_tax_action_allowed` | `rejected` | `False` | `True` | legal_kyc_tax_action_allowed_must_be_false |
| `negative_public_payment_address_allowed` | `rejected` | `False` | `True` | public_payment_address_allowed_must_be_false |
| `negative_real_money_action_allowed` | `rejected` | `False` | `True` | real_money_action_allowed_must_be_false |
| `negative_browser_session_start_allowed` | `rejected` | `False` | `True` | browser_session_start_allowed_must_be_false |
| `negative_account_actions` | `rejected` | `False` | `True` | account_actions_must_be_false |
| `negative_wallet_actions` | `rejected` | `False` | `True` | wallet_actions_must_be_false |
| `negative_payment_actions` | `rejected` | `False` | `True` | payment_actions_must_be_false |
| `negative_real_money_actions` | `rejected` | `False` | `True` | real_money_actions_must_be_false |
| `negative_service_requests_assigned` | `rejected` | `False` | `True` | service_requests_assigned_must_be_zero |
| `negative_service_requests_updated` | `rejected` | `False` | `True` | service_requests_updated_must_be_zero |
| `negative_mcp_tool_calls` | `rejected` | `False` | `True` | mcp_tool_calls_must_be_false |
| `negative_model_api_calls` | `rejected` | `False` | `True` | model_api_calls_must_be_false |
| `negative_public_actions` | `rejected` | `False` | `True` | public_actions_must_be_false |
| `negative_external_side_effects` | `rejected` | `False` | `True` | external_side_effects_must_be_false |
| `negative_outside_source_preflight` | `rejected` | `False` | `True` | source_apply_preflight_blocker_path_must_match_current_source, source_apply_preflight_blocker_path_must_stay_inside_lab |
| `negative_target_request_id` | `rejected` | `False` | `True` | target_request_ids_must_be_empty |
| `negative_short_rollback` | `rejected` | `False` | `True` | rollback_plan_too_short |
| `negative_real_decision_path` | `rejected` | `False` | `True` | real_signed_decision_must_be_absent |
| `negative_exact_approval_path` | `rejected` | `False` | `True` | exact_account_wallet_payment_approval_must_be_absent |
| `negative_boundary_apply_commands_written` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_written_must_equal_0 |
| `negative_boundary_apply_commands_executed` | `rejected` | `False` | `True` | runtime_boundary_apply_commands_executed_must_equal_0 |
| `negative_boundary_decisions_applied` | `rejected` | `False` | `True` | runtime_boundary_decisions_applied_must_equal_0 |
| `negative_boundary_approval_rows_written` | `rejected` | `False` | `True` | runtime_boundary_approval_rows_written_must_equal_0 |
| `negative_boundary_gateway_registrations` | `rejected` | `False` | `True` | runtime_boundary_gateway_registrations_must_equal_0 |
| `negative_boundary_gateway_starts` | `rejected` | `False` | `True` | runtime_boundary_gateway_starts_must_equal_0 |
| `negative_boundary_live_egress_events` | `rejected` | `False` | `True` | runtime_boundary_live_egress_events_must_equal_0 |
| `negative_boundary_accounts_created` | `rejected` | `False` | `True` | runtime_boundary_accounts_created_must_equal_0 |
| `negative_boundary_terms_accepted` | `rejected` | `False` | `True` | runtime_boundary_terms_accepted_must_equal_0 |
| `negative_boundary_wallets_created` | `rejected` | `False` | `True` | runtime_boundary_wallets_created_must_equal_0 |
| `negative_boundary_private_keys_stored` | `rejected` | `False` | `True` | runtime_boundary_private_keys_stored_must_equal_0 |
| `negative_boundary_seed_phrases_stored` | `rejected` | `False` | `True` | runtime_boundary_seed_phrases_stored_must_equal_0 |
| `negative_boundary_funds_transferred` | `rejected` | `False` | `True` | runtime_boundary_funds_transferred_must_equal_0 |
| `negative_boundary_payment_methods_changed` | `rejected` | `False` | `True` | runtime_boundary_payment_methods_changed_must_equal_0 |
| `negative_boundary_kyc_submissions` | `rejected` | `False` | `True` | runtime_boundary_kyc_submissions_must_equal_0 |
| `negative_boundary_tax_forms_submitted` | `rejected` | `False` | `True` | runtime_boundary_tax_forms_submitted_must_equal_0 |
| `negative_boundary_payment_addresses_published` | `rejected` | `False` | `True` | runtime_boundary_payment_addresses_published_must_equal_0 |
| `negative_boundary_worker_starts` | `rejected` | `False` | `True` | runtime_boundary_worker_starts_must_equal_0 |
| `negative_boundary_runtime_starts` | `rejected` | `False` | `True` | runtime_boundary_runtime_starts_must_equal_0 |
| `negative_boundary_browser_sessions_started` | `rejected` | `False` | `True` | runtime_boundary_browser_sessions_started_must_equal_0 |
| `negative_boundary_service_requests_updated` | `rejected` | `False` | `True` | runtime_boundary_service_requests_updated_must_equal_0 |
| `negative_boundary_payment_actions` | `rejected` | `False` | `True` | runtime_boundary_payment_actions_must_equal_False |
| `negative_boundary_wallet_actions` | `rejected` | `False` | `True` | runtime_boundary_wallet_actions_must_equal_False |
| `negative_boundary_real_money_actions` | `rejected` | `False` | `True` | runtime_boundary_real_money_actions_must_equal_False |
| `negative_boundary_external_side_effects` | `rejected` | `False` | `True` | runtime_boundary_external_side_effects_must_equal_False |

## Boundary

- This contract is report-only and writes no apply command.
- Account/wallet/payment execution remains blocked until a real signed decision, exact approval, and immutable command preview exist.
- No account creation, terms acceptance, wallet creation, private-key or seed custody, fund transfer, payment method change, KYC/tax/legal action, public payment-address publication, service-request mutation, worker start, browser start, model/MCP call, live egress, or external side effect is allowed.

Next action: Build account_wallet_payment_gateway apply-command guard only after a real signed operator decision, exact account/wallet/payment approval, and immutable command preview exist; until then, keep account/wallet/payment egress blocked.
