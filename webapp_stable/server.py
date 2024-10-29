from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import serial
import time
import threading
import logging
import numpy as np
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

# Set up logging
logging.basicConfig(filename='flask_app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

ser = None
current_angles = [90] * 6  # Initialize with default angles
ser_lock = threading.Lock()

def initialize_serial(port='COM9', baudrate=9600, timeout=1):
    global ser
    try:
        if ser and ser.is_open:
            ser.close()
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Wait for the serial connection to establish
        if ser.is_open:
            logging.info("Serial connection established.")
        else:
            logging.error("Serial connection failed to open.")
        return ser
    except serial.SerialException as e:
        logging.error(f"Error opening serial port: {e}")
        return None

def move_servo(servo_num, angle):
    if ser and ser.is_open:
        with ser_lock:
            command = f"{servo_num} {angle}\n"
            logging.debug(f"Sending command: {command.strip()}")
            try:
                ser.write(command.encode())
                ser.flush()
            except Exception as e:
                logging.error(f"Error sending command: {e}")
    else:
        logging.error("Serial port not open or initialized.")

@app.route('/')
def index():
    return render_template('index.html', angles=current_angles)

@app.route('/move', methods=['POST'])
def move():
    global current_angles
    try:
        data = request.json
        servo_num = data.get('servo_num')
        angle = data.get('angle')
        if servo_num is None or angle is None:
            return jsonify({"status": "error", "message": "Invalid data"}), 400
        if servo_num < 0 or servo_num >= len(current_angles) or angle < 0 or angle > 180:
            return jsonify({"status": "error", "message": "Invalid input"}), 400
        move_servo(servo_num, angle)
        current_angles[servo_num] = angle
        return jsonify({"status": "success", "angles": current_angles})
    except Exception as e:
        logging.error(f"Error in /move route: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/gripper', methods=['POST'])
def gripper():
    global current_angles
    try:
        data = request.json
        action = data.get('action')
        angle = 180 if action == 'open' else 0
        move_servo(5, angle)
        current_angles[5] = angle
        return jsonify({"status": "success", "angles": current_angles})
    except Exception as e:
        logging.error(f"Error in /gripper route: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/sit', methods=['POST'])
def sit():
    global current_angles
    try:
        sit_positions = [170, 90, 180, 80, 30, 0]
        for i, angle in enumerate(sit_positions):
            move_servo(i, angle)
            current_angles[i] = angle
        return jsonify({"status": "success", "angles": current_angles})
    except Exception as e:
        logging.error(f"Error in /sit route: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/stand', methods=['POST'])
def stand():
    global current_angles
    try:
        stand_positions = [90, 90, 90, 90, 30, 90]
        for i, angle in enumerate(stand_positions):
            move_servo(i, angle)
            current_angles[i] = angle
        return jsonify({"status": "success", "angles": current_angles})
    except Exception as e:
        logging.error(f"Error in /stand route: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/animation', methods=['POST'])
def animation():
    socketio.emit('start_animation')
    return jsonify({"status": "success"})

@app.route('/process_image', methods=['POST'])
def process_image():
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({"status": "error", "message": "No image file provided"}), 400

    try:
        image = Image.open(image_file.stream)
        image_np = np.array(image)

        detected_objects = detect_objects(image_np)

        if detected_objects:
            trigger_robotic_arm_actions(detected_objects)

        return jsonify({"status": "success", "detected_objects": detected_objects})
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

def detect_objects(image_np):
    # Implement your object detection logic here
    return []

def trigger_robotic_arm_actions(detected_objects):
    # Implement the logic to control the robotic arm based on detected objects
    pass

@socketio.on('start_animation')
def handle_animation():
    global current_angles
    logging.info("Animation started")
    steps = [
        [90, 90, 90, 90, 30, 90],
        [110, 70, 40, 90, 30, 180],
        [70, 120, 50, 60, 70, 0],
        [50, 40, 120, 120, 140, 180],
        [140, 160, 30, 170, 170, 0],
        [90, 90, 90, 90, 30, 180],
    ]

    for angles in steps:
        if not ser or not ser.is_open:
            logging.error("Serial port not available during animation.")
            break
        for i, angle in enumerate(angles):
            move_servo(i, angle)
        current_angles = angles
        socketio.emit('update_angles', {'angles': current_angles})
        socketio.sleep(1)  # Wait for the servo to reach the new position

if __name__ == "__main__":
    initialize_serial()
    if ser and ser.is_open:
        logging.info("Serial port initialized successfully. Starting Flask app...")
        try:
            socketio.run(app, host='0.0.0.0', port=5000, debug=False)
        finally:
            if ser and ser.is_open:
                ser.close()
                logging.info("Serial port closed.")
    else:
        logging.error("Failed to initialize serial port. Exiting.")
