# Service Worker Bureau Catalog

Generated UTC: 2026-06-14T12:46:44Z
Source definition: `E:\agent-company-lab\architecture\service-catalog-draft.json`

## Purpose

This catalog is the company service desk for side-effect-adjacent work. Lane managers use it to create precise service requests for registration, wallet, browser, public-action, outreach, model/API, legal/KYC/payment, security-report, trading, and secret-handling needs.

The catalog does not approve actions. A real side effect still needs a `service_requests` row plus an exact approved scope.

## Source-Backed Design Signals

- Temporal's human-in-the-loop AI workflow docs show a pattern where risky actions pause for approval by signal, wait without consuming compute, use durable timers, and preserve an audit trail: https://docs.temporal.io/ai-cookbook/human-in-the-loop-python
- LangGraph interrupts pause execution with persisted state and warn that side effects before an interrupt must be idempotent: https://docs.langchain.com/oss/python/langgraph/interrupts
- MCP security best practices emphasize consent, authorization, access controls, and privacy-aware tool/resource design: https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
- OpenAI Agents SDK guardrail docs distinguish agent-level input/output guardrails from per-function-tool guardrails and note that handoffs do not pass through the normal function-tool guardrail pipeline: https://openai.github.io/openai-agents-python/guardrails/

## Counts

- Services in report: `13`
- By status: `{"available": 10, "gated": 3}`
- By request type: `{"account_registration": 1, "browser_research": 1, "data_purchase_api_access": 1, "github_public_action": 1, "legal_kyc_tax_payment": 1, "model_api_execution": 1, "outreach_delivery": 1, "public_action_execution": 1, "real_money_trade": 1, "secrets_credentials_handling": 1, "security_report_submission": 1, "wallet_public_address_or_payment_reply": 1, "wallet_setup": 1}`
- By owner role: `{"account_registration_worker": 1, "browser_action_worker": 2, "chief_risk_officer": 5, "observability_worker": 1, "reputation_review_worker": 2, "wallet_ops_worker": 2}`

## Operating Rule

Managers may ask service workers to prepare packets, read public documentation, inspect non-sensitive browser state, and write local checklists. They must stop before account creation, identity verification, terms acceptance, payments, credential entry, public posting, bounty/report submission, wallet transactions, or real-money trades unless a specific service request has been approved.

## Service Index

| Service | Request Type | Owner Role | Department | Status | Purpose |
| --- | --- | --- | --- | --- | --- |
| `account_registration_intake` - Account Registration Intake | account_registration | `account_registration_worker` | Service Bureau/Identity | available | Prepare a local registration packet for a venue without creating the account or accepting terms. |
| `browser_read_only_session` - Browser Read-Only Session | browser_research | `browser_action_worker` | Service Bureau/Browser | available | Inspect public or already-approved signed-in browser state and capture evidence without posting or changing settings. |
| `data_purchase_api_access_gate` - Data Purchase/API Access Gate | data_purchase_api_access | `chief_risk_officer` | Service Bureau/Platform | available | Review paid APIs, premium data, scraped data, or restricted sources before a lane depends on them. |
| `github_public_action_gate` - GitHub Public Action Gate | github_public_action | `reputation_review_worker` | Service Bureau/Reputation | gated | Review PRs, issue comments, bounty claims, advisory comments, and maintainer-facing GitHub actions before public execution. |
| `legal_kyc_tax_payment_gate` - Legal/KYC/Tax/Payment Gate Review | legal_kyc_tax_payment | `chief_risk_officer` | Service Bureau/Risk | available | Summarize legal, KYC, tax, billing, payment, and account-contract obligations before the user decides. |
| `model_api_execution_gate` - Model/API Execution Gate | model_api_execution | `observability_worker` | Service Bureau/Platform | available | Approve and observe real model/API executions after dry-runs pass and cost/data scope is explicit. |
| `outreach_delivery_gate` - Outreach Delivery Gate | outreach_delivery | `reputation_review_worker` | Service Bureau/Reputation | available | Review and gate outbound email, DM, proposal, marketplace, or form-contact actions for non-spam and brand safety. |
| `public_action_execution` - Public Action Execution | public_action_execution | `browser_action_worker` | Service Bureau/Public Actions | gated | Execute one exact approved public action, such as a reply, post, PR comment, bounty claim, proposal submission, or form submission. |
| `real_money_trade_gate` - Real-Money Trade Gate | real_money_trade | `chief_risk_officer` | Service Bureau/Treasury | available | Evaluate whether a paper-only market or trading hypothesis is even eligible for real-money consideration. |
| `secrets_credentials_handling_gate` - Secrets/Credentials Handling Gate | secrets_credentials_handling | `chief_risk_officer` | Service Bureau/Risk | available | Define how a task can use credentials, tokens, API keys, private files, cookies, or session state without leaking or storing sensitive data. |
| `security_report_submission_gate` - Security Report Submission Gate | security_report_submission | `chief_risk_officer` | Service Bureau/Risk | available | Gate private vulnerability reports, advisory submissions, and program contacts after local-only proof work. |
| `wallet_public_address_response` - Wallet Public Address Response | wallet_public_address_or_payment_reply | `wallet_ops_worker` | Service Bureau/Wallet | gated | Prepare or verify the exact public payment-address response for payout collection after user approval. |
| `wallet_setup_packet` - Wallet Setup Packet | wallet_setup | `wallet_ops_worker` | Service Bureau/Wallet | available | Prepare wallet requirements, network/token details, custody choices, and user action checklist without controlling keys or funds. |

