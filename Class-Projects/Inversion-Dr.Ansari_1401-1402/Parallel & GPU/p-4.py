import random
import math
import dask.array as da

# Define the function that calculates y for a single value of x
def calculate_y(x):
    y = (x**2) + math.log(x) + x + 2
    return y

if __name__ == '__main__':
    # Generate 10000 random numbers
    random_numbers = da.random.uniform(1, 100, size=(1000000,))

    # Calculate y for each random number using parallel processing
    results = calculate_y(random_numbers).compute(num_workers=4)

    # Print the list of results
    print(results)

