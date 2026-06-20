# Service Request Intake Validator

Generated UTC: 2026-06-14T12:52:00Z

Task: `task-service-request-intake-validator-20260614`

## Purpose

Service requests now have a catalog link and structured intake:

- `service_requests.service_id`
- `service_requests.intake_json`

`create-service-request` can resolve a unique catalog entry from `request_type` or use an explicit `--service-id`. If the service catalog entry has required intake fields, missing fields block request creation. `start-service-request` also revalidates the row before a worker can begin.

## New CLI Surface

```powershell
python E:\agent-company-lab\tools\agent_company.py create-service-request --service-id SERVICE --request-type TYPE --intake-file FILE ...
python E:\agent-company-lab\tools\agent_company.py validate-service-request --request-id REQ
```

## Validation Checks

Negative check:

```powershell
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id req-test-service-intake-missing-20260614 --service-id real_money_trade_gate --request-type real_money_trade --lane-id platform_engineering --requester-agent-id recovered-profitable-edge-infra --risk-gate test_validator_no_external_action --requested-action "Validator negative test: should fail because required intake fields are missing."
```

Result: failed as expected with missing fields:

- `lane_id`
- `venue`
- `instrument_or_market`
- `paper_evidence_artifact`
- `fees_and_depth`
- `max_loss`
- `proposed_capital`
- `kill_switch`

Positive check:

```powershell
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id req-test-service-intake-valid-20260614 --service-id real_money_trade_gate --request-type real_money_trade --lane-id platform_engineering --requester-agent-id recovered-profitable-edge-infra --risk-gate test_validator_no_external_action --requested-action "Validator positive test only: no external action, no real trade, no funds." --intake-file E:\agent-company-lab\evals\service-request-intake-valid-real-money-trade-20260614.json --artifact-path E:\agent-company-lab\reports\service-catalog-latest.md
```

Result:

- request created
- `service_id`: `real_money_trade_gate`
- status: `needs_review`
- `validate-service-request` returned `ok: true`
- missing fields: none
- request was then rejected as a test row with no external action

## Safety Impact

Lane managers can no longer create catalog-backed service requests with only vague prose. Requests for account, wallet, browser, public action, legal/KYC/payment, real-money trading, model/API, outreach, GitHub, security-report, secrets, or paid data/API support now have a path to structured intake before a worker starts.

This still does not approve any external action. It only improves the gate before approval and execution.
