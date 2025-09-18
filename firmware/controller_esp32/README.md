# controller_esp32

ESP32 firmware to read sensors, control pumps/buzzer locally, and upload sensor readings to ThingSpeak.

Quick steps:
1. Copy `firmware/secrets.example.h` to `firmware/controller_esp32/secrets.h` and fill values.
2. Open `controller_esp32.ino` in Arduino IDE / PlatformIO.
3. Install required libraries: DHT, OneWire, DallasTemperature, HTTPClient (comes with ESP core).
4. Upload to ESP32.
5. Monitor serial logs for JSON lines and ThingSpeak upload responses.

Notes:
- Calibrate ADC mapping for pH, turbidity, chlorine.
- Tune thresholds in the sketch to match your hardware.
