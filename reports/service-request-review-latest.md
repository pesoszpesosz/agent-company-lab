# Service Request Review Queue

Generated UTC: 2026-06-15T10:14:55Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
JSON mirror: `E:\agent-company-lab\reports\service-request-review-latest.json`

## Operating Rule

This report is read-only review infrastructure. It does not approve, assign, start, submit, browse, register, trade, spend, post, or contact anyone.

A service request may move only through explicit CLI lifecycle commands with exact scope, reviewer, assignee, and proof artifact. `needs_review` means blocked.

## Counts

- Requests in report: `14`
- By status: `{"complete": 1, "needs_review": 11, "rejected": 2}`
- By lane: `{"ai_ml_competitions": 1, "content_and_social_growth": 1, "digital_products_templates_plugins": 3, "money_source_discovery": 1, "paid_code_bounties": 1, "platform_engineering": 5, "security_bounty_private_reports": 2}`
- By service/request type: `{"browser_read_only_session": 7, "legal_kyc_tax_payment_gate": 1, "lifecycle_test": 2, "model_api_execution": 1, "real_money_trade_gate": 1, "research_enrichment": 1, "security_report_submission_gate": 1}`

## Review Index

| Status | Request | Lane | Service | Validation | Approval Scope | Recommended Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| `needs_review` | `req-next-wave-digital-legal-payment-review-20260614` | `digital_products_templates_plugins` | `legal_kyc_tax_payment_gate` | ok | missing | Review as signed-in browser research only; no posts, likes, follows, replies, profile/account settings, or public actions. |
| `needs_review` | `req-next-wave-digital-marketplace-browser-readonly-20260614` | `digital_products_templates_plugins` | `browser_read_only_session` | ok | missing | Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions. |
| `needs_review` | `req-next-wave-security-google-oss-vrp-browser-readonly-20260614` | `security_bounty_private_reports` | `browser_read_only_session` | ok | missing | Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions. |
| `needs_review` | `req-next-wave-paid-code-algora-archestra-browser-readonly-20260614` | `paid_code_bounties` | `browser_read_only_session` | ok | missing | Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions. |
| `needs_review` | `req-next-wave-security-report-route-review-20260614` | `security_bounty_private_reports` | `security_report_submission_gate` | ok | missing | Review with user, chief_risk_officer; if approved, record exact scope before assignment or start. |
| `needs_review` | `req-wave4-money-source-discovery-browser-readonly-20260614` | `money_source_discovery` | `browser_read_only_session` | ok | missing | Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions. |
| `needs_review` | `req-wave4-ai-ml-competitions-browser-readonly-20260614` | `ai_ml_competitions` | `browser_read_only_session` | ok | missing | Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions. |
| `needs_review` | `req-wave4-digital-products-browser-readonly-20260614` | `digital_products_templates_plugins` | `browser_read_only_session` | ok | missing | Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions. |
| `needs_review` | `req-test-browser-readonly-complete-20260614` | `content_and_social_growth` | `browser_read_only_session` | ok | missing | Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions. |
| `needs_review` | `req-pydantic-ai-model-backed-adapter-20260614` | `platform_engineering` | `model_api_execution` | missing: lane_id, provider, model, max_cost_usd, data_scope, allowed_tools, prompt_version_id, eval_run_id, output_artif | present | Fill or regenerate the intake packet before review; missing: lane_id, provider, model, max_cost_usd, data_scope, allowed_tools, prompt_version_id, eval_run_id, output_artifact_path. |
| `needs_review` | `req-grok-research-worker-20260614` | `platform_engineering` | `research_enrichment` | ok | present | Review as signed-in browser research only; no posts, likes, follows, replies, profile/account settings, or public actions. |
| `complete` | `req-test-lifecycle-approve-20260614` | `platform_engineering` | `lifecycle_test` | ok | present | No action; keep as completed evidence. |
| `rejected` | `req-test-service-intake-valid-20260614` | `platform_engineering` | `real_money_trade_gate` | ok | missing | No action; keep closed unless a new request is scaffolded with a different scope. |
| `rejected` | `req-test-lifecycle-reject-20260614` | `platform_engineering` | `lifecycle_test` | ok | missing | No action; keep closed unless a new request is scaffolded with a different scope. |

## Detail

### req-next-wave-digital-legal-payment-review-20260614