## Detail

### account_registration_intake

- Name: Account Registration Intake
- Request type: `account_registration`
- Owner role: `account_registration_worker`
- Department: `Service Bureau/Identity`
- Status: `available`
- Purpose: Prepare a local registration packet for a venue without creating the account or accepting terms.
- Notes: Use for bounty marketplaces, grant portals, hackathon sites, lead-gen tools, broker venues, and research APIs.
- Allowed preparation:
  - Read public signup, pricing, eligibility, and terms pages.
  - List required fields, identity checks, account owner choices, and account-use constraints.
  - Draft a user checklist and recommended account posture.
  - Record blockers and expected value before asking the user to act.
- Hard gates:
  - Do not create accounts.
  - Do not accept legal terms or platform policies.
  - Do not enter personal data, OTPs, payment details, tax details, or KYC information.
  - Do not change existing account settings.
- Required intake:
  - `lane_id`
  - `venue_url`
  - `business_reason`
  - `expected_value`
  - `deadline`
  - `requested_account_owner`
  - `needed_capabilities`
- Approval required by:
  - `user`
  - `chief_risk_officer`
- Output artifacts:
  - `registration-intake-packet.md`
  - `terms-and-eligibility-snapshot.md`
  - `blocker-note.md`

### browser_read_only_session

- Name: Browser Read-Only Session
- Request type: `browser_research`
- Owner role: `browser_action_worker`
- Department: `Service Bureau/Browser`
- Status: `available`
- Purpose: Inspect public or already-approved signed-in browser state and capture evidence without posting or changing settings.
- Notes: Use for X/Grok/Radar/Gemini/public site inspection only after the request is explicit.
- Allowed preparation:
  - Open public pages and read visible information.
  - Use signed-in pages only when the service request names the site and allowed read scope.
  - Capture screenshots, URLs, DOM text, and local notes.
  - Stop if a page requires credentials, OTP, consent, payment, account settings, or private data.
- Hard gates:
  - Do not click submit, publish, apply, buy, trade, follow, like, reply, repost, withdraw, deposit, connect wallet, or save settings.
  - Do not enter credentials, OTPs, payment details, personal data, or wallet signatures.
  - Do not bypass rate limits, paywalls, access controls, or platform rules.
- Required intake:
  - `lane_id`
  - `target_url`
  - `allowed_read_scope`
  - `forbidden_actions`
  - `evidence_needed`
  - `session_sensitivity`
- Approval required by:
  - `requesting_manager`
  - `chief_risk_officer`
- Output artifacts:
  - `browser-readonly-capture.md`
  - `screenshots`
  - `blocker-note.md`

### data_purchase_api_access_gate

- Name: Data Purchase/API Access Gate
- Request type: `data_purchase_api_access`
- Owner role: `chief_risk_officer`
- Department: `Service Bureau/Platform`
- Status: `available`
- Purpose: Review paid APIs, premium data, scraped data, or restricted sources before a lane depends on them.
- Notes: Applies to market data, lead data, social data, security feeds, and paid SaaS APIs.
- Allowed preparation:
  - Read public API documentation, pricing, usage limits, terms, and data license.
  - Check whether free/public/local alternatives are enough.
  - Write a cost, license, and integration packet.
- Hard gates:
  - Do not create API keys, subscribe, attach payment methods, purchase credits, or agree to data licenses.
  - Do not scrape against robots, terms, login gates, or rate limits.
  - Do not store or redistribute restricted datasets without explicit permission.
- Required intake:
  - `lane_id`
  - `data_source_url`
  - `needed_fields`
  - `cadence`
  - `expected_value`
  - `estimated_cost`
  - `license_or_terms_url`
