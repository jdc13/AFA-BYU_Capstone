/*multiDeck.ino
Created by Josh Chapman
This file is to test interfaceing an arduino board with a CrazyFlie ranging deck
This file is a work in progress
*/

/* The Crazyflie multi range board switches sensors using the XSHUT pin, which resets the sensor every time it is used. This SEVERELY limits the possible speed of data aquisition.
*/


//Current task: Test MUX interface and attempt sensor read
#include <Wire.h>               //Standard I2C Library
#include "SparkFun_VL53L1X.h"   //Sparkfun's distance sensor library


//PCA9534 MUX Registers
#define PCA_IN 0x00   //input register (not used)
#define PCA_OUT 0x01  //output register (used to select sensor)
#define PCA_POL 0x02  //polarity register (not used)
#define PCA_CON 0X03  //configuration register (used to set outputs)
//address register
#define A0 0 //A pin signal. 0 = pulled gnd, 1 = pulled high
#define A1 0 
#define A2 0
// Slave register from datasheet:
// 0b0100 A2 A1 A0 R/W
// First 4 bits fixed at 0x4. next 3 bits are determined by A# pins (See above) last bit is read/write.
#define PCA_ADDR 0x20 + A0*0b0010 + A1*0b0100 + A2*0b1000


//PCA MUX pin assignments
#define up    0b000000001
#define back  0b000000010
#define Right 0b000000100
//Not used    0b000001000
#define Front 0b000010000
//Not used    0b000100000
#define Left  0b001000000
//Not used    0b010000000
//Not used    0b100000000
//Create an array for loops... later

void PCASetSensor(byte sensor){//Function to activate the selected sensor through the PCA chip
  Wire.beginTransmission(PCA_ADDR + 0);
  Wire.write(PCA_OUT);
  Wire.write(sensor);
  Wire.endTransmission();


  //Debug Code:
  // Wire.requestFrom(PCA_ADDR,1);
  // while(Wire.available()){
  //   byte reg = Wire.read();
  //   Serial.print("MUX Register:");
  //   Serial.println(reg);
  // }
  
  
  
}

//Will use separate instances for consistency and readability. In an array to help with loops.

SFEVL53L1X dist_sensor[5]; //Create an array of distance sensors.
//Sensor indexes - can call the sensors by name or by the index.
#define sen_up 0
#define sen_left 1
#define sen_right 2
#define sen_front 3
#define sen_back 4


void setup(){
  Wire.begin(); //Initialize I2C
  Serial.begin(115200);
  
  //Initialize PCA9534 MUX
    Wire.beginTransmission(PCA_ADDR + 0);
    Wire.write(PCA_CON);
    Wire.write(0x00); //set all pins to 0 so everything is an output
    Wire.endTransmission();



  
  
  
  // status = sen_left.begin();
  // if(status != 0 ){//returns 0 for successful initialization
  //   Serial.print("Left sensor initialization failed. Status = ");
  //   Serial.println(status);
  //   while(1);
  // }
  // else{
  //   Serial.println("Successful initialization");
  // }
  

}

void loop(){


  //Initialize sensor(s)
  PCASetSensor(up);
  int status = dist_sensor[0].begin();
  if(status != 0 ){//returns 0 for successful initialization
    Serial.print("up sensor initialization failed. Status = ");
    Serial.println(status);
    while(1);
  }
  
  dist_sensor[0].startRanging(); //Write configuration bytes to initiate measurement
  // Serial.println("Data collection initialized");

  // Code blocking-- will need to change this to work with an interrupt
  // Serial.println("Waiting for data");
  while(!dist_sensor[0].checkForDataReady()){
    delay(1);
  }
  // delay(100);  

    
  int distance = dist_sensor[0].getDistance(); //Get the result of the measurement
  //Reset sensor
  PCASetSensor(Left);
  // sen_up.clearInterrupt();
  // sen_up.stopRanging(); //From example code. May be beneficial to remove this to remove an extra step.
  
  Serial.print("Distance (mm): ");
  Serial.println(distance);
  }