- Status: `needs_review`
- Lane: `digital_products_templates_plugins`
- Department: Product Studio
- Service: `legal_kyc_tax_payment_gate` Legal/KYC/Tax/Payment Gate Review
- Request type: `legal_kyc_tax_payment`
- Owner role: `chief_risk_officer`
- Risk gate: legal_kyc_tax_payment_requires_user_decision_no_commitment
- Requested action: Review legal/KYC/tax/payment/payout/account-contract gates for Agent Skill Starter Kit marketplace route; no commitments.
- Validation: `ok`
- Missing fields: none
- Required intake: lane_id, venue_url, action_requested, jurisdiction_if_relevant, funds_or_payout_involved, deadline
- Approval required by: user
- Approval scope present: `False`
- Assigned agent: ``
- Artifact path: `E:\agent-company-lab\requests\service-requests\req-next-wave-digital-legal-payment-review-20260614\packet.md`
- Decision note: 
- Recommended next action: Review as signed-in browser research only; no posts, likes, follows, replies, profile/account settings, or public actions.

### req-next-wave-digital-marketplace-browser-readonly-20260614

- Status: `needs_review`
- Lane: `digital_products_templates_plugins`
- Department: Product Studio
- Service: `browser_read_only_session` Browser Read-Only Session
- Request type: `browser_research`
- Owner role: `browser_action_worker`
- Risk gate: catalog_required_approval_no_external_action
- Requested action: Read public digital marketplace terms/fees/listing requirements for Agent Skill Starter Kit route; no browser side effects.
- Validation: `ok`
- Missing fields: none
- Required intake: lane_id, target_url, allowed_read_scope, forbidden_actions, evidence_needed, session_sensitivity
- Approval required by: requesting_manager, chief_risk_officer
- Approval scope present: `False`
- Assigned agent: ``
- Artifact path: `E:\agent-company-lab\requests\service-requests\req-next-wave-digital-marketplace-browser-readonly-20260614\packet.md`
- Decision note: 
- Recommended next action: Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions.

### req-next-wave-security-google-oss-vrp-browser-readonly-20260614

- Status: `needs_review`
- Lane: `security_bounty_private_reports`
- Department: Security Research
- Service: `browser_read_only_session` Browser Read-Only Session
- Request type: `browser_research`
- Owner role: `browser_action_worker`
- Risk gate: catalog_required_approval_no_external_action
- Requested action: Read public Google OSS VRP rendered rules/scope/submission route for rules_android; no account or submission action.
- Validation: `ok`
- Missing fields: none
- Required intake: lane_id, target_url, allowed_read_scope, forbidden_actions, evidence_needed, session_sensitivity
- Approval required by: requesting_manager, chief_risk_officer
- Approval scope present: `False`
- Assigned agent: ``
- Artifact path: `E:\agent-company-lab\requests\service-requests\req-next-wave-security-google-oss-vrp-browser-readonly-20260614\packet.md`
- Decision note: 
- Recommended next action: Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions.

### req-next-wave-paid-code-algora-archestra-browser-readonly-20260614

- Status: `needs_review`
- Lane: `paid_code_bounties`
- Department: Cashflow Engineering
- Service: `browser_read_only_session` Browser Read-Only Session
- Request type: `browser_research`
- Owner role: `browser_action_worker`
- Risk gate: catalog_required_approval_no_external_action
- Requested action: Read public Algora/GitHub issue state for archestra-ai/archestra#3218; no GitHub public action.
- Validation: `ok`
- Missing fields: none
- Required intake: lane_id, target_url, allowed_read_scope, forbidden_actions, evidence_needed, session_sensitivity
- Approval required by: requesting_manager, chief_risk_officer
- Approval scope present: `False`
- Assigned agent: ``
- Artifact path: `E:\agent-company-lab\requests\service-requests\req-next-wave-paid-code-algora-archestra-browser-readonly-20260614\packet.md`
- Decision note: 
- Recommended next action: Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions.

### req-next-wave-security-report-route-review-20260614

