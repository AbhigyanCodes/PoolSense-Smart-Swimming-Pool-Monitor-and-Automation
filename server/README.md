# Server

Small Flask server to ingest JSON payloads. Useful if you want to store data locally instead of/in addition to ThingSpeak.

Usage:
1. Create virtualenv and install `pip install -r requirements.txt`
2. Run `python3 app.py`
3. POST JSON to `/ingest`
