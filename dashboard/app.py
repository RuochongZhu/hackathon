"""Shiny entrypoint for Posit Cloud.

Allows platforms that expect `app.py` to run this dashboard.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure repo root is importable before loading ui_app.
THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ui_app import app  # noqa: E402,F401
