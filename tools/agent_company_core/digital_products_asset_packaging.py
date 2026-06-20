from __future__ import annotations

"""Compatibility facade for digital-product asset packaging stages."""

from .digital_products_packaging_manifest import (
    digital_products_package_files,
    digital_products_readme_sections,
    write_digital_products_local_packaging_manifest,
)
from .digital_products_package_files import write_digital_products_local_package_files
from .digital_products_package_files_content import (
    digital_products_post_launch_prompts,
    digital_products_qa_rows,
    digital_products_screenshot_rows,
)
from .digital_products_completeness_check import (
    digital_products_completeness_checks,
    digital_products_missing_file_stubs,
    write_digital_products_local_completeness_check,
)

__all__ = [
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
