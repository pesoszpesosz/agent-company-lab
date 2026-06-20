"""Repository paths used by Agent Company tooling.

Keeping path discovery here lets CLI tools and future service modules share the
same durable workspace contract instead of each script deriving paths itself.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "state" / "agent_company.sqlite"
ROLE_REGISTRY_PATH = ROOT / "architecture" / "role-registry-draft.json"
LANE_TAXONOMY_PATH = ROOT / "architecture" / "lane-taxonomy-draft.json"
SOURCE_SPECS_PATH = ROOT / "architecture" / "source-specs-draft.json"
SERVICE_CATALOG_PATH = ROOT / "architecture" / "service-catalog-draft.json"
REPORTS_DIR = ROOT / "reports"
LAUNCH_DIR = REPORTS_DIR / "launch-packets"
MANAGER_PACKET_DIR = REPORTS_DIR / "manager-packets"
PROFIT_EDGE_ROOT = Path("E:/profit-edge-lab")

