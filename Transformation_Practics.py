import numpy as np
import matplotlib.pyplot as plt

theta = 10*np.pi/180 *-1 #random angle multiply by negative to corect which axis is being measured from
Delta = [10,5] #random translation

# Refference frame rotation
R = np.array([[np.cos(theta), -1*np.sin(theta)],
              [np.sin(theta), np.cos(theta)]])

x = np.array([-5,-5]) #random point
# x = np.array([np.linspace)

ax = plt.subplot(1, 1, 1)
#plot coordinate systems
plt.scatter(x[0],x[1])
#point in first frame

xaxis = np.array([[-10,10],[0,0]])
plt.plot(xaxis[0], xaxis[1], "--", color = "r", )
xaxis = R@xaxis
xaxis[0] = xaxis[0]-Delta[0]
xaxis[1] = xaxis[1]-Delta[1]

yaxis = np.array([[0, 0],[-10, 10]])
plt.plot(yaxis[0], yaxis[1], "--", color = "r", )

yaxis = R@yaxis
yaxis[0] = yaxis[0]-Delta[0]
yaxis[1] = yaxis[1]-Delta[1]





plt.plot(xaxis[0], xaxis[1], "--", color = "k", )
plt.plot(yaxis[0], yaxis[1], "--", color = "k", )

R_point = R

# R_point = np.array([[np.cos(-theta), -1*np.sin(-theta)],
#                     [np.sin(-theta), np.cos(-theta)]])


#Small angle approximation
R_point = np.array([[1, -theta],
                    [theta, 1]])

p = R_point.T@(x+Delta)
# p = R_point@x + Delta
plt.grid("on")

plt.figure(2)
plt.grid("on")
plt.axis("on")

plt.scatter(p[0], p[1])

ax.set_aspect("equal")
plt.grid("on")
plt.show()
