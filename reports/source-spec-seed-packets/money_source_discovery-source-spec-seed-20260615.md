# Source Spec Seed Packet: money_source_discovery

Generated UTC: 2026-06-15T17:00:55Z
JSON mirror: `E:\agent-company-lab\reports\source-spec-seed-packets\money_source_discovery-source-spec-seed-20260615.json`

## Proposed Source Spec

- ID: `money_source_discovery_public_venue_source_seed`
- Name: Money Source Discovery Public Venue Source Seed
- Type: `public_venue_registry`
- Cadence: `lane_owner_on_demand_or_weekly`
- Risk gate: `read_only_discovery_no_registration_outreach_wallet_payment_or_submission`

## Source Paths

- public bounty and paid-task venue lists
- grant and hackathon aggregators
- creator-marketplace opportunity lists
- AI evaluation and data-labeling opportunity pages
- local profit-edge imported negative and parked rows

## Outputs

- E:\agent-company-lab\reports\money-source-discovery\public-venue-source-refresh-YYYYMMDD.md
- lane_evidence
- service_request_candidates

## Boundary

This packet is report-only. It does not add a source spec, execute refresh commands, browse, register accounts, accept terms, download gated data, publish, submit, touch wallets/payments, mutate service requests, assign workers, call APIs, or create external side effects.

## Next Action

Review and, if accepted, convert into a source-spec registry row in a separate local-only task.

