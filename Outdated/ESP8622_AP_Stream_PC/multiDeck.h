/*multiDeck.h
Created by:   Josh Chapman
Date:         11/29/2023
Description:  This file contains functions to initialize the crazyflie deck at a high refresh rate and make readings accessable.

*/

#ifndef multiDeck_H
#define multiDeck_H

#include "SparkFun_VL53L1X.h"   //Sparkfun's distance sensor library
#include <Wire.h>

float MD_dist[5] = {0, 0, 0, 0, 0};//array of distances. Will be a 0 if there isn't any data for that sensor. Updated by multiDeck_refresh()

//PCA9534 I/O Extender Registers:
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
  

//PCA pin assignments:
  const int up =    0b000000001;
  const int back =  0b000000010;
  const int Right = 0b000000100;
  //Not used        0b000001000
  const int Front = 0b000010000;
  //Not used        0b000100000
  const int Left =  0b001000000;
  //Not used        0b010000000
  //Not used        0b100000000

void PCASetSensor(byte sensor){//Function to activate the selected sensor(s) through the PCA chip
  Wire.beginTransmission(PCA_ADDR + 0); //Begin communication in write mode
  Wire.write(PCA_OUT);                  //Tell the PCA to change output pin levels
  Wire.write(sensor);                   //Activate the pin(s) coresponding to the desired sensor(s)
  Wire.endTransmission();               //End Transmission
  }

SFEVL53L1X dist_sensor[5]; //Create an array of distance sensors.

//Sensor indexes - can call the sensors by name or by the index.
  #define sen_up 0
  #define sen_back 1
  #define sen_right 2
  #define sen_front 3
  #define sen_left 4


void CFMultiDeck_init(){ //Initialize all hardware on the CF Multi range deck. 
    Wire.begin();
    int PCAPins[] = {up, back, Right, Front, Left}; //array of pin assignments for the PCA

  //Initialize PCA9534 MUX
    Wire.beginTransmission(PCA_ADDR + 0);
    Wire.write(PCA_CON);
    Wire.write(0x00); //set all pins to 0 so everything is an output
    Wire.endTransmission();

  
  //Initialize sensor array:
    Serial.println("Initializing Sensors:");
    int active = 0;   

    PCASetSensor(0x00); //reset all sensors - this prevents errors if the MCU is reset but the sensor array is not.
    for(int i = 0; i <5; i++){
      active += PCAPins[i]; //leave all initialized sensors active
      PCASetSensor(active); //activate next sensor
      delay(1); //delay to allow boot up.
      
      //Change sensor address:
        //Uncomment serial lines to view process in the terminal.
        int addr = 0x20 + i*2; //New sensor address
        
        //Change sensor address - show process in terminal (optional)
        // Serial.print("Sensor ");
        // Serial.print(i);
        // Serial.print(": 0X");
        // Serial.print(dist_sensor[i].getI2CAddress(), HEX);
        // Serial.print(" Canged to 0X");
        
        dist_sensor[i].setI2CAddress(addr);
        
        // Serial.println(dist_sensor[i].getI2CAddress(), HEX);
      
      //initialize sensor      
        int status = dist_sensor[i].begin();
    
        if(status != 0 ){//returns 0 for successful initialization
          Serial.print("Sensor ");
          Serial.print(i);
          Serial.print(" initialization failed. Status = ");
          Serial.println(status);
          while(1);
          }

          //Set the intermeasurement period to as small as possible. Needs to be >= timing budget.
            int period = 10; //ms
            dist_sensor[i].setTimingBudgetInMs(period);
            dist_sensor[i].setIntermeasurementPeriod(period);
            dist_sensor[i].startRanging(); //Write configuration bytes to initiate measurement
    }
  }



void multiDeck_refresh(){ //Update MD_dist with current measurements
  for(int i = 0; i < 5; i++){//Check for data from the sensors. If there is data, record it.
    if(dist_sensor[i].checkForDataReady()){
      MD_dist[i] = dist_sensor[i].getDistance();
      dist_sensor[i].clearInterrupt();      
      }
    else{
      MD_dist[i] = 0; //if there is no data, use 0 as a place holder.
      }
    }
  }


void multiDeck_print(){ //Print distance values to serial terminal
   //Print any non-0 values
  if(MD_dist[0] != 0){  
    Serial.print("up: ");
    Serial.print(MD_dist[0]);
  }
  if(MD_dist[1] !=0){
    Serial.print("\tback: ");
    Serial.print(MD_dist[1]);
  }
  if(MD_dist[2] !=0){
  Serial.print("\tright: ");
  Serial.print(MD_dist[2]);
  }
  if(MD_dist[3] != 0){
    Serial.print("\tfront: ");  
    Serial.print(MD_dist[3]);
  }
  if(MD_dist[4] !=0){
    Serial.print("\tleft: ");
    Serial.print(MD_dist[4]);
  }
  Serial.println(); 
  }

#endif