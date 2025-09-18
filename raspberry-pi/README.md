# Raspberry Pi Gateway

This folder contains scripts to read JSON from Arduino Serial and:
- upload to ThingSpeak
- log data to CSV
- send email alerts (with cooldown)

Quick start:
1. Copy `.env.example` -> `.env` and fill values.
2. Create virtualenv and install:
