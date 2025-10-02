// Library採 RadioHead
// Arduino UNO + Dragino Lora Shield
// rf95.setModemConfig(RH_RF95::Bw31_25Cr48Sf512); // test OK (Slow + long range適用長距離)
// 採 RadioHead Library   
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on
  // Set Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. Slow+long range
  //  rf95.setModemConfig(RH_RF95::Bw125Cr48Sf4096);  // failed
  //  rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);   // test OK (Default medium range)
  //  rf95.setModemConfig(RH_RF95::Bw500Cr45Sf128);   // test OK (Fast + short range)
  //  rf95.setModemConfig(RH_RF95::Bw31_25Cr48Sf512); // test OK (Slow + long range適用長距離)
  
// 頻率設定位置: setFrequency() in the file: Sketchbook\libraries\RadioHead\RH_RF95.cpp;
// Example sketch showing how to create a simple messageing client
// with the RH_RF95 class. RH_RF95 class does not provide for addressing or
// reliability, so you should only use RH_RF95 if you do not need the higher
// level messaging abilities.
// It is designed to work with the other example rf95_server
// Tested with Anarduino MiniWirelessLoRa, Rocket Scream Mini Ultra Pro with
// the RFM95W, Adafruit Feather M0 with RFM95

#include <SPI.h>
#include <RH_RF95.h>
#include <Wire.h>
// #include <LiquidCrystal_I2C.h>
// LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x27 for a 16 chars and 2 line display

// Singleton instance of the radio driver
RH_RF95 rf95;
//RH_RF95 rf95(5, 2); // Rocket Scream Mini Ultra Pro with the RFM95W
//RH_RF95 rf95(8, 3); // Adafruit Feather M0 with RFM95 

// Need this on Arduino Zero with SerialUSB port (eg RocketScream Mini Ultra Pro)
//#define Serial SerialUSB
int counter=0;
int led = 13;

void setup() 
{
  // lcd.init();                      // initialize the lcd
  // Print a message to the LCD.
  // lcd.backlight();
  // lcd.setCursor(0,0);
  // lcd.print("III Lora Client   ");
  // lcd.setCursor(0,1);
  // lcd.print("Hsu Honghai");
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);

  Serial.begin(9600);
  while (!Serial) ; // Wait for serial port to be available
  if (!rf95.init())
    Serial.println("init failed");
  Serial.println("init passed");  
  // Defaults after init are 915.1MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on
  // Set Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. Slow+long range
  rf95.setModemConfig(RH_RF95::Bw125Cr48Sf4096);  // failed
  // rf95.setModemConfig(RH_RF95::Bw125Cr45Sf128);   // test OK (Default medium range)
  // rf95.setModemConfig(RH_RF95::Bw500Cr45Sf128);   // test OK (Fast + short range)
  // rf95.setModemConfig(RH_RF95::Bw31_25Cr48Sf512);    // test OK (Slow+long range)
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
 
   if (rf95.available())
  {
    // Should be a message for us now   
    uint8_t buf[14];
    uint8_t len = sizeof(buf);
    if (rf95.recv(buf, &len))
    {
      digitalWrite(led, HIGH);
      counter++;
//    RH_RF95::printBuffer("request: ", buf, len);
      Serial.print("Rx: ");
      Serial.println((char*)buf);
      Serial.print("RSSI: ");
      Serial.println(rf95.lastRssi(), DEC);
      // lcd.clear();
      // lcd.setCursor(0,0);
      // lcd.print((char*)buf);   
      // lcd.setCursor(0,1);
      // lcd.print("RSSI: "); 
      // lcd.print(rf95.lastRssi()); 
      // lcd.print(" T"); 
      // lcd.print(counter);
    }
  }
}


