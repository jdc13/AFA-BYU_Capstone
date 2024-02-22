/*
  Reading distance from the laser based VL53L1X
  By: Nathan Seidle
  SparkFun Electronics
  Date: April 4th, 2018
  License: This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).

  SparkFun labored with love to create this code. Feel like supporting open source hardware? 
  Buy a board from SparkFun! https://www.sparkfun.com/products/14667

  This example prints the distance to an object.

  Are you getting weird readings? Be sure the vacuum tape has been removed from the sensor.
*/

#include <Wire.h>
#include "SparkFun_VL53L1X.h" //Click here to get the library: http://librarymanager/All#SparkFun_VL53L1X

//Optional interrupt and shutdown pins.
#define SHUTDOWN_PIN 2
#define INTERRUPT_PIN 3

SFEVL53L1X distanceSensor;
//Uncomment the following line to use the optional shutdown and interrupt pins.
//SFEVL53L1X distanceSensor(Wire, SHUTDOWN_PIN, INTERRUPT_PIN);

void setup(void)
{
  Wire.begin();

  Serial.begin(115200);
  Serial.println("VL53L1X Qwiic Test");

  if (distanceSensor.begin() != 0) //Begin returns 0 on a good init
  {
    Serial.println("Sensor failed to begin. Please check wiring. Freezing...");
    while (1)
      ;
  }
  Serial.println("Sensor online!");



  //attempt to ramp down
  distanceSensor.startRanging(); // Start only once (and do never call stop)
  for(int i = 0; i < 105; i+=5){
    distanceSensor.stopRanging();
    distanceSensor.setTimingBudgetInMs(10 + 100-i);
    distanceSensor.setIntermeasurementPeriod(13 + 100-i);
    distanceSensor.startRanging(); // Start only once (and do never call stop)
    delay(200);

  }
  // Intermeasurement period must be >= timing budget. Default = 100 ms.
  Serial.print("Intermeasurement period: ");
  Serial.println(distanceSensor.getIntermeasurementPeriod());
  delay(500);
  

}

int counter = 0;
int poll = millis();
int poll2 = millis();
int hold = 9;
void loop(void)
{
  
  if(millis() > poll2 + hold)
  {
    if(distanceSensor.checkForDataReady()){
      int distance = distanceSensor.getDistance(); //Get the result of the measurement from the sensor
      distanceSensor.clearInterrupt();
      // Serial.println(distance);
      counter++;
      poll2 = millis();
    }
  }

  if(millis() > poll + 1000){
    Serial.println(counter);
    // delay(500);
    counter = 0;
    poll = millis();
  }


  long var; //variable to store the first integer
  long new_period;//variable to store the new period
  
  if(Serial.available()){
    var = Serial.parseInt();
    while(!Serial.available()){} //wait for the next variable
    long new_period = Serial.parseInt();

    
    while(Serial.available()){
      Serial.read();//Clear the buffer
    }

    if(var == 0){
      Serial.println("Changing Timing Budget.");
      Serial.print("New Budget: ");
      Serial.println(new_period);
      distanceSensor.stopRanging();
      distanceSensor.setTimingBudgetInMs(new_period);
      distanceSensor.startRanging();
    }
    else if(var ==1){
      Serial.println("Changing Intermeasurement period.");
      Serial.print("New Period: ");
      Serial.println(new_period);
      distanceSensor.stopRanging();
      distanceSensor.setIntermeasurementPeriod(new_period);
      distanceSensor.startRanging();
    }
    else if(var == 2){
      Serial.println("Changing hold time");
      Serial.print("New Period: ");
      Serial.println(new_period);
      hold = new_period;
    }
    
    
    // distanceSensor.setIntermeasurementPeriod(new_period);
    Serial.print("Timing changed. New period:");
    Serial.println(new_period);
    // Serial.println(". Restarting Sensor");
    // distanceSensor.startRanging();
    
    hold = new_period;

    poll = millis();
  }
    
  

  // Serial.print("Distance(mm): ");
  // Serial.print(distance);

  // float distanceInches = distance * 0.0393701;
  // float distanceFeet = distanceInches / 12.0;

  // Serial.print("\tDistance(ft): ");
  // Serial.print(distanceFeet, 2);

  // Serial.println();
}
