# AI Resources Candidate Registry V1

Generated UTC: 2026-06-20T16:52:00Z
Lane: `ai_resources_lab`
Owner: `lane-manager-ai_resources_lab-20260620`
Status: report-only seed registry
JSON mirror: `E:\agent-company-lab\reports\ai-resources-candidate-registry-v1-20260620.json`

## Purpose

Create the first AI Resources registry for agents, tools, frameworks, research infrastructure, and money-making systems that the company may test locally. This registry is a queue for fast evaluation, not permission to install dependencies, run untrusted code, start runtimes, call APIs, open browsers, create accounts, or publish anything.

## Evaluation Rules

- Prefer improving an existing agent/tool over creating a duplicate.
- Require a local proof artifact before promotion.
- Kill, watch, or park any candidate that cannot show useful local proof within two focused work blocks.
- Keep license, account, API-cost, browser, public-action, wallet/payment, and security gates explicit.
- Record every adoption or rejection as an artifact with evidence and next action.

## Candidate Queue

| Candidate | Category | Why Test | First Local Proof | Disposition |
| --- | --- | --- | --- | --- |
| `ceo_state_packet_v1` | company memory | Keeps the CEO thread small while preserving decisions. | Current-state packet from SQLite and reports. | promote now |
| `human_action_feed_v1` | human-in-loop | Separates required user actions from optional approvals. | Feed with no-immediate-action status and optional gate queue. | promote now |
| `youtube_no_post_content_batch_v1` | money lane workflow | Starts YouTube without account or upload actions. | Ten script/title/asset briefs and gate map. | promote now |
| `LangGraph Agent Inbox patterns` | supervisor inbox | Existing radar shows useful packet shape without live transport. | Local packet schema only. | watch |
| `Temporal workflow adapter` | durable orchestration | Good future fit for long-running service-worker workflows. | Report-only decision matrix and dry-run fixture. | watch |
| `DBOS workflow adapter` | durable orchestration | Closest to database-first posture if SQLite later moves to Postgres. | Local reducer fixture against copied data. | watch |
| `Hatchet queue adapter` | worker queues | Useful future queue/concurrency model. | Report-only pool-cap simulation. | watch |
| `Trigger.dev wait/queue adapter` | worker queues | Useful waitpoint and human approval patterns. | Report-only waitpoint packet. | watch |
| `Pydantic AI TestModel adapter` | model harness | Existing local adapter can test prompts without paid API calls. | Fixture-only eval run. | keep and harden |
| `OpenAI Agents manifest-only adapter` | model harness | Can preserve future shape without running external tools. | Manifest validation only. | keep and harden |
| `PromptBase skill route` | marketplace route | Existing product may fit prompt/skill marketplace routes. | Eligibility packet from local asset and public-source notes. | test soon |
| `Algora/Opik bounty route` | paid code route | Existing worksheets can be hardened before live claims. | Claim-readiness packet and duplicate check. | test soon |
| `Kaggle/ARC baseline harness` | competition route | Prize upside exists, but time-to-cash is high. | Local baseline packet and rules gate. | test after higher-ROI routes |
| `Kalshi public-data worksheet` | prediction-market route | Public market data can support paper-only research. | No-auth schema and paper worksheet. | test after product/code lanes |

## Next Action

Create `ai_resources_candidate_evaluation_packet_v1` for the top three promote-now candidates: CEO state packet, human-action feed, and YouTube no-post content batch.

## Boundary

- Dependency installs: 0
- Runtime starts: 0
- Browser sessions: 0
- Accounts created or modified: 0
- Public actions: 0
- Model/API/MCP calls: 0
- Service requests approved, assigned, or started: 0
- External side effects: false
