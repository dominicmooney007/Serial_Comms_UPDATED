#!/usr/bin/env python3
"""
Diagnostic script for Arduino serial communication
Tests connection and identifies potential issues
"""

import serial
import time

# Configuration
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

print("="*50)
print("Arduino Serial Communication Diagnostic")
print("="*50)

try:
    # Test 1: Open connection
    print("\n[Test 1] Opening serial port...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    print(f"✓ Successfully opened {SERIAL_PORT}")

    # Test 2: Wait for Arduino reset
    print("\n[Test 2] Waiting for Arduino to reset (3 seconds)...")
    time.sleep(3)
    print("✓ Wait complete")

    # Test 3: Check for startup message
    print("\n[Test 3] Checking for startup message...")
    if ser.in_waiting > 0:
        startup_msg = ser.readline().decode().strip()
        print(f"✓ Arduino sent: '{startup_msg}'")
    else:
        print("✗ No startup message received")
        print("  This might mean:")
        print("  - Arduino sketch not uploaded")
        print("  - Wrong baud rate")
        print("  - Arduino not connected properly")

    # Test 4: Clear buffers
    print("\n[Test 4] Clearing buffers...")
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    print("✓ Buffers cleared")

    # Test 5: Send test message
    print("\n[Test 5] Sending test message...")
    test_msg = "Test Message"
    ser.write(test_msg.encode() + b'\n')
    ser.flush()
    print(f"✓ Sent: '{test_msg}'")

    # Test 6: Wait for response
    print("\n[Test 6] Waiting for response (2 seconds)...")
    time.sleep(2)

    bytes_waiting = ser.in_waiting
    print(f"  Bytes in buffer: {bytes_waiting}")

    if bytes_waiting > 0:
        response = ser.readline().decode().strip()
        print(f"✓ Arduino replied: '{response}'")
        print("\n✓✓✓ SUCCESS! Communication is working! ✓✓✓")
    else:
        print("✗ No response received")

        # Additional diagnostics
        print("\n[Additional Diagnostics]")
        print(f"  Serial port: {ser.port}")
        print(f"  Baud rate: {ser.baudrate}")
        print(f"  Timeout: {ser.timeout}")
        print(f"  Is open: {ser.is_open}")

        print("\nPossible issues:")
        print("1. Arduino sketch not uploaded - upload arduino_twoway.ino")
        print("2. Arduino Serial Monitor is open - close it")
        print("3. Wrong serial port - check with: ls /dev/tty*")
        print("4. Permissions issue - try: sudo chmod 666 /dev/ttyUSB0")

    ser.close()
    print("\n[Test 7] Serial port closed")

except serial.SerialException as e:
    print(f"\n✗ Serial Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check connection: lsusb")
    print("2. Check port: ls -l /dev/ttyUSB* /dev/ttyACM*")
    print("3. Check permissions: groups $USER")
    print("4. Add to dialout group: sudo usermod -a -G dialout $USER")

except KeyboardInterrupt:
    print("\n\nInterrupted by user")

except Exception as e:
    print(f"\n✗ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("Diagnostic complete")
print("="*50)
