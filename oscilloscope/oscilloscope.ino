//UNO code

int val;



void setup(){

  Serial.begin(9600);

  pinMode(7,INPUT);

  }



void loop(){

  if (Serial.available() == 1){//is there a "?" in the receiver buffer?

    Serial.read();//clean receiving buffer

    val = digitalRead(7);//since it is digital, val can only be 1 or 0. by all means, val only occupies one byte

    Serial.print(val);//since val only occupies one byte, print only sends one character "1" or "0"

	}

}