- Status: `needs_review`
- Lane: `security_bounty_private_reports`
- Department: Security Research
- Service: `security_report_submission_gate` Security Report Submission Gate
- Request type: `security_report_submission`
- Owner role: `chief_risk_officer`
- Risk gate: security_report_submission_requires_user_and_cro_approval_no_submission
- Requested action: Review security report submission route readiness for rules_android packet; no report submission.
- Validation: `ok`
- Missing fields: none
- Required intake: lane_id, program_url, scope_evidence, vulnerability_artifact, impact_assessment, safe_harbor_text, submission_route
- Approval required by: user, chief_risk_officer
- Approval scope present: `False`
- Assigned agent: ``
- Artifact path: `E:\agent-company-lab\requests\service-requests\req-next-wave-security-report-route-review-20260614\packet.md`
- Decision note: 
- Recommended next action: Review with user, chief_risk_officer; if approved, record exact scope before assignment or start.

### req-wave4-money-source-discovery-browser-readonly-20260614

- Status: `needs_review`
- Lane: `money_source_discovery`
- Department: Strategic Research
- Service: `browser_read_only_session` Browser Read-Only Session
- Request type: `browser_research`
- Owner role: `browser_action_worker`
- Risk gate: catalog_required_approval_no_external_action
- Requested action: Read public opportunity-source directories and capture monetizable source candidates; no browser side effects.
- Validation: `ok`
- Missing fields: none
- Required intake: lane_id, target_url, allowed_read_scope, forbidden_actions, evidence_needed, session_sensitivity
- Approval required by: requesting_manager, chief_risk_officer
- Approval scope present: `False`
- Assigned agent: ``
- Artifact path: `E:\agent-company-lab\requests\service-requests\req-wave4-money-source-discovery-browser-readonly-20260614\packet.md`
- Decision note: 
- Recommended next action: Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions.

### req-wave4-ai-ml-competitions-browser-readonly-20260614

- Status: `needs_review`
- Lane: `ai_ml_competitions`
- Department: Competition Lab
- Service: `browser_read_only_session` Browser Read-Only Session
- Request type: `browser_research`
- Owner role: `browser_action_worker`
- Risk gate: catalog_required_approval_no_external_action
- Requested action: Read public AI/ML competition listings and capture rules/prize/dataset gates; no browser side effects.
- Validation: `ok`
- Missing fields: none
- Required intake: lane_id, target_url, allowed_read_scope, forbidden_actions, evidence_needed, session_sensitivity
- Approval required by: requesting_manager, chief_risk_officer
- Approval scope present: `False`
- Assigned agent: ``
- Artifact path: `E:\agent-company-lab\requests\service-requests\req-wave4-ai-ml-competitions-browser-readonly-20260614\packet.md`
- Decision note: 
- Recommended next action: Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions.

### req-wave4-digital-products-browser-readonly-20260614

- Status: `needs_review`
- Lane: `digital_products_templates_plugins`
- Department: Product Studio
- Service: `browser_read_only_session` Browser Read-Only Session
- Request type: `browser_research`
- Owner role: `browser_action_worker`
- Risk gate: catalog_required_approval_no_external_action
- Requested action: Read public digital-product marketplace pages and capture product opportunity signals; no browser side effects.
- Validation: `ok`
- Missing fields: none
- Required intake: lane_id, target_url, allowed_read_scope, forbidden_actions, evidence_needed, session_sensitivity
- Approval required by: requesting_manager, chief_risk_officer
- Approval scope present: `False`
- Assigned agent: ``
- Artifact path: `E:\agent-company-lab\requests\service-requests\req-wave4-digital-products-browser-readonly-20260614\packet.md`
- Decision note: 
- Recommended next action: Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions.

### req-test-browser-readonly-complete-20260614

- Status: `needs_review`
- Lane: `content_and_social_growth`
- Department: Audience/Distribution
- Service: `browser_read_only_session` Browser Read-Only Session
- Request type: `browser_research`
- Owner role: `browser_action_worker`
- Risk gate: catalog_required_approval_no_external_action
- Requested action: Generate complete read-only browser service packet acceptance test; no browser opened.
- Validation: `ok`
- Missing fields: none
- Required intake: lane_id, target_url, allowed_read_scope, forbidden_actions, evidence_needed, session_sensitivity
- Approval required by: requesting_manager, chief_risk_officer
- Approval scope present: `False`
- Assigned agent: ``
- Artifact path: `E:\agent-company-lab\requests\service-requests\req-test-browser-readonly-complete-20260614\packet.md`
- Decision note: 
- Recommended next action: Review for exact read-only scope with requesting_manager, chief_risk_officer; if approved, assign to a browser worker and stop at login, consent, payment, private data, or public actions.