- Approval required by:
  - `user`
  - `chief_risk_officer`
- Output artifacts:
  - `data-api-access-review.md`
  - `cost-license-summary.md`
  - `alternative-source-note.md`

### github_public_action_gate

- Name: GitHub Public Action Gate
- Request type: `github_public_action`
- Owner role: `reputation_review_worker`
- Department: `Service Bureau/Reputation`
- Status: `gated`
- Purpose: Review PRs, issue comments, bounty claims, advisory comments, and maintainer-facing GitHub actions before public execution.
- Notes: This exists specifically to prevent repeating broad low-attribution PR/comment behavior.
- Allowed preparation:
  - Check duplicate PRs/issues, assignment rules, bounty claim rules, maintainer sentiment, and code quality evidence.
  - Review patch/test artifact and public-action draft.
  - Recommend submit, revise, or park.
- Hard gates:
  - Do not open PRs, comment, claim bounties, submit advisories, or contact maintainers.
  - Do not touch the submitted bounty payout lane owned by the parallel worker.
  - Do not use low-quality automated submissions or duplicate active work.
- Required intake:
  - `lane_id`
  - `repo_url`
  - `issue_or_bounty_url`
  - `draft_action`
  - `patch_or_report_artifact`
  - `duplicate_check`
  - `payout_rules`
- Approval required by:
  - `user`
  - `chief_risk_officer`
  - `reputation_review_worker`
- Output artifacts:
  - `github-public-action-review.md`
  - `duplicate-check.md`
  - `submission-draft.md`

### legal_kyc_tax_payment_gate

- Name: Legal/KYC/Tax/Payment Gate Review
- Request type: `legal_kyc_tax_payment`
- Owner role: `chief_risk_officer`
- Department: `Service Bureau/Risk`
- Status: `available`
- Purpose: Summarize legal, KYC, tax, billing, payment, and account-contract obligations before the user decides.
- Notes: This is the default escalation for account, payment, and identity commitments.
- Allowed preparation:
  - Read public terms, privacy, fee, payout, tax, and eligibility pages.
  - Identify commitments, documents, payments, personal data, and jurisdiction constraints.
  - Write a decision packet with risks, alternatives, and user-only actions.
  - Mark unresolved blockers in the service request.
- Hard gates:
  - Do not accept terms, sign contracts, upload identity documents, enter tax forms, attach payment methods, subscribe, deposit, or withdraw.
  - Do not provide legal, tax, or financial advice as a substitute for professional review.
  - Do not proceed when obligations are unclear.
- Required intake:
  - `lane_id`
  - `venue_url`
  - `action_requested`
  - `jurisdiction_if_relevant`
  - `funds_or_payout_involved`
  - `deadline`
- Approval required by:
  - `user`
- Output artifacts:
  - `legal-kyc-tax-payment-review.md`
  - `terms-snapshot.md`
  - `user-decision-checklist.md`

### model_api_execution_gate

- Name: Model/API Execution Gate
- Request type: `model_api_execution`
- Owner role: `observability_worker`
- Department: `Service Bureau/Platform`
- Status: `available`
- Purpose: Approve and observe real model/API executions after dry-runs pass and cost/data scope is explicit.
- Notes: Matches the existing gated Pydantic AI adapter request.
- Allowed preparation:
  - Run local dry-runs and static evals without paid API calls.
  - Estimate cost, model/provider, input data sensitivity, output artifact path, and allowed lanes.
  - Add prompt version, eval dataset, run metadata, and trace expectations.
  - Block real execution until request status is approved.
- Hard gates:
  - Do not make paid or external model/API calls without approved provider, model, max cost, data scope, lane scope, and artifact path.
  - Do not send secrets, private keys, credentials, unpublished vulnerabilities, or sensitive personal data to external models.
  - Do not enable autonomous tool execution beyond the approved scope.
- Required intake:
  - `lane_id`
  - `provider`
  - `model`
  - `max_cost_usd`
  - `data_scope`
  - `allowed_tools`
  - `prompt_version_id`
  - `eval_run_id`
  - `output_artifact_path`
- Approval required by:
  - `user`
  - `chief_risk_officer`
  - `observability_worker`
- Output artifacts:
  - `model-api-execution-plan.md`
  - `cost-estimate.md`
  - `trace-report.md`
  - `eval-report.md`

### outreach_delivery_gate

