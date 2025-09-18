/*
  serial_test.ino
  Basic sketch to send test JSON lines over serial for gateway testing
*/

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println("{\"waterLevel\":500,\"pH\":7.1,\"dhtTemp\":25.3,\"dhtHum\":55.2,\"dsTemp\":25.0,\"turbidity\":120,\"chlorine\":400}");
  delay(2000);
}
