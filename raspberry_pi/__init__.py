# raspberry_pi/__init__.py
"""
Package initializer for raspberry_pi.

This makes `raspberry_pi` a proper Python package so tests can import:
    from raspberry_pi import thingspeak_uploader as tu
"""

# Import the uploader module so `from raspberry_pi import thingspeak_uploader`
# works at the package level.
from . import thingspeak_uploader  # noqa: F401

__all__ = ["thingspeak_uploader"]
