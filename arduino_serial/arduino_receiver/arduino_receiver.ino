/*
  Quick Start Guide - Arduino Receiver
  Basic Serial Communication Example

  This sketch receives text messages from the Raspberry Pi via serial
  communication and displays them in the Arduino Serial Monitor.

  Hardware Required:
  - Arduino Uno R3
  - USB cable connected to Raspberry Pi

  Instructions:
  1. Upload this sketch to your Arduino
  2. Open Serial Monitor (Tools > Serial Monitor)
  3. Set baud rate to 9600
  4. Run the Python script on Raspberry Pi
  5. Watch for incoming messages!

  Created: October 2025
  For: Quick Start Guide - Raspberry Pi & Arduino Communication
*/

void setup() {
  // Initialize serial communication at 9600 bits per second
  Serial.begin(9600);

  // Send a ready message
  Serial.println("Arduino ready to receive!");
  Serial.println("Waiting for messages...");
  Serial.println("----------------------------");
}

void loop() {
  // Check if data has arrived
  if (Serial.available() > 0) {

    // Read the incoming message until newline character
    String message = Serial.readStringUntil('\n');

    // Display the received message
    Serial.print("Received: ");
    Serial.println(message);
    Serial.println("----------------------------");
  }
}
