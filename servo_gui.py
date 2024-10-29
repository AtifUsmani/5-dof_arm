import serial
import time
import threading
import tkinter as tk
from tkinter import ttk

def initialize_serial(port='COM10', baudrate=9600, timeout=1):
    """Initialize serial communication."""
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Wait for the serial connection to establish
        print("Serial connection established.")
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

def move_servo(ser, servo_num, angle):
    """Send command to move a specific servo to the given angle."""
    command = f"{servo_num} {angle}\n"
    ser.write(command.encode())
    ser.flush()

def smooth_move(ser, servo_num, start_angle, end_angle, steps=20, delay=0.05):
    """Move a servo smoothly from start_angle to end_angle."""
    step_size = (end_angle - start_angle) / steps
    for i in range(steps):
        angle = start_angle + step_size * i
        move_servo(ser, servo_num, int(angle))
        time.sleep(delay)
    move_servo(ser, servo_num, end_angle)

def sit(ser):
    """Move the robotic arm to a sitting position."""
    print("Moving to sitting position.")
    positions = [170, 90, 180, 80, 30, 0]
    for i, angle in enumerate(positions):
        move_servo(ser, i, angle)
    time.sleep(2)

def stand(ser):
    """Move the robotic arm to a standing position."""
    print("Moving to standing position.")
    positions = [90, 90, 90, 90, 30, 90]
    for i, angle in enumerate(positions):
        move_servo(ser, i, angle)
    time.sleep(2)

def anim1(ser):
    """Perform a predefined animation sequence."""
    print("Starting animation.")
    steps = [
        [90, 90, 90, 90, 30, 90],  # Starting position
        [110, 70, 40, 90, 30, 180],  # Move hand up
        [70, 120, 50, 60, 70, 0],  # Move hand further up
        [50, 40, 120, 120, 140, 180],  # Move hand to top
        [140, 160, 30, 170, 170, 0],  # Move hand down
        [90, 90, 90, 90, 30, 180],  # Move hand back up
    ]
    
    servo_delays = [0.5] * 6  # Delay for each servo in seconds
    global stop_animation
    stop_animation = False

    def input_listener():
        """Listen for user input to stop the animation."""
        global stop_animation
        while True:
            user_input = input("Type 'quit(q)' to stop animation: ").strip().lower()
            if user_input == 'q':
                stop_animation = True
                print("Stopping animation...")

    # Start the input listener in a separate thread
    input_thread = threading.Thread(target=input_listener)
    input_thread.daemon = True
    input_thread.start()

    for _ in range(3):  # Repeat animation 3 times
        if stop_animation:
            break
        for angles in steps:
            if stop_animation:
                break
            for servo_num, angle in enumerate(angles):
                move_servo(ser, servo_num, angle)
                time.sleep(servo_delays[servo_num])
            time.sleep(0.5)  # Additional delay between steps

    sit(ser)
    print("Moved to sitting position.")
    time.sleep(2)

