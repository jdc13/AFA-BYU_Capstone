#This file is designed to be run on a computer, not on Circuit Python. 
#Some dependencies need to be removed prior to implementation.

import numpy as np
import pandas as pd
import controlers as ctrl
import matplotlib.pyplot as plt
import time as tm
import RANSAC as RS
import warnings

warnings.filterwarnings("ignore")

import ClydeBldgLayout as bld

#Import the dataset
dataset = pd.read_excel("Dataset 2.xlsx","Sheet1")

#RANSAC parameters          Best Tested Value
threshold_r = 1             #1m
ratio = .8                  #.8
gap = .01                   #.01m
acceptance_ratio = .7       #.7
leftovers = 10              #10
x_step = 20                 #20

#Time, readings are in ns
time = np.asarray(dataset["time"],float)
time*=1e-9 #Convert to s
t0 = time[0] #Save initial time

#Sensor readings:
#  Determine the sensor configuration, display in terminal and store sensor data in arrays for analysis
print("Sensor Configuration:")
try:
    D0 = np.asarray(dataset["D0"],float)
    print("\tD0")
except:
    pass
try:
    D1 = np.asarray(dataset["D1"],float)
    print("\tD1")
except:
    pass
try:
    D2 = np.asarray(dataset["D2"],float)
    print("\tD2")
except:
    pass
try:
    D3 = np.asarray(dataset["D3"],float)
    print("\tD3")
except:
    pass
try:
    D4 = np.asarray(dataset["D4"],float)
    print("\tD4")
except:
    pass
try:
    D5 = np.asarray(dataset["D5"],float)
    print("\tD5")
except:
    pass
try:
    D6 = np.asarray(dataset["D6"],float)
    print("\tD6")
except:
    pass
try:
    D7 = np.asarray(dataset["D7"],float)
    print("\tD7")
except:
    pass


#Angles that the sensors are pointing relative to the module
def deg2rad(angle):
    return angle * np.pi/180
a0 = deg2rad(45)
a1 = deg2rad(60)
a2 = deg2rad(90)
a3 = deg2rad(120)
a4 = deg2rad(-120)
a5 = deg2rad(-90)
a6 = deg2rad(-60)
a7 = deg2rad(-45)

#Unit vectors for the sensor orientations
v0 = np.array([np.cos(a0),np.sin(a0)])
v1 = np.array([np.cos(a1),np.sin(a1)])
v2 = np.array([np.cos(a2),np.sin(a2)])
v3 = np.array([np.cos(a3),np.sin(a3)])
v4 = np.array([np.cos(a4),np.sin(a4)])
v5 = np.array([np.cos(a5),np.sin(a5)])
v6 = np.array([np.cos(a6),np.sin(a6)])
v7 = np.array([np.cos(a7),np.sin(a7)])

#Most simple: Constant speed: No acceleration
#Find the constant speed based on the known distance traveled vs time. In the final product, this will be a constant
speed = 82/(time[-1]-time[0])
x = [] #array to store location
x.append(0)

t = [0] #array to store time
points = [[], [], [], [], [], [], [],[]] #List of lists to store sensor data


#Two variables for eliminating out of range sensor readings
threshold = 90 #Minimum distance walls must be
delta_thresh = 30 #Maximum variation between sensor readings


for i in range(1,np.size(time)):
    #Estimate and store position
    x.append(x[-1] + speed*(time[i]-time[i-1]))
    #Calculate and store elapsed time
    t.append(time[i]-time[0])

    #Convert sensor readings to data points, eliminating the out of range measurements
    #In try statements to allow sensor configurations to change without having to modify code
    try:
        if(D0[i] > threshold and abs(D0[i-1]-D0[i]) < delta_thresh):
            points[0].append(D0[i]*v0*1e-2+ np.array([x[i],0])) #Lots of errors
    except:
        pass
    try:
        if(D1[i] > threshold and abs(D1[i-1]-D1[i]) < delta_thresh):
            points[1].append(D1[i]*v1*1e-2 + np.array([x[i],0])) #Fairly good data
    except:
        pass
    try:
        if(D2[i] > threshold and abs(D2[i-1]-D2[i]) < delta_thresh):
            points[2].append(D2[i]*v3*1e-2 + np.array([x[i],0])) #decent
    except:
        pass
    try:
        if(D3[i] > threshold and abs(D3[i-1]-D3[i]) < delta_thresh):
            points[3].append(D3[i]*v3*1e-2 + np.array([x[i],0])) #decent
    except:
        pass
    try:
        if(D4[i] > threshold+10 and abs(D4[i-1]-D4[i]) < delta_thresh):
            points[4].append(D4[i]*v4*1e-2 + np.array([x[i],0])) #Decent
    except:
        pass
    try:
        if(D5[i] > threshold+10 and abs(D5[i-1]-D5[i]) < delta_thresh):
            points[5].append(D5[i]*v4*1e-2 + np.array([x[i],0])) #Decent
    except:
        pass
    try:
        if(D6[i] > threshold+20 and abs(D6[i-1]-D6[i]) < delta_thresh):
            points[6].append(D6[i]*v6*1e-2 + np.array([x[i],0])) #Decent
    except:
        pass
    try:
        if(D7[i] > threshold+10 and abs(D7[i-1]-D7[i]) < delta_thresh):
            points[7].append(D7[i]*v7*1e-2 + np.array([x[i],0])) #lots of errors
    except:
        pass