- Name: Outreach Delivery Gate
- Request type: `outreach_delivery`
- Owner role: `reputation_review_worker`
- Department: `Service Bureau/Reputation`
- Status: `available`
- Purpose: Review and gate outbound email, DM, proposal, marketplace, or form-contact actions for non-spam and brand safety.
- Notes: Use for lead-generation and freelance marketplaces after local proof artifacts exist.
- Allowed preparation:
  - Review offer clarity, recipient fit, public-source legitimacy, unsubscribe/opt-out handling, and volume limits.
  - Draft outreach text and a send/no-send recommendation.
  - Check whether a platform account or marketplace action also needs account registration approval.
- Hard gates:
  - Do not send emails, DMs, contact forms, proposals, marketplace messages, or bulk outreach.
  - Do not scrape or upload contact lists against source rules.
  - Do not target sensitive or regulated categories without explicit policy review.
  - Do not impersonate the user or claim credentials/results not proven by artifacts.
- Required intake:
  - `lane_id`
  - `recipient_source`
  - `targeting_reason`
  - `exact_message_draft`
  - `volume`
  - `opt_out_plan`
  - `proof_artifact`
- Approval required by:
  - `user`
  - `chief_risk_officer`
  - `reputation_review_worker`
- Output artifacts:
  - `outreach-review.md`
  - `message-draft.md`
  - `send-list-audit.md`

### public_action_execution

- Name: Public Action Execution
- Request type: `public_action_execution`
- Owner role: `browser_action_worker`
- Department: `Service Bureau/Public Actions`
- Status: `gated`
- Purpose: Execute one exact approved public action, such as a reply, post, PR comment, bounty claim, proposal submission, or form submission.
- Notes: This is intentionally gated. Lane managers should prefer draft artifacts first.
- Allowed preparation:
  - Preflight the exact action text, destination, account, and user-approved scope.
  - Capture before/after evidence.
  - Execute only the named action and stop immediately after proof capture.
  - Record public URL or submission receipt when available.
- Hard gates:
  - Do not improvise text, targets, recipients, wallet addresses, attachments, or claims.
  - Do not perform follow-up actions without a new approval.
  - Do not submit legal, KYC, payment, or tax commitments.
  - Do not execute if account, route, or source rules are unclear.
- Required intake:
  - `lane_id`
  - `account_or_profile`
  - `exact_destination_url`
  - `exact_action_text`
  - `approved_scope`
  - `rollback_or_correction_plan`
  - `reputation_review_artifact`
- Approval required by:
  - `user`
  - `chief_risk_officer`
  - `reputation_review_worker`
- Output artifacts:
  - `public-action-preflight.md`
  - `public-action-proof.md`
  - `receipt-or-url.txt`

### real_money_trade_gate

- Name: Real-Money Trade Gate
- Request type: `real_money_trade`
- Owner role: `chief_risk_officer`
- Department: `Service Bureau/Treasury`
- Status: `available`
- Purpose: Evaluate whether a paper-only market or trading hypothesis is even eligible for real-money consideration.
- Notes: Applies to prediction markets, brokers, crypto venues, and local trading systems.
- Allowed preparation:
  - Review paper-trade evidence, fees, liquidity, settlement rules, account eligibility, and kill-switch criteria.
  - Calculate maximum loss, capital lockup, and operational blockers.
  - Produce a no-trade or user-decision packet.
- Hard gates:
  - Do not place, cancel, or modify real-money orders.
  - Do not deposit, withdraw, transfer, borrow, lend, or pledge funds.
  - Do not connect broker, exchange, or prediction-market APIs for trading.
  - Do not treat paper edge as tradable without explicit user approval and capital limits.
- Required intake:
  - `lane_id`
  - `venue`
  - `instrument_or_market`
  - `paper_evidence_artifact`
  - `fees_and_depth`
  - `max_loss`
  - `proposed_capital`
  - `kill_switch`
- Approval required by:
  - `user`
  - `chief_risk_officer`
- Output artifacts:
  - `real-money-trade-gate-review.md`
  - `paper-evidence-summary.md`
  - `no-trade-note.md`

### secrets_credentials_handling_gate

- Name: Secrets/Credentials Handling Gate
- Request type: `secrets_credentials_handling`
- Owner role: `chief_risk_officer`
- Department: `Service Bureau/Risk`
- Status: `available`
- Purpose: Define how a task can use credentials, tokens, API keys, private files, cookies, or session state without leaking or storing sensitive data.
- Notes: Use before any worker touches credentials, cookies, API keys, private repos, or account sessions.
- Allowed preparation:
  - Inventory what secret class is needed and whether a safer read-only alternative exists.
  - Define environment-variable, vault, browser-profile, or user-mediated access requirements.
  - Write a secret-minimization and redaction plan.
