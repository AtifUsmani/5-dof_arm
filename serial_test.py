import serial
import time

def test_serial(port='COM4'):
    try:
        with serial.Serial(port, 9600, timeout=1) as ser:
            print(f"Successfully opened {port}")
            time.sleep(10)  # Keep the port open for 10 seconds
            print(f"{port} remains open")
    except serial.SerialException as e:
        print(f"Failed to open {port}: {e}")

test_serial('COM4')
