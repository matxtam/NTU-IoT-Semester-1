// myLoraServerSFtest-FieldTrailTx.ino
// 頻率設定位置: setFrequency() in the file: Sketchbook\libraries\RadioHead\RH_RF95.cpp;
// Arduino UNO + Dragino Lora Shield
// rf95.setModemConfig(RH_RF95::Bw31_25Cr48Sf512); // test OK (Slow + long range適用長距離)
// 採 RadioHead Library 
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on
  // Set Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. Slow+long range
  //  rf95.setModemConfig(RH_RF95::Bw125Cr48Sf4096);  // failed
  //  rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);   // test OK (Default medium range)
  //  rf95.setModemConfig(RH_RF95::Bw500Cr45Sf128);   // test OK (Fast + short range)
  //  rf95.setModemConfig(RH_RF95::Bw31_25Cr48Sf512); // test OK (Slow + long range適用長距離)

// Example sketch showing how to create a simple messageing server
// with the RH_RF95 class. RH_RF95 class does not provide for addressing or
// reliability, so you should only use RH_RF95  if you do not need the higher
// level messaging abilities.
// It is designed to work with the other example rf95_client
// Tested with Anarduino MiniWirelessLoRa, Rocket Scream Mini Ultra Pro with
// the RFM95W, Adafruit Feather M0 with RFM95

#include <SPI.h>
#include <RH_RF95.h>

// Singleton instance of the radio driver
RH_RF95 rf95;
//RH_RF95 rf95(5, 2); // Rocket Scream Mini Ultra Pro with the RFM95W
//RH_RF95 rf95(8, 3); // Adafruit Feather M0 with RFM95 

// Need this on Arduino Zero with SerialUSB port (eg RocketScream Mini Ultra Pro)
//#define Serial SerialUSB

int led = 13;
long counter=0;
void setup() 
{
  // Rocket Scream Mini Ultra Pro with the RFM95W only:
  // Ensure serial flash is not interfering with radio communication on SPI bus
//  pinMode(4, OUTPUT);
//  digitalWrite(4, HIGH);

//  pinMode(led, OUTPUT);     
  Serial.begin(9600);
  delay(1000);
  while (!Serial) ; // Wait for serial port to be available
  if (!rf95.init())
    Serial.println("init failed"); 
   Serial.println();
   Serial.println("Lora init passed");  
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on
  // Set Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. Slow+long range
  rf95.setModemConfig(RH_RF95::Bw125Cr48Sf4096);  // failed
  // rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);   // test OK (Default medium range)
  // rf95.setModemConfig(RH_RF95::Bw500Cr45Sf128);   // test OK (Fast + short range)
  // rf95.setModemConfig(RH_RF95::Bw31_25Cr48Sf512); // test OK (Slow + long range適用長距離)
  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);
  // If you are using Modtronix inAir4 or inAir9,or any other module which uses the
  // transmitter RFO pins and not the PA_BOOST pins
  // then you can configure the power transmitter power for -1 to 14 dBm and with useRFO true. 
  // Failure to do that will result in extremely low transmit powers.
//  driver.setTxPower(14, true);
  //rf95.printRegisters(); 
}

void loop()
{
  digitalWrite(led, LOW);
  counter++;
  String numString = "Server1: "+String(counter, DEC)+"         ";  //加空白以去除亂碼
  
  uint8_t data[14] = ""; 
  for (int i=0; i<14; i++)
  {
   data[i] =numString[i];  //     
  }   
      rf95.send(data, sizeof(data));
      rf95.waitPacketSent();
      digitalWrite(led, HIGH);
      Serial.println(numString);
  delay(1000);
}


