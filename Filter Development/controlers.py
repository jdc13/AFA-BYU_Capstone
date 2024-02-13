#controlers.py
#This file contains several controllers to be used in different types of systems. The controlers are developed based on
#the BYU controls class, and are intended to allow for quick design of control loops based on the transfer function of the system.
#This file is currently under development. changes to controllers may be made and cause problems. Some blocks of code may be rather messy.
#Created by Josh Chapman

import numpy as np
import control as cnt
from scipy import signal

live = False #Set time step to this to use actual elapsed time in the integrals and derivatives.
import time

#Controllers:

class PD2ndOrder:#PD controller using pure derivative
    #Physical System Transfer Function:
    #       b0
    # s**2 + a1*s + a0
    
    #Desired Reponse Parameters:
    # wn = Natural Frequency
    # z = Damping Ratio
    
    
    def __init__(self, b0, a1, a0, tr, z, Tstep, mn=0, mx=0):
        #operating variables
        self.timeOld = 0            #Variable to store old time for live calculations
        self.firstRun = True        #Tells whether or not the controller is on its first run
        self.Tstep = Tstep          #time step for simulation
        self.yold = 0               #Old value for differentiator and integrators

        #Physical system transfer coefficients
        self.a1 = a1                
        self.a0 = a0
        self.b0 = b0
        
        #output saturation limits
        self.mn = mn
        self.mx = mx
        
        #Desired closed loop characteristics
        self.wn = 2.2/tr
        self.z = z
        
        #Find controller parameters:
        self.kd = (2*z*self.wn-a1)/b0
        self.kp = (self.wn**2-a0)/b0
        
        #Find DC gain of the sysetem:
        self.k = b0*self.kp/self.wn**2
        
        
        

    def update(self, ref, y):
        #Numerical Derivative
        now = 0
        if self.Tstep == live:
            now = time.time()

        #only do derivative if there is a previous value to refference
        if self.firstRun: 
            self.firstRun = False
            d = 0
        else:
            if self.Tstep == live:
                d = (y-self.yold)/(now-self.timeOld) #Calculate derivative based on 
                self.timeOld = now #Update time
            else:
                d = (y-self.yold)/self.Tstep 
        
        #save current point as the old point for next iteration
        self.yold = y

        #calculate output and return it      
        u = (ref-y)*self.kp - d*self.kd   #Multipy the error by kp, subtract kd*dy
        return(saturate(u, self.mn, self.mx))

    def showParams(self):
        print("Parameters:",
              "\nkd =\t", self.kd,
              "\nkp =\t", self.kp,
              "\nk =\t",  self.k)
    
    def showCharEquation(self):
        print("Characteristic Equation:",
               "\ns**2 + ", self.a1+self.b0*self.kd,"*s + ", self.a0 + self.b0*self.kp,
               "\ns**2 + ", 2*self.wn*self.z,"*s + ", self.wn**2,
               "\nThe equations are calculated differently, but should be equivalent."  )
        
        
    def showPoles(self):  
        alph1 = 2*self.wn*self.z
        alph0 = self.wn**2
        print("Poles:\n",
              (-1*alph1 + np.sqrt(alph1**2-4*alph0))/2, "\n",
              (-1*alph1 - np.sqrt(alph1**2-4*alph0))/2)

