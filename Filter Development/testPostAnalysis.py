import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

import RANSAC as RS


test = " 4-6-2024 11-47-42"

test_dir = os.getcwd() + "\\Tests\\"


segments = pd.read_csv(test_dir  + test + "\\Segments.csv")

# points = pd.read_csv(test_dir + test + "\\Points.csv")

for i in range(len(segments)):
    print()
    segment = segments.loc[i]
    if segment["x1"] < 400:
        s = np.array([[segment["x1"], segment["y1"]],
                    [segment["x2"], segment["y2"]]])
        RS.plot_segment(s)

plt.show()
