/*multiDeck.ino
Created by Josh Chapman
This file is to test interfaceing an arduino board with a CrazyFlie ranging deck
This file is a work in progress
*/

/* The Crazyflie multi range board switches sensors using the XSHUT pin, which resets the sensor every time it is used. This SEVERELY limits the possible speed of data aquisition.
*/

// Can use this command to set each sensor on its own address. If this is done the PCA is only needed for the initial setup.
// distanceSensor.setI2CAddress(0x23);


//Current task: Migrate code to multiDeck.h
#include <Wire.h>               //Standard I2C Library
#include "multiDeck.h"



void setup(){
  Wire.begin(); //Initialize I2C
  Serial.begin(115200); //Serial for debug purposes
  CFMultiDeck_init();
}

void loop(){
  delay(100);//delay for prototyping
  



  multiDeck_refresh();
  
  multiDeck_print();
  
  }