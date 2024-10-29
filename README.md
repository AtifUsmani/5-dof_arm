# Arduino Servo Control with Adafruit PWM Servo Driver

This project demonstrates how to control multiple servos using the Adafruit PWM Servo Driver with an Arduino. It allows smooth movements of servos based on commands received via the serial interface.

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

- Control up to 6 servos.
- Smooth movement to target angles.
- Serial command interface for dynamic control.
- Customizable pulse width ranges for each servo.

## Hardware Requirements

- Arduino board (e.g., Arduino Uno, Mega, etc.)
- Adafruit PWM Servo Driver
- Servo motors (6 or fewer)
- Jumper wires
- External power supply (recommended for multiple servos)

## Software Requirements

- Arduino IDE
- [Adafruit PWM Servo Driver Library](https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/arduino-servo-control.git
   cd arduino-servo-control
   ```

2. **Open the Arduino IDE.**
3. **Install the Adafruit PWM Servo Driver library**:
   - Go to **Sketch** > **Include Library** > **Manage Libraries**.
   - Search for "Adafruit PWM Servo Driver" and install it.

4. **Open the `servo_control.ino` file** in the Arduino IDE.
5. **Connect your Arduino board** to your computer.
6. **Upload the code** to the Arduino board.

## Usage

1. Open the Serial Monitor in the Arduino IDE (set the baud rate to 9600).
2. Send commands in the format:
   ```
   <servoNum> <angle>
   ```
   - `servoNum`: Integer from 0 to 5 (representing each servo).
   - `angle`: Integer from 0 to 180 (the target angle for the servo).

### Example Commands

- To move servo 0 to 90 degrees:
  ```
  0 90
  ```
- To move servo 3 to 45 degrees:
  ```
  3 45
  ```

### Error Handling
- If the input is invalid (e.g., an invalid servo number or angle), an error message will be displayed in the Serial Monitor.

## Code Explanation

- **Libraries**: Uses `Wire.h` for I2C communication and `Adafruit_PWMServoDriver.h` for controlling PWM outputs.
- **Initialization**: Sets up the PWM driver and initializes servos in the `setup()` function.
- **Main Loop**: Listens for serial input and processes commands to control the servos smoothly using the `smoothMove()` function.
- **Pulse Width Mapping**: Converts angle values to pulse widths based on predefined ranges for each servo.

### Key Functions

- `angleToPulse(int angle, int servoNum)`: Converts an angle (0-180) to the corresponding pulse width for the specified servo.
- `smoothMove(int servoNum, int targetAngle)`: Gradually moves a servo to the target angle for smooth transitions.
- `initializeServos()`: Sets the initial positions of all servos.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.
