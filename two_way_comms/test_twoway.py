#!/usr/bin/env python3
"""
Quick Start Guide - Two-Way Communication
Raspberry Pi and Arduino Bidirectional Communication

This script sends a message to Arduino and reads the response back.

Hardware Required:
- Raspberry Pi 5
- Arduino Uno R3
- USB A to B cable

Before running:
1. Upload arduino_twoway.ino to your Arduino
2. Close the Arduino Serial Monitor
3. Verify the port is /dev/ttyACM0 (or change in code below)

Usage:
    python3 test_twoway.py

Created: October 2025
For: Quick Start Guide - Two-Way Communication Example
"""

import serial
import time

# Configuration
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

try:
    # Connect to Arduino
    print("Connecting to Arduino...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)

    # Wait longer for Arduino to complete reset and setup
    print("Waiting for Arduino to reset and initialize...")
    time.sleep(3)  # Increased to 3 seconds

    # Flush any old data from buffer
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    print("Buffers cleared")

    # Send message
    message = "Hello Arduino!"
    print(f"Sending: {message}")
    ser.write(message.encode() + b'\n')
    ser.flush()  # Ensure data is sent immediately

    # Wait and read response (Arduino needs time to process)
    print("Waiting for response...")
    time.sleep(1.5)  # Increased wait time

    # Check how many bytes are waiting
    waiting = ser.in_waiting
    print(f"Bytes waiting: {waiting}")

    if waiting > 0:
        response = ser.readline().decode().strip()
        print(f"Arduino replied: {response}")
    else:
        print("No response from Arduino (timeout)")
        print("\nTroubleshooting tips:")
        print("1. Verify Arduino sketch is uploaded")
        print("2. Check Arduino Serial Monitor is CLOSED")
        print("3. Try pressing reset button on Arduino, then run script again")

    ser.close()
    print("\nCommunication complete!")

except serial.SerialException as e:
    print(f"Error: Could not open serial port {SERIAL_PORT}")
    print(f"Details: {e}")
    print("\nTroubleshooting:")
    print("1. Is the Arduino connected?")
    print("2. Is the Arduino Serial Monitor closed?")
    print("3. Try: sudo chmod 666 /dev/ttyACM0")
    print("4. Check port: ls /dev/ttyACM*")

except KeyboardInterrupt:
    print("\nProgram interrupted by user")

except Exception as e:
    print(f"Unexpected error: {e}")
