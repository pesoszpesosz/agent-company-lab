#!/usr/bin/env python3
"""
Executable wrapper for the agent-company control-plane CLI.

Command wiring lives in `agent_company_core.cli`; domain behavior lives in
focused core modules so this file stays as a thin entrypoint.
"""

from __future__ import annotations

from agent_company_core.cli import main


if __name__ == "__main__":
    main()
