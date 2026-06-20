# Browser Worker Stack Radar Wave 18

Generated UTC: 2026-06-17T22:16:25Z

Lane: `platform_engineering`

Task: `task-browser-worker-stack-radar-wave18-20260618`

Scope: read-only current-source radar for browser-worker infrastructure. No browser sessions, installs, MCP starts, worker starts, accounts, payments, model/API calls, public actions, wallet actions, security tests, or external mutations were performed.

## Decision

Use Playwright as the deterministic base for any future approved browser worker. Treat Stagehand, Browser Use, Playwright MCP, and agent-browser as adapter candidates. Park cloud/session/credential-heavy tools behind stronger service-worker gates until the browser_worker_adapter_contract exists.

## Ranked Candidates

| Rank | Score | Repo | Category | Decision | Gate |
| --- | ---: | --- | --- | --- | --- |
| 1 | 95 | [microsoft/playwright](https://github.com/microsoft/playwright) | deterministic_browser_automation_foundation | `preferred_foundation_library` | browser install/start still requires approval; public actions and signed-in state need service-worker gates |
| 2 | 91 | [browser-use/browser-use](https://github.com/browser-use/browser-use) | browser_agent_runtime | `candidate_adapter_after_approval` | browser_read_only_worker_policy plus signed approval; model/API and cloud keys gated separately |
| 3 | 89 | [browserbase/stagehand](https://github.com/browserbase/stagehand) | browser_agent_sdk | `candidate_adapter_after_approval` | Browserbase/cloud/API keys/payment gates if remote sessions are used; local CDP only after approval |
| 4 | 83 | [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | browser_mcp_server | `candidate_read_only_mcp_after_registry_gate` | MCP registry gate, prompt-injection/RCE review, no browser_run_code-style tool exposure without denylist and signed scope |
| 5 | 80 | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | native_browser_cli | `candidate_cli_after_install_gate` | Chrome install/start, cloud API key, and provider selection all require explicit approval |
| 6 | 76 | [steel-dev/steel-browser](https://github.com/steel-dev/steel-browser) | browser_api_sandbox | `gated_infra_candidate` | cloud/self-host runtime, credential injection, proxies, CAPTCHA/stealth claims, and payment/API keys require stronger CRO approval |
| 7 | 74 | [browser-use/browser-harness](https://github.com/browser-use/browser-harness) | low_level_cdp_harness | `study_pattern_not_default_runtime` | high autonomy; require domain allowlist, no credential entry, egress logging, and kill switch before any browser start |
| 8 | 68 | [Skyvern-AI/skyvern](https://github.com/Skyvern-AI/skyvern) | workflow_browser_automation_platform | `gated_workflow_platform_only` | AGPL, Docker/service footprint, credentials/download/form-fill risk, and account/workflow execution approvals required |
| 9 | 61 | [browserbase/stagehand-python](https://github.com/browserbase/stagehand-python) | python_browser_agent_sdk | `watch_secondary_adapter` | same as Stagehand plus maturity gap; do not adopt before TypeScript core review |
| 10 | 59 | [hyperbrowserai/HyperAgent](https://github.com/hyperbrowserai/HyperAgent) | ai_playwright_wrapper | `watch_adapter` | cloud/browser infra and API key gates likely required for production use |
| 11 | 55 | [nanobrowser/nanobrowser](https://github.com/nanobrowser/nanobrowser) | browser_extension_agent | `watch_user_browser_risk` | extension install, user browser data exposure, API keys, and public/account actions require explicit approval and isolated profile |
| 12 | 52 | [hyperbrowserai/mcp](https://github.com/hyperbrowserai/mcp) | cloud_browser_mcp | `gated_mcp_only` | MCP registry, API key, scraping/crawling policy, cloud billing, and browser action approvals required |
| 13 | 48 | [browseros-ai/BrowserOS](https://github.com/browseros-ai/BrowserOS) | agentic_browser_fork | `watch_not_adopt_now` | AGPL, browser fork install/update trust, profile isolation, secrets, and extension/tool surface review required |

## Architecture Takeaways

- Deterministic first: Playwright remains the safest foundation for replayable capture, assertions, screenshots, and fixture tests.
- Natural-language browser agents are adapters, not root authority. They need service-request scope, domain allowlists, action denylist, trace events, and result artifacts before any session starts.
- MCP browser tools are useful only after the MCP tool registry gate reviews tool names, code-execution surfaces, prompt-injection exposure, and output artifact contracts.
- Cloud browsers, persistent profiles, credential injection, CAPTCHA/stealth, proxies, MFA, and session reuse are high-risk service-worker capabilities. They need legal/credential/payment/browser approval chains, not lane-manager discretion.
- Extension/browser-fork projects are useful as UX references, but unsafe for this lab until isolated profile, update-trust, and data-exposure reviews exist.

## Next Local Build

Create browser_worker_adapter_contract_v1 that maps any approved browser runtime to domain allowlists, action-class denylist, screenshot/DOM capture artifacts, session lifecycle records, and egress trace events before a browser starts.

## Boundary

Report-only. No clone, no install, no browser start, no MCP server start, no API key use, no login, no account action, no public action, no payment, no wallet action, no security testing, and no external side effect.
