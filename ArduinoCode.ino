#include "Arduino.h"
#include <dht.h>
#include <Servo.h>
#include <SPI.h>
#include <SD.h>
const int chipSelect = 10; 
File dataFile;
#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04
int I1,I2;
#define dht_apin A4 // Analog Pin sensor is connected to
 
dht DHT;

Servo updownServo, RLServo;

int check=0;
int incomingByte = 0;
long duration; 
int distance; 


void randomNavigate();
void goStraight();
void RRstraight();
void RLstraight();
void RR();
void RL();
void Stop2scan();
void rotateAbit();
void back();

#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04



void setup() {
  Serial.begin(9600);
   while (!Serial) {
 ; // wait for serial port to connect. Needed for Leonardo onl\y
 }
  pinMode(SS, OUTPUT);
  if (!SD.begin(chipSelect)) {
 //Serial.println("Card failed, or not present");
 // don't do anything more:
 while (1) ;
 }
 dataFile = SD.open("datalog.txt", FILE_WRITE);

 
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT

  updownServo.attach(5);
  RLServo.attach(6);

  updownServo.write(100);
  RLServo.write(120);
  
  pinMode(12,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(11,OUTPUT);

  
  digitalWrite(12,LOW);
  digitalWrite(9,LOW);
  digitalWrite(7,LOW);
  digitalWrite(11,LOW);

  while(Serial. read() >= 0) ; 
 
    
}

void loop() {
  
  
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    check=1;
  //}

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor
  //Serial.println(distance);

  switch((char)incomingByte){
    
    case '0' : 
    if(distance>=50){
    randomNavigate();}
    else{
      back();
      RR();    // new function
    }
    break;
    
    case '1' :
    if(check==1 ){
    Stop2scan();
    check=0;}
    break;
    
//    case '2' :
//    if(distance>60 && check==1){
//    goStraight();
//    Stop2scan();
//    check=0;
//    }
//    break;

    case '2' :
    if(check==1 ){
    Stop2scan();
    check=0;}
    break;
      
    case '3' :
    if( check==1){
    RL();
    //goStraight();
    Stop2scan();
    check=0;
    }
    break;
    
    case '4' :
    if( check==1){
    RL();
    Stop2scan();
    check=0;
    }
    break;
    
    case '5' : 
    if( check==1){
    RR();
   // goStraight();
    Stop2scan();
    check=0;
    }
    break;
    
    case '6' :
    if( check==1){
    RR();
    Stop2scan();
    check=0;
    }
    break;

  }
  }
}
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////

void randomNavigate(){
 
    digitalWrite(12,LOW);
    digitalWrite(9,HIGH);
    digitalWrite(7,LOW);
    digitalWrite(11,HIGH);
  
}
//void goStraight(){
//    digitalWrite(12,LOW);
//    digitalWrite(9,HIGH);
//    digitalWrite(7,LOW);
//    digitalWrite(11,HIGH);
//    delay(2000);
//}


void RR(){
    digitalWrite(12,LOW);
    digitalWrite(9,LOW);
    digitalWrite(7,LOW);
    digitalWrite(11,LOW);
    delay(100);
    digitalWrite(12,LOW);
    digitalWrite(9,LOW);
    digitalWrite(7,HIGH);
    digitalWrite(11,HIGH);
    delay(1000);
    digitalWrite(12,LOW);
    digitalWrite(9,LOW);
    digitalWrite(7,LOW);
    digitalWrite(11,LOW);
    
  
    
}

void RL(){
    digitalWrite(12,LOW);
    digitalWrite(9,LOW);
    digitalWrite(7,LOW);
    digitalWrite(11,LOW);
    delay(100);
    digitalWrite(12,HIGH);
    digitalWrite(9,HIGH);
    digitalWrite(7,LOW);
    digitalWrite(11,LOW);
    delay(1000);
    digitalWrite(12,LOW);
    digitalWrite(9,LOW);
    digitalWrite(7,LOW);
    digitalWrite(11,LOW);
    

}

void Stop2scan(){
    //Serial.flush();
    
    digitalWrite(12,LOW);
    digitalWrite(9,LOW);
    digitalWrite(7,LOW);
    digitalWrite(11,LOW);
    delay(1000);
    updownServo.write(60);
    delay(1000);
    updownServo.write(100);
    delay(1000);
    updownServo.write(140);
    delay(1000);
    updownServo.write(100);
    delay(1000);
    
    
    
    I1=analogRead(A0);
    I2=analogRead(A1);

    DHT.read11(dht_apin);
    String s="Current humidity = ";
    dataFile.print(s);
    delay(500);
    dataFile.print(DHT.humidity);
    delay(500);
    dataFile.print("%  ");
    delay(500);
    dataFile.print("temperature = ");
    delay(500);
    dataFile.print(DHT.temperature);
    delay(500); 
    dataFile.println("C  ");
    delay(500);
    dataFile.print("light intensity: ");
    delay(500);
    I1=(I1+I2)/2;
    dataFile.println(I1);
    delay(500);
    dataFile.flush();
     check =0;
 
      
}
void back(){
    digitalWrite(12,LOW);
    digitalWrite(9,LOW);
    digitalWrite(7,LOW);
    digitalWrite(11,LOW);
    delay(100);
    digitalWrite(12,HIGH);
    digitalWrite(9,LOW);
    digitalWrite(7,HIGH);
    digitalWrite(11,LOW);
    delay(1000);
    digitalWrite(12,LOW);
    digitalWrite(9,LOW);
    digitalWrite(7,LOW);
    digitalWrite(11,LOW);
    
  
}
