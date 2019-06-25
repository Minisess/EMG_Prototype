int sensorpin = A0;

void setup() {
 Serial.begin(115200);
}

void loop() {
 if (Serial.read() == 's') {
     showSensorData();
 }
 delay(1);
}

void showSensorData() {
     int sensorValue = analogRead(sensorpin);
     Serial.println(sensorValue);
}
