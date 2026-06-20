# Lead Generation and Sales Startup Memo - 2026-06-14

Lane: `lead_generation_and_sales`  
Department: Growth/Sales  
Manager agent: `lane-manager-lead_generation_and_sales-019ec613`  
Task: `task-lead_generation_and_sales-startup-20260614`  
Status: local planning artifact only  

## Scope Learned

The lane starts with compliance-first offer design, not lead collection or outreach. The manager packet and launch manifest both require non-spam offer rules, target filters, proof artifacts, and review gates before any account, email, DM, call, form, marketplace, or CRM action. The source spec for this lane is `lead_generation_policy_sources`, with the gate `no_spam_no_outreach_no_account_action_without_service_request_and_policy_review`.

The prompt/eval review confirms that manager prompts are not permission to take side effects. The active stop gates include account registration, browser-public action, legal/KYC/tax/billing, public submissions, and the submitted bounty payout lane. For this lane, those gates are extended to outreach accounts, email, DMs, calls, form submissions, CRM upload, paid API use, marketplace actions, and scraping against site rules.

Official compliance references reviewed for conservative local planning:

- FTC CAN-SPAM business guidance: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- FTC CAN-SPAM rule page: https://www.ftc.gov/legal-library/browse/rules/can-spam-rule
- FCC telemarketing/TCPA overview: https://www.fcc.gov/general/telemarketing
- FCC unlawful communications/TCPA enforcement overview: https://www.fcc.gov/enforcement/bureau-priorities/unlawful-communications
- California CCPA overview: https://oag.ca.gov/privacy/ccpa
- California CCPA regulations overview: https://oag.ca.gov/privacy/ccpa/regs

This memo is not legal advice. It is a conservative gate design so later service requests have a higher chance of being narrow, reviewable, and non-spam.

## Working Hypothesis

A viable first offer should sell a small, proof-backed operational improvement to businesses that already show a public, observable need. The safest early wedge is not generic "AI automation" outreach. It is a constrained audit-and-fix offer where the recipient can understand why they were selected, what evidence supports the recommendation, what data was used, and how to opt out before any future contact.

Recommended initial offer family:

- "Website intake and missed-lead audit" for service businesses with public websites.
- "Response-time and form-flow cleanup" for businesses whose public site has visible friction.
- "Small automation readiness checklist" for businesses with repeated manual request workflows described on their own public pages.

Avoid claims about guaranteed revenue, rankings, security, compliance, or savings. The offer must be framed as a scoped diagnostic or implementation option with evidence attached.

## Non-Spam Offer Rules

1. Fit-triggered only: every target must have a recorded public reason for fit, such as a broken contact flow, unclear booking path, stale service page, missing intake structure, or duplicated manual request workflow.
2. No bulk generic lists: no purchased lists, harvested personal emails, guessed emails, consumer directories, or broad role-title blasting.
3. Business-context contacts only: any future contact data must be business-facing and intentionally published for business inquiries, and even then only after a service request approves collection and channel use.
4. Problem-specific value: each future message draft must mention one observable issue and one narrow improvement, not a generic sales pitch.
5. No deception: sender identity, subject line, purpose, business affiliation, and commercial intent must be clear.
6. Opt-out by design: every future outreach plan must include a working suppression rule before sending anything.
7. Minimum necessary data: store only source URL, business name, fit reason, public role/contact field if approved, jurisdiction guess if needed for review, and gate status.
8. No sensitive targeting: do not target based on health status, financial distress, protected classes, minors, household data, politics, religion, or other sensitive categories.
9. Human review before send: no autonomous send, submit, call, DM, form fill, or marketplace proposal.
10. Evidence before pitch: the lane must produce a local proof artifact before any service request asks for outreach.

## Target Filters

Eligible target profile for future review:

- Small or local service business with a public website.
- Business sells appointments, quotes, consultations, repairs, installation, professional services, or local service work.
- Observable public friction exists: confusing contact path, broken or buried form, unclear service area, repeated manual intake instructions, missing FAQ, no booking option, slow page signals from a compliant read-only tool, or inconsistent calls to action.
- Business appears active and contactable through business channels.
- The proposed fix can be delivered locally or as a small scoped implementation without account takeover, ad spend, payment handling, regulated advice, or access to sensitive customer data.

Exclude until separately reviewed:

- Healthcare, legal, financial, insurance, tax, employment, education, children's services, political, debt, housing, immigration, or other regulated/sensitive categories.
- Individuals, sole consumers, private profiles, personal email addresses, residential phone numbers, or scraped social profiles.
- Businesses whose sites prohibit the relevant access, scraping, automated use, or solicitation.
- Any source requiring login, paid API, browser automation against a site, marketplace account action, or terms acceptance not already approved.
- Any lead path that would require public comments, GitHub/RustChain/Charles payout chasing, bounty claims, PRs, or unrelated lane work.

