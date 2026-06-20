# Lead Generation and Sales - Source Category Policy Review

Date: 2026-06-14  
Lane: `lead_generation_and_sales`  
Manager agent: `lane-manager-lead_generation_and_sales-019ec613`  
Task: `task-leadgen-source-category-policy-review-20260614`  
Artifact status: local-only policy proof  
Real prospect data: none  
Contacts collected: none  
Public action: none  
Realized USD: 0  

## Boundary Statement

This artifact reviews source categories only. It does not identify, collect, enrich, rank, contact, message, scrape, upload, or submit anything about real leads or real companies. It is a local policy proof for future lead-discovery governance.

Hard stops:

- No real contacts or real lead list.
- No scraping or browser automation against websites.
- No outreach, email, DM, call, text, form submission, proposal, marketplace action, or CRM upload.
- No account login, account creation, paid API, data broker, list vendor, or enrichment provider.
- No `submitted_bounty_payouts`, RustChain, Charles, GitHub payout, PR/comment, claim, or public action.

## Review Standard

Every possible future lead source gets one of four statuses:

- `allowed_local_only`: usable now for fictional samples, templates, policies, and internal proof artifacts.
- `requires_service_request`: potentially usable later, but only after approval for exact source, access method, data fields, and channel.
- `prohibited_default`: blocked unless the user creates a specialized reviewed exception.
- `out_of_lane`: not lead generation and sales work.

Default rule: when source rights, data rights, channel rules, or target category are unclear, mark the source `prohibited_default`.

## Source Category Matrix

| Source Category | Status | What May Be Done Now | What Is Blocked | Future Gate |
| --- | --- | --- | --- | --- |
| Fictional companies and sample data | `allowed_local_only` | Create rubric examples, mock proof packets, policy templates, and service-request templates. | Treating fictional examples as real prospects. | None if clearly labeled fictional. |
| Internal lane artifacts | `allowed_local_only` | Reuse prior startup memo, fictional audit rubric, and local policy notes. | Turning notes into real contact lists. | None for local review. |
| Own portfolio, demo pages, or consented test pages | `requires_service_request` | Policy design only until approval confirms ownership/consent. | Contact extraction, claims, screenshots for outreach, or public use without approval. | Consent/ownership evidence and artifact scope. |
| Public business websites | `requires_service_request` | Define criteria for future manual review. | Browsing real prospects, scraping, contact collection, emails, calls, DMs, or CRM rows. | Exact source scope, manual access method, fields, excluded categories, message/use plan. |
| Search engine result pages | `requires_service_request` | Define query rules and exclusion filters locally. | Automated result scraping, bulk collection, contact capture, or ranking real businesses. | Search method, max volume, no-scrape assurance, data fields, retention. |
| Official chamber or local business directories | `requires_service_request` | Review category type generically. | Copying member lists, scraping, contact harvest, or outreach. | Directory terms review, manual-read limit, allowed data fields. |
| Government business registries | `prohibited_default` | Note as a possible regulated/public-record category only. | Lead generation from registries, personal/officer data use, bulk download, contact extraction. | Specialized privacy/legal review before any use. |
| Review platforms and map listings | `prohibited_default` | Policy discussion only. | Scraping listings/reviews, extracting phones/emails, profile claiming, messages, reviews, or public edits. | Exact platform terms, anti-scraping review, account/action approval. |
| Social platforms | `prohibited_default` | Policy discussion only. | Scraping profiles, DMs, follows, likes, comments, account use, personal-data collection. | Separate approved service request for read-only research or action. |
| Freelance marketplaces | `requires_service_request` | Review possible offer fit and policy needs locally. | Account login, proposal drafting/submission, messages, bids, profile changes. | Marketplace terms, account identity, exact action scope. |
| Public GitHub repositories/issues | `out_of_lane` | None for this lead-gen task. | PRs, comments, bounty claims, payout chasing, maintainer contact. | Route to the appropriate non-leadgen lane only if assigned. |
| Data brokers and purchased lists | `prohibited_default` | None. | Buying, importing, renting, enriching, or using lists. | Do not use by default. |
| Email guessing or pattern generation | `prohibited_default` | None. | Guessing addresses, validating addresses, or sending to guessed contacts. | Do not use by default. |
| Contact enrichment tools | `prohibited_default` | None. | Enrichment, lookup, verification, phone/email append, paid API use. | Specialized approval with privacy/legal review. |
| Contact forms as outbound channel | `prohibited_default` | None. | Submitting sales pitches through forms. | Exact approval required; default remains blocked. |
| CRM or spreadsheet imports | `requires_service_request` | Define schema locally with fictional rows only. | Uploading or storing real leads. | Privacy review, data fields, retention, suppression, owner. |

