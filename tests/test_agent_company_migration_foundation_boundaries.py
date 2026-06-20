import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_agent_company_migration_foundation_facades_reexport_phase_modules() -> None:
    import agent_company_core.agent_company_migration as migration_facade
    import agent_company_core.agent_company_migration_foundation as foundation_facade
    from agent_company_core import agent_company_migration_foundation_architecture
    from agent_company_core import agent_company_migration_foundation_review

    assert (
        foundation_facade.write_agent_company_infrastructure_radar
        is agent_company_migration_foundation_architecture.write_agent_company_infrastructure_radar
    )
    assert (
        foundation_facade.write_agent_company_department_schema_plan
        is agent_company_migration_foundation_architecture.write_agent_company_department_schema_plan
    )
    assert (
        foundation_facade.write_agent_company_report_only_migration_draft
        is agent_company_migration_foundation_review.write_agent_company_report_only_migration_draft
    )
    assert (
        foundation_facade.write_agent_company_migration_operator_review
        is agent_company_migration_foundation_review.write_agent_company_migration_operator_review
    )
    assert (
        migration_facade.write_agent_company_migration_apply_preflight
        is agent_company_migration_foundation_review.write_agent_company_migration_apply_preflight
    )

def test_report_only_migration_draft_content_builds_sql_plan_without_side_effects() -> None:
    from agent_company_core.agent_company_migration_report_only_draft_content import (
        APPLY_GATES,
        build_report_only_migration_draft_content,
        column_type,
    )

    table_plans = [
        {
            "table": "agent_departments",
            "columns": ["department_id", "state", "expected_value_usd", "approval_required"],
            "indexes": ["department_state", "missing_index"],
        },
        {
            "table": "agent_outcomes",
            "columns": ["outcome_id", "summary", "created_at"],
            "indexes": ["source_task"],
        },
    ]

    content = build_report_only_migration_draft_content(table_plans)

    assert column_type("expected_value_usd") == "REAL"
    assert column_type("approval_required") == "INTEGER"
    assert column_type("summary") == "TEXT"
    assert content["table_migration_count"] == 2
    assert content["create_statement_count"] == 2
    assert content["index_statement_count"] == 3
    assert content["validation_query_count"] == 2
    assert content["rollback_statement_count"] == 5
    assert content["apply_gate_count"] == 7
    assert content["apply_gates"] == APPLY_GATES
    assert content["create_statements"][0].startswith("CREATE TABLE IF NOT EXISTS agent_departments")
    assert "department_id TEXT PRIMARY KEY NOT NULL" in content["create_statements"][0]
    assert "expected_value_usd REAL" in content["create_statements"][0]
    assert "idx_agent_departments_department_state" in content["index_statements"][0]
    assert "idx_agent_departments_missing_index" in content["index_statements"][1]
    assert "department_id" in content["index_statements"][1]
    assert content["validation_queries"] == [
        "SELECT COUNT(*) AS row_count FROM agent_departments;",
        "SELECT COUNT(*) AS row_count FROM agent_outcomes;",
    ]
    assert content["table_migrations"][0]["rollback_statements"][-1] == "DROP TABLE IF EXISTS agent_departments;"

