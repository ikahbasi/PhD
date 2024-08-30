import numpy as np
import scipy.stats as stats

n1 = 40
x1_bar = 9.1
s1 = 1.9

n2 = 50
x2_bar = 8.0
s2 = 2.1

alpha = 0.05


z = (x1_bar-x2_bar) / np.sqrt((s1**2/n1)+(s2**2/n2))
print(f'Z: {z:.4}')


degree_of_freedom = (n1-1) + (n2-1)
print('Degree of freedom:', degree_of_freedom)



p_exceed_critical_value = stats.t.ppf(alpha/2, degree_of_freedom)
print('Probability of exceeding the critical value:', p_exceed_critical_value)

if z < abs(p_exceed_critical_value):
    print('Retained')
else:
    print('reject')