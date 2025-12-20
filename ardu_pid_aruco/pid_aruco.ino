#define SPEED_1      5 
#define DIR_1        4
 
#define SPEED_2      6
#define DIR_2        7

const float Kp = 1.05;                 // Proportional gain
const float Ki = 0.026;                // Integral gain
const float Kd = 0.095;                // Derivative gain

float setpoint = 0.0; 
float error = 0.0;
float lastError = 0.0;
float integral = 0.0;

void setup() {
  Serial.begin(9600);   
  Serial.setTimeout(10);          
  for (int i = 4; i < 8; i++) {     
    pinMode(i, OUTPUT);
  }
  delay(2000);
}

void loop() {

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int s1Index = data.indexOf("S1:") + 3; 
    int delIndex = data.indexOf(";", s1Index); 
    String s1String = data.substring(s1Index, delIndex);
    float currAngle = s1String.toFloat();

    String s2String = data.substring(delIndex + 4, data.length());
    float setpoint = s2String.toFloat();

    error = setpoint - currAngle;
    integral += error;
    float derivative = error - lastError;

    // Calculate PID output
    float output = Kp * error + Ki * integral + Kd * derivative;

    // Map the PID output to PWM range
    int pwmValue = map(output, 255, -255, 0, 255);
    pwmValue = constrain(pwmValue, 55, 60);

    if (output > 0) {
      digitalWrite(DIR_1, HIGH);
      digitalWrite(DIR_2, LOW);
    }
    else {
      digitalWrite(DIR_1, LOW);
      digitalWrite(DIR_2, HIGH);
    }

    analogWrite(SPEED_1, pwmValue);
    analogWrite(SPEED_2, pwmValue);
    
    Serial.println("Setpoint: " + String(setpoint) + "\tCurr Angle: " + String(currAngle) + "\tPWM Value: " + String(pwmValue) + "\tPID Value: " + String(output));

    lastError = error;
    //delay(100); 
  }
  else {
    analogWrite(SPEED_1, 0);
    analogWrite(SPEED_2, 0);
  }
}