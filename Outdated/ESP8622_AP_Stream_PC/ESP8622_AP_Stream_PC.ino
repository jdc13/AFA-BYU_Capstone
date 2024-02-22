/*ESP8622_AP_Stream_PC
This file streams points in 2D related to the location of the sensor package

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
int counter;
ESP8266WebServer server(80);
void handleRoot() {
  server.send(200, "text/html", line);
  line = ""; //clear the line  
  // server.send(200, "text/html", String(counter));
  // counter = 0;
}

//Sensor Setup
#include "multiDeck.h"
#include <Kalman.h>

//Observer Setup
#include "observer.h"
observer location;

void setup() {
  delay(100);
  Serial.begin(115200);
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
  Serial.println("Sensor initialization successful");
  
}

// Timer poll variables (using polling to avoid timer conflicts)
int serv_refresh = 0;
int sen_refresh = 0;
float obs_refresh = millis();
int counter_refresh = millis();

void loop() {
  //Handle client requests 10 times a second
  if(millis()> serv_refresh+100){
    // Serial.println(counter);
    // counter = 0;
  server.handleClient();
  serv_refresh = millis();
  }

  //Code to check refresh rate
  if(millis() > counter_refresh + 1000){
    Serial.println(counter);
    counter = 0;
    counter_refresh = millis();    
  }
  
  //Refresh sensor> data
  if(millis() > sen_refresh + 20){ //don't constantly bug the distance sensors.
    multiDeck_refresh(); 
    // multiDeck_print();
    sen_refresh = millis();
    location.update((float(millis())-obs_refresh));
    obs_refresh = float(millis());  
  }

  //Update observer
  
  
  
  //Convert the sensor data to a string to send to the server
  // up    0
  // back  1
  // right 2
  // front 3
  // left  4
  // Values to convert sensor readings to vectors in the relative frame
  //               u    b       r       f     l
  float x_rel[] = {0,   -.707,  .707,   .707, -.707};   
  float y_rel[] = {0,   -.707,  -.707,  .707, .707 };
  float z_rel[] = {1,   0,      0,      0,    0    };

  for(int i = 1; i < 5; i++){
    if(MD_dist[i] !=0){
      counter++; //Show an additional reading has been made
      //convert sensor reading to m 
      MD_dist[i] /= 1000;     
      //Get relative coordinate      
      float x = MD_dist[i] * x_rel[i];
      float y = MD_dist[i] * y_rel[i];
      float z = MD_dist[i] * z_rel[i];

      //Convert relative coordinate to absolute frame
      /*  State Vector Variables:
          Index Variable    Meaning
          0     x           (Primary direction of movement. forward is positive)
          1     dx/dt 
          2     y           (Lateral direction, left is positive)
          3     dy/dt
          4     z           (Verticle direction, up is positive)
          5     dzdt
          6     gamma       (Rotation on x axis, roll)
          7     dgamma/dt
          8     beta        (Rotation on y axis, pitch)
          9     dbeta/dt
          10    alpha       (Rotation on z axis, yaw)
          11    dalpha/dt

          Signs for angles follow right hand convention
          linear units may be anything. 
          Angular units must be radians
      */
      float Dx      = location.X[0];
      float Dy      = location.X[2];
      float Dz      = location.X[4];
      float gamma   = location.X[6];
      float beta    = location.X[8];
      float alpha   = location.X[10];

      //Get coordinates using small angle approximation
      x = x + Dx                      + alpha*(y + Dy)                + (beta + gamma*alpha)*(z+Dz);
      y = (x+Dx)*(beta*gamma + alpha) + (alpha*beta*gamma + 1)*(y+Dy) + (z+Dz)*(alpha*beta-gamma);
      z = (x+Dx)*(beta + alpha*gamma)  + (y+Dy)*gamma                  + z+Dz;

      line +=  String(x) + "," + String(y) + "," + String(z) + "@";
      
                  
      MD_dist[i] = 0;   
    }      
  } 
  // Serial.println(location.X[0]);
}
