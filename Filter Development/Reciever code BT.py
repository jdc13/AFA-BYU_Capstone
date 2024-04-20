# '''This file contains the main functions to recieve data from the sensor array
# This file is not compatible with python 3.12. Use 3.11'''

#Import dependencies
import serial #Communication with the sensors pip install pyserial
import numpy as np #Linear algebra and data management
import matplotlib.pyplot as plt #

import keyboard as key
import pandas as pd
import os
import datetime as date
#import the RANSAC code
import RANSAC as RS

from Parameters import *
ser = serial.Serial("COM12", 115200, timeout=3)

#Deliminators:
#Data is transmitted in the form ###c###p###c###l###c###p###c###
delim_coord = "c"
delim_point = "p"
delim_line = "l"




print("Starting")

x_current = x_step

#Create empty lists for the sensor banks
right_bank = []
left_bank = []

#Empty list for all of the data
all_points = []
#Create empty lists for RANSAC output
segments = []



def parse_points(line):
    '''Take the raw line from a request and convert it into a list of points'''
    #Separate the lines into lists of points (Still strings)
    line = line.split(delim_point)[0:-1]#We want to drop the last entry since it is empty (see Arduino Code)

    #Create an empty list to store the points to return
    points = []

    #Parse the strings into points
    for entry in line:
        pt = entry.split(delim_coord)
        if abs(float(pt[1])) > .28:
            points.append(np.array([float(pt[0]), float(pt[1])])) #Parse the coordinates into floats and save them
    
    #Add the new points to the full list
    global all_points
    all_points = all_points + points

    #Remove points in the center band and outside the valid zone.
    len_original = len(points)
    for i in range(len(points)):
        if(abs(points[len_original-i-1][1]) < .28 or abs(points[len_original-i-1][1]) > 2.15):
            points.pop(len_original-i-1)
    return points


#Send the set speed to the sensors
string =  str(speed)
ser.write(string.encode('utf-8'))

#remove a few lines, which may have data from before the soft reset
ser.readline() 
bs = ser.readline().decode("utf-8")
bs = ser.readline().decode("utf-8")

while True:
    #Wait for data:
    while(ser.in_waiting < 8):
        pass
    bs = ser.readline().decode("utf-8")

    if len(bs) > 8: #Double check to make sure there is enough data
        lines = bs.split(delim_line) #Split the sensor banks into lines

        line_r = lines[0]
        line_l = lines[1]

        #Empty lists for new points
        right_new = []
        left_new = []

        #Parse the points
        try:
            right_new = right_new + parse_points(line_r)
            left_new = left_new + parse_points(line_l)
        except:
            pass

        #Add the points to the list for plotting
        all_points = all_points + right_new + left_new

        #Sort the points by their x coordinate to check for new data
        right_new = RS.sort_points(right_new)
        left_new = RS.sort_points(left_new)

        if(len(right_new) > 1 and len(left_new)>1):
            #If the smallest of the new points is larger than the current window, run RANSAC on the old points
            if (right_new[0][0] > x_current) and (left_new[0][0] > x_current): 
                segments = segments +  RS.RANSAC_Segments_2D(right_bank,
                                                            threshold_r,
                                                            ratio,
                                                            gap,
                                                            acceptance_ratio,
                                                            leftovers,
                                                            n)
                segments = segments +  RS.RANSAC_Segments_2D(left_bank,
                                                            threshold_r,
                                                            ratio,
                                                            gap,
                                                            acceptance_ratio,
                                                            leftovers,
                                                            n)
                

                #Increment window
                x_current += x_step
                
                #Clear the figure and plot segments
                plt.clf()
                # plt.axes("off")
                #Arrays of current points
                rb = np.array(right_bank)
                lb = np.array(left_bank)
                
                for i in segments:
                    RS.plot_segment(i)
                ap = np.array(all_points)
                plt.scatter(ap[:,1], ap[:,0])
                plt.scatter(rb[:,1],rb[:,0])
                plt.scatter(lb[:,1],lb[:,0])
                plt.draw()
                plt.pause(.01)

                #Reset the old points
                right_bank = []
                left_bank = []
        #endif
            
        #After RANSAC, or if RANSAC wasn't ready, add new points to the sensor banks
        
        right_bank = right_bank + right_new
        left_bank = left_bank + left_new

    if(key.is_pressed("a")):
        break


print("Stopped")
#Save the data
now = date.datetime.now()
test_dir = os.getcwd() + "\\Tests\\ " + str(now.month) + "-" + str(now.day) + "-" + str(now.year) + " " + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second)
os.mkdir(test_dir)

segments_df = pd.DataFrame(columns=["x1", "y1", "x2", "y2"])
for s in segments:
    segments_df.loc[len(segments_df)] = list(np.concatenate(s,axis=0), )
segments_df.to_csv(test_dir+"\\Segments.csv")

point_df = pd.DataFrame(columns = ["x", "y"])

for p in all_points:
    point_df.loc[len(point_df)] = list(p)

point_df.to_csv(test_dir+"\\Points.csv")

#Save the figure as a svg

#Clear the figure and plot any stragglers
plt.clf()
# plt.axes("off")
for i in segments:
    RS.plot_segment(i)
ap = np.array(all_points)
plt.scatter(ap[:,1], ap[:,0])

fig = plt.gcf()

fig.savefig(test_dir + "\\figure.pdf",format="pdf" )

plt.show()