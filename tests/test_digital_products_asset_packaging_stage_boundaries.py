import sys
from pathlib import Path


ROOT = Path(r"E:\agent-company-lab")
sys.path.insert(0, str(ROOT / "tools"))


def test_digital_products_asset_packaging_facade_reexports_stage_modules() -> None:
    from agent_company_core import digital_products_asset_packaging as facade
    from agent_company_core import digital_products_packaging_manifest
    from agent_company_core import digital_products_packaging_manifest_content
    from agent_company_core import digital_products_package_files
    from agent_company_core import digital_products_package_files_content
    from agent_company_core import digital_products_completeness_check

    assert facade.digital_products_package_files is digital_products_packaging_manifest_content.digital_products_package_files
    assert facade.digital_products_readme_sections is digital_products_packaging_manifest_content.digital_products_readme_sections
    assert digital_products_packaging_manifest.digital_products_package_files is digital_products_packaging_manifest_content.digital_products_package_files
    assert digital_products_packaging_manifest.digital_products_readme_sections is digital_products_packaging_manifest_content.digital_products_readme_sections
    assert facade.write_digital_products_local_packaging_manifest is digital_products_packaging_manifest.write_digital_products_local_packaging_manifest
    assert facade.digital_products_screenshot_rows is digital_products_package_files_content.digital_products_screenshot_rows
    assert facade.digital_products_qa_rows is digital_products_package_files_content.digital_products_qa_rows
    assert facade.digital_products_post_launch_prompts is digital_products_package_files_content.digital_products_post_launch_prompts
    assert digital_products_package_files.digital_products_screenshot_rows is digital_products_package_files_content.digital_products_screenshot_rows
    assert digital_products_package_files.digital_products_qa_rows is digital_products_package_files_content.digital_products_qa_rows
    assert digital_products_package_files.digital_products_post_launch_prompts is digital_products_package_files_content.digital_products_post_launch_prompts
    assert facade.write_digital_products_local_package_files is digital_products_package_files.write_digital_products_local_package_files
    assert facade.digital_products_completeness_checks is digital_products_completeness_check.digital_products_completeness_checks
    assert facade.digital_products_missing_file_stubs is digital_products_completeness_check.digital_products_missing_file_stubs
    assert facade.write_digital_products_local_completeness_check is digital_products_completeness_check.write_digital_products_local_completeness_check


def test_digital_products_package_files_content_counts() -> None:
    from agent_company_core import digital_products_package_files_content

    assert len(digital_products_package_files_content.digital_products_screenshot_rows()) == 6
    assert len(digital_products_package_files_content.digital_products_qa_rows()) == 7
    assert len(digital_products_package_files_content.digital_products_post_launch_prompts()) == 6

def test_digital_products_packaging_manifest_content_counts() -> None:
    from agent_company_core import digital_products_packaging_manifest_content

    files = digital_products_packaging_manifest_content.digital_products_package_files()
    sections = digital_products_packaging_manifest_content.digital_products_readme_sections()

    assert len(files) == 6
    assert len(sections) == 7
    assert files[0]["path"] == "README.md"
    assert files[-1]["path"] == "post-launch-review.md"
    assert sections[-1]["section_id"] == "gates-before-public-use"

