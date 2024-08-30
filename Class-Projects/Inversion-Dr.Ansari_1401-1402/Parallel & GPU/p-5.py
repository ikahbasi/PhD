import random
import math
import ray

# Define the function that calculates y for a single value of x
@ray.remote
def calculate_y(x):
    y = (x**2) + math.log(x) + x + 2
    return y

if __name__ == '__main__':
    # Initialize Ray
    ray.init(num_cpus=4)

    # Generate 10000 random numbers
    random_numbers = [random.uniform(1, 100) for _ in range(1000000)]

    # Calculate y for each random number using parallel processing
    results = ray.get([calculate_y.remote(x) for x in random_numbers])

    # Print the list of results
    print(results)


