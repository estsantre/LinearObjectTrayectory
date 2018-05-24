#include <Servo.h>

Servo servox;
Servo servoy;

const int LED = 13;

int angulox = 90;
int anguloy = 10;
int salto = 2;

void setup() 
{
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  servox.attach(9);
  servox.write(90);
  servoy.attach(10);
  servoy.write(10);
}
 
void loop()
{
  if (Serial.available()>0) 
  {
    
    int option = Serial.read();
    
    if (option == '1' && angulox < 170)
    {
      angulox = angulox + salto;
      servox.write(angulox);
      delay(15);
    }

    else if (option == '2' && angulox > 10)
    {
      angulox = angulox - salto;
      servox.write(angulox);
      delay(15);
    } 

    else if (option == '3' && anguloy < 170)
    {
      anguloy = anguloy + salto;
      servoy.write(anguloy);
      delay(25);
    }

    else if (option == '4' && anguloy > 10)
    {
      anguloy = anguloy - salto;
      servoy.write(anguloy);
      delay(25);
    } 

    else if (option == '5')
    {
      if (angulox > 90){
        for (angulox; angulox > 90; angulox -= 1) {
          servox.write(angulox);
          delay(20);
        }
      }
      else if (angulox < 90){
        for (angulox; angulox < 90; angulox += 1) {
          servox.write(angulox);
          delay(20);
        }
      }
      
      anguloy = 10;
      servoy.write(anguloy);
      delay(50);
    } 

  } 
}
