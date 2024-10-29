from flask import Flask, render_template, request, jsonify
import serial
import time

app = Flask(__name__)

ser = None

def initialize_serial(port='COM9', baudrate=9600, timeout=1):
    global ser
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Wait for the serial connection to establish
        print("Serial connection established.")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")

def move_servo(servo_num, angle):
    if ser:
        command = f"{servo_num} {angle}\n"
        try:
            ser.write(command.encode())
            ser.flush()
        except serial.SerialException as e:
            print(f"Error sending command: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    command = data.get('command')
    
    try:
        if command == 'sit':
            # Implement sit command
            pass
        elif command == 'stand':
            # Implement stand command
            pass
        elif command == 'animation':
            # Implement animation command
            pass
        elif command.startswith('servo'):
            parts = command.split()
            if len(parts) == 3:
                try:
                    servo_num = int(parts[1])
                    angle = int(parts[2])
                    move_servo(servo_num, angle)
                except ValueError:
                    return jsonify({'status': 'error', 'message': 'Invalid command format'})
        else:
            return jsonify({'status': 'error', 'message': 'Unknown command'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

    return jsonify({'status': 'success'})

if __name__ == "__main__":
    initialize_serial()
    app.run(debug=True)
    if ser:
        ser.close()
