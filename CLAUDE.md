# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational project demonstrating serial communication between Raspberry Pi 5 and Arduino Uno R3. The project contains multiple examples of varying complexity:
- Basic one-way communication (Raspberry Pi → Arduino)
- Two-way communication with echo responses
- LED control via serial commands
- Servo motor control (SG90)
- Bidirectional messaging

All communication occurs via USB serial connection (typically `/dev/ttyUSB0` or `/dev/ttyACM0`) at 9600 baud using PySerial library.

## Project Structure

```
/home/dom/Serial_Comms/
├── requirements.txt                # Python dependencies (pyserial>=3.5)
├── arduino_serial/                 # Basic communication examples
│   ├── test_serial.py              # Quick start - basic one-way communication
│   ├── arduino_receiver/           # Simple receiver sketch
│   └── arduino_receiver_with_led/  # Receiver with LED indicator
├── Servo_Control/
│   ├── servo_control.py            # SG90 servo control script
│   └── arduino_servo/              # Arduino servo control sketch
├── two_way_comms/
│   ├── test_twoway.py              # Bidirectional communication test
│   ├── test_diagnostic.py          # Diagnostic tool for troubleshooting
│   └── arduino_twoway/             # Arduino two-way sketch
└── venv/                           # Python virtual environment
```

## Running the Code

### Prerequisites

```bash
# Grant serial port access (required once, then logout/login)
sudo usermod -a -G dialout $USER

# Verify Arduino connection
ls /dev/tty*          # Look for /dev/ttyUSB0 or /dev/ttyACM0
lsusb                 # Should show "Arduino SA Uno R3"
```

### Run Python Scripts

All Python scripts are executable:

```bash
# Activate virtual environment (recommended)
source venv/bin/activate

# Basic one-way communication (quick start)
python3 arduino_serial/test_serial.py

# Servo motor control
python3 Servo_Control/servo_control.py

# Two-way communication test
python3 two_way_comms/test_twoway.py

# Diagnostic tool (for troubleshooting serial connection)
python3 two_way_comms/test_diagnostic.py
```

### Install Dependencies

```bash
# Using requirements.txt
pip3 install -r requirements.txt

# Or manually
pip3 install pyserial
```

### Upload Arduino Sketches

Using Arduino IDE on Raspberry Pi:
1. Open .ino file from appropriate subdirectory
2. Select Tools → Board → Arduino Uno
3. Select Tools → Port → /dev/ttyUSB0 (or /dev/ttyACM0)
4. Click Upload button
5. **Important**: Close Arduino Serial Monitor before running Python scripts

## Serial Communication Architecture

### Communication Pattern

All Python scripts follow this pattern:
```python
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # CRITICAL: Wait for Arduino reset after connection

# Send (must encode to bytes)
ser.write("message\n".encode())

# Receive (must decode from bytes)
if ser.in_waiting > 0:
    response = ser.readline().decode('utf-8').strip()

ser.close()
```

### Critical Configuration

**Python side** (`SERIAL_PORT`, `BAUD_RATE`, `TIMEOUT`):
- Port: `/dev/ttyUSB0` or `/dev/ttyACM0` (check with `ls /dev/tty*`)
- Baud: 9600 (must match Arduino)
- Timeout: 1 second (read timeout)

**Arduino side** (`Serial.begin()`):
- Baud: 9600 (must match Python)
- Use `Serial.println()` for newline-terminated messages (expected by `readline()`)

### Data Encoding Rules

- **Python → Arduino**: Use `.encode()` or `b''` prefix to convert strings to bytes
- **Arduino → Python**: Use `.decode('utf-8')` to convert bytes to strings
- **Newline handling**: Arduino sends `\n` with `println()`, Python reads with `readline()`

## Common Development Tasks

### Add New Communication Example

1. Create new subdirectory under `/home/dom/Serial_Comms/`
2. Write Python script following the standard serial pattern (see above)
3. Write Arduino .ino sketch in subdirectory
4. Update this file with new example

### Modify Serial Port

If Arduino appears on different port (check with `ls /dev/tty*`):
- Update `SERIAL_PORT` constant in Python scripts
- Common ports: `/dev/ttyUSB0`, `/dev/ttyACM0`, `/dev/ttyUSB1`

### Troubleshoot Serial Communication

**Port access denied:**
```bash
sudo usermod -a -G dialout $USER  # Then logout/login
# OR temporary fix:
sudo chmod 666 /dev/ttyUSB0
```

**No response from Arduino:**
- Verify baud rates match (9600 on both sides)
- Increase delay after `serial.Serial()` to 2-3 seconds
- Check Arduino sketch is uploaded and correct
- Ensure Arduino Serial Monitor is closed

**Garbage characters:**
- Baud rate mismatch - verify both use 9600
- Add `ser.reset_input_buffer()` after opening connection

**Port busy:**
- Only one program can access serial port at a time
- Close Arduino IDE Serial Monitor
- Kill other Python scripts using port: `fuser /dev/ttyUSB0`

### Protocol Design Pattern

For structured commands (see servo_control.py and Servo_Control/arduino_servo/):
- Format: `COMMAND:parameter\n`
- Example: `SERVO:90\n` to set servo to 90 degrees
- Arduino parses using `indexOf(':')` and `substring()`
- Always include newline terminator for `readline()`

### Script Purposes

**arduino_serial/test_serial.py**: Basic one-way communication example. Sends a message from Raspberry Pi to Arduino and reads Arduino's response. Good starting point for learning serial communication.

**two_way_comms/test_twoway.py**: Bidirectional communication example with message exchange between Raspberry Pi and Arduino.

**two_way_comms/test_diagnostic.py**: Diagnostic tool for troubleshooting serial connection issues. Useful for verifying port configuration, baud rates, and basic connectivity.

**Servo_Control/servo_control.py**: Demonstrates command-based protocol for controlling SG90 servo motor. Uses structured `COMMAND:parameter` format.

## Hardware Notes

### Servo Motor Control (Servo_Control/)

- Servo type: SG90 micro servo
- Arduino connection: Signal pin → Digital pin 9
- Power requirements: 4.8-6V (may need external power supply for multiple servos)
- Angle range: 0-180 degrees
- Control protocol: `SERVO:angle\n` where angle is 0-180

### LED Control

- Built-in LED: Pin 13 (LED_BUILTIN)
- External LEDs: Connect through 220Ω resistor
- Control commands: '0' (off), '1' (on)

## Important Constraints

- **2-second delay**: Always wait 2+ seconds after opening serial connection (Arduino resets on connection)
- **Exclusive port access**: Only one program can use serial port at a time
- **Encoding requirement**: All Python strings must be encoded to bytes before sending
- **Matching baud rates**: Both devices must use 9600 baud
- **Virtual environment**: Project has venv/ with PySerial installed - use `source venv/bin/activate`
