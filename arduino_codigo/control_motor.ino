
String inString = "";    // string to hold input
int value = 0;
const int LED = 13;

void setup()
{
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
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
