

/* DAQ_Server
Created By:   Joshua Chapman
Date:         2/21/24
Description:  This code collects data from several sensors and posts 2D point cloud data to a wifi server
              to be retrieved by a base station.
*/

/*To Do:
- Set up wifi access point to transmit data
- Have WiFi access point running on one core while the sensor data is running on the second core.
- Verify Sensor rates
*/

//Hardware Libraries
#include <Wire.h>               //I2C Main
#include <TCA9548A.h>           //I2C Mux
#include "SparkFun_VL53L1X.h"   //Distance Sensor


//Hardware Class Initializations
TCA9548A      I2CMux;     //I2C Mux
SFEVL53L1X    dist[8];    //Distance Sensor Array. Using 8 channels to keep the channel matching the array index. Only using 1,2,3,4,5,6



//Data Transformation Variables
float position = 0;
float vectors[8][2] = {{.707, .707}, //Unit vectors to convert distance readings to points relative to projectile Using 8 vectors to keep indexes consistent for the sensors.
                     {.5, .086,},
                     {0, 1},
                     {-.5, 0.866},
                     {-.5, -.866},
                     {0, -1},
                     {0.5, -0.866},
                     {0.707, -0.707}};
float speed = 10; //m/s
unsigned long start = 0;
unsigned long end = 0;


//Sensor Bank Data Strings
String Bank_R; // Main string to transmit sensor data from right bank
bool lock_R = false; //Boolean to avoid data conflicts in dual core mode
String Bank_L; //Main string to transmit sensor data from left bank
bool lock_L = false; //Boolean to avoid data conflicts in dual core mode
String buff_R; //Buffer for right (place data here if the main string is being used to transmit data)
String buff_L; //Buffer for left (place data here if the main string is being used to transmit data)





void setup() {
  Serial.begin(115200);

  //Mux Initialization
  //  Wire.setPins(21, 22);       // ESP32 users, use setPins(sda, scl) if customised, *before* passing Wire to the library (the line below).  
  I2CMux.begin(Wire);             // Wire instance is passed to the library
  I2CMux.closeAll();              // Set a base state which we know (also the default state on power on)  

  //Initialize Distance Sensors
  for(int i = 1; i <= 6; i++){
    Serial.print("Initializing Sensor ");
    Serial.println(i);
    I2CMux.openChannel(i); //Open the channel
    if(dist[i].begin() !=0){
      Serial.print("Sensor ");
      Serial.print(i);
      Serial.println("Failed");
    }  
    else{
      dist[i].setTimingBudgetInMs(17); 
      dist[i].setIntermeasurementPeriod(20);
      dist[i].startRanging();
    }      
    I2CMux.closeChannel(i);
    start = millis();
  }

    
}


void loop() {
  
  //Check Distance Sensors
  //Left Bank
  for(int i = 1; i <=3; i++){
    I2CMux.openChannel(i);
    if(dist[i].checkForDataReady()){ //Check the sensor to see if it has data
      
      float distance = dist[i].getDistance(); //Will need to change this line to feed data to the server
      if(!lock_R){
        Bank_R += String(distance * vectors[i][0] + position) + "," + String(distance * vectors[i][1]) + "\t";
      }
      else{
        buff_R += String(distance * vectors[i][0])+ position + "," + String(distance * vectors[i][1]) + "\t";  
      }
      
      dist[i].clearInterrupt(); //Clear the interrupt to make sure the sensor is good to go
    }
    I2CMux.closeChannel(i);
  }

  
  //Right Bank
  for(int i = 4; i <=6; i++){
    I2CMux.openChannel(i);
    if(dist[i].checkForDataReady()){ //Check the sensor to see if it has data
      float distance = dist[i].getDistance(); //Will need to change this line to feed data to the server
      if(!lock_L){
        Bank_L += String(distance * vectors[i][0] + position) + "," + String(distance * vectors[i][1]) + "\t";  
      }
      else{
        buff_L += String(distance * vectors[i][0] + position) + "," + String(distance * vectors[i][1]) + "\t";  
      }
      dist[i].clearInterrupt(); //Clear the interrupt to make sure the sensor is good to go
    }
  I2CMux.closeChannel(i);    
  }
  
  //Increment travel distance
  end = millis();
  position = position + speed * (end-start)*1e-3;
  
  start = end;

  // String Data = Bank_R + "\n" + Bank_L;
  // Bank_R = "";
  // Bank_L = "";
  
  // Serial.println(Data);
  // delay(10);

  
  
}
