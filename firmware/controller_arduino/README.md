# controller_serial (Arduino)

Arduino sketch to read sensors, control pumps & buzzer locally and print a JSON line on Serial.
This is used with the Raspberry Pi gateway.

Steps:
1. Open `controller_serial.ino`.
2. Install required libraries: DHT, OneWire, DallasTemperature.
3. Upload to Arduino.
4. Connect Arduino Serial to Raspberry Pi (USB or TTL).
