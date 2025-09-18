# Raspberry Pi Gateway

This folder contains scripts to read JSON from Arduino Serial and:
- upload to ThingSpeak
- log data to CSV
- send email alerts (with cooldown)

Quick start:
1. Copy `.env.example` -> `.env` and fill values.
2. Create virtualenv and install:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Run:
```
python3 thingspeak_uploader.py
```
Notes:
- Ensure `SERIAL_PORT` is correct (e.g. `/dev/ttyUSB0`).
- Use Gmail app password for `EMAIL_PASS` if using Gmail.
- Buzzer alerts are handled locally by the microcontroller (Arduino/ESP).
