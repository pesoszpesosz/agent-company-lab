# Gate Checklist Template

Use this checklist before an agent moves from local drafting to any action with account, money, reputation, legal, or platform consequences.

Task: `{{task_id}}`  
Lane: `{{lane_id}}`  
Artifact: `{{artifact_path}}`  
Reviewer: `{{reviewer_or_service_request}}`  

## Gate Summary

| Gate | Status | Evidence | Required approval |
| --- | --- | --- | --- |
| Lane ownership | {{allowed_blocked_or_review}} | {{owner_and_task}} | {{approval_if_needed}} |
| Account creation/login | blocked by default | {{site_or_account}} | account registration/service request |
| Terms acceptance | blocked by default | {{terms_source}} | legal/account review |
| Marketplace listing/upload | blocked by default | {{platform_and_listing}} | public-action and listing review |
| Payment/payout/tax/KYC | blocked by default | {{payment_requirement}} | legal/KYC/tax/payment gate |
| Purchase/sale/real money | blocked by default | {{money_flow}} | user approval and payment gate |
| Public post/comment/message | blocked by default | {{channel_and_copy}} | public-action or outreach gate |
| Browser side effect | blocked by default | {{browser_action}} | approved browser/public-action request |
| Model/API execution | blocked unless scoped | {{provider_model_cost}} | model/API execution gate |
| Paid data/API access | blocked unless scoped | {{data_source_cost_terms}} | data/API access gate |
| Credentials/secrets/private files | blocked by default | {{secret_or_private_data}} | secrets handling gate |
| IP/license/trademark | review required | {{asset_or_brand}} | IP/license review |
| Sensitive/regulatory domain | review required | {{domain}} | legal/risk review |
| Cross-lane work | blocked by default | {{other_lane}} | reassignment from owner |

## Approval Rule

If any row is `blocked`, `unknown`, or `review required`, the agent stops at a local artifact and records the exact next service request. A broad instruction to move fast is not approval.

## Notes

- {{note_1}}
- {{note_2}}
- {{note_3}}
