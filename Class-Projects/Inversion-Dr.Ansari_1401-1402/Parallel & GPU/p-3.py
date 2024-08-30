import random
import math
from joblib import Parallel, delayed

# Define the function that calculates y for a single value of x
def calculate_y(x):
    y = (x**2) + math.log(x) + x + 2
    return y

if __name__ == '__main__':
    # Generate 10000 random numbers
    random_numbers = [random.uniform(1, 100) for _ in range(1000000)]

    # Calculate y for each random number using parallel processing
    results = Parallel(n_jobs=8)(delayed(calculate_y)(x) for x in random_numbers)

    # Print the list of results
    print(results)

