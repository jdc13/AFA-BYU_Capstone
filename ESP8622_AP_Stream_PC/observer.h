/*Observer.h
Created by:   Josh Chapman
Date:         12/1/2023
Description:  This file contains a class for a basic 6 axis observer.
              Requires linearized functions.
*/

class observer{
  public:
    float X[12]; //State vector:
      /*  
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
    
    //State Space Equation Matricies
    // float A[12][12]; //nxn matrix where n is number of states
    // float B[12][1];  //nxm matrix where m is number of inputs
    // float C[12][12]; //nxn matrix
    // float D[12][1];
    
    //Corrector Gain
    float L[1]; //k vector where k is number of sensors
  
    //constructor
    observer(){
      
    }
    
    //simple update using Euler's method
    void update(float t){
      X[0] += X[1] * t; // X position = x velocity * time
      X[1] = 1; //X velocity equation
      X[2] += X[3] * t; //y position = y velocity * time
      X[3] = 0; //y velocity equation
      X[4] += X[5] * t; //z position = z velocity * time
      X[5] = 0; // Z velocity equation
      X[6] += X[7] * t; //roll position = roll velocity * time
      X[7] = 0; // Roll velocity equation
      X[8] += X[9] * t; //pitch position = pitch velocity * time
      X[9] = 0; // Pitch velocity equation
      X[10] += X[11] * t; //Yaw position = yaw velocity * time
      X[11] = 0; //Yaw velocity equation
      }
    

};