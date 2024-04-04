/*DAQ_BT_Serial_Dual_Core
This file will collect and transform the data from the distance sensors and transfer them over bluetooth
Core 1 will handle data collection
Core 2 will handle transmission
*/

#include "second_core.h"

//Hardware Libraries
#include <Wire.h>               //I2C Main
#include <TCA9548A.h>           //I2C Mux
#include "SparkFun_VL53L1X.h"   //Distance Sensor


//Bad reading filtering parameters
const float   dist_min  = .15;  //Minimum reading for a valid measurement
const float   dist_var  = .3;   //Maximum variation between distance readings for a given sensor
float         last_reading[8];  //Array to store last reading for each sensor

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
float speed = 1; //m/s
unsigned long start = 0;
unsigned long end = 0;

//Built in user-controlled button on the ESP32 v2
#define button 38




void setup() {
  Serial.begin(115200);
  
  //Hardware Initializations:
  pinMode(button, INPUT);
  
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


  xTaskCreatePinnedToCore(
                          Task0Code,    //Function
                          "Task 0",     //Name
                          10000,        //Stack size (words)
                          NULL,         //Input parameter
                          0,            //Task Priority
                          &Task0,       //Task Handle
                          0             //Core to run the task
);



}

void loop() {
  //Soft Reset:
  if(digitalRead(button) == false){
          Bank_R = "";
          Bank_L = "";
          position = 0;     
  }
  if(SerialBT.available())  {
    char signal = SerialBT.read();    
    if(signal = 'r'){
      Bank_R = "";
      Bank_L = "";
      position = 0; 
      Serial.println("Soft Reset");
      while(SerialBT.available()){
        SerialBT.read();
      }      

    }
  }
  //Check Distance Sensors
  //Left Bank
  for(int i = 1; i <=6; i++){
    I2CMux.openChannel(i);
    if(dist[i].checkForDataReady()){ //Check the sensor to see if it has data

      while(dualCore::lock == true){ //Wait for the second core to free up the variable
                Serial.println("Primary core waiting on locked variables (1)");
      }
           
      
      
      float distance = dist[i].getDistance()*1e-3; //get distance and convert to meters 
      
      if(abs(distance-last_reading[i]) < dist_var && distance > dist_min){ //Only store the point if the filtering requirements are met
        
        dualCore::lock = true; //Lock the bank buffer
        if(i <=3){//Left Bank
          Bank_L += String(distance * vectors[i][0] + position) + "c" + String(distance * vectors[i][1]) + "p";    
        }
        else{ //Right Bank
          Bank_R += String(distance * vectors[i][0] + position) + "c" + String(distance * vectors[i][1]) + "p";          
        }
         
        dualCore::lock = false; //Unlock the buffers
      }
      last_reading[i] = distance; //Save the distance as the last reading for the next comparison
      
      dist[i].clearInterrupt(); //Clear the interrupt to make sure the sensor is good to go
    }
    I2CMux.closeChannel(i);
  }

  

  
  
  end = millis();
  position = position + speed * (end-start)*1e-3;
  
  start = end;



  
}
