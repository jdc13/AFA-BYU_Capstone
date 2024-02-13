import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
fontprops = fm.FontProperties(size=12)

import pandas as pd

#Show walls in the CB as line segments
#Line segment format: [[x1, y1],[x2,y2]] (will need to transpose to plot)

def plot_wall(wall):
    plt.plot(wall.T[0], wall.T[1], color = "b")

def plot_door(door):
    plt.plot(door.T[0], door.T[1], color = "tab:brown")

def plot_other(other):
    plt.plot(other.T[0], other.T[1], color = "tab:orange")


class wall:
    def __init__(self, corner):
        self.corner = corner
    def update(self, delta):
        corner_old = self.corner
        self.corner = self.corner + np.array(delta)
        return np.array([corner_old, self.corner])       

trace_left = wall(np.array([0,0]))
walls = []
doors = []
other = []

#left side:
corner = [0,0]
walls.append(trace_left.update([0,13]))
doors.append(trace_left.update([0,3]))
walls.append(trace_left.update([0,30.5]))
doors.append(trace_left.update([0,7]))
walls.append(trace_left.update([0,15.8]))
# walls.append(trace_left.update([-2.5, 0]))
walls.append(trace_left.update([0, 43]))
# walls.append(trace_left.update([2.5,0]))
walls.append(trace_left.update([0,21]))
doors.append(trace_left.update([0,3]))
walls.append(trace_left.update([0,9]))
doors.append(trace_left.update([0,3]))
walls.append(trace_left.update([0,1]))
doors.append(trace_left.update([0,3]))
walls.append(trace_left.update([0,11]))
doors.append(trace_left.update([0,7]))
walls.append(trace_left.update([0,13]))
walls.append(trace_left.update([0,6.9]))
walls.append(trace_left.update([0,3.5]))
walls.append(trace_left.update([0,7.9]))
walls.append(trace_left.update([0,7]))
doors.append(trace_left.update([0,3]))
walls.append(trace_left.update([0,57]))
doors.append(trace_left.update([0,3]))
walls.append(trace_left.update([0,3]))
doors.append(trace_left.update([0,3]))
walls.append(trace_left.update([0,17]))

print(trace_left.corner)

#Right Side
trace_righta = wall(np.array([10.5,0]))

walls.append(trace_righta.update([0,17]))
doors.append(trace_righta.update([0,3]))
walls.append(trace_righta.update([-1.5,0]))
walls.append(trace_righta.update([0,1]))
doors.append(trace_righta.update([0,3]))
walls.append(trace_righta.update([0,22.5]))

#Hall 1
next_corner = trace_righta.corner + np.array([0, 11.5])
walls.append(trace_righta.update([30, 0]))

trace_rb = wall(next_corner)

walls.append(trace_rb.update([9.8,0]))
doors.append(trace_rb.update([7,0]))
walls.append(trace_rb.update([0,-2.5]))
walls.append(trace_rb.update([30-9.8-7,0]))

#Wall along path
trace_rc = wall(next_corner)
other.append(trace_rc.update([0,32.1]))
walls.append(trace_rc.update([0,8]))
doors.append(trace_rc.update([0,8]))
walls.append(trace_rc.update([0,32]))
doors.append(trace_rc.update([0,3]))
walls.append(trace_rc.update([0,19.5]))
other.append(trace_rc.update([0,32.1]))

#Hall 2
next_corner = trace_rc.corner + np.array([0,11.5])
walls.append(trace_rc.update([9.8,0]))
doors.append(trace_rc.update([7,0]))
walls.append(trace_rc.update([0,2.5]))
walls.append(trace_rc.update([30-9.8-7,0]))

trace_rd = wall(next_corner)

walls.append(trace_rd.update([2.5,0]))
doors.append(trace_rd.update([3,0]))
walls.append(trace_rd.update([30-2.5-3,0]))

#wall along path
trace_re = wall(next_corner)
walls.append(trace_re.update([0,37]))

#Hall 3
walls.append(trace_re.update([30,0]))

