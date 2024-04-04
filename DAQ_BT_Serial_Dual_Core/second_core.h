/*Header to keep second core code seperate from the rest.
*/
//Bluetooth setup will be handled by this core
#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

//Global variables that need to be shared between cores need to be in this file
//dualCore namespace reserved for variables that are only required to enable dual core functionality
namespace dualCore
{
  bool lock = false;
}

String Bank_R; // Main string to transmit sensor data from right bank
String Bank_L; //Main string to transmit sensor data from left bank

//Second Core Task Handle
TaskHandle_t Task0; //Task to run on core 0
//Loop and setup code run on core 1


void Task0Code(void * parameter){
  SerialBT.begin("ESP32test"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
  
  for(;;){
    delay(200); //Small delay to make sure the other core can process.
    while(dualCore::lock == true){
     Serial.println("Second core waiting on locked variables");
    }
    dualCore::lock = true; //Lock the bank variables
    String Transmit_buffer = Bank_R + "l" + Bank_L; //Save the sensor data to the buffer
    //Clear the buffers:
    Bank_R = "";
    Bank_L = "";
    dualCore::lock = false; //unlock the buffers
      
    //Transmit the data
    SerialBT.println(Transmit_buffer);

    
  }
}