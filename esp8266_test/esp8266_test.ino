#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "TP-Link_BC37";
const char* password = "Voltmeter654";

ESP8266WebServer server(80);
const int ledPin = LED_BUILTIN; // Built-in LED on NodeMCU (D0 / GPIO 16)
unsigned long lastCommandTime = 0;
const unsigned long commandTimeout = 30000; // 30 seconds

void setup() {
  Serial.begin(115200);
  
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH); // Ensure LED is off initially (active LOW)
  
  WiFi.begin(ssid, password);
  Serial.println();
  Serial.println("Connecting to Wi-Fi...");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("Connected to Wi-Fi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/sendCommand", HTTP_GET, handleSendCommand);
  
  server.begin();
  lastCommandTime = millis(); // Initialize last command time
}

void loop() {
  server.handleClient();
  
  // Check if 30 seconds have passed since the last command
  if (millis() - lastCommandTime >= commandTimeout) {
    blinkLED();
  }
}

void blinkLED() {
  static unsigned long blinkStartTime = millis();
  static bool ledState = HIGH; // Start with LED off

  // Blink LED for 30 seconds
  if (millis() - blinkStartTime < 30000) {
    ledState = !ledState; // Toggle LED state
    digitalWrite(ledPin, ledState);
    delay(500); // Blink interval
  } else {
    digitalWrite(ledPin, HIGH); // Ensure LED is off after blinking
  }
}

void handleRoot() {
  String html = "<html><head>";
  html += "<style>";
  html += "body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }";
  html += "h1 { color: #333; }";
  html += "form { background-color: #fff; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }";
  html += "input[type=text] { width: calc(100% - 22px); padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }";
  html += "input[type=submit] { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }";
  html += "input[type=submit]:hover { background-color: #45a049; }";
  html += "</style>";
  html += "</head><body>";
  html += "<h1>Control Arduino</h1>";
  html += "<form action=\"/sendCommand\" method=\"get\">";
  html += "Servo Number (0-5): <input type=\"text\" name=\"servoNum\"><br>";
  html += "Angle (0-180): <input type=\"text\" name=\"angle\"><br>";
  html += "<input type=\"submit\" value=\"Send Command\">";
  html += "</form>";
  html += "</body></html>";

  server.send(200, "text/html", html);
}

void handleSendCommand() {
  String servoNum = server.arg("servoNum");
  String angle = server.arg("angle");

  if (servoNum.length() > 0 && angle.length() > 0) {
    int servo = servoNum.toInt();
    int ang = angle.toInt();

    if (servo >= 0 && servo <= 5 && ang >= 0 && ang <= 180) {
      String command = servoNum + " " + angle;
      Serial.println(command); // Send command to Arduino via Serial
      digitalWrite(ledPin, LOW); // Turn LED on when command is received
      lastCommandTime = millis(); // Update last command time
      server.send(200, "text/html", "Command sent: " + command + "<br><a href=\"/\">Go Back</a>");
    } else {
      server.send(400, "text/html", "Error: Invalid servo number or angle.<br><a href=\"/\">Go Back</a>");
    }
  } else {
    server.send(400, "text/html", "Error: Missing parameters.<br><a href=\"/\">Go Back</a>");
  }
}