next_corner = trace_re.corner + np.array([0,9])
trace_rf = wall(next_corner)
walls.append(trace_rf.update([-30,0]))
walls.append(trace_rf.update([0,19]))
doors.append(trace_rf.update([0,3]))
walls.append(trace_rf.update([0,3.1]))
doors.append(trace_rf.update([0,4]))
print(trace_left.corner -trace_rf.corner)
walls.append(trace_rf.update([0,15.3]))




#Transformations into proper reference frame:
    # Translate 4.5 to the left
for i in range(len(walls)):
    walls[i] = walls[i] - np.array([4.5,0])

for i in range(len(doors)):
    doors[i] = doors[i] - np.array([4.5,0])

for i in range(len(other)):
    other[i] = other[i] - np.array([4.5,0])

    #rotate 90 degrees clockwise about the origin

for i in range(len(walls)):
    walls[i] = np.array([[walls[i][0][1], -1*walls[i][0][0]],
                         [walls[i][1][1], -1*walls[i][1][0]]])

for i in range(len(doors)):
    doors[i] = np.array([[doors[i][0][1], -1*doors[i][0][0]],
                         [doors[i][1][1], -1*doors[i][1][0]]])

for i in range(len(other)):
    other[i] = np.array([[other[i][0][1], -1*other[i][0][0]],
                         [other[i][1][1], -1*other[i][1][0]]])


#Convert mm measurements to inches on drawing
for i in range(len(walls)):
    walls[i] /= 25.4

for i in range(len(doors)):
    doors[i] /= 25.4

for i in range(len(other)):
    other[i] /= 25.4



#Scale based on drawing scale of 1" = 22' 8"
scale = 22*12 + 8

for i in range(len(walls)):
    walls[i] *= scale

for i in range(len(doors)):
    doors[i] *= scale

for i in range(len(other)):
    other[i] *= scale


#Convert inches to m

for i in range(len(walls)):
    walls[i] /= 39.37

for i in range(len(doors)):
    doors[i] /= 39.37

for i in range(len(other)):
    other[i] /= 39.37



# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)

# plt.plot([0,walls[-1][1][0]],[0,0], "--", color = "tab:cyan", label = "Path")
# plt.scatter(0,0, color = "k", label = "Start")
# plt.scatter(walls[-1][1][0],0, color = "tab:green", label = "Finish")





# plt.plot(walls[0].T[0], walls[0].T[1], color = "b", label = "Walls")

# plt.plot(doors[0].T[0], doors[0].T[1], color = "tab:brown", label = "Doors")

# plt.plot(other[0].T[0], other[0].T[1], color = "tab:orange", label = "Stairs, Chairs, etc.")


# for i in walls:
#     plot_wall(i)

# for i in doors:
#     plot_door(i)

# for i in other:
#     plot_other(i)


# # To equalize our aspect ratio
# ax.set_aspect('equal')
# ax.set_ylim([-10,30])


# plt.legend()

# scalebar = AnchoredSizeBar(ax.transData,
#                            10, '10 m', 'lower center', 
#                            pad=0.1,
#                            color='black',
#                            frameon=False,
#                            size_vertical=.5,
#                            fontproperties=fontprops)

# ax.add_artist(scalebar)

# plt.axis("off")
# plt.show()

# Convert lists of walls into a format that pandas can export
# walls_CSV = []
# for i in walls:
#     walls_CSV.append([i[0][0],i[0][1],i[1][0],i[1][1]])
# walls_DF = pd.DataFrame(walls_CSV)
# walls_DF.to_csv("hallway\walls.csv", index=False)

# doors_CSV = []
# for i in doors:
#     doors_CSV.append([i[0][0],i[0][1],i[1][0],i[1][1]])
# doors_DF = pd.DataFrame(doors_CSV)
# doors_DF.to_csv("hallway\doors.csv", index = False)

# other_CSV = []
# for i in other:
#     other_CSV.append([i[0][0],i[0][1],i[1][0],i[1][1]])
# other_DF = pd.DataFrame(other_CSV)
# other_DF.to_csv("hallway\other.csv", index = False)