## Allowed Local Data Fields

For this phase, the lane may store only policy-level fields and fictional examples:

- Source category name.
- Category status.
- Rationale.
- Allowed local use.
- Blocked action.
- Future service-request gates.
- Fictional company name using `.example`, `.invalid`, or clearly invented labels.

Do not store:

- Real business names.
- Real domains.
- Real email addresses.
- Real phone numbers.
- Real social handles.
- Real contact names.
- Real addresses.
- Personal data.
- Scraped fields.
- CRM rows.

## Future Real-Source Minimum Data Schema

If a future approved service request permits real-source review, start with this minimum schema and no more:

| Field | Purpose | Gate |
| --- | --- | --- |
| `source_url` | Trace where the public fit signal was seen. | Source terms reviewed. |
| `business_name` | Identify the business only within the approved review set. | Business-context source only. |
| `business_category` | Check inclusion/exclusion rules. | Exclude sensitive categories. |
| `fit_trigger` | Explain why the business might benefit. | Must be observable and non-sensitive. |
| `rubric_summary` | Link to local proof criteria. | No private data. |
| `source_rights_status` | Record allowed/prohibited/unclear. | Unclear means stop. |
| `contact_channel_status` | Record whether channel is approved. | No channel defaults to blocked. |
| `suppression_status` | Prevent re-contact where applicable. | Required before outreach. |

Fields still blocked by default:

- Personal names.
- Direct personal emails.
- Personal phones.
- Social profiles.
- Customer details.
- Health, finance, legal, family, household, political, religious, or protected-class attributes.
- Any inferred sensitive trait.

## Source-Rights Checklist

Before a future source is used for real lead discovery, answer:

1. Is the source public without login?
2. Do the source terms allow the proposed access method?
3. Does the source disallow scraping, automated access, reuse, marketing, or commercial solicitation?
4. Is the access manual, rate-limited, and low volume?
5. Are only business-context pages reviewed?
6. Are excluded regulated/sensitive categories filtered out before data capture?
7. Is the exact data schema approved?
8. Is there a retention and deletion rule?
9. Is there a suppression/opt-out rule before any outreach?
10. Is the channel approved separately from source review?

If any answer is unknown or no, stop and do not collect data.

## Data Handling Gates

Data minimization:

- Collect only what the approved task needs.
- Keep notes at the source-category level until a service request allows real-source review.
- Avoid personal data even when visible.

Retention:

- Fictional/local policy artifacts may remain in the lab.
- Real-source review artifacts need a retention date and deletion owner.
- Rejected or unclear-source rows should be deleted or reduced to non-identifying category notes.

Suppression:

- Any future outreach path needs a do-not-contact/suppression mechanism before sending.
- Suppression records should store only the minimum needed to prevent re-contact.

Audit:

- Every real-source phase needs artifact, outcome, and trace rows.
- Trace metadata should state `api_calls`, `public_actions`, `real_prospect_data`, and `approved_service_request`.

## Channel Separation

Source review is not outreach approval.

Approval to read a source does not approve:

- Email.
- DM.
- Call or text.
- Contact form submission.
- Marketplace proposal.
- CRM upload.
- Account use.
- Paid API use.
- Public comments or posts.

Each channel needs its own exact service-request scope.

## Prohibited Target Categories

Do not build future lead discovery around:

- Healthcare, therapy, dental, patient services, medical devices, or wellness claims.
- Legal, tax, finance, insurance, debt, credit, investment, lending, accounting, employment, housing, education, immigration, or political work.
- Children's services, minors, schools, family status, household targeting, or sensitive personal situations.
- Emergency services or safety-critical operations.
- Any category where the offer would imply legal, security, medical, financial, compliance, or guaranteed business outcomes.

## Approved Future Source Review Shape

A safe future source-review task should look like:

```text
Task:
Source category:
Exact source examples:
Access method:
Max pages/items:
Allowed fields:
Excluded categories:
Terms/robots review:
No-outreach statement:
No-account statement:
Retention:
Suppression:
Artifact path:
Trace metadata:
```

It should not include message sending, lead export, contact enrichment, CRM upload, or account use.

## Policy Decision

Current local-only allowed sources:

- Fictional examples.
- Existing local lane artifacts.
- Generic source-category policy templates.

All real-source categories are blocked until an approved service request names exact scope and data handling. Data brokers, purchased lists, email guessing, contact enrichment, social scraping, map/review scraping, and contact-form pitching are prohibited by default.

## Outcome

This artifact satisfies the local source-category policy review requirement. It creates no revenue, no lead list, no real contacts, and no external action.

Recommended next action:

If the lane continues, draft a service-request template for a future tiny manual source-category review. Keep it separate from outreach, and keep real prospect data blocked unless explicitly approved.
