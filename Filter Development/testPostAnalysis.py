import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

import RANSAC as RS

test = "3"


#RANSAC parameters          Best Tested Value   #Explanation
threshold_r = .08            #.5m          Threshold used to define inliers
ratio = .8                  #.8            Initial ratio of inliers to outliers in the data
gap = .2                     #1m            Standard deviation of distance between n points to characterize a gap
acceptance_ratio = .6       #.5            min Number of inliers/outliers to accept a line
leftovers = 4              #40             Maximum number of outliers in the final iteration
x_step = 5               #10m            How much to increment the RANSAC window
n = 4                      #4             How many points to evaluate when trying to find a gap


datasets = {"1": " 4-10-2024 9-9-12",
            "2": " 4-10-2024 9-10-29",
            "3": " 4-10-2024 9-12-1",
            "4": " 4-10-2024 9-13-47",
            "5": " 4-10-2024 9-21-7",
            "6": " 4-10-2024 9-21-23",
            "7": " 4-10-2024 9-21-51"}

cutoff = {"2": 45.5,
          "3": 42.6,
          "4": 45,
          "5": 0,
          "6": 0,
          "7": 60}

test_dir = os.getcwd() + "\\Tests\\"


segments = pd.read_csv(test_dir  + datasets[test] + "\\Segments.csv")

points = pd.read_csv(test_dir + datasets[test] + "\\Points.csv")


#Plot the points for detailed review
# for i in range(len(segments)):
#     segment = segments.loc[i]
#     if segment["x1"] < 400:
#         s = np.array([[segment["x1"], segment["y1"]],
#                     [segment["x2"], segment["y2"]]])
#         RS.plot_segment(s)
points.columns = ["ind", "x", "y"]

points = points.drop(columns="ind")
# plt.scatter(points['x'], points['y'])


#Convert points dataframe to a list
points = np.asarray(points)
points = list(points)
#sort points
points = RS.sort_points(points)


#Remove points after the cutoff
for i in range(len(points)):
    if points[i][0] > cutoff[test]:
        points = points[0:i-1]
        break


len_original = len(points)
for i in range(len(points)):
    if(abs(points[len_original-i-1][1]) < .28):
        points.pop(len_original-i-1)




#Separate banks:
left_bank = []
right_bank = []
for p in points:
    if p[1] > 0:
        # print(p[0])
        left_bank.append(p)
    else:
        right_bank.append(p)


tmp = np.asanyarray(left_bank)
plt.scatter(tmp[:,0], tmp[:,1])
tmp = np.asanyarray(right_bank)
plt.scatter(tmp[:,0], tmp[:,1])

#Run RANSAC on filtered points
position = 0
tmp = np.asanyarray(points)
segments = []
while(len(right_bank) + len(left_bank) > 1):
    right = []
    left = []
    # print(len(right_bank), "\t", len(left_bank))
    if len(right_bank) < 50:
        right = right_bank
        right_bank = []
    
    else:
        for i in range(len(right_bank)-1):
            if right_bank[i][0] > position:
                right = right_bank[0:i]
                right_bank = right_bank[i+1:-1]
                break
    if(len(left_bank) < 50):
        left = left_bank
        left_bank = []
    else:
        for i in range(len(left_bank)-1):
            if left_bank[i][0] > position:
                left = left_bank[0:i]
                left_bank = left_bank[i+1:-1]
                break

    segments = segments + RS.RANSAC_Segments_2D(right,
                                                threshold_r,
                                                ratio,
                                                gap,
                                                acceptance_ratio,
                                                leftovers,
                                                n)
    segments = segments +  RS.RANSAC_Segments_2D(left,
                                                threshold_r,
                                                ratio,
                                                gap,
                                                acceptance_ratio,
                                                leftovers,
                                                n)

    position = position + x_step


for s in segments:
    RS.plot_segment(s)
plt.gca().set_aspect("equal")
plt.title(datasets[test])
plt.show()