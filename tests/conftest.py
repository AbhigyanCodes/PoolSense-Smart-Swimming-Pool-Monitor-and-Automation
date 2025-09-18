# tests/conftest.py
"""
Ensure repo root is on sys.path so tests can import local packages.
This helps CI runs where pytest's import path may not include the repo root.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # repo root
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