#Show the resulting sensor data superimposed on the hallway
#Display all sensor data together, and each sensor's data individually
plt.clf()
# ax = plt.subplot(9,1,1)
left_bank  = RS.sort_points(points[0] + points[1] + points[2] + points[3])
right_bank = RS.sort_points(points[4] + points[5] + points[6] + points[7])


allpoints = left_bank + right_bank

#sudo code for finding wall segments:
#Test in 1m blocks measured in x
#RANSAC to get a line
#-split into random inlier and outlier groups
#-linear regression on inliers
#-Sort inliers and outliers based on value errors, counting changes
#-when changes = 0 count members of inliers
#-if number of inliers is greater than a threshold accept the model
#-if number of outliers is under a threshold end process, else store outliers for next round
#-Return the x values for the largest and smallest x values in the inlier group

#Time how long RANSAC algorithm takes
start = tm.time()

#List of regressed segments
segments = []

#Current value of X to base the "window" around
x_current = 0

#Allow some weirdness in not all data points being removed
while len(right_bank)>20:
    RANSAC_points = []
    
    #Shift points from right_bank into RANSAC category
    l_initial = len(right_bank)
    for i in range(len(right_bank)):
        try:
            if(right_bank[l_initial-i][0]>x_current-x_step/2 
               and 
               right_bank[l_initial-i][0]<x_current+x_step/2): #Can try using sort algorithm to cut time here
                RANSAC_points.append(right_bank.pop(l_initial-i))
                # print()
        except:
            pass

    segments = segments + RS.RANSAC_Segments_2D(RANSAC_points, 
                                                threshold_r,
                                                ratio,
                                                gap,
                                                acceptance_ratio,
                                                leftovers)

    x_current+=x_step
    
x_current = 0

#Allow some weirdness in not all data points being removed
while len(left_bank)>20:
    RANSAC_points = []
    
    #Shift points from right_bank into RANSAC category
    l_initial = len(left_bank)
    for i in range(len(left_bank)):
        try:
            if(left_bank[l_initial-i][0]>x_current-x_step/2 
               and 
               left_bank[l_initial-i][0]<x_current+x_step/2): #Can try using sort algorithm to cut time here
                RANSAC_points.append(left_bank.pop(l_initial-i))
                # print()
        except:
            pass
    segments_r = segments
    segments_l = RS.RANSAC_Segments_2D(RANSAC_points, 
                                        threshold_r,
                                        ratio,
                                        gap ,
                                        acceptance_ratio,
                                        leftovers)
    segments = segments_r + segments_l

    x_current+=x_step


finish = tm.time()

allpoints = np.array(allpoints)
plt.scatter(allpoints[:,0],allpoints[:,1], s=2, color = "g")
for i in segments:
    RS.plot_segment(i)

for i in bld.walls:
    bld.plot_wall(i)
for i in bld.other:
    bld.plot_wall(i)
for i in bld.doors:
    bld.plot_door(i)


# ax.set_ybound(-2.5,2)
plt.ylim([-2.5, 2])

plt.draw()
plt.pause(.01)


#Quantitative Evaluation

left_bank  = RS.sort_points(points[0] + points[1] + points[2] + points[3])
right_bank = RS.sort_points(points[4] + points[5] + points[6] + points[7])

walls = bld.walls + bld.doors + bld.other

