# '''This file contains the main functions to recieve data from the sensor array
# This file is not compatible with python 3.12. Use 3.11'''

#Import dependencies
import serial
#pip install pyserial
import numpy as np
import matplotlib.pyplot as plt

import keyboard as key
import pandas as pd
import os
import datetime as date
#import the RANSAC code
import RANSAC as RS
ser = serial.Serial("COM17", 115200, timeout=3)

#Deliminators:
delim_coord = "c"
delim_point = "p"
delim_line = "l"


#Parameters:

print("Starting")
#RANSAC parameters          Best Tested Value   #Explanation
threshold_r = .5            #.5m                 Threshold used to define inliers
ratio = .8                  #.8                 Initial ratio of inliers to outliers in the data
gap = 1                     #1m               Standard deviation between n points to characterize a gap
acceptance_ratio = .5       #.5                 min Number of inliers/outliers to accept a line
leftovers = 40              #40                 Maximum number of outliers in the final iteration
x_step = 2                 #10m                How much to increment the RANSAC window
n = 4                       #4                  How many points to evaluate when trying to find a gap

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
        pt = entry.split(delim_coord) #The point coordinates are split by a comma
        points.append(np.array([float(pt[0]), float(pt[1])])) #Parse the coordinates into floats and save them
    global all_points
    all_points = all_points + points
    return points

string =  "r"
ser.write(string.encode('utf-8'))
ser.readline() #remove the first line, which may have data from before the soft reset
while True:
    #Wait for data:
    # print(ser.in_waiting)
    while(ser.in_waiting < 16):
        pass
    # print("Have new data")
    # print(ser.in_waiting)
    bs = ser.readline().decode("utf-8")
    # print(bs)
    if len(bs) > 8:
        lines = bs.split(delim_line)

        line_r = lines[0]
        line_l = lines[1]
        # print(line_l)
        # print(line_r)

        right_new = []
        left_new = []
        right_new = right_new + parse_points(line_r)
        left_new = left_new + parse_points(line_l)

        all_points = all_points + right_new + left_new


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
                #Reset the old points
                right_bank = []
                left_bank = []

                #Increment window
                x_current += x_step
                
                #Clear the figure and plot segments
                plt.clf()
                for i in segments:
                    RS.plot_segment(i)
                ap = np.array(all_points)
                plt.scatter(ap[:,0], ap[:,1])
                plt.draw()
                plt.pause(.01)
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
for i in segments:
    RS.plot_segment(i)
ap = np.array(all_points)
plt.scatter(ap[:,0], ap[:,1])

fig = plt.gcf()

fig.savefig(test_dir + "\\figure.pdf",format="pdf" )

plt.show()






















# import bluetooth 
# #For installation instructions: https://pybluez.readthedocs.io/en/latest/install.html
# import os
# #Clear the screen to see only code from this attempt
# # os.system("cls")

# # target_name = "My Phone"
# target_name = ""
# target_address = None

# nearby_devices = bluetooth.discover_devices()
# # print(nearby_devices)

# # print(nearby_devices)
# # bluetooth.lookup_name
# # (bluetooth.lookup_name('0C:8B:95:94:9F:2E'))
# for bdaddr in nearby_devices:
#     # print("Device: ", bluetooth.lookup_name( bdaddr ))
#     if target_name == bluetooth.lookup_name( bdaddr ):
        
#         target_address = bdaddr
#         break

# if target_address is not None:
#     print ("\nfound target bluetooth device with address ", target_address)
# else:
#     print ("\ncould not find target bluetooth device nearby")



# print(bluetooth.find_service())#name = "", uuid="4fafc201-1fb5-459e-8fcc-c5c9c331914b")
# # target_name = "BYU/AFA Capstone Server"
# # target_address = None

# # nearby_devices = bluetooth.discover_devices()

# # print(nearby_devices)

# # for bdaddr in nearby_devices:
# #     if target_name == bluetooth.lookup_name( bdaddr ):
# #         target_address = bdaddr
# #         break

# # print(target_address)
# # # I wrote this without testing anything, so there is probably a lot of errors that need to be worked through.

# # #Import dependencies
# # import numpy as np
# # import requests
# # import matplotlib.pyplot as plt
# # import time

# # #import the RANSAC code
# # import RANSAC as RS

# # #Parameters:
# # x_step = 10# step to move through the code.

# # print("Starting")
# # #RANSAC parameters          Best Tested Value   #Explanation
# # threshold_r = 1             #1m                 #maximum distance between regressed line and inliers
# # ratio = 7                  #.8                 #Ratio of inliers to outliers in the initial run
# # gap = .2                 #.01m               #minimum gap between points to be considered a gap in the wall
# # acceptance_ratio = .9       #.7                 #Minimum ratio of inliers to outliers to accept a line
# # leftovers = 10              #10                 #Maximum number of outliers to complete the RANSAC run
# # x_step = 30                 #20                 #Step taken for the window.

# # x_current = x_step
# # #Create empty lists for the sensor banks
# # right_bank = []
# # left_bank = []

# # #Create empty lists for RANSAC output
# # segments = []


# # def parse_points(line):
# #     '''Take the raw line from a request and convert it into a list of points'''
# #     #Decode:
# #     line = line.decode("utf-8")

# #     #Separate the lines into lists of points (Still strings)
# #     line = line.split("\t")[0:-1]#We want to drop the last entry since it is empty (see Arduino Code)

# #     #Create an empty list to store the points to return

# #     points = []
# #     #Parse the strings into points
# #     for entry in line:
# #         pt = entry.split(",") #The point coordinates are split by a comma
# #         points.append(np.array([float(pt[0]), float(pt[1])])) #Parse the coordinates into floats and save them

# #     return points


# # while(1):
# #     try:
# #         print("Trying")
# #         #Pull Data from the server
# #         r = requests.get("http://192.168.4.1")
# #         print("1")      
# #         # print(r)
# #         #Save the two lines individually as separate sensor banks
# #         i = 0
# #         lines = []
# #         for line in r.iter_lines():
# #             # print("Recieved points")
# #             lines.append(line)
# #             # print(line)
# #         print("2")
# #         line_r = lines[0]
# #         line_l = lines[1]
# #         # print(lines)
# #         #Create empty lists to store data
# #         right_new = []
# #         left_new = []
# #         print(line_r)
# #         #parse the lines into lists of points and add them to the new lists
# #         right_new = right_new + (parse_points(line_r))
# #         left_new = left_new + parse_points(line_l)
# #         print("3")
# #         #Sort the new points
# #         right_new = RS.sort_points(right_new)
# #         left_new = RS.sort_points(left_new)
# #         print(right_new)
# #         #If the smallest of the new points is larger than the current window, run RANSAC on the old points
# #         if (right_new[0][0] > x_current) and (left_new[0][0] > x_current): 
# #             segments = segments +  RS.RANSAC_Segments_2D(right_bank,
# #                                                         threshold_r,
# #                                                         ratio,
# #                                                         gap,
# #                                                         acceptance_ratio,
# #                                                         leftovers)
# #             segments = segments +  RS.RANSAC_Segments_2D(left_bank,
# #                                                         threshold_r,
# #                                                         ratio,
# #                                                         gap,
# #                                                         acceptance_ratio,
# #                                                         leftovers)
# #             #Reset the old points
# #             right_bank = []
# #             left_bank = []
# #             x_current += x_step
            
# #             #Clear the figure and plot segments
# #             plt.clf()
# #             for i in segments:
# #                 RS.plot_segment(i)

# #             plt.draw()
# #             plt.pause(.01)
# #             #endif

# #         #After RANSAC, or if RANSAC wasn't ready, add the new points to the sensor banks
# #         right_bank = right_bank + right_new
# #         left_bank = left_bank + left_new


# #     except Exception as error:
# #         #Try statement is to prevent the code from crashing if there is a connection problem, or no data
# #         #Don't need to do any exception handling
# #         #Can print the exception for debug purposes
# #         # print(error)
# #         print("Failed")
# #         pass
    
# #     #Pause momentarilly to allow the server to collect new data.
# #     time.sleep(.1)    