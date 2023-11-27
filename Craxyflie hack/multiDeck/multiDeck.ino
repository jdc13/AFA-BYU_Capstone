/*multiDeck.ino
Created by Josh Chapman
This file is to test interfaceing an arduino board with a CrazyFlie ranging deck
This file is a work in progress
*/

/* The Crazyflie multi range board switches sensors using the XSHUT pin, which resets the sensor every time it is used. This SEVERELY limits the possible speed of data aquisition.
*/

// Can use this command to set each sensor on its own address. If this is done the PCA is only needed for the initial setup.
// distanceSensor.setI2CAddress(0x23);


//Current task: Test MUX interface and attempt sensor read
#include <Wire.h>               //Standard I2C Library
#include "SparkFun_VL53L1X.h"   //Sparkfun's distance sensor library


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

void PCASetSensor(byte sensor){//Function to activate the selected sensor through the PCA chip
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



void setup(){
  Wire.begin(); //Initialize I2C
  Serial.begin(115200); //Serial for debug purposes
  
  int PCAPins[] = {up, back, Right, Front, Left};

  //Initialize PCA9534 MUX
    Wire.beginTransmission(PCA_ADDR + 0);
    Wire.write(PCA_CON);
    Wire.write(0x00); //set all pins to 0 so everything is an output
    Wire.endTransmission();

  
  //Initialize sensor array:
    Serial.println("Initializing Sensors:");
    int active = 0;   
     
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
            int period = 10;
            dist_sensor[i].setTimingBudgetInMs(period);
            dist_sensor[i].setIntermeasurementPeriod(period + 1);
            dist_sensor[i].startRanging(); //Write configuration bytes to initiate measurement
    }
    
}

void loop(){
  delay(100);//delay for prototyping
  
  int dist[5] = {0, 0, 0, 0, 0};//array of distances. Will be a 0 if there isn't any data for that sensor.


  for(int i = 0; i < 5; i++){//Check for data from the sensors. If there is data, record it.
    if(dist_sensor[i].checkForDataReady()){
      dist[i] = dist_sensor[i].getDistance();
      dist_sensor[i].clearInterrupt(); 
    }
  }
 
  //Print any non-0 values
  if(dist[0] != 0){  
    Serial.print("up: ");
    Serial.print(dist[0]);
  }
  if(dist[1] !=0){
    Serial.print("\tback: ");
    Serial.print(dist[1]);
  }
  if(dist[2] !=0){
  Serial.print("\tright: ");
  Serial.print(dist[2]);
  }
  if(dist[3] != 0){
    Serial.print("\tfront: ");  
    Serial.print(dist[3]);
  }
  if(dist[4] !=0){
    Serial.print("\tleft: ");
    Serial.print(dist[4]);
  }
  Serial.println();  
  }