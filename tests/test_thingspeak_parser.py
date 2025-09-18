import json
import sys
from pathlib import Path
# make sure raspberry-pi module path is available
sys.path.append(str(Path(__file__).resolve().parents[1] / "raspberry-pi"))

import thingspeak_uploader as tu

def test_parse_json_line_valid():
    line = '{"waterLevel":100,"pH":7.0,"dhtTemp":25.0,"dhtHum":55.0,"dsTemp":24.5,"turbidity":100,"chlorine":400}'
    payload = tu.parse_json_line(line)
    assert isinstance(payload, dict)
    assert payload["pH"] == 7.0
