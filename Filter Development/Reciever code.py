'''This file contains the main functions to recieve data from the sensor array'''

# I wrote this without testing anything, so there is probably a lot of errors that need to be worked through.

#Import dependencies
import numpy as np
import requests
import matplotlib.pyplot as plt

#import the RANSAC code
import RANSAC as RS

#Parameters:
x_step = 10# step to move through the code.


#RANSAC parameters          Best Tested Value   #Explanation
threshold_r = 1             #1m                 #maximum distance between regressed line and inliers
ratio = .8                  #.8                 #Ratio of inliers to outliers in the initial run
gap = .01                   #.01m               #minimum gap between points to be considered a gap in the wall
acceptance_ratio = .7       #.7                 #Minimum ratio of inliers to outliers to accept a line
leftovers = 10              #10                 #Maximum number of outliers to complete the RANSAC run
x_step = 20                 #20                 #Step taken for the window.

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
        points.append([float(pt[0], float(pt[1]))]) #Parse the coordinates into floats and save them

    return points


while(1):
    r = requests.get("http://192.168.4.1", stream=True)
    right_new = []
    left_new = []
    try:
        #Save the two lines individually as separate sensor banks
        line_r = r.iter_lines()[0]
        line_l = r.iter_lines()[1]


        #parse the lines into lists of points.
        right_new.append(parse_points(line_r))
        left_new.append(parse_points(line_l))
    except:
        #Don't kill the code if there is a connection issue.
        pass

    #Sort the new points
    right_new = RS.sort_points(right_new)
    left_new = RS.sort_points(left_new)
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

    #After RANSAC, or if RANSAC wasn't ready, add the new points to the sensor banks
    right_bank = right_bank + right_new
    left_bank = left_bank + left_new

    for i in segments:
        RS.plot_segment(i)

    plt.draw()
    plt.pause(.01)
