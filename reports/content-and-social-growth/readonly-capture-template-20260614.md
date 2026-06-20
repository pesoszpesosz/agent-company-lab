# content_and_social_growth read-only capture template

Date: 2026-06-14
Task: task-content-social-readonly-capture-template-20260614
Manager agent: lane-manager-content_and_social_growth-019ec613
Artifact type: local proof fixture
Realized USD: 0

## Boundary

This artifact is a local template and fixture set only. It does not contain live X, Grok, Radar, browser, signed-in, API, or public-action research.

Blocked unless a service request is approved for the exact scope:

- X, Grok, Radar, signed-in browser, account session, or API use.
- Posting, replying, quoting, reposting, liking, following, unfollowing, bookmarking, DMs, list changes, profile edits, account settings, notifications, or feed-training actions.
- Any outreach, public comment, submission, or action that could notify another account.
- Work on `submitted_bounty_payouts`, RustChain, Charles, GitHub payout chasing, platform engineering execution, or any other lane.

Allowed use of this template:

- Normalize non-account, public, read-only source observations into local rows.
- Keep X/Grok/Radar surfaces represented as schema fields while marking them `awaiting_service_approval`.
- Score candidates for local planning only.
- Route any future public action candidate to brand review and an approved executor service request.

## Capture fields

Use one row per source observation or candidate.

| Field | Required | Notes |
| --- | --- | --- |
| `candidate_id` | yes | Stable id from source family, topic slug, and capture date. |
| `captured_at_utc` | yes | Exact capture time for real rows; fixture rows use `fixture`. |
| `source_family` | yes | `hacker_news`, `product_hunt`, `google_trends_style`, `x_public`, `grok`, `x_radar`, or `cross_source`. |
| `source_surface` | yes | Feed/search/query/prompt/page label. |
| `service_gate_status` | yes | `open_public_readonly`, `awaiting_service_approval`, `blocked`, or `approved_readonly`. |
| `source_url_or_artifact` | yes | Public URL, local artifact path, or `fixture://...` for fixture rows. |
| `source_actor` | no | Author, submitter, maker, company, or blank if not applicable. |
| `topic` | yes | Normalized topic or pattern. |
| `raw_title_or_text_summary` | yes | Short paraphrase; do not copy long source text. |
| `visible_metrics` | no | Public points/comments/votes/views/likes/etc. Leave blank when gated. |
| `age_hours` | no | Numeric when known. |
| `weighted_engagement` | no | For X-style rows only when metrics are visible and approved: likes + 2*replies + 2*reposts + 3*quotes + bookmarks. |
| `velocity_score` | no | Weighted engagement divided by max(age_hours, 1), or local source equivalent. |
| `audience_fit` | yes | `ai_builder`, `agent_infra`, `product_launch`, `tooling`, `workflow`, `policy`, `business_model`, or `off_lane`. |
| `evidence_strength` | yes | `fixture`, `direct_source`, `multi_source`, `metric_only`, `anecdotal`, or `weak`. |
| `reply_gap_signal` | no | `unknown`, `none`, `possible`, or `strong`; never approval by itself. |
| `content_use` | yes | `draft_seed`, `watchlist`, `reply_target_pending_gate`, `source_candidate`, `pattern_note`, or `reject`. |
| `risk_flags` | yes | Semicolon-separated flags such as `public_action_gated`, `account_gated`, `claim_risk`, `hype_risk`, `off_lane`, `fixture_only`. |
| `next_allowed_action` | yes | Local-only next step, or `await_service_request_approval`. |
| `approval_required` | yes | `none_for_local`, `service_request_for_readonly`, `brand_review`, or `executor_service_request`. |
| `notes` | no | Short operational note. |

## CSV header

```csv
candidate_id,captured_at_utc,source_family,source_surface,service_gate_status,source_url_or_artifact,source_actor,topic,raw_title_or_text_summary,visible_metrics,age_hours,weighted_engagement,velocity_score,audience_fit,evidence_strength,reply_gap_signal,content_use,risk_flags,next_allowed_action,approval_required,notes
```

## Fixture rows

These rows are local fixtures, not live research. They prove the schema and gating behavior.

