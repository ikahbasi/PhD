import random
import math
import concurrent.futures

# Define the function that calculates y for a single value of x
def calculate_y(x):
    y = (x**2) + math.log(x) + x + 2
    return y

if __name__ == '__main__':
    # Generate 10000 random numbers
    random_numbers = [random.uniform(1, 100) for _ in range(1000000)]

    # Create a ThreadPoolExecutor with 4 threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Calculate y for each random number using parallel processing
        results = list(executor.map(calculate_y, random_numbers))

    # Print the list of results
    print(results)

