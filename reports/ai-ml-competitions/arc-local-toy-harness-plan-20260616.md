# ARC Local Toy Harness Plan

Generated UTC: 2026-06-16T20:55:00Z
Task: `task-arc-local-toy-harness-plan-20260616`
Lane: `ai_ml_competitions`
Owner: `lane-manager-ai_ml_competitions-019ec69a`
JSON mirror: `E:\agent-company-lab\reports\ai-ml-competitions\arc-local-toy-harness-plan-20260616.json`

## Purpose

Define a no-login, no-gated-data, no-paid-compute local toy harness for testing whether an ARC-style reasoning approach is worth deeper investment.

## Minimal DSL

| Operation | Meaning | Example |
| --- | --- | --- |
| `crop_nonzero` | Trim background rows/columns. | isolate object |
| `translate(dx, dy)` | Move colored cells. | shift shape right |
| `recolor(src, dst)` | Change one color to another. | red to blue |
| `mirror(axis)` | Reflect grid horizontally or vertically. | left-right symmetry |
| `tile(nx, ny)` | Repeat pattern. | 2x2 motif |
| `fill_bbox(color)` | Fill bounding box of an object. | enclosure |
| `compose(a, b)` | Apply transforms in order. | crop then mirror |

## Synthetic Task Families

| Family | Train Example | Expected Rule | Verification |
| --- | --- | --- | --- |
| Translation | object appears one cell right in output | detect object and `translate(1, 0)` | exact grid match |
| Recolor | all red object cells become blue | infer color mapping | exact grid match |
| Mirror | asymmetric object flips horizontally | detect `mirror(x)` | exact grid match |
| Crop and tile | nonzero object is cropped and repeated | `crop_nonzero` then `tile(2, 1)` | exact grid match |

## Harness Flow

1. Load synthetic train/test grids from JSON.
2. Generate candidate DSL programs up to depth 3.
3. Score candidates by exact train-match count.
4. Break ties by program length.
5. Apply best candidate to test input.
6. Produce explanation: candidate program, train score, failure mode, and confidence.

## Acceptance Tests

| Test | Pass Condition |
| --- | --- |
| Deterministic generation | Same input produces same candidate order and output. |
| Three families pass | Translation, recolor, and mirror families pass exact-match verification. |
| Failure is explicit | Unknown transform returns `no_solution` with inspected candidates. |
| No external dependency | Runs with Python standard library only. |
| No official data | Uses synthetic examples only. |

## Kill Criterion

Do not move toward Kaggle/rules/submission approval until the toy harness solves at least three synthetic families and produces useful failure explanations on one unsolved family.

## Next Action

Create `arc-toy-harness-fixture-20260616.json` and a local-only harness draft or pseudocode artifact. Keep official ARC/Kaggle access gated.

## Boundary

- Kaggle login: `false`
- Gated data downloaded: `false`
- Paid compute/API: `false`
- Submission: `false`
- Account actions: `false`
- Public actions: `false`
- External side effects: `false`
