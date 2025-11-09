// Ch8 AWS: Arduino + PM2.5 Sensor


int dustPin=0;   // A0
float dustVal=0;
int ledPower=7;   // D7
int delayTime=280;
int delayTime2=40;
float offTime=9680;
//=========================
void setup() {
  pinMode(ledPower,OUTPUT);
  pinMode(dustPin, INPUT);
  Serial.begin(9600);

}
void loop()
{
  digitalWrite(ledPower,LOW); // power on the LED
  delayMicroseconds(delayTime);
  dustVal=analogRead(dustPin); // read the dust value via pin 5 on the sensor
  delayMicroseconds(delayTime2);
  digitalWrite(ledPower,HIGH); // turn the LED off
  delayMicroseconds(offTime);
  delay(3000);
  float AirQ=float((dustVal/1024)-0.0356)*120000*0.035;
  String AirQT=" ";
  if (AirQ < 300)   { AirQT=" : Good      ";}
  if (AirQ >= 300 && AirQ < 1050)    { AirQT=" :Moderate";}
  if  ( AirQ >= 1050 && AirQ < 3000){ AirQT=" :Unhealthy";}
  if  (  AirQ > 3000){ AirQT=" :Hazardous";}
  Serial.println(AirQ+ AirQT);

  delay(4000);

}


