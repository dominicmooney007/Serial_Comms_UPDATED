/*
  Quick Start Guide - Two-Way Communication
  Arduino Echo and Response Example

  This sketch receives messages from Raspberry Pi and sends back
  a confirmation response.

  Hardware Required:
  - Arduino Uno R3
  - USB cable connected to Raspberry Pi

  Instructions:
  1. Upload this sketch to your Arduino
  2. Run the Python two-way script on Raspberry Pi
  3. Arduino will receive messages and echo them back

  Created: October 2025
  For: Quick Start Guide - Two-Way Communication Example
*/

void setup() {
  // Initialize serial communication at 9600 bits per second
  Serial.begin(9600);

  // Wait for serial port to be ready
  while (!Serial) {
    ; // Wait for serial port to connect
  }

  // Send ready message
  Serial.println("Arduino Ready!");
}

void loop() {
  // Check if data has arrived
  if (Serial.available() > 0) {

    // Read the incoming message until newline character
    String message = Serial.readStringUntil('\n');

    // Echo back with confirmation
    Serial.print("Arduino received: ");
    Serial.println(message);
  }
}
