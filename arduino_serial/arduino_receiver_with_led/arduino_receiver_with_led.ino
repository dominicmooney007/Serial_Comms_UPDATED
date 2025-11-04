/*
  Quick Start Guide - Arduino Receiver with LED Indicator
  Serial Communication with Visual Feedback

  This sketch receives text messages from the Raspberry Pi via serial
  communication and provides both visual (LED) and text confirmation.

  Hardware Required:
  - Arduino Uno R3
  - USB cable connected to Raspberry Pi
  - Built-in LED (pin 13) - no external components needed

  Features:
  - Receives messages from Raspberry Pi
  - Flashes onboard LED 3 times when message received
  - Sends confirmation back to Python
  - Displays messages in Serial Monitor (optional)

  Instructions:
  1. Upload this sketch to your Arduino
  2. Run the Python script on Raspberry Pi
  3. Watch for LED flashing - confirms message received!
  4. Check Python output for Arduino's response

  Created: November 2025
  For: Quick Start Guide - Raspberry Pi & Arduino Communication
*/

// LED pin (built-in LED on Arduino Uno)
const int LED_PIN = LED_BUILTIN;

void setup() {
  // Initialize serial communication at 9600 bits per second
  Serial.begin(9600);

  // Initialize LED pin
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Send a ready message
  Serial.println("Arduino ready to receive!");
  Serial.println("Waiting for messages...");
  Serial.println("LED will flash when message is received");
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

    // Flash LED to indicate message received
    flashLED(10);
  }
}

// Function to flash the LED a specified number of times
void flashLED(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_PIN, HIGH);  // Turn LED on
    delay(150);                    // Wait 150ms
    digitalWrite(LED_PIN, LOW);   // Turn LED off
    delay(150);                    // Wait 150ms
  }
}
