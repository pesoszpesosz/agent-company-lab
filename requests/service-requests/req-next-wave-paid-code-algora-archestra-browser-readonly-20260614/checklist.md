# Service Request Checklist

- Request ID: `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614`
- Service ID: `browser_read_only_session`
- Validation OK: `true`
- DB request created: `true`

## Missing Required Fields

- None

## Next Action

- Fill missing fields in `intake.json` before requesting worker action.
- Keep all hard gates in `packet.md` intact.
- If complete, create the control-plane service request:

```powershell
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id req-next-wave-paid-code-algora-archestra-browser-readonly-20260614 --service-id browser_read_only_session --request-type browser_research --lane-id paid_code_bounties --risk-gate "catalog_required_approval_no_external_action" --requested-action "Read public Algora/GitHub issue state for archestra-ai/archestra#3218; no GitHub public action." --intake-file E:\agent-company-lab\requests\service-requests\req-next-wave-paid-code-algora-archestra-browser-readonly-20260614\intake.json --requester-agent-id recovered-profitable-edge-infra
```
