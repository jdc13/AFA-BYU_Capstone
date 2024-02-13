#This file is designed to be run on a computer, not on Circuit Python. 
#Some dependencies need to be removed prior to implementation.

import numpy as np
import pandas as pd
import controlers as ctrl
import matplotlib.pyplot as plt

import ClydeBldgLayout as bld

import warnings

warnings.simplefilter('ignore', np.RankWarning)


dataset = pd.read_excel("Dataset 2.xlsx","Sheet1")
print(dataset.columns)

#Relavant readings (constant speed model)

#Pull time, readings are in ns
time = np.asarray(dataset["time"],float)
time*=1e-9 #Convert to s

t0 = time[0]

#Sensor readings:
#  Determine the sensor configuration, display in terminal and store in arrays for analysis
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


#Sensor relative vectors:
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

v0 = np.array([np.cos(a0),np.sin(a0)])
v1 = np.array([np.cos(a1),np.sin(a1)])
v2 = np.array([np.cos(a2),np.sin(a2)])
v3 = np.array([np.cos(a3),np.sin(a3)])
v4 = np.array([np.cos(a4),np.sin(a4)])
v5 = np.array([np.cos(a5),np.sin(a5)])
v6 = np.array([np.cos(a6),np.sin(a6)])
v7 = np.array([np.cos(a7),np.sin(a7)])




#Most simple: Constant speed: No acceleration

speed = 82/(time[-1]-time[0])
x = [] #array to store location
x.append(0)

t = [0] #array to store time
points = [[], [], [], [], [], [], [],[]] #List of lists to store sensor data

#Find 
threshold = 90
delta_thresh = 30
for i in range(1,np.size(time)):
    x.append(x[-1] + speed*(time[i]-time[i-1]))
    t.append(time[i]-time[0])
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

plt.clf()
ax = plt.subplot(8,1,1)

for j in bld.walls:
    bld.plot_wall(j)
for j in bld.doors:
    bld.plot_door(j)
for j in bld.other:
    bld.plot_other(j)


allpoints = []
for i in range(0,8):
    axi = plt.subplot(9,1,i+2)

    points_array = np.array(points[i])
    
    allpoints.extend(points[i])
    for j in bld.walls:
        bld.plot_wall(j)
    for j in bld.doors:
        bld.plot_door(j)
    for j in bld.other:
        bld.plot_other(j)

    # plt.plot([0,x[-1]],[0,0])
    try:
        ax.scatter(points_array[:,0],points_array[:,1], s = 2, color = "g")
        axi.scatter(points_array[:,0],points_array[:,1], s = 2, color = "g")
    except:
        pass
    axi.set_ylabel("D"+str(i))
    # axi.set_ybound(-2.5, 2)

ax.set_ylabel("All")
# ax.set_ybound(-2.5,2)


plt.show()

# print(allpoints)

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

segments = []
x_current = 0
while len(allpoints)>20:
    #RANSAC parameters:
    max_error = .2
    inlier_thresh = 5
    outlier_thresh = 5

    RANSAC_points = []
    
    #Shift points from allpoints into RANSAC category
    l_initial = len(allpoints)
    for i in range(len(allpoints)):
        
        try:
            if(allpoints[l_initial-i][0]>x_current-1 and allpoints[l_initial-i][0]<x_current+1):
                RANSAC_points.append(allpoints.pop(l_initial-i))
                # print()
        except:
            pass
    # print(len(RANSAC_points), "\t", len(allpoints), "\t", x_current-1, "\t", x_current + 1)
    


    #RANSAC
    inliers = []
    outliers = []
    rng = np.random.default_rng()
    for i in range(50): #time out after 100 attempts
        #randomly assign points:
        if(i==48):
            print("WARNING: TOO MANY ATTEMPTS")
        outliers =[]
        inliers = []
        # print(len(RANSAC_points))
        for element in RANSAC_points:
            if rng.random() > .9:
                inliers.append(element)
            else:
                outliers.append(element)
        # print(len(inliers), "\t", len(outliers))

        

        n_changes = 100
        while(n_changes>0):
            
            #linear regression on inliers
            tmp = np.array(inliers)
            if(len(tmp) < 1):
                break
            a = np.polyfit(tmp[:,0],tmp[:,1],1)
            # print(a,"\t",b)

            # Process visualization
            plt.clf()
            try:
                plt.scatter(np.array(inliers)[:,0], np.array(inliers)[:,1], color = "b", label = "Inliers")
            except:
                pass
            try:
                plt.scatter(np.array(outliers)[:,0], np.array(outliers)[:,1], color = "r", label = "Outliers")
            except:
                pass
            plt.plot([x_current-1, x_current+1],[(x_current-1)*a[0] + a[1], (x_current+1)*a[0] + a[1]], label = "Regressed Line")
            plt.ylim([-1.6, 1.6])
            plt.axis("off")
            plt.legend()
            plt.draw()
            plt.pause(.0001)
            n_changes = 0
            
            l_initial=len(inliers)
            threshold = .3 #max distance allowed between regressed line and inliers
            for i in range(len(inliers)):
                try:
                    if abs(inliers[l_initial-i][0]*a[0]+a[1] - inliers[l_initial-i][1])>threshold:
                        n_changes = n_changes+1
                        outliers.append(inliers.pop(l_initial-i))
                except:
                    pass
            for i in range(len(outliers)):
                try:
                    if abs(outliers[l_initial-i][0]*a[0]+a[1] - outliers[l_initial-i][1])<threshold:
                        n_changes = n_changes+1
                        inliers.append(outliers.pop(l_initial-i))
                except:
                    pass
        # [[x1,x2],[y1,y2]]
        if len(inliers) > len(outliers)/2:
            #if there are a significant number of inliers, accept the segment
            #Find the segment points
            xs = np.array([min(np.array(inliers)[:,0]),max(np.array(inliers)[:,0])])
            ys = xs*a[0] + a[1]
            segments.append([xs, ys])
            #remove the inliers from the RANSAC points
            RANSAC_points = outliers
            #reset out and inliers lists
            
        if(len(outliers) < 10):
            break






    x_current+=2
    
    
    

        
    





# # #Observer Setup:
# tr = 100
# z = .707
# wn = 2.2/tr
# dist_Pole = np.array([-1.5])
# wn*=10
# poles = np.roots(np.convolve([1, 2*z*wn, wn**2], np.poly(dist_Pole)))
# A = np.array([[0,1,0],
#               [0,0,1],
#               [0,0,0]])
# B = np.array([[0],[0],[0]])
# C = np.array([[1,0,0]])
# D = np.array([[0,0,0]])

# filter = ctrl.Observer(A, B, C, D, poles, Ts = .001, t_old = t0)
# # filter.x_hat[1] = 80/(time[-1]-time[0])
# print(filter.x_hat)



# for i in range(np.size(Ax)):
#     ym = Ax[i]
#     F = 0
#     T = time[i]
#     t.append(time[i])
#     obs = (filter.updateObserver(y_m=ym, F=F, T=T))
#     x.append(obs.item(0))
#     x_dot.append(obs.item(1))
#     x_dd.append(obs.item(2))
#     plt.clf()
#     plt.plot(t,x, label = "position")
#     plt.plot(t, x_dot, label = "speed")
#     plt.plot(t, x_dd, label = "acceleration")
#     plt.legend()
#     plt.draw()
#     plt.pause(0.01)

# print(np.size(x))
# # plt.plot(x)
# plt.show()