class PD2ndOrderADV:#PD controller using dirty derivative (pure derivative combined with a low pass filter)
    #Physical System Transfer Function:
    #       b0
    # s**2 + a1*s + a0
    
    #Desired Reponse Parameters:
    # wn = Natural Frequency
    # z = Damping Ratio
    
    
    def __init__(self, b0, a1, a0, tr, z, sigma,Tstep, mn=0, mx=0):
        #operating variables
        self.timeOld = 0            #Variable to store old time for live calculations
        self.firstRun = True        #Tells whether or not the controller is on its first run
        self.Tstep = Tstep          #time step for simulation
        self.yold = 0               #Old value for differentiator and integrators
        self.errord1 = 0            #previous iteration error value

        #Physical system transfer coefficients
        self.a1 = a1                
        self.a0 = a0
        self.b0 = b0
        
        #output saturation limits
        self.mn = mn
        self.mx = mx
        
        #Desired closed loop characteristics
        self.wn = 2.2/tr
        self.z = z
        
        #Find controller parameters:
        self.kd = (2*z*self.wn-a1)/b0
        self.kp = (self.wn**2-a0)/b0
        self.sigma = sigma
        
        #Find DC gain of the sysetem:
        self.k = b0*self.kp/self.wn**2
        
        
        

    def update(self, ref, y):
        #Numerical Derivative
        now = 0
        if self.Tstep == live:
            now = time.time()
            Ts = now - self.timeOld
            self.timeOld = now
        else:
            Ts = self.Tstep
        
        beta =  (2.0*self.sigma-Ts)/(2.0*self.sigma+Ts) 
        #only do derivative if there is a previous value to refference
        if self.firstRun: 
            self.firstRun = False
            self.d = 0
        else:
            self.d = beta * self.d + (1-beta)/Ts * (y - self.yold  + self.errord1)

        #save current point as the old point for next iteration
        self.yold = y

        #calculate output and return it
             
        u = (ref-y)*self.kp - self.d*self.kd   #Multipy the error by kp, subtract kd*dy
        return(saturate(u, self.mn, self.mx))

    def showParams(self):
        print("Parameters:",
              "\nkd =\t", self.kd,
              "\nkp =\t", self.kp,
              "\nk =\t",  self.k)
    
    def showCharEquation(self):
        print("Characteristic Equation:",
               "\ns**2 + ", self.a1+self.b0*self.kd,"*s + ", self.a0 + self.b0*self.kp,
               "\ns**2 + ", 2*self.wn*self.z,"*s + ", self.wn**2,
               "\nThe equations are calculated differently, but should be equivalent."  )
        
        
    def showPoles(self):  
        alph1 = 2*self.wn*self.z
        alph0 = self.wn**2
        print("Poles:\n",
              (-1*alph1 + np.sqrt(alph1**2-4*alph0))/2, "\n",
              (-1*alph1 - np.sqrt(alph1**2-4*alph0))/2)

class PDManual:
    def __init__(self, kp, kd, Tstep, mn = 0, mx = 0):
        self.kp = kp
        self.kd = kd
        self.Tstep = Tstep
        self.mn = mn
        self.mx = mx
        self.firstRun = True

    def update(self, ref, y):
        #Numerical Derivative
        now = 0
        if self.Tstep == live:
            now = time.time()

        #only do derivative if there is a previous value to refference
        if self.firstRun: 
            self.firstRun = False
            d = 0
        else:
            if self.Tstep == live:
                d = (y-self.yold)/(now-self.timeOld) #Calculate derivative based on 
                self.timeOld = now #Update time
            else:
                d = (y-self.yold)/self.Tstep 
        
        #save current point as the old point for next iteration
        self.yold = y

        #calculate output and return it      
        u = (ref-y)*self.kp - d*self.kd   #Multipy the error by kp, subtract kd*dy
        return(saturate(u, self.mn, self.mx))

