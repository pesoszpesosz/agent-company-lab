# Service Request Checklist

- Request ID: `req-next-wave-security-report-route-review-20260614`
- Service ID: `security_report_submission_gate`
- Validation OK: `true`
- DB request created: `true`

## Missing Required Fields

- None

## Next Action

- Fill missing fields in `intake.json` before requesting worker action.
- Keep all hard gates in `packet.md` intact.
- If complete, create the control-plane service request:

```powershell
python E:\agent-company-lab\tools\agent_company.py create-service-request --request-id req-next-wave-security-report-route-review-20260614 --service-id security_report_submission_gate --request-type security_report_submission --lane-id security_bounty_private_reports --risk-gate "security_report_submission_requires_user_and_cro_approval_no_submission" --requested-action "Review security report submission route readiness for rules_android packet; no report submission." --intake-file E:\agent-company-lab\requests\service-requests\req-next-wave-security-report-route-review-20260614\intake.json --requester-agent-id recovered-profitable-edge-infra
```
