import random
import math
from multiprocessing import Pool

# Define the function that calculates y for a single value of x
def calculate_y(x):
    y = (x**2) + math.log(x) + x + 2
    return y

if __name__ == '__main__':
    # Create a Pool of worker processes
    with Pool() as p:
        # Generate 10000 random numbers
        random_numbers = [random.uniform(1, 100) for _ in range(100000000)]
        # Calculate y for each random number using parallel processing
        results = p.map(calculate_y, random_numbers)
    
    # Print the list of results
    #print(results)

