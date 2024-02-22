/*ESP8622_AP_Stream_MD
This file streams raw data from the multiDeck. This is an intermediate step file in getting points from the environment to a user interface device.

*/

/*This file is adapted from the wifi access point example */
/* Go to http://192.168.4.1 in a web browser
   connected to this access point to see it.
*/

//Wifi Libraries
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

//Access point Setup
#ifndef APSSID
#define APSSID "ESPap"
#define APPSK "thereisnospoon"
#endif
const char *ssid = APSSID;
const char *password = APPSK;

//Server Setup
String line; // empty string to store the line to send to the server

ESP8266WebServer server(80);
void handleRoot() {
  server.send(200, "text/html", "Sensor Data: " + line);
  line = ""; //clear the line  
}

//Sensor Setup
#include "multiDeck.h"

void setup() {
  delay(1000);
  Serial.begin(115200);
  Serial.println();
  Serial.print("Configuring access point...");
  /* You can remove the password parameter if you want the AP to be open. */
  WiFi.softAP(ssid, password);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  server.on("/", handleRoot);
  server.begin();
  Serial.println("HTTP server started");

  //Initialize the mutlideck
  CFMultiDeck_init();
  
}


void loop() {
  server.handleClient();
  
  //Refresh sensor data
  multiDeck_refresh();
  delay(1);
  
  //Convert the sensor data to a string to send to the server

  for(int i = 0; i < 4; i++){
    if(MD_dist[i] !=0){
      line = line + String(MD_dist[i]);
      line = line + ", ";
    }      
  } 
  if(MD_dist[4]!=0){   
    line = line + String(MD_dist[5]);
  }
  // Serial.println(line);

  // server.send(200, "text/html", line);

}
