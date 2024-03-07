'''This file contains (or will contain) functions to run the RANSAC algorithm on datasets'''

import numpy as np
import matplotlib.pyplot as plt
import random
import warnings

warnings.simplefilter('ignore', np.RankWarning) #RANSAC keeps triggering warnings from numpy's polyfit program. They are usually resolved after the 2nd iteration.


def plot_segment(segment):
    '''Function to plot the line segments'''
    plt.plot(segment.T[0], segment.T[1], color = "k")

def sort_points(data, index = 0):
    '''Sort a list of points (as numpy arrays) based on the x y or z coordinate \n
    data: Data to sort, list of 2 or 3 member numpy arrays\n
    index: Use 0 for x, 1 for y and 2 for z'''
    
    #If there is only one point left in the dataset, return the point
    if len(data) <= 1:
        return(data)
    
    #If there are multiple points in the dataset, sort them
    else:
        #Find the index required to cut the data into 2 equal or nearly equal sets
        cut = int(len(data)/2)
        
        #Cut and sort the two list using this function recursively
        set1 = sort_points(data[0:cut], index)
        set2 = sort_points(data[cut:len(data)], index)

        #empty list to place sorted data
        sorted = []

        #Since the datasets are presorted, we only need to compare the first two members of each set
        #append the smaller of the two sets to the sorted list, and remove it from its set
        #repeat this process until one of the lists is empty
        while len(set1)>0 and len(set2)>0:
            if(set1[0].item(index) < set2[0].item(index)):
                sorted.append(set1.pop(0))
            else:
                sorted.append(set2.pop(0))

        #Once one of the lists is empty, we know that the remaining set just needs to be appended. 
        #We can do this in 1 line of code since we removed the data from the sets as they were sorted. 
        #Adding an empty list to a list in python has no effect.
        sorted = sorted + set1 + set2

        #Return the sorted data to either to repeat the above loop, or to the program
        return(sorted)


    

    #Test code for this function. Uncomment and unindent to run.

    # test_data = [np.array([1,2,3]), 
    #              np.array([0,7,0]), 
    #              np.array([4,2,2]), 
    #              np.array([2,3,90]),
    #              np.array([7,5,9])]


    # print("\n\n", sort_points(test_data, 0))


def RANSAC_basic_2D(RANSAC_points, threshold, ratio, acceptance_ratio = .5):
    '''Run Random Sample Consensus on a set of data points\n
    This function will only return 1 regressed line, along with the inliers and outliers\n
    RANSAC_points: A list of numpy arrays in the form [[x1,y1],[x2,y2]...]\n
    threshold: Maximum distance allowed between datapoints and the regressed line in defining new inliers\n
    ratio: number of points in the inlier vs the outlier group\n
    acceptance_ratio: minimum ratio of inliers/outliers required to accept the line'''
    
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
        

        if len(inliers) > len(outliers)*acceptance_ratio:
            #if there are a significant number of inliers, accept the segment
            return a, inliers, outliers
        
    #if time out
    #will need to address this error case in final version of code
    TimeoutError
        
def RANSAC_Segments_2D(RANSAC_points, threshold, ratio, gap, acceptance_ratio = .5, leftovers = 20):
    ''''Run Random Sample Consensus on a set of data points, and extract line segments\n
    This function will return a list of line segments in the form [array([[x1, y1],[x2, y2]]),...]\n
    RANSAC_points: A list of numpy arrays in the form [array([x1,y1]),array([x2,y2])...]\n
    threshold: Maximum distance allowed between datapoints and the regressed line in defining new inliers\n
    ratio: number of points in the inlier vs the outlier group in the initla iteration\n
    gap: distance between points that is considered a gap\n
    acceptance_ratio: minimum ratio of inliers/outliers required to accept the line\n
    leftovers: The maximum number of outliers in the final iteration. A set of outliers larger than this number will triger a loop'''
    segments = [] #list to store the line segments
    while(len(RANSAC_points) > leftovers):
        #Run RANSAC 
        a, inliers, RANSAC_points = RANSAC_basic_2D(RANSAC_points, 
                                                    threshold, 
                                                    ratio, 
                                                    acceptance_ratio)
        
        
        #Sort the inlier group based on x values for shallow slopes, and y values for steep slopes
        if(abs(a[1])<2):
            index = 0
        else:
            index = 1
        inliers = sort_points(inliers, index)

        wall = True #boolean to track whether or not we are in a wall
        #Search the inlier group for gaps along the index that was used for sorting
        start = inliers[0][0]
        for i in range(len(inliers)-2):
            
            if inliers[i+1][index] - inliers[i][index] > gap: #When a gap is found
                if wall: #If we are tracking a wall:
                    #save the segment
                    segments.append(np.array([[start,            a[0]*start + a[1]],
                                               [inliers[i][0],    a[0]*inliers[i][0]+a[1]]])
                                    )
                    #stop tracking a wall
                    wall = False
                
                else: #Tracking a gap
                    #Check the next point to make sure this measurement isn't noise in the data
                    if not(inliers[i+2][index] - inliers[i+1][index] > gap): #There is data close after this point
                        wall = True #Start tracking a wall
                        start = inliers[i][0] #Save the start of the wall
        
        segments.append(np.array([[start,            a[0]*start + a[1]],
                                     [inliers[-1][0],    a[0]*inliers[-1][0]+a[1]]])
                        )
        
    return(segments)




                    

