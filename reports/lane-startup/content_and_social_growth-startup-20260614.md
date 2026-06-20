# content_and_social_growth startup memo and read-only source plan

Date: 2026-06-14
Manager agent: lane-manager-content_and_social_growth-019ec613
Thread: 019ec613-1080-7520-80e3-24dc7cfc31ea
Lane: content_and_social_growth
Task: task-content_and_social_growth-startup-20260614

## Startup context

Required files read:

- E:\agent-company-lab\README.md
- E:\agent-company-lab\reports\manager-packets\content_and_social_growth-manager-packet.md
- E:\agent-company-lab\reports\lane-manager-thread-launch-manifest-latest.md
- E:\agent-company-lab\reports\prompt-eval-review-latest.md

Control-plane state at startup:

- Lane was unowned, then claimed by `lane-manager-content_and_social_growth-019ec613`.
- Lane has one active startup task: `task-content_and_social_growth-startup-20260614`.
- Lane evidence count was 0 before this memo.
- Lane source spec is `content_grok_x_read_only_research`.
- Related Grok/X service request `req-grok-research-worker-20260614` remains `needs_review`; it is not permission to use X, Grok, Radar, browser surfaces, account sessions, or APIs.

## Hard stop

This lane is read-only until a service request is explicitly approved for the exact action scope.

Blocked without exact approval:

- X post, reply, quote, repost, like, follow, DM, list action, bookmark, notification setting, profile edit, account setting, or any other public/account action.
- X, Grok, Radar, or signed-in browser use for discovery.
- Account registration, login changes, API-token use, paid-tool calls, or model/API calls.
- Any public claim, submission, outreach, or action that could notify a third party.
- Work on `submitted_bounty_payouts`, RustChain, Charles, GitHub payout chasing, or any non-content lane.

Allowed now:

- Local planning and local artifact writing.
- Reading the lane packet, launch manifest, prompt safety report, and lane-scoped control-plane rows.
- Defining source plans, capture schemas, scoring rubrics, service-request scopes, and review gates.
- Using non-account public data sources later only if they do not require login, paid access, public interaction, scraping against terms, or browser/account actions.

## Source plan

The lane needs a trend-discovery packet that converts visible trend signals into local candidate rows, not public actions. Every captured item should preserve its source URL, timestamp, query used, visible metrics, and why it might matter to an AI-builder audience.

| Source family | Access mode | Can gather without public action | Requires service request | Blocked actions |
| --- | --- | --- | --- | --- |
| X public posts/search | No use in this startup turn. Future use only through approved read-only request. | If approved: public URL, author handle, timestamp, post text summary, linked sources, visible metrics, reply-gap notes, topic cluster. | Any X browser/API/session use, Grok-backed search, Radar, or signed-in view. | Post, reply, like, follow, DM, repost, quote, bookmark, profile/settings/list action. |
| Grok | No use in this startup turn. Future use only through approved read-only request. | If approved: prompt, output summary, cited URLs, candidate clusters, verification notes, prompt/output artifact. | Any Grok browser/API/session/model use. | Public action, account setting, paid/API action, unsourced claim adoption. |
| X Radar | No use in this startup turn. Future use only through approved read-only request. | If approved: trend labels, topic velocity, representative public posts, visible engagement, watchlist tags. | Any Radar browser/session use. | Public action, feed training, follows, likes, hidden-account operations. |
| Hacker News | Public, non-account sources such as Algolia HN Search API, Firebase item API, RSS, or public story pages. | Story title, URL, points, comment count, submitter, created time, top comment themes, source link, ranking page. | Browser automation only if needed and approved; account use never by default. | Voting, commenting, logging in, contacting users, scraping beyond polite public endpoints. |
| Product Hunt | Public pages, public RSS/feed if available, or official API only if a token and scope are approved. | Product name, tagline, categories, launch date, public votes/comments if visible, maker/public site URL, pricing/positioning notes. | Authenticated API, logged-in pages, or rate-limited automated capture. | Upvote, comment, follow maker/product, submit product, login, notifications. |
| Google Trends-style signals | Public trend pages, RSS-style feeds, or manually supplied exports. | Query/topic, region, timeframe, related queries/topics, trend direction, breakout labels, comparison terms. | Browser automation, account use, or any unofficial collector that triggers consent/captcha/rate-limit issues. | Account actions, paid API, circumvention of bot checks, claims without source timestamp. |
| Cross-source validation | Local normalization over gathered rows. | Compare same topic across HN/Product Hunt/Trends and approved X/Grok/Radar artifacts; mark confidence and contradictions. | None if using local/public artifacts only. | Treating a single engagement spike as proof of durable demand. |

