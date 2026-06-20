# Service Request Checklist

- Request ID: `req-test-browser-readonly-missing-20260614`
- Service ID: `browser_read_only_session`
- Validation OK: `false`
- DB request created: `false`

## Missing Required Fields

- `target_url`
- `allowed_read_scope`
- `forbidden_actions`
- `evidence_needed`
- `session_sensitivity`

## Next Action

- Fill missing fields in `intake.json` before requesting worker action.
- Keep all hard gates in `packet.md` intact.
- If complete, create the control-plane service request:

```powershell
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id req-test-browser-readonly-missing-20260614 --service-id browser_read_only_session --request-type browser_research --lane-id content_and_social_growth --risk-gate "catalog_required_approval_no_external_action" --requested-action "Read-only capture acceptance test; no browser opened." --intake-file E:\agent-company-lab\requests\service-requests\req-test-browser-readonly-missing-20260614\intake.json
```