class PID2ndOrderADV:#PD controller using dirty derivative
    #Physical System Transfer Function:
    #       b0
    # s**2 + a1*s + a0
    
    #Desired Reponse Parameters:
    # wn = Natural Frequency
    # z = Damping Ratio
    
    
    def __init__(self, b0, a1, a0,          #Physical System Parameters
                 tr, z, sigma, ki, ilim,    #Controller Parameters
                 Tstep, mn=0, mx=0):        #time step and saturation values
        #operating variables
        self.timeOld = 0            #Variable to store old time for live calculations
        self.firstRun = True        #Tells whether or not the controller is on its first run
        self.Tstep = Tstep          #time step for simulation
        self.yold = 0               #Old value for differentiator and integrators
        self.timeOld = 0            #Old value for differentiator and integrators
        self.I = integrator()       #Integral
        self.timeOld = 0            #Old value for differentiator and integrators
        self.errord1 = 0            #previous iteration error value
        
        #Physical system transfer coefficients
        self.a1 = a1                
        self.a0 = a0
        self.b0 = b0
        
        #output saturation limits
        self.mn = mn
        self.mx = mx
        
        #Desired closed loop characteristics
        self.wn = 2.2/tr
        self.z = z
        
        #Find controller parameters:
        self.kd = (2*z*self.wn-a1)/b0
        self.kp = (self.wn**2-a0)/b0
        self.sigma = sigma
        self.ki = ki #integrator
        #Find DC gain of the sysetem:
        self.k = b0*self.kp/self.wn**2
        self.ilim = ilim
        
        

    def update(self, ref, y):
        #Numerical Derivative
        now = 0
        if self.Tstep == live:
            now = time.time()
            Ts = now - self.timeOld
            self.timeOld = now
        else:
            Ts = self.Tstep
        
        beta =  (2.0*self.sigma-Ts)/(2.0*self.sigma+Ts) 
        #only do derivative if there is a previous value to refference
        if self.firstRun: 
            self.firstRun = False
            self.d = 0
        else:
            self.d = beta * self.d + (1-beta)/Ts * (y - self.yold)
        
        #Integrate
        #anti-windup
        error = ref-y
        if abs(self.d) < self.ilim: 
        # if error-self.errord1 > 0:
            # self.I = self.I + (Ts/2)*(error+ self.errord1) 
            I = self.I.update(error, self.Tstep)
        else:
            self.I.I = 0#reset integrator
        self.errord1 = (error)

        #save current point as the old point for next iteration
        self.yold = y
        
        #calculate output and return it   
        u = (ref-y)*self.kp - self.d*self.kd + self.I.I*self.ki   #Multipy the error by kp, subtract kd*dy
        return(saturate(u, self.mn, self.mx))

    def showParams(self):
        print("Parameters:",
              "\nkd =\t", self.kd,
              "\nkp =\t", self.kp,
              "\nk =\t",  self.k)
    
    def showCharEquation(self):
        print("Characteristic Equation:",
               "\ns**2 + ", self.a1+self.b0*self.kd,"*s + ", self.a0 + self.b0*self.kp,
               "\ns**2 + ", 2*self.wn*self.z,"*s + ", self.wn**2,
               "\nThe equations are calculated differently, but should be equivalent."  )
        
        
    def showPoles(self):  
        alph1 = 2*self.wn*self.z
        alph0 = self.wn**2
        print("Poles:\n",
              (-1*alph1 + np.sqrt(alph1**2-4*alph0))/2, "\n",
              (-1*alph1 - np.sqrt(alph1**2-4*alph0))/2)

class StateFeedback:
    #This controller does not do anything to update the state.
    #use an observer or derivatives outside the controller.
    def __init__(self, A, B, C, D, Poles):


        Cr = C[0][:] #Cr is negative first row of C
        #Check controlability:
        if np.linalg.matrix_rank(cnt.ctrb(A, B)) != np.size(A, 1):
            print("The system is not controlable")
        #If controlable, generate gains matrix:
        else:
            self.K = cnt.acker(A, B, Poles)
            self.kr = -1.0/(Cr @ np.linalg.inv(A-B@self.K)@B)
        print('K: ', self.K)
        print('kr: ', self.kr)

    def update(self, ref, state):
        u = -self.K @ state + self.kr * ref
        return u.item(0)

