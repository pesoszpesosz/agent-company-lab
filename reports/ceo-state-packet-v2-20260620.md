# CEO State Packet V2

Generated UTC: 2026-06-20T17:04:00Z
Status: current local state packet after premium customer intake install
JSON mirror: `E:\agent-company-lab\reports\ceo-state-packet-v2-20260620.json`

## Company Counts

| Table | Count |
| --- | ---: |
| Lanes | 15 |
| Departments | 22 |
| Roles | 18 |
| Agents | 16 |
| Tasks | 580 |
| Artifacts | 2413 |
| Outcomes | 419 |
| Trace events | 510 |
| Service requests | 16 |

## Active New Lanes

| Lane | Department | Owner | Status |
| --- | --- | --- | --- |
| `ai_resources_lab` | AI Resources | `lane-manager-ai_resources_lab-20260620` | active |
| `youtube_content_channels` | Audience/Distribution | `lane-manager-youtube_content_channels-20260620` | active |
| `premium_customer_intake` | Customer/Operator Success | `premium-customer-intake-agent-20260620` | active |

## New CEO Context Rule

Customer raw requests and materials flow through `premium_customer_intake`. The CEO receives compact capsules, route status, and applied-knowledge deltas.

## Current Decision Batch

1. Use premium intake for future customer requests and lane materials.
2. Create `youtube_no_post_content_batch_v1`.
3. Create `control_plane_capacity_benchmark_packet_v1`.
4. Convert blocker triage into manager dispatch.

## Human Action State

Immediate human action required: none.

## Boundary

This packet is a state summary only. It does not approve service requests, start workers, call models/APIs, open browsers, create accounts, publish content, submit code, trade, spend, or perform security testing.