### req-pydantic-ai-model-backed-adapter-20260614

- Status: `needs_review`
- Lane: `platform_engineering`
- Department: Platform Engineering
- Service: ``
- Request type: `model_api_execution`
- Owner role: ``
- Risk gate: model_api_call_requires_provider_model_cost_lane_and_artifact_scope
- Requested action: Run a real model-backed Pydantic AI adapter only after provider, model, max cost, allowed lanes, output artifact path, and credential route are explicitly approved.
- Validation: `missing`
- Missing fields: lane_id, provider, model, max_cost_usd, data_scope, allowed_tools, prompt_version_id, eval_run_id, output_artifact_path
- Required intake: none
- Approval required by: not cataloged
- Approval scope present: `True`
- Assigned agent: ``
- Artifact path: `E:\agent-company-lab\reports\worker-runtime\pydantic-ai-eval-latest.md`
- Decision note: 
- Recommended next action: Fill or regenerate the intake packet before review; missing: lane_id, provider, model, max_cost_usd, data_scope, allowed_tools, prompt_version_id, eval_run_id, output_artifact_path.

### req-grok-research-worker-20260614

- Status: `needs_review`
- Lane: `platform_engineering`
- Department: Platform Engineering
- Service: ``
- Request type: `research_enrichment`
- Owner role: ``
- Risk gate: browser_grok_or_x_requires_signed_in_browser_and_no_public_actions
- Requested action: Later run Grok/X research prompts for current agent-company infrastructure trends; save prompt/output/verification artifacts; do not post, like, follow, or reply.
- Validation: `ok`
- Missing fields: none
- Required intake: none
- Approval required by: not cataloged
- Approval scope present: `True`
- Assigned agent: ``
- Artifact path: `E:\agent-company-lab\notes\research-log-20260614.md`
- Decision note: 
- Recommended next action: Review as signed-in browser research only; no posts, likes, follows, replies, profile/account settings, or public actions.

### req-test-lifecycle-approve-20260614

- Status: `complete`
- Lane: `platform_engineering`
- Department: Platform Engineering
- Service: ``
- Request type: `lifecycle_test`
- Owner role: ``
- Risk gate: test_no_external_action
- Requested action: Dummy lifecycle approval/start/complete test; no browser, account, wallet, public, or money action.
- Validation: `ok`
- Missing fields: none
- Required intake: none
- Approval required by: not cataloged
- Approval scope present: `True`
- Assigned agent: `recovered-profitable-edge-infra`
- Artifact path: `E:\agent-company-lab\reports\source-research-refresh-20260614.md`
- Decision note: Completed lifecycle verification; unapproved start was blocked, approval path completed, rejection path recorded.
- Recommended next action: No action; keep as completed evidence.

### req-test-service-intake-valid-20260614

- Status: `rejected`
- Lane: `platform_engineering`
- Department: Platform Engineering
- Service: `real_money_trade_gate` Real-Money Trade Gate
- Request type: `real_money_trade`
- Owner role: `chief_risk_officer`
- Risk gate: test_validator_no_external_action
- Requested action: Validator positive test only: no external action, no real trade, no funds.
- Validation: `ok`
- Missing fields: none
- Required intake: lane_id, venue, instrument_or_market, paper_evidence_artifact, fees_and_depth, max_loss, proposed_capital, kill_switch
- Approval required by: user, chief_risk_officer
- Approval scope present: `False`
- Assigned agent: ``
- Artifact path: `E:\agent-company-lab\reports\service-catalog-latest.md`
- Decision note: Validator positive-path test completed; no external action required or allowed.
- Recommended next action: No action; keep closed unless a new request is scaffolded with a different scope.

### req-test-lifecycle-reject-20260614

- Status: `rejected`
- Lane: `platform_engineering`
- Department: Platform Engineering
- Service: ``
- Request type: `lifecycle_test`
- Owner role: ``
- Risk gate: test_no_external_action
- Requested action: Dummy lifecycle rejection test; no browser, account, wallet, public, or money action.
- Validation: `ok`
- Missing fields: none
- Required intake: none
- Approval required by: not cataloged
- Approval scope present: `False`
- Assigned agent: ``
- Artifact path: ``
- Decision note: Lifecycle rejection-path test. No external action required or allowed.
- Recommended next action: No action; keep closed unless a new request is scaffolded with a different scope.

