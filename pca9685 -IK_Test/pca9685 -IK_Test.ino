#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates
  delay(10);

  // Initialize servo positions
  initializeServos();
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    int separatorIndex = command.indexOf(' ');
    if (separatorIndex != -1) {
      int servoNum = command.substring(0, separatorIndex).toInt();
      int angle = command.substring(separatorIndex + 1).toInt();
      
      // Validate servo number
      if (servoNum >= 0 && servoNum <= 5) {
        int pulseLength = angleToPulse(angle, servoNum);
        pwm.setPWM(servoNum, 0, pulseLength);
        Serial.print("Servo "); Serial.print(servoNum); Serial.print(" set to angle "); Serial.println(angle);
      }
    }
  }
}

int angleToPulse(int angle, int servoNum) {
  // Adjust pulse ranges per servo
  int minPulse, maxPulse;
  switch (servoNum) {
    case 0: // Shoulder
      minPulse = 150; maxPulse = 450;
      break;
    case 1: // Base
      minPulse = 100; maxPulse = 500;
      break;
    case 2: // Elbow
      minPulse = 100; maxPulse = 480;
      break;
    case 3: // Wrist Y
      minPulse = 100; maxPulse = 500;
      break;
    case 4: // Wrist Rot
      minPulse = 150; maxPulse = 400;
      break;
    case 5: // Gripper
      minPulse = 170; maxPulse = 320;
      break;
    default:
      minPulse = 150; maxPulse = 500; // Default range
      break;
  }
  return map(angle, 0, 180, minPulse, maxPulse);
}

void initializeServos() {
  // Set default positions for all servos
  pwm.setPWM(0, 0, angleToPulse(170, 0));
  pwm.setPWM(1, 0, angleToPulse(90, 1));
  pwm.setPWM(2, 0, angleToPulse(180, 2));
  pwm.setPWM(3, 0, angleToPulse(80, 3));
  pwm.setPWM(4, 0, angleToPulse(30, 4));
  pwm.setPWM(5, 0, angleToPulse(0, 5));
}