def dist2walls(point):
    dist = 1e10 #set initial distance to something stupid high so that the first reading is kept
    for w in walls:
        # print(round(w[0][0], 3), "\t", round(w[1][0],3))
        if point[0] > w[0][0] and point[0] < w[1][0] \
            or\
            point[0] > w[1][0] and point[0] < w[0][0]:#if the point is within the boundary of the wall(in x direction) Check for both orientations of the wall
            global m
            m = (w[1][1]-w[0][1])/(w[1][0]-w[0][0]) #Find slope of wall
            dist_current = (point[1]- (m*(point[0]-w[0][0]) + w[0][1])).item(0) #distance is the perpindicular distance to the wall
            if abs(dist_current)<abs(dist): #if this is smaller than other checked distances, save it.
                dist = dist_current
        elif point[1] > w[0][1] and point[1] < w[1][1]\
             or\
             point[1] > w[1][1] and point[1] < w[0][1]: #if the point is within the boundary of the wall in y direction, checking for both orientations of the wall
            #Reverse x and y in point slope
            m = (w[1][0]-w[0][0])/(w[1][1]-w[0][1]) #Find slope of wall
            dist_current = (point[0]- (m*(point[1]-w[0][1]) + w[0][0])).item(0) #distance is the perpindicular distance to the wall
            if abs(dist_current)<abs(dist): #if this is smaller than other checked distances, save it.
                dist = dist_current
        else: #the point is not in any boundary of the wall. Check to the nearest corner
            dist_current = np.sqrt((point[0]-w[0][0])**2 + (point[1]-w[0][1]**2))#Find the distance to one corner of the wall.
            if abs(dist_current)<abs(dist): #if this is smaller than other checked distances, save it.
                dist = dist_current
            dist_current = np.sqrt((point[0]-w[1][0])**2 + (point[1]-w[1][1]**2))#Find the distance to the other corner of the wall.
            if abs(dist_current)<abs(dist): #if this is smaller than other checked distances, save it.
                dist = dist_current
    return [dist, m]


#find rms of the distances for the right bank:
#find distance and square it (r)
print("\nRaw Data Error:")
rms = 0
for i in right_bank:
    rms += dist2walls(i)[0]**2
#Find the mean of the squares (m)
rms = rms/len(right_bank)
#take the square root of the mean (s)
rms = np.sqrt(rms)
print("\tRight Bank RMS error:\t", round(rms,5), "m")
rms_right = rms

rms = 0
for i in left_bank:
    rms += dist2walls(i)[0]**2
#Find the mean of the squares (m)
rms = rms/len(right_bank)
#take the square root of the mean (s)
rms = np.sqrt(rms)
print("\tLeft Bank RMS error:\t", round(rms, 5), "m")
rms_left = rms


print("\nRANSAC Performance:")
print("\tElapsed time:\t", round(finish-start,5)) 

#RANSAC output error evaluation:
#approach:
#Calculate Bias of the line segments based on the mean distance to the walls over the line segment
#Find average and standard deviation of the error in the angle between the wall and the RANSAC regressed segments
print("\tRight Bank Output Error")

right_bias = []
right_slope_error = []

for s in segments_r:
    center = [(s[0][0]+s[1][0])/2, (s[0][1] + s[1][1])/2]
    dist, slope = dist2walls(center)
    if(s[1][0]-s[0][0]) != 0:
        # m_s = 1000
        m_s = (s[1][1]-s[0][1])/(s[1][0]-s[0][0]) #Find slope of wall
        right_slope_error.append(m_s-slope)
    
    right_bias.append(dist)
    
# print(right_slope_error)
right_bias = np.mean(np.array(right_bias))
right_slope_error = np.mean(np.array(right_slope_error))

print("\t\tBias:\t", round(right_bias, 5), " m")
print("\t\tSlope:\t", round(np.tan(right_slope_error)*180/np.pi, 5), "degrees")

print("\tLeft Bank Output Error")

left_bias = []
left_slope_error = []

for s in segments_l:
    center = [(s[0][0]+s[1][0])/2, (s[0][1] + s[1][1])/2]
    dist, slope = dist2walls(center)
    if(s[1][0]-s[0][0]) != 0:
        # m_s = 1000
        m_s = (s[1][1]-s[0][1])/(s[1][0]-s[0][0]) #Find slope of wall
        left_slope_error.append(m_s-slope)
    
    left_bias.append(dist)
    
# print(right_slope_error)
left_bias = np.mean(np.array(left_bias))
left_slope_error = np.mean(np.array(left_slope_error))

print("\t\tBias:\t", round(left_bias, 5), " m")
print("\t\tSlope:\t", round(np.tan(left_slope_error)*180/np.pi, 5), "degrees")
    

plt.waitforbuttonpress()
