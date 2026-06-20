# service-worker-browser-read-only-pool Registration Review

Packet: `pool-review-service-worker-browser-read-only-pool`
Worker type: `browser_read_only`
Role: `browser_action_worker`
Department: `service_worker_browser_operations`
Current request count: `7`
Priority: `high`
Decision route: `manual_review_register_later`

## Manual Command Preview

```powershell
python E:\agent-company-lab\tools\agent_company.py register-agent --agent-id service-worker-browser-read-only-pool --role-id browser_action_worker --department-id service_worker_browser_operations
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
- Does the pool require signed-in browser state, and how is session safety verified?
