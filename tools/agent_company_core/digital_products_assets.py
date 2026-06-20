from __future__ import annotations

"""Compatibility facade for digital-product asset authoring, quality, and packaging writers."""

from .digital_products_asset_authoring import (
    digital_products_asset_outline_components,
    digital_products_positioning_template_fields,
    digital_products_sample_positioning_sections,
    write_digital_products_local_asset_outline,
    digital_products_positioning_answers,
    digital_products_launch_checklist_rows,
    digital_products_asset_boundary_notes,
    write_digital_products_local_asset_draft,
)

from .digital_products_asset_quality import (
    digital_products_quality_checks,
    digital_products_quality_revision_items,
    write_digital_products_local_quality_pass,
)

from .digital_products_asset_packaging import (
    digital_products_package_files,
    digital_products_readme_sections,
    write_digital_products_local_packaging_manifest,
    digital_products_screenshot_rows,
    digital_products_qa_rows,
    digital_products_post_launch_prompts,
    write_digital_products_local_package_files,
    digital_products_completeness_checks,
    digital_products_missing_file_stubs,
    write_digital_products_local_completeness_check,
)

__all__ = [
    "digital_products_asset_outline_components",
    "digital_products_positioning_template_fields",
    "digital_products_sample_positioning_sections",
    "write_digital_products_local_asset_outline",
    "digital_products_positioning_answers",
    "digital_products_launch_checklist_rows",
    "digital_products_asset_boundary_notes",
    "write_digital_products_local_asset_draft",
    "digital_products_quality_checks",
    "digital_products_quality_revision_items",
    "write_digital_products_local_quality_pass",
    "digital_products_package_files",
    "digital_products_readme_sections",
    "write_digital_products_local_packaging_manifest",
    "digital_products_screenshot_rows",
    "digital_products_qa_rows",
    "digital_products_post_launch_prompts",
    "write_digital_products_local_package_files",
    "digital_products_completeness_checks",
    "digital_products_missing_file_stubs",
    "write_digital_products_local_completeness_check",
]
