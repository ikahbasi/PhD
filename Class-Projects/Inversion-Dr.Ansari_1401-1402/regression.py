#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:12:47 2023

@author: iman
"""

import numpy as np

m = np.random.random(size=(10, 2))
m1 = np.arange(10)
# m = m1.reshape(-1, 2)
m = m/4 + m1.reshape(-1, 1)
print(m)


c = np.cov(m)
print(c.shape)

import matplotlib.pyplot as plt
plt.plot(m)
plt.show()
plt.imshow(c)

import numpy as np

# Create some example data
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])

# Construct the design matrix
G = np.vstack((x, np.ones(len(x)))).T

# Compute the coefficients using least squares
m = np.linalg.inv(G.T @ G) @ G.T @ y

# Print the results
print("Slope: ", m[0])
print("Intercept: ", m[1])



########################
m = x.size
part1 = 1 / (m*sum(x**2) - sum(x)**2)
part2 = np.array([[sum(x**2), -sum(x)],
                  [-sum(x), m]])
part3 = np.array([[sum(y)],
                  [sum(x*y)]])

print(part1*(part2 @ part3))