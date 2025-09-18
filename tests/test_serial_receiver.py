"""Tests for alert cooldown function."""

from raspberry_pi import thingspeak_uploader as tu


def test_should_send_alert_callable():
    """Ensure the should_send_alert function exists and is callable."""
    assert callable(getattr(tu, "should_send_alert", None))
