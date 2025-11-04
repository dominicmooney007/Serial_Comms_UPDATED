#!/usr/bin/env python3
"""
Quick Start Guide - Basic Serial Communication
Raspberry Pi to Arduino Message Sender

This script sends a simple text message from Raspberry Pi to Arduino.
The message will appear in the Arduino Serial Monitor.

Hardware Required:
- Raspberry Pi 5
- Arduino Uno R3
- USB A to B cable

Before running:
1. Upload arduino_receiver.ino to your Arduino
2. Close the Arduino Serial Monitor (only one program can use the port at a time)
3. Verify the port is /dev/ttyACM0 (or change in code below)

Usage:
    python3 test_serial.py

Created: October 2025
For: Quick Start Guide
"""

import serial
import time

# Configuration
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

try:
    # Connect to Arduino
    print("Connecting to Arduino...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(3)  # Wait for Arduino to reset - CRITICAL!

    # Send message
    message = "Hello from Raspberry Pi!"
    print(f"Sending: {message}")
    ser.write(message.encode())
    ser.write(b'\n')  # Message delimiter
    ser.flush()  # Ensure data is sent immediately

    # Wait for Arduino to process and respond
    time.sleep(0.5)

    # Read Arduino's response
    print("\nWaiting for Arduino response...")
    while ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        if response:
            print(f"Arduino says: {response}")

    time.sleep(1)
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
