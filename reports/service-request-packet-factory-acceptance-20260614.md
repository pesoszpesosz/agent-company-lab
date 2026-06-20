# Service Request Packet Factory Acceptance Report

Generated UTC: 2026-06-14

Task: `task-service-request-packet-factory-implementation-20260614`

## Implementation

Added `scaffold-service-request` to `E:\agent-company-lab\tools\agent_company.py`.

The command generates local-only packet folders from the existing catalog-backed service definitions:

- `intake.json`
- `packet.md`
- `checklist.md`
- `metadata.json`

It registers each generated packet as a `service_request_packet` artifact and writes a `service_request_packet_scaffolded` trace event. It does not approve, assign, start, or complete service work.

## Acceptance Results

### Compile

Command:

```powershell
python -m py_compile E:\agent-company-lab\tools\agent_company.py
```

Result: pass.

### Incomplete Intake Packet

Command generated packet:

```powershell
python E:\agent-company-lab\tools\agent_company.py scaffold-service-request --request-id req-test-browser-readonly-missing-20260614 --service-id browser_read_only_session --lane-id content_and_social_growth --requester-agent-id test-manager --task-id task-service-request-packet-factory-implementation-20260614 --requested-action "Read-only capture acceptance test; no browser opened." --output-dir E:\agent-company-lab\requests\service-requests
```

Result: pass.

- Packet directory: `E:\agent-company-lab\requests\service-requests\req-test-browser-readonly-missing-20260614`
- `validation_ok`: false
- Missing fields: `target_url`, `allowed_read_scope`, `forbidden_actions`, `evidence_needed`, `session_sensitivity`
- `db_request_created`: false
- Unknown requester agent warning recorded without DB foreign-key failure.

### Complete Intake With DB Request

Prefill fixture:

`E:\agent-company-lab\evals\service-request-packet-prefill-browser-readonly-complete-20260614.json`

Command generated packet and service request:

```powershell
python E:\agent-company-lab\tools\agent_company.py scaffold-service-request --request-id req-test-browser-readonly-complete-20260614 --service-id browser_read_only_session --lane-id content_and_social_growth --requester-agent-id recovered-profitable-edge-infra --task-id task-service-request-packet-factory-implementation-20260614 --requested-action "Generate complete read-only browser service packet acceptance test; no browser opened." --prefill-file E:\agent-company-lab\evals\service-request-packet-prefill-browser-readonly-complete-20260614.json --output-dir E:\agent-company-lab\requests\service-requests --create-db-request
```

Result: pass.

- Packet directory: `E:\agent-company-lab\requests\service-requests\req-test-browser-readonly-complete-20260614`
- `validation_ok`: true
- Missing fields: none
- DB request status: `needs_review`
- Generated files: `intake.json`, `packet.md`, `checklist.md`, `metadata.json`
- `packet.md` contains catalog hard gates and non-approval notice.

Validation command:

```powershell
python E:\agent-company-lab\tools\agent_company.py validate-service-request --request-id req-test-browser-readonly-complete-20260614
```

Result: pass, `ok: true`, `request_status: needs_review`.

### Mismatched Service Type Negative Test

Command:

```powershell
python E:\agent-company-lab\tools\agent_company.py scaffold-service-request --request-id req-test-mismatch-20260614 --service-id browser_read_only_session --request-type real_money_trade --lane-id content_and_social_growth --requested-action "Should fail" --output-dir E:\agent-company-lab\requests\service-requests
```

Result: pass. Command failed as expected with request type mismatch.

### Unapproved Start Negative Test

Command:

```powershell
python E:\agent-company-lab\tools\agent_company.py start-service-request --request-id req-test-browser-readonly-complete-20260614 --agent-id recovered-profitable-edge-infra --artifact-path E:\agent-company-lab\requests\service-requests\req-test-browser-readonly-complete-20260614\packet.md --decision-note "Intentional acceptance test: should not start without approval."
```

Result: pass. Command failed as expected because request is still `needs_review`.

## Safety Result

No browser was opened. No account, wallet, payment, public post, PR/comment, API call, credential handling, or real-money action was performed. The complete request remains `needs_review` and unstarted.

## Follow-Up

The packet factory now requires a lane-expansion step before it can generate starter packets under the new Wave-4 lane IDs, because `scaffold-service-request` correctly refuses unknown lanes. Next action: add controlled DB lane creation for `money_source_discovery`, `ai_ml_competitions`, and `digital_products_templates_plugins`, or generate their starter packets under `platform_engineering` as launch-prep artifacts.
