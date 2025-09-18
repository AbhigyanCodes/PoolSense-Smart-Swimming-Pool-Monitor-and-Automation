# Firmware

This folder contains microcontroller sketches for the Swimming Pool Control & Monitoring System.

Subfolders:
- `controller_esp32/` — ESP32 direct-to-ThingSpeak (Wi-Fi).
- `controller_arduino/` — Arduino sketch that outputs JSON to Serial (Raspberry Pi gateway).
- `sensors/` — per-sensor test sketches.
- `examples/` — helper sketches (serial test, etc.).

Important:
- Copy `secrets.example.h` → `secrets.h` locally and fill Wi-Fi & ThingSpeak credentials.
- Do not commit `secrets.h`.
