# PromptBase Approval Rubric Local Proof

Generated UTC: 2026-06-18T06:24:22Z
Task: `task-lane-scout-promptbase_agent_skill_route-20260618`
Lane: `digital_products_templates_plugins`

Purpose: convert the Wave 27 do-not-run PromptBase approval packet into a no-browser human-review rubric. This is not a PromptBase browser session, seller account action, payout/tax action, package build, listing draft, upload, submission, or publication.

## Source Packet

- Source: `E:\agent-company-lab\data\digital-products-promptbase-do-not-run-submission-packet-wave27-20260618.json`
- Route: `promptbase_agent_skill_route`
- Product: Agent Skill Starter Kit v0
- Product status: `internal_review_manifest_only`

## Approval Rubric

| Seq | Approval | Gate | Weight | Default | Required Output |
| ---: | --- | --- | ---: | --- | --- |
| 1 | `approval-promptbase-readonly-guideline-review` | `browser_read_only_session` | 30 | `park` | PromptBase guideline mapping report with each package file marked pass, edit-needed, blocked, or not-applicable. |
| 2 | `approval-ip-license-claims-review` | `ip_license_claims_review` | 22 | `park` | IP/license/claims checklist with required copy edits and final human signoff fields. |
| 3 | `approval-seller-terms-fees-payout-review` | `legal_kyc_tax_payment` | 20 | `park` | Legal/payment review memo with explicit proceed, revise, or park recommendation. |
| 4 | `approval-package-build-and-preview-assets` | `package_artifact_publication_review` | 14 | `park` | Package build manifest with zip hash, screenshot paths, and publication readiness result. |
| 5 | `approval-seller-account-and-payout-setup` | `account_payment_approval` | 8 | `park` | Human account setup checklist or parked decision; no automated account action by default. |
| 6 | `approval-public-listing-submission` | `public_action_approval` | 6 | `park` | Public action receipt with URL, timestamp, exact submitted text, asset hashes, and next monitoring step. |

## Review Detail

### `approval-promptbase-readonly-guideline-review`

Recommended sequence: 1
Gate: `browser_read_only_session`
Default decision: `park`
Reason for sequence: It is read-only and resolves the core route-fit uncertainty before account/payment/public work.

Approve only if:
- The operator accepts this exact approval scope.
- Allowed actions are narrow enough to perform without combining unrelated gates.
- Forbidden actions remain explicit and enforceable.
- The required output path and receipt standard are understood.

Revise if:
- The allowed actions are too broad.
- The approval mixes browser, account, payment, package build, or public action scopes.
- The receipt does not prove what happened.

Park if:
- The operator is not ready to review this gate.
- The gate depends on a prior review that is still missing.
- The action could create public, legal, financial, account, or platform obligations.

Still forbidden:
- No account creation or login.
- No form submission, upload, listing creation, marketplace save, checkout, or message.
- No accepting terms, seller onboarding, payout setup, or profile changes.

Service request policy: If approved later, create one separate exact-scope service request with owner, expiry, permitted URLs/actions, forbidden actions, expected receipt, and validation command.

### `approval-ip-license-claims-review`

Recommended sequence: 2
Gate: `ip_license_claims_review`
Default decision: `park`
Reason for sequence: It can mostly stay local and may reduce later public-listing risk.

Approve only if:
- The operator accepts this exact approval scope.
- Allowed actions are narrow enough to perform without combining unrelated gates.
- Forbidden actions remain explicit and enforceable.
- The required output path and receipt standard are understood.

Revise if:
- The allowed actions are too broad.
- The approval mixes browser, account, payment, package build, or public action scopes.
- The receipt does not prove what happened.

Park if:
- The operator is not ready to review this gate.
- The gate depends on a prior review that is still missing.
- The action could create public, legal, financial, account, or platform obligations.

Still forbidden:
- No publication, upload, sale, marketplace submission, or public promotion.
- No legal advice claim or compliance guarantee.

Service request policy: If approved later, create one separate exact-scope service request with owner, expiry, permitted URLs/actions, forbidden actions, expected receipt, and validation command.

### `approval-seller-terms-fees-payout-review`

Recommended sequence: 3
Gate: `legal_kyc_tax_payment`
Default decision: `park`
Reason for sequence: It should happen before seller account or payout setup.

Approve only if:
- The operator accepts this exact approval scope.
- Allowed actions are narrow enough to perform without combining unrelated gates.
- Forbidden actions remain explicit and enforceable.
- The required output path and receipt standard are understood.

Revise if:
- The allowed actions are too broad.
- The approval mixes browser, account, payment, package build, or public action scopes.
- The receipt does not prove what happened.

