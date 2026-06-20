# Service Request Checklist

- Request ID: `req-test-browser-readonly-complete-20260614`
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
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id req-test-browser-readonly-complete-20260614 --service-id browser_read_only_session --request-type browser_research --lane-id content_and_social_growth --risk-gate "catalog_required_approval_no_external_action" --requested-action "Generate complete read-only browser service packet acceptance test; no browser opened." --intake-file E:\agent-company-lab\requests\service-requests\req-test-browser-readonly-complete-20260614\intake.json --requester-agent-id recovered-profitable-edge-infra
```
