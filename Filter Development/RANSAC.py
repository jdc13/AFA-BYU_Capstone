'''This file contains (or will contain) functions to run the RANSAC algorithm on datasets'''

import numpy as np


def sort_points(data, index = 0):
    '''Sort a list of points (as numpy arrays) based on the x y or z coordinate \n
    Use 0 for x, 1 for y and 2 for z'''
    
    #If there is only one point left in the dataset, return the point
    if len(data) <= 1:
        return(data)
    
    #If there are multiple points in the dataset, sort them
    else:
        #cut the dataset into 2 equal, or nearly equal for an odd number of members, sets
        cut = int(len(data)/2)
        
        #Sort the two list using this function recursively
        set1 = sort_points(data[0:cut], index)
        set2 = sort_points(data[cut:len(data)], index)

        #empty list to place sorted data
        sorted = []

        #Since the datasets are presorted, we only need to compare the first two members of each set
        #append the smaller of the two sets to the sorted list, and remove it from its set
        #repeat this process until one of the lists is empty
        while len(set1)>0 and len(set2)>0:
            if(set1[0][index] < set2[0][index]):
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
