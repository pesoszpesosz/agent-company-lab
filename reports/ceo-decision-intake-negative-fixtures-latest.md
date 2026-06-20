# CEO Decision Intake Negative Fixtures

Generated UTC: 2026-06-15T23:17:31Z
JSON mirror: `E:\agent-company-lab\reports\ceo-decision-intake-negative-fixtures-latest.json`
Validation: `E:\agent-company-lab\reports\ceo-decision-intake-negative-fixtures-validation-latest.json`

## Decision

`ceo_decision_intake_negative_fixtures_ready`

Created local negative fixtures for the CEO decision intake guard, covering every rejection rule with no accepted fixture.

## Fixtures

| Fixture | Expected Rule | Accepted |
| --- | --- | --- |
| `missing-packet-id` | `reject_missing_packet_id` | `False` |
| `unknown-option` | `reject_unknown_option` | `False` |
| `unbounded-scope` | `reject_unbounded_scope` | `False` |
| `forbidden-action-conflict` | `reject_forbidden_action_conflict` | `False` |
| `no-expiration` | `reject_no_expiration_or_review` | `False` |
| `implicit-contextual-approval` | `reject_implicit_or_contextual_approval` | `False` |

## Boundary

These are local negative fixtures only. They accept no decisions and do not approve, reject, assign, update, or start any service request; run browser sessions; perform legal/payment review; open accounts; accept terms; publish; list; configure payouts; touch wallets/payments; call APIs; or create external side effects.

## Next Action

Use these fixtures when implementing any future decision parser; a parser must reject all six before it can mutate service requests.

