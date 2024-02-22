

//Libraries
#include <Wire.h>                               //Standard I2C libary
#include <SparkFun_I2C_Mux_Arduino_Library.h>   //MUX Library
#include "SparkFun_VL53L1X.h"                   //Distance Sensor Library

//Class instances:
QWIICMUX mux;
SFEVL53L1X dist_sensor[8]; //Create an array of distance sensors.
bool active[] = {0,0,0,0,0,0,0,0}; //Array to show active sensors


void setup() {
  Wire.begin();
  Serial.begin(115200);
  
  //Initialize MUX:
  if(!mux.begin()){
    Serial.println("MUX Failed");
    while(1);
  }
  else{
    Serial.println("Mux Initialized. Initializing Sensors.");
  }

  //Sensor initialization
  for(int i = 0; i < 8; i++){
    mux.setPort(i); //Set the mux port
    active[i] = dist_sensor[i].begin(); //Attempt to activate the sensor. Note if it failed.
    if(!active[i]){
      Serial.print("Sensor ");
      Serial.print(i);
      Serial.print(" present. Initializing...");
      //Initialize the sensor and ramp up the speed
      dist_sensor[i].startRanging(); // Start only once (and do never call stop)
      for(int j = 0; j < 105; j+=5){
        dist_sensor[i].stopRanging();
        dist_sensor[i].setTimingBudgetInMs(11 + 100-j);
        dist_sensor[i].setIntermeasurementPeriod(13 + 100-j);
        dist_sensor[i].startRanging(); // Start only once (and do never call stop)
        delay(10);
      }
      Serial.print(" Intermeasurement period: ");
      Serial.println(dist_sensor[i].getIntermeasurementPeriod());
      // Serial.println(" Complete.");
    }
    else{ //if(!active[i])
      Serial.print("Sensor ");
      Serial.print(i);
      Serial.println(" not present.");
    }
  }
}

//Timer polling counters
int dist_poll = millis();
int UI_poll = millis();
int counter[] = {1,0,0,0,0,0,0,0};
int counter2 = 0;

void loop() {
  //Poll the sensors every 9ms
  if(millis() > dist_poll + 5){
    counter2++;
    for(int i = 0; i < 8; i++){
      if(!active[i]){
        mux.setPort(i); //Set the mux port
        if(dist_sensor[i].checkForDataReady()){
          int distance = dist_sensor[i].getDistance();
          dist_sensor[i].clearInterrupt();
          counter[i]++;
          dist_poll = millis();
        }
      }
    }
  }

  if(millis() > UI_poll + 1000){
    for(int i = 0; i < 8; i++)
      if(!active[i]){
         Serial.print(counter[i]);
         Serial.print("\t");
         counter[i]=0;
        }
    Serial.print("\t");
    Serial.print(counter2);
    Serial.println();
    UI_poll = millis();   
    counter2 = 0;  
  }
  
    
}
