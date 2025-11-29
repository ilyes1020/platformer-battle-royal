const int JoyStick_pin = 11; //plug Joystick 'Button' into pin 8
const int X_pin = A0;       //plug joystick X direction into pin A0
const int Y_pin = A1;       //plug joystick Y direction into pin A1
const int button_pin = 12;
int xc;
int yc;
int JSButton;


void setup() {
//bouton vert
    // Défini la broche #12 comme entrée et active la résistance pull-up interne
  pinMode(button_pin, INPUT_PULLUP);
  
  pinMode(JoyStick_pin, INPUT);

  Serial.begin(9600);
}

void loop() {
  
  int x = analogRead(X_pin) - 517;  //read x direction value and -517 to bring back to around 0
  int y = analogRead(Y_pin) - 480;  //read y direction value and -512 to bring back to around 0
  //bouton vert
  // Lit la valeur de l'entrée. Elle peut être 1 ou 0
  int buttonValue = digitalRead(button_pin);

  int zValue = digitalRead(JoyStick_pin);
  

  if (x <-10) {         //joystick has off set of +/-8 so this negates that
    xc = 0;             //turn analogue value into integer. 0, 1 or 2 depending on state
  } else if (x >10) {   
    xc = 2;
  } else {
    xc = 1;
  }

  if (y <-10) {
    yc = 0;
  } else if (y >60) {
    yc = 2;
  } else {
    yc = 1;
  }


  Serial.print("S");
  Serial.print(xc);
  Serial.print(",");
  Serial.print(yc);
  Serial.print(",");
  Serial.print(zValue);
  Serial.print(",");
  Serial.println(buttonValue);

  delay(40);
}
