# service-worker-legal-kyc-payment-review-pool Registration Review

Packet: `pool-review-service-worker-legal-kyc-payment-review-pool`
Worker type: `legal_kyc_tax_payment_review`
Role: `chief_risk_officer`
Department: `service_worker_risk_review`
Current request count: `1`
Priority: `medium`
Decision route: `manual_review_register_later`

## Manual Command Preview

```powershell
python E:\agent-company-lab\tools\agent_company.py register-agent --agent-id service-worker-legal-kyc-payment-review-pool --role-id chief_risk_officer --department-id service_worker_risk_review
```

## Must Not Do

- `do_not_execute_command_preview`
- `do_not_register_pool_without_manual_user_decision`
- `do_not_assign_service_requests`
- `do_not_start_workers`
- `do_not_open_browser_or_use_accounts`
- `do_not_touch_wallet_payment_kyc_tax_or_legal_commitments`
- `do_not_call_model_or_external_api`

## Review Questions

- Is this pool needed before the next approved service request?
- Who is allowed to own this pool if registered?
- What exact approval scope must exist before assignment?
- What user/CRO/reputation review evidence is required before any public or commitment-adjacent action?
