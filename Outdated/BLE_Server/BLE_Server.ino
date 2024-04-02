#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>


#define bleServerName   "Capstone_Server"
#define SERVICE_UUID    "1c6a7649-9856-412c-89ac-e11532014156"
#define right_bank_UUID "71b9e3f9-d79d-492c-a1ba-421a984355f5"
#define left_bank_UUID  "60ca246c-0619-42cb-a31e-037c5ef12306"


BLECharacteristic right_bank_Characteristic(right_bank_UUID);
BLEDescriptor right_bank_Descriptor(BLEUUID((uint16_t)0x2902));

BLECharacteristic left_bank_Characteristic(left_bank_UUID);
BLEDescriptor left_bank_Descriptor(BLEUUID((uint16_t)0x2902));

bool deviceConnected = false;

//Setup callbacks onConnect and onDisconnect
class MyServerCallbacks: public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) {
    deviceConnected = true;
    Serial.println("Connected");
  };
  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
  }
};



void setup() {
//Initialize Server:
Serial.begin(115200);

//Create the BLE device
BLEDevice::init(bleServerName);

//Create the BLE server
BLEServer *pServer = BLEDevice::createServer();
pServer->setCallbacks(new MyServerCallbacks());

//Create the BLE service:
BLEService *daqService = pServer->createService(SERVICE_UUID);

//Create the BLE characteristics and BLE Descriptors
daqService->addCharacteristic(&right_bank_Characteristic);
right_bank_Descriptor.setValue("Right Bank");
right_bank_Characteristic.addDescriptor(&right_bank_Descriptor);

daqService->addCharacteristic(&left_bank_Characteristic);
left_bank_Descriptor.setValue("Left Bank");
left_bank_Characteristic.addDescriptor(&left_bank_Descriptor);

//Start the service:
daqService->start();

//Start Advertising
BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
pAdvertising->addServiceUUID(SERVICE_UUID);
pServer->getAdvertising()->start();



}
int val = 1234;
void loop() {
  val++;
  delay(1000);
  
  Bl
  
  if(deviceConnected){
    Serial.println("Connected");
    char value[6];
    dtostrf(val, 6, 2, value);
        right_bank_Characteristic.setValue(value);
        right_bank_Characteristic.notify();
        left_bank_Characteristic.setValue(value);
        left_bank_Characteristic.notify();
  }

}