| candidate_id | captured_at_utc | source_family | source_surface | service_gate_status | source_url_or_artifact | source_actor | topic | raw_title_or_text_summary | visible_metrics | age_hours | weighted_engagement | velocity_score | audience_fit | evidence_strength | reply_gap_signal | content_use | risk_flags | next_allowed_action | approval_required | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| fixture-hn-agent-runtime-20260614 | fixture | hacker_news | public top/new story fixture | open_public_readonly | fixture://hacker-news/story/agent-runtime | fixture_submitter | agent runtime reliability | Public technical discussion about a lightweight agent runtime and failure recovery. | points=128;comments=42 | 6 |  |  | agent_infra | fixture | unknown | draft_seed | fixture_only;verify_before_use | Replace with real public HN row in next proof. | none_for_local | Shows how HN story metadata maps into a candidate row. |
| fixture-hn-mcp-safety-20260614 | fixture | hacker_news | public comment-theme fixture | open_public_readonly | fixture://hacker-news/comment-theme/mcp-safety | fixture_submitter | MCP tool permissions | Comment theme about tool permissions, local approvals, and accidental side effects. | points=76;comments=31 | 12 |  |  | tooling | fixture | unknown | pattern_note | fixture_only;claim_risk | Verify against direct source before drafting. | none_for_local | Useful as a pattern note, not a reply target. |
| fixture-ph-agent-debugger-20260614 | fixture | product_hunt | public launch fixture | open_public_readonly | fixture://product-hunt/launch/agent-debugger | fixture_maker | agent observability | Product launch positioning for debugging agent runs with timeline traces. | upvotes=214;comments=18 | 18 |  |  | product_launch | fixture | unknown | source_candidate | fixture_only;verify_before_use | Replace with public launch URL and pricing notes. | none_for_local | Maps launch-page fields without requiring login or voting. |
| fixture-ph-prompt-evals-20260614 | fixture | product_hunt | public launch fixture | open_public_readonly | fixture://product-hunt/launch/prompt-evals | fixture_maker | prompt eval harness | Product launch angle around prompt regression testing for teams shipping agents. | upvotes=89;comments=9 | 30 |  |  | tooling | fixture | unknown | draft_seed | fixture_only;claim_risk | Verify claims and category before use. | none_for_local | Candidate for local product-teardown seed after verification. |
| fixture-trends-coding-agents-20260614 | fixture | google_trends_style | public trend-query fixture | open_public_readonly | fixture://google-trends/query/coding-agents |  | coding agents | Query cluster indicates rising interest around coding agents and desktop agent workflows. | breakout=fixture;region=US | 24 |  |  | ai_builder | fixture | unknown | watchlist | fixture_only;metric_only | Replace with timestamped public trend export. | none_for_local | Good cross-source validator, not enough alone for a claim. |
| fixture-x-coding-agent-thread-20260614 | fixture | x_public | public search placeholder | awaiting_service_approval | service-gated://x/search/coding-agents |  | coding agents | Placeholder for future X public-post candidate after exact read-only approval. |  |  |  |  | ai_builder | fixture | unknown | reply_target_pending_gate | fixture_only;public_action_gated;account_gated | Await exact approved service request before capture. | service_request_for_readonly | X fields stay empty until approval. |
| fixture-grok-agent-brief-20260614 | fixture | grok | semantic scan placeholder | awaiting_service_approval | service-gated://grok/prompt/agent-trends |  | agent trend brief | Placeholder for future Grok prompt/output/citation artifact. |  |  |  |  | agent_infra | fixture | unknown | source_candidate | fixture_only;model_api_gated;account_gated | Await exact approved service request before prompt/use. | service_request_for_readonly | Grok output would be treated as leads, not proof. |
| fixture-radar-ai-builder-20260614 | fixture | x_radar | radar trend placeholder | awaiting_service_approval | service-gated://x-radar/topic/ai-builders |  | AI-builder trend cluster | Placeholder for future Radar topic velocity and representative-post capture. |  |  |  |  | ai_builder | fixture | unknown | watchlist | fixture_only;public_action_gated;account_gated | Await exact approved service request before capture. | service_request_for_readonly | Radar is not opened or queried here. |
| fixture-cross-source-agent-observability-20260614 | fixture | cross_source | local normalization fixture | open_public_readonly | fixture://cross-source/agent-observability |  | agent observability | Local combined pattern from HN-style discussion plus Product Hunt-style launch fixture. | sources=2 fixture rows | 24 |  |  | agent_infra | fixture | unknown | draft_seed | fixture_only;verify_before_use | Replace with at least two real verified public sources. | none_for_local | Demonstrates cross-source promotion without public action. |

## Local scoring

Use local scoring only. A high score never authorizes a public action.

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Freshness | Older than 7 days or unknown | 1-7 days | Under 24 hours |
| Audience fit | Off-lane | Adjacent AI/business topic | Direct AI-builder, agent infra, tooling, or workflow fit |
| Evidence density | Metric-only or unsourced | One direct public source | Multiple sources or one high-authority direct source |
| Novelty | Generic AI news | Useful but common angle | Specific workflow, failure mode, data point, or product mechanic |
| Safety | Requires account/public action or risky claim | Needs verification | Local-only and safe to analyze |
| Actionability | No useful next step | Watchlist or verify | Local draft seed or source-candidate packet |

Recommended local decision:

- `0-5`: reject or archive as weak context.
- `6-8`: watchlist or pattern note.
- `9-10`: local draft seed after source verification.
- `11-12`: strong local candidate, still gated before any public action.

## Gate behavior for X/Grok/Radar fields

Until an exact approved service request exists, rows from `x_public`, `grok`, and `x_radar` must keep:

- `service_gate_status=awaiting_service_approval`
- `visible_metrics` blank
- `weighted_engagement` blank
- `velocity_score` blank
- `content_use` limited to `reply_target_pending_gate`, `source_candidate`, or `watchlist`
- `next_allowed_action=await_service_request_approval`
- `approval_required=service_request_for_readonly`
- `risk_flags` including `public_action_gated` or `account_gated`

## Next local step

Create a real non-account public capture packet from safe sources only, starting with Hacker News public endpoints and Product Hunt/Google Trends-style public exports if they are accessible without login, paid tools, browser-account action, API tokens, or captcha/consent circumvention. Keep X/Grok/Radar placeholders untouched until approval.
