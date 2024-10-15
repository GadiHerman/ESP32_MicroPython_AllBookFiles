#include <SoftwareSerial.h>


// RX is digital pin 2 (connect to TX of other device)
// TX is digital pin 3 (connect to RX of other device)
SoftwareSerial ESP32Serial(2, 3); // RX, TX


void setup()
{
  // Open serial communications and wait for port to open:
  Serial.begin(115200);


  // set the data rate for the SoftwareSerial port
  ESP32Serial.begin(115200);
}


void loop() // run over and over
{
  if (ESP32Serial.available())
    Serial.write(ESP32Serial.read());
  if (Serial.available())
    ESP32Serial.write(Serial.read());
}