class RobotArmGUI(tk.Tk):
    def __init__(self, ser):
        super().__init__()
        self.ser = ser
        self.title("Robot Arm Controller")

        # Create a Canvas and a Frame to hold the widgets
        self.canvas = tk.Canvas(self, bg='#2E2E2E')
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas_frame = ttk.Frame(self.canvas, padding=(10, 5))

        # Configure the Canvas
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        # Pack the widgets
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")

        # Update scroll region
        self.canvas_frame.bind("<Configure>", self.on_frame_configure)

        # Define joint names and corresponding numbers
        self.joint_names = ["Shoulder", "Base", "Elbow", "Wrist Y", "Wrist Rot", "Gripper"]
        self.joint_mapping = {name: i for i, name in enumerate(self.joint_names)}

        # Create UI components
        self.create_widgets()

        # Set dark theme
        self.configure(bg='#2E2E2E')
        self.option_add('*Font', 'Helvetica 12')
        self.option_add('*Foreground', 'white')
        self.option_add('*Background', '#2E2E2E')
        self.option_add('*BorderWidth', 2)

    def create_widgets(self):
        """Create and place all UI widgets."""
        # Joint Selection
        self.joint_label = ttk.Label(self.canvas_frame, text="Select Joint:")
        self.joint_label.pack(padx=10, pady=10)

        self.joint_var = tk.StringVar(value=self.joint_names[0])
        self.joint_menu = ttk.OptionMenu(self.canvas_frame, self.joint_var, *self.joint_names)
        self.joint_menu.pack(padx=10, pady=10)

        # Sliders for each servo
        self.sliders = {}
        self.sliders_frame = ttk.Frame(self.canvas_frame)
        self.sliders_frame.pack(padx=10, pady=10, fill=tk.X)

        for joint in self.joint_names:
            self.create_slider(joint)

        # Control Buttons
        self.sit_button = ttk.Button(self.canvas_frame, text="Sit", command=self.sit)
        self.sit_button.pack(padx=10, pady=10)

        self.stand_button = ttk.Button(self.canvas_frame, text="Stand", command=self.stand)
        self.stand_button.pack(padx=10, pady=10)

        self.anim_button = ttk.Button(self.canvas_frame, text="Start Animation", command=self.start_animation)
        self.anim_button.pack(padx=10, pady=10)

        # Gripper Control Buttons
        self.open_gripper_button = ttk.Button(self.canvas_frame, text="Open Gripper", command=self.open_gripper)
        self.open_gripper_button.pack(padx=10, pady=10)

        self.close_gripper_button = ttk.Button(self.canvas_frame, text="Close Gripper", command=self.close_gripper)
        self.close_gripper_button.pack(padx=10, pady=10)

        # Exit Button
        self.exit_button = ttk.Button(self.canvas_frame, text="Exit", command=self.quit)
        self.exit_button.pack(padx=10, pady=10)

    def create_slider(self, joint):
        """Create a slider for a specific joint."""
        label = ttk.Label(self.sliders_frame, text=joint)
        label.pack(padx=10, pady=5, anchor='w')

        slider = ttk.Scale(self.sliders_frame, from_=0, to=180, orient='horizontal', command=lambda value, j=joint: self.update_servo(j, value))
        slider.set(90)  # Default position
        slider.pack(padx=10, pady=5, fill=tk.X)
        self.sliders[joint] = slider

    def update_servo(self, joint, value):
        """Update the servo position based on slider value."""
        servo_num = self.joint_mapping[joint]
        try:
            angle = int(float(value))
            move_servo(self.ser, servo_num, angle)
        except ValueError:
            print("Invalid angle value.")

    def sit(self):
        """Start the sit command in a separate thread."""
        threading.Thread(target=lambda: sit(self.ser), daemon=True).start()

    def stand(self):
        """Start the stand command in a separate thread."""
        threading.Thread(target=lambda: stand(self.ser), daemon=True).start()

    def start_animation(self):
        """Start the animation in a separate thread."""
        threading.Thread(target=lambda: anim1(self.ser), daemon=True).start()

    def open_gripper(self):
        """Open the gripper."""
        threading.Thread(target=lambda: move_servo(self.ser, 5, 180), daemon=True).start()

    def close_gripper(self):
        """Close the gripper."""
        threading.Thread(target=lambda: move_servo(self.ser, 5, 0), daemon=True).start()

    def on_frame_configure(self, event):
        """Update the scroll region of the canvas."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

def follow_path(ser, path, step_size=10):
    """
    Move the robotic arm through a series of waypoints.

    :param ser: Serial object for communication
    :param path: List of waypoints (each waypoint is a list of angles)
    :param step_size: Number of steps to interpolate between waypoints
    """
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        for step in range(step_size):
            interpolated_angles = [
                int(start[j] + (end[j] - start[j]) * step / step_size)
                for j in range(len(start))
            ]
            for servo_num, angle in enumerate(interpolated_angles):
                move_servo(ser, servo_num, angle)
            time.sleep(0.05)  # Delay between steps


if __name__ == "__main__":
    ser = initialize_serial()
    if ser:
        app = RobotArmGUI(ser)
        app.mainloop()
        ser.close()
