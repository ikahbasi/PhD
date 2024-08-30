import random
import torch

# Define the function that calculates y for a single value of x
def calculate_y(x):
    x_tensor = torch.tensor(x).cuda()
    y = (x_tensor**2) + torch.log(x_tensor) + x_tensor + 2
    return y.item()

if __name__ == '__main__':
    # Generate 10000 random numbers
    random_numbers = [random.uniform(1, 100) for _ in range(10000)]

    # Initialize CUDA
    if torch.cuda.is_available():
        device = torch.device('cuda')
        torch.backends.cudnn.benchmark = True
    else:
        device = torch.device('cpu')

    # Calculate y for each random number using GPU processing
    with torch.no_grad():
        results = [calculate_y(x) for x in random_numbers]

    # Print the list of results
    print(results)

