import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_catalog_facade_preserves_seed_listing_and_report_boundaries() -> None:
    from agent_company_core import catalog
    from agent_company_core import catalog_listing
    from agent_company_core import catalog_report
    from agent_company_core import catalog_seed

    assert catalog.department_id is catalog_seed.department_id
    assert catalog.upsert_source_spec is catalog_seed.upsert_source_spec
    assert catalog.seed is catalog_seed.seed
    assert catalog.seed_source_specs is catalog_seed.seed_source_specs
    assert catalog.seed_service_catalog is catalog_seed.seed_service_catalog

    assert catalog.list_evidence is catalog_listing.list_evidence
    assert catalog.list_source_specs is catalog_listing.list_source_specs
    assert catalog.list_service_catalog is catalog_listing.list_service_catalog
    assert catalog.service_catalog_where is catalog_listing.service_catalog_where

    assert catalog.write_service_catalog_report is catalog_report.write_service_catalog_report