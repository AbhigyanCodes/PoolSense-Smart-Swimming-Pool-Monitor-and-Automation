/*
  ds18b20.ino (test)
  Read DS18B20 temperature.
*/

#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 3

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(9600);
  sensors.begin();
}

void loop() {
  sensors.requestTemperatures();
  float t = sensors.getTempCByIndex(0);
  if (t == DEVICE_DISCONNECTED_C) {
    Serial.println("DS18B20 disconnected");
  } else {
    Serial.print("DS18B20: ");
    Serial.print(t);
    Serial.println(" *C");
  }
  delay(2000);
}
