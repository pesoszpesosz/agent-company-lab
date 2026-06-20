from __future__ import annotations

"""Compatibility facade for local digital product asset authoring phases."""

from .digital_products_asset_draft import write_digital_products_local_asset_draft
from .digital_products_asset_draft_content import (
    digital_products_asset_boundary_notes,
    digital_products_launch_checklist_rows,
    digital_products_positioning_answers,
)
from .digital_products_asset_outline import (
    digital_products_asset_outline_components,
    digital_products_positioning_template_fields,
    digital_products_sample_positioning_sections,
    write_digital_products_local_asset_outline,
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
]