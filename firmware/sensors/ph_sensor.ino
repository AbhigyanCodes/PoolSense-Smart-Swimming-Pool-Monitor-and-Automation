/*
  ph_sensor.ino (test)
  Read pH sensor analog value and convert roughly to pH (0-14).
  Calibrate on hardware with buffer solutions.
*/

const int phPin = A1;

void setup() {
  Serial.begin(9600);
}

float analogToPH(int raw) {
  // Very rough conversion; replace with calibration
  return (raw / 1023.0) * 14.0;
}

void loop() {
  int raw = analogRead(phPin);
  float pH = analogToPH(raw);
  Serial.print("pH: ");
  Serial.println(pH);
  delay(1000);
}
