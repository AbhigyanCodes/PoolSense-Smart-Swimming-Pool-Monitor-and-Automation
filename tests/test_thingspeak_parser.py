"""Tests for thingspeak_uploader parsing and utilities."""

from raspberry_pi import thingspeak_uploader as tu


def test_parse_json_line_valid():
    """Verify JSON parsing returns a dict and correct value."""
    line = (
        '{"waterLevel":100,"pH":7.0,"dhtTemp":25.0,'
        '"dhtHum":55.0,"dsTemp":24.5,"turbidity":100,"chlorine":400}'
    )
    payload = tu.parse_json_line(line)
    assert isinstance(payload, dict)
    assert payload["pH"] == 7.0
