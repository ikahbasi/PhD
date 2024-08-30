#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 13:55:27 2023

@author: iman
"""

def PseudoInverse(matrix):
    U, S, VT = la.svd(matrix)
    S = np.diag(S)
    return VT.T @ la.inv(S) @ U.T

import numpy.linalg as la
import numpy as np

#a = np.arange(1, 10)
#b = a.reshape(3, 3)

b = np.array([[2, 4, 3],
              [3, 2, 1],
              [5, 2, 1]]
            )

#U, S, VT = la.svd(b)
#S = np.diag(S)
#
#print(f'{U=}')
#print(f'{S=}')
#print(f'{VT=}')


inv = la.inv(b)
inv_p = PseudoInverse(matrix=b)
inv_p2 = la.pinv(b)

print(inv)
print(inv_p.round(2))
print(inv_p2.round(2))