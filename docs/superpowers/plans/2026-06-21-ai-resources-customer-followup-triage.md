# AI Resources Customer Follow-Up Triage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a report-only AI Resources triage runner that converts premium-customer follow-up escalations into reuse, evolve, park, or CEO-decision recommendations without starting workers.

**Architecture:** Add one focused module under `tools/agent_company_core` with a pure triage builder, JSON/Markdown writers, and optional SQLite audit recording. Wire it into `tools/agent_company_core/cli.py` as `triage-ai-resources-customer-followups`. Cover behavior with in-memory SQLite tests.

**Tech Stack:** Python, argparse, sqlite3, pytest, existing Agent Company report and DB helpers.

---

### Task 1: Triage Builder And Report Writer

**Files:**
- Create: `tools/agent_company_core/ai_resources_customer_followup_triage.py`
- Test: `tests/test_ai_resources_customer_followup_triage.py`

- [ ] **Step 1: Write the failing test**

```python
def test_ai_resources_triage_classifies_escalation_items_without_mutating_followups(tmp_path: Path) -> None:
    conn = _conn()
    payload = triage_ai_resources_customer_followups(conn, _args(tmp_path, no_db_record=False))
    assert payload["status"] == "triage_ready"
    assert payload["counts"]["reuse_existing_owner"] == 1
    assert payload["counts"]["evolve_existing_agent"] == 1
    assert payload["counts"]["park_with_revisit_condition"] == 1
    assert payload["counts"]["ceo_decision_batch"] == 1
    assert conn.execute("select status from tasks where task_id='task-followup-new'").fetchone()["status"] == "new"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests\test_ai_resources_customer_followup_triage.py -q`
Expected: FAIL with `ModuleNotFoundError` or missing `triage_ai_resources_customer_followups`.

- [ ] **Step 3: Implement the module**

Create `build_ai_resources_customer_followup_triage`, `triage_ai_resources_customer_followups`, and `write_ai_resources_customer_followup_triage`. The runner must read `escalation_items`, classify each item, write `.json` and `.md`, record a completed `ai_resources_lab` audit task when DB recording is enabled, and preserve original follow-up task statuses.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests\test_ai_resources_customer_followup_triage.py -q`
Expected: PASS.

### Task 2: CLI Wiring

**Files:**
- Modify: `tools/agent_company_core/cli.py`
- Test: `tests/test_ai_resources_customer_followup_triage.py`

- [ ] **Step 1: Add a failing CLI parser/dispatch test**

```python
def test_ai_resources_triage_cli_parser_supports_command() -> None:
    parser = build_parser()
    args = parser.parse_args([
        "triage-ai-resources-customer-followups",
        "--escalation-report",
        "reports/customer-followup-escalation-v1-20260620.json",
    ])
    assert args.cmd == "triage-ai-resources-customer-followups"
    assert args.escalation_report.endswith("customer-followup-escalation-v1-20260620.json")
```

- [ ] **Step 2: Run parser test to verify it fails**

Run: `python -m pytest tests\test_ai_resources_customer_followup_triage.py::test_ai_resources_triage_cli_parser_supports_command -q`
Expected: FAIL because the command is not registered.

- [ ] **Step 3: Wire CLI**

Import `write_ai_resources_customer_followup_triage`, register `triage-ai-resources-customer-followups`, add `--escalation-report`, `--now-utc`, `--path`, `--json-path`, and `--no-db-record`, and dispatch after `escalate-premium-customer-followups`.

- [ ] **Step 4: Run focused tests**

Run: `python -m pytest tests\test_ai_resources_customer_followup_triage.py tests\test_premium_customer_followup_escalation.py -q`
Expected: PASS.

### Task 3: Live Packet And Verification

**Files:**
- Generate: `reports/ai-resources-customer-followup-triage-v1-20260621.json`
- Generate: `reports/ai-resources-customer-followup-triage-v1-20260621.md`

- [ ] **Step 1: Run the command on the live escalation packet**

Run: `python tools\agent_company.py triage-ai-resources-customer-followups --escalation-report reports\customer-followup-escalation-v1-20260620.json`
Expected: writes the triage packet and prints `ok: true`.

- [ ] **Step 2: Verify DB and original follow-up tasks**

Run a SQLite query confirming one completed `ai_resources_lab` triage audit task exists and the six `customer-input-ceo-operating-goal-objective-20260620-002:lane-followup:%` tasks remain `new`.

- [ ] **Step 3: Run the regression suite**

Run: `python -m pytest tests\test_ai_resources_customer_followup_triage.py tests\test_premium_customer_followup_escalation.py tests\test_premium_customer_followup_monitor.py tests\test_premium_customer_followup_synthesizer.py tests\test_premium_customer_intake_router.py -q`
Expected: PASS.
