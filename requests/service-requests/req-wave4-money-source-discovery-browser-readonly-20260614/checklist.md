# Service Request Checklist

- Request ID: `req-wave4-money-source-discovery-browser-readonly-20260614`
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
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id req-wave4-money-source-discovery-browser-readonly-20260614 --service-id browser_read_only_session --request-type browser_research --lane-id money_source_discovery --risk-gate "catalog_required_approval_no_external_action" --requested-action "Read public opportunity-source directories and capture monetizable source candidates; no browser side effects." --intake-file E:\agent-company-lab\requests\service-requests\req-wave4-money-source-discovery-browser-readonly-20260614\intake.json --requester-agent-id recovered-profitable-edge-infra
```
