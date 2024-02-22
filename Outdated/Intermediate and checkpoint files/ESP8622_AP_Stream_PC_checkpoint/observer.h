/*Observer.h
Created by:   Josh Chapman
Date:         12/1/2023
Description:  This file contains a class for a basic 6 axis observer.
              Requires linearized functions.
*/

class observer{
  public:
    float X[12]; //State matrix:
      /*  
          Index Variable    Meaning
          0     x           (Primary direction of movement. forward is positive)
          1     dx/dt 
          2     y           (Lateral direction, left is positive)
          3     dy/dt
          4     z           (Verticle direction, up is positive)
          5     dzdt
          6     theta       (Rotation on x axis, roll)
          7     dtheta/dt
          8     alpha       (Rotation on y axis, pitch)
          9     dalpha/dt
          10    beta        (Rotation on z axis, yaw)
          11    dbeta/dt

          Signs for angles follow right hand convention
          linear units may be anything. 
          Angular units must be radians
      */
    
    //State Space Equation Matricies
    float A[12][12]; //nxn matrix where n is number of states
    float B[12][1];  //nxm matrix where m is number of inputs
    float C[12][12]; //nxn matrix
    // float D[12][1];
    
    //Corrector Gain
    float L[12][1]; //nxk matrix where k is number of sensors
      

};