# Service Worker Approval Authority Coverage v1

Generated UTC: 2026-06-21T15:44:19Z
Report JSON: `E:\agent-company-lab\reports\service-worker-approval-authority-coverage-v1-20260617.json`
Validation JSON: `E:\agent-company-lab\reports\service-worker-approval-authority-coverage-v1-validation-20260617.json`

## Summary

- All checks passed: `True`
- Coverage status: `report_only_no_authority_granted`
- Services covered: `13` / `13`
- Current requests covered: `16` / `16`
- Missing roles: `0`
- Approval granted by coverage: `False`
- External side effects: `False`

## Services

| Service | Risk Family | Authorities | Route | Covered |
| --- | --- | --- | --- | --- |
| `account_registration_intake` | `public_reputation` | `human_user`, `chief_risk_officer` | `human_user_cro_required_review_packet_no_external_action` | `True` |
| `browser_read_only_session` | `wallet_payment_or_real_money` | `requesting_manager`, `chief_risk_officer` | `requesting_manager_and_cro_preflight_only_no_browser_start` | `True` |
| `data_purchase_api_access_gate` | `public_reputation` | `human_user`, `chief_risk_officer` | `human_user_cro_required_review_packet_no_external_action` | `True` |
| `github_public_action_gate` | `public_reputation` | `human_user`, `chief_risk_officer`, `reputation_review_worker` | `human_user_cro_reputation_required_exact_public_action_only` | `True` |
| `legal_kyc_tax_payment_gate` | `public_reputation` | `human_user` | `human_user_cro_or_user_only_decision_packet_no_commitment` | `True` |
| `model_api_execution_gate` | `secrets_or_api` | `human_user`, `chief_risk_officer`, `observability_worker` | `human_user_cro_observability_required_cost_data_scope` | `True` |
| `outreach_delivery_gate` | `public_reputation` | `human_user`, `chief_risk_officer`, `reputation_review_worker` | `human_user_cro_reputation_required_exact_public_action_only` | `True` |
| `public_action_execution` | `wallet_payment_or_real_money` | `human_user`, `chief_risk_officer`, `reputation_review_worker` | `human_user_cro_reputation_required_exact_public_action_only` | `True` |
| `real_money_trade_gate` | `wallet_payment_or_real_money` | `human_user`, `chief_risk_officer` | `human_user_cro_or_user_only_decision_packet_no_commitment` | `True` |
| `secrets_credentials_handling_gate` | `secrets_or_api` | `human_user`, `chief_risk_officer` | `human_user_cro_required_review_packet_no_external_action` | `True` |
| `security_report_submission_gate` | `public_reputation` | `human_user`, `chief_risk_officer` | `human_user_cro_required_review_packet_no_external_action` | `True` |
| `wallet_public_address_response` | `wallet_payment_or_real_money` | `human_user`, `chief_risk_officer` | `human_user_cro_required_wallet_no_key_or_fund_control` | `True` |
| `wallet_setup_packet` | `wallet_payment_or_real_money` | `human_user`, `chief_risk_officer` | `human_user_cro_required_wallet_no_key_or_fund_control` | `True` |

## Boundary

- This report covers authority routes only.
- It does not approve, reject, assign, update, start, browse, call APIs, or perform external actions.
