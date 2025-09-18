/*
  controller_esp32.ino
  ESP32 -> ThingSpeak uploader + local control (pumps, buzzer)
*/

#include "secrets.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define DHTPIN 27
#define DHTTYPE DHT22
#define ONE_WIRE_BUS 26

// analog pins - adjust per board
const int waterLevelPin = 34;
const int phPin = 35;
const int turbidityPin = 32;
const int chlorinePin = 33;

// control pins
const int pump1Pin = 25;
const int pump2Pin = 26;
const int buzzerPin = 14;

// thresholds (calibrate)
const int MAX_WATER_LEVEL = 3000; // ESP32 ADC 0-4095
const int MIN_WATER_LEVEL = 1000;
const float TEMP_MAX = 30.0;
const float TEMP_MIN = 20.0;

const unsigned long UPLOAD_INTERVAL_MS = 20000;
unsigned long lastUpload = 0;

DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature dsensor(&oneWire);

const char* THINGSPEAK_HOST = "http://api.thingspeak.com/update";

void setupPins() {
  pinMode(pump1Pin, OUTPUT);
  pinMode(pump2Pin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(pump1Pin, LOW);
  digitalWrite(pump2Pin, LOW);
  digitalWrite(buzzerPin, LOW);
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  dsensor.begin();
  setupPins();

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected.");
}

int analogReadSafe(int pin) {
  return analogRead(pin);
}

float readDS18B20() {
  dsensor.requestTemperatures();
  float t = dsensor.getTempCByIndex(0);
  if (t == DEVICE_DISCONNECTED_C) return NAN;
  return t;
}

void controlPumps(int wl, float tC) {
  if (wl >= MAX_WATER_LEVEL) {
    digitalWrite(pump1Pin, LOW);
    digitalWrite(pump2Pin, HIGH);
  } else if (wl <= MIN_WATER_LEVEL) {
    digitalWrite(pump1Pin, HIGH);
    digitalWrite(pump2Pin, LOW);
  } else {
    digitalWrite(pump1Pin, LOW);
    digitalWrite(pump2Pin, LOW);
  }

  // simple temperature control example: if too hot, ensure pump1 on
  if (!isnan(tC) && tC > TEMP_MAX) digitalWrite(pump1Pin, HIGH);
}

void uploadToThingSpeak(int wl, float pH, float dhtT, float dhtH, float dsT, int turb, int chl) {
  if (WiFi.status() != WL_CONNECTED) return;
  String url = String(THINGSPEAK_HOST) + "?api_key=" + THINGSPEAK_API_KEY;
  url += "&field1=" + String(wl);
  url += "&field2=" + String(pH, 2);
  url += "&field3=" + String(dhtT, 2);
  url += "&field4=" + String(dhtH, 2);
  url += "&field5=" + String(dsT, 2);
  url += "&field6=" + String(turb);
  url += "&field7=" + String(chl);

  HTTPClient http;
  http.begin(url);
  int code = http.GET();
  if (code > 0) {
    String resp = http.getString();
    Serial.printf("ThingSpeak: code=%d resp=%s\n", code, resp.c_str());
  } else {
    Serial.printf("ThingSpeak failed: %d\n", code);
  }
  http.end();
}

void setupBuzzer(bool on) {
  digitalWrite(buzzerPin, on ? HIGH : LOW);
}

void loop() {
  unsigned long now = millis();
  if (now - lastUpload < UPLOAD_INTERVAL_MS) {
    delay(200);
    return;
  }
  lastUpload = now;

  int waterLevel = analogReadSafe(waterLevelPin);
  int phRaw = analogReadSafe(phPin);
  int turbidityRaw = analogReadSafe(turbidityPin);
  int chlorineRaw = analogReadSafe(chlorinePin);

  float pH = (phRaw / 4095.0) * 14.0; // TODO: replace with calibrated conversion
  float dhtH = dht.readHumidity();
  float dhtT = dht.readTemperature();
  float dsT = readDS18B20();

  // local control
  controlPumps(waterLevel, dsT);

  // alerts
  bool alert = false;
  if (pH < 6.5 || pH > 7.5) alert = true;
  if (turbidityRaw > 2000) alert = true;  // tune after calibration
  if (chlorineRaw < 1500) alert = true;   // tune after calibration
  if (isnan(dhtH) || isnan(dhtT) || isnan(dsT)) alert = true;
  setupBuzzer(alert);

  // upload
  uploadToThingSpeak(waterLevel, pH, dhtT, dhtH, dsT, turbidityRaw, chlorineRaw);

  // debug JSON line
  Serial.printf("{\"waterLevel\":%d,\"pH\":%.2f,\"dhtTemp\":%.2f,\"dhtHum\":%.2f,\"dsTemp\":%.2f,\"turbidity\":%d,\"chlorine\":%d}\n",
                waterLevel, pH, dhtT, dhtH, dsT, turbidityRaw, chlorineRaw);

  delay(1000);
}
