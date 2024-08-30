import random
import math

# Create an empty list to store the results
results = []

# Generate 10000 random numbers
for i in range(10000):
    # Generate a random number between 1 and 100
    x = random.uniform(1, 100)
    # Calculate the value of y using the formula given
    y = (x**2) + math.log(x) + x + 2
    # Add the result to the list
    results.append(y)

# Print the list of results
print(results)

