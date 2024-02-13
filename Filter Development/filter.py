#This file is designed to be run on a computer, not on Circuit Python. 
#Some dependencies need to be removed prior to implementation.

import numpy as np
import pandas as pd
import controlers as ctrl
import matplotlib.pyplot as plt
import time as tm
import RANSAC as RS
import random

import ClydeBldgLayout as bld

import warnings

warnings.simplefilter('ignore', np.RankWarning) #RANSAC keeps triggering warnings from numpy's polyfit program. They are usually resolved after the 2nd iteration.


#Import the dataset
dataset = pd.read_excel("Dataset 2.xlsx","Sheet5")
# print(dataset.columns)

#Relavant sensor data (constant speed model)
#Time, readings are in ns
time = np.asarray(dataset["time"],float)
time*=1e-9 #Convert to s
t0 = time[0] #Save initial time

#Sensor readings:
#  Determine the sensor configuration, display in terminal and store sensor data in arrays for analysis
print("Sensor Configuration:")
try:
    D0 = np.asarray(dataset["D0"],float)
    print("D0")
except:
    pass
try:
    D1 = np.asarray(dataset["D1"],float)
    print("D1")
except:
    pass
try:
    D2 = np.asarray(dataset["D2"],float)
    print("D2")
except:
    pass
try:
    D3 = np.asarray(dataset["D3"],float)
    print("D3")
except:
    pass
try:
    D4 = np.asarray(dataset["D4"],float)
    print("D4")
except:
    pass
try:
    D5 = np.asarray(dataset["D5"],float)
    print("D5")
except:
    pass
try:
    D6 = np.asarray(dataset["D6"],float)
    print("D6")
except:
    pass
try:
    D7 = np.asarray(dataset["D7"],float)
    print("D7")
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
allpoints = []
for i in points:
    allpoints = allpoints + i



# for j in bld.walls:
#     bld.plot_wall(j)
# for j in bld.doors:
#     bld.plot_door(j)
# for j in bld.other:
#     bld.plot_other(j)
# allpoints = np.array(allpoints)

# plt.scatter(allpoints[:,0],allpoints[:,1], s=2, color = "g")
# plt.show()



# allpoints = []
# for i in range(0,8):
#     axi = plt.subplot(9,1,i+2)

#     points_array = np.array(points[i])
    
#     allpoints.extend(points[i])
#     for j in bld.walls:
#         bld.plot_wall(j)
#     for j in bld.doors:
#         bld.plot_door(j)
#     for j in bld.other:
#         bld.plot_other(j)

#     # plt.plot([0,x[-1]],[0,0])
#     try:
#         ax.scatter(points_array[:,0],points_array[:,1], s = 2, color = "g")
#         axi.scatter(points_array[:,0],points_array[:,1], s = 2, color = "g")
#     except:
#         pass
#     axi.set_ylabel("D"+str(i))
#     axi.set_ybound(-2.5, 2)

# ax.set_ylabel("All")
# ax.set_ybound(-2.5,2)


# plt.show()



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
while len(allpoints)>20:
    #RANSAC parameters:
    threshold = .3          #Max allowable error to be considered an inlier
    inlier_thresh = 5
    outlier_thresh = 5
    ratio = .9

    RANSAC_points = []
    
    #Shift points from allpoints into RANSAC category
    l_initial = len(allpoints)
    for i in range(len(allpoints)):
        try:
            if(allpoints[l_initial-i][0]>x_current-1 and allpoints[l_initial-i][0]<x_current+1): #Can try using sort algorithm to cut time here
                RANSAC_points.append(allpoints.pop(l_initial-i))
                # print()
        except:
            pass


    #RANSAC
    for i in range(50): #time out after a large number of attempts
        if(i==48):
            print("WARNING: TOO MANY ATTEMPTS")#show warning if there have been too many iterations
        
        #Scramble RANSAC list
        random.shuffle(RANSAC_points)
        
        #Cut RANSAC list based on the ratio of points specified
        cut = int(len(RANSAC_points)*ratio)
        inliers = RANSAC_points[0:cut]
        outliers =RANSAC_points[cut:len(RANSAC_points)]
        

        n_changes = 100
        while(n_changes>0):
            
            #linear regression on inliers
            #Make inliers into an array so numpy can understand it
            tmp = np.array(inliers)
            if(len(inliers) < 1):
                break
            a = np.polyfit(tmp[:,0],tmp[:,1],1)
            

            # Process visualization
            # plt.clf()
            # try:
            #     plt.scatter(np.array(inliers)[:,0], np.array(inliers)[:,1], color = "b", label = "Inliers")
            # except:
            #     pass
            # try:
            #     plt.scatter(np.array(outliers)[:,0], np.array(outliers)[:,1], color = "r", label = "Outliers")
            # except:
            #     pass
            # plt.plot([x_current-1, x_current+1],[(x_current-1)*a[0] + a[1], (x_current+1)*a[0] + a[1]], label = "Regressed Line")
            # plt.ylim([-1.6, 1.6])
            # plt.axis("off")
            # plt.legend()
            # # plt.draw()
            # # plt.pause(.0001)
            
            #Re-sort the points based on their proximity to the regression line and count the changes made.
            n_changes = 0
            
            l_initial=len(inliers)
            for i in range(len(inliers)):
                try:
                    if abs(inliers[l_initial-i][0]*a[0]+a[1] - inliers[l_initial-i][1])>threshold:
                        n_changes = n_changes+1
                        outliers.append(inliers.pop(l_initial-i))
                except:
                    pass
            l_initial=len(outliers)
            for i in range(len(outliers)):
                try:
                    if abs(outliers[l_initial-i][0]*a[0]+a[1] - outliers[l_initial-i][1])<threshold:
                        n_changes = n_changes+1
                        inliers.append(outliers.pop(l_initial-i))
                except:
                    pass
        

        if len(inliers) > len(outliers)/2:
            #if there are a significant number of inliers, accept the segment
            #Find the segment points
            xs = np.array([min(np.array(inliers)[:,0]),max(np.array(inliers)[:,0])])
            ys = xs*a[0] + a[1]

            # [[x1,x2],[y1,y2]]
            segments.append([xs, ys]) #This line is wrong
            #remove the inliers from the RANSAC points
            RANSAC_points = outliers
            
        #if there aren't many data points left, break    
        if(len(outliers) < 10):
            break




    #Increment to the next dataset

    x_current+=2
    
    
finish = tm.time()
print("RANSAC Elapsed time: ", finish-start) 