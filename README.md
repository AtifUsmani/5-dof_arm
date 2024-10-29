# 6DOF Robotic Arm Control

This project allows you to control a 6DOF robotic arm using an Arduino that receives commands from an ESP8266 microcontroller. The ESP8266 hosts a web interface for sending commands to the Arduino, making it easy to control the servos remotely.

## Table of Contents

- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Code Overview](#code-overview)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- Control of up to 6 servos for a 6DOF robotic arm.
- Web-based interface hosted on the ESP8266 for sending commands to the Arduino.
- LED indication for command activity.
- Real-time feedback in the web interface.

## Hardware Requirements

- **Arduino** (e.g., Arduino Uno or compatible)
- **ESP8266** (e.g., NodeMCU or Wemos D1 Mini)
- **6 Servos** (compatible with PWM control)
- **Breadboard** and jumper wires
- **Power supply** for servos (if required)
- **USB cable** for programming the Arduino and ESP8266
- Optional: **Resistors** for LED if needed

## Software Requirements

- Arduino IDE
- [ESP8266 Board Package](https://github.com/esp8266/Arduino) installed in the Arduino IDE
- Required libraries:
  - `ESP8266WiFi`
  - `ESP8266WebServer`

## Setup Instructions

1. **Install the Arduino IDE**:
   - Download and install the Arduino IDE from the [official website](https://www.arduino.cc/en/software).

2. **Install ESP8266 Board Package**:
   - Open the Arduino IDE, go to `File` > `Preferences`.
   - In the "Additional Board Manager URLs" field, add: `http://arduino.esp8266.com/stable/package_esp8266com_index.json`.
   - Go to `Tools` > `Board` > `Board Manager`, search for "ESP8266" and install the package.

3. **Connect the Arduino and ESP8266**:
   - Connect your Arduino to your computer via USB.
   - Connect the ESP8266 to the Arduino:
     - Connect the `TX` pin of the ESP8266 to the `RX` pin of the Arduino.
     - Connect the `RX` pin of the ESP8266 to the `TX` pin of the Arduino.
     - Ensure both devices share a common ground.

4. **Clone or Download the Repository**:
   - Clone this repository or download the code files for both the Arduino and ESP8266.

5. **Configure Wi-Fi Credentials**:
   - Open the ESP8266 code file and replace the `ssid` and `password` variables with your Wi-Fi network credentials.

6. **Upload the Code**:
   - Upload the Arduino code to the Arduino board.
   - Then, upload the ESP8266 code to the ESP8266 board.

## Usage

1. **Connect to the Wi-Fi**:
   - After uploading, open the Serial Monitor (set baud rate to 115200) for the ESP8266.
   - Wait for the ESP8266 to connect to Wi-Fi. Note the IP address printed in the Serial Monitor.

2. **Access the Web Interface**:
   - Open a web browser and enter the IP address of your ESP8266.
   - You should see a web page with fields to enter the servo number (0-5) and the desired angle (0-180).

3. **Send Commands**:
   - Fill in the servo number and angle, then click "Send Command" to control the servo.

## Code Overview

### Main Components

- **ESP8266**:
  - Connects to Wi-Fi and hosts a web server.
  - Receives commands from the web interface and sends them to the Arduino via Serial.

- **Arduino**:
  - Listens for commands from the ESP8266.
  - Controls the servos based on the received commands.

### Key Functions

- **ESP8266 Code**:
  - `setup()`: Initializes Wi-Fi, sets up the server, and handles LED states.
  - `loop()`: Handles incoming client requests and manages LED blinking when no commands are received.
  - `handleRoot()`: Serves the main control HTML page.
  - `handleSendCommand()`: Processes the command from the web form and sends it to the Arduino.

- **Arduino Code**:
  - `setup()`: Initializes the serial communication and sets up the servos.
  - `loop()`: Listens for incoming commands from the ESP8266 and controls the servos accordingly.

## Troubleshooting

- **Wi-Fi Connection Issues**: Ensure the SSID and password are correct. Check if your router is functioning properly.
- **Command Not Working**: Make sure the servo number and angle are within the specified ranges (0-5 for servo number, 0-180 for angle).
- **LED Behavior**: If the LED does not blink, check the wiring and ensure the `ledPin` is correctly configured.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for any bugs or enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
