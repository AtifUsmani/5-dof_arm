#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVO_FREQ 52 // Analog servos run at ~50 Hz updates
#define STEP_DELAY 20 // Delay between steps in milliseconds

// Array to hold current pulse widths for each servo
int currentPulses[6] = {0, 0, 0, 0, 0, 0}; // Assuming 6 servos

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);
  delay(10);
  
  initializeServos();
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    int separatorIndex = command.indexOf(' ');
    if (separatorIndex != -1) {
      int servoNum = command.substring(0, separatorIndex).toInt();
      int angle = command.substring(separatorIndex + 1).toInt();

      if (servoNum >= 0 && servoNum <= 5) {
        if (angle >= 0 && angle <= 180) {
          smoothMove(servoNum, angle);
        } else {
          Serial.println("Error: Angle must be between 0 and 180.");
        }
      } else {
        Serial.println("Error: Invalid servo number.");
      }
    }
  }
}

int angleToPulse(int angle, int servoNum) {
  int minPulse, maxPulse;
  switch (servoNum) {
    case 0: minPulse = 150; maxPulse = 450; break;
    case 1: minPulse = 100; maxPulse = 500; break;
    case 2: minPulse = 100; maxPulse = 480; break;
    case 3: minPulse = 100; maxPulse = 500; break;
    case 4: minPulse = 150; maxPulse = 400; break;
    case 5: minPulse = 170; maxPulse = 320; break;
    default: minPulse = 150; maxPulse = 500; break;
  }
  return map(angle, 0, 180, minPulse, maxPulse);
}

void smoothMove(int servoNum, int targetAngle) {
  // Get the current pulse width for the specified servo
  int targetPulse = angleToPulse(targetAngle, servoNum);
  
  // Gradually move to the target pulse width
  // Check the current pulse width stored in the array
  int currentPulse = currentPulses[servoNum];

  // Determine the direction of movement
  int step = (currentPulse < targetPulse) ? 1 : -1;

  // Gradually move to the target pulse width
  for (int pulse = currentPulse; pulse != targetPulse; pulse += step) {
    pwm.setPWM(servoNum, 0, pulse);
    delay(STEP_DELAY); // Wait for a short period to smooth the movement
  }
  
  // Ensure the final position is set to the target pulse width
  pwm.setPWM(servoNum, 0, targetPulse);
  
  // Update the current pulse in the array
  currentPulses[servoNum] = targetPulse;
}

void initializeServos() {
  setServo(0, 170); // Shoulder
  setServo(1, 90);  // Base
  setServo(2, 180); // Elbow
  setServo(3, 80);  // Wrist Y
  setServo(4, 30);  // Wrist Rot
  setServo(5, 0); // Gripper
}

// Helper function to set servo angle and update current pulse
void setServo(int servoNum, int angle) {
  int pulse = angleToPulse(angle, servoNum);
  pwm.setPWM(servoNum, 0, pulse);
  currentPulses[servoNum] = pulse; // Update the current pulse
}