class StateFeedback_Int:
    def __init__(self, A, B, C, D, poles, Ts):
        
        #time step for integrator:
        self.Ts = Ts

        Cr = -1*C[0][:]

        #New matricies:
        A1 = np.vstack((np.hstack((A, np.zeros([np.shape(A)[1],1]))),
                       np.hstack((Cr, np.zeros([1])))))
        # print(A1)    
        B1 = np.vstack((B,
                       np.array([0])))
        
        #Integrator:
        self.I = integrator()

        #Check controlability:
        if np.linalg.matrix_rank(cnt.ctrb(A1, B1)) != np.size(A1, 1):
            print("The system is not controllable")
        else:
            #Calculate Gains:
            K1 = (cnt.acker(A1, B1, poles))
            # Separate gains
            self.ki = K1[0][-1] #* -1#np.abs(K1[0][-1])*-1 #This *-1 shouldn't need to be there...
            self.K = K1[0][0:-1]
            print('K: ', self.K)
            print('ki: ', self.ki)
        
    def update (self, ref, state):
        error = ref - state.item(0)
        I = self.I.update(error, self.Ts)
        u = -self.K @ state - self.ki *I
        return u.item(0)

class Observer:
    def __init__(self, A, B, C, D, poles, Ts, t_old = 0):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.Ts = Ts
        self.t_old = t_old

        #Compute gains
        if np.linalg.matrix_rank(cnt.ctrb(A.T, C.T)) != np.size(A.T, 1):
            print("The system is not observable")
        else:
            # place_poles returns an object with various properties.
            # The gains are accessed through .gain_matrix
            # .T transposes the matrix
            self.L = cnt.place(A.T, C.T, poles).T
        # print gains to terminal
        print('L^T: ', self.L.T)

        #Estimated State Variable:
        # self.state = np.zeros((np.shape(A)[1],1))
        self.x_hat = np.zeros((np.shape(A)[1],1))
        # print(self.x_hat)

        #Previous Force:
        self.Fd1 = 0.

    def updateObserver(self, y_m, F, xe = np.array(0), T = 0):
        
        if xe == np.array(0):
            xe = np.zeros(np.shape(self.x_hat))
        # update the observer using RK4 integration
        self.Fd1 = F

        if self.Ts == live:
            Ts = T-self.t_old
            self.t_old = T
        else:
            Ts = self.Ts     

        F1 = self.observer_f(self.x_hat, y_m, xe)
        F2 = self.observer_f(self.x_hat + Ts / 2 * F1, y_m,xe)
        F3 = self.observer_f(self.x_hat + Ts / 2 * F2, y_m,xe)
        F4 = self.observer_f(self.x_hat + Ts * F3, y_m,xe)
        self.x_hat += self.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)
        
        return self.x_hat
    
    def observer_f(self, x_hat, y_m, xe):
        # xhatdot = A*xhat + B*u + L(y-C*xhat)
        xhat_dot = self.A @ (x_hat-xe) \
                   + self.B * self.Fd1 \
                   + self.L @ (y_m - self.C @ x_hat)
        return xhat_dot

