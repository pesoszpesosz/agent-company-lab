import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_digital_products_asset_authoring_facade_reexports_outline_and_draft_modules() -> None:
    from agent_company_core import digital_products_asset_authoring as authoring_facade
    from agent_company_core import digital_products_asset_draft
    from agent_company_core import digital_products_asset_draft_content
    from agent_company_core import digital_products_asset_outline
    from agent_company_core import digital_products_asset_outline_content

    assert authoring_facade.digital_products_asset_outline_components is digital_products_asset_outline_content.digital_products_asset_outline_components
    assert authoring_facade.digital_products_positioning_template_fields is digital_products_asset_outline_content.digital_products_positioning_template_fields
    assert authoring_facade.digital_products_sample_positioning_sections is digital_products_asset_outline_content.digital_products_sample_positioning_sections
    assert digital_products_asset_outline.digital_products_asset_outline_components is digital_products_asset_outline_content.digital_products_asset_outline_components
    assert digital_products_asset_outline.digital_products_positioning_template_fields is digital_products_asset_outline_content.digital_products_positioning_template_fields
    assert digital_products_asset_outline.digital_products_sample_positioning_sections is digital_products_asset_outline_content.digital_products_sample_positioning_sections
    assert authoring_facade.write_digital_products_local_asset_outline is digital_products_asset_outline.write_digital_products_local_asset_outline

    assert authoring_facade.digital_products_positioning_answers is digital_products_asset_draft_content.digital_products_positioning_answers
    assert authoring_facade.digital_products_launch_checklist_rows is digital_products_asset_draft_content.digital_products_launch_checklist_rows
    assert authoring_facade.digital_products_asset_boundary_notes is digital_products_asset_draft_content.digital_products_asset_boundary_notes
    assert digital_products_asset_draft.digital_products_positioning_answers is digital_products_asset_draft_content.digital_products_positioning_answers
    assert digital_products_asset_draft.digital_products_launch_checklist_rows is digital_products_asset_draft_content.digital_products_launch_checklist_rows
    assert digital_products_asset_draft.digital_products_asset_boundary_notes is digital_products_asset_draft_content.digital_products_asset_boundary_notes
    assert authoring_facade.write_digital_products_local_asset_draft is digital_products_asset_draft.write_digital_products_local_asset_draft


def test_digital_products_assets_facades_reexport_phase_modules() -> None:
    import agent_company_core.digital_products as digital_products_facade
    import agent_company_core.digital_products_assets as assets_facade
    from agent_company_core import digital_products_asset_authoring
    from agent_company_core import digital_products_asset_packaging
    from agent_company_core import digital_products_asset_quality
    from agent_company_core import digital_products_asset_quality_content

    assert (
        assets_facade.digital_products_asset_outline_components
        is digital_products_asset_authoring.digital_products_asset_outline_components
    )
    assert (
        assets_facade.write_digital_products_local_asset_draft
        is digital_products_asset_authoring.write_digital_products_local_asset_draft
    )
    assert assets_facade.digital_products_quality_checks is digital_products_asset_quality_content.digital_products_quality_checks
    assert digital_products_asset_quality.digital_products_quality_checks is digital_products_asset_quality_content.digital_products_quality_checks
    assert (
        assets_facade.write_digital_products_local_quality_pass
        is digital_products_asset_quality.write_digital_products_local_quality_pass
    )
    assert assets_facade.digital_products_package_files is digital_products_asset_packaging.digital_products_package_files
    assert (
        assets_facade.write_digital_products_local_completeness_check
        is digital_products_asset_packaging.write_digital_products_local_completeness_check
    )
    assert (
        digital_products_facade.write_digital_products_local_packaging_manifest
        is digital_products_asset_packaging.write_digital_products_local_packaging_manifest
    )

def test_digital_products_asset_draft_content_is_reusable_without_writer_import() -> None:
    from agent_company_core import digital_products_asset_draft_content

    assert len(digital_products_asset_draft_content.digital_products_positioning_answers()) == 10
    assert len(digital_products_asset_draft_content.digital_products_launch_checklist_rows()) == 9
    assert len(digital_products_asset_draft_content.digital_products_asset_boundary_notes()) == 4

def test_digital_products_asset_outline_content_is_reusable_without_writer_import() -> None:
    from agent_company_core import digital_products_asset_outline_content

    components = digital_products_asset_outline_content.digital_products_asset_outline_components()
    fields = digital_products_asset_outline_content.digital_products_positioning_template_fields()
    sections = digital_products_asset_outline_content.digital_products_sample_positioning_sections()

    assert len(components) == 6
    assert len(fields) == 10
    assert len(sections) == 5
    assert components[0]["component_id"] == "positioning-template"
    assert fields[-1]["field_id"] == "validation-gate"
    assert sections[-1]["section_id"] == "boundary"

def test_digital_products_asset_quality_content_is_reusable_without_writer_import() -> None:
    from agent_company_core import digital_products_asset_quality_content

    checks = digital_products_asset_quality_content.digital_products_quality_checks()
    revisions = digital_products_asset_quality_content.digital_products_quality_revision_items()

    assert len(checks) == 8
    assert sum(1 for check in checks if check["status"] == "pass") == 8
    assert len(revisions) == 5
    assert checks[0]["check_id"] == "single-buyer"
    assert revisions[-1]["revision_id"] == "add-local-packaging-manifest"

