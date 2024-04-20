speed = 15
threshold_r = .04            #.5m          Threshold used to define inliers
ratio = .8                  #.8            Initial ratio of inliers to outliers in the data
gap = .5                    #1m            Standard deviation of distance between n points to characterize a gap
acceptance_ratio = .7       #.5            min Number of inliers/outliers to accept a line
leftovers = 0             #40             Maximum number of outliers in the final iteration
x_step = speed               #10m            How much to increment the RANSAC window
n = 4                      #4             How many points to evaluate when trying to find a gap

loosen_threshold = .1
loosen_ratio = .05