class Observer_Dist:
    def __init__(self, A, B, C, D, poles, Ts):
        
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.Ts = Ts

        Cr = -1*C # C from the plant

        B1 = np.vstack((B,
                       np.array([0])))
        print(np.shape(self.C))
        A2 = np.concatenate((
                            np.concatenate((A,B), axis = 1),
                            np.zeros((1,np.size(A,1)+1))), axis = 0)
        C2 = np.concatenate((C, np.zeros((np.size(C,0), 1))), axis = 1)

        if np.linalg.matrix_rank(cnt.ctrb(A2.T, C2.T)) != np.size(A2.T, 1):
            print("The system is not observable")
        else:
            # place_poles returns an object with various properties.
            # The gains are accessed through .gain_matrix
            # .T transposes the matrix
            self.L2 = signal.place_poles(A2.T, C2.T, poles).gain_matrix.T
        # print gains to terminal
        # print('K: ', self.K)
        # print('ki: ', self.ki)
        print('L^T: ', self.L2.T)


        #Estimated state vairalbes: 
        self.x_hat = np.zeros((np.shape(A2)[1],1))
        print("\n\n\n\n\n", self.x_hat)
        self.Fd1 = 0.
        self.L = self.L2
        self.A = A2
        self.B = B1
        self.C = C2
        print(np.shape(self.x_hat))

        print('L^T: ', self.L2.T)

    def update(self, y_m, F, xe = np.array(0)):
        if np.shape(xe) != np.shape(self.x_hat):
            xe = np.zeros(np.shape(self.x_hat))
        
        # update the observer using RK4 integration
        F1 = self.observer_f(self.x_hat, y_m,xe)
        F2 = self.observer_f(self.x_hat + self.Ts / 2 * F1, y_m, xe)
        F3 = self.observer_f(self.x_hat + self.Ts / 2 * F2, y_m, xe)
        F4 = self.observer_f(self.x_hat + self.Ts * F3, y_m, xe)
        self.x_hat += self.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)
        self.Fd1 = F
        return self.x_hat[:-1], self.x_hat[-1]

    def observer_f(self, x_hat, y_m, xe):
        # print(self.A)
        # xhatdot = A*xhat + B*u + L(y-C*xhat)
        xhat_dot = self.A @ (x_hat-xe) \
                   + self.B * self.Fd1 \
                   + self.L @ (y_m - self.C @ x_hat)
        return xhat_dot

class Loopshape_ctrl:
    #As of now, the prefilter isn't working. Integrate the prefilter into the controller.
    def __init__(self, C, F, Ts):
            self.x_C = np.zeros((C.A.shape[0], 1))
            self.x_F = np.zeros((F.A.shape[0], 1))
            self.A_C = C.A
            self.B_C = C.B
            self.C_C = C.C
            self.D_C = C.D
            self.A_F = F.A
            self.B_F = F.B
            self.C_F = F.C
            self.D_F = F.D
            self.N = 10  #number of Euler integration steps for each sample
            self.Ts = Ts
    def update_filter(self, r):
        for i in range(0, self.N):
            self.x_F = self.x_F + (self.Ts/self.N)*(
                self.A_F @ self.x_F + self.B_F * r
            )

    def update(self, r, y):
        self.update_filter(r)
        #update filter
        r_filtered = (self.C_F @ self.x_F + self.D_F * r).item(0)
        #update error
        error = r_filtered-y
        #update controller
        for i in range(0, self.N):
            self.x_C = self.x_C + (self.Ts/self.N)*(
                self.A_C @ self.x_C + self.B_C * error)
        u = (self.C_C @ self.x_C + self.D_C*error ).item(0)
        return u



#Supporting Classes:

class dirtyDerivative:
    def __init__(self,sigma,Ts):
        self.sigma = sigma
        self.Tstep = Ts
        self.firstRun = True
        

    def update(self, y):
        now = 0
        if self.Tstep == live:
            now = time.time()
            Ts = now - self.timeOld
            self.timeOld = now
        else:
            Ts = self.Tstep
        
        beta =  (2.0*self.sigma-Ts)/(2.0*self.sigma+Ts) 
        if(self.firstRun):
            self.d = 0
            self.firstRun = False
        else:
            self.d = beta * self.d + (1-beta)/Ts * (y - self.yold)

        self.yold = y
        return self.d


class integrator:
    def __init__(self):
        self.yd1 = 0.
        self.firstRun = True
        self.I = 0.
    
    def update(self, y, Ts):
        if(self.firstRun):
            self.firstRun = False
            #Don't perform the integral because there isn't anything to integrate yet.
        else:
            self.I = self.I + Ts/2*(y + self.yd1) #Run integral if it isn't on the 1st iteration
        
        self.yd1 = y #Store the current value to be used as the previous value on the next iteration

        return self.I

        
def saturate(u, mn, mx): 
    # raise ValueError("System saturated")
    if(mn == 0 and mx == 0): # Mins and maxes weren't specified
        return(u)
    elif(u < mn):
        # print("Saturation")
        return(mn)
    elif(u > mx):
        # print("Saturation")
        return(mx)
    else:
        return(u)