import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "raspberry-pi"))

from thingspeak_uploader import should_send_alert

def test_should_send_alert_callable():
    assert callable(should_send_alert)
