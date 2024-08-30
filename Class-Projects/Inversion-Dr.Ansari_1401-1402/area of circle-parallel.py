import numpy as np
import multiprocessing
import os

# Number of random points to generate
n = 1000000

# Number of processes to use for parallel processing
num_processes = 4

# Define the function for estimating pi using Monte Carlo
def estimate_pi(num_points, seed):
    """Estimate the value of pi using Monte Carlo"""
    np.random.seed(seed)
    random_points = np.random.uniform(-1, 1, size=(num_points, 2))
    points_inside_circle = np.sum(np.linalg.norm(random_points, axis=1) < 1)
    return points_inside_circle

if __name__ == '__main__':
    # Generate unique seeds for each process based on process ID (PID)
    seeds = np.random.randint(0, 999999, size=num_processes)
    
    # Create a multiprocessing Pool with specified number of processes
    pool = multiprocessing.Pool(num_processes)

    # Estimate pi using Monte Carlo in parallel
    results = pool.starmap(estimate_pi, [(n // num_processes, seed) for seed in seeds])
    print(results)
    # Close the multiprocessing Pool
    pool.close()
    pool.join()

    # Calculate the total number of points inside the circle
    total_points_inside_circle = sum(results)

    # Estimate the value of pi by multiplying the ratio of points inside the circle to total points by 4
    pi_approximation = 4 * total_points_inside_circle / n

    print("Approximate value of pi:", pi_approximation)
