#!/usr/bin/env python3
"""
thingspeak_uploader.py

Reads JSON lines from serial (Arduino) and:
 - posts to ThingSpeak
 - logs to CSV
 - sends email alerts with cooldown

This module is import-safe for unit tests: it does NOT import `serial`
at module import time. The `serial` import happens only inside main().
"""

import os
import time
import json
import csv
import requests
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyUSB0")
BAUDRATE = int(os.getenv("BAUDRATE", "9600"))
THINGSPEAK_API_KEY = os.getenv("THINGSPEAK_API_KEY", "")
THINGSPEAK_URL = os.getenv(
    "THINGSPEAK_URL", "https://api.thingspeak.com/update"
)
ALERT_RECIPIENTS = [
    e.strip()
    for e in os.getenv("ALERT_RECIPIENTS", "").split(",")
    if e.strip()
]
ALERT_COOLDOWN = int(os.getenv("ALERT_COOLDOWN_SECONDS", "600"))
LOG_CSV = os.getenv("LOG_CSV", "logs/sensor_log.csv")

THRESHOLDS = {
    "pH_min": 6.5,
    "pH_max": 7.5,
    "turbidity_max": 700,
    "chlorine_min": 300,
    "humidity_min": 30.0,
    "humidity_max": 70.0,
}

_last_alert_sent = {}


def ensure_csv():
    """Create logs folder and CSV header if not present."""
    d = os.path.dirname(LOG_CSV)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    if not os.path.exists(LOG_CSV):
        with open(LOG_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "timestamp",
                    "waterLevel",
                    "pH",
                    "dhtTemp",
                    "dhtHum",
                    "dsTemp",
                    "turbidity",
                    "chlorine",
                ]
            )


def send_email(subject, body):
    """Send an email alert using SMTP credentials from .env."""
    user = os.getenv("EMAIL_USER")
    pwd = os.getenv("EMAIL_PASS")
    smtp = os.getenv("EMAIL_SMTP", "smtp.gmail.com")
    port = int(os.getenv("EMAIL_PORT", "587"))
    if not (user and pwd and ALERT_RECIPIENTS):
        print("Email not configured; skipping")
        return

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = ", ".join(ALERT_RECIPIENTS)
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp, port) as s:
            s.starttls()
            s.login(user, pwd)
            s.send_message(msg)
        print("Email sent.")
    except Exception as e:
        print("Email failed:", e)


def should_send_alert(key):
    """Return True if allowed by cooldown; update last-sent time."""
    now = time.time()
    last = _last_alert_sent.get(key, 0)
    if now - last >= ALERT_COOLDOWN:
        _last_alert_sent[key] = now
        return True
    return False


def post_thingspeak(payload):
    """Map payload dict -> ThingSpeak fields and POST via HTTP GET."""
    params = {"api_key": THINGSPEAK_API_KEY}
    params["field1"] = payload.get("waterLevel")
    params["field2"] = payload.get("pH")
    params["field3"] = payload.get("dhtTemp")
    params["field4"] = payload.get("dhtHum")
    params["field5"] = payload.get("dsTemp")
    params["field6"] = payload.get("turbidity")
    params["field7"] = payload.get("chlorine")

    try:
        r = requests.get(THINGSPEAK_URL, params=params, timeout=10)
        if r.status_code == 200:
            print("ThingSpeak OK")
        else:
            print("ThingSpeak failed", r.status_code, r.text)
    except Exception as e:
        print("ThingSpeak exception:", e)


def log_payload(payload):
    """Append a payload row to the CSV log."""
    ts = datetime.now().isoformat()
    with open(LOG_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                ts,
                payload.get("waterLevel"),
                payload.get("pH"),
                payload.get("dhtTemp"),
                payload.get("dhtHum"),
                payload.get("dsTemp"),
                payload.get("turbidity"),
                payload.get("chlorine"),
            ]
        )


def parse_json_line(line):
    """Parse a JSON string into a dict, or return None on failure."""
    try:
        return json.loads(line)
    except Exception:
        return None


def check_alerts(payload):
    """Return a list of alerts (param, value) that exceeded thresholds."""
    alerts = []
    if payload.get("pH") is not None:
        if (
            payload["pH"] < THRESHOLDS["pH_min"]
            or payload["pH"] > THRESHOLDS["pH_max"]
        ):
            alerts.append(("pH", payload["pH"]))

    if (
        payload.get("turbidity") is not None
        and payload["turbidity"] > THRESHOLDS["turbidity_max"]
    ):
        alerts.append(("turbidity", payload["turbidity"]))

    if (
        payload.get("chlorine") is not None
        and payload["chlorine"] < THRESHOLDS["chlorine_min"]
    ):
        alerts.append(("chlorine", payload["chlorine"]))

    if payload.get("dhtHum") is not None:
        h = payload["dhtHum"]
        if h < THRESHOLDS["humidity_min"] or h > THRESHOLDS["humidity_max"]:
            alerts.append(("humidity", h))

    return alerts


def main():
    """
    Main loop: read serial, parse, log, upload, and alert.

    Note: `serial` is imported here to keep module import-time safe for tests.
    """
    # Import serial only when running, to avoid ImportError at import-time.
    try:
        import serial  # type: ignore
    except Exception as e:  # pragma: no cover - runtime environment may differ
        print("pyserial not available:", e)
        raise

    ensure_csv()
    print("Opening serial", SERIAL_PORT)
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=2)
    time.sleep(2)
    while True:
        try:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if not line:
                continue
            print("RAW:", line)
            payload = parse_json_line(line)
            if not payload:
                continue

            log_payload(payload)
            post_thingspeak(payload)

            alerts = check_alerts(payload)
            if alerts:
                for key, value in alerts:
                    if should_send_alert(key):
                        subject = f"POOL ALERT - {key.upper()} out of range"
                        body = (
                            f"Time: {datetime.now().isoformat()}\n"
                            f"Parameter: {key}\nValue: {value}\n"
                            f"Full payload: {json.dumps(payload)}"
                        )
                        send_email(subject, body)
        except Exception as exc:
            print("Main loop error:", exc)
            time.sleep(1)


if __name__ == "__main__":
    main()
