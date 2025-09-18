# ThingSpeak Field Mapping (recommended)

Use the following mapping across firmware and uploaders.

field1 = waterLevel        (raw ADC or percent)
field2 = pH                (calibrated 0–14)
field3 = dhtTemp           (°C)
field4 = dhtHum            (%)
field5 = dsTemp            (°C)   (DS18B20)
field6 = turbidity         (raw ADC / NTU estimate)
field7 = chlorine          (raw ADC / ppm estimate)
field8 = batteryVoltage    (optional)

Notes:
- Keep ThingSpeak write API key secret.
- Calibrate sensors; update conversion formulas in firmware.
