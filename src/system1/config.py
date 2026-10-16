"""Project paths, secrets from .env, and pinned prices.

ROOT defaults to the source checkout; set SYSTEM1_ROOT in the process
environment to move it (for example inside a Docker image). .env is loaded
from ROOT first, so SYSTEM1_CONFIGS and SYSTEM1_RESULTS may also be set there.
"""

from __future__ import annotations

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(os.environ.get("SYSTEM1_ROOT", Path(__file__).resolve().parents[2]))

# Existing environment variables win over .env (override=False).
load_dotenv(ROOT / ".env")

CONFIGS = Path(os.environ.get("SYSTEM1_CONFIGS", ROOT / "configs"))
RESULTS = Path(os.environ.get("SYSTEM1_RESULTS", ROOT / "results"))


def load_prices(path: Path | None = None) -> dict:
    with open(path or CONFIGS / "prices.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)
