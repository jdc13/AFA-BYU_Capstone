import matplotlib.pyplot as plt
import numpy as np
line = "1,2,3@4,5,6@7,8,9@10,11,12@"

print(line)
line = line.split("@")[0:-1]
print(line)
points = []
for i in range(len(line)):
    points.append([float(j) for j in line[i].split(",")])
print(points)
plt.scatter(np.array(points)[:,0],np.array(points)[:,1])
plt.show()
# print(points[:][0])
# plt.scatter(points[:][0],points[:][1])
# plt.figure(2)
# plt.scatter(points[0][:], points[1][:])
# plt.show()