Park if:
- The operator is not ready to review this gate.
- The gate depends on a prior review that is still missing.
- The action could create public, legal, financial, account, or platform obligations.

Still forbidden:
- No entering legal identity, tax data, payout account, card, bank, wallet, or KYC information.
- No agreeing to terms or creating seller obligations.
- No real-money transaction.

Service request policy: If approved later, create one separate exact-scope service request with owner, expiry, permitted URLs/actions, forbidden actions, expected receipt, and validation command.

### `approval-package-build-and-preview-assets`

Recommended sequence: 4
Gate: `package_artifact_publication_review`
Default decision: `park`
Reason for sequence: It prepares local artifacts only after route/IP/legal checks are clearer.

Approve only if:
- The operator accepts this exact approval scope.
- Allowed actions are narrow enough to perform without combining unrelated gates.
- Forbidden actions remain explicit and enforceable.
- The required output path and receipt standard are understood.

Revise if:
- The allowed actions are too broad.
- The approval mixes browser, account, payment, package build, or public action scopes.
- The receipt does not prove what happened.

Park if:
- The operator is not ready to review this gate.
- The gate depends on a prior review that is still missing.
- The action could create public, legal, financial, account, or platform obligations.

Still forbidden:
- No upload, public link, marketplace draft, external storage, or publication.
- No screenshots from signed-in marketplace pages.

Service request policy: If approved later, create one separate exact-scope service request with owner, expiry, permitted URLs/actions, forbidden actions, expected receipt, and validation command.

### `approval-seller-account-and-payout-setup`

Recommended sequence: 5
Gate: `account_payment_approval`
Default decision: `park`
Reason for sequence: It creates account/payment exposure and should wait for legal/payment clarity.

Approve only if:
- The operator accepts this exact approval scope.
- Allowed actions are narrow enough to perform without combining unrelated gates.
- Forbidden actions remain explicit and enforceable.
- The required output path and receipt standard are understood.

Revise if:
- The allowed actions are too broad.
- The approval mixes browser, account, payment, package build, or public action scopes.
- The receipt does not prove what happened.

Park if:
- The operator is not ready to review this gate.
- The gate depends on a prior review that is still missing.
- The action could create public, legal, financial, account, or platform obligations.

Still forbidden:
- No credentials, OTPs, cookies, tax/KYC data, payout data, or account settings handled by an agent unless a later exact-scope approval says so.
- No accepting agreements without human confirmation.

Service request policy: If approved later, create one separate exact-scope service request with owner, expiry, permitted URLs/actions, forbidden actions, expected receipt, and validation command.

### `approval-public-listing-submission`

Recommended sequence: 6
Gate: `public_action_approval`
Default decision: `park`
Reason for sequence: It is a public-action gate and should be last.

Approve only if:
- The operator accepts this exact approval scope.
- Allowed actions are narrow enough to perform without combining unrelated gates.
- Forbidden actions remain explicit and enforceable.
- The required output path and receipt standard are understood.

Revise if:
- The allowed actions are too broad.
- The approval mixes browser, account, payment, package build, or public action scopes.
- The receipt does not prove what happened.

Park if:
- The operator is not ready to review this gate.
- The gate depends on a prior review that is still missing.
- The action could create public, legal, financial, account, or platform obligations.

Still forbidden:
- No price, claim, refund term, support promise, promotion, cross-post, message, or follow-up outside the approved text and scope.
- No mutation of other marketplace/account settings.

Service request policy: If approved later, create one separate exact-scope service request with owner, expiry, permitted URLs/actions, forbidden actions, expected receipt, and validation command.

## Operator Decision Form

Decision schema: `promptbase_approval_rubric.operator_decision.v1`

Allowed decisions:
- `approve_exact_scope`
- `revise_scope`
- `park`

Required fields:
- `approval_id`
- `decision`
- `operator_name_or_initials`
- `decision_utc`
- `exact_scope`
- `expiry_utc`
- `forbidden_actions_confirmed`
- `expected_receipt`
- `next_validation_command`

Invalid broad decisions:
- Approve all marketplace work.
- Go create the account and publish.
- Use whatever browser steps are needed.
- Handle payment/tax setup if it appears.

## Recommended Next Approval

`approval-promptbase-readonly-guideline-review`

If the operator wants to proceed, review only the read-only guideline approval first and convert it into one exact-scope service request; keep account, payment, package build, listing, upload, submission, worker/runtime, model/MCP, and public actions blocked.

## Boundary

No browser session, account, login, terms acceptance, payment/payout/KYC/tax action, zip, upload, marketplace draft, submission, publication, public promotion, service-request mutation, worker/runtime start, dependency install, model/MCP call, or external side effect occurred.
