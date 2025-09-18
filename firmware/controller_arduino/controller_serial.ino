/*
  controller_serial.ino
  Arduino: reads sensors, controls pumps & buzzer locally,
  prints JSON over Serial for Raspberry Pi ingestion.
*/

#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define DHTPIN 2
#define DHTTYPE DHT22
#define ONE_WIRE_BUS 3

const int waterLevelPin = A0;
const int phPin = A1;
const int turbidityPin = A2;
const int chlorinePin = A3;

const int pump1Pin = 8;
const int pump2Pin = 9;
const int buzzerPin = 10;

DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature dsensor(&oneWire);

const int MAX_WATER_LEVEL = 700;
const int MIN_WATER_LEVEL = 300;

void setup() {
  Serial.begin(9600);
  dht.begin();
  dsensor.begin();
  pinMode(pump1Pin, OUTPUT);
  pinMode(pump2Pin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(pump1Pin, LOW);
  digitalWrite(pump2Pin, LOW);
  digitalWrite(buzzerPin, LOW);
}

void loop() {
  int waterLevel = analogRead(waterLevelPin);
  int phRaw = analogRead(phPin);
  int turbidityRaw = analogRead(turbidityPin);
  int chlorineRaw = analogRead(chlorinePin);

  float pH = (phRaw / 1023.0) * 14.0; // calibrate on hardware
  float humidity = dht.readHumidity();
  float dhtTemp = dht.readTemperature();
  dsensor.requestTemperatures();
  float dsTemp = dsensor.getTempCByIndex(0);

  // pump control (from report logic)
  if (waterLevel >= MAX_WATER_LEVEL) {
    digitalWrite(pump1Pin, LOW);
    digitalWrite(pump2Pin, HIGH);
  } else if (waterLevel <= MIN_WATER_LEVEL) {
    digitalWrite(pump1Pin, HIGH);
    digitalWrite(pump2Pin, LOW);
  } else {
    digitalWrite(pump1Pin, LOW);
    digitalWrite(pump2Pin, LOW);
  }

  // buzzer logic
  bool alert = false;
  if (pH < 6.5 || pH > 7.5) alert = true;
  if (turbidityRaw > 700) alert = true;
  if (chlorineRaw < 300) alert = true;
  if (isnan(humidity) || isnan(dhtTemp) || dsTemp == DEVICE_DISCONNECTED_C) alert = true;
  digitalWrite(buzzerPin, alert ? HIGH : LOW);

  // print JSON line to serial (gateway reads this)
  Serial.print("{");
  Serial.print("\"waterLevel\":"); Serial.print(waterLevel); Serial.print(",");
  Serial.print("\"pH\":"); Serial.print(pH, 2); Serial.print(",");
  Serial.print("\"dhtTemp\":"); Serial.print(dhtTemp, 2); Serial.print(",");
  Serial.print("\"dhtHum\":"); Serial.print(humidity, 2); Serial.print(",");
  Serial.print("\"dsTemp\":"); Serial.print(dsTemp, 2); Serial.print(",");
  Serial.print("\"turbidity\":"); Serial.print(turbidityRaw); Serial.print(",");
  Serial.print("\"chlorine\":"); Serial.print(chlorineRaw);
  Serial.println("}");

  delay(2000);
}
