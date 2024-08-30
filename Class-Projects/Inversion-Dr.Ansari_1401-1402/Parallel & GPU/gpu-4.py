import random
import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import numpy as np

# Define the CUDA kernel that calculates y for a single value of x
cuda_kernel = """
__global__ void calculate_y(float *x, float *y) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    y[tid] = (x[tid]*x[tid]) + log(x[tid]) + x[tid] + 2;
}
"""

# Compile the CUDA kernel
mod = SourceModule(cuda_kernel)

# Get a handle to the CUDA kernel function
calculate_y_gpu = mod.get_function("calculate_y")

if __name__ == '__main__':
    # Generate 10000 random numbers
    random_numbers = np.array([random.uniform(1, 100) for _ in range(10000)], dtype=np.float32)

    # Allocate memory on the GPU
    x_gpu = drv.mem_alloc(random_numbers.nbytes)
    y_gpu = drv.mem_alloc(random_numbers.nbytes)

    # Copy the data to the GPU
    drv.memcpy_htod(x_gpu, random_numbers)

    # Calculate y for each random number using PyCUDA on the GPU
    block_size = 128
    num_blocks = (random_numbers.size + block_size - 1) // block_size
    calculate_y_gpu(x_gpu, y_gpu, block=(block_size, 1, 1), grid=(num_blocks, 1, 1))

    # Copy the results back to the CPU
    results = np.empty_like(random_numbers)
    drv.memcpy_dtoh(results, y_gpu)

    # Print the list of results
    print(results)

