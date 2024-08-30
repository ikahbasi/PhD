import random
import tensorflow as tf

# Define the function that calculates y for a single value of x
@tf.function
def calculate_y(x):
    return (x**2) + tf.math.log(x) + x + 2

if __name__ == '__main__':
    # Generate 10000 random numbers
    random_numbers = [random.uniform(1, 100) for _ in range(10000)]

    # Calculate y for each random number using TensorFlow on the GPU
    with tf.device('/GPU:0'):
        results = [calculate_y(x).numpy() for x in random_numbers]

    # Print the list of results
    print(results)