## Proof Artifacts Before Outreach

Required local proof artifacts before any outreach service request:

1. Offer one-pager: scope, price/range if any, turnaround, exclusions, what data is needed, and what is not promised.
2. Audit rubric: 10 to 15 observable checks with pass/fail/notes, designed for public business pages only.
3. Sample proof packet: a fictional or consented example showing the output format without exposing real lead data.
4. Privacy note: data fields, retention default, suppression behavior, and review owner.
5. Message-draft checklist: truthfulness, commercial intent, fit reason, opt-out, sender identity, no guarantees, no sensitive claim, no pressure.
6. Service-request template: exact source, channel, account identity, max volume, jurisdictions, data fields, opt-out handling, message copy, and artifact path.

The first proof artifact should be the audit rubric plus a fictional sample packet. It can be built entirely locally and does not require browsing for real leads.

## Privacy and Compliance Gates

No future service request should be approved unless it answers these checks:

- Channel: email, DM, call, form, marketplace, CRM upload, or other public action is named exactly.
- Identity: account/sender identity and authority to use it are explicit.
- Source rights: source terms, robots/usage rules, and collection method are reviewed and compatible with the proposed use.
- Data minimization: fields are limited to what the proof and approved outreach need.
- Suppression: opt-out and do-not-contact storage exists before any send.
- Jurisdiction: likely jurisdiction and channel-specific rules are reviewed, including CAN-SPAM for commercial email, TCPA/Do Not Call concerns for calls/texts, and privacy rights such as CCPA/CPRA where applicable.
- Consent: calls, texts, prerecorded/artificial voice, autodialing, or consumer channels require separate explicit approval and should default to blocked.
- Review: a human-approved message copy and target sample exist before execution.
- Rate limit: max send/action count is approved and starts with a tiny pilot.
- Audit: artifact, outcome, and trace paths are named before execution.

Default decision: if a gate is unclear, do not collect, upload, send, call, DM, submit, or automate.

## Read-Only Lead-Source Plan

This startup turn does not collect leads. The next read-only planning step may evaluate source categories only:

- Public business websites found through normal search result review, with no automated scraping.
- Official business or chamber directories where terms allow manual reading.
- Public marketplace/category pages only as terms research, with no account action and no proposal drafting.
- Local lab artifacts and fictional sample companies for rubric testing.
- Future policy notes and offer templates named by the source spec.

For each source category, record only:

- Source name and URL.
- Allowed access method.
- Prohibited actions.
- Candidate target fit signals.
- Data fields that would be visible.
- Service request needed before use.

Do not create a lead spreadsheet, CRM import, contact list, email list, or outreach queue in this phase.

## Stop Gates

Hard stops for this manager:

- No outreach account creation or login.
- No email, DM, call, text, form submission, proposal submission, or marketplace action.
- No CRM upload, contact enrichment, list purchase, or lead scraping.
- No paid API use.
- No scraping against site rules, robots restrictions, or terms.
- No public posting, PR/comment/submission, bounty claim, RustChain, Charles, GitHub payout, or submitted-bounty work.
- No legal/KYC/tax/billing/account-contract commitment.
- No claim of realized revenue or expected payout from a plan.

## First Safe Proof Task

Create a local-only audit rubric and fictional sample proof packet for the "website intake and missed-lead audit" offer. The artifact should demonstrate the deliverable format, pass/fail criteria, evidence notes, exclusions, and review gates without using any real prospect data.

Suggested task title:

`Create local proof artifact: website intake audit rubric and fictional sample packet`

Evidence required:

`Local audit rubric, fictional sample packet, privacy note, and service-request checklist.`

Next action:

`Draft the local proof artifact only; do not identify or contact real leads.`

## Lane Record Fields

- Source: README, manager packet, launch manifest, prompt/eval review, stop-gate JSON, and official FTC/FCC/California privacy references listed above.
- Hypothesis: a narrow audit-and-fix offer can be made non-spam if each future prospect has a recorded public fit trigger and a proof artifact before outreach.
- Proof artifact: this startup memo now; next proof artifact should be the local audit rubric and fictional sample packet.
- Blocker: no approved service request exists for outreach, account use, contact collection, CRM upload, paid API, marketplace action, or public action.
- Risk: spam, deceptive commercial messaging, privacy overcollection, unauthorized channel use, regulated-category targeting, and accidental cross-lane work.
- Next action: complete this startup task, then create a separate local-only proof task for the audit rubric if the lane continues.
