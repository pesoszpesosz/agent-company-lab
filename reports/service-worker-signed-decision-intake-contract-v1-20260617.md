# Service Worker Signed Decision Intake Contract v1

Generated UTC: 2026-06-21T15:49:46Z
Report JSON: `E:\agent-company-lab\reports\service-worker-signed-decision-intake-contract-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\service-worker-signed-decision-intake-contract-v1-validation-20260617.json`

## Summary

- All checks passed: `True`
- Contract status: `report_only_intake_contract_ready`
- Service templates: `13` / `13`
- Current requests covered: `16` / `16`
- Approval granted by contract: `False`
- Apply allowed: `False`
- External side effects: `False`

## Templates

| Service | Decisions | Bound Requests | Route |
| --- | --- | --- | --- |
| `account_registration_intake` | `deny`, `approve_review_packet_only` | `0` | `human_user_cro_required_review_packet_no_external_action` |
| `browser_read_only_session` | `deny`, `approve_review_packet_only`, `approve_assignment_preflight_only` | `9` | `requesting_manager_and_cro_preflight_only_no_browser_start` |
| `data_purchase_api_access_gate` | `deny`, `approve_review_packet_only` | `0` | `human_user_cro_required_review_packet_no_external_action` |
| `github_public_action_gate` | `deny`, `approve_review_packet_only`, `approve_exact_action_preflight_only` | `0` | `human_user_cro_reputation_required_exact_public_action_only` |
| `legal_kyc_tax_payment_gate` | `deny`, `approve_review_packet_only` | `1` | `human_user_cro_or_user_only_decision_packet_no_commitment` |
| `model_api_execution_gate` | `deny`, `approve_review_packet_only`, `approve_assignment_preflight_only` | `1` | `human_user_cro_observability_required_cost_data_scope` |
| `outreach_delivery_gate` | `deny`, `approve_review_packet_only`, `approve_exact_action_preflight_only` | `0` | `human_user_cro_reputation_required_exact_public_action_only` |
| `public_action_execution` | `deny`, `approve_review_packet_only`, `approve_exact_action_preflight_only` | `0` | `human_user_cro_reputation_required_exact_public_action_only` |
| `real_money_trade_gate` | `deny`, `approve_review_packet_only` | `1` | `human_user_cro_or_user_only_decision_packet_no_commitment` |
| `secrets_credentials_handling_gate` | `deny`, `approve_review_packet_only` | `0` | `human_user_cro_required_review_packet_no_external_action` |
| `security_report_submission_gate` | `deny`, `approve_review_packet_only` | `1` | `human_user_cro_required_review_packet_no_external_action` |
| `wallet_public_address_response` | `deny`, `approve_review_packet_only`, `approve_exact_action_preflight_only` | `0` | `human_user_cro_required_wallet_no_key_or_fund_control` |
| `wallet_setup_packet` | `deny`, `approve_review_packet_only` | `0` | `human_user_cro_required_wallet_no_key_or_fund_control` |

## Boundary

- This contract defines the signed-decision intake shape only.
- It grants no approval, applies no decision, assigns no request, starts no worker, opens no browser, and calls no APIs.
- Any accepted decision still requires a separate apply preflight.
