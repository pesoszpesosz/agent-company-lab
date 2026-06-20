import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_constants_facade_reexports_domain_modules() -> None:
    from agent_company_core import constants
    from agent_company_core import constants_agent_company_migration
    from agent_company_core import constants_ceo_decisions
    from agent_company_core import constants_digital_products
    from agent_company_core import constants_durable_adapters
    from agent_company_core import constants_reports
    from agent_company_core import constants_service_workers

    assert constants.SERVICE_WORKER_REQUEST_QUEUE_REPORT is constants_service_workers.SERVICE_WORKER_REQUEST_QUEUE_REPORT
    assert constants.DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_REPORT is constants_digital_products.DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_REPORT
    assert constants.CEO_DECISION_INTAKE_GUARD_REPORT is constants_ceo_decisions.CEO_DECISION_INTAKE_GUARD_REPORT
    assert constants.AGENT_COMPANY_MIGRATION_DECISION_INTAKE_CONTRACT_REPORT is constants_agent_company_migration.AGENT_COMPANY_MIGRATION_DECISION_INTAKE_CONTRACT_REPORT
    assert constants.DURABLE_RUNTIME_INTERFACE_CONTRACT_REPORT is constants_durable_adapters.DURABLE_RUNTIME_INTERFACE_CONTRACT_REPORT
    assert constants.MONEY_PATH_COVERAGE_AUDIT_REPORT is constants_reports.MONEY_PATH_COVERAGE_AUDIT_REPORT


def test_constants_domain_modules_expose_explicit_public_names() -> None:
    from agent_company_core import constants
    from agent_company_core import constants_digital_products
    from agent_company_core import constants_durable_adapters
    from agent_company_core import constants_service_workers

    assert "SERVICE_WORKER_REQUEST_QUEUE_REPORT" in constants_service_workers.__all__
    assert "DIGITAL_PRODUCTS_LOCAL_ASSET_DRAFT_REPORT" in constants_digital_products.__all__
    assert "DURABLE_ADAPTER_ALLOWED_OUTPUT_STATES" in constants_durable_adapters.__all__
    assert "SERVICE_WORKER_REQUEST_QUEUE_REPORT" in constants.__all__
