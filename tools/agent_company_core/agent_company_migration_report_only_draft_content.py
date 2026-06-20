"""Pure SQL draft builders for the report-only agent-company migration."""

from __future__ import annotations

from typing import Any

INDEX_COLUMN_MAP = {
    "department_state": ["department_id", "state"],
    "owner_state": ["owner_agent_id", "state"],
    "status_manager": ["status", "manager_role_id"],
    "default_lane": ["default_lane_id"],
    "department_status": ["department_id", "status"],
    "category_score": ["category", "expected_value_score"],
    "money_path_status": ["money_path_id", "status"],
    "risk_payout": ["risk_score", "payout_max"],
    "approval_status": ["approval_required", "status"],
    "state_type": ["approval_state", "gate_type"],
    "service_request_state": ["service_request_id", "approval_state"],
    "source_task": ["source_task_id"],
    "to_thread_status": ["to_thread_id", "status"],
    "task_status": ["task_id", "status"],
    "money_path_result": ["money_path_id", "result_state"],
    "department_started": ["department_id", "started_at"],
    "value_probability": ["expected_value_usd", "payout_probability"],
}

APPLY_GATES = [
    "operator_approval_required_before_sql_execution",
    "backup_agent_company_sqlite_before_apply",
    "run_migration_against_throwaway_copy_first",
    "confirm_no_service_request_state_mutation",
    "confirm_no_worker_threads_started",
    "confirm_no_browser_account_wallet_payment_public_or_security_actions",
    "record_post_apply_integrity_report_before_next_layer",
]


def column_type(column_name: str) -> str:
    if column_name.endswith("_id") or column_name in {"id", "status", "state", "category", "currency"}:
        return "TEXT"
    if column_name.endswith("_at") or column_name.endswith("_date") or column_name in {"expires_at", "started_at", "completed_at", "created_at", "updated_at"}:
        return "TEXT"
    if (
        column_name.endswith("_json")
        or column_name.endswith("_path")
        or column_name.endswith("_url")
        or "summary" in column_name
        or "reason" in column_name
        or "note" in column_name
        or "schema" in column_name
        or "actions" in column_name
        or column_name in {"purpose", "name", "scope", "hypothesis", "rollback_plan", "decision_note", "risk_summary", "next_action"}
    ):
        return "TEXT"
    if column_name.startswith("payout_") or column_name.endswith("_usd") or column_name.endswith("_score") or column_name.endswith("_probability") or column_name == "capital_required":
        return "REAL"
    if column_name in {"account_required", "approval_required"}:
        return "INTEGER"
    if column_name.startswith("max_") or column_name.endswith("_limit") or column_name.endswith("_spent"):
        return "INTEGER"
    return "TEXT"


def build_report_only_migration_draft_content(table_plans: list[dict[str, Any]]) -> dict[str, Any]:
    table_migrations = []
    create_statements = []
    index_statements = []
    validation_queries = []
    rollback_statements = []
    for table_plan in table_plans:
        table_name = table_plan["table"]
        columns = table_plan.get("columns", [])
        indexes = table_plan.get("indexes", [])
        column_lines = []
        for idx, column in enumerate(columns):
            ddl_type = column_type(column)
            suffix = " PRIMARY KEY NOT NULL" if idx == 0 else ""
            column_lines.append(f"  {column} {ddl_type}{suffix}")
        create_statement = "CREATE TABLE IF NOT EXISTS " + table_name + " (\n" + ",\n".join(column_lines) + "\n);"
        create_statements.append(create_statement)
        table_index_statements = []
        for index_name in indexes:
            raw_columns = INDEX_COLUMN_MAP.get(index_name, columns[:2])
            index_columns = [column for column in raw_columns if column in columns] or columns[:1]
            statement = f"CREATE INDEX IF NOT EXISTS idx_{table_name}_{index_name} ON {table_name} ({', '.join(index_columns)});"
            index_statements.append(statement)
            table_index_statements.append(statement)
        validation_query = f"SELECT COUNT(*) AS row_count FROM {table_name};"
        validation_queries.append(validation_query)
        table_rollback = [f"DROP INDEX IF EXISTS idx_{table_name}_{index_name};" for index_name in indexes]
        table_rollback.append(f"DROP TABLE IF EXISTS {table_name};")
        rollback_statements.extend(table_rollback)
        table_migrations.append(
            {
                "table": table_name,
                "create_statement": create_statement,
                "index_statements": table_index_statements,
                "validation_query": validation_query,
                "rollback_statements": table_rollback,
            }
        )
    return {
        "table_migrations": table_migrations,
        "create_statements": create_statements,
        "index_statements": index_statements,
        "validation_queries": validation_queries,
        "rollback_statements": rollback_statements,
        "apply_gates": APPLY_GATES,
        "table_migration_count": len(table_migrations),
        "create_statement_count": len(create_statements),
        "index_statement_count": len(index_statements),
        "validation_query_count": len(validation_queries),
        "rollback_statement_count": len(rollback_statements),
        "apply_gate_count": len(APPLY_GATES),
    }


__all__ = [
    "APPLY_GATES",
    "INDEX_COLUMN_MAP",
    "build_report_only_migration_draft_content",
    "column_type",
]
