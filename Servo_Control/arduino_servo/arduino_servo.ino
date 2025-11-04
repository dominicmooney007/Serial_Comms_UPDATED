/*
 * Servo Motor Control - Arduino Sketch
 *
 * This sketch receives servo angle commands from Raspberry Pi via serial
 * and controls an SG90 servo motor.
 *
 * Hardware Setup:
 * - SG90 Servo connected to Arduino Uno R3
 * - Signal wire (Orange/Yellow): Pin 9
 * - Power wire (Red): 5V
 * - Ground wire (Brown): GND
 *
 * IMPORTANT: SG90 can draw up to 100-250mA when moving under load.
 * For testing without load, Arduino 5V is sufficient.
 * For applications with load, use external 5V power supply (4.8-6V).
 *
 * Communication Protocol:
 * - Receives: "SERVO:angle\n" (e.g., "SERVO:90\n")
 * - Sends: Confirmation message back to Raspberry Pi
 * - Baud Rate: 9600
 *
 * SG90 Specifications:
 * - Operating Voltage: 4.8V - 6V
 * - Operating Speed: 0.12s/60° at 4.8V (0.1s/60° at no load)
 * - Stall Torque: 1.2kg/cm at 4.8V, 1.6kg/cm at 6V
 * - Rotation: 0° to 180° (typical servo range)
 * - Weight: 9g
 * - Size: 22 x 11.5 x 27mm
 */

#include <Servo.h>

// Configuration
const int SERVO_PIN = 9;          // PWM pin for servo signal
const int LED_PIN = LED_BUILTIN;  // Built-in LED for status indication

// Servo object
Servo myServo;

// Variables
String inputString = "";          // String to hold incoming data
boolean stringComplete = false;   // Whether the string is complete
int currentAngle = 90;            // Track current servo position

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Attach servo to pin
  myServo.attach(SERVO_PIN);

  // Initialize servo to center position (90 degrees)
  myServo.write(90);
  currentAngle = 90;

  // Initialize LED pin
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Reserve 200 bytes for the input string
  inputString.reserve(200);

  // Startup message
  Serial.println("Arduino Servo Control Ready");
  Serial.println("Servo: SG90 on Pin 9");
  Serial.println("Centered at 90 degrees");
  Serial.println("Waiting for commands...");

  // Flash LED to indicate ready
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
}

void loop() {
  // Check if a complete command has been received
  if (stringComplete) {
    processCommand(inputString);

    // Clear the string for next command
    inputString = "";
    stringComplete = false;
  }
}

/*
 * SerialEvent occurs whenever new data comes in the serial receive buffer.
 * This runs between each loop() execution.
 */
void serialEvent() {
  while (Serial.available()) {
    // Read the new byte
    char inChar = (char)Serial.read();

    // Add it to the inputString
    inputString += inChar;

    // If the incoming character is a newline, set flag
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

/*
 * Process incoming servo command
 * Expected format: "SERVO:angle\n"
 */
void processCommand(String command) {
  // Remove whitespace and newline characters
  command.trim();

  // Check if command starts with "SERVO:"
  if (command.startsWith("SERVO:")) {
    // Extract angle value after "SERVO:"
    String angleStr = command.substring(6); // Get substring after "SERVO:"
    int targetAngle = angleStr.toInt();

    // Validate angle range (0-180 degrees)
    if (targetAngle >= 0 && targetAngle <= 180) {
      moveServo(targetAngle);
    } else {
      Serial.print("Error: Invalid angle ");
      Serial.print(targetAngle);
      Serial.println(". Must be 0-180 degrees.");
      digitalWrite(LED_PIN, HIGH);
      delay(100);
      digitalWrite(LED_PIN, LOW);
    }
  } else {
    Serial.print("Error: Unknown command: ");
    Serial.println(command);
  }
}

/*
 * Move servo to specified angle with smooth motion
 * SG90 takes approximately 0.12s per 60 degrees at 4.8V
 */
void moveServo(int targetAngle) {
  // Turn on LED to indicate movement
  digitalWrite(LED_PIN, HIGH);

  // Calculate movement direction and distance
  int angleDiff = abs(targetAngle - currentAngle);
  int step = (targetAngle > currentAngle) ? 1 : -1;

  // Smooth movement: step by step with small delay
  // SG90 is lightweight and fast, but smooth motion prevents mechanical stress
  if (angleDiff > 5) {
    // For large movements, use incremental steps
    for (int angle = currentAngle;
         (step > 0) ? (angle <= targetAngle) : (angle >= targetAngle);
         angle += step) {
      myServo.write(angle);
      delay(15); // Small delay for smooth motion (adjust if needed)
    }
  } else {
    // For small movements, go directly
    myServo.write(targetAngle);
  }

  // Update current position
  currentAngle = targetAngle;

  // Calculate approximate movement time for SG90
  // At 4.8V: 0.12s per 60 degrees = 2ms per degree
  int moveTime = (angleDiff * 2);
  delay(moveTime); // Wait for servo to reach position

  // Turn off LED
  digitalWrite(LED_PIN, LOW);

  // Send confirmation
  Serial.print("Servo moved to ");
  Serial.print(targetAngle);
  Serial.println(" degrees");
}

/*
 * Alternative version: Direct move without smoothing
 * Uncomment this and comment out the above moveServo() if you prefer instant movement
 */
/*
void moveServo(int targetAngle) {
  digitalWrite(LED_PIN, HIGH);

  myServo.write(targetAngle);
  currentAngle = targetAngle;

  // Calculate movement time for SG90 (0.12s per 60 degrees)
  int angleDiff = abs(targetAngle - currentAngle);
  int moveTime = (angleDiff * 2) + 50; // Add 50ms buffer
  delay(moveTime);

  digitalWrite(LED_PIN, LOW);

  Serial.print("Servo moved to ");
  Serial.print(targetAngle);
  Serial.println(" degrees");
}
*/
