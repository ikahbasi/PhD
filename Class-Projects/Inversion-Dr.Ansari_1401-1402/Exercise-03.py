#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 20:09:14 2023

@author: iman
"""
import numpy as np
import scipy.stats as stats


x = np.array([22, 24, 24, 30, 22, 20, 28, 30, 24, 34, 36, 15, 37])
x_bar = sum(x) / len(x)
n = len(x)
mu = 21
alpha = 0.01


s_square = sum((x-x_bar)**2) / (n-1)
s = np.sqrt(s_square)


sigma = s * (n-1) / n

z = (x_bar-mu) / s / np.sqrt(n)


p_exceed_critical_value = stats.t.ppf(alpha, degree_of_freedom)


from scipy.stats import norm
value = norm.ppf(p)
print(value)

# Student t-distribution Percent Point Function
from scipy.stats import t
# define probability
p = 0.95
df = 10
# retrieve value <= probability
value = t.ppf(p, df)
print(value)
# confirm with cdf
p = t.cdf(value, df)
print(p)