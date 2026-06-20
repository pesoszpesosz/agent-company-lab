# Agent Company Trace Events

Generated UTC: 2026-06-20T16:55:13Z
Database: `E:\agent-company-lab\state\agent_company.sqlite`
Rows shown: 2

## Boundary

- Trace events are local audit records for agent/company operations.
- A trace event is not approval to perform account, wallet, browser, public, legal/KYC/billing, or real-money actions.

## Counts By Event Type

| Event Type | Count |
| --- | ---: |
| `ceo_operating_goal_installed` | 1 |
| `ceo_state_packets_installed` | 1 |

## Counts By Lane

| Lane | Count |
| --- | ---: |
| `ai_resources_lab` | 2 |

## Events

| Time | Type | Trace | Lane | Task | Agent | Event | Source | Artifact | Metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-20T16:54:52Z | ceo_state_packets_installed | `trace-ceo-first-state-packets-v1-20260620` | `ai_resources_lab` | `task-ceo-first-state-packets-v1-20260620` | lane-manager-ai_resources_lab-20260620 | `trace-event-ceo-first-state-packets-v1-20260620` - Installed first CEO state packets: AI Resources candidate registry, human-action feed, CEO state packet, and YouTube lane scout; added and claimed youtube_content_channels. | codex_current_ceo_thread | E:\agent-company-lab\reports\ceo-state-packet-v1-20260620.md | {"accounts_created": 0, "api_calls": false, "browser_sessions_started": 0, "external_side_effects": false, "lane_added": "youtube_content_channels", "packets_created": ["ai_resources_candidate_registry_v1", "human_action |
| 2026-06-20T16:48:52Z | ceo_operating_goal_installed | `trace-ceo-operating-goal-v1-20260620` | `ai_resources_lab` | `task-ceo-operating-goal-v1-20260620` | lane-manager-ai_resources_lab-20260620 | `trace-event-ceo-operating-goal-v1-installed-20260620` - Installed CEO operating goal v1, AI Resources lane/roles, goal-evolver charter, and human-action-desk role as local control-plane artifacts. | codex_current_ceo_thread | E:\agent-company-lab\architecture\ceo-operating-goal-v1.md | {"accounts_created": 0, "api_calls": false, "browser_sessions_started": 0, "department_added": "ai_resources", "external_side_effects": false, "lane_added": "ai_resources_lab", "public_actions": 0, "registered_agents": [ |
