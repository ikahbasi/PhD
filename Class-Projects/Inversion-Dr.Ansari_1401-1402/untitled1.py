#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 08:44:41 2023

@author: iman
"""

# Listing 1

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import math as mt
from numpy import linalg as LA
from mpl_toolkits.mplot3d import Axes3D

#%matplotlib inline

x=np.array([1,0]) # Original vector
theta = 30 * mt.pi / 180 # 30 degress in radian
A = np.array([[np.cos(theta), -np.sin(theta)],
               [np.sin(theta), np.cos(theta)]]) # Rotation
B = np.array([[3,0],[0,1]]) # Stretching matrix
Ax = A @ x # Ax is the rotated vector
Bx = B @ x # Bx is the stretched vector



xi1 = np.linspace(-1.0, 1.0, 100)
xi2 = np.linspace(1.0, -1.0, 100)
yi1 = np.sqrt(1 - xi1**2)
yi2 = -np.sqrt(1 - xi2**2)
xi = np.concatenate((xi1, xi2),axis=0)
yi = np.concatenate((yi1, yi2),axis=0)
plt.plot(xi, yi)

x = np.vstack((xi, yi))
A = np.array([[3, 2],
              [0, 2]])

t = A @ x

plt.plot(x[0, :], x[1, :])
plt.plot(t[0, :], t[1, :])
ax = plt.gca()
ax.set_aspect('equal', 'box')
plt.grid()






B = np.array([[-1, 1],[0, -2]])
lam, u = LA.eig(B)
print("lam=", np.round(lam, 4))
print("u=", np.round(u, 4))