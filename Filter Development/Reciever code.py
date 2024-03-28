'''This file contains the main functions to recieve data from the sensor array'''

# I wrote this without testing anything, so there is probably a lot of errors that need to be worked through.

#Import dependencies
import numpy as np
import requests
import matplotlib.pyplot as plt
import time

#import the RANSAC code
import RANSAC as RS

#Parameters:
x_step = 10# step to move through the code.

print("Starting")
#RANSAC parameters          Best Tested Value   #Explanation
threshold_r = 1             #1m                 #maximum distance between regressed line and inliers
ratio = 7                  #.8                 #Ratio of inliers to outliers in the initial run
gap = .2                 #.01m               #minimum gap between points to be considered a gap in the wall
acceptance_ratio = .9       #.7                 #Minimum ratio of inliers to outliers to accept a line
leftovers = 10              #10                 #Maximum number of outliers to complete the RANSAC run
x_step = 30                 #20                 #Step taken for the window.

x_current = x_step
#Create empty lists for the sensor banks
right_bank = []
left_bank = []

#Create empty lists for RANSAC output
segments = []


def parse_points(line):
    '''Take the raw line from a request and convert it into a list of points'''
    #Decode:
    line = line.decode("utf-8")

    #Separate the lines into lists of points (Still strings)
    line = line.split("\t")[0:-1]#We want to drop the last entry since it is empty (see Arduino Code)

    #Create an empty list to store the points to return

    points = []
    #Parse the strings into points
    for entry in line:
        pt = entry.split(",") #The point coordinates are split by a comma
        points.append(np.array([float(pt[0]), float(pt[1])])) #Parse the coordinates into floats and save them

    return points


while(1):
    try:
        print("Trying")
        #Pull Data from the server
        r = requests.get("http://192.168.4.1")
        print("1")      
        # print(r)
        #Save the two lines individually as separate sensor banks
        i = 0
        lines = []
        for line in r.iter_lines():
            # print("Recieved points")
            lines.append(line)
            # print(line)
        print("2")
        line_r = lines[0]
        line_l = lines[1]
        # print(lines)
        #Create empty lists to store data
        right_new = []
        left_new = []
        print(line_r)
        #parse the lines into lists of points and add them to the new lists
        right_new = right_new + (parse_points(line_r))
        left_new = left_new + parse_points(line_l)
        print("3")
        #Sort the new points
        right_new = RS.sort_points(right_new)
        left_new = RS.sort_points(left_new)
        print(right_new)
        #If the smallest of the new points is larger than the current window, run RANSAC on the old points
        if (right_new[0][0] > x_current) and (left_new[0][0] > x_current): 
            segments = segments +  RS.RANSAC_Segments_2D(right_bank,
                                                        threshold_r,
                                                        ratio,
                                                        gap,
                                                        acceptance_ratio,
                                                        leftovers)
            segments = segments +  RS.RANSAC_Segments_2D(left_bank,
                                                        threshold_r,
                                                        ratio,
                                                        gap,
                                                        acceptance_ratio,
                                                        leftovers)
            #Reset the old points
            right_bank = []
            left_bank = []
            x_current += x_step
            
            #Clear the figure and plot segments
            plt.clf()
            for i in segments:
                RS.plot_segment(i)

            plt.draw()
            plt.pause(.01)
            #endif

        #After RANSAC, or if RANSAC wasn't ready, add the new points to the sensor banks
        right_bank = right_bank + right_new
        left_bank = left_bank + left_new


    except Exception as error:
        #Try statement is to prevent the code from crashing if there is a connection problem, or no data
        #Don't need to do any exception handling
        #Can print the exception for debug purposes
        # print(error)
        print("Failed")
        pass
    
    #Pause momentarilly to allow the server to collect new data.
    time.sleep(.1)    