/*
  water_level.ino (test)
  Simple ADC read to test water level sensor and serial output.
*/

const int waterPin = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int v = analogRead(waterPin);
  Serial.println(v);
  delay(500);
}
