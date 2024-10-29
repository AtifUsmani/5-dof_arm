import serial
import time
import threading

def initialize_serial(port='COM9', baudrate=9600, timeout=1):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Wait for the serial connection to establish
        print("Serial connection established.")
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

def move_servo(ser, servo_num, angle):
    command = f"{servo_num} {angle}\n"
    print(f"Sending command: {command.strip()}")  # Debugging output
    ser.write(command.encode())
    ser.flush()  # Ensure command is sent immediately

def get_angle_input(joint_name):
    while True:
        user_input = input(f"Enter angle for {joint_name} (0-180) or 'exit' to quit: ")
        if user_input.lower() == 'exit':
            return 'exit'
        try:
            angle = int(user_input)
            if 0 <= angle <= 180:
                return angle
            else:
                print("Please enter a valid angle between 0 and 180.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def sit(ser):
    print("Moving to sitting position.")
    move_servo(ser, 0, 170)
    move_servo(ser, 1, 90)
    move_servo(ser, 2, 180)
    move_servo(ser, 3, 80)
    move_servo(ser, 4, 30)
    move_servo(ser, 5, 0)
    time.sleep(2)  # Allow time for the movement

def stand(ser):
    print("Moving to standing position.")
    move_servo(ser, 0, 90)
    move_servo(ser, 1, 90)
    move_servo(ser, 2, 90)
    move_servo(ser, 3, 90)
    move_servo(ser, 4, 30)
    move_servo(ser, 5, 90)
    time.sleep(2)  # Allow time for the movement

def anim1(ser):
    print("Starting animation.")
    steps = [
        [90, 90, 90, 90, 30, 90],  # Starting position
        [110, 70, 40, 90, 30, 180],  # Move hand up
        [70, 120, 50, 60, 70, 0],  # Move hand further up
        [50, 40, 120, 120, 140, 180],  # Move hand to top
        [140, 160, 30, 170, 170, 0],  # Move hand down
        [90, 90, 90, 90, 30, 180],  # Move hand back up
    ]
    
    # Define individual delays for each servo
    servo_delays = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]  # Delay for each servo in seconds
    global stop_animation
    stop_animation = False

    def input_listener():
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
                time.sleep(servo_delays[servo_num])  # Delay for each servo
            time.sleep(0.5)  # Additional delay between steps
    
    # Move to the sitting position after animation
    sit(ser)
    print("Moved to sitting position.")
    time.sleep(2)  # Allow time for the reset

def control_robotic_arm(ser):
    joints = ["Shoulder", "Base", "Elbow", "Wrist Y", "Wrist Rot", "Gripper"]
    current_angles = [90] * len(joints)  # Default angles

    while True:
        print("\nSelect an option:")
        print("1: Control individual servos")
        print("2: Move to sitting position")
        print("3: Move to standing position")
        print("4: anim1")
        print("5: Exit")

        option = input("Enter your choice: ").strip()

        if option == '1':
            print("\nSelect the servo to control (0-5):")
            for i, joint in enumerate(joints):
                print(f"{i}: {joint}")
            
            try:
                servo_num = int(input("Enter servo number: "))
                if servo_num < 0 or servo_num >= len(joints):
                    print("Invalid servo number. Please enter a number between 0 and 5.")
                    continue
                
                new_angle = get_angle_input(joints[servo_num])
                if new_angle == 'exit':
                    print("Exiting...")
                    ser.close()
                    return
                
                current_angles[servo_num] = new_angle

                while True:
                    move_servo(ser, servo_num, current_angles[servo_num])
                    time.sleep(0.1)  # Adjust the delay as needed
                    user_input = input("Type 'done(d)' when finished or 'change(c)' to change angle: ").strip().lower()
                    if user_input == 'd':
                        break
                    elif user_input == 'c':
                        new_angle = get_angle_input(joints[servo_num])
                        if new_angle == 'exit':
                            ser.close()
                            return
                        else:
                            current_angles[servo_num] = new_angle
                    else:
                        print("Invalid input. Type 'done' or 'change'.")
            
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        elif option == '2':
            sit(ser)
        
        elif option == '3':
            stand(ser)
        
        elif option == '4':
            anim1(ser)

        elif option == '5':
            print("Exiting...")
            ser.close()
            break
        
        else:
            print("Invalid option. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    ser = initialize_serial()
    if ser:
        control_robotic_arm(ser)