## Candidate row schema

Each trend candidate should be stored locally as Markdown, CSV, JSONL, or SQLite rows with these fields:

- `candidate_id`: stable id from source, timestamp, and normalized topic.
- `source_family`: X, Grok, Radar, HN, Product Hunt, Google Trends-style, or local cross-source.
- `source_url`: canonical public URL or local artifact path.
- `captured_at_utc`: exact capture time.
- `query_or_surface`: search query, feed, ranking page, or prompt label.
- `topic`: short normalized topic.
- `raw_title_or_text_summary`: concise source-backed summary, not copied wholesale.
- `source_actor`: author, submitter, maker, or source account when public.
- `visible_metrics`: points, comments, votes, views, likes, reposts, trend labels, or empty if unavailable.
- `freshness_window`: under 1h, 1-6h, 6-24h, 1-7d, or older.
- `audience_fit`: AI-builder, agent infra, product launch, tooling, policy, business model, or off-lane.
- `evidence_strength`: direct source, multiple sources, anecdotal, metric-only, or weak.
- `content_use`: original post seed, reply target, watchlist, research note, product teardown, or reject.
- `risk_flags`: public-action gated, account-gated, private-data risk, claim-risk, spam-risk, off-lane, duplicate.
- `next_allowed_action`: local draft, local verify, wait for service request, or no action.

## Scoring rubric

Score candidates 0-2 on each dimension:

- Freshness: recent enough to matter to discovery.
- Audience fit: useful to AI builders, agent-company operators, or distribution strategy.
- Evidence density: has source links, metrics, and verifiable details.
- Novelty: offers a non-obvious angle beyond generic AI news.
- Cross-source confirmation: appears in at least two independent surfaces or has one high-authority source.
- Safety: can be discussed without private data, regulated claims, public-action pressure, or platform-rule risk.

High-score candidates can become local draft seeds or watchlist rows. They do not authorize posting, replying, following, or account actions.

## Read-only workflow

1. Create a local capture template under the lane task.
2. Start with non-account, public, low-risk sources: HN public endpoints, public Product Hunt launch pages or feeds, and Google Trends-style public exports.
3. Normalize rows into the candidate schema.
4. Rank with the scoring rubric and separate `draft_seed`, `watchlist`, `needs_verification`, and `reject`.
5. For X/Grok/Radar, wait for an approved service request naming exact scope, account/session boundaries, allowed surfaces, maximum duration, artifact path, and explicit no-public-action gate.
6. If a future packet suggests a public post/reply/follow, route it to brand review and an `x_action_executor` service request. The content manager does not execute it directly.

## Prompt and safety gates

From `prompt-eval-review-latest.md`:

- The active manager prompt passed local static safety evals, but eval success is not permission for model/API, account, wallet, public-action, legal, security, or real-money gates.
- Human reviews and service requests record decisions; they do not bypass the exact-scope approval requirement.
- All lane advances need saved artifacts, reproducible evidence, or explicitly gated next actions.

## First narrow proof task

Next local proof task after startup:

Create a read-only capture template and fill it with 5-10 candidates from non-account public sources only, starting with HN and public Product Hunt/Google Trends-style feeds. Keep X/Grok/Radar rows empty or marked `awaiting_service_request_approval` until an exact approved service request exists.

Expected output path:

- E:\agent-company-lab\data\content-social-trend-discovery\trend-candidate-template-20260614.md

Stop if any source requires login, paid access, account session, browser action, API token, captcha/consent circumvention, public interaction, or cross-lane data.

## Outcome

Status: planned_next_proof
Realized USD: 0

This startup produced a local read-only source plan only. No X, Grok, Radar, browser, account, API, public social, or payout-lane action was taken.
