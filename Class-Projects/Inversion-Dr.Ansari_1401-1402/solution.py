
import numpy as np

# Define the function to integrate
def f(x):
    return (3*x**3) - (5*x**2) + (10*x) - 67

# Define the interval limits
a = -4
b = 6

# Number of random points to generate
n = 1000000

# Generate n random points uniformly within the interval [a, b]
random_points = np.random.uniform(a, b, n)

# Evaluate the function at the random points
function_values = f(random_points)

# Estimate the integral using the Monte Carlo method
integral_approximation = np.mean(function_values) * (b - a)

print("Approximate integral result:", integral_approximation)






####################################################################################

def func(x):
    return (3/4)*x**4 - (5/3)*x**3 + 5*x**2 - 67 *x

c = func(b) - func(a)

print(c)
