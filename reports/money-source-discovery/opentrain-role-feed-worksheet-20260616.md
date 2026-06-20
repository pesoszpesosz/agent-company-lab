# OpenTrain AI Role-Feed Worksheet

Generated UTC: 2026-06-16T20:38:00Z
Task: `task-opentrain-role-feed-worksheet-20260616`
Lane: `money_source_discovery`
Owner: `lane-manager-money_source_discovery-019ec699`
JSON mirror: `E:\agent-company-lab\reports\money-source-discovery\opentrain-role-feed-worksheet-20260616.json`

## Purpose

Convert the OpenTrain AI public freelancer/feed source into a local, no-side-effect worksheet that a future worker can use to decide whether AI-training contractor work is worth a gated application path.

OpenTrain currently presents itself as a single feed for AI training and data-labeling jobs from 20+ platforms, with filtering by domain, language, pay rate, and platform. Public examples include roles such as math reasoning evaluation, RLHF red teaming, medical data review, code generation QA, legal document analysis, image annotation, physics problem solving, multilingual translation, safety/alignment evaluation, and creative writing judging.

## Source Signals

| Signal | Evidence | Routing Meaning |
| --- | --- | --- |
| Aggregated role feed | Public page says jobs are pulled from 20+ platforms and can be filtered by domain, language, pay rate, and platform. | Treat OpenTrain as source discovery first, not a single employer proof. |
| Role examples show skilled work | Public examples include math, RLHF, medical, code QA, legal, image, physics, language, safety, and writing. | Strong fit for agents that can prepare domain-specific profile packets. |
| Pay examples are hourly | Public page shows sample hourly rates around $28/hr to $70/hr depending on role. | Expected value is plausible, but must be verified per role before application. |
| Account/profile path is central | Public page describes creating a profile and applying/tracking from a dashboard. | Account, contractor, tax/KYC, and assessment gates are mandatory before external action. |
| Work may span third-party platforms | Public page names platforms such as Mercor, Micro1, DataAnnotation, and Outlier. | Each downstream venue needs its own terms/payment/assessment check. |

## Worksheet Rows

| Row | Role Cluster | Public Pay Signal | Skills To Prepare Locally | Gate Burden | Volatility Risk | Local Proof Before Applying | Decision |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | Math reasoning evaluator | Example around `$45/hr`; domain pages show math/RLHF examples at higher ranges. | Algebra, probability, contest-style reasoning, step-by-step rubric writing, LaTeX-style formatting. | Account/profile, possible assessment, contractor/payment terms. | Medium: project availability and qualification can change quickly. | Build a 5-example math reasoning rubric sample pack, no platform upload. | Promote to local sample-pack task. |
| 2 | RLHF red teaming and safety/alignment eval | Example around `$65/hr` to `$70/hr`. | Prompt attack taxonomy, refusal-quality critique, harmful-content policy summarization, structured eval notes. | Account/profile, policy/assessment, possible NDA/contract. | High: trust/safety work may require stricter identity and confidentiality gates. | Create a local red-team evaluation worksheet using synthetic prompts only. | Park behind account/legal review after local sample. |
| 3 | Code generation QA | Example around `$50/hr`. | Python/JS test writing, code review, bug reproduction, concise issue reporting. | Account/profile, coding assessment, payment/tax review. | Medium: strong agent fit, but duplicate with paid-code lane. | Draft a code-QA sample with failing test, fix rationale, and rubric. | Promote to cross-lane proof with `paid_code_bounties`. |
| 4 | Medical/legal document review | Examples around `$55/hr` to `$60/hr`. | Domain literacy, citation discipline, uncertainty marking, no professional-advice claims. | High: domain credential, liability, privacy, contract, and platform gates. | High: may require credentials or strict confidentiality. | Create a credential-free public-document rubric only; do not imply expertise. | Park unless user has relevant credential route. |
| 5 | Image annotation / visual evaluation | Examples around `$20/hr` to `$70/hr`; separate public job page showed visual evaluation range. | Visual QA, labeling consistency, written English, classification/ranking rubric. | Account/profile, assessment, possible 15-20 hour/week commitment. | Medium: easier proof but may be lower margin or time-heavy. | Create local image-eval rubric and time-per-item estimate. | Promote if no higher-value coding/math queue is available. |
| 6 | Multilingual translation / linguistics | Example around `$35/hr`; domain page lists linguistics/language. | Language pair fluency, translation QA, cultural nuance, error taxonomy. | Account/profile, language assessment, residency/payment gates. | Medium-high if language claims cannot be verified. | Only create if a verified language pair exists. | Park pending human skill inventory. |

## Score

| Metric | Score | Notes |
| --- | ---: | --- |
| Expected dollars/hour | 4 | Public examples show credible hourly ranges, but role access is uncertain. |
| Time to first local proof | 5 | Sample rubrics and profile packets can be drafted locally. |
| Gate burden | 4 | Account, contractor terms, tax/KYC/payment, assessments, and downstream platform rules. |
| Repeatability | 4 | Feed model may produce many role attempts once gates clear. |
| Agent fit | 4 | Strong fit for rubric-writing, coding QA, math, and source tracking. |

## Required Approval Gates

- `account_registration_intake`
- `legal_kyc_tax_payment_gate`
- Assessment/contract review before any test, application, dashboard action, identity submission, or payment setup.

## Prohibited Actions

- No OpenTrain account creation.
- No application.
- No profile creation.
- No assessment.
- No identity/tax/payment submission.
- No contractor-term acceptance.
- No downstream platform login.

## Next Action

Create a local `ai-training-sample-pack` task for math reasoning, code QA, and RLHF evaluation samples. Keep all platform/application work parked until account and legal/payment gates are explicitly approved.

## Source URLs

- https://www.opentrain.ai/become-freelancer/
- https://www.opentrain.ai/ai-training-careers/
- https://www.opentrain.ai/jobs/visual-evaluation-specialist--cmpkicvsf003b04k3hgf3ppqp/
- https://www.opentrain.ai/jobs/ai-data-reviewer--cmphrb2yr002004l86molnuw7/

## Boundary

- Browser sessions started: `0`
- Account actions: `false`
- Wallet actions: `false`
- Payment actions: `false`
- Public actions: `false`
- Security testing actions: `false`
- Real-money actions: `false`
- Service requests updated: `0`
- Worker starts: `0`
- External side effects: `false`
