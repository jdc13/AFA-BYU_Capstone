from sklearn.linear_model import RANSACRegressor
from sklearn.datasets import make_regression
import matplotlib.pyplot as plt
import numpy as np
X, y = make_regression(
    n_samples=200, n_features=2, noise=4.0, random_state=0)
reg = RANSACRegressor(random_state=0).fit(X, y)
reg.score(X, y)
reg.predict(X[:1])
X = np.array(X)
print(X[1][0])
# plt.scatter(X[:0], X[:1])


plt.show()
