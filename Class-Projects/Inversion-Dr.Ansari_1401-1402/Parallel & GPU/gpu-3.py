import random
import cupy as cp

# Define the function that calculates y for a single value of x
def calculate_y(x):
    x_array = cp.array(x)
    y = (x_array**2) + cp.log(x_array) + x_array + 2
    return y.get()

if __name__ == '__main__':
    # Generate 10000 random numbers
    random_numbers = [random.uniform(1, 100) for _ in range(10000)]

    # Calculate y for each random number using CuPy on the GPU
    with cp.cuda.Device(0):
        results = [calculate_y(x) for x in random_numbers]

    # Print the list of results
    print(results)

