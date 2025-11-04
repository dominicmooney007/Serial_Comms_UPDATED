#!/usr/bin/env python3
"""
Servo Motor Control - Raspberry Pi to Arduino
This script controls an SG90 servo motor connected to the Arduino via serial commands.
The SG90 servo can be positioned at specific angles (0-180 degrees).
"""

import serial
import time

# Configuration
SERIAL_PORT = '/dev/ttyUSB0'  # Default Arduino port on Raspberry Pi
BAUD_RATE = 9600
TIMEOUT = 1

def set_servo_angle(ser, angle):
    """
    Send angle command to Arduino to position servo.

    Args:
        ser: Serial connection object
        angle: Desired angle (0-180 degrees)

    Returns:
        bool: True if successful, False otherwise
    """
    if not 0 <= angle <= 180:
        print(f"Error: Angle must be between 0 and 180 degrees. Got {angle}")
        return False

    # Send angle command in format "SERVO:angle\n"
    command = f"SERVO:{angle}\n"
    ser.write(command.encode())
    print(f"Sent: {command.strip()}")

    # Wait for Arduino response
    time.sleep(0.1)
    if ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        print(f"Arduino says: {response}")
        return True

    return True


def sweep_servo(ser, delay=0.5):
    """
    Sweep servo from 0 to 180 degrees and back.

    Args:
        ser: Serial connection object
        delay: Delay between movements in seconds
    """
    print("\n=== Sweeping Servo ===")

    # Sweep forward (0 to 180)
    print("Sweeping forward (0 -> 180)...")
    for angle in range(0, 181, 15):
        set_servo_angle(ser, angle)
        time.sleep(delay)

    # Sweep backward (180 to 0)
    print("Sweeping backward (180 -> 0)...")
    for angle in range(180, -1, -15):
        set_servo_angle(ser, angle)
        time.sleep(delay)

    print("Sweep complete!\n")


def preset_positions(ser):
    """
    Move servo to preset positions with user selection.

    Args:
        ser: Serial connection object
    """
    print("\n=== Preset Positions ===")
    positions = {
        '1': (0, "Minimum (0°)"),
        '2': (45, "45 degrees"),
        '3': (90, "Center (90°)"),
        '4': (135, "135 degrees"),
        '5': (180, "Maximum (180°)")
    }

    while True:
        print("\nPreset Positions:")
        for key, (angle, description) in positions.items():
            print(f"{key}. {description}")
        print("6. Back to main menu")

        choice = input("\nSelect position (1-6): ").strip()

        if choice == '6':
            break
        elif choice in positions:
            angle, description = positions[choice]
            print(f"\nMoving to {description}...")
            set_servo_angle(ser, angle)
        else:
            print("Invalid choice. Please select 1-6")


def manual_control(ser):
    """
    Allow manual angle input for precise servo control.

    Args:
        ser: Serial connection object
    """
    print("\n=== Manual Servo Control ===")
    print("Enter angle (0-180) or 'q' to quit\n")

    while True:
        user_input = input("Enter angle: ").strip()

        if user_input.lower() == 'q':
            break

        try:
            angle = int(user_input)
            set_servo_angle(ser, angle)
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 180, or 'q' to quit")


def smooth_move(ser, start_angle, end_angle, steps=20, delay=0.05):
    """
    Smoothly move servo from start angle to end angle.

    Args:
        ser: Serial connection object
        start_angle: Starting angle (0-180)
        end_angle: Ending angle (0-180)
        steps: Number of steps for smooth movement
        delay: Delay between each step
    """
    print(f"\nSmooth move from {start_angle}° to {end_angle}°")

    step_size = (end_angle - start_angle) / steps

    for i in range(steps + 1):
        angle = int(start_angle + (step_size * i))
        set_servo_angle(ser, angle)
        time.sleep(delay)

    print("Movement complete!\n")


def main():
    """Main function with menu for servo control"""
    print("=" * 50)
    print("SG90 Servo Control - Raspberry Pi to Arduino")
    print("=" * 50)
    print("\nMake sure:")
    print("- SG90 servo is connected to Arduino pin 9")
    print("- Arduino is running the servo control sketch")
    print("- Servo has adequate power supply (4.8-6V)")
    print()

    # Open serial connection
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud")
        time.sleep(2)  # Wait for connection to establish
        print("Connection established!\n")
    except serial.SerialException as e:
        print(f"\nSerial Error: {e}")
        print("Make sure Arduino is connected to the correct port.")
        print(f"Current port: {SERIAL_PORT}\n")
        return

    try:
        while True:
            print("\n" + "=" * 50)
            print("Servo Control Menu:")
            print("=" * 50)
            print("1. Manual Control (enter specific angle)")
            print("2. Preset Positions (0°, 45°, 90°, 135°, 180°)")
            print("3. Sweep Demo (0° to 180° and back)")
            print("4. Smooth Movement Demo")
            print("5. Center Servo (90°)")
            print("6. Exit")
            print()

            choice = input("Enter choice (1-6): ").strip()

            if choice == '1':
                manual_control(ser)
            elif choice == '2':
                preset_positions(ser)
            elif choice == '3':
                sweep_servo(ser)
            elif choice == '4':
                print("\nSmooth Movement Demo:")
                smooth_move(ser, 0, 180, steps=30, delay=0.05)
                time.sleep(1)
                smooth_move(ser, 180, 0, steps=30, delay=0.05)
            elif choice == '5':
                print("\nCentering servo at 90°...")
                set_servo_angle(ser, 90)
            elif choice == '6':
                print("\nCentering servo before exit...")
                set_servo_angle(ser, 90)
                time.sleep(1)
                print("Goodbye!")
                break
            else:
                print("\nInvalid choice. Please select 1-6")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user...")
        print("Centering servo before exit...")
        set_servo_angle(ser, 90)
        time.sleep(1)

    except Exception as e:
        print(f"\nError: {e}")

    finally:
        ser.close()
        print("Connection closed")


if __name__ == "__main__":
    main()