- Hard gates:
  - Do not ask the user to paste secrets into chat.
  - Do not write secrets, cookies, OTPs, seed phrases, or private keys to repo files or reports.
  - Do not exfiltrate session data or bypass platform authentication.
  - Do not run tools that would expose sensitive files outside the approved scope.
- Required intake:
  - `lane_id`
  - `secret_type`
  - `why_needed`
  - `least_privilege_scope`
  - `storage_plan`
  - `redaction_plan`
  - `expiration_or_rotation_plan`
- Approval required by:
  - `user`
  - `chief_risk_officer`
- Output artifacts:
  - `secret-handling-plan.md`
  - `redaction-checklist.md`
  - `blocked-secret-note.md`

### security_report_submission_gate

- Name: Security Report Submission Gate
- Request type: `security_report_submission`
- Owner role: `chief_risk_officer`
- Department: `Service Bureau/Risk`
- Status: `available`
- Purpose: Gate private vulnerability reports, advisory submissions, and program contacts after local-only proof work.
- Notes: Security lane managers should use this before any report/submission action.
- Allowed preparation:
  - Review program scope, safe-harbor language, allowed testing, duplicate policy, and report route.
  - Check proof artifact for minimization and non-destructive reproduction.
  - Draft a private report packet and unresolved-risk list.
- Hard gates:
  - Do not perform live testing beyond allowed read-only public code review.
  - Do not submit reports, emails, advisories, or comments.
  - Do not include exploit details in public channels.
  - Do not proceed if scope, impact, or disclosure route is unclear.
- Required intake:
  - `lane_id`
  - `program_url`
  - `scope_evidence`
  - `vulnerability_artifact`
  - `impact_assessment`
  - `safe_harbor_text`
  - `submission_route`
- Approval required by:
  - `user`
  - `chief_risk_officer`
- Output artifacts:
  - `security-report-gate-review.md`
  - `scope-snapshot.md`
  - `private-report-draft.md`

### wallet_public_address_response

- Name: Wallet Public Address Response
- Request type: `wallet_public_address_or_payment_reply`
- Owner role: `wallet_ops_worker`
- Department: `Service Bureau/Wallet`
- Status: `gated`
- Purpose: Prepare or verify the exact public payment-address response for payout collection after user approval.
- Notes: Useful for payout collection, but the parallel submitted-payout worker owns the active GitHub payout lane.
- Allowed preparation:
  - Check requested chain, token, network, memo/tag, and deadline.
  - Compare requested format against the user-provided public address or payment instruction.
  - Draft the exact response text for user review.
  - Record payout-request evidence and follow-up reminders.
- Hard gates:
  - Do not invent or choose a wallet address.
  - Do not publish or send payment details without exact approval.
  - Do not expose private keys, seed phrases, exchange credentials, or sensitive identity details.
  - Do not interact with funds.
- Required intake:
  - `lane_id`
  - `payout_source_url`
  - `requested_chain`
  - `requested_token`
  - `user_provided_public_address`
  - `exact_destination`
  - `deadline`
- Approval required by:
  - `user`
  - `chief_risk_officer`
- Output artifacts:
  - `payment-address-response-draft.md`
  - `payout-request-snapshot.md`
  - `approval-proof.md`

### wallet_setup_packet

- Name: Wallet Setup Packet
- Request type: `wallet_setup`
- Owner role: `wallet_ops_worker`
- Department: `Service Bureau/Wallet`
- Status: `available`
- Purpose: Prepare wallet requirements, network/token details, custody choices, and user action checklist without controlling keys or funds.
- Notes: Use for Web3 grants, hackathons, airdrops, bounty payouts, and venue eligibility checks.
- Allowed preparation:
  - Read public wallet, network, faucet, grant, airdrop, or payout requirements.
  - List supported chains, tokens, address formats, fees, deadlines, and risk notes.
  - Draft a user-owned custody plan and verification checklist.
  - Verify public transactions or addresses only after the user provides them.
- Hard gates:
  - Do not generate, store, request, or expose seed phrases or private keys.
  - Do not sign messages or transactions.
  - Do not connect a wallet, move funds, bridge assets, claim rewards, deploy contracts, or approve token allowances.
  - Do not tell a public venue a payment address without a separate exact approval.
- Required intake:
  - `lane_id`
  - `program_url`
  - `network`
  - `token_or_asset`
  - `wallet_action_needed`
  - `deadline`
  - `funds_or_identity_required`
- Approval required by:
  - `user`
  - `chief_risk_officer`
- Output artifacts:
  - `wallet-requirements-packet.md`
  - `custody-risk-note.md`
  - `public-address-verification.md`

