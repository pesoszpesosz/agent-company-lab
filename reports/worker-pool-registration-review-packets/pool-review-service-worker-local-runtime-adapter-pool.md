# service-worker-local-runtime-adapter-pool Registration Review

Packet: `pool-review-service-worker-local-runtime-adapter-pool`
Worker type: `local_runtime_adapter`
Role: `observability_worker`
Department: `service_worker_observability`
Current request count: `2`
Priority: `high`
Decision route: `manual_review_register_later`

## Manual Command Preview

```powershell
python E:\agent-company-lab\tools\agent_company.py register-agent --agent-id service-worker-local-runtime-adapter-pool --role-id observability_worker --department-id service_worker_observability
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
