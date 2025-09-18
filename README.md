# PoolSense - Swimming Pool Control & Monitoring System

![cover](images/cover.png)

**IoT system** for automatic water-level & temperature regulation, cloud logging (ThingSpeak), and immediate alerts (email + buzzer) for turbidity, chlorine, humidity, and sensor failure.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/AbhigyanCodes/PoolSense-Smart-Swimming-Pool-Monitor-and-Automation/tree/main?tab=MIT-1-ov-file)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/downloads/)
[![Build Status](https://github.com/AbhigyanCodes/PoolSense-Smart-Swimming-Pool-Monitor-and-Automation/actions/workflows/ci.yml/badge.svg)](https://github.com/AbhigyanCodes/PoolSense-Smart-Swimming-Pool-Monitor-and-Automation/actions/workflows/ci.yml)
[![Issues](https://img.shields.io/github/issues/AbhigyanCodes/PoolSense-Smart-Swimming-Pool-Monitor-and-Automation.svg)](https://github.com/AbhigyanCodes/PoolSense-Smart-Swimming-Pool-Monitor-and-Automation/issues)
[![Stars](https://img.shields.io/github/stars/AbhigyanCodes/PoolSense-Smart-Swimming-Pool-Monitor-and-Automation.svg)](https://github.com/AbhigyanCodes/PoolSense-Smart-Swimming-Pool-Monitor-and-Automation/stargazers)

---

## Quick overview

- **Deploy mode A (recommended):** ESP32 posts sensor data directly to ThingSpeak, controls pumps & buzzer locally.
- **Deploy mode B:** Arduino reads sensors & controls pumps/buzzer locally and prints JSON over serial → Raspberry Pi gateway uploads to ThingSpeak, logs CSV, and sends email alerts.
- Data fields, conversions, and thresholds are centrally documented in `docs/THINGSPEAK_FIELD_MAP.md` and `docs/design-notes.md`.

---

## Quick start — ESP32 (Option A)

1. Copy `firmware/secrets.example.h` → `firmware/controller_esp32/secrets.h` and fill:
   ```cpp
   #define WIFI_SSID "YOUR_WIFI_SSID"
   #define WIFI_PASS "YOUR_WIFI_PASS"
   #define THINGSPEAK_API_KEY "YOUR_THINGSPEAK_WRITE_KEY"
   ```
   **Do not commit** `secrets.h`.

2. Open `firmware/controller_esp32/controller_esp32.ino` in Arduino IDE / PlatformIO.
3. Install required libraries: `DHT`, `OneWire`, `DallasTemperature` (and ensure ESP32 core is installed).
4. Upload to your ESP32 and monitor serial output. The sketch uploads to ThingSpeak and handles local pump/buzzer control.

---

## Quick start — Arduino + Raspberry Pi (Option B)

1. Upload `firmware/controller_arduino/controller_serial.ino` to your Arduino (install `DHT`, `OneWire`, `DallasTemperature`).
2. On Raspberry Pi:
   ```bash
   cd raspberry_pi
   cp .env.example .env
   # Edit .env and fill SERIAL_PORT, THINGSPEAK_API_KEY, EMAIL_* etc.
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python3 thingspeak_uploader.py
   ```
3. The Pi will log data to `logs/sensor_log.csv`, upload to ThingSpeak, and send email alerts when thresholds are breached. The Arduino will operate the buzzer locally until parameters return to safe ranges.

---

## ThingSpeak field mapping (short)
See `docs/THINGSPEAK_FIELD_MAP.md` for full detail. Recommended mapping:
```
field1 = waterLevel
field2 = pH
field3 = dhtTemp
field4 = dhtHum
field5 = dsTemp
field6 = turbidity
field7 = chlorine
field8 = batteryVoltage (optional)
```

---

## Repository structure (short)
```
swimming-pool-iot/
├─ firmware/                 # Arduino/ESP sketches (controller_esp32, controller_arduino, sensors)
├─ raspberry_pi/             # Pi uploader, .env.example, requirements.txt
├─ docs/                     # report, mapping, wiring
├─ hardware/                 # BOM, schematics, photos
├─ server/                   # optional Flask ingest endpoint
├─ dashboard/                # optional front-end assets
├─ tests/                    # lightweight tests
├─ scripts/                  # calibration, export helpers
├─ images/                   # demo images & GIFs
├─ logs/                     # runtime logs (gitignored)
├─ .github/                  # CI & templates
├─ LICENSE
├─ CONTRIBUTING.md
└─ README.md                 # (this file)
```

---

## Calibration & safety notes

- **Calibrate** pH, turbidity, and chlorine sensors using known standards and update conversion formulas in `firmware/*` sketches (see `scripts/calibrate_sensor.py`).
- **Never** drive pumps from MCU pins — use relays or motor drivers with proper isolation and fuses.
- Use app-specific SMTP credentials (app password) for email alerts; never commit credentials to the repo.

---

## Contributing & development

- Run tests: `pytest -q`
- Lint: `flake8 .`
- Branch naming: `feature/...`, `fix/...`, `docs/...`
- See `CONTRIBUTING.md` for PR guidelines.

---

## License & attribution

This repository uses the **MIT License** — see `LICENSE` for details.

---

## Contact / Support

If you need help setting up hardware or calibrating sensors, create an issue with hardware details and serial logs (attach `logs/sensor_log.csv` sample). Happy to help!

---
