#include <Stepper.h>

const int numberOfSteps = 100;
const int motor_speed = 60;

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(numberOfSteps, 8, 9, 10, 11);

String inString = "";    // string to hold input
int value = 0;
const int LED = 13;

void setup()
{
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  myStepper.setSpeed(motor_speed);
}

void loop() {
  // Read serial input
  while (Serial.available() > 0) {
    int inChar = Serial.read();
    if (isDigit(inChar)) {
      inString += (char)inChar;
    }
    // if newline, get the string
    if (inChar == '\n') {
      Serial.print("Value:");
      value = inString.toInt();
      Serial.println(value);

      // CAMBIAR ESTE CICLO POR LA LOGICA DEL MOTOR
      // myStepper.step(numberOfSteps);
      for (int i = 0; i<value; i++)
      {
        digitalWrite(LED, HIGH);
        delay(250);
        digitalWrite(LED, LOW);
        delay(250);
      }

      // clear the string for new input:
      inString = "";
    }
  }
}
