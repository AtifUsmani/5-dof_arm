# 6 DOF Robotic Arm Control with Adafruit PWM Servo Driver

This project demonstrates how to control a 6 DOF robotic arm using the Adafruit PWM Servo Driver with an Arduino. It allows for smooth movements of each joint based on commands received via the serial interface.

## Table of Contents

- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [License](#license)
- [Contributing](#contributing)

## Features

- Control up to 6 servos for a complete robotic arm.
- Smooth and precise movements for each joint.
- Serial command interface for dynamic control.
- Customizable pulse width ranges for each servo to accommodate different servo specifications.

## Hardware Requirements

- Arduino board (e.g., Arduino Uno, Mega, etc.)
- Adafruit PWM Servo Driver
- 6 Servo motors for the robotic arm
- Jumper wires
- External power supply (recommended for multiple servos)

## Software Requirements

- Arduino IDE
- [Adafruit PWM Servo Driver Library](https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/6dof-robotic-arm.git
   cd 6dof-robotic-arm
   ```

2. **Open the Arduino IDE.**
3. **Install the Adafruit PWM Servo Driver library**:
   - Go to **Sketch** > **Include Library** > **Manage Libraries**.
   - Search for "Adafruit PWM Servo Driver" and install it.

4. **Open the `robotic_arm_control.ino` file** in the Arduino IDE.
5. **Connect your Arduino board** to your computer.
6. **Upload the code** to the Arduino board.

## Usage

1. Open the Serial Monitor in the Arduino IDE (set the baud rate to 9600).
2. Send commands in the format:
   ```
   <servoNum> <angle>
   ```
   - `servoNum`: Integer from 0 to 5 (representing each joint of the robotic arm).
   - `angle`: Integer from 0 to 180 (the target angle for the joint).

### Example Commands

- To move joint 0 to 90 degrees:
  ```
  0 90
  ```
- To move joint 3 to 45 degrees:
  ```
  3 45
  ```

### Error Handling
- If the input is invalid (e.g., an invalid joint number or angle), an error message will be displayed in the Serial Monitor.

## Code Explanation

- **Libraries**: Uses `Wire.h` for I2C communication and `Adafruit_PWMServoDriver.h` for controlling PWM outputs.
- **Initialization**: Sets up the PWM driver and initializes the servos in the `setup()` function.
- **Main Loop**: Listens for serial input and processes commands to control the robotic arm joints smoothly using the `smoothMove()` function.
- **Pulse Width Mapping**: Converts angle values to pulse widths based on predefined ranges for each joint.

### Key Functions

- `angleToPulse(int angle, int servoNum)`: Converts an angle (0-180) to the corresponding pulse width for the specified servo.
- `smoothMove(int servoNum, int targetAngle)`: Gradually moves a joint to the target angle for smooth transitions.
- `initializeServos()`: Sets the initial positions of all joints in the robotic arm